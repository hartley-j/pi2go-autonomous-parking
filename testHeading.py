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


if __name__ == "__main__":
    main()
