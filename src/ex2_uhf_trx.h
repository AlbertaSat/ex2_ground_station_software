/*!
 * @file ex2_uhf_trx.h
 * @author Steven Knudsen
 * @date May 10, 2021
 *
 * @details
 *
 * @copyright
 * Copyright (C) 2021 AlbertaSat
 *
 * @license
 * This software may not be modified or distributed in any form.
 * See the LICENSE file for details.
 */

#ifndef EX2_SDR_UHF_TRX_H_
#define EX2_SDR_UHF_TRX_H_

#include <cstdint>

#include "../include/phy_layer/phy.hpp"
#include "app.h"
#include "configuration.h"
#include "mls.h"

namespace ex2
{
  namespace sdr
  {

    /*!
     * @brief Override \p PHY class to make Ex2 PHY layer
     */
    class DarkstarPHY: public PHY {
    public:
      DarkstarPHY(std::string& outputFilename);

      virtual ~DarkstarPHY();

      PPDU_u8::ppdu_function_t transmitPpdu();

    protected:
      void processPpdu(PPDU_u8& ppdu);


    private:

      std::string m_outputFilename;
      std::ofstream m_outputFS;

      MLS *m_mls;
    };


    /*!
     * @brief Override \p app class to make test app layer
     */
    class TestApp : public APP
    {
    public:

      TestApp(std::string& filename, uint32_t apduLength);

      virtual ~TestApp();

      void start ();

      void sendData(const PDU<uint8_t>::payload_t &payload);

    private:
      void processApdu(APDU& apdu);

      Configuration *m_configuration;

      std::ifstream m_inputFS;

      std::string m_inputFilename;
      uint32_t m_inputFileLength;
      uint32_t m_apduLength;

    };

  } /* namespace sdr */
} /* namespace ex2 */


#endif /* EX2_SDR_UHF_TRX_H_ */
