// uTransceiver.h
// Author: Thomas Ganley
// May 28, 2020

#ifndef UTRANSCEIVER_H
#define UTRANSCEIVER_H

#include <stdint.h>
#include <mock_i2c.h>

#define U_WRITE_0 "ES+WAA00WWWW CCCCCCCC\r"

// Converts hex values to their ASCII characters
int convHexToASCII(int length, uint8_t * arr);
int set_U_control(uint8_t * array);
#endif // UTRANSCEIVER_H
