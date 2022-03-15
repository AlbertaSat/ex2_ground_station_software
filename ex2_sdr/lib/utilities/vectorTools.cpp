/*!
 * @file vectorTools.cpp
 * @author Steven Knudsen
 * @date Nov. 14, 2019
 *
 * @details Implement @p vectorTools.h interface
 *
 * @copyright Xiphos Systems Corp. 2019
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#include <vectorTools.h>

namespace xiphos {
  namespace darkstar {


    VectorTools::VectorTools()
    {
    }

    VectorTools::~VectorTools() {
    }

    void
    VectorTools::floatToBytes(float threshold, bool reverseBitOrder, std::vector<float>& in, std::vector<uint8_t>& out)
    {

      out.resize(0); // lazy way to make sure we get all the bytes...

      if (reverseBitOrder) {
        for (uint32_t f = 0; f < in.size(); f += 8) {
          uint8_t byte = 0x00;
          for (uint32_t b = 0; b < 8; b++) {
            byte >>= 1;
            if (f+b < in.size()) {
              if (in[f+b] > threshold) {
                byte = byte | 0x80;
              }
              else {
                byte = byte & 0x7F;
              }
            }
          } // for 8 bits
          out.push_back(byte);
        }
      }
      else {
        for (uint32_t f = 0; f < in.size(); f += 8) {
          uint8_t byte = 0x00;
          for (uint32_t b = 0; b < 8; b++) {
            byte <<= 1;
            if (f+b < in.size()) {
              if (in[f+b] > threshold) {
                byte = byte | 0x01;
              }
              else {
                byte = byte & 0xFE;
              }
            }
          } // for 8 bits
          out.push_back(byte);
        }
      }
    } // floatToBytes

    void
    VectorTools::bytesToFloat(std::vector<uint8_t>& in, bool packed, bool lsbFirst, bool nrz, float magnitude, std::vector<float>& out)
    {
      out.resize(0);

      uint8_t byte;
      float fbit;
      for (uint32_t i = 0; i < in.size(); i++) {
        byte = in[i];
        if (packed) {
          for (uint32_t b = 0; b < 8; b++) {
            if (lsbFirst) {
              fbit = (float)(byte & 0x01);
              byte >>= 1;
            }
            else {
              fbit = (float)((byte & 0x80) >> 7);
              byte <<= 1;
            }
            if (nrz) {
              fbit = fbit*2.0 - 1.0;
            }
            fbit *= magnitude;
            out.push_back(fbit);
          } // for 8 bits per byte
        }
        else {
          if (lsbFirst) {
            fbit = (float)(byte & 0x01);
          }
          else {
            fbit = (float)((byte & 0x80) >> 7);
          }
          if (nrz) {
            fbit = fbit*2.0 - 1.0;
          }
          fbit *= magnitude;
          out.push_back(fbit);
        }
      }
    } //bytesToFloat

    void
    VectorTools::blockReverse(uint32_t blockSize, std::vector<float>& v)
    {
      if (v.size() % blockSize != 0) {
        throw std::exception(); // TODO make more descriptive
      }

      float tmp = 0.0;
      bool even = (blockSize % 2 == 0);
      for (uint32_t i = 0; i < v.size(); i += blockSize) {
        if (even) {
          for (uint32_t j = 0; j < blockSize/2; j++) {
            tmp = v[blockSize - 1 - j + i];
            v[blockSize - 1 - j + i] = v[j + i];
            v[j + i] = tmp;
          }
        }
        else {
          for (uint32_t j = 0; j < (blockSize - 1)/2; j++) {
            tmp = v[blockSize - 1 - j + i];
            v[blockSize - 1 - j + i] = v[j + i];
            v[j + i] = tmp;
          }
        }
      }

    } // blockReverse

  } /* namespace darkstar */
} /* namespace xiphos */
