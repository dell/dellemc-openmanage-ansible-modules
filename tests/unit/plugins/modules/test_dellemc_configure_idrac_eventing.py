# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.2.0
# Copyright (C) 2020-2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible_collections.dellemc.openmanage.plugins.modules import dellemc_configure_idrac_eventing
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from unittest.mock import MagicMock, Mock, PropertyMock
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from pytest import importorskip
from ansible.module_utils._text import to_text
import json
from io import StringIO

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


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
        idrac_default_args.update({"share_name": None, 'share_password': None, "destination_number": 1,
                                   "destination": "1.1.1.1", 'share_mnt': None, 'share_user': None})
        message = {'msg': 'Successfully configured the idrac eventing settings.',
                   'eventing_status': {"Id": "JID_12345123456", "JobState": "Completed"},
                   'changed': True}
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_configure_idrac_eventing.run_idrac_eventing_config', return_value=message)
        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Successfully configured the iDRAC eventing settings."
        status_msg = {"Status": "Success", "Message": "No changes found to commit!"}
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_configure_idrac_eventing.run_idrac_eventing_config', return_value=status_msg)
        result = self._run_module(idrac_default_args)
        assert result["msg"] == "No changes found to commit!"

    def test_run_idrac_eventing_config_success_case01(self, idrac_connection_configure_eventing_mock,
                                                      idrac_file_manager_config_eventing_mock, idrac_default_args,
                                                      is_changes_applicable_eventing_mock):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "destination_number": 1, "destination": "1.1.1.1",
                                   "snmp_v3_username": "snmpuser", "snmp_trap_state": "Enabled", "alert_number": 4,
                                   "email_alert_state": "Enabled", "address": "abc@xyz", "custom_message": "test",
                                   "enable_alerts": "Enabled", "authentication": "Enabled",
                                   "smtp_ip_address": "XX.XX.XX.XX", "smtp_port": 443, "username": "uname",
                                   "password": "pwd"})
        message = {"changes_applicable": True, "message": "Changes found to commit!"}
        idrac_connection_configure_eventing_mock.config_mgr.is_change_applicable.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        with pytest.raises(Exception) as ex:
            self.module.run_idrac_eventing_config(idrac_connection_configure_eventing_mock, f_module)
        assert "Changes found to commit!" == ex.value.args[0]

    def test_run_idrac_eventing_config_success_case02(self, idrac_connection_configure_eventing_mock,
                                                      idrac_file_manager_config_eventing_mock, idrac_default_args):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "destination_number": 1, "destination": "1.1.1.1",
                                   "snmp_v3_username": "snmpuser", "snmp_trap_state": "Enabled", "alert_number": 4,
                                   "email_alert_state": "Enabled", "address": "abc@xyz", "custom_message": "test",
                                   "enable_alerts": "Enabled", "authentication": "Enabled",
                                   "smtp_ip_address": "XX.XX.XX.XX", "smtp_port": 443, "username": "uname",
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
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "destination_number": 1,
                                   "destination": "1.1.1.1", "snmp_v3_username": "snmpuser",
                                   "snmp_trap_state": "Enabled", "alert_number": 4, "email_alert_state": "Enabled",
                                   "address": "abc@xyz", "custom_message": "test", "enable_alerts": "Enabled",
                                   "authentication": "Enabled", "smtp_ip_address": "XX.XX.XX.XX", "smtp_port": 443,
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
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "destination_number": 1, "destination": "1.1.1.1",
                                   "snmp_v3_username": "snmpuser", "snmp_trap_state": "Enabled", "alert_number": 4,
                                   "email_alert_state": "Enabled", "address": "abc@xyz", "custom_message": "test",
                                   "enable_alerts": "Enabled", "authentication": "Enabled",
                                   "smtp_ip_address": "XX.XX.XX.XX", "smtp_port": 443, "username": "uname",
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
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "destination_number": None, "destination": None,
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
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "destination_number": 1, "destination": "1.1.1.1",
                                   "snmp_v3_username": "snmpuser", "snmp_trap_state": "Enabled", "alert_number": 4,
                                   "email_alert_state": "Enabled", "address": "abc@xyz", "custom_message": "test",
                                   "enable_alerts": "Enabled", "authentication": "Enabled",
                                   "smtp_ip_address": "XX.XX.XX.XX", "smtp_port": 443, "username": "uname",
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
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "destination_number": 1, "destination": "1.1.1.1",
                                   "snmp_v3_username": "snmpuser", "snmp_trap_state": "Enabled", "alert_number": 4,
                                   "email_alert_state": "Enabled", "address": "abc@xyz", "custom_message": "test",
                                   "enable_alerts": "Enabled", "authentication": "Enabled",
                                   "smtp_ip_address": "XX.XX.XX.XX", "smtp_port": 443, "username": "uname",
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
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "destination_number": 1,
                                   "destination": "1.1.1.1", "snmp_v3_username": "snmpuser",
                                   "snmp_trap_state": "Enabled", "alert_number": 4, "email_alert_state": "Enabled",
                                   "address": "abc@xyz", "custom_message": "test", "enable_alerts": "Enabled",
                                   "authentication": "Enabled", "smtp_ip_address": "XX.XX.XX.XX",
                                   "smtp_port": 443, "username": "uname", "password": "pwd"})
        message = {'Status': 'Failed', "Data": {'Message': "Failed to found changes"}}
        idrac_connection_configure_eventing_mock.file_share_manager.create_share_obj.return_value = "mnt/iso"
        idrac_connection_configure_eventing_mock.config_mgr.set_liason_share.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as ex:
            self.module.run_idrac_eventing_config(idrac_connection_configure_eventing_mock, f_module)
        assert ex.value.args[0] == 'Failed to found changes'

    @pytest.mark.parametrize("exc_type", [ImportError, ValueError, RuntimeError, HTTPError, URLError, SSLValidationError, ConnectionError])
    def test_main_dellemc_configure_idrac_eventing_handling_case(self, exc_type, idrac_connection_configure_eventing_mock,
                                                                 idrac_file_manager_config_eventing_mock, idrac_default_args,
                                                                 is_changes_applicable_eventing_mock, mocker):
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH +
                         'dellemc_configure_idrac_eventing.run_idrac_eventing_config',
                         side_effect=exc_type('test'))
        else:
            mocker.patch(MODULE_PATH +
                         'dellemc_configure_idrac_eventing.run_idrac_eventing_config',
                         side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
        if exc_type != URLError:
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result

    def test_run_run_idrac_eventing_config_invalid_share(self, idrac_connection_configure_eventing_mock,
                                                         idrac_file_manager_config_eventing_mock, idrac_default_args,
                                                         is_changes_applicable_eventing_mock, mocker):
        f_module = self.get_module_mock(params=idrac_default_args)
        obj = MagicMock()
        obj.IsValid = False
        mocker.patch(
            MODULE_PATH + "dellemc_configure_idrac_eventing.file_share_manager.create_share_obj", return_value=(obj))
        with pytest.raises(Exception) as exc:
            self.module.run_idrac_eventing_config(
                idrac_connection_configure_eventing_mock, f_module)
        assert exc.value.args[0] == "Unable to access the share. Ensure that the share name, share mount, and share credentials provided are correct."

    def test_run_idrac_eventing_config_Error(self, idrac_connection_configure_eventing_mock,
                                             idrac_file_manager_config_eventing_mock, idrac_default_args,
                                             is_changes_applicable_eventing_mock, mocker):
        f_module = self.get_module_mock(params=idrac_default_args)
        obj = MagicMock()
        obj.IsValid = True
        mocker.patch(
            MODULE_PATH + "dellemc_configure_idrac_eventing.file_share_manager.create_share_obj", return_value=(obj))
        message = {'Status': 'Failed', 'Message': 'Key Error Expected', "Data1": {
            'Message': 'Status failed in checking data'}}
        idrac_connection_configure_eventing_mock.config_mgr.set_liason_share.return_value = message
        idrac_connection_configure_eventing_mock.config_mgr.apply_changes.return_value = "Returned on Key Error"
        with pytest.raises(Exception) as exc:
            self.module.run_idrac_eventing_config(
                idrac_connection_configure_eventing_mock, f_module)
        assert exc.value.args[0] == "Key Error Expected"

    def test_dellemc_configure_idrac_eventing_main_cases(self, idrac_connection_configure_eventing_mock,
                                                         idrac_file_manager_config_eventing_mock, idrac_default_args,
                                                         is_changes_applicable_eventing_mock, mocker):
        status_msg = {"Status": "Success", "Message": "No changes found"}
        mocker.patch(MODULE_PATH +
                     'dellemc_configure_idrac_eventing.run_idrac_eventing_config', return_value=status_msg)
        result = self._run_module(idrac_default_args)
        assert result['changed'] is True
        assert result['msg'] == "Successfully configured the iDRAC eventing settings."
        assert result['eventing_status'].get("Message") == "No changes found"

        status_msg = {"Status": "Failed", "Message": "No changes found"}
        mocker.patch(MODULE_PATH +
                     'dellemc_configure_idrac_eventing.run_idrac_eventing_config', return_value=status_msg)
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result['failed'] is True
        assert result['msg'] == "Failed to configure the iDRAC eventing settings"

    def test_run_idrac_eventing_config_main_cases(self, idrac_connection_configure_eventing_mock,
                                                  idrac_file_manager_config_eventing_mock, idrac_default_args,
                                                  is_changes_applicable_eventing_mock, mocker):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "destination_number": 1,
                                   "destination": None, "snmp_v3_username": None,
                                   "snmp_trap_state": None, "alert_number": 4, "email_alert_state": None,
                                   "address": None, "custom_message": None, "enable_alerts": "Enabled",
                                   "authentication": "Enabled", "smtp_ip_address": "XX.XX.XX.XX",
                                   "smtp_port": 443, "username": "uname", "password": "pwd"})

        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        obj = MagicMock()
        obj.IsValid = True
        mocker.patch(
            MODULE_PATH + "dellemc_configure_idrac_eventing.file_share_manager.create_share_obj", return_value=(obj))
        message = {'Status': 'Success', 'Message': 'Message Success', "Data": {
            'Message': 'Status failed in checking data'}}
        idrac_connection_configure_eventing_mock.config_mgr.set_liason_share.return_value = message
        idrac_connection_configure_eventing_mock.config_mgr.is_change_applicable.return_value = {
            "changes_applicable": False}
        with pytest.raises(Exception) as exc:
            self.module.run_idrac_eventing_config(
                idrac_connection_configure_eventing_mock, f_module)
        assert exc.value.args[0] == "No changes found to commit!"
