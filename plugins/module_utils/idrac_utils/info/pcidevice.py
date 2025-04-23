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


GET_IDRAC_PCI_DETAILS_URI = "/redfish/v1/Chassis/System.Embedded.1/PCIeDevices/"
NA = "Not Available"
SLOT_TYPE_MAPPING = {
    "Other": "0001",
    "Unknown": "0002",
    "ISA": "0003",
    "MCA": "0004",
    "EISA": "0005",
    "PCI": "0006",
    "PC Card (PCMCIA)": "0007",
    "VL-VESA": "0008",
    "Proprietary": "0009",
    "Processor Card Slot": "000A",
    "Proprietary Memory Card Slot": "000B",
    "I/O Riser Card Slot": "000C",
    "NuBus": "000D",
    "PCI - 66MHz Capable": "000E",
    "AGP": "000F",
    "AGP 2X": "0010",
    "AGP 4X": "0011",
    "PCI-X": "0012",
    "AGP 8X": "0013",
    "PC-98/C20": "00A0",
    "PC-98/C24": "00A1",
    "PC-98/E": "00A2",
    "PC-98/Local Bus": "00A3",
    "PC-98/Card": "00A4",
    "PCI Express": "00A5",
    "PCI Express x1": "00A6",
    "PCI Express x2": "00A7",
    "PCI Express x4": "00A8",
    "PCI Express x8": "00A9",
    "PCI Express x16": "00AA",
    "PCI Express Gen 2": "00AB",
    "PCI Express Gen 2 x1": "00AC",
    "PCI Express Gen 2 x2": "00AD",
    "PCI Express Gen 2 x4": "00AE",
    "PCI Express Gen 2 x8": "00AF",
    "PCI Express Gen 2 x16": "00B0",
    "PCI Express Gen 3": "00B1",
    "PCI Express Gen 3 x1": "00B2",
    "PCI Express Gen 3 x2": "00B3",
    "PCI Express Gen 3 x4": "00B4",
    "PCI Express Gen 3 x8": "00B5",
    "PCI Express Gen 3 x16": "00B6"
}
SLOT_LENGTH_MAPPING = {
    "Other": "0001",
    "Unknown": "0002",
    "Short Length": "0003",
    "Long Length": "0004"
}
BUS_WIDTH_MAPPING = {
    "Other": "0001",
    "Unknown": "0002",
    "8Bit": "0003",
    "16Bit": "0004",
    "32Bit": "0005",
    "64Bit": "0006",
    "128Bit": "0007",
    "1XOrX1": "0008",
    "2XOrX2": "0009",
    "4XOrX4": "000A",
    "8XOrX8": "000B",
    "12XOrX12": "000C",
    "16XOrX16": "000D",
    "32XOrX32": "000E"
}


class IDRACPCIDeviceInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def get_device_links(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_PCI_DETAILS_URI)
        device_links_list = []
        if response.status_code == 200:
            members = response.json_data.get("Members")
            for each in members:
                device_links_list.append(each.get("@odata.id"))
        return device_links_list

    def get_device_function_details(self, function_link):
        response = self.idrac.invoke_request(method='GET', uri=function_link)
        buswidth = NA
        slot_type = NA
        deviceid = NA
        buswidth_api = NA
        slot_type_api = NA
        slot_length = NA
        slot_length_api = NA
        if response.status_code == 200:
            resp = response.json_data.get("Oem", {}).\
                get("Dell", {}).get("DellPCIeFunction", {})
            buswidth = \
                BUS_WIDTH_MAPPING.get(resp.get("DataBusWidth"), NA)
            buswidth_api = resp.get("DataBusWidth")
            deviceid = resp.get("Id", NA)
            slot_type = \
                SLOT_TYPE_MAPPING.get(resp.get("SlotType"), NA)
            slot_type_api = resp.get("SlotType")
            slot_length = \
                SLOT_LENGTH_MAPPING.get(resp.get("SlotLength"), NA)
            slot_length_api = resp.get("SlotLength")
        return buswidth, buswidth_api, deviceid, slot_type, slot_type_api, slot_length, slot_length_api

    def get_device_details(self, device_link):
        response = self.idrac.invoke_request(method='GET', uri=device_link)
        functions_output = []
        if response.status_code == 200:
            pci_functions = response.json_data.get("Links", {}).\
                get("PCIeFunctions", [{}])
            for link in pci_functions:
                output = {}
                device_link = link.get("@odata.id")
                if device_link is not None:
                    buswidth, buswidth_api, deviceid, slot_type, \
                        slot_type_api, slot_length, slot_length_api = \
                        self.get_device_function_details(device_link)
                else:
                    buswidth = NA
                    slot_type = NA
                    deviceid = NA
                    buswidth_api = NA
                    slot_type_api = NA
                    slot_length = NA
                    slot_length_api = NA
                output["DataBusWidth"] = buswidth
                output["DataBusWidth_API"] = buswidth_api
                output["DeviceDescription"] = response.json_data.get("Description")
                output["FQDD"] = deviceid
                output["Key"] = deviceid
                output["Manufacturer"] = response.json_data.get("Manufacturer")
                output["SlotLength"] = slot_length
                output["SlotLength_API"] = slot_length_api
                output["SlotType"] = slot_type
                output["SlotType_API"] = slot_type_api
                output["Description"] = response.json_data.get("Description")
                functions_output.append(output)
        return functions_output

    def get_pcidevice_info(self):
        pcidevice_output = []
        device_links_list = self.get_device_links()
        for each_link in device_links_list:
            pcidevice_output.extend(self.get_device_details(each_link))
        return pcidevice_output
