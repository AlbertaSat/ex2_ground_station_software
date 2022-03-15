/*!
 * @file ppdu_u8.cpp
 * @author Steven Knudsen
 * @date May 10, 2021
 *
 * @details The PHY PDU class for 8-bit data.
 *
 * @copyright University of Alberta 2021
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#include "../../../include/phy_layer/pdu/ppdu_u8.hpp"

#include <algorithm>
#include <stdio.h>
#include <iostream>
#include <vector>

namespace ex2
{
  namespace sdr
  {
    PPDU_u8::PPDU_u8(const BitsPerSymbol bps) : PDU()
    {
      m_bps = bps;
      m_reversed = false;

    }

    PPDU_u8::PPDU_u8 (
        const payload_t& payload,
        const BitsPerSymbol bps) :
            PDU(payload),
                  m_bps (bps),
                  m_reversed(false)
    {
      uint8_t mask = 0x00;
      switch (bps)
      {
        case BitsPerSymbol::BPSymb_1:
          mask = 0x01;
          break;
        case BitsPerSymbol::BPSymb_2:
          mask = 0x03;
          break;
        case BitsPerSymbol::BPSymb_3:
          mask = 0x07;
          break;
        case BitsPerSymbol::BPSymb_4:
          mask = 0x0f;
          break;
        case BitsPerSymbol::BPSymb_5:
          mask = 0x1f;
          break;
        case BitsPerSymbol::BPSymb_6:
          mask = 0x3f;
          break;
        case BitsPerSymbol::BPSymb_7:
          mask = 0x7f;
          break;
        case BitsPerSymbol::BPSymb_8:
          return;
      }
      for (unsigned int i = 0; i < m_payload.size (); i++)
        m_payload[i] = m_payload[i] & mask;
    }

    PPDU_u8::~PPDU_u8 ()
    {
    }

    PPDU_u8::BitsPerSymbol
    PPDU_u8::getBps () const
    {
      return m_bps;
    }

    void
    PPDU_u8::append(PPDU_u8& ppdu)
    {
      // make sure the data are packed the same
      BitsPerSymbol originalBPS = ppdu.getBps();
      if (originalBPS != m_bps) {
        ppdu.repack(m_bps);
      }

      std::vector<uint8_t>::iterator payloadEnd = ((std::vector<uint8_t>)m_payload).end();
      std::vector<uint8_t> toAppend = ppdu.getPayload();

      ((std::vector<uint8_t>)m_payload).insert(payloadEnd, toAppend.begin(), toAppend.end());

      // If we had to repack the @p ppdu, put it back
      if (originalBPS != m_bps) {
        ppdu.repack(originalBPS);
      }
    }

    void
    PPDU_u8::append (
        const uint8_t *data,
        const size_t count)
    {
      for (size_t i = 0; i < count; i++)
      {
        m_payload.push_back (data[i]);
      }
    }

    void
    PPDU_u8::repack (
        PPDU_u8::BitsPerSymbol newBps)
    {
      // already done?
      if (m_bps == newBps) return;

      if (m_bps == BitsPerSymbol::BPSymb_8 and newBps == BitsPerSymbol::BPSymb_1)
        unpack ();
      else if (m_bps == BitsPerSymbol::BPSymb_1 and newBps == BitsPerSymbol::BPSymb_8)
        pack ();
      else
      {
        // Determine how many output bytes are needed
        unsigned int packedBitsCount = m_payload.size () * m_bps;
        div_t symbs = div (packedBitsCount, newBps);
        unsigned int repackedCount = symbs.quot;
        if (symbs.rem > 0) repackedCount++;

        payload_t repackedPayload (repackedCount);
        payload_t::pointer packedData = m_payload.data ();

        uint8_t packedSymb = 0;
        uint8_t repackedSymb = 0;

        unsigned int packedSymbsProcessed = 0;
        unsigned int packedBitsProcessed = 0;
        unsigned int repackedSymbsProcessed = 0;
        unsigned int repackedBitsProcessed = 0;
        uint8_t mask;

        for (unsigned int bits = 0; bits < packedBitsCount; bits++)
        {
          repackedSymb <<= 1;

          if (packedBitsProcessed == 0) // new packed symbol
            packedSymb = packedData[packedSymbsProcessed++];

          mask = m_bps - packedBitsProcessed - 1;
          repackedSymb |= (packedSymb >> mask) & 0x01;

          if (repackedBitsProcessed == (unsigned int)(newBps - 1))
          {
            repackedPayload[repackedSymbsProcessed++] = repackedSymb;
            repackedSymb = 0;
          }

          packedBitsProcessed = (packedBitsProcessed + 1) % m_bps;
          repackedBitsProcessed = (repackedBitsProcessed + 1) % newBps;
        } // for

        if (repackedSymbsProcessed < repackedCount)
        {
          repackedSymb <<= (newBps - repackedBitsProcessed);
          repackedPayload[repackedSymbsProcessed++] = repackedSymb;
        }

        m_payload = repackedPayload;
        m_bps = newBps;
      }
    }

    void
    PPDU_u8::pack ()
    {
      // already packed?
      if (m_bps == BitsPerSymbol::BPSymb_8) return;

      // Determine how many output bytes are needed
      div_t symbs = div (m_payload.size (), 8);
      unsigned int packedCount = symbs.quot;
      if (symbs.rem > 0) packedCount++;

      payload_t packedPayload (packedCount);

      unsigned int uIdx; // unpacked index
      unsigned int pIdx; // packed index
      unsigned int bIdx; // bit index
      uint8_t packing = 0;

      bIdx = 0;
      pIdx = 0;
      for (uIdx = 0; uIdx < m_payload.size (); uIdx++)
      {
        // OR the current unpacked sample into the packing var
        packing |= (m_payload[uIdx] & 0x01);
        bIdx++;
        if (bIdx == 8) // if packing full, save it
        {
          packedPayload[pIdx] = packing;
          pIdx++;
          packing = 0;
          bIdx = 0;
        }
        else
          packing <<= 1;
      }

      // If the last byte was not full, may need an extra shift.
      // Keep in mind that there is one last shift above if symbs.rem > 0
      if (symbs.rem > 0) packedPayload[pIdx] = packing << (7 - symbs.rem);

      m_payload = packedPayload;
      m_bps = BitsPerSymbol::BPSymb_8;
    } // pack

    void
    PPDU_u8::unpack ()
    {
      // already unpacked?
      if (m_bps == BitsPerSymbol::BPSymb_1) return;

      // have to assume that all bits in a packed payload are required,
      // so the number of unpacked samples will always be a multiple of 8
      unsigned int unpackedCount = m_payload.size () * 8;
      payload_t unpackedPayload (unpackedCount);

      unsigned int uIdx = 0; // unpacked index
      uint8_t packedSample;

      for (unsigned int pIdx = 0; pIdx < m_payload.size (); pIdx++)
      {
        packedSample = m_payload[pIdx];

        // might as un-roll the loop
        unpackedPayload[uIdx++] = (packedSample >> 7) & 0x01;
        unpackedPayload[uIdx++] = (packedSample >> 6) & 0x01;
        unpackedPayload[uIdx++] = (packedSample >> 5) & 0x01;
        unpackedPayload[uIdx++] = (packedSample >> 4) & 0x01;
        unpackedPayload[uIdx++] = (packedSample >> 3) & 0x01;
        unpackedPayload[uIdx++] = (packedSample >> 2) & 0x01;
        unpackedPayload[uIdx++] = (packedSample >> 1) & 0x01;
        unpackedPayload[uIdx++] = packedSample & 0x01;
      }

      m_payload = unpackedPayload;
      m_bps = BitsPerSymbol::BPSymb_1;

    } // unpack

    void
    PPDU_u8::reverse(bool byteLevel)
    {
      BitsPerSymbol tempBPS = m_bps;
      if (!byteLevel) {
        if (tempBPS != BitsPerSymbol::BPSymb_1) {
          unpack();
        }
      }
      std::reverse(std::begin(m_payload), std::end(m_payload));
      if (!byteLevel) {
        if (tempBPS != BitsPerSymbol::BPSymb_1) {
          repack(tempBPS);
        }
      }
      m_reversed = !m_reversed;
    }

    void
    PPDU_u8::roll(uint32_t numBits, bool left)
    {
      if (numBits == 0) return;
      BitsPerSymbol tempBPS = m_bps;
      repack(BitsPerSymbol::BPSymb_1);
      uint32_t shiftPositions = numBits % m_payload.size();
      if (left) {
        std::rotate(m_payload.begin(), m_payload.begin()+shiftPositions, m_payload.end());
      } else {
        std::rotate(m_payload.begin(), m_payload.end()-shiftPositions, m_payload.end());
      }
      repack(tempBPS);
    }

  } /* namespace sdr */
} /* namespace ex2 */
