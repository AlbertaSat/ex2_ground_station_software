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
 * @file options.py
 * @author Robert Taylor
 * @date 2022-09-21
'''

import argparse
import sys

def optionsFactory(kind : str):
    if (kind == "basic"):
        return Options()
    elif (kind == "updater"):
        return UpdateOptions()
    elif (kind == "ftp"):
        return FTPOptions()
    else:
        raise NotImplementedError("Options class type {} not implemented".format(type))

class Options(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Parses command.')

    def getOptions(self):
        self.parser.add_argument(
            '--hkeyfile',
            type=str,
            default="test_key.dat",
            help='Key to use for CSP HMAC')
        self.parser.add_argument(
            '-I',
            '--interface',
            type=str,
            default='uart',
            help='CSP interface to use')

        self.parser.add_argument(
            '-d',
            '--device',
            type=str,
            default='/dev/ttyUSB0',
            help='External device file')

        self.parser.add_argument(
            '-t',
            '--timeout',
            type=int,
            default='15000', # 15 seconds
            help='RDP connection timeout')
        
        self.parser.add_argument(
            '-u', 
            action='store_true',
            help='Enable UHF SDR functionality (e.g automatic pipe mode commands)')

        self.parser.add_argument(
            '-s',
            '--satellite',
            type=str,
            default="EX2",
            help='Satellite parameter for automatic programs (e.g FTP)')
        return self.parser.parse_args(sys.argv[1:])

class UpdateOptions(Options):
    def __init__(self):
        super().__init__();

    def getOptions(self):
        self.parser.add_argument(
            '-f',
            '--file',
            type=str,
            help='Binary to upload')
        self.parser.add_argument(
            '-b',
            '--blocksize',
            type=int,
            default='512',
            help='Number of bytes to send at a time')
        self.parser.add_argument(
            '-a',
            '--address',
            type=lambda x: int(x,0),
            default='0x00200000',
            help='address to flash update on OBC')
        self.parser.add_argument(
            '-r',
            '--resume',
            action='store_true',
            help="Attempt to resume update if possible"
        )
        self.parser.add_argument(
            '-c',
            '--crc',
            type=lambda x: int(x,0),
            default=None,
            help="Provide file CRC. Can be hex or decimal"
        )

        return super().getOptions();


class FTPOptions(Options):
    def __init__(self):
        super().__init__();

    def getOptions(self):
        self.parser.add_argument(
            '-g',
            '--get',
            type=str,
            default='',
            help='File to download from satellite')
        self.parser.add_argument(
            '-p',
            '--post',
            type=str,
            default='',
            help='File to upload to satellite')
        self.parser.add_argument(
            '-o',
            '--outfile',
            type=str,
            default='',
            help='Filename to save on target (satellite or ground). Defaults is get or post filename')
        self.parser.add_argument(
            '-b',
            '--burst-size',
            type=int,
            default='100',
            help='Number of packets to receive in a single burst download')
        self.parser.add_argument(
            '--sband',
            action='store_true',
            help="Download over sband instead of UHF"
        )
        return super().getOptions();