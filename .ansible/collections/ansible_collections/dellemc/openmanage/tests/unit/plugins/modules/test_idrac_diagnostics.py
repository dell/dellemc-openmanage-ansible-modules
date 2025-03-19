# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
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
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_diagnostics
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from unittest.mock import MagicMock
from ansible_collections.dellemc.openmanage.plugins.modules.idrac_diagnostics import main

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_diagnostics.'
MODULE_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.'

SUCCESS_EXPORT_MSG = "Successfully exported the diagnostics."
FAILURE_EXPORT_MSG = "Unable to copy the ePSA Diagnostics results file to the network share."
SUCCESS_RUN_MSG = "Successfully ran the diagnostics operation."
SUCCESS_RUN_AND_EXPORT_MSG = "Successfully ran and exported the diagnostics."
RUNNING_RUN_MSG = "Successfully triggered the job to run diagnostics."
ALREADY_RUN_MSG = "The diagnostics job is already present."
INVALID_DIRECTORY_MSG = "Provided directory path '{path}' is not valid."
NO_OPERATION_SKIP_MSG = "The operation is skipped."
INSUFFICIENT_DIRECTORY_PERMISSION_MSG = "Provided directory path '{path}' is not writable. " \
                                        "Please check if the directory has appropriate permissions"
UNSUPPORTED_FIRMWARE_MSG = "iDRAC firmware version is not supported."
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The parameter `job_wait_timeout` value cannot be negative or zero."
WAIT_TIMEOUT_MSG = "The job is not complete after {0} seconds."
START_TIME = "The specified scheduled time occurs in the past, " \
             "provide a future time to schedule the job."
INVALID_TIME = "The specified date and time `{0}` to schedule the diagnostics is not valid. Enter a valid date and time."
END_START_TIME = "The end time `{0}` to schedule the diagnostics must be greater than the start time `{1}`."
CHANGES_FOUND_MSG = "Changes found to be applied."
NO_FILE = "The diagnostics file does not exist."

PROXY_SERVER = "proxy.example.com"
PAYLOAD_FUNC = "Diagnostics.get_payload_details"
VALIDATE_TIME_FUNC = "RunDiagnostics._RunDiagnostics__validate_time"
EXPORT_FUNC = "ExportDiagnostics._ExportDiagnostics__export_diagnostics"
RUN_EXEC_FUNC = "RunDiagnostics.execute"
MESSAGE_EXTENDED = "@Message.ExtendedInfo"
DIAGS_ODATA = "/DiagnosticsService"
REDFISH = "/redfish/v1"
REDFISH_DIAGNOSTICS_URL = "/redfish/v1/diagnostics"
REDFISH_BASE_API = '/redfish/v1/api'
MANAGER_URI_ONE = "/redfish/v1/managers/1"
API_ONE = "/local/action"
EXPORT_URL_MOCK = '/redfish/v1/export_diagnostics'
RUN_URL_MOCK = '/redfish/v1/import_diagnostics'
API_INVOKE_MOCKER = "iDRACRedfishAPI.invoke_request"
ODATA = "@odata.id"
DIAGS_FILE_NAME = 'test_diagnostics.txt'
SHARE_NAME = tempfile.gettempdir()
IP = "X.X.X.X"
HTTPS_PATH = "https://testhost.com"
HTTP_ERROR = "http error message"
APPLICATION_JSON = "application/json"


