# ****************************************************
# Filename: testRobot.py
# Creater: Joe
# Description: Tests robot.py module
# ****************************************************

import robot
import heading
from time import sleep

def main():
    rob = robot.Robot()
    head = heading.CompassHeading()

    rob.rotateAngle(90, head.getHeading())
    del rob

if __name__ == '__main__':
    main()