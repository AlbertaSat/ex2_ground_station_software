  /*!
 * @file ppdu_u8.h
 * @author Steven Knudsen
 * @date May 10, 2021
 *
 * @details The PHY PDU class for 8-bit data.
 *
 * @copyright University of Alberta 2021
 *
 * @license
 * This software may not be modified or distributed in any form, except as described in the LICENSE file.
 */

#ifndef EX2_SDR_PHY_LAYER_PDU_PPDU_U8_H_
#define EX2_SDR_PHY_LAYER_PDU_PPDU_U8_H_

#include <functional>

#include "pdu.hpp"

namespace ex2
{
  namespace sdr
  {
    /*!
     * @brief PHY PDU class that contains @p uint8_t symbols.
     *
     * @details This class defines a PHY PDU containing @p uint8_t symbols.
     * A symbol is a mapping of 1 to 8 data bits.
     *
     * Symbols may be "unpacked", which means there is one symbol per byte
     * in the PDU. Or they may be "packed" so that a minimum number of bits
     * in the PDU are used. For example, a symbol with 2 data bits will
     * occupy 2 bits per byte in an unpacked representation. Four, 2-bit symbols
     * occupy a byte in a packed representation.
     *
     * In the unpacked representation, symbols bits are placed in the byte's
     * least significant bits.
     */

    class PPDU_u8 :
        public PDU<uint8_t>
    {
      /*!
       * @details Make @p crc a friend so that we can avoid copying the payload
       * for CRC operations.
       */
      friend class crc;

    public:

      /*!
       * @brief PPDU function type.
       */
      typedef std::function< void(PPDU_u8&) > ppdu_function_t;

        enum  BitsPerSymbol {
        BPSymb_1 = 1,
        BPSymb_2 = 2,
        BPSymb_3 = 3,
        BPSymb_4 = 4,
        BPSymb_5 = 5,
        BPSymb_6 = 6,
        BPSymb_7 = 7,
        BPSymb_8 = 8
      };

      /*!
       * @brief Default Constructor
       *
       * @param[in] bps The number of bits per symbol
       *
       * @note The default @p bps value is 8 bits per symbol. This let's you
       * make a PPDU_u8 that is packed, which is convenient when constructing
       * with a bit stream (i.e., symbols are concatenated)
       */
        PPDU_u8 (const BitsPerSymbol bps = BitsPerSymbol::BPSymb_8);

      /*!
       * @brief Constructor
       *
       * @param[in] payload unsigned 8-bit data, which is copied
       * @param[in] bps The number of bits per symbol
       *
       * @note The default @p bps value is 8 bits per symbol. This let's you
       * make a PPDU_u8 that is packed, which is convenient when constructing
       * with a bit stream (i.e., symbols are concatenated)
       */
        PPDU_u8 (
        const payload_t& payload,
        const BitsPerSymbol bps = BitsPerSymbol::BPSymb_8);

      virtual
      ~PPDU_u8 ();

      /*!
       * @brief Append the payload from another @p PPDU_u8 to this one.
       *
       * @param[in] ppdu A payload to append, which is copied.
       */
      void
      append(PPDU_u8& ppdu);

      /*!
       * @brief Bits per symbol accessor.
       *
       * @return Bits per symbol.
       */
      BitsPerSymbol
      getBps () const;

      /*!
       * @brief Repack the symbols.
       *
       * @details Repack the symbols based on the new bits per symbol setting.
       *
       * @param[in] newBps New number of bits per symbol
       */
      void repack(BitsPerSymbol newBps);

      /*!
       * @brief reverse the order of the payload
       *
       * @param[in] byteLevel If true, the bytes of the payload are reversed,
       * otherwise the payload bits are reversed.
       */
      void reverse(bool byteLevel);

      /*!
       * @brief Indicate if the payload is reversed.
       *
       * @return true if the payload is reversed, false otherwise.
       */
      bool isReversed() const {
        return m_reversed;
      }

      /*!
       * @brief Roll the payload bits right or left a number of bit positions.
       *
       * @param[in] numBits The number of bit positions to roll the vector
       * @param[in] left If true, roll the bits left. Otherwise roll right.
       */
      void roll(uint32_t numBits, bool left);

    private:

      typedef payload_t::pointer data_ptr_t;

      void
      append (
        const uint8_t *data,
        const size_t count);

      /*!
       * @brief Pack 1-bit symbols into bytes
       */
      void pack();

      /*!
       * @brief Unpack bytes into 1-bit symbols
       */
      void unpack();

      BitsPerSymbol m_bps;
      bool m_reversed;
    };

  } /* namespace sdr */
} /* namespace ex2 */

#endif /* EX2_SDR_PHY_LAYER_PDU_PPDU_U8_H_ */
