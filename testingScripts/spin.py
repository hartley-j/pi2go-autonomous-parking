import pi2go
import time

pi2go.init()

speed = 30

try:
    while True:
        pi2go.spinLeft(speed)
        time.sleep(10)
        print(pi2go.getDistance())
        time.sleep(1)


except:
    pi2go.cleanup()

