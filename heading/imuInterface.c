#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "i2c-dev.h"
#include "LIS3MDL.h"
#include "LSM6DSL.h"

int file;


void openBus() {
    char filename[20];
    sprintf(filename, "/dev/i2c-%d", 1);
    file = open(filename, O_RDWR);
    if (file<0) {
        printf("Unable to open I2C bus!\n");
        exit(1);
    }
}

void selectDevice(int file, int addr)
{
	if (ioctl(file, I2C_SLAVE, addr) < 0) {
		 printf("Failed to select I2C device.\n");
	}
}

void writeMagReg(u_int8_t reg, u_int8_t value) {
    selectDevice(file, LIS3MDL_ADDRESS);
    int result = i2c_smbus_write_byte_data(file, reg, value);
    if (result  == -1) {
        printf("Failed to write to i2c mag\n");
        exit(1);
    }
}

void writeAccReg(u_int8_t reg, u_int8_t value) {
    selectDevice(file, LSM6DSL_ADDRESS);
    int result = i2c_smbus_write_byte_data(file, reg, value);
    if (result  == -1) {
        printf("Failed to write to i2c acc\n");
        exit(1);
    }
}

void readBlock(u_int8_t command, u_int8_t size, char device, u_int8_t *data) {
    if (device = 'a') {
        selectDevice(file, LSM6DSL_ADDRESS);
    } else if (device = 'm') {
        selectDevice(file, LIS3MDL_ADDRESS);
    }

    int result = i2c_smbus_read_i2c_block_data(file, command, size, data);
    if (result != size) {
       printf("Failed to read block from I2C.\n");
        exit(1);
    }
}

void readAcc(int *a) {
    u_int8_t block[6];
    selectDevice(file, LSM6DSL_ADDRESS);
    readBlock(LSM6DSL_OUTX_L_XL, sizeof(block), 'a',block);
    *a = (u_int8_t)(block[0] | block[1] << 8);
    *(a+1) = (int16_t)(block[2] | block[3] << 8);
    *(a+2) = (int16_t)(block[4] | block[5] << 8);
}

void readMag(int *m) {
    u_int8_t block[6];
    selectDevice(file, LIS3MDL_ADDRESS);
    readBlock(LIS3MDL_OUT_X_L, sizeof(block), 'm',block);
    *m = (int16_t)(block[0] | block[1] << 8);
    *(m+1) = (int16_t)(block[2] | block[3] << 8);
    *(m+2) = (int16_t)(block[4] | block[5] << 8);
}

void enableAcc() {
    writeAccReg(LSM6DSL_CTRL1_XL, 0b10011111);
    printf("ODR 3.33 kHz, +/- 8g , BW = 400hz\n");
	writeAccReg(LSM6DSL_CTRL8_XL, 0b11001000);
	printf("Low pass filter enabled, BW9, composite filter\n");
	writeAccReg(LSM6DSL_CTRL3_C, 0b01000100);
	printf("Enable Block Data update, increment during multi byte read\n");
}

void enableMag() {
    writeMagReg(LIS3MDL_CTRL_REG1, 0b11111000);
    printf("Temp sesnor enabled, High performance, ODR 80 Hz, FAST ODR disabled and Selft test disabled.\n");
	writeMagReg(LIS3MDL_CTRL_REG2, 0b01000000);
	printf("+/- 12 gauss\n");
	writeMagReg(LIS3MDL_CTRL_REG3, 0b00000000);
	printf("Continuous-conversion mode\n");
}

void calcHeading(int rawMag, int rawAcc, float *heading) {
    accXnorm = rawAcc[0]/sqrt(rawAcc[0]* rawAcc[0] + rawAcc[1] * rawAcc[1] + rawAcc[2] * rawAcc[2]);
    accYnorm = rawAcc[1]/sqrt(accRaw[0] *accRaw[0] + accRaw[1] * accRaw[1] + accRaw[2] * accRaw[2]);
    pitch = asin(accYnorm);
    roll = -asin(accYnorm/cos(pitch));
    magXcomp = *mag_raw*cos(pitch)+*(mag_raw+2)*sin(pitch);
    magYcomp = *mag_raw*sin(roll)*sin(pitch)+*(mag_raw+1)*cos(roll)-*(mag_raw+2)*sin(roll)*cos(pitch);

    *heading = 180*atan2(magYcomp,magXcomp)/M_PI;
    if (*heading < 0) {
        *heading += 360;
    }
}

void main() {
    openBus();

    enableAcc();
    enableMag();

    int magRaw[3];
    int accRaw[3];
    float heading;
    while(1)
    {
        readMag(magRaw);
        readAcc(accRaw);
        calcHeading(magRaw, accRaw, heading);

        printf("current heading: %i", heading);
        usleep(25000);
    }
}