# ****************************************************
# Filename: calibrateIMU.py
# Creater: Joe
# Description: Calibrates mag sensor
# ****************************************************

from time import sleep
import pi2go
from icm20948 import ICM20948
import RPi.GPIO
import os
import sys
import numpy as np
from heading import Compass

def turnOneWheel(clockwise=False, wheel="Right", speed=20, duration=10):
    heading = Compass()
    try:
        pi2go.init()
    except:
        pass

    start = heading.getMedianHeading()
    if clockwise and (wheel == "Right"):
        # Right wheel reverses
        print(f"Moving {wheel} wheel at speed {-1 * speed}")
        left, right = (0, -1 * speed)
    elif clockwise and (wheel == "Left"):
        # Left wheel forward
        print(f"Moving {wheel} wheel at speed {speed}")
        left, right = (speed, 0)
    elif not clockwise and (wheel == "Right"):
        print(f"Moving {wheel} wheel at speed {speed}")
        left, right = (0, speed)
    elif not clockwise and (wheel == "Left"):
        print(f"Moving {wheel} wheel at speed {-1 * speed}")
        left, right = (-1 * speed, 0)
    else:
        left, right = (speed, 0)

    pi2go.go(left, right)
    sleep(duration)
    pi2go.go(0, 0)
    end = heading.getMedianHeading()

    pi2go.cleanup()

    # Difference between angles
    # Spinning in a anti-clockwise direction
    if (not clockwise) and (end > start):
        # Then, we have passed South (from -180 to +179)
        end -= 360
    elif clockwise and (end < start):
        end += 360
    else:
        pass

    diff = start - end
    print(f"Start: {start}, End: {end}, Diff:{diff}")

    return start, end, diff


def wheelTurn():

    turnOneWheel(clockwise=False, wheel="Right", speed=40, duration=10)
    turnOneWheel(clockwise=False, wheel="Left", speed=40, duration=10)


def getCalibration(overwrite):
    '''
    Looks for a calibration file, and if it doesn't exist, run the calibration
    '''

    calfile = "calibration.txt"

    if (not os.path.isfile(calfile)) or overwrite:
        # Run calibration
        # cal = runCalibration()
        cal = runManualCalibration()
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
    heading = Compass()
    pi2go.init()
    nmax = 500
    data_list = []
    calfile = "calibration_manual.txt"
    if os.path.isfile(calfile):
        os.remove(calfile)

    for obs in ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]:
        input(f"Manually position the pi2go to face {obs}, then press Enter")
        n = 0
        while n < nmax:
            magData = heading.getMag()
            data_list.append([n, magData['x'], magData['y'], magData['z'], obs])
            with open(calfile, "a") as file:
                file.write(f"{n},{magData['x']},{magData['y']},{magData['z']},{obs}\n")
            n += 1

    cal = {'xmin': np.median([i[1] for i in data_list if i[4] == 'W']),
           'ymin': np.median([i[2] for i in data_list if i[4] == 'S']),
           'zmin': np.min([i[3] for i in data_list]),
           'xmax': np.median([i[1] for i in data_list if i[4] == 'E']),
           'ymax': np.median([i[2] for i in data_list if i[4] == 'N']),
           'zmax': np.max([i[3] for i in data_list])}

    with open("calibration.txt", "w") as file:
        for key, val in cal.items():
            file.write(f"{key}:{val}\n")

    return cal

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

    test = sys.argv[1]

    if test == 'getCalibration':
        overwrite = True
        try:
            cal = getCalibration(overwrite)
        finally:
            pi2go.cleanup()

        print(cal)

    elif test == 'turnWheels':
        wheelTurn()

    else:
        print("Argument not recognised")
