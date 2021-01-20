# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.0.0
# Copyright (C) 2020-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible_collections.dellemc.openmanage.plugins.modules import dellemc_configure_idrac_eventing
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible_collections.dellemc.openmanage.tests.unit.compat.mock import MagicMock, patch, Mock, PropertyMock
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")


class TestConfigureEventing(FakeAnsibleModule):
    module = dellemc_configure_idrac_eventing

    @pytest.fixture
    def idrac_configure_eventing_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.file_share_manager = idrac_obj
        omsdk_mock.config_mgr = idrac_obj
        type(idrac_obj).create_share_obj = Mock(return_value="Status")
        type(idrac_obj).set_liason_share = Mock(return_value="Status")
        return idrac_obj

    @pytest.fixture
    def idrac_file_manager_config_eventing_mock(self, mocker):
        try:
            file_manager_obj = mocker.patch(
                'ansible_collections.dellemc.openmanage.plugins.modules.dellemc_configure_idrac_eventing.file_share_manager')
        except AttributeError:
            file_manager_obj = MagicMock()
        obj = MagicMock()
        file_manager_obj.create_share_obj.return_value = obj
        return file_manager_obj

    @pytest.fixture
    def is_changes_applicable_eventing_mock(self, mocker):
        try:
            changes_applicable_obj = mocker.patch(
                'ansible_collections.dellemc.openmanage.plugins.modules.dellemc_configure_idrac_eventing.config_mgr')
        except AttributeError:
            changes_applicable_obj = MagicMock()
        obj = MagicMock()
        changes_applicable_obj.is_change_applicable.return_value = obj
        return changes_applicable_obj

    @pytest.fixture
    def idrac_connection_configure_eventing_mock(self, mocker, idrac_configure_eventing_mock):
        idrac_conn_class_mock = mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                                             'dellemc_configure_idrac_eventing.iDRACConnection',
                                             return_value=idrac_configure_eventing_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_configure_eventing_mock
        return idrac_configure_eventing_mock

    def test_main_configure_eventing_success_case01(self, idrac_connection_configure_eventing_mock, idrac_default_args,
                                                    mocker, idrac_file_manager_config_eventing_mock):
        idrac_default_args.update({"share_name": "sharename", 'share_password': None, "destination_number": 1,
                                   "destination": "1.1.1.1", 'share_mnt': None, 'share_user': None})
        message = {'msg': 'Successfully configured the idrac eventing settings.',
                   'eventing_status': {"Id": "JID_12345123456", "JobState": "Completed"},
                   'changed': True}
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_configure_idrac_eventing.run_idrac_eventing_config', return_value=message)
        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Successfully configured the iDRAC eventing settings."

    def test_run_idrac_eventing_config_success_case01(self, idrac_connection_configure_eventing_mock,
                                                      idrac_file_manager_config_eventing_mock, idrac_default_args,
                                                      is_changes_applicable_eventing_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "destination_number": 1, "destination": "1.1.1.1",
                                   "snmp_v3_username": "snmpuser", "snmp_trap_state": "Enabled", "alert_number": 4,
                                   "email_alert_state": "Enabled", "address": "abc@xyz", "custom_message": "test",
                                   "enable_alerts": "Enabled", "authentication": "Enabled",
                                   "smtp_ip_address": "192.168.0.1", "smtp_port": 443, "username": "uname",
                                   "password": "pwd"})
        message = {"changes_applicable": True, "message": "Changes found to commit!"}
        idrac_connection_configure_eventing_mock.config_mgr.is_change_applicable.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        with pytest.raises(Exception) as ex:
            self.module.run_idrac_eventing_config(idrac_connection_configure_eventing_mock, f_module)
        assert "Changes found to commit!" == ex.value.args[0]

    def test_run_idrac_eventing_config_success_case02(self, idrac_connection_configure_eventing_mock,
                                                      idrac_file_manager_config_eventing_mock, idrac_default_args):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "destination_number": 1, "destination": "1.1.1.1",
                                   "snmp_v3_username": "snmpuser", "snmp_trap_state": "Enabled", "alert_number": 4,
                                   "email_alert_state": "Enabled", "address": "abc@xyz", "custom_message": "test",
                                   "enable_alerts": "Enabled", "authentication": "Enabled",
                                   "smtp_ip_address": "192.168.0.1", "smtp_port": 443, "username": "uname",
                                   "password": "pwd"})
        message = {"changes_applicable": True, "message": "changes found to commit!", "changed": True,
                   "Status": "Success"}
        idrac_connection_configure_eventing_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        result = self.module.run_idrac_eventing_config(idrac_connection_configure_eventing_mock, f_module)
        assert result['message'] == 'changes found to commit!'

    def test_run_idrac_eventing_config_success_case03(self, idrac_connection_configure_eventing_mock,
                                                      idrac_file_manager_config_eventing_mock, idrac_default_args):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "destination_number": 1,
                                   "destination": "1.1.1.1", "snmp_v3_username": "snmpuser",
                                   "snmp_trap_state": "Enabled", "alert_number": 4, "email_alert_state": "Enabled",
                                   "address": "abc@xyz", "custom_message": "test", "enable_alerts": "Enabled",
                                   "authentication": "Enabled", "smtp_ip_address": "192.168.0.1", "smtp_port": 443,
                                   "username": "uname", "password": "pwd"})
        message = {"changes_applicable": False, "Message": "No changes found to commit!", "changed": False,
                   "Status": "Success"}
        idrac_connection_configure_eventing_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        result = self.module.run_idrac_eventing_config(idrac_connection_configure_eventing_mock, f_module)
        assert result["Message"] == 'No changes found to commit!'

    def test_run_idrac_eventing_config_success_case04(self, idrac_connection_configure_eventing_mock,
                                                      idrac_default_args, idrac_file_manager_config_eventing_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "destination_number": 1, "destination": "1.1.1.1",
                                   "snmp_v3_username": "snmpuser", "snmp_trap_state": "Enabled", "alert_number": 4,
                                   "email_alert_state": "Enabled", "address": "abc@xyz", "custom_message": "test",
                                   "enable_alerts": "Enabled", "authentication": "Enabled",
                                   "smtp_ip_address": "192.168.0.1", "smtp_port": 443, "username": "uname",
                                   "password": "pwd"})
        message = {"changes_applicable": False, "Message": "No changes were applied", "changed": False,
                   "Status": "Success"}
        idrac_connection_configure_eventing_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        result = self.module.run_idrac_eventing_config(idrac_connection_configure_eventing_mock, f_module)
        assert result['Message'] == 'No changes were applied'

    def test_run_idrac_eventing_config_success_case05(self, idrac_connection_configure_eventing_mock,
                                                      idrac_file_manager_config_eventing_mock, idrac_default_args):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "destination_number": None, "destination": None,
                                   "snmp_v3_username": None, "snmp_trap_state": None, "alert_number": None,
                                   "email_alert_state": None, "address": None, "custom_message": None,
                                   "enable_alerts": None, "authentication": None,
                                   "smtp_ip_address": None, "smtp_port": None, "username": None,
                                   "password": None})
        message = {"changes_applicable": False, "Message": "No changes were applied", "changed": False,
                   "Status": "Success"}
        obj = MagicMock()
        idrac_connection_configure_eventing_mock.config_mgr = obj
        type(obj).configure_snmp_trap_destination = PropertyMock(return_value=message)
        type(obj).configure_email_alerts = PropertyMock(return_value=message)
        type(obj).configure_idrac_alerts = PropertyMock(return_value=message)
        type(obj).configure_smtp_server_settings = PropertyMock(return_value=message)
        idrac_connection_configure_eventing_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        result = self.module.run_idrac_eventing_config(idrac_connection_configure_eventing_mock, f_module)
        assert result['Message'] == 'No changes were applied'

    def test_run_idrac_eventing_config_failed_case01(self, idrac_connection_configure_eventing_mock,
                                                     idrac_file_manager_config_eventing_mock, idrac_default_args):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "destination_number": 1, "destination": "1.1.1.1",
                                   "snmp_v3_username": "snmpuser", "snmp_trap_state": "Enabled", "alert_number": 4,
                                   "email_alert_state": "Enabled", "address": "abc@xyz", "custom_message": "test",
                                   "enable_alerts": "Enabled", "authentication": "Enabled",
                                   "smtp_ip_address": "192.168.0.1", "smtp_port": 443, "username": "uname",
                                   "password": "pwd"})
        message = {'Status': 'Failed', "Data": {'Message': 'status failed in checking Data'}}
        idrac_connection_configure_eventing_mock.file_share_manager.create_share_obj.return_value = "mnt/iso"
        idrac_connection_configure_eventing_mock.config_mgr.set_liason_share.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as ex:
            self.module.run_idrac_eventing_config(idrac_connection_configure_eventing_mock, f_module)
        assert ex.value.args[0] == 'status failed in checking Data'

    def test_run_idrac_eventing_config_failed_case02(self, idrac_connection_configure_eventing_mock,
                                                     idrac_default_args, idrac_file_manager_config_eventing_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "destination_number": 1, "destination": "1.1.1.1",
                                   "snmp_v3_username": "snmpuser", "snmp_trap_state": "Enabled", "alert_number": 4,
                                   "email_alert_state": "Enabled", "address": "abc@xyz", "custom_message": "test",
                                   "enable_alerts": "Enabled", "authentication": "Enabled",
                                   "smtp_ip_address": "192.168.0.1", "smtp_port": 443, "username": "uname",
                                   "password": "pwd"})
        message = {"changes_applicable": False, "Message": "No changes were applied", "changed": False,
                   "Status": "failed"}
        idrac_connection_configure_eventing_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        result = self.module.run_idrac_eventing_config(idrac_connection_configure_eventing_mock, f_module)
        assert result['Message'] == 'No changes were applied'

    def test_run_idrac_eventing_config_failed_case03(self, idrac_connection_configure_eventing_mock,
                                                     idrac_default_args, idrac_file_manager_config_eventing_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "destination_number": 1,
                                   "destination": "1.1.1.1", "snmp_v3_username": "snmpuser",
                                   "snmp_trap_state": "Enabled", "alert_number": 4, "email_alert_state": "Enabled",
                                   "address": "abc@xyz", "custom_message": "test", "enable_alerts": "Enabled",
                                   "authentication": "Enabled", "smtp_ip_address": "192.168.0.1",
                                   "smtp_port": 443, "username": "uname", "password": "pwd"})
        message = {'Status': 'Failed', "Data": {'Message': "Failed to found changes"}}
        idrac_connection_configure_eventing_mock.file_share_manager.create_share_obj.return_value = "mnt/iso"
        idrac_connection_configure_eventing_mock.config_mgr.set_liason_share.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as ex:
            self.module.run_idrac_eventing_config(idrac_connection_configure_eventing_mock, f_module)
        assert ex.value.args[0] == 'Failed to found changes'

    @pytest.mark.parametrize("exc_type", [ImportError, ValueError, RuntimeError])
    def test_main_configure_eventing_exception_handling_case(self, exc_type, mocker, idrac_default_args,
                                                             idrac_connection_configure_eventing_mock,
                                                             idrac_file_manager_config_eventing_mock):
        idrac_default_args.update({"share_name": "sharename", 'share_password': None,
                                   'share_mnt': None, 'share_user': None})
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_configure_idrac_eventing.run_idrac_eventing_config', side_effect=exc_type('test'))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True
