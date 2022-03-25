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
import libcsp_py3 as libcsp
from groundStation import groundStation

opts = groundStation.options()
gs = groundStation.groundStation(opts.getOptions())
flag = groundStation.GracefulExiter()

def cli():
    #csp = groundStation(opts.getOptions())
    sysVals = groundStation.SystemValues()
    print("hello world\n")
    while True:
        if flag.exit():
            print('Exiting receiving loop\n')
            flag.reset()
            return
        try:
            server, port, toSend = gs.getInput(prompt='to send: ')
            data = bytearray(libcsp.packet_get_data(toSend))

            print('about to enter if loop\n')

            if (
                server == sysVals.APP_DICT.get('OBC') and 
                port == sysVals.SERVICES.get('SCHEDULER').get('port')
                #data[0] == sysVals.SERVICES.get('SCHEDULER').get('subservice').get('SET_SCHEDULE').get('subPort')
                #server == sysVals.APP_DICT['OBC'] and 
                #port == sysVals.SERVICES['SCHEDULER']
                #data[0] == 
                ):
                # open the scheduler text file as an array of strings
                with open('schedule.txt') as f:
                    cmdList = f.readlines()

                print(cmdList)

                #create an empty list, and create another list of csp objects
                schedule = list()

                print("empty list created\n")

                #cspObj = [embeddedCSP() for i in range(len(cmdList))]
                # for each line of command, parse the packet
                if len(cmdList) > 0:
                    for i in range(len(cmdList)):
                        # parse the time and command as strings
                        cmdStart = groundStation.parseScheduler.parseCmd(cmdList[i])
                        scheduledTime = cmdList[i][:cmdStart]
                        scheduledCmd = cmdList[i][cmdStart:]
                        # embed the parsed command as csp packet
                        embeddedPacket = groundStation.embedCSP.embedCSP(scheduledTime,scheduledCmd)
                        # append the list
                        schedule.append(embeddedPacket)
                # embed the csp packet in each cspObj
                gs.transaction(server, port, toSend)

            resp = gs.transaction(server, port, toSend)

            #checks if housekeeping multiple packets. if so, a list of dictionaries is returned
            if type(resp) == list:
                for rxData in resp:
                    print("--------------------------------------------------------------------------")
                    [print(key,':',value) for key, value in rxData.items()]
            #else, only a single dictionary is returned
            else:
                [print(key,':',value) for key, value in resp.items()]
            
        except Exception as e:
            print(e)

if __name__ == '__main__':
    flag = groundStation.GracefulExiter()
    cli()
