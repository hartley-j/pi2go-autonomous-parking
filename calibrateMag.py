# ****************************************************
# Filename: calibrateMage.py
# Creater: Joe
# Description: Calibrates mag sensor
# ****************************************************

from time import sleep

import pi2go
from heading import CompassHeading


def main(head):

    pi2go.spinRight(30)

    while True:
        sleep(0.001)
        print(head.getHeading())


if __name__ == '__main__':
    head = CompassHeading()
    pi2go.init()

    try:
        main(head)
    except KeyboardInterrupt:
        pi2go.go(0,0)
        pi2go.cleanup()
        del head
