# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.0.0
# Copyright (C) 2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
import pytest
from ssl import SSLError
from io import StringIO
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils._text import to_text
from ansible_collections.dellemc.openmanage.plugins.modules import ome_device_quick_deploy
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_device_quick_deploy.'


@pytest.fixture
def ome_conn_mock_qd(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOMEMDevicePower(FakeAnsibleModule):

    module = ome_device_quick_deploy

    def test_check_domain_service(self, ome_conn_mock_qd, ome_default_args):
        f_module = self.get_module_mock()
        result = self.module.check_domain_service(f_module, ome_conn_mock_qd)
        assert result is None

    def test_get_chassis_device(self, ome_conn_mock_qd, ome_default_args, mocker, ome_response_mock):
        mocker.patch(MODULE_PATH + "get_ip_from_host", return_value="192.18.1.1")
        ome_response_mock.json_data = {"value": [{"DeviceId": 25011, "DomainRoleTypeValue": "LEAD",
                                                  "PublicAddress": ["192.168.1.1"]},
                                                 {"DeviceId": 25012, "DomainRoleTypeValue": "STANDALONE",
                                                  "PublicAddress": ["192.168.1.2"]}]}
        param = {"device_id": 25012, "hostname": "192.168.1.6"}
        f_module = self.get_module_mock(params=param)
        with pytest.raises(Exception) as err:
            self.module.get_chassis_device(f_module, ome_conn_mock_qd)
        assert err.value.args[0] == "Unable to retrieve the device information."

    def test_get_ip_from_host(self, ome_conn_mock_qd, ome_default_args, ome_response_mock):
        result = self.module.get_ip_from_host("192.168.0.1")
        assert result == "192.168.0.1"

    def test_validate_ip_address(self, ome_conn_mock_qd, ome_response_mock, ome_default_args):
        result = self.module.validate_ip_address("192.168.0.1", "IPV4")
        assert result is True
        result = self.module.validate_ip_address("192.168.0.1.1", "IPV4")
        assert result is False
        result = self.module.validate_ip_address("::", "IPV6")
        assert result is True

    def test_ip_address_field(self, ome_conn_mock_qd, ome_response_mock, ome_default_args, mocker):
        param = {"device_id": 25011, "setting_type": "ServerQuickDeploy",
                 "quick_deploy_options": {"ipv4_enabled": False, "ipv4_subnet_mask": "192.168.0.1",
                                          "ipv4_gateway": "0.0.0.0.0"}, "slots": [{"vlan_id": 1}]}
        fields = [("ipv4_subnet_mask", "IPV4"), ("ipv4_gateway", "IPV4"), ("ipv6_gateway", "IPV6")]
        f_module = self.get_module_mock(params=param)
        mocker.patch(MODULE_PATH + "validate_ip_address", return_value=False)
        with pytest.raises(Exception) as err:
            self.module.ip_address_field(f_module, fields, param["quick_deploy_options"], slot=False)
        assert err.value.args[0] == "Invalid '192.168.0.1' address provided for the ipv4_subnet_mask."

    def test_get_device_details(self, ome_conn_mock_qd, ome_response_mock, ome_default_args, mocker):
        param = {"device_id": 25012, "hostname": "192.168.1.6", "setting_type": "ServerQuickDeploy",
                 "quick_deploy_options": {"ipv4_enabled": False, "ipv4_subnet_mask": "192.168.0.1",
                                          "ipv4_gateway": "0.0.0.0"}, "slots": [{"vlan_id": 1}]}
        f_module = self.get_module_mock(params=param)
        ome_response_mock.status_code = 200
        ome_response_mock.success = True
        ome_response_mock.json_data = {"value": [], "SettingType": "ServerQuickDeploy",
                                       "ProtocolTypeV4": "true", "NetworkTypeV4": "Static",
                                       "IpV4Gateway": "192.168.0.1", "IpV4SubnetMask": "255.255.255.0"}
        mocker.patch(MODULE_PATH + 'get_chassis_device', return_value=("Id", 25011))
        mocker.patch(MODULE_PATH + "check_mode_validation", return_value=({}, {}))
        mocker.patch(MODULE_PATH + "job_payload_submission", return_value=12345)
        with pytest.raises(Exception) as err:
            self.module.get_device_details(ome_conn_mock_qd, f_module)
        assert err.value.args[0] == "Unable to complete the operation because the entered " \
                                    "target device id '25012' is invalid."
        param.update({"job_wait": False})
        ome_response_mock.json_data.update({"value": [{"Id": 25012}]})
        f_module = self.get_module_mock(params=param)
        result = self.module.get_device_details(ome_conn_mock_qd, f_module)
        assert result == (12345, None)
        param.update({"job_wait": True})

    def test_job_payload_submission(self, ome_conn_mock_qd, ome_response_mock, ome_default_args):
        ome_response_mock.status_code = 200
        ome_response_mock.success = True
        ome_response_mock.json_data = {"Id": 12345}
        ome_conn_mock_qd.job_submission.return_value = ome_response_mock
        payload = {"ProtocolTypeV4": True, "NetworkTypeV4": "Static", "IpV4SubnetMask": "255.255.255.0",
                   "IpV4Gateway": "0.0.0.0", "ProtocolTypeV6": True, "NetworkTypeV6": "Static",
                   "PrefixLength": "1", "IpV6Gateway": "0.0.0.0"}
        slot_payload = [{"SlotId": 1, "IPV4Address": "192.168.0.2", "IPV6Address": "::", "VlanId": 1}]
        resp_data = {"Slots": [
            {"SlotId": 1, "IPV4Address": "192.168.0.2", "IPV6Address": "::", "VlanId": 1, "SlotSelected": False},
            {"SlotId": 1, "IPV4Address": "192.168.0.2", "IPV6Address": "::", "VlanId": 1, "SlotSelected": False},
        ]}
        result = self.module.job_payload_submission(ome_conn_mock_qd, payload, slot_payload,
                                                    "ServerQuickDeploy", 25012, resp_data)
        assert result == 12345

    def test_check_mode_validation(self, ome_conn_mock_qd, ome_response_mock, ome_default_args):
        param = {"device_id": 25012, "hostname": "192.168.1.6", "setting_type": "ServerQuickDeploy",
                 "quick_deploy_options": {
                     "ipv4_enabled": True, "ipv4_network_type": "Static", "ipv4_subnet_mask": "255.255.255.0",
                     "ipv4_gateway": "0.0.0.0", "ipv6_enabled": True, "ipv6_network_type": "Static",
                     "ipv6_prefix_length": "1", "ipv6_gateway": "0.0.0.0",
                     "slots": [{"slot_id": 1, "slot_ipv4_address": "192.168.0.1",
                                "slot_ipv6_address": "::", "vlan_id": "1"}]}}
        f_module = self.get_module_mock(params=param)
        deploy_data = {"ProtocolTypeV4": True, "NetworkTypeV4": "Static", "IpV4SubnetMask": "255.255.255.0",
                       "IpV4Gateway": "0.0.0.0", "ProtocolTypeV6": True, "NetworkTypeV6": "Static",
                       "PrefixLength": "1", "IpV6Gateway": "0.0.0.0",
                       "Slots": [{"SlotId": 1, "SlotIPV4Address": "192.168.0.1", "SlotIPV6Address": "::", "VlanId": "1"}]}
        with pytest.raises(Exception) as err:
            self.module.check_mode_validation(f_module, deploy_data)
        assert err.value.args[0] == "No changes found to be applied."
        f_module.check_mode = True
        with pytest.raises(Exception) as err:
            self.module.check_mode_validation(f_module, deploy_data)
        assert err.value.args[0] == "No changes found to be applied."
        param["quick_deploy_options"]["ipv6_prefix_length"] = "2"
        with pytest.raises(Exception) as err:
            self.module.check_mode_validation(f_module, deploy_data)
        assert err.value.args[0] == "Changes found to be applied."
        f_module.check_mode = False
        result = self.module.check_mode_validation(f_module, deploy_data)
        assert result[0]["NetworkTypeV4"] == "Static"

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_device_power_main_exception_case(self, exc_type, mocker, ome_default_args,
                                                  ome_conn_mock_qd, ome_response_mock):
        ome_default_args.update({"device_id": 25011, "setting_type": "ServerQuickDeploy", "validate_certs": False,
                                 "quick_deploy_options": {"ipv4_enabled": False,
                                                          "slots": [{"slot_id": 1, "vlan_id": 1}]}})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'check_domain_service', side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'check_domain_service', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'check_domain_service',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result
