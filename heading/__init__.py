# ****************************************************
# Filename: __init__.py
# Creater: Joe
# Description: main file for heading package
# ****************************************************

import math
from icm20948 import ICM20948
from cmath import rect, phase
import numpy as np
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


    def getMag(self):
        '''
        Get mag values in form: [X, Y, Z]
        Raw output (from the sensor) is: X, Y, Z
        But, because of the orientation of the sensor, these values are ACTUALLY:
              Z1, Y1, X1
        '''
        Z1, Y1, X1 = list(self.imu.read_magnetometer_data())
        X1 *= -1
        Y1 *= -1
        return {'x': X1, 'y': Y1, 'z': Z1}


    def calibrate(self, raw):
        '''
        Calibrates the raw magnetometer output by normalising between min and max values from the calibration.txt file
        '''

        # Normalises every axes value with respective min and max values
        out = {}
        for k, val in raw.items():
            # # Correct for the direction of the axes due to the position of the sensor on the pi2go
            # raw[k] = raw[k] * -1
            # Remove the minimum value, so all values are positive
            raw[k] -= self.cal[f"{k}min"]
            # Divide by the range so that all values are scaled to between 0 and 1
            raw[k] /= (self.cal[f"{k}max"] - self.cal[f"{k}min"])
            # Subtract 0.5 so that all values are between -0.5 and 0.5
            raw[k] -= 0.5

        return raw

    def headingCalc(self, coord):
        '''
        We want the heading, which is the angle from North which, in our case, lies on the Y axis.
        Atan2 takes the arguments atan2(y, x) to find the angle from the X axis.
        However, we want the angle from the Y axis so we switch x and y around.
        '''

        heading = math.degrees(math.atan2(coord['x'], coord['y']))
        # TODO: Flip the heading (Currently, heading=0 is south, whereas it should be north and vice-versa)

        return heading

    def getHeading(self):
        '''
        Gets data from the magnetometer, calibrates it, and calculates the heading
        '''

        magData = self.getMag()
        magData = self.calibrate(magData)
        heading = self.headingCalc(coord=magData)

        return heading

    def getMedianHeading(self, nmax=50):
        '''
        Get a median angle from a sample of nmax
        '''
        n = 0
        xlist, ylist = [[], []]
        while n < nmax:
            magData = self.getMag()
            magData = self.calibrate(magData)
            xlist.append(magData['x'])
            ylist.append(magData['y'])
            n += 1

        xmedian = np.median(xlist)
        ymedian = np.median(ylist)
        heading_median = self.headingCalc({'x': xmedian, 'y': ymedian})

        return heading_median

    def normaliseHeading(self, deg):
        # Used in map.py and robot.py
        if deg > 180:
            deg -= 360
        if deg < -180:
            deg += 360
        return deg

    def meanAngle(self, deg):
        '''
        Finds an average from a list of degrees (cannot just be sum/len because of -179 and 179 will be 0, when it should be 180 or -180)
        deg: list of degrees ranging from -180 to 180
        '''
        return math.degrees(phase(sum(rect(1, math.radians(d)) for d in deg)/len(deg)))
