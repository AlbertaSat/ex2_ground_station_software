Src contains functions to access s-band transmitter functionality. These read and/or write each register outlined in the HSTXC-01-00090 User Manual.
These functions should be used in other code as needed to configure and get housekeeping 
data from the S-Band transmitter. Since we don't have the actual hardware, i2c and spi communication has 
to be mocked using CMock. Other simulated aspects include the register "memory" and the buffer, which stores data prior to transmission. There are functions to add and remove from this buffer. Though no data is actually stored, the buffer count, underrun, overrun, and status of the transmit ready line should be accurate.
Refer to the User Manual for more details or the "Simulate an S-Band transmitter" task in clickup. Functions are listed in the "S-Band and 
UHF Functions List" spreadsheet on the drive. Refer to that for details about input/output.

Test contains the ceedling test file.
