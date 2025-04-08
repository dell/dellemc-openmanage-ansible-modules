# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.0.0
# Copyright (C) 2020-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_lifecycle_controller_job_status_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from unittest.mock import MagicMock, Mock
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestLcJobStatus(FakeAnsibleModule):
    module = idrac_lifecycle_controller_job_status_info

    @pytest.fixture
    def idrac_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.job_mgr = idrac_obj
        type(idrac_obj).get_job_status = Mock(return_value="job_id")
        return idrac_obj

    @pytest.fixture
    def idrac_redfish_system_info_mock(self):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.get_entityjson = idrac_obj
        type(idrac_obj).get_json_device = Mock(return_value="msg")
        return idrac_obj

    @pytest.fixture
    def idrac_redfish_system_info_connection_mock(self, mocker, idrac_redfish_system_info_mock):
        idrac_redfish_conn_class_mock = mocker.patch(MODULE_PATH +
                                                     'idrac_lifecycle_controller_job_status_info.iDRACRedfishAPI',
                                                     return_value=idrac_redfish_system_info_mock)
        idrac_redfish_conn_class_mock.return_value.__enter__.return_value = idrac_redfish_system_info_mock
        return idrac_redfish_system_info_mock

    @pytest.fixture
    def idrac_get_lc_job_status_connection_mock(self, mocker, idrac_mock):
        idrac_conn_class_mock = mocker.patch(MODULE_PATH +
                                             'idrac_lifecycle_controller_job_status_info.iDRACConnection',
                                             return_value=idrac_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_mock
        return idrac_mock

    @pytest.mark.parametrize("exc_type", [HTTPError])
    def test_main_idrac_get_lc_job_status_success_case01(self, idrac_get_lc_job_status_connection_mock,
                                                         exc_type,
                                                         idrac_redfish_system_info_mock,
                                                         idrac_redfish_system_info_connection_mock,
                                                         idrac_default_args,
                                                         mocker):
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_job_status_info",
                     return_value=True)
        json_str = to_text(json.dumps({"data": "out"}))
        idrac_redfish_system_info_mock.get_entityjson.return_value = None
        idrac_redfish_system_info_connection_mock.get_json_device.return_value = ""
        idrac_redfish_system_info_connection_mock.invoke_request.side_effect = exc_type('https://testhost.com', 404,
                                                                                        'http error message',
                                                                                        {"accept-type": "application/json"},
                                                                                        StringIO(json_str))
        idrac_default_args.update({"job_id": "job_id"})
        idrac_get_lc_job_status_connection_mock.job_mgr.get_job_status.return_value = {"Status": "Success"}
        result = self._run_module(idrac_default_args)
        assert result["changed"] is False

    def test_main_idrac_get_lc_job_status_success_case02(self, idrac_get_lc_job_status_connection_mock,
                                                         idrac_redfish_system_info_mock,
                                                         idrac_redfish_system_info_connection_mock,
                                                         idrac_default_args,
                                                         mocker):
        obj = MagicMock()
        obj.status_code = 200
        obj.json_data = {
            "ActualRunningStartTime": None,
            "ActualRunningStopTime": None,
            "CompletionTime": "2025-04-01T11:05:17",
            "Description": "Job Instance",
            "EndTime": "TIME_NA",
            "Id": "JID_435235166998",
            "JobState": "Completed",
            "JobType": "iDRACConfiguration",
            "Message": "Job successfully completed.",
            "MessageArgs": ["NA"],
            "MessageId": "JCP007",
            "Name": "Configure: iDRAC.Embedded.1",
            "PercentComplete": 100,
            "StartTime": "2025-04-01T11:05:16",
            "TargetSettingsURI": None,
            "status_code": 200}
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_job_status_info",
                     return_value=True)
        idrac_default_args.update({"job_id": "job_id"})
        idrac_redfish_system_info_mock.get_entityjson.return_value = None
        idrac_redfish_system_info_connection_mock.invoke_request.return_value = obj
        idrac_redfish_system_info_connection_mock.get_json_device.return_value = ""
        idrac_get_lc_job_status_connection_mock.job_mgr.get_job_status.return_value = {"Status": "Success"}
        result = self._run_module(idrac_default_args)
        assert result["changed"] is False

    def test_main_idrac_get_lc_job_status_success_case03(self, idrac_get_lc_job_status_connection_mock,
                                                         idrac_redfish_system_info_mock,
                                                         idrac_redfish_system_info_connection_mock,
                                                         idrac_default_args,
                                                         mocker):
        obj = MagicMock()
        obj.status_code = 200
        obj.json_data = {
            "ActualRunningStartTime": None,
            "ActualRunningStopTime": None,
            "CompletionTime": "2025-04-01T11:05:17",
            "Description": "Job Instance",
            "EndTime": "TIME_NA",
            "Id": "JID_435235166998",
            "JobState": "Failed",
            "JobType": "iDRACConfiguration",
            "Message": "Job successfully completed.",
            "MessageArgs": [],
            "MessageId": "JCP007",
            "Name": "Configure: iDRAC.Embedded.1",
            "PercentComplete": 100,
            "StartTime": "2025-04-01T11:05:16",
            "TargetSettingsURI": None,
            "status_code": 200}
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_job_status_info",
                     return_value=True)
        idrac_default_args.update({"job_id": "job_id"})
        idrac_redfish_system_info_mock.get_entityjson.return_value = None
        idrac_redfish_system_info_connection_mock.invoke_request.return_value = obj
        idrac_redfish_system_info_connection_mock.get_json_device.return_value = ""
        idrac_get_lc_job_status_connection_mock.job_mgr.get_job_status.return_value = {"Status": "Success"}
        result = self._run_module(idrac_default_args)
        assert result["changed"] is False

    def test_main_idrac_get_lc_job_status_success_case04(self, idrac_get_lc_job_status_connection_mock,
                                                         idrac_redfish_system_info_mock,
                                                         idrac_redfish_system_info_connection_mock,
                                                         idrac_default_args,
                                                         mocker):
        obj = MagicMock()
        obj.status_code = 200
        obj.json_data = {
            "ActualRunningStartTime": None,
            "ActualRunningStopTime": None,
            "CompletionTime": "2025-04-01T11:05:17",
            "Description": "Job Instance",
            "EndTime": "TIME_NA",
            "Id": "JID_435235166998",
            "JobState": "Sample job state",
            "JobType": "iDRACConfiguration",
            "Message": "Job successfully completed.",
            "MessageArgs": ["NA"],
            "MessageId": "JCP007",
            "Name": "Configure: iDRAC.Embedded.1",
            "PercentComplete": 100,
            "StartTime": "2025-04-01T11:05:16",
            "TargetSettingsURI": None,
            "status_code": 200}
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_job_status_info",
                     return_value=True)
        idrac_default_args.update({"job_id": "job_id"})
        idrac_redfish_system_info_mock.get_entityjson.return_value = None
        idrac_redfish_system_info_connection_mock.invoke_request.return_value = obj
        idrac_redfish_system_info_connection_mock.get_json_device.return_value = ""
        idrac_get_lc_job_status_connection_mock.job_mgr.get_job_status.return_value = {"Status": "Success"}
        result = self._run_module(idrac_default_args)
        assert result["changed"] is False

    def test_main_idrac_get_lc_job_status_success_case05(self, idrac_get_lc_job_status_connection_mock,
                                                         idrac_redfish_system_info_mock,
                                                         idrac_redfish_system_info_connection_mock,
                                                         idrac_default_args,
                                                         mocker):
        obj = MagicMock()
        obj.status_code = 200
        obj.json_data = {
            "ActualRunningStartTime": None,
            "ActualRunningStopTime": None,
            "CompletionTime": "2025-04-01T11:05:17",
            "Description": "Job Instance",
            "EndTime": "TIME_NA",
            "Id": "JID_435235166998",
            "JobState": "Pending",
            "JobType": "iDRACConfiguration",
            "Message": "Job is in progress",
            "MessageArgs": ["NA"],
            "MessageId": "JCP007",
            "Name": "Configure: iDRAC.Embedded.1",
            "PercentComplete": 100,
            "StartTime": "2025-04-01T11:05:16",
            "TargetSettingsURI": None,
            "status_code": 200}
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_job_status_info",
                     return_value=True)
        idrac_default_args.update({"job_id": "job_id"})
        idrac_redfish_system_info_mock.get_entityjson.return_value = None
        idrac_redfish_system_info_connection_mock.invoke_request.return_value = obj
        idrac_redfish_system_info_connection_mock.get_json_device.return_value = ""
        idrac_get_lc_job_status_connection_mock.job_mgr.get_job_status.return_value = {"Status": "Success"}
        result = self._run_module(idrac_default_args)
        assert result["changed"] is False

    @pytest.mark.parametrize("exc_type", [SSLValidationError, URLError, ValueError, TypeError,
                                          ConnectionError, HTTPError])
    def test_main_exception_handling_case(self, exc_type, mocker, idrac_redfish_system_info_connection_mock,
                                          idrac_default_args):
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_job_status_info",
                     return_value=True)
        idrac_default_args.update({"job_id": "job_id"})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            idrac_redfish_system_info_connection_mock.invoke_request.side_effect = exc_type("exception message")
        elif exc_type in [URLError]:
            idrac_redfish_system_info_connection_mock.invoke_request.side_effect = exc_type("exception message")
        else:
            idrac_redfish_system_info_connection_mock.invoke_request.side_effect = exc_type('https://testhost.com', 400,
                                                                                            'http error message',
                                                                                            {"accept-type": "application/json"},
                                                                                            StringIO(json_str))
        if exc_type != URLError:
            result = self._run_module(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result
