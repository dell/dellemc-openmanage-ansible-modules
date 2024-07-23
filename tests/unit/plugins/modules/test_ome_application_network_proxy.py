# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.5.0
# Copyright (C) 2019-2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json

import pytest
from urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text
from ansible_collections.dellemc.openmanage.plugins.modules import ome_application_network_proxy
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.modules.ome_application_network_proxy import main

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
CHECK_MODE_CHANGE_FOUND_MSG = "Changes found to be applied."
CHECK_MODE_CHANGE_NOT_FOUND_MSG = "No Changes found to be applied."
NO_PROXY_CONFIGURATION = "Unable to configure the proxy because proxy configuration settings " \
                         "are not provided."
NO_CHANGE_IN_CONFIGURATION = "No changes made to proxy configuration as entered values are the " \
                             "same as current configuration values"


@pytest.fixture
def ome_connection_mock_for_application_network_proxy(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'ome_application_network_proxy.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    ome_connection_mock_obj.get_all_report_details.return_value = {"report_list": []}
    return ome_connection_mock_obj


class TestOmeTemplate(FakeAnsibleModule):
    module = ome_application_network_proxy

    sub_param1 = {"enable_proxy": True, "ip_address": "255.0.0.0", "proxy_port": 443, "proxy_username": "username",
                  "proxy_password": "password",
                  "enable_authentication": True,
                  "proxy_exclusion_list": []}
    sub_param2 = {"enable_proxy": False}

    @pytest.mark.parametrize("sub_param", [sub_param1, sub_param2])
    def test_ome_application_network_proxy_main_success_case_01(self, mocker, ome_default_args, sub_param,
                                                                ome_connection_mock_for_application_network_proxy,
                                                                ome_response_mock):
        ome_default_args.update(sub_param)
        mocker.patch(MODULE_PATH + "ome_application_network_proxy.get_payload", return_value={"key": "val"})
        mocker.patch(MODULE_PATH + "ome_application_network_proxy.get_updated_payload", return_value={"key": "val"})
        ome_response_mock.json_data = {"EnableProxy": True, "IpAddress": "255.0.0.0", "PortNumber": 443,
                                       "Username": "username", "Password": "password", "EnableAuthentication": True}
        result = self._run_module(ome_default_args)
        assert result['changed'] is True
        assert "msg" in result
        assert "proxy_configuration" in result and result["proxy_configuration"] == {"EnableProxy": True,
                                                                                     "IpAddress": "255.0.0.0",
                                                                                     "PortNumber": 443,
                                                                                     "Username": "username",
                                                                                     "Password": "password",
                                                                                     "EnableAuthentication": True,
                                                                                     "ProxyExclusionList": []}
        assert result["msg"] == "Successfully updated network proxy configuration."

    sub_param1 = {"param": {"enable_proxy": True, "ip_address": "255.0.0.0"},
                  "msg": 'enable_proxy is True but all of the following are missing: proxy_port'}
    sub_param2 = {"param": {"enable_proxy": True, "proxy_port": 443},
                  "msg": 'enable_proxy is True but all of the following are missing: ip_address'}
    sub_param3 = {"param": {"enable_proxy": True},
                  "msg": 'enable_proxy is True but all of the following are missing: ip_address, proxy_port'}
    sub_param4 = {"param": {}, "msg": 'missing required arguments: enable_proxy'}

    @pytest.mark.parametrize("param", [sub_param1, sub_param2, sub_param3, sub_param4])
    def test_ome_application_network_proxy_main_failure_case_01(self, mocker, ome_default_args, param,
                                                                ome_connection_mock_for_application_network_proxy,
                                                                ome_response_mock):
        sub_param = param["param"]
        msg = param["msg"]
        ome_default_args.update(sub_param)
        result = self._run_module_with_fail_json(ome_default_args)
        assert result["msg"] == msg
        assert "proxy_configuration" not in result
        assert result["failed"] is True

    sub_param1 = {
        "param": {"enable_proxy": True, "proxy_port": 443, "ip_address": "255.0.0.0", "enable_authentication": True,
                  "proxy_username": "255.0.0.0"},
        "msg": 'enable_authentication is True but all of the following are missing: proxy_password'}
    sub_param2 = {
        "param": {"enable_proxy": True, "proxy_port": 443, "ip_address": "255.0.0.0", "enable_authentication": True,
                  "proxy_password": 443},
        "msg": 'enable_authentication is True but all of the following are missing: proxy_username'}
    sub_param3 = {
        "param": {"enable_proxy": True, "proxy_port": 443, "ip_address": "255.0.0.0", "enable_authentication": True},
        "msg": 'enable_authentication is True but all of the following are missing: proxy_username, proxy_password'}

    @pytest.mark.parametrize("param", [sub_param1, sub_param2, sub_param3])
    def test_ome_application_network_proxy_main_failure_case_02(self, mocker, ome_default_args, param,
                                                                ome_connection_mock_for_application_network_proxy,
                                                                ome_response_mock):
        sub_param = param["param"]
        msg = param["msg"]
        ome_default_args.update(sub_param)
        result = self._run_module_with_fail_json(ome_default_args)
        assert result["msg"] == msg
        assert "proxy_configuration" not in result
        assert result["failed"] is True

    @pytest.mark.parametrize("exc_type",
                             [ValueError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_application_network_proxy_main_success_failure_case3(self, exc_type, mocker, ome_default_args,
                                                                      ome_connection_mock_for_application_network_proxy,
                                                                      ome_response_mock):
        ome_default_args.update({"enable_proxy": False})
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'ome_application_network_proxy.get_payload',
                         side_effect=exc_type("TEST"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'ome_application_network_proxy.get_payload',
                         side_effect=exc_type("exception message"))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'ome_application_network_proxy.get_payload',
                         side_effect=exc_type('https://testhost.com', 400,
                                              'http error message',
                                              {"accept-type": "application/json"},
                                              StringIO(json_str)))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
        assert 'proxy_configuration' not in result
        assert 'msg' in result

    def test_remove_unwanted_keys(self, ome_default_args):
        removable_keys = list(ome_default_args.keys())
        new_param = {
            "ip_address": "IpAddress",
            "proxy_port": "PortNumber",
            "enable_proxy": "EnableProxy",
            "proxy_username": "Username",
            "proxy_password": "Password",
            "enable_authentication": "EnableAuthentication"
        }
        ome_default_args.update(new_param)
        self.module.remove_unwanted_keys(removable_keys, ome_default_args)
        assert len(set(new_param.keys()) - set(ome_default_args.keys())) == 0

    def test_remove_unwanted_keys_case2(self):
        """when key not exists should not throw error"""
        current_setting = {"@odata.context": "context", "@odata.type": "data_type", "@odata.id": "@odata.id"}
        removable_keys = ["@odata.context", "@odata.type", "@odata.id", "Password"]
        self.module.remove_unwanted_keys(removable_keys, current_setting)
        assert len(current_setting) == 0

    def test_get_payload(self, ome_default_args):
        new_param = {
            "ip_address": "YY.YY.YY.YY",
            "proxy_port": 443,
            "enable_proxy": True,
            "proxy_username": "username",
            "proxy_password": "password",
            "enable_authentication": False,
            "port": 443
        }
        ome_default_args.update(new_param)
        f_module = self.get_module_mock(params=ome_default_args)
        payload = self.module.get_payload(f_module)
        assert ome_default_args == {"ip_address": "YY.YY.YY.YY",
                                    "proxy_port": 443,
                                    "enable_proxy": True,
                                    "proxy_username": "username",
                                    "proxy_password": "password",
                                    "enable_authentication": False,
                                    "hostname": "XX.XX.XX.XX",
                                    "username": "username",
                                    "password": "password",
                                    "port": 443,
                                    "ca_path": "/path/ca_bundle"}
        assert payload == {"EnableProxy": True, "IpAddress": "YY.YY.YY.YY", "PortNumber": 443, "Username": "username",
                           "Password": "password", "EnableAuthentication": False}

    def test_get_updated_payload_success_case(self, mocker, ome_default_args, ome_connection_mock_for_application_network_proxy,
                                              ome_response_mock):
        current_setting = {"@odata.context": "/api/$metadata#Network.ProxyConfiguration",
                           "@odata.type": "#Network.ProxyConfiguration",
                           "@odata.id": "/api/ApplicationService/Network/ProxyConfiguration", "IpAddress": "255.0.0.0",
                           "PortNumber": 443, "EnableAuthentication": False, "EnableProxy": True,
                           "Username": "username1", "Password": "password1"}
        payload = {"EnableAuthentication": True, "IpAddress": "XX.XX.XX.XX", "PortNumber": 443, 'EnableProxy': True,
                   'Username': 'username2', "Password": "password2"}
        f_module = self.get_module_mock(params=ome_default_args)
        ome_response_mock.json_data = current_setting
        mocker.patch(MODULE_PATH + "ome_application_network_proxy.validate_check_mode_for_network_proxy",
                     return_value=None)
        setting = self.module.get_updated_payload(ome_connection_mock_for_application_network_proxy, f_module, payload)
        assert setting == payload

    def test_get_updated_payload_enable_auth_disable_success_case(self, mocker, ome_default_args,
                                                                  ome_connection_mock_for_application_network_proxy,
                                                                  ome_response_mock):
        """when EnableAuthentication is False setting will not have Password and UserName even if its passed"""
        ome_default_args.update(
            {"enable_authentication": False, "proxy_username": 'username2', "proxy_password": "password2"})
        current_setting = {"@odata.context": "/api/$metadata#Network.ProxyConfiguration",
                           "@odata.type": "#Network.ProxyConfiguration",
                           "@odata.id": "/api/ApplicationService/Network/ProxyConfiguration", "IpAddress": "255.0.0.0",
                           "PortNumber": 443, "EnableAuthentication": True, "EnableProxy": True,
                           "Username": "username1", "Password": "password1"}
        payload = {"EnableAuthentication": False, "IpAddress": "XX.XX.XX.XX", "PortNumber": 443, 'EnableProxy': True,
                   'Username': 'username2', "Password": "password2"}
        f_module = self.get_module_mock(params=ome_default_args)
        ome_response_mock.json_data = current_setting
        mocker.patch(MODULE_PATH + "ome_application_network_proxy.validate_check_mode_for_network_proxy",
                     return_value=None)
        setting = self.module.get_updated_payload(ome_connection_mock_for_application_network_proxy, f_module, payload)
        assert setting == {"EnableAuthentication": False, "IpAddress": "XX.XX.XX.XX", "PortNumber": 443,
                           'EnableProxy': True}

    def test_get_updated_payload_when_same_setting_failure_case1(self, mocker, ome_default_args,
                                                                 ome_connection_mock_for_application_network_proxy,
                                                                 ome_response_mock):
        current_setting = {"@odata.context": "/api/$metadata#Network.ProxyConfiguration",
                           "@odata.type": "#Network.ProxyConfiguration",
                           "@odata.id": "/api/ApplicationService/Network/ProxyConfiguration", "IpAddress": "255.0.0.0",
                           "PortNumber": 443, "EnableAuthentication": False, "EnableProxy": True,
                           "Username": "username", "Password": "password"}
        payload = {"IpAddress": "255.0.0.0", "PortNumber": 443, "EnableAuthentication": False, "EnableProxy": True,
                   "Username": "username", "Password": "password"}
        f_module = self.get_module_mock(params=ome_default_args)
        ome_response_mock.json_data = current_setting
        error_message = NO_CHANGE_IN_CONFIGURATION
        mocker.patch(MODULE_PATH + "ome_application_network_proxy.validate_check_mode_for_network_proxy",
                     return_value=None)
        with pytest.raises(Exception, match=error_message) as err:
            self.module.get_updated_payload(ome_connection_mock_for_application_network_proxy, f_module, payload)

    def test_get_updated_payload_when_same_setting_failure_case2(self, mocker, ome_default_args,
                                                                 ome_connection_mock_for_application_network_proxy,
                                                                 ome_response_mock):
        """Password are ignored for difference check in payload"""
        current_setting = {"@odata.context": "/api/$metadata#Network.ProxyConfiguration",
                           "@odata.type": "#Network.ProxyConfiguration",
                           "@odata.id": "/api/ApplicationService/Network/ProxyConfiguration", "IpAddress": "255.0.0.0",
                           "PortNumber": 443, "EnableAuthentication": False, "EnableProxy": True,
                           "Username": "username", "Password": "password1"}
        payload = {"IpAddress": "255.0.0.0", "PortNumber": 443, "EnableAuthentication": False, "EnableProxy": True,
                   "Username": "username", "Password": "password2"}
        f_module = self.get_module_mock(params=ome_default_args)
        ome_response_mock.json_data = current_setting
        error_message = NO_CHANGE_IN_CONFIGURATION
        mocker.patch(MODULE_PATH + "ome_application_network_proxy.validate_check_mode_for_network_proxy",
                     return_value=None)
        with pytest.raises(Exception, match=error_message) as err:
            self.module.get_updated_payload(ome_connection_mock_for_application_network_proxy, f_module, payload)

    def test_get_updated_payload_when_no_diff_failure_case(self, mocker, ome_default_args,
                                                           ome_connection_mock_for_application_network_proxy,
                                                           ome_response_mock):
        current_setting = {"@odata.context": "/api/$metadata#Network.ProxyConfiguration",
                           "@odata.type": "#Network.ProxyConfiguration",
                           "@odata.id": "/api/ApplicationService/Network/ProxyConfiguration", "IpAddress": "255.0.0.0",
                           "PortNumber": 443, "EnableAuthentication": False, "EnableProxy": True,
                           "Username": "username", "Password": "password"}
        payload = {}
        f_module = self.get_module_mock(params=ome_default_args)
        ome_response_mock.json_data = current_setting
        error_message = NO_PROXY_CONFIGURATION
        mocker.patch(MODULE_PATH + "ome_application_network_proxy.validate_check_mode_for_network_proxy",
                     return_value=None)
        with pytest.raises(Exception, match=error_message) as err:
            self.module.get_updated_payload(ome_connection_mock_for_application_network_proxy, f_module, payload)

    def test_validate_check_mode_for_network_proxy_case01(self):
        f_module = self.get_module_mock(params={}, check_mode=True)
        with pytest.raises(Exception, match=CHECK_MODE_CHANGE_FOUND_MSG):
            self.module.validate_check_mode_for_network_proxy(True, f_module)

    def test_validate_check_mode_for_network_proxy_case02(self):
        f_module = self.get_module_mock(params={}, check_mode=True)
        with pytest.raises(Exception, match=CHECK_MODE_CHANGE_NOT_FOUND_MSG):
            self.module.validate_check_mode_for_network_proxy(False, f_module)

    def test_validate_check_mode_for_network_proxy_case03(self):
        f_module = self.get_module_mock(params={}, check_mode=False)
        self.module.validate_check_mode_for_network_proxy(True, f_module)

    def test_validate_check_mode_for_network_proxy_case04(self):
        f_module = self.get_module_mock(params={}, check_mode=False)
        self.module.validate_check_mode_for_network_proxy(False, f_module)

    def test_main(self, mocker):
        module_mock = mocker.MagicMock()

        mocker.patch(MODULE_PATH + "ome_application_network_proxy.OmeAnsibleModule", return_value=module_mock)
        main()
