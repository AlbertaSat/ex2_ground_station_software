/*
 * i2c.c
 *
 *  Created on: Feb 17, 2021
 *      Author: thomas
 */

#include "HL_i2c.h"
#include "i2c.h"
#include "i2c_io.h"

void i2c_sendCommand(uint8_t addr, char * command, uint8_t length){
    i2c_Send(I2C_BUS_REG, addr, length, command);
}

void i2c_receiveResponse(uint8_t addr, char * response, uint8_t length){
    i2c_Receive(I2C_BUS_REG, addr, length, response);
}

void i2c_sendAndReceive(uint8_t addr, char * command, uint8_t command_len, char * response, uint8_t response_len){
    i2c_sendCommand(addr, command, command_len);
    i2c_receiveResponse(addr, response, response_len);
}
