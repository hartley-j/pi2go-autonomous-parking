# ****************************************************
# Filename: yawAngle.py
# Creator: Joe
# Description: calculates yaw angle from mpu6050
# ****************************************************

from time import sleep

import smbus

# Assigns register values to activate module
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

# Address of i2c module
address = 0x68

# Set angle to initial value of 0
angle = 0


def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg + 1)
    value = (h << 8) + l
    return value


def read_word_2c(reg):
    val = read_word(reg)
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val


if __name__ == '__main__':
    bus = smbus.SMBus(1)

    try:
        while True:
            sleep(1)
            angle += read_word_2c(0x47)
            print(angle)
    except KeyboardInterrupt:
        print("shutting down")
