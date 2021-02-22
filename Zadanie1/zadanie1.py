import fei.ppds as fp
from fei.ppds import Mutex


class Shared():
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.array = [0] * self.end
        self.mutex = Mutex()


def counter_first_mutex(shared):
    while True:
        if shared.counter >= shared.end:
            break
        shared.mutex.lock()
        shared.counter += 1
        shared.mutex.unlock()
        shared.array[shared.counter] += 1


for _ in range(10):
    shared_object = Shared(10000)

    first_thread = fp.Thread(counter_first_mutex, shared_object)
    second_thread = fp.Thread(counter_first_mutex, shared_object)

    first_thread.join()
    second_thread.join()

    print(shared_object.array)
