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
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, OpenURLResponse
from unittest.mock import MagicMock
import json
import os

MODULE_UTIL_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.'
OPEN_URL = 'idrac_redfish.open_url'
TEST_PATH = "/testpath"
INVOKE_REQUEST = 'idrac_redfish.iDRACRedfishAPI.invoke_request'
JOB_COMPLETE = 'idrac_redfish.iDRACRedfishAPI.wait_for_job_complete'
API_TASK = '/api/tasks'
SLEEP_TIME = 'idrac_redfish.time.sleep'
MANAGER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"
GET_IDRAC_MANAGER_ATTRIBUTES_9_10 = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/iDRAC.Embedded.1"
RESP = {
    "Model": "17G",
    "FirmwareVersion": "1.20.30"
}
RESP_10 = {
    "Attributes":
    {
        "Info.1.HWModel": "iDRAC 10"
    }
}
RESP_MANAGER_8 = {
    "Model": "13G xxx",
    "FirmwareVersion": "x.x.x"
}
SESSION_ID_10 = "/redfish/v1/SessionService/Sessions/{Id}"
SESSION_10 = "/redfish/v1/SessionService/Sessions"


class TestIdracRedfishRest(object):

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
        module_parameters = {'idrac_ip': 'xxx.xxx.x.x', 'idrac_user': 'username',
                             'idrac_password': 'password', 'idrac_port': '443'}
        return module_parameters

    @pytest.fixture
    def idrac_redfish_object(self, module_params):
        idrac_redfish_obj = iDRACRedfishAPI(module_params)
        return idrac_redfish_obj

    def test_invoke_request_with_session(self, mock_response, mocker, module_params):
        mocker.patch(MODULE_UTIL_PATH + OPEN_URL,
                     return_value=mock_response)
        req_session = True
        with iDRACRedfishAPI(module_params, req_session) as obj:
            response = obj.invoke_request(TEST_PATH, "GET")
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    def test_invoke_request_without_session(self, mock_response, mocker):
        mocker.patch(MODULE_UTIL_PATH + OPEN_URL,
                     return_value=mock_response)
        module_params = {'idrac_ip': '2001:db8:3333:4444:5555:6666:7777:8888', 'idrac_user': 'username',
                         'idrac_password': 'password', "idrac_port": '443'}
        req_session = False
        with iDRACRedfishAPI(module_params, req_session) as obj:
            response = obj.invoke_request(TEST_PATH, "GET")
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    def test_invoke_request_without_session_with_header(self, mock_response, mocker, module_params):
        mocker.patch(MODULE_UTIL_PATH + OPEN_URL,
                     return_value=mock_response)
        req_session = False
        with iDRACRedfishAPI(module_params, req_session) as obj:
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
            with iDRACRedfishAPI(module_params, req_session) as obj:
                obj.invoke_request(TEST_PATH, "GET")

    @pytest.mark.parametrize("exc", [URLError, SSLValidationError, ConnectionError])
    def test_invoke_request_error_case_handling(self, exc, mock_response, mocker, module_params):
        mocker.patch(MODULE_UTIL_PATH + OPEN_URL,
                     side_effect=exc("test"))
        req_session = False
        with pytest.raises(exc):
            with iDRACRedfishAPI(module_params, req_session) as obj:
                obj.invoke_request(TEST_PATH, "GET")

    def test_invoke_request_http_error_handling(self, mock_response, mocker, module_params):
        open_url_mock = mocker.patch(MODULE_UTIL_PATH + OPEN_URL,
                                     return_value=mock_response)
        open_url_mock.side_effect = HTTPError('https://testhost.com/', 400,
                                              'Bad Request Error', {}, None)
        req_session = False
        with pytest.raises(HTTPError):
            with iDRACRedfishAPI(module_params, req_session) as obj:
                obj.invoke_request(TEST_PATH, "GET")

    def test_get_idrac_local_account_attr(self, idrac_redfish_object):
        idrac_attrs = {
            "SystemConfiguration": {
                "Components": [
                    {
                        "FQDD": "iDRAC.Embedded.1",
                        "Attributes": [
                            {
                                "Name": "Users.1",
                                "Value": 1
                            },
                            {
                                "Name": "Users.2",
                                "Value": 2
                            },
                            {
                                "Name": "System1",
                                "Value": "system_data"
                            }
                        ]
                    }
                ]
            }
        }
        result = idrac_redfish_object.get_idrac_local_account_attr(
            idrac_attribues=idrac_attrs, fqdd="iDRAC.Embedded.1")
        assert result == {'Users.1': 1, 'Users.2': 2}

    @pytest.mark.parametrize("query_params", [
        {"inp": {"$filter": "UserName eq 'admin'"},
            "out": "%24filter=UserName+eq+%27admin%27"},
        {"inp": {"$top": 1, "$skip": 2, "$filter": "JobType/Id eq 8"}, "out":
            "%24top=1&%24skip=2&%24filter=JobType%2FId+eq+8"},
        {"inp": {"$top": 1, "$skip": 3}, "out": "%24top=1&%24skip=3"}
    ])
    def test_build_url(self, query_params, mocker, idrac_redfish_object):
        """builds complete url"""
        base_uri = 'https://xxx.xxx.x.x:443/api'
        path = "/AccountService/Accounts"
        mocker.patch(MODULE_UTIL_PATH + 'idrac_redfish.iDRACRedfishAPI._get_url',
                     return_value=base_uri + path)
        inp = query_params["inp"]
        out = query_params["out"]
        url = idrac_redfish_object._build_url(
            path, query_param=inp)
        assert url == base_uri + path + "?" + out

    def test_build_url_none(self, mocker, idrac_redfish_object):
        """builds complete url"""
        base_uri = 'https://xxx.xxx.x.x:443/api'
        mocker.patch(MODULE_UTIL_PATH + 'redfish.Redfish._get_base_url',
                     return_value=base_uri)
        url = idrac_redfish_object._build_url("", None)
        assert url == ""

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

    @pytest.mark.parametrize("task_inp", [{"job_wait": True, "job_status": {"TaskState": "Completed"}}])
    def test_wait_for_job_complete(self, mocker, mock_response, task_inp, idrac_redfish_object):
        mock_response.json_data = task_inp.get("job_status")
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        mocker.patch(MODULE_UTIL_PATH + SLEEP_TIME,
                     return_value=None)
        ret_resp = idrac_redfish_object.wait_for_job_complete(
            API_TASK, task_inp.get("job_wait"))
        assert ret_resp.json_data == mock_response.json_data

    def test_wait_for_job_complete_false(self, mocker, mock_response, idrac_redfish_object):
        mock_response.json_data = {"TaskState": "Completed"}
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        mocker.patch(MODULE_UTIL_PATH + SLEEP_TIME,
                     return_value=None)
        ret_resp = idrac_redfish_object.wait_for_job_complete(API_TASK, False)
        assert ret_resp is None

    def test_wait_for_job_complete_value_error(self, mocker, mock_response, module_params):
        mock_response.json_data = {"TaskState": "Completed"}
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     side_effect=ValueError("test"))
        with pytest.raises(ValueError):
            with iDRACRedfishAPI(module_params, True) as obj:
                obj.wait_for_job_complete(API_TASK, True)

    @pytest.mark.parametrize("inp_data", [
        {
            "j_data": {"PercentComplete": 100, "JobState": "Completed"},
            "job_wait": True,
            "reboot": True,
            "apply_update": True
        },
        {
            "j_data": {"PercentComplete": 0, "JobState": "Starting"},
            "job_wait": True,
            "reboot": False,
            "apply_update": True
        },
        {
            "j_data": {"PercentComplete": 0, "JobState": "Starting"},
            "job_wait": False,
            "reboot": False,
            "apply_update": True
        },
    ])
    def test_wait_for_job_completion(self, mocker, mock_response, inp_data, idrac_redfish_object):
        mock_response.json_data = inp_data.get("j_data")
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        mocker.patch(MODULE_UTIL_PATH + SLEEP_TIME,
                     return_value=None)
        ret_resp = idrac_redfish_object.wait_for_job_completion(API_TASK, inp_data.get(
            "job_wait"), inp_data.get("reboot"), inp_data.get("apply_update"))
        assert ret_resp.json_data is mock_response.json_data

    @pytest.mark.parametrize("share_inp", [
        {"share_ip": "share_ip", "share_name": "share_name", "share_type": "share_type",
         "file_name": "file_name", "username": "username", "password": "password",
         "ignore_certificate_warning": "ignore_certificate_warning",
         "proxy_support": "proxy_support", "proxy_type": "proxy_type",
         "proxy_port": "proxy_port", "proxy_server": "proxy_server",
         "proxy_username": "proxy_username", "proxy_password": "proxy_password"}, {}, None])
    def test_export_scp(self, mocker, mock_response, share_inp, idrac_redfish_object):
        mock_response.json_data = {"Status": "Completed"}
        mock_response.status_code = 202
        mock_response.headers = {"Location": API_TASK}
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        mocker.patch(MODULE_UTIL_PATH + JOB_COMPLETE,
                     return_value={"Status": "Completed"})
        job_wait = share_inp is not None
        resp = idrac_redfish_object.export_scp("xml", "export_use",
                                               "All", job_wait, share_inp)
        if job_wait:
            assert resp == {"Status": "Completed"}
        else:
            assert resp.json_data == {"Status": "Completed"}

    @pytest.mark.parametrize("share_inp", [
        {"share_ip": "share_ip", "share_name": "share_name", "share_type": "share_type",
         "file_name": "file_name", "username": "username", "password": "password",
         "ignore_certificate_warning": "ignore_certificate_warning",
         "proxy_support": "proxy_support", "proxy_type": "proxy_type",
         "proxy_port": "proxy_port", "proxy_server": "proxy_server",
         "proxy_username": "proxy_username", "proxy_password": "proxy_password"}, {}, None])
    def test_import_scp_share(self, mocker, mock_response, share_inp, idrac_redfish_object):
        mock_response.json_data = {"Status": "Completed"}
        mock_response.status_code = 202
        mock_response.headers = {"Location": API_TASK}
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        imp_buffer = "import_buffer"
        if share_inp is not None:
            imp_buffer = None
        resp = idrac_redfish_object.import_scp_share(
            "shutdown_type", "host_powerstate", True, "All", imp_buffer, share_inp)
        assert resp.json_data == {"Status": "Completed"}

    @pytest.mark.parametrize("share_inp", [
        {"share_ip": "share_ip", "share_name": "share_name", "share_type": "share_type",
         "file_name": "file_name", "username": "username", "password": "password",
         "ignore_certificate_warning": "ignore_certificate_warning",
         "proxy_support": "proxy_support", "proxy_type": "proxy_type",
         "proxy_port": "proxy_port", "proxy_server": "proxy_server",
         "proxy_username": "proxy_username", "proxy_password": "proxy_password"}, {}, None])
    def test_import_preview(self, mocker, mock_response, share_inp, idrac_redfish_object):
        mock_response.json_data = {"Status": "Completed"}
        mock_response.status_code = 202
        mock_response.headers = {"Location": API_TASK}
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        mocker.patch(MODULE_UTIL_PATH + JOB_COMPLETE,
                     return_value={"Status": "Completed"})
        job_wait = True
        imp_buffer = "import_buffer"
        if share_inp is not None:
            imp_buffer = None
            job_wait = False
        resp = idrac_redfish_object.import_preview(
            imp_buffer, "All", share_inp, job_wait)
        if job_wait:
            assert resp == {"Status": "Completed"}
        else:
            assert resp.json_data == {"Status": "Completed"}

    @pytest.mark.parametrize("status_code", [202, 200])
    def test_import_scp(self, mocker, mock_response, status_code, idrac_redfish_object):
        mock_response.json_data = {"Status": "Completed"}
        mock_response.status_code = status_code
        mock_response.headers = {"Location": "/tasks/1"}
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        mocker.patch(MODULE_UTIL_PATH + JOB_COMPLETE,
                     return_value=mock_response)
        resp = idrac_redfish_object.import_scp("imp_buffer", "All", True)
        assert resp.json_data == {"Status": "Completed"}

    @pytest.mark.parametrize("status_code", [202, 200])
    def test_import_preview_scp(self, mocker, mock_response, status_code, idrac_redfish_object):
        mock_response.json_data = {"Status": "Completed"}
        mock_response.status_code = status_code
        mock_response.headers = {"Location": "/tasks/1"}
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        mocker.patch(MODULE_UTIL_PATH + JOB_COMPLETE,
                     return_value=mock_response)
        resp = idrac_redfish_object.import_preview_scp(
            "imp_buffer", "All", True)
        assert resp.json_data == {"Status": "Completed"}

    def test_requests_ca_bundle_set(self, mocker, mock_response, idrac_redfish_object):
        os.environ["REQUESTS_CA_BUNDLE"] = "/path/to/requests_ca_bundle.pem"
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        result = idrac_redfish_object._get_omam_ca_env()
        assert result == "/path/to/requests_ca_bundle.pem"
        del os.environ["REQUESTS_CA_BUNDLE"]

    def test_curl_ca_bundle_set(self, mocker, mock_response, idrac_redfish_object):
        os.environ["CURL_CA_BUNDLE"] = "/path/to/curl_ca_bundle.pem"
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        result = idrac_redfish_object._get_omam_ca_env()
        assert result == "/path/to/curl_ca_bundle.pem"
        del os.environ["CURL_CA_BUNDLE"]

    def test_omam_ca_bundle_set(self, mocker, mock_response, idrac_redfish_object):
        os.environ["OMAM_CA_BUNDLE"] = "/path/to/omam_ca_bundle.pem"
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        result = idrac_redfish_object._get_omam_ca_env()
        assert result == "/path/to/omam_ca_bundle.pem"
        del os.environ["OMAM_CA_BUNDLE"]

    def test_no_env_variable_set(self, mocker, mock_response, idrac_redfish_object):
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        result = idrac_redfish_object._get_omam_ca_env()
        assert result is None

    def test_find_ip_address_ipv4(self, idrac_redfish_object):
        result = idrac_redfish_object.find_ip_address(sharename="\\\\100.100.100.100\\cifsshare")
        assert result == "100.100.100.100"

    def test_find_ip_address_ipv6(self, idrac_redfish_object):
        result = idrac_redfish_object.find_ip_address(sharename="\\\\2001:db8:85a3:0:0:8a2e:370:7334\\cifsshare")
        assert result == "2001:db8:85a3:0:0:8a2e:370:7334"

    def test_get_job_uri_idrac_10(self, idrac_redfish_object):
        idrac_redfish_object.validate_idrac10_and_above = \
            MagicMock(return_value=True)
        result = idrac_redfish_object.get_job_uri()
        assert result == "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/{job_id}"

    def test_get_job_uri_not_idrac_10(self, idrac_redfish_object):
        idrac_redfish_object.validate_idrac10_and_above = \
            MagicMock(return_value=False)
        result = idrac_redfish_object.get_job_uri()
        assert result == "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/{job_id}"

    def mock_get_dynamic_idrac_invoke_request(self, *args):
        obj = MagicMock()
        obj.status_code = 200
        if MANAGER_URI in args:
            obj.json_data = RESP
        else:
            obj.json_data = RESP_10
        return obj

    def test_get_server_generation(self, idrac_redfish_object, mocker):
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     self.mock_get_dynamic_idrac_invoke_request)
        result = idrac_redfish_object.get_server_generation
        assert result == (17, '1.20.30', 'iDRAC 10')
