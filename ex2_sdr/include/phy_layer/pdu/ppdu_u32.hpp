/*!
 * @file .h
 * @author Steven Knudsen
 * @date May 10, 2021
 *
 * @details The PHY PDU class for 32-bit data.
 *
 * @copyright University of Alberta 2021
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#ifndef EX2_SDR_PHY_LAYER_PDU_PPDU_U32_H_
#define EX2_SDR_PHY_LAYER_PDU_PPDU_U32_H_

#include <cstdint>
#include <functional>

#include "pdu.hpp"

namespace ex2
{
  namespace sdr
  {
    /*!
     * @brief PHY PDU class that contains @p float symbols.
     *
     * @details This class defines a PHY PDU containing @p float symbols.
     *
     */

    class PPDU_u32 :
        public PDU<uint32_t>
    {
    public:

      /*!
       * @brief PPDU function type.
       */
      typedef std::function< void(PPDU_u32&) > ppdu_function_t;

      /*!
       * @brief Default Constructor
       */
      PPDU_u32 () { };

      /*!
       * @brief Constructor
       *
       * @param[in] payload uint32_t data, which is copied.
       */
      PPDU_u32 (const payload_t& payload) : PDU(payload) { };

      virtual
      ~PPDU_u32 () { };

    private:

      typedef payload_t::pointer data_ptr_t;

    };

  } /* namespace sdr */
} /* namespace ex2 */

#endif /* EX2_SDR_PHY_LAYER_PDU_PPDU_U32_H_ */
