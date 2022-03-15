/*!
 * @file phy.h
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

#ifndef EX2_SDR_PHY_LAYER_PHY_H_
#define EX2_SDR_PHY_LAYER_PHY_H_

#include <functional>
#include <glog/logging.h>

#include "ppdu_f.hpp"
#include "ppdu_u8.hpp"

namespace ex2
{
  namespace sdr
  {

    /*!
     * @brief This is the physical (PHY) layer class
     * @ingroup ex2_sdr
     *
     * @details The PHY class interfaces with the MAC to facilitate the sending
     * of PPDUs, and to pass along PPDUs received from remote radios.
     *
     * @todo add more detail
     *
     */
    class PHY
    {
    public:

      PHY ();
      virtual ~PHY ();

      /************************************************************************
       * Functions to handle exchange of PHY Protocol Data Units with the MAC
       ***********************************************************************/

      /*!
       * @brief Provide a transmit PPDU function.
       *
       * @details It's assumed that the higher (MAC) layer uses this function to
       * transmit PPDUs.
       *
       * @return Pointer to a function that accepts PPDUs
       */
      PPDU_u8::ppdu_function_t transmitPpdu();

      /*!
       * @brief Set the receive PPDU function.
       *
       * @details It's assumed that higher (MAC) layer provides a function
       * pointer that accepts PPDUs to be forwarded up.
       *
       * @param[in] receivePpdu Pointer to the forwarding function
       */
      void setReceivePpdu(PPDU_f::ppdu_function_t receivePpdu);

      /*!
       * @brief Get the number of raw PPDUs received (over the air)
       *
       * @return Number of raw PPDUs
       */
      uint32_t
      getPPDUsReceived () const;

      /*!
       * @brief Get the number of PPDUs transmitted.
       *
       * @return Number of PPDUs
       */
      uint32_t
      getPPDUsTransmitted () const;

    protected:

      virtual void processPpdu(PPDU_u8& ppdu) = 0;

      /*!
       * @brief Pointer to function that receives
       */
      PPDU_f::ppdu_function_t m_receivePpdu;

      uint32_t m_PPDUsTransmitted;
      uint32_t m_PPDUsReceived;
    };

  } /* namespace sdr */
} /* namespace ex2 */

#endif /* EX2_SDR_PHY_LAYER_PHY_H_ */
