import robot
import pi2go
import math

class Map:
    def __init__(self):
        self.robot = robot.Robot()

    def __del__(self):
        del self.robot

    def __call__(self, *args, **kwargs):
        pass
        # When the main program wants to map, Map will be called and the procedures in this function will be run

    def takeDistanceAngle(self):
        data = (self.robot.heading.getHeading(), pi2go.getDistance())
        return data

    def getCoordinates(self, angles):
        coordinates = []

        for i in angles:
            angle = math.radians(float(i[0]))
            distance = float(i[1])
            xCoord, yCoord = 0, 0

            xCoord = self.robot.coordinate[0] + distance * math.sin(angle)
            yCoord = self.robot.coordinate[1] + distance * math.cos(angle)

            coordinates.append((xCoord, yCoord))

        return coordinates

