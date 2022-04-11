# ****************************************************
# Filename: calibrateIMU.py
# Creater: Joe
# Description: Calibrates mag sensor
# ****************************************************

from time import sleep
import pi2go
from icm20948 import ICM20948
import os
import numpy as np


def getCalibration(overwrite):

    calfile = "calibration.txt"

    if (not os.path.isfile(calfile)) or overwrite:
        # Run calibration
        cal = runCalibration()
    else:
        # Load calibration file
        cal = {}
        with open(calfile, "r") as file:
            lines = file.readlines()
            for line in lines:
                key, val = line.split(':')
                cal[key] = float(val.strip('\n'))

    return cal


def runCalibration():

    imu = ICM20948()
    pi2go.init()
    nmax = 300

    pi2go.spinRight(50)
    n = 0
    xlist, ylist, zlist = [[], [], []]

    while n < nmax:
        sleep(0.001)
        # Raw output (from the sensor) is: X, Y, Z
        # But, because of the orientation of the sensor, these values are ACTUALLY:
        #       Z1, Y1, X1
        Z1, Y1, X1 = list(imu.read_magnetometer_data())
        xlist.append(X1)
        ylist.append(Y1)
        zlist.append(Z1)
        n += 1

    pi2go.cleanup()
    del imu

    cal = {'xmin': np.min(xlist), 'ymin': np.min(ylist), 'xmax': np.max(xlist), 'ymax': np.max(ylist)}
    with open("calibration.txt", "w") as file:
        for key, val in cal.items():
            file.write(f"{key}:{val}\n")

    return cal


if __name__ == '__main__':

    overwrite = True
    try:
        cal = getCalibration(overwrite)
    finally:
        pi2go.cleanup()

    print(cal)
