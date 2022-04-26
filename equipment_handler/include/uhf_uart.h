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
 * @file uart.h
 * @author Thomas Ganley
 * @date 2021-08-23
 */

#ifndef EX2_HAL_EX2_UHF_SOFTWARE_EQUIPMENT_HANDLER_INCLUDE_UHF_UART_H_
#define EX2_HAL_EX2_UHF_SOFTWARE_EQUIPMENT_HANDLER_INCLUDE_UHF_UART_H_

#include <stdbool.h>
#include <FreeRTOS.h>
#include "system.h"
#include "HL_sci.h"
#include "uhf.h"

#define UHF_DIRECT_TX_TIMEOUT 1000

void uhf_enter_direct_command_mode(void);

void uhf_exit_direct_command_mode(void);

UHF_return uhf_uart_init(void);

UHF_return uhf_uart_sendAndReceive(uint8_t *command, uint8_t command_len, uint8_t *ans, uint8_t ans_len);

UHF_return uhf_command_mode_callback(uint8_t ans_byte);

#endif /* EX2_HAL_EX2_UHF_SOFTWARE_EQUIPMENT_HANDLER_INCLUDE_UHF_UART_H_ */
