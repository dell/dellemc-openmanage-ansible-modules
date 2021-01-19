# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.0.0
# Copyright (C) 2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_firmware_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible_collections.dellemc.openmanage.tests.unit.compat.mock import MagicMock, PropertyMock
from pytest import importorskip
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from io import StringIO
from ansible.module_utils._text import to_text

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")

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

    def test_main_idrac_get_firmware_info_success_case01(self, idrac_firmware_info_connection_mock,
                                                         idrac_default_args):
        obj2 = MagicMock()
        idrac_firmware_info_connection_mock.update_mgr = obj2
        type(obj2).InstalledFirmware = PropertyMock(return_value={"Status": "Success"})
        result = self._run_module(idrac_default_args)
        assert result == {"firmware_info": {"Status": "Success"},
                          "msg": "Successfully fetched the firmware inventory details.",
                          "changed": False}

    @pytest.mark.parametrize("exc_type", [SSLValidationError, URLError, ValueError, TypeError,
                                          ConnectionError, HTTPError])
    def test_idrac_get_firmware_info_exception_handling_case(self, idrac_firmware_info_connection_mock,
                                                             exc_type, mocker, idrac_default_args):
        json_str = to_text(json.dumps({"data": "out"}))
        obj2 = MagicMock()
        idrac_firmware_info_connection_mock.update_mgr = obj2
        if exc_type not in [HTTPError, SSLValidationError]:
            type(obj2).InstalledFirmware = PropertyMock(side_effect=exc_type('test'))
        else:
            type(obj2).InstalledFirmware = PropertyMock(side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                                                             {"accept-type": "application/json"}, StringIO(json_str)))
        if not exc_type == URLError:
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result
