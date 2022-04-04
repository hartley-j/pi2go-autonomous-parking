# ****************************************************
# Filename: robot.py
# Creater: Joe
# Description: contains declaration of robot object.
# ****************************************************

import pi2go
from heading import CompassHeading
from time import sleep
from simple_pid import PID
import functools


class Robot:

    def __init__(self):
        pi2go.init()

        self.heading = CompassHeading()
        self.initHeading = self.heading.averageHeading(10)


    def __del__(self):
        pi2go.cleanup()

    def forward(self, speed):
        heading = self.heading.averageHeading(10)

        pid = PID(1, 0.1, 0, setpoint=heading)
        pid.output_limits = (-100, 100)

        while True:
            currentHeading = self.heading.averageHeading(5)

            correction = pid(currentHeading)
            self.forwardUpdate(val=correction, speed=speed)

    def forwardUpdate(self, val, speed=80):
        if val != 0:
            pi2go.go(speed, (speed + val))

        sleep(1)

        return self.heading.averageHeading(5)

    def spin(self, deg, speed=50):
        currenthead = self.heading.getHeading()
        if 360 > deg > -360:
            self.rotateAngle(deg, currenthead)
        elif abs(deg) >= 360:
            nspin = deg // 360
            n = 0
            inithead = currenthead

            while n != nspin:
                if deg > 0:
                    pi2go.spinRight(speed)
                    sleep(0.001)
                    currenthead = self.heading.getHeading()

                    if currenthead == inithead:
                        n += 1
                elif deg < 0:
                    pi2go.spinLeft(speed)
                    sleep(0.001)
                    currenthead = self.heading.getHeading()

                    if currenthead == inithead:
                        n += 1

            currenthead = self.heading.getHeading()
            degreestoturn = deg - (nspin * 360)
            self.rotateAngle(degreestoturn, currenthead)

    def rotateAngle(self,deg,speed=20):
        currenthead = self.heading.averageHeading(10)

        head = currenthead + deg
        print("head=", head)

        if head > 360:
            head -= 360
        elif head < 0:
            head += 360

        pi2go.spinRight(speed)

        while not(head - 5 <= currenthead <= head + 5):
            sleep(0.001)
            currenthead = self.heading.averageHeading(5)
            print("current heading is:", currenthead)

        pi2go.go(0,0)

    def stop(self):
        pi2go.go(0,0)

def handleExceptions(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        try:
            func(*args,**kwargs)
        except Exception as e:
            print('Unable to run due to following exception:')
            print(e)
            exit()
        finally:
            pi2go.cleanup()
    return wrapper

if __name__ == '__main__':
    pass
