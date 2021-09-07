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

bool uhf_enter_direct_hardware_mode();

void uhf_exit_direct_hardware_mode();

int uhf_direct_send(uint32_t length, uint8_t *data);

int uhf_direct_sendAndReceive(uint32_t command_length, uint8_t *command, uint32_t answer_length, uint8_t *ans);

#endif /* EX2_HAL_EX2_UHF_SOFTWARE_EQUIPMENT_HANDLER_INCLUDE_UHF_UART_H_ */
