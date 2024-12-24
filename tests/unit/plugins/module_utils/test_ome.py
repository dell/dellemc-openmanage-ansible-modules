# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.0.0
# Copyright (C) 2019-2023 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OpenURLResponse
from unittest.mock import MagicMock
import json

MODULE_UTIL_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.'
OME_OPENURL = 'ome.open_url'
TEST_PATH = "/testpath"
INVOKE_REQUEST = 'ome.RestOME.invoke_request'
JOB_SUBMISSION = 'ome.RestOME.job_submission'
DEVICE_API = "DeviceService/Devices"
TEST_HOST = 'https://testhost.com/'
BAD_REQUEST = 'Bad Request Error'
ODATA_COUNT = "@odata.count"
ODATA_TYPE = "@odata.type"
DDEVICE_TYPE = "#DeviceService.DeviceType"


class TestOMERest(object):

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
        ome_obj = RestOME(module_params=module_params)
        return ome_obj

    def test_invoke_request_with_session(self, mock_response, mocker):

        mocker.patch(MODULE_UTIL_PATH + OME_OPENURL,
                     return_value=mock_response)
        module_params = {'hostname': '[2001:db8:3333:4444:5555:6666:7777:8888]', 'username': 'username',
                         'password': 'password', "port": 443}
        req_session = True
        with RestOME(module_params, req_session) as obj:

            response = obj.invoke_request(TEST_PATH, "GET")
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    def test_invoke_request_without_session(self, mock_response, mocker, module_params):
        mocker.patch(MODULE_UTIL_PATH + OME_OPENURL,
                     return_value=mock_response)
        req_session = False
        with RestOME(module_params, req_session) as obj:
            response = obj.invoke_request(TEST_PATH, "GET")
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    def test_invoke_request_without_session_with_header(self, mock_response, mocker, module_params):
        mocker.patch(MODULE_UTIL_PATH + OME_OPENURL,
                     return_value=mock_response)
        req_session = False
        with RestOME(module_params, req_session) as obj:
            response = obj.invoke_request(TEST_PATH, "POST", headers={
                                          "application": "octstream"})
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    def test_invoke_request_with_session_connection_error(self, mocker, mock_response, module_params):
        mock_response.success = False
        mock_response.status_code = 500
        mock_response.json_data = {}
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        req_session = True
        with pytest.raises(ConnectionError):
            with RestOME(module_params, req_session) as obj:
                obj.invoke_request(TEST_PATH, "GET")

    @pytest.mark.parametrize("exc", [URLError, SSLValidationError, ConnectionError])
    def test_invoke_request_error_case_handling(self, exc, mock_response, mocker, module_params):
        open_url_mock = mocker.patch(MODULE_UTIL_PATH + OME_OPENURL,
                                     return_value=mock_response)
        open_url_mock.side_effect = exc("test")
        req_session = False
        with pytest.raises(exc):
            with RestOME(module_params, req_session) as obj:
                obj.invoke_request(TEST_PATH, "GET")

    def test_invoke_request_http_error_handling(self, mock_response, mocker, module_params):
        open_url_mock = mocker.patch(MODULE_UTIL_PATH + OME_OPENURL,
                                     return_value=mock_response)
        open_url_mock.side_effect = HTTPError(TEST_HOST, 400,
                                              BAD_REQUEST, {}, None)
        req_session = False
        with pytest.raises(HTTPError):
            with RestOME(module_params, req_session) as obj:
                obj.invoke_request(TEST_PATH, "GET")

    def test_get_all_report_details(self, mock_response, mocker, module_params):
        mock_response.success = True
        mock_response.status_code = 200
        mock_response.json_data = {ODATA_COUNT: 53, "value": list(range(50))}
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        with RestOME(module_params, True) as obj:
            reports = obj.get_all_report_details(DEVICE_API)
        assert reports == {"resp_obj": mock_response,
                           "report_list": list(range(50)) + (list(range(50)))}

    def test_get_report_list_error_case(self, mock_response, mocker, ome_object):
        mocker.patch(MODULE_UTIL_PATH + OME_OPENURL,
                     return_value=mock_response)
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     side_effect=HTTPError(TEST_HOST, 400, BAD_REQUEST, {}, None))
        with pytest.raises(HTTPError):
            ome_object.get_all_report_details(DEVICE_API)

    @pytest.mark.parametrize("query_param", [
        {"inp": {"$filter": "UserName eq 'admin'"},
            "out": "%24filter=UserName%20eq%20%27admin%27"},
        {"inp": {"$top": 1, "$skip": 2, "$filter": "JobType/Id eq 8"}, "out":
            "%24top=1&%24skip=2&%24filter=JobType%2FId%20eq%208"},
        {"inp": {"$top": 1, "$skip": 3}, "out": "%24top=1&%24skip=3"}
    ])
    def test_build_url(self, query_param, mocker, module_params):
        """builds complete url"""
        base_uri = 'https://xxx.xxx.x.x:443/api'
        path = "AccountService/Accounts"
        mocker.patch(MODULE_UTIL_PATH + 'ome.RestOME._get_base_url',
                     return_value=base_uri)
        inp = query_param["inp"]
        out = query_param["out"]
        url = RestOME(module_params=module_params)._build_url(
            path, query_param=inp)
        assert url == base_uri + "/" + path + "?" + out
        assert "+" not in url

    def test_get_job_type_id(self, mock_response, mocker, ome_object):
        mock_response.success = True
        mock_response.status_code = 200
        mock_response.json_data = {ODATA_COUNT: 50,
                                   "value": [{"Name": "PowerChange", "Id": 11}]}
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        jobtype_name = "PowerChange"
        job_id = ome_object.get_job_type_id(jobtype_name)
        assert job_id == 11

    def test_get_job_type_id_null_case(self, mock_response, mocker, ome_object):
        mock_response.success = True
        mock_response.status_code = 200
        mock_response.json_data = {ODATA_COUNT: 50,
                                   "value": [{"Name": "PowerChange", "Id": 11}]}
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        jobtype_name = "FirmwareUpdate"
        job_id = ome_object.get_job_type_id(jobtype_name)
        assert job_id is None

    def test_get_device_id_from_service_tag_ome_case01(self, mocker, mock_response, ome_object):
        mock_response.success = True
        mock_response.status_code = 200
        mock_response.json_data = {ODATA_COUNT: 1,
                                   "value": [{"Name": "xyz", "Id": 11}]}
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        details = ome_object.get_device_id_from_service_tag("xyz")
        assert details["Id"] == 11
        assert details["value"] == {"Name": "xyz", "Id": 11}

    def test_get_device_id_from_service_tag_ome_case02(self, mocker, mock_response, ome_object):
        mock_response.success = True
        mock_response.status_code = 200
        mock_response.json_data = {ODATA_COUNT: 0, "value": []}
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        details = ome_object.get_device_id_from_service_tag("xyz")
        assert details["Id"] is None
        assert details["value"] == {}

    def test_get_all_items_with_pagination(self, mock_response, mocker, ome_object):
        mock_response.success = True
        mock_response.status_code = 200
        mock_response.json_data = {ODATA_COUNT: 100, "value": list(
            range(50)), '@odata.nextLink': '/api/DeviceService/Devices2'}

        mock_response_page2 = MagicMock()
        mock_response_page2.success = True
        mock_response_page2.status_code = 200
        mock_response_page2.json_data = {
            ODATA_COUNT: 100, "value": list(range(50, 100))}

        def mock_invoke_request(*args, **kwargs):
            if args[1] == DEVICE_API:
                return mock_response
            return mock_response_page2

        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     side_effect=mock_invoke_request)
        reports = ome_object.get_all_items_with_pagination(DEVICE_API)
        assert reports == {"total_count": 100, "value": list(range(100))}

    def test_get_all_items_with_pagination_error_case(self, mock_response, mocker, ome_object):
        mocker.patch(MODULE_UTIL_PATH + OME_OPENURL,
                     return_value=mock_response)
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     side_effect=HTTPError(TEST_HOST, 400, BAD_REQUEST, {}, None))
        with pytest.raises(HTTPError):
            ome_object.get_all_items_with_pagination(DEVICE_API)

    def test_get_device_type(self, mock_response, mocker, ome_object):
        mock_response.success = True
        mock_response.status_code = 200
        mock_response.json_data = {
            "@odata.context": "/api/$metadata#Collection(DeviceService.DeviceType)",
            ODATA_COUNT: 5,
            "value": [
                {
                    ODATA_TYPE: DDEVICE_TYPE,
                    "DeviceType": 1000,
                    "Name": "SERVER",
                    "Description": "Server Device"
                },
                {
                    ODATA_TYPE: DDEVICE_TYPE,
                    "DeviceType": 2000,
                    "Name": "CHASSIS",
                    "Description": "Chassis Device"
                },
                {
                    ODATA_TYPE: DDEVICE_TYPE,
                    "DeviceType": 3000,
                    "Name": "STORAGE",
                    "Description": "Storage Device"
                },
                {
                    ODATA_TYPE: DDEVICE_TYPE,
                    "DeviceType": 4000,
                    "Name": "NETWORK_IOM",
                    "Description": "NETWORK IO Module Device"
                },
                {
                    ODATA_TYPE: DDEVICE_TYPE,
                    "DeviceType": 8000,
                    "Name": "STORAGE_IOM",
                    "Description": "Storage IOM Device"
                }
            ]
        }
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        type_map = ome_object.get_device_type()
        assert type_map == {1000: "SERVER", 2000: "CHASSIS", 3000: "STORAGE",
                            4000: "NETWORK_IOM", 8000: "STORAGE_IOM"}

    def test_invalid_json_openurlresp(self):
        obj = OpenURLResponse({})
        obj.body = 'invalid json'
        with pytest.raises(ValueError) as e:
            obj.json_data
        assert e.value.args[0] == "Unable to parse json"

    @pytest.mark.parametrize("status_assert", [
        {'id': 2060, 'exist_poll': True, 'job_failed': False,
            'message': "Job Completed successfully."},
        {'id': 2070, 'exist_poll': True, 'job_failed': True,
            'message': "Job is in Failed state, and is not completed."},
        {'id': 1234, 'exist_poll': False, 'job_failed': False, 'message': None}])
    def test_get_job_info(self, mocker, mock_response, status_assert, ome_object):

        mock_response.success = True
        mock_response.status_code = 200
        mock_response.json_data = {
            'LastRunStatus': {'Id': status_assert['id']}
        }
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        exit_poll, job_failed, message = ome_object.get_job_info(12345)

        assert exit_poll is status_assert['exist_poll']
        assert job_failed is status_assert['job_failed']
        assert message == status_assert['message']

    def test_get_job_exception(self, mocker, module_params):
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     side_effect=HTTPError(TEST_HOST, 400,
                                           BAD_REQUEST, {}, None))
        with pytest.raises(HTTPError):
            with RestOME(module_params, True) as obj:
                obj.get_job_info(12345)

    @pytest.mark.parametrize("ret_val", [
        (True, False, "My Message"),
        (False, True, "The job is not complete after 2 seconds.")])
    def test_job_tracking(self, mocker, mock_response, ret_val, ome_object):
        mocker.patch(MODULE_UTIL_PATH + 'ome.time.sleep',
                     return_value=())
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)

        mocker.patch(MODULE_UTIL_PATH + 'ome.RestOME.get_job_info',
                     return_value=ret_val)
        job_failed, message = ome_object.job_tracking(12345, 2, 1)
        assert job_failed is ret_val[1]
        assert message == ret_val[2]

    def test_strip_substr_dict(self, mocker, mock_response, ome_object):
        data_dict = {"@odata.context": "/api/$metadata#Collection(DeviceService.DeviceType)",
                     ODATA_COUNT: 5,
                     "value": [
                         {
                             ODATA_TYPE: DDEVICE_TYPE,
                             "DeviceType": 1000,
                             "Name": "SERVER",
                             "Description": "Server Device"
                         },
                         {
                             ODATA_TYPE: DDEVICE_TYPE,
                             "DeviceType": 2000,
                             "Name": "CHASSIS",
                             "Description": "Chassis Device"
                         }
                     ]}
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        ret = ome_object.strip_substr_dict(data_dict)
        assert ret == {'value': [{'@odata.type': '#DeviceService.DeviceType', 'Description': 'Server Device', 'DeviceType': 1000, 'Name': 'SERVER'}, {
            '@odata.type': '#DeviceService.DeviceType', 'Description': 'Chassis Device', 'DeviceType': 2000, 'Name': 'CHASSIS'}]}

    def test_job_submission(self, mocker, mock_response, ome_object):
        mock_response.success = True
        mock_response.status_code = 200
        mock_response.json_data = {
            'JobStatus': "Completed"
        }
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        ret = ome_object.job_submission(
            "job_name", "job_desc", "targets", "params", "job_type")
        assert ret.json_data == mock_response.json_data

    def test_test_network_connection(self, mocker, mock_response, ome_object):
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        mock_response.success = True
        mock_response.status_code = 200
        mock_response.json_data = {
            'JobStatus': "Completed"
        }
        mocker.patch(MODULE_UTIL_PATH + JOB_SUBMISSION,
                     return_value=mock_response)
        ret = ome_object.test_network_connection(
            "share_address", "share_path", "share_type", "share_user", "share_password", "share_domain")
        assert ret.json_data == mock_response.json_data

        ret = ome_object.test_network_connection(
            "share_address", "share_path", "share_type")
        assert ret.json_data == mock_response.json_data

    def test_check_existing_job_state(self, mocker, mock_response, ome_object):
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        mock_response.success = True
        mock_response.status_code = 200
        mock_response.json_data = {
            'value': [{"JobType": {"Name": "Job_Name_1"}}]
        }
        mocker.patch(MODULE_UTIL_PATH + JOB_SUBMISSION,
                     return_value=mock_response)
        job_allowed, available_jobs = ome_object.check_existing_job_state(
            "Job_Name_1")
        assert job_allowed is False
        assert available_jobs == {"JobType": {"Name": "Job_Name_1"}}

        mock_response.json_data = {
            'value': []
        }
        mocker.patch(MODULE_UTIL_PATH + JOB_SUBMISSION,
                     return_value=mock_response)
        job_allowed, available_jobs = ome_object.check_existing_job_state(
            "Job_Name_1")
        assert job_allowed is True
        assert available_jobs == []

        mock_response.json_data = {
            'value': [{"JobType": {"Name": "Job_Name_2"}}]
        }
        mocker.patch(MODULE_UTIL_PATH + JOB_SUBMISSION,
                     return_value=mock_response)
        job_allowed, available_jobs = ome_object.check_existing_job_state(
            "Job_Name_1")
        assert job_allowed is True
        assert available_jobs == [{'JobType': {'Name': 'Job_Name_2'}}]
