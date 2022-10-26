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
			self.setBaudRate(1200)
			self.setFSKDev(600)			
		elif mode == 1:
			self.setBaudRate(2400)
			self.setFSKDev(600)			
		elif mode == 2:
			self.setBaudRate(4800)
			self.setFSKDev(1200)			
		elif mode == 3:
			self.setBaudRate(9600)
			self.setFSKDev(2400)			
		elif mode == 4:
			self.setBaudRate(9600)
			self.setFSKDev(4800)			
		elif mode == 5:
			self.setBaudRate(19200)
			self.setFSKDev(4800)			
		elif mode == 6:
			self.setBaudRate(19200)
			self.setFSKDev(9600)			
		elif mode == 7:
			self.setBaudRate(19200)
			self.setFSKDev(19200)			
		else:
			raise ValueError('Error: invalid UHF RF mode')
