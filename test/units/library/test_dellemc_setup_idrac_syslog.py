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
from ansible.modules.remote_management.dellemc import dellemc_setup_idrac_syslog
from units.modules.remote_management.dellemc.common import FakeAnsibleModule, Constants
from units.compat.mock import MagicMock, patch, Mock
from units.modules.utils import set_module_args, exit_json, fail_json, AnsibleFailJson, AnsibleExitJson
from units.compat.mock import PropertyMock
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")


class TestSetupSyslog(FakeAnsibleModule):
    module = dellemc_setup_idrac_syslog

    @pytest.fixture
    def idrac_setup_syslog_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.file_share_manager = idrac_obj
        omsdk_mock.config_mgr = idrac_obj
        return idrac_obj

    @pytest.fixture
    def idrac_file_manager_mock(self, mocker):
        try:
            file_manager_obj = mocker.patch(
                'ansible.modules.remote_management.dellemc.dellemc_setup_idrac_syslog.file_share_manager')
        except AttributeError:
            file_manager_obj = MagicMock()
        obj = MagicMock()
        file_manager_obj.create_share_obj.return_value = obj
        return file_manager_obj

    @pytest.fixture
    def is_changes_applicable_setup_syslog_mock(self, mocker):
        try:
            changes_applicable_mock = mocker.patch('ansible.modules.remote_management.dellemc.'
                                                   'dellemc_setup_idrac_syslog.config_mgr')
        except AttributeError:
            changes_applicable_mock = MagicMock()
        obj = MagicMock()
        changes_applicable_mock.is_change_applicable.return_value = obj
        return changes_applicable_mock

    @pytest.fixture
    def idrac_connection_setup_syslog_mock(self, mocker, idrac_setup_syslog_mock):
        idrac_conn_class_mock = mocker.patch('ansible.modules.remote_management.dellemc.dellemc_setup_idrac_syslog.'
                                             'iDRACConnection', return_value=idrac_setup_syslog_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_setup_syslog_mock
        return idrac_setup_syslog_mock

    def test_main_setup_syslog_success_case01(self,idrac_connection_setup_syslog_mock, idrac_default_args, mocker,
                                              idrac_file_manager_mock):
        idrac_default_args.update({"share_name": "sharename", 'share_password': None, "syslog": "Enabled",
        'share_mnt': None, 'share_user': None})
        message = {'changed': False, 'msg': {'Status': "Success", "message": "No changes found to commit!"}}
        mocker.patch('ansible.modules.remote_management.dellemc.dellemc_setup_idrac_syslog.run_setup_idrac_syslog',
                     return_value=(message, False))
        result = self._run_module(idrac_default_args)
        assert result == {'changed': False, 'msg': {'Status': 'Success', "message": "No changes found to commit!"}}

    def test_run_setup_idrac_syslog_success_case01(self, idrac_connection_setup_syslog_mock, idrac_default_args,
                                                   idrac_file_manager_mock, is_changes_applicable_setup_syslog_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "syslog": "Enabled", "share_password": "sharepassword"})
        message = {"changes_applicable": True, "message": "changes are applicable"}
        idrac_connection_setup_syslog_mock.config_mgr.is_change_applicable.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        msg, err = self.module.run_setup_idrac_syslog(idrac_connection_setup_syslog_mock, f_module)
        assert msg == {"changed": True, "failed": False, "msg": {"changes_applicable": True,
                                                                 "message": "changes are applicable"}}
        assert msg['changed'] is True
        assert msg['failed'] is False

    def test_run_setup_idrac_syslog_disable_success_case01(self, idrac_connection_setup_syslog_mock, idrac_default_args,
                                                   idrac_file_manager_mock, is_changes_applicable_setup_syslog_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "syslog": "Disabled", "share_password": "sharepassword"})
        message = {"changes_applicable": True, "message": "changes are applicable"}
        idrac_connection_setup_syslog_mock.config_mgr.is_change_applicable.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        msg, err = self.module.run_setup_idrac_syslog(idrac_connection_setup_syslog_mock, f_module)
        assert msg == {'changed': True, 'failed': False, 'msg': {'changes_applicable': True,
                                                                 'message': 'changes are applicable'}}

    def test_run_setup_idrac_syslog_success_case02(self, idrac_connection_setup_syslog_mock, idrac_default_args,
                                                   idrac_file_manager_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "syslog": "Enabled", "share_password": "sharepassword"})
        message = {"changes_applicable": True, "message": "changes found to commit!", "changed": True,
                   "Status": "Success"}
        idrac_connection_setup_syslog_mock.config_mgr.enable_syslog.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        msg, err = self.module.run_setup_idrac_syslog(idrac_connection_setup_syslog_mock, f_module)
        assert msg == {"changed": True, "failed": False, "msg": {"changes_applicable": True,
                                                                 "message": "changes found to commit!",
                                                                 "changed": True, "Status": "Success"}}
        assert msg['changed'] is True
        assert msg['failed'] is False

    def test_run_setup_idrac_syslog_success_case03(self, idrac_connection_setup_syslog_mock, idrac_default_args,
                                                   idrac_file_manager_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "syslog": "Enabled", "share_password": "sharepassword"})
        message = {"changes_applicable": True, "Message": "No changes found to commit!", "changed": False,
                   "Status": "Success"}
        idrac_connection_setup_syslog_mock.config_mgr.enable_syslog.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        msg, err = self.module.run_setup_idrac_syslog(idrac_connection_setup_syslog_mock, f_module)
        assert msg == {"changed": False, "failed": False, "msg": {"changes_applicable": True,
                                                                  "Message": "No changes found to commit!",
                                                                  "changed": False, "Status": "Success"}}
        assert msg['changed'] is False
        assert msg['failed'] is False

    def test_run_setup_idrac_syslog_success_case04(self, idrac_connection_setup_syslog_mock, idrac_default_args,
                                                   idrac_file_manager_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "syslog": "Disabled", "share_password": "sharepassword"})
        message = {"changes_applicable": True, "Message": "No Changes found to commit!", "changed": False,
                   "Status": "Success"}
        idrac_connection_setup_syslog_mock.config_mgr.disable_syslog.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        msg, err = self.module.run_setup_idrac_syslog(idrac_connection_setup_syslog_mock, f_module)
        assert msg == {"changed": True, "failed": False, "msg": {"changes_applicable": True,
                                                                  "Message": "No Changes found to commit!",
                                                                  "changed": False, "Status": "Success"}}
        assert msg['changed'] is True
        assert msg['failed'] is False

    def test_run_setup_syslog_disable_case(self, idrac_connection_setup_syslog_mock, idrac_default_args,
                                           idrac_file_manager_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "syslog": 'Disabled'})
        message = "Disabled"
        idrac_connection_setup_syslog_mock.config_mgr.disable_syslog.return_value = message
        idrac_connection_setup_syslog_mock.config_mgr.is_change_applicable.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        msg, err = self.module.run_setup_idrac_syslog(idrac_connection_setup_syslog_mock, f_module)
        assert msg == {'changed': False, 'failed': False, 'msg': 'Disabled'}
        assert err is False

    def test_run_setup_syslog_enable_case(self, idrac_connection_setup_syslog_mock, idrac_default_args,
                                          idrac_file_manager_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "syslog": 'Enabled'})
        message = "Enabled"
        idrac_connection_setup_syslog_mock.config_mgr.enable_syslog.return_value = message
        idrac_connection_setup_syslog_mock.config_mgr.is_change_applicable.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        msg, err = self.module.run_setup_idrac_syslog(idrac_connection_setup_syslog_mock, f_module)
        assert msg == {'changed': False, 'failed': False, 'msg': 'Enabled'}
        assert err is False

    def test_run_setup_idrac_syslog_failed_case01(self, idrac_connection_setup_syslog_mock, idrac_default_args,
                                                  idrac_file_manager_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "syslog": "Enable", "share_password": "sharepassword"})
        message = {'Status': 'Failed', "Data": {'Message': 'status failed in checking Data'}}
        idrac_connection_setup_syslog_mock.file_share_manager.create_share_obj.return_value = "mnt/iso"
        idrac_connection_setup_syslog_mock.config_mgr.set_liason_share.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        result, err = self.module.run_setup_idrac_syslog(idrac_connection_setup_syslog_mock, f_module)
        assert result == {'changed': False, 'failed': True, 'msg': 'status failed in checking Data'}

    @pytest.mark.parametrize("exc_type", [IndexError, KeyError])
    def test_run_setup_idrac_syslog_failed_indexerror_case01(self, exc_type, idrac_connection_setup_syslog_mock, idrac_default_args,
                                                  idrac_file_manager_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "syslog": "Enable", "share_password": "sharepassword"})
        message = {'Status': 'Failed', 'Message': "failed to fetch data"}
        idrac_connection_setup_syslog_mock.file_share_manager.create_share_obj.return_value = "mnt/iso"
        idrac_connection_setup_syslog_mock.config_mgr.set_liason_share.return_value = message
        idrac_connection_setup_syslog_mock.config_mgr.set_liason.side_effect = exc_type
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.run_setup_idrac_syslog(idrac_connection_setup_syslog_mock, f_module)
        assert result == ({'changed': False, 'failed': True, 'msg': 'failed to fetch data'}, True)

    def test_run_setup_idrac_syslog_failed_case03(self, idrac_connection_setup_syslog_mock, idrac_default_args,
                                                  idrac_file_manager_mock):
        idrac_default_args.update({"share_name": "dummy_share_name", "share_mnt": "mountname",
                                   "share_user": "shareuser",
                                   "syslog": "Disabled", "share_password": "sharepassword"})
        message = {"message": "No changes were applied", "changed": False,
                   "Status": "failed"}
        idrac_connection_setup_syslog_mock.config_mgr.enable_syslog.return_value = message
        idrac_connection_setup_syslog_mock.config_mgr.disable_syslog.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        msg, err = self.module.run_setup_idrac_syslog(idrac_connection_setup_syslog_mock, f_module)
        assert msg == {'msg': {"message": "No changes were applied", "changed": False,
                      "Status": "failed"}, 'failed': True, 'changed': False}
        assert msg['changed'] is False
        assert msg['failed'] is True

    def test_main_setup_syslog_failure_case(self, idrac_connection_setup_syslog_mock, idrac_default_args,
                                            idrac_file_manager_mock):
        idrac_default_args.update({"share_name": "dummy_share_name"})
        error_msg = "Error in Runtime"
        obj2 = MagicMock()
        idrac_connection_setup_syslog_mock.file_share_manager = obj2
        idrac_connection_setup_syslog_mock.config_mgr = obj2
        type(obj2).create_share_obj = Mock(side_effect=Exception(error_msg))
        type(obj2).set_liason_share = Mock(side_effect=Exception(error_msg))
        msg = self._run_module_with_fail_json(idrac_default_args)
        assert msg['failed'] is True
        assert msg['msg'] == "Error: {0}".format(error_msg)

    @pytest.mark.parametrize("exc_type", [ImportError, ValueError, RuntimeError])
    def test_main_setup_syslog_exception_handling_case(self, exc_type, mocker, idrac_connection_setup_syslog_mock,
                                                       idrac_default_args, idrac_file_manager_mock):
        idrac_default_args.update({"share_name": "sharename", 'share_password': None,
                                   "syslog": "Enabled", 'share_mnt': None, 'share_user': None})
        mocker.patch('ansible.modules.remote_management.dellemc.dellemc_setup_idrac_syslog.run_setup_idrac_syslog',
                     side_effect=exc_type('test'))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True
