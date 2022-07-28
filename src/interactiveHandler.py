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
from inputParser import InputParser
from receiveParser import ReceiveParser
from embedCSP import EmbedPacket
import time

class InteractiveHandler:
    def __init__(self):
        self.services = services
        self.inParser = InputParser()

        # TODO: This is bad, make it good when fixing inputParser
        self.appIdx = 0
        self.serviceIdx = 2
        self.subserviceIdx = 4

    def getTransactionObject(self, command : str, networkHandler):
        transactObj = None
        # TODO: Make this less bad after fixing inputParser badness
        tokens = self.inParser.lexer(command)
        if tokens[self.serviceIdx] == "HOUSEKEEPING" and tokens[self.subserviceIdx] == "GET_HK":
            transactObj = getHKTransaction(command, networkHandler)
        elif tokens[self.serviceIdx] == "CLI":
            transactObj = satcliTransaction(command, networkHandler)
        elif tokens[self.serviceIdx] == "SCHEDULER" and (tokens[self.subserviceIdx] in ['SET_SCHEDULE', 'DELETE_SCHEDULE', 'REPLACE_SCHEDULE']):
            transactObj = schedulerTransaction(command, networkHandler)
        elif tokens[self.serviceIdx] == "TIME_MANAGEMENT" and tokens[self.subserviceIdx] == "SET_TIME":
            transactObj = setTimeTransaction(command, networkHandler)
        else:
            transactObj = baseTransaction(command, networkHandler)

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

    def send(self):
        self.networkHandler.send(self.dst, self.dport, self.args)

    def receive(self):
        return self.networkHandler.receive(self.dst, self.dport, 10000)
        
    def parseReturnValue(self, data):
        return self.returnParse.parseReturnValue(self.dport, data)

    def execute(self):
        self.send()
        ret = self.receive()
        return self.parseReturnValue(ret)

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
        f = open(file_param, "r")
        cmdList = f.readlines()
        packetEmbedder = EmbedPacket(cmdList, self.args)
        self.args = packetEmbedder.embedCSP()
        self.send()
        return self.parseReturnValue(self.receive())

class getHKTransaction(baseTransaction):
    def execute(self):
        print("WARN: I have no idea how HK receive works, it may not at all")
        self.send()
        rxData = dict()
        while True:
            ret = self.receive()
            rxData = {**rxData, **self.parseReturnValue(ret)}
            if ret[2] != 1:
                break
        return rxData

class satcliTransaction(baseTransaction):
    def execute(self):
        response = ""
        self.send()
        while True:
            ret = self.receive()
            returnVal = self.parseReturnValue(ret)
            response += "{}\n".format(returnVal['resp'].decode("ascii").rstrip())
            if (returnVal['status']) == 0:
                break
        return response.strip()

class dummyTransaction(baseTransaction):
    def execute(self):
        raise NotImplementedError("dummy transactions not implemented")