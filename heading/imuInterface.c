#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "i2c-dev.h"

char filename[20];
sprintf(filename, "/dev/i2c-%d", 1);
file = open(filename, O_RD)


