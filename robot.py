# ****************************************************
# Filename: robot.py
# Creater: Joe
# Description: contains declaration of robot object.
# ****************************************************
import math

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
        self.width = 13.6
        self.widthOfWheels = 2.6
        self.coordinate = [0, 0]

    def __del__(self):
        pi2go.cleanup()
        del self.heading

    def updateCoordinate(self, bearing, distance):
        rads = math.radians(bearing)
        self.coordinate[0] = self.coordinate[0] + distance * math.sin(rads)
        self.coordinate[1] = self.coordinate[1] + distance * math.cos(rads)

    def forward(self,distance, speed=40):
        # Move the robot forward for a set distance
        initHead = self.heading.getHeading()
        currentHeading = initHead
        currentDistance = pi2go.getDistance()

        pid = PID(1.95, 0, 0.075, setpoint=0)
        pid.output_limits = (-(100 + speed)/2, (100 - speed)/2)
        pid.sample_time = 0.01

        changeDistance = currentDistance - distance
        lowerBound = changeDistance - 5
        upperBound  = changeDistance + 5
        n = 0
        oldCorrection = 0
        while not(lowerBound <= currentDistance <= upperBound):

            change = self.heading.normaliseHeading(currentHeading - initHead)

            correction = pid(change)
            print(f"Current heading: {currentHeading}\tChange: {change}\tCorrection: {correction}\n")
            if n == 0 or correction != oldCorrection:
                pi2go.go(round(speed + correction), speed)
            currentDistance = pi2go.getDistance()
            currentHeading = self.heading.getHeading()
            n += 1
            oldCorrection = correction


    def rotateAngle(self,deg,speed=10, tolerance=None):
        # Rotates the robot a set number of degrees from -180 to 180
        # Used in oldMap.py and ...
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