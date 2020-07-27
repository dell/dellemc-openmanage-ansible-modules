#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.1
# Copyright (C) 2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import

import pytest
from ansible_collections.dellemc.openmanage.plugins.modules import dellemc_idrac_reset
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible_collections.dellemc.openmanage.tests.unit.compat.mock import MagicMock, patch, Mock
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")


@pytest.fixture
def idrac_reset_connection_mock(mocker, idrac_mock):
    idrac_connection_class_mock = mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                                               'dellemc_idrac_reset.iDRACConnection')
    idrac_connection_class_mock.return_value.__enter__.return_value = idrac_mock
    return idrac_mock


class TestReset(FakeAnsibleModule):
    module = dellemc_idrac_reset

    @pytest.fixture
    def idrac_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.config_mgr = idrac_obj
        type(idrac_obj).reset_idrac = Mock(return_value="idracreset")
        return idrac_obj

    @pytest.fixture
    def idrac_config_mngr_reset_mock(self, mocker):
        try:
            config_manager_obj = mocker.patch(
                'ansible_collections.dellemc.openmanage.plugins.modules.dellemc_idrac_reset.config_mgr')
        except AttributeError:
            config_manager_obj = MagicMock()
        obj = MagicMock()
        config_manager_obj.config_mgr.return_value = obj
        config_manager_obj.config_mgr.reset_idrac().return_value = obj
        return config_manager_obj

    def test_main_idrac_reset_success_case01(self, idrac_reset_connection_mock, idrac_default_args, mocker):
        mocker.patch("ansible_collections.dellemc.openmanage.plugins.modules.dellemc_idrac_reset.run_idrac_reset",
                     return_value=({"Status": "Success"}, False))
        idrac_reset_connection_mock.config_mgr.reset_idrac.return_value = {"Status": "Success"}
        idrac_reset_connection_mock.config_mgr.reset_idrac.return_value = "Success"
        result = self._run_module(idrac_default_args)
        assert result == {'Status': 'Success', 'changed': False}

    def test_run_idrac_reset_success_case01(self, idrac_reset_connection_mock, idrac_default_args,
                                            idrac_config_mngr_reset_mock):
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        result = self.module.run_idrac_reset(idrac_reset_connection_mock, f_module)
        assert result == ({'changed': True, 'failed': False,
                           'msg': {'Status': 'Success', 'Message': 'Changes found to commit!',
                                   'changes_applicable': True}}, False)

    def test_run_idrac_reset_Exception_fail_case01(self, idrac_reset_connection_mock, idrac_default_args,
                                         idrac_config_mngr_reset_mock):
        error_msg = "Error in Runtime"
        obj2 = MagicMock()
        idrac_reset_connection_mock.config_mgr = obj2
        type(obj2).reset_idrac = Mock(side_effect=Exception(error_msg))
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        result, err = self.module.run_idrac_reset(idrac_reset_connection_mock, f_module)
        assert result['failed'] is True
        assert result['msg'] == "Error: {0}".format(error_msg)

    def test_run_idrac_reset_status_success_case02(self, idrac_reset_connection_mock, idrac_default_args):
        msg = {"Status": "Success"}
        obj = MagicMock()
        idrac_reset_connection_mock.config_mgr = obj
        obj.reset_idrac = Mock(return_value="msg")
        f_module = self.get_module_mock(params=msg, check_mode=False)
        msg, err = self.module.run_idrac_reset(idrac_reset_connection_mock, f_module)
        assert msg == {'changed': False, 'failed': False, 'msg': {'idracreset': 'msg'}}

    def test_main_idrac_reset_failure_case(self, idrac_reset_connection_mock, idrac_default_args, mocker):
        mocker.patch("ansible_collections.dellemc.openmanage.plugins.modules.dellemc_idrac_reset.run_idrac_reset",
                     return_value=({"Status": "failed"}, True))
        msg, err = self._run_module_with_fail_json(idrac_default_args)
        assert msg == 'Status'

    @pytest.mark.parametrize("exc_type", [ImportError, ValueError, RuntimeError])
    def test_main_exception_handling_case(self, exc_type, mocker, idrac_reset_connection_mock, idrac_default_args):
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.dellemc_idrac_reset.run_idrac_reset',
            side_effect=exc_type('test'))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True
