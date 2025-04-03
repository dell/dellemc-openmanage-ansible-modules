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


GET_IDRAC_MEMORY_DETAILS_OEM_URI = "/redfish/v1/Systems/System.Embedded.1/Oem/Dell/DellMemory"
GET_IDRAC_MEMORY_DETAILS_URI = "/redfish/v1/Systems/System.Embedded.1/Memory"


class IDRACMemoryInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def get_memory_links(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_MEMORY_DETAILS_URI)
        memory_links_list = []
        if response.status_code == 200:
            members = response.json_data.get("Members")
            for each in members:
                memory_links_list.append(each.get("@odata.id"))
        return memory_links_list

    def get_memory_details(self, memory_link):
        response = self.idrac.invoke_request(method='GET', uri=memory_link)
        output = {
            "BankLabel": "",
            "CurrentOperatingSpeed": "",
            "DeviceDescription": "",
            "FQDD": "",
            "Key": "",
            "ManufactureDate": "",
            "Manufacturer": "",
            "MemoryType": "",
            "Model": "",
            "PartNumber": "",
            "PrimaryStatus": "",
            "Rank": "",
            "SerialNumber": "",
            "Size": "",
            "Speed": "",
            "memoryDeviceStateSettings": ""
        }
        if response.status_code == 200:
            output["BankLabel"] = response.json_data.get("Oem")\
                .get("Dell").get("DellMemory").get("BankLabel")
            output["CurrentOperatingSpeed"] = \
                response.json_data.get("OperatingSpeedMhz")
            if output["CurrentOperatingSpeed"] is not None:
                output["CurrentOperatingSpeed"] = \
                    str(response.json_data.get("OperatingSpeedMhz")) + " MHz"
            output["DeviceDescription"] = response.json_data.get("Description")
            output["FQDD"] = response.json_data.get("Id")
            output["Key"] = response.json_data.get("Id")
            output["ManufactureDate"] = response.json_data.get("Oem")\
                .get("Dell").get("DellMemory").get("ManufactureDate")
            output["Manufacturer"] = response.json_data.get("Manufacturer")
            output["MemoryType"] = response.json_data.get("MemoryDeviceType")
            output["Model"] = response.json_data.get("Oem")\
                .get("Dell").get("DellMemory").get("Model")
            output["PartNumber"] = response.json_data.get("PartNumber")
            output["PrimaryStatus"] = \
                response.json_data.get("Status").get("Health")
            output["Rank"] = response.json_data.get("RankCount")
            output["SerialNumber"] = response.json_data.get("SerialNumber")
            output["Size"] = response.json_data.get("CapacityMiB")
            if output["Size"] is not None:
                output["Size"] = \
                    str(response.json_data.get("CapacityMiB")) + " MiB"
            output["Speed"] = response.json_data.get("AllowedSpeedsMHz")
            if output["Speed"]:
                output["Speed"] = \
                    str(response.json_data.get("AllowedSpeedsMHz")[0]) + " MHz"
            output["memoryDeviceStateSettings"] = \
                response.json_data.get("Status").get("State")
        return output

    def get_memory_info(self):
        memory_output = []
        memory_links_list = self.get_memory_links()
        for each_link in memory_links_list:
            memory_output.append(self.get_memory_details(each_link))
        return memory_output
