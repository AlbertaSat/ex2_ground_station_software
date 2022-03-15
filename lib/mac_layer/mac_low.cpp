/*!
 * @file mac_low.cpp
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

#include <iostream>
#include <boost/format.hpp>
#include <functional>
#include <ldpc.h>
#include <vector>

#include "mac_low.h"

#include "../../include/mac_layer/pdu/mpduHeader.hpp"

#define DEBUG_MAC_LOWER 0 // set to 1 to enable

namespace xiphos {
  namespace darkstar {

    MACLowException::MACLowException(const std::string& message) :
        runtime_error(message)
    { }

    MAC_low::MAC_low () :
      m_started(false)
    {
      m_configuration = Configuration::instance();
      m_errorCorrection = new ErrorCorrection(m_configuration->getECCoding(), m_configuration->getECRate());
      m_errorCorrectionMPDUHeader = new ErrorCorrection(ErrorCorrection::ErrorCorrectionCoding::LDPC_IEEE_1944, ErrorCorrection::CodingRate::RATE_1_2);

      m_ldpcHeader = new LDPC(false, m_errorCorrection->errorCorrection(), m_errorCorrection->codingRate(), LDPC::DECODE_ITERATIONS_DEFAULT);
      m_ldpcPayload = new LDPC(false, m_errorCorrectionMPDUHeader->errorCorrection(), m_errorCorrectionMPDUHeader->codingRate());
    }

    MAC_low::~MAC_low()
    {
      delete m_errorCorrection;
      delete m_errorCorrectionMPDUHeader;
      delete m_ldpcHeader;
      delete m_ldpcPayload;
    }

    /**************************************************************************
     * Higher layer facing functions
     *************************************************************************/
    MPDU::mpdu_function_t
    MAC_low::sendMpdu()
    {
      return std::bind(&MAC_low::processMpdu,this, std::placeholders::_1);
    }


    void
    MAC_low::processMpdu (
        MPDU &mpdu)
    {
      // Apply error coding to the MPDU

      PPDU_u8 ppdu = m_encodeMPDU(mpdu);

      // Send it up
      m_sendPpdu (ppdu);
    } // process_mpdu

    void
    MAC_low::setReceiveMpdu(MPDU::mpdu_function_t receive_mpdu)
    {
      m_receiveMpdu = receive_mpdu;
    }

    /**************************************************************************
     * Lower layer facing functions
     *************************************************************************/
    PPDU_f::ppdu_function_t
    MAC_low::receivePpdu()
    {
      return std::bind(&MAC_low::processPpdu,this, std::placeholders::_1);
    }


    void MAC_low::processPpdu(PPDU_f &rawPpdu)
    {
      try {
        m_decodePPDU(rawPpdu);
      }
      catch (MACLowException& e) {
        std::cerr << e.what() << std::endl;
        throw e;
      }

    } // processPpdu

    void
    MAC_low::setSendPpdu(PPDU_u8::ppdu_function_t sendPpdu)
    {
      m_sendPpdu = sendPpdu;
    }

    PPDU_u8
    MAC_low::m_encodeMPDU(MPDU& mpdu)
    {
      // 1. Prepare to encode the header.
      // The encoder will pad out the header bits as needed, so
      // just get the data and put into a PPDU.
      // @TODO should change to get rid of PPDU since we don't care
      // much about timestamping, but wait and see, maybe we will...
      MPDUHeader *mh = mpdu.getMpduHeader();
      PDU<uint8_t>::payload_t header = mh->getHeaderPayload();
      PPDU_u8 headerPPDU(header);

      // 2. Encode the header
      // @TODO the LDPC object(s) should be instantiated in the
      PPDU_u8 encodedHeader = m_ldpcHeader->encodeSparse(headerPPDU);
#if DEBUG_MAC_LOWER
      printf("Header length is %ld bytes\n", header.size());
      printf("Encoded header length = %ld bits\n", encodedHeader.getPayload().size());
#endif
      encodedHeader.repack(PPDU_u8::BitsPerSymbol::BPSymb_8);
#if DEBUG_MAC_LOWER
      printf("Encoded header length = %ld bytes\n", encodedHeader.getPayload().size());
#endif

      // 3. Make a payload to hold all the encoded data
      PPDU_u8::payload_t payload = mpdu.getPayload();
#if DEBUG_MAC_LOWER
      printf("raw payload size %ld\n",payload.size());
#endif
      if (m_configuration->getFrameMessageBytes() > payload.size()) {
        // need to pad out the payload.
        uint32_t paddingCount = m_configuration->getFrameMessageBytes() - payload.size();
        for (uint32_t i = 0; i < paddingCount; i++)
          payload.push_back(0);
#if DEBUG_MAC_LOWER
        printf("payload should be %d bytes\n",m_configuration->getFrameMessageBytes());
        printf("   adding %d bytes\n",paddingCount);
        printf("raw payload size %ld\n",payload.size());
#endif
      }
      PPDU_u8 payloadPPDU(payload);
      PPDU_u8 encodedFrame = m_ldpcPayload->encodeSparse(payloadPPDU);
#if DEBUG_MAC_LOWER
      printf("Encoded payload length = %ld bits\n", encodedFrame.getPayload().size());
#endif
      encodedFrame.repack(PPDU_u8::BitsPerSymbol::BPSymb_8);
#if DEBUG_MAC_LOWER
      printf("Encoded payload length = %ld bytes\n", encodedFrame.getPayload().size());
#endif

      // 4. Concatenate the header and the payload to make a frame
      PDU<uint8_t>::payload_t headerPay = encodedHeader.getPayload();
      PDU<uint8_t>::payload_t framePay = encodedFrame.getPayload();
      framePay.insert(framePay.begin(), headerPay.begin(), headerPay.end());
#if DEBUG_MAC_LOWER
      printf("Encoded frame length = %ld bytes\n", framePay.size());
#endif

      PPDU_u8 framePPDU(framePay);

      return framePPDU;
    }

    void
    MAC_low::m_decodePPDU(PPDU_f& ppdu)
    {
      PPDU_f::payload_t encPPDU = ppdu.getPayload();

      // 1. Extract the encoded header
      uint32_t encHeaderLen = m_ldpcHeader->getCodewordLength();
      PPDU_f::payload_t encodedHeader(encPPDU.begin(), encPPDU.begin()+encHeaderLen);

      // 2. Decode the header
      PPDU_u8::payload_t decodedHeader;
      float snrEstimate = 10.0f; // TODO use real number
      uint32_t bitErrors = m_ldpcHeader->decode(encodedHeader, snrEstimate, decodedHeader);
      if (bitErrors == 0) {

        // TODO CRC check header
        // TODO If no error, log header info, otherwise log error and continue

        PPDU_u8 header(decodedHeader, PPDU_u8::BitsPerSymbol::BPSymb_1);
        header.repack(PPDU_u8::BitsPerSymbol::BPSymb_8);

        uint32_t framePayloadBitCount = 0; // bits

        // Now make the MPDU
        try {
          MPDUHeader mpduH(header.getPayload());
          framePayloadBitCount = mpduH.getFramePayloadBitCount();

          // 3. Decode the payload
          // TODO this might be the final Frame and it may not be full of actual
          // source bits. That is, we could maybe resize it based on the payload
          // bits saved in the header, but save that for later as it does not save
          // all that much time for a large reception.
          PPDU_f::payload_t encodedPayload(encPPDU.begin()+encHeaderLen, encPPDU.end());
          PPDU_u8::payload_t decodedPayload;
          bitErrors = m_ldpcPayload->decode(encodedPayload, snrEstimate, decodedPayload);

          // Pass up the payload only.
          // If there are bit errors, log them, but continue no matter what.
          PPDU_u8 payload(decodedPayload, PPDU_u8::BitsPerSymbol::BPSymb_1);
          payload.repack(PPDU_u8::BitsPerSymbol::BPSymb_8);

          // If the header failed to be constructed above, we must assume that the
          // frame length is the whole payload.
          if (framePayloadBitCount == 0) framePayloadBitCount = payload.payloadLength() * 8;
          if (bitErrors > 0) {
            // TODO Log the bit error count, frame number, etc.
          }
          // Always resize the payload to match the actual number of bits of data
          // meant to be received.
          PPDU_u8::payload_t resizedPayload = payload.getPayload();
          uint32_t framePayloadByteCount = framePayloadBitCount / 8 + (framePayloadBitCount % 8 == 0 ? 0 : 1);

          resizedPayload.resize(framePayloadByteCount);
          MPDU payloadMPDU(mpduH, resizedPayload);
          m_receiveMpdu(payloadMPDU);
        }
        catch (MPDUHeaderException& e) {
          std::cerr << e.what() << std::endl;
        } // try to make an MPDU header from the start of the Frame
      }
      else {
        throw MACLowException("MAC low: Decoded header is bad.");
      }
    }

  } /* namespace darkstar */
} /* namespace xiphos */

