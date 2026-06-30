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
from unittest.mock import MagicMock, PropertyMock
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from urllib.error import URLError, HTTPError
from io import StringIO
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestFirmware(FakeAnsibleModule):
    module = idrac_firmware_info

    @pytest.fixture
    def idrac_redfish_mock(self, mocker):
        redfish_mock = MagicMock()
        redfish_conn_mock = mocker.patch(MODULE_PATH + 'idrac_firmware_info.iDRACRedfishAPI',
                                         return_value=redfish_mock)
        redfish_conn_mock.return_value.__enter__.return_value = redfish_mock
        return redfish_mock

    def test_get_idrac_firmware_info_success(self, mocker, idrac_redfish_mock, idrac_default_args):

        mock_data = {
            "Members": [
                {"Id": "Component1", "MajorVersion": 1, "MinorVersion": 2, "BuildNumber": 123, "RevisionNumber": 5, "VersionString": "1.2.5"},
                {"Id": "Component2", "MajorVersion": 1, "MinorVersion": 3, "BuildNumber": 456, "RevisionNumber": 5, "VersionString": "1.3.5"}
            ]
        }

        idrac_redfish_mock.invoke_request.return_value.status_code = 200
        idrac_redfish_mock.invoke_request.return_value.json_data = mock_data

        result = self._run_module(idrac_default_args)

        firmware_info_filtered = [
            {
                "BuildNumber": str(fw["BuildNumber"]),
                "MajorVersion": str(fw["MajorVersion"]),
                "MinorVersion": str(fw["MinorVersion"]),
                "RevisionNumber": str(fw.get("RevisionNumber", "Not Available")),
                "VersionString": fw.get("VersionString", "Not Available")
            }
            for fw in result['firmware_info']['Firmware']
        ]

        expected_firmware_info = [
            {
                "BuildNumber": "123",
                "MajorVersion": "1",
                "MinorVersion": "2",
                "RevisionNumber": "5",
                "VersionString": "1.2.5"
            },
            {
                "BuildNumber": "456",
                "MajorVersion": "1",
                "MinorVersion": "3",
                "RevisionNumber": "5",
                "VersionString": "1.3.5"
            }
        ]

        assert firmware_info_filtered == expected_firmware_info

    def test_idrac_get_firmware_info_url_error(self, idrac_redfish_mock, idrac_default_args):

        idrac_redfish_mock.invoke_request.side_effect = URLError('idrac-mock-url')
        result = self._run_module(idrac_default_args)
        assert 'idrac-mock-url' in result['msg']
        assert result['changed'] is False
        assert result['unreachable'] is True

    @pytest.mark.parametrize("exc_type", [SSLValidationError, URLError, ValueError, TypeError, ConnectionError, HTTPError])
    def test_idrac_get_firmware_info_exception_handling_case(self, idrac_redfish_mock,
                                                             exc_type, mocker, idrac_default_args):
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            if exc_type == URLError:
                idrac_redfish_mock.invoke_request.side_effect = exc_type('https://idrac-mock-url')
            else:
                idrac_redfish_mock.invoke_request.side_effect = exc_type('test')
        else:
            idrac_redfish_mock.invoke_request.side_effect = exc_type('https://testhost.com', 400, 'http error message',
                                                                     {"accept-type": "application/json"}, StringIO(json_str))

        if not exc_type == URLError:
            result = self._run_module(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
            assert result['changed'] is False
        assert 'msg' in result
