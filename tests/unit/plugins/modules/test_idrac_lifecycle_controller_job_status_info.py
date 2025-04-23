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
from ansible_collections.dellemc.openmanage.plugins.\
    module_utils.idrac_utils.info.lifecycle_controller_job_status import IDRACLifecycleControllerJobStatusInfo
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
JOB_MEMBERS = [
    {
        "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/job_id"
    },
]
JOB_LINK = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/job_id"
RESPONSE = {
    "Status": {
        "Health": "OK",
        "State": "Enabled"
    },
    "LastResetTime": "2025-04-15T05:34:47-05:00",
    "DateTime": "2025-04-15T09:39:04-05:00",
    "PowerState": "On",
    "GraphicalConsole": {
        "ServiceEnabled": True,
        "ConnectTypesSupported": [
            "KVMIP"
        ],
        "ConnectTypesSupported@odata.count": 1,
        "MaxConcurrentSessions": 6
    },
    "SerialConsole": {
        "ServiceEnabled": False,
        "ConnectTypesSupported": [
        ],
        "ConnectTypesSupported@odata.count": 0,
        "MaxConcurrentSessions": 0
    },
    "SerialNumber": "CNWS3004A700O2",
    "LogServices": {
        "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/LogServices"
    },
    "TimeZoneName": "CST6CDT",
    "ServiceIdentification": "DN04203",
    "Model": "17G Monolithic",
    "Name": "Manager",
    "DateTimeLocalOffset": "-05:00",
    "Certificates": {
        "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Certificates"
    },
    "EthernetInterfaces": {
        "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/EthernetInterfaces"
    },
    "@odata.type": "#Manager.v1_20_0.Manager",
    "Oem": {
        "Dell": {
            "Jobs": {
                "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs"
            },
        }
    },
    "PartNumber": "03TJR3",
    "ManagerType": "BMC",
    "Redundancy@odata.count": 0,
    "ManagerDiagnosticData": {
        "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/ManagerDiagnosticData"
    },
    "Id": "iDRAC.Embedded.1"
}

