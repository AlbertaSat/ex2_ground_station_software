from xmlrpc.client import ServerProxy


class GNURadioHandler:

	def __init__(self):	
		self.server = ServerProxy('http://localhost:8080')

	def setBaudRate(self, baud):
		self.server.set_baud_bit(baud)
	
	def setFSKDevHz(self, fsk_dev):
		self.server.set_fsk_dev(fsk_dev)

	def setCenterFreqHz(self, center_freq):
		self.server.set_center_freq(center_freq)

	def setUHF_RFMode(self, mode):
		if mode == 0:
			setBaudRate(1200)
			setFSKDev(600)			
		elif mode == 1:
			setBaudRate(2400)
			setFSKDev(600)			
		elif mode == 2:
			setBaudRate(4800)
			setFSKDev(1200)			
		elif mode == 3:
			setBaudRate(9600)
			setFSKDev(2400)			
		elif mode == 4:
			setBaudRate(9600)
			setFSKDev(4800)			
		elif mode == 5:
			setBaudRate(19200)
			setFSKDev(4800)			
		elif mode == 6:
			setBaudRate(19200)
			setFSKDev(9600)			
		elif mode == 7:
			setBaudRate(19200)
			setFSKDev(19200)			
		else:
			raise Exception('Error: invalid UHF RF mode')
