/*!
 * @file parity_check.h
 * @author Steven Knudsen
 * @date April 13, 2021
 *
 * @details
 *
 * @copyright University of Alberta 2021
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#ifndef EX2_SDR_ERROR_CONTROL_QCLDPC_PARITY_CHECK_H_
#define EX2_SDR_ERROR_CONTROL_QCLDPC_PARITY_CHECK_H_

#include <eigen3/Eigen/Dense>
#include <eigen3/Eigen/Sparse>
#include <glog/logging.h>
#include <sstream>

#include "../error_correction.hpp"

// TODO: make this a path read from a config file
#ifndef PATH_TO_PROTO_H
#define PATH_TO_PROTO_H "/opt/darkstar/fec/ldpc/802.11/proto_H"
#endif

namespace ex2
{
  namespace sdr
  {

    class ParityCheck
    {
    public:
      /*!
       * @brief ParityCheck constructor
       *
       * @param[in] errorCorrectionCoding One of the IEEE 802.11n error correction codes
       * @param[in] codingRate One of the IEEE 802.11n rates.
       * @throws std::runtime_error If bad path to submatrices or problem with
       * submatrices.
       */
      ParityCheck (
          ErrorCorrection::ErrorCorrectionCoding errorCorrectionCoding,
          ErrorCorrection::CodingRate codingRate);

      ~ParityCheck ();

      /*!
       * @brief Check the validity of the ParityCheck object.
       *
       * @details The object may be invalid if there is a configuration problem.
       * @return True if valid, false otherwise.
       */
      bool isValid() const;

      /*!
       * @brief Return the integer parity check martrix
       *
       * @return The parity check matrix corresponding to @p codeword_size and @p rate of the constructor.
       */
      Eigen::MatrixXi & parityCheckMatrix();

      /*!
       * @brief Return the double parity check martrix
       *
       * @return The parity check matrix corresponding to @p codeword_size and @p rate of the constructor.
       */
      Eigen::MatrixXd  & parityCheckMatrixDouble();

      /*!
       * @brief Return the parity check martrix as a sparse double matrix
       *
       * @return The parity check matrix corresponding to @p codeword_size and @p rate of the constructor.
       */
      Eigen::SparseMatrix<double>  & parityCheckMatrixSparse();

      /*!
       * @brief Return the IEEE 802.11n prototype matrix size for this parity check matrix.
       *
       * @return The prototype matrix size.
       */
      unsigned int prototypeMatrixSize();

      /*!
       * @brief Rank of the parity check matrix.
       *
       * @return Parity check matrix rank. Zero if matrix is not valid.
       */
      unsigned int rank();

    private:
      /*!
       * The parity check matrix comprises submatrices.
       */
      const static unsigned int k_submatrix27x27Size = 27;
      const static unsigned int k_submatrix54x54Size = 54;
      const static unsigned int k_submatrix81x81Size = 81;

      const static int k_submatricesPerRow = 24;

      unsigned int m_submatricesPerColumn() const;

      const std::string m_proto_h_filename()
      {
        char codewordLengthStr[32];
        sprintf(codewordLengthStr,"%d",m_errorCorrection->getCodewordLen());
        std::string filename(codewordLengthStr);
        switch (m_errorCorrection->codingRate())
        {
          case ErrorCorrection::CodingRate::RATE_1_2:
            filename.append("_12");
            break;
          case ErrorCorrection::CodingRate::RATE_2_3:
            filename.append("_23");
            break;
          case ErrorCorrection::CodingRate::RATE_3_4:
            filename.append("_34");
            break;
          case ErrorCorrection::CodingRate::RATE_5_6:
            filename.append("_56");
            break;
          case ErrorCorrection::CodingRate::RATE_1_4:
          case ErrorCorrection::CodingRate::RATE_1_3:
          case ErrorCorrection::CodingRate::RATE_2_5:
          case ErrorCorrection::CodingRate::RATE_3_5:
          case ErrorCorrection::CodingRate::RATE_4_5:
          case ErrorCorrection::CodingRate::RATE_8_9:
          case ErrorCorrection::CodingRate::RATE_9_10:
          case ErrorCorrection::CodingRate::RATE_NA:
          case ErrorCorrection::CodingRate::RATE_FIRST:
          case ErrorCorrection::CodingRate::RATE_LAST:
          default:
            break;
        }
        return filename;
      }

      unsigned int m_submatrixSize() const;

      Eigen::MatrixXi m_read_proto_h();

      void m_makeParityCheckMatrix();

      bool m_valid;

      ErrorCorrection *m_errorCorrection;

      unsigned int m_rank;

      Eigen::MatrixXi m_parityCheckMatrix;
      Eigen::MatrixXd m_parityCheckMatrixDouble;
      Eigen::SparseMatrix<double> m_parityCheckMatrixSparse;

    }; // ParityCheck

  } /* namespace sdr */
} /* namespace ex2 */

#endif /* EX2_SDR_ERROR_CONTROL_QCLDPC_PARITY_CHECK_H_ */
