/*!
 * @file scrambler.h
 * @author Steven Knudsen
 * @date April 13, 2021
 *
 * @details See class description below
 *
 * @copyright University of Alberta 2021
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#ifndef EX2_SDR_ERROR_CONTROL_SCRAMBLER_H_
#define EX2_SDR_ERROR_CONTROL_SCRAMBLER_H_

#include <cstdint>

#include "ppdu_u8.hpp"
#include "galoisLFSR.h"

namespace ex2 {
  namespace sdr {


    /*!
     * @brief Class Scrambler
     *
     * @todo This should be templated!
     *
     * @details Scramble bits is based on a Pseudo-random Binary Sequence (PRBS). The design is
     * arithmetic (as opposed to multiplicative) and uses a Maximum Length Sequence
     * Linear Feedback Shift Register (MLS LFSR). The LFSR polynomial can be specified,
     * or will default to a 16-bit MLS LFSR based on 1 + x^11 + +x^13 + x^14 + x^16, which
     * is specified as
     *   uint64_t polynomial = 0x000000000000B400;
     *
     * @see Xilinx, Efficient Shift Registers, LFSR Counters, and Long Pseudo-Random Sequence
     * Generators, application note (xapp052.pdf)[https://www.xilinx.com/support/documentation/application_notes/xapp052.pdf]
     * for other examples, though we don't use the n=16 polynomial suggested there
     *
     * @todo insert diagram
     */
    class Scrambler {
    public:

      /*!
       * @brief The initial shift register fill; 0x0234 extended to 64 bits.
       *
       * @warning Never change this otherwise any previously scrambled data
       * will not be unscrambled.
       *
       * @todo Perhaps this should be private?
       */
      static const uint64_t InitialRegisterFill = 0x0000000000000234;

      /*!
       * @brief Constructor
       *
       * @details Scrambler that defaults to a 16 bit MLS
       *
       * @param[in] polynomial The LFSR polynomial @see lfsr.h
       * @param[in] initialRegisterFill The initial register fill.
       *
       * @warning The @p initialRegisterFill must be the same if the @p Scrambler
       * class is used to create scramble and descramble bit sequences.
       */
      Scrambler(uint64_t polynomial = GaloisLFSR::polynomialForOrder(16),
          uint64_t initialRegisterFill = Scrambler::InitialRegisterFill);

      ~Scrambler();

      /*!
       * @brief Scramble (descramble) a payload
       *
       * @param[in] original Input byte vector aka payload
       * @param[inout] scrambled Scrambled @p original
       *
       * @todo Should be able to scramble in-place
       */
      void scramble(PPDU_u8::payload_t& original,
          PPDU_u8::payload_t& scrambled);

      /*!
       * @brief Scramble (descramble) a vector
       *
       * @param[in] original Input float vector
       * @param[inout] scrambled Scrambled @p original
       *
       * @todo Should be able to scramble in-place
       */
      void scramble(std::vector<float>& original,
          std::vector<float>& scrambled);

      /*!
       * @brief Scramble (descramble) a vector
       *
       * @param[in] original Input complex float vector
       * @param[inout] scrambled Scrambled @p original
       *
       * @todo Should be able to scramble in-place
       */
      void scramble(std::vector<std::complex<float>>& original,
          std::vector<std::complex<float>>& scrambled);

    private:
      GaloisLFSR *m_lfsr;

      // support for bit reversal
      uint8_t bitReverse(uint8_t byte);
    };

  } /* namespace sdr */
} /* namespace ex2 */

#endif /* EX2_SDR_ERROR_CONTROL_SCRAMBLER_H_ */
