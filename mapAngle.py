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

mag = []
angles = []

try:
    pi2go.spinRight(25)
    angles.append(head.getHeading())
    mag.append(head.getMag())
    while True:
        angles.append(head.getHeading())
        mag.append(head.getMag())
        time.sleep(0.1)

except KeyboardInterrupt:
    pi2go.go(0,0)

    with open('test.csv','w') as f:
        for i in range(len(angles)):
            f.write("%s, %s, %s\n" % (i, angles[i], mag[i]))

    del head