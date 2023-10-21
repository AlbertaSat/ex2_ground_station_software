'''
 * Copyright (C) 2022  University of Alberta
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
'''
'''
 * @file interactiveHandler.py
 * @author Robert Taylor
 * @date 2022-07-21
'''

from system import services
from dummyUtils import generateFakeHKDict
from inputParser import InputParser
from receiveParser import ReceiveParser
from embedCSP import EmbedPacket
import GNURadioHandler
import libcsp_py3 as libcsp
from uTransceiver import uTransceiver
import time

hkCommands = ["GET_HK", "GET_INSTANT_HK", "GET_LATEST_HK"]; # List of HK commands that need a special handler

class InteractiveHandler:
    def __init__(self, dummy=False):
        self.services = services
        self.inParser = InputParser()
        self.dummy = dummy # Use dummy responses instead
        self.fake_hk_id = 1 # Dummy value for HK dataPosition

        # TODO: This is bad, make it good when fixing inputParser
        self.appIdx = 0
        self.serviceIdx = 2
        self.subserviceIdx = 4

    def getTransactionObject(self, command : str, networkHandler):
        transactObj = None
        # TODO: Make this less bad after fixing inputParser badness
        tokens = self.inParser.lexer(command)
        if self.dummy:
            return self.getDummyTransactionObject(command, networkHandler)
        elif tokens[self.serviceIdx] == "HOUSEKEEPING" and tokens[self.subserviceIdx] in hkCommands:
            return getHKTransaction(command, networkHandler)
        elif tokens[self.serviceIdx] == "CLI":
            return satcliTransaction(command, networkHandler)
        elif tokens[self.serviceIdx] == "SCHEDULER" and (tokens[self.subserviceIdx] == "SET_SCHEDULE"):
            return schedulerTransaction(command, networkHandler)
        elif tokens[self.serviceIdx] == "TIME_MANAGEMENT" and tokens[self.subserviceIdx] == "SET_TIME":
            return setTimeTransaction(command, networkHandler)
        elif tokens[self.serviceIdx] == "IRIS" and (tokens[self.subserviceIdx] in ["IRIS_SET_TIME"]):
            return irisTransaction(command, networkHandler)
        elif tokens[self.serviceIdx] == "NS_PAYLOAD":
            return longTimeoutTransaction(command, networkHandler)
        elif (tokens[self.serviceIdx] == "GENERAL") and (tokens[self.subserviceIdx == "DEPLOY_DEPLOYABLES"]):
            return longTimeoutTransaction(command, networkHandler)
        elif tokens[self.serviceIdx] == "COMMUNICATION" and (tokens[self.subserviceIdx] in ["UHF_SET_RF_MODE"]):
            return setRFModeTransaction(command, networkHandler)
        else:
            return baseTransaction(command, networkHandler)

    def getDummyTransactionObject(self, command: str, networkHandler):
        transactObj = None
        tokens = self.inParser.lexer(command)
        if tokens[self.serviceIdx] == "HOUSEKEEPING" and tokens[self.subserviceIdx] in hkCommands:
            transactObj = dummyHKTransaction(command, networkHandler, self.fake_hk_id)
            self.fake_hk_id += 1
        elif tokens[self.serviceIdx] == "CLI":
            transactObj = dummySatCliTransaction(command, networkHandler)
        elif tokens[self.serviceIdx] == "SCHEDULER" and (tokens[self.subserviceIdx] in ['SET_SCHEDULE', 'DELETE_SCHEDULE']):
            transactObj = dummySchedulerTransaction(command, networkHandler)
        else:
            transactObj = dummyTransaction(command, networkHandler)
        return transactObj

class baseTransaction:
    def __init__(self, command, networkHandler):
        self.networkHandler = networkHandler
        self.inputParse = InputParser()
        self.returnParse = ReceiveParser()
        self.command = command
        self.pkt = self.inputParse.parseInput(self.command)
        self.dst = self.pkt["dst"]
        self.dport = self.pkt['dport']
        self.args = self.pkt['args']
        self.timeout = 10000

    def send(self):
        self.networkHandler.send(self.dst, self.dport, self.args)

    def receive(self):
        return self.networkHandler.receive(self.dst, self.dport, self.timeout)

    def parseReturnValue(self, data):
        return self.returnParse.parseReturnValue(self.dst, self.dport, data)

    def execute(self):
        self.send()
        ret = self.receive()
        return self.parseReturnValue(ret)

