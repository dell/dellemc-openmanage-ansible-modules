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

from urllib.error import HTTPError

GET_IDRAC_CPU_URI = "/redfish/v1/Systems/System.Embedded.1/Processors?$expand=*($levels=1)"

class IDRACCpuInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac
        
    def get_cpu_mapped_data(self, value={}):
        processor = value.get("Oem", {}).get("Dell", {}).get("DellProcessor", {})
        data = {
            "CPUFamily": processor.get("CPUFamily", ""),
            "Characteristics": "Not Available",
            "CurrentClockSpeed": str(int(processor.get("CurrentClockSpeedMhz", 0))/1000) + " GHz",
            "DeviceDescription": value.get("Name", ""),
            "ExecuteDisabledCapable": processor.get("ExecuteDisabledCapable", ""),
            "ExecuteDisabledEnabled": processor.get("ExecuteDisabledEnabled", ""),
            "FQDD": value.get("Id", ""),
            "HyperThreadingCapable": processor.get("HyperThreadingCapable", ""),
            "HyperThreadingEnabled": processor.get("HyperThreadingEnabled", ""),
            "Key": value.get("Socket", ""),
            "Manufacturer": value.get("Manufacturer", ""),
            "MaxClockSpeed": str(int(value.get("MaxSpeedMHz", 0))/1000) + " GHz",
            "Model": value.get("Model", ""),
            "NumberOfEnabledCores": value.get("TotalEnabledCores", ""),
            "NumberOfEnabledThreads": "Not Available",
            "NumberOfProcessorCores": "Not Available",
            "PrimaryStatus": value.get("Status", {}).get("Health", ""),
            "TurboModeCapable": processor.get("TurboModeCapable", ""),
            "TurboModeEnabled": processor.get("TurboModeEnabled", ""),
            "VirtualizationTechnologyCapable": processor.get("VirtualizationTechnologyCapable", ""),
            "VirtualizationTechnologyEnabled": processor.get("VirtualizationTechnologyEnabled", ""),
            "Voltage": processor.get("Volts", ""),
            "processorDeviceStateSettings": "Not Available"
        }
        return data

    def get_cpu_system_info(self):
        output = []
        resp = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_CPU_URI)
        for each_member in resp.json_data.get("Members", []):
            output.append(self.get_cpu_mapped_data(each_member))
        return output
