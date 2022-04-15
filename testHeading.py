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

    if heading.getHeading() != 0:
        isNorth = False
        pi2go.spinRight(35)
    else:
        isNorth = True

    while not isNorth:
        currentHead = heading.getHeading()
        print(currentHead)
        if -10 < currentHead < 10:
            break

    pi2go.go(0,0)

def captureHeadingUncertainty():
    '''
    Capture data by manually pointing the pi2go in N-E-S-W directions, and capturing x number of heading observations
    - How many observations of heading do we need in order to have a stable heading value?
    - Is median or mean the best measure?
    '''

    # On the pi2go, run the following code:
    # python calibrateIMU.py



if __name__ == "__main__":
    faceNorth()
