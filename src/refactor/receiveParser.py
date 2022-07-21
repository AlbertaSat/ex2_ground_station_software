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
 * @file receiveParser.py
 * @author Robert Taylor
 * @date 2022-09-21
'''

import numpy as np
from system import services, SatelliteNodes

class receiveParser:
    def __init__(self):
        self.services = services

    def parseReturnValue(self, dport, data):
        # TODO: Refactor this
        length = len(data)
        service = [
            x for x in self.services if self.services[x]['port'] == dport][0]

        idx = 0
        outputObj = {}
        subservice = {}

        if service and (
                'subservice' in self.services[service]) and length > 0:
            subservice = [self.services[service]['subservice'][x] for x in self.services[service]
                          ['subservice'] if self.services[service]['subservice'][x]['subPort'] == data[idx]][0]
            idx += 1

        if 'inoutInfo' not in subservice:
            # error: check system SystemValues
            return None
        
        returns = subservice['inoutInfo']['returns']
        args = subservice['inoutInfo']['args']
        for retVal in returns:
            if returns[retVal] == 'var':
                #Variable size config return
                outputObj[retVal] = np.frombuffer( data, dtype = "b", count=-1, offset=idx)
                return outputObj
            else:
                try:
                    outputObj[retVal] = np.frombuffer(
                        data, dtype=returns[retVal], count=1, offset=idx)[0]
                except:
                    outputObj[retVal] = None
                idx += np.dtype(returns[retVal]).itemsize
        return outputObj

if __name__ == '__main__':
    parser = receiveParser()
    returnval = parser.parseReturnValue(8, bytearray(b'\x01\x00')) # ba[0] = 01 (set time)
    print(returnval)

    returnval = parser.parseReturnValue(8, bytearray(b'\x00\x00@\xaa\xe1H@\x06ffA\x90\x14{')) # ba[0] = 00 (set time)
    print(returnval)

    returnval = parser.parseReturnValue(10, bytearray(b'\x01\x00D|\x86w'))
    print(returnval)
