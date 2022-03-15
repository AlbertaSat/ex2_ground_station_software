/*!
 * @file phy.cpp
 * @author Steven Knudsen
 * @date May 10, 2021
 *
 * @details The base PHY class.
 *
 * @copyright University of Alberta 2021
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */
#include "phy.hpp"

namespace ex2
{
  namespace sdr
  {

    PHY::~PHY ()
    {
    }

    PHY::PHY()
    : m_PPDUsTransmitted(0),
      m_PPDUsReceived(0)
    {
    }

    PPDU_u8::ppdu_function_t PHY::transmitPpdu()
    {
      return std::bind (&PHY::processPpdu, this, std::placeholders::_1);
    }

    void PHY::setReceivePpdu(PPDU_f::ppdu_function_t receivePpdu)
    {
      m_receivePpdu = receivePpdu;
    }

    uint32_t
    PHY::getPPDUsReceived () const
    {
      return m_PPDUsReceived;
    }

    uint32_t
    PHY::getPPDUsTransmitted () const
    {
      return m_PPDUsTransmitted;
    }

  } /* namespace sdr */
} /* namespace ex2 */
