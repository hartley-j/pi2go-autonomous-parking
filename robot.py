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

        self.lengthtoback = 14.3 # Distance from ultrasonic sensors to the back of the robot
        self.wheelDiameter = 6.5 # Diameter of wheels
        self.coordinate = [0, 0]

    def __del__(self):
        pi2go.cleanup()
        del self.heading

    def forward(self, speed, distance):
        # Move the robot forward for a set distance
        head = self.heading.getHeading()
        currentDistance = pi2go.getDistance()

        pid = PID(-0.5, 0, 0, setpoint=head)
        pid.output_limits = (-(100 + speed), (100 - speed))

        changeDistance = currentDistance - distance
        lowerBound = changeDistance - 5
        upperBound  = changeDistance + 5
        while not(lowerBound <= currentDistance <= upperBound):
            currentHeading = self.heading.getHeading()
            change = self.heading.normaliseHeading(head - currentHeading)
            print(currentHeading)
            correction = pid(change)
            print(correction)
            self.forwardUpdate(val=correction, speed=speed)
            currentDistance = pi2go.getDistance()
            sleep(0.1)

    def forwardUpdate(self, val, speed=80):
        # Sets the speed of the robot with correction value created by forward function
        # Returns heading after 100th second to show the affect of correction

        pi2go.go(speed+val,speed)

        sleep(0.01)

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

    def rotateAngle(self,deg,speed=40, tolerance=5):
        # Rotates the robot a set number of degrees from -180 to 180
        # Used in map.py and ...
        currenthead = self.heading.getHeading()
        targetHead = self.heading.normaliseHeading(currenthead + deg)

        lowerBound = targetHead - tolerance
        upperBound = targetHead + tolerance

        while not(lowerBound <= currenthead <= upperBound):
            if deg > 0:
                pi2go.go(speed, 0)
            if deg < 0:
                pi2go.go(-speed, 0)

            sleep(0.001)
            currenthead = self.heading.getHeading()

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