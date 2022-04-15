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
    '''
    Looks for a calibration file, and if it doesn't exist, run the calibration
    '''

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


def runManualCalibration():
    '''
    Manually position the pi2go facing N-NE-E-SE-S-SW-W-NW, and record the median x, y and z values
    '''
    imu = ICM20948()
    pi2go.init()
    nmax = 500

    for obs in ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]:
        input(f"Manually position the pi2go to face {obs}, then press Enter")
        n = 0
        while n < nmax:
            Z1, Y1, X1 = list(imu.read_magnetometer_data())
            with open("calibration_manual.txt", "w") as file:
                file.write(f"{n},{X1},{Y1},{Z1},{obs}\n")
            n += 1


def runCalibration():
    '''
    Rotate the pi2go in a clockwise direction, until we have nmax values for x, y and z
    '''
    imu = ICM20948()
    pi2go.init()
    nmax = 2000

    pi2go.go(50, 0)
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

    pi2go.go(0, 0)
    pi2go.cleanup()
    del imu

    cal = {'xmin': np.min(xlist),
           'ymin': np.min(ylist),
           'zmin': np.min(zlist),
           'xmax': np.max(xlist),
           'ymax': np.max(ylist),
           'zmax': np.max(zlist)}

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
