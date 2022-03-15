/*!
 * @file frameheader.cpp
 * @author Steven Knudsen
 * @date April 30, 2021
 *
 * @details
 *
 * @copyright AlbertaSat 2021
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#include "golay.h"
#include "mpduHeader.hpp"
#include "rfMode.hpp"

namespace ex2 {
  namespace sdr {

    MPDUHeaderException::MPDUHeaderException(const std::string& message) :
       runtime_error(message) { }

    MPDUHeader::MPDUHeader(const RF_Mode::RF_ModeNumber modulation,
      const ErrorCorrection::ErrorCorrectionScheme errorCorrectionScheme,
      const uint8_t codewordFragmentIndex,
      const uint16_t userPacketLength,
      const uint8_t userPacketFragmentIndex) :
          m_rfModeNumber(modulation),
          m_errorCorrectionScheme(errorCorrectionScheme),
          m_codewordFragmentIndex(codewordFragmentIndex),
          m_userPacketLength(userPacketLength),
          m_userPacketFragmentIndex(userPacketFragmentIndex)
    {
      // Set and encode the MAC header bytes
      m_headerPayload.resize(9,0);

      encodeMACHeader();

      m_headerValid = true;
    }

    MPDUHeader::MPDUHeader (std::vector<uint8_t> &packet){

      m_headerPayload.resize(9,0);

      if (decodeMACHeader(packet, true)) {
        // The header may be valid, but if there were more than 4 errors in the
        // Golay codewords, we will have a false positive result. We can check
        // a little more by making sure the FEC scheme is possible

        // Any rfMode value is valid, so not worth checking.

        if (m_errorCorrectionScheme != ErrorCorrection::ErrorCorrectionScheme::NO_FEC &&
            m_errorCorrectionScheme >= ErrorCorrection::ErrorCorrectionScheme::LAST) {
          // The header is bad
          throw MPDUHeaderException("MPDUHeader: Bad transparent mode packet data; ErrorCorrectionScheme not allowed.");
        }

        // Last thing to check is the size of the packet. The first byte should
        // be 128 for a transparent mode packet, but since it's not protected,
        // it may not be 128 and we still have a transparent mode packet. Can
        // only check the received packet length
        if (packet.size() != 129) {
          throw MPDUHeaderException("MPDUHeader: Bad transparent mode packet length; ");
        }

      }

    }

    MPDUHeader::MPDUHeader (MPDUHeader& header)
    {
      m_rfModeNumber = header.m_rfModeNumber;
      m_errorCorrectionScheme = header.m_errorCorrectionScheme;
      m_codewordFragmentIndex = header.m_codewordFragmentIndex;
      m_userPacketLength = header.m_userPacketLength;
      m_userPacketFragmentIndex = header.m_userPacketFragmentIndex;
      m_headerValid = header.m_headerValid;
      m_headerPayload = header.m_headerPayload;
    }

    MPDUHeader::~MPDUHeader() {
      // TODO Auto-generated destructor stub
    }

    bool
    MPDUHeader::decodeMACHeader(std::vector<uint8_t> &packet,
      bool dataField1Included) {
      // The Golay-encoded MAC Header comprises 3, 3-byte codewords.
      // Decode the codewords and if all decode properly, return true

      uint16_t headerStart = 0;
      if (dataField1Included) headerStart++;

      // Remember, the first byte is the Data Field 1, the packet length
      // Decode the first 3 bytes (24 bits)
      uint32_t recd = ((packet[headerStart++] << 16) & 0x00FF0000);
      recd = recd | ((packet[headerStart++] << 8 ) & 0x0000FF00);
      recd = recd | (packet[headerStart++] & 0x000000FF);
      int16_t decodedFirst = golay_decode(recd);

      if (decodedFirst < 0) {
        // there were 4 errors in the codeword, so we know it's bad
        return false;
      }

      // Decode the middle 3 bytes (24 bits)
      recd = ((packet[headerStart++] << 16) & 0x00FF0000);
      recd = recd | ((packet[headerStart++] << 8 ) & 0x0000FF00);
      recd = recd | (packet[headerStart++] & 0x000000FF);
      int16_t decodedSecond = golay_decode(recd);

      if (decodedSecond < 0) {
        // there were 4 errors in the codeword, so we know it's bad
        return false;
      }

      // Decode the last 3 bytes (24 bits)
      recd = ((packet[headerStart++] << 16) & 0x00FF0000);
      recd = recd | ((packet[headerStart++] << 8 ) & 0x0000FF00);
      recd = recd | (packet[headerStart++] & 0x000000FF);
      int16_t decodedThird = golay_decode(recd);

      if (decodedThird < 0) {
        // there were 4 errors in the codeword, so we know it's bad
        return false;
      }

      // We may have good message bits, but if there were more than 4 errors in
      // either codeword, we won't know. That has to be checked outside of here.

      // decodedFirst comprises from msb to lsb rfMode, fecScheme, and 3 msb of
      // codeword fragment index
      // decodedSecond comprises the 4 lsb of codeword fragment index and 8 msb
      // of user packet length.
      // decodedThird comprises 4 lsb of user packet length and the 8 bits of
      // user packet fragment index
      m_rfModeNumber =
          static_cast<RF_Mode::RF_ModeNumber>((decodedFirst >> 9) & 0x0007); // 3 bits
      m_errorCorrectionScheme =
          static_cast<ErrorCorrection::ErrorCorrectionScheme>((decodedFirst >> 3) & 0x003F); // 6 bits
      m_codewordFragmentIndex = (decodedFirst & 0x0007) << 4;     // top 3 bits
      m_codewordFragmentIndex |= ((decodedSecond >> 8) & 0x000F); // bottom 4 bits
      m_userPacketLength = (decodedSecond & 0x00FF) << 4;         // top 8 bits
      m_userPacketLength |= ((decodedThird >> 8) & 0x000F);       // bottom 4 bits
      m_userPacketFragmentIndex = decodedThird & 0x00FF;

      return true;
    } // decodeMACHeader

    void
    MPDUHeader::encodeMACHeader() {
      // Unfortunately, the fields of the header do not line up along 12 bit
      // boudaries, so a bit of bit shifting is needed to get things right.
      uint16_t msgBits = ((uint16_t) m_rfModeNumber << 9) & 0x0E00; // 3 bits
      msgBits = msgBits | (((uint16_t) m_errorCorrectionScheme << 3) & 0x01F8); // 6 bits
      msgBits = msgBits | ((m_codewordFragmentIndex >> 4) & 0x0007); // top 3 bits

      uint32_t codeword = golay_encode(msgBits);

      m_headerPayload[2] = (uint8_t)(codeword & 0x000000FF);
      codeword >>= 8;
      m_headerPayload[1] = (uint8_t)(codeword & 0x000000FF);
      codeword >>= 8;
      m_headerPayload[0] = (uint8_t)(codeword & 0x000000FF);

      msgBits = 0;
      msgBits = (m_codewordFragmentIndex << 8) & 0x00000F00;        // bottom 4 bits
      msgBits = msgBits | ((m_userPacketLength >> 4) & 0x000000FF); // top 8 bits

      codeword = golay_encode(msgBits);

      m_headerPayload[5] = (uint8_t)(codeword & 0x000000FF);
      codeword >>= 8;
      m_headerPayload[4] = (uint8_t)(codeword & 0x000000FF);
      codeword >>= 8;
      m_headerPayload[3] = (uint8_t)(codeword & 0x000000FF);

      msgBits = 0;
      msgBits = (m_userPacketLength << 8) & 0x00000F00;
      msgBits = msgBits | (m_userPacketFragmentIndex & 0x000000FF);

      codeword = golay_encode(msgBits);

      m_headerPayload[8] = (uint8_t)(codeword & 0x000000FF);
      codeword >>= 8;
      m_headerPayload[7] = (uint8_t)(codeword & 0x000000FF);
      codeword >>= 8;
      m_headerPayload[6] = (uint8_t)(codeword & 0x000000FF);
    } // encodeMACHeader


  } /* namespace sdr */
} /* namespace ex2 */
