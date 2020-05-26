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
int add_vBuffer(int);
int transmit_vBuffer(int);
void empty_vBuffer(void);
//* Simulated register functions
int read_reg(uint8_t, uint8_t *);
int write_reg(uint8_t, uint8_t);

// Internal bit manipulation functions
uint16_t append_bytes(uint8_t, uint8_t);
float b_Temp(uint16_t);

// External access/control functions

int get_S_control(uint8_t * pa, uint8_t * mode);

int set_S_control(uint8_t new_pa, uint8_t new_mode);

int get_S_encoder(uint8_t * scrambler, uint8_t * filter, uint8_t * mod, uint8_t * rate);

int set_S_encoder(uint8_t new_scrambler, uint8_t new_filter, uint8_t new_mod, uint8_t new_rate);

int get_S_paPower(uint8_t * power);

int set_S_paPower(uint8_t new_paPower);

int get_S_frequency(float * freq);

int set_S_frequency(float new_frequency);

int softResetFPGA(void);

int get_S_firmwareVersion(float * version);

int get_S_status(uint8_t * stat);

int get_S_TR(int * transmit);

int get_S_bufferUnderrun(uint16_t * underrun);

int get_S_bufferOverrun(uint16_t * overrun);

int get_S_bufferCount(uint16_t * count);

int get_S_hk(float * arr);

#endif /* STRANSMITTER_H */
