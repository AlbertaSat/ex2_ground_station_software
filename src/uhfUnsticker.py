import GNURadioHandler
import uTransceiver
import time

# Changes satellite from mode 0 to default mode (mode 4)
# Sleeps added to ensure no conflicts or race conditions due to
# time of command transfer
if __name__ == '__main__':
    gnuradio = GNURadioHandler.GNURadioHandler()
    utrns = uTransceiver.uTransceiver()
    gnuradio.setUHF_RFMode(0)
    time.sleep(1)
    utrns.UHFDIRCommand('UHFDIR_genericWrite(0, 0 3 0 4 0 1 1 0 0 0 0 0)')
    time.sleep(1)
    gnuradio.setUHF_RFMode(4)

