import subprocess
from pprint import pprint
import os
import datetime

def change_working_dir():
    path = os.path.abspath(__file__)

    split = path.split("/")[0:-1]
    split.append("ftp")
    new_path = "/".join(split)
    os.chdir(new_path)


class logger():
    def __init__(self, path="ftp_log/log.txt"):
        self.log_file = self.create_ftp_log(path)
        
    def create_ftp_log(self, path):
        if not os.path.exists("ftp_log"):
            os.makedirs("ftp_log")

        file = open(path, "a")
        return file

    def close(self):
        self.log_file.close()

    def log(self, stuff):
        self.log_file.writelines(str(datetime.datetime.today()) + ":" + stuff)

def get_request(sat_path, file_path, block=True):
    change_working_dir()
    
    #print("need sudo password for opening /dev/ttyUSB0")
    cmd = ["sudo", "./ftp", "-i", "10", "-c", "1", "-k", "/dev/ttyUSB0", "-f", 'GET {0}|{1}'.format(sat_path, file_path)]

    if block:
        output = subprocess.run(cmd)
        print(output)
        return 

    #subprocess.Popen(cmd)
    
def put_request(file_path, sat_path, block=True):
    change_working_dir()
    
    #print("need sudo password for opening /dev/ttyUSB0")
    cmd = ["sudo", "./ftp", "-i", "10", "-c", "1", "-k", "/dev/ttyUSB0", "-f", 'PUT {0}|{1}'.format(file_path, sat_path)]
    
    if block:
        output = subprocess.run(cmd)
        print(output)
        return
    
    #subprocess.Popen(cmd)


if __name__ == "__main__":
    print("thats not how you use this, please import either 'get_request' or 'put_request' into your program")
