from groundStation import groundStation
from options import optionsFactory

class cli(groundStation):
    def run(self):
        while(1):
            inStr = self.inputHandler.getInput("to send: ")
            transactObj = self.interactive.getTransactionObject(inStr, self.networkManager)
            print(transactObj.execute())

if __name__ == "__main__":
    opts = optionsFactory("basic")
    cliRunner = cli(opts.getOptions())
    cliRunner.run()