class TestDiagnostics(FakeAnsibleModule):
    module = idrac_diagnostics

    @pytest.fixture
    def idrac_diagnostics_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_diagnostics_mock(self, mocker, idrac_diagnostics_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_diagnostics_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_diagnostics_mock
        return idrac_conn_mock

    def test_execute(self, idrac_default_args, idrac_connection_diagnostics_mock):
        obj = MagicMock()
        diagnostics_obj = self.module.Diagnostics(idrac_connection_diagnostics_mock, obj)
        diagnostics_obj.execute()

    def test_get_payload_details(self, idrac_connection_diagnostics_mock):
        obj = MagicMock()
        diags_obj = self.module.Diagnostics(idrac_connection_diagnostics_mock, obj)
        # Scenario 1: With all values
        obj.params.get.return_value = {
            'ip_address': IP,
            'share_name': 'my_share',
            'username': 'my_user',
            'password': 'my_password',
            'file_name': DIAGS_FILE_NAME,
            'share_type': 'http',
            'ignore_certificate_warning': 'on',
            'proxy_support': 'parameters_proxy',
            'proxy_type': 'socks',
            'proxy_server': PROXY_SERVER,
            'proxy_port': 8080,
            'proxy_username': 'my_username',
            'proxy_password': 'my_password'
        }
        result = diags_obj.get_payload_details()
        expected_result = {
            'IPAddress': IP,
            'ShareName': 'my_share',
            'UserName': 'my_user',
            'Password': 'my_password',
            'FileName': DIAGS_FILE_NAME,
            'ShareType': 'HTTP',
            'IgnoreCertWarning': 'On',
            'ProxySupport': 'ParametersProxy',
            'ProxyType': 'SOCKS',
            'ProxyServer': PROXY_SERVER,
            'ProxyPort': '8080',
            'ProxyUname': 'my_username',
            'ProxyPasswd': 'my_password'
        }
        assert result == expected_result

        # Scenario 2: With no proxy values
        obj.params.get.return_value = {
            'ip_address': IP,
            'share_name': 'my_share',
            'username': 'my_user',
            'password': 'my_password',
            'file_name': DIAGS_FILE_NAME,
            'share_type': 'http',
            'ignore_certificate_warning': 'on'
        }
        result = diags_obj.get_payload_details()
        expected_result = {
            'IPAddress': IP,
            'ShareName': 'my_share',
            'UserName': 'my_user',
            'Password': 'my_password',
            'FileName': DIAGS_FILE_NAME,
            'ShareType': 'HTTP',
            'IgnoreCertWarning': 'On'
        }
        assert result == expected_result

        # Scenario 3: With no proxy username and password values
        obj.params.get.return_value = {
            'ip_address': IP,
            'share_name': 'my_share',
            'username': 'my_user',
            'password': 'my_password',
            'file_name': DIAGS_FILE_NAME,
            'share_type': 'http',
            'ignore_certificate_warning': 'on',
            'proxy_support': 'parameters_proxy',
            'proxy_type': 'socks',
            'proxy_server': PROXY_SERVER,
            'proxy_port': 8080
        }
        result = diags_obj.get_payload_details()
        expected_result = {
            'IPAddress': IP,
            'ShareName': 'my_share',
            'UserName': 'my_user',
            'Password': 'my_password',
            'FileName': DIAGS_FILE_NAME,
            'ShareType': 'HTTP',
            'IgnoreCertWarning': 'On',
            'ProxySupport': 'ParametersProxy',
            'ProxyType': 'SOCKS',
            'ProxyServer': PROXY_SERVER,
            'ProxyPort': '8080'
        }
        assert result == expected_result

    def test_network_share(self, idrac_connection_diagnostics_mock, idrac_default_args, mocker):
        # Scenario 1: ShareType is LOCAL and directory is invalid
        payload = {"FileName": DIAGS_FILE_NAME, "ShareType": "LOCAL", "ShareName": "my_share"}
        mocker.patch(MODULE_PATH + PAYLOAD_FUNC, return_value=payload)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        diagnostics_obj = self.module.Diagnostics(idrac_connection_diagnostics_mock, f_module)
        with pytest.raises(Exception) as exc:
            diagnostics_obj.test_network_share()
        assert exc.value.args[0] == INVALID_DIRECTORY_MSG.format(path="my_share")

        # Scenario 2: ShareType is LOCAL and directory is not writable
        payload = {"FileName": DIAGS_FILE_NAME, "ShareType": "HTTP", "ShareName": SHARE_NAME}
        mocker.patch(MODULE_PATH + PAYLOAD_FUNC, return_value=payload)
        mocker.patch(MODULE_PATH + "Diagnostics.get_test_network_share_url", return_value=API_ONE)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        diagnostics_obj = self.module.Diagnostics(idrac_connection_diagnostics_mock, f_module)
        ob = diagnostics_obj.test_network_share()
        assert ob is None

        # Scenario 3: ShareType is not LOCAL
        obj = MagicMock()
        payload = {"FileName": DIAGS_FILE_NAME, "ShareType": "HTTP", "ShareName": "my_share"}
        mocker.patch(MODULE_PATH + PAYLOAD_FUNC, return_value=payload)
        mocker.patch(MODULE_PATH + "Diagnostics.get_test_network_share_url", return_value=API_ONE)
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        diagnostics_obj = self.module.Diagnostics(idrac_connection_diagnostics_mock, f_module)
        diagnostics_obj.test_network_share()

        # Scenario 4: HTTP Error
        payload = {"FileName": DIAGS_FILE_NAME, "ShareType": "HTTP", "ShareName": "my_share"}
        mocker.patch(MODULE_PATH + PAYLOAD_FUNC, return_value=payload)
        json_str = to_text(json.dumps({"error": {MESSAGE_EXTENDED: [
            {
                'MessageId': "123",
                "Message": "Error"
            }
        ]}}))
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     side_effect=HTTPError(HTTPS_PATH, 400,
                                           HTTP_ERROR,
                                           {"accept-type": APPLICATION_JSON},
                                           StringIO(json_str)))
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        diagnostics_obj = self.module.Diagnostics(idrac_connection_diagnostics_mock, f_module)
        with pytest.raises(Exception) as exc:
            diagnostics_obj.test_network_share()
        assert exc.value.args[0] == 'Error'

    def test_get_test_network_share_url(self, idrac_connection_diagnostics_mock, idrac_default_args, mocker):
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value={"Links": {"Oem": {"Dell": {"DellLCService": {ODATA: DIAGS_ODATA}}}},
                                   "Actions": {"#DellLCService.TestNetworkShare": {"target": API_ONE}}})

        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        obj = self.module.Diagnostics(idrac_connection_diagnostics_mock, f_module)
        resp = obj.get_test_network_share_url()
        assert resp == API_ONE

        # Scenario 2: for error message
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, "Error"))
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        obj = self.module.Diagnostics(idrac_connection_diagnostics_mock, f_module)
        with pytest.raises(Exception) as exc:
            obj.get_test_network_share_url()
        assert exc.value.args[0] == "Error"


