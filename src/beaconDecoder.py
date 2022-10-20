import socket
import numpy as np


class beaconDecoder:

	def __init__(self):
		#note: certain beacon fields have specially formatted data. Future TODO is to implement that special display formatting here.
		self.beaconDict_1 = {
			"time": '>u4',
			"packet_number": '>u1',
			"switch_stat": '>u1',
			"eps_mode": '>u1',
			"battery_voltage": '>u2',
			"battery_input_current": '>u2',
			"current_channel_1": '>u2',
			"current_channel_2": '>u2',
			"current_channel_3": '>u2',
			"current_channel_4": '>u2',
			"current_channel_5": '>u2',
			"current_channel_6": '>u2',
			"current_channel_7": '>u2',
			"current_channel_8": '>u2',
			"current_channel_9": '>u2',
			"current_channel_10": '>u2',
			"output_status": '>u2',
			"output_faults_1": '>u1',
			"output_faults_2": '>u1',
			"output_faults_3": '>u1',
			"output_faults_4": '>u1',
			"output_faults_5": '>u1',
			"output_faults_6": '>u1',
			"output_faults_7": '>u1',
			"output_faults_8": '>u1',
			"output_faults_9": '>u1',
			"output_faults_10": '>u1',
			"EPS_boot_count": '>u2',
			"eps_last_reset_reason": '>u1',
			"gs_wdt_time": '>u4',
			"gs_wdt_cnt": '>u1',
			"obc_wdt_toggles": '>u1',
			"obc_wdt_turnoffs": '>u1',
		}
    
		self.beaconDict_2 = {
			"time": '>u4',
			"packet_number": '>u1',
			"temp_1": '>i1',
			"temp_2": '>i1',
			"temp_3": '>i1',
			"temp_4": '>i1',
			"temp_5": '>i1',
			"temp_6": '>i1',
			"temp_7": '>i1',
			"temp_8": '>i1',
			"temp_9": '>i1',
			"temp_10": '>i1',
			"temp_11": '>i1',
			"temp_12": '>i1',
			"temp_13": '>i1',
			"temp_14": '>i1',
			"temp_15": '>i1',
			"temp_16": '>i1',
			"temp_17": '>i1',
			"angular_rate_X": '>i1',
			"angular_rate_Y": '>i1',
			"angular_rate_Z": '>i1',
			"adcs_control_mode": '>i1',
			"uhf_uptime": '>u2',
			"payload_software_version": '>u1',
			"obc_boot_count": '>u2',
			"obc_last_reset_reason": '>u1',
			"obc_mode": '>u1',
			"obc_uptime": '>u2',
			"solar_panel_supply_current": '>u1',
			"obc_software_version": '>u1',
			"cmds_received": '>u2',
			
		}

		self.rxport = 4322
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(("127.0.0.1", self.rxport))

	
	def run(self):
		while True:
			self.rawdata = s.recv(10000)
			print("Beacon Received:")
			idx = 0;
			if rawdata[5] == 1:
				currentbeacon_t = self.beaconDict_1
			elif rawdata[5] == 2:
				currentbeacon_t = self.beaconDict_2
			else:
				print('Received beacon with invalid packet number' + rawdata[5])			
			for field in currentbeacon_t: 
				try:
				    output[field] = np.frombuffer(
					self.rawdata, dtype=currentbeacon_t[field], count=1, offset=idx)[0]
				except:
				    output[field] = None
				idx += np.dtype(currentbeacon_t[field]).itemsize
			print(output)

if __name__ == '__main__':
	decoder = beaconDecoder()
	decoder.run()	
