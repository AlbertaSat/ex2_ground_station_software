/*
 * i2c.c
 *
 *  Created on: Feb 17, 2021
 *      Author: thomas
 */

#include "i2c.h"

#include "HL_i2c.h"
#include "i2c_io.h"

void i2c_sendCommand(uint8_t length, char* start, char* response,
                     uint8_t addr) {
  // TODO: make this use error code return
  i2cBASE_t* regset = i2cREG1;

  i2c_Send(regset, addr, length, start);

  i2c_Receive(regset, addr, 100, response);
}
