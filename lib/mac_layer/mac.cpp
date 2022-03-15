/*!
 * @file mac.cpp
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

#include "mac.hpp"

#include <functional>
#include <vector>

#ifdef __cplusplus
extern "C" {
#endif

#include "HL_sci.h"
#include "HL_reg_sci.h"
#include "queue.h"

#ifdef __cplusplus
}
#endif

#include "golay.h"
#include "mpdu.hpp"

namespace ex2 {
  namespace sdr {


    MAC* MAC::m_instance = 0;

    MAC*
    MAC::instance (RF_Mode::RF_ModeNumber rfModeNumber,
      ErrorCorrection::ErrorCorrectionScheme errorCorrectionScheme)
    {
      if (m_instance == 0)
      {
        m_instance = new MAC (rfModeNumber, errorCorrectionScheme);
      }
      return m_instance;
    }

    MAC*
    MAC::instance() {
      if (m_instance == 0)
        throw std::exception();
      return m_instance;
    }


    MAC::MAC (RF_Mode::RF_ModeNumber rfModeNumber,
      ErrorCorrection::ErrorCorrectionScheme errorCorrectionScheme) :
                      m_rfModeNumber(rfModeNumber),
                      m_errorCorrectionScheme(errorCorrectionScheme)
    {
      xSendQueue = xQueueCreate( QUEUE_LENGTH, sizeof( uint32_t ) );
      xRecvQueue = xQueueCreate( QUEUE_LENGTH, sizeof( uint32_t ) );

      if( xSendQueue != NULL )
      {
        /* Start the two tasks as described in the comments at the top of this
        file. */
        xTaskCreate( queueSendTask,     /* The function that implements the task. */
          "SendToUHF",               /* The text name assigned to the task - for debug only as it is not used by the kernel. */
          configMINIMAL_STACK_SIZE,     /* The size of the stack to allocate to the task. */
          NULL,               /* The parameter passed to the task - not used in this simple case. */
          mainQUEUE_RECEIVE_TASK_PRIORITY,/* The priority assigned to the task. */
          NULL );             /* The task handle is not required, so NULL is passed. */

      }
    }

    MAC::~MAC () { }

    void
    MAC::queueReceiveTask( void *taskParameters ) {

    }

    /*!
     * @brief The task that receives UHF radio packets, assembles them into CSP
     * packets, and sends them via a queue to the application layer.
     *
     * @details Packets come from the UHF radio via UART. They can be ESTTC or
     * transparent mode packets. ESTTC packets should be valid since they are
     * checked using the CRC16 defined for all but transparent mode packets, but
     * some simple checks should be done before passing to the application layer
     * (such as length consistency).
     *
     * Transparent mode packets are passed along regardless of the CRC16 check
     * since we employ FEC; packets may have errors and still be correctable.
     * Transparent mode packets are always 128 bytes. The MAC header is
     * protected by Golay encoding and the payload by the selected FEC scheme.
     * Thus, there is a check for length (128 bytes) and MAC header decoding
     * success.
     *
     * @param taskParameters
     */
    void
    MAC::queueSendTask( void *taskParameters ) {

      std::vector<uint8_t> uartPacket; //
      std::vector<uint8_t> cspData;
      uint16_t tmPacketIndex = 0;

      std::vector<MPDU> codewordFragments;

      // Initialize things needed to recieve transparent mode packets from the UHF radio
      bool goodUHFPacket = true;

      for( ;; )
      {

        /*!
         * Check sci for bytes. If we get some, we have to assume that the radio
         * has passed a whole packet to us.
         *
         * In transparent mode the packet is supposed to be 128 bytes long. The
         * first byte is Data Field 1, the packet length. If it is not 128, then
         * either we have an bit error in that field, or maybe a AX.25 or ESTTC
         * packet. All these possibilities must be checked.
         */

        if(sciIsRxReady(sciREG2) != 0) {

          // A new packet arrived; get all the bytes. First byte is Data Field 1
          uartPacket.resize(0);
          uint8_t data = sciReceiveByte(sciREG2);
          uartPacket.push_back(data);

          // Get the rest of the bytes
          while(sciIsRxReady(sciREG2)) {
            data = sciReceiveByte(sciREG2);
            uartPacket.push_back(data);
          }

          // Should be a complete packet in uartPacket. Get the length and check
          // if ESTTC, AX.25, or transparent mode packet.
          uint8_t packetLength = uartPacket[0];

          if (isESTTCPacket(uartPacket) || isAX25Packet(uartPacket)) {
            // Send up to the CSP server
            // TODO implement this!

          }
          else {
            // Might be a transparent mode packet. Let's try to make an MPDU
            try {
              MPDU recdMPDU(uartPacket);

            }
            catch (MPDUHeaderException& e) {
              std::cerr << e.what() << std::endl;
              throw e;
            }

          }

          // First byte we are receiving?
          if (tmPacketIndex == 0) {
            // Check for
            if (data != 128) {
              goodUHFPacket = false;
            }
            while (sciIsRxReady(sciREG2) && tmPacketIndex < 128) {
              uartPacket[tmPacketIndex] = sciReceiveByte(sciREG2);
              tmPacketIndex++;
            }
            if (!goodUHFPacket) { // could still be ESTTC
              if (uartPacket[0] == 'E' && uartPacket[1] == 'S' && uartPacket[2] == '+') {
                csp_packet_t * packet = csp_buffer_get(tmPacketIndex);
                if (packet == NULL) {
                  /* Could not get buffer element */
                  csp_log_error("Failed to get CSP buffer");
                }
                else {
                  memcpy((char *) packet->data, &uartPacket.front(), tmPacketIndex);
                  packet->length = (strlen((char *) packet->data) + 1); /* include the 0 termination */
                  // enqueue the packet
                }
              }
            }
            else {
              // decode transparent mode packet

              // check that we are expecting this packet, if we are, append the data to the payload
            }
          }
        }

        // If bytes,
        /* Send to the queue - causing the queue receive task to unblock and
        write to the console.  0 is used as the block time so the send operation
        will not block - it shouldn't need to block as the queue should always
        have at least one space at this point in the code. */
        //        xQueueSend( xQueue, &ulValueToSend, 0U );
      }

    }

    bool
    MAC::isESTTCPacket(std::vector<uint8_t> &packet) {
      bool isPacket = false;
      // First byte should be the Data Field 1, the Data Field 2 length in bytes
      // Thus, the length of packet should be the value of the first byte + 1

      if (packet[0] + 1 == packet.size()) {
        if ((packet[1] == 'E') &&
            (packet[2] == 'S') &&
            (packet[3] == '+')) {
          isPacket = true;
        }
        if ((packet[1] == 'O') &&
            (packet[2] == 'K')) {
          isPacket = true;
        }
        if ((packet[1] == '+') &&
            (packet[2] == 'E') &&
            (packet[3] == 'S')) {
          isPacket = true;
        }
        if ((packet[1] == 'E') &&
            (packet[2] == 'R') &&
            (packet[3] == 'R')) {
          isPacket = true;
        }
      } // packet length is good

      return isPacket;

    } // isESTTCPacket

    bool
    MAC::isAX25Packet(std::vector<uint8_t> &packet) {
      bool isPacket = false;
      // First byte should be the Data Field 1, the Data Field 2 length in bytes
      // Thus, the length of packet should be the value of the first byte + 1

      if (packet[0] + 1 == packet.size()) {
        // The AX.25 frame starts with 9 bytes that have the value 0x7E
        uint8_t i;
        isPacket = true;
        for (i = 1; i <= 9; i++) {
          isPacket = isPacket & (packet[i] == 0x7E);
        }
      } // packet length is good

      return isPacket;

    }

    void processReceivedCSP(csp_packet_t *packet);


  } /* namespace sdr */
} /* namespace ex2 */

