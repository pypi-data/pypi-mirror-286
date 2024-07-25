import io
import json
import lzma
import pickle
import yaml
import re
import zlib
from pathlib import Path
from types import ModuleType
from typing import Any


class Compressor:
    LZMA = 'lzma'
    ZLIB = 'zlib'

    def __init__(self, lib: str = ZLIB, encoding: str = 'utf-8'):
        self.lib = lib
        self.encoding = encoding

    def compress(self, data: bytes, lib: str = '') -> bytes:
        lib = lib or self.lib
        compressed_data = globals()[lib].compress(data)
        return compressed_data

    def decompress(self, compressed_data: bytes, lib: str = '') -> bytes:
        lib = lib or self.lib
        data = globals()[lib].decompress(compressed_data)
        return data


def _check_int_or_float(input_str: str) -> type:
    int_pattern = r'^[-+]?\d+$'
    float_pattern = r'^[-+]?\d+(\.\d+)?$'

    if re.match(int_pattern, input_str):
        return int
    elif re.match(float_pattern, input_str):
        return float
    else:
        return str


def _convert_json_dict_key_to_number(data: Any) -> Any:
    if isinstance(data, dict):
        # if data type is dict, convert it
        converted_dict = {}
        for key, value in data.items():
            if type(key) == str:
                trans_type = _check_int_or_float(key)
                key = trans_type(key)
            # process the values in dict, using recursion
            value = _convert_json_dict_key_to_number(value)
            converted_dict[key] = value
        return converted_dict
    elif isinstance(data, (list, tuple, set)):
        # if date type is list, tuple or set, process it recursively
        converted_list = []
        for item in data:
            converted_item = _convert_json_dict_key_to_number(item)
            converted_list.append(converted_item)
        return type(data)(converted_list)
    else:
        # if it's other type, don't process
        return data


def _get_empty_data_structure(data_type: type | None) -> dict | list | tuple | set | None:
    if data_type is None:
        return None
    types = (dict, list, tuple, set)
    if data_type in types:
        return data_type()
    else:
        raise TypeError(f"Unsupported data type {data_type}")


class Serializer:
    def __init__(self, path: str | Path = None, encoding: str = 'utf-8', data_type: type = None):
        self.path, self.encoding, self.data_type = path, encoding, data_type

    def _load(self, lib: ModuleType, data: str | bytes = None) -> Any:
        if not data:
            try:
                if lib in [json, yaml]:
                    data = Path(self.path).read_text(encoding=self.encoding)
                else:
                    data = Path(self.path).read_bytes()
            except FileNotFoundError:  # when file not found
                return _get_empty_data_structure(self.data_type)
        if lib is json:
            try:
                deserialized_data = json.loads(data)
            except json.decoder.JSONDecodeError:  # when file is empty
                return _get_empty_data_structure(self.data_type)
        elif lib is yaml:
            deserialized_data = yaml.safe_load(data)
        elif lib is pickle:
            try:
                deserialized_data = pickle.loads(data)
            except EOFError:  # when file is empty
                return _get_empty_data_structure(self.data_type)
        else:
            raise AssertionError
        return deserialized_data

    def load_yaml(self, data: str = None) -> Any:
        return self._load(yaml, data=data)

    def load_json(self, data: str = None, trans_key_to_num: bool = False) -> Any:
        json_data = self._load(json, data=data)
        if trans_key_to_num:
            return _convert_json_dict_key_to_number(json_data)
        return json_data

    def load_pickle(self, data: bytes = None) -> Any:
        return self._load(pickle, data=data)

    def _dump(self, data: bytes | str) -> bytes | str:
        if self.path:
            if isinstance(data, str):
                data = data.encode(encoding=self.encoding)
            Path(self.path).write_bytes(data)
        return data

    def dump_yaml(self, data: Any, allow_unicode: bool = True) -> str:
        string_io = io.StringIO()
        yaml.dump(data, string_io, allow_unicode=allow_unicode)
        data = string_io.getvalue()
        return self._dump(data)

    def dump_json(self, data: Any, indent: int = 4, ensure_ascii: bool = False, minimum: bool = True) -> str:
        kwargs = {'ensure_ascii': ensure_ascii}
        if minimum:
            kwargs['separators'] = (',', ':')
        else:
            kwargs['indent'] = indent
        data = json.dumps(data, **kwargs)
        return self._dump(data)

    def dump_pickle(self, data: Any) -> bytes:
        data = pickle.dumps(data)
        return self._dump(data)


class CompressSerializer:
    _UNCOMPRESSED = b'0'
    _COMPRESSED = b'1'
    _ZLIB = b'0'
    _LZMA = b'1'

    def __init__(self, compress_lib: str = Compressor.ZLIB, threshold: int = 1024 * 128):
        """When threshold is greater than 0 and less than the data length, will enable compression"""
        self.threshold, self.compress_lib = threshold, compress_lib
        self._c = Compressor(compress_lib)
        self._s = Serializer()

    def load_pickle(self, data: Any) -> Any:
        compressed = chr(data[0]).encode('utf-8')
        compress_lib = chr(data[1]).encode('utf-8')
        data = data[2:]
        if compressed == self._COMPRESSED:
            compressed = True
        else:
            compressed = False
        if compress_lib == self._ZLIB:
            compress_lib = Compressor.ZLIB
        elif compress_lib == self._LZMA:
            compress_lib = Compressor.LZMA
        else:
            raise AssertionError
        if compressed:
            data = self._c.decompress(data, lib=compress_lib)
        return self._s.load_pickle(data)

    def dump_pickle(self, data: Any, compress: bool = None) -> bytes:
        data = self._s.dump_pickle(data)
        if compress is None and (0 < self.threshold < len(data)):
            compress = True
        else:
            compress = compress or False
        if compress:
            data = self._c.compress(data)

        if self.compress_lib == Compressor.ZLIB:
            meta_data = self._ZLIB
        elif self.compress_lib == Compressor.LZMA:
            meta_data = self._LZMA
        else:
            raise AssertionError
        if compress:
            meta_data = self._COMPRESSED + meta_data
        else:
            meta_data = self._UNCOMPRESSED + meta_data
        return meta_data + data
