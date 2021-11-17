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

#include <FreeRTOS.h>
#include <os_semphr.h>
#include <os_timer.h>
#include "i2c.h"

#include "HL_i2c.h"
#include "i2c_io.h"

SemaphoreHandle_t uTransceiver_semaphore;
TimerHandle_t uTransceiverPipe_timer;

bool uhf_i2c_init() {
    uTransceiver_semaphore = xSemaphoreCreateBinary();
    if (uTransceiver_semaphore == NULL) {
        return false;
    }
    uTransceiverPipe_timer =
        xTimerCreate("uTransceiverPipe", pdMS_TO_TICKS(100), pdFALSE, NULL, uhf_pipe_timer_callback);
    if (uTransceiverPipe_timer == NULL) {
        return false;
    }
    return true;
}

bool i2c_prepare_for_pipe_mode(uint32_t timeout_ms) {
    if (xSemaphoreTake(uTransceiver_semaphore, 0) != pdTRUE) {
        // must already be in pipe mode.
        return false;
    }

    int timer_cushion = 10; // a little extra time to make sure the timer comes affer pipe mode expires.
    if (xTimerChangePeriod(uTransceiverPipe_timer, pdMS_TO_TICKS(timeout_ms + timer_cushion), 0) != pdPASS) {
        // failed to change timer period
        return false;
    }

    if (xTimerStart(uTransceiverPipe_timer, 0) != pdPASS) {
        // failed to start timer
        return false;
    }
    return true;
}

static void uhf_pipe_timer_callback(TimerHandle_t xTimer) {
    // release semaphore - safe to send over I2C again.
    xSemaphoreGive(uTransceiver_semaphore);
}

void uhf_pipe_timer_reset_from_isr(BaseType_t *xHigherPriorityTaskWoken) {
    xTimerResetFromISR(uTransceiverPipe_timer, xHigherPriorityTaskWoken);
}

bool i2c_sendCommand(uint8_t addr, char *command, uint8_t length) {
    if (xSemaphoreTake(uTransceiver_semaphore, 0) == pdTRUE) {
        return i2c_Send(I2C_BUS_REG, addr, length, command) == I2C_OK;
    }
    return false;
}

bool i2c_receiveResponse(uint8_t addr, char *response, uint8_t length) {
    if (xSemaphoreTake(uTransceiver_semaphore, 0) == pdTRUE) {
        return i2c_Receive(I2C_BUS_REG, addr, length, response) == I2C_OK;
    }
    return false;
}

bool i2c_sendAndReceive(uint8_t addr, char *command, uint8_t command_len, char *response, uint8_t response_len) {
    if (xSemaphoreTake(uTransceiver_semaphore, 0) == pdTRUE) {
        if (i2c_Send(I2C_BUS_REG, addr, command_len, command) != I2C_OK) {
            return false;
        }
        if (i2c_Receive(I2C_BUS_REG, addr, response_len, response) != I2C_OK) {
            return false;
        }
        return true;
    }
    return false;
}
