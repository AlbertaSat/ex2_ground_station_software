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
 * @file docGen.py
 * @author Andrew Rooney
 * @date 2020-11-20
'''

''' to run > python3 docGen.py  '''

from system import services

f = open("CommandDocs.txt", "w")

f.write('\t\t\t\t-- Ex-Alta 2 Ground Station Commands --\n' +
'Note: arguments and return types are given as numpy types\n\n\n')

for serv in services:
    subservice = services[serv]['subservice']
    supported = services[serv]['supports']
    for subName in subservice.keys():
        f.write(serv + '.' + subName + ':\n')

        sub = subservice[subName]
        subport = sub['subPort'] if 'subPort' in sub else None
        inoutInfo = sub['inoutInfo']

        args = 'None' if inoutInfo['args'] is None else repr(inoutInfo['args'])
        returns = 'None' if inoutInfo['returns'] is None else repr(inoutInfo['returns'])
        info = 'None' if not 'what' in sub else sub['what']
        f.write(
        '\t\tAbout: ' + info + '\n'
        '\t\tSupports:' + repr(supported) + '\n'
        '\t\tArguments: ' + args + '\n' +
        '\t\treturn values: ' + returns + '\n'
        '\t\tport: ' + str(services[serv]['port']) +
        '\t\tsubport: ' + str(subport) + '\n\n\n')
