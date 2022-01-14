# ****************************************************
# Filename: straight.py
# Creater: Joe Hartley
# Description: Makes the pi2go robot move in a straight line. Uses accelerometer and pid controller
# ****************************************************

import pi2go
from icm20948 import ICM20948
import math
from simple_pid import PID
from time import sleep
from packages.heading import compassHeading


class RobotForward:

    def __init__(self):
        self.heading = Heading()
        self.initHeading = self.heading.heading()

    def update(self, val, speed=50):
        if val != 0:
            pi2go.go(speed, (speed + val))

        return self.heading.heading()


def main():
    head = compassHeading()
    rob = RobotForward()

    pid = PID(1, 0.1, 0, setpoint=rob.initHeading)
    pid.output_limits = (-50, 50)

    try:
        while True:
            currentHeading = head.heading()

            correction = pid(currentHeading)
            rob.update(val=correction)
    except KeyboardInterrupt:
        pass
    finally:
        pi2go.cleanup()


if __name__ == '__main__':
    pi2go.init()
    main()
