# ****************************************************
# Filename: headingICM20948.py
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
        self.axes = 1, 2

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

                    self.amax = read[0]
                    self.amin = read[1]
                else:
                    FileNotFoundError
        except FileNotFoundError:
            self.amax = list(self.imu.read_magnetometer_data())
            self.amin = list(self.imu.read_magnetometer_data())

        try:
            pi2go.spinRight(50)
        except Exception:
            pi2go.init()
            pi2go.spinRight(50)
        finally:
            for i in range(10):
                sleep(1)
                print(self.getHeading())
            pi2go.go(0,0)

    def __del__(self):
        print("Shutting down magnetometer")

        with open("calibrate.txt", "w") as f:
            f.write(str(self.amax) + ',' + str(self.amin))

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
        headcalc = math.atan2(mag[self.axes[1]],
                              mag[self.axes[0]])

        if headcalc < 0:
            headcalc += 2 * math.pi

        return math.degrees(headcalc)

    def averageHeading(self, n):
        values = [self.getHeading() for i in range(n)]
        print(values)
        return roundNearest(sum(values)/len(values))

    def getData(self):
        ax, ay, az, gx, gy, gz = self.imu.read_accelerometer_gyro_data()
        mx, my, mz = self.imu.read_magnetometer_data()

        roll = math.atan2(-ay, az)
        pitch = math.atan2(-ax, math.sqrt(ay * ay + az * az))
        heading = math.atan2(my*math.cos(roll) + mz*math.sin(roll),
                             -mx*math.cos(pitch) + -my*math.sin(pitch)*math.sin(roll) + mz*math.sin(pitch)*math.cos(roll))

        #print("Roll:%s Pitch:%s Heading:%s" %(roll, pitch, heading))
        return math.degrees(heading)

def roundNearest(n, base=5):
    return base * round(n/base)

def normaliseDeg(deg):
    if deg > 360:
        return deg - 360
    elif deg < 0:
        return deg + 360
    else:
        return deg

if __name__ == '__main__':
    try:
        heading = CompassHeading()
        while True:
            print(heading.getData())
            sleep(0.25)

    except KeyboardInterrupt:
        del heading

