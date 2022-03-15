/*!
 * @file app.cpp
 * @author Steven Knudsen
 * @date April 30, 2021
 *
 * @details Application layer class
 *
 * @copyright AlbertaSat 2021
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#include <functional>
#include "app.h"

namespace ex2
{
  namespace sdr
  {

    APP::APP()
    : m_apdusReceived(0),
      m_apdusSent(0)
    {
    }

    APP::~APP ()
    {
    }

    APDU::apdu_function_t APP::receiveApdu()
    {
      return std::bind (&APP::processApdu, this, std::placeholders::_1);
    }

    void APP::setSendApdu(APDU::apdu_function_t sendApdu)
    {
      m_sendApdu = sendApdu;
    }

    void APP::resetStatistics()
    {
      m_apdusReceived = 0;
    }

    unsigned long APP::getApdusReceived() const
    {
      return m_apdusReceived;
    }

    unsigned long APP::getApdusSent() const
    {
      return m_apdusSent;
    }

  } /* namespace ex2 */
} /* namespace sdr */
