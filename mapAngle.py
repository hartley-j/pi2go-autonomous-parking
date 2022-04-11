# ****************************************************
# Filename: mapAngle.py
# Creater: Joe
# Description: Will create a csv file of the angles as the pi2go rotates
# ****************************************************

# Imports the required packages
import pi2go
import time
from icm20948 import ICM20948

# Initialises pi2go and imu code
pi2go.init()
imu = ICM20948()

# Declares required variables
mag = []
n = 0

try:
    # Turns pi2go at a constant speed clockwise
    pi2go.spinRight(80)

    # Takes raw magnetometer data and appends to mag list
    init_data = list(imu.read_magnetometer_data())
    init_data.append(n)
    mag.append(init_data)

    # Loops data collection forever
    while True:
        n += 1
        data = list(imu.read_magnetometer_data())
        data.append(n)
        mag.append(data)
        time.sleep(0.01)

# On KeyboardInterrupt, run following:
except KeyboardInterrupt:
    # Stop both motors
    pi2go.go(0,0)

    # Write raw data to csv in format: n, x, y, z
    with open('test360Spin.csv','w') as f:
        for i in mag:
            f.write(f"{i[3]}, {i[0]}, {i[1]}, {i[2]}\n")
