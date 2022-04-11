from icm20948 import ICM20948
# import pandas as pd
import math
import os

def getCalibration():

    file = 'heading/calibration.txt'
    if not os.path.isfile():
        # Run calibration
    else:
        cal = {}
        with open("heading/calibration.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                key, val = line.split(':')
                cal[key] = val.strip('\n')

    return cal


def main():
    imu = ICM20948()
    n = 0
    magData =[]
    # df = pd.DataFrame(columns=['id', 'X', 'Y', 'Z', 'X1', 'Y1', 'Z1', 'atan2'])
    try:
        while True:
            # NB: mag output is
            # mag[0] = Z
            # mag[1] = Y
            # mag[2] = X
            mag = list(imu.read_magnetometer_data())
            heading = math.atan2(mag[1], mag[2])
            # item = pd.DataFrame({'id': n, 'X': mag[0], 'Y':mag[1], 'Z':mag[2], 'X1':mag[2], 'Y1':mag[1], 'Z1':mag[0], 'atan2':heading})
            # df = pd.concat(item, df)
            print(f"{n}, {mag[0]}, {mag[1]}, {mag[2]}, {heading}")
            magData.append(f"{n}, {mag[0]}, {mag[1]}, {mag[2]}, {heading}\n")
            n += 1

    except KeyboardInterrupt:
        # df.to_csv('testICMNorth.csv')
        with open("testICMSouth.csv", "w") as f:
            for line in magData:
                f.write(line)



if __name__ == "__main__":
    main()
