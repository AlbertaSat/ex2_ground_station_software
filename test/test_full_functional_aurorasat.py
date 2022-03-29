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
 * @file test_full_functional_aurorasat.py
 * @author Daniel Sacro
 * @date 2022-03-28
'''

from functionalTestLib import functionalTestLib as fTest

fTest = fTest() # Call to initialize local functional test class

def runTests():
    fTest.testSystemWide_HK()
    fTest.testSystemWideDeployment() # Cannot be automated
    fTest.run_ADCS_healthCheck() # Partially cannot be automated
    fTest.testClockSynchronization()
    fTest.testCharonPowerChannelForcedResets()
    fTest.checkDeployablesSwitchStatus()
    fTest.testSBandFullDataRateOverRadio()
    fTest.test_UHF_Tx_Rx_overRadio()
    fTest.check_DFGM_dataOutput()
    fTest.test_EPS_powerChannelResets()
    fTest.test_EPS_andSolarPanelCharging() # Cannot be automated
    fTest.test_EPS_deploymentTimer() # Cannot be automated
    fTest.test_OBC_RTC_backupPowerCircuit()
    fTest.test_OBC_solarPanelCurrentMeasurementAndSwitch()
    
    

    fTest.runAuroraSatPayloadTest()

    fTest.getSummary()


if __name__ == '__main__':
    runTests()