# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.2.0
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_lifecycle_controller_status_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from mock import MagicMock, patch, Mock
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from mock import PropertyMock
from io import StringIO
from ansible.module_utils._text import to_text
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestLcStatus(FakeAnsibleModule):
    module = idrac_lifecycle_controller_status_info

    @pytest.fixture
    def idrac_lc_status_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.config_mgr = idrac_obj
        type(idrac_obj).LCStatus = Mock(return_value="lcstatus")
        type(idrac_obj).LCReady = Mock(return_value="lcready")
        return idrac_obj

    @pytest.fixture
    def idrac_connection_lcstatus_mock(self, mocker, idrac_lc_status_mock):
        idrac_conn_class_mock = mocker.patch(MODULE_PATH + 'idrac_lifecycle_controller_status_info.iDRACConnection',
                                             return_value=idrac_lc_status_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_lc_status_mock
        return idrac_lc_status_mock

    def test_main_get_lcstatus_success_case01(self, idrac_connection_lcstatus_mock, idrac_default_args):
        obj2 = MagicMock()
        idrac_connection_lcstatus_mock.config_mgr = obj2
        type(obj2).LCStatus = PropertyMock(return_value="lcstatus")
        type(obj2).LCReady = PropertyMock(return_value="lcready")
        result = self._run_module(idrac_default_args)
        assert result['lc_status_info']['LCReady'] == "lcready"
        assert result['lc_status_info']['LCStatus'] == "lcstatus"

    @pytest.mark.parametrize("exc_type", [RuntimeError, SSLValidationError, ConnectionError, KeyError,
                                          ImportError, ValueError, TypeError, HTTPError, URLError])
    def test_main_get_lcstatus_exception_handling_case(self, exc_type, idrac_connection_lcstatus_mock,
                                                       idrac_default_args):
        obj2 = MagicMock()
        idrac_connection_lcstatus_mock.config_mgr = obj2
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type == URLError:
            type(obj2).LCReady = PropertyMock(side_effect=exc_type("url open error"))
            result = self._run_module(idrac_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            type(obj2).LCReady = PropertyMock(side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
            assert 'msg' in result
        else:
            type(obj2).LCReady = PropertyMock(side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                                                   {"accept-type": "application/json"},
                                                                   StringIO(json_str)))
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
            assert 'msg' in result
