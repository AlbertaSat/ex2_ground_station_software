/*!
 * @file ldpc.cpp
 * @author Steven Knudsen
 * @date June 18, 2019
 *
 * @details LDPC encoding and decoding functions.
 *
 * @copyright Xiphos Systems Corp. 2019
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#include <iostream>
#include <stdio.h>
#include <vector>
#include <eigen3/Eigen/Dense>
#include <boost/format.hpp>
#include <boost/random.hpp>
#include <boost/random/normal_distribution.hpp>

#include "ldpc.h"
#include "parity_check.h"

#define LDPC_DEBUG 0
#define LDPC_DEBUG_VERBOSE 0
#define LDPC_DEBUG_SAMPLES_TO_PRINT 30

namespace xiphos
{
  namespace darkstar
  {

    class LDPCException: public std::exception {
    private:
      std::string message_;
    public:
      explicit LDPCException(const std::string& message);
      virtual const char* what() const throw() {
        return message_.c_str();
      }
    };

    LDPCException::LDPCException(const std::string& message) : message_(message) { }

    LDPC::LDPC (
        bool testMode,
        ErrorCorrection::ErrorCorrectionCoding errorCorrectionCoding,
        ErrorCorrection::CodingRate codingRate,
        uint32_t decodeIterations) :
                                      m_testMode(testMode),
                                      m_ECCoding (errorCorrectionCoding),
                                      m_codingRate (codingRate),
                                      m_decodeIterations (decodeIterations),
                                      m_parityCheckMatrix_rank(0)
    {
      ErrorCorrection ec = ErrorCorrection(errorCorrectionCoding, codingRate);
      m_k = ec.getMessageLen();
      m_n = ec.getCodewordLen();
      m_pchk = new ParityCheck(errorCorrectionCoding, codingRate);
      m_parityCheckMatrix = m_pchk->parityCheckMatrix();
      m_parityCheckMatrixSparse = m_parityCheckMatrix.sparseView();
#if LDPC_DEBUG_VERBOSE
      std::cout << "m_k " << m_k << std::endl;
      std::cout << "m_n " << m_n << std::endl;
      std::cout << "m_parityCheckMatrix rows " << m_parityCheckMatrix.rows() << std::endl;
      std::cout << "m_parityCheckMatrix cols " << m_parityCheckMatrix.cols() << std::endl;
#endif
      if (!m_testMode) {
        m_makeEncoderMatrices();
        m_makeDecoderMatrices();
      }
    }

    LDPC::~LDPC ()
    {
      delete m_pchk;
    }

    const PPDU_u8
    LDPC::encode (PPDU_u8 &inPDU)
    {

      // The encoding algorithm expects 1 bit per byte (sample)
      if (inPDU.getBps() > 1)
        inPDU.repack(PPDU_u8::BitsPerSymbol::BPSymb_1);

      // The input PPDU data length must be an multiple of the
      // message length, m_k. Zero pad as needed.
      PDU<uint8_t>::payload_t inPayload = inPDU.getPayload();
      uint32_t pduLen = inPayload.size();
      uint32_t numCodewords = pduLen / m_k + (pduLen % m_k != 0 ? 1 : 0);
      uint32_t numPadding = numCodewords * m_k - pduLen;
      if (numPadding > 0) {
        for (uint32_t z = 0; z < numPadding; z++) {
          inPayload.push_back(0);
        }
      }

#if LDPC_DEBUG
      printf("LDPC::encode pduLen %d m_k %d numCodewords %d\n", pduLen, m_k, numCodewords);
      printf("LDPC::encode numPadding length = %d bytes\n", numPadding);
#endif
      if (m_testMode) {
        // Since no encoding is going to be done in this mode, we
        // fake it by padding out the data so it's as long
        // as it would be for the given codeword length and multiple
        uint32_t codewordPadding = numCodewords * m_n - inPayload.size();
#if LDPC_DEBUG
        printf("LDPC::encode In test mode;\n");
        printf("\tm_n %d m_k %d numCodewords = %d\n",m_n,m_k,numCodewords);
        printf("\tpadding to get to %d full codeword = %d\n",numCodewords, codewordPadding);
#endif
        PDU<uint8_t>::payload_t cpad(codewordPadding,0);
        inPayload.insert(inPayload.end(),cpad.begin(),cpad.end());
        return PPDU_u8(inPayload, PPDU_u8::BitsPerSymbol::BPSymb_1);
      }
      else {
        Eigen::VectorXd m(m_k);
        uint8_t * inPayloadPtr = inPayload.data();

        PDU<uint8_t>::payload_t outPayload(0);

        for (uint32_t nc = 0; nc < numCodewords; nc++)
        {
          // TODO make this more efficient? Have to have msg as double for Eigen arithmetic
          for (uint32_t i = 0; i < m_k; i++)
            m[i] = (double) inPayload[(nc * m_k) + i];

          m_p1 = m_EinvTA_C * m;
#if LDPC_DEBUG_VERBOSE
          std::cout << "m_p1 size "  << m_p1.size() << std::endl;
          std::cout << "m_p1" << std::endl;
          std::cout << m_p1 << std::endl;
#endif
          m_p2 = m_invTA * m + m_invTB * m_p1;
#if LDPC_DEBUG_VERBOSE
          std::cout << "m_p2 size "  << m_p2.size() << std::endl;
          std::cout << "m_p2" << std::endl;
          std::cout << m_p2 << std::endl;
#endif
          Eigen::VectorXi p1i = m_p1.cast<int>();
          Eigen::VectorXi p2i = m_p2.cast<int>();
#if LDPC_DEBUG_VERBOSE
          std::cout << "p1i size "  << p1i.size() << std::endl;
          std::cout << "p2i size "  << p2i.size() << std::endl;
#endif

          // append m p1 p2
          outPayload.insert (outPayload.end (), inPayloadPtr, inPayloadPtr + m_k);
          int * p1iPtr = p1i.data ();
          outPayload.insert (outPayload.end (), p1iPtr, p1iPtr + p1i.size ());
          int * p2iPtr = p2i.data ();
          outPayload.insert (outPayload.end (), p2iPtr, p2iPtr + p2i.size ());

          inPayloadPtr += m_k;
        }

        return PPDU_u8(outPayload, PPDU_u8::BitsPerSymbol::BPSymb_1);
      }
    }

    const PPDU_u8
    LDPC::encodeSparse (PPDU_u8 &inPDU)
    {
      // The encoding algorithm expects 1 bit per byte (sample)
      if (inPDU.getBps() > 1)
        inPDU.repack(PPDU_u8::BitsPerSymbol::BPSymb_1);

      // The input PPDU data length must be an multiple of the
      // message length, m_k. Zero pad as needed.
      PDU<uint8_t>::payload_t inPayload = inPDU.getPayload();
      uint32_t pduLen = inPayload.size();
      uint32_t numCodewords = pduLen / m_k + (pduLen % m_k != 0 ? 1 : 0);
      uint32_t numPadding = numCodewords * m_k - pduLen;
      if (numPadding > 0) {
        for (uint32_t z = 0; z < numPadding; z++) {
          inPayload.push_back(0);
        }
      }
#if LDPC_DEBUG
      printf("LDPC::encode pduLen %d m_k %d numCodewords %d\n", pduLen, m_k, numCodewords);
      printf("LDPC::encode numPadding length = %d BPSymb_1 samples\n", numPadding);
      printf("LDPC::padded payload length = %ld BPSymb_1 samples\n", inPayload.size());
#endif
      if (m_testMode) {
        // Since no encoding is going to be done in this mode, we
        // fake it by padding out the data so it's as long
        // as it would be for the given codeword length and multiple
        uint32_t codewordPadding = numCodewords * m_n - inPayload.size();
#if LDPC_DEBUG
        printf("LDPC::encode In test mode;\n");
        printf("\tm_n %d m_k %d numCodewords = %d\n",m_n,m_k,numCodewords);
        printf("\tpadding to get to %d full codeword = %d\n",numCodewords, codewordPadding);
#endif
        PDU<uint8_t>::payload_t cpad(codewordPadding,0);
        inPayload.insert(inPayload.end(),cpad.begin(),cpad.end());
        return PPDU_u8(inPayload, PPDU_u8::BitsPerSymbol::BPSymb_1);
      }
      else {
        Eigen::VectorXd m(m_k);
        uint8_t * inPayloadPtr = inPayload.data();

        PDU<uint8_t>::payload_t outPayload(0);

        for (uint32_t nc = 0; nc < numCodewords; nc++)
        {
          // TODO make this more efficient? Have to have msg as double for Eigen arithmetic
          for (uint32_t i = 0; i < m_k; i++)
            m[i] = (double) inPayload[(nc * m_k) + i];

          m_p1.noalias() = m_sEinvTA_C * m;
          m_p2.noalias() = m_sinvTA * m + m_sinvTB * m_p1;

          Eigen::VectorXi p1i = m_p1.cast<int>();
          Eigen::VectorXi p2i = m_p2.cast<int>();

          // append m p1 p2
          outPayload.insert (outPayload.end (), inPayloadPtr, inPayloadPtr + m_k);
          int * p1iPtr = p1i.data ();
          outPayload.insert (outPayload.end (), p1iPtr, p1iPtr + p1i.size ());
          int * p2iPtr = p2i.data ();
          outPayload.insert (outPayload.end (), p2iPtr, p2iPtr + p2i.size ());

          inPayloadPtr += m_k;
        }

        return PPDU_u8(outPayload, PPDU_u8::BitsPerSymbol::BPSymb_1);
      }
    }

    //    double
    //    lntanh (
    //        double x)
    //    {
    //      double result = -log (tanh (x / 2));
    //      return std::isinf(result) ? 10000 : result;
    //    }

    uint32_t
    LDPC::decode(PPDU_f::payload_t& encodedPayload, float snrEstimate,
        PPDU_u8::payload_t& decodedPayload)
    {
      // TODO Are there places to use sparse matrices?

      // Check that the payload is an integer number of codewords
      uint32_t totalEncSize = encodedPayload.size();
      if (totalEncSize % m_n != 0) {
        throw LDPCException((boost::format ("Encoded Payload length %1% not an integral multiple of codeword length %2%")
        % totalEncSize % m_n).str());
      }

      decodedPayload.resize(0);
      uint32_t numCodewords = totalEncSize / m_n;
      decodedPayload.reserve(numCodewords*m_k);

      // number of bit errors in a codeword. Will be zero if decoding perfect,
      // otherwise will have the number of errors, which we return
      uint32_t sum = 0;
      uint32_t totalBitErrors = 0;
      uint32_t codewordCount = 0;

      float sigma2 = 1.0 / pow (10.0, snrEstimate / 10.0); // noise variance

      Eigen::VectorXd f0 = Eigen::VectorXd::Zero (m_n);
      Eigen::VectorXd f1 = Eigen::VectorXd::Zero (m_n);
      Eigen::MatrixXd Q0 (m_n - m_k, m_n);
      Eigen::MatrixXd Q1 (m_n - m_k, m_n);
      Eigen::MatrixXd deltaQ (m_n - m_k, m_n);
      Eigen::MatrixXd R0 (m_n - m_k, m_n);
      Eigen::MatrixXd R1 (m_n - m_k, m_n);
      Eigen::MatrixXd deltaR (m_n - m_k, m_n);
      Eigen::VectorXi dHat (m_n); // current codeword estimate
      Eigen::VectorXi cwCheck (m_n - m_k); // used to check dHat, codeword est.

      Eigen::VectorXi decoded = Eigen::VectorXi::Zero (m_k);
      Eigen::VectorXd r(m_n);

      unsigned int maxConnectedSymbolNodes = m_N_numSymbolNodes.maxCoeff ();

      uint32_t processedBits = 0;
      while (processedBits < totalEncSize) {
        double totalIterations = 0;

#if LDPC_DEBUG_VERBOSE
        printf("sigma2 %f\n",sigma2);
        printf("max iterations %d\n",m_decodeIterations);
#endif
        for (uint32_t p = 0; p < m_n; p++)
          r[p] = encodedPayload[processedBits+p];

        r = -2 * r / sigma2;
        Eigen::ArrayXd re = Eigen::ArrayXd::Ones (m_n) + r.array ().exp ();
        f1 = re.inverse ();
        f0 = Eigen::VectorXd::Ones (m_n) - f1;

#if LDPC_DEBUG_VERBOSE
        printf("r\n");
        for (uint32_t i = 0; i < LDPC_DEBUG_SAMPLES_TO_PRINT; i++)
          printf("%g ",r[i]);
        printf("\nre\n");
        for (uint32_t i = 0; i < LDPC_DEBUG_SAMPLES_TO_PRINT; i++)
          printf("%g ",re[i]);
        printf("\nf1\n");
        for (uint32_t i = 0; i < LDPC_DEBUG_SAMPLES_TO_PRINT; i++)
          printf("%g ",f1[i]);
        printf("\nf0\n");
        for (uint32_t i = 0; i < LDPC_DEBUG_SAMPLES_TO_PRINT; i++)
          printf("%g ",f0[i]);
        printf("\n");
#endif
        // initilize Q0 and Q1
        for (unsigned int i = 0; i < m_n - m_k; i++)
        {
          for (int j = 0; j < m_N_numSymbolNodes (i); j++)
          {
            Q0 (i, m_N (i, j)) = f0 (m_N (i, j));
            Q1 (i, m_N (i, j)) = f1 (m_N (i, j));
          }
        }
#if LDPC_DEBUG_VERBOSE
        std::cout << "Q0\n" << Q0 << std::endl;
        std::cout << "Q1\n" << Q1 << std::endl;
#endif
        unsigned int iter = 0;
        while (iter < m_decodeIterations)
        {
          totalIterations++;

          deltaQ = Q0 - Q1;

          // update deltaR
          for (unsigned int i = 0; i < m_n - m_k; i++)
          {
            for (int j = 0; j < m_N_numSymbolNodes (i); j++)
            {
              deltaR (i, m_N (i, j)) = 1.0;
              for (int k = 0; k < m_N_numSymbolNodes (i); k++)
              {
                if (k != j)
                  deltaR (i, m_N (i, j)) = deltaR (i, m_N (i, j))
                  * deltaQ (i, m_N (i, k));
              }
            } // for all symbols nodes connected to the current parity check node
          } // for all parity check nodes

          R0 = Eigen::MatrixXd::Ones (m_n - m_k, m_n) + deltaR;
          R0 = 0.5 * R0;
          R1 = Eigen::MatrixXd::Ones (m_n - m_k, m_n) - deltaR;
          R1 = 0.5 * R1;
          // TODO do we have to replace the 0.5 values?
//          R0 = (R0.array () == 0.5).select (0.0, R0.array ());
//          R1 = (R1.array () == 0.5).select (0.0, R1.array ());

#if LDPC_DEBUG_VERBOSE
          std::cout << "R0\n" << R0 << std::endl;
          std::cout << "R1\n" << R1 << std::endl;
#endif

          // Values R appear as normalized values with respect to those seen
          // in tables 8.2 to 8.12. By normalizing values NaN is avoided.

          for (unsigned int i = 0; i < m_n - m_k; i++)
          {
            Eigen::MatrixXd g = Eigen::MatrixXd::Zero (m_n - m_k,
                maxConnectedSymbolNodes);
            for (int j = 0; j < m_N_numSymbolNodes (i); j++)
            {
              double b0 = 1;
              double b1 = 1;

              for (int p1 = 0; p1 < m_M_numCheckNodes (m_N (i, j));
                  p1++)
              {
                if (m_N (i, j) != 0 and ((long) i) != m_M (m_N (i, j), p1))
                {
                  b0 = b0 * R0 (m_M (m_N (i, j), p1), m_N (i, j));
                  b1 = b1 * R1 (m_M (m_N (i, j), p1), m_N (i, j));
                }
              }

              // Normalization of coefficients
              b0 = f0 (m_N (i, j)) * b0;
              b1 = f1 (m_N (i, j)) * b1;

              if (b0 == 0 and b1 == 0)
              {
                Q0 (i, m_N (i, j)) = 0;
                Q1 (i, m_N (i, j)) = 0;
              }
              else
              {
                g (i, j) = 1.0 / (b0 + b1);
                Q0 (i, m_N (i, j)) = b0 * g (i, j);
                Q1 (i, m_N (i, j)) = b1 * g (i, j);
              }

            } // for all symbols nodes connected to the current parity check node
          } // for all parity check nodes

          Eigen::VectorXd d0 = Eigen::VectorXd::Ones (m_n);
          Eigen::VectorXd d1 = Eigen::VectorXd::Ones (m_n);
          for (unsigned int j = 0; j < m_n; j++)
          {
            for (int i = 0; i < m_M_numCheckNodes (j); i++)
            {
              d0 (j) = d0 (j) * R0 (m_M (j, i), j);
              d1 (j) = d1 (j) * R1 (m_M (j, i), j);
            }
            d0 (j) = d0 (j) * f0 (j);
            d1 (j) = d1 (j) * f1 (j);
          }

          // hard decision on the codeword bits
          for (unsigned int j = 0; j < m_n; j++)
            if (d0 (j) > d1 (j))
              dHat (j) = 0;
            else
              dHat (j) = 1;

#if LDPC_DEBUG_VERBOSE
          std::cout << "dHat\n" << dHat.transpose() << std::endl;
#endif
#if 0
          cwCheck = m_parityCheckMatrix * dHat;
#else
          cwCheck = m_parityCheckMatrixSparse * dHat;
#endif
          sum = 0;
          for (unsigned int c = 0; c < cwCheck.size (); c++)
            sum += (cwCheck (c) % 2);
#if LDPC_DEBUG_VERBOSE
          std::cout << "cwCheck \n" << cwCheck.transpose() << std::endl;
          std::cout << "cwCheck.sum() \n" << sum << std::endl;
          std::cout << "iteration " << iter << std::endl;
#endif
          if (sum == 0)
          {
#if LDPC_DEBUG_VERBOSE
            std::cout << " sum == 0 at iteration " << iter << std::endl;
#endif
            break;
          }
          iter++;
          if (iter == m_decodeIterations)
          {
#if LDPC_DEBUG_VERBOSE
            std::cout << (boost::format(" Reached max iterations at codeword %1%; bit errors = %2%") % codewordCount % sum).str() << std::endl;
            for (uint32_t dd = 0; dd < 30; dd++) {
              printf("          e[%d] %g\n", dd, encodedPayload[processedBits-m_n+dd]);
            }
            for (uint32_t dd = 0; dd < 30; dd++) {
              printf("f1[%d] %g e %g\n", dd, f1[dd], encodedPayload[processedBits+dd]);
            }
#endif
          }
        } // while

        totalBitErrors += sum;
        codewordCount++;

        // Save the decoded message
        for (uint32_t i = 0; i < m_k; i++) {
          decodedPayload.push_back(dHat[i] % 2);
        }

        processedBits += m_n;
      } // while not all input samples processed

      std::cout << "Total bit errors = " << totalBitErrors << " for " << (numCodewords*m_k) << " message bits" << std::endl;
      return totalBitErrors;
    }

    uint32_t
    LDPC::decodeLog(PPDU_f::payload_t& encodedPayload, float snrEstimate,
        PPDU_u8::payload_t& decodedPayload)
    {
      // TODO Are there places to use sparse matrices?

      // Check that the payload is an integer number of codewords
      uint32_t totalEncSize = encodedPayload.size();
      if (totalEncSize % m_n != 0) {
        throw LDPCException((boost::format ("Encoded Payload length %1% not an integral multiple of codeword length %2%")
        % totalEncSize % m_n).str());
      }

      decodedPayload.resize(0);
      uint32_t numCodewords = totalEncSize / m_n;
      decodedPayload.reserve(numCodewords*m_k);

      // number of bit errors in a codeword. Will be zero if decoding perfect,
      // otherwise will have the number of errors, which we return
      uint32_t sum = 0;
      uint32_t totalBitErrors = 0;
      uint32_t codewordCount = 0;

      float sigma2 = 1.0 / pow (10.0, snrEstimate / 10.0); // noise variance

      Eigen::VectorXd f0 = Eigen::VectorXd::Zero (m_n);
      Eigen::VectorXd f1 = Eigen::VectorXd::Zero (m_n);
      Eigen::MatrixXd Q0 (m_n - m_k, m_n);
      Eigen::MatrixXd Q1 (m_n - m_k, m_n);
      Eigen::MatrixXd deltaQ (m_n - m_k, m_n);
      Eigen::MatrixXd R0 (m_n - m_k, m_n);
      Eigen::MatrixXd R1 (m_n - m_k, m_n);
      Eigen::MatrixXd deltaR (m_n - m_k, m_n);
      Eigen::VectorXi dHat (m_n); // current codeword estimate
      Eigen::VectorXi cwCheck (m_n - m_k); // used to check dHat, codeword est.

      Eigen::VectorXi decoded = Eigen::VectorXi::Zero (m_k);
      Eigen::VectorXd r(m_n);

      unsigned int maxConnectedSymbolNodes = m_N_numSymbolNodes.maxCoeff ();

      uint32_t processedBits = 0;
      while (processedBits < totalEncSize) {
        double totalIterations = 0;

#if LDPC_DEBUG_VERBOSE
        printf("sigma2 %f\n",sigma2);
        printf("max iterations %d\n",m_decodeIterations);
#endif
        for (uint32_t p = 0; p < m_n; p++)
          r[p] = encodedPayload[processedBits+p];

        r = -2 * r / sigma2;
        Eigen::ArrayXd re = Eigen::ArrayXd::Ones (m_n) + r.array ().exp ();
        f1 = re.inverse ();
        f0 = Eigen::VectorXd::Ones (m_n) - f1;

#if LDPC_DEBUG_VERBOSE
        printf("r\n");
        for (uint32_t i = 0; i < LDPC_DEBUG_SAMPLES_TO_PRINT; i++)
          printf("%g ",r[i]);
        printf("\nre\n");
        for (uint32_t i = 0; i < LDPC_DEBUG_SAMPLES_TO_PRINT; i++)
          printf("%g ",re[i]);
        printf("\nf1\n");
        for (uint32_t i = 0; i < LDPC_DEBUG_SAMPLES_TO_PRINT; i++)
          printf("%g ",f1[i]);
        printf("\nf0\n");
        for (uint32_t i = 0; i < LDPC_DEBUG_SAMPLES_TO_PRINT; i++)
          printf("%g ",f0[i]);
        printf("\n");
#endif
        // initilize Q0 and Q1
        for (unsigned int i = 0; i < m_n - m_k; i++)
        {
          for (int j = 0; j < m_N_numSymbolNodes (i); j++)
          {
            Q0 (i, m_N (i, j)) = f0 (m_N (i, j));
            Q1 (i, m_N (i, j)) = f1 (m_N (i, j));
          }
        }
#if LDPC_DEBUG_VERBOSE
        std::cout << "Q0\n" << Q0 << std::endl;
        std::cout << "Q1\n" << Q1 << std::endl;
#endif
        unsigned int iter = 0;
        while (iter < m_decodeIterations)
        {
          totalIterations++;

          deltaQ = Q0 - Q1;

          // update deltaR
          for (unsigned int i = 0; i < m_n - m_k; i++)
          {
            for (int j = 0; j < m_N_numSymbolNodes (i); j++)
            {
              deltaR (i, m_N (i, j)) = 1.0;
              for (int k = 0; k < m_N_numSymbolNodes (i); k++)
              {
                if (k != j)
                  deltaR (i, m_N (i, j)) = deltaR (i, m_N (i, j))
                  * deltaQ (i, m_N (i, k));
              }
            } // for all symbols nodes connected to the current parity check node
          } // for all parity check nodes

          R0 = Eigen::MatrixXd::Ones (m_n - m_k, m_n) + deltaR;
          R0 = 0.5 * R0;
          R1 = Eigen::MatrixXd::Ones (m_n - m_k, m_n) - deltaR;
          R1 = 0.5 * R1;
          // TODO do we have to replace the 0.5 values?
          R0 = (R0.array () == 0.5).select (0.0, R0.array ());
          R1 = (R1.array () == 0.5).select (0.0, R1.array ());

#if LDPC_DEBUG_VERBOSE
          std::cout << "R0\n" << R0 << std::endl;
          std::cout << "R1\n" << R1 << std::endl;
#endif

          // Values R appear as normalized values with respect to those seen
          // in tables 8.2 to 8.12. By normalizing values NaN is avoided.

          for (unsigned int i = 0; i < m_n - m_k; i++)
          {
            Eigen::MatrixXd g = Eigen::MatrixXd::Zero (m_n - m_k,
                maxConnectedSymbolNodes);
            for (int j = 0; j < m_N_numSymbolNodes (i); j++)
            {
              double b0 = 1;
              double b1 = 1;

              for (int p1 = 0; p1 < m_M_numCheckNodes (m_N (i, j));
                  p1++)
              {
                if (m_N (i, j) != 0 and ((long) i) != m_M (m_N (i, j), p1))
                {
                  b0 = b0 * R0 (m_M (m_N (i, j), p1), m_N (i, j));
                  b1 = b1 * R1 (m_M (m_N (i, j), p1), m_N (i, j));
                }
              }

              // Normalization of coefficients
              b0 = f0 (m_N (i, j)) * b0;
              b1 = f1 (m_N (i, j)) * b1;

              if (b0 == 0 and b1 == 0)
              {
                Q0 (i, m_N (i, j)) = 0;
                Q1 (i, m_N (i, j)) = 0;
              }
              else
              {
                g (i, j) = 1.0 / (b0 + b1);
                Q0 (i, m_N (i, j)) = b0 * g (i, j);
                Q1 (i, m_N (i, j)) = b1 * g (i, j);
              }

            } // for all symbols nodes connected to the current parity check node
          } // for all parity check nodes

          Eigen::VectorXd d0 = Eigen::VectorXd::Ones (m_n);
          Eigen::VectorXd d1 = Eigen::VectorXd::Ones (m_n);
          for (unsigned int j = 0; j < m_n; j++)
          {
            for (int i = 0; i < m_M_numCheckNodes (j); i++)
            {
              d0 (j) = d0 (j) * R0 (m_M (j, i), j);
              d1 (j) = d1 (j) * R1 (m_M (j, i), j);
            }
            d0 (j) = d0 (j) * f0 (j);
            d1 (j) = d1 (j) * f1 (j);
          }

          // hard decision on the codeword bits
          for (unsigned int j = 0; j < m_n; j++)
            if (d0 (j) > d1 (j))
              dHat (j) = 0;
            else
              dHat (j) = 1;

#if LDPC_DEBUG_VERBOSE
          std::cout << "dHat\n" << dHat.transpose() << std::endl;
#endif
          cwCheck = m_parityCheckMatrix * dHat;

          sum = 0;
          for (unsigned int c = 0; c < cwCheck.size (); c++)
            sum += (cwCheck (c) % 2);
#if LDPC_DEBUG_VERBOSE
          std::cout << "cwCheck \n" << cwCheck.transpose() << std::endl;
          std::cout << "cwCheck.sum() \n" << sum << std::endl;
          std::cout << "iteration " << iter << std::endl;
#endif
          if (sum == 0)
          {
#if LDPC_DEBUG_VERBOSE
            std::cout << " sum == 0 at iteration " << iter << std::endl;
#endif
            break;
          }
          iter++;
          if (iter == m_decodeIterations)
          {
//#if LDPC_DEBUG_VERBOSE
            std::cout << (boost::format(" Reached max iterations at codeword %1%; bit errors = %2%") % codewordCount % sum).str() << std::endl;
            for (uint32_t dd = 0; dd < 30; dd++) {
              printf("          e[%d] %g\n", dd, encodedPayload[processedBits-m_n+dd]);
            }
            for (uint32_t dd = 0; dd < 30; dd++) {
              printf("f1[%d] %g e %g\n", dd, f1[dd], encodedPayload[processedBits+dd]);
            }
//#endif
          }
        } // while

        totalBitErrors += sum;
        codewordCount++;

        // Save the decoded message
        for (uint32_t i = 0; i < m_k; i++) {
          decodedPayload.push_back(dHat[i] % 2);
        }

        processedBits += m_n;
      } // while not all input samples processed

      std::cout << "Total bit errors = " << totalBitErrors << " for " << (numCodewords*m_k) << " message bits" << std::endl;
      return totalBitErrors;
    }


    uint32_t
    LDPC::getDecodeIterations () const
    {
      return m_decodeIterations;
    }

    void
    LDPC::setDecodeIterations (
        uint32_t decodeIterations)
    {
      if (decodeIterations != m_decodeIterations)
      {
        // TODO update the number of iterations when it's safe
        m_decodeIterations = decodeIterations;
      }
    }

    const Eigen::MatrixXi  &
    LDPC::getParityMatrix() const
    {
      return m_parityCheckMatrix;
    }

    /*!
     * @brief Matrices needed to support encoding
     *
     * @note See Richardson, T., Urbanke, R., "Efficient Encoding of Low-
     * Density Parity-Check Codes". IEEE Trans. on Information Theory,
     * Feb. 2001
     */
    void
    LDPC::m_makeEncoderMatrices()
    {
      // The parity check matrix H is quasi-cyclic by design. I think this means
      // that a the minimum "gap" size (g) is <= Z, the prototype matrix size. We can
      // either just choose that value or search the last column of H for the first
      // non-zero value row index r and calculate g as n - r.

      uint32_t n = m_parityCheckMatrix.cols();   // codeword size
      uint32_t m = m_parityCheckMatrix.rows();   // parity check row count
      uint32_t g = m_pchk->prototypeMatrixSize(); // Assume Z is gap size

      // The objective is to put H into the partial lower-trianglar form
      // described in the paper as
      //
      // H = [ A B T ]
      //     [ C D E ]
      //
      // Where,
      //   A is m - g x n - m
      //   B is m - g x g
      //   T is m - g x m - g
      //   C is     g x n - m
      //   D is     g x g
      //   E is     g x m - g

      Eigen::MatrixXd H = m_parityCheckMatrix.cast <double> ();

      // Extract A, B, C, D, E and T from H
      m_A = Eigen::MatrixXd(m-g,n-m);
      m_A = H.block(0,0,m-g,n-m);
      m_B = Eigen::MatrixXd(m-g,g);
      m_B = H.block(0,n-m,m-g,g);
      Eigen::MatrixXd T(m-g,m-g);
      T = H.block(0,n-m+g,m-g,m-g);
      Eigen::MatrixXd C(g,n-m);
      C = H.block(m-g,0,g,n-m);
      Eigen::MatrixXd D(g,g);
      D = H.block(m-g,n-m,g,g);
      Eigen::MatrixXd E(g,m-g);
      E = H.block(m-g,n-m+g,g,m-g);

      // From the paper, multiply H on the left by equation/term (6)
      //   [I          0]
      //   [-E*inv(T)  I]                                                (6)
      // to get equation/term (7)
      //   [     A                B           T]
      //   [-E*inv(T)*A + C  -E*inv(T)*B + D  0]                         (7)
      //
      // If the codeword x is systematic so that x = [s, p1, p2] where s are
      // the message bits, then the requirement that the parity matrix and the
      // codeword be orthogonal leads to the equation H*trans(x) = trans(0). This
      // leads to equations (8) and (9)
      //   A*trans(s) + B*trans(p1) + T*trans(p2) = 0                    (8)
      //   (-E*inv(T)*A + C)*trans(s) + (-E*inv(T)*B + D)*trans(p1) = 0  (9)
      //

      // create all the rest of the matrices needed to encode messages and, if so
      // desired, check the codewords against the parity check matrix

      Eigen::MatrixXd invT = T.inverse();
      Eigen::MatrixXd EinvT = -(E*invT);

      // From the paper, p1 is calculated using
      //   p1 = mod(-inv(phi)*EinvTA_C*(msg'),2)
      // However, because H is quasi-cyclic, phi is always -I (i.e., -eye(Z).
      // Since the product is forced into GF2 (i.e., elements are 1 or 0), the
      // sign is irrelevant and we can do away with the multiplication by I. That
      // is, we don't need or use phi.

      Eigen::MatrixXd phi = EinvT*m_B + D; // calculate for now, for no good reason except I'm paranoid

      // used to calculate p1 as per above
      m_EinvTA_C = EinvT*m_A + C;

      // save some time in calculating p2 by precalculating these two products
      m_invTA = invT*m_A;
      m_invTB = invT*m_B;

      // Now make sparse versions
      // TODO make sure these are actually used... are there other places?
      m_sA = m_A.sparseView();
      m_sB = m_B.sparseView();
      m_sEinvTA_C = m_EinvTA_C.sparseView();
      m_sinvTA = m_invTA.sparseView();
      m_sinvTB = m_invTB.sparseView();
    }

    void
    LDPC::m_makeDecoderMatrices()
    {
      int maxCheckNodes = 0;
      int maxSymbolNodes = 0;
      // find the largest number of check nodes connected to a symbol node over all
      // symbol nodes
      for (unsigned int sn = 0; sn < m_n; sn++)
      {
        int count = 0;
        for (unsigned int cn = 0; cn < (m_n - m_k); cn++)
          if (m_parityCheckMatrix (cn, sn) > 0) count++;
        if (count > maxCheckNodes) maxCheckNodes = count;
      }

      // find the largest number of symbol nodes connected to a check node over all
      // check nodes
      for (unsigned int cn = 0; cn < (m_n - m_k); cn++)
      {
        int count = 0;
        for (unsigned int sn = 0; sn < m_n; sn++)
          if (m_parityCheckMatrix (cn, sn) > 0) count++;
        if (count > maxSymbolNodes) maxSymbolNodes = count;
      }
#if LDPC_DEBUG_VERBOSE
      std::cout << "maxCheckNodes " << maxCheckNodes << std::endl;
      std::cout << "maxSymbolNodes " << maxSymbolNodes << std::endl;
#endif
      // M(j) represents the set of indexes of all the children parity check nodes
      // connected to the symbol node d(j)
      m_M = Eigen::MatrixXi::Zero (m_n, maxCheckNodes);
      m_M_numCheckNodes = Eigen::VectorXi::Zero (m_n);
      // N(i) represents the set of indexes of all the parent symbol nodes connected
      // to the parity check node h(i)
      m_N = Eigen::MatrixXi::Zero (m_n - m_k, maxSymbolNodes);
      m_N_numSymbolNodes = Eigen::VectorXi::Zero (m_n - m_k);

      // populate M(j) with check nodes connected to a symbol node over all
      // symbol nodes
      for (unsigned int sn = 0; sn < m_n; sn++)
      {
        int count = 0;
        for (unsigned int cn = 0; cn < (m_n - m_k); cn++)
          if (m_parityCheckMatrix (cn, sn) > 0) m_M (sn, count++) = cn;
        m_M_numCheckNodes (sn) = count;
      }

      // populate N(i) symbol nodes connected to a check node over all
      // check nodes
      for (unsigned int cn = 0; cn < (m_n - m_k); cn++)
      {
        int count = 0;
        for (unsigned int sn = 0; sn < m_n; sn++)
          if (m_parityCheckMatrix (cn, sn) > 0) m_N (cn, count++) = sn;
        m_N_numSymbolNodes (cn) = count;
      }

#if LDPC_DEBUG_VERBOSE
      std::cout << "m_M\n" << m_M << std::endl;
      std::cout << "m_M_numCheckNodes\n" << m_M_numCheckNodes << std::endl;
      std::cout << "m_N\n" << m_N << std::endl;
      std::cout << "m_N_numSymbolNodes\n" << m_N_numSymbolNodes << std::endl;
#endif
    }


  } /* namespace darkstar */
} /* namespace xiphos */
