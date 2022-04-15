import robot
import pi2go
import math
import time
from line import Line

class Map:
    def __init__(self):
        self.robot = robot.Robot()
        self.initHeading = self.robot.heading.getHeading()

    def __del__(self):
        del self.robot

    def __call__(self, *args, **kwargs): # When the main program wants to map, Map will be called and the procedures in this function will be run
        """
        Moves forward, takes FLR data, moves forward again, takes more data, and repeats
        Maps area to return coordinate of Dm
        :param args:
        :param kwargs:
        :return:
        """
        initDistance = pi2go.getDistance() + self.robot.lengthtoback
        self.robot.forward(initDistance/4)

        coordinateMap = list(self.sampleFLRData())

        for i in range(2):
            self.robot.forward(initDistance/4)
            sample = list(self.sampleFLRData())
            [coordinateMap[i].extend(sample[i]) for i in range(3)]

        self.robot.rotateAngle(-180)
        self.robot.forward(initDistance/4)
        self.robot.rotateAngle(-90)

        observedWalls = []
        for i in range(len(coordinateMap)):
            wall = self.getEquations(coordinateMap[i])
            observedWalls.append(wall)

    def takeDistanceAngle(self):
        """
        Measures the heading and distance from IMU and ultrasonic
        :return: tuple of (heading, distance) measured by imu and ultrasonic
        """
        data = (self.robot.heading.getHeading(), pi2go.getDistance())
        return data

    def getCoordinates(self, angles):
        """
        Calculates the coordinates of each angle against heading
        :param angles: list of tuples of (angles, distances)
        :return: list of (x, y) coordinates
        """
        coordinates = []

        for i in angles:
            angle = math.radians(float(i[0]))
            distance = float(i[1])

            xCoord = self.robot.coordinate[0] + distance * math.sin(angle)
            yCoord = self.robot.coordinate[1] + distance * math.cos(angle)

            coordinates.append((xCoord, yCoord))

        return coordinates

    def sampleDistanceAngles(self, nsamples, degrange):
        """
        :param nsamples: number of samples that will be taken
        :param degrange: the angle range of the samples (e.g. x samples over 30 degrees)
        :return: list of (angles, distances) for each sample
        """
        angleDistance = []
        angle = degrange / nsamples
        for i in range(nsamples):
            self.robot.rotateAngle(angle, tolerance=1)
            time.sleep(0.5)
            angleDistance.append(self.takeDistanceAngle())

        self.robot.rotateAngle(-degrange)
        return angleDistance

    def sampleFLRData(self):
        """
        Rotates samples coordinate data of front, left and right (FLR) of robot
        :return: list of lists of (x, y) coordinates for f, l and r
        """
        self.robot.rotateAngle(deg=90)
        data = self.sampleDistanceAngles(5, 25)
        coordinatesR = self.getCoordinates(data)

        self.robot.rotateAngle(deg=-180)
        data = self.sampleDistanceAngles(5, 25)
        coordinatesL = (self.getCoordinates(data))

        self.robot.rotateAngle(deg=90)
        data = self.sampleDistanceAngles(5, 25)
        coordinatesF = (self.getCoordinates(data))

        return coordinatesR, coordinatesL, coordinatesF

    def sampleFrontData(self):
        """
        Samples the front of robot between -30 to 30 degrees from normal to wall
        :return: list of (x, y) coordinates
        """
        self.robot.rotateAngle(deg=-30)
        data = self.sampleDistanceAngles(30, 60)
        self.robot.rotateAngle(deg=-30)

        return self.getCoordinates(data)

    def findBackWall(self, angleDistances):
        """
        Finds the start and end coordinates of the back wall of the parking space (named D)
        :param angleDistances: list of tuples of angles against distances
        :return: equation of back wall as Line object
        """

        startIndex = 0
        endIndex = 0
        tolerance = 1.5

        for i in range(len(angleDistances) - 1):
            if angleDistances[i + 1][2] > angleDistances[i][2] + tolerance:
                startIndex = i + 1
            elif angleDistances[i + 1][2] < angleDistances[i][2] - tolerance:
                endIndex = i + 1

        startCoord = self.getCoordinates(angleDistances[startIndex])
        endCoord = self.getCoordinates(angleDistances[endIndex])

        return Line(startCoord, endCoord)

    @staticmethod # Since this function does not need any instances of the class, it is static
    def getEquations(coords):
        """
        Gets the equations of all walls 'seen' by robot
        :param coords: list of ordered (x, y) coordinates
        :return: list of line objects
        """
        nWalls = 0
        wallIndex = []
        startIndex = 0
        walls = []

        for i in range(len(coords)):
            if 0 < i < (len(coords) - 1):
                line = Line(coords[startIndex], coords[i])
                distanceToNext = line.distanceToPoint(coords[i + 1])
                if distanceToNext >= 0.2:
                    wallIndex.append((startIndex, i))
                    del line
                    nWalls += 1
                    startIndex = i + 1
                else:
                    del line
            elif i == (len(coords) - 1):
                wallIndex.append((startIndex, i))
                nWalls += 1

        for i in range(len(wallIndex)):
            start = coords[wallIndex[i][0]]
            end = coords[wallIndex[i][1]]
            wall = Line(start, end)
            walls.append(wall)

        return walls