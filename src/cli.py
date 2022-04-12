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
import unicodedata
from groundStation import groundStation

opts = groundStation.options()
gs = groundStation.groundStation(opts.getOptions())
flag = groundStation.GracefulExiter()

def cli():

    sysVals = groundStation.SystemValues()

    while True:
        if flag.exit():
            print('Exiting receiving loop\n')
            flag.reset()
            return
        try:
            server, port, toSend = gs.getInput(prompt='to send: ')
            data = bytearray(libcsp.packet_get_data(toSend))
            print("data in bytearray is : ", data)

            if (
                server == sysVals.APP_DICT.get('OBC') and 
                port == sysVals.SERVICES.get('SCHEDULER').get('port') and
                data[0] == sysVals.SERVICES.get('SCHEDULER').get('subservice').get('SET_SCHEDULE').get('subPort')
                ):

                print('entered SET_SCHEDULE\n')

                # open the scheduler text file as an array of strings
                with open('schedule.txt') as f:
                    cmdList = f.readlines()

                #create an empty list, and create another list of csp objects
                schedule = list()

                # for each line of command, parse the packet
                if len(cmdList) > 0:
                    for i in range(0, len(cmdList)):

                        # parse the time and command, then embed the command as a CSP packet
                        schedulerObj = groundStation.embedCSP(cmdList[i])
                        scheduler = schedulerObj.embedCSP()
                        
                        # append the list
                        schedule.append(scheduler)
                        scheduledTime = schedule[i]['time']
                        scheduledDst = schedule[i]['dst']
                        dst = (scheduledDst).to_bytes(1, byteorder='big')
                        scheduledDport = schedule[i]['dport']
                        dport = (scheduledDport).to_bytes(1, byteorder='big')
                        scheduleSubservice = schedule[i]['subservice']
                        packetContent = bytearray(libcsp.packet_get_data(scheduleSubservice))
                        packetLength = bytearray(libcsp.packet_get_length(scheduleSubservice))
                        data.extend(scheduledTime)
                        data.extend(dst)
                        data.extend(dport)
                        data.extend((len(packetContent)).to_bytes(2, byteorder='big'))
                        data.extend(packetContent)
                    #reply = libcsp.buffer_get(len(scheduledTime)+1)
                    libcsp.packet_set_data(toSend, data)
                    #libcsp.sendto_reply(toSend, reply, libcsp.CSP_O_NONE)
                    print("data is: ", data)
                    print("the server is: ", server)
                    print("the port is: ", port)
                    resp = gs.transaction(server, port, toSend)
            else:
                print("the server is: ", server)
                print("the port is: ", port)
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
