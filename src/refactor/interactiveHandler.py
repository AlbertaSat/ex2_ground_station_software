
from system import services
from inputParser import inputParser
from receiveParser import receiveParser
from embedCSP import embedPacket

class interactiveHandler:
    def __init__(self):
        self.services = services
        self.inParser = inputParser()

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
        else:
            transactObj = baseTransaction(command, networkHandler)

        return transactObj
    
class baseTransaction:
    def __init__(self, command, networkHandler):
        self.networkHandler = networkHandler
        self.inputParse = inputParser()
        self.returnParse = receiveParser()
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
        return self.returnParse.parseReturnValue(self.dport, data, len(data))

    def execute(self):
        self.send()
        ret = self.receive()
        return self.parseReturnValue(ret)


class schedulerTransaction(baseTransaction):
    def execute(self):
        tokens = self.inputParse.lexer(self.command)
        file_param = tokens[-2]
        f = open(file_param, "r")
        cmdList = f.readlines()
        packetEmbedder = embedPacket(cmdList, self.args)
        self.args = packetEmbedder.embedCSP()
        self.send()
        return self.parseReturnValue(self.receive())

class getHKTransaction(baseTransaction):
    def execute(self):
        print("WARN: I have no idea how HK receive works, it may not at all")
        self.send()
        rxDataList = []
        while True:
            ret = self.receive()
            rxDataList.append(self.parseReturnValue(ret))
            if ret[2] != 1:
                break
        return rxDataList

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