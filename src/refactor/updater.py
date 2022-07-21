from groundStation import groundStation
from options import optionsFactory

class updater(groundStation):
    def __init__(self, opts):
        raise NotImplementedError("Updater not avaialble yet")
    def run(self):
        raise NotImplementedError("Updater not avaialble yet")

if __name__ == "__main__":
    opts = optionsFactory("updater")
    updaterRunner =  updater(opts.getOptions())
    updaterRunner.run()