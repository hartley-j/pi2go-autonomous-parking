import pi2go
from heading import Compass
from time import sleep


def main():
    try:
        heading = Compass()
        pi2go.init()
        pi2go.spinRight(50)
        while True:
            print(heading.getHeading())
            sleep(0.25)

    except KeyboardInterrupt:
        pi2go.go(0, 0)
        pi2go.cleanup()

def currentHeading():
    try:
        heading = Compass()

        while True:
            print(heading.getHeading())
            sleep(0.01)
    except:
        del heading

def faceNorth():
    pi2go.init()
    heading = Compass()

    if heading.getHeading():
        isNotNorth = True
        pi2go.spinRight(30)
    else:
        isNotNorth = False

    while isNotNorth:
        currentHead = heading.getHeading()
        if -10 < currentHead < 10:
            break

    pi2go.go(0,0)

if __name__ == "__main__":
    faceNorth()
