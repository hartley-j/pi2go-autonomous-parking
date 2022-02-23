# ****************************************************
# Filename: calibrateMage.py
# Creater: Joe
# Description: Calibrates mag sensor
# ****************************************************

from time import sleep

import pi2go
from heading import CompassHeading


def main(file):
    pi2go.init()
    head = CompassHeading()

    for i in range(50):
        pi2go.spinRight(50)
        sleep(1)
        print(head.getHeading())

    amax = head.amax
    amin = head.amin

    with open(file, "w") as f:
        f.write(str(amax) + "," + str(amin))


if __name__ == '__main__':
    main("calibrate.txt")
