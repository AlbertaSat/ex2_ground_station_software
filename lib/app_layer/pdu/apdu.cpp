/*!
 * @file apdu.cpp
 * @author Steven Knudsen
 * @date April 30, 2021
 *
 * @details The Application PDU for CubeSat Protocol (CSP).
 *
 * @copyright AlbertaSat 2021
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#include <pdu/apdu.h>
#include <iostream>
#include <stdexcept>

namespace ex2
{
  namespace sdr
  {

    APDU::APDU (
      const std::string& filename,
      const csp_packet_t& packet)
    {
      m_packet = packet;
      m_filename = std::string(filename);
    }

    APDU::~APDU ()
    {
    }

    bool
    APDU::valid() const
    {
      // no point checking the payload as it is allowed to be empty
      return true;
    }

  } /* namespace ex2 */
} /* namespace sdr */
