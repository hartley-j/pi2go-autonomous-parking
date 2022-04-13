import robot
import pi2go
from time import sleep


def main():
    """
    Function to test the distance sensor
    Pointing at a long wall and taking distance data for small increments of degrees
    """
    rob = robot.Robot()
    distances = [pi2go.getDistance()]

    for i in range(10):
        distances.append(angleDistance(5, rob))

    del rob

    return distances

def angleDistance(degrees, rob):
    rob.rotateAngle(degrees)
    sleep(1)
    return degrees, pi2go.getDistance()


if __name__ == "__main__":
    data = main()
    print(data)