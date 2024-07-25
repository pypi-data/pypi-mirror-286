import errno
import multiprocessing
import queue
import socket
import sys
import threading
import time
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Any, Callable
import requests
from serialization_utils import CompressSerializer


def _find(func: Callable, try_ports: list[int] = None, exclude_ports: list[int] = None,
          try_range: tuple[int, int] = None) -> int | None:
    ports = (try_ports or []) + list(range(*try_range))
    exclude_ports = exclude_ports or []
    for port in ports:
        if port not in exclude_ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    result = func(s, port)
                    if result is not None:
                        return result
            except socket.error:
                continue


def find_running_port(host: str = '127.0.0.1', try_ports: list[int] = None, exclude_ports: list[int] = None,
                      try_range: tuple[int, int] = None, timeout: float = 0.5) -> int | None:
    def _test(s: socket.socket, port: int):
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        if result == 0:
            return port

    return _find(_test, try_ports, exclude_ports, try_range)


def find_free_port(host: str = '127.0.0.1', try_ports: list[int] = None, exclude_ports: list[int] = None,
                   try_range: tuple[int, int] = (1024, 65536)) -> int | None:
    def _test(s: socket.socket, port: int):
        s.bind((host, port))
        return port

    return _find(_test, try_ports, exclude_ports, try_range)


class ClientSocket:
    def __init__(self, host: str = '127.0.0.1', port: int = 12345, client_socket: socket.socket = None,
                 client_host: str = None, client_port: int = 12345):
        self.host = host
        self.port = port
        self.client_host = client_host
        self.client_port = client_port
        self.client_socket = client_socket

        self._length_bytes = 5

        if self.client_socket:
            self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 32 * 1024 * 1024)

    def connect(self) -> None:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 32 * 1024 * 1024)
        # use the certain address of the client to connect the server
        if self.client_host and self.client_port:
            self.client_socket.bind((self.client_host, self.client_port))
        self.client_socket.connect((self.host, self.port))

    def _get_length(self, data: bytes) -> bytes:
        # for 5 bytes unsigned int, the max data length is 2**40 - 1, namely about 1tb
        bytes_result = len(data).to_bytes(self._length_bytes, byteorder='big')
        return bytes_result

    def _recv_length(self) -> int:
        byte_result = self.client_socket.recv(self._length_bytes)
        return int.from_bytes(byte_result, byteorder='big')

    def send(self, data: bytes):
        return self.client_socket.sendall(self._get_length(data) + data)

    def recv(self) -> bytes:
        length = self._recv_length()
        data = bytearray()
        while len(data) < length:
            data += self.client_socket.recv(length - len(data))
        return bytes(data)

    def recvf(self, output_path: str | Path, bufsize: int = 1024 * 1024 * 16) -> None:
        with open(output_path, 'wb') as f:
            while True:
                data = self.client_socket.recv(bufsize)
                if not data:
                    break
                f.write(data)

    def sendf(self, input_path: str | Path, bufsize: int = 1024 * 1024 * 16) -> None:
        with open(input_path, 'rb') as f:
            while True:
                data = f.read(bufsize)
                if not data:
                    break
                self.client_socket.send(data)

    def close(self) -> None:
        return self.client_socket.close()


class ServerSocket:
    def __init__(self, host: str = '127.0.0.1', port: int = 12345, backlog: int = 64):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(backlog)
        self.server_socket.setblocking(False)

    def accept(self) -> tuple[ClientSocket, Any] | tuple[None, None]:
        while True:
            try:
                client_socket, addr = self.server_socket.accept()
                return ClientSocket(client_socket=client_socket), addr
            except socket.error as e:
                if e.errno == errno.EWOULDBLOCK or e.errno == errno.EAGAIN:
                    time.sleep(0.01)
                    continue
                elif e.errno == errno.EBADF:
                    return None, None
                else:
                    raise e

    def handle(self, handler: Callable, *args, **kwargs) -> None:
        def _handle():
            while True:
                client_socket, addr = self.accept()
                if not (client_socket and addr):
                    break
                handle_thread = threading.Thread(target=handler, args=(client_socket, addr, *args), kwargs=kwargs)
                handle_thread.daemon = True
                handle_thread.start()

        threading.Thread(target=_handle).start()

    def close(self) -> None:
        self.server_socket.close()


class MpHttpError(Exception):
    def __init__(self, *args, traceback_info: str = ''):
        super().__init__(*args)
        self.traceback_info = traceback_info

    def __str__(self):
        return self.traceback_info
    __repr__ = __str__


