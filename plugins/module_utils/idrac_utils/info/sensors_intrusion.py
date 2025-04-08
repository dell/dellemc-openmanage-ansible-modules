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

GET_IDRAC_SENSOR_INTRUSION_DETAILS_URI_10 = "/redfish/v1/Chassis/System.Embedded.1?$select=PhysicalSecurity/IntrusionSensor"
GET_IDRAC_SYSTEM_DETAILS_URI_10 = "/redfish/v1/Systems/System.Embedded.1"
NA = "Not Available"


class IDRACSensorsIntrusionInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def get_state(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_SYSTEM_DETAILS_URI_10)
        if response.status_code == 200:
            state = response.json_data.get("Status", {}).get("State", "")
            return state
        return ""

    def sensors_intrusion_mapped_data(self, resp):
        state = self.get_state()
        health_state = resp.get("PhysicalSecurity", {}).get("IntrusionSensor", "Not Available")
        output = {
            "CurrentReading": resp.get("CurrentReading", NA),
            "CurrentState": "No Breach",  # remove
            "DeviceID": "iDRAC.Embedded.1#SystemBoardIntrusion",
            "HealthState": health_state,
            "Key": "System Board Intrusion",
            "Location": "System Board Intrusion",
            "OtherSensorTypeDescription": "Not Available",
            "PrimaryStatus": "Healthy" if health_state == "Normal" else health_state,
            "SensorType": "Intrusion",
            "State": NA if (state == "") else state,
            "Type": "Not Available"
        }
        return output

    def get_sensors_intrusion_info(self):
        output = []
        resp = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_SENSOR_INTRUSION_DETAILS_URI_10)
        if resp.status_code == 200:
            output.append(self.sensors_intrusion_mapped_data(resp.json_data))
        return output
