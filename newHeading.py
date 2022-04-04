# ****************************************************
# Filename: newHeading.py
# Creater: Joe
# Description: uses icm20948 sensor to find the heading that board is currently facing.
#              Requres calibrate.txt to calibrate sensor readings
#              NOTE: THIS FILE CONTAINS SOURCE CODE FROM AN ONLINE RESOURCE TO DEAL WITH THE DATA
#              MORE INFO IN WRITE UP
# ****************************************************

import math
from icm20948 import ICM20948
import ast
import pi2go
from time import sleep

class CompassHeading:
    """ALWAYS DEL BEFORE SHUTTING DOWN"""

    def __init__(self):

        global FileNotFoundError
        self.imu = ICM20948()
        self.x, self.y, self.z = 0, 1, 2
        self.declination = 0.01076

        try:
            FileNotFoundError
        except NameError:
            FileNotFoundError = IOError

        try:
            with open("calibrate.txt", "r") as f:
                read = f.readline()
                read.split(',')

                if read != "":
                    read = ast.literal_eval(read)
                    for i in range(len(read)):
                        for l in range(len(read[i])):
                            read[i][l] = float(read[i][l])

                    self.magMax = read[0]
                    self.magMin = read[1]
                    self.accMax = read[2]
                    self.accMin = read[3]
                else:
                    FileNotFoundError
        except FileNotFoundError:
            self.magMax = list(self.imu.read_magnetometer_data())
            self.magMin = list(self.imu.read_magnetometer_data())
            self.accMax = list(self.imu.read_accelerometer_gyro_data())[:3]
            self.accMin = list(self.imu.read_accelerometer_gyro_data())[:3]

        try:
            pi2go.spinRight(50)
        except Exception:
            pi2go.init()
            pi2go.spinRight(50)
        finally:
            for i in range(10):
                sleep(1)
            pi2go.go(0,0)

    def __del__(self):
        print("Shutting down magnetometer")

        with open("calibrate.txt", "w") as f:
            f.write(str(self.magMax) + ',' + str(self.magMin) + ',' + str(self.accMax) + ',' + str(self.accMin))

    def getMag(self):

        mag = list(self.imu.read_magnetometer_data())

        for i in range(3):
            v = mag[i]

            if v < self.magMin[i]:
                self.magMin[i] = v
            elif v > self.magMax[i]:
                self.magMax[i] = v

            mag[i] -= self.magMin[i]

            try:
                mag[i] /= self.magMax[i] - self.magMin[i]
            except ZeroDivisionError:
                pass

            mag[i] -= (self.magMax[i] + self.magMin[i]) / 2

        return mag

    def getAcc(self):

        acc = list(self.imu.read_accelerometer_gyro_data())[:3]

        for i in range(3):
            v = acc[i]

            if v < self.accMin[i]:
                self.accMin[i] = v
            elif v > self.accMax[i]:
                self.accMax[i] = v

            acc[i] -= (self.accMax[i] + self.accMin[i]) / 2

            acc[i] -= self.accMin[i]
            try:
                acc[i] /= self.accMax[i] - self.accMin[i]
            except ZeroDivisionError:
                pass

        return acc


    def getHeading(self):
        mag = self.getMag()
        acc = self.getAcc()

        pitch = math.asin(acc[self.x])
        roll = -math.asin(acc[self.y]/math.cos(pitch))

        xComp = mag[self.x]*math.cos(math.asin(acc[self.x])) + mag[self.z]*math.sin(pitch)
        yComp = mag[self.x]*math.sin(math.asin(acc[self.y]/math.cos(pitch))) * math.sin(math.asin(acc[self.x])) \
                + mag[self.y]*math.cos(math.asin(acc[self.y]/math.cos(pitch)))\
                - mag[self.z]*math.sin(math.asin(acc[self.y]/math.cos(pitch)))*math.cos(math.asin(acc[self.x]))

        calcheading = math.degrees(math.atan2(yComp, xComp))
        calcheading -= math.degrees(self.declination)
        if calcheading > 360:
            calcheading -= 360
        elif calcheading < 0:
            calcheading += 360

        return calcheading

if __name__ == "__main__":
    try:
        heading = CompassHeading()
        while True:
            print(heading.getHeading())
            sleep(0.25)

    except KeyboardInterrupt:
        del heading
