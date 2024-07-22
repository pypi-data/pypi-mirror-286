from time import sleep

from mciwb.imports import Monitor


def test_single_use(mock_client):
    def test_func():
        nonlocal count
        count += 1

    count = 0
    time = 0

    mon = Monitor(test_func, once=True)
    while mon._polling:
        sleep(0.1)
        time += 1
        if time > 10:
            break

    assert count == 1


def test_multiple_use(mock_client):
    def test_func():
        nonlocal count
        count += 1

    count = 0
    time = 0

    mon = Monitor(test_func, poll_rate=0.0001)
    while count < 100:
        sleep(0.1)
        time += 1
        if time > 10:
            break

    mon.remove_poller_func(test_func)

    Monitor.stop_all()

    assert count >= 100
