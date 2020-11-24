# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.4
# Copyright (C) 2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible_collections.dellemc.openmanage.plugins.modules import dellemc_change_power_state
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible_collections.dellemc.openmanage.tests.unit.compat.mock import MagicMock, PropertyMock
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")


class TestChangePowerState(FakeAnsibleModule):
    module = dellemc_change_power_state

    @pytest.fixture
    def idrac_change_powerstate_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.config_mgr.ComputerSystemResetTypesEnum = idrac_obj
        type(idrac_obj).change_power = PropertyMock(return_value="change_power")
        return idrac_obj

    @pytest.fixture
    def idrac_change_power_state_connection_mock(self, mocker, idrac_change_powerstate_mock):
        idrac_connection_class_mock = mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                                                   'dellemc_change_power_state.iDRACConnection')
        idrac_connection_class_mock.return_value.__enter__.return_value = idrac_change_powerstate_mock
        return idrac_change_powerstate_mock

    def test_is_change_applicable_for_powerstate_success_case01(self, idrac_change_power_state_connection_mock):
        result = self.module.is_change_applicable_for_power_state("GracefulRestart", "Nmi")
        assert result['Status'] == "Success"
        assert result["Message"] == "Changes found to commit!"
        assert result["changes_applicable"] is True

    def test_is_change_applicable_for_powerstate_success_case02(self, idrac_change_power_state_connection_mock):
        result = self.module.is_change_applicable_for_power_state("On", "On")
        assert result['Status'] == "Success"
        assert result["Message"] == 'No changes found to commit!'
        assert result["changes_applicable"] is False

    def test_is_change_applicable_for_powerstate_success_case03(self, idrac_change_power_state_connection_mock):
        result = self.module.is_change_applicable_for_power_state("Off - Soft", "On")
        assert result['Status'] == "Success"
        assert result["Message"] == 'Changes found to commit!'
        assert result["changes_applicable"] is True

    def test_is_change_applicable_for_powerstate_success_case04(self, idrac_change_power_state_connection_mock):
        result = self.module.is_change_applicable_for_power_state("Off - Soft", "GracefulRestart")
        assert result['Status'] == "Success"
        assert result["Message"] == 'No changes found to commit!'
        assert result["changes_applicable"] is False

    def test_is_change_applicable_for_powerstate_failed_case(self, idrac_change_power_state_connection_mock):
        result = self.module.is_change_applicable_for_power_state("GracefulRestart", "Nmis")
        assert result['Status'] == "Failed"
        assert result["Message"] == 'Failed to execute the command!'
        assert result["changes_applicable"] is False

    def test_run_change_powerstate_success_case01(self, idrac_change_power_state_connection_mock, idrac_default_args,
                                                  mocker):
        idrac_default_args.update({"change_power": "GracefulRestart"})
        message = {'Status': 'Success', 'Message': 'Changes found to commit!', 'changes_applicable': True}
        obj2 = MagicMock()
        idrac_change_power_state_connection_mock.config_mgr = obj2
        type(obj2).change_power = PropertyMock(return_value=message)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        result = self.module.run_change_power_state(idrac_change_power_state_connection_mock, f_module)
        assert result == ({'changed': True, 'failed': False,
                           'msg': {'Message': 'Changes found to commit!',
                                   'Status': 'Success', 'changes_applicable': True}}, False)

    def test_run_change_powerstate_success_case02(self, idrac_change_power_state_connection_mock, mocker,
                                                  idrac_default_args):
        idrac_default_args.update({"change_power": "On"})
        message = {'Status': 'Success', 'Message': 'No changes found to commit!', 'changes_applicable': False}
        idrac_change_power_state_connection_mock.config_mgr.change_power.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        result = self.module.run_change_power_state(idrac_change_power_state_connection_mock, f_module)
        assert result == ({'changed': True, 'failed': False,
                           'msg': {'Message': 'No changes found to commit!',
                                   'Status': 'Success', 'changes_applicable': False}}, False)
        if "Status" in result[0]['msg']:
            if result[0]['msg']['Status'] == "Success":
                assert result[0]['changed'] is True

    def test_run_change_power_state_failed_case01(self, idrac_change_power_state_connection_mock,
                                                  idrac_default_args, mocker):
        idrac_default_args.update({"change_power": "On"})
        message = {'Status': 'Failed', 'Message': 'Failed to execute the command!', 'changes_applicable': False}
        idrac_change_power_state_connection_mock.config_mgr.change_power.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        result = self.module.run_change_power_state(idrac_change_power_state_connection_mock, f_module)
        assert result == ({'changed': False, 'failed': True,
                           'msg': {'Message': 'Failed to execute the command!',
                                   'Status': 'Failed', 'changes_applicable': False}}, False)
        if "Status" in result[0]['msg']:
            if not result[0]['msg']['Status'] == "Success":
                assert result[0]['failed'] is True

    def test_main_change_powerstate_success_case01(self, idrac_change_power_state_connection_mock,
                                                   idrac_default_args, mocker):
        idrac_default_args.update({"change_power": "GracefulRestart"})
        message = ({'changed': False, 'failed': False,
                   'msg': {'Status': 'Success', 'Message': 'Changes found to commit!', 'changes_applicable': True}},
                   False)
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.dellemc_change_power_state.run_change_power_state',
                     return_value=message)
        result = self._run_module(idrac_default_args)
        assert result['changed'] is False
        assert result['failed'] is False

    def test_run_change_powerstate_failed_case02(self, idrac_change_power_state_connection_mock, idrac_default_args):
        idrac_default_args.update({"change_power": "GracefulRestart"})
        error_msg = "Error in Runtime"
        obj2 = MagicMock()
        idrac_change_power_state_connection_mock.config_mgr = obj2
        type(obj2).change_power = PropertyMock(side_effect=Exception(error_msg))
        msg = self._run_module_with_fail_json(idrac_default_args)
        assert msg['failed'] is True
        assert msg['msg'] == "Error: {0}".format(error_msg)

    @pytest.mark.parametrize("exc_type", [ImportError, ValueError, RuntimeError])
    def test_main_exception_handling_case(self, exc_type, idrac_default_args, idrac_change_power_state_connection_mock,
                                          mocker):
        idrac_default_args.update({"change_power": "GracefulRestart"})
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.dellemc_change_power_state.run_change_power_state',
                     side_effect=exc_type('test'))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True
