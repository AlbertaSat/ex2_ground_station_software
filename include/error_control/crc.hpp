/*!
 * @file crc.h
 * @author Steven Knudsen
 * @date April 13, 2021
 *
 * @details CRC 16 and 32 support.
 *
 * @copyright University of Alberta 2021
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#ifndef EX2_SDR_ERROR_CONTROL_CRC_H_
#define EX2_SDR_ERROR_CONTROL_CRC_H_

#include <cstdint>
#include <boost/crc.hpp>

#include "ppdu_u8.hpp"

namespace ex2 {
  namespace sdr {

    class PPDU_u8;

    class crc
    {
    public:
      enum crc_size_t
      {
        CRC_16_BITS = 16,
        CRC_32_BITS = 32
      };

      crc ();
      virtual
      ~crc ();

      /*!
       * @brief Calculate the CRC syndrome and add to the PDU.
       *
       * @details If the CRC syndrome can be calculated, it's added to the end
       * of the PDU payload.
       *
       * @param[inout] pdu
       * @param[in] crcSize
       */
      void add(PPDU_u8 &pdu, crc_size_t crcSize);

      /*!
       * @brief Checks the PDU.
       *
       * @details If the CRC check passes, the CRC is removed from the end of
       * the PDU payload.
       *
       * @param[inout] pdu
       * @param[in] crcSize
       * @throws std::runtime_error if the CRC check fails.
       */
      void check(PPDU_u8 &pdu, crc_size_t crcSize);

    private:

      boost::crc_16_type m_crc16Impl;
      boost::crc_32_type m_crc32Impl;

      union dataSyndrome16_t {
        uint8_t lastBytes[2];
        uint16_t syndrome16;
      };

      union dataSyndrome32_t {
        uint8_t lastBytes[4];
        uint32_t syndrome32;
      };

    };

  } /* namespace sdr */
} /* namespace ex2 */

#endif /* EX2_SDR_ERROR_CONTROL_CRC_H_ */
