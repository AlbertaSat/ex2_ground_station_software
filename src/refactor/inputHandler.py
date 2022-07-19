



class inputHandler():
    def __init__(self):
        self.historyFile = open("command_history.txt", "a")
    def getInput(self, prompt):
        inStr = input(prompt)
        self.historyFile.write(inStr + '\n')
        return inStr