class TestRunDiagnostics(FakeAnsibleModule):
    module = idrac_diagnostics

    @pytest.fixture
    def idrac_diagnostics_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_diagnostics_mock(self, mocker, idrac_diagnostics_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_diagnostics_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_diagnostics_mock
        return idrac_conn_mock

    def test_execute(self, idrac_default_args, idrac_connection_diagnostics_mock, mocker):
        obj = MagicMock()
        obj.status_code = 200
        # Scenario 1: JobState is completed
        job = {"JobState": "Completed"}
        mocker.patch(MODULE_PATH + "Diagnostics.test_network_share", return_value=None)
        mocker.patch(MODULE_PATH + "RunDiagnostics._RunDiagnostics__get_run_diagnostics_url", return_value=None)
        mocker.patch(MODULE_PATH + "RunDiagnostics.check_diagnostics_jobs", return_value=None)
        mocker.patch(MODULE_PATH + "RunDiagnostics._RunDiagnostics__run_diagnostics", return_value=obj)
        mocker.patch(MODULE_PATH + "RunDiagnostics._RunDiagnostics__perform_job_wait", return_value=job)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        msg, job_status, file_path = run_diagnostics_obj.execute()
        assert msg == SUCCESS_RUN_MSG
        assert job_status == job
        assert file_path is None

        # Scenario 2: JobState is scheduled
        job = {"JobState": "Scheduled"}
        idrac_default_args.update({'export': True})
        mocker.patch(MODULE_PATH + "RunDiagnostics._RunDiagnostics__perform_job_wait", return_value=job)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        msg, job_status, file_path = run_diagnostics_obj.execute()
        assert msg == RUNNING_RUN_MSG
        assert job_status == job
        assert file_path is None

    def test_run_diagnostics(self, idrac_default_args, idrac_connection_diagnostics_mock, mocker):
        obj = MagicMock()
        obj.status_code = 200
        mocker.patch(MODULE_PATH + "RunDiagnostics._RunDiagnostics__get_run_diagnostics_url", return_value=API_ONE)
        mocker.patch(MODULE_PATH + "RunDiagnostics._RunDiagnostics__validate_time_format", return_value=True)
        mocker.patch(MODULE_PATH + VALIDATE_TIME_FUNC, return_value=True)
        mocker.patch(MODULE_PATH + "RunDiagnostics._RunDiagnostics__validate_end_time", return_value=True)
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)

        # Scenario 1: With start and end time
        run_params = {
            'run_mode': 'express',
            'reboot_type': 'power_cycle',
            'scheduled_start_time': '20240715235959',
            'scheduled_end_time': '20250715235959'
        }
        idrac_default_args.update(run_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        status = run_diagnostics_obj._RunDiagnostics__run_diagnostics()
        assert status == obj

        # Scenario 2: Without time
        run_params = {
            'run_mode': 'express',
            'reboot_type': 'force'
        }
        idrac_default_args.update(run_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        status = run_diagnostics_obj._RunDiagnostics__run_diagnostics()
        assert status == obj

        # Scenario 3: With start and end time as empty
        run_params = {
            'run_mode': 'express',
            'reboot_type': 'power_cycle',
            'scheduled_start_time': '',
            'scheduled_end_time': ''
        }
        idrac_default_args.update(run_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        status = run_diagnostics_obj._RunDiagnostics__run_diagnostics()
        assert status == obj

        # Scenario 4: With start time
        run_params = {
            'run_mode': 'express',
            'reboot_type': 'power_cycle',
            'scheduled_start_time': '20200715235959'
        }
        mocker.patch(MODULE_PATH + VALIDATE_TIME_FUNC, return_value=False)
        idrac_default_args.update(run_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        status = run_diagnostics_obj._RunDiagnostics__run_diagnostics()
        assert status == obj

        # Scenario 5: With end time
        run_params = {
            'run_mode': 'express',
            'reboot_type': 'power_cycle',
            'scheduled_end_time': '20200715235959'
        }
        mocker.patch(MODULE_PATH + VALIDATE_TIME_FUNC, return_value=False)
        idrac_default_args.update(run_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        status = run_diagnostics_obj._RunDiagnostics__run_diagnostics()
        assert status == obj

    def test_get_run_diagnostics_url(self, idrac_default_args, idrac_connection_diagnostics_mock, mocker):
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        # Scenario 1: With url
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value={"Links": {"Oem": {"Dell": {"DellLCService": {ODATA: DIAGS_ODATA}}}},
                                   "Actions": {"#DellLCService.RunePSADiagnostics": {"target": API_ONE}}})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        run_diagnostics_obj._RunDiagnostics__get_run_diagnostics_url()
        assert run_diagnostics_obj.run_url == API_ONE

        # Scenario 2: When url is empty for Links
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value={"Links": {}})
        with pytest.raises(Exception) as exc:
            run_diagnostics_obj._RunDiagnostics__get_run_diagnostics_url()
        assert exc.value.args[0] == UNSUPPORTED_FIRMWARE_MSG

        # Scenario 3: For error message
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, "error"))
        with pytest.raises(Exception) as exc:
            run_diagnostics_obj._RunDiagnostics__get_run_diagnostics_url()
        assert exc.value.args[0] == "error"

    def test_check_diagnostics_jobs(self, idrac_default_args, idrac_connection_diagnostics_mock, mocker):
        obj = MagicMock()
        temp_list = {"Members": [{"Id": "JID_123", "JobType": "RemoteDiagnostics", "JobState": "New"}]}
        obj.json_data = temp_list
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)

        # Scenario 1: Check mode with job id
        with pytest.raises(Exception) as exc:
            run_diagnostics_obj.check_diagnostics_jobs()
        assert exc.value.args[0] == ALREADY_RUN_MSG

        # Scenario 2: Check mode without job id
        temp_list = {"Members": [{"Id": "", "JobType": "Test", "JobState": "New"}]}
        obj.json_data = temp_list
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        with pytest.raises(Exception) as exc:
            run_diagnostics_obj.check_diagnostics_jobs()
        assert exc.value.args[0] == CHANGES_FOUND_MSG

        # Scenario 3: Normal mode with job id
        temp_list = {"Members": [{"Id": "666", "JobType": "RemoteDiagnostics", "JobState": "New"}]}
        obj.json_data = temp_list
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        with pytest.raises(Exception) as exc:
            run_diagnostics_obj.check_diagnostics_jobs()
        assert exc.value.args[0] == ALREADY_RUN_MSG

        # Scenario 4: Normal mode without job id
        temp_list = {"Members": [{"Id": "", "JobType": "RemoteDiagnostics", "JobState": "New"}]}
        obj.json_data = temp_list
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        resp = run_diagnostics_obj.check_diagnostics_jobs()
        assert resp is None

    def test_validate_job_timeout(self, idrac_default_args, idrac_connection_diagnostics_mock, mocker):
        # Scenario 1: Negative timeout
        idrac_default_args.update({'job_wait': True, 'job_wait_timeout': -120})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        with pytest.raises(Exception) as exc:
            run_diagnostics_obj._RunDiagnostics__validate_job_timeout()
        assert exc.value.args[0] == TIMEOUT_NEGATIVE_OR_ZERO_MSG

        # Scenario 2: Valid timeout
        idrac_default_args.update({'job_wait': True, 'job_wait_timeout': 120})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        resp = run_diagnostics_obj._RunDiagnostics__validate_job_timeout()
        assert resp is None

    def test_validate_time_format(self, idrac_default_args, idrac_connection_diagnostics_mock, mocker):
        idrac_default_args.update({'time': "20250715235959"})
        # Scenario 1: Time with offset
        time = "2024-09-14T05:59:35-05:00"
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        formatted_time = run_diagnostics_obj._RunDiagnostics__validate_time_format(time)
        assert formatted_time == "20240914055935"

        # Scenario 2: Time without offset
        time = "20250715235959"
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        formatted_time = run_diagnostics_obj._RunDiagnostics__validate_time_format(time)
        assert formatted_time == "20250715235959"

        # Scenario 3: Invalid time
        time = "2025"
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        with pytest.raises(Exception) as exc:
            run_diagnostics_obj._RunDiagnostics__validate_time_format(time)
        assert exc.value.args[0] == INVALID_TIME.format(time)

    def test_validate_time(self, idrac_default_args, idrac_connection_diagnostics_mock, mocker):
        resp = ("2024-09-14T05:59:35-05:00", "-05:00")
        mocker.patch(MODULE_PATH + "get_current_time", return_value=resp)

        # Scenario 1: Future time
        idrac_default_args.update({'time': "20250715235959"})
        time = idrac_default_args['time']
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        assert run_diagnostics_obj._RunDiagnostics__validate_time(time) is True

        # Scenario 2: Past time
        idrac_default_args.update({'time': "20230715235959"})
        time = idrac_default_args['time']
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        with pytest.raises(Exception) as exc:
            run_diagnostics_obj._RunDiagnostics__validate_time(time)
        assert exc.value.args[0] == START_TIME

    def test_validate_end_time(self, idrac_default_args, idrac_connection_diagnostics_mock, mocker):
        # Scenario 1: start_time less than end_time
        start_time = "20230715235959"
        end_time = "20240715235959"
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        assert run_diagnostics_obj._RunDiagnostics__validate_end_time(start_time, end_time) is True

        # Scenario 2: start_time greater than end_time
        start_time = "20250715235959"
        end_time = "20240715235959"
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        with pytest.raises(Exception) as exc:
            run_diagnostics_obj._RunDiagnostics__validate_end_time(start_time, end_time)
        assert exc.value.args[0] == END_START_TIME.format(end_time, start_time)

    def test_perform_job_wait(self, idrac_default_args, idrac_connection_diagnostics_mock, mocker):
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
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        job_dict = run_diagnostics_obj._RunDiagnostics__perform_job_wait(obj)
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
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        with pytest.raises(Exception) as exc:
            run_diagnostics_obj._RunDiagnostics__perform_job_wait(obj)
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
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        with pytest.raises(Exception) as exc:
            run_diagnostics_obj._RunDiagnostics__perform_job_wait(obj)
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
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        job_dict = run_diagnostics_obj._RunDiagnostics__perform_job_wait(obj)
        assert job_dict == obj.json_data

        # Scenario 5: When there's no job uri
        obj = MagicMock()
        obj.headers = {'Location': ''}
        idrac_default_args.update({'job_wait': False, 'job_wait_timeout': 1200})
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_diagnostics_obj = self.module.RunDiagnostics(idrac_connection_diagnostics_mock, f_module)
        job_dict = run_diagnostics_obj._RunDiagnostics__perform_job_wait(obj)
        assert job_dict == {}


