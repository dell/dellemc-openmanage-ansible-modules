# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.0.0
# Copyright (C) 2019-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import pytest
from io import StringIO
from ssl import SSLError
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils._text import to_text
from ansible_collections.dellemc.openmanage.plugins.modules import ome_application_network_address
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


@pytest.fixture
def ome_connection_mock_for_application_network_address(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'ome_application_network_address.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeAppNetwork(FakeAnsibleModule):
    module = ome_application_network_address

    inp_param = {
        "hostname": "192.1.2.3",
        "password": "password",
        "port": 443,
        "username": "root",
        "enable_nic": True,
        "interface_name": "eth0",
        "dns_configuration": {"dns_domain_name": "localdomain", "dns_name": "openmanage-enterprise",
                              "register_with_dns": False,
                              "use_dhcp_for_dns_domain_name": False},
        "ipv4_configuration": {"enable": True, "enable_dhcp": True, "use_dhcp_for_dns_server_names": True,
                               "static_ip_address": "192.168.11.20", "static_subnet_mask": "255.255.255.0",
                               "static_gateway": "192.168.11.1", "static_preferred_dns_server": "192.168.11.2",
                               "static_alternate_dns_server": "192.168.11.3"},
        "ipv6_configuration": {"enable": True, "enable_auto_configuration": True,
                               "static_alternate_dns_server": "2607:f2b1:f081:9:1c8c:f1c7:47e:f121",
                               "static_gateway": "0000::ffff",
                               "static_ip_address": "2607:f2b1:f081:9:1c8c:f1c7:47e:f120",
                               "static_preferred_dns_server": "2607:f2b1:f081:9:1c8c:f1c7:47e:f122",
                               "static_prefix_length": 0, "use_dhcp_for_dns_server_names": True},
        "management_vlan": {"enable_vlan": False, "vlan_id": 0},
        "reboot_delay": 1}
    inp_param1 = {
        "hostname": "192.1.2.3",
        "password": "password",
        "port": 443,
        "username": "root",
        "enable_nic": False
    }
    out_param = {"EnableNIC": False,
                 "InterfaceName": "eth0",
                 "PrimaryInterface": True,
                 "Ipv4Configuration": {"Enable": True, "EnableDHCP": True, "StaticIPAddress": "192.168.11.20",
                                       "StaticSubnetMask": "255.255.255.0", "StaticGateway": "192.168.11.1",
                                       "UseDHCPForDNSServerNames": True, "StaticPreferredDNSServer": "192.168.11.2",
                                       "StaticAlternateDNSServer": "192.168.11.3"},
                 "Ipv6Configuration": {"Enable": True, "EnableAutoConfiguration": True,
                                       "StaticIPAddress": "2607:f2b1:f081:9:1c8c:f1c7:47e:f120",
                                       "StaticPrefixLength": 0, "StaticGateway": "0000::ffff",
                                       "UseDHCPForDNSServerNames": True,
                                       "StaticPreferredDNSServer": "2607:f2b1:f081:9:1c8c:f1c7:47e:f122",
                                       "StaticAlternateDNSServer": "2607:f2b1:f081:9:1c8c:f1c7:47e:f121"},
                 "ManagementVLAN": {"EnableVLAN": False, "Id": 0},
                 "DnsConfiguration": {"RegisterWithDNS": False, "DnsName": "openmanage-enterprise",
                                      "UseDHCPForDNSDomainName": False, "DnsDomainName": "localdomain"},
                 "Delay": 0
                 }

    @pytest.mark.parametrize("addr_param", [{"in": inp_param, "out": out_param},
                                            {"in": inp_param1, "out": out_param}])
    def test_ome_application_network_address_main_success_case_01(self, mocker, ome_default_args, addr_param,
                                                                  ome_connection_mock_for_application_network_address,
                                                                  ome_response_mock):
        IP_CONFIG = "ApplicationService/Network/AddressConfiguration"
        JOB_IP_CONFIG = "ApplicationService/Network/AdapterConfigurations"
        POST_IP_CONFIG = "ApplicationService/Actions/Network.ConfigureNetworkAdapter"
        ome_default_args.update(addr_param["in"])
        ipv4 = {"Enable": True, "EnableDHCP": True, "StaticIPAddress": "192.168.11.20",
                "StaticSubnetMask": "255.255.255.0", "StaticGateway": "192.168.11.1",
                "UseDHCPForDNSServerNames": True, "StaticPreferredDNSServer": "192.168.11.1",
                "StaticAlternateDNSServer": ""}
        ipv6 = {"Enable": False, "EnableAutoConfiguration": True, "StaticIPAddress": "",
                "StaticPrefixLength": 0, "StaticGateway": "", "UseDHCPForDNSServerNames": True,
                "StaticPreferredDNSServer": "", "StaticAlternateDNSServer": ""}
        dns = {"RegisterWithDNS": False, "DnsName": "openmanage-enterprise",
               "UseDHCPForDNSDomainName": False, "DnsDomainName": "localdomain"}
        vlan = {"EnableVLAN": False, "Id": 1}
        mocker.patch(MODULE_PATH + "ome_application_network_address.validate_input")
        mocker.patch(MODULE_PATH + "ome_application_network_address.get_payload",
                     return_value=(ipv4, ipv6, dns, vlan))
        mocker.patch(MODULE_PATH + "ome_application_network_address.get_updated_payload",
                     return_value=(addr_param["out"], "PUT", IP_CONFIG))
        ome_response_mock.json_data = addr_param["out"]
        ome_response_mock.success = True
        mresult = self.execute_module(ome_default_args)
        assert mresult['changed'] is True
        assert "msg" in mresult
        assert "network_configuration" in mresult and mresult["network_configuration"] == addr_param["out"]
        assert mresult["msg"] == "Successfully triggered task to update network address configuration."

    @pytest.mark.parametrize("addr_param", [{"in": inp_param, "out": out_param}])
    def test_ome_application_network_address_main_success_case_02(self, mocker, ome_default_args, addr_param,
                                                                  ome_connection_mock_for_application_network_address,
                                                                  ome_response_mock):
        POST_IP_CONFIG = "ApplicationService/Actions/Network.ConfigureNetworkAdapter"
        ome_default_args.update(addr_param["in"])
        ipv4 = {"Enable": True, "EnableDHCP": True, "StaticIPAddress": "192.168.11.20",
                "StaticSubnetMask": "255.255.255.0", "StaticGateway": "192.168.11.1",
                "UseDHCPForDNSServerNames": True, "StaticPreferredDNSServer": "192.168.11.1",
                "StaticAlternateDNSServer": ""}
        ipv6 = {"Enable": False, "EnableAutoConfiguration": True, "StaticIPAddress": "",
                "StaticPrefixLength": 0, "StaticGateway": "", "UseDHCPForDNSServerNames": True,
                "StaticPreferredDNSServer": "", "StaticAlternateDNSServer": ""}
        dns = {"RegisterWithDNS": False, "DnsName": "openmanage-enterprise",
               "UseDHCPForDNSDomainName": False, "DnsDomainName": "localdomain"}
        vlan = {"EnableVLAN": False, "Id": 1}
        mocker.patch(MODULE_PATH + "ome_application_network_address.validate_input")
        mocker.patch(MODULE_PATH + "ome_application_network_address.get_payload",
                     return_value=(ipv4, ipv6, dns, vlan))
        mocker.patch(MODULE_PATH + "ome_application_network_address.get_updated_payload",
                     return_value=(addr_param["out"], "POST", POST_IP_CONFIG))
        ome_response_mock.json_data = addr_param["out"]
        ome_response_mock.success = True
        mresult = self.execute_module(ome_default_args)
        assert mresult['changed'] is True
        assert "msg" in mresult
        assert "network_configuration" in mresult and mresult["network_configuration"] == addr_param["out"]
        assert mresult["msg"] == "Successfully triggered job to update network address configuration."

    @pytest.mark.parametrize("addr_param", [{"in": inp_param, "out": out_param}])
    def test_get_payload(self, addr_param, ome_default_args):
        ome_default_args.update(addr_param["in"])
        f_module = self.get_module_mock(params=addr_param["in"])
        ipv4_payload, ipv6_payload, dns_payload, vlan_payload = self.module.get_payload(f_module)
        assert ipv4_payload == addr_param["out"]["Ipv4Configuration"]
        assert ipv6_payload == addr_param["out"]["Ipv6Configuration"]
        assert dns_payload == addr_param["out"]["DnsConfiguration"]
        assert vlan_payload == addr_param["out"]["ManagementVLAN"]

    @pytest.mark.parametrize("addr_param", [{"in": inp_param, "out": out_param}])
    def test_get_updated_payload(self, mocker, ome_default_args, addr_param,
                                 ome_connection_mock_for_application_network_address,
                                 ome_response_mock):
        ome_default_args.update(addr_param["in"])
        f_module = self.get_module_mock(params=addr_param["in"])
        ome_response_mock.json_data = {"value": [addr_param["out"]]}
        ipv4 = {"Enable": True, "EnableDHCP": True, "StaticIPAddress": "192.168.11.20",
                "StaticSubnetMask": "255.255.255.0", "StaticGateway": "192.168.11.1",
                "UseDHCPForDNSServerNames": True, "StaticPreferredDNSServer": "192.168.11.2",
                "StaticAlternateDNSServer": "192.168.11.3"}
        ipv6 = {"Enable": True, "EnableAutoConfiguration": False,
                "StaticIPAddress": "2607:f2b1:f081:9:1c8c:f1c7:47e:f12",
                "StaticPrefixLength": 0, "StaticGateway": "0000::ffff", "UseDHCPForDNSServerNames": True,
                "StaticPreferredDNSServer": "2607:f2b1:f081:9:1c8c:f1c7:47e:f122",
                "StaticAlternateDNSServer": "2607:f2b1:f081:9:1c8c:f1c7:47e:f12"}
        dns = {"RegisterWithDNS": False, "DnsName": "openmanage-enterprise",
               "UseDHCPForDNSDomainName": False, "DnsDomainName": "localdomain"}
        vlan = {"EnableVLAN": False, "Id": 1}
        current_setting, method, uri = self.module.get_updated_payload(
            ome_connection_mock_for_application_network_address, f_module, ipv4, ipv6, dns, vlan)
        assert current_setting == addr_param["out"]

    def test_get_updated_payload_when_same_setting_failure_case(self, ome_default_args,
                                                                ome_connection_mock_for_application_network_address,
                                                                ome_response_mock):
        ipv4 = {"Enable": True, "EnableDHCP": True, "StaticIPAddress": "192.168.11.20",
                "StaticSubnetMask": "255.255.255.0", "StaticGateway": "192.168.11.1",
                "UseDHCPForDNSServerNames": True, "StaticPreferredDNSServer": "192.168.11.2",
                "StaticAlternateDNSServer": "192.168.11.3"}
        ipv6 = {"Enable": True, "EnableAutoConfiguration": True,
                "StaticIPAddress": "2607:f2b1:f081:9:1c8c:f1c7:47e:f120",
                "StaticPrefixLength": 0, "StaticGateway": "0000::ffff", "UseDHCPForDNSServerNames": True,
                "StaticPreferredDNSServer": "2607:f2b1:f081:9:1c8c:f1c7:47e:f122",
                "StaticAlternateDNSServer": "2607:f2b1:f081:9:1c8c:f1c7:47e:f121"}
        dns = {"RegisterWithDNS": False, "DnsName": "openmanage-enterprise",
               "UseDHCPForDNSDomainName": False, "DnsDomainName": "localdomain"}
        vlan = {"EnableVLAN": False, "Id": 1}
        current_setting = {"value": [{
            "@odata.context": "/api/$metadata#Network.AddressConfiguration/$entity",
            "@odata.type": "#Network.AddressConfiguration",
            "@odata.id": "/api/ApplicationService/Network/AddressConfiguration",
            "EnableNIC": True,
            "InterfaceName": "eth0",
            "PrimaryInterface": True,
            "Ipv4Configuration": ipv4,
            "Ipv6Configuration": ipv6,
            "DnsConfiguration": dns,
            "ManagementVLAN": vlan,
            "Delay": 0
        }]}
        ome_default_args.update({"enable_nic": True, "interface_name": "eth0"})
        f_module = self.get_module_mock(params=ome_default_args)
        ome_response_mock.json_data = current_setting
        error_message = "No changes found to be applied."
        with pytest.raises(Exception, match=error_message) as err:
            self.module.get_updated_payload(ome_connection_mock_for_application_network_address, f_module, ipv4, ipv6,
                                            dns, vlan)

    @pytest.mark.parametrize("addr_param",
                             [{"in": inp_param["ipv4_configuration"], "out": out_param["Ipv4Configuration"]},
                              {"in": {"enable": True, "enable_auto_configuration": True,
                                      "static_alternate_dns_server": "2607:f2b1:f081:9:1c8c:f1c7:47e:f121",
                                      "static_gateway": "0000::ffff",
                                      "static_ip_address": "2607:f2b1:f081:9:1c8c:f1c7:47e:f120",
                                      "static_preferred_dns_server": "2607:f2b1:f081:9:1c8c:f1c7:47e:f122",
                                      "static_prefix_length": 0, "use_dhcp_for_dns_server_names": True},
                               "out": {"Enable": True, "EnableAutoConfiguration": True,
                                       "StaticIPAddress": "2607:f2b1:f081:9:1c8c:f1c7:47e:f120",
                                       "StaticPrefixLength": 0, "StaticGateway": "0000::ffff",
                                       "UseDHCPForDNSServerNames": True,
                                       "StaticPreferredDNSServer": "2607:f2b1:f081:9:1c8c:f1c7:47e:f122",
                                       "StaticAlternateDNSServer": "2607:f2b1:f081:9:1c8c:f1c7:47e:f121"}},
                              {"in": inp_param["dns_configuration"], "out": out_param["DnsConfiguration"]},
                              {"in": None, "out": None}])
    def test_format_payload(self, addr_param):
        result = self.module.format_payload(addr_param["in"])
        assert result == addr_param["out"]

    @pytest.mark.parametrize("addr_param", [{"in": inp_param},
                                            {"in": {"dns_configuration": {"register_with_dns": True}}},
                                            {"in": {"management_vlan": {"enable_vlan": True}}}
                                            ])
    def test_validate_input_success(self, addr_param):
        f_module = self.get_module_mock(params=addr_param["in"])
        self.module.validate_input(f_module)

    def _test_validate_input_fail1(self, ome_default_args):
        ome_default_args.update(
            {"management_vlan": {"enable_vlan": True}, "dns_configuration": {"register_with_dns": True}})
        f_module = self.get_module_mock(params=ome_default_args)
        error_message = "The vLAN settings cannot be updated if the 'register_with_dns' is true. " \
                        "The 'register_with_dns' cannot be updated if vLAN settings change."
        with pytest.raises(Exception, match=error_message) as err:
            self.module.validate_input(f_module)

    def test_validate_input_fail2(self, ome_default_args):
        ome_default_args.update({"reboot_delay": -1})
        f_module = self.get_module_mock(params=ome_default_args)
        error_message = "Invalid value provided for 'reboot_delay'"
        with pytest.raises(Exception, match=error_message) as err:
            self.module.validate_input(f_module)

    @pytest.mark.parametrize("addr_param", [{"in": "192.168.0.5", "out": True},
                                            {"in": "2607:f2b1:f081:9:1c8c:f1c7:47e:f121", "out": False}])
    def test_validate_ip_address(self, addr_param):
        ret_val = self.module.validate_ip_address(addr_param["in"])
        assert ret_val == addr_param["out"]

    @pytest.mark.parametrize("addr_param", [{"in": "192.168.0.5", "out": False},
                                            {"in": "2607:f2b1:f081:9:1c8c:f1c7:47e:f121", "out": True}])
    def test_validate_ip_v6_address(self, addr_param):
        ret_val = self.module.validate_ip_v6_address(addr_param["in"])
        assert ret_val == addr_param["out"]

    src_dict1 = {"Enable": False, "EnableDHCP": True, "UseDHCPForDNSServerNames": False,
                 "StaticGateway": "192.168.11.2",
                 "StaticIPAddress": "192.168.11.20", "StaticSubnetMask": "255.255.255.0",
                 "StaticPreferredDNSServer": "192.168.11.3", "EnableAutoConfiguration": True}
    new_dict1 = {"Enable": True, "EnableDHCP": False, "StaticGateway": "192.168.11.1",
                 "UseDHCPForDNSServerNames": True, "StaticPreferredDNSServer": "192.168.11.2",
                 "StaticAlternateDNSServer": "192.168.11.3"}
    src_dict2 = {"StaticIPAddress": "192.168.11.20", "StaticSubnetMask": "255.255.255.0",
                 "EnableAutoConfiguration": False}
    new_dict2 = {"StaticIPAddress": "192.168.11.20", "StaticSubnetMask": "255.255.255.0"}

    @pytest.mark.parametrize("addr_param", [{"src_dict": src_dict1, "new_dict": new_dict1, 'diff': 4},
                                            {"src_dict": src_dict2, "new_dict": new_dict2, 'diff': False},
                                            {"src_dict": src_dict2, "new_dict": {}, 'diff': 0},
                                            {"src_dict": src_dict2, "new_dict": {"EnableDHCP": None}, 'diff': 0}
                                            ])
    def test_update_ipv4_payload(self, addr_param):
        ret_val = self.module.update_ipv4_payload(addr_param["src_dict"], addr_param["new_dict"])
        assert ret_val == addr_param['diff']

    v6src_dict1 = {"Enable": False, "UseDHCPForDNSServerNames": False,
                   "StaticGateway": "192.168.11.2",
                   "StaticIPAddress": "192.168.11.20", "StaticSubnetMask": "255.255.255.0",
                   "StaticPreferredDNSServer": "192.168.11.3", "EnableAutoConfiguration": False}
    v6new_dict1 = {"Enable": True, "EnableAutoConfiguration": True, "StaticGateway": "192.168.11.1",
                   "UseDHCPForDNSServerNames": True, "StaticPreferredDNSServer": "2607:f2b1:f081:9:1c8c:f1c7:47e:f122",
                   "StaticAlternateDNSServer": "2607:f2b1:f081:9:1c8c:f1c7:47e:f121"}

    @pytest.mark.parametrize("addr_param", [{"src_dict": v6src_dict1, "new_dict": v6new_dict1, 'diff': 3},
                                            {"src_dict": v6src_dict1, "new_dict": {}, 'diff': 0}])
    def test_update_ipv6_payload(self, addr_param):
        ret_val = self.module.update_ipv6_payload(addr_param["src_dict"], addr_param["new_dict"])
        assert ret_val == addr_param['diff']

    dns_src = {"RegisterWithDNS": False, "DnsName": "openmanage-enterprise",
               "UseDHCPForDNSDomainName": False, "DnsDomainName": "localdomain"}
    dns_new = {"RegisterWithDNS": True, "DnsName": "openmanage-enterprise1",
               "UseDHCPForDNSDomainName": True, "DnsDomainName": "localdomain1"}

    @pytest.mark.parametrize("addr_param", [{"src_dict": dns_src, "new_dict": dns_new, 'diff': 3},
                                            {"src_dict": dns_src, "new_dict": {}, 'diff': 0},
                                            {"src_dict": dns_src, "new_dict": {"RegisterWithDNS": None,
                                                                               "UseDHCPForDNSDomainName": None},
                                             'diff': 0}])
    def test_update_dns_payload(self, addr_param):
        ret_val = self.module.update_dns_payload(addr_param["src_dict"], addr_param["new_dict"])
        assert ret_val == addr_param['diff']

    vlan_src = {"EnableVLAN": False, "Id": 0}
    vlan_new = {"EnableVLAN": True, "Id": 1}

    @pytest.mark.parametrize("addr_param", [{"src_dict": vlan_src, "new_dict": vlan_new, 'diff': 2},
                                            {"src_dict": vlan_src, "new_dict": {}, 'diff': 0},
                                            {"src_dict": vlan_src, "new_dict": {"EnableVLAN": None}, 'diff': 0}])
    def test_update_vlan_payload(self, addr_param):
        ret_val = self.module.update_vlan_payload(addr_param["src_dict"], addr_param["new_dict"])
        assert ret_val == addr_param['diff']

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_application_network_address_main_success_failure_case1(self, exc_type, mocker, ome_default_args,
                                                                        ome_connection_mock_for_application_network_address,
                                                                        ome_response_mock):
        ome_default_args.update({"dns_configuration": {"dns_domain_name": "localdomain"},
                                 "ipv4_configuration": {"enable": True, "enable_dhcp": True},
                                 "ipv6_configuration": {"enable": False, "enable_auto_configuration": True}})
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'ome_application_network_address.validate_input',
                         side_effect=exc_type("url open error"))
            ome_default_args.update({"dns_configuration": {"dns_domain_name": "localdomain"},
                                     "ipv4_configuration": {"enable": True, "enable_dhcp": True},
                                     "ipv6_configuration": {"enable": False, "enable_auto_configuration": True}})
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'ome_application_network_address.validate_input',
                         side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'ome_application_network_address.validate_input',
                         side_effect=exc_type('https://testhost.com', 400,
                                              'http error message',
                                              {"accept-type": "application/json"},
                                              StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'network_configuration' not in result
        assert 'msg' in result

    def test_get_network_config_data_case_01(self, ome_connection_mock_for_application_network_address,
                                             ome_response_mock):
        param = {}
        ome_response_mock.json_data = {"value": [{"PrimaryInterface": "val1"}]}
        f_module = self.get_module_mock(params=param)
        nt_adp, method, POST_IP_CONFIG = self.module.get_network_config_data(
            ome_connection_mock_for_application_network_address, f_module)
        assert nt_adp == {'PrimaryInterface': 'val1'}
        assert method == "POST"
        assert POST_IP_CONFIG == "ApplicationService/Actions/Network.ConfigureNetworkAdapter"

    def test_get_network_config_data_case_02(self, ome_connection_mock_for_application_network_address,
                                             ome_response_mock):
        param = {"interface_name": "val1"}
        ome_response_mock.json_data = {"value": [{"InterfaceName": "val1"}]}
        f_module = self.get_module_mock(params=param)
        nt_adp, method, POST_IP_CONFIG = self.module.get_network_config_data(
            ome_connection_mock_for_application_network_address, f_module)
        assert nt_adp == {'InterfaceName': 'val1'}
        assert method == "POST"
        assert POST_IP_CONFIG == "ApplicationService/Actions/Network.ConfigureNetworkAdapter"

    def test_get_network_config_data_case_03(self, ome_connection_mock_for_application_network_address,
                                             ome_response_mock):

        param = {"interface_name": "interface_name"}
        ome_response_mock.json_data = {"value": [{"InterfaceName": "val2", "PrimaryInterface": "val3"}]}
        f_module = self.get_module_mock(params=param)
        nt_adp, method, POST_IP_CONFIG = self.module.get_network_config_data(
            ome_connection_mock_for_application_network_address, f_module)
        assert nt_adp == "val3"
        assert method == "POST"
        assert POST_IP_CONFIG == "ApplicationService/Actions/Network.ConfigureNetworkAdapter"

    def test_get_network_config_data_case_03(self, ome_connection_mock_for_application_network_address,
                                             ome_response_mock):
        param = {}
        ome_response_mock.json_data = {"value": []}
        f_module = self.get_module_mock(params=param)
        nt_adp, method, POST_IP_CONFIG = self.module.get_network_config_data(
            ome_connection_mock_for_application_network_address, f_module)
        assert nt_adp is None
        assert method == "POST"
        assert POST_IP_CONFIG == "ApplicationService/Actions/Network.ConfigureNetworkAdapter"

    def test_get_network_config_data_exception_case_01(self, ome_connection_mock_for_application_network_address,
                                                       ome_response_mock):
        param = {"interface_name": "interface_name_val"}
        ome_response_mock.json_data = {"value": []}
        f_module = self.get_module_mock(params=param)
        msg = "The 'interface_name' value provided interface_name_val is invalid"
        with pytest.raises(Exception) as exc:
            self.module.get_network_config_data(ome_connection_mock_for_application_network_address, f_module)
        assert exc.value.args[0] == msg

    def test_get_network_config_data_exception_case_02(self, ome_connection_mock_for_application_network_address):
        param = {}
        msg = "exception message"
        ome_connection_mock_for_application_network_address.invoke_request.side_effect = Exception("exception message")
        f_module = self.get_module_mock(params=param)
        with pytest.raises(Exception, match=msg):
            self.module.get_network_config_data(
                ome_connection_mock_for_application_network_address, f_module)
