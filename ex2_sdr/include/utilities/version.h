/*!
 * @file version.h
 * @author Steven Knudsen
 * @date April 30, 2021
 *
 * @details
 *
 * @copyright AlbertaSat 2021
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#ifndef EX2_SDR_UTILITIES_VERSION_H_
#define EX2_SDR_UTILITIES_VERSION_H_

#include <cstdint>
#include <string>

namespace ex2 {
  namespace sdr {

  /*!
   * @brief Manage a version number in the form <major>.<minor>.<patch>
   */
  class Version {
  public:

    /*!
     * @brief Default Constructor
     */
    Version();

    /*!
     * @brief Constructor
     *
     * @param[in] major The major version number [0, 2^8 - 1]
     * @param[in] minor The minor version number [0, 2^8 - 1]
     * @param[in] patch The patch number [0, 2^8 - 1]
     */
    Version(uint8_t major, uint8_t minor, uint8_t patch);

    /*!
     * @brief Constructor
     *
     * @param[in] versionString The version string in format <major>.<minor>.<patch>
     */
    Version(std::string versionString);

    virtual ~Version();

    /*!
     * @brief Accessor
     *
     * @return The major version number
     */
    uint8_t majorVersion() const {
      return m_majorVersion;
    }

    /*!
     * @brief Accessor
     *
     * @return The minor version number
     */
    uint8_t minorVersion() const {
      return m_minorVersion;
    }

    /*!
     * @brief Accessor
     *
     * @return The patch number
     */
    uint8_t patch() const {
      return m_patch;
    }

    /*!
     * @brief Version as a C string
     *
     * @return The version in a C string
     */
    std::string c_str() const;

    /*!
     * @brief Version as a Git string
     *
     * @return The version in Git string
     */
    std::string git() const;

  private:
    uint8_t m_majorVersion;
    uint8_t m_minorVersion;
    uint8_t m_patch;
  };

  } /* namespace sdr */
} /* namespace ex2 */

#endif /* EX2_SDR_UTILITIES_VERSION_H_ */
