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
from ansible_collections.dellemc.openmanage.plugins.modules import dellemc_configure_idrac_services
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from unittest.mock import MagicMock, Mock
from pytest import importorskip
from ansible.module_utils._text import to_text
import json
from io import StringIO

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestConfigServices(FakeAnsibleModule):
    module = dellemc_configure_idrac_services

    @pytest.fixture
    def idrac_configure_services_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.file_share_manager = idrac_obj
        omsdk_mock.config_mgr = idrac_obj
        type(idrac_obj).create_share_obj = Mock(return_value="servicesstatus")
        type(idrac_obj).set_liason_share = Mock(return_value="servicestatus")
        return idrac_obj

    @pytest.fixture
    def idrac_file_manager_config_services_mock(self, mocker):
        try:
            file_manager_obj = mocker.patch(
                'ansible_collections.dellemc.openmanage.plugins.modules.dellemc_configure_idrac_services.file_share_manager')
        except AttributeError:
            file_manager_obj = MagicMock()
        obj = MagicMock()
        file_manager_obj.create_share_obj.return_value = obj
        return file_manager_obj

    @pytest.fixture
    def is_changes_applicable_mock_services(self, mocker):
        try:
            changes_applicable_mock = mocker.patch(
                'ansible_collections.dellemc.openmanage.plugins.modules.dellemc_configure_idrac_services.'
                'config_mgr')
        except AttributeError:
            changes_applicable_mock = MagicMock()
        obj = MagicMock()
        changes_applicable_mock.is_change_applicable.return_value = obj
        return changes_applicable_mock

    @pytest.fixture
    def idrac_connection_configure_services_mock(self, mocker, idrac_configure_services_mock):
        idrac_conn_class_mock = mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                                             'dellemc_configure_idrac_services.iDRACConnection',
                                             return_value=idrac_configure_services_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_configure_services_mock
        return idrac_configure_services_mock

    def test_main_idrac_services_config_success_Case(self, idrac_connection_configure_services_mock, idrac_default_args,
                                                     mocker, idrac_file_manager_config_services_mock):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "enable_web_server": "Enabled", "http_port": 443,
                                   "https_port": 343, "timeout": 10, "ssl_encryption": "T_128_Bit_or_higher",
                                   "tls_protocol": "TLS_1_1_and_Higher", "snmp_enable": "Enabled",
                                   "community_name": "communityname", "snmp_protocol": "All", "alert_port": 445,
                                   "discovery_port": 1000, "trap_format": "SNMPv1",
                                   "ipmi_lan": {"community_name": "public"}})
        message = {'changed': False, 'msg': {'Status': "Success", "message": "No changes found to commit!"}}
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_configure_idrac_services.run_idrac_services_config', return_value=message)
        with pytest.raises(Exception) as ex:
            self._run_module(idrac_default_args)
        assert ex.value.args[0]['msg'] == "Failed to configure the iDRAC services."
        status_msg = {"Status": "Success", "Message": "No changes found to commit!"}
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_configure_idrac_services.run_idrac_services_config', return_value=status_msg)
        result = self._run_module(idrac_default_args)
        assert result["msg"] == "No changes found to commit!"
        status_msg = {"Status": "Failed"}
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_configure_idrac_services.run_idrac_services_config', return_value=status_msg)
        with pytest.raises(Exception) as ex:
            self._run_module(idrac_default_args)
        assert ex.value.args[0]['msg'] == "Failed to configure the iDRAC services."

    def test_run_idrac_services_config_success_case01(self, idrac_connection_configure_services_mock,
                                                      idrac_default_args, idrac_file_manager_config_services_mock,
                                                      is_changes_applicable_mock_services):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "enable_web_server": "Enabled", "http_port": 443,
                                   "https_port": 343, "timeout": 10, "ssl_encryption": "T_128_Bit_or_higher",
                                   "tls_protocol": "TLS_1_1_and_Higher", "snmp_enable": "Enabled",
                                   "community_name": "communityname", "snmp_protocol": "All", "alert_port": 445,
                                   "discovery_port": 1000, "trap_format": "SNMPv1",
                                   "ipmi_lan": {"community_name": "public"}})
        message = {"changes_applicable": True, "message": "changes are applicable"}
        idrac_connection_configure_services_mock.config_mgr.is_change_applicable.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        with pytest.raises(Exception) as ex:
            self.module.run_idrac_services_config(idrac_connection_configure_services_mock, f_module)
        assert ex.value.args[0] == "Changes found to commit!"

    def test_run_idrac_services_config_success_case02(self, idrac_connection_configure_services_mock,
                                                      idrac_default_args, idrac_file_manager_config_services_mock):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "enable_web_server": "Enabled", "http_port": 443,
                                   "https_port": 343, "timeout": 10, "ssl_encryption": "T_128_Bit_or_higher",
                                   "tls_protocol": "TLS_1_1_and_Higher", "snmp_enable": "Enabled",
                                   "community_name": "communityname", "snmp_protocol": "All", "alert_port": 445,
                                   "discovery_port": 1000, "trap_format": "SNMPv1",
                                   "ipmi_lan": {"community_name": "public"}})
        message = {"changes_applicable": True, "message": "changes found to commit!",
                   "Status": "Success"}
        idrac_connection_configure_services_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_idrac_services_config(idrac_connection_configure_services_mock, f_module)
        assert msg == {'changes_applicable': True, 'message': 'changes found to commit!', 'Status': 'Success'}

    def test_run_idrac_services_config_success_case03(self, idrac_connection_configure_services_mock,
                                                      idrac_default_args, idrac_file_manager_config_services_mock):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "enable_web_server": "Enabled", "http_port": 443,
                                   "https_port": 343, "timeout": 10, "ssl_encryption": "T_128_Bit_or_higher",
                                   "tls_protocol": "TLS_1_1_and_Higher", "snmp_enable": "Enabled",
                                   "community_name": "communityname", "snmp_protocol": "All", "alert_port": 445,
                                   "discovery_port": 1000, "trap_format": "SNMPv1",
                                   "ipmi_lan": {"community_name": "public"}})
        message = {"changes_applicable": False, "Message": "No changes found to commit!", "changed": False,
                   "Status": "Success"}
        idrac_connection_configure_services_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_idrac_services_config(idrac_connection_configure_services_mock, f_module)
        assert msg == {'changes_applicable': False, 'Message': 'No changes found to commit!',
                       'changed': False, 'Status': 'Success'}

    def test_run_idrac_services_config_success_case04(self, idrac_connection_configure_services_mock,
                                                      idrac_default_args, idrac_file_manager_config_services_mock):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "enable_web_server": "Enabled", "http_port": 443,
                                   "https_port": 343, "timeout": 10, "ssl_encryption": "T_128_Bit_or_higher",
                                   "tls_protocol": "TLS_1_1_and_Higher", "snmp_enable": "Enabled",
                                   "community_name": "communityname", "snmp_protocol": "All", "alert_port": 445,
                                   "discovery_port": 1000, "trap_format": "SNMPv1",
                                   "ipmi_lan": {"community_name": "public"}})
        message = {"changes_applicable": False, "Message": "No changes found to commit!", "changed": False,
                   "Status": "Success"}
        idrac_connection_configure_services_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_idrac_services_config(idrac_connection_configure_services_mock, f_module)
        assert msg == {'changes_applicable': False, 'Message': 'No changes found to commit!',
                       'changed': False, 'Status': 'Success'}

    def test_run_idrac_services_config_success_case05(self, idrac_connection_configure_services_mock,
                                                      idrac_default_args, idrac_file_manager_config_services_mock):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "enable_web_server": None, "http_port": None,
                                   "https_port": None, "timeout": None, "ssl_encryption": None,
                                   "tls_protocol": None, "snmp_enable": None,
                                   "community_name": None, "snmp_protocol": None, "alert_port": None,
                                   "discovery_port": None, "trap_format": None,
                                   "ipmi_lan": {"community_name": "public"}})
        message = {"changes_applicable": False, "Message": "No changes found to commit!", "changed": False,
                   "Status": "Success"}
        idrac_connection_configure_services_mock.config_mgr.configure_web_server.return_value = message
        idrac_connection_configure_services_mock.config_mgr.configure_snmp.return_value = message
        idrac_connection_configure_services_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_idrac_services_config(idrac_connection_configure_services_mock, f_module)
        assert msg == {'changes_applicable': False, 'Message': 'No changes found to commit!',
                       'changed': False, 'Status': 'Success'}

    def test_run_idrac_services_config_failed_case01(self, idrac_connection_configure_services_mock,
                                                     idrac_default_args, idrac_file_manager_config_services_mock):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "enable_web_server": "Enabled", "http_port": 443,
                                   "https_port": 343, "timeout": 10, "ssl_encryption": "T_128_Bit_or_higher",
                                   "tls_protocol": "TLS_1_1_and_Higher", "snmp_enable": "Enabled",
                                   "community_name": "communityname", "snmp_protocol": "All", "alert_port": 445,
                                   "discovery_port": 1000, "trap_format": "SNMPv1"})
        message = {'Status': 'Failed', "Data": {'Message': 'status failed in checking Data'}}
        idrac_connection_configure_services_mock.file_share_manager.create_share_obj.return_value = "mnt/iso"
        idrac_connection_configure_services_mock.config_mgr.set_liason_share.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as ex:
            self.module.run_idrac_services_config(idrac_connection_configure_services_mock, f_module)
        assert ex.value.args[0] == 'status failed in checking Data'

    def test_run_idrac_services_config_failed_case02(self, idrac_connection_configure_services_mock,
                                                     idrac_default_args, idrac_file_manager_config_services_mock):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "enable_web_server": "Enabled", "http_port": 443,
                                   "https_port": 343, "timeout": 10, "ssl_encryption": "T_128_Bit_or_higher",
                                   "tls_protocol": "TLS_1_1_and_Higher", "snmp_enable": "Enabled",
                                   "community_name": "communityname", "snmp_protocol": "All", "alert_port": 445,
                                   "discovery_port": 1000, "trap_format": "SNMPv1",
                                   "ipmi_lan": {"community_name": "public"}})
        message = {"changes_applicable": False, "Message": "No changes were applied", "changed": False,
                   "Status": "failed"}
        idrac_connection_configure_services_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_idrac_services_config(idrac_connection_configure_services_mock, f_module)
        assert msg == {'changes_applicable': False, 'Message': 'No changes were applied',
                       'changed': False, 'Status': 'failed'}

    def test_run_idrac_services_config_failed_case03(self, idrac_connection_configure_services_mock,
                                                     idrac_default_args, idrac_file_manager_config_services_mock):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "enable_web_server": "Enabled", "http_port": 443,
                                   "https_port": 343, "timeout": 10, "ssl_encryption": "T_128_Bit_or_higher",
                                   "tls_protocol": "TLS_1_1_and_Higher", "snmp_enable": "Enabled",
                                   "community_name": "communityname", "snmp_protocol": "All", "alert_port": 445,
                                   "discovery_port": 1000, "trap_format": "SNMPv1"})
        message = {'Status': 'Failed', "Data": {'Message': "Failed to found changes"}}
        idrac_connection_configure_services_mock.file_share_manager.create_share_obj.return_value = "mnt/iso"
        idrac_connection_configure_services_mock.config_mgr.set_liason_share.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as ex:
            self.module.run_idrac_services_config(idrac_connection_configure_services_mock, f_module)
        assert ex.value.args[0] == "Failed to found changes"

    def test_main_idrac_configure_fail_case(self, mocker, idrac_default_args, idrac_connection_configure_services_mock,
                                            idrac_file_manager_config_services_mock):
        idrac_default_args.update({"share_name": None})
        message = {'changed': False, 'msg': {'Status': "failed", "message": "No changes found to commit!"}}
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_configure_idrac_services.run_idrac_services_config', return_value=message)
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result['failed'] is True

    @pytest.mark.parametrize("exc_type", [ImportError, ValueError, RuntimeError, HTTPError, URLError, SSLValidationError, ConnectionError])
    def test_main_dellemc_configure_idrac_services_handling_case(self, exc_type, mocker, idrac_default_args, idrac_connection_configure_services_mock,
                                                                 idrac_file_manager_config_services_mock):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "enable_web_server": "Enabled", "http_port": 443,
                                   "https_port": 343, "timeout": 10, "ssl_encryption": "T_128_Bit_or_higher",
                                   "tls_protocol": "TLS_1_1_and_Higher", "snmp_enable": "Enabled",
                                   "community_name": "communityname", "snmp_protocol": "All", "alert_port": 445,
                                   "discovery_port": 1000, "trap_format": "SNMPv1"})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH +
                         'dellemc_configure_idrac_services.run_idrac_services_config',
                         side_effect=exc_type('test'))
        else:
            mocker.patch(MODULE_PATH +
                         'dellemc_configure_idrac_services.run_idrac_services_config',
                         side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
        if exc_type != URLError:
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result

    def test_run_idrac_services_config_invalid_share(self, mocker, idrac_default_args, idrac_connection_configure_services_mock,
                                                     idrac_file_manager_config_services_mock):
        f_module = self.get_module_mock(params=idrac_default_args)
        obj = MagicMock()
        obj.IsValid = False
        mocker.patch(
            MODULE_PATH + "dellemc_configure_idrac_services.file_share_manager.create_share_obj", return_value=(obj))
        with pytest.raises(Exception) as exc:
            self.module.run_idrac_services_config(idrac_connection_configure_services_mock, f_module)
        assert exc.value.args[0] == "Unable to access the share. Ensure that the share name, share mount, and share credentials provided are correct."

    def test_run_idrac_services_config_Error(self, mocker, idrac_default_args, idrac_connection_configure_services_mock,
                                             idrac_file_manager_config_services_mock):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "enable_web_server": "Enabled", "http_port": 443,
                                   "https_port": 343, "timeout": 10, "ssl_encryption": "T_128_Bit_or_higher",
                                   "tls_protocol": "TLS_1_1_and_Higher", "snmp_enable": "Enabled",
                                   "community_name": "communityname", "snmp_protocol": "All", "alert_port": 445,
                                   "discovery_port": 1000, "trap_format": "SNMPv1"})
        f_module = self.get_module_mock(params=idrac_default_args)
        obj = MagicMock()
        obj.IsValid = True
        mocker.patch(
            MODULE_PATH + "dellemc_configure_idrac_services.file_share_manager.create_share_obj", return_value=(obj))
        message = {'Status': 'Failed', 'Message': 'Key Error Expected', "Data1": {
            'Message': 'Status failed in checking data'}}
        idrac_connection_configure_services_mock.config_mgr.set_liason_share.return_value = message
        idrac_connection_configure_services_mock.config_mgr.apply_changes.return_value = "Returned on Key Error"
        with pytest.raises(Exception) as exc:
            self.module.run_idrac_services_config(idrac_connection_configure_services_mock, f_module)
        assert exc.value.args[0] == "Key Error Expected"

    def test_run_idrac_services_config_extra_coverage(self, mocker, idrac_default_args, idrac_connection_configure_services_mock,
                                                      idrac_file_manager_config_services_mock):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "enable_web_server": "Enabled", "http_port": 443,
                                   "https_port": 343, "timeout": 10, "ssl_encryption": "T_128_Bit_or_higher",
                                   "tls_protocol": "TLS_1_1_and_Higher", "snmp_enable": "Enabled",
                                   "community_name": "communityname", "snmp_protocol": "All", "alert_port": 445,
                                   "discovery_port": 1000, "trap_format": "SNMPv1", "ipmi_lan": {}})
        f_module = self.get_module_mock(params=idrac_default_args)
        obj = MagicMock()
        obj.IsValid = True
        mocker.patch(
            MODULE_PATH + "dellemc_configure_idrac_services.file_share_manager.create_share_obj", return_value=(obj))
        message = {'Status': 'Success', "Data": {
            'Message': 'Status failed in checking data'}}
        idrac_connection_configure_services_mock.config_mgr.set_liason_share.return_value = message
        idrac_connection_configure_services_mock.config_mgr.apply_changes.return_value = "Returned on community name none"
        ret_data = self.module.run_idrac_services_config(idrac_connection_configure_services_mock, f_module)
        assert ret_data == "Returned on community name none"

        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        idrac_connection_configure_services_mock.config_mgr.is_change_applicable.return_value = {
            'changes_applicable': False}
        with pytest.raises(Exception) as exc:
            self.module.run_idrac_services_config(idrac_connection_configure_services_mock, f_module)
        assert exc.value.args[0] == "No changes found to commit!"

        idrac_default_args.update({"ipmi_lan": None})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        ret_data = self.module.run_idrac_services_config(
            idrac_connection_configure_services_mock, f_module)
        assert ret_data == "Returned on community name none"

    def test_run_idrac_services_config_success_case06(self, idrac_connection_configure_services_mock,
                                                      idrac_default_args, idrac_file_manager_config_services_mock, mocker):
        status_msg = {"Status": "Success", "Message": "No changes found"}
        mocker.patch(
            MODULE_PATH + 'dellemc_configure_idrac_services.run_idrac_services_config', return_value=status_msg)
        resp = self._run_module(idrac_default_args)
        assert resp['changed'] is True
        assert resp['msg'] == "Successfully configured the iDRAC services settings."
        assert resp['service_status'].get('Status') == "Success"
        assert resp['service_status'].get('Message') == "No changes found"
