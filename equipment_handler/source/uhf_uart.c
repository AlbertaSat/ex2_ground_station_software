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
 * @file uhf_uart.c
 * @author Thomas Ganley
 * @date 2022-02-16
 */

#include <string.h>
#include "uhf_uart.h"
#include "uTransceiver.h"

static int response_index;
static uint8_t response_length;
static uint8_t response[UHF_ULTIMATE_BUFF_SIZE];

static xQueueHandle uhf_response_queue;

UHF_return uhf_uart_init(void){
    uhf_response_queue = xQueueCreate((unsigned portBASE_TYPE)3, (unsigned portBASE_TYPE)(sizeof(uint8_t) * UHF_ULTIMATE_BUFF_SIZE));
    return U_GOOD_CONFIG;
}

UHF_return uhf_uart_sendAndReceive(uint8_t *command, uint8_t command_len, uint8_t *ans, uint8_t ans_len){
    UHF_return err = U_UART_SUCCESS;
    uhf_enter_direct_command_mode();
    response_index = 0;
    response_length = ans_len;

    sciSend(UHF_SCI, command_len, command);

    uint8_t temp_ans[UHF_ULTIMATE_BUFF_SIZE];
    if(xQueueReceive(uhf_response_queue, temp_ans, portMAX_DELAY) == pdFALSE){
        err = U_UART_FAIL;
    }

    memcpy(ans, temp_ans, ans_len);
    return err;
}


UHF_return uhf_command_mode_callback(uint8_t ans_byte){
    response[response_index] = ans_byte;
    response_index++;
    portBASE_TYPE xHigherPriorityTaskWoken = pdFALSE;

    if(response_index >= response_length){
        xQueueSendToBack(uhf_response_queue, &response, &xHigherPriorityTaskWoken);
        uhf_exit_direct_command_mode();
    }
}
