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
import json
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv import RestOMEVV, OMEVVAnsibleModule, AnsibleModule
from unittest.mock import MagicMock

MODULE_UTIL_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.'
OMEVV_OPENURL = 'omevv.RestOMEVV._base_invoke_request'
TEST_PATH = "/testpath"
INVOKE_REQUEST = 'omevv.RestOMEVV.invoke_request'
JOB_SUBMISSION = 'omevv.RestOMEVV.job_submission'
DEVICE_API = "DeviceService/Devices"
TEST_HOST = 'https://testhost.com/'
BAD_REQUEST = 'Bad Request Error'
ODATA_COUNT = "@odata.count"
ODATA_TYPE = "@odata.type"
DDEVICE_TYPE = "#DeviceService.DeviceType"


class TestRestOMEVV(object):

    @pytest.fixture
    def mock_response(self):
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = mock_response.getheaders.return_value = {
            'x_omivv-api-vcenter-identifier': 'token_id'}
        mock_response.read.return_value = json.dumps({"value": "data"})
        return mock_response

    @pytest.fixture
    def module_params(self):
        module_parameters = {'hostname': 'xxx.xxx.x.x', 'username': 'username',
                             'password': 'password', "port": 443}
        return module_parameters

    @pytest.fixture
    def ome_object(self, module_params):
        ome_obj = RestOMEVV(module_params=module_params)
        return ome_obj

    def test_invoke_request_without_session(self, mock_response, mocker, module_params):
        obj = MagicMock()
        obj.status_code = 200
        obj.json_data = {"value": "data"}
        obj.success = True
        mocker.patch(MODULE_UTIL_PATH + OMEVV_OPENURL,
                     return_value=obj)
        module_params.update({"vcenter_uuid": "some_token"})
        with RestOMEVV(module_params) as obj:
            response = obj.invoke_request("GET", TEST_PATH)
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    def test_invoke_request_without_session_with_header(self, mock_response, mocker, module_params):
        obj = MagicMock()
        obj.status_code = 200
        obj.json_data = {"value": "data"}
        obj.success = True
        mocker.patch(MODULE_UTIL_PATH + OMEVV_OPENURL,
                     return_value=obj)
        with RestOMEVV(module_params) as obj:
            response = obj.invoke_request("POST", TEST_PATH, headers={
                                          "application": "octstream"})
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    @pytest.mark.parametrize("exc", [URLError, SSLValidationError, ConnectionError])
    def test_invoke_request_error_case_handling(self, exc, mock_response, mocker, module_params):
        open_url_mock = mocker.patch(MODULE_UTIL_PATH + OMEVV_OPENURL,
                                     return_value=mock_response)
        open_url_mock.side_effect = exc("test")
        with pytest.raises(exc):
            with RestOMEVV(module_params) as obj:
                obj.invoke_request(TEST_PATH, "GET")

    def test_invoke_request_http_error_handling(self, mock_response, mocker, module_params):
        open_url_mock = mocker.patch(MODULE_UTIL_PATH + OMEVV_OPENURL,
                                     return_value=mock_response)
        open_url_mock.side_effect = HTTPError(TEST_HOST, 400,
                                              BAD_REQUEST, {}, None)
        with pytest.raises(HTTPError):
            with RestOMEVV(module_params) as obj:
                obj.invoke_request(TEST_PATH, "GET")


class TestOMEVVAnsibleModule(object):

    def test_omevv_ansible_module(self, mocker):
        mocker.patch.object(AnsibleModule, '__init__', return_value=None)
        module = OMEVVAnsibleModule({})
        assert module
