# ****************************************************
# Filename: straight.py
# Creater: Joe Hartley
# Description: Makes the pi2go robot move in a straight line. Uses accelerometer and pid controller
# ****************************************************

import pi2go
from time import sleep
from icm20948 import ICM20948
import math
from simple_pid import PID


class Heading:

    def __init__(self):

        self.imu = ICM20948()
        self.axes = 1, 2

        try:
            pi2go.init()
            pi2go.go(-50, 50)
            pi2go.cleanup()
        except ModuleNotFoundError:
            pass

        self.amin = list(self.imu.read_magnetometer_data())
        self.amax = list(self.imu.read_magnetometer_data())



    def getMag(self):

        mag = list(self.imu.read_magnetometer_data())

        for i in range(3):
            v = mag[i]

            if v < self.amin[i]:
                self.amin[i] = v
            elif v > self.amax[i]:
                self.amax[i] = v

            mag[i] -= self.amin[i]

            try:
                mag[i] /= self.amax[i] - self.amin[i]
            except ZeroDivisionError:
                pass

            mag[i] -= 0.5

        return mag

    def heading(self):

        mag = self.getMag()
        heading = math.atan2(mag[self.axes[0]], mag[self.axes[1]])

        if heading < 0:
            heading += 2 * math.pi

        return math.degrees(heading)


class RobotForward:

    def __init__(self):
        pi2go.init()

        self.heading = Heading()
        self.initHeading = self.heading.heading()

    def update(self, val, speed=20):
        if val != 0:
            pi2go.go(speed, speed + val)

        return self.heading.heading()


def main():

    head = Heading()
    rob = RobotForward()


    pid = PID(1, 0.1, 0, setpoint=rob.initHeading)
    pid.output_limits = (-50, 50)

    try:
        while True:
            currentHeading = head.heading()

            correction = pid(currentHeading)
            rob.update(val=correction)
    except:
        pass
    finally:
        pi2go.cleanup()


if __name__ == '__main__':
    main()
