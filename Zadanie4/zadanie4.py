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
    def __init__(self,ls_operators,without_operators,without_sensors):
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
    def __init__(self,ls_sensors,w_data_by_sens,without_sensors,without_operators):
        self.lightswitch_sensors = ls_sensors
        self.written_data_by_sensors = w_data_by_sens
        self.without_sensors = without_sensors
        self.without_operators = without_operators

    def sensor_P_T(self,sensor_id):
        while True:
            sleep(randint(5,6)/100)
            number_writing_sensors = self.lightswitch_sensors.lock(self.without_operators)
            self.without_sensors.wait()
            waiting_time_of_sensor = randint(1, 2)/100
            print('cidlo "%02d": pocet_zapisujucich_cidiel=%02d, trvanie_zapisu=%0.3f\n' % (sensor_id,number_writing_sensors,waiting_time_of_sensor))
            sleep(waiting_time_of_sensor)
            self.without_sensors.signal()
            self.lightswitch_sensors.unlock(self.without_operators)

    def sensor_H(self, sensor_id):
        while True:
            sleep(randint(5,6)/100)
            number_writing_sensors = self.lightswitch_sensors.lock(self.without_operators)
            self.without_sensors.wait()
            waiting_time_of_sensor = randint(20, 25)/1000
            print('cidlo "%02d": pocet_zapisujucich_cidiel=%02d, trvanie_zapisu=%0.3f\n' % (sensor_id,number_writing_sensors,waiting_time_of_sensor))
            sleep(waiting_time_of_sensor)
            self.without_sensors.signal()
            self.lightswitch_sensors.unlock(self.without_operators)


class PowerStation:
    def __init__(self):
        self.lightswitch_sensors = Lightswitch()
        self.lightswitch_operators = Lightswitch()
        self.written_data_by_sensors = Event()
        self.without_operators = Semaphore(1)
        self.without_sensors = Semaphore(1)
        self.operator = Operator(
            self.lightswitch_operators,
            self.without_operators,
            self.without_sensors
            )
        self.sensor = Sensor(
            self.lightswitch_sensors,
            self.written_data_by_sensors,
            self.without_sensors,
            self.without_operators)