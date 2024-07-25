import random

if __name__ == '__main__':
    from __init__ import *
else:
    from . import *
from psplpyProject.psplpy.serialization_utils import *
from psplpyProject.psplpy.other_utils import PerfCounter


def tests():
    serializer = Serializer()
    compress_serializer = CompressSerializer(threshold=1)

    bench_data = {}
    rand_round = 10000
    for i in range(rand_round):
        bench_data[str(random.randint(0, rand_round))] = random.uniform(0, rand_round)

    p = PerfCounter()
    serialized_data = compress_serializer.dump_pickle(bench_data)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f}ms,\t compress')
    serialized_data = serializer.dump_pickle(bench_data)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f}ms,\t dumps_pickle')
    serialized_data = serializer.dump_json(bench_data)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f}ms,\t dumps_json')
    serialized_data = serializer.dump_yaml(bench_data)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f}ms,\t dumps_yaml')

    python_data = {1: '100', 2: 200, 3: ['你好', [3.14, None, False]]}

    dumps_data = compress_serializer.dump_pickle(python_data)
    print(dumps_data)
    loads_data = compress_serializer.load_pickle(dumps_data)
    assert loads_data == python_data, loads_data

    dumps_data = serializer.dump_json(python_data, ensure_ascii=False)
    loads_data = serializer.load_json(dumps_data, trans_key_to_num=True)
    assert dumps_data == '{"1":"100","2":200,"3":["你好",[3.14,null,false]]}', dumps_data
    assert loads_data == python_data

    dumps_data = serializer.dump_pickle(loads_data)
    loads_data = serializer.load_pickle(dumps_data)
    assert dumps_data == (b'\x80\x04\x95/\x00\x00\x00\x00\x00\x00\x00}\x94(K\x01\x8c\x03100\x94K\x02K\xc8K\x03]\x94('
                          b'\x8c\x06\xe4\xbd\xa0\xe5\xa5\xbd\x94]\x94(G@\t\x1e\xb8Q\xeb\x85\x1fN\x89eeu.'), loads_data
    assert loads_data == python_data

    dumps_data = serializer.dump_yaml(python_data)
    loads_data = serializer.load_yaml(dumps_data)
    assert dumps_data == "1: '100'\n2: 200\n3:\n- 你好\n- - 3.14\n  - null\n  - false\n", dumps_data
    assert loads_data == python_data

    serializer = Serializer(path=tmp_file, data_type=dict)
    loads_data = serializer.load_json()
    assert loads_data == dict(), loads_data

    serializer.dump_json(python_data)
    loads_data = serializer.load_json(trans_key_to_num=True)
    assert loads_data == python_data, loads_data

    serializer.dump_yaml(python_data)
    loads_data = serializer.load_yaml()
    assert loads_data == python_data, loads_data

    serializer.dump_pickle(python_data)
    loads_data = serializer.load_pickle()
    assert loads_data == python_data, loads_data

    tmp_file.unlink()


if __name__ == '__main__':
    tests()
