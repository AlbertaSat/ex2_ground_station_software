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
 * @file cli.py
 * @author Robert Taylor
 * @date 2022-07-21
'''

from groundStation import GroundStation
from options import optionsFactory
import pprint

class cli(GroundStation):
    def run(self):
        pp = pprint.PrettyPrinter()
        while(1):
            inStr = self.inputHandler.getInput("to send: ")
            try:
                transactObj = self.interactive.getTransactionObject(inStr, self.networkManager)
                ret = transactObj.execute()
                print()
                # Housekeeping data can be a list of dicts
                if isinstance(ret, list):
                    for entry in ret:
                        for key, value in entry.items():
                            print("{} : {}".format(key, value))
                else:
                    for key, value in ret.items():
                        print("{} : {}".format(key, value))
                print()
            except Exception as e:
                print(e)
                continue

if __name__ == "__main__":
    opts = optionsFactory("basic")
    cliRunner = cli(opts.getOptions())
    cliRunner.run()
