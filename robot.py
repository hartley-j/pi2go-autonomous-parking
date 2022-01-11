# ****************************************************
# Filename: robot.py
# Creater: Joe
# Description: contains declaration of robot object.
# ****************************************************

import pi2go
from heading import compassHeading
from time import sleep


class Robot:

    def __init__(self):
        self.heading = compassHeading()
        self.initHeading = self.heading.getHeading()

    def turn(self, deg):
        currentHead = self.heading.getHeading()
        head = currentHead + deg

        if head > currentHead:
            while currentHead != head:
                pi2go.turnLeft()
                sleep(0.2)
                currentHead = self.heading.getHeading()
        elif head < currentHead:
            while currentHead != head:
                pi2go.turnRight()
                sleep(0.2)
                currentHead = self.heading.getHeading()
        else:
            pass

    def forwardUpdate(self, val, speed=50):
        if val != 0:
            pi2go.go(speed, (speed + val))

        sleep(0.5)

        return self.heading.getHeading()


if __name__ == '__main__':
    pass
