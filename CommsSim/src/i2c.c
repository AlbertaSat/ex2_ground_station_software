/*
 * i2c.c
 *
 *  Created on: Feb 17, 2021
 *      Author: thomas
 */

#include "HL_i2c.h"
#include "i2c.h"

void i2c_sendCommand(uint8_t addr, char * command, uint8_t length){
    i2cSetSlaveAdd(I2C_BUS_REG, addr);
    i2cSetDirection(I2C_BUS_REG, I2C_TRANSMITTER);
    i2cSetBaudrate(I2C_BUS_REG, I2C_SPEED);
    i2cSetCount(I2C_BUS_REG, length);
    i2cSetMode(I2C_BUS_REG, I2C_MASTER);
    i2cSetStop(I2C_BUS_REG);
    i2cSetStart(I2C_BUS_REG);

    while(i2cIsBusBusy(I2C_BUS_REG) == true); // This line is critical
    i2cSend(I2C_BUS_REG, length, command);

    /* Wait until Bus Busy is cleared */
    while(i2cIsBusBusy(I2C_BUS_REG) == true);

    /* Wait until Stop is detected */
    while(i2cIsStopDetected(I2C_BUS_REG) == 0);

    /* Clear the Stop condition */
    i2cClearSCD(I2C_BUS_REG);
}

void i2c_receiveResponse(uint8_t addr, char * response, uint8_t length){

    i2cSetSlaveAdd(I2C_BUS_REG, addr);
    /* Set direction to receiver */
    i2cSetDirection(I2C_BUS_REG, I2C_RECEIVER);
    i2cSetCount(I2C_BUS_REG, length);
    /* Set mode as Master */
    i2cSetMode(I2C_BUS_REG, I2C_MASTER);
    i2cSetStop(I2C_BUS_REG);
    /* Transmit command Condition */
    i2cSetStart(I2C_BUS_REG);

    while(i2cIsBusBusy(I2C_BUS_REG) == true);
    i2cReceive(I2C_BUS_REG, length, response);

    /* Wait until Bus Busy is cleared */
    while(i2cIsBusBusy(I2C_BUS_REG) == true);

    /* Wait until Stop is detected */
    while(i2cIsStopDetected(I2C_BUS_REG) == 0);

    /* Clear the Stop condition */
    i2cClearSCD(I2C_BUS_REG);
}

void i2c_sendAndReceive(uint8_t addr, char * command, uint8_t command_len, char * response, uint8_t response_len){
    i2c_sendCommand(addr, command, command_len);
    i2c_receiveResponse(addr, response, response_len);
}
