from fei.ppds import Event
from random import randint as rand
from fei.ppds import Thread, Semaphore, Mutex
from time import sleep
from fei.ppds import print


class ReusableBarrier:
    def __init__(self, numberOfThreads):
        self.numberOfThreads = numberOfThreads
        self.mutex = Mutex()
        self.semaphore = Semaphore(0)
        self.counter = 0

    def wait(self):
        self.mutex.lock()
        self.counter += 1

        if self.counter == self.numberOfThreads:
            self.semaphore.signal(self.numberOfThreads)
            self.counter = 0

        self.mutex.unlock()
        self.semaphore.wait()


def rendezvous(thread_id):
    sleep(rand(1, 10)/10)
    print('rendezvous: Vlakno %d' % thread_id)


def ko(thread_id):
    print('ko: Vlanko %d' % thread_id)
    sleep(rand(1, 10)/10)


def barrier_example(barrier, thread_id):
    while True:

        barrier.wait()
        rendezvous(thread_id)
        barrier.wait()
        ko(thread_id)


numberOfThreads = 5
sb = ReusableBarrier(numberOfThreads)

threads = list()
for i in range(numberOfThreads):
    t = Thread(barrier_example, sb, i)
    threads.append(t)

for t in threads:
    t.join()
