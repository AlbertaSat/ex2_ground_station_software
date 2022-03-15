/*!
 * @file configuration.h
 * @author Steven Knudsen
 * @date April 30, 2021
 *
 * @details Manage the parameters that define the confguration of the transmitter
 * and recevier. In general, these define
 *
 * @ref
 *
 * @copyright AlbertaSat 2021
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#ifndef EX2_SDR_CONFIGURATION_CONFIGURATION_H_
#define EX2_SDR_CONFIGURATION_CONFIGURATION_H_

#include <cstdint>
#include <string>
#include <vector>

#include "error_correction.hpp"

namespace ex2 {
  namespace sdr {


    /*!
     * @brief Manage the configuration.
     *
     * @details The Configuration class encapsulates all
     * configuration parameters. Most are common to transmit and receive
     * functions, but not all; if not noted otherwise in the constructor
     * description, then a parameter is common to both.
     *
     * @note Perhaps a singleton is not the best way to do this, but it is
     * convenient. This could be re-designed...
     */
    class Configuration {
    public:

      /*!
       * @brief Return a pointer to singleton instance of Configuration.
       *
       * @details Provides access to the Configuration.
       *
       * @warning This class is not thread-safe.
       *
       * @param[in] errorCorrectionScheme The current error correction scheme
       * @param[in] phyStubbed True if radio is stubbed out (no UART)
       * @return pointer to the @p Configuration instance
       */
      static Configuration *
      instance (
          ErrorCorrection::ErrorCorrectionScheme errorCorrectionScheme,
          bool phyStubbed
      );

      /*!
       * @brief Return a pointer to singleton instance of Configuration.
       *
       * @details Provides access to the Configuration.
       *
       * @warning This class is not thread-safe.
       *
       * @return pointer to the @p Configuration instance
       *
       * @throws @std::exception if the @p Configuration was not initialized
       * first by invoking the other @p instance method
       *
       * @todo make a class-specific exception
       */
      static Configuration * instance();

      virtual ~Configuration();

      /*!
       * @brief Accessor
       * @return
       */
      ErrorCorrection::ErrorCorrectionScheme getECScheme() const {
        return m_ECScheme;
      }

    private:

      static Configuration* m_instance;

      /*!
       * @brief Constructor
       *
       * @details
       *
       * @param[in] errorCorrectionScheme The current error correction scheme
       * @param[in] phyStubbed True if radio is stubbed out (no UART)
       */
      Configuration(
        ErrorCorrection::ErrorCorrectionScheme errorCorrectionScheme,
        bool phyStubbed
      );

      /*
       * Error Correction stuff
       */
      ErrorCorrection::ErrorCorrectionScheme m_ECScheme;

      /*
       * Use for testing with no radio
       */
      bool m_phyStubbed;
    };

  } /* namespace sdr */
} /* namespace ex2 */

#endif /* EX2_SDR_CONFIGURATION_CONFIGURATION_H_ */
