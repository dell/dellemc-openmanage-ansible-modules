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
from ansible_collections.dellemc.openmanage.plugins.modules import dellemc_configure_idrac_services
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from mock import MagicMock, patch, Mock
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")


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
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "enable_web_server": "Enabled", "http_port": 443,
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

    def test_run_idrac_services_config_success_case01(self, idrac_connection_configure_services_mock,
                                                      idrac_default_args, idrac_file_manager_config_services_mock,
                                                      is_changes_applicable_mock_services):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "enable_web_server": "Enabled", "http_port": 443,
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
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "enable_web_server": "Enabled", "http_port": 443,
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
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "enable_web_server": "Enabled", "http_port": 443,
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
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "enable_web_server": "Enabled", "http_port": 443,
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
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "enable_web_server": None, "http_port": None,
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
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "enable_web_server": "Enabled", "http_port": 443,
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
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "enable_web_server": "Enabled", "http_port": 443,
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
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "enable_web_server": "Enabled", "http_port": 443,
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
        idrac_default_args.update({"share_name": "sharename"})
        message = {'changed': False, 'msg': {'Status': "failed", "message": "No changes found to commit!"}}
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_configure_idrac_services.run_idrac_services_config', return_value=message)
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result['failed'] is True

    @pytest.mark.parametrize("exc_type", [ImportError, ValueError, RuntimeError])
    def test_main_idrac_configure_services_exception_handling_case(self, exc_type, mocker, idrac_default_args,
                                                                   idrac_connection_configure_services_mock,
                                                                   idrac_file_manager_config_services_mock):
        idrac_default_args.update({"share_name": "sharename"})
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_configure_idrac_services.run_idrac_services_config', side_effect=exc_type('test'))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True
