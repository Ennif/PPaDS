import fei.ppds as fp
from fei.ppds import Mutex
from fei.ppds import Semaphore


class Lightswitch:
    def __init__(self):
        self.counter = 0
        self.mutex = Mutex()
        self.semaphore = Semaphore(1)

    def lock(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == 1:
            self.semaphore.wait()
        self.mutex.unlock()

    def unlock(self):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            self.semaphore.signal()
        self.mutex.unlock()


ls = Lightswitch()
