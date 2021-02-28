from fei.ppds import Event
from random import randint as rand
from fei.ppds import Thread, Semaphore, Mutex
from time import sleep
from fei.ppds import print


class SimpleBarrier:
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

        self.mutex.unlock()
        self.semaphore.wait()
        



def barrier_example(barrier, thread_id):
    sleep(rand(1,10)/10)
    print("vlakno %d pred barierou" % thread_id)
    barrier.wait()
    print("vlanko %d po bariere" % thread_id)



numberOfThreads = 5
sb = SimpleBarrier(numberOfThreads)

threads = list()
for i in range(numberOfThreads):
    t = Thread(barrier_example, sb, i)
    threads.append(t)

for t in threads:
    t.join()





