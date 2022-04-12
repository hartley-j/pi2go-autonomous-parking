# ****************************************************
# Filename: map.py
# Creater: Joe
# Description: Program to find the equation of the four walls around the robot
# ****************************************************

import numpy as np
import robot
import heading
import pi2go

def main():
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


    while (n < 30) and (currentHeading >= endHeading):
        rob.rotateAngle(incr, tolerance=2)
        currentHeading = head.meanAngle([head.getHeading() for i in np.arange(10)])
        print(f"Average heading = {currentHeading} n = {n}")
        angles.append((currentHeading, pi2go.getDistance()))
        n += 1

    with open("map.txt", "w") as file:
        for line in angles:
            file.write(f"{line}\n")


if __name__ == '__main__':
    main()
