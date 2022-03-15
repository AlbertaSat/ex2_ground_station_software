/*!
 * @file mac.h
 * @author Steven Knudsen
 * @date May 25, 2021
 *
 * @details The MAC class. It handles CSP packets received from the application
 * layer, processes them to make transparent more packets, and sends them to
 * the PHY. It also receives transparent mode packets, processes them, and
 * reassembles them into CSP packets to be sent to the application layer.
 *
 * @copyright University of Alberta, 2021
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#ifndef EX2_SDR_MAC_LAYER_MAC_H_
#define EX2_SDR_MAC_LAYER_MAC_H_

#include <vector>
#include <time.h>

#ifdef __cplusplus
extern "C" {
#endif

#include "csp_types.h"

#include "FreeRTOS.h"
#include "FreeRTOSConfig.h"

#include "queue.h"

#ifdef __cplusplus
}
#endif

#include "ppdu_cf.hpp"
#include "ppdu_u8.hpp"
//#include "configuration.h"
#include "mpdu.hpp"
#include "rfMode.hpp"

// For FreeRTOS queues
#define QUEUE_LENGTH ( 5 )

/* Priorities at which the tasks are created. */
#define mainQUEUE_RECEIVE_TASK_PRIORITY   ( tskIDLE_PRIORITY + 2 )
#define mainQUEUE_SEND_TASK_PRIORITY      ( tskIDLE_PRIORITY + 1 )

namespace ex2
{
  namespace sdr
  {
    /*!
     * @brief This is the Darkstar media access controller (MAC)
     * @ingroup darkstar
     *
     * @details The MAC class interfaces with the App layer to process and
     * forward received APDUs to the PHY layer as MPDUs. It interfaces with the
     * PHY layer to process received MPDUs and forward the resulting APDUs to
     * the App layer.
     *
     * The MAC comprises two components:
     * @li mac_high - an interface layer that handles Application Layer PDUs
     * @li mac_low - an interface layer that handles PHY Layer PDUs
     * The MAC configures and connects these components, sets up and presents
     * the message interfaces.
     *
     * @todo Add stack diagram?
     */
    class MAC
    {
    public:

      /*!
       * @brief Return a pointer to singleton instance of Configuration.
       *
       * @details Provides access to the Configuration.
       *
       * @warning This class may not be thread-safe.
       *
       * @param rfModeNumber The UHF radio modulation in use.
       * @param errorCorrectionScheme The FEC scheme in use.
       * @return pointer to the @p MAC instance
       */
      static MAC *
      instance (RF_Mode::RF_ModeNumber rfModeNumber,
        ErrorCorrection::ErrorCorrectionScheme errorCorrectionScheme
      );

      static MAC * instance();

      ~MAC ();

      /************************************************************************
       * Functions to handle Application Protocol Data Units
       ***********************************************************************/

      /*!
       * @brief Provide a function to send APDUs.
       *
       * @details It's assumed that an upper layer (Application) submits APDUs
       * to the MAC via @p sendApdu.
       */
      //      APDU::apdu_function_t sendApdu();

      /*!
       * @brief Set the receive APDU function.
       *
       * @details It's assumed that upper layer (Application) provides a
       * function pointer that accepts APDUs from the MAC.
       *
       * @param[in] receiveApdu Pointer to the forwarding function
       */
      //      void setReceiveApdu(APDU::apdu_function_t receiveApdu);

      /*!
       * @brief The recommended APDU payload length in bytes.
       *
       * @details If possible, the application should send APDUs of this payload
       * length. Obviously, it's very likely the final APDU will be shorter, but
       * when the MAC @p stop() or @p flush() methods are called.
       *
       * @return recommended APDU payload length in bytes.
       */
      //      uint32_t apduPayloadLength() const;

      /************************************************************************
       * Functions to handle PHY Protocol Data Units to/from the lower layer
       ***********************************************************************/

      /*!
       * @brief Set the send PPDU function.
       *
       * @details It's assumed that lower layer (PHY) provides a function
       * pointer that accepts PPDUs from the MAC.
       *
       * @param[in] sendPpdu Pointer to the send function
       */
      //      void setSendPpdu(PPDU_u8::ppdu_function_t sendPpdu);

      /*!
       * @brief Provide a function to receive PPDUs.
       *
       * @details It's assumed that a lower layer (PHY) submits PPDUs to
       * the MAC via @p receivePpdu.
       *
       * @return receivePpdu Pointer to the receiving function
       */
      //      PPDU_f::ppdu_function_t receivePpdu();


      /*!
       * @brief The task that receives CSP packets via a queue from the application layer.
       *
       * @param taskParameters
       */
      static void queueReceiveTask( void *taskParameters );

      /*!
       * @brief The task that sends CSP packets via a queue to the application layer.
       *
       * @param taskParameters
       */
      static void queueSendTask( void *taskParameters );

      QueueHandle_t
      getSendQueueHandle () const
      {
        return xSendQueue;
      }

      QueueHandle_t
      getRecvQueueHandle () const
      {
        return xRecvQueue;
      }

    private:

      static MAC* m_instance;

      QueueHandle_t xSendQueue = NULL;
      QueueHandle_t xRecvQueue = NULL;

      /*!
       * @brief Constructor
       *
       * @param rfModeNumber The UHF radio modulation in use.
       * @param errorCorrectionScheme The FEC scheme in use.
       */
      MAC (RF_Mode::RF_ModeNumber rfModeNumber,
        ErrorCorrection::ErrorCorrectionScheme errorCorrectionScheme);

      bool isESTTCPacket(std::vector<uint8_t> &packet);

      bool isAX25Packet(std::vector<uint8_t> &packet);

      void processReceivedCSP(csp_packet_t *packet);

      RF_Mode::RF_ModeNumber m_rfModeNumber;
      ErrorCorrection::ErrorCorrectionScheme m_errorCorrectionScheme;

    };

  } // namespace sdr
} // namespace ex2

#endif /* EX2_SDR_MAC_LAYER_MAC_H_ */

