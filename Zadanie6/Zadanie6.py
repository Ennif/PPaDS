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
        self.mutex.wait()
        self.hydrogen += 1
        if self.hydrogen < 2 or self.oxygen < 1:
            self.mutex.signal()
        else:
            self.oxygen -= 1
            self.hydrogen -= 2
            self.oxygenQueue.signal()
            self.hydrogenQueue.signal(2)

        self.hydrogenQueue.wait()
        print("Hydrogen do zlucenia")
        self.bond()

        self.barrier.wait()

    def bond(self):
        sleep(randint(5, 15)/10)
        print("Zlucenie buniek")


def init_and_run():

    threads = list()
    molecule = Molecule()
    while True:
        threads.append(Thread(molecule.oxygenFunc))
        threads.append(Thread(molecule.hydrogenFunc))

    # for t in threads:
    #    t.join()

if __name__ == "__main__":
    init_and_run()
