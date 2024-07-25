import datetime
import multiprocessing
import platform
import time
from abc import ABC, abstractmethod
from typing import Any, Type
import json
import os
from pathlib import Path
from PIL import ImageGrab


class FunctionClass(ABC):
    def __new__(cls, *args, **kwargs) -> Any:
        instance = super().__new__(cls)
        return instance(*args, **kwargs)

    @abstractmethod
    def __call__(self, *args, **kwargs): ...


class is_sys(FunctionClass):
    WINDOWS = 'Windows'
    LINUX = 'Linux'
    MACOS = 'Darwin'

    def __new__(cls, os_name: str) -> bool:
        return super().__new__(cls, os_name)

    def __call__(self, os_name: str) -> bool:
        this_os_name = platform.system()
        if os_name == this_os_name:
            return True
        return False


def recursive_convert(data: list | tuple, to: Type) -> tuple | list:
    """Recursively convert the lists and tuples are nested within each other to only tuples or lists"""
    if isinstance(data, (list, tuple)):
        return to(recursive_convert(item, to=to) for item in data)
    return data


class get_env(FunctionClass):
    ENV_FILE = '.env'

    @staticmethod
    def _parse_key_value() -> dict:
        result = {}
        lines = Path(get_env.ENV_FILE).read_text(encoding='utf-8').strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                key_value = line.split('=', maxsplit=2)
                result[key_value[0].strip()] = key_value[1].strip()
        return result

    def __new__(cls, env_name: str) -> Any:
        return super().__new__(cls, env_name)

    def __call__(self, env_name: str) -> Any:
        env = os.environ.get(env_name)
        try:
            return json.loads(env)
        except json.decoder.JSONDecodeError:
            return env
        except TypeError:
            for key_value in self._parse_key_value().items():
                os.environ[key_value[0]] = key_value[1]
            return get_env(env_name)


class PerfCounter:
    MS = 'ms'
    S = 's'
    close = False

    def __init__(self, unit: str = MS):
        if not self.close:
            self.unit = unit
            self.places = 7
            if self.unit == self.MS:
                self.places -= 3

            self._start = time.perf_counter()

    def refresh(self) -> None:
        if not self.close:
            self._start = time.perf_counter()

    def elapsed(self) -> float:
        if not self.close:
            elapsed = time.perf_counter() - self._start
            if self.unit == self.MS:
                elapsed = elapsed * 1000
            self.refresh()
            return elapsed
        return 0

    def show(self, tag: str = '') -> None:
        if not self.close:
            if tag:
                tag = tag + ': '
            print(f'{tag}{self.elapsed():.{self.places}f}ms')
            self.refresh()


class TimeoutChecker:
    instances = {}

    def __new__(cls, timeout_seconds: float, unique_id: Any = None):
        if unique_id in cls.instances:
            cls.instances[unique_id]['is_first_created'] = False
            return cls.instances[unique_id]['instance']
        else:
            instance = super().__new__(cls)
            cls.instances[unique_id] = {'instance': instance, 'is_first_created': True}
            return instance

    def __init__(self, timeout_seconds: float, unique_id: Any = None):
        """unique_id is required when two or more instances existing simultaneously, e.g. using threading"""
        self.unique_id = unique_id
        if self.instances[self.unique_id]['is_first_created']:
            self.timeout_seconds = timeout_seconds
            self.start_time = time.time()

    def _delete_instance(self):
        if self.unique_id in self.instances:
            del self.instances[self.unique_id]

    def ret_false(self) -> bool:
        current_time = time.time()
        if current_time - self.start_time > self.timeout_seconds:
            self._delete_instance()
            return False
        return True

    def raise_err(self, error_type: Type = None) -> bool:
        if not self.ret_false():
            if not error_type:
                message = (f'Start at {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.start_time))}, '
                           f'after {self.timeout_seconds}s time out')
                raise TimeoutError(message)
            raise error_type()
        return True


class ScreenShotMaker:
    def __init__(self, region: (int, int, int, int) = None, fps: float = 10, save_dir: str | Path = None,
                 show_info: bool = True, enable_warning: bool = True, savers_num: int = 10) -> None:
        self._region = region
        self._fps = fps
        self._interval = 1 / self._fps
        self._save_dir = Path(save_dir) if save_dir is not None else Path().cwd()
        self._save_dir = self._save_dir / f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")}'
        self._save_dir.mkdir(parents=True, exist_ok=True)
        self._show_info = show_info
        self._enable_warning = enable_warning
        self._savers_num = savers_num
        self._frame_counter = 0
        self._frame_queue = multiprocessing.Queue()

        self._start_savers()
        self._screenshot()

    def _warning(self, lag: float) -> None:
        if self._enable_warning and lag > self._interval:
            print(f'Warning - {datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")} - '
                  f'frame {self._frame_counter} - the lag is {lag:.3f}s')
        if self._enable_warning and self._frame_queue.qsize() > self._fps:
            print(f'Warning - {datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")} - '
                  f'frame {self._frame_counter} - the queue size is {self._frame_queue.qsize()}')

    @staticmethod
    def _timer(func):
        def wrapper(self, *args, **kwargs):
            t_start = time.perf_counter()
            while True:
                expected_time = t_start + self._frame_counter * self._interval
                current_time = time.perf_counter()
                lag = current_time - expected_time
                if current_time > expected_time:
                    self._warning(lag)
                    result = func(self, *args, **kwargs)
                    self._frame_queue.put({'time': current_time, 'result': result, 'counter': self._frame_counter})
                    self._frame_counter += 1
                else:
                    time.sleep(0.001)
        return wrapper

    @_timer
    def _screenshot(self):
        return ImageGrab.grab(self._region)

    def _saver(self, frame_queue: multiprocessing.Queue):
        while True:
            if not frame_queue.empty():
                frame = frame_queue.get()
                frame['result'].save(self._save_dir / f'{frame["time"]:.2f}.png')
                if self._show_info:
                    print(f'At {frame["time"]:.3f}, save frame {frame["counter"]}')
            else:
                time.sleep(0.01)

    def _start_savers(self):
        for _ in range(self._savers_num):
            multiprocessing.Process(target=self._saver, args=(self._frame_queue,)).start()