class dummyTransaction(baseTransaction):
    def execute(self):
        return {
            'dst': self.dst,
            'dport': self.dport,
            'args': self.args
        }

class longTimeoutTransaction(baseTransaction): 
    def __init__(self, command, networkHandler):
        super().__init__(command, networkHandler)
        self.timeout = 40000

class setTimeTransaction(baseTransaction):
    def execute(self):
        tokens = self.inputParse.lexer(self.command)
        time_param = tokens[-2]
        now = (int(time_param))
        if (now == 0):
            now = int(time.time())

        tokens[-2] = str(now)
        self.pkt = self.inputParse.parseInput("".join(tokens))
        self.args = self.pkt['args']
        self.send()
        return self.parseReturnValue(self.receive())

class schedulerTransaction(baseTransaction):
    def execute(self):
        tokens = self.inputParse.lexer(self.command)
        file_param = tokens[-2]
        with open(file_param, "r") as f:
            cmdList = f.readlines()
        packetEmbedder = EmbedPacket(cmdList, self.args)
        self.args = packetEmbedder.embedCSP()
        self.send()
        return self.parseReturnValue(self.receive())

class dummySchedulerTransaction(baseTransaction):
    def execute(self):
        tokens = self.inputParse.lexer(self.command)
        file_param = tokens[-2]
        with open(file_param, "r") as f:
            cmdList = f.readlines()
        packetEmbedder = EmbedPacket(cmdList, self.args)
        self.args = packetEmbedder.embedCSP()
        return {
            'err': 0,
            'dst': self.dst,
            'dport': self.dport,
            'args': self.args
        }

class getHKTransaction(baseTransaction):
    def execute(self):
        self.send()
        rxlist = []
        rxData = {}
        while True:
            try:
                ret = self.receive()
            except:
                return rxlist
            rxData = self.parseReturnValue(ret)
            rxlist.append(rxData)
            if ret[2] != 1:
                break
        return rxlist

class dummyHKTransaction(getHKTransaction):
    def __init__(self, command, networkHandler, fake_hk_id):
        super().__init__(command, networkHandler)
        self.fake_hk_id = fake_hk_id

    def execute(self):
        # TODO: Figure out how to fake multipacket transmission using args
        fake_hk = generateFakeHKDict()
        fake_hk['err'] = 0
        fake_hk['###############################\r\npacket meta\r\n###############################\r\nfinal'] = 0
        fake_hk['UNIXtimestamp'] = int(time.time())
        fake_hk['dataPosition'] = self.fake_hk_id
        return [fake_hk]

class satcliTransaction(baseTransaction):
    def execute(self):
        response = ""
        self.send()
        while True:
            ret = self.receive()
            returnVal = self.parseReturnValue(ret)
            response += f"""{returnVal['resp'].decode("ascii").rstrip()}\n"""
            if (returnVal['status']) == 0:
                break
        return response.strip()

class irisTransaction(baseTransaction):
    def execute(self):
        tokens = self.inputParse.lexer(self.command)

        if (tokens[4] == "IRIS_SET_TIME"): #tokens[4] refers to subservice
            time_param = tokens[-2]
            now = (int(time_param))
            if (now == 0):
                now = int(time.time())

            tokens[-2] = str(now)
            self.pkt = self.inputParse.parseInput("".join(tokens))
            self.args = self.pkt['args']
            self.send()

        return self.parseReturnValue(self.receive())

class setRFModeTransaction(baseTransaction):
    def __init__(self, command, networkHandler):
        super().__init__(command, networkHandler)
        self.gnuradio = GNURadioHandler.GNURadioHandler()

    def execute(self):
        self.send()
        print("Command does not give valid return upon success. Need to wait >20 seconds for Pipe mode to time out")
        time.sleep(21)#TODO make coupled with uTransceiver pipemode time in case of change 
        self.gnuradio.setUHF_RFMode(self.args[1])
        return "Pipe timeout complete"

class dummySatCliTransaction(satcliTransaction):
    def execute(self):
        return """Running as SatCli command \
            | dst: {} \
            | dport: {} \
            | args: {}""".format(
            self.dst, self.dport, self.args
        )
