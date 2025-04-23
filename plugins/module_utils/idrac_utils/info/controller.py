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


GET_IDRAC_CONTROLLER_URI = "/redfish/v1/Systems/System.Embedded.1/Oem/Dell/DellControllers"
NA = "Not Available"


class IDRACControllerInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def get_controller_data(self, resp):
        output = {
            "Bus": NA,
            "CacheSize": str(resp.get("CacheSizeInMB")) + " MB",
            "CachecadeCapability": str(resp.get("CachecadeCapability", NA)),
            "ControllerFirmwareVersion": str(resp.get("ControllerFirmwareVersion", NA)),
            "DeviceCardDataBusWidth": str(resp.get("DeviceCardDataBusWidth", NA)),
            "DeviceCardManufacturer": NA,
            "DeviceCardSlotLength": str(resp.get("DeviceCardSlotLength", NA)),
            "DeviceCardSlotType": str(resp.get("DeviceCardSlotType", NA)),
            "DeviceDescription": NA,
            "DriverVersion": str(resp.get("DriverVersion", NA)),
            "EncryptionCapability": str(resp.get("EncryptionCapability", NA)),
            "EncryptionMode": str(resp.get("WiredOrder", NA)),
            "FQDD": str(resp.get("Id", NA)),
            "Key": str(resp.get("Id", NA)),
            "MaxAvailablePCILinkSpeed": str(resp.get("MaxAvailablePCILinkSpeed", NA)),
            "MaxPossiblePCILinkSpeed": str(resp.get("MaxPossiblePCILinkSpeed", NA)),
            "PCISlot": str(resp.get("PCISlot", NA)),
            "PCIVendorID": NA,
            "PrimaryStatus": NA,
            "ProductName": NA,
            "RollupStatus": str(resp.get("RollupStatus", NA)),
            "SASAddress": str(resp.get("SASAddress", NA)),
            "SecurityStatus": str(resp.get("SecurityStatus", NA)),
            "SlicedVDCapability": str(resp.get("SlicedVDCapability", NA)),
            "SupportControllerBootMode": str(resp.get("SupportControllerBootMode", NA)),
            "SupportEnhancedAutoForeignImport": str(resp.get("SupportEnhancedAutoForeignImport", NA)),
            "SupportRAID10UnevenSpans": str(resp.get("SupportRAID10UnevenSpans", NA)),
            "T10PICapability": str(resp.get("T10PICapability", NA))
        }
        return output

    def get_controller_system_info(self):
        output = []
        resp = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_CONTROLLER_URI)
        for each_member in resp.json_data.get("Members", []):
            output.append(self.get_controller_data(each_member))
        return output
