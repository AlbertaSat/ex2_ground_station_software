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

	uint32_t freq[2] = {0};
	char answer4[30] = "OK+02F6278F41 CC7F38DE\r";
	i2c_sendCommand_ExpectAnyArgs();
	i2c_sendCommand_ReturnArrayThruPtr_response(answer4, strlen(answer4));
	generic_U_read(1, freq);

	TEST_ASSERT_UINT32_WITHIN(1000, new_freq, freq[0]);
}

void test_readUptimeTransmittedReceivedError(void)
{
	uint32_t value = 0;

	uint8_t answer5[30] = "OK+0200A201F3 E7CB498E\r";
	i2c_sendCommand_ExpectAnyArgs();
	i2c_sendCommand_ReturnArrayThruPtr_response(answer5, strlen(answer5));
	generic_U_read(2, &value);
	TEST_ASSERT_EQUAL_UINT32(0x00A201F3, value);

	uint8_t answer6[30] = "OK+0201B30029 500C26FF\r";
	i2c_sendCommand_ExpectAnyArgs();
	i2c_sendCommand_ReturnArrayThruPtr_response(answer6, strlen(answer6));
	generic_U_read(3, &value);
	TEST_ASSERT_EQUAL_UINT32(0x01B30029, value);

	uint8_t answer7[30] = "OK+03A190013D 37A57297\r";
	i2c_sendCommand_ExpectAnyArgs();
	i2c_sendCommand_ReturnArrayThruPtr_response(answer7, strlen(answer7));
	generic_U_read(4, &value);
	TEST_ASSERT_EQUAL_UINT32(0xA190013D, value);

	uint8_t answer8[30] = "OK+A23265D948 23C2F404\r";
	i2c_sendCommand_ExpectAnyArgs();
	i2c_sendCommand_ReturnArrayThruPtr_response(answer8, strlen(answer8));
	generic_U_read(5, &value);
	TEST_ASSERT_EQUAL_UINT32(0x3265D948, value);
	
}

void test_setPIPEtimeout_getPIPEtimeout(void)
{
	uint8_t time = 45;
	uint8_t read_time = 0;

	uint8_t answer9[30] = "OK D736D92D\r";
	i2c_sendCommand_ExpectAnyArgs();
	i2c_sendCommand_ReturnArrayThruPtr_response(answer9, strlen(answer9));
	generic_U_write(6, &time);

	uint8_t answer10[30] = "OK+3D0000002D B10BF78C\r";
	i2c_sendCommand_ExpectAnyArgs();
	i2c_sendCommand_ReturnArrayThruPtr_response(answer10, strlen(answer10));
	generic_U_read(6, &read_time);

	TEST_ASSERT_EQUAL_UINT8(time, read_time);
}

void test_setDefaultValues(void)
{
	uint8_t conf = 1;
	uint8_t answer11[20] = "OK D736D92D\r";
	i2c_sendCommand_ExpectAnyArgs();
	i2c_sendCommand_ReturnArrayThruPtr_response(answer11, strlen(answer11));
	generic_U_write(9, &conf);
}

void test_readInternalTempSensor(void)
{	
	float temp = 0;
	uint8_t answer12[20] = "OK -018 131D221A\r";
	i2c_sendCommand_ExpectAnyArgs();
	i2c_sendCommand_ReturnArrayThruPtr_response(answer12, strlen(answer12));
	generic_U_read(10, &temp);
        
	TEST_ASSERT_FLOAT_WITHIN(0.01, -1.8f, temp);	
}
