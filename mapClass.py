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
        # When the main program wants to map, Map will be called and the procedure in this function will be run

    def takeDistanceAngle(self):
        data = (self.robot.heading.getHeading(), pi2go.getDistance())
        return data

    def getCoordinates(self, angles):
        coordinates = []

        for i in angles:
            angle = float(i[0])
            distance = float(i[1])
            xCoord, yCoord = 0, 0

            if 0 <= angle <= 90:  # In +x and +y quadrant
                theta = math.radians(angle)
                yCoord = distance * math.cos(theta)
                xCoord = distance * math.sin(theta)
            elif 90 < angle <= 180:  # In +x and -y quadrant
                theta = math.radians(angle - 90)
                yCoord = -(distance * math.sin(theta))
                xCoord = distance * math.cos(theta)
            elif 0 > angle >= -90:  # In the -x and +y quadrant
                theta = math.radians(abs(angle))
                yCoord = distance * math.cos(theta)
                xCoord = -(distance * math.sin(theta))
            elif -90 > angle >= -180:  # In the -x and -y quadrant
                theta = math.radians(abs(angle + 90))
                yCoord = -(distance * math.sin(theta))
                xCoord = -(distance * math.cos(theta))

            coordinates.append((xCoord, yCoord))

        return coordinates

