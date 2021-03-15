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
    def __init__(self,
                 ls_operators,
                 without_operators,
                 without_sensors,
                 simple_barrier
                 ):
        self.ls_ops = ls_operators
        self.without_operators = without_operators
        self.without_sensors = without_sensors
        self.simple_barrier = simple_barrier

    def operator(self, operator_id):
        while True:
            self.simple_barrier.wait()
            self.without_operators.wait()
            num_reading_ops = self.ls_ops.lock(self.without_sensors)
            self.without_operators.signal()
            waiting_time_of_operator = randint(4, 5)/100
            print(
                'monit "d": pocet_citajucich_monitorov=d,'
                "trvanie_citania=%0.3f\n"
                % (operator_id, num_reading_ops, waiting_time_of_operator)
            )
            sleep(waiting_time_of_operator)
            self.ls_ops.unlock(self.without_sensors)


class Sensor:
    def __init__(self,
                 ls_sensors,
                 w_data_by_sens,
                 without_sensors,
                 without_operators,
                 simple_barrier
                 ):
        self.ls_sens = ls_sensors
        self.written_data_by_sensors = w_data_by_sens
        self.without_sensors = without_sensors
        self.without_operators = without_operators
        self.simple_barrier = simple_barrier

    def sensor_P_T(self, sensor_id):
        while True:
            sleep(randint(5, 6)/100)
            num_writing_sens = self.ls_sens.lock(self.without_operators)
            self.without_sensors.wait()
            waiting_time_of_sensor = randint(1, 2)/100
            print(
                'cidlo "d": pocet_zapisujucich_cidiel=d,'
                "trvanie_zapisu=%0.3f\n"
                % (sensor_id, num_writing_sens, waiting_time_of_sensor)
            )
            sleep(waiting_time_of_sensor)
            self.without_sensors.signal()
            self.simple_barrier.wait()
            self.ls_sens.unlock(self.without_operators)

    def sensor_H(self, sensor_id):
        while True:
            sleep(randint(5, 6)/100)
            num_writing_sens = self.ls_sens.lock(self.without_operators)
            self.without_sensors.wait()
            waiting_time_of_sensor = randint(20, 25)/1000
            print(
                'cidlo "d": pocet_zapisujucich_cidiel=d,'
                "trvanie_zapisu=%0.3f\n"
                % (sensor_id, num_writing_sens, waiting_time_of_sensor)
            )
            sleep(waiting_time_of_sensor)
            self.without_sensors.signal()
            self.simple_barrier.wait()
            self.ls_sens.unlock(self.without_operators)


class PowerStation:
    def __init__(self):
        self.lightswitch_sensors = Lightswitch()
        self.lightswitch_operators = Lightswitch()
        self.written_data_by_sensors = Event()
        self.without_operators = Semaphore(1)
        self.without_sensors = Semaphore(1)
        self.simple_barrier = SimpleBarrier(3)
        self.operator = Operator(self.lightswitch_operators,
                                 self.without_operators,
                                 self.without_sensors,
                                 self.simple_barrier
                                 )
        self.sensor = Sensor(self.lightswitch_sensors,
                             self.written_data_by_sensors,
                             self.without_sensors,
                             self.without_operators,
                             self.simple_barrier
                             )


class SimpleBarrier:
    def __init__(self, number_of_threads):
        self.number_of_threads = number_of_threads
        self.mutex = Mutex()
        self.event = Event()
        self.counter = 0

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.number_of_threads:
            self.event.signal()
        self.mutex.unlock()
        self.event.wait()


threads = []
power_station = PowerStation()

threads.append(Thread(power_station.sensor.sensor_H, 0))
threads.append(Thread(power_station.sensor.sensor_P_T, 1))
threads.append(Thread(power_station.sensor.sensor_P_T, 2))

for i in range(8):
    t = Thread(power_station.operator.operator, i)
    threads.append(t)

for t in threads:
    t.join()
