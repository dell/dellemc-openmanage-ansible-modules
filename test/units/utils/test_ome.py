# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1
# Copyright (C) 2019-2010 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

from __future__ import absolute_import

import pytest
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.remote_management.dellemc.ome import RestOME
from units.compat.mock import MagicMock
import json


class TestRestOME(object):
    module = RestOME

    @pytest.fixture
    def mock_response(self):
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = mock_response.getheaders.return_value = {'X-Auth-Token': 'token_id'}
        mock_response.read.return_value = json.dumps({"value": "data"})
        return mock_response

    def test_invoke_request_with_session(self, mock_response, mocker):
        mocker.patch('ansible.module_utils.remote_management.dellemc.ome.open_url',
                     return_value=mock_response)
        module_params = {'hostname': '192.168.0.1', 'username': 'username',
                         'password': 'password', "port": 443}
        req_session = True
        with RestOME(module_params, req_session) as obj:
            response = obj.invoke_request("/testpath", "GET")
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    def test_invoke_request_without_session(self, mock_response, mocker):
        mocker.patch('ansible.module_utils.remote_management.dellemc.ome.open_url',
                     return_value=mock_response)
        module_params = {'hostname': '192.168.0.1', 'username': 'username',
                         'password': 'password', "port": 443}
        req_session = False
        with RestOME(module_params, req_session) as obj:
            response = obj.invoke_request("/testpath", "GET")
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    @pytest.mark.parametrize("exc", [URLError, SSLValidationError, ConnectionError])
    def test_invoke_request_error_case_handling(self, exc, mock_response, mocker):
        open_url_mock = mocker.patch('ansible.module_utils.remote_management.dellemc.ome.open_url',
                                     return_value=mock_response)
        open_url_mock.side_effect = exc("test")
        module_params = {'hostname': '192.168.0.1', 'username': 'username',
                         'password': 'password', "port": 443}
        req_session = False
        with pytest.raises(exc) as e:
            with RestOME(module_params, req_session) as obj:
                obj.invoke_request("/testpath", "GET")

    def test_invoke_request_http_error_handling(self, mock_response, mocker):
        open_url_mock = mocker.patch('ansible.module_utils.remote_management.dellemc.ome.open_url',
                                     return_value=mock_response)
        open_url_mock.side_effect = HTTPError('http://testhost.com/', 400,
                                              'Bad Request Error', {}, None)
        module_params = {'hostname': '192.168.0.1', 'username': 'username',
                         'password': 'password', "port": 443}
        req_session = False
        with pytest.raises(HTTPError) as e:
            with RestOME(module_params, req_session) as obj:
                obj.invoke_request("/testpath", "GET")

    def test_get_all_report_details(self, mock_response, mocker):
        mock_response.success = True
        mock_response.status_code = 200
        mock_response.json_data = {"@odata.count": 50, "value": list(range(51))}
        mocker.patch('ansible.module_utils.remote_management.dellemc.ome.RestOME.invoke_request',
                     return_value=mock_response)
        module_params = {'hostname': '192.168.0.1', 'username': 'username',
                         'password': 'password', "port": 443}
        with RestOME(module_params, True) as obj:
            reports = obj.get_all_report_details("DeviceService/Devices")
        assert reports == {"resp_obj": mock_response, "report_list": list(range(51))}

    def test_get_report_list_error_case(self, mock_response, mocker):
        mocker.patch('ansible.module_utils.remote_management.dellemc.ome.open_url',
                     return_value=mock_response)
        invoke_obj = mocker.patch('ansible.module_utils.remote_management.dellemc.ome.RestOME.invoke_request',
                                  side_effect=HTTPError('http://testhost.com/', 400, 'Bad Request Error', {}, None))
        module_params = {'hostname': '192.168.0.1', 'username': 'username',
                         'password': 'password', "port": 443}
        with pytest.raises(HTTPError) as e:
            with RestOME(module_params, False) as obj:
                obj.get_all_report_details("DeviceService/Devices")

    @pytest.mark.parametrize("query_param", [
        {"inp": {"$filter": "UserName eq 'admin'"}, "out": "%24filter=UserName%20eq%20%27admin%27"},
        {"inp": {"$top": 1, "$skip": 2, "$filter": "JobType/Id eq 8"}, "out":
            "%24top=1&%24skip=2&%24filter=JobType%2FId%20eq%208"},
        {"inp": {"$top": 1, "$skip": 3}, "out": "%24top=1&%24skip=3"}
    ])
    def test_build_url(self, query_param, mocker):
        """builds complete url"""
        base_uri = 'https://192.168.0.1:443/api'
        path = "AccountService/Accounts"
        module_params = {'hostname': '192.168.0.1', 'username': 'username',
                         'password': 'password', "port": 443}
        mocker.patch('ansible.module_utils.remote_management.dellemc.ome.RestOME._get_base_url',
                     return_value=base_uri)
        inp = query_param["inp"]
        out = query_param["out"]
        url = RestOME(module_params=module_params)._build_url(path, query_param=inp)
        assert url == base_uri + "/" + path + "?" + out
        assert "+" not in url
