# ****************************************************
# Filename: straight.py
# Creater: Joe Hartley
# Description: Makes the pi2go robot move in a straight line. Uses accelerometer and pid controller
# ****************************************************

from simple_pid import PID
from heading import CompassHeading
import robot

def main():
    head = CompassHeading()
    rob = robot.Robot()

    pid = PID(1, 0.1, 0, setpoint=rob.initHeading)
    pid.output_limits = (-50, 50)

    try:
        while True:
            currentHeading = head.getHeading()

            correction = pid(currentHeading)
            rob.forwardUpdate(val=correction)
    except KeyboardInterrupt:
        pass
    finally:
        del rob


if __name__ == '__main__':
    main()
