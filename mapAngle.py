# ****************************************************
# Filename: mapAngle.py
# Creater: Joe
# Description: Will create a csv file of the angles as the pi2go rotates
# ****************************************************

import pi2go
import headingICM20948
import time
from icm20948 import ICM20948

pi2go.init()
# head = headingICM20948.CompassHeading()
imu = ICM20948()

mag = []
# angles = []
n= 0

try:
    pi2go.spinRight(25)
    mag.append(list(imu.read_magnetometer_data()))
    # angles.append(head.getHeading())
    # mag.append(head.getMag())
    while True:
        # angles.append(head.getHeading())
        mag.append(list(imu.read_magnetometer_data()).append(n))
        n += 1
        time.sleep(0.1)

except KeyboardInterrupt:
    pi2go.go(0,0)

    with open('test360Spin.csv','w') as f:
        for i in mag:
            f.write(f"{i[3]}, {i[0]}, {i[1]}, {i[2]}\n")
