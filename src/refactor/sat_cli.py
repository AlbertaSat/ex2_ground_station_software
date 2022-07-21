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
 * @file sat_cli.py
 * @author Robert Taylor
 * @date 2022-09-21
'''

from click import option
from groundStation import groundStation
from options import optionsFactory

class sat_cli(groundStation):
    def run(self):
        while(1):
            inStr = self.inputHandler.getInput("$ ")
            commandStr = "{}.cli.send_cmd({},{})".format(self.satellite, len(inStr), inStr)
            try:
                transactObj = self.interactive.getTransactionObject(commandStr, self.networkManager)
            except Exception as e:
                print(e)
                continue
            print(transactObj.execute())


if __name__ == "__main__":
    opts = optionsFactory("basic")
    cliRunner =  sat_cli(opts.getOptions())
    cliRunner.run()