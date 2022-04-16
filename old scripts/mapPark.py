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
    rob.forward(60, initDistance/2)
    distance = pi2go.getDistance()
    print(f"Final distance: {distance} \n")
    # if not ((initDistance/2) -3) < distance < ((initDistance/2) + 3):
    #     rob.forward(40,(initDistance/2) - distance)

if __name__ == '__main__':
    main()