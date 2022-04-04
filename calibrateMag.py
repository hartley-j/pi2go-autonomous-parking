# ****************************************************
# Filename: calibrateMage.py
# Creater: Joe
# Description: Calibrates mag sensor
# ****************************************************

from time import sleep

import pi2go
from heading import CompassHeading


def main(file, head):
    pi2go.init()

    for i in range(100):
        pi2go.spinRight(30)
        sleep(1)
        print(head.getHeading())

    amax = head.amax
    amin = head.amin

    with open(file, "w") as f:
        f.write(str(amax) + "," + str(amin))


if __name__ == '__main__':
    head = CompassHeading()

    try:
        main("calibrate.txt", head)
    except KeyboardInterrupt:
        del head