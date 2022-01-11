# ****************************************************
# Filename: roam
# Creater: Joe Hartley
# Description: puts the pi2go robot go into a 'roam' state; robot bounces off wall
# ****************************************************

import pi2go
from time import sleep
from icm20948 import ICM20948
import math
from simple_pid import PID
import ast
import random
from heading import compassHeading
from robot import Robot


def reverseTurn():
    pi2go.reverse(50)
    lr = random.randint(0, 10)
    if lr < 5:
        pi2go.spinRight(30)
    elif lr > 5:
        pi2go.spinLeft(30)
    sleep(random.randrange(1, 4))
    pi2go.go(0, 0)


def main():
    head = compassHeading()
    rob = Robot()

    pid = PID(1, 0.1, 0, setpoint=rob.initHeading)
    pid.output_limits = (-100, 100)

    try:
        while True:

            currentHeading = head.getHeading()

            if pi2go.getDistance() < 3 and pi2go.irCentre():
                print("Detected a wall! moving back and turning.")
                sleep(0.3)
                pi2go.go(0, 0)
                reverseTurn()
                pid.setpoint = head.getHeading()
            elif pi2go.irLeft():
                print("Detected a wall! moving back and turning.")
                sleep(0.3)
                pi2go.go(0, 0)
                reverseTurn()
                pid.setpoint = head.getHeading()
            elif pi2go.irRight():
                print("Detected a wall! moving back and turning.")
                sleep(0.3)
                pi2go.go(0, 0)
                reverseTurn()
                pid.setpoint = head.getHeading()
            else:
                correction = pid(currentHeading)
                rob.forwardUpdate(val=correction)
    except:
        pass
    finally:
        pi2go.cleanup()


if __name__ == '__main__':
    pi2go.init()
    main()
