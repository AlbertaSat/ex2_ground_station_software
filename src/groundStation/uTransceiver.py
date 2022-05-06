from ctypes import cdll, c_int, c_char
import sys
import zmq
import threading

uhf = cdll.LoadLibrary('../../ex2_uhf_software/uTransceiver.so')#consider making an env var for this?

# command format follows https://docs.google.com/spreadsheets/d/1zNhxhs0KJCp1187Vm3-zAzQHCY31f77l-0nlQmfXu1w/edit#gid=565953736
# but with UHFDIR_ instead of UHF_ prefix. See document for examples

#After sending a uhf-direct command, terminal displays all rx'd raw ASCII data for listentimeout_s

class uTransceiver(object):

    listentimeout_s = 1.0
    pipetimeout_s = 30.0
    listen_en = False
    pipe_en = False

    def __init__(self, opts):

    def resetListenTimer(self):
        uTransceiver.listen_en = False

    def resetPipeTimer(self):
        uTransceiver.pipe_en = False

    def listen(self):
        port = "0002"

        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect ("tcp://localhost:%s" % port)
        socket.setsockopt(zmq.SUBSCRIBE, "")

        while uTransceiver.listen_en is True:
            print(socket.recv())

        socket.disconnect("tcp://localhost:%s" % port)

    def enterPipeMode(self):
        if groundStation.uhf_en is True:
            if uTransceiver.pipe_en is False:
                #current config is for RF mode 5, baudrate = 115200
                uTransceiver.UHFDIRCommand('UHFDIR_genericWrite(0, 0 3 0 5 0 0 0 0 0 0 1 1)')
                uTransceiver.pipe_en = True
                timer = threading.Timer(uTransceiver.pipetimeout_s, uTransceiver.resetPipeTimer())

                #TODO: send "tell Athena pipe mode is enabled" command here once implemented
        else:
            print('UHF functionality not enabled. Please run CLI with -u flag to enable.')

    def UHFDIRCommand(self, str):
        if groundStation.uhf_en is True:
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
            if uTransceiver.pipe_en is False:
                retval = 0
                if cmd is 'genericWrite':
                    retval = uhf.UHF_genericWrite(cmd, arg)
                if cmd is 'genericRead':
                    voidptr = (ctypes.c_void_p * len(objs))()
                    uhf.UHF_genericRead(cmd, voidptr)
                if cmd is 'genericI2C':
                    #TODO someday
                    #retval = uhf.UHF_genericI2C(cmd, )

                #This should be a catch-all for any syntax errors as-is
                #TODO: make more robust handler for incorrect inputs to prevent erronious commands being sent?
                if retval is not 0:
                    print('UHF Equipment Handler error' + retval)

                uTransceiver.listen_en = True
                timer = threading.Timer(uTransceiver.listentimeout_s, uTransceiver.resetListenTimer())
                uTransceiver.listen()
            else:
                print('Error: Command not sent. Wait for pipe mode to expire')
                print('Pipe mode timer set to ' + uTransceiver.pipetimeout_s + 's')
        else:
            print('UHF functionality not enabled. Please run CLI with -u flag to enable.')


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
