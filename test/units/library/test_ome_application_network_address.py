# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0.10
# Copyright (C) 2020 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

from __future__ import absolute_import

import json

import pytest
from ansible.modules.remote_management.dellemc import ome_application_network_address
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from units.modules.remote_management.dellemc.common import FakeAnsibleModule, Constants, AnsibleFailJSonException
from io import StringIO
from ansible.module_utils._text import to_text
from ssl import SSLError


@pytest.fixture
def ome_connection_mock_for_application_network_address(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(
        'ansible.modules.remote_management.dellemc.ome_application_network_address.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeTemplate(FakeAnsibleModule):
    module = ome_application_network_address
    inp_param = {
        "hostname": "192.1.2.3",
        "password": "password",
        "port": 443,
        "username": "root",
        "dns_configuration": {"dns_domain_name": "localdomain","dns_name": "openmanage-enterprise","register_with_dns": False,
                              "use_dhcp_for_dns_domain_name": False},
        "ipv4_configuration": {"enable": True,"enable_dhcp": True,"use_dhcp_for_dns_server_names": True,
                               "static_ip_address": "192.168.11.20", "static_subnet_mask": "255.255.255.0",
                               "static_gateway": "192.168.11.1", "static_preferred_dns_server":"192.168.11.2",
                               "static_alternate_dns_server": "192.168.11.3"},
        "ipv6_configuration": {"enable": False,"enable_auto_configuration": True,
                               "static_alternate_dns_server": "2607:f2b1:f081:9:1c8c:f1c7:47e:f121",
                               "static_gateway": "0000::ffff", "static_ip_address": "2607:f2b1:f081:9:1c8c:f1c7:47e:f120",
                               "static_preferred_dns_server": "2607:f2b1:f081:9:1c8c:f1c7:47e:f122",
                               "static_prefix_length": 0,"use_dhcp_for_dns_server_names": True},
        "reboot_delay": 1}

    out_param = {"EnableNIC": True,
                 "Ipv4Configuration": {"Enable": True,"EnableDHCP": True,"StaticIPAddress": "192.168.11.20",
                                       "StaticSubnetMask": "255.255.255.0","StaticGateway": "192.168.11.1",
                                       "UseDHCPForDNSServerNames": True,"StaticPreferredDNSServer": "192.168.11.2",
                                       "StaticAlternateDNSServer": "192.168.11.3"},
                 "Ipv6Configuration": {"Enable": False,"EnableAutoConfiguration": True,"StaticIPAddress": "2607:f2b1:f081:9:1c8c:f1c7:47e:f120",
                                       "StaticPrefixLength": 0,"StaticGateway": "0000::ffff","UseDHCPForDNSServerNames": True,
                                       "StaticPreferredDNSServer": "2607:f2b1:f081:9:1c8c:f1c7:47e:f122",
                                       "StaticAlternateDNSServer": "2607:f2b1:f081:9:1c8c:f1c7:47e:f121"},
                 "ManagementVLAN": {"EnableVLAN": False,"Id": 0},
                 "DnsConfiguration": {"RegisterWithDNS": False,"DnsName": "openmanage-enterprise",
                                      "UseDHCPForDNSDomainName": False,"DnsDomainName": "localdomain"},
                 "Delay": 0,
                 "@odata.context": "/api/$metadata#Network.AddressConfiguration/$entity",
                 "@odata.type": "#Network.AddressConfiguration",
                 "@odata.id": "/api/ApplicationService/Network/AddressConfiguration"
                 }

    @pytest.mark.parametrize("addr_param", [{"in" : inp_param, "out" :out_param}])
    def _test_ome_application_network_address_main_success_case_01(self, mocker, ome_default_args, addr_param,
                                                                ome_connection_mock_for_application_network_address,
                                                                ome_response_mock):
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
        mocker.patch("ansible.modules.remote_management.dellemc.ome_application_network_address.get_payload",
                     return_value=(ipv4, ipv6, dns))
        mocker.patch("ansible.modules.remote_management.dellemc.ome_application_network_address.get_updated_payload",
                     return_value=(addr_param["out"], "PUT"))
        ome_response_mock.json_data = addr_param["out"]
        # ome_response_mock.success = True
        result = self.execute_module(ome_default_args)
        assert result['changed'] is True
        assert "msg" in result
        assert "network_configuration" in result and result["network_configuration"] == addr_param["out"]
        assert result["msg"] == "Successfully updated network address configuration"

    @pytest.mark.parametrize("addr_param", [{"in": inp_param, "out": out_param}])
    def test_get_payload(self, addr_param, ome_default_args):
        ome_default_args.update(addr_param["in"])
        f_module = self.get_module_mock(params=addr_param["in"])
        ipv4_payload, ipv6_payload, dns_payload = self.module.get_payload(f_module)
        assert ipv4_payload == addr_param["out"]["Ipv4Configuration"]
        assert ipv6_payload == addr_param["out"]["Ipv6Configuration"]
        assert dns_payload == addr_param["out"]["DnsConfiguration"]

    @pytest.mark.parametrize("addr_param", [{"in": inp_param, "out": out_param}])
    def _test_get_updated_payload(self, mocker, ome_default_args, addr_param,
                                                                ome_connection_mock_for_application_network_address,
                                                                ome_response_mock):
        ome_default_args.update(addr_param["in"])
        f_module = self.get_module_mock(params=addr_param["in"])
        ome_response_mock.json_data = addr_param["out"]
        ipv4 = {"Enable": True, "EnableDHCP": True, "StaticIPAddress": "192.168.11.20",
                              "StaticSubnetMask": "255.255.255.0", "StaticGateway": "192.168.11.1",
                              "UseDHCPForDNSServerNames": True, "StaticPreferredDNSServer": "192.168.11.2",
                              "StaticAlternateDNSServer": "192.168.11.3"}
        ipv6 = {"Enable": False, "EnableAutoConfiguration": True,
                              "StaticIPAddress": "2607:f2b1:f081:9:1c8c:f1c7:47e:f120",
                              "StaticPrefixLength": 0, "StaticGateway": "0000::ffff", "UseDHCPForDNSServerNames": True,
                              "StaticPreferredDNSServer": "2607:f2b1:f081:9:1c8c:f1c7:47e:f122",
                              "StaticAlternateDNSServer": "2607:f2b1:f081:9:1c8c:f1c7:47e:f121"}
        dns = {"RegisterWithDNS": False, "DnsName": "openmanage-enterprise",
                             "UseDHCPForDNSDomainName": False, "DnsDomainName": "localdomain"}
        current_setting, method = self.module.get_updated_payload(ome_connection_mock_for_application_network_address, f_module, ipv4, ipv6, dns)
        assert current_setting == addr_param["out"]

    def _test_get_updated_payload_when_same_setting_failure_case(self, ome_default_args, ome_connection_mock_for_application_network_address, ome_response_mock):
        current_setting = {
            "@odata.context": "/api/$metadata#Network.AddressConfiguration/$entity",
            "@odata.type": "#Network.AddressConfiguration",
            "@odata.id": "/api/ApplicationService/Network/AddressConfiguration",
            "EnableNIC": True,
            "Ipv4Configuration": {"Enable": True, "EnableDHCP": True, "StaticIPAddress": "192.168.11.20",
                "StaticSubnetMask": "255.255.255.0", "StaticGateway": "192.168.11.1",
                "UseDHCPForDNSServerNames": True, "StaticPreferredDNSServer": "192.168.11.2",
                "StaticAlternateDNSServer": "192.168.11.3"
            },
            "Ipv6Configuration": {"Enable": False, "EnableAutoConfiguration": True,
                "StaticIPAddress": "2607:f2b1:f081:9:1c8c:f1c7:47e:f120",
                "StaticPrefixLength": 0, "StaticGateway": "0000::ffff", "UseDHCPForDNSServerNames": True,
                "StaticPreferredDNSServer": "2607:f2b1:f081:9:1c8c:f1c7:47e:f122",
                "StaticAlternateDNSServer": "2607:f2b1:f081:9:1c8c:f1c7:47e:f121"
            },
            "DnsConfiguration": {"RegisterWithDNS": False, "DnsName": "openmanage-enterprise",
               "UseDHCPForDNSDomainName": False, "DnsDomainName": "localdomain"
            },
            "Delay": 0
        }
        ipv4 = {"Enable": True, "EnableDHCP": True, "StaticIPAddress": "192.168.11.20",
                "StaticSubnetMask": "255.255.255.0", "StaticGateway": "192.168.11.1",
                "UseDHCPForDNSServerNames": True, "StaticPreferredDNSServer": "192.168.11.2",
                "StaticAlternateDNSServer": "192.168.11.3"}
        ipv6 = {"Enable": False, "EnableAutoConfiguration": True,
                "StaticIPAddress": "2607:f2b1:f081:9:1c8c:f1c7:47e:f120",
                "StaticPrefixLength": 0, "StaticGateway": "0000::ffff", "UseDHCPForDNSServerNames": True,
                "StaticPreferredDNSServer": "2607:f2b1:f081:9:1c8c:f1c7:47e:f122",
                "StaticAlternateDNSServer": "2607:f2b1:f081:9:1c8c:f1c7:47e:f121"}
        dns = {"RegisterWithDNS": False, "DnsName": "openmanage-enterprise",
               "UseDHCPForDNSDomainName": False, "DnsDomainName": "localdomain"}
        f_module = self.get_module_mock(params=ome_default_args)
        ome_response_mock.json_data = current_setting
        error_message = "No changes made to network configuration as entered values are the same as current configured values"
        with pytest.raises(Exception, match=error_message) as err:
            self.module.get_updated_payload(ome_connection_mock_for_application_network_address, f_module, ipv4, ipv6, dns)

    def test_get_updated_payload_when_no_diff_failure_case(self, ome_default_args, ome_connection_mock_for_application_network_address, ome_response_mock):
        current_setting = {"@odata.context":"/api/$metadata#Network.ProxyConfiguration","@odata.type":"#Network.ProxyConfiguration","@odata.id":"/api/ApplicationService/Network/ProxyConfiguration","IpAddress":"255.0.0.0","PortNumber":443,"EnableAuthentication":False,"EnableProxy":True,"Username":"username","Password":"password"}
        ipv4 = {}
        ipv6 = {}
        dns = {}
        f_module = self.get_module_mock(params=ome_default_args)
        ome_response_mock.json_data = current_setting
        error_message = "Unable to configure the network because network configuration settings are not provided."
        with pytest.raises(Exception, match=error_message) as err:
            self.module.get_updated_payload(ome_connection_mock_for_application_network_address, f_module, ipv4,ipv6,dns)


    @pytest.mark.parametrize("addr_param", [{"in": inp_param["ipv4_configuration"], "out": out_param["Ipv4Configuration"]},
                                            {"in": inp_param["ipv6_configuration"], "out": out_param["Ipv6Configuration"]},
                                            {"in": inp_param["dns_configuration"], "out": out_param["DnsConfiguration"]}])
    def test_format_payload(self, addr_param):
        result = self.module.format_payload(addr_param["in"])
        assert result == addr_param["out"]

    @pytest.mark.parametrize("addr_param", [{"in": inp_param, "out": out_param}])
    def test_validate_input_success(self, addr_param):
        f_module = self.get_module_mock(params=addr_param["in"])
        self.module.validate_input(f_module)

    @pytest.mark.parametrize("addr_param", [{"in": "100.100.255.255", "out": True},
                                            {"in": "2607:f2b1:f081:9:1c8c:f1c7:47e:f121", "out": False}])
    def test_validate_ip_address(self, addr_param):
        ret_val = self.module.validate_ip_address(addr_param["in"])
        assert ret_val==addr_param["out"]

    @pytest.mark.parametrize("addr_param", [{"in": "100.100.255.255", "out": False},
                                            {"in":  "2607:f2b1:f081:9:1c8c:f1c7:47e:f121", "out": True}])
    def test_validate_ip_v6_address(self, addr_param):
        ret_val = self.module.validate_ip_v6_address(addr_param["in"])
        assert ret_val == addr_param["out"]

    src_dict1 = {"StaticIPAddress": "192.168.11.20","StaticSubnetMask": "255.255.255.0", "EnableAutoConfiguration": True}
    new_dict1 = {"StaticGateway": "192.168.11.1",
                                       "UseDHCPForDNSServerNames": True,"StaticPreferredDNSServer": "192.168.11.2",
                                       "StaticAlternateDNSServer": "192.168.11.3"}
    src_dict2 = {"StaticIPAddress": "192.168.11.20", "StaticSubnetMask": "255.255.255.0", "EnableAutoConfiguration": False}
    new_dict2 = {"StaticIPAddress": "192.168.11.20", "StaticSubnetMask": "255.255.255.0"}
    @pytest.mark.parametrize("addr_param", [{"src_dict": src_dict1, "new_dict": new_dict1, 'diff': 0},
                                            {"src_dict": src_dict2, "new_dict": new_dict2, 'diff': False}])
    def test_update_ipv4_payload(self, addr_param):
        ret_val = self.module.update_ipv4_payload(addr_param["src_dict"], addr_param["new_dict"])
        assert ret_val == addr_param['diff']

    @pytest.mark.parametrize("addr_param", [{"src_dict": src_dict1, "new_dict": new_dict1, 'diff': 0},
                                            {"src_dict": src_dict2, "new_dict": new_dict2, 'diff': False}])
    def test_update_ipv6_payload(self, addr_param):
        ret_val = self.module.update_ipv6_payload(addr_param["src_dict"], addr_param["new_dict"])
        assert ret_val == addr_param['diff']

    @pytest.mark.parametrize("addr_param", [{"src_dict": src_dict1, "new_dict": new_dict1, 'diff': 0},
                                            {"src_dict": src_dict2, "new_dict": new_dict2, 'diff': False}])
    def test_update_dns_payload(self, addr_param):
        ret_val = self.module.update_dns_payload(addr_param["src_dict"], addr_param["new_dict"])
        assert ret_val == addr_param['diff']

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_application_network_address_main_success_failure_case1(self, exc_type, mocker, ome_default_args,
                                                                      ome_connection_mock_for_application_network_address,
                                                                      ome_response_mock):
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch('ansible.modules.remote_management.dellemc.ome_application_network_address.validate_input',
                         side_effect=exc_type("urlopen error"))
            ome_default_args.update({"dns_configuration": {"dns_domain_name": "localdomain"},
                                     "ipv4_configuration": {"enable": True, "enable_dhcp": True},
                                     "ipv6_configuration": {"enable": False, "enable_auto_configuration": True}})
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch('ansible.modules.remote_management.dellemc.ome_application_network_address.validate_input',
                         side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch('ansible.modules.remote_management.dellemc.ome_application_network_address.validate_input',
                         side_effect=exc_type('http://testhost.com', 400,
                                              'http error message',
                                              {"accept-type": "application/json"},
                                              StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'network_configuration' not in result
        assert 'msg' in result