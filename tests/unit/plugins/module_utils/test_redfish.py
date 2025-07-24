# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.3
# Copyright (C) 2023-2025 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import io
import sys
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible_collections.dellemc.openmanage.plugins.module_utils.redfish \
    import Redfish, OpenURLResponse, RedfishAnsibleModule
from unittest.mock import MagicMock, patch
import json

MODULE_UTIL_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.'
OPEN_URL = 'redfish.open_url'
TEST_PATH = "/testpath"
MANAGER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"


class TestRedfishRest(object):

    @pytest.fixture
    def mock_response(self):
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = mock_response.getheaders.return_value = {
            'X-Auth-Token': 'token_id'}
        mock_response.read.return_value = json.dumps({"value": "data"})
        return mock_response

    @pytest.fixture
    def module_params(self):
        module_parameters = {'baseuri': 'xxx.xxx.x.x:443', 'username': 'username',
                             'password': 'password'}
        return module_parameters

    @pytest.fixture
    def redfish_object(self, module_params):
        redfish_obj = Redfish(module_params=module_params)
        return redfish_obj

    def mock_get_dynamic_redfish_invoke_request(self, *args, **kwargs):
        obj = MagicMock()
        obj.status_code = 200
        obj.success = True
        if 'path' in kwargs and kwargs['path'] == MANAGER_URI:
            obj.json_data = {'Model': '17G Monolithic',
                             'FirmwareVersion': 'x.x.x.x'}
        else:
            obj.json_data = {'Attributes': {'Info.1.HWModel': 'iDRAC 10'}}
        return obj

    def test_get_server_generation(self, mocker, module_params):
        mocker.patch(MODULE_UTIL_PATH + 'redfish.Redfish.invoke_request', self.mock_get_dynamic_redfish_invoke_request)
        req_session = False
        module_params.update({'x_auth_token': 'token_id'})
        with Redfish(module_params, req_session) as obj:
            response = obj.get_server_generation
        assert response == (17, 'x.x.x.x', 'iDRAC 10')

    def test_invoke_request_with_session_with_header(self, mock_response, mocker, module_params):
        Redfish.get_server_generation = [12]
        mocker.patch(MODULE_UTIL_PATH + OPEN_URL,
                     return_value=mock_response)
        req_session = False
        module_params.update({'x_auth_token': 'token_id'})
        with Redfish(module_params, req_session) as obj:
            response = obj.invoke_request(TEST_PATH, "GET", headers={
                                          "application": "octstream"})
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    def test_invoke_request_without_session(self, mock_response, mocker):
        mocker.patch(MODULE_UTIL_PATH + OPEN_URL,
                     return_value=mock_response)
        mocker.patch(MODULE_UTIL_PATH + OPEN_URL,
                     return_value=mock_response)
        module_params = {'baseuri': '[2001:db8:3333:4444:5555:6666:7777:8888]:443', 'username': 'username',
                         'password': 'password', "port": 443}
        req_session = False
        with Redfish(module_params, req_session) as obj:
            response = obj.invoke_request(TEST_PATH, "GET")
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True
        assert response.headers == {"X-Auth-Token": "token_id"}

    def test_invoke_request_with_session(self, mock_response, mocker, module_params):
        mocker.patch(MODULE_UTIL_PATH + OPEN_URL,
                     return_value=mock_response)
        req_session = True
        with Redfish(module_params, req_session) as obj:
            response = obj.invoke_request(TEST_PATH, "GET")
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    def test_invoke_request_without_session(self, mock_response, mocker):
        mocker.patch(MODULE_UTIL_PATH + OPEN_URL,
                     return_value=mock_response)
        module_params = {'baseuri': '[2001:db8:3333:4444:5555:6666:7777:8888]:443', 'username': 'username',
                         'password': 'password', "port": 443}
        req_session = False
        with Redfish(module_params, req_session) as obj:
            response = obj.invoke_request(TEST_PATH, "GET")
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    def test_invoke_request_without_session_with_header(self, mock_response, mocker, module_params):
        mocker.patch(MODULE_UTIL_PATH + OPEN_URL,
                     return_value=mock_response)
        req_session = False
        with Redfish(module_params, req_session) as obj:
            response = obj.invoke_request(TEST_PATH, "POST", headers={
                                          "application": "octstream"})
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    def test_invoke_request_with_session_connection_error(self, mocker, mock_response, module_params):
        mock_response.success = False
        mock_response.status_code = 500
        mock_response.json_data = {}
        mocker.patch(MODULE_UTIL_PATH + 'redfish.Redfish.invoke_request',
                     return_value=mock_response)
        req_session = True
        with pytest.raises(ConnectionError):
            with Redfish(module_params, req_session) as obj:
                obj.invoke_request(TEST_PATH, "GET")

    @pytest.mark.parametrize("exc", [URLError, SSLValidationError, ConnectionError])
    def test_invoke_request_error_case_handling(self, exc, mock_response, mocker, module_params):
        mocker.patch(MODULE_UTIL_PATH + OPEN_URL,
                     side_effect=exc("test"))
        req_session = False
        with pytest.raises(exc):
            with Redfish(module_params, req_session) as obj:
                obj.invoke_request(TEST_PATH, "GET")

    def test_invoke_request_http_error_handling(self, mock_response, mocker, module_params):
        open_url_mock = mocker.patch(MODULE_UTIL_PATH + OPEN_URL,
                                     return_value=mock_response)
        open_url_mock.side_effect = HTTPError('https://testhost.com/', 400,
                                              'Bad Request Error', {}, None)
        req_session = False
        with pytest.raises(HTTPError):
            with Redfish(module_params, req_session) as obj:
                obj.invoke_request(TEST_PATH, "GET")

    @pytest.mark.parametrize("query_params", [
        {"inp": {"$filter": "UserName eq 'admin'"},
            "out": "%24filter=UserName+eq+%27admin%27"},
        {"inp": {"$top": 1, "$skip": 2, "$filter": "JobType/Id eq 8"}, "out":
            "%24top=1&%24skip=2&%24filter=JobType%2FId+eq+8"},
        {"inp": {"$top": 1, "$skip": 3}, "out": "%24top=1&%24skip=3"}
    ])
    def test_build_url(self, query_params, mocker, redfish_object):
        """builds complete url"""
        base_uri = 'https://xxx.xxx.x.x:443/api'
        path = "/AccountService/Accounts"
        mocker.patch(MODULE_UTIL_PATH + 'redfish.Redfish._get_base_url',
                     return_value=base_uri)
        inp = query_params["inp"]
        out = query_params["out"]
        url = redfish_object._build_url(
            path, query_param=inp)
        assert url == base_uri + path + "?" + out

    def test_build_url_none(self, mocker, redfish_object):
        """builds complete url"""
        base_uri = 'https://xxx.xxx.x.x:443/api'
        mocker.patch(MODULE_UTIL_PATH + 'redfish.Redfish._get_base_url',
                     return_value=base_uri)
        url = redfish_object._build_url("", None)
        assert url == ""

    def test_strip_substr_dict(self, mocker, mock_response, redfish_object):
        data_dict = {"@odata.context": "/api/$metadata#Collection(DeviceService.DeviceType)",
                     "@odata.count": 5,
                     "value": [
                         {
                             "@odata.type": "#DeviceService.DeviceType",
                             "DeviceType": 1000,
                             "Name": "SERVER",
                             "Description": "Server Device"
                         }
                     ]}
        ret = redfish_object.strip_substr_dict(data_dict)
        assert ret == {'value': [{'@odata.type': '#DeviceService.DeviceType',
                                  'Description': 'Server Device', 'DeviceType': 1000, 'Name': 'SERVER'}]}

    def test_invalid_json_openurlresp(self):
        obj = OpenURLResponse({})
        obj.body = 'invalid json'
        with pytest.raises(ValueError) as e:
            obj.json_data
        assert e.value.args[0] == "Unable to parse json"

    def test_reason(self):
        def mock_read():
            return "{}"
        obj = MagicMock()
        obj.reason = "returning reason"
        obj.read = mock_read
        ourl = OpenURLResponse(obj)
        reason_ret = ourl.reason
        assert reason_ret == "returning reason"


class TestRedfishAnsibleModule:
    def test_redfish_module_initialization(self):
        # Simulate Ansible JSON input
        fake_input = json.dumps({
            "baseuri": "https://example.com",
            "username": "admin",
            "password": "secret"
        }).encode('utf-8')

        # Create a binary stream and wrap it with a text wrapper
        fake_stdin = io.TextIOWrapper(io.BytesIO(fake_input), encoding='utf-8')

        with patch.object(sys, 'stdin', fake_stdin):
            with pytest.raises(SystemExit) as ex:
                RedfishAnsibleModule(argument_spec={}, bypass_checks=True)

            # AnsibleModule exits after parsing input
            assert ex.type == SystemExit
