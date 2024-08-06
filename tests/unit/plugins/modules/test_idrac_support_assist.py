# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.6.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

from io import StringIO
import json
import tempfile

import pytest
from urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils._text import to_text
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_support_assist
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from mock import MagicMock
from ansible_collections.dellemc.openmanage.plugins.modules.idrac_support_assist import main

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_support_assist.'
MODULE_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.'

SUCCESS_EXPORT_MSG = "Successfully exported the support assist collections."
SUCCESS_RUN_MSG = "Successfully ran the support assist collections."
SUCCESS_RUN_AND_EXPORT_MSG = "Successfully ran and exported the support assist collections."
RUNNING_RUN_MSG = "Successfully triggered the job to run support assist collections."
ALREADY_RUN_MSG = "The support assist collections job is already present."
EULA_ACCEPTED_MSG = "The SupportAssist End User License Agreement (EULA) is accepted by iDRAC user root via iDRAC interface REDFISH."
INVALID_DIRECTORY_MSG = "Provided directory path '{path}' is not valid."
NO_OPERATION_SKIP_MSG = "The operation is skipped."
INSUFFICIENT_DIRECTORY_PERMISSION_MSG = "Provided directory path '{path}' is not writable. " \
                                        "Please check if the directory has appropriate permissions"
UNSUPPORTED_FIRMWARE_MSG = "iDRAC firmware version is not supported."
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The parameter `job_wait_timeout` value cannot be negative or zero."
WAIT_TIMEOUT_MSG = "The job is not complete after {0} seconds."
CHANGES_FOUND_MSG = "Changes found to be applied."
CHANGES_NOT_FOUND_MSG = "No changes found to be applied."
ALLOWED_VALUES_MSG = "Enter a valid value from the list of allowable values: {0}"
PROXY_SERVER = "proxy.example.com"
PAYLOAD_FUNC = "SupportAssist.get_payload_details"
EULA_STATUS_FUNC = "AcceptEULA.eula_status"
VALIDATE_TIME_FUNC = "RunSupportAssist._RunSupportAssist__validate_time"
EXPORT_FUNC = "ExportSupportAssist._ExportSupportAssist__export_support_assist"
RUN_EXEC_FUNC = "RunSupportAssist.execute"
MESSAGE_EXTENDED = "@Message.ExtendedInfo"
ASSIST_ODATA = "/SupportAssistService"
REDFISH = "/redfish/v1"
REDFISH_DIAGNOSTICS_URL = "/redfish/v1/support_assist"
REDFISH_BASE_API = '/redfish/v1/api'
MANAGER_URI_ONE = "/redfish/v1/managers/1"
API_ONE = "/local/action"
EXPORT_URL_MOCK = '/redfish/v1/export_support_assist'
RUN_URL_MOCK = '/redfish/v1/run_support_assist'
API_INVOKE_MOCKER = "iDRACRedfishAPI.invoke_request"
ODATA = "@odata.id"
SHARE_NAME = tempfile.gettempdir()
IP = "X.X.X.X"
HTTPS_PATH = "https://testhost.com"
HTTP_ERROR = "http error message"
APPLICATION_JSON = "application/json"


