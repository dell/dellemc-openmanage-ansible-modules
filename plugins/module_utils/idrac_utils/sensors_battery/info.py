# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 9.12.0
# Copyright (C) 2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:

#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.

#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


GET_IDRAC_SENSOR_BATTERY_DETAILS_URI_10 = "/redfish/v1/Systems/System.Embedded.1/Oem/Dell/DellSensors/iDRAC.Embedded.1_0x23_SystemBoardCMOSBattery"


class IDRACSensorsBatteryInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def sensors_battery_mapped_data(self, resp):
        output = {
            "CurrentReading": resp.get("CurrentReading", "Not Available"),
            "CurrentState": resp.get("CurrentState", "Not Available"),
            "DeviceID": "iDRAC.Embedded.1#SystemBoardCMOSBattery",
            "HealthState": resp.get("HealthState", "Not Available"),
            "Key": "System Board CMOS Battery",
            "Location": "System Board CMOS Battery",
            "OtherSensorTypeDescription": "Battery",
            # "PrimaryStatus": resp.get("HealthState", "Not Available"),
            "SensorType": "Battery",
            "State": resp.get("EnabledState", "Not Available")
        }
        return output

    def get_sensors_battery_info(self):
        output = []
        resp = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_SENSOR_BATTERY_DETAILS_URI_10)
        if resp.status_code == 200:
            output.append(self.sensors_battery_mapped_data(resp.json_data))
        return output
