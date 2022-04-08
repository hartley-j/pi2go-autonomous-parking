#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "i2c-dev.h"
#include "LIS3MDL.h"
#include "LSM6DSL.h"

#define mxMax 1378
#define myMax 1211
#define mzMax 1560
#define mxMin -1846
#define myMin -1782
#define mzMin -1770

float declination = 0.58327;
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

float calcHeading(float mRaw[3], float aRaw[3]) {
    float axNorm, ayNorm, pitch, roll, myComp, mxComp, heading;

    axNorm = aRaw[0]/sqrt(aRaw[0] * aRaw[0] + aRaw[1] * aRaw[1] + aRaw[2] * aRaw[2]);
    ayNorm = aRaw[1]/sqrt(aRaw[0] * aRaw[0] + aRaw[1] * aRaw[1] + aRaw[2] * aRaw[2]);
    pitch = asin(ayNorm);
    roll = -asin(ayNorm/cos(pitch));
    mxComp = mRaw[0] * cos(pitch) + mRaw[2] * sin(pitch);
    myComp = mRaw[0] * sin(roll) * sin(pitch) + mRaw[1] * cos(roll) - mRaw[2] * sin(roll) * cos(pitch);

    heading = 180 * atan2f(myComp, mxComp)/M_PI;

    heading -= declination;

    if (heading < 0) {
        heading += 360;
    }

    return heading;
}

void main() {
    openBus();

    enableAcc();
    enableMag();

    float magRaw[3];
    float accRaw[3];
    double heading;
    int scaledMag[3];
    while(1)
    {
        readMag(magRaw);
        readAcc(accRaw);

        magRaw[0] -= (mxMin + mxMax) /2 ;
        magRaw[1] -= (myMin + myMax) /2 ;
        magRaw[2] -= (mzMin + mzMax) /2 ;

        scaledMag[0]  = (float)(magRaw[0] - mxMin) / (mxMax - mxMin) * 2 - 1;
        scaledMag[1]  = (float)(magRaw[1] - myMax) / (myMax - myMin) * 2 - 1;
        scaledMag[2]  = (float)(magRaw[2] - mzMin) / (mzMax - mzMin) * 2 - 1;

        heading = calcHeading(scaledMag, accRaw);

        printf("Mag X: %d\tMag Y: %d\tMag Z: %d", scaledMag[0], scaledMag[1],scaledMag[2]);
        printf("current heading: %d\n", heading);
        usleep(250000);
    }
}