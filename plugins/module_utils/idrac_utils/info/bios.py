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


GET_IDRAC_SYSTEM_URI = "/redfish/v1/Systems/System.Embedded.1"
GET_IDRAC_FIRMWARE_URI = "/redfish/v1/UpdateService/Oem/Dell/DellSoftwareInventory"


class IDRACBiosInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def get_bios_release_date_and_version_and_symbios(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_SYSTEM_URI)
        if response.status_code == 200:
            version = response.json_data.get("BiosVersion", "")
            system = response.json_data.get("Oem", {}).get("Dell", {}).get("DellSystem", {})
            is_symbios_available = "True" if system.get("smbiosGUID", "") else "False"
            return system.get("BIOSReleaseDate", ""), version, is_symbios_available
        return "", "", ""

    def get_bios_fqdd_and_instance_id_and_key(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_FIRMWARE_URI)
        if response.status_code == 200:
            members = response.json_data.get("Members")
            for each in members:
                if each.get('ElementName', '') == 'BIOS' and each.get('Status', '') == 'Installed':
                    instance_id = each.get('Id')
                    fqdd = instance_id.split('__')[-1]
                    key = fqdd
                    return fqdd, instance_id, key
        return "", "", ""

    def get_bios_system_info(self):
        output = {
            "BIOSReleaseDate": "",
            "FQDD": "",
            "InstanceID": "",
            "Key": "",
            "SMBIOSPresent": "",
            "VersionString": ""
        }
        release, version, symbios = self.get_bios_release_date_and_version_and_symbios()
        fqdd, instance_id, key = self.get_bios_fqdd_and_instance_id_and_key()
        output["BIOSReleaseDate"] = release
        output["VersionString"] = version
        output["SMBIOSPresent"] = symbios
        output["FQDD"] = fqdd
        output["InstanceID"] = instance_id
        output["Key"] = key
        return [output]
