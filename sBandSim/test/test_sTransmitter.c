// test_sTransmitter.c
// Author: Thomas Ganley
// May 13, 2020

#include "unity.h"

#include "sTransmitter.h"
#include "mock_i2c.h"
#include "mock_spi.h"
#include <stdint.h>

void setUp(void)
{
}

void tearDown(void)
{
}

void test_setControl130_getControl130(void)
{
	uint8_t new_control = 130; // Data Mode
	set_S_control(new_control);
	
	uint8_t control = 0;
	get_S_control(&control);

	TEST_ASSERT_EQUAL_UINT8(new_control, control);
	resetTest();
}

void test_setEncoder4_getEncoder4(void)
{
	uint8_t new_encoder = 4;
	set_S_control(0); // Must be in Configuration Mode
	set_S_encoder(new_encoder);
	
	uint8_t encoder = 0;
       	get_S_encoder(&encoder);

	TEST_ASSERT_EQUAL_UINT8(new_encoder, encoder);
}

void test_setPAPower26_getPAPower26(void)
{
	uint8_t new_paPower = 26;
	set_S_paPower(new_paPower);

	uint8_t power = 0;
	get_S_paPower(&power);

	TEST_ASSERT_EQUAL_UINT8(new_paPower, power);
}

void test_setFrequency_getFrequency(void)
{
	float new_frequency = 2225.5f;
	set_S_frequency(new_frequency);

	float frequency = 0;
	get_S_frequency(&frequency);

	TEST_ASSERT_FLOAT_WITHIN(0.1, new_frequency, frequency);
}

void test_PAtemp(void)
{
	float exp_temp = -50;
	float temperature = 0;
	get_S_paTemp(&temperature);
	TEST_ASSERT_FLOAT_WITHIN(0.1, exp_temp, temperature);
}
void test_putAmountBytesInBuffer(void)
{
	int amount = 10000;
	add_vBuffer(amount);
	uint16_t count = 0;
	get_S_bufferCount(&count);
	TEST_ASSERT_EQUAL_UINT16(amount, count);
}
void test_sendAmountBytesInBuffer(void)
{
	int amount = 10000;
	set_S_control(130);
	transmit_vBuffer(amount);
	uint16_t count = 0;
	get_S_bufferCount(&count);
	TEST_ASSERT_EQUAL_UINT16(0, count);
}

void test_bufferOverrun(void)
{
	empty_vBuffer();
	int amount = 20481;
	add_vBuffer(amount);
	uint16_t overrun = 0;
	get_S_bufferOverrun(&overrun);

	TEST_ASSERT_EQUAL_UINT16(1, overrun);
}
void test_bufferUnderrun()
{
	empty_vBuffer();
	int amount = 1;
	transmit_vBuffer(amount);
	uint16_t underrun = 0;
	get_S_bufferUnderrun(&underrun);

	TEST_ASSERT_EQUAL_UINT16(1, underrun);
}
