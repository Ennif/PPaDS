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
        