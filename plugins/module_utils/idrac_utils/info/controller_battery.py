# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 10.0.0
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

GET_IDRAC_CONTROLLER_BATTERY_DETAILS_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/PowerSubsystem/Oem/Dell/DellControllerBattery"
NA = "Not Available"


class IDRACControllerBatteryInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def map_controller_battery_data(self, battery):
        health_state_map = {
            "CriticalFailure": "Critical",
            "Degraded/Warning": "Warning",
            "MajorFailure": "Critical",
            "MinorFailure": "Critical",
            "NonRecoverableError": "Critical",
            "OK": "Healthy",
            "Unknown": "Unknown"
        }

        health_state = battery.get("PrimaryStatus", NA)
        primary_status = health_state_map.get(health_state, NA)
        output = {
            "DeviceDescription": battery.get("Name", NA),
            "FQDD": battery.get("FQDD", NA),
            "InstanceID": battery.get("Id", NA),
            "Key": battery.get("Id", NA),
            "PrimaryStatus": primary_status,
            "RAIDState": battery.get("RAIDState", NA),
        }
        return output

    def get_controller_battery_info(self):
        """Fetches controller battery data from iDRAC and maps it."""
        output = []
        resp = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_CONTROLLER_BATTERY_DETAILS_URI_10)

        if resp.status_code == 200:
            battery_members = resp.json_data.get("Members", [])
            for member in battery_members:
                output.append(self.map_controller_battery_data(member))
        return output
