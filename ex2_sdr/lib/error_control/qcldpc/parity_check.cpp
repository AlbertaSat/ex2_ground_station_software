/*!
 * @file partity_check.cpp
 * @author Steven Knudsen
 * @date June 18, 2019
 *
 * @details
 *
 * @copyright Xiphos Systems Corp. 2019
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#include "parity_check.h"

#include <boost/foreach.hpp>
#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>
#include <iostream>
#include <fstream>
#include <stdexcept>
#include <sys/stat.h>

#include "matrix2d.h"

namespace xiphos
{
  namespace darkstar
  {
    class ParityCheckException: public std::exception {
    private:
      std::string message_;
    public:
      explicit ParityCheckException(const std::string& message);
      virtual const char* what() const throw() {
        return message_.c_str();
      }
    };

    ParityCheckException::ParityCheckException(const std::string& message) : message_(message) {
    }


    ParityCheck::ParityCheck (
        ErrorCorrection::ErrorCorrectionCoding errorCorrectionCoding,
        ErrorCorrection::CodingRate codingRate)
    {
      m_errorCorrection = new ErrorCorrection(errorCorrectionCoding, codingRate);
      m_makeParityCheckMatrix();
      m_rank = m_parityCheckMatrix.rows();
      m_valid = m_rank > 0;
    }

    ParityCheck::~ParityCheck ()
    {
    }

    bool ParityCheck::isValid() const
    {
      return m_valid;
    }

    Eigen::MatrixXi & ParityCheck::parityCheckMatrix()
    {
      return m_parityCheckMatrix;
    }

    Eigen::MatrixXd  & ParityCheck::parityCheckMatrixDouble()
    {
      return m_parityCheckMatrixDouble;
    }

    Eigen::SparseMatrix<double>  & ParityCheck::parityCheckMatrixSparse()
    {
      return m_parityCheckMatrixSparse;
    }

    unsigned int ParityCheck::prototypeMatrixSize()
    {
      return m_submatrixSize();
    }

    unsigned int ParityCheck::rank()
    {
      return m_rank;
    }

    unsigned int
    ParityCheck::m_submatrixSize() const
    {
      unsigned int size = 0;
      switch(m_errorCorrection->errorCorrection()) {
        case ErrorCorrection::ErrorCorrectionCoding::LDPC_IEEE_648:
          size = k_submatrix27x27Size;
          break;
        case ErrorCorrection::ErrorCorrectionCoding::LDPC_IEEE_1296:
          size = k_submatrix54x54Size;
          break;
        case ErrorCorrection::ErrorCorrectionCoding::LDPC_IEEE_1944:
          size = k_submatrix81x81Size;
          break;
        case ErrorCorrection::ErrorCorrectionCoding::LDPC_DVB_S2_64800:
        case ErrorCorrection::ErrorCorrectionCoding::LDPC_ARxA_1024:
        case ErrorCorrection::ErrorCorrectionCoding::LDPC_ARxA_4096:
        case ErrorCorrection::ErrorCorrectionCoding::LDPC_ARxA_16384:
        case ErrorCorrection::ErrorCorrectionCoding::LDPC_CCSDS_131_1024:
        case ErrorCorrection::ErrorCorrectionCoding::LDPC_CCSDS_131_4096:
        case ErrorCorrection::ErrorCorrectionCoding::LDPC_CCSDS_131_8160:
        case ErrorCorrection::ErrorCorrectionCoding::LDPC_CCSDS_131_16384:
        case ErrorCorrection::ErrorCorrectionCoding::LDPC_FIRST:
        case ErrorCorrection::ErrorCorrectionCoding::LDPC_LAST:
        default:
          break;
      }
      return size;
    }

    unsigned int
    ParityCheck::m_submatricesPerColumn() const
    {
      int spc = 0;
      switch (m_errorCorrection->codingRate()) {
        case ErrorCorrection::CodingRate::RATE_1_2:
          spc = 12;
          break;
        case ErrorCorrection::CodingRate::RATE_2_3:
          spc = 8;
          break;
        case ErrorCorrection::CodingRate::RATE_3_4:
          spc = 6;
          break;
        case ErrorCorrection::CodingRate::RATE_5_6:
          spc = 4;
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
      return spc;
    }

    Eigen::MatrixXi ParityCheck::m_read_proto_h()
    {
      // check if correct prototype file exists
      std::string pathToPrototypeHfile(PATH_TO_PROTO_H);
      pathToPrototypeHfile.append("/");
      pathToPrototypeHfile.append(m_proto_h_filename());

      struct stat buffer;
      if (stat(pathToPrototypeHfile.c_str(), &buffer) != 0) {
        throw std::runtime_error((boost::format("ParityCheck: Unable to find %s") % pathToPrototypeHfile.c_str()).str());
      }

      // Need the correct number of rows and columns for this codeword and rate
      unsigned int rows = m_submatricesPerColumn();
      unsigned int cols = k_submatricesPerRow;
      Eigen::MatrixXi protoH(rows,cols);

      std::string line;
      std::ifstream infile;
      infile.open(pathToPrototypeHfile.c_str(), std::ifstream::in | std::ifstream::binary);

      unsigned int row_count = 0;
      bool col_count_okay = true;
      while (! infile.eof()) {
        std::getline(infile, line);

        if (row_count >= rows)
          throw std::runtime_error((boost::format("ParityCheck: %s has wrong number of rows.") % pathToPrototypeHfile.c_str()).str());

        std::vector<std::string> dataLine;
        boost::trim_if(line, boost::is_any_of("\t "));
        boost::split(dataLine, line, boost::is_any_of("\t "), boost::token_compress_on);

        col_count_okay = col_count_okay and (dataLine.size() == cols);
        if (!col_count_okay)
          throw std::runtime_error((boost::format("ParityCheck: %s has wrong number of cols.") % pathToPrototypeHfile.c_str()).str());

        int n, j = 0;
        BOOST_FOREACH( std::string & s, dataLine ) {
          std::istringstream(s) >> n;
          protoH(row_count,j++) = n;
        }
        row_count++;
      } //while not EOF

      infile.close();

      if (row_count != rows or !col_count_okay) {
        throw std::runtime_error((boost::format("ParityCheck: %s has bad contents.") % pathToPrototypeHfile.c_str()).str());
      }

      return protoH;
    }

    void ParityCheck::m_makeParityCheckMatrix()
    {
      unsigned int submatrix_size = m_submatrixSize();
      unsigned int cols = submatrix_size*k_submatricesPerRow;
      unsigned int rows = submatrix_size*m_submatricesPerColumn();

      Eigen::MatrixXi proto_h;
      try {
        proto_h = m_read_proto_h();
      }
      catch (std::runtime_error& re) {
        m_valid = false;
        throw ParityCheckException("Unable to read parity check prototype");
      }

      m_parityCheckMatrix = Eigen::MatrixXi::Zero(rows,cols);

      unsigned int iH, jH;
      for (unsigned int i = 0; i < m_submatricesPerColumn(); i++) {
        for (unsigned int j = 0; j < k_submatricesPerRow; j++) {
          if (proto_h(i,j) >= 0)
          {
            Eigen::MatrixXi A = Eigen::MatrixXi::Identity(submatrix_size,submatrix_size);
            unsigned int k = proto_h(i,j);
            iH = i*submatrix_size;
            jH = j*submatrix_size;
            m_parityCheckMatrix.block(iH,jH,submatrix_size,submatrix_size) = rotate<Eigen::MatrixXi> (A,0,false,k,false);
          }
        }
      }

      m_parityCheckMatrixDouble = m_parityCheckMatrix.cast<double> ();
      m_parityCheckMatrixSparse = m_parityCheckMatrixDouble.sparseView();
    }

  } /* namespace darkstar */
} /* namespace xiphos */
