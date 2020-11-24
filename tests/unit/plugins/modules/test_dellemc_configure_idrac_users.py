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
from ansible_collections.dellemc.openmanage.plugins.modules import dellemc_configure_idrac_users
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible_collections.dellemc.openmanage.tests.unit.compat.mock import MagicMock, patch, Mock
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")


class TestConfigUsers(FakeAnsibleModule):
    module = dellemc_configure_idrac_users

    @pytest.fixture
    def idrac_configure_users_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.file_share_manager = idrac_obj
        omsdk_mock.config_mgr = idrac_obj
        type(idrac_obj).create_share_obj = Mock(return_value="servicesstatus")
        type(idrac_obj).set_liason_share = Mock(return_value="servicestatus")
        return idrac_obj

    @pytest.fixture
    def idrac_file_manager_config_users_mock(self, mocker):
        try:
            file_manager_obj = mocker.patch(
                'ansible_collections.dellemc.openmanage.plugins.modules.dellemc_configure_idrac_users.file_share_manager')
        except AttributeError:
            file_manager_obj = MagicMock()
        obj = MagicMock()
        file_manager_obj.create_share_obj.return_value = obj
        return file_manager_obj

    @pytest.fixture
    def is_changes_applicable_mock_users(self, mocker):
        try:
            changes_applicable_mock = mocker.patch(
                'ansible_collections.dellemc.openmanage.plugins.modules.dellemc_configure_idrac_users.config_mgr')
        except AttributeError:
            changes_applicable_mock = MagicMock()
        obj = MagicMock()
        changes_applicable_mock.is_change_applicable.return_value = obj
        return changes_applicable_mock

    @pytest.fixture
    def idrac_connection_configure_users_mock(self, mocker, idrac_configure_users_mock):
        idrac_conn_class_mock = mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                                             'dellemc_configure_idrac_users.iDRACConnection',
                                             return_value=idrac_configure_users_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_configure_users_mock
        return idrac_configure_users_mock

    def test_main_idrac_users_config_success_Case(self, idrac_connection_configure_users_mock, idrac_default_args,
                                                  mocker, idrac_file_manager_config_users_mock):
        idrac_default_args.update({"share_name": "sharename"})
        message = {'changed': False, 'msg': {'Status': "Success", "message": "No changes found to commit!"}}
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_configure_idrac_users.run_idrac_users_config', return_value=(message, False))
        result = self._run_module(idrac_default_args)
        assert result == {'changed': False, 'msg': {'Status': 'Success', "message": "No changes found to commit!"}}

    def test_run_idrac_users_config_success_case01(self, idrac_connection_configure_users_mock,
                                                   idrac_default_args, idrac_file_manager_config_users_mock,
                                                   is_changes_applicable_mock_users):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "enable_users": "Enabled",
                                   "solenable_users": "Enabled", "protocolenable_users": "Enabled",
                                   "privilege_users": "Administrator", "ipmilanprivilege_users": "Administrator",
                                   "ipmiserialprivilege_users": "Administrator",
                                   "authenticationprotocol_users": "SHA",
                                   "privacyprotocol_users": "AES", "action": "test"})
        message = {"changes_applicable": True, "message": "changes are applicable"}
        idrac_connection_configure_users_mock.config_mgr.is_change_applicable.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        msg, err = self.module.run_idrac_users_config(idrac_connection_configure_users_mock, f_module)
        assert msg == {"changed": True, "failed": False, "msg": {"changes_applicable": True,
                                                                 "message": "changes are applicable"}}
        assert msg['changed'] is True
        assert msg['failed'] is False

    def test_run_idrac_users_config_success_case02(self, idrac_connection_configure_users_mock, idrac_default_args,
                                                   idrac_file_manager_config_users_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "enable_users": "Enabled",
                                   "solenable_users": "Enabled", "protocolenable_users": "Enabled",
                                   "privilege_users": "Administrator", "ipmilanprivilege_users": "Administrator",
                                   "ipmiserialprivilege_users": "Administrator",
                                   "authenticationprotocol_users": "SHA",
                                   "privacyprotocol_users": "AES", "action": "test"})
        message = {"changes_applicable": True, "message": "changes found to commit!", "changed": True,
                   "Status": "Success"}
        idrac_connection_configure_users_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg, err = self.module.run_idrac_users_config(idrac_connection_configure_users_mock, f_module)
        assert msg == {'msg': {'Status': 'Success', 'message': 'changes found to commit!', 'changed': True,
                               'changes_applicable': True}, 'failed': False, 'changed': True}
        assert msg['changed'] is True
        assert msg['failed'] is False

    def test_run_idrac_users_config_success_case03(self, idrac_connection_configure_users_mock, idrac_default_args,
                                                   idrac_file_manager_config_users_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "enable_users": "Enabled",
                                   "solenable_users": "Enabled", "protocolenable_users": "Enabled",
                                   "privilege_users": "Administrator", "ipmilanprivilege_users": "Administrator",
                                   "ipmiserialprivilege_users": "Administrator",
                                   "authenticationprotocol_users": "SHA",
                                   "privacyprotocol_users": "AES", "action": "test"})
        message = {"changes_applicable": False, "Message": "No changes found to commit!", "changed": False,
                   "Status": "Success"}
        idrac_connection_configure_users_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg, err = self.module.run_idrac_users_config(idrac_connection_configure_users_mock, f_module)
        assert msg == {'msg': {'Status': 'Success', 'Message': 'No changes found to commit!', 'changed': False,
                               'changes_applicable': False}, 'failed': False, 'changed': False}
        assert msg['changed'] is False
        assert msg['failed'] is False

    def test_run_idrac_users_config_create_success_case04(self, idrac_connection_configure_users_mock,
                                                          idrac_default_args, idrac_file_manager_config_users_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "enable_users": "Enabled",
                                   "solenable_users": "Enabled", "protocolenable_users": "Enabled",
                                   "privilege_users": "Administrator", "ipmilanprivilege_users": "Administrator",
                                   "ipmiserialprivilege_users": "Administrator",
                                   "authenticationprotocol_users": "SHA",
                                   "privacyprotocol_users": "AES", "action": "create", "user_name": "username",
                                   "user_password": "userpassword"})
        message = {"changes_applicable": False, "Message": 'No changes found to commit', "changed": False,
                   "Status": "Success"}
        idrac_connection_configure_users_mock.config_mgr._sysconfig.iDRAC.Users.find_first.return_value = message
        idrac_connection_configure_users_mock.user_mgr.Users.new.return_value = {
            "user_name": "username", "user_password": "userpassword", "enable_users": "Enabled",
            "solenable_users": "Enabled", "protocolenable_users": "Enabled", "privilege_users": "Administrator",
            "ipmilanprivilege_users": "Administrator", "ipmiserialprivilege_users": "Administrator",
            "authenticationprotocol_users": "SHA", "privacyprotocol_users": "AES", "action": "create"}
        idrac_connection_configure_users_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg, err = self.module.run_idrac_users_config(idrac_connection_configure_users_mock, f_module)
        assert msg == {'msg': {'Status': 'Success', 'Message': "No changes found to commit", 'changed': False,
                               'changes_applicable': False}, 'failed': False, 'changed': True}
        assert msg['changed'] is True
        assert msg['failed'] is False

    def test_run_idrac_users_config_create_checkmode_success_case04(self, idrac_connection_configure_users_mock,
                                                                    idrac_default_args,
                                                                    idrac_file_manager_config_users_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "enable_users": "Enabled",
                                   "solenable_users": "Enabled", "protocolenable_users": "Enabled",
                                   "privilege_users": "Administrator", "ipmilanprivilege_users": "Administrator",
                                   "ipmiserialprivilege_users": "Administrator",
                                   "authenticationprotocol_users": "SHA",
                                   "privacyprotocol_users": "AES", "action": "create", "user_name": "username",
                                   "user_password": "userpassword"})
        message = {'Status': 'Success', 'Message': 'No changes found to commit', 'changes_applicable': False}
        idrac_connection_configure_users_mock.config_mgr._sysconfig.iDRAC.Users.find_first.return_value = message
        idrac_connection_configure_users_mock.user_mgr.Users.new.return_value = {
            "user_name": "username", "user_password": "userpassword", "enable_users": "Enabled",
            "solenable_users": "Enabled", "protocolenable_users": "Enabled", "privilege_users": "Administrator",
            "ipmilanprivilege_users": "Administrator", "ipmiserialprivilege_users": "Administrator",
            "authenticationprotocol_users": "SHA", "privacyprotocol_users": "AES", "action": "create"}
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = True
        msg, err = self.module.run_idrac_users_config(idrac_connection_configure_users_mock, f_module)
        assert msg == {'msg': {'Status': 'Success', 'Message': 'No changes found to commit', 'changes_applicable': False},
                       'failed': False, 'changed': False}
        assert msg['changed'] is False
        assert msg['failed'] is False

    def test_run_idrac_users_config_modify_success_case05(self, idrac_connection_configure_users_mock,
                                                          idrac_default_args, idrac_file_manager_config_users_mock,
                                                          is_changes_applicable_mock_users):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "enable_users": "Enabled",
                                   "solenable_users": "Enabled", "protocolenable_users": "Enabled",
                                   "privilege_users": "Administrator", "ipmilanprivilege_users": "Administrator",
                                   "ipmiserialprivilege_users": "Administrator",
                                   "authenticationprotocol_users": "SHA",
                                   "privacyprotocol_users": "AES", "action": "modify", "user_name": None,
                                   "user_password": "password"})
        message = {"changes_applicable": False, "Message": "No changes found to commit!", "changed": False,
                   "Status": "Success"}
        idrac_connection_configure_users_mock.config_mgr.is_change_applicable.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        msg, err = self.module.run_idrac_users_config(idrac_connection_configure_users_mock, f_module)
        assert msg == {'msg': {'Status': 'Success', 'Message': 'No changes found to commit!', 'changed': False,
                               'changes_applicable': False}, 'failed': False, 'changed': False}
        assert msg['failed'] is False
        assert err is False

    def test_run_idrac_users_config_delete_success_case06(self, idrac_connection_configure_users_mock,
                                                          idrac_default_args, idrac_file_manager_config_users_mock,
                                                          is_changes_applicable_mock_users):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "enable_users": "Enabled",
                                   "solenable_users": "Enabled", "protocolenable_users": "Enabled",
                                   "privilege_users": "Administrator", "ipmilanprivilege_users": "Administrator",
                                   "ipmiserialprivilege_users": "Administrator",
                                   "authenticationprotocol_users": "SHA",
                                   "privacyprotocol_users": "AES", "action": "delete", "user_name": "username",
                                   "user_password": "userpassword"})
        message = {"changes_applicable": False, "Message": "No changes found to commit", "changed": False,
                   "Status": "Success"}
        idrac_connection_configure_users_mock.user_mgr.Users.remove.return_value = message
        idrac_connection_configure_users_mock.config_mgr.is_change_applicable.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        msg, err = self.module.run_idrac_users_config(idrac_connection_configure_users_mock, f_module)
        assert msg == {'msg': {'Status': 'Success', 'Message': "No changes found to commit", 'changed': False,
                               'changes_applicable': False}, 'failed': False, 'changed': False}
        assert msg['changed'] is False
        assert msg['failed'] is False

    def test_run_idrac_users_config_modify_Nonevalue_success_case05(self, idrac_connection_configure_users_mock,
                                                                    idrac_default_args,
                                                                    idrac_file_manager_config_users_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "enable_users": None,
                                   "solenable_users": None, "protocolenable_users": None,
                                   "privilege_users": None, "ipmilanprivilege_users": None,
                                   "ipmiserialprivilege_users": None,
                                   "authenticationprotocol_users": None,
                                   "privacyprotocol_users": None, "action": "modify", "user_name": None,
                                   "user_password": None})
        message = {"changes_applicable": False, "Message": "No changes found to commit!", "changed": False,
                   "Status": "Success"}
        idrac_connection_configure_users_mock.config_mgr.is_change_applicable.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        msg, err = self.module.run_idrac_users_config(idrac_connection_configure_users_mock, f_module)
        assert msg == {'msg': {'Status': 'Success', 'Message': 'No changes found to commit!', 'changed': False,
                               'changes_applicable': False}, 'failed': False, 'changed': False}
        assert msg['failed'] is False
        assert err is False

    def test_run_idrac_users_config_failed_case01(self, idrac_connection_configure_users_mock, idrac_default_args,
                                                  idrac_file_manager_config_users_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "enable_users": "Enabled",
                                   "solenable_users": "Enabled", "protocolenable_users": "Enabled",
                                   "privilege_users": "Administrator", "ipmilanprivilege_users": "Administrator",
                                   "ipmiserialprivilege_users": "Administrator",
                                   "authenticationprotocol_users": "SHA",
                                   "privacyprotocol_users": "AES", "action": "test"})
        message = {'Status': 'Failed', "Data": {'Message': 'status failed in checking Data'}}
        idrac_connection_configure_users_mock.file_share_manager.create_share_obj.return_value = "mnt/iso"
        idrac_connection_configure_users_mock.config_mgr.set_liason_share.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        result, err = self.module.run_idrac_users_config(idrac_connection_configure_users_mock, f_module)
        assert result == {'msg': 'status failed in checking Data', 'failed': True, 'changed': False}
        assert err is True

    def test_run_idrac_users_config_failed_case02(self, idrac_connection_configure_users_mock,
                                                  idrac_default_args, idrac_file_manager_config_users_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "enable_users": "Enabled",
                                   "solenable_users": "Enabled", "protocolenable_users": "Enabled",
                                   "privilege_users": "Administrator", "ipmilanprivilege_users": "Administrator",
                                   "ipmiserialprivilege_users": "Administrator",
                                   "authenticationprotocol_users": "SHA",
                                   "privacyprotocol_users": "AES", "action": "test"})
        message = {"changes_applicable": False, "Message": "No changes were applied", "changed": False,
                   "Status": "failed"}
        idrac_connection_configure_users_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg, err = self.module.run_idrac_users_config(idrac_connection_configure_users_mock, f_module)
        assert msg == {'msg': {'Status': 'failed', 'Message': 'No changes were applied', 'changed': False,
                               'changes_applicable': False}, 'failed': True, 'changed': False}
        assert msg['changed'] is False
        assert msg['failed'] is True

    def test_run_idrac_users_config_failed_case03(self, idrac_connection_configure_users_mock,
                                                  idrac_default_args, idrac_file_manager_config_users_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "enable_users": "Enabled",
                                   "solenable_users": "Enabled", "protocolenable_users": "Enabled",
                                   "privilege_users": "Administrator", "ipmilanprivilege_users": "Administrator",
                                   "ipmiserialprivilege_users": "Administrator",
                                   "authenticationprotocol_users": "SHA",
                                   "privacyprotocol_users": "AES", "action": "test"})
        message = {'Status': 'Failed', "Data": {'Message': "Failed to found changes"}}
        idrac_connection_configure_users_mock.file_share_manager.create_share_obj.return_value = "mnt/iso"
        idrac_connection_configure_users_mock.config_mgr.set_liason_share.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        msg, err = self.module.run_idrac_users_config(idrac_connection_configure_users_mock, f_module)
        assert msg == {'changed': False, 'failed': True, 'msg': 'Failed to found changes'}
        assert msg['changed'] is False
        assert msg['failed'] is True
        assert err is True

    def test_main_configure_users_failure_case(self, idrac_connection_configure_users_mock, idrac_default_args,
                                               idrac_file_manager_config_users_mock):
        idrac_default_args.update({"share_name": "sharename"})
        error_msg = "Error in Runtime"
        obj2 = MagicMock()
        idrac_connection_configure_users_mock.file_share_manager = obj2
        idrac_connection_configure_users_mock.config_mgr = obj2
        type(obj2).create_share_obj = Mock(side_effect=Exception(error_msg))
        type(obj2).set_liason_share = Mock(side_effect=Exception(error_msg))
        msg = self._run_module_with_fail_json(idrac_default_args)
        assert msg['failed'] is True
        assert msg['msg'] == "Error: {0}".format(error_msg)

    @pytest.mark.parametrize("exc_type", [ImportError, ValueError, RuntimeError])
    def test_main_idrac_configure_users_exception_handling_case(self, exc_type, mocker,
                                                                idrac_connection_configure_users_mock,
                                                                idrac_default_args,
                                                                idrac_file_manager_config_users_mock):
        idrac_default_args.update({"share_name": "sharename"})
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_configure_idrac_users.run_idrac_users_config', side_effect=exc_type('test'))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True
