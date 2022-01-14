# ****************************************************
# Filename: calibrateMage.py
# Creater: Joe
# Description: Calibrates mag sensor
# ****************************************************

from icm20948 import ICM20948
import math
from ... import pi2go
from time import sleep
from ... import heading


def main(file):
    pi2go.init()
    head = compassHeading()

    for i in range(50):
        pi2go.spinRight(50)
        sleep(1)
        print(head.heading())

    amax = head.amax
    amin = head.amin

    with open(file, "w") as f:
        f.write(str(amax) + "," + str(amin))


if __name__ == '__main__':
    main("../calibrate.txt")
