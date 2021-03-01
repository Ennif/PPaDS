from fei.ppds import Event
from random import randint as rand
from fei.ppds import Thread, Semaphore, Mutex
from time import sleep
from fei.ppds import print


class Fibannoci:
    def __init__(self, numberOfThreads):
        self.numberOfThreads = numberOfThreads
        self.actualPosition = 1
        self.fibannociList = [0, 1]
        self.semaphoreList = []

        for _ in range(numberOfThreads):
            self.semaphoreList.append(Semaphore(0))
        self.semaphoreList[0].signal()


def start(f, thread_id):

    print("Thread %d done" % thread_id)
    print(f.fibannociList)


numberOfThreads = 20
f = Fibannoci(numberOfThreads)

threads = list()

for i in range(numberOfThreads):
    t = Thread(start, f, i)
    threads.append(t)

for t in threads:
    t.join()
