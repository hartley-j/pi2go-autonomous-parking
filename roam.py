# ****************************************************
# Filename: roam
# Creater: Joe Hartley
# Description: puts the pi2go robot go into a 'roam' state
# ****************************************************

import pi2go
from time import sleep


def reverseTurn():
    pi2go.reverse(10)
    sleep(2)
    pi2go.go(50,-50)
    sleep(5)

def main(speed):
    while True:
        pi2go.forward(speed)
        print("Moving forward at speed: %s" (speed))
        sleep(3)
        if pi2go.irCentre():
            print("Detected a wall! moving back and turning.")
            pi2go.go(0,0)
            reverseTurn()
        elif pi2go.irLeft():
            print("Detected a wall! moving back and turning.")
            pi2go.go(0,0)
            reverseTurn()
        elif pi2go.irRight():
            print("Detected a wall! moving back and turning.")
            pi2go.go(0,0)
            reverseTurn()
        else:
            pass



if __name__ == '__main__':
    pi2go.init()
    try:
        main(50)
    except:
        pi2go.cleanup()