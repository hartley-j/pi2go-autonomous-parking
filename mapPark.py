import robot
import heading
import pi2go

def main():
    rob = robot.Robot()
    lengthFrontToBack = 14.3
    width = 13.6
    widthWheels = 2.6

    initDistance = pi2go.getDistance() + lengthFrontToBack
    rob.forward(50, initDistance/2)
    distance = pi2go.getDistance()
    if not ((initDistance/2) -3) < distance < ((initDistance/2) + 3):
        rob.forward(40,(initDistance/2) - distance)

if __name__ == '__main__':
    main()