class TestExportDiagnostics(FakeAnsibleModule):
    module = idrac_diagnostics

    @pytest.fixture
    def idrac_diagnostics_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_diagnostics_mock(self, mocker, idrac_diagnostics_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_diagnostics_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_diagnostics_mock
        return idrac_conn_mock

    def test_execute(self, idrac_default_args, idrac_connection_diagnostics_mock, mocker):
        obj = MagicMock()
        obj.headers = {"Location": REDFISH}
        obj.status_code = 200
        obj.share_name = SHARE_NAME
        obj.file_name = DIAGS_FILE_NAME
        mocker.patch(MODULE_PATH + "Diagnostics.test_network_share", return_value=None)
        mocker.patch(MODULE_PATH + "ExportDiagnostics._ExportDiagnostics__get_export_diagnostics_url", return_value=None)
        mocker.patch(MODULE_PATH + "ExportDiagnostics._ExportDiagnostics__export_diagnostics_local", return_value=obj)

        # Scenario 1: share_type = local
        export_params = {'share_parameters': {'share_type': "local"}}
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        export_diagnostics_obj = self.module.ExportDiagnostics(idrac_connection_diagnostics_mock, f_module)
        msg, job_status, file_path = export_diagnostics_obj.execute()
        assert msg == SUCCESS_EXPORT_MSG
        assert job_status == {}
        assert file_path == 'None/None'

        # Scenario 2: share_type = nfs
        job = {"JobState": "Completed"}
        export_params = {'share_parameters': {'share_type': "nfs"}}
        mocker.patch(MODULE_PATH + "ExportDiagnostics._ExportDiagnostics__export_diagnostics_nfs", return_value=obj)
        mocker.patch(MODULE_PATH + "ExportDiagnostics.get_job_status", return_value=job)
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        export_diagnostics_obj = self.module.ExportDiagnostics(idrac_connection_diagnostics_mock, f_module)
        msg, job_status, file_path = export_diagnostics_obj.execute()
        assert msg == SUCCESS_EXPORT_MSG
        assert job_status == job
        assert file_path == 'None/None'

        # Scenario 3: Check mode
        obj.status = 400
        mocker.patch(MODULE_PATH + "ExportDiagnostics.perform_check_mode", return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        export_diagnostics_obj = self.module.ExportDiagnostics(idrac_connection_diagnostics_mock, f_module)
        export_diagnostics_obj.execute()

    def test_export_diagnostics_local(self, idrac_default_args, idrac_connection_diagnostics_mock, mocker):
        export_params = {
            'share_parameters': {
                'share_name': SHARE_NAME,
                'file_name': DIAGS_FILE_NAME
            }
        }
        obj = MagicMock()
        obj.status = 200
        obj.headers = {'Location': REDFISH_BASE_API}
        obj.filename = DIAGS_FILE_NAME
        mocker.patch(MODULE_PATH + 'ExportDiagnostics._ExportDiagnostics__export_diagnostics', return_value=obj)
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        export_diagnostics_obj = self.module.ExportDiagnostics(idrac_connection_diagnostics_mock, f_module)
        with pytest.raises(Exception):
            export_diagnostics_obj._ExportDiagnostics__export_diagnostics_local()

    def test_export_diagnostics_http(self, idrac_default_args, idrac_connection_diagnostics_mock, mocker):
        obj = MagicMock()
        obj.status_code = 200
        mocker.patch(MODULE_PATH + PAYLOAD_FUNC, return_value=None)
        mocker.patch(MODULE_PATH + EXPORT_FUNC, return_value=obj)
        # Scenario 1: With ipv4
        export_params = {
            'share_parameters': {
                'ip_address': IP,
                'file_name': 'test_diags',
                'share_type': 'http',
                'share_name': 'myshare'
            }
        }
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        export_diagnostics_obj = self.module.ExportDiagnostics(idrac_connection_diagnostics_mock, f_module)
        result = export_diagnostics_obj._ExportDiagnostics__export_diagnostics_http()
        assert result == obj

        # Scenario 2: With ipv6
        export_params = {
            'share_parameters': {
                'ip_address': 'XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX',
                'file_name': 'test_diags',
                'share_type': 'http',
                'share_name': 'myshare'
            }
        }
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        export_diagnostics_obj = self.module.ExportDiagnostics(idrac_connection_diagnostics_mock, f_module)
        result = export_diagnostics_obj._ExportDiagnostics__export_diagnostics_http()
        assert result == obj

    def test_export_diagnostics_cifs(self, idrac_default_args, idrac_connection_diagnostics_mock, mocker):
        obj = MagicMock()
        obj.status_code = 200
        mocker.patch(MODULE_PATH + PAYLOAD_FUNC, return_value={})
        mocker.patch(MODULE_PATH + EXPORT_FUNC, return_value=obj)
        # Scenario 1: With workgroup
        export_params = {
            'share_parameters': {
                'file_name': 'test_diags',
                'share_type': 'cifs',
                'share_name': 'myshare',
                'ignore_certificate_warning': 'off',
                'workgroup': 'myworkgroup'
            }
        }
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        export_diagnostics_obj = self.module.ExportDiagnostics(idrac_connection_diagnostics_mock, f_module)
        result = export_diagnostics_obj._ExportDiagnostics__export_diagnostics_cifs()
        assert result == obj

        # Scenario 2: Without workgroup
        export_params = {
            'share_parameters': {
                'file_name': 'test_diags',
                'share_type': 'cifs',
                'share_name': 'myshare',
                'ignore_certificate_warning': 'off'
            }
        }
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        export_diagnostics_obj = self.module.ExportDiagnostics(idrac_connection_diagnostics_mock, f_module)
        result = export_diagnostics_obj._ExportDiagnostics__export_diagnostics_cifs()
        assert result == obj

    def test_export_diagnostics_nfs(self, idrac_default_args, idrac_connection_diagnostics_mock, mocker):
        obj = MagicMock()
        obj.status_code = 200
        mocker.patch(MODULE_PATH + PAYLOAD_FUNC, return_value={"UserName": "user", "Password": "password"})
        mocker.patch(MODULE_PATH + EXPORT_FUNC, return_value=obj)
        export_params = {
            'share_parameters': {
                'share_name': 'share',
                'share_type': 'nfs',
                'ignore_certificate_warning': 'off'
            }
        }
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        export_diagnostics_obj = self.module.ExportDiagnostics(idrac_connection_diagnostics_mock, f_module)
        result = export_diagnostics_obj._ExportDiagnostics__export_diagnostics_nfs()
        assert result == obj

    def test_get_export_diagnostics_url(self, idrac_default_args, idrac_connection_diagnostics_mock, mocker):
        export_params = {
            'share_parameters': {
                'file_name': DIAGS_FILE_NAME,
                'share_type': 'local',
                'ignore_certificate_warning': 'off'
            }
        }
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        # Scenario 1: With url
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value={"Links": {"Oem": {"Dell": {"DellLCService": {ODATA: DIAGS_ODATA}}}},
                                   "Actions": {"#DellLCService.ExportePSADiagnosticsResult": {"target": API_ONE}}})
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        export_diagnostics_obj = self.module.ExportDiagnostics(idrac_connection_diagnostics_mock, f_module)
        export_diagnostics_obj._ExportDiagnostics__get_export_diagnostics_url()
        assert export_diagnostics_obj.export_url == API_ONE

        # Scenario 2: When url is empty
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value={"Links": {}})
        with pytest.raises(Exception) as exc:
            export_diagnostics_obj._ExportDiagnostics__get_export_diagnostics_url()
        assert exc.value.args[0] == UNSUPPORTED_FIRMWARE_MSG

        # Scenario 3: For error message
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, "error"))
        with pytest.raises(Exception) as exc:
            export_diagnostics_obj._ExportDiagnostics__get_export_diagnostics_url()
        assert exc.value.args[0] == "error"

    def test_export_diagnostics(self, idrac_default_args, idrac_connection_diagnostics_mock, mocker):
        obj = MagicMock()
        obj.status_code = 200
        payload = mocker.patch(MODULE_PATH + PAYLOAD_FUNC, return_value={})
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        mocker.patch(MODULE_PATH + "ExportDiagnostics._ExportDiagnostics__get_export_diagnostics_url", return_value=API_ONE)
        # Scenario 1: With file name
        export_params = {
            'share_parameters': {
                'file_name': DIAGS_FILE_NAME
            }
        }
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        export_diagnostics_obj = self.module.ExportDiagnostics(idrac_connection_diagnostics_mock, f_module)
        result = export_diagnostics_obj._ExportDiagnostics__export_diagnostics(payload)
        assert result == obj

        # Scenario 2: Without file name
        export_params = {
            'idrac_ip': IP,
            'share_parameters': {
                'file_name': ''
            }
        }
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        export_diagnostics_obj = self.module.ExportDiagnostics(idrac_connection_diagnostics_mock, f_module)
        result = export_diagnostics_obj._ExportDiagnostics__export_diagnostics(payload)
        assert result == obj

    def test_get_job_status_success(self, mocker, idrac_diagnostics_mock):
        obj = self.get_module_mock()
        diagnostics_job_response_mock = mocker.MagicMock()
        diagnostics_job_response_mock.headers.get.return_value = "HTTPS_PATH/job_tracking/12345"
        mocker.patch(MODULE_PATH + "remove_key", return_value={"job_details": "mocked_job_details"})
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri", return_value=[MANAGER_URI_ONE])
        obj_under_test = self.module.ExportDiagnostics(idrac_diagnostics_mock, obj)
        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking", return_value=(False, "mocked_message", {"job_details": "mocked_job_details"}, 0))
        result = obj_under_test.get_job_status(diagnostics_job_response_mock)
        assert result == {"job_details": "mocked_job_details"}

    def test_get_job_status_failure(self, mocker, idrac_diagnostics_mock):
        obj = self.get_module_mock()
        diagnostics_job_response_mock = mocker.MagicMock()
        diagnostics_job_response_mock.headers.get.return_value = "HTTPS_PATH/job_tracking/12345"
        mocker.patch(MODULE_PATH + "remove_key", return_value={"Message": "None"})
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri", return_value=[MANAGER_URI_ONE])
        obj_under_test = self.module.ExportDiagnostics(idrac_diagnostics_mock, obj)
        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking", return_value=(True, "None", {"Message": "None"}, 0))
        exit_json_mock = mocker.patch.object(obj, "exit_json")
        result = obj_under_test.get_job_status(diagnostics_job_response_mock)
        exit_json_mock.assert_called_once_with(msg="None", failed=True, job_details={"Message": "None"})
        assert result == {"Message": "None"}

    def test_perform_check_mode(self, idrac_default_args, idrac_connection_diagnostics_mock, mocker):
        obj = MagicMock()
        # Scenario 1: With status code 200
        obj.status_code = 200
        idrac_default_args.update({'ShareType': 'Local'})
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        export_diagnostics_obj = self.module.ExportDiagnostics(idrac_connection_diagnostics_mock, f_module)
        with pytest.raises(Exception) as exc:
            export_diagnostics_obj.perform_check_mode()
        assert exc.value.args[0] == CHANGES_FOUND_MSG

        # Scenario 2: With status code 400
        obj.status_code = 400
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        export_diagnostics_obj = self.module.ExportDiagnostics(idrac_connection_diagnostics_mock, f_module)
        val = export_diagnostics_obj.perform_check_mode()
        assert val is None

        # Scenario 3: HTTP Error with message id SYS099
        json_str = to_text(json.dumps({"error": {MESSAGE_EXTENDED: [
            {
                'MessageId': "SYS099",
                "Message": NO_FILE
            }
        ]}}))
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     side_effect=HTTPError(HTTPS_PATH, 400,
                                           HTTP_ERROR,
                                           {"accept-type": APPLICATION_JSON},
                                           StringIO(json_str)))
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        export_diagnostics_obj = self.module.ExportDiagnostics(idrac_connection_diagnostics_mock, f_module)
        with pytest.raises(Exception) as exc:
            export_diagnostics_obj.perform_check_mode()
        assert exc.value.args[0] == NO_FILE

        # Scenario 4: HTTP Error without message id
        json_str = to_text(json.dumps({"error": {MESSAGE_EXTENDED: [
            {
                'MessageId': "123",
                "Message": "error"
            }
        ]}}))
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     side_effect=HTTPError(HTTPS_PATH, 400,
                                           HTTP_ERROR,
                                           {"accept-type": APPLICATION_JSON},
                                           StringIO(json_str)))
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        export_diagnostics_obj = self.module.ExportDiagnostics(idrac_connection_diagnostics_mock, f_module)
        val = export_diagnostics_obj.perform_check_mode()
        assert val is None


