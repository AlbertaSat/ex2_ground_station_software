// i2c.h
// Author: Thomas Ganley
// May 13, 2020

#ifndef i2c_H
#define i2c_H

#include <stdint.h>

// Mocked i2c functions
uint8_t i2c_readRegister(uint8_t registerAddress);
void i2c_writeRegister(uint8_t registerAddress, uint8_t value);

#endif /* i2c_H */

