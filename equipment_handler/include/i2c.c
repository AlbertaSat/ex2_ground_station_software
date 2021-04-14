/*
 * i2c.c
 *
 *  Created on: Feb 17, 2021
 *      Author: thomas
 */

#include "i2c.h"

#include "HL_i2c.h"

void i2c_sendCommand(uint8_t length, char* start, char* response,
                     uint8_t addr) {
  i2cBASE_t* regset = i2cREG1;

  i2cSetSlaveAdd(regset, addr);
  i2cSetDirection(regset, I2C_TRANSMITTER);
  i2cSetBaudrate(regset, 400);  // Hardcoded
  i2cSetCount(regset, length);
  i2cSetMode(regset, I2C_MASTER);
  i2cSetStop(regset);
  i2cSetStart(regset);

  while (i2cIsBusBusy(regset) == true)
    ;  // This line is critical
  i2cSend(regset, length, start);

  /* Wait until Bus Busy is cleared */
  while (i2cIsBusBusy(regset) == true)
    ;

  /* Wait until Stop is detected */
  while (i2cIsStopDetected(regset) == 0)
    ;

  /* Clear the Stop condition */
  i2cClearSCD(regset);

  /* Change to receive mode */

  i2cSetSlaveAdd(regset, addr);
  /* Set direction to receiver */
  i2cSetDirection(regset, I2C_RECEIVER);
  i2cSetCount(regset, 100);
  /* Set mode as Master */
  i2cSetMode(regset, I2C_MASTER);
  i2cSetStop(regset);
  /* Transmit Start Condition */
  i2cSetStart(regset);

  while (i2cIsBusBusy(regset) == true)
    ;
  i2cReceive(regset, 100, response);

  /* Wait until Bus Busy is cleared */
  while (i2cIsBusBusy(regset) == true)
    ;

  /* Wait until Stop is detected */
  while (i2cIsStopDetected(regset) == 0)
    ;

  /* Clear the Stop condition */
  i2cClearSCD(regset);
}
