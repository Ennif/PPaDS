from fei.ppds import Semaphore, Mutex, Thread, print
from random import randint
from time import sleep

max_servings = 5
number_of_savages = 3
number_of_cook = 3


class SimpleBarrier:

    def __init__(self, N):
        self.N = N
        self.mutex = Mutex()
        self.cnt = 0
        self.sem = Semaphore(0)

    def wait(self,
             print_str,
             savage_id,
             print_last_thread=False,
             print_each_thread=False):
        self.mutex.lock()
        self.cnt += 1
        if print_each_thread:
            print(print_str % (savage_id, self.cnt))
        if self.cnt == self.N:
            self.cnt = 0
            if print_last_thread:
                print(print_str % (savage_id))
            self.sem.signal(self.N)
        self.mutex.unlock()
        self.sem.wait()


class Shared:

    def __init__(self):
        self.mutex = Mutex()
        self.mutex2 = Mutex()
        self.servings = 0
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)
        self.barrier1 = SimpleBarrier(number_of_savages)
        self.barrier2 = SimpleBarrier(number_of_savages)


def get_serving_from_pot(savage_id, shared):
    print("divoch %2d: beriem si porciu" % savage_id)
    shared.servings -= 1


def eat(savage_id):
    print("divoch %2d: hodujem" % savage_id)
    sleep(0.2 + randint(0, 3) / 10)


def savage(savage_id, shared):
    while True:
        shared.barrier1.wait(
            "divoch %2d: prisiel som na veceru, uz nas je %2d",
            savage_id,
            print_each_thread=True)
        shared.barrier2.wait("divoch %2d: uz sme vsetci, zaciname vecerat",
                             savage_id,
                             print_last_thread=True)
        shared.mutex.lock()
        print("divoch %2d: pocet zostavajucich porcii v hrnci je %2d" %
              (savage_id, shared.servings))
        if shared.servings == 0:
            print("divoch %2d: budim kuchara" % savage_id)
            shared.empty_pot.signal(max_servings)
            shared.full_pot.wait()
        get_serving_from_pot(savage_id, shared)
        shared.mutex.unlock()

        eat(savage_id)


def put_serving_in_pot(servings, shared, cook_id):

    print("kuchar %2d: varim" % cook_id)
    sleep(0.4 + randint(0, 2) / 10)
    shared.mutex2.lock()
    shared.servings += 1
    if shared.servings == servings:
            print("kuchar %2d hrniec je plny" % cook_id)
            shared.full_pot.signal()
    shared.mutex2.unlock()


def cook(servings, shared, cook_id):

    while True:
        shared.empty_pot.wait()
        put_serving_in_pot(servings, shared, cook_id)
