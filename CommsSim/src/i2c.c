/*
 * i2c.c
 *
 *  Created on: Feb 17, 2021
 *      Author: thomas
 */

#include "HL_i2c.h"
#include "i2c.h"

#define I2C_SPEED 400

void i2c_sendCommand(uint8_t cmd_len, char * command, char * response, uint8_t response_len, uint8_t addr){
    i2cBASE_t * regset = i2cREG1;
    int i;

    i2cSetSlaveAdd(regset, addr);
    i2cSetDirection(regset, I2C_TRANSMITTER);
    i2cSetBaudrate(regset, I2C_SPEED);
    i2cSetCount(regset, cmd_len);
    i2cSetMode(regset, I2C_MASTER);
    i2cSetStop(regset);
    i2cSetStart(regset);

    while(i2cIsBusBusy(regset) == true); // This line is critical
    i2cSend(regset, cmd_len, command);

    /* Wait until Bus Busy is cleared */
    while(i2cIsBusBusy(regset) == true);

    /* Wait until Stop is detected */
    while(i2cIsStopDetected(regset) == 0);

    /* Clear the Stop condition */
    i2cClearSCD(regset);

    /* Change to receive mode */

    for (i = 0; i < 0x800000; i++);

    i2cSetSlaveAdd(regset, addr);
    /* Set direction to receiver */
    i2cSetDirection(regset, I2C_RECEIVER);
    i2cSetCount(regset, response_len);
    /* Set mode as Master */
    i2cSetMode(regset, I2C_MASTER);
    i2cSetStop(regset);
    /* Transmit command Condition */
    i2cSetStart(regset);

    while(i2cIsBusBusy(regset) == true);
    i2cReceive(regset, response_len, response);

    /* Wait until Bus Busy is cleared */
    while(i2cIsBusBusy(regset) == true);

    /* Wait until Stop is detected */
    while(i2cIsStopDetected(regset) == 0);

    /* Clear the Stop condition */
    i2cClearSCD(regset);
}


