# UHF Transceiver Equipment Handler
The EnduroSat UHF Transceiver type II is a half-duplex transceiver we will be using for downlinking housekeeping data and uplinking commands. The code in this repository follow's EnduroSat's command format to allow us to read and write parameters and collect housekeeping data from the board. I2C and UART communications have been mocked using CMock. Functions implemented here are also listed in the ["S-Band and
UHF Functions List" spreadsheet](https://docs.google.com/spreadsheets/d/1zNhxhs0KJCp1187Vm3-zAzQHCY31f77l-0nlQmfXu1w/edit#gid=565953736) on the drive. Refer to that for details about input/output.

## Building on OBC vs Ground Station
If building on OBC, ensure IS_SATELLITE is defined in the project. If it is not, commands will not be sent/received from the actual Transceiver.

If building on Ground Station, note that data received by the ground station radio is not handled by this code, but is instead handled separately by the ex2_ground_station_software code.

## Ceedling Build Instructions
First, [install Ceedling](https://github.com/ThrowTheSwitch/Ceedling). Then run:
```
git clone https://github.com/AlbertaSat/ex2_uhf_software
cd ex2_uhf_software/CommsSim
ceedling
```
The above instructions should run all unit tests of the UHF Transceiver Equipment Handler

## Error Reporting

![error reporting](./Docs/UHF_Error_Reporting.png)
