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


class IDRACSystemInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def system_mapped_data(self, resp):
        keys_to_search = {
            "AssetTag": "Not Available",
            "BIOSReleaseDate": "BIOSReleaseDate",
            "BIOSVersionString": "BIOSVersionString",
            "BaseBoardChassisSlot": "BaseBoardChassisSlot",
            "BoardPartNumber": "BoardPartNumber",
            "BoardSerialNumber": "BoardSerialNumber",
            "ChassisModel": "ChassisModel",
            "ChassisServiceTag": "ChassisServiceTag",
            "ChassisSystemHeight": "ChassisSystemHeight",
            "CurrentRollupStatus": "CurrentRollupStatus",
            "DeviceDescription": "DeviceDescription",
            "ExpressServiceCode": "ExpressServiceCode",
            "Key": "ServiceTag",
            "LifecycleControllerVersion": "LifecycleControllerVersion",
            "Manufacturer": "Manufacturer",
            "Model": "Model",
            "OSName": "OSName",
            "OSVersion": "OSVersion",
            "PowerState": "PowerState",
            "PrimaryStatus": "PrimaryStatus",
            "ServiceTag": "ServiceTag",
            "SysMemTotalSize": "SysMemTotalSize",
            "SystemGeneration": "SystemGeneration",
            "SystemID": "SystemID",
            "SystemLockDown": "SystemLockDown",
            "UUID": "UUID",
            "iDRACURL": "iDRACURL"
        }

        system_data = {}
        system_data = resp.get("Oem", {}).get("Dell", {}).get("DellSystem", {})

        # Extract the relevant fields
        extracted_data = {
            key: system_data.get(response_key, "Not Available")
            for key, response_key in keys_to_search.items()
        }

        return extracted_data

    def get_system_info(self):
        output = []
        resp = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_SYSTEM_DETAILS_URI_10)
        if resp.status_code == 200:
            output.append(self.system_mapped_data(resp.json_data))
        return output
