/*!
 * @file .cpp
 * @author Steven Knudsen
 * @date June 18, 2019
 *
 * @details
 *
 * @copyright Xiphos Systems Corp. 2019
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#include "crc.hpp"

#include <iostream>
#include <stdexcept>
#include <stdio.h>

//#define CRC_DEBUG 0

namespace xiphos
{
  namespace darkstar
  {

    crc::crc ()
    {
    }

    crc::~crc ()
    {
    }

    void crc::add(PPDU_u8 &pdu, crc_size_t crcSize)
    {
      PPDU_u8::data_ptr_t dPtr = pdu.m_payload.data();
      uint16_t crc16Syndrome;
      uint32_t crc32Syndrome;
      switch(crcSize)
      {
        case CRC_16_BITS:
          m_crc16Impl.reset ();
          m_crc16Impl.process_bytes(dPtr, pdu.payloadLength());
          crc16Syndrome = m_crc16Impl.checksum();
#ifdef CRC_DEBUG
          printf("crc::add crc16 syndrome   = 0x%x\n",crc16Syndrome);
#endif
          pdu.append((const unsigned char *) &crc16Syndrome, sizeof(crc16Syndrome));
          break;
        case CRC_32_BITS:
          m_crc32Impl.reset ();
          m_crc32Impl.process_bytes(dPtr, pdu.payloadLength());
          crc32Syndrome = m_crc32Impl.checksum();
#ifdef CRC_DEBUG
          printf("crc::add crc32 syndrome   = 0x%x\n",crc32Syndrome);
#endif
          pdu.append((const unsigned char *) &crc32Syndrome, sizeof(crc32Syndrome));
          break;
        default:
          break;
      }
    }

    void crc::check(PPDU_u8 &pdu, crc_size_t crcSize)
    {
      PPDU_u8::data_ptr_t dPtr = pdu.m_payload.data();
      uint16_t crc16Syndrome;
      uint32_t crc32Syndrome;
      int N = pdu.payloadLength();
      switch(crcSize)
      {
        case CRC_16_BITS:
          m_crc16Impl.reset ();
          m_crc16Impl.process_bytes(dPtr, N-sizeof(crc16Syndrome));
          crc16Syndrome = m_crc16Impl.checksum();
#ifdef CRC_DEBUG
          printf("crc::check crc16 syndrome = 0x%x\n",crc16Syndrome);
#endif
          dataSyndrome16_t ds16;
          ds16.lastBytes[1] = dPtr[N-1];
          ds16.lastBytes[0] = dPtr[N-2];
#ifdef CRC_DEBUG
          printf("crc::check data syndrome  = 0x%x\n",ds16.syndrome16);
#endif
          if (crc16Syndrome == ds16.syndrome16)
          {
            pdu.m_payload.pop_back();
            pdu.m_payload.pop_back();
          } else
            throw std::runtime_error("CRC16 check failed.");
          break;
        case CRC_32_BITS:
          m_crc32Impl.reset ();
          m_crc32Impl.process_bytes(dPtr, N-sizeof(crc32Syndrome));
          crc32Syndrome = m_crc32Impl.checksum();
#ifdef CRC_DEBUG
          printf("crc::check crc32 syndrome = 0x%x\n",crc32Syndrome);
#endif
          dataSyndrome32_t ds32;
          ds32.lastBytes[3] = dPtr[N-1];
          ds32.lastBytes[2] = dPtr[N-2];
          ds32.lastBytes[1] = dPtr[N-3];
          ds32.lastBytes[0] = dPtr[N-4];
#ifdef CRC_DEBUG
          printf("crc::check data syndrome  = 0x%x\n",ds32.syndrome32);
#endif
          if (crc32Syndrome == ds32.syndrome32)
          {
            pdu.m_payload.pop_back();
            pdu.m_payload.pop_back();
            pdu.m_payload.pop_back();
            pdu.m_payload.pop_back();
          } else
            throw std::runtime_error("CRC16 check failed.");
          break;
        default:
          break;
      }
    }

  } /* namespace darkstar */
} /* namespace xiphos */
