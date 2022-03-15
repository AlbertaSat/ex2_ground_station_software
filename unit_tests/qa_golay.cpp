/*!
 * @file qa_golay.cpp
 * @author Steven Knudsen
 * @date May 28, 2021
 *
 * @details Unit test for the golay codec.
 *
 * This unit test exercises the golay codec.
 *
 * @copyright AlbertaSat 2021
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#include <cstdio>
#include <iostream>
#include <random>
#include <vector>
#include <stdio.h>
#include <stdlib.h>

#include "golay.h"

using namespace std;
//using namespace ex2::sdr;

#include "gtest/gtest.h"

/*!
 * @brief Factorial n!
 */
uint64_t factorial(uint16_t n) {
  uint64_t f = 1;
  for (uint16_t i = 0; i < n; i++) {
    f *= i;
  }
  return f;
}

uint64_t combination (uint16_t k, uint16_t n) {
  uint64_t c = factorial(n) * factorial (k - n);
  c = factorial(k) / c;
  return c;
}

/*!
 * @brief Generate an error pattern of n bits for a 24 bit word.
 *
 *
 * @param n
 * @return
 */

uint32_t nBitErrorPattern(uint8_t n) {
  uint32_t pattern = 0;

  vector<uint8_t> positions(24,0);
  uint8_t count = 0;
  while (count < n) {
    uint8_t bitPosition = random() % (24);
    if (positions[bitPosition] == 0) {
      positions[bitPosition] = 1;
      uint32_t bitPattern = (0x00000001 << bitPosition) & 0x00ffffff;
      pattern = pattern | bitPattern;
      count++;
    }
  }
  return pattern;
}

/*!
 * @brief Test correction of 3 or fewer errors.
 */
TEST(golay, CheckManyCorrectableErrors )
{
  uint16_t numTrials = 100;
  /* ---------------------------------------------------------------------
   * Confirm Golay codec corrects 1, 2, and 3 errors
   * ---------------------------------------------------------------------
   */
  srandom(time(NULL));
  /*
   * data = 12 information bits, an information polynomial i(x)
   */
  for (uint8_t numBitErrors = 1; numBitErrors <= 3; numBitErrors++) {
    for (uint16_t nt = 0; nt < numTrials; nt++) {
      // Golay encodes 12 bits
      uint16_t data = random() & 0x0fff;
      uint32_t codeword = golay_encode(data);
      // Generate the bit error pattern
      uint32_t pattern = nBitErrorPattern(numBitErrors);
      // Apply the bit error tothe codeword to get received codeword
      uint32_t recd = codeword ^ pattern;
      // Decode
      int16_t decoded = golay_decode(recd);
      printf("data     0x%08x\n", data);
      printf("codeword 0x%08x\n", codeword);
      printf("pattern  0x%08x\n", pattern);
      printf("recd     0x%08x\n", recd);
      printf("decode 0x%08x\n", decoded);
      printf("-------------------\n");
      // Check decoded is same as data
      ASSERT_TRUE(data == decoded) << "Oops, Golay failed!";
    } // num trials
  } // 1, 2, and 3 bits in error
}

/*!
 * @brief Test correction of 3 or fewer errors.
 */
TEST(golay, CheckManyUncorrectableErrors )
{
  uint16_t numTrials = 100;
  /* ---------------------------------------------------------------------
   * Confirm Golay codec corrects 1, 2, and 3 errors
   * ---------------------------------------------------------------------
   */
  srandom(time(NULL));
  /*
   * data = 12 information bits, an information polynomial i(x)
   */
  for (uint8_t numBitErrors = 4; numBitErrors <= 10; numBitErrors++) {
    for (uint16_t nt = 0; nt < numTrials; nt++) {
      // Golay encodes 12 bits
      uint16_t data = random() & 0x00000fff;
      uint32_t codeword = golay_encode(data);
      // Generate the bit error pattern
      uint32_t pattern = nBitErrorPattern(numBitErrors);
      // Apply the bit error tothe codeword to get received codeword
      uint32_t recd = codeword ^ pattern;
      printf("pattern 0x%08x codeword 0x%08x recd 0x%08x\n", pattern, codeword, recd);
      // Decode
      int16_t decoded = golay_decode(recd);
      // Check decoded is same as data
      ASSERT_TRUE(data != decoded) << "Oops, Golay succeeded correcting too many errors!";
    } // num trials
  } // 1, 2, and 3 bits in error
}
