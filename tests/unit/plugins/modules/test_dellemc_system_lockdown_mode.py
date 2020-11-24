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
from ansible_collections.dellemc.openmanage.plugins.modules import dellemc_system_lockdown_mode
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible_collections.dellemc.openmanage.tests.unit.compat.mock import MagicMock, Mock
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")


class TestSysytemLockdownMode(FakeAnsibleModule):
    module = dellemc_system_lockdown_mode

    @pytest.fixture
    def idrac_system_lockdown_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.file_share_manager = idrac_obj
        omsdk_mock.config_mgr = idrac_obj
        return idrac_obj

    @pytest.fixture
    def idrac_file_manager_system_lockdown_mock(self, mocker):
        try:
            file_manager_obj = mocker.patch(
                'ansible_collections.dellemc.openmanage.plugins.modules.dellemc_system_lockdown_mode.file_share_manager')
        except AttributeError:
            file_manager_obj = MagicMock()
        obj = MagicMock()
        file_manager_obj.create_share_obj.return_value = obj
        return file_manager_obj

    @pytest.fixture
    def idrac_connection_system_lockdown_mode_mock(self, mocker, idrac_system_lockdown_mock):
        idrac_conn_class_mock = mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                                             'dellemc_system_lockdown_mode.iDRACConnection',
                                             return_value=idrac_system_lockdown_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_system_lockdown_mock
        return idrac_system_lockdown_mock

    def test_main_system_lockdown_mode_success_case01(self, idrac_connection_system_lockdown_mode_mock, mocker,
                                                      idrac_file_manager_system_lockdown_mock, idrac_default_args):
        idrac_default_args.update({"share_name": "dummy_share_name", "share_password": "dummy_share_password",
                                   "lockdown_mode": "Enabled"})
        message = {"Status": "Success"}
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.dellemc_system_lockdown_mode.run_system_lockdown_mode',
                     return_value=(message, False))
        idrac_connection_system_lockdown_mode_mock.config_mgr.set_liason_share.return_value = {"Status": "Success"}
        result = self._run_module(idrac_default_args)
        assert result == {'Status': 'Success', 'changed': False}

    def test_main_system_lockdown_mode_fail_case(self, idrac_connection_system_lockdown_mode_mock, mocker,
                                                 idrac_file_manager_system_lockdown_mock, idrac_default_args):
        idrac_default_args.update({"share_name": "dummy_share_name", "share_password": "dummy_share_password",
                                   "lockdown_mode": "Enabled"})
        message = {"Status": "Failed"}
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.dellemc_system_lockdown_mode.run_system_lockdown_mode',
                     return_value=(message, True))
        idrac_connection_system_lockdown_mode_mock.config_mgr.set_liason_share.return_value = {"Status": "Failed"}
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result == {'Status': 'Failed', 'failed': True}

    @pytest.mark.parametrize("exc_type", [ImportError, ValueError, RuntimeError])
    def test_main_exception_handling_case(self, exc_type, mocker, idrac_connection_system_lockdown_mode_mock,
                                          idrac_file_manager_system_lockdown_mock, idrac_default_args):
        idrac_default_args.update({"share_name": "dummy_share_name", "share_password": "dummy_share_password",
                                   "lockdown_mode": "Enabled"})
        idrac_connection_system_lockdown_mode_mock.config_mgr.set_liason_share.return_value = {"Status": "Failed"}
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.dellemc_system_lockdown_mode.run_system_lockdown_mode',
                     side_effect=exc_type('test'))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True

    def test_run_system_lockdown_mode_success_case01(self, idrac_connection_system_lockdown_mode_mock, mocker,
                                                     idrac_file_manager_system_lockdown_mock, idrac_default_args):
        idrac_default_args.update({"share_name": "dummy_share_name", "share_password": "dummy_share_password",
                                   "lockdown_mode": "Enabled", "share_mnt": "sharemnt", "share_user": "sharuser"})
        message = {"Status": "Success"}
        idrac_connection_system_lockdown_mode_mock.config_mgr.set_liason_share.return_value = message
        idrac_connection_system_lockdown_mode_mock.config_mgr.enable_system_lockdown.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        msg, err = self.module.run_system_lockdown_mode(idrac_connection_system_lockdown_mode_mock, f_module)
        assert msg == {'msg': {'Status': 'Success'}, 'failed': False, 'changed': True}
        assert err is False

    def test_run_system_lockdown_mode_failed_case01(self, idrac_connection_system_lockdown_mode_mock, mocker,
                                                    idrac_file_manager_system_lockdown_mock, idrac_default_args):
        idrac_default_args.update({"share_name": "dummy_share_name", "share_password": "dummy_share_password",
                                   "lockdown_mode": "Disabled", "share_mnt": "sharemnt", "share_user": "sharuser"})
        message = {"Status": "failed"}
        idrac_connection_system_lockdown_mode_mock.config_mgr.set_liason_share.return_value = message
        idrac_connection_system_lockdown_mode_mock.config_mgr.disable_system_lockdown.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        msg, err = self.module.run_system_lockdown_mode(idrac_connection_system_lockdown_mode_mock, f_module)
        assert msg == {'changed': False, 'failed': True, 'msg': {'Status': 'failed'}}

    def test_run_system_lockdown_mode_failed_case02(self, idrac_connection_system_lockdown_mode_mock, mocker,
                                                    idrac_file_manager_system_lockdown_mock, idrac_default_args):
        idrac_default_args.update({"share_name": "dummy_share_name", "share_password": "dummy_share_password",
                                   "lockdown_mode": "Enabled", "share_mnt": "sharemnt", "share_user": "sharuser"})
        message = {"Status": "Failed", "Message": "message inside data"}
        idrac_connection_system_lockdown_mode_mock.config_mgr.set_liason_share.return_value = message
        idrac_connection_system_lockdown_mode_mock.config_mgr.enable_system_lockdown.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        msg, err = self.module.run_system_lockdown_mode(idrac_connection_system_lockdown_mode_mock, f_module)
        assert msg == {'changed': False, 'failed': True, 'msg': 'message inside data'}
        assert err is True

    def test_run_system_lock_down_mode_exception_case01(self, idrac_connection_system_lockdown_mode_mock,
                                                        idrac_default_args, idrac_file_manager_system_lockdown_mock):
        idrac_default_args.update({"share_name": "dummy_share_name", "share_password": "dummy_share_password",
                                   "lockdown_mode": "Enabled", "share_mnt": "sharemnt", "share_user": "sharuser"})
        error_msg = "Error in Runtime"
        obj2 = MagicMock()
        idrac_connection_system_lockdown_mode_mock.config_mgr = obj2
        type(obj2).set_liason_share = Mock(side_effect=Exception(error_msg))
        f_module = self.get_module_mock(params=idrac_default_args)
        result, err = self.module.run_system_lockdown_mode(idrac_connection_system_lockdown_mode_mock, f_module)
        assert result['failed'] is True
        assert result['msg'] == "Error: {0}".format(error_msg)
