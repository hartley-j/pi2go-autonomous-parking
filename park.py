import robot
from map import Map
from line import Line

def main():
    if __name__ == '__main__':
        m = Map()
        backWall, rob = m() # Calls map to get Line D and robot object

def courseCorrect(coord, rob):
    lineToCoord = Line(rob.coordinate, coord)
    targetHeading = lineToCoord.heading()


if __name__ == "__main__":
    main()