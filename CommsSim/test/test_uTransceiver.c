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
	char answer[20] = "OK+33FE 98876F4E\r"; // Assuming successful write
	
	//* Mocking setup
	i2c_sendCommand_ExpectAnyArgs();
	i2c_sendCommand_ReturnArrayThruPtr_response(answer,strlen(answer));

	set_U_control(array);
	
	uint8_t array2[12] ={0};
	char answer2[30] = "OK+03220133FE 0A8340A4\r"; // Assuming successful read
	i2c_sendCommand_ExpectAnyArgs();
	i2c_sendCommand_ReturnArrayThruPtr_response(answer2,strlen(answer2));

	get_U_control(array2);	

	TEST_ASSERT_EQUAL_UINT8_ARRAY(array, array2, 12);
}
