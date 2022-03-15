/*!
 * @file configuration.cpp
 * @author knud
 * @date Jun. 20, 2019
 *
 * @details
 *
 * @copyright Xiphos Systems Corp. 2019
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#include "configuration.h"

namespace ex2 {
  namespace sdr {


    Configuration* Configuration::m_instance = 0;

    Configuration*
    Configuration::instance (
      ErrorCorrection::ErrorCorrectionScheme errorCorrectionScheme,
      bool phyStubbed)
    {
      if (m_instance == 0)
      {
        m_instance = new Configuration (
          errorCorrectionScheme,
          phyStubbed);
      }
      return m_instance;
    }

    Configuration*
    Configuration::instance() {
      if (m_instance == 0)
        throw std::exception();
      return m_instance;
    }

    Configuration::Configuration(
      ErrorCorrection::ErrorCorrectionScheme errorCorrectionScheme,
      bool phyStubbed) :
    m_ECScheme(errorCorrectionScheme),
    m_phyStubbed(phyStubbed)
    {
    }

    Configuration::~Configuration() {
      delete m_instance;
    }

  } /* namespace sdr */
} /* namespace ex2 */
