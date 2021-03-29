"""
Vypracovanie ulohy - tvorba molekul vody
"""
from fei.ppds import Semaphore, Mutex, Thread, Event, print
from random import randint
from time import sleep


class Barrier:

    def __init__(self, N):
        self.N = N
        self.mutex = Mutex()
        self.counter = 0
        self.semaphore = Semaphore(0)

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.N:
            self.counter = 0
            self.semaphore.signal(self.N)
        self.mutex.unlock()
        self.semaphore.wait()


class Molecule:
    def __init__(self):
        self.mutex = Semaphore(1)
        self.oxygenQueue = Semaphore(0)
        self.hydrogenQueue = Semaphore(0)
        self.oxygen = 0
        self.hydrogen = 0
        self.barrier = Barrier(3)

    def oxygenFunc(self):
            self.mutex.wait()
            self.oxygen += 1
            if self.hydrogen < 2:
                self.mutex.signal()
            else:
                self.oxygen -= 1
                self.hydrogen -= 2
                self.oxygenQueue.signal()
                self.hydrogenQueue.signal(2)

            self.oxygenQueue.wait()
            print("oxygen do zlucenia")
            self.bond()
            self.barrier.wait()
            self.mutex.signal()

    def hydrogenFunc(self):
        pass

    def bond(self):
        pass
