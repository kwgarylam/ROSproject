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
timeTick = 0

# Scaling Factor
# A = 32

# List to store the car objects
cars = []
writeData = []
data = []
data2 = []
mytime = []

inputList = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2]
#inputList = [3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2]
#print(len(inputList))

class Car:
    def __init__(self, name, power, valueA, carCreate, carDuration, charging):
        self.name = name
        self.power = power
        self.valueA = valueA
        self.carCreate = carCreate
        self.carDuration = carDuration
        self.charging = charging


def powerCorrection(t, A):
    power = c * A * math.exp(-t / tau)
    if power <= 0.001:
        power = 0
    return power

def time_format(mytime):
    h = math.floor(np.mod(mytime / 60, 24))
    m = math.ceil((np.mod(mytime / 60, 24) % 1) * 60)
    return h, m

def basic_arrange(carNum):
    if carNum <= 4:
        A = 32
    elif 5 <= carNum <= 8:
        A = 20
    elif 9 <= carNum <= 12:
        A = 15
    elif 13 <= carNum <= 15:
        A = 10
    elif carNum >= 16:
        A = 5
    return A


with open('output.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile, dialect='excel')
    writer.writerow(['time', 'cars'])

    i = 0
    j = 0
    while day <= 2:
        # 8am-8pm
        if 0 <= time <= 480 or 1200 <= time < 1440:
            ##### Do something #####
            # Main function
            hh, mm = time_format(time)
            print("Day ", day, "Doing")
            print("Time now: ", str(hh) + ':' + str(mm))

            for x in range (inputList[j]):
                # Create new objects. There are two cars enter for every cycle
                cars.append(Car('car' + str(i), 0, 0, timeTick, 0, "Charge"))
                i = i + 1

        else:
            # The system is idle
            hh, mm = time_format(time)
            print("Day ", day, "Waiting")
            print("Time now: ", str(hh) + ':' + str(mm))

        if time > time_rollOver:
            print("Next day")
            time = 0
            day = day + 1

        ######## Update the value ##########
        # Write the car power information into csv format
        data.append(str(hh) + ':' + str(mm))
        data2.append(str(hh) + ':' + str(mm))

        #print("Charge Num: ", sum(c.charging == "Charge" for c in cars))

        for car in cars:
            carNum = sum(c.charging == "Charge" for c in cars)

            car.valueA = basic_arrange(carNum)
            car.carDuration = timeTick - car.carCreate
            car.power = powerCorrection(car.carDuration, car.valueA)

            if car.power == 0:
                car.charging = "Completed"
                car.valueA = 0
                carNum = sum(c.charging == "Charge" for c in cars)

            data.append(str(car.valueA))
            data2.append(str(car.power))

        writer.writerow(data)
        writer.writerow(data2)

        # Reset the information write to the csv file of every row
        data = []
        data2 = []
        j = j + 1
        time = time + time_spacing
        timeTick = timeTick + time_spacing

print("Program completed...")
