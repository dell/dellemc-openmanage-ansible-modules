# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 4.2.0
# Copyright (C) 2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
from io import StringIO

import pytest
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import ome_device_mgmt_network
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_device_mgmt_network.'

DEVICE_NOT_FOUND = "Device with {0} '{1}' not found."
NON_CONFIG_NETWORK = "Network settings for {0} is not configurable."
SUCCESS_MSG = "Successfully applied the network settings."
INVALID_IP = "Invalid {0} address provided for the {1}"
DNS_SETT_ERR1 = "'SecondaryDNS' requires 'PrimaryDNS' to be provided."
DNS_SETT_ERR2 = "'TertiaryDNS' requires both 'PrimaryDNS' and 'SecondaryDNS' to be provided."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
SERVER = 1000
CHASSIS = 2000
IO_MODULE = 4000


@pytest.fixture
def ome_connection_mock_for_device_network(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeDeviceMgmtNetwork(FakeAnsibleModule):
    module = ome_device_mgmt_network
    dns_configuration = {"dns_domain_name": "localdomain", "dns_name": "openmanage-enterprise",
                         "register_with_dns": False, "auto_negotiation": False,
                         "network_speed": "10_MB", "use_dhcp_for_dns_domain_name": False}
    ipv4_configuration = {"enable_ipv4": True, "enable_dhcp": False, "use_dhcp_to_obtain_dns_server_address": False,
                          "static_ip_address": "192.168.11.20", "static_subnet_mask": "255.255.255.0",
                          "static_gateway": "192.168.11.1", "static_preferred_dns_server": "192.168.11.2",
                          "static_alternate_dns_server": "192.168.11.3"}
    ipv6_configuration = {"enable_ipv6": True, "enable_auto_configuration": False,
                          "static_alternate_dns_server": "2607:f2b1:f081:9:1c8c:f1c7:47e:f121",
                          "static_gateway": "0000::ffff",
                          "static_ip_address": "2607:f2b1:f081:9:1c8c:f1c7:47e:f120",
                          "static_preferred_dns_server": "2607:f2b1:f081:9:1c8c:f1c7:47e:f122",
                          "static_prefix_length": 0, "use_dhcpv6_to_obtain_dns_server_address": False}
    dns_server_settings = {"preferred_dns_server": "192.96.20.181", "alternate_dns_server1": "192.96.20.182"}
    management_vlan = {"enable_vlan": True, "vlan_id": 0}
    inp_param = {
        "hostname": "192.1.2.3",
        "password": "password",
        "port": 443,
        "username": "root",
        "device_service_tag": Constants.service_tag1,
        "delay": 10,
        "dns_configuration": dns_configuration,
        "ipv4_configuration": ipv4_configuration,
        "ipv6_configuration": ipv6_configuration,
        "management_vlan": management_vlan,
        "dns_server_settings": dns_server_settings
    }
    chassis = {
        "SettingType": "Network",
        "MgmtVLANId": "1",
        "EnableVLAN": True,
        "Ipv4Settings": {
            "EnableIPv4": True,
            "EnableDHCP": False,
            "StaticIPAddress": "192.196.24.176",
            "StaticSubnetMask": "255.255.254.0",
            "StaticGateway": "192.196.24.1",
            "UseDHCPObtainDNSServerAddresses": False,
            "StaticPreferredDNSServer": "",
            "StaticAlternateDNSServer": ""
        },
        "Ipv6Settings": {
            "EnableIPv6": False,
            "EnableAutoconfiguration": False,
            "StaticIPv6Address": "",
            "StaticPrefixLength": "0",
            "StaticGateway": "",
            "UseDHCPv6ObtainDNSServerAddresses": False,
            "StaticPreferredDNSServer": "",
            "StaticAlternateDNSServer": ""
        },
        "GeneralSettings": {
            "EnableNIC": True,
            "RegisterDNS": False,
            "DnsName": "MX-6H5S6Z2",
            "UseDHCPForDomainName": False,
            "DnsDomainName": "",
            "AutoNegotiation": True,
            "NetworkSpeed": "1_GB",
            "Delay": 0
        }
    }
    server = {"SettingType": "Network",
              "useDHCPToObtainDNSIPv6": "Disabled",
              "staticPreferredDNSIPv6": "::",
              "currentGatewayIPv4": "192.92.24.1",
              "vlanId": "1",
              "staticPreferredDNSIPv4": "10.8.8.8",
              "staticSubnetMaskIPv4": "255.255.254.0",
              "currentIPAddressIPv4": "192.92.24.177",
              "enableDHCPIPv4": "Disabled",
              "currentIPAddressIPv6": "::",
              "staticIPAddressIPv6": "::",
              "staticIPAddressIPv4": "192.92.24.177",
              "useDHCPToObtainDNSIPv4": "Disabled",
              "staticGatewayIPv6": "::",
              "staticPrefixLengthIPv6": "64",
              "vlanEnable": "Disabled",
              "enableAutoConfigurationIPv6": "Enabled",
              "staticGatewayIPv4": "192.92.24.1",
              "enableIPv6": "Disabled",
              "staticAlternateDNSIPv6": "::",
              "enableIPv4": "Enabled",
              "enableNIC": "Enabled",
              "staticAlternateDNSIPv4": "192.96.7.7"}
    iom = {"SettingType": "Network",
           "MgmtVLANId": "",
           "EnableMgmtVLANId": False,
           "IomIPv4Settings": {
               "EnableIPv4": True,
               "EnableDHCP": True,
               "StaticIPAddress": "192.96.24.35",
               "StaticSubnetMask": "255.255.254.0",
               "StaticGateway": "192.96.24.1"
           },
           "IomIPv6Settings": {
               "EnableIPv6": True,
               "StaticIPv6Address": "2607:f2b1:f2b1:9:f2b1:f2b1:f2b1:be45",
               "StaticPrefixLength": "64",
               "StaticGateway": "fe80::f2b1:f2b1:f2b1:9",
               "UseDHCPv6": False
           },
           "IomDNSSettings": {
               "PrimaryDNS": "",
               "SecondaryDNS": "",
               "TertiaryDNS": ""
           }}

    @pytest.mark.parametrize("params", [
        {"module_args": inp_param, "dvc": {"Type": 2000}, "msg": SUCCESS_MSG},
        {"module_args": inp_param, "dvc": {"Type": 1000}, "msg": SUCCESS_MSG},
        {"module_args": inp_param, "dvc": {"Type": 4000}, "msg": SUCCESS_MSG}
    ])
    def test_ome_device_mgmt_network_success(self, params, ome_connection_mock_for_device_network,
                                             ome_response_mock, ome_default_args, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = {"IPAddress": "192.1.2.3"}
        mocker.patch(MODULE_PATH + 'get_device_details', return_value=params.get("dvc", {"Type": 2000}))
        mocker.patch(MODULE_PATH + 'get_network_payload', return_value={"Type": 2000})
        ome_default_args.update(params['module_args'])
        result = self._run_module(ome_default_args, check_mode=params.get('check_mode', False))
        assert result['msg'] == params['msg']

    @pytest.mark.parametrize("params", [
        {"module_args": inp_param, "dvc": {"Type": 3000, "Model": "Unsupported"}, "msg": NON_CONFIG_NETWORK}, ])
    def test_ome_device_mgmt_network_fails(self, params, ome_connection_mock_for_device_network,
                                           ome_response_mock, ome_default_args, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = {"IPAddress": "192.1.2.3"}
        dvc = params.get("dvc")
        mocker.patch(MODULE_PATH + 'get_device_details', return_value=dvc)
        mocker.patch(MODULE_PATH + 'get_network_payload', return_value={})
        ome_default_args.update(params['module_args'])
        result = self._run_module_with_fail_json(ome_default_args)
        assert result['msg'] == params['msg'].format(dvc.get('Model'))

    @pytest.mark.parametrize("params", [
        {"module_args": {"device_id": 123, "dns_server_settings": {"alternate_dns_server1": "192.96.20.182"}},
         "json_data": {"IomDNSSettings": {"PrimaryDNS": None, "SecondaryDNS": "", "TertiaryDNS": ""}},
         "dvc": {"Type": 4000}, "msg": DNS_SETT_ERR1}])
    def _test_ome_device_mgmt_iom_dns_failure(self, params, ome_connection_mock_for_device_network,
                                              ome_response_mock, ome_default_args, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params.get("json_data")
        dvc = params.get("dvc")
        mocker.patch(MODULE_PATH + 'get_device_details', return_value=dvc)
        ome_default_args.update(params['module_args'])
        result = self._run_module_with_fail_json(ome_default_args)
        assert result['msg'] == params['msg']

    @pytest.mark.parametrize("addr_param", [{"in": inp_param},
                                            {"in": {"dns_configuration": {"register_with_dns": True}}},
                                            {"in": {"management_vlan": {"enable_vlan": True}}}
                                            ])
    def test_validate_input_success(self, addr_param):
        f_module = self.get_module_mock(params=addr_param["in"])
        self.module.validate_input(f_module)

    @pytest.mark.parametrize("param", [{"in": inp_param, "device": chassis, "enable_nic": False, "delay": 5,
                                        "diff": {'EnableNIC': False, 'Delay': 5}},
                                       {"in": inp_param, "device": chassis, "enable_nic": True,
                                        "diff": {'StaticAlternateDNSServer': '2607:f2b1:f081:9:1c8c:f1c7:47e:f121',
                                                 'StaticPreferredDNSServer': '2607:f2b1:f081:9:1c8c:f1c7:47e:f122',
                                                 'StaticGateway': '0000::ffff', 'StaticSubnetMask': '255.255.255.0',
                                                 'StaticIPAddress': '192.168.11.20',
                                                 'StaticIPv6Address': '2607:f2b1:f081:9:1c8c:f1c7:47e:f120',
                                                 'StaticPrefixLength': 0, 'EnableIPv6': True, 'NetworkSpeed': '10_MB',
                                                 'DnsName': 'openmanage-enterprise', 'AutoNegotiation': False,
                                                 'DnsDomainName': 'localdomain', 'MgmtVLANId': 0}},
                                       {"in": {"ipv6_configuration": ipv6_configuration}, "device": chassis,
                                        "enable_nic": True,
                                        "diff": {'StaticAlternateDNSServer': '2607:f2b1:f081:9:1c8c:f1c7:47e:f121',
                                                 'StaticPreferredDNSServer': '2607:f2b1:f081:9:1c8c:f1c7:47e:f122',
                                                 'StaticGateway': '0000::ffff',
                                                 'StaticIPv6Address': '2607:f2b1:f081:9:1c8c:f1c7:47e:f120',
                                                 'StaticPrefixLength': 0, 'EnableIPv6': True}},
                                       {"in": {"ipv4_configuration": ipv4_configuration}, "device": chassis,
                                        "enable_nic": True,
                                        "diff": {'StaticAlternateDNSServer': '192.168.11.3',
                                                 'StaticPreferredDNSServer': '192.168.11.2',
                                                 'StaticGateway': '192.168.11.1', 'StaticSubnetMask': '255.255.255.0',
                                                 'StaticIPAddress': '192.168.11.20'}},
                                       {"in": {"dns_configuration": dns_configuration}, "device": chassis,
                                        "enable_nic": True,
                                        "diff": {'NetworkSpeed': '10_MB', 'DnsName': 'openmanage-enterprise',
                                                 'AutoNegotiation': False, 'DnsDomainName': 'localdomain'}},
                                       {"in": {"management_vlan": management_vlan}, "device": chassis,
                                        "enable_nic": True,
                                        "diff": {'MgmtVLANId': 0}}])
    def test_update_chassis_payload_success(self, param):
        inp = param["in"]
        inp['enable_nic'] = param.get("enable_nic")
        inp['delay'] = param.get('delay', 0)
        f_module = self.get_module_mock(params=inp)
        diff = self.module.update_chassis_payload(f_module, param["device"])
        assert diff == param.get("diff")

    @pytest.mark.parametrize("param", [{"in": inp_param, "device": server, "enable_nic": False,
                                        "diff": {'enableNIC': 'Disabled'}},
                                       {"in": inp_param, "device": server, "enable_nic": True,
                                        "diff": {'staticIPAddressIPv4': '192.168.11.20',
                                                 'staticSubnetMaskIPv4': '255.255.255.0',
                                                 'staticGatewayIPv4': '192.168.11.1',
                                                 'staticPreferredDNSIPv4': '192.168.11.2',
                                                 'staticAlternateDNSIPv4': '192.168.11.3',
                                                 'enableAutoConfigurationIPv6': 'Disabled',
                                                 'vlanEnable': 'Enabled',
                                                 'staticPreferredDNSIPv6': '2607:f2b1:f081:9:1c8c:f1c7:47e:f122',
                                                 'staticAlternateDNSIPv6': '2607:f2b1:f081:9:1c8c:f1c7:47e:f121',
                                                 'staticIPAddressIPv6': '2607:f2b1:f081:9:1c8c:f1c7:47e:f120',
                                                 'staticPrefixLengthIPv6': 0, 'staticGatewayIPv6': '0000::ffff',
                                                 'enableIPv6': 'Enabled',
                                                 'vlanId': 0}},
                                       {"in": {"ipv6_configuration": ipv6_configuration}, "device": server,
                                        "enable_nic": True,
                                        "diff": {'staticPreferredDNSIPv6': '2607:f2b1:f081:9:1c8c:f1c7:47e:f122',
                                                 'staticAlternateDNSIPv6': '2607:f2b1:f081:9:1c8c:f1c7:47e:f121',
                                                 'staticIPAddressIPv6': '2607:f2b1:f081:9:1c8c:f1c7:47e:f120',
                                                 'staticPrefixLengthIPv6': 0, 'staticGatewayIPv6': '0000::ffff',
                                                 'enableAutoConfigurationIPv6': 'Disabled', 'enableIPv6': 'Enabled'}},
                                       {"in": {"ipv4_configuration": ipv4_configuration}, "device": server,
                                        "enable_nic": True, "diff": {'staticIPAddressIPv4': '192.168.11.20',
                                                                     'staticSubnetMaskIPv4': '255.255.255.0',
                                                                     'staticGatewayIPv4': '192.168.11.1',
                                                                     'staticPreferredDNSIPv4': '192.168.11.2',
                                                                     'staticAlternateDNSIPv4': '192.168.11.3'}},
                                       {"in": {"management_vlan": management_vlan}, "device": server,
                                        "enable_nic": True, "diff": {'vlanEnable': 'Enabled', 'vlanId': 0}}
                                       ])
    def test_update_server_payload_success(self, param):
        inp = param["in"]
        inp['enable_nic'] = param.get("enable_nic")
        f_module = self.get_module_mock(params=inp)
        diff = self.module.update_server_payload(f_module, param["device"])
        assert diff == param.get("diff")

    @pytest.mark.parametrize("param", [{"in": inp_param, "device": iom, "enable_nic": False,
                                        "diff": {'StaticGateway': '0000::ffff', 'StaticIPAddress': '192.168.11.20',
                                                 'StaticSubnetMask': '255.255.255.0', 'EnableDHCP': False,
                                                 'EnableMgmtVLANId': True,
                                                 'StaticPrefixLength': 0,
                                                 'StaticIPv6Address': '2607:f2b1:f081:9:1c8c:f1c7:47e:f120',
                                                 'MgmtVLANId': 0, 'SecondaryDNS': '192.96.20.182',
                                                 'PrimaryDNS': '192.96.20.181'}},
                                       {"in": inp_param, "device": iom, "enable_nic": True,
                                        "diff": {'StaticGateway': '0000::ffff', 'StaticIPAddress': '192.168.11.20',
                                                 'StaticSubnetMask': '255.255.255.0', 'EnableDHCP': False,
                                                 'StaticPrefixLength': 0, 'EnableMgmtVLANId': True,
                                                 'StaticIPv6Address': '2607:f2b1:f081:9:1c8c:f1c7:47e:f120',
                                                 'MgmtVLANId': 0, 'SecondaryDNS': '192.96.20.182',
                                                 'PrimaryDNS': '192.96.20.181'}},
                                       {"in": {"ipv6_configuration": ipv6_configuration}, "device": iom,
                                        "enable_nic": True, "diff": {'StaticGateway': '0000::ffff',
                                                                     'StaticPrefixLength': 0,
                                                                     'StaticIPv6Address': '2607:f2b1:f081:9:1c8c:f1c7:47e:f120'}},
                                       {"in": {"ipv4_configuration": ipv4_configuration}, "device": iom,
                                        "enable_nic": True,
                                        "diff": {'StaticGateway': '192.168.11.1', 'StaticIPAddress': '192.168.11.20',
                                                 'StaticSubnetMask': '255.255.255.0', 'EnableDHCP': False}},
                                       {"in": {"management_vlan": management_vlan}, "device": iom,
                                        "enable_nic": True, "diff": {'EnableMgmtVLANId': True, 'MgmtVLANId': 0}}
                                       ])
    def test_update_iom_payload_success(self, param):
        inp = param["in"]
        inp['enable_nic'] = param.get("enable_nic")
        f_module = self.get_module_mock(params=inp)
        diff = self.module.update_iom_payload(f_module, param["device"])
        assert diff == param.get("diff")

    @pytest.mark.parametrize("params", [{"mparams": {
        'dns_configuration': {'dns_domain_name': 'localdomain', 'dns_name': 'openmanage-enterprise',
                              'register_with_dns': True, 'auto_negotiation': True,
                              'network_speed': '10_MB', 'use_dhcp_for_dns_domain_name': True},
        'ipv4_configuration': {'enable_ipv4': False, 'enable_dhcp': True, 'use_dhcp_to_obtain_dns_server_address': True,
                               'static_ip_address': '192.168.11.20', 'static_subnet_mask': '255.255.255.0',
                               'static_gateway': '192.168.11.1', 'static_preferred_dns_server': '192.168.11.2',
                               'static_alternate_dns_server': '192.168.11.3'},
        'ipv6_configuration': {'enable_ipv6': False, 'enable_auto_configuration': True,
                               'static_alternate_dns_server': '2607:f2b1:f081:9:1c8c:f1c7:47e:f121',
                               'static_gateway': '0000::ffff', 'static_ip_address': '2607:f2b1:f081:9:1c8c:f1c7:47e:f120',
                               'static_preferred_dns_server': '2607:f2b1:f081:9:1c8c:f1c7:47e:f122',
                               'static_prefix_length': 0, 'use_dhcpv6_to_obtain_dns_server_address': True},
        'management_vlan': {'enable_vlan': False, 'vlan_id': 0},
        'dns_server_settings': {'preferred_dns_server': '192.96.20.181',
                                'alternate_dns_server1': '192.96.20.182'}},
        "res": {'dns_configuration': {'dns_name': 'openmanage-enterprise',
                                      'register_with_dns': True, 'auto_negotiation': True,
                                      'use_dhcp_for_dns_domain_name': True},
                'ipv4_configuration': {'enable_ipv4': False},
                'ipv6_configuration': {'enable_ipv6': False},
                'management_vlan': {'enable_vlan': False},
                'dns_server_settings': {'preferred_dns_server': '192.96.20.181',
                                        'alternate_dns_server1': '192.96.20.182'}}}])
    def test_validate_dependency(self, params):
        mparams = params["mparams"]
        result = self.module.validate_dependency(mparams)
        assert result == params["res"]

    @pytest.mark.parametrize("params", [{"mparams": {"device_id": 123}, "success": True, "json_data": {
        "value": [{"Name": "vlan_name1", "Id": 124, "Identifier": "ABCD345"},
                  {"Name": "vlan_name", "Id": 123, "Identifier": "ABCD123"}]}, "res":
        {"Name": "vlan_name", "Id": 123, "Identifier": "ABCD123"}}, {
        "mparams": {"device_service_tag": "ABCD123"}, "success": True,
        "json_data": {"value": [{"Name": "vlan_name", "Id": 123, "Identifier": "ABCD123"}]},
        "res": {"Name": "vlan_name", "Id": 123, "Identifier": "ABCD123"}}])
    def test_get_device_details(
            self, params, ome_connection_mock_for_device_network, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params["mparams"])
        result = self.module.get_device_details(
            f_module, ome_connection_mock_for_device_network)
        assert result == params["res"]

    @pytest.mark.parametrize("params", [
        {"mparams": {"device_id": 123}, "success": True,
         "json_data": {"Type": 2000, "Id": 123, "Identifier": "ABCD123"},
         "res": {"Type": 2000, "Id": 123, "Identifier": "ABCD123"},
         "diff": {"IPV4": "1.2.3.4"}},
        {"mparams": {"device_id": 123}, "success": True,
         "json_data": {"Type": 4000, "Id": 123, "Identifier": "ABCD123"},
         "res": {"Type": 4000, "Id": 123, "Identifier": "ABCD123"},
         "diff": {"IPV4": "1.2.3.4"}},
    ])
    def test_get_network_payload(
            self, params, ome_connection_mock_for_device_network, ome_response_mock, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        ome_connection_mock_for_device_network.strip_substr_dict.return_value = params.get("json_data")
        mocker.patch(MODULE_PATH + 'update_chassis_payload', return_value=params['diff'])
        f_module = self.get_module_mock(params=params["mparams"])
        result = self.module.get_network_payload(
            f_module, ome_connection_mock_for_device_network, {"Id": 123, "Type": 2000})
        assert result == params.get("res")

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLValidationError, TypeError, ConnectionError, HTTPError, URLError])
    def test_device_network_main_exception_case(self, exc_type, mocker, ome_default_args,
                                                ome_connection_mock_for_device_network, ome_response_mock):
        ome_default_args.update({"device_service_tag": Constants.service_tag1})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'validate_input', side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'validate_input', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'validate_input',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result
