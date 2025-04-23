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
NA = "Not Available"


class IDRACFanInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def map_fan_data(self, fan):
        health = fan.get("Status", {}).get("Health", NA)
        fan_pwm = fan.get("Oem", {}).get("Dell", {}).get("FanPWM", 0)
        current_reading = fan.get("SpeedPercent", {}).get("SpeedRPM", NA)
        output = {
            "ActiveCooling": fan.get("HotPluggable", NA),
            "CurrentReading": current_reading,
            "DeviceDescription": fan.get("Name", NA),
            "FQDD": fan.get("Id", NA),
            "Key": fan.get("Id", NA),
            "Location": fan.get("Location", NA),
            "PWM": fan_pwm,
            "PrimaryStatus": "Healthy" if health == "OK" else health,
            "State": fan.get("State", NA),
            "VariableSpeed": "true" if fan_pwm > 0 else "false"
        }
        return output

    def get_fan_info(self):
        """Fetches fan data from iDRAC and maps it."""
        output = []
        resp = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_FAN_DETAILS_URI_10)

        if resp.status_code == 200:
            fan_members = resp.json_data.get("Members", [])
            for fan in fan_members:
                output.append(self.map_fan_data(fan))
        return output
