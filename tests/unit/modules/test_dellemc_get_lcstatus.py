#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0.14
# Copyright (C) 2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import

import pytest
from ansible.modules.remote_management.dellemc import dellemc_get_lcstatus
from units.modules.remote_management.dellemc.common import FakeAnsibleModule, Constants
from units.compat.mock import MagicMock, patch, Mock
from units.modules.utils import set_module_args, exit_json, fail_json, AnsibleFailJson, AnsibleExitJson
from units.compat.mock import PropertyMock
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")


class TestLcStatus(FakeAnsibleModule):
    module = dellemc_get_lcstatus

    @pytest.fixture
    def idrac_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.config_mgr = idrac_obj
        type(idrac_obj).LCStatus = PropertyMock(return_value="lcstatus")
        type(idrac_obj).LCReady = PropertyMock(return_value="lcready")
        return idrac_obj

    @pytest.fixture
    def idrac_connection_lcstatus_mock(self, mocker, idrac_mock):
        idrac_conn_class_mock = mocker.patch('ansible.modules.remote_management.dellemc.'
                                             'dellemc_get_lcstatus.iDRACConnection', return_value=idrac_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_mock
        return idrac_mock

    def test_run_get_lcstatus_failed_case01(self, idrac_connection_lcstatus_mock, idrac_default_args):
        f_module = self.get_module_mock(params=idrac_default_args)
        error_msg = "Error in Runtime"
        obj2 = MagicMock()
        idrac_connection_lcstatus_mock.config_mgr = obj2
        type(obj2).LCStatus = PropertyMock(side_effect=Exception(error_msg))
        type(obj2).LCReady = PropertyMock(side_effect=Exception(error_msg))
        msg, err = self.module.run_get_lc_status(idrac_connection_lcstatus_mock, f_module)
        assert msg['failed'] is True
        assert msg['msg'] == "Error: {0}".format(error_msg)
        assert err is True

    def test_run_get_lcstatus_success_case01(self, idrac_connection_lcstatus_mock, idrac_default_args):
        obj2 = MagicMock()
        idrac_connection_lcstatus_mock.config_mgr = obj2
        type(obj2).LCStatus =PropertyMock(return_value="lcstatus")
        type(obj2).LCReady = PropertyMock(return_value="lcready")
        f_module = self.get_module_mock(params=idrac_default_args)
        msg, err = self.module.run_get_lc_status(idrac_connection_lcstatus_mock, f_module)
        assert msg['msg']['LCReady'] == "lcready"
        assert msg['msg']['LCStatus'] == "lcstatus"
        assert msg['failed'] is False
        assert err is False

    def test_main_get_lcstatus_success_case01(self, mocker, idrac_connection_lcstatus_mock, idrac_mock, idrac_default_args):
        message = ({"msg": {"LCReady": "lcready", "LCStatus": "lcstatus"}, "failed": False, "changed": False}, False)
        mocker.patch('ansible.modules.remote_management.dellemc.dellemc_get_lcstatus.run_get_lc_status',
                     return_value=message)
        idrac_mock.config_mgr.LCReady.return_value = {"Status": "Success"}
        result = self._run_module(idrac_default_args)
        assert result["changed"] is False
        assert result["failed"] is False
        assert result["msg"]["LCReady"] == "lcready"
        assert result["msg"]["LCStatus"] == "lcstatus"

    def test_main_get_lcstatus_failed_case01(self, idrac_connection_lcstatus_mock, idrac_default_args):
        error_msg = "Error in Runtime"
        obj2 = MagicMock()
        idrac_connection_lcstatus_mock.config_mgr = obj2
        type(obj2).LCStatus = PropertyMock(side_effect=Exception(error_msg))
        type(obj2).LCReady = PropertyMock(side_effect=Exception(error_msg))
        msg = self._run_module_with_fail_json(idrac_default_args)
        assert msg['failed'] is True
        assert msg['msg'] == "Error: {0}".format(error_msg)

    @pytest.mark.parametrize("exc_type", [ImportError, ValueError, RuntimeError])
    def test_main_get_lcstatus_exception_handling_case(self, exc_type, mocker, idrac_mock,
                                                       idrac_connection_lcstatus_mock, idrac_default_args):
        mocker.patch('ansible.modules.remote_management.dellemc.dellemc_get_lcstatus.run_get_lc_status',
                     side_effect=exc_type('test'))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True
