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


GET_IDRAC_MEMORY_DETAILS_URI = "/redfish/v1/Systems/System.Embedded.1/Memory"
NA = "Not Available"
MAPPING_DICT_FOR_RANK = {
    0: "Unknown",
    1: "Single Rank",
    2: "Double Rank",
    4: "Quad Rank"
}
MAPPING_MEMORY_TYPE_DICT = {
    "Other": "1",
    "Unknown": "2",
    "DRAM": "3",
    "EDRAM": "4",
    "VRAM": "5",
    "SRAM": "6",
    "RAM": "7",
    "ROM": "8",
    "Flash": "9",
    "EEPROM": "10",
    "FEPROM": "11",
    "EPROM": "12",
    "CDRAM": "13",
    "3DRAM": "14",
    "SDRAM": "15",
    "SGRAM": "16",
    "RDRAM": "17",
    "DDR": "18",
    "DDR-2": "19",
    "DDR-2-FB-DIMM": "20",
    "DDR-3": "24",
    "FBD2": "25"
}


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

    def get_parameters_with_units(self, response, output):
        if output["CurrentOperatingSpeed"] is not None:
            output["CurrentOperatingSpeed"] = \
                str(float(response.json_data.get("OperatingSpeedMhz"))) \
                + " MHz"
        else:
            output["CurrentOperatingSpeed"] = NA
        if output["Speed"]:
            output["Speed"] = \
                str(response.json_data.get("AllowedSpeedsMHz")[0] / 1000)\
                + " GHz"
        else:
            output["Speed"] = NA
        if output["Size"] is not None:
            output["Size"] = \
                str(response.json_data.get("CapacityMiB") / 1024) + " GB"
        else:
            output["Size"] = NA
        return output

    def get_memory_details(self, memory_link):
        response = self.idrac.invoke_request(method='GET', uri=memory_link)
        output = {}
        if response.status_code == 200:
            output["BankLabel"] = response.json_data.get("Oem", {})\
                .get("Dell", {}).get("DellMemory", {}).get("BankLabel", NA)
            output["CurrentOperatingSpeed"] = \
                response.json_data.get("OperatingSpeedMhz")
            output["DeviceDescription"] = \
                response.json_data.get("Description", NA)
            output["FQDD"] = response.json_data.get("Id", NA)
            output["Key"] = response.json_data.get("Id", NA)
            output["ManufactureDate"] = response.json_data.get("Oem", {})\
                .get("Dell", {}).get("DellMemory", {}).\
                get("ManufactureDate", NA)
            output["Manufacturer"] = response.json_data.\
                get("Manufacturer", NA)
            output["MemoryType"] = \
                MAPPING_MEMORY_TYPE_DICT.get(
                    response.json_data.get("MemoryDeviceType"),
                    NA)
            output["MemoryType_API"] = response.json_data.\
                get("MemoryDeviceType", NA)
            output["Model"] = response.json_data.get("Oem", {})\
                .get("Dell", {}).get("DellMemory", {}).\
                get("Model", NA)
            output["PartNumber"] = response.json_data.get("PartNumber", NA)
            output["PrimaryStatus"] = \
                response.json_data.get("Status", {}).get("Health", NA)
            output["Rank"] = \
                MAPPING_DICT_FOR_RANK.get(response.json_data.get("RankCount"),
                                          NA)
            output["SerialNumber"] = response.json_data.\
                get("SerialNumber", NA)
            output["Size"] = response.json_data.get("CapacityMiB")
            output["Speed"] = response.json_data.get("AllowedSpeedsMHz")
            output["memoryDeviceStateSettings"] = \
                response.json_data.get("Status", {}).get("State", NA)
            if response.json_data.get("Status", {}).get("Health") == "OK":
                output["PrimaryStatus"] = "Healthy"
            else:
                output["PrimaryStatus"] = response.json_data.\
                    get("Status", {}).get("Health", NA)
            self.get_parameters_with_units(response, output)
        return output

    def get_memory_info(self):
        memory_output = []
        memory_links_list = self.get_memory_links()
        for each_link in memory_links_list:
            memory_output.append(self.get_memory_details(each_link))
        return memory_output
