// test_uTransceiver.c
// Author: Thomas Ganley
// May 28, 2020

#include "unity.h"
#include "uTransceiver.h"
#include "mock_i2c.h"

void setUp(void)
{
}

void tearDown(void)
{
}

void test_setControl_getControl(void)
{
	uint8_t array[12] = {0,3,0,3,1,1,1,1,1,1,1,0};
	char answer[20] = "OK+WWWW CCCCCCCC\r";
	
	//* Mocking setup
	i2c_sendCommand_ExpectAnyArgs();
	i2c_sendCommand_ReturnArrayThruPtr_response(answer,strlen(answer));
	

	set_U_control(array);
}
