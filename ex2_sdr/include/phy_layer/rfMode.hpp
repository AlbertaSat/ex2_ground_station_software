/*!
 * @file rfMode.h
 * @author Steven Knudsen
 * @date May 25, 2021
 *
 * @details The RF_Mode class that defines the possible modulation modes
 * for the Endurosat UHF Type II radio.
 *
 * @copyright University of Alberta, 2021
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */
#ifndef EX2_SDR_PHY_LAYER_MODULATION_H_
#define EX2_SDR_PHY_LAYER_MODULATION_H_

#include <cstdint>
#include <string>

namespace ex2 {
  namespace sdr {

    /*!
     * @brief Define a forward error correction scheme.
     */
    class RF_Mode {
    public:

      /*!
       * @brief The RF modes from Table 11 in the Endurosat UHF type II manual
       */
      enum class RF_ModeNumber : uint8_t {
        RF_MODE_0 = 0x00,    // 2GFSK, 1200 bps,  Fdev 600Hz,   ModInd 1
        RF_MODE_1 = 0x01,    // 2GFSK, 2400 bps,  Fdev 600Hz,   ModInd 0.5
        RF_MODE_2 = 0x02,    // 2GFSK, 4800 bps,  Fdev 1200Hz,  ModInd 0.5
        RF_MODE_3 = 0x03,    // 2GFSK, 9600 bps,  Fdev 2400Hz,  ModInd 0.5
        RF_MODE_4 = 0x04,    // 2GFSK, 9600 bps,  Fdev 4800Hz,  ModInd 1
        RF_MODE_5 = 0x05,    // 2GFSK, 19200 bps, Fdev 4800Hz,  ModInd 0.5
        RF_MODE_6 = 0x06,    // 2GFSK, 19200 bps, Fdev 9600Hz,  ModInd 1
        RF_MODE_7 = 0x07,    // 2GFSK, 19200 bps, Fdev 19200Hz, ModInd 2
      };

      static const std::string RF_ModeDescription(RF_ModeNumber rfModeNumber);

    public:

      /*!
       * @brief Constructor
       *
       * @param[in] Modulation The error correction block code
       * @param[in] rate The fractional encoding rate
       */
      RF_Mode(RF_ModeNumber rfMode = RF_ModeNumber::RF_MODE_3);

      virtual
      ~RF_Mode();

      /*!
       * @brief Return the bit rate
       * @return The bit rate
       */
      uint16_t getBitRate() const {
        return m_bitRate;
      }

    private:
      RF_ModeNumber m_rfMode;
      uint16_t m_bitRate;
    };


  } /* namespace sdr */
} /* namespace ex2 */


#endif /* EX2_SDR_PHY_LAYER_MODULATION_H_ */
