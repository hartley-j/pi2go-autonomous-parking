# ****************************************************
# Filename: robot.py
# Creater: Joe
# Description: contains declaration of robot object.
# ****************************************************

import pi2go
from heading import CompassHeading
from time import sleep
from simple_pid import PID


class Robot:

    def __init__(self):
        self.heading = CompassHeading()
        self.initHeading = self.heading.getHeading()

# The destructor method is required below due to the nature of raspi GPIO pins
# ie they require a 'cleanup' at the end of each program so that they can be used again

    def __del__(self):
        pi2go.cleanup()

    def turn(self, deg):
        currenthead = self.heading.getHeading()
        if 360 > deg > -360:
            head = currenthead + deg

            if head > currenthead:
                while currenthead != head:
                    pi2go.turnLeft()
                    sleep(0.2)
                    currenthead = self.heading.getHeading()
            elif head < currenthead:
                while currenthead != head:
                    pi2go.turnRight()
                    sleep(0.2)
                    currenthead = self.heading.getHeading()
            else:
                pass
        elif abs(deg) >= 360:
            nspin = deg // 360
            n = 0
            inithead = currenthead

            while n != nspin:
                if deg > 0:
                    pi2go.spinRight()
                    sleep(1)
                    currenthead = self.heading.getHeading()

# TODO: finish off turn method. ask mr bailey?



    def forwardUpdate(self, val, speed=50):
        if val != 0:
            pi2go.go(speed, (speed + val))

        sleep(1)

        return self.heading.getHeading()

    def straight(self, deg):

        pid = PID(1, 0.1, 0, setpoint=deg)
        pid.output_limits = (-50, 50)

        while True:
            currentHeading = self.heading.getHeading()

            correction = pid(currentHeading)
            self.forwardUpdate(val=correction)


if __name__ == '__main__':
    pass
