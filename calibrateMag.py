# ****************************************************
# Filename: calibrateMage.py
# Creater: Joe
# Description: Calibrates mag sensor
# ****************************************************

from icm20948 import ICM20948
import math
import pi2go
from time import sleep


class Heading:

    def __init__(self):

        self.imu = ICM20948()
        self.axes = 1, 2

        self.amin = list(self.imu.read_magnetometer_data())
        self.amax = list(self.imu.read_magnetometer_data())
        pi2go.go(0, 0)

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


def main(file):
    pi2go.init()
    head = Heading()

    for i in range(50):
        pi2go.spinRight(50)
        sleep(1)
        print(head.heading())

    amax = head.amax
    amin = head.amin

    with open(file, "w") as f:
        f.write(str(amax) + "," + str(amin))


if __name__ == '__main__':
    main("calibrate.txt")
