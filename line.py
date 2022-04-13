
import math

class Line:
    def __init__(self, start, end):
        self.startCoord = start
        self.endCoord = end

        self.gradient = (start[1] - end[1])/(start[0] - end[0])
        self.yIntercept = -(self.gradient * start[0]) + start[1]
        self.xIntercept = (-(start[1])+(self.gradient * start[0]))/self.gradient

    def getY(self, x):
        # Returns the y value at x
        return (self.gradient * x) + self.yIntercept

    def getX(self, y):
        # Returns the x value at y
        return (y - self.yIntercept)/self.gradient

    def distanceToPoint(self, coord):
        a = -1
        b = 1/self.gradient
        c = -self.yIntercept/self.gradient
        return abs(a * coord[0] + b * coord[1] + c)/math.sqrt(a**2 + b**2)

