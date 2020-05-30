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
uint32_t crc32_calc(size_t length, const void *);
int set_U_control(uint8_t * array);
int get_U_control(uint8_t * array);
#endif // UTRANSCEIVER_H
