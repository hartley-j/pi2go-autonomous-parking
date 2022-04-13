import robot
import heading
import pi2go

def main():
    rob = robot.Robot()
    lengthFrontToBack = 14.3
    width = 13.6
    widthWheels = 2.6

    initDistance = pi2go.getDistance() + lengthFrontToBack
    print(f"Init distance: {initDistance} \t")
    rob.forward(30, initDistance/2)
    distance = pi2go.getDistance()
    print(f"Final distance: {distance} \n")

if __name__ == '__main__':
    main()