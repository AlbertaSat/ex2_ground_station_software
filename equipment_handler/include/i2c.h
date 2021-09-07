/*
 * Copyright (C) 2021  University of Alberta
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 */
/**
 * @file i2c.h
 * @author Thomas Ganley
 * @date 2020-05-20
 */
#ifndef i2c_H
#define i2c_H

#include <stdint.h>

#define I2C_SPEED 400
#define I2C_BUS_REG i2cREG1

void i2c_sendCommand(uint8_t addr, char *command, uint8_t length);

void i2c_receiveResponse(uint8_t addr, char *response, uint8_t length);

void i2c_sendAndReceive(uint8_t addr, char *command, uint8_t command_len, char *response, uint8_t response_len);

#endif /* i2c_H */