class TestRunAndExportDiagnostics(FakeAnsibleModule):
    module = idrac_diagnostics

    @pytest.fixture
    def idrac_diagnostics_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_diagnostics_mock(self, mocker, idrac_diagnostics_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_diagnostics_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_diagnostics_mock
        return idrac_conn_mock

    def test_execute(self, idrac_default_args, idrac_connection_diagnostics_mock, mocker):
        obj = MagicMock()
        obj.status_code = 200

        def export_execute():
            msg = SUCCESS_EXPORT_MSG
            job_status = "None"
            file_path = SHARE_NAME
            return msg, job_status, file_path

        # Scenario 1: When job wait is true
        idrac_default_args.update({'job_wait': True})
        mocker.patch(MODULE_PATH + "RunDiagnostics", return_value=obj)
        obj.execute = export_execute
        mocker.patch(MODULE_PATH + "ExportDiagnostics", return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_and_export_obj = self.module.RunAndExportDiagnostics(idrac_connection_diagnostics_mock, f_module)
        msg, job_status, file_path = run_and_export_obj.execute()
        assert msg == SUCCESS_RUN_AND_EXPORT_MSG

        # Scenario 2: When job wait is false
        def run_execute():
            msg = RUNNING_RUN_MSG
            job_status = "None"
            file_path = "None"
            return msg, job_status, file_path

        idrac_default_args.update({'job_wait': False})
        obj.execute = run_execute
        mocker.patch(MODULE_PATH + "RunDiagnostics", return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        run_obj = self.module.RunAndExportDiagnostics(idrac_connection_diagnostics_mock, f_module)
        msg, job_status, file_path = run_obj.execute()
        assert msg == RUNNING_RUN_MSG


class TestDiagnosticsType(FakeAnsibleModule):
    module = idrac_diagnostics

    @pytest.fixture
    def idrac_diagnostics_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_diagnostics_mock(self, mocker, idrac_diagnostics_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_diagnostics_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_diagnostics_mock
        return idrac_conn_mock

    def test_diagnostics_operation(self, idrac_default_args, idrac_connection_diagnostics_mock):
        idrac_default_args.update({"run": True, "export": False})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        diags_class = self.module.DiagnosticsType.diagnostics_operation(idrac_connection_diagnostics_mock, f_module)
        assert isinstance(diags_class, self.module.RunDiagnostics)

        idrac_default_args.update({"run": False, "export": True})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        diags_class = self.module.DiagnosticsType.diagnostics_operation(idrac_connection_diagnostics_mock, f_module)
        assert isinstance(diags_class, self.module.ExportDiagnostics)

        idrac_default_args.update({"run": True, "export": True})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        diags_class = self.module.DiagnosticsType.diagnostics_operation(idrac_connection_diagnostics_mock, f_module)
        assert isinstance(diags_class, self.module.RunAndExportDiagnostics)

        idrac_default_args.update({"run": False, "export": False})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        with pytest.raises(Exception) as exc:
            self.module.DiagnosticsType.diagnostics_operation(idrac_connection_diagnostics_mock, f_module)
        assert exc.value.args[0] == NO_OPERATION_SKIP_MSG

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_idrac_diagnostics_main_exception_handling_case(self, exc_type, mocker, idrac_default_args):
        idrac_default_args.update({"run": True})
        # Scenario 1: HTTPError with message id SYS099
        json_str = to_text(json.dumps({"error": {MESSAGE_EXTENDED: [
            {
                'MessageId': "SYS099",
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

        # Scenario 2: HTTPError with message id SYS098
        json_str = to_text(json.dumps({"error": {MESSAGE_EXTENDED: [
            {
                'MessageId': "SYS098",
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
        diagnostics_mock = mocker.MagicMock()
        diagnostics_mock.execute.return_value = (None, None, None)
        mocker.patch(MODULE_PATH + 'get_argument_spec', return_value={})
        mocker.patch(MODULE_PATH + 'IdracAnsibleModule', return_value=module_mock)
        mocker.patch(MODULE_PATH + 'iDRACRedfishAPI', return_value=idrac_mock)
        mocker.patch(MODULE_PATH + 'DiagnosticsType.diagnostics_operation', return_value=diagnostics_mock)
        main()
        diagnostics_mock.execute.return_value = (None, None, SHARE_NAME)
        mocker.patch(MODULE_PATH + 'DiagnosticsType.diagnostics_operation', return_value=diagnostics_mock)
        main()
