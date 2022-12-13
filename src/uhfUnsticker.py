import GNURadioHandler
import uTransceiver
import time

# Changes satellite from mode 0 to default mode (mode 4)
if __name__ == '__main__':
    gnuradio = GNURadioHandler.GNURadioHandler()
    utrns = uTransceiver.uTransceiver()
    gnuradio.setUHF_RFMode(0)
    utrns.UHFDIRCommand('UHFDIR_genericWrite(0, 0 3 0 4 0 1 1 0 0 0 0 0)')
    gnuradio.setUHF_RFMode(4)

