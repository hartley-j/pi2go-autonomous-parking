
import math

class Line:
    def __init__(self, start, end):
        """
        Initialises the line object and defines parameters needed for calc
        :param start: start coordinate in form of tuple (x, y)
        :param end: end coordinate in form of tuple (x, y)
        """
        self.startCoord = start
        self.endCoord = end

        self.gradient = (start[1] - end[1])/(start[0] - end[0])
        self.yIntercept = -(self.gradient * start[0]) + start[1]
        self.xIntercept = (-(start[1])+(self.gradient * start[0]))/self.gradient

    def getY(self, x):
        """
        Returns the Y value of line at X
        :param x: X value
        :return: Y value
        """
        return (self.gradient * x) + self.yIntercept

    def getX(self, y):
        """
        Returns the X value at Y
        :param y: Y value
        :return: X value
        """
        return (y - self.yIntercept)/self.gradient

    def length(self):
        """
        Calculates length of line
        :return: length of line as tuple
        """
        dx = self.startCoord[0] - self.endCoord[0]
        dy = self.startCoord[1] - self.endCoord[1]
        return math.sqrt(dx**2 + dy**2)

    def midpoint(self):
        """
        Calculates midpoint of line
        :return: coordinate as tuple (x, y)
        """
        x = (self.startCoord[0] + self.startCoord[0])/2
        y = (self.startCoord[1] + self.startCoord[1])/2
        return x, y

    def distanceToPoint(self, coord):
        """
        Finds the perpendicular distance a point is from the line
        :param coord: tuple of coordinate (x, y)
        :return: perpendicular distance
        """
        a = -1
        b = 1/self.gradient
        c = -self.yIntercept/self.gradient
        return abs(a * coord[0] + b * coord[1] + c)/math.sqrt(a**2 + b**2)

    def heading(self):
        """
        Returns the heading of the line with the equation: 1/m = tan(heading)
        :return: heading as float
        """
        return math.atan(1/self.gradient)

