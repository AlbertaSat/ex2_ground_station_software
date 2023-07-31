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
 * @date 2022-07-21
'''

from groundStation import GroundStation
from options import optionsFactory

class Listener(GroundStation):
    def run(self):
        while(1):
            try:
                ret = self.networkManager.receive(1, 2, 10000)
                print(self.networkManager.parseReturnValue(ret))
            except Exception as e:
                print(e)
                continue


if __name__ == "__main__":
    opts = optionsFactory("basic")
    listener = Listener(opts.getOptions())
    listener.run()
