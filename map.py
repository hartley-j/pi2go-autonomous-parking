# ****************************************************
# Filename: map.py
# Creater: Joe
# Description: Program to find the equation of the four walls around the robot
# ****************************************************

import numpy as np
import robot
import heading
import pi2go

def getEquation(heading, distance):
    x = np.linspace(-100, 100, 400)

def main():
    rob = robot.Robot()
    head = heading.CompassHeading()
    a = True
    averagerps = 0.599

    angles = {}

    pi2go.turnleft(50)

    while a:
        angles[head.getHeading()] = pi2go.getDistance()
        sleep(0.5)



if __name__ == '__main__':
    main()
