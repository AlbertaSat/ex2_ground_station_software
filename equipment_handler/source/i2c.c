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
 * @file i2c.c
 * @author Thomas Ganley
 * @date 2021-02-17
 */

#include "i2c.h"

#include "HL_i2c.h"
#include "i2c_io.h"

void i2c_sendCommand(uint8_t addr, char *command, uint8_t length) { i2c_Send(I2C_BUS_REG, addr, length, command); }

void i2c_receiveResponse(uint8_t addr, char *response, uint8_t length) {
    i2c_Receive(I2C_BUS_REG, addr, length, response);
}

void i2c_sendAndReceive(uint8_t addr, char *command, uint8_t command_len, char *response, uint8_t response_len) {
    i2c_sendCommand(addr, command, command_len);
    i2c_receiveResponse(addr, response, response_len);
}
