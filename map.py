# ****************************************************
# Filename: map.py
# Creater: Joe
# Description: Program to find the equation of the four walls around the robot
# ****************************************************
import math
import numpy as np
import robot
import heading
import pi2go
import ast

def collectData(filename=None):
    rob = robot.Robot()
    head = heading.Compass()
    initHeading = head.meanAngle([head.getHeading() for i in np.arange(10)])
    endHeading = head.normaliseHeading(initHeading + 45)
    currentHeading = initHeading
    print((endHeading, currentHeading))

    n = 1
    incr = 10 # in degrees
    # times = round(360/incr) + 5

    angles = []


    while (n < 100) or (currentHeading <= endHeading):
        rob.rotateAngle(incr, tolerance=5)
        currentHeading = head.meanAngle([head.getHeading() for i in np.arange(10)])
        print(f"n = {n} Current heading = {currentHeading} | {endHeading}")
        angles.append((currentHeading, pi2go.getDistance()))
        n += 1

    if filename:
        with open(filename, "w") as file:
            for line in angles:
                file.write(f"{line}\n")

    return angles

def getCoordinates(angles, readfile='map.txt', writefile='coordinates.txt'):
    coordinates = []

    if not angles:
        with open(readfile, 'r') as file:
            for line in file:
                angles.append(ast.literal_eval(line))

    for i in angles:
        angle = float(i[0])
        distance = float(i[1])
        xCoord, yCoord = 0, 0

        if 0 <= angle <= 90:  # In +x and +y quadrant
            theta = angle
            yCoord = distance * math.sin(theta)
            xCoord = distance * math.cos(theta)
        elif 90 < angle <= 180:  # In +x and -y quadrant
            theta = angle - 90
            yCoord = -(distance * math.sin(theta))
            xCoord = distance * math.cos(theta)
        elif 0 > angle >= -90:  # In the -x and +y quadrant
            theta = abs(angle)
            yCoord = distance * math.sin(theta)
            xCoord = -(distance * math.cos(theta))
        elif -90 > angle >= -180:  # In the -x and -y quadrant
            theta = abs(angle + 90)
            yCoord = -(distance * math.sin(theta))
            xCoord = -(distance * math.cos(theta))

        coordinates.append((xCoord, yCoord))

    with open(writefile, 'w') as file:
        for coord in coordinates:
            file.write(f"{coord[0]},{coord[1]}\n")

    return coordinates

if __name__ == '__main__':
    data = collectData("map.txt")
    # coords = getCoordinates([])

