import fei.ppds as fp
from fei.ppds import Mutex, Semaphore, print, Thread, Event
from time import sleep
from random import randint


class Lightswitch:
    def __init__(self):
        self.counter = 0
        self.mutex = Mutex()

    def lock(self, semaphore):
        self.mutex.lock()
        tmp_counter = self.counter
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.unlock()
        return tmp_counter

    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()


class Operator:
    def __init__(self):
        pass

    def operator(self,operator_id):
        pass


class Sensor:
    def __init__(self):
        pass

    def sensor_P_T(self,sensor_id):
        pass

    def sensor_H(self, sensor_id):
        pass


class PowerStation:
    def __init__(self):
        pass