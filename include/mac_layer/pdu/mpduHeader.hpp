/*!
 * @file frameheader.h
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

#ifndef EX2_SDR_MAC_LAYER_PDU_FRAME_HEADER_H_
#define EX2_SDR_MAC_LAYER_PDU_FRAME_HEADER_H_

#include <chrono>
#include <cstdint>
#include <stdexcept>
#include <vector>

#include "error_correction.hpp"
#include "pdu.hpp"
#include "rfMode.hpp"

namespace ex2 {
  namespace sdr {

    class MPDUHeaderException: public std::runtime_error {

    public:
      MPDUHeaderException(const std::string& message);
    };

    class MPDUHeader {
    public:


      /*!
       * @brief Constructor
       *
       * @param[in] modulation The UHF radio modulation (RF mode)
       * @param[in] errorCorrectionScheme The error correction scheme
       * @param[in] codewordFragmentIndex The index of the codeword
       * @param[in] packetNumber The packet number
       */
      MPDUHeader(const RF_Mode::RF_ModeNumber modulation,
          const ErrorCorrection::ErrorCorrectionScheme errorCorrectionScheme,
          const uint8_t codewordFragmentIndex,
          const uint16_t userPacketLength,
          const uint8_t userPacketFragmentIndex);

      /*!
       * @brief Constructor
       *
       * @details Reconstitute a header object from raw (received, we assume)
       * packet. Check the data for correctness and throw an exepction if bad.
       *
       * @param[in] rawHeader
       * @throws MPDUHeaderException
       */
      MPDUHeader (std::vector<uint8_t> &packet);

      /*!
       * @brief Copy Constructor
       *
       * @param[in] header
       */
      MPDUHeader (MPDUHeader& header);

      virtual ~MPDUHeader();

      /*!
       * @brief Accessor
       * @return MAC header length in bits
       */
      static uint16_t
      MACHeaderLength ()
      {
        return k_MACHeaderLength;
      }

      uint8_t
      getMCodewordFragmentIndex () const
      {
        return m_codewordFragmentIndex;
      }

      ErrorCorrection::ErrorCorrectionScheme
      getMErrorCorrectionScheme () const
      {
        return m_errorCorrectionScheme;
      }

      const std::vector<uint8_t>&
      getMHeaderPayload () const
      {
        return m_headerPayload;
      }

      bool
      isMHeaderValid () const
      {
        return m_headerValid;
      }

      RF_Mode::RF_ModeNumber
      getMRfModeNumber () const
      {
        return m_rfModeNumber;
      }

      uint16_t
      getMUserPacketFragmentIndex () const
      {
        return m_userPacketFragmentIndex;
      }

      uint16_t
      getMUserPacketLength () const
      {
        return m_userPacketLength;
      }

    private:

      /*!
       * @details These constants are a function of the number of bits allocated
       * for their information in the header, not a function of the underlying
       * type size.
       */
      static const uint16_t k_modulation              = 3; // bits
      static const uint16_t k_FECScheme               = 6; // bits
      static const uint16_t k_modulationFECScheme     = k_modulation + k_FECScheme;
      static const uint16_t k_codewordFragmentIndex   = 7; // bits
      static const uint16_t k_userPacketLength        = 12; // bits
      static const uint16_t k_userPacketFragmentIndex = 8; // bits
      static const uint16_t k_parityBits              = 36; // bits
      static const uint16_t k_MACHeaderLength =
          k_modulationFECScheme +
          k_codewordFragmentIndex +
          k_userPacketLength +
          k_userPacketFragmentIndex;

      RF_Mode::RF_ModeNumber m_rfModeNumber;
      ErrorCorrection::ErrorCorrectionScheme m_errorCorrectionScheme;
      uint8_t  m_codewordFragmentIndex;
      uint16_t m_userPacketLength;
      uint16_t m_userPacketFragmentIndex;
      std::vector<uint8_t> m_headerPayload;

      bool m_headerValid;

      /*!
       * @brief Used to decode a raw received packet to get the MAC header
       *
       * @param packet The received transparent mode packet
       * @param dataField1Included True if Data Field 1 is the first byte
       * @return True if header decodes without errors, but could still bad because
       * if there are > 4 errors in a Golay codeword, they will not be detected
       */
      bool decodeMACHeader(std::vector<uint8_t> &packet, bool dataField1Included = true);

      void encodeMACHeader();

    };

  } /* namespace sdr */
} /* namespace ex2 */

#endif /* EX2_SDR_MAC_LAYER_PDU_FRAME_HEADER_H_ */
