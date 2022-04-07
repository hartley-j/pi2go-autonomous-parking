#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "i2c-dev.h"


void writeMagReg(u_int8_t reg, u_int8_t value) {
    int result = i2c_smbus_write_byte_data(file, reg, value);
    if (result  == -1) {
        printf("Failed to write to i2c mag");
        exit(1);
    }
}

void accMagReg(u_int8_t reg, u_int8_t value) {
    int result = i2c_smbus_write_byte_data(file, reg, value);
    if (result  == -1) {
        printf("Failed to write to i2c acc");
        exit(1);
}

void readBlock(u_int8_t command, u_int8_t size, u_int8_t *data) {
    int result = i2c_smbus_read_i2c_block_data(file, command, size, data);
    if (result != size) {
       printf("Failed to read block from I2C.");
        exit(1);
    }
}

void readMag(int *m) {
    uint8_t block[6];
    readBlock(0x80 | OUT_X_L_M, sizeof(block), block);
    *m = (uint8_t)(block[0] | block[1] << 8);
    *(m+1) = (int16_t)(block[2] | block[3] << 8);
    *(m+2) = (int16_t)(block[4] | block[5] << 8);
}

void readAcc(int *a) {
    uint8_t block[6];
    selectDevice(file,ACC_ADDRESS);
    readBlock(0x80 | OUT_X_L_A, sizeof(block), block);
    *a = (int16_t)(block[0] | block[1] << 8);
    *(a+1) = (int16_t)(block[2] | block[3] << 8);
    *(a+2) = (int16_t)(block[4] | block[5] << 8);
}

void enableAcc() {
    writeAccReg(CTRL_REG1_XM, 0b01100111);
    /* tells accelerometer to enable all axis, set it to continous update mode and a data rate of 100 Hz */
    writeAccReg(CTRL_REG2_XM, 0b00100000);
    /* will set the accelerometer to +- gauss full scale */
}

void enableMag() {
    writeMagReg( CTRL_REG5_XM, 0b11110000);
    /* enable internal temp sensor, set mag to high resolution and set data rate of 50 Hz */
    writeMagReg( CTRL_REG6_XM, 0b01100000);
    /* set full scale selection to +- gauss */
    writeMagReg( CTRL_REG7_XM, 0b00000000);
    /* set the mag to continuous-conversion mode */
}


enableAcc();
enableMag();

int magRaw[3];
while(1) {
    readMag(magRaw);
    printf("magRaw X %i \tmagRaw Y %i \tmagRaw Z %i \n", magRaw[0],magRaw[1],magRaw[2]);
    usleep(25000);
}
