# ****************************************************
# Filename: testRobot.py
# Creater: Joe
# Description: Tests robot.py module
# ****************************************************

import robot
from time import sleep

@robot.handleExceptions
def main():
    rob = robot.Robot()

    for i in range(3):
        rob.forward(50)
        sleep(2)
        rob.stop()
        rob.spin(90)

if __name__ == '__main__':
    main()