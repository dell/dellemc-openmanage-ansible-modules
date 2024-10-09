# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.8.0
# Copyright (C) 2021-2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_firmware_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from mock import MagicMock, PropertyMock
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from urllib.error import URLError, HTTPError
from io import StringIO
from ansible.module_utils._text import to_text


MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestFirmware(FakeAnsibleModule):
    module = idrac_firmware_info

    @pytest.fixture
    def idrac_firmware_info_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.update_mgr = idrac_obj
        type(idrac_obj).InstalledFirmware = PropertyMock(return_value="msg")
        return idrac_obj

    @pytest.fixture
    def idrac_firmware_info_connection_mock(self, mocker, idrac_firmware_info_mock):
        idrac_conn_class_mock = mocker.patch(MODULE_PATH + 'idrac_firmware_info.iDRACConnection',
                                             return_value=idrac_firmware_info_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_firmware_info_mock
        return idrac_firmware_info_mock

    @pytest.fixture
    def idrac_redfish_mock(self, mocker):
        redfish_mock = MagicMock()
        redfish_conn_mock = mocker.patch(MODULE_PATH + 'idrac_firmware_info.iDRACRedfishAPI',
                                         return_value=redfish_mock)
        redfish_conn_mock.return_value.__enter__.return_value = redfish_mock
        return redfish_mock

    def test_remove_key_functionality(self, mocker, idrac_redfish_mock, idrac_default_args):
        mock_data = {
            "Members": [
                {"KeyToRemove": "Data", "FirmwareVersion": "1.10.05.00"},
                {"KeyToRemove": "Data", "FirmwareVersion": "1.20.05.00"}
            ]
        }

        mock_remove_key = mocker.patch(MODULE_PATH + 'idrac_firmware_info.remove_key', return_value={
            "Members": [
                {"FirmwareVersion": "1.10.05.00"},
                {"FirmwareVersion": "1.20.05.00"}
            ]
        })

        idrac_redfish_mock.invoke_request.return_value.status_code = 200
        idrac_redfish_mock.invoke_request.return_value.json_data = mock_data
        result = self._run_module(idrac_default_args)
        mock_remove_key.assert_called_once_with(mock_data)

        assert result['firmware_info'] == {
            "Members": [
                {"FirmwareVersion": "1.10.05.00"},
                {"FirmwareVersion": "1.20.05.00"}
            ]
        }

    def test_main_idrac_get_firmware_info_success_case01(self, idrac_firmware_info_connection_mock,
                                                         idrac_default_args):
        obj2 = MagicMock()
        idrac_firmware_info_connection_mock.update_mgr = obj2
        type(obj2).InstalledFirmware = PropertyMock(return_value={"Status": "Success"})
        result = self._run_module(idrac_default_args)
        assert result == {"firmware_info": {"Status": "Success"},
                          "msg": "Successfully fetched the firmware inventory details.",
                          "changed": False}

    @pytest.mark.parametrize("exc_type", [SSLValidationError, URLError, ValueError, TypeError, ConnectionError, HTTPError])
    def test_idrac_get_firmware_info_exception_handling_case(self, idrac_firmware_info_connection_mock,
                                                             exc_type, mocker, idrac_default_args):
        json_str = to_text(json.dumps({"data": "out"}))
        obj2 = MagicMock()
        idrac_firmware_info_connection_mock.update_mgr = obj2
        if exc_type not in [HTTPError, SSLValidationError]:
            if exc_type == URLError:
                type(obj2).InstalledFirmware = PropertyMock(side_effect=exc_type('https://idrac-mock-url'))
            else:
                type(obj2).InstalledFirmware = PropertyMock(side_effect=exc_type('test'))
        else:
            type(obj2).InstalledFirmware = PropertyMock(side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                                                             {"accept-type": "application/json"}, StringIO(json_str)))

        if not exc_type == URLError:
            result = self._run_module(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
            assert result['unreachable'] is True
        assert 'msg' in result
