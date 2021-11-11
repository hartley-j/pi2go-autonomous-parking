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


class Heading:

    def __init__(self):

        global FileNotFoundError
        self.imu = ICM20948()
        self.axes = 1, 2

        try:
            FileNotFoundError
        except NameError:
            FileNotFoundError = IOError

        try:
            with open("calibrate.txt", "r") as f:
                read = f.readline()
                read.split(',')

                read = ast.literal_eval(read)
                for i in range(len(read)):
                    for l in range(len(i)):
                        read[i][l] = float(read[i][l])

                self.amax = read[0]
                self.amin = read[1]
        except FileNotFoundError:
            self.amax = self.imu.read_magnetometer_data()
            self.amin = self.imu.read_magnetometer_data()

    def getMag(self):

        mag = list(self.imu.read_magnetometer_data())

        for i in range(3):
            v = mag[i]

            if v < self.amin[i]:
                self.amin[i] = v
            elif v > self.amax[i]:
                self.amax[i] = v

            mag[i] -= self.amin[i]

            try:
                mag[i] /= self.amax[i] - self.amin[i]
            except ZeroDivisionError:
                pass

            mag[i] -= 0.5

        return mag

    def heading(self):

        mag = self.getMag()
        heading = math.atan2(mag[self.axes[0]], mag[self.axes[1]])

        if heading < 0:
            heading += 2 * math.pi

        return math.degrees(heading)


class RobotForward:

    def __init__(self, heading):
        self.heading = heading
        self.initHeading = self.heading.heading()

    def update(self, val, speed=50):
        if val != 0:
            pi2go.go(speed, (speed + val))

        return self.heading.heading()


def reverseTurn():
    pi2go.reverse(50)
    sleep(0.5)
    pi2go.spinRight(30)
    sleep(1)
    pi2go.go(0, 0)


def main():
    head = Heading()
    rob = RobotForward(head)

    pid = PID(1, 0.1, 0, setpoint=rob.initHeading)
    pid.output_limits = (-50, 50)

    try:
        while True:

            currentHeading = head.heading()

            if pi2go.getDistance() < 3 and pi2go.irCentre():
                print("Detected a wall! moving back and turning.")
                sleep(0.3)
                pi2go.go(0, 0)
                reverseTurn()
                pid.setpoint = head.heading()
            elif pi2go.irLeft():
                print("Detected a wall! moving back and turning.")
                sleep(0.3)
                pi2go.go(0, 0)
                reverseTurn()
                pid.setpoint = head.heading()
            elif pi2go.irRight():
                print("Detected a wall! moving back and turning.")
                sleep(0.3)
                pi2go.go(0, 0)
                reverseTurn()
                pid.setpoint = head.heading()
            else:
                correction = pid(currentHeading)
                rob.update(val=correction)
    except:
        pass
    finally:
        pi2go.cleanup()


if __name__ == '__main__':
    pi2go.init()
    main()
