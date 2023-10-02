from xmlrpc.client import ServerProxy


class GNURadioHandler:
    """Uses the xmlrpc package to get and set some server parameters"""

    def __init__(self):
        self.server = ServerProxy('http://localhost:8080')
        self.mode_dict = {0: [1200, 600],
                        1: [2400, 600],
                        2: [4800, 1200],
                        3: [9600, 2400],
                        4: [9600, 4800],
                        5: [19200, 4800],
                        6: [19200, 9600],
                        7: [19200, 19200]}

    def setBaudRate(self, baud):
        self.server.set_baud_bit(baud)

    def setFSKDevHz(self, fsk_dev):
        self.server.set_fsk_dev(fsk_dev)

    def setCenterFreqHz(self, center_freq):
        self.server.set_center_freq(center_freq)

    def setSamplesPerSymbol(self, spsym):
        self.server.set_spsym(spsym)

    def setUHF_RFMode(self, mode):
        if mode < 8:
            self.setBaudRate((self.mode_dict[mode])[0])
            self.setFSKDevHz((self.mode_dict[mode])[1])
        else:
            raise ValueError('Error: invalid UHF RF mode')

    def getBaudRate(self):
        return self.server.get_baud_bit()

    def getFSKDevHz(self):
        return self.server.get_fsk_dev()

    def getUHF_RFMode(self):
        current_rf_config = []
        current_rf_config.append(self.getBaudRate())
        current_rf_config.append(self.getFSKDevHz())
        for key, value in self.mode_dict.items():
            if value == current_rf_config:
                return key
