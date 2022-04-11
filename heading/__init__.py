# ****************************************************
# Filename: __init__.py
# Creater: Joe
# Description: main file for heading package
# ****************************************************

import math
from icm20948 import ICM20948
import ast
from time import sleep


class Compass:
    """
    Takes data from icm20948 and calculates the current heading from north
        Prerequisites:
            - icm20948 connected to SCL and SDA
            - icm20948 package downloaded from pimoroni github
    """

    def __init__(self):
        self.imu = ICM20948()
        calfile = 'calibration.txt'

        # Max and min values for each axes
        # Load calibration file
        self.cal = {}
        with open(calfile, "r") as file:
            lines = file.readlines()
            for line in lines:
                key, val = line.split(':')
                self.cal[key] = float(val.strip('\n'))


        # TODO: add support for opening calibrate file and changing max and min vals

    # def maxMin(self):
    #     pi2go.init()
    #     pi2go.spinRight(80)
    #     for i in range(50):
    #         mag = list(self.imu.read_magnetometer_data())
    #
    #         for j in range(3):
    #             v = mag[j]
    #
    #             if v > self.axesMax[j]:
    #                 self.axesMax[j] = v
    #             if v < self.axesMin[j]:
    #                 self.axesMin[j] = v
    #     pi2go.go(0,0)
    #     pi2go.cleanup()


    def getMag(self):
        """" Gets magnetometer data and returns as [x, y, z]"""
        # Get mag values in form: [X, Y, Z]
        # Raw output (from the sensor) is: X, Y, Z
        # But, because of the orientation of the sensor, these values are ACTUALLY:
        #       Z1, Y1, X1
        Z1, Y1, X1 = list(self.imu.read_magnetometer_data())

        return {'x':X1, 'y':Y1, 'z':Z1}


    def calibrate(self, raw):
        """ raw in form of measured [x, y, z] """
        # Uses list comprehension to multiply every value in list by -1
        # raw = [raw[i] * -1 for i in range(3)]

        # Normalises every axes value with respective min and max values
        for k, val in raw.items():
            raw[k] -= self.cal[f"{k}min"]
            raw[k] /= (self.cal[f"{k}max"] - self.cal[f"{k}min"])
            raw[k] -= 0.5

        return raw


    def headingCalc(self, coord):
        # We want the heading, which is the angle from North which, in our case, lies on the Y axis.
        # Atan2 takes the arguments atan2(y, x) to find the angle from the X axis.
        # However, we want the angle from the Y axis so we switch it around.
        heading = math.degrees(math.atan2(coord['x'], coord['y']))

        return heading


    def getHeading(self):
        '''
        Gets data from the magnetometre, calibrates it, and calculates the heading
        '''
        magData = self.getMag()
        magData = self.calibrate(magData)
        heading = self.headingCalc(coord=magData)

        return heading
