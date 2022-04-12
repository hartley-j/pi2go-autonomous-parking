# ****************************************************
# Filename: robot.py
# Creater: Joe
# Description: contains declaration of robot object.
# ****************************************************

import pi2go
from heading import Compass
from time import sleep
from simple_pid import PID

class Robot:

    def __init__(self):
        pi2go.init()

        self.heading = Compass()
        self.initHeading = self.heading.getHeading()

    def __del__(self):
        pi2go.cleanup()
        del self.heading

    def forward(self, speed, distance):
        head = round(self.heading.getHeading())
        currentDistance = pi2go.getDistance()

        pid = PID(0.1, -0.1, 0, setpoint=head)
        pid.output_limits = (-(100 + speed), (100 - speed))

        changeDistance = currentDistance - distance
        lowerBound = changeDistance - 5
        upperBound  = changeDistance + 5
        while not(lowerBound <= currentDistance <= upperBound):
            currentHeading = round(self.heading.getHeading())
            print(currentHeading)
            correction = pid(currentHeading)
            print(correction)
            self.forwardUpdate(val=correction, speed=speed)
            currentDistance = pi2go.getDistance()
            sleep(0.1)

    def forwardUpdate(self, val, speed=80):
        if val != 0:
            pi2go.go(speed, (speed + val))

        sleep(0.1)

        return self.heading.getHeading()

    # def spin(self, deg, speed=50):
    #     currenthead = self.heading.getHeading()
    #     if 360 > deg > -360:
    #         self.rotateAngle(deg, currenthead)
    #     elif abs(deg) >= 360:
    #         nspin = deg // 360
    #         n = 0
    #         inithead = currenthead
    #
    #         while n != nspin:
    #             if deg > 0:
    #                 pi2go.spinRight(speed)
    #                 sleep(0.001)
    #                 currenthead = self.heading.getHeading()
    #
    #                 if currenthead == inithead:
    #                     n += 1
    #             elif deg < 0:
    #                 pi2go.spinLeft(speed)
    #                 sleep(0.001)
    #                 currenthead = self.heading.getHeading()
    #
    #                 if currenthead == inithead:
    #                     n += 1
    #
    #         currenthead = self.heading.getHeading()
    #         degreestoturn = deg - (nspin * 360)
    #         self.rotateAngle(degreestoturn, currenthead)

    def rotateAngle(self,deg,speed=20):
        currenthead = self.heading.getHeading()
        print("Current heading=", currenthead)
        targetHead = self.heading.normaliseHeading(currenthead + deg)
        print("Pointing towards:", targetHead)

        lowerBound = targetHead - 20
        upperBound = targetHead + 20

        while not(lowerBound <= currenthead <= upperBound):
            if currenthead > upperBound:
                pi2go.spinRight(speed)
            if currenthead < lowerBound:
                pi2go.spinLeft(speed)

            sleep(0.001)
            currenthead = self.heading.getHeading()
            print("current heading is:", currenthead)

        pi2go.go(0,0)

    def stop(self):
        pi2go.go(0,0)

# def handleExceptions(func):
#     @functools.wraps(func)
#     def wrapper(*args,**kwargs):
#         try:
#             func(*args,**kwargs)
#         except Exception as e:
#             print('Unable to run due to following exception:')
#             print(e)
#             exit()
#         finally:
#             pi2go.cleanup()
#     return wrapper