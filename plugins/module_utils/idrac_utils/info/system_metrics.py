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

GET_SYSTEMBOARD_POWERCONSUMPTION_DETAILS_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/Sensors/SystemBoardPwrConsumption"
GET_SYSTEMBOARDINLETTEMP_DETAILS_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/Sensors/SystemBoardInletTemp"
GET_POWERHEADROOM_DETAILS_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/Sensors/PowerHeadroom"
NA = "Not Available"


class IDRACSystemMetricsInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def get_energy_consumption_details(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_SYSTEMBOARD_POWERCONSUMPTION_DETAILS_URI_10)
        if response.status_code == 200:
            return response.json_data.get("LifetimeReading", NA)
        return {}

    def get_temperature_details(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_SYSTEMBOARDINLETTEMP_DETAILS_URI_10)
        if response.status_code == 200:
            inlettemp_critical = response.json_data.get("Oem", {}).get("Dell", {}).get("DurationInCriticalThresholdPercent", NA)
            inlettemp_warn = response.json_data.get("Oem", {}).get("Dell", {}).get("DurationInWarningThresholdPercent", NA)
            return inlettemp_critical, inlettemp_warn
        return {}, {}

    def get_power_consumption_details(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_POWERHEADROOM_DETAILS_URI_10)
        if response.status_code == 200:
            return response.json_data.get("LowestReading", NA)
        return {}

    def get_system_metrics_info(self):
        output = []
        energy_consump = self.get_energy_consumption_details()
        inlettemp_critical, inlettemp_warn = self.get_temperature_details()
        power_consumption = self.get_power_consumption_details()

        output = [{
            "EnergyConsumption": energy_consump,
            "InletTempCriticalPerc": inlettemp_critical,
            "InletTempWarnPerc": inlettemp_warn,
            "Key": "SystemMetrics",
            "PowerConsumption": power_consumption,
            "SystemMetrics": "Not Available"
        }]

        return output
