# ****************************************************
# Filename: heading.py
# Creater: Joe
# Description: uses icm20948 sensor to find the heading that board is currently facing.
#              Requres calibrate.txt to calibrate sensor readings
#              NOTE: THIS FILE CONTAINS SOURCE CODE FROM AN ONLINE RESOURCE TO DEAL WITH THE DATA
# ****************************************************

import math
from icm20948 import ICM20948
import ast

class CompassHeading:

    def __init__(self):

        global FileNotFoundError
        self.imu = ICM20948()
        self.axes = 1, 2

        try:
            FileNotFoundError
        except NameError:
            FileNotFoundError = IOError

        try:
            with open("calibrate.txt", "r") as f:
                read = f.readline()
                read.split(',')

                read = ast.literal_eval(read)
                for i in range(len(read)):
                    for l in range(len(read[i])):
                        read[i][l] = float(read[i][l])

                self.amax = read[0]
                self.amin = read[1]
        except FileNotFoundError:
            self.amax = self.imu.read_magnetometer_data()
            self.amin = self.imu.read_magnetometer_data()

    def getMag(self):

        mag = list(self.imu.read_magnetometer_data())

        for i in range(3):
            v = mag[i]

            if v < self.amin[i]:
                self.amin[i] = v
            elif v > self.amax[i]:
                self.amax[i] = v

            mag[i] -= self.amin[i]

            try:
                mag[i] /= self.amax[i] - self.amin[i]
            except ZeroDivisionError:
                pass

            mag[i] -= 0.5

        return mag

    def getHeading(self):

        mag = self.getMag()
        heading = math.atan2(mag[self.axes[0]], mag[self.axes[1]])

        if heading < 0:
            heading += 2 * math.pi

        return math.degrees(heading)


if __name__ == '__main__':
    try:
        heading = CompassHeading()
        while True:
            print("Current heading: %s" %(heading.getHeading()))

    except KeyboardInterrupt:
        pass

