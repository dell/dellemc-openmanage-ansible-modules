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

    def get_device_details(self, device_link):
        response = self.idrac.invoke_request(method='GET', uri=device_link)
        output = {}
        if response.status_code == 200:
            output["BusWidth"] = response.json_data.get("DataBusWidth")
            output["DeviceDescription"] = "DeviceDescription"
            output["DeviceID"] = "Key"
            output["Manufacturer"] = "Manufacturer"
            output["SlotLength"] = "SlotLength"
            output["SlotType"] = "SlotType"
            output["Description"] = "Description"
            output["BankLabel"] = response.json_data.get("Oem", {})\
                .get("Dell", {}).get("DellMemory", {}).get("BankLabel", "NA")
        return output

    def get_pcidevice_info(self):
        pcidevice_output = []
        device_links_list = self.get_device_links()
        for each_link in device_links_list:
            pcidevice_output.append(self.get_device_details(each_link))
        return pcidevice_output
