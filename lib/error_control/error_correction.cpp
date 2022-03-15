/*!
 * @file error_correction.cpp
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

#include "error_correction.hpp"

#include <exception>
#include <string>


namespace ex2 {
  namespace sdr {

    class ECException: public std::exception {
    private:
      std::string message_;
    public:
      explicit ECException(const std::string& message);
      virtual const char* what() const throw() {
        return message_.c_str();
      }
    };

    ECException::ECException(const std::string& message) : message_(message) {
    }

    ErrorCorrection::ErrorCorrection(ErrorCorrectionScheme scheme) :
    m_errorCorrectionScheme(scheme)
    {
      if (scheme < ErrorCorrection::ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_648_R_1_2 ||
          scheme > ErrorCorrection::ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1944_R_5_6) {
        throw ECException("Invalid FEC Scheme");
      }
      m_codingRate = m_getCodingRate(scheme);
      if (m_codingRate != ErrorCorrection::CodingRate::RATE_NA) {
        throw ECException("Invalid FEC Scheme; no rate known");
      }

      m_rate = 1.0;
      m_rate = m_codingRateToFractionalRate();
      m_codewordLen = m_ErrorCorrectionCodingToCodewordLen();
      m_messageLen = (uint32_t) ((double) m_codewordLen * m_rate);
    }

    ErrorCorrection::~ErrorCorrection() {
    }

    ErrorCorrection::CodingRate
    ErrorCorrection::m_bits2rate(uint16_t bits) const
    {
      return static_cast<CodingRate>(bits);
    }

    ErrorCorrection::ErrorCorrectionScheme
    ErrorCorrection::m_bits2errorCorrection(uint16_t bits) const
    {
      return static_cast<ErrorCorrectionScheme>(bits);
    }

    const std::string
    ErrorCorrection::ErrorCorrectionName(ErrorCorrection::ErrorCorrectionScheme scheme)
    {
      // @TODO This is so ugly
      switch(scheme) {
        case ErrorCorrectionScheme::CONVOLUTIONAL_CODING_R_1_2:
          return std::string("Convolutional Coding rate 1/2");
          break;
        case ErrorCorrectionScheme::CONVOLUTIONAL_CODING_R_2_3:
          return std::string("Convolutional Coding rate 2/3");
          break;
        case ErrorCorrectionScheme::CONVOLUTIONAL_CODING_R_3_4:
          return std::string("Convolutional Coding rate 3/4");
          break;
        case ErrorCorrectionScheme::CONVOLUTIONAL_CODING_R_5_6:
          return std::string("Convolutional Coding rate 5/6");
          break;
        case ErrorCorrectionScheme::CONVOLUTIONAL_CODING_R_7_8:
          return std::string("Convolutional Coding rate 7/8");
          break;
        case ErrorCorrectionScheme::REED_SOLOMON_255_239_INTERLEAVING_1:
          return std::string("Reed-Solomon (255,239) interleaving level 1");
          break;
        case ErrorCorrectionScheme::REED_SOLOMON_255_239_INTERLEAVING_2:
          return std::string("Reed-Solomon (255,239) interleaving level 2");
          break;
        case ErrorCorrectionScheme::REED_SOLOMON_255_239_INTERLEAVING_3:
          return std::string("Reed-Solomon (255,239) interleaving level 3");
          break;
        case ErrorCorrectionScheme::REED_SOLOMON_255_239_INTERLEAVING_4:
          return std::string("Reed-Solomon (255,239) interleaving level 4");
          break;
        case ErrorCorrectionScheme::REED_SOLOMON_255_239_INTERLEAVING_5:
          return std::string("Reed-Solomon (255,239) interleaving level 5");
          break;
        case ErrorCorrectionScheme::REED_SOLOMON_255_239_INTERLEAVING_8:
          return std::string("Reed-Solomon (255,239) interleaving level 8");
          break;
        case ErrorCorrectionScheme::REED_SOLOMON_255_223_INTERLEAVING_1:
          return std::string("Reed-Solomon (255,223) interleaving level 1");
          break;
        case ErrorCorrectionScheme::REED_SOLOMON_255_223_INTERLEAVING_2:
          return std::string("Reed-Solomon (255,223) interleaving level 2");
          break;
        case ErrorCorrectionScheme::REED_SOLOMON_255_223_INTERLEAVING_3:
          return std::string("Reed-Solomon (255,223) interleaving level 3");
          break;
        case ErrorCorrectionScheme::REED_SOLOMON_255_223_INTERLEAVING_4:
          return std::string("Reed-Solomon (255,223) interleaving level 4");
          break;
        case ErrorCorrectionScheme::REED_SOLOMON_255_223_INTERLEAVING_5:
          return std::string("Reed-Solomon (255,223) interleaving level 5");
          break;
        case ErrorCorrectionScheme::REED_SOLOMON_255_223_INTERLEAVING_8:
          return std::string("Reed-Solomon (255,223) interleaving level 8");
          break;
        case ErrorCorrectionScheme::CCSDS_TURBO_1784_R_1_2:
          return std::string("CCSDS Turbo rate n=1784 1/2");
          break;
        case ErrorCorrectionScheme::CCSDS_TURBO_1784_R_1_3:
          return std::string("CCSDS Turbo rate n=1784 1/3");
          break;
        case ErrorCorrectionScheme::CCSDS_TURBO_1784_R_1_4:
          return std::string("CCSDS Turbo rate n=1784 1/4");
          break;
        case ErrorCorrectionScheme::CCSDS_TURBO_1784_R_1_6:
          return std::string("CCSDS Turbo rate n=1784 1/6");
          break;
        case ErrorCorrectionScheme::CCSDS_TURBO_3568_R_1_2:
          return std::string("CCSDS Turbo rate n=3568 1/2");
          break;
        case ErrorCorrectionScheme::CCSDS_TURBO_3568_R_1_3:
          return std::string("CCSDS Turbo rate n=3568 1/3");
          break;
        case ErrorCorrectionScheme::CCSDS_TURBO_3568_R_1_4:
          return std::string("CCSDS Turbo rate n=3568 1/4");
          break;
        case ErrorCorrectionScheme::CCSDS_TURBO_3568_R_1_6:
          return std::string("CCSDS Turbo rate n=3568 1/6");
          break;
        case ErrorCorrectionScheme::CCSDS_TURBO_7136_R_1_2:
          return std::string("CCSDS Turbo rate n=7136 1/2");
          break;
        case ErrorCorrectionScheme::CCSDS_TURBO_7136_R_1_3:
          return std::string("CCSDS Turbo rate n=7136 1/3");
          break;
        case ErrorCorrectionScheme::CCSDS_TURBO_7136_R_1_4:
          return std::string("CCSDS Turbo rate n=7136 1/4");
          break;
        case ErrorCorrectionScheme::CCSDS_TURBO_7136_R_1_6:
          return std::string("CCSDS Turbo rate n=7136 1/6");
          break;
        case ErrorCorrectionScheme::CCSDS_LDPC_ORANGE_BOOK_1280:
          return std::string("CCSDS Orange Book LDPC n=1288");
          break;
        case ErrorCorrectionScheme::CCSDS_LDPC_ORANGE_BOOK_1356:
          return std::string("CCSDS Orange Book LDPC n=1356");
          break;
        case ErrorCorrectionScheme::CCSDS_LDPC_ORANGE_BOOK_2048:
          return std::string("CCSDS Orange Book LDPC n=2048");
          break;
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_648_R_1_2:
          return std::string("IEEE 802.11n QC-LDPC n=648 rate 1/2");
          break;
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_648_R_2_3:
          return std::string("IEEE 802.11n QC-LDPC n=648 rate 2/3");
          break;
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_648_R_3_4:
          return std::string("IEEE 802.11n QC-LDPC n=648 rate 3/4");
          break;
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_648_R_5_6:
          return std::string("IEEE 802.11n QC-LDPC n=648 rate 5/6");
          break;
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1296_R_1_2:
          return std::string("IEEE 802.11n QC-LDPC n=1296 rate 1/2");
          break;
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1296_R_2_3:
          return std::string("IEEE 802.11n QC-LDPC n=1296 rate 2/3");
          break;
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1296_R_3_4:
          return std::string("IEEE 802.11n QC-LDPC n=1296 rate 3/4");
          break;
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1296_R_5_6:
          return std::string("IEEE 802.11n QC-LDPC n=1296 rate 5/6");
          break;
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1944_R_1_2:
          return std::string("IEEE 802.11n QC-LDPC n=1944 rate 1/2");
          break;
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1944_R_2_3:
          return std::string("IEEE 802.11n QC-LDPC n=1944 rate 2/3");
          break;
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1944_R_3_4:
          return std::string("IEEE 802.11n QC-LDPC n=1944 rate 3/4");
          break;
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1944_R_5_6:
          return std::string("IEEE 802.11n QC-LDPC n=1944 rate 5/6");
          break;
        case ErrorCorrectionScheme::NO_FEC:
          return std::string("No FEC");
          break;

        default:
          throw ECException("Invalid Error Correction Coding value.");
          break;
      }
      return std::string("bad error coding name");
    }


    double
    ErrorCorrection::m_codingRateToFractionalRate()
    {
      double fractionalRate = 1.0; // assume no encoding
      // @TODO This is so ugly
      switch(m_codingRate) {
        case CodingRate::RATE_1_6:
          fractionalRate = 1.0/6.0;
          break;
        case CodingRate::RATE_1_5:
          fractionalRate = 0.20;
          break;
        case CodingRate::RATE_1_4:
          fractionalRate = 0.25;
          break;
        case CodingRate::RATE_1_3:
          fractionalRate = 1.0/3.0;
          break;
        case CodingRate::RATE_1_2:
          fractionalRate = 0.5;
          break;
        case CodingRate::RATE_2_3:
          fractionalRate = 2.0/3.0;
          break;
        case CodingRate::RATE_3_4:
          fractionalRate = 0.75;
          break;
        case CodingRate::RATE_4_5:
          fractionalRate = 0.8;
          break;
        case CodingRate::RATE_5_6:
          fractionalRate = 5.0/6.0;
          break;
        case CodingRate::RATE_7_8:
          fractionalRate = 7.0/8.0;
          break;
        case CodingRate::RATE_8_9:
          fractionalRate = 8.0/9.0;
          break;
        case CodingRate::RATE_NA:
          break;
        default:
          throw ECException("Invalid Coding Rate value.");
          break;
      }
      return fractionalRate;
    }

    uint32_t
    ErrorCorrection::m_ErrorCorrectionCodingToCodewordLen()
    {
      uint32_t codewordLen = 0; // @TODO this may cause trouble, but is fine for now
      // @TODO This is so ugly
      switch(m_errorCorrectionScheme) {
        case ErrorCorrectionScheme::REED_SOLOMON_255_239_INTERLEAVING_1:
        case ErrorCorrectionScheme::REED_SOLOMON_255_239_INTERLEAVING_2:
        case ErrorCorrectionScheme::REED_SOLOMON_255_239_INTERLEAVING_3:
        case ErrorCorrectionScheme::REED_SOLOMON_255_239_INTERLEAVING_4:
        case ErrorCorrectionScheme::REED_SOLOMON_255_239_INTERLEAVING_5:
        case ErrorCorrectionScheme::REED_SOLOMON_255_239_INTERLEAVING_8:
        case ErrorCorrectionScheme::REED_SOLOMON_255_223_INTERLEAVING_1:
        case ErrorCorrectionScheme::REED_SOLOMON_255_223_INTERLEAVING_2:
        case ErrorCorrectionScheme::REED_SOLOMON_255_223_INTERLEAVING_3:
        case ErrorCorrectionScheme::REED_SOLOMON_255_223_INTERLEAVING_4:
        case ErrorCorrectionScheme::REED_SOLOMON_255_223_INTERLEAVING_5:
        case ErrorCorrectionScheme::REED_SOLOMON_255_223_INTERLEAVING_8:
          codewordLen = 255;
          break;
        case ErrorCorrectionScheme::CCSDS_TURBO_1784_R_1_2:
        case ErrorCorrectionScheme::CCSDS_TURBO_1784_R_1_3:
        case ErrorCorrectionScheme::CCSDS_TURBO_1784_R_1_4:
        case ErrorCorrectionScheme::CCSDS_TURBO_1784_R_1_6:
          codewordLen = 1784;
          break;
        case ErrorCorrectionScheme::CCSDS_TURBO_3568_R_1_2:
        case ErrorCorrectionScheme::CCSDS_TURBO_3568_R_1_3:
        case ErrorCorrectionScheme::CCSDS_TURBO_3568_R_1_4:
        case ErrorCorrectionScheme::CCSDS_TURBO_3568_R_1_6:
          codewordLen = 3568;
          break;
        case ErrorCorrectionScheme::CCSDS_TURBO_7136_R_1_2:
        case ErrorCorrectionScheme::CCSDS_TURBO_7136_R_1_3:
        case ErrorCorrectionScheme::CCSDS_TURBO_7136_R_1_4:
        case ErrorCorrectionScheme::CCSDS_TURBO_7136_R_1_6:
          codewordLen = 7136;
          break;
        case ErrorCorrectionScheme::CCSDS_LDPC_ORANGE_BOOK_1280:
          codewordLen = 1288;
          break;
        case ErrorCorrectionScheme::CCSDS_LDPC_ORANGE_BOOK_1356:
          codewordLen = 1356;
          break;
        case ErrorCorrectionScheme::CCSDS_LDPC_ORANGE_BOOK_2048:
          codewordLen = 2048;
          break;
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_648_R_1_2:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_648_R_2_3:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_648_R_3_4:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_648_R_5_6:
          codewordLen = 648;
          break;
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1296_R_1_2:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1296_R_2_3:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1296_R_3_4:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1296_R_5_6:
          codewordLen = 1296;
          break;
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1944_R_1_2:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1944_R_2_3:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1944_R_3_4:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1944_R_5_6:
          codewordLen = 1944;
          break;

        case ErrorCorrectionScheme::CONVOLUTIONAL_CODING_R_1_2:
        case ErrorCorrectionScheme::CONVOLUTIONAL_CODING_R_2_3:
        case ErrorCorrectionScheme::CONVOLUTIONAL_CODING_R_3_4:
        case ErrorCorrectionScheme::CONVOLUTIONAL_CODING_R_5_6:
        case ErrorCorrectionScheme::CONVOLUTIONAL_CODING_R_7_8:
        case ErrorCorrectionScheme::NO_FEC:
          break;


        default:
          throw ECException("Invalid Error Correction Coding value.");
          break;
      }
      return codewordLen;
    }

    ErrorCorrection::CodingRate
    ErrorCorrection::m_getCodingRate(ErrorCorrectionScheme scheme) {
      CodingRate r = ErrorCorrection::CodingRate::RATE_NA;
      switch(scheme) {

        case ErrorCorrectionScheme::CONVOLUTIONAL_CODING_R_1_2:
        case ErrorCorrectionScheme::CCSDS_TURBO_1784_R_1_2:
        case ErrorCorrectionScheme::CCSDS_TURBO_3568_R_1_2:
        case ErrorCorrectionScheme::CCSDS_TURBO_7136_R_1_2:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_648_R_1_2:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1296_R_1_2:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1944_R_1_2:
          r = ErrorCorrection::CodingRate::RATE_1_2;
          break;

        case ErrorCorrectionScheme::CCSDS_TURBO_1784_R_1_3:
        case ErrorCorrectionScheme::CCSDS_TURBO_3568_R_1_3:
        case ErrorCorrectionScheme::CCSDS_TURBO_7136_R_1_3:
          r = ErrorCorrection::CodingRate::RATE_1_3;
          break;

        case ErrorCorrectionScheme::CCSDS_TURBO_1784_R_1_4:
        case ErrorCorrectionScheme::CCSDS_TURBO_3568_R_1_4:
        case ErrorCorrectionScheme::CCSDS_TURBO_7136_R_1_4:
          r = ErrorCorrection::CodingRate::RATE_1_4;
          break;

        case ErrorCorrectionScheme::CCSDS_TURBO_1784_R_1_6:
        case ErrorCorrectionScheme::CCSDS_TURBO_3568_R_1_6:
        case ErrorCorrectionScheme::CCSDS_TURBO_7136_R_1_6:
          r = ErrorCorrection::CodingRate::RATE_1_6;
          break;

        case ErrorCorrectionScheme::CONVOLUTIONAL_CODING_R_2_3:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_648_R_2_3:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1296_R_2_3:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1944_R_2_3:
          r = ErrorCorrection::CodingRate::RATE_2_3;
          break;

        case ErrorCorrectionScheme::CONVOLUTIONAL_CODING_R_3_4:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_648_R_3_4:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1296_R_3_4:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1944_R_3_4:
          r = ErrorCorrection::CodingRate::RATE_3_4;
          break;

        case ErrorCorrectionScheme::CONVOLUTIONAL_CODING_R_5_6:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_648_R_5_6:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1296_R_5_6:
        case ErrorCorrectionScheme::IEEE_802_11N_QCLDPC_1944_R_5_6:
          r = ErrorCorrection::CodingRate::RATE_5_6;
          break;

        case ErrorCorrectionScheme::CONVOLUTIONAL_CODING_R_7_8:
          r = ErrorCorrection::CodingRate::RATE_7_8;
          break;

        case ErrorCorrectionScheme::REED_SOLOMON_255_239_INTERLEAVING_1:
        case ErrorCorrectionScheme::REED_SOLOMON_255_239_INTERLEAVING_2:
        case ErrorCorrectionScheme::REED_SOLOMON_255_239_INTERLEAVING_3:
        case ErrorCorrectionScheme::REED_SOLOMON_255_239_INTERLEAVING_4:
        case ErrorCorrectionScheme::REED_SOLOMON_255_239_INTERLEAVING_5:
        case ErrorCorrectionScheme::REED_SOLOMON_255_239_INTERLEAVING_8:
        case ErrorCorrectionScheme::REED_SOLOMON_255_223_INTERLEAVING_1:
        case ErrorCorrectionScheme::REED_SOLOMON_255_223_INTERLEAVING_2:
        case ErrorCorrectionScheme::REED_SOLOMON_255_223_INTERLEAVING_3:
        case ErrorCorrectionScheme::REED_SOLOMON_255_223_INTERLEAVING_4:
        case ErrorCorrectionScheme::REED_SOLOMON_255_223_INTERLEAVING_5:
        case ErrorCorrectionScheme::REED_SOLOMON_255_223_INTERLEAVING_8:
        case ErrorCorrectionScheme::CCSDS_LDPC_ORANGE_BOOK_1280: // TODO check for rate
        case ErrorCorrectionScheme::CCSDS_LDPC_ORANGE_BOOK_1356: // TODO check for rate
        case ErrorCorrectionScheme::CCSDS_LDPC_ORANGE_BOOK_2048: // TODO check for rate
        case ErrorCorrectionScheme::NO_FEC:
          r = ErrorCorrection::CodingRate::RATE_NA;
          break;

        default:
          r = ErrorCorrection::CodingRate::RATE_NA;
          break;
      }
      return r;
    }

  } /* namespace darkstar */
} /* namespace xiphos */
