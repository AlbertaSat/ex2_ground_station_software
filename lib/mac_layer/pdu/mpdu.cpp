/*!
 * @file frame.cpp
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

#include "mpdu.hpp"

#include <boost/format.hpp>
#include <iostream>


namespace xiphos
{
  namespace darkstar
  {

    MPDU::MPDU (
      const std::string& observationName,
      const std::chrono::milliseconds timeMillis,
      const uint32_t frameNumber,
      const uint32_t frameLengthBits,
      const payload_t& payload) :
          PDU(payload)
    {
      Configuration *c = Configuration::instance();
      // @TODO calculate the GMT milliseconds. For now just use as provided
      ErrorCorrection ec(c->getECCoding(), c->getECRate());
      m_mpduHeader = new
          MPDUHeader(
              c->getVersion(),
              observationName,
              timeMillis,
              frameNumber,
              frameLengthBits,
              ec.scheme());
   }

    MPDU::MPDU (
      MPDUHeader& header,
      const payload_t& payload) :
          PDU(payload)
    {
      m_mpduHeader = new MPDUHeader(header);
    }

    MPDU::~MPDU ()
    {
      delete m_mpduHeader;
    }

  } /* namespace darkstar */
} /* namespace xiphos */

