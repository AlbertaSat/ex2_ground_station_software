from click import option
from groundStation import groundStation
from options import optionsFactory

class sat_cli(groundStation):
    def run(self):
        while(1):
            inStr = self.inputHandler.getInput("$ ")
            commandStr = "{}.cli.send_cmd({},{})".format(self.satellite, len(inStr), inStr)
            transactObj = self.interactive.getTransactionObject(commandStr, self.networkManager)
            print(transactObj.execute())


if __name__ == "__main__":
    opts = optionsFactory("basic")
    cliRunner =  sat_cli(opts.getOptions())
    cliRunner.run()