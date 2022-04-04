# ****************************************************
# Filename: mapAngle.py
# Creater: Joe
# Description: Will create a csv file of the angles as the pi2go rotates
# ****************************************************

import pi2go
import heading
import time

pi2go.init()
head = heading.CompassHeading()

mag = {}
angles = {}
n = 0

try:
    pi2go.spinRight(25)
    angles[n] = head.getHeading()
    while True:
        n += 1
        angles.update({n: head.getHeading()})
        mag.update({n: head.getMag()})
        time.sleep(0.1)

except KeyboardInterrupt:
    pi2go.go(0,0)

    with open('test.csv','w') as f:
        for key in angles.keys():
            f.write("%s, %s, %s\n" % (key, angles[key], mag[key]))

    del head