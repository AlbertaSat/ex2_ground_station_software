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
#include <FreeRTOS.h>
#include <stdint.h>
#include <stdbool.h>
#include <os_portmacro.h>
#include <os_timer.h>
#include "HL_i2c.h"
#include "i2c_io.h"

/**
 * @brief Initialize the UHF I2C system. This includes the semaphore for the
 * pipe mode, and timer. Does not actually initialize the I2C bus.
 *
 * @return true If initialization was successful.
 * @return false Otherwise.
 */
bool uhf_i2c_init(void);

/**
 * @brief Checks the UHF semaphore, which indicates if the transceiver is
 * busy transmitting/receiving.
 *
 * @return true If UHF is busy and will not respond to commands.
 * @return false Otherwise.
 */

bool uhf_is_busy(void);

/**
 * @brief Prepare the UHF I2C system to be put into pipe mode. This will consume the semaphore and
 * start the timer to go off when pipe mode expires.
 *
 * @note This function should be called immidiately before entering pipe mode.
 *
 * @param timeout_ms Time in ms that the pipe mode will last.
 * @return true If the system is ready to enter pipe mode.
 * @return false If consuming the semaphore, or starting the timer failed.
 */
bool i2c_prepare_for_pipe_mode(uint32_t timeout_ms);

/**
 * @brief Reset the UHF I2C pipe mode timer. This should be callled when any data is received from the UHF.
 *
 * @param xHigherPriorityTaskWoken Token to signal the scheduler that a task should be woken after ISR.
 */
void uhf_pipe_timer_reset_from_isr(BaseType_t *xHigherPriorityTaskWoken);

bool i2c_sendCommand(uint8_t addr, char *command, uint8_t length);

bool i2c_receiveResponse(uint8_t addr, char *response, uint8_t length);

bool i2c_sendAndReceive(uint8_t addr, char *command, uint8_t command_len, char *response, uint8_t response_len);

bool i2c_sendAndReceivePIPE(uint8_t addr, char *command, uint8_t command_len, char *response,
                            uint8_t response_len);

#endif /* i2c_H */
