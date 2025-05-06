# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 9.13.0
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


BASE_URI = "/redfish/v1/Managers/"
ODATA_ID = "@odata.id"


class IDRACLifecycleControllerStatusInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def get_lifecycle_controller_status_api(self):
        controller_status_baseuri_response = self._get_controller_status_baseuri_response()
        manager_uri = self._get_manager_uri(controller_status_baseuri_response)
        if manager_uri:
            manager_response = self._get_manager_response(manager_uri)
            lc_service_uri = self._get_lc_service_uri(manager_response)
            if lc_service_uri:
                lc_service_response = self._get_lc_service_response(lc_service_uri)
                lc_status_check_uri = self._get_lc_status_check_uri(lc_service_response)
                if lc_status_check_uri:
                    return lc_status_check_uri
        return ""

    def _get_controller_status_baseuri_response(self):
        return self.idrac.invoke_request(uri=BASE_URI, method="GET")

    def _get_manager_uri(self, controller_status_baseuri_response):
        return controller_status_baseuri_response.json_data.get("Members", [])[0].get(ODATA_ID, "")

    def _get_manager_response(self, manager_uri):
        return self.idrac.invoke_request(uri=manager_uri, method="GET")

    def _get_lc_service_uri(self, manager_response):
        return manager_response.json_data.get("Links", {}).get("Oem", {}).get("Dell", {}).get("DellLCService", {}).get(ODATA_ID, "")

    def _get_lc_service_response(self, lc_service_uri):
        return self.idrac.invoke_request(uri=lc_service_uri, method="GET")

    def _get_lc_status_check_uri(self, lc_service_response):
        return lc_service_response.json_data.get("Actions", {}).get("#DellLCService.GetRemoteServicesAPIStatus", {}).get("target", "")

    def get_lifecycle_controller_status_info(self):
        lc_status_check_uri = self.get_lifecycle_controller_status_api()
        if lc_status_check_uri:
            controller_status_response = self.idrac.invoke_request(
                uri=lc_status_check_uri,
                method='POST',
                data="{}",
                dump=False
            )
            if controller_status_response.status_code == 200:
                lc_status = controller_status_response.json_data.\
                    get("LCStatus")
                return lc_status
        return ""
