/*!
 * @file scrambler.cpp
 * @author Steven Knudsen
 * @date June 28, 2019
 *
 * @details
 *
 * @copyright Xiphos Systems Corp. 2019
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#include "scrambler.hpp"

namespace ex2 {
  namespace sdr {

    Scrambler::Scrambler(uint64_t polynomial,
        uint64_t initialRegisterFill) {
      m_lfsr = new GaloisLFSR(polynomial, initialRegisterFill);
    }

    Scrambler::~Scrambler() {
      delete m_lfsr;
    }

    void
    Scrambler::scramble(PPDU_u8::payload_t& original,
        PPDU_u8::payload_t& scrambled)
    {
      if (original.size() != scrambled.size()) {
        scrambled.resize(original.size());
      }

      for (uint32_t i = 0; i < original.size(); i++) {
        uint8_t lfsrByte = m_lfsr->nextByte();
        scrambled[i] = lfsrByte ^ original[i];
      }
    }

    uint8_t
    Scrambler::bitReverse(uint8_t byte)
    {
      static uint8_t nibbleReverse[16]  = {0x0, 0x8, 0x4, 0xc, 0x2,
           0xa, 0x6, 0xe, 0x1, 0x9, 0x5, 0xd, 0x3, 0xb, 0x7, 0xf};

      return ((nibbleReverse[byte & 0x0f] << 4) | nibbleReverse[(byte & 0xf0) >> 4]);
    }

    void
    Scrambler::scramble(std::vector<float>& original,
        std::vector<float>& scrambled)
    {
      if (original.size() % 8 != 0) {
        //TODO make this specific
        throw std::exception();
      }

      if (original.size() != scrambled.size()) {
        scrambled.resize(original.size());
      }

      uint32_t i = 0;
      while ( i < original.size()) {
        uint8_t lfsrByte = m_lfsr->nextByte();
        lfsrByte = bitReverse(lfsrByte);
        for (uint32_t b = 0; b < 8; b++) {
          if (lfsrByte & 0x01) // if 1, then flip the symbol
            scrambled[i] = -1.0*original[i];
          else
            scrambled[i] = original[i];
          lfsrByte >>= 1;
          i++;
        }
      }

    }

    void
    Scrambler::scramble(std::vector<std::complex<float>>& original,
        std::vector<std::complex<float>>& scrambled)
    {
      if (original.size() % 8 != 0) {
        //TODO make this specific
        throw std::exception();
      }

      if (original.size() != scrambled.size()) {
        scrambled.resize(original.size());
      }

      uint32_t i = 0;
      while ( i < original.size()) {
        uint8_t lfsrByte = m_lfsr->nextByte();
        lfsrByte = bitReverse(lfsrByte);
        for (uint32_t b = 0; b < 8; b++) {
          if (lfsrByte & 0x01) // if 1, then flip the symbol
            scrambled[i] = original[i]*-1.0f;
          else
            scrambled[i] = original[i];
          lfsrByte >>= 1;
          i++;
        }
      }

    }

  } /* namespace sdr */
} /* namespace ex2 */
