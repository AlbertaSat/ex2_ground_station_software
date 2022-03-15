/*!
 * @file mpdu.h
 * @author Steven Knudsen
 * @date May 25, 2021
 *
 * @details The MPDU class.
 *
 * @copyright University of Alberta, 2021
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#ifndef EX2_SDR_MAC_LAYER_PDU_FRAME_H_
#define EX2_SDR_MAC_LAYER_PDU_FRAME_H_

#include <functional>
#include <chrono>

#include "pdu.hpp"
//#include "configuration.h"
#include "mpduHeader.hpp"

namespace ex2
{
  namespace sdr
  {
    /*!
     * @brief Defines the MPDU.
     *
     * @details The MAC Protocol Data Unit (MPDU) comprises the MAC header and
     * codeword. The codeword comprises the message and parity bits, if any.
     *
     * The MAC header and codeword are contained in the Data Field 2 of the
     * transparent mode packet. The fields and their length are shown in the
     * two figures below.
     *
     * @dot
     * digraph html {
     *   packet [shape=none, margin=0, label=<
     *     <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
     *       <TR >
     *       <TD bgcolor="#aaaaaa" COLSPAN="5" Align = "Center">Data Field 2</TD>
     *       </TR>
     *       <TR >
     *       <TD bgcolor="#ffffff" COLSPAN="5" Align = "Center"></TD>
     *       </TR>
     *       <TR>
     *       <TD bgcolor="#ff7777" COLSPAN="1" Align = "Center">MAC Header (4 bytes)</TD>
     *       <TD bgcolor="#77ff77" COLSPAN="4" Align = "Center">Codeword (Message + Parity) (0 - 124 bytes)</TD>
     *       </TR>
     *     </TABLE>
     *   >];
     *  }
     * @enddot
     * The MAC header comprises
     * * the Modulation/FEC scheme (9 bits)
     *   * the Modulation (3 bits)
     *   * the FEC Scheme (6 bits)
     * * the Codeword index (7 bits), an index used to order split codewords when a FEC scheme codeword is longer than 124 bytes
     * * the Packet Number (2 bytes), an index used to order the codewords in a multi-packet transmission, such as happens when the CSP packet is longer than 124 bytes
     * @dot
     * digraph html {
     *   packet [shape=none, margin=0, label=<
     *     <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
     *       <TR >
     *       <TD bgcolor="#ff7777" COLSPAN="12" Align = "Center">MAC Header (4 bytes)</TD>
     *       </TR>
     *       <TR>
     *       <TD bgcolor="#ffffff" COLSPAN="12"></TD>
     *       </TR>
     *       <TR>
     *       <TD bgcolor="#ff7777" COLSPAN="3" Align = "Center">Modulation/FEC Scheme (9 bits)</TD>
     *       <TD bgcolor="#ff7777" COLSPAN="4" Align = "Center">Codeword Index (7 bits)</TD>
     *       <TD bgcolor="#ff7777" COLSPAN="5" Align = "Center">Packet Number (2 bytes)</TD>
     *       </TR>
     *       <TR>
     *       <TD bgcolor="#ffffff" COLSPAN="3"></TD>
     *       </TR>
     *       <TR>
     *       <TD bgcolor="#ff7777" COLSPAN="1">Modulation (4 bits)</TD>
     *       <TD bgcolor="#ff7777" COLSPAN="2">FEC Scheme (6 bits)</TD>
     *       </TR>
     *     </TABLE>
     *   >];
     *  }
     * @enddot
     *
     */
    class MPDU :
        public PDU<uint8_t>
    {
    public:

      class MPDUHeaderException: public std::runtime_error {

      public:
        MPDUHeaderException(const std::string& message);
      };

      /*!
       * @brief MPDU function type.
       */
      typedef std::function< void(MPDU&) > mpdu_function_t;

      /*!
       * @brief Constructor
       *
       * @details Used when reconstructing an MPDU based on a received
       * transparent mode packet

       * @param[in] rawPayload The received transparent mode packet
       * @note The @p rawPayload should always be 128 bytes
       */
      MPDU (
        const payload_t& rawPayload);

      /*!
       * @brief Constructor
       *
       * @param[in] header The header corresponding to this MPDU
       * @param[in] payload MAC service data unit (aka payload)
       */
      MPDU (
        MPDUHeader& header,
        const payload_t& payload);

      ~MPDU ();

      /*!
       * @brief Accessor for the payload.
       *
       * @return The payload.
       */
      const payload_t& getPayload() const {
        return m_payload;
      }

      /*!
       * @brief Accessor for MPDU header
       * @return The header.
       */
      MPDUHeader* getMpduHeader() const {
        return m_mpduHeader;
      }

    private:
      MPDUHeader *m_mpduHeader;
    };

  } // namespace sdr
} // namespace ex2

#endif /* EX2_SDR_MAC_LAYER_PDU_FRAME_H_ */

