from map import Map
from line import Line
import pi2go

def main():
    m = Map()
    backWall, rob = m() # Calls map to get Line D and robot object

    target = backWall.midpoint()
    rob.rotateToCoordinate()

    while not isParked():
        distance = pi2go.getDistance()
        rob.forward(distance/4)
        courseCorrect(target, rob)

def courseCorrect(coord, rob):
    lineToCoord = Line(rob.coordinate, coord)
    targetHeading = lineToCoord.heading()
    currentHeading = rob.heading.getMedianHeading()

    if targetHeading - 5 < currentHeading < targetHeading + 5:
        return
    else:
        if targetHeading > currentHeading:
            angle = targetHeading - currentHeading
            rob.rotateAngle(angle)
        elif targetHeading < currentHeading:
            angle = currentHeading - targetHeading
            rob.rotateAngle(-angle)
        return

def isParked():
    if pi2go.irAll() and pi2go.getDistance() < 2:
        return True
    else:
        return False

if __name__ == "__main__":
    main()