class TestSupportAssist(FakeAnsibleModule):
    module = idrac_support_assist

    @pytest.fixture
    def idrac_support_assist_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_support_assist_mock(self, mocker, idrac_support_assist_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_support_assist_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_support_assist_mock
        return idrac_conn_mock

    def test_execute(self, idrac_default_args, idrac_connection_support_assist_mock):
        obj = MagicMock()
        support_assist_obj = self.module.SupportAssist(idrac_connection_support_assist_mock, obj)
        support_assist_obj.execute()


class TestAcceptEULA(FakeAnsibleModule):
    module = idrac_support_assist

    @pytest.fixture
    def idrac_support_assist_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_support_assist_mock(self, mocker, idrac_support_assist_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_support_assist_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_support_assist_mock
        return idrac_conn_mock

    def test_execute(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        obj = MagicMock()
        # Scenario 1: run and accept_eula both as true
        obj.status_code = 200
        obj.json_data = {
            MESSAGE_EXTENDED: [
                {
                    "Message": EULA_ACCEPTED_MSG,
                    "MessageId": "IDRAC.2.8.SRV074"
                },
                {
                    "Message": "The request completed successfully.",
                    "MessageId": "Base.1.12.Success"
                }
            ]
        }
        mocker.patch(MODULE_PATH + "AcceptEULA._AcceptEULA__get_eula_status_url", return_value=None)
        mocker.patch(MODULE_PATH + "AcceptEULA._AcceptEULA__get_eula_accept_url", return_value=None)
        mocker.patch(MODULE_PATH + EULA_STATUS_FUNC, return_value=obj)
        idrac_default_args.update({'run': True, 'accept_eula': True, 'export': False})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        support_assist_obj = self.module.AcceptEULA(idrac_connection_support_assist_mock, f_module)
        msg = support_assist_obj.execute()
        assert msg == EULA_ACCEPTED_MSG

        # Scenario 2: Only accept_eula as true when eula is not accepted
        obj2 = MagicMock()
        obj2.status_code = 200
        obj2.json_data = {
            MESSAGE_EXTENDED: [
                {
                    "Message": EULA_ACCEPTED_MSG,
                    "MessageId": "IDRAC.2.8.SRV074",
                }
            ]
        }
        mocker.patch(MODULE_PATH + "AcceptEULA._AcceptEULA__get_eula_status_url", return_value=None)
        mocker.patch(MODULE_PATH + "AcceptEULA._AcceptEULA__get_eula_accept_url", return_value=None)
        mocker.patch(MODULE_PATH + EULA_STATUS_FUNC, return_value=obj)
        mocker.patch(MODULE_PATH + "AcceptEULA.accept_eula", return_value=obj2)
        idrac_default_args.update({'run': False, 'accept_eula': True, 'export': False})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        support_assist_obj = self.module.AcceptEULA(idrac_connection_support_assist_mock, f_module)
        msg = support_assist_obj.execute()
        assert msg == EULA_ACCEPTED_MSG

    def test_get_eula_status_url(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        # Scenario 1: With url
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value={"Links": {"Oem": {"Dell": {"DellLCService": {ODATA: ASSIST_ODATA}}}},
                                   "Actions": {"#DellLCService.SupportAssistGetEULAStatus": {"target": API_ONE}}})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        eula_status_support_assist_obj = self.module.AcceptEULA(idrac_connection_support_assist_mock, f_module)
        eula_status_support_assist_obj._AcceptEULA__get_eula_status_url()
        assert eula_status_support_assist_obj.eula_status_url == API_ONE

        # Scenario 2: When url is empty for Links
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value={"Links": {}})
        with pytest.raises(Exception) as exc:
            eula_status_support_assist_obj._AcceptEULA__get_eula_status_url()
        assert exc.value.args[0] == UNSUPPORTED_FIRMWARE_MSG

        # Scenario 3: For error message
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, "error"))
        with pytest.raises(Exception) as exc:
            eula_status_support_assist_obj._AcceptEULA__get_eula_status_url()
        assert exc.value.args[0] == "error"

    def test_get_eula_accept_url(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        # Scenario 1: With url
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value={"Links": {"Oem": {"Dell": {"DellLCService": {ODATA: ASSIST_ODATA}}}},
                                   "Actions": {"#DellLCService.SupportAssistAcceptEULA": {"target": API_ONE}}})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        eula_accept_obj = self.module.AcceptEULA(idrac_connection_support_assist_mock, f_module)
        eula_accept_obj._AcceptEULA__get_eula_accept_url()
        assert eula_accept_obj.eula_accept_url == API_ONE

        # Scenario 2: When url is empty for Links
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value={"Links": {}})
        with pytest.raises(Exception) as exc:
            eula_accept_obj._AcceptEULA__get_eula_accept_url()
        assert exc.value.args[0] == UNSUPPORTED_FIRMWARE_MSG

        # Scenario 3: For error message
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, "error"))
        with pytest.raises(Exception) as exc:
            eula_accept_obj._AcceptEULA__get_eula_accept_url()
        assert exc.value.args[0] == "error"

    def test_eula_status(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        obj = MagicMock()
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        eula_status_obj = self.module.AcceptEULA(idrac_connection_support_assist_mock, f_module)
        status = eula_status_obj.eula_status()
        assert status

    def test_accept_eula(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        obj = MagicMock()
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        eula_accept_obj = self.module.AcceptEULA(idrac_connection_support_assist_mock, f_module)
        status = eula_accept_obj.accept_eula()
        assert status

    def test_perform_check_mode(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        obj = MagicMock()
        obj.status_code = 200
        mocker.patch(MODULE_PATH + EULA_STATUS_FUNC, return_value=obj)
        idrac_default_args.update({"accept_eula": True})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        cm_obj = self.module.AcceptEULA(idrac_connection_support_assist_mock, f_module)
        # Scenario 1: When EULA is not accepted
        obj.json_data = {
            MESSAGE_EXTENDED: [
                {
                    "Message": "The SupportAssist End User License Agreement (EULA) is not accepted.",
                    "MessageId": "IDRAC.2.8.SRV104",
                }
            ]
        }
        with pytest.raises(Exception) as exc:
            cm_obj.perform_check_mode()
        assert exc.value.args[0] == 'Changes found to be applied.'

        # Scenario 2: When EULA is accepted
        obj.json_data = {
            MESSAGE_EXTENDED: [
                {
                    "Message": EULA_ACCEPTED_MSG,
                    "MessageId": "IDRAC.2.8.SRV074",
                }
            ]
        }
        with pytest.raises(Exception) as exc:
            cm_obj.perform_check_mode()
        assert exc.value.args[0] == 'No changes found to be applied.'


class TestRunSupportAssist(FakeAnsibleModule):
    module = idrac_support_assist

    @pytest.fixture
    def idrac_support_assist_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_support_assist_mock(self, mocker, idrac_support_assist_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_support_assist_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_support_assist_mock
        return idrac_conn_mock

    def test_execute(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        obj = MagicMock()
        obj.status_code = 200
        # Scenario 1: JobState is completed
        job = {"JobState": "Completed"}
        idrac_default_args.update({'data_collector': ['gpu_logs'], 'export': False})
        mocker.patch(MODULE_PATH + "RunSupportAssist._RunSupportAssist__get_run_support_assist_url", return_value=None)
        mocker.patch(MODULE_PATH + "RunSupportAssist.check_support_assist_jobs", return_value=None)
        mocker.patch(MODULE_PATH + "RunSupportAssist._RunSupportAssist__run_support_assist", return_value=obj)
        mocker.patch(MODULE_PATH + "RunSupportAssist._RunSupportAssist__validate_job_timeout", return_value=None)
        mocker.patch(MODULE_PATH + "RunSupportAssist._RunSupportAssist__perform_job_wait", return_value=job)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(idrac_connection_support_assist_mock, f_module)
        msg, job_status = run_support_assist_obj.execute()
        assert msg == SUCCESS_RUN_MSG
        assert job_status == job

        # Scenario 2: JobState is scheduled
        job = {"JobState": "Scheduled"}
        idrac_default_args.update({'data_collector': ['gpu_logs'], 'export': False})
        mocker.patch(MODULE_PATH + "RunSupportAssist._RunSupportAssist__perform_job_wait", return_value=job)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(idrac_connection_support_assist_mock, f_module)
        msg, job_status = run_support_assist_obj.execute()
        assert msg == RUNNING_RUN_MSG
        assert job_status == job

    def test_run_support_assist(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        obj = MagicMock()
        obj.status_code = 200
        mocker.patch(MODULE_PATH + "RunSupportAssist._RunSupportAssist__get_run_support_assist_url", return_value=API_ONE)
        mocker.patch(MODULE_PATH + "RunSupportAssist._RunSupportAssist__validate_input", return_value=None)
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)

        # Scenario 1: With data_collector as gpu_logs
        run_params = {
            'data_collector': ['gpu_logs']
        }
        idrac_default_args.update(run_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(idrac_connection_support_assist_mock, f_module)
        status = run_support_assist_obj._RunSupportAssist__run_support_assist()
        assert status == obj

        # Scenario 2: With data_collector as gpu_logs and filter_data as true
        run_params = {
            'data_collector': ['gpu_logs'],
            'filter_data': True
        }
        idrac_default_args.update(run_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(idrac_connection_support_assist_mock, f_module)
        status = run_support_assist_obj._RunSupportAssist__run_support_assist()
        assert status == obj

        # Scenario 3: With all the data_collector and filter_data as true
        run_params = {
            'data_collector': ['storage_logs', 'os_app_data', 'debug_logs', 'telemetry_reports', 'gpu_logs', 'tty_logs'],
            'filter_data': True
        }
        idrac_default_args.update(run_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(idrac_connection_support_assist_mock, f_module)
        status = run_support_assist_obj._RunSupportAssist__run_support_assist()
        assert status == obj

    def test_validate_input(self, idrac_default_args, idrac_connection_support_assist_mock, mocker, ):
        obj = MagicMock()
        obj.status_code = 200
        obj.json_data = {
            "Actions": {
                "#DellLCService.SupportAssistCollection": {
                    "DataSelectorArrayIn@Redfish.AllowableValues": [
                        "DebugLogs",
                        "HWData",
                        "OSAppData",
                        "TTYLogs",
                        "TelemetryReports"
                    ]}}}
        data_selector = {
            "storage_logs": "HWData",
            "os_app_data": "OSAppData",
            "debug_logs": "DebugLogs",
            "telemetry_reports": "TelemetryReports",
            "gpu_logs": "GPULogs",
            "tty_logs": "TTYLogs"
        }
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri", return_value=(REDFISH, None))
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value={"Links": {"Oem": {"Dell": {"DellLCService": {ODATA: ASSIST_ODATA}}}}})
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(idrac_connection_support_assist_mock, f_module)
        # Scenario 1: Valid input which is not in allowable values
        data_selected = ['GPULogs']
        with pytest.raises(Exception) as exc:
            run_support_assist_obj._RunSupportAssist__validate_input(data_selected, data_selector)
        assert exc.value.args[0] == ALLOWED_VALUES_MSG.format(['storage_logs', 'os_app_data', 'debug_logs', 'telemetry_reports', 'tty_logs'])

        # Scenario 2: Valid input which is in allowable values
        data_selected = ['HWData']
        obj = run_support_assist_obj._RunSupportAssist__validate_input(data_selected, data_selector)
        assert obj is None

    def test_get_run_support_assist_url(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        # Scenario 1: With url
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value={"Links": {"Oem": {"Dell": {"DellLCService": {ODATA: ASSIST_ODATA}}}},
                                   "Actions": {"#DellLCService.SupportAssistCollection": {"target": API_ONE}}})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(idrac_connection_support_assist_mock, f_module)
        run_support_assist_obj._RunSupportAssist__get_run_support_assist_url()
        assert run_support_assist_obj.run_url == API_ONE

        # Scenario 2: When url is empty for Links
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value={"Links": {}})
        with pytest.raises(Exception) as exc:
            run_support_assist_obj._RunSupportAssist__get_run_support_assist_url()
        assert exc.value.args[0] == UNSUPPORTED_FIRMWARE_MSG

        # Scenario 3: For error message
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, "error"))
        with pytest.raises(Exception) as exc:
            run_support_assist_obj._RunSupportAssist__get_run_support_assist_url()
        assert exc.value.args[0] == "error"

    def test_check_support_assist_jobs(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        obj = MagicMock()
        temp_list = {"Members": [{"Id": "JID_123", "JobType": "SACollectExportHealthData", "JobState": "New"}]}
        obj.json_data = temp_list
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        run_support_assist_obj = self.module.RunSupportAssist(idrac_connection_support_assist_mock, f_module)

        # Scenario 1: Check mode with job id
        with pytest.raises(Exception) as exc:
            run_support_assist_obj.check_support_assist_jobs()
        assert exc.value.args[0] == ALREADY_RUN_MSG

        # # Scenario 2: Check mode without job id
        # temp_list = {"Members": [{"Id": "", "JobType": "Test", "JobState": "New"}]}
        # obj.json_data = temp_list
        # mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        # f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        # run_support_assist_obj = self.run_module(idrac_connection_support_assist_mock, f_module)
        # resp = run_support_assist_obj.check_support_assist_jobs()
        # assert resp is None

        # Scenario 3: Normal mode with job id
        temp_list = {"Members": [{"Id": "666", "JobType": "SACollectExportHealthData", "JobState": "New"}]}
        obj.json_data = temp_list
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(idrac_connection_support_assist_mock, f_module)
        with pytest.raises(Exception) as exc:
            run_support_assist_obj.check_support_assist_jobs()
        assert exc.value.args[0] == ALREADY_RUN_MSG

        # Scenario 4: Normal mode without job id
        temp_list = {"Members": [{"Id": "", "JobType": "SACollectExportHealthData", "JobState": "New"}]}
        obj.json_data = temp_list
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(idrac_connection_support_assist_mock, f_module)
        resp = run_support_assist_obj.check_support_assist_jobs()
        assert resp is None

    def test_validate_job_timeout(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        # Scenario 1: Negative timeout
        idrac_default_args.update({'job_wait': True, 'job_wait_timeout': -120})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(idrac_connection_support_assist_mock, f_module)
        with pytest.raises(Exception) as exc:
            run_support_assist_obj._RunSupportAssist__validate_job_timeout()
        assert exc.value.args[0] == TIMEOUT_NEGATIVE_OR_ZERO_MSG

        # Scenario 2: Valid timeout
        idrac_default_args.update({'job_wait': True, 'job_wait_timeout': 120})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(idrac_connection_support_assist_mock, f_module)
        resp = run_support_assist_obj._RunSupportAssist__validate_job_timeout()
        assert resp is None

    def test_perform_job_wait(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        # Scenario 1: When JobState is completed
        obj = MagicMock()
        obj.headers = {'Location': REDFISH_BASE_API}
        obj.json_data = {'JobState': 'Completed'}
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking",
                     return_value=(False, 'msg', obj.json_data, 120))
        idrac_default_args.update({'job_wait': True, 'job_wait_timeout': 1200})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(idrac_connection_support_assist_mock, f_module)
        job_dict = run_support_assist_obj._RunSupportAssist__perform_job_wait(obj)
        assert job_dict == obj.json_data

        # Scenario 2: When wait time is less
        obj = MagicMock()
        obj.headers = {'Location': REDFISH_BASE_API}
        obj.json_data = {'JobState': 'Scheduled'}
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking",
                     return_value=(False, 'msg', obj.json_data, 120))
        idrac_default_args.update({'job_wait': True, 'job_wait_timeout': 10})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(idrac_connection_support_assist_mock, f_module)
        with pytest.raises(Exception) as exc:
            run_support_assist_obj._RunSupportAssist__perform_job_wait(obj)
        assert exc.value.args[0] == WAIT_TIMEOUT_MSG.format(10)

        # Scenario 3: When JobState is Failed
        obj = MagicMock()
        obj.headers = {'Location': REDFISH_BASE_API}
        obj.json_data = {'JobState': 'Failed', 'Message': 'Job Failed'}
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking",
                     return_value=(True, 'msg', obj.json_data, 120))
        idrac_default_args.update({'job_wait': True, 'job_wait_timeout': 1200})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(idrac_connection_support_assist_mock, f_module)
        with pytest.raises(Exception) as exc:
            run_support_assist_obj._RunSupportAssist__perform_job_wait(obj)
        assert exc.value.args[0] == 'Job Failed'

        # Scenario 4: When job_wait is False
        obj = MagicMock()
        obj.headers = {'Location': REDFISH_BASE_API}
        obj.json_data = {'JobState': 'Scheduled'}
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking",
                     return_value=(True, 'msg', obj.json_data, 120))
        idrac_default_args.update({'job_wait': False, 'job_wait_timeout': 1200})
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(idrac_connection_support_assist_mock, f_module)
        job_dict = run_support_assist_obj._RunSupportAssist__perform_job_wait(obj)
        assert job_dict == obj.json_data

        # Scenario 5: When there's no job uri
        obj = MagicMock()
        obj.headers = {'Location': ''}
        idrac_default_args.update({'job_wait': False, 'job_wait_timeout': 1200})
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(idrac_connection_support_assist_mock, f_module)
        job_dict = run_support_assist_obj._RunSupportAssist__perform_job_wait(obj)
        assert job_dict == {}


class TestSupportAssistType(FakeAnsibleModule):
    module = idrac_support_assist

    @pytest.fixture
    def idrac_support_assist_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_support_assist_mock(self, mocker, idrac_support_assist_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_support_assist_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_support_assist_mock
        return idrac_conn_mock

    def test_support_assist_operation(self, idrac_default_args, idrac_connection_support_assist_mock):
        idrac_default_args.update({"run": True, "data_collector": ['gpu_logs'], "export": False})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        assist_class = self.module.SupportAssistType.support_assist_operation(idrac_connection_support_assist_mock, f_module)
        assert isinstance(assist_class, self.module.RunSupportAssist)

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_idrac_support_assist_main_exception_handling_case(self, exc_type, mocker, idrac_default_args):
        idrac_default_args.update({"run": True, "data_collector": ['gpu_logs'], "export": False})
        # Scenario 1: HTTPError with message id SRV095
        json_str = to_text(json.dumps({"error": {MESSAGE_EXTENDED: [
            {
                'MessageId': "SRV095",
                "Message": "Error"
            }
        ]}}))
        if exc_type in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + RUN_EXEC_FUNC,
                         side_effect=exc_type(HTTPS_PATH, 400,
                                              HTTP_ERROR,
                                              {"accept-type": APPLICATION_JSON},
                                              StringIO(json_str)))
        else:
            mocker.patch(MODULE_PATH + RUN_EXEC_FUNC,
                         side_effect=exc_type('test'))
        result = self._run_module(idrac_default_args)
        if exc_type == URLError:
            assert result['unreachable'] is True
        assert 'msg' in result

        # Scenario 2: HTTPError with message id SRV085
        json_str = to_text(json.dumps({"error": {MESSAGE_EXTENDED: [
            {
                'MessageId': "SRV085",
                "Message": "Error"
            }
        ]}}))
        if exc_type in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + RUN_EXEC_FUNC,
                         side_effect=exc_type(HTTPS_PATH, 400,
                                              HTTP_ERROR,
                                              {"accept-type": APPLICATION_JSON},
                                              StringIO(json_str)))
        result = self._run_module(idrac_default_args)
        assert 'msg' in result

        # Scenario 3: HTTPError with random message id
        json_str = to_text(json.dumps({"error": {MESSAGE_EXTENDED: [
            {
                'MessageId': "123",
                "Message": "Error"
            }
        ]}}))
        if exc_type in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + RUN_EXEC_FUNC,
                         side_effect=exc_type(HTTPS_PATH, 400,
                                              HTTP_ERROR,
                                              {"accept-type": APPLICATION_JSON},
                                              StringIO(json_str)))
        result = self._run_module(idrac_default_args)
        assert 'msg' in result

    def test_main(self, mocker):
        module_mock = mocker.MagicMock()
        idrac_mock = mocker.MagicMock()
        support_assist_mock = mocker.MagicMock()
        support_assist_mock.execute.return_value = (None, None)
        mocker.patch(MODULE_PATH + 'get_argument_spec', return_value={})
        mocker.patch(MODULE_PATH + 'IdracAnsibleModule', return_value=module_mock)
        mocker.patch(MODULE_PATH + 'iDRACRedfishAPI', return_value=idrac_mock)
        mocker.patch(MODULE_PATH + 'SupportAssistType.support_assist_operation', return_value=support_assist_mock)
        main()
        support_assist_mock.execute.return_value = (None, None)
        mocker.patch(MODULE_PATH + 'SupportAssistType.support_assist_operation', return_value=support_assist_mock)
        main()
