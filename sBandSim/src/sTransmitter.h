// sTransmitter.h
// Author: Thomas Ganley
// May 13, 2020

#ifndef STRANSMITTER_H
#define STRANSMITTER_H

#include <stdint.h>
#define S_DATA_TIME 0.000002

typedef enum{
	FUNC_PASS  = 0,
	BAD_READ   = 1,
	BAD_WRITE  = 1,
	BAD_PARAM  = 2,
}ret_state;

//* Simulated buffer functions
ret_state add_vBuffer(int);
ret_state transmit_vBuffer(int);
void empty_vBuffer(void);

//* Simulated register functions
ret_state read_reg(uint8_t, uint8_t *);
ret_state write_reg(uint8_t, uint8_t);

// Internal bit manipulation functions
uint16_t append_bytes(uint8_t, uint8_t);
float b_Temp(uint16_t);

// External access/control functions

ret_state get_S_control(uint8_t * pa, uint8_t * mode);

ret_state set_S_control(uint8_t new_pa, uint8_t new_mode);

ret_state get_S_encoder(uint8_t * scrambler, uint8_t * filter, uint8_t * mod, uint8_t * rate);

ret_state set_S_encoder(uint8_t new_scrambler, uint8_t new_filter, uint8_t new_mod, uint8_t new_rate);

ret_state get_S_paPower(uint8_t * power);

ret_state set_S_paPower(uint8_t new_paPower);

ret_state get_S_frequency(float * freq);

ret_state set_S_frequency(float new_frequency);

ret_state softResetFPGA(void);

ret_state get_S_firmwareVersion(float * version);

ret_state get_S_status(uint8_t * pwrgd, uint8_t * txl);

ret_state get_S_TR(int * transmit);

ret_state get_S_buffer(int quantity, uint16_t * ptr);

ret_state get_S_hk(float * arr);

#endif /* STRANSMITTER_H */
