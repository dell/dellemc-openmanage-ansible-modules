# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.2
# Copyright (C) 2025 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.bios import IDRACBiosInfo, \
    GET_IDRAC_SYSTEM_URI
from unittest.mock import MagicMock

MODULE_UTIL_PATH = "ansible_collections.dellemc.openmanage.plugins.module_utils."
INVOKE_REQUEST = 'idrac_redfish.iDRACRedfishAPI.invoke_request'

SYSTEM_RESP = {"BiosVersion": "1.11",
               "Oem": {
                   "Dell": {
                       "DellSystem": {
                           "BIOSReleaseDate": "02/06/2019",
                           "smbiosGUID": "0001110000-1000-111-00110-11111"
                       }
                   }
               }}
FIRMWARE_RESP = {
    "Members": [
        {
            "ElementName": "BIOS",
            "Status": "Installed",
            "Id": "DCIM:Installed__BIOS.Setup-1.1"
        },
        {
            "ElementName": "IDRAC",
            "Status": "Installed",
            "Id": "DCIM:Installed__IDRAC.Setup-1.2"
        }
    ]
}


class TestIDRACBiosInfo(object):

    @pytest.fixture
    def module_params(self):
        module_parameters = {'idrac_ip': 'xxx.xxx.x.x', 'idrac_user': 'username',
                             'idrac_password': 'password', 'idrac_port': '443'}
        return module_parameters

    @pytest.fixture
    def idrac_redfish_object(self, module_params):
        iDRACRedfishAPI._get_session_resource_collection = MagicMock(
            return_value={
                "SESSION": "/redfish/v1/SessionService/Sessions",
                "SESSION_ID": "/redfish/v1/SessionService/Sessions/{Id}",
            }
        )
        idrac_redfish_obj = iDRACRedfishAPI(module_params)
        return idrac_redfish_obj

    def mock_get_dynamic_idrac_invoke_request(self, *args, **kwargs):
        obj = MagicMock()
        obj.status_code = 200
        if 'uri' in kwargs and kwargs['uri'] == GET_IDRAC_SYSTEM_URI:
            obj.json_data = SYSTEM_RESP
        else:
            obj.json_data = FIRMWARE_RESP
        return obj

    def test_get_bios_system_info_without_idrac(self, mocker):
        resp = IDRACBiosInfo(MagicMock()).get_bios_system_info()
        assert sorted(resp[0]) == sorted({
            "BIOSReleaseDate": "",
            "FQDD": "",
            "InstanceID": "",
            "Key": "",
            "SMBIOSPresent": "",
            "VersionString": ""
        })

    def test_get_bios_system_info(self, mocker, module_params):
        iDRACRedfishAPI._get_session_resource_collection = MagicMock(
            return_value={
                "SESSION": "/redfish/v1/SessionService/Sessions",
                "SESSION_ID": "/redfish/v1/SessionService/Sessions/{Id}",
            }
        )
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST, self.mock_get_dynamic_idrac_invoke_request)
        idrac_obj = iDRACRedfishAPI(module_params=module_params)
        resp = IDRACBiosInfo(idrac_obj).get_bios_system_info()
        assert resp == [{
            "BIOSReleaseDate": "02/06/2019",
            "FQDD": "BIOS.Setup-1.1",
            "InstanceID": "DCIM:Installed__BIOS.Setup-1.1",
            "Key": "BIOS.Setup-1.1",
            "SMBIOSPresent": "True",
            "VersionString": "1.11"
        }]
