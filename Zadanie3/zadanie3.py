import fei.ppds as fp
from fei.ppds import Mutex, Semaphore, print
from time import sleep
from random import randint


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
