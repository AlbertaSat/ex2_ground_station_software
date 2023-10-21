'''
 * Copyright (C) 2023  University of Alberta
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
 * @file test_ftp.py
 * @author Ron Unrau
 * @date
'''

'''  to run > LD_LIBRARY_PATH=./libcsp/build PYTHONPATH=./libcsp/build:./:./src:./test python3 test/test_ftp.py -I sdr -d /dev/ttyUSB0 '''

import subprocess

from datetime import datetime
from datetime import timezone
from datetime import timedelta
import calendar

from src.options import optionsFactory
from src.options import Options
from src.ftp import ftpSender
from src.ftp import ftpGetter

def test_ftp_upload():
    opts = optionsFactory("ftp")
    options = "-p README.md -d /dev/ttyUSB0".split()
    ftpRunner = ftpSender(opts.getOptions(argv=options))
    ftpRunner.run()

def test_ftp_partial_upload():
    opts = optionsFactory("ftp")
    options = "-p README.md --skip 1024 -d /dev/ttyUSB0".split()
    ftpRunner = ftpSender(opts.getOptions(argv=options))
    ftpRunner.run()

def test_ftp_download():
    cmdout = subprocess.check_output(["rm", "-f", "readme.tst"])

    opts = optionsFactory("ftp")
    options = "-g README.md -o readme.tst -d /dev/ttyUSB0".split()
    ftpRunner = ftpGetter(opts.getOptions(argv=options))
    ftpRunner.run()

    cmdout = subprocess.check_output(["diff", "README.md", "readme.tst"])
    print(f"diff: {cmdout}")

if __name__ == '__main__':
    test_ftp_upload()
    test_ftp_partial_upload()
    test_ftp_download()
