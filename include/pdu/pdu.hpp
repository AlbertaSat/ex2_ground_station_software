/*!
 * @file pdu.h
 * @author Steven Knudsen
 * @date April 13, 2021
 *
 * @details The based Protocol Data Unit class. It encapsulates a payload
 * vector that is either @p uint8_t, @p uint32_t, @p float, @p complex<float>,
 * or @p complex<double>
 *
 * @copyright University of Alberta 2021
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#ifndef EX2_SDR_PDU_PDU_H_
#define EX2_SDR_PDU_PDU_H_

#include <cstdint>
#include <vector>

namespace ex2 {
  namespace sdr {

    template <class T>
    class PDU {
    public:

      /*!
       * @brief Payload type
       */
      typedef std::vector<T> payload_t;

      /*!
       * @brief Constructor
       */
      PDU () {};

      /*!
       * @brief Constructor
       *
       * @param[in] payload The PDU payload, which is copied.
       */
      PDU (payload_t payload) {
        m_payload.reserve(payload.size());
        for (uint32_t i = 0; i < payload.size(); i++)
          m_payload.push_back(payload[i]);
      };

      virtual
      ~PDU () {};

      /*!
       * @brief Accessor - payload
       *
       * @return payload
       */
      const payload_t& getPayload() const {
        return m_payload;
      }

      /*!
       * @brief The number of payload elements.
       *
       * @return The number of payload elements.
       */
      unsigned long
      payloadLength () const {
        return m_payload.size();
      }

    protected:
      payload_t m_payload;
    };

  } /* namespace sdr */
} /* namespace ex2 */

#endif /* EX2_SDR_PDU_PDU_H_ */
