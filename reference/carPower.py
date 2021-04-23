from time import sleep
import numpy as np
import math
import csv

# Constants
c = 0.658
tau = 36
duration = 0
time_spacing = 30
time = 1200
time_rollOver = 1440
day = 1

# Scaling Factor
A = 32

# List to store the car objects
cars = []


class Car:
    def __init__(self, name, power, duration):
        self.name = name
        self.power = power
        self.duration = duration

    def details(self):
        return self.name, self.power, self.duration


def powerCorrection(t):
    return c * A * math.exp(-t / tau)


def time_format(mytime):
    h = math.floor(np.mod(mytime / 60, 24))
    m = math.ceil((np.mod(mytime / 60, 24) % 1) * 60)
    return h, m


def basic_arrange():
    # Do something
    pass


with open('output.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['time', 'car', 'power'])

    # car1 = Car('car1', '1234')
    # car2 = Car('car2', '2222')

    # cars.append(car1)
    # cars.append(car2)

    # for car in cars:
    #     print(car.name, car.power, sep=' ')

    i = 0
    while day <= 2:
        if 0 <= time <= 480 or 1200 <= time < 1440:
            ##### Do something #####
            # Main function

            print("Doing")
            print("Time now: ")
            hh, mm = time_format(time)

            carPower = powerCorrection(duration)

            cars.append(Car('car' + str(i), carPower, duration))
            writer.writerow([str(hh) + ':' + str(mm), cars[i].name, cars[i].power])
            duration = duration + time_spacing

            i = i + 1

            time = time + time_spacing

            # sleep(0.1)

        else:
            # The system is idle
            print("Waiting")
            print("Time now: ")
            time_format(time)
            time = time + time_spacing
            # sleep(0.1)

        if time > time_rollOver:
            time = time_spacing
            day = day + 1
