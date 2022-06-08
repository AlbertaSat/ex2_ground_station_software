import ctypes
from ctypes import cdll, c_int, c_char
import sys
import zmq
import threading
import os.path
import socket
import time
from enum import Enum

# command format follows https://docs.google.com/spreadsheets/d/1zNhxhs0KJCp1187Vm3-zAzQHCY31f77l-0nlQmfXu1w/edit#gid=565953736
# but with UHFDIR_ instead of UHF_ prefix. See document for examples

#After sending a uhf-direct command, terminal displays all rx'd raw ASCII data for listentimeout_s

class UHF_return(Enum):
    U_GOOD_CONFIG =  0
    U_BAD_CONFIG  = -1
    U_BAD_PARAM   = -2
    U_BAD_ANS_CRC = -3
    U_BAD_CMD_CRC = -4
    U_BAD_CMD_LEN = -5
    U_CMD_SPEC_2 = 2
    U_CMD_SPEC_3 = 3
    U_UNK_ERR = -10
    IS_STUBBED_U = 0 # Used for stubbed UHF in hardware interface
    U_I2C_IN_PIPE = 4

class uTransceiver(object):

    def __init__(self, opt):
        self.listentimeout_s = 2.0
        self.pipetimeout_s = 20.0
        self.last_tx_time = 0
        self.listen_en = False
        self.pipe_en = False
        self.u = opt
        self.uhf = cdll.LoadLibrary("./ex2_uhf_software/uTransceiver.so")#consider making an env var for this?

    def resetListenTimer(self):
        self.listen_en = False
    def listen(self):
        port = 4321

        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://localhost:%s" % port)
        socket.setsockopt(zmq.SUBSCRIBE, b"")
        #socket.RCVTIMEO = 100 #for testing purposes

        # Initialize poll set
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)

        #for testing purposes
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.connect(("127.0.0.1", port))

        print('Received from UHF:')
        self.listen_en = True
        start = time.time()
        while (time.time() - start) < self.listentimeout_s:

            #for testing purposes
            #print('here')
            # data = s.recv(10000)
            # print(repr(data))

            if dict(poller.poll())[socket] == zmq.POLLIN:
                print(socket.recv(zmq.DONTWAIT))#for testing purposes

        socket.disconnect("tcp://localhost:%s" % port)
        # s.close() #for testing purposes

    def enterPipeMode(self):
            #current config is for RF mode 5, baudrate = 115200
            print("sending pipe cmd")
            self.UHFDIRCommand('UHFDIR_genericWrite(0, 0 3 0 5 0 0 1 0 0 0 1 1)')

    def UHFDIRCommand(self, string):
        if self.u == True:
            print("sending UHFDIRcommand: " + string)
            cmd = (string.split('_')[1]).split('(')[0]
            cmdcode = string.split(',')[0]
            cmdcode = int(cmdcode.split('(')[1])

            param = string.split(',')[1]
            param = param.split(')')[0]
            #parse param into correct ctypes based on cmdcode
            if cmdcode == 0:
                paramlist = param.split()
                paramlist = list(map(int, paramlist))
                arg = (ctypes.c_ubyte * len(paramlist))(*paramlist)#is this a pointer or just a list?

                #arg = ctypes.cast(args, ctypes.POINTER(ctypes.c_ubyte))
            if cmdcode == 6:
                param = ctypes.c_uint16(param) #TODO check that this works with space after comma in command
                arg = ctypes.cast(param, ctypes.POINTER(ctypes.c_uint16))
            if cmdcode == 253:
                pass
                #TODO someday (FRAM usage)

            #check command and call relevant functions with args
            if (time.time() - self.last_tx_time) > 0:# change 0 to self.pipetimeout_s
                retval = 0
                if cmd == 'genericWrite':
                    retval = self.uhf.UHF_genericWrite(ctypes.c_ubyte(cmdcode), arg)
                if cmd == 'genericRead':
                    voidptr = (ctypes.c_void_p * 1)()
                    self.uhf.UHF_genericRead(cmdcode, voidptr)
                if cmd == 'genericI2C':
                    pass
                    #TODO someday
                    #retval = uhf.UHF_genericI2C(cmd, )

                #This should be a catch-all for any syntax errors as-is
                #TODO: make more robust handler for incorrect inputs to prevent erronious commands being sent?
                if retval != 0:
                    print('UHF Equipment Handler error ' + UHF_return(retval).name)
                time.sleep(0.5)
                #self.listen()
            else:
                print('Error: Command not sent. Wait for pipe mode to expire')
                print('Pipe mode timer set to ' + str(self.pipetimeout_s) + 's')
        else:
            print('UHF functionality not enabled. Please run CLI with -u flag to enable.')
