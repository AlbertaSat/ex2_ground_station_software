/*!
 * @file rfMode.cpp
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
#include "rfMode.hpp"

namespace ex2 {
  namespace sdr {

    RF_Mode::RF_Mode(RF_ModeNumber rfMode) :
            m_rfMode(rfMode) {
      switch(rfMode) {
        case RF_ModeNumber::RF_MODE_0:
          m_bitRate = 1200;
          break;
        case RF_ModeNumber::RF_MODE_1:
          m_bitRate = 2400;
          break;
        case RF_ModeNumber::RF_MODE_2:
          m_bitRate = 4800;
          break;
        case RF_ModeNumber::RF_MODE_3:
        case RF_ModeNumber::RF_MODE_4:
          m_bitRate = 9600;
          break;
        case RF_ModeNumber::RF_MODE_5:
        case RF_ModeNumber::RF_MODE_6:
        case RF_ModeNumber::RF_MODE_7:
          m_bitRate = 19200;
          break;
        default:
          m_bitRate = 9600;
          break;
      }
    }

    RF_Mode::~RF_Mode() {
    }

  } /* namespace sdr */
} /* namespace ex2 */
