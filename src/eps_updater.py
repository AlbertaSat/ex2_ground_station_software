from groundStation import GroundStation
from inputParser import InputParser
from receiveParser import ReceiveParser
from options import optionsFactory
import os
import time

class EPSUpdater(GroundStation):

    def __init__(self, opts):
        super(EPSUpdater, self).__init__(opts)
        self.inFileName = opts.file
        self.inFileSize = os.path.getsize(self.inFileName)
        self.inFile = open(self.inFileName, "rb")
        self.fileNo = 0
        self.cell_size = 0
        self.cell_qty = 0
        
    def configureUpdate(self):
        inf = self.getFileInfo(self.fileNo)
        print(inf)
        sectorSize = inf['sector_sz']
        entrySize = (sectorSize - (6*4)) // 4
        print("Entry size: {}".format(entrySize))
        self.cell_size = entrySize
        self.cell_qty = self.inFileSize // self.cell_size
        print(self.cell_qty)

        if (self.cell_size % self.inFileSize >= 1):
            self.cell_qty += 1
        print(self.cell_qty)

        self.cell_qty = int(self.cell_qty)

    def run(self):
        self.doUpdate()

    def getFileInfo(self, filenum):
        return self.interactive.getTransactionObject("EPS.EPS_FILE.FILE_INFO({})".format(filenum), self.networkManager).execute()
    
    def formatFile(self, filenum):
        print(filenum)
        print(self.interactive.getTransactionObject("EPS.EPS_FILE.FILE_FORMAT({},0,{},{})".format(filenum, self.cell_qty, self.cell_size), self.networkManager).execute())


    def checkFormatFinished(self, filenum):
        while True:
            try:
                inf = self.getFileInfo(filenum)
            except:
                continue
            if inf['file_status'] == 0:
                print(inf)
                return True
    
    def sendFile(self, filenum):
        inParse = InputParser()
        receiveParse = ReceiveParser()
        first_entry_id = 0
        offset = 0
        print(self.cell_qty)
        while first_entry_id < self.cell_qty:
            data = self.inFile.read(self.cell_size)
            dataLen = len(data)
            commandStr = "eps.eps_file.data_upload_packet({},{},{},{})".format(filenum, first_entry_id, offset, dataLen)
            toSend = inParse.parseInput(commandStr)
            toSend['args'].extend(data)
            self.networkManager.send(toSend['dst'], toSend['dport'], toSend['args'])
            #ret = self.networkManager.receive(toSend['dst'], toSend['dport'], 10000)
            print("sent")
            first_entry_id += 1
            time.sleep(0.2)
            
        

    def doUpdate(self):
        self.configureUpdate()
        #self.getFileInfo(self.fileNo)
        #self.formatFile(self.fileNo)
        #self.checkFormatFinished(0)
        self.sendFile(self.fileNo)
        #self.getFileInfo(self.fileNo)

if __name__ == "__main__":
    opts = optionsFactory("EPSUpdater")
    cliRunner = EPSUpdater(opts.getOptions())
    cliRunner.run()