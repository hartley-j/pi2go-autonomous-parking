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
    n = 0
    incr = 5 # in degrees
    times = round(360/incr) + 5

    angles = []

    while n <= times:
        rob.rotateAngle(incr, tolerance=2)
        averageHeading = head.meanAngle([head.getHeading() for i in np.arange(10)])
        angles.append((averageHeading, pi2go.getDistance()))
        n += 1

    with open("map.txt", "w") as file:
        for line in angles:
            file.write(f"{line}\n")


if __name__ == '__main__':
    main()
