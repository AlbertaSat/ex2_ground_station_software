/*
 * Copyright (C) 2015  University of Alberta
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
 * @file uTransceiver.c
 * @author Thomas Ganley
 * @date 2020-05-28
 */

#include "mock_i2c.h"
#include "unity.h"
#include "uTransceiver.h"

void setUp(void)
{
}

void tearDown(void)
{
}

void test_receiveData_sendData(void) {
  uint8_t dummy_data[128] = {0};
  receive_U_data(dummy_data);
  printf("Received data: %d %d %d %d %d ...\n", dummy_data[0], dummy_data[1],
         dummy_data[2], dummy_data[3], dummy_data[4]);
  send_U_data(dummy_data);
  printf("After transmission: %d %d %d %d %d ...\n", dummy_data[0],
         dummy_data[1], dummy_data[2], dummy_data[3], dummy_data[4]);

  TEST_IGNORE();
}

void test_setControl_getControl(void)
{
	uint8_t array[12] = {0,3,0,3,1,1,1,1,1,1,1,0};
	char answer[20] = "OK+33FE 98876F4E\r"; // Assuming successful write
	i2c_sendCommand_ExpectAnyArgs();
	i2c_sendCommand_ReturnArrayThruPtr_response(answer,strlen(answer));
	generic_U_write(0, array);

        uint8_t array2[12] = {0};
        char answer2[30] =
            "OK+03220133FE 0A8340A4\r";  // Assuming successful read
        i2c_sendCommand_ExpectAnyArgs();
        i2c_sendCommand_ReturnArrayThruPtr_response(answer2, strlen(answer2));
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

void test_readInternalTempSensor(void) {
  float temp = 0;
  uint8_t answer12[20] = "OK -018 131D221A\r";
  i2c_sendCommand_ExpectAnyArgs();
  i2c_sendCommand_ReturnArrayThruPtr_response(answer12, strlen(answer12));
  generic_U_read(10, &temp);

  TEST_ASSERT_FLOAT_WITHIN(0.01, -1.8f, temp);
}

void test_setLowPowerMode_getLowPowerMode(void)
{
	uint8_t val = 1;
        uint8_t read_val = 0;

        uint8_t answer13[30] = "OK D736D92D\r";
        i2c_sendCommand_ExpectAnyArgs();
        i2c_sendCommand_ReturnArrayThruPtr_response(answer13, strlen(answer13));
        generic_U_write(244, &val);

        uint8_t answer14[30] = "OK+01 EA147871\r";
        i2c_sendCommand_ExpectAnyArgs();
        i2c_sendCommand_ReturnArrayThruPtr_response(answer14, strlen(answer14));
        generic_U_read(244, &read_val);

        TEST_ASSERT_EQUAL_UINT8(val, read_val);
}

void test_setCallsign_getCallsign(void)
{
  uhf_configStruct callsign = {6, "VA6AZA"};
  uint8_t answer15[20] = "OK D736D92D\r";
  i2c_sendCommand_ExpectAnyArgs();
  i2c_sendCommand_ReturnArrayThruPtr_response(answer15, strlen(answer15));
  generic_U_write(246, &callsign);

  uhf_configStruct read_callsign;
  uint8_t answer16[20] = "OK+VA6AZA 04BC75E4\r";
  i2c_sendCommand_ExpectAnyArgs();
  i2c_sendCommand_ReturnArrayThruPtr_response(answer16, strlen(answer16));
  generic_U_read(246, &read_callsign);

  TEST_ASSERT_EQUAL_UINT8_ARRAY(callsign.message, read_callsign.message, 6);
}

void test_setMorseCodeCallSign_getMorseCodeCallSign(void)
{
  uhf_configStruct callsign = {14, ".-- -..--- . ."};
  uint8_t answer17[20] = "OK D736D92D\r";
  i2c_sendCommand_ExpectAnyArgs();
  i2c_sendCommand_ReturnArrayThruPtr_response(answer17, strlen(answer17));
  generic_U_write(247, &callsign);

  uhf_configStruct read_callsign;
  uint8_t answer18[30] = "OK+14.-- -..--- . . 083E3C38\r";
  i2c_sendCommand_ExpectAnyArgs();
  i2c_sendCommand_ReturnArrayThruPtr_response(answer18, strlen(answer18));
  generic_U_read(247, &read_callsign);

  TEST_ASSERT_EQUAL_UINT8_ARRAY(callsign.message, read_callsign.message, 14);
}

void test_setMidiAudioBeacon_getMidiAudioBeacon(void)
{
  uhf_configStruct beacon = {
      8,
      {42, 'w', 42, 'w', 23, 'q', 41, 'Q', 86, 'H', 87, 'H', 20, 'W', 20, 'X'}};
  uint8_t answer19[20] = "OK D736D92D\r";
  i2c_sendCommand_ExpectAnyArgs();
  i2c_sendCommand_ReturnArrayThruPtr_response(answer19, strlen(answer19));
  generic_U_write(248, &beacon);

  uhf_configStruct read_beacon;
  uint8_t answer20[40] = "OK+0842w42w23q41Q86H87H20W20X F304942B\r";
  i2c_sendCommand_ExpectAnyArgs();
  i2c_sendCommand_ReturnArrayThruPtr_response(answer20, strlen(answer20));
  generic_U_read(248, &read_beacon);

  TEST_ASSERT_EQUAL_UINT8_ARRAY(beacon.message, read_beacon.message, 16);
}

void test_getSoftwareVersion(void)
{
	uint8_t exp_version[4] = "2.06";
	uint8_t version[4] = {0};
	uint8_t answer21[40] = "OK+2.0612/11/2020,22:04 06AC1779\r";
	i2c_sendCommand_ExpectAnyArgs();
	i2c_sendCommand_ReturnArrayThruPtr_response(answer21, strlen(answer21));
	generic_U_read(249, version);

	TEST_ASSERT_EQUAL_UINT8_ARRAY(exp_version, version, 4);
}

void test_getDevicePayloadSize(void)
{
	uint8_t size = 0;
	uint8_t answer22[20] = "OK+0064 804946A5\r";
	i2c_sendCommand_ExpectAnyArgs();
	i2c_sendCommand_ReturnArrayThruPtr_response(answer22, strlen(answer22));
	generic_U_read(250, &size);

	TEST_ASSERT_EQUAL_UINT8(100, size);
}

void test_setBeaconMessageContent_getBeaconMessageContent(void)
{
  uhf_configStruct content = {
      39, {'M', 'y', ' ', 'b', 'a', 't', 't', 'e', 'r', 'y', ' ', 'i', 's',
           ' ', 'l', 'o', 'w', ' ', 'a', 'n', 'd', ' ', 'i', 't', 39,  's',
           ' ', 'g', 'e', 't', 't', 'i', 'n', 'g', ' ', 'd', 'a', 'r', 'k'}};
  uint8_t answer23[20] = "OK D736D92D\r";
  i2c_sendCommand_ExpectAnyArgs();
  i2c_sendCommand_ReturnArrayThruPtr_response(answer23, strlen(answer23));
  generic_U_write(251, &content);

  uhf_configStruct read_content;
  uint8_t answer24[150] =
      "OK+"
      "277E7E7E7E7E7E7E7E7E00564136415A41E045583132303137E103F04D79206261747465"
      "7279206973206C6F7720616E6420697427732067657474696E67206461726B "
      "B834A831\r";
  i2c_sendCommand_ExpectAnyArgs();
  i2c_sendCommand_ReturnArrayThruPtr_response(answer24, strlen(answer24));
  generic_U_read(251, &read_content);
  TEST_ASSERT_EQUAL_UINT8_ARRAY(content.message, read_content.message, 39);
}

void test_deviceAddressConfiguration(void)
{
	uint8_t answer25[20] = "OK+23 144056B1\r";
	uint8_t new_add = 0x23;
	i2c_sendCommand_ExpectAnyArgs();
	i2c_sendCommand_ReturnArrayThruPtr_response(answer25, strlen(answer25));
	generic_U_write(252, &new_add);
}

void test_setFRAM_getFRAM(void)
{
  uhf_framStruct new_write = {0x65, "ABCD"};
  uint8_t answer26[20] = "OK D736D92D\r";
  i2c_sendCommand_ExpectAnyArgs();
  i2c_sendCommand_ReturnArrayThruPtr_response(answer26, strlen(answer26));
  generic_U_write(253, &new_write);

  uhf_framStruct read;
  uint8_t answer27[50] = "OK+41424344000000000000000000000000 EA37A956\r";
  read.add = 0x65;
  i2c_sendCommand_ExpectAnyArgs();
  i2c_sendCommand_ReturnArrayThruPtr_response(answer27, strlen(answer27));
  generic_U_read(253, &read);

  TEST_ASSERT_EQUAL_UINT8_ARRAY(new_write.data, read.data, 16);
}

void test_setSecureMode_getSecureMode(void)
{
	uint8_t answer28[20] = "OK D736D92D\r";
	uint8_t confirm = 1;
	i2c_sendCommand_ExpectAnyArgs();
	i2c_sendCommand_ReturnArrayThruPtr_response(answer28, strlen(answer28));
	generic_U_write(255, &confirm);

        uint32_t key = 0;
        uint8_t answer29[25] = "OK+ABBACDDC DC9B88B5\r";
        i2c_sendCommand_ExpectAnyArgs();
        i2c_sendCommand_ReturnArrayThruPtr_response(answer29, strlen(answer29));
        generic_U_read(255, &key);

        TEST_ASSERT_EQUAL_UINT32(0xABBACDDC, key);
}

void test_genericI2C_action_no_return(void)
{
  uint8_t answer30[20] = "OK+SENT 51B42655\r";
  // TODO: UART mock
  uint8_t data[25] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25};
  generic_i2c_action('D', 0x41, 25, data, 0);
}
