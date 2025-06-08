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
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.cpu import IDRACCpuInfo, \
    GET_IDRAC_CPU_URI
from unittest.mock import MagicMock

MODULE_UTIL_PATH = "ansible_collections.dellemc.openmanage.plugins.module_utils."
INVOKE_REQUEST = 'idrac_redfish.iDRACRedfishAPI.invoke_request'

CPU_RESP = {
    "Members": [
        {
            "Oem": {
                "Dell": {
                    "DellProcessor": {
                        "CPUFamily": "Intel(R) Xeon(R) CPU E5-2680 v3 @ 2.50GHz",
                        "ExecuteDisabledCapable": "Enabled",
                        "ExecuteDisabledEnabled": "Enabled",
                        "HyperThreadingCapable": "Disabled",
                        "HyperThreadingEnabled": "Enabled",
                        "TurboModeCapable": "Enabled",
                        "TurboModeEnabled": "Disabled",
                        "VirtualizationTechnologyCapable": "Disabled",
                        "VirtualizationTechnologyEnabled": "Enabled",
                        "Volts": "2.5",
                        "CurrentClockSpeedMhz": 2000
                    }
                }
            },
            "Name": "CPU 1",
            "Socket": "1",
            "Status": {
                "Health": "OK"
            },
            "TotalEnabledCores": 24,
            "Id": "DCIM:Processor.1",
            "MaxSpeedMHz": 2500,
            "Model": "Intel(R) Xeon(R) CPU E5-2680 v3 @ 2.50GHz",
            "InstructionSet": "x86-64"
        },
    ]
}


class TestIDRACCpuInfo(object):

    @pytest.fixture
    def module_params(self):
        module_parameters = {'idrac_ip': 'xxx.xxx.x.x', 'idrac_user': 'username',
                             'idrac_password': 'password', 'idrac_port': '443'}
        return module_parameters

    @pytest.fixture
    def idrac_redfish_object(self, module_params):
        iDRACRedfishAPI.get_server_generation = [17, '1.20.30', 'iDRAC 10']
        idrac_redfish_obj = iDRACRedfishAPI(module_params)
        return idrac_redfish_obj

    def mock_get_dynamic_idrac_invoke_request(self, *args, **kwargs):
        obj = MagicMock()
        obj.status_code = 200
        if 'uri' in kwargs and kwargs['uri'] == GET_IDRAC_CPU_URI:
            obj.json_data = CPU_RESP
        return obj

    def test_get_cpu_system_info(self, mocker, module_params):
        iDRACRedfishAPI._get_session_resource_collection = MagicMock(
            return_value={
                "SESSION": "/redfish/v1/SessionService/Sessions",
                "SESSION_ID": "/redfish/v1/SessionService/Sessions/{Id}",
            }
        )
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     self.mock_get_dynamic_idrac_invoke_request)
        idrac_obj = iDRACRedfishAPI(module_params=module_params)
        expected_resp = [
            {
                'CPUFamily': 'Intel(R) Xeon(R) CPU E5-2680 v3 @ 2.50GHz',
                'Characteristics': '64-bit Capable',
                'CurrentClockSpeed': '2.0 GHz',
                'DeviceDescription': 'CPU 1',
                'ExecuteDisabledCapable': 'Enabled',
                'ExecuteDisabledEnabled': 'Enabled',
                'FQDD': 'DCIM:Processor.1',
                'HyperThreadingCapable': 'Disabled',
                'HyperThreadingEnabled': 'Enabled',
                'Key': '1',
                'Manufacturer': 'Not Available',
                'MaxClockSpeed': '2.5 GHz',
                'Model': 'Intel(R) Xeon(R) CPU E5-2680 v3 @ 2.50GHz',
                'NumberOfEnabledCores': '24',
                'NumberOfEnabledThreads': 'Not Available',
                'NumberOfProcessorCores': 'Not Available',
                'PrimaryStatus': 'OK',
                'TurboModeCapable': 'Enabled',
                'TurboModeEnabled': 'Disabled',
                'VirtualizationTechnologyCapable': 'Disabled',
                'VirtualizationTechnologyEnabled': 'Enabled',
                'Voltage': '2.5',
                'processorDeviceStateSettings': 'Not Available'
            }
        ]
        resp = IDRACCpuInfo(idrac_obj).get_cpu_system_info()
        assert resp == expected_resp
