# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.2.0
# Copyright (C) 2021-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_system_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from mock import MagicMock, Mock
from pytest import importorskip
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from io import StringIO
from ansible.module_utils._text import to_text

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestSystemInventory(FakeAnsibleModule):
    module = idrac_system_info

    @pytest.fixture
    def idrac_system_info_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.get_entityjson = idrac_obj
        type(idrac_obj).get_json_device = Mock(return_value="msg")
        return idrac_obj

    @pytest.fixture
    def idrac_system_info_connection_mock(self, mocker, idrac_system_info_mock):
        idrac_conn_class_mock = mocker.patch(MODULE_PATH +
                                             'idrac_system_info.iDRACConnection',
                                             return_value=idrac_system_info_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_system_info_mock
        return idrac_system_info_mock

    def test_idrac_system_info_main_success_case01(self, idrac_system_info_mock, idrac_system_info_connection_mock,
                                                   idrac_default_args):
        idrac_system_info_mock.get_entityjson.return_value = None
        idrac_system_info_connection_mock.get_json_device.return_value = {"status": "Success"}
        result = self._run_module(idrac_default_args)
        assert result == {"system_info": {"status": "Success"},
                          "msg": "Successfully fetched the system inventory details.",
                          "changed": False}

    @pytest.mark.parametrize("exc_type", [SSLValidationError, URLError, ValueError, TypeError,
                                          ConnectionError, HTTPError])
    def test_idrac_system_info_main_exception_handling_case(self, exc_type, idrac_system_info_connection_mock,
                                                            idrac_default_args):
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            idrac_system_info_connection_mock.get_json_device.side_effect = exc_type('test')
        else:
            idrac_system_info_connection_mock.get_json_device.side_effect = exc_type('http://testhost.com', 400,
                                                                                     'http error message',
                                                                                     {
                                                                                         "accept-type": "application/json"},
                                                                                     StringIO(json_str))
        if not exc_type == URLError:
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result
