// test_uTransceiver.c
// Author: Thomas Ganley
// May 28, 2020

#include "unity.h"
#include "uTransceiver.h"

void setUp(void)
{
}

void tearDown(void)
{
}

void test_setControl_getControl(void)
{
	uint8_t array[12] = {0,3,0,3,1,1,1,1,1,1,1,0};
	set_U_control(array);
}
