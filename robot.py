# ****************************************************
# Filename: robot.py
# Creater: Joe
# Description: contains declaration of robot object.
# ****************************************************
import math
from line import Line
import pi2go
from heading import Compass
from time import sleep
from simple_pid import PID

class Robot:

    def __init__(self):
        pi2go.init()

        self.heading = Compass()
        self.initHeading = self.heading.getMedianHeading(nmax=25)

        self.lengthtoback = 14.3 # Distance from ultrasonic sensors to the back of the robot
        self.wheelDiameter = 6.5 # Diameter of wheels
        self.width = 13.6
        self.widthOfWheels = 2.6
        self.coordinate = [0, 0]

    def __del__(self):
        pi2go.cleanup()
        del self.heading

    def updateCoordinate(self, bearing, distance):
        """
        Updates the instance coordinates of the robot. Used inside instance
        :param bearing: the heading that the robot has moved along
        :param distance: distance the robot has travelled
        """
        rads = math.radians(bearing)
        self.coordinate[0] = self.coordinate[0] + distance * math.sin(rads)
        self.coordinate[1] = self.coordinate[1] + distance * math.cos(rads)

    def forward(self,distance, speed=40):
        """
        Moves robot forward for certain distance. Used in map.py and park.py.
        :param distance: distance to travel
        :param speed: speed from 0 to 100 of motors
        """
        initHead = self.heading.getMedianHeading()
        currentHeading = initHead
        currentDistance = pi2go.getDistance()

        pid = PID(1.95, 0, 0.075, setpoint=0)
        pid.output_limits = (-(100 + speed)/2, (100 - speed)/2)
        pid.sample_time = 0.01

        changeDistance = currentDistance - distance
        lowerBound = changeDistance - 5
        upperBound  = changeDistance + 5
        while not(lowerBound <= currentDistance <= upperBound):

            change = self.heading.normaliseHeading(currentHeading - initHead)

            correction = pid(change)
            # print(f"Current heading: {currentHeading}\tChange: {change}\tCorrection: {correction}\n")
            pi2go.go(round(speed + correction), speed)
            sleep(0.5)
            pi2go.go(0,0)
            currentDistance = pi2go.getDistance()
            currentHeading = self.heading.getMedianHeading(nmax=10)

        self.updateCoordinate(initHead, distance)

    def moveToCoordinate(self, coord):
        """
        Rotates and moves towards a coordinate
        :param coord: the coordinate as (x, y) tuple
        """
        lineToCoord = Line(self.coordinate, coord)
        distance = lineToCoord.length()

        self.rotateToCoordinate(coord)
        self.forward(distance)

    def rotateToCoordinate(self, coord):
        """
        Rotates towards a given coordinate
        :param coord: coordinate as (x, y) coordinate
        """
        lineToCoord = Line(self.coordinate, coord)
        heading = lineToCoord.heading()
        currentHeading = self.heading.getMedianHeading()

        angle = self.heading.normaliseHeading(heading - currentHeading)
        self.rotateAngle(angle)

    def rotateAngle(self,deg,speed=10, tolerance=None):
        """Rotates the robot a set number of degrees from -180 to 180. Used in map.py and ...
        :param deg: number of degrees to rotate
        :param speed: the relative speed of the motors from 0 to 100
        :param tolerance: the tolerance of the angle of rotation
        """
        if deg > 180 or deg < -180:
            return

        currenthead = self.heading.getMedianHeading()
        targetHead = self.heading.normaliseHeading(currenthead + deg)

        lowerBound = targetHead - tolerance
        upperBound = targetHead + tolerance

        while not(lowerBound <= currenthead <= upperBound):
            if deg > 0:
                pi2go.go(speed, 0)
            if deg < 0:
                pi2go.go(-speed, 0)


            currenthead = self.heading.getMedianHeading(nmax=5)
            sleep(0.01)
        pi2go.go(0,0)

    def stop(self):
        """Stops the robot"""
        pi2go.go(0,0)