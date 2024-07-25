import time
from threading import Thread

if __name__ == '__main__':
    from __init__ import *
else:
    from . import *
from psplpyProject.psplpy.other_utils import *


def test_timeout_checker():
    def checker(timeout: float, unique_id: Any = None, check_time: float = None,
                func: str = 'ret_false', end_loop_time: float = 10000):
        t_start = time.time()
        while getattr(TimeoutChecker(timeout, unique_id=unique_id), func)():
            if time.time() - t_start > end_loop_time:
                break
            time.sleep(0.01)
        print(time.time() - t_start)
        assert int(time.time() - t_start) == check_time or timeout

    Thread(target=checker, kwargs={'timeout': 1, 'unique_id': 1}).start()
    timeout = 2
    Thread(target=checker, kwargs={'timeout': 2, 'unique_id': 2}).start()
    time.sleep(timeout + 0.5)

    kwargs = {'timeout': 2, 'unique_id': 1, 'check_time': 1, 'func': 'raise_err', 'end_loop_time': 1}
    Thread(target=checker, kwargs=kwargs).start()
    try:
        checker(timeout=1, unique_id=2, func='raise_err')
    except Exception as e:
        assert isinstance(e, TimeoutError)


def test_screenshot_maker():
    pass
    # ScreenShotMaker()


def test_perf_counter():
    p = PerfCounter()
    time.sleep(0.1)
    assert int(p.elapsed()) == int(0.1 * 1000)
    time.sleep(0.2)
    p.show('perf')


def tests():
    print('test other utils')
    assert is_sys(is_sys.LINUX) is True
    assert is_sys(is_sys.WINDOWS) is False

    data = [1, (2, [3, 4])]
    assert recursive_convert(data, to=list) == [1, [2, [3, 4]]]
    assert recursive_convert(data, to=tuple) == (1, (2, (3, 4)))

    assert get_env('SERVICE') == 'psplpy'

    test_timeout_checker()
    test_screenshot_maker()
    test_perf_counter()


if __name__ == '__main__':
    tests()