class MpHttpServer:
    _PROCESS_ID = '_process_id'

    def __init__(self, host: str = '0.0.0.0', port: int = 80, workers: int = 1, timeout: int = 3600,
                 show_info: bool = True, compress_threshold: int = 1024 * 128):
        self.host, self.port, self.workers, self.timeout, self.show_info = host, port, workers, timeout, show_info
        self.compress_threshold = compress_threshold
        self._process_id = 0
        self._lock = multiprocessing.Lock()
        self._s = CompressSerializer(threshold=self.compress_threshold)
        self._result_dict = multiprocessing.Manager().dict()
        self._req_que = multiprocessing.Queue()
        self._closed_flag = multiprocessing.Value('b', False)

    class _RequestHandler(BaseHTTPRequestHandler):
        def __init__(self, s: 'MpHttpServer', *args, **kwargs):
            self.s = s
            super().__init__(*args, **kwargs)

        def log_request(self, code="-", size="-"):
            pass

        def log_message(self, format, *args):
            if self.s.show_info:
                super().log_message(format, *args)

        def _fetch_result(self, process_id: int) -> dict:
            t_start = time.time()
            while time.time() - t_start < self.s.timeout:
                if self.s._result_dict.get(process_id) is not None:
                    return self.s._result_dict.pop(process_id)
                time.sleep(0.01)

        def _put_data(self, data: Any) -> list:
            process_ids = []
            for sub_data in data:
                with self.s._lock:
                    sub_data = {'data': sub_data, MpHttpServer._PROCESS_ID: self.s._process_id}
                    process_ids.append(self.s._process_id)
                    self.s._process_id += 1
                self.s._req_que.put(sub_data)
            return process_ids

        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = self.s._s.load_pickle(post_data)

            process_ids = self._put_data(data)
            results = [self._fetch_result(process_id) for process_id in process_ids]

            response = self.s._s.dump_pickle(results)
            self.log_message('"%s" %s %s %s', self.requestline, '200',
                             str(len(response)), str(self.client_address))
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Length', str(len(response)))
            self.end_headers()
            self.wfile.write(response)

    @staticmethod
    def get_data(req_que: multiprocessing.Queue) -> dict | None:
        try:
            data = req_que.get(timeout=0.5)
        except queue.Empty:
            return None
        return data

    @staticmethod
    def put_result(result: Any, result_dict, data) -> None:
        result_dict[data[MpHttpServer._PROCESS_ID]] = result

    @staticmethod
    def put_error(result_dict, data) -> None:
        result_dict[data[MpHttpServer._PROCESS_ID]] = MpHttpError(traceback_info=traceback.format_exc())

    def init(self) -> None: ...

    def main_loop(self, data: Any) -> Any:
        return data

    def main_process(self, req_que: multiprocessing.Queue, result_dict) -> None:
        self.init()
        while True:
            data = self.get_data(req_que)
            if data is None:
                if self._closed_flag.value:
                    break
                continue
            try:
                result = self.main_loop(data['data'])
                self.put_result(result, result_dict, data)
            except Exception:
                self.put_error(result_dict, data)

    def _start_processes(self):
        for _ in range(self.workers):
            multiprocessing.Process(target=self.main_process, args=(self._req_que, self._result_dict)).start()

    def run_server(self):
        self._start_processes()
        self._httpd = HTTPServer((self.host, self.port),
                           lambda *args, **kwargs: self._RequestHandler(self, *args, **kwargs))
        if self.show_info:
            sys.stderr.write(f"Starting server on port {self.port}...\n")
        self._httpd.serve_forever()

    def close_server(self):
        self._closed_flag.value = True
        self._httpd.shutdown()
        self._httpd.server_close()


class MpHttpClient:
    def __init__(self, host: str = '127.0.0.1', port: int = 80, compress_threshold: int = 1024 * 128):
        self.host, self.port, self.compress_threshold = host, port, compress_threshold
        self._s = CompressSerializer(threshold=self.compress_threshold)

    def batch(self, data_list: list | tuple, compress: bool = None) -> list[Any]:
        data = self._s.dump_pickle(data_list, compress=compress)
        resp = requests.post(f'http://{self.host}:{self.port}', data=data)
        return self._s.load_pickle(resp.content)

    def get(self, data: Any, compress: bool = None) -> Any:
        return MpHttpClient.batch(self, [data], compress=compress)[0]
