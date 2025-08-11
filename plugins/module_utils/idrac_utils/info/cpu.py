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


GET_IDRAC_CPU_URI = "/redfish/v1/Systems/System.Embedded.1/Processors?$expand=*($levels=1)"
NA = "Not Available"


class IDRACCpuInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def get_cpu_mapped_data(self, member):
        processor = member.get("Oem", {}).get("Dell", {}).get("DellProcessor", {})
        ccs = str(int(processor.get("CurrentClockSpeedMhz", 0)) / 1000) + " GHz"
        mcs = str(int(member.get("MaxSpeedMHz", 0)) / 1000) + " GHz"
        chars = "64-bit Capable" if str(member.get("InstructionSet", "")).lower() == "x86-64" else "Unknown"
        data = {
            "CPUFamily": processor.get("CPUFamily", NA),
            "Characteristics": chars,
            "CurrentClockSpeed": ccs,
            "DeviceDescription": member.get("Name", NA),
            "ExecuteDisabledCapable": processor.get("ExecuteDisabledCapable", NA),
            "ExecuteDisabledEnabled": processor.get("ExecuteDisabledEnabled", NA),
            "FQDD": member.get("Id", NA),
            "HyperThreadingCapable": processor.get("HyperThreadingCapable", NA),
            "HyperThreadingEnabled": processor.get("HyperThreadingEnabled", NA),
            "Key": member.get("Socket", NA),
            "Manufacturer": member.get("Manufacturer", NA),
            "MaxClockSpeed": mcs,
            "Model": member.get("Model", NA),
            "NumberOfEnabledCores": str(member.get("TotalEnabledCores", NA)),
            "NumberOfEnabledThreads": str(member.get("TotalThreads", NA)),
            "NumberOfProcessorCores": str(member.get("TotalCores", NA)),
            "PrimaryStatus": member.get("Status", {}).get("Health", NA),
            "TurboModeCapable": processor.get("TurboModeCapable", NA),
            "TurboModeEnabled": processor.get("TurboModeEnabled", NA),
            "VirtualizationTechnologyCapable": processor.get("VirtualizationTechnologyCapable", NA),
            "VirtualizationTechnologyEnabled": processor.get("VirtualizationTechnologyEnabled", NA),
            "Voltage": processor.get("Volts", NA),
            "processorDeviceStateSettings": NA
        }
        return data

    def get_cpu_system_info(self):
        output = []
        resp = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_CPU_URI)
        for each_member in resp.json_data.get("Members", []):
            output.append(self.get_cpu_mapped_data(each_member))
        return output
