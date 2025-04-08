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


GET_IDRAC_LICENSE_DETAILS_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellLicenses?$expand=*($levels=1)"
NA = "Not Available"


class IDRACLicenseInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def get_license_info(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_LICENSE_DETAILS_URI)
        license_output = []
        if response.status_code == 200:
            members = response.json_data.get("Members")
            for each in members:
                output = {
                    "InstanceID": each.get("Id", NA),
                    "Key": each.get("Id", NA),
                    "LicenseDescription": each.get("LicenseDescription", [NA])[0],
                    "LicenseInstallDate": each.get("LicenseInstallDate", NA),
                    "LicenseSoldDate": each.get("LicenseSoldDate", NA),
                    "LicenseType": each.get("LicenseType", NA),
                }
                if each.get("LicensePrimaryStatus") == "OK":
                    output["PrimaryStatus"] = "Healthy"
                else:
                    output["PrimaryStatus"] = each.get("LicensePrimaryStatus", NA)
                license_output.append(output)
        return license_output
