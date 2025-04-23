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


GET_IDRAC_SENSOR_FAN_DETAILS_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/Oem/Dell/DellEnclosureFanSensors"
NA = "Not Available"


class IDRACSensorsFanInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def sensors_fan_mapped_data(self, resp):
        response = self.idrac.invoke_request(method='GET', uri=resp)
        if response.status_code == 200:
            output = {
                "CurrentReading": NA,
                "CurrentState": NA,
                "DeviceID": NA,
                "FQDD": NA,
                "HealthState": NA,
                "Key": NA,
                "Location": NA,
                "Name": NA,
                "OtherSensorTypeDescription": NA,
                "PrimaryStatus": NA,
                "SensorType": NA,
                "State": NA,
                "SubType": NA,
                "Type": NA,
                "coolingUnitIndexReference": NA
            }
            return output

    def get_sensors_fan_info(self):
        output = []
        resp = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_SENSOR_FAN_DETAILS_URI_10)
        if resp.status_code == 200:
            for each_member in resp.json_data.get("Members", []):
                output.append(self.sensors_fan_mapped_data(each_member))
        return output
