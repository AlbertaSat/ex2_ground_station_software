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
 * @file uhf_i2c.c
 * @author Thomas Ganley
 * @date 2021-02-17
 */

#include "uhf_i2c.h"

SemaphoreHandle_t uTransceiver_semaphore;
TimerHandle_t uTransceiverPipe_timer;

static const bool I2C_OK = 0;

static void uhf_pipe_timer_callback(TimerHandle_t xTimer) {
    // release semaphore - safe to send over I2C again.
    xSemaphoreGive(uTransceiver_semaphore);
}

UHF_return uhf_i2c_init(void) {
    uTransceiver_semaphore = xSemaphoreCreateMutex();
    if (uTransceiver_semaphore == NULL) {
        return U_I2C_FAIL;
    }
    xSemaphoreGive(uTransceiver_semaphore);

    uTransceiverPipe_timer =
        xTimerCreate("uTransceiverPipe", pdMS_TO_TICKS(100), pdFALSE, NULL, uhf_pipe_timer_callback);
    if (uTransceiverPipe_timer == NULL) {
        return U_I2C_FAIL;
    }
    return U_I2C_SUCCESS;
}

bool uhf_is_busy(void) {
    if (xSemaphoreTake(uTransceiver_semaphore, 0) == pdTRUE) {
        xSemaphoreGive(uTransceiver_semaphore);
        return false;
    }
    return true;
}

UHF_return i2c_prepare_for_pipe_mode(uint32_t timeout_ms) {
    if (xSemaphoreTake(uTransceiver_semaphore, 0) != pdTRUE) {
        // the UHF must already be in pipe mode.
        return U_I2C_FAIL;
    }

    const int timer_cushion_ms = 1000; // a little extra time to make sure the timer comes after pipe mode expires.
    if (xTimerChangePeriod(uTransceiverPipe_timer, pdMS_TO_TICKS(timeout_ms + timer_cushion_ms), 0) != pdPASS) {
        // failed to change timer period
        return U_I2C_FAIL;
    }
    if (xTimerStart(uTransceiverPipe_timer, 0) != pdPASS) {
        // failed to start timer
        return U_I2C_FAIL;
    }
    return U_I2C_SUCCESS;
}

void uhf_pipe_timer_reset_from_isr(BaseType_t *xHigherPriorityTaskWoken) {
    xTimerResetFromISR(uTransceiverPipe_timer, xHigherPriorityTaskWoken);
}

UHF_return i2c_sendCommand(uint8_t addr, char *command, uint8_t length) {
    if (xSemaphoreTake(uTransceiver_semaphore, 0) == pdTRUE) {
        // TODO: Fix error return once I2C send returns properly
        bool result = (i2c_Send(UHF_I2C, addr, length, command) == I2C_OK);
        xSemaphoreGive(uTransceiver_semaphore);
        return result;
    }
    return U_I2C_FAIL;
}

UHF_return i2c_receiveResponse(uint8_t addr, char *response, uint8_t length) {
    if (xSemaphoreTake(uTransceiver_semaphore, 0) == pdTRUE) {
        // TODO: Fix error return once I2C send returns properly
        bool result = (i2c_Receive(UHF_I2C, addr, length, response) == I2C_OK);
        xSemaphoreGive(uTransceiver_semaphore);
        return result;
    }
    return U_I2C_FAIL;
}

UHF_return i2c_sendAndReceive(uint8_t addr, char *command, uint8_t command_len, char *response,
                              uint8_t response_len) {
    if (xSemaphoreTake(uTransceiver_semaphore, 0) == pdTRUE) {
        if (i2c_Send(UHF_I2C, addr, command_len, command) != I2C_OK) {
            xSemaphoreGive(uTransceiver_semaphore);
            return U_I2C_FAIL;
        }
        xSemaphoreGive(uTransceiver_semaphore);
    }
    if (xSemaphoreTake(uTransceiver_semaphore, 0) == pdTRUE) {
        if (i2c_Receive(UHF_I2C, addr, response_len, response) != I2C_OK) {
            xSemaphoreGive(uTransceiver_semaphore);
            return U_I2C_FAIL;
        }
        xSemaphoreGive(uTransceiver_semaphore);
        return U_I2C_SUCCESS;
    }
    return U_I2C_IN_PIPE;
}

UHF_return i2c_sendAndReceivePIPE(uint8_t addr, char *command, uint8_t command_len, char *response,
                                  uint8_t response_len) {
    uint32_t pipe_timeout = 0;
    HAL_UHF_getPipeT(&pipe_timeout);
    if (i2c_prepare_for_pipe_mode(1000 * pipe_timeout)) {
        if (i2c_Send(UHF_I2C, addr, command_len, command) != I2C_OK) {
            xSemaphoreGive(uTransceiver_semaphore);
            return U_I2C_FAIL;
        }
        if (i2c_Receive(UHF_I2C, addr, response_len, response) != I2C_OK) {
            xSemaphoreGive(uTransceiver_semaphore);
            return U_I2C_FAIL;
        }
        return U_I2C_SUCCESS;
    } else {
        ex2_log("Error preparing for pipe mode.");
    }
    xSemaphoreGive(uTransceiver_semaphore);
    return U_I2C_FAIL;
}
