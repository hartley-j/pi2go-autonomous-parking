# ****************************************************
# Filename: roam
# Creater: Joe Hartley
# Description: puts the pi2go robot go into a 'roam' state
# ****************************************************

import pi2go
from time import sleep

def reverseTurn(speed):
    pi2go.reverse(10)
    sleep(2)
    pi2go.go(50,-50)
    sleep(5)

def main():
    while True:
        pi2go.forward(50)
        sleep(3)
        if pi2go.irAll():
            pi2go.go(0)
            reverseTurn()
        else:
            pass



if __name__ == '__main__':
    try:
        main()
    except:
        pi2go.cleanup()