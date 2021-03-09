import fei.ppds as fp
from fei.ppds import Mutex, Semaphore, print, Thread
from time import sleep
from random import randint


class Lightswitch:
    def __init__(self):
        self.counter = 0
        self.mutex = Mutex()

    def lock(self, semaphore):
        self.mutex.lock()
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.unlock()

    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()


class Shared:
    def __init__(self):
        self.semaphore = Semaphore(1)


def read(lightswitch, shared):
    while True:
        sleep(randint(1, 10)/10)
        lightswitch.lock(shared.semaphore)
        sleep(randint(1, 10)/10)
        lightswitch.unlock(shared.semaphore)


def write(shared):
    while True:
        sleep(randint(1, 10)/10)
        shared.semaphore.wait()
        sleep(randint(1, 10)/10)
        shared.semaphore.signal()
        print("vpisovanie3")


ls = Lightswitch()
shared = Shared()

threads = []

for i in range(9):
    t = Thread(read,ls,shared)
    threads.append(t)

for i in range(1):
    t = Thread(write,shared)
    threads.append(t)

for t in threads:
    t.join()
