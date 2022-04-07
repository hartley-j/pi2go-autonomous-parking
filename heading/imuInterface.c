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
        printf("Unable to open I2C bus!");
        exit(1);
    }
}

void writeMagReg(u_int8_t reg, u_int8_t value) {
    int result = i2c_smbus_write_byte_data(file, reg, value);
    if (result  == -1) {
        printf("Failed to write to i2c mag");
        exit(1);
    }
}

void writeAccReg(u_int8_t reg, u_int8_t value) {
    int result = i2c_smbus_write_byte_data(file, reg, value);
    if (result  == -1) {
        printf("Failed to write to i2c acc");
        exit(1);
    }
}

void readBlock(u_int8_t command, u_int8_t size, u_int8_t *data) {
    int result = i2c_smbus_read_i2c_block_data(file, command, size, data);
    if (result != size) {
       printf("Failed to read block from I2C.");
        exit(1);
    }
}

void readAcc(int *a) {
    u_int8_t block[6];
    readBlock(0x80 | LSM6DSL_OUTX_L_XL, sizeof(block), block);
    *a = (u_int8_t)(block[0] | block[1] << 8);
    *(a+1) = (int16_t)(block[2] | block[3] << 8);
    *(a+2) = (int16_t)(block[4] | block[5] << 8);
}

void readMag(int *m) {
    u_int8_t block[6];
    readBlock(0x80 | LIS3MDL_OUT_X_L, sizeof(block), block);
    *m = (int16_t)(block[0] | block[1] << 8);
    *(m+1) = (int16_t)(block[2] | block[3] << 8);
    *(m+2) = (int16_t)(block[4] | block[5] << 8);
}

void enableAcc() {
    writeAccReg(LSM6DSL_CTRL1_XL,0b10011111);
	writeAccReg(LSM6DSL_CTRL8_XL,0b11001000);
	writeAccReg(LSM6DSL_CTRL3_C,0b01000100);
}

void enableMag() {
    writeMagReg(LIS3MDL_CTRL_REG1, 0b11011100);
	writeMagReg(LIS3MDL_CTRL_REG2, 0b00100000);
	writeMagReg(LIS3MDL_CTRL_REG3, 0b00000000);
}

openBus();

enableAcc();
enableMag();

int magRaw[3];
while(1)
{
    readMag(magRaw);
    printf("magRaw X %i \tmagRaw Y %i \tmagRaw Z %i \n", magRaw[0],magRaw[1],magRaw[2]);
    usleep(25000);
}
