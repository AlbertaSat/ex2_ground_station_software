/*!
 * @file version.cpp
 * @author Steven Knudsen
 * @date May 10, 2021
 *
 * @details
 *
 * @copyright AlbertaSat 2021
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#include "version.h"
#include <exception>
#include <string>
#include <cstring>
#include <cstdio>
#include <iostream>

#define NO_GIT_VERSION 1

#if NO_GIT_VERSION
#define EX2_SDR_MAJOR_VERSION 0
#define EX2_SDR_MINOR_VERSION 2
#define EX2_SDR_PATCH 0
#endif

namespace ex2 {
  namespace sdr {

    class VersionException: public std::exception {
    private:
      std::string message_;
    public:
      explicit VersionException(const std::string& message);
      virtual const char* what() const throw() {
        return message_.c_str();
      }
    };

    VersionException::VersionException(const std::string& message) : message_(message) {
    }

    Version::Version() :
      m_majorVersion(EX2_SDR_MAJOR_VERSION), // @suppress("Symbol is not resolved") // @suppress("Type cannot be resolved")
      m_minorVersion(EX2_SDR_MINOR_VERSION), // @suppress("Symbol is not resolved") // @suppress("Type cannot be resolved")
      m_patch(EX2_SDR_PATCH) // @suppress("Symbol is not resolved") // @suppress("Type cannot be resolved")
    {
    }

    Version::Version(uint8_t major, uint8_t minor, uint8_t patch) :
      m_majorVersion(major),
      m_minorVersion(minor),
      m_patch(patch)
    {
      // Can't really have a bad version number if we allow the full range for
      // each part, i.e., [0, 2^8 - 1]
    }

    Version::Version(std::string versionString) :
      m_majorVersion(0),
      m_minorVersion(0),
      m_patch(0)
    {
      // It's okay to initialize to 0.0.0 because if we don't get something
      // from @p versionString, we throw an exception anyway

      std::string major_str("");
      std::string minor_str("");
      std::string patch_str("");

      std::string delimiter = ".";
      size_t p = versionString.find(delimiter);
      if (p != std::string::npos) {
        major_str = versionString.substr(0, p);
        versionString = versionString.substr(p + delimiter.length());
        p = versionString.find(delimiter);
        if (p != std::string::npos) {
          minor_str = versionString.substr(0, p);
          versionString = versionString.substr(p + delimiter.length());
          if (versionString.length() > 0)
            patch_str = versionString;
        }
      }
      bool okay = false;
      if (major_str.length() > 0 && minor_str.length() > 0 && patch_str.length() > 0) {
        okay = true;
        // Note that if stol doesn't get valid input, it throws the appropriate exception.
        // However, since there is not stoui (unsigned int) function, we have to start with
        // unsigned long and then check the range.
        unsigned long temp = std::stoul (major_str,nullptr,10);
        if (temp <= UINT8_MAX) {
          m_majorVersion = (uint8_t)temp;
        }
        else {
          okay = false;
        }
        temp = std::stoul (minor_str,nullptr,10);
        if (temp <= UINT8_MAX) {
          m_minorVersion = (uint8_t)temp;
        }
        else {
          okay = false;
        }
        temp = std::stoul (patch_str,nullptr,10);
        if (temp <= UINT8_MAX) {
          m_patch = (uint8_t)temp;
        }
        else {
          okay = false;
        }
      }
      if (!okay) {
        std::string e("Bad version string : ");
        e.append(versionString);
        throw VersionException(e);
      }
    }

    Version::~Version() {
    }

    std::string
    Version::c_str() const
    {
      // Largest string is 255.255.255
      char tempStr[64];
      sprintf(tempStr, "%d.%d.%d", m_majorVersion, m_minorVersion, m_patch);
      std::string ret(tempStr);
      return ret;
    }

    std::string Version::git() const
    {
      return GIT_VERSION; // @suppress("Symbol is not resolved")
    }


  } /* namespace sdr */
} /* namespace ex2 */
