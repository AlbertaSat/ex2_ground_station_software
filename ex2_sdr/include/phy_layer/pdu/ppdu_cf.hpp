  /*!
 * @file ppdu_cf.h
 * @author Steven Knudsen
 * @date May 10, 2021
 *
 * @details The PHY PDU class for complex float data.
 *
 * @copyright University of Alberta 2021
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#ifndef EX2_SDR_PHY_LAYER_PDU_PPDU_CF_H_
#define EX2_SDR_PHY_LAYER_PDU_PPDU_CF_H_

#include <complex>
#include <cstdint>
#include <functional>

#include "pdu.hpp"

namespace ex2
{
  namespace sdr
  {
    /*!
     * @brief PHY PDU class that contains @p std::complex<float> symbols.
     *
     * @details This class defines a PHY PDU containing @p std::complex<float> symbols.
     *
     */

    class PPDU_cf :
        public PDU<std::complex<float>>
    {
    public:

      /*!
       * @brief PPDU function type.
       */
      typedef std::function< void(PPDU_cf&) > ppdu_function_t;

      /*!
       * @brief Default Constructor
       */
      PPDU_cf () { };

      /*!
       * @brief Constructor
       *
       * @param[in] payload Complex float data, which is copied.
       */
      PPDU_cf (const payload_t& payload) : PDU(payload) { };

      virtual
      ~PPDU_cf () { };

    private:

      typedef payload_t::pointer data_ptr_t;

    };

  } /* namespace sdr */
} /* namespace ex2 */

#endif /* EX2_SDR_PHY_LAYER_PDU_PPDU_CF_H_ */
