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

GET_IDRAC_SYSTEM_DETAILS_URI_10 = "/redfish/v1/Systems/System.Embedded.1"
GET_IDRAC_MANAGER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/"
NA = "Not Available"


class IDRACSystemInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def get_firmware_ver_idrac_url(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_MANAGER_URI)
        if response.status_code == 200:
            version = response.json_data.get("FirmwareVersion", "")
            idrac_url = response.json_data.get("Oem", {}).get("Dell", {}).get("DelliDRACCard", {}).get("URLString")
            return version , idrac_url
        return ""

    def system_mapped_data(self, resp):
        system_data = resp.get("Oem", {}).get("Dell", {}).get("DellSystem", {})
        firmware_ver, idrac_url = self.get_firmware_ver_idrac_url()
        output = {
            "AssetTag": NA if (asset := resp.get("AssetTag")) == "" else asset,
            "BIOSReleaseDate": system_data.get("BIOSReleaseDate", NA),
            "BIOSVersionString": resp.get("BiosVersion", NA),
            "BaseBoardChassisSlot": system_data.get("BaseBoardChassisSlot", NA),
            "BladeGeometry": system_data.get("BladeGeometry", NA),
            "BoardPartNumber": system_data.get("BoardPartNumber", NA),
            "BoardSerialNumber": system_data.get("BoardSerialNumber", NA),
            "CMCIP": "CMCIP",
            "CPLDVersion": "CPLDVersion",
            "ChassisModel": system_data.get("ChassisModel", NA),
            "ChassisName": system_data.get("ChassisName", NA),
            "ChassisServiceTag": system_data.get("ChassisServiceTag", NA),
            "ChassisSystemHeight": system_data.get("ChassisSystemHeightUnit", NA),
            "CurrentRollupStatus": system_data.get("CurrentRollupStatus", NA),
            "DeviceDescription": resp.get("Name"),
            "DeviceType": resp.get("DeviceType", NA),
            "ExpressServiceCode": system_data.get("ExpressServiceCode", NA),
            "HostName": resp.get("HostName", NA),
            "Key": resp.get("SKU"),
            "LifecycleControllerVersion": NA if (firmware_ver == "") else firmware_ver,
            "MachineName": "MachineName",
            "Manufacturer": "Manufacturer",
            "MaxCPUSockets": system_data.get("MaxCPUSockets", NA),
            "MaxDIMMSlots": system_data.get("MaxDIMMSlots", NA),
            "MaxPCIeSlots": system_data.get("MaxPCIeSlots", NA),
            "MemoryOperationMode": system_data.get("MemoryOperationMode", NA),
            "Model": system_data.get("SystemGeneration", NA),
            "NodeID": system_data.get("NodeID", NA),
            "OSName": "OSName",
            "OSVersion": "OSVersion",
            "PlatformGUID": system_data.get("PlatformGUID", NA),
            "PowerCap": system_data.get("PowerCap", NA),
            "PowerCapEnabledState": system_data.get("PowerCapEnabledState", NA),
            "PowerState": "PowerState",
            "PrimaryStatus": "PrimaryStatus",
            "RACType": "RACType",
            "ServerAllocation": "ServerAllocation",
            "ServiceTag": system_data.get("NodeID", NA),
            "SysMemMaxCapacitySize": "SysMemMaxCapacitySize",
            # "SysMemTotalSize": total_system_memory_GiB,
            "SysName": system_data.get("Name", NA),
            "SystemGeneration": system_data.get("SystemGeneration", NA),
            "SystemID": system_data.get("SystemID", NA),
            "SystemLockDown": "SystemLockDown",
            "SystemRevision": system_data.get("SystemRevision", NA),
            "UUID": system_data.get("UUID", NA),
            "VirtualAddressManagementApplication": "VirtualAddressManagementApplication",
            "_Type": "Server",
            "iDRACURL": NA if (idrac_url == "") else idrac_url,
            "smbiosGUID": system_data.get("smbiosGUID", NA)
        }

        return output

    def get_system_info(self):
        output = []
        resp = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_SYSTEM_DETAILS_URI_10)
        if resp.status_code == 200:
            output.append(self.system_mapped_data(resp.json_data))
        return output
