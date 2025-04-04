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

GET_IDRAC_FAN_DETAILS_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/ThermalSubsystem/Fans?$expand=*($levels=1)"


class IDRACFanInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def map_fan_data(self, fan):
        """Maps fan fields from the API response to a structured format."""
        keys_to_search = {
            "ActiveCooling": "HotPluggable",
            # "BaseUnits": "SpeedPercent.SpeedRPM",
            "CurrentReading": "SpeedPercent.SpeedRPM",
            "DeviceDescription": "Name",
            "FQDD": "Id",
            "Key": "Id",
            # "Location": "Location",
            "PWM": "Oem.Dell.FanPWM",
            "PrimaryStatus": "Status.Health",
            # "RateUnits": "RateUnits",
            "State": "State",
            # "VariableSpeed": "VariableSpeed"
        }

        fan_data = {}

        for key, response_key in keys_to_search.items():
            keys = response_key.split(".")
            value = fan
            for k in keys:
                value = value.get(k, "Not Available") if isinstance(value, dict) else "Not Available"

            fan_data[key] = value

        return fan_data

    def get_fan_info(self):
        """Fetches fan data from iDRAC and maps it."""
        output = []
        resp = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_FAN_DETAILS_URI_10)

        if resp.status_code == 200:
            fan_members = resp.json_data.get("Members", [])
            for fan in fan_members:
                output.append(self.map_fan_data(fan))
        return output
