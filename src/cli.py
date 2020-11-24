'''
 * Copyright (C) 2020  University of Alberta
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
 * @file test.py
 * @author Andrew Rooney
 * @date 2020-11-20
'''

'''  to run > sudo LD_LIBRARY_PATH=../libcsp/build PYTHONPATH=../libcsp/build python3 src/cli.py -I uart -d /dev/ttyUSB1  '''
import time
from groundStation.groundStation import *

opts = options()
csp = groundStation(opts.getOptions())
flag = GracefulExiter()

class GracefulExiter():
    '''
    Allows us to exit while loops with CTRL+C.
    (When we cannot get a connection for some reason.)
    By Esben Folger Thomas https://stackoverflow.com/a/57649638
    '''

    def __init__(self):
        self.state = False
        signal.signal(signal.SIGINT, self.flip_true)

    def flip_true(self, signum, frame):
        print('exit flag set to True (repeat to exit now)')
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.state = True

    def reset(self):
        self.state = False
        signal.signal(signal.SIGINT, self.flip_true)

    def exit(self):
        return self.state

def cli():
    while True:
        if flag.exit():
            print('Exiting receiving loop')
            flag.reset()
            return
        try:
            server, port, toSend = csp.getInput(prompt='to send: ')
            resp = csp.transaction(server, port, toSend)
            print(resp)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    flag = GracefulExiter()
    cli()
