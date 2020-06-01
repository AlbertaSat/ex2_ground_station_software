// uTransceiver.h
// Author: Thomas Ganley
// May 28, 2020

#ifndef UTRANSCEIVER_H
#define UTRANSCEIVER_H

#include <stdint.h>
#include <mock_i2c.h>
#include <string.h>

// Converts hex values to their ASCII characters
int convHexToASCII(int length, uint8_t * arr);
int crc32_calc(size_t length, char * cmd);
int find_blankSpace(char * string);
int check_crc32(int length, char * ans)

int set_U_control(uint8_t * array);
int get_U_control(uint8_t * array);
#endif // UTRANSCEIVER_H