JOB_RESPONSE = {
    "ActualRunningStopTime": None,
    "@odata.etag": "W/\"gen-31\"",
    "Id": "job_id",
    "EndTime": None,
    "PercentComplete": 100,
    "Description": "Job Instance",
    "MessageId": "RED106",
    "Message": "Unable to parse the lc_validator_output.xml file because of an internal error.",
    "Name": "update:new",
    "StartTime": "2025-04-15T06:01:03",
    "JobType": "FirmwareUpdate",
    "MessageArgs": [],
    "MessageArgs@odata.count": 0,
    "JobState": "Failed",
    "ActualRunningStartTime": None,
    "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/job_id",
    "TargetSettingsURI": None,
    "@odata.type": "#DellJob.v1_6_0.DellJob",
    "CompletionTime": "2025-04-15T06:01:14",
    "@odata.context": "/redfish/v1/$metadata#DellJob.DellJob"
}


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
    def idrac_lc_job_status_info_mock(self):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.get_entityjson = idrac_obj
        type(idrac_obj).get_json_device = Mock(return_value="msg")
        return idrac_obj

    @pytest.fixture
    def idrac_lc_job_status_info_connection_mock(self, mocker, idrac_lc_job_status_info_mock):
        idrac_redfish_conn_class_mock = mocker.patch(MODULE_PATH +
                                                     'idrac_lifecycle_controller_job_status_info.iDRACRedfishAPI',
                                                     return_value=idrac_lc_job_status_info_mock)
        idrac_redfish_conn_class_mock.return_value.__enter__.return_value = idrac_lc_job_status_info_mock
        return idrac_lc_job_status_info_mock

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
                                                         idrac_lc_job_status_info_mock,
                                                         idrac_lc_job_status_info_connection_mock,
                                                         idrac_default_args,
                                                         mocker):
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_job_status_info",
                     return_value=True)
        json_str = to_text(json.dumps({"data": "out"}))
        idrac_lc_job_status_info_mock.get_entityjson.return_value = None
        idrac_lc_job_status_info_connection_mock.get_json_device.return_value = ""
        idrac_lc_job_status_info_connection_mock.invoke_request.side_effect = exc_type(
            'https://testhost.com', 404,
            'http error message',
            {"accept-type": "application/json"},
            StringIO(json_str))
        idrac_default_args.update({"job_id": "job_id"})
        idrac_get_lc_job_status_connection_mock.job_mgr.get_job_status.return_value = {"Status": "Success"}
        result = self._run_module(idrac_default_args)
        assert result["changed"] is False

    @pytest.mark.parametrize("exc_type", [HTTPError])
    def test_main_idrac_get_lc_job_status_success_case03(self, idrac_get_lc_job_status_connection_mock,
                                                         exc_type,
                                                         idrac_lc_job_status_info_mock,
                                                         idrac_lc_job_status_info_connection_mock,
                                                         idrac_default_args,
                                                         mocker):
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_job_status_info",
                     return_value=True)
        json_str = to_text(json.dumps({"data": "out"}))
        idrac_lc_job_status_info_mock.get_entityjson.return_value = None
        idrac_lc_job_status_info_connection_mock.get_json_device.return_value = ""
        idrac_lc_job_status_info_connection_mock.invoke_request.side_effect = exc_type(
            'https://testhost.com', 404,
            'http error message',
            {"accept-type": "application/json"},
            StringIO(json_str))
        idrac_default_args.update({"job_id": "job_id"})
        idrac_get_lc_job_status_connection_mock.job_mgr.get_job_status.return_value = {"Status": "Found Fault"}
        result = self._run_module(idrac_default_args)
        assert result == {
            "msg": "Successfully fetched the job info.",
            "job_info": {},
            "changed": False}

    def test_get_lifecycle_controller_job_status_info_case02(
            self,
            idrac_default_args,
            idrac_mock,
            mocker):
        idrac_default_args.update({"job_id": "job_id"})
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_job_status_info.IDRACFirmwareInfo.is_omsdk_required",
                     return_value=False)
        idrac_mock.invoke_request.return_value.status_code = 200
        response1 = MagicMock()
        response1.json_data = {"status": "Success"}
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_job_status_info.IDRACLifecycleControllerJobStatusInfo.get_lifecycle_controller_job_status_info",
                     return_value=response1)
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_job_status_info.IDRACLifecycleControllerJobStatusInfo.transform_job_status_data",
                     return_value={"status": "Success"})
        result = self._run_module(idrac_default_args)
        assert result == {
            "job_info": {"status": "Success"},
            "msg": "Successfully fetched the job info.",
            "changed": False}

    def test_get_lifecycle_controller_job_status_info_invalid_id(
            self,
            idrac_default_args,
            idrac_mock,
            mocker):
        idrac_default_args.update({"job_id": "job_id"})
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_job_status_info.IDRACFirmwareInfo.is_omsdk_required",
                     return_value=False)
        idrac_mock.invoke_request.return_value.status_code = 200
        response1 = "Job ID is invalid"
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_job_status_info.IDRACLifecycleControllerJobStatusInfo.get_lifecycle_controller_job_status_info",
                     return_value=response1)
        result = self._run_module(idrac_default_args)
        assert result == {
            "msg": "Successfully fetched the job info.",
            "job_info": {},
            "changed": False}

    def test_get_lifecycle_controller_job_status_info(self, idrac_mock, idrac_default_args):
        idrac_default_args.update({"job_id": "job_id"})
        idrac_mock.invoke_request.return_value.json_data = RESPONSE
        idrac_lc_job_status_info = IDRACLifecycleControllerJobStatusInfo(idrac_mock)
        idrac_lc_job_status_info.get_lifecycle_controller_job_list = \
            MagicMock(return_value=JOB_RESPONSE)
        result = idrac_lc_job_status_info.get_lifecycle_controller_job_status_info(job_id="job_id")
        expected_result = {
            '@odata.context': '/redfish/v1/$metadata#DellJob.DellJob',
            '@odata.etag': 'W/"gen-31"',
            '@odata.id': '/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/job_id',
            '@odata.type': '#DellJob.v1_6_0.DellJob',
            'ActualRunningStartTime': None,
            'ActualRunningStopTime': None,
            'CompletionTime': '2025-04-15T06:01:14',
            'JobType': 'FirmwareUpdate',
            'Description': 'Job Instance',
            'EndTime': None,
            'Id': 'job_id',
            'JobState': 'Failed',
            'Message': 'Unable to parse the lc_validator_output.xml file because of an internal '
            'error.',
            'MessageArgs': [],
            'MessageArgs@odata.count': 0,
            'MessageId': 'RED106',
            'Name': 'update:new',
            'PercentComplete': 100,
            'StartTime': '2025-04-15T06:01:03',
            'TargetSettingsURI': None,
        }
        assert result == expected_result

    @pytest.mark.parametrize("exc_type", [SSLValidationError, URLError, ValueError, TypeError,
                                          ConnectionError, HTTPError])
    def test_main_exception_handling_case(self, exc_type, mocker, idrac_lc_job_status_info_connection_mock,
                                          idrac_default_args):
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_job_status_info",
                     return_value=True)
        idrac_default_args.update({"job_id": "job_id"})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            idrac_lc_job_status_info_connection_mock.invoke_request.side_effect = exc_type("exception message")
        elif exc_type in [URLError]:
            idrac_lc_job_status_info_connection_mock.invoke_request.side_effect = exc_type("exception message")
        else:
            idrac_lc_job_status_info_connection_mock.invoke_request.side_effect = exc_type(
                'https://testhost.com', 400,
                'http error message',
                {"accept-type": "application/json"},
                StringIO(json_str))
        if exc_type != URLError:
            result = self._run_module(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result
