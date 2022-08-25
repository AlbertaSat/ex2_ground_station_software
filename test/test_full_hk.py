'''
 * Copyright (C) 2021  University of Alberta
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
 * @file test_full_hk.py
 * @author Jenish Patel
 * @date 2022-08-08
'''

import sys
from os import path

from groundstation_tester import Tester

from adcs.expected_adcs_hk import expected_ADCS_HK
from charon.expected_charon_hk import expected_charon_HK
from dfgm.expected_dfgm_hk import expected_DFGM_HK
from eps.expected_eps_hk import expected_EPS_HK
from iris.expected_iris_hk import expected_iris_HK
from nim.expected_nim_hk import expected_NIM_HK
from obc.expected_obc_hk import expected_OBC_HK
from sband.expected_sband_hk import expected_sBand_HK
from solar.expected_solarPanel_hk import expected_solarPanel_HK
from uhf.expected_uhf_hk import expected_UHF_HK
from yukon.expected_yukon_hk import expected_yukon_HK

# TODO - Add in remaining HK variables and their expected values to the following dictionaries:
#        expected_EPS_HK, expected_OBC_HK, expected_charon_HK, expected_sBand_HK, expected_DFGM_HK
#        expected_NIM_HK, expected_yukon_HK, expected_adcs_HK
# NOTE - The HK variables to be added in don't exist yet at the time of last edit

# Checks all HK data by default
def testSystemWideHK(EPS=1, OBC=1, UHF=1, solar=1, charon=1, sBand=1, iris=1, DFGM=1, NIM=1, yukon=1, ADCS=1):
    hk_tester = Tester()
    testPassed = 'Pass'

    inStr = "ex2.housekeeping.get_hk(1, 0 ,0)"
    try:
        transactObj = hk_tester.interactive.getTransactionObject(inStr, hk_tester.networkManager)
        ret = transactObj.execute()
        
        print()
        [print(key,':',value) for key, value in ret.items()]
        print()

        if (EPS):
            checkPassed = hk_tester.checkModuleHK(ret, expected_EPS_HK)
            if not checkPassed:
                testPassed = 'Fail'

        if (OBC):
            checkPassed = hk_tester.checkModuleHK(ret, expected_OBC_HK)
            if not checkPassed:
                testPassed = 'Fail'

        if (UHF):
            checkPassed = hk_tester.checkModuleHK(ret, expected_UHF_HK)
            if not checkPassed:
                testPassed = 'Fail'

        if (solar):
            # if NIM + yukon > 0, certain HK values will be ignored in the test since the AuroraSat and YukonSat payloads don't require them
            ignore_list = ['Port_Temp3', 'Port_Dep_Temp3', 'Star_Temp3', 'Star_Dep_Temp3',
                  'Zenith_Temp3', 'Port_Pd3', 'Port_Dep_Pd3', 'Star_Pd3', 'Star_Dep_Pd3', 'Zenith_Pd3']
            checkPassed = hk_tester.checkModuleHK(ret, expected_solarPanel_HK, ignore_list)
            if not checkPassed:
                testPassed = 'Fail'

        if (charon):
            # if NIM + yukon > 0, certain HK values will be ignored in the test since the AuroraSat and YukonSat payloads don't require them
            ignore_list = []
            checkPassed = hk_tester.checkModuleHK(ret, expected_charon_hk, ignore_list)
            if not checkPassed:
                testPassed = 'Fail'

        if (sBand):
            checkPassed = hk_tester.checkModuleHK(ret, expected_sBand_HK)
            if not checkPassed:
                testPassed = 'Fail'

        if (iris):
            checkPassed = hk_tester.checkModuleHK(ret, expected_iris_HK)
            if not checkPassed:
                testPassed = 'Fail'

        if (DFGM):
            checkPassed = hk_tester.checkModuleHK(ret, expected_DFGM_HK)
            if not checkPassed:
                testPassed = 'Fail'

        if (NIM):
            checkPassed = hk_tester.checkModuleHK(ret, expected_NIM_HK)
            if not checkPassed:
                testPassed = 'Fail'

        if (yukon):
            checkPassed = hk_tester.checkModuleHK(ret, expected_yukon_HK)
            if not checkPassed:
                testPassed = 'Fail'

        if (ADCS):
            checkPassed = hk_tester.checkModuleHK(ret, expected_ADCS_HK)
            if not checkPassed:
                testPassed = 'Fail'

        # Take note of the test's result
        if (testPassed == 'Pass'):
            colour = '\033[92m'  # green
        else:
            colour = '\033[91m'  # red

        print(colour + ' - HOUSEKEEPING TEST ' +
              testPassed + '\n\n' + '\033[0m')

    except Exception as e:
        print(e)
        pass
        