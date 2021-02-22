import fei.ppds as fp
from fei.ppds import Mutex


class Shared():
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.array = [0] * self.end
        self.mutex = Mutex()


class Histogram(dict):
    """
        Pouzity program z cvicenia PPaDS
    """
    def __init__(self, seq=[]):
        for item in seq:
            self[item] = self.get(item, 0) + 1


def counter_first_mutex(shared):
    while True:
        if shared.counter >= shared.end:
            break
        shared.mutex.lock()
        shared.counter += 1
        shared.mutex.unlock()
        shared.array[shared.counter] += 1


def counter_second_mutex(shared):
    while True:
        shared.mutex.lock()
        if shared.counter >= shared.end:
            break
        shared.array[shared.counter] += 1
        shared.counter += 1
        shared.mutex.unlock()


def counter_third_mutex(shared):
    while True:
        shared.mutex.lock()
        if shared.counter >= shared.end:
            shared.mutex.unlock()
            break
        shared.array[shared.counter] += 1
        shared.counter += 1
        shared.mutex.unlock()


for _ in range(10):
    shared_object = Shared(1_000_000)

    first_thread = fp.Thread(counter_third_mutex, shared_object)
    second_thread = fp.Thread(counter_third_mutex, shared_object)

    first_thread.join()
    second_thread.join()

    print(Histogram(shared_object.array))
