// i2c.h
// Author: Thomas Ganley
// May 13, 2020

#ifndef i2c_H
#define i2c_H

#include <stdint.h>

#define I2C_SPEED 400
#define I2C_BUS_REG i2cREG1

void i2c_sendCommand(uint8_t addr, uint8_t * command, uint8_t length);

void i2c_receiveResponse(uint8_t addr, uint8_t * response, uint8_t length);

void i2c_sendAndReceive(uint8_t addr, uint8_t * command, uint8_t command_len, uint8_t * response, uint8_t response_len);

#endif /* i2c_H */
