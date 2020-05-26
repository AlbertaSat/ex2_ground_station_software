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

void test_setControl_getControl(void)
{
	set_S_control(1,2);
	
	uint8_t pa = 0, mode = 0;
	get_S_control(&pa, &mode);

	TEST_ASSERT_EQUAL_UINT8(2, mode);
	TEST_ASSERT_EQUAL_UINT8(1, pa);
	resetTest();
}

void test_setEncoder_getEncoder(void)
{
	set_S_control(0,0); // Must be in Configuration Mode
	set_S_encoder(1,0,1,0);
	
	uint8_t scrambler = 0, filter = 0, mod = 0, rate = 0;
       	get_S_encoder(&scrambler, &filter, &mod, &rate);

	TEST_ASSERT_EQUAL_UINT8(1, scrambler);
	TEST_ASSERT_EQUAL_UINT8(0, filter);
	TEST_ASSERT_EQUAL_UINT8(1, mod);
	TEST_ASSERT_EQUAL_UINT8(0, rate);
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
	set_S_control(1,2);
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
