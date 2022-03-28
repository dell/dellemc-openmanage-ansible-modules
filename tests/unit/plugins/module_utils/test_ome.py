# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.2.0
# Copyright (C) 2019-2022 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME
from mock import MagicMock
import json

MODULE_UTIL_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.'


class TestRestOME(object):

    @pytest.fixture
    def ome_response_mock(self, mocker):
        set_method_result = {'json_data': {}}
        response_class_mock = mocker.patch(
            MODULE_UTIL_PATH + 'ome.OpenURLResponse',
            return_value=set_method_result)
        response_class_mock.success = True
        response_class_mock.status_code = 200
        return response_class_mock

    @pytest.fixture
    def mock_response(self):
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = mock_response.getheaders.return_value = {'X-Auth-Token': 'token_id'}
        mock_response.read.return_value = json.dumps({"value": "data"})
        return mock_response

    def test_invoke_request_with_session(self, mock_response, mocker):
        mocker.patch(MODULE_UTIL_PATH + 'ome.open_url',
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
        mocker.patch(MODULE_UTIL_PATH + 'ome.open_url',
                     return_value=mock_response)
        module_params = {'hostname': '192.168.0.1', 'username': 'username',
                         'password': 'password', "port": 443}
        req_session = False
        with RestOME(module_params, req_session) as obj:
            response = obj.invoke_request("/testpath", "GET")
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    def test_invoke_request_without_session_with_header(self, mock_response, mocker):
        mocker.patch(MODULE_UTIL_PATH + 'ome.open_url',
                     return_value=mock_response)
        module_params = {'hostname': '192.168.0.1', 'username': 'username',
                         'password': 'password', "port": 443}
        req_session = False
        with RestOME(module_params, req_session) as obj:
            response = obj.invoke_request("/testpath", "POST", headers={"application": "octstream"})
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    def test_invoke_request_with_session_connection_error(self, mocker, mock_response):
        mock_response.success = False
        mock_response.status_code = 500
        mock_response.json_data = {}
        mocker.patch(MODULE_UTIL_PATH + 'ome.RestOME.invoke_request',
                     return_value=mock_response)
        module_params = {'hostname': '192.168.0.1', 'username': 'username',
                         'password': 'password', "port": 443}
        req_session = True
        with pytest.raises(ConnectionError):
            with RestOME(module_params, req_session) as obj:
                obj.invoke_request("/testpath", "GET")

    @pytest.mark.parametrize("exc", [URLError, SSLValidationError, ConnectionError])
    def test_invoke_request_error_case_handling(self, exc, mock_response, mocker):
        open_url_mock = mocker.patch(MODULE_UTIL_PATH + 'ome.open_url',
                                     return_value=mock_response)
        open_url_mock.side_effect = exc("test")
        module_params = {'hostname': '192.168.0.1', 'username': 'username',
                         'password': 'password', "port": 443}
        req_session = False
        with pytest.raises(exc) as e:
            with RestOME(module_params, req_session) as obj:
                obj.invoke_request("/testpath", "GET")

    def test_invoke_request_http_error_handling(self, mock_response, mocker):
        open_url_mock = mocker.patch(MODULE_UTIL_PATH + 'ome.open_url',
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
        mocker.patch(MODULE_UTIL_PATH + 'ome.RestOME.invoke_request',
                     return_value=mock_response)
        module_params = {'hostname': '192.168.0.1', 'username': 'username',
                         'password': 'password', "port": 443}
        with RestOME(module_params, True) as obj:
            reports = obj.get_all_report_details("DeviceService/Devices")
        assert reports == {"resp_obj": mock_response, "report_list": list(range(51))}

    def test_get_report_list_error_case(self, mock_response, mocker):
        mocker.patch(MODULE_UTIL_PATH + 'ome.open_url',
                     return_value=mock_response)
        invoke_obj = mocker.patch(MODULE_UTIL_PATH + 'ome.RestOME.invoke_request',
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
        mocker.patch(MODULE_UTIL_PATH + 'ome.RestOME._get_base_url',
                     return_value=base_uri)
        inp = query_param["inp"]
        out = query_param["out"]
        url = RestOME(module_params=module_params)._build_url(path, query_param=inp)
        assert url == base_uri + "/" + path + "?" + out
        assert "+" not in url

    def test_get_job_type_id(self, mock_response, mocker):
        mock_response.success = True
        mock_response.status_code = 200
        mock_response.json_data = {"@odata.count": 50, "value": [{"Name": "PowerChange", "Id": 11}]}
        mocker.patch(MODULE_UTIL_PATH + 'ome.RestOME.invoke_request',
                     return_value=mock_response)
        jobtype_name = "PowerChange"
        module_params = {'hostname': '192.168.0.1', 'username': 'username',
                         'password': 'password', "port": 443}
        with RestOME(module_params, True) as obj:
            job_id = obj.get_job_type_id(jobtype_name)
        assert job_id == 11

    def test_get_job_type_id_null_case(self, mock_response, mocker):
        mock_response.success = True
        mock_response.status_code = 200
        mock_response.json_data = {"@odata.count": 50, "value": [{"Name": "PowerChange", "Id": 11}]}
        mocker.patch(MODULE_UTIL_PATH + 'ome.RestOME.invoke_request',
                     return_value=mock_response)
        jobtype_name = "FirmwareUpdate"
        module_params = {'hostname': '192.168.0.1', 'username': 'username',
                         'password': 'password', "port": 443}
        with RestOME(module_params, True) as obj:
            job_id = obj.get_job_type_id(jobtype_name)
        assert job_id is None

    def test_get_device_id_from_service_tag_ome_case01(self, mocker, mock_response):
        mock_response.success = True
        mock_response.status_code = 200
        mock_response.json_data = {"@odata.count": 1, "value": [{"Name": "xyz", "Id": 11}]}
        mocker.patch(MODULE_UTIL_PATH + 'ome.RestOME.invoke_request',
                     return_value=mock_response)
        ome_default_args = {'hostname': '192.168.0.1', 'username': 'username',
                            'password': 'password', "port": 443}
        with RestOME(ome_default_args, True) as obj:
            details = obj.get_device_id_from_service_tag("xyz")
        assert details["Id"] == 11
        assert details["value"] == {"Name": "xyz", "Id": 11}

    def test_get_device_id_from_service_tag_ome_case02(self, mocker, mock_response):
        mock_response.success = True
        mock_response.status_code = 200
        mock_response.json_data = {"@odata.count": 0, "value": []}
        mocker.patch(MODULE_UTIL_PATH + 'ome.RestOME.invoke_request',
                     return_value=mock_response)
        ome_default_args = {'hostname': '192.168.0.1', 'username': 'username',
                            'password': 'password', "port": 443}
        with RestOME(ome_default_args, True) as obj:
            details = obj.get_device_id_from_service_tag("xyz")
        assert details["Id"] is None
        assert details["value"] == {}

    def test_get_all_items_with_pagination(self, mock_response, mocker):
        mock_response.success = True
        mock_response.status_code = 200
        mock_response.json_data = {"@odata.count": 50, "value": list(range(51))}
        mocker.patch(MODULE_UTIL_PATH + 'ome.RestOME.invoke_request',
                     return_value=mock_response)
        module_params = {'hostname': '192.168.0.1', 'username': 'username',
                         'password': 'password', "port": 443}
        with RestOME(module_params, True) as obj:
            reports = obj.get_all_items_with_pagination("DeviceService/Devices")
        assert reports == {"total_count": 50, "value": list(range(51))}

    def test_get_all_items_with_pagination_error_case(self, mock_response, mocker):
        mocker.patch(MODULE_UTIL_PATH + 'ome.open_url',
                     return_value=mock_response)
        invoke_obj = mocker.patch(MODULE_UTIL_PATH + 'ome.RestOME.invoke_request',
                                  side_effect=HTTPError('http://testhost.com/', 400, 'Bad Request Error', {}, None))
        module_params = {'hostname': '192.168.0.1', 'username': 'username',
                         'password': 'password', "port": 443}
        with pytest.raises(HTTPError) as e:
            with RestOME(module_params, False) as obj:
                obj.get_all_items_with_pagination("DeviceService/Devices")

    def test_get_device_type(self, mock_response, mocker):
        mock_response.success = True
        mock_response.status_code = 200
        mock_response.json_data = {
            "@odata.context": "/api/$metadata#Collection(DeviceService.DeviceType)",
            "@odata.count": 5,
            "value": [
                {
                    "@odata.type": "#DeviceService.DeviceType",
                    "DeviceType": 1000,
                    "Name": "SERVER",
                    "Description": "Server Device"
                },
                {
                    "@odata.type": "#DeviceService.DeviceType",
                    "DeviceType": 2000,
                    "Name": "CHASSIS",
                    "Description": "Chassis Device"
                },
                {
                    "@odata.type": "#DeviceService.DeviceType",
                    "DeviceType": 3000,
                    "Name": "STORAGE",
                    "Description": "Storage Device"
                },
                {
                    "@odata.type": "#DeviceService.DeviceType",
                    "DeviceType": 4000,
                    "Name": "NETWORK_IOM",
                    "Description": "NETWORK IO Module Device"
                },
                {
                    "@odata.type": "#DeviceService.DeviceType",
                    "DeviceType": 8000,
                    "Name": "STORAGE_IOM",
                    "Description": "Storage IOM Device"
                }
            ]
        }
        mocker.patch(MODULE_UTIL_PATH + 'ome.RestOME.invoke_request',
                     return_value=mock_response)
        module_params = {'hostname': '192.168.0.1', 'username': 'username',
                         'password': 'password', "port": 443}
        with RestOME(module_params, False) as obj:
            type_map = obj.get_device_type()
        assert type_map == {1000: "SERVER", 2000: "CHASSIS", 3000: "STORAGE",
                            4000: "NETWORK_IOM", 8000: "STORAGE_IOM"}
