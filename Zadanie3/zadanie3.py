import fei.ppds as fp
from fei.ppds import Mutex, Semaphore, print, Thread
from time import sleep
from random import randint


#Global variables
numberOfReaders = 1
numberOfWriters = 100
timeForRead = 10
timeForWrite = 10


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
        self.turniket = Semaphore(1)


def read(lightswitch, shared):
    while True:
        sleep(randint(1, 10)/timeForRead)
        # shared.turniket.wait()
        # shared.turniket.signal()
        print("citanie1")
        lightswitch.lock(shared.semaphore)
        print("citanie2")
        sleep(randint(1, 10)/timeForRead)
        lightswitch.unlock(shared.semaphore)
        print("citanie3")


def write(shared):
    while True:
        sleep(randint(1, 10)/timeForWrite)
        # print("vpisovanie1")
        shared.semaphore.wait()
        # shared.turniket.wait()
        # print("vypisovanie2")
        sleep(randint(1, 10)/timeForWrite)
        # shared.turniket.signal()
        shared.semaphore.signal()
        print("vpisovanie3")


ls = Lightswitch()
shared = Shared()

threads = []

for i in range(numberOfReaders):
    t = Thread(read, ls, shared)
    threads.append(t)

for i in range(numberOfWriters):
    t = Thread(write, shared)
    threads.append(t)

for t in threads:
    t.join()
