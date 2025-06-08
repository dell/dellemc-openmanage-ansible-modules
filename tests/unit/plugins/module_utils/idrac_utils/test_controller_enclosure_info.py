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
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.controller_enclosure import IDRACEnclosureInfo, \
    GET_IDRAC_CHASSIS_URI
from unittest.mock import MagicMock

MODULE_UTIL_PATH = "ansible_collections.dellemc.openmanage.plugins.module_utils."
INVOKE_REQUEST = 'idrac_redfish.iDRACRedfishAPI.invoke_request'


CHASSIS_RESP = {
    "Members": [
        {
            "@odata.id": "/redfish/v1/Chassis/Enclosure/Enclosure_device/1"
        },
        {
            "@odata.id": "/redfish/v1/Chassis/PcieDevice/1"
        }
    ]
}

ENCLOSURE_RESP = {
    "Oem": {
        "Dell": {
            "DellChassisEnclosure": {
                "Links": {
                    "DellEnclosureEMMCollection@odata.count": 2
                },
                "SlotCount": 24,
                "Version": "2.0.0",
                "WiredOrder": 0,
                "Connector": "SAS",
                "ServiceTag": "XXXXXXX"
            },
        },
    },
    "AssetTag": "",
    "Description": "This is description.",
    "Id": "Enclosure_device",
    "Name": "Enclosure",
    "Status": {
        "Health": "Critical"
    },
}

expected_resp = [
    {
        'AssetTag': 'Not Available',
        'DeviceDescription': 'This is description.',
        'FQDD': 'Enclosure_device',
        'Key': 'Enclosure_device',
        'SlotCount': '24',
        'State': 'Not Available',
        'Version': '2.0.0',
        'WiredOrder': '0',
        'Connector': 'SAS',
        'ServiceTag': 'XXXXXXX',
        'PrimaryStatus': 'Critical',
        'ProductName': 'Enclosure',
        'PSUCount': 'Not Available',
        'FanCount': 'Not Available',
        'EMMCount': '2',
    }
]


class TestIDRACCpuInfo(object):

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
        if 'uri' in kwargs and kwargs['uri'] == GET_IDRAC_CHASSIS_URI:
            obj.json_data = CHASSIS_RESP
        else:
            obj.json_data = ENCLOSURE_RESP
        return obj

    def test_get_cpu_system_info(self, mocker, module_params):
        iDRACRedfishAPI.get_server_generation = (17, '1.20.30', 'iDRAC 10')
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     self.mock_get_dynamic_idrac_invoke_request)
        idrac_obj = iDRACRedfishAPI(module_params=module_params)
        resp = IDRACEnclosureInfo(idrac_obj).get_enclosure_system_info()
        assert resp == expected_resp

    def test_get_controller_enclosure_sensor_info(self, mocker, module_params):
        iDRACRedfishAPI.get_server_generation = (17, '1.20.30', 'iDRAC 10')
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     self.mock_get_dynamic_idrac_invoke_request)
        idrac_obj = iDRACRedfishAPI(module_params=module_params)
        resp = IDRACEnclosureInfo(
            idrac_obj).get_controller_enclosure_sensor_info(expected_resp)
        enclosure_sensor_expected_resp = [
            {'FQDD': 'Enclosure_device', 'Key': 'Enclosure_device'}]
        assert resp == enclosure_sensor_expected_resp
