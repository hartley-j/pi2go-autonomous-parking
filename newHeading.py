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

    def getHeading(self):
        ax, ay, az, gx, gy, gz = self.imu.read_accelerometer_gyro_data()
        mx, my, mz = self.imu.read_magnetometer_data()

        pitch = math.asin(ax)
        roll = -math.asin(ay/math.cos(pitch))

        magXcomp = (mx * math.cos(pitch)) + ((mx + 2) * math.sin(pitch))
        magYcomp = (my * math.sin(roll) * math.sin(pitch)) + (my + 1) * math.cos(roll) - (my + 2) * math.sin(roll) * math.cos(pitch)

        heading = math.degrees(math.atan2(magYcomp, magXcomp))

        return heading

if __name__ == "__main__":
    try:
        heading = CompassHeading()
        while True:
            print(heading.getHeading())
            sleep(0.25)

    except KeyboardInterrupt:
        del heading
