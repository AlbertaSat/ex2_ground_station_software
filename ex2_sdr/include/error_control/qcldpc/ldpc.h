/*!
 * @file ldpc.h
 * @author Steven Knudsen
 * @date April 13, 2021
 *
 * @details The LDPC class implementing encoding and decoding.
 *
 * @copyright University of Alberta 2021
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#ifndef EX2_SDR_ERROR_CONTROL_QCLDPC_QCLDPC_H_
#define EX2_SDR_ERROR_CONTROL_QCLDPC_QCLDPC_H_

#include <eigen3/Eigen/Sparse>

#include "../../phy_layer/pdu/ppdu_f.hpp"
#include "../../phy_layer/pdu/ppdu_u8.hpp"
#include "parity_check.h"

namespace ex2
{
  namespace sdr
  {

    class parity_check;

    class LDPC
    {
    public:

      static const uint32_t DECODE_ITERATIONS_DEFAULT = 12;
      /*!
       * @brief Constructor
       *
       * @param[in] testMode If true, the encoder doesn't encode, it just returns
       * @param[in] errorCorrectionCoding An IEEE 802.11n LDPC codeword size
       * @param[in] codingRate An IEEE 802.11n LDPC rate
       * @param[in] decodeIterations The number of iterations to use for decoding
       * the input data padded out to the codeword size
       *
       * @throws std::runtime_error If bad path to submatrices or problem with
       * submatrices.
       *
       */
      LDPC (
        bool testMode = false,
        ErrorCorrection::ErrorCorrectionCoding errorCorrectionCoding = ErrorCorrection::ErrorCorrectionCoding::LDPC_IEEE_1944,
        ErrorCorrection::CodingRate codingRate = ErrorCorrection::CodingRate::RATE_1_2,
        uint32_t decodeIterations = DECODE_ITERATIONS_DEFAULT);

      virtual
      ~LDPC ();

      /*!
       * @brief Encode the input PDU
       *
       * @details The implementation is based on Richardson, T., Urbanke, R.,
       * "Efficient Encoding of Low-Density Parity-Check Codes". IEEE Trans.
       * on Information Theory, Feb. 2001
       *
       * @param[in] inPDU
       * @return The encoded PDU
       */
      const PPDU_u8 encode(PPDU_u8 &inPDU);

      /*!
       * @brief Encode the input PDU
       *
       * @details The implementation is based on Richardson, T., Urbanke, R.,
       * "Efficient Encoding of Low-Density Parity-Check Codes". IEEE Trans.
       * on Information Theory, Feb. 2001
       *
       * @param[in] inPDU
       * @return The encoded PDU
       */
      const PPDU_u8 encodeSparse(PPDU_u8 &inPDU);

      /*!
       * @brief Decode the input PDU
       *
       * @param[in] encodedPayload The encoded payload
       * @param[in] snrEstimate The estimated signal to noise ratio for the encoded
       * payload
       * @param[out] decodedPayload The decoded payload
       * @return The number of bit errors in the decoded payload. If 0, the
       * payload was properly decoded.
       */
      uint32_t decode(PPDU_f::payload_t& encodedPayload, float snrEstimate,
          PPDU_u8::payload_t& decodedPayload);

      /*!
       * @brief Decode the input PDU using the logarithmic algorithm
       *
       * @param[in] encodedPayload The encoded payload
       * @param[in] snrEstimate The estimated signal to noise ratio for the encoded
       * payload
       * @param[out] decodedPayload The decoded payload
       * @return The number of bit errors in the decoded payload. If 0, the
       * payload was properly decoded.
       *
       * @todo Not yet implemented
       */
      uint32_t decodeLog(PPDU_f::payload_t& encodedPayload, float snrEstimate,
          PPDU_u8::payload_t& decodedPayload);

      /*!
       * @brief Decode iterations count accessor
       * @return Number of decode iterations
       */
      uint32_t
      getDecodeIterations () const;

      /*!
       * @brief Set the number of decode iterations.
       *
       * @details If @p decodeIterations is zero, the number of decode iterations is set to @p DECODE_ITERATIONS_DEFAULT.
       * @param[in] decodeIterations Number of decode iterations
       */
      void
      setDecodeIterations (
        uint32_t decodeIterations);

      /*!
       * @brief Parity Check matrix accessor
       *
       * @return The parity check matrix defined by the @p codewordSize and @p rate provided to the constructor.
       */
      const Eigen::MatrixXi  & getParityMatrix() const;

      uint32_t getMessageLength() const {
        return m_k;
      }

      uint32_t getCodewordLength() const {
        return m_n;
      }

    private:

      bool m_testMode;

      ErrorCorrection::ErrorCorrectionCoding m_ECCoding;
      ErrorCorrection::CodingRate m_codingRate;

      uint32_t m_k; // message length
      uint32_t m_n; // codeword length

      ParityCheck * m_pchk;
      Eigen::MatrixXi m_parityCheckMatrix;
      Eigen::SparseMatrix<int> m_parityCheckMatrixSparse;

      // Dense matrices needed for encoding
      Eigen::MatrixXd m_A, m_B, m_EinvTA_C, m_invTA, m_invTB;
      Eigen::VectorXd m_p1, m_p2;//, m_msg;
      // Sparse matrices needed for encoding
      Eigen::SparseMatrix<double> m_sA, m_sB, m_sEinvTA_C, m_sinvTA, m_sinvTB;
      Eigen::SparseVector<double> m_sp1, m_sp2;

      // Matrices needed for decoding
      // M(j) represents the set of indexes of all the children parity check nodes
      // connected to the symbol node d(j)
      Eigen::MatrixXi m_M;
      Eigen::VectorXi m_M_numCheckNodes;
      // N(i) represents the set of indexes of all the parent symbol nodes connected
      // to the parity check node h(i)
      Eigen::MatrixXi m_N;
      Eigen::VectorXi m_N_numSymbolNodes;

      /*!
       * The number of LDPC decoder iterations
       */
      uint32_t m_decodeIterations;

      uint32_t m_parityCheckMatrix_rank;

      void m_makeDecoderMatrices();

      void m_makeEncoderMatrices();

    };

  } /* namespace sdr */
} /* namespace ex2 */

#endif /* EX2_SDR_ERROR_CONTROL_QCLDPC_QCLDPC_H_ */
