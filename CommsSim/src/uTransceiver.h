// uTransceiver.h
// Author: Thomas Ganley
// May 28, 2020

#ifndef UTRANSCEIVER_H
#define UTRANSCEIVER_H

#include "mock_i2c.h"
#include <stdint.h>
#include <string.h>

// Converts hex values to their ASCII characters
int convHexToASCII(int length, uint8_t * arr);
int crc32_calc(size_t length, char * cmd);
int find_blankSpace(char * string);
int check_crc32(int length, char * ans);

int generic_U_write(uint8_t code, void * param);
int generic_U_read(uint8_t code, void * param);
#endif // UTRANSCEIVER_H
