# Northern Images (NIM) Response Table
The following two tables contains all of the possible responses and error codes from the NIM payload.
git
## Error codes given by the OBC
| Decimal | Hex | Error |
|:-------:|:---:|:-----|
| 0 | 0x00 | OK |
| 1 | 0x01 | Fail |
| 2 | 0x02 | Hanlder Busy |
| 3 | 0x03 | UART Fail |
| 4 | 0x04 | UART Busy |
| 5 | 0x05 | Malloc Fail |

## Error codes given by NIM
| ASCII | Decimal | Hex | Error |
|:-----:|:-------:|:---:|:-----|
| 0 | 48 | 0x30 | Command Not Recognized               |
| 1 | 49 | 0x31 | Command Definition Out of Bounds     |
| 2 | 50 | 0x32 | Second Byte Time Out                 |
| 3 | 51 | 0x33 | Triplcate Mismatch                   |
| 4 | 52 | 0x34 | SD Not Available                     |
| 5 | 53 | 0x35 | No Such File                         |
| 6 | 54 | 0x36 | Camera Failure                       |
| 7 | 55 | 0x37 | File Receive Failure                 |
| A | 65 | 0x41 | No artwork saved on payload.         |
| B | 66 | 0x42 | No room for more artwork on payload. |
| C | 67 | 0x43 | No images saved on payload.          |
| D | 68 | 0x44 | No room for more images on payload.  |
| E | 69 | 0x45 | Second Byte Not Recognized           |