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

#include "uhf_uart.h"

//#define UHF_DIRECT_TX_TIMEOUT 1000
//
//static bool command_mode = false;
//
//bool uhf_enter_direct_hardware_mode() {
//
//    while (*rx_mode != KISS_MODE_NOT_STARTED) {
//        vTaskDelay(10);
//    }
//    command_mode = true;
//    return true;
//}
//
//void uhf_exit_direct_hardware_mode() {
//    command_mode = false;
//    sciReceive(CSP_SCI, sizeof(uint8_t), &incomingData);
//}
//
//int uhf_direct_send(uint32_t length, uint8_t * data) {
//    configASSERT(command_mode);
//
//    sciSend(UHF_SCI, length, data);
//    if (xSemaphoreTake(uhf_tx_semphr, UHF_DIRECT_TX_TIMEOUT) != pdTRUE) {
//        return 0;
//    }
//}
//
//int uhf_direct_sendAndReceive(uint32_t command_length, uint8_t * command, uint32_t answer_length, uint8_t * ans) {
//    configASSERT(command_mode);
//
//    uhf_direct_send(command_length, command);
//    sciReceive(UHF_SCI, answer_length, ans);
//    if (xSemaphoreTake(uhf_tx_semphr, UHF_DIRECT_TX_TIMEOUT) != pdTRUE) {
//        return 0;
//    }
//}
