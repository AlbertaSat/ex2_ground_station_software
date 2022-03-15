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

#include <chrono>
#include <exception>
#include <iostream>
#include "mac.h"
#include "mac_high.h"

// TODO make this an MAC option?
// This define was used to see if a receiver benefited from a regular stream
// of packets.
#define LOG_TX_TIMES 0

namespace xiphos
{
  namespace darkstar
  {
    MACHighException::MACHighException(const std::string& message) :
        runtime_error(message)
    { }

    MAC_high::MAC_high () :
            m_currentTxFrameNumber(0),
            m_currentRxFrameNumber(0),
            m_started(false)
    {
      m_configuration = Configuration::instance();
    }

    MAC_high::~MAC_high ()
    {
    }

    /**************************************************************************
     * Application Protocol Data Unit functions
     *************************************************************************/

    void MAC_high::send(APDU& apdu)
    {
      // 1) Process the apdu and form mpdu
      PDU<uint8_t>::payload_t payload = apdu.getPayload();

      // TODO Is this efficient enough? Definitely there is a data copy that could be a problem...
      std::chrono::milliseconds timeMillis =
          std::chrono::duration_cast< std::chrono::milliseconds >(std::chrono::system_clock::now().time_since_epoch());
      uint32_t payloadBitCount = payload.size() * 8;
      MPDU mm(apdu.getFilename(), timeMillis, m_currentTxFrameNumber, payloadBitCount, payload);

      m_sendMpdu(mm);

      m_currentTxFrameNumber++;
    }

    void MAC_high::setReceiveApdu(APDU::apdu_function_t receive_apdu)
    {
      m_sendApdu = receive_apdu;
    }

    /**************************************************************************
     * MAC Protocol Data Unit functions
     *************************************************************************/
    MPDU::mpdu_function_t
    MAC_high::receiveMpdu ()
    {
      return std::bind (&MAC_high::processMpdu, this, std::placeholders::_1);
    }

    void
    MAC_high::processMpdu (
        MPDU &mpdu)
    {
      PPDU_u8::payload_t payload = mpdu.getPayload();
      MPDUHeader *h = mpdu.getMpduHeader();
      std::string obsName = h->getObservationName();
      try
      {
        APDU apdu(obsName, mpdu.getPayload());
        // Forward APDU (MPDU after processing) up
        m_sendApdu (apdu);
      }
      catch (std::range_error& re)
      {
        std::cerr << re.what() << std::endl;
      }

    } // process_mpdu

    void
    MAC_high::setSendMpdu (
        MPDU::mpdu_function_t send_mpdu)
    {
      m_sendMpdu = send_mpdu;
    }

  } /* namespace darkstar */
} /* namespace xiphos */
