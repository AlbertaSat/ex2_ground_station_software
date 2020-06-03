// test_uTransceiver.c
// Author: Thomas Ganley
// May 28, 2020

#include "mock_i2c.h"
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
	char answer[20] = "OK+33FE 98876F4E\r"; // Assuming successful write
	
	//* Mocking setup
	i2c_sendCommand_ExpectAnyArgs();
	i2c_sendCommand_ReturnArrayThruPtr_response(answer,strlen(answer));

	generic_U_write(0, array);
	
	uint8_t array2[12] ={0};
	char answer2[30] = "OK+03220133FE 0A8340A4\r"; // Assuming successful read
	i2c_sendCommand_ExpectAnyArgs();
	i2c_sendCommand_ReturnArrayThruPtr_response(answer2,strlen(answer2));

	generic_U_read(0, array2);	

	TEST_ASSERT_EQUAL_UINT8_ARRAY(array, array2, 12);
}

void test_setFrequency_getFrequency(void)
{
	uint32_t new_freq = 435000000;
	char answer3[20] = "OK D736D92D\r";

	i2c_sendCommand_ExpectAnyArgs();
	i2c_sendCommand_ReturnArrayThruPtr_response(answer3, strlen(answer3));
	generic_U_write(1, &new_freq);
}
