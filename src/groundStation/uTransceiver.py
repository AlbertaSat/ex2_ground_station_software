from ctypes import cdll, c_int, c_char
import sys
import zmq
import threading

uhf = cdll.LoadLibrary('../../ex2_uhf_software/uTransceiver.so')#consider making an env var for this?

# command format follows https://docs.google.com/spreadsheets/d/1zNhxhs0KJCp1187Vm3-zAzQHCY31f77l-0nlQmfXu1w/edit#gid=565953736
# but with UHFDIR_ instead of UHF_ prefix. See document for examples

#After sending a uhf-direct command, terminal displays all rx'd raw ASCII data for listentimeout_s

class uTransceiver(object):

    listentimeout_s = 1
    listen_en = False

    def __init__(self, opts):

    def listen_rst(self):
        listen_en = False

    def listen(self):
        port = "0002"

        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect ("tcp://localhost:%s" % port)
        socket.setsockopt(zmq.SUBSCRIBE, "")

        while listen_en is True:
            print(socket.recv())

        socket.disconnect("tcp://localhost:%s" % port)


    def parseUHFDIRCommand(self, str):

        cmd = (str.split('_')[1]).split('(')[0]
        cmdcode = str.split(',')[0]

        param = str.split(',')[1]
        param = param.split(')')[0]

        #parse param into correct ctypes based on cmdcode
        if cmdcode is 0:
            paramlist = param.split()
            paramlist = list(map(int, paramlist))
            arg = (c_ubyte * 12)(*paramlist)#is this a pointer or just a list?
            #args = ctypes.cast(args, ctypes.POINTER(ctypes.c_ubyte))
        if cmdcode is 6:
            param = ctypes.c_uint16(param) #TODO check that this works with space after comma in command
            arg = ctypes.cast(param, ctypes.POINTER(ctypes.c_uint16))
        if cmdcode is 253:
            #TODO someday (FRAM usage)

        #check command and call relevant functions with args
        retval = 0
        if cmd is 'genericWrite':
            retval = uhf.UHF_genericWrite(cmd, arg)
        if cmd is 'genericRead':
            voidptr = (ctypes.c_void_p * len(objs))()
            uhf.UHF_genericRead(cmd, voidptr)
        if cmd is 'genericI2C':
            #TODO someday
            #retval = uhf.UHF_genericI2C(cmd, )

        #This should be a catch-all for any syntax errors
        #TODO: make more robust handler for incorrect inputs to prevent erronious commands being sent?
        if retval is not 0:
            print('UHF Equipment Handler error' + retval)

        listen_en = True
        timer = threading.Timer(uTransceiver.listentimeout_s, listen_rst)
        uTransceiver.listen()


#typedef enum{
#	U_GOOD_CONFIG =  0,
#	U_BAD_CONFIG  = -1,
#	U_BAD_PARAM   = -2,
#	U_BAD_ANS_CRC = -3,
#
 # U_BAD_CMD_CRC = -4,
#  U_BAD_CMD_LEN = -5,
#  U_CMD_SPEC_2 = 2,
#  U_CMD_SPEC_3 = 3,

#  U_UNK_ERR = -10,
#  IS_STUBBED_U = 0, // Used for stubbed UHF in hardware interface

#  U_I2C_IN_PIPE = 4
#} UHF_return;
