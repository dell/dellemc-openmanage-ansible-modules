# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.8.0
# Copyright (C) 2024 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible_collections.dellemc.openmanage.plugins.module_utils.rest_api import RestAPI, OpenURLResponse
from mock import MagicMock
import json

MODULE_UTIL_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.'
OMEVV_OPENURL = 'rest_api.open_url'
TEST_PATH = "/testpath"
INVOKE_REQUEST = 'rest_api.RestAPI._base_invoke_request'
JOB_SUBMISSION = 'rest_api.RestAPI.job_submission'
DEVICE_API = "DeviceService/Devices"
TEST_HOST = 'https://testhost.com/'
BAD_REQUEST = 'Bad Request Error'
ODATA_COUNT = "@odata.count"
ODATA_TYPE = "@odata.type"
DDEVICE_TYPE = "#DeviceService.DeviceType"
URI = "/uri/v1"

class TestRestAPI(object):

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
        module_parameters = {'hostname': 'xxx.xxx.x.x', 'username': 'username',
                             'password': 'password', "port": 443}
        return module_parameters

    @pytest.fixture
    def ome_object(self, module_params):
        ome_obj = RestAPI(module_params=module_params)
        return ome_obj

    def test_invoke_request_with_session(self, mock_response, mocker):

        mocker.patch(MODULE_UTIL_PATH + OMEVV_OPENURL,
                     return_value=mock_response)
        module_params = {'hostname': '[2001:db8:3333:4444:5555:6666:7777:8888]', 'username': 'username',
                         'password': 'password', "port": 443}
        req_session = True
        with RestAPI(URI, module_params, req_session) as obj:
            response = obj._base_invoke_request(TEST_PATH, "GET")
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    def test_invoke_request_without_session(self, mock_response, mocker, module_params):
        mocker.patch(MODULE_UTIL_PATH + OMEVV_OPENURL,
                     return_value=mock_response)
        with RestAPI(URI, module_params) as obj:
            response = obj._base_invoke_request(TEST_PATH, "GET")
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    def test_invoke_request_without_session_with_header(self, mock_response, mocker, module_params):
        mocker.patch(MODULE_UTIL_PATH + OMEVV_OPENURL,
                     return_value=mock_response)
        with RestAPI(URI, module_params) as obj:
            response = obj._base_invoke_request(TEST_PATH, "POST",
                                                headers={"application": "octstream"})
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    @pytest.mark.parametrize("exc", [URLError, SSLValidationError, ConnectionError])
    def test_invoke_request_error_case_handling(self, exc, mock_response, mocker, module_params):
        open_url_mock = mocker.patch(MODULE_UTIL_PATH + OMEVV_OPENURL,
                                     return_value=mock_response)
        open_url_mock.side_effect = exc("test")
        req_session = True
        with pytest.raises(exc):
            with RestAPI(URI, module_params, req_session) as obj:
                obj._base_invoke_request(TEST_PATH, "GET")

    def test_invoke_request_http_error_handling(self, mock_response, mocker, module_params):
        open_url_mock = mocker.patch(MODULE_UTIL_PATH + OMEVV_OPENURL,
                                     return_value=mock_response)
        open_url_mock.side_effect = HTTPError(TEST_HOST, 400,
                                              BAD_REQUEST, {}, None)
        with pytest.raises(HTTPError):
            with RestAPI(URI, module_params) as obj:
                obj._base_invoke_request(TEST_PATH, "GET")

    @pytest.mark.parametrize("query_param", [
        {"inp": {"$filter": "UserName eq 'admin'"},
            "out": "%24filter=UserName%20eq%20%27admin%27"},
        {"inp": {"$top": 1, "$skip": 2, "$filter": "JobType/Id eq 8"}, "out":
            "%24top=1&%24skip=2&%24filter=JobType%2FId%20eq%208"},
        {"inp": {"$top": 1, "$skip": 3}, "out": "%24top=1&%24skip=3"}
    ])
    def test_build_url(self, query_param, mocker, module_params):
        """builds complete url"""
        base_uri = "https://xxx.xxx.x.x:443"
        path = "/AccountService/Accounts"
        inp = query_param["inp"]
        out = query_param["out"]
        url = RestAPI("url/v1", module_params)._RestAPI__build_url(
            path, query_param=inp)
        assert url == base_uri + path + "?" + out
        assert "+" not in url

    def test_invalid_json_openurlresp(self):
        obj = OpenURLResponse({})
        obj.body = 'invalid json'
        with pytest.raises(ValueError) as e:
            obj.json_data
        assert e.value.args[0] == "Unable to parse json"
