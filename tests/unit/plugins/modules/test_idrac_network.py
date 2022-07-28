# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 6.0.0
# Copyright (C) 2018-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_network
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from mock import MagicMock, patch, Mock
from io import StringIO
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestConfigNetwork(FakeAnsibleModule):
    module = idrac_network

    @pytest.fixture
    def idrac_configure_network_mock(self):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.file_share_manager = idrac_obj
        omsdk_mock.config_mgr = idrac_obj
        type(idrac_obj).create_share_obj = Mock(return_value="networkstatus")
        type(idrac_obj).set_liason_share = Mock(return_value="networkstatus")
        return idrac_obj

    @pytest.fixture
    def idrac_file_manager_config_networking_mock(self, mocker):
        try:
            file_manager_obj = mocker.patch(
                MODULE_PATH + 'idrac_network.file_share_manager')
        except AttributeError:
            file_manager_obj = MagicMock()
        obj = MagicMock()
        file_manager_obj.create_share_obj.return_value = obj
        return file_manager_obj

    @pytest.fixture
    def idrac_connection_configure_network_mock(self, mocker, idrac_configure_network_mock):
        idrac_conn_class_mock = mocker.patch(MODULE_PATH +
                                             'idrac_network.iDRACConnection',
                                             return_value=idrac_configure_network_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_configure_network_mock
        return idrac_configure_network_mock

    def test_main_idrac_configure_network_success_case(self, idrac_connection_configure_network_mock, mocker,
                                                       idrac_default_args, idrac_file_manager_config_networking_mock):
        idrac_default_args.update({"share_name": None})
        message = {'changed': False, 'msg': {'Status': "Success", "message": "No changes found to commit!"}}
        mocker.patch(MODULE_PATH + 'idrac_network.run_idrac_network_config', return_value=message)
        result = self._run_module(idrac_default_args)
        assert result == {'msg': 'Successfully configured the idrac network settings.',
                          'network_status': {
                              'changed': False,
                              'msg': {'Status': 'Success', 'message': 'No changes found to commit!'}},
                          'changed': False, 'failed': False}
        status_msg = {"Status": "Success", "Message": "No changes found to commit!"}
        mocker.patch(MODULE_PATH + 'idrac_network.run_idrac_network_config', return_value=status_msg)
        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Successfully configured the idrac network settings."
        status_msg = {"Status": "Success", "Message": "No changes were applied"}
        mocker.patch(MODULE_PATH + 'idrac_network.run_idrac_network_config', return_value=status_msg)
        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Successfully configured the idrac network settings."

    def test_run_idrac_network_config_success_case01(self, idrac_connection_configure_network_mock, idrac_default_args,
                                                     idrac_file_manager_config_networking_mock):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "register_idrac_on_dns": "Enabled",
                                   "dns_idrac_name": "testname", "auto_config": "Disabled", "static_dns": "staticdns",
                                   "setup_idrac_nic_vlan": "Enabled", "vlan_id": 4, "vlan_priority": "Enabled",
                                   "enable_nic": "Enabled", "nic_selection": "Dedicated",
                                   "failover_network": "ALL", "auto_detect": "Enabled", "auto_negotiation": "Enabled",
                                   "network_speed": "T_10", "duplex_mode": "Full", "nic_mtu": "nicmtu",
                                   "enable_dhcp": "Enabled", "ip_address": "100.100.102.114", "enable_ipv4": "Enabled",
                                   "dns_from_dhcp": "Enabled", "static_dns_1": "staticdns1",
                                   "static_dns_2": "staticdns2", "static_gateway": "staticgateway",
                                   "static_net_mask": "staticnetmask"})
        message = {"changes_applicable": True, "message": "changes are applicable"}
        idrac_connection_configure_network_mock.config_mgr.is_change_applicable.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        msg = self.module.run_idrac_network_config(idrac_connection_configure_network_mock, f_module)
        assert msg == {'changes_applicable': True, 'message': 'changes are applicable'}

    def test_run_idrac_network_config_success_case02(self, idrac_connection_configure_network_mock, idrac_default_args,
                                                     idrac_file_manager_config_networking_mock):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "register_idrac_on_dns": "Enabled",
                                   "dns_idrac_name": "testname", "auto_config": "Disabled", "static_dns": "staticdns",
                                   "setup_idrac_nic_vlan": "Enabled", "vlan_id": 4, "vlan_priority": "Enabled",
                                   "enable_nic": "Enabled", "nic_selection": "Dedicated",
                                   "failover_network": "ALL", "auto_detect": "Enabled", "auto_negotiation": "Enabled",
                                   "network_speed": "T_10", "duplex_mode": "Full", "nic_mtu": "nicmtu",
                                   "enable_dhcp": "Enabled", "ip_address": "100.100.102.114", "enable_ipv4": "Enabled",
                                   "dns_from_dhcp": "Enabled", "static_dns_1": "staticdns1",
                                   "static_dns_2": "staticdns2", "static_gateway": "staticgateway",
                                   "static_net_mask": "staticnetmask"})
        message = {"changes_applicable": True, "message": "changes found to commit!", "changed": True,
                   "Status": "Success"}
        idrac_connection_configure_network_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_idrac_network_config(idrac_connection_configure_network_mock, f_module)
        assert msg == {'Status': 'Success',
                       'changed': True,
                       'changes_applicable': True,
                       'message': 'changes found to commit!'}

    def test_run_idrac_network_config_success_case03(self, idrac_connection_configure_network_mock, idrac_default_args,
                                                     idrac_file_manager_config_networking_mock):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "register_idrac_on_dns": "Enabled",
                                   "dns_idrac_name": "testname", "auto_config": "Disabled", "static_dns": "staticdns",
                                   "setup_idrac_nic_vlan": "Enabled", "vlan_id": 4, "vlan_priority": "Enabled",
                                   "enable_nic": "Enabled", "nic_selection": "Dedicated",
                                   "failover_network": "ALL", "auto_detect": "Enabled", "auto_negotiation": "Enabled",
                                   "network_speed": "T_10", "duplex_mode": "Full", "nic_mtu": "nicmtu",
                                   "enable_dhcp": "Enabled", "ip_address": "100.100.102.114", "enable_ipv4": "Enabled",
                                   "dns_from_dhcp": "Enabled", "static_dns_1": "staticdns1",
                                   "static_dns_2": "staticdns2", "static_gateway": "staticgateway",
                                   "static_net_mask": "staticnetmask"})
        message = {"changes_applicable": False, "Message": "No changes found to commit!", "changed": False,
                   "Status": "Success"}
        idrac_connection_configure_network_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_idrac_network_config(idrac_connection_configure_network_mock, f_module)
        assert msg == {'Message': 'No changes found to commit!',
                       'Status': 'Success',
                       'changed': False,
                       'changes_applicable': False}

    def test_run_idrac_network_config_success_case04(self, idrac_connection_configure_network_mock,
                                                     idrac_default_args, idrac_file_manager_config_networking_mock):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "register_idrac_on_dns": "Enabled",
                                   "dns_idrac_name": "testname", "auto_config": "Disabled", "static_dns": "staticdns",
                                   "setup_idrac_nic_vlan": "Enabled", "vlan_id": 4, "vlan_priority": "Enabled",
                                   "enable_nic": "Enabled", "nic_selection": "Dedicated",
                                   "failover_network": "ALL", "auto_detect": "Enabled", "auto_negotiation": "Enabled",
                                   "network_speed": "T_10", "duplex_mode": "Full", "nic_mtu": "nicmtu",
                                   "enable_dhcp": "Enabled", "ip_address": "100.100.102.114", "enable_ipv4": "Enabled",
                                   "dns_from_dhcp": "Enabled", "static_dns_1": "staticdns1",
                                   "static_dns_2": "staticdns2", "static_gateway": "staticgateway",
                                   "static_net_mask": "staticnetmask"})
        message = {"changes_applicable": False, "Message": "No changes were applied", "changed": False,
                   "Status": "Success"}
        idrac_connection_configure_network_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_idrac_network_config(idrac_connection_configure_network_mock, f_module)
        assert msg == {'Message': 'No changes were applied',
                       'Status': 'Success',
                       'changed': False,
                       'changes_applicable': False}

    def test_run_idrac_network_config_success_case05(self, idrac_connection_configure_network_mock, idrac_default_args,
                                                     idrac_file_manager_config_networking_mock):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "register_idrac_on_dns": None,
                                   "dns_idrac_name": None, "auto_config": None, "static_dns": None,
                                   "setup_idrac_nic_vlan": None, "vlan_id": None, "vlan_priority": None,
                                   "enable_nic": None, "nic_selection": None,
                                   "failover_network": None, "auto_detect": None, "auto_negotiation": None,
                                   "network_speed": None, "duplex_mode": None, "nic_mtu": None,
                                   "enable_dhcp": None, "ip_address": None, "enable_ipv4": None,
                                   "dns_from_dhcp": None, "static_dns_1": None, "static_dns_2": None,
                                   "static_gateway": None, "static_net_mask": None})
        message = {"changes_applicable": False, "Message": "No changes were applied", "changed": False,
                   "Status": "Success"}
        idrac_connection_configure_network_mock.config_mgr.configure_dns.return_value = message
        idrac_connection_configure_network_mock.config_mgr.configure_nic_vlan.return_value = message
        idrac_connection_configure_network_mock.config_mgr.configure_network_settings.return_value = message
        idrac_connection_configure_network_mock.config_mgr.configure_ipv4.return_value = message
        idrac_connection_configure_network_mock.config_mgr.configure_static_ipv4.return_value = message
        idrac_connection_configure_network_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_idrac_network_config(idrac_connection_configure_network_mock, f_module)
        assert msg == {'Message': 'No changes were applied',
                       'Status': 'Success',
                       'changed': False,
                       'changes_applicable': False}

    def test_run_idrac_network_config_failed_case01(self, idrac_connection_configure_network_mock, idrac_default_args,
                                                    idrac_file_manager_config_networking_mock):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "register_idrac_on_dns": "Enabled",
                                   "dns_idrac_name": "testname", "auto_config": "Disabled", "static_dns": "staticdns",
                                   "setup_idrac_nic_vlan": "Enabled", "vlan_id": 4, "vlan_priority": "Enabled",
                                   "enable_nic": "Enabled", "nic_selection": "Dedicated",
                                   "failover_network": "ALL", "auto_detect": "Enabled", "auto_negotiation": "Enabled",
                                   "network_speed": "T_10", "duplex_mode": "Full", "nic_mtu": "nicmtu",
                                   "enable_dhcp": "Enabled", "ip_address": "100.100.102.114", "enable_ipv4": "Enabled",
                                   "dns_from_dhcp": "Enabled", "static_dns_1": "staticdns1",
                                   "static_dns_2": "staticdns2", "static_gateway": "staticgateway",
                                   "static_net_mask": "staticnetmask"})
        message = {'Status': 'Failed', "Data": {'Message': 'status failed in checking Data'}}
        idrac_connection_configure_network_mock.file_share_manager.create_share_obj.return_value = "mnt/iso"
        idrac_connection_configure_network_mock.config_mgr.set_liason_share.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        result = self.module.run_idrac_network_config(idrac_connection_configure_network_mock, f_module)
        assert result == idrac_connection_configure_network_mock.config_mgr.is_change_applicable()

    def test_run_idrac_network_config_failed_case02(self, idrac_connection_configure_network_mock,
                                                    idrac_default_args, idrac_file_manager_config_networking_mock):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "register_idrac_on_dns": "Enabled",
                                   "dns_idrac_name": "testname", "auto_config": "Disabled", "static_dns": "staticdns",
                                   "setup_idrac_nic_vlan": "Enabled", "vlan_id": 4, "vlan_priority": "Enabled",
                                   "enable_nic": "Enabled", "nic_selection": "Dedicated",
                                   "failover_network": "ALL", "auto_detect": "Enabled", "auto_negotiation": "Enabled",
                                   "network_speed": "T_10", "duplex_mode": "Full", "nic_mtu": "nicmtu",
                                   "enable_dhcp": "Enabled", "ip_address": "100.100.102.114", "enable_ipv4": "Enabled",
                                   "dns_from_dhcp": "Enabled", "static_dns_1": "staticdns1",
                                   "static_dns_2": "staticdns2", "static_gateway": "staticgateway",
                                   "static_net_mask": "staticnetmask"})
        message = {"changes_applicable": False, "Message": "No changes were applied", "changed": False,
                   "Status": "failed"}
        idrac_connection_configure_network_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_idrac_network_config(idrac_connection_configure_network_mock, f_module)
        assert msg == {'Message': 'No changes were applied', 'Status': 'failed', 'changed': False,
                       'changes_applicable': False}

    def test_run_idrac_network_config_failed_case03(self, idrac_connection_configure_network_mock,
                                                    idrac_default_args, idrac_file_manager_config_networking_mock):
        idrac_default_args.update({"share_name": None, "share_mnt": None, "share_user": None,
                                   "share_password": None, "register_idrac_on_dns": "Enabled",
                                   "dns_idrac_name": "testname", "auto_config": "Disabled", "static_dns": "staticdns",
                                   "setup_idrac_nic_vlan": "Enabled", "vlan_id": 4, "vlan_priority": "Enabled",
                                   "enable_nic": "Enabled", "nic_selection": "Dedicated",
                                   "failover_network": "ALL", "auto_detect": "Enabled", "auto_negotiation": "Enabled",
                                   "network_speed": "T_10", "duplex_mode": "Full", "nic_mtu": "nicmtu",
                                   "enable_dhcp": "Enabled", "ip_address": "100.100.102.114", "enable_ipv4": "Enabled",
                                   "dns_from_dhcp": "Enabled", "static_dns_1": "staticdns1",
                                   "static_dns_2": "staticdns2", "static_gateway": "staticgateway",
                                   "static_net_mask": "staticnetmask"})
        message = {'Status': 'Failed', "Data": {'Message': "Failed to found changes"}}
        idrac_connection_configure_network_mock.file_share_manager.create_share_obj.return_value = "mnt/iso"
        idrac_connection_configure_network_mock.config_mgr.set_liason_share.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        msg = self.module.run_idrac_network_config(idrac_connection_configure_network_mock, f_module)
        assert msg == idrac_connection_configure_network_mock.config_mgr.is_change_applicable()

    @pytest.mark.parametrize("exc_type", [RuntimeError, SSLValidationError, ConnectionError, KeyError,
                                          ImportError, ValueError, TypeError, HTTPError, URLError])
    def test_main_idrac_configure_network_exception_handling_case(self, exc_type, mocker, idrac_default_args,
                                                                  idrac_connection_configure_network_mock,
                                                                  idrac_file_manager_config_networking_mock):
        idrac_default_args.update({"share_name": None})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(
                MODULE_PATH + 'idrac_network.run_idrac_network_config',
                side_effect=exc_type('test'))
        else:
            mocker.patch(
                MODULE_PATH + 'idrac_network.run_idrac_network_config',
                side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                     {"accept-type": "application/json"}, StringIO(json_str)))
        if not exc_type == URLError:
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result
