# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.2.0
# Copyright (C) 2021-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
import pdb

import pytest
from ssl import SSLError
from io import StringIO
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils._text import to_text
from ansible_collections.dellemc.openmanage.plugins.modules import ome_device_network_services
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from mock import MagicMock, patch, Mock

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_device_network_services.'


@pytest.fixture
def ome_conn_mock_network(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOMEMDeviceNetworkService(FakeAnsibleModule):

    module = ome_device_network_services

    def test_check_domain_service(self, ome_conn_mock_network, ome_default_args):
        f_module = self.get_module_mock()
        result = self.module.check_domain_service(f_module, ome_conn_mock_network)
        assert result is None

    def test_check_domain_service_http(self, ome_conn_mock_network, ome_default_args, mocker):
        f_module = self.get_module_mock()
        err_message = {'error': {'@Message.ExtendedInfo': [{'MessageId': 'CGEN1006'}]}}
        ome_conn_mock_network.invoke_request.side_effect = HTTPError('http://testhost.com', 400,
                                                                     json.dumps(err_message),
                                                                     {"accept-type": "application/json"}, None)
        mocker.patch(MODULE_PATH + 'json.loads', return_value=err_message)
        with pytest.raises(Exception) as err:
            self.module.check_domain_service(f_module, ome_conn_mock_network)
        assert err.value.args[0] == "The device location settings operation is supported only on " \
                                    "OpenManage Enterprise Modular."

    def test_get_chassis_device(self, ome_conn_mock_network, ome_default_args, mocker, ome_response_mock):
        mocker.patch(MODULE_PATH + "get_ip_from_host", return_value="192.18.1.1")
        ome_response_mock.json_data = {"value": [{"DeviceId": 25011, "DomainRoleTypeValue": "LEAD",
                                                  "PublicAddress": ["192.168.1.1"]},
                                                 {"DeviceId": 25012, "DomainRoleTypeValue": "STANDALONE",
                                                  "PublicAddress": ["192.168.1.2"]}]}
        param = {"device_id": 25012, "hostname": "192.168.1.6", "remote_racadm_settings": {"enabled": True}}
        f_module = self.get_module_mock(params=param)
        with pytest.raises(Exception) as err:
            self.module.get_chassis_device(f_module, ome_conn_mock_network)
        assert err.value.args[0] == "Failed to retrieve the device information."
        ome_response_mock.json_data = {"value": [{"DeviceId": 25011, "DomainRoleTypeValue": "LEAD",
                                                  "PublicAddress": ["192.18.1.1"]}]}
        param = {"hostname": "192.18.1.1", "remote_racadm_settings": {"enabled": True}}
        f_module = self.get_module_mock(params=param)
        key, value = self.module.get_chassis_device(f_module, ome_conn_mock_network)
        assert key == "Id"
        assert value == 25011

    def test_main_validation(self, ome_conn_mock_network, ome_default_args, ome_response_mock, mocker):
        resp = self._run_module_with_fail_json(ome_default_args)
        assert resp['msg'] == "one of the following is required: snmp_settings, " \
                              "ssh_settings, remote_racadm_settings"
        mocker.patch(MODULE_PATH + "check_domain_service", return_value=None)
        mocker.patch(MODULE_PATH + "fetch_device_details", return_value=ome_response_mock)
        ome_response_mock.json_data = {"value": [{"Id": 25011, "DeviceServiceTag": "XE3FRS"}],
                                       "EnableRemoteRacadm": True, "SettingType": "NetworkServices",
                                       "SnmpConfiguration": {"PortNumber": 161, "SnmpEnabled": True,
                                                             "SnmpV1V2Credential": {"CommunityName": "public"}},
                                       "SshConfiguration": {"IdleTimeout": 60, "MaxAuthRetries": 3, "MaxSessions": 1,
                                                            "PortNumber": 22, "SshEnabled": False}}
        ome_default_args.update({"device_id": 25012, "hostname": "192.168.1.6", "remote_racadm_settings": {"enabled": True},
                                 "snmp_settings": {"enabled": True, "port_number": 161, "community_name": "public"},
                                 "ssh_settings": {"enabled": True, "port_number": 22, "max_sessions": 1,
                                                  "max_auth_retries": 3, "idle_timeout": 60}})
        resp = self._run_module(ome_default_args)
        assert resp['msg'] == "Successfully updated the network services settings."

    def test_fetch_device_details(self, ome_conn_mock_network, ome_default_args, ome_response_mock, mocker):
        param = {"device_id": 25012, "hostname": "192.168.1.6", "remote_racadm_settings": {"enabled": True}}
        f_module = self.get_module_mock(params=param)
        ome_response_mock.status_code = 200
        ome_response_mock.success = True
        ome_response_mock.json_data = {"value": [{"Id": 25011, "DeviceServiceTag": "XE3FRS"}],
                                       "EnableRemoteRacadm": True, "SettingType": "NetworkServices",
                                       "SnmpConfiguration": {"PortNumber": 161, "SnmpEnabled": True,
                                                             "SnmpV1V2Credential": {"CommunityName": "public"}},
                                       "SshConfiguration": {"IdleTimeout": 60, "MaxAuthRetries": 3, "MaxSessions": 1,
                                                            "PortNumber": 22, "SshEnabled": False}}
        with pytest.raises(Exception) as err:
            self.module.fetch_device_details(f_module, ome_conn_mock_network)
        assert err.value.args[0] == "Unable to complete the operation because the entered target " \
                                    "device id '25012' is invalid."
        ome_response_mock.strip_substr_dict.return_value = {"EnableRemoteRacadm": True}
        ome_response_mock.json_data = {"value": [{"Id": 25012, "DeviceServiceTag": "XE3FRS"}],
                                       "EnableRemoteRacadm": True, "SnmpConfiguration": {}, "SshConfiguration": {}}
        resp = self.module.fetch_device_details(f_module, ome_conn_mock_network)
        assert resp.json_data["SnmpConfiguration"] == {}
        param = {"hostname": "192.168.1.6", "remote_racadm_settings": {"enabled": True}}
        f_module = self.get_module_mock(params=param)
        mocker.patch(MODULE_PATH + "get_chassis_device", return_value=("Id", "25012"))
        resp = self.module.fetch_device_details(f_module, ome_conn_mock_network)
        assert resp.json_data["SnmpConfiguration"] == {}

    def test_get_ip_from_host(self, ome_conn_mock_network, ome_default_args, ome_response_mock):
        result = self.module.get_ip_from_host("192.168.0.1")
        assert result == "192.168.0.1"

    def test_check_mode_validation(self, ome_conn_mock_network, ome_default_args, ome_response_mock):
        param = {"device_id": 25012, "hostname": "192.168.1.6", "remote_racadm_settings": {"enabled": True},
                 "snmp_settings": {"enabled": True, "port_number": 161, "community_name": "public"},
                 "ssh_settings": {"enabled": True, "port_number": 22, "max_sessions": 1,
                                  "max_auth_retries": 3, "idle_timeout": 120}}
        f_module = self.get_module_mock(params=param)
        loc_data = {"EnableRemoteRacadm": True, "SettingType": "NetworkServices",
                    "SnmpConfiguration": {"PortNumber": 161, "SnmpEnabled": True,
                                          "SnmpV1V2Credential": {"CommunityName": "public"}},
                    "SshConfiguration": {"IdleTimeout": 7200, "MaxAuthRetries": 3, "MaxSessions": 1,
                                         "PortNumber": 22, "SshEnabled": True}}
        with pytest.raises(Exception) as err:
            self.module.check_mode_validation(f_module, loc_data, ome_conn_mock_network)
        assert err.value.args[0] == "No changes found to be applied."
        f_module.check_mode = True
        loc_data["SshConfiguration"]["IdleTimeout"] = 7200
        with pytest.raises(Exception) as err:
            self.module.check_mode_validation(f_module, loc_data, ome_conn_mock_network)
        assert err.value.args[0] == "No changes found to be applied."
        loc_data = {"EnableRemoteRacadm": True, "SettingType": "NetworkServices",
                    "SnmpConfiguration": {"PortNumber": 161, "SnmpEnabled": False,
                                          "SnmpV1V2Credential": {"CommunityName": "public"}},
                    "SshConfiguration": {"IdleTimeout": 60, "MaxAuthRetries": 3, "MaxSessions": 1,
                                         "PortNumber": 22, "SshEnabled": False}}
        with pytest.raises(Exception) as err:
            self.module.check_mode_validation(f_module, loc_data, ome_conn_mock_network)
        assert err.value.args[0] == "Changes found to be applied."
        param = {"device_id": 25012, "hostname": "192.168.1.6", "remote_racadm_settings": {"enabled": False},
                 "snmp_settings": {"enabled": False, "port_number": 161, "community_name": "public"},
                 "ssh_settings": {"enabled": False, "port_number": 22, "max_sessions": 1,
                                  "max_auth_retries": 3, "idle_timeout": 60}}
        f_module = self.get_module_mock(params=param)
        resp = self.module.check_mode_validation(f_module, loc_data, ome_conn_mock_network)
        assert resp["SnmpConfiguration"]["PortNumber"] == 161

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_device_network_main_exception_case(self, exc_type, mocker, ome_default_args,
                                                    ome_conn_mock_network, ome_response_mock):
        ome_default_args.update({"device_id": 25011, "remote_racadm_settings": {"enabled": True}})
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
