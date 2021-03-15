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
    def __init__(self,ls_operators,without_operators,without_sensors,simple_barrier):
        self.lightswitch_operators = ls_operators
        self.without_operators = without_operators
        self.without_sensors = without_sensors

    def operator(self,operator_id):
        while True:
            self.without_operators.wait()
            number_reading_operators = self.lightswitch_operators.lock(self.without_sensors)
            self.without_operators.signal()
            waiting_time_of_operator = randint(4, 5)/100
            print('monit "%02d": pocet_citajucich_monitorov=%02d, trvanie_citania=%0.3f\n' % (operator_id,number_reading_operators,waiting_time_of_operator))
            sleep(waiting_time_of_operator)
            self.lightswitch_operators.unlock(self.without_sensors)


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