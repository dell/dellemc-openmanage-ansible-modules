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
from unittest.mock import MagicMock
from ansible_collections.dellemc.openmanage.plugins.modules.idrac_support_assist import main

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_support_assist.'
MODULE_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.'

SUCCESS_EXPORT_MSG = "Successfully exported the support assist collections."
SUCCESS_RUN_MSG = "Successfully ran the support assist collections."
SUCCESS_RUN_AND_EXPORT_MSG = "Successfully ran and exported the support assist collections."
RUNNING_RUN_MSG = "Successfully triggered the job to run support assist collections."
RUNNING_RUN_AND_EXPORT_MSG = "Successfully triggered the job to run and export support assist collections."
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
OPERATION_NOT_ALLOWED_MSG = "Export to local is only supported when both run and export is set to true."
PROXY_SERVER = "proxy.example.com"
PAYLOAD_FUNC = "SupportAssist.get_payload_details"
EULA_STATUS_FUNC = "AcceptEULA.eula_status"
EULA_STATUS_URL = "AcceptEULA._AcceptEULA__get_eula_status_url"
VALIDATE_TIME_FUNC = "RunSupportAssist._RunSupportAssist__validate_time"
EXPORT_FUNC = "ExportSupportAssist._ExportSupportAssist__export_support_assist"
JOB_WAIT_FUNC = "RunSupportAssist._RunSupportAssist__perform_job_wait"
NETWORK_SHARE_URL = "SupportAssist.get_test_network_share_url"
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
        support_assist_obj = self.module.SupportAssist(
            idrac_connection_support_assist_mock, obj)
        support_assist_obj.execute()

    def test_get_payload_details(self, idrac_connection_support_assist_mock):
        obj = MagicMock()
        diags_obj = self.module.SupportAssist(
            idrac_connection_support_assist_mock, obj)
        # Scenario 1: With all values
        obj.params.get.return_value = {
            'ip_address': IP,
            'share_name': 'my_share',
            'username': 'my_user',
            'password': 'my_password',
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
            'share_type': 'http',
            'ignore_certificate_warning': 'on'
        }
        result = diags_obj.get_payload_details()
        expected_result = {
            'IPAddress': IP,
            'ShareName': 'my_share',
            'UserName': 'my_user',
            'Password': 'my_password',
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
            'ShareType': 'HTTP',
            'IgnoreCertWarning': 'On',
            'ProxySupport': 'ParametersProxy',
            'ProxyType': 'SOCKS',
            'ProxyServer': PROXY_SERVER,
            'ProxyPort': '8080'
        }
        assert result == expected_result

    def test_network_share(self, idrac_connection_support_assist_mock, idrac_default_args, mocker):
        # Scenario 1: ShareType is LOCAL and directory is invalid
        payload = {"ShareType": "LOCAL", "ShareName": "my_share"}
        mocker.patch(MODULE_PATH + PAYLOAD_FUNC, return_value=payload)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        support_assist_obj = self.module.SupportAssist(
            idrac_connection_support_assist_mock, f_module)
        with pytest.raises(Exception) as exc:
            support_assist_obj.test_network_share()
        assert exc.value.args[0] == INVALID_DIRECTORY_MSG.format(
            path="my_share")

        # Scenario 2: ShareType is LOCAL and directory is not writable
        payload = {"ShareType": "LOCAL", "ShareName": SHARE_NAME}
        mocker.patch(MODULE_PATH + PAYLOAD_FUNC, return_value=payload)
        mocker.patch(
            MODULE_PATH + NETWORK_SHARE_URL, return_value=API_ONE)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        support_assist_obj = self.module.SupportAssist(
            idrac_connection_support_assist_mock, f_module)
        ob = support_assist_obj.test_network_share()
        assert ob is None

        # Scenario 3: ShareType is not LOCAL
        obj = MagicMock()
        payload = {"ShareType": "HTTP", "ShareName": "my_share"}
        mocker.patch(MODULE_PATH + PAYLOAD_FUNC, return_value=payload)
        mocker.patch(
            MODULE_PATH + NETWORK_SHARE_URL, return_value=API_ONE)
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        support_assist_obj = self.module.SupportAssist(
            idrac_connection_support_assist_mock, f_module)
        support_assist_obj.test_network_share()

        # Scenario 4: HTTP Error
        payload = {"ShareType": "HTTP", "ShareName": "my_share"}
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
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        support_assist_obj = self.module.SupportAssist(
            idrac_connection_support_assist_mock, f_module)
        with pytest.raises(Exception) as exc:
            support_assist_obj.test_network_share()
        assert exc.value.args[0] == 'Error'

    def test_get_test_network_share_url(self, idrac_connection_support_assist_mock, idrac_default_args, mocker):
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value={"Links": {"Oem": {"Dell": {"DellLCService": {ODATA: ASSIST_ODATA}}}},
                                   "Actions": {"#DellLCService.TestNetworkShare": {"target": API_ONE}}})

        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        obj = self.module.SupportAssist(
            idrac_connection_support_assist_mock, f_module)
        resp = obj.get_test_network_share_url()
        assert resp == API_ONE

        # Scenario 2: for error message
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, "Error"))
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        obj = self.module.SupportAssist(
            idrac_connection_support_assist_mock, f_module)
        with pytest.raises(Exception) as exc:
            obj.get_test_network_share_url()
        assert exc.value.args[0] == "Error"


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
        mocker.patch(
            MODULE_PATH + EULA_STATUS_URL, return_value=None)
        mocker.patch(
            MODULE_PATH + "AcceptEULA._AcceptEULA__get_eula_accept_url", return_value=None)
        mocker.patch(MODULE_PATH + EULA_STATUS_FUNC, return_value=obj)
        idrac_default_args.update(
            {'run': True, 'accept_eula': True, 'export': False})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        support_assist_obj = self.module.AcceptEULA(
            idrac_connection_support_assist_mock, f_module)
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
        mocker.patch(
            MODULE_PATH + EULA_STATUS_URL, return_value=None)
        mocker.patch(MODULE_PATH + EULA_STATUS_FUNC, return_value=obj)
        mocker.patch(MODULE_PATH + "AcceptEULA.accept_eula", return_value=obj2)
        idrac_default_args.update(
            {'run': False, 'accept_eula': True, 'export': False})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        support_assist_obj = self.module.AcceptEULA(
            idrac_connection_support_assist_mock, f_module)
        msg = support_assist_obj.execute()
        assert msg == EULA_ACCEPTED_MSG

    def test_get_eula_status_url(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        # Scenario 1: With url
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value={"Links": {"Oem": {"Dell": {"DellLCService": {ODATA: ASSIST_ODATA}}}},
                                   "Actions": {"#DellLCService.SupportAssistGetEULAStatus": {"target": API_ONE}}})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        eula_status_support_assist_obj = self.module.AcceptEULA(
            idrac_connection_support_assist_mock, f_module)
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
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        eula_accept_obj = self.module.AcceptEULA(
            idrac_connection_support_assist_mock, f_module)
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
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        eula_status_obj = self.module.AcceptEULA(
            idrac_connection_support_assist_mock, f_module)
        status = eula_status_obj.eula_status()
        assert status

    def test_accept_eula(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        obj = MagicMock()
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        eula_accept_obj = self.module.AcceptEULA(
            idrac_connection_support_assist_mock, f_module)
        status = eula_accept_obj.accept_eula()
        assert status

    def test_perform_check_mode(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        obj = MagicMock()
        obj.status_code = 200
        mocker.patch(MODULE_PATH + EULA_STATUS_FUNC, return_value=obj)
        idrac_default_args.update({"accept_eula": True})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        cm_obj = self.module.AcceptEULA(
            idrac_connection_support_assist_mock, f_module)
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
        assert exc.value.args[0] == CHANGES_FOUND_MSG

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
        assert exc.value.args[0] == CHANGES_NOT_FOUND_MSG


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
        idrac_default_args.update(
            {'data_collector': ['gpu_logs'], 'export': False})
        mocker.patch(
            MODULE_PATH + "RunSupportAssist._RunSupportAssist__get_run_support_assist_url", return_value=None)
        mocker.patch(
            MODULE_PATH + "RunSupportAssist.check_support_assist_jobs", return_value=None)
        mocker.patch(
            MODULE_PATH + "RunSupportAssist._RunSupportAssist__run_support_assist", return_value=obj)
        mocker.patch(
            MODULE_PATH + "RunSupportAssist._RunSupportAssist__validate_job_timeout", return_value=None)
        mocker.patch(
            MODULE_PATH + JOB_WAIT_FUNC, return_value=job)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        msg, job_status = run_support_assist_obj.execute()
        assert msg == SUCCESS_RUN_MSG
        assert job_status == job

        # Scenario 2: JobState is scheduled
        job = {"JobState": "Scheduled"}
        idrac_default_args.update(
            {'data_collector': ['gpu_logs'], 'export': False})
        mocker.patch(
            MODULE_PATH + JOB_WAIT_FUNC, return_value=job)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        msg, job_status = run_support_assist_obj.execute()
        assert msg == RUNNING_RUN_MSG
        assert job_status == job

        # Scenario 3: JobState is scheduled and run and export both are true
        job = {"JobState": "Scheduled"}
        idrac_default_args.update(
            {'data_collector': ['gpu_logs'], 'run': True, 'export': True, 'share_parameters':
             {'share_type': 'nfs', 'share_name': 'share', 'ip_address': IP, 'ignore_certificate_warning': 'yes'}})
        mocker.patch(
            MODULE_PATH + NETWORK_SHARE_URL, return_value=API_ONE)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        msg, job_status = run_support_assist_obj.execute()
        assert msg == RUNNING_RUN_AND_EXPORT_MSG
        assert job_status == job

        # Scenario 4: JobState is scheduled and run and export both are true
        job = {"JobState": "Completed"}
        mocker.patch(
            MODULE_PATH + JOB_WAIT_FUNC, return_value=job)
        idrac_default_args.update(
            {'data_collector': ['gpu_logs'], 'run': True, 'export': True, 'share_parameters':
             {'share_type': 'nfs', 'share_name': 'share', 'ip_address': IP, 'ignore_certificate_warning': 'yes'}})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        msg, job_status = run_support_assist_obj.execute()
        assert msg == SUCCESS_RUN_AND_EXPORT_MSG
        assert job_status == job

    def test_run_support_assist(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        obj = MagicMock()
        obj.status_code = 200
        mocker.patch(
            MODULE_PATH + "RunSupportAssist._RunSupportAssist__get_run_support_assist_url", return_value=API_ONE)
        mocker.patch(
            MODULE_PATH + "RunSupportAssist._RunSupportAssist__validate_input", return_value=None)
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)

        # Scenario 1: With data_collector as gpu_logs
        run_params = {
            'data_collector': ['gpu_logs']
        }
        idrac_default_args.update(run_params)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        status = run_support_assist_obj._RunSupportAssist__run_support_assist()
        assert status == obj

        # Scenario 2: With data_collector as gpu_logs and filter_data as true
        run_params = {
            'data_collector': ['gpu_logs'],
            'filter_data': True
        }
        idrac_default_args.update(run_params)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        status = run_support_assist_obj._RunSupportAssist__run_support_assist()
        assert status == obj

        # Scenario 3: With all the data_collector and filter_data as true
        run_params = {
            'data_collector': ['storage_logs', 'os_app_data', 'debug_logs', 'telemetry_reports', 'gpu_logs', 'tty_logs'],
            'filter_data': True
        }
        idrac_default_args.update(run_params)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        status = run_support_assist_obj._RunSupportAssist__run_support_assist()
        assert status == obj

        # Scenario 4: With run and export both as true
        run_params = {
            'data_collector': ['storage_logs'],
            'filter_data': True,
            'share_parameters': {'share_type': 'nfs', 'share_name': 'share', 'ip_address': IP, 'ignore_certificate_warning': 'off'},
            'run': True,
            'export': True
        }
        idrac_default_args.update(run_params)
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        export_support_assist_obj = self.module.ExportSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        export_support_assist_obj.execute()
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
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value={"Links": {"Oem": {"Dell": {"DellLCService": {ODATA: ASSIST_ODATA}}}}})
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        # Scenario 1: Valid input which is not in allowable values
        data_selected = ['GPULogs']
        with pytest.raises(Exception) as exc:
            run_support_assist_obj._RunSupportAssist__validate_input(
                data_selected, data_selector)
        assert exc.value.args[0] == ALLOWED_VALUES_MSG.format(
            ['storage_logs', 'os_app_data', 'debug_logs', 'telemetry_reports', 'tty_logs'])

        # Scenario 2: Valid input which is in allowable values
        data_selected = ['HWData']
        obj = run_support_assist_obj._RunSupportAssist__validate_input(
            data_selected, data_selector)
        assert obj is None

    def test_get_run_support_assist_url(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        # Scenario 1: With url
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value={"Links": {"Oem": {"Dell": {"DellLCService": {ODATA: ASSIST_ODATA}}}},
                                   "Actions": {"#DellLCService.SupportAssistCollection": {"target": API_ONE}}})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
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
        temp_list = {"Members": [
            {"Id": "JID_123", "JobType": "SACollectExportHealthData", "JobState": "New"}]}
        obj.json_data = temp_list
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     return_value=obj)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)

        # Scenario 1: Check mode with job id
        with pytest.raises(Exception) as exc:
            run_support_assist_obj.check_support_assist_jobs()
        assert exc.value.args[0] == ALREADY_RUN_MSG

        # Scenario 2: Check mode without job id
        temp_list = {"Members": [{"Id": "", "JobType": "Test", "JobState": "New"}]}
        obj.json_data = temp_list
        obj.status_code = 200
        mocker.patch(
            MODULE_PATH + EULA_STATUS_URL, return_value=None)
        mocker.patch(
            MODULE_PATH + "AcceptEULA._AcceptEULA__get_eula_accept_url", return_value=None)
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        obj2 = MagicMock()
        obj2.status_code = 200
        obj2.json_data = {
            MESSAGE_EXTENDED: [
                {
                    "Message": "The SupportAssist End User License Agreement (EULA) is not accepted.",
                    "MessageId": "IDRAC.2.8.SRV104",
                }
            ]
        }
        mocker.patch(MODULE_PATH + EULA_STATUS_FUNC, return_value=obj2)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        with pytest.raises(Exception) as exc:
            run_support_assist_obj.check_support_assist_jobs()
        assert exc.value.args[0] == CHANGES_NOT_FOUND_MSG

        # Scenario 3: Normal mode with job id
        temp_list = {"Members": [
            {"Id": "666", "JobType": "SACollectExportHealthData", "JobState": "New"}]}
        obj.json_data = temp_list
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     return_value=obj)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        with pytest.raises(Exception) as exc:
            run_support_assist_obj.check_support_assist_jobs()
        assert exc.value.args[0] == ALREADY_RUN_MSG

        # Scenario 4: Normal mode without job id
        temp_list = {"Members": [
            {"Id": "", "JobType": "SACollectExportHealthData", "JobState": "New"}]}
        obj.json_data = temp_list
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     return_value=obj)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        resp = run_support_assist_obj.check_support_assist_jobs()
        assert resp is None

    def test_validate_job_timeout(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        # Scenario 1: Negative timeout
        idrac_default_args.update({'job_wait': True, 'job_wait_timeout': -120})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        with pytest.raises(Exception) as exc:
            run_support_assist_obj._RunSupportAssist__validate_job_timeout()
        assert exc.value.args[0] == TIMEOUT_NEGATIVE_OR_ZERO_MSG

        # Scenario 2: Valid timeout
        idrac_default_args.update({'job_wait': True, 'job_wait_timeout': 120})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
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
        mocker.patch(MODULE_PATH + "RunSupportAssist.file_download", return_value=None)
        idrac_default_args.update(
            {'job_wait': True, 'job_wait_timeout': 1200, 'share_parameters': {'share_type': 'nfs'}})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        job_dict = run_support_assist_obj._RunSupportAssist__perform_job_wait(
            obj)
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
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
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
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        with pytest.raises(Exception) as exc:
            run_support_assist_obj._RunSupportAssist__perform_job_wait(obj)
        assert exc.value.args[0] == 'Job Failed'

        # Scenario 4: When job_wait is False
        obj = MagicMock()
        obj.headers = {'Location': REDFISH_BASE_API}
        obj.json_data = {'JobState': 'Running'}
        idrac_default_args.update(
            {'job_wait': False, 'job_wait_timeout': 1200})
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking",
                     return_value=(True, 'msg', obj.json_data, 120))
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        mocker.patch(MODULE_PATH + "RunSupportAssist.file_download", return_value=None)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        job_dict = run_support_assist_obj._RunSupportAssist__perform_job_wait(
            obj)
        assert job_dict == obj.json_data

        # Scenario 5: When there's no job uri
        obj = MagicMock()
        obj.headers = {'Location': ''}
        idrac_default_args.update(
            {'job_wait': False, 'job_wait_timeout': 1200})
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        job_dict = run_support_assist_obj._RunSupportAssist__perform_job_wait(
            obj)
        assert job_dict == {}

    def test_file_download(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        obj = MagicMock()
        obj.headers = {'Location': REDFISH_BASE_API, 'Content-Type': 'application/x-tar'}
        obj.json_data = {'JobState': 'Completed'}
        obj.status_code = 200
        obj.body = b'Hello, world!'
        idrac_default_args.update(
            {'job_wait': True, 'share_parameters': {'share_name': tempfile.gettempdir()}})
        job_tracking_uri = REDFISH_BASE_API
        local_share = 'local'
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        job_dict = run_support_assist_obj.file_download(job_tracking_uri, local_share)
        assert job_dict is None

    def test_expand_ipv6(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        run_support_assist_obj = self.module.RunSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        ip = "XX:XX:XX:XX:XX:XX"
        expanded_ip = "00XX:00XX:00XX:00XX:00XX:00XX"
        expanded_ip_obj = run_support_assist_obj.expand_ipv6(ip)
        assert expanded_ip_obj == expanded_ip

        # Scenario 2: When ip is ipv6 with groups of zeros
        ip = "XXXX:XXXX::XXXX:XXXX"
        expanded_ip = "XXXX:XXXX:0000:0000:0000:0000:XXXX:XXXX"
        expanded_ip_obj = run_support_assist_obj.expand_ipv6(ip)
        assert expanded_ip_obj == expanded_ip


class TestExportSupportAssist(FakeAnsibleModule):
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
        obj.headers = {"Location": REDFISH}
        obj.status_code = 200
        mocker.patch(
            MODULE_PATH + "RunSupportAssist.check_support_assist_jobs", return_value=None)
        mocker.patch(
            MODULE_PATH + "SupportAssist.test_network_share", return_value=None)
        mocker.patch(
            MODULE_PATH + "ExportSupportAssist._ExportSupportAssist__get_export_support_assist_url", return_value=None)

        # Scenario 1: When share_type is local and run and export both are true
        payload = {
            "ShareType": "Local"
        }
        export_params = {'run': True, 'export': True,
                         'share_parameters': {'share_type': "local"}}
        idrac_default_args.update(export_params)
        mocker.patch(
            MODULE_PATH + "ExportSupportAssist._ExportSupportAssist__export_support_assist_local", return_value=payload)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        export_support_assist_obj = self.module.ExportSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        result = export_support_assist_obj.execute()
        assert result == payload

        # Scenario 2: When share_type is local and run is true but export is false
        payload = {
            "ShareType": "Local"
        }
        export_params = {'run': True, 'export': False,
                         'share_parameters': {'share_type': "local"}}
        idrac_default_args.update(export_params)
        mocker.patch(
            MODULE_PATH + "ExportSupportAssist._ExportSupportAssist__export_support_assist_local", return_value=payload)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        export_support_assist_obj = self.module.ExportSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        with pytest.raises(Exception) as exc:
            export_support_assist_obj.execute()
        assert exc.value.args[0] == OPERATION_NOT_ALLOWED_MSG

        # Scenario 3: When run and export both are true
        payload = {
            "ShareType": "NFS",
            "ShareName": SHARE_NAME,
            'IPAddress': IP
        }
        export_params = {'run': True, 'export': True, 'share_parameters': {
            'share_type': "nfs", 'share_name': SHARE_NAME, 'ip_address': IP}}
        idrac_default_args.update(export_params)
        mocker.patch(
            MODULE_PATH + "ExportSupportAssist._ExportSupportAssist__export_support_assist_nfs", return_value=payload)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        export_support_assist_obj = self.module.ExportSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        result = export_support_assist_obj.execute()
        assert result == payload

        # Scenario 4: When run is false but export is true
        job = {"JobState": "Completed"}
        export_params = {'run': False, 'export': True, 'share_parameters': {
            'share_type': "nfs", 'share_name': SHARE_NAME, 'ip_address': IP}}
        mocker.patch(
            MODULE_PATH + "ExportSupportAssist._ExportSupportAssist__export_support_assist_nfs", return_value=payload)
        mocker.patch(
            MODULE_PATH + "ExportSupportAssist._ExportSupportAssist__export_support_assist", return_value=obj)
        mocker.patch(
            MODULE_PATH + "ExportSupportAssist.get_job_status", return_value=job)
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        export_support_assist_obj = self.module.ExportSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        msg, job_status = export_support_assist_obj.execute()
        assert msg == SUCCESS_EXPORT_MSG
        assert job_status == job

    def test_export_support_assist_local(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        payload = {
            "ShareType": "Local",
        }
        export_params = {
            'share_parameters': {
                'share_type': 'local'
            }
        }
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        export_support_assist_obj = self.module.ExportSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        result = export_support_assist_obj._ExportSupportAssist__export_support_assist_local()
        assert result == payload

    def test_export_support_assist_http(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        payload = {
            "IPAddress": IP,
            "ShareType": "http",
            "ShareName": "share"
        }
        mocker.patch(MODULE_PATH + PAYLOAD_FUNC, return_value=payload)
        export_params = {
            'share_parameters': {
                'ip_address': IP,
                'share_type': 'http',
                'share_name': 'myshare'
            }
        }
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        export_support_assist_obj = self.module.ExportSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        result = export_support_assist_obj._ExportSupportAssist__export_support_assist_remote_shares()
        assert result == payload

    def test_export_support_assist_cifs(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        payload = {
            'share_parameters': {
                'share_type': 'cifs',
                'share_name': 'myshare',
                'ignore_certificate_warning': 'off',
                'workgroup': 'myworkgroup'
            }
        }
        mocker.patch(MODULE_PATH + PAYLOAD_FUNC, return_value=payload)
        # Scenario 1: Without workgroup
        payload = {
            'share_parameters': {
                'share_type': 'cifs',
                'share_name': 'myshare',
                'ignore_certificate_warning': 'off',
            }
        }
        export_params = {
            'share_parameters': {
                'share_type': 'cifs',
                'share_name': 'myshare',
                'ignore_certificate_warning': 'off'
            }
        }
        mocker.patch(MODULE_PATH + PAYLOAD_FUNC, return_value=payload)
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        export_support_assist_obj = self.module.ExportSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        result = export_support_assist_obj._ExportSupportAssist__export_support_assist_remote_shares()
        assert result == payload

    def test_export_support_assist_nfs(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        payload = {
            'share_name': 'share',
            'share_type': 'nfs',
            "UserName": "user",
            "Password": "password"
        }
        mocker.patch(MODULE_PATH + PAYLOAD_FUNC, return_value=payload)
        export_params = {
            'share_parameters': {
                'share_name': 'share',
                'share_type': 'nfs'
            }
        }
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        export_support_assist_obj = self.module.ExportSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        result = export_support_assist_obj._ExportSupportAssist__export_support_assist_nfs()
        assert result == export_params["share_parameters"]

    def test_get_export_support_assist_url(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        export_params = {
            'share_parameters': {
                'share_type': 'local',
                'ignore_certificate_warning': 'off'
            }
        }
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        # Scenario 1: With url
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value={"Links": {"Oem": {"Dell": {"DellLCService": {ODATA: ASSIST_ODATA}}}},
                                   "Actions": {"#DellLCService.SupportAssistExportLastCollection": {"target": API_ONE}}})
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        export_support_assist_obj = self.module.ExportSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        export_support_assist_obj._ExportSupportAssist__get_export_support_assist_url()
        assert export_support_assist_obj.export_url == API_ONE

        # Scenario 2: When url is empty
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value={"Links": {}})
        with pytest.raises(Exception) as exc:
            export_support_assist_obj._ExportSupportAssist__get_export_support_assist_url()
        assert exc.value.args[0] == UNSUPPORTED_FIRMWARE_MSG

        # Scenario 3: For error message
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, "error"))
        with pytest.raises(Exception) as exc:
            export_support_assist_obj._ExportSupportAssist__get_export_support_assist_url()
        assert exc.value.args[0] == "error"

    def test_export_support_assist(self, idrac_default_args, idrac_connection_support_assist_mock, mocker):
        obj = MagicMock()
        obj.status_code = 200
        payload = mocker.patch(MODULE_PATH + PAYLOAD_FUNC, return_value={})
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        mocker.patch(
            MODULE_PATH + "ExportSupportAssist._ExportSupportAssist__get_export_support_assist_url", return_value=API_ONE)
        # Scenario 1: When share_type is local and run is true
        export_params = {
            'share_parameters': {
                'share_type': 'local'
            }
        }
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        export_support_assist_obj = self.module.ExportSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        result = export_support_assist_obj._ExportSupportAssist__export_support_assist(
            payload)
        assert result == payload

        # Scenario 2: When share_type is not local
        export_params = {
            'share_parameters': {
                'ip_address': IP,
                'share_name': 'share',
                'share_type': 'nfs'
            }
        }
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        export_support_assist_obj = self.module.ExportSupportAssist(
            idrac_connection_support_assist_mock, f_module)
        result = export_support_assist_obj._ExportSupportAssist__export_support_assist(
            payload)
        assert result == obj

    def test_get_job_status_success(self, mocker, idrac_support_assist_mock):
        obj = self.get_module_mock()
        support_assist_job_response_mock = mocker.MagicMock()
        support_assist_job_response_mock.headers.get.return_value = "HTTPS_PATH/job_tracking/12345"
        mocker.patch(MODULE_PATH + "remove_key",
                     return_value={"job_details": "mocked_job_details"})
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=[MANAGER_URI_ONE])
        obj_under_test = self.module.ExportSupportAssist(
            idrac_support_assist_mock, obj)
        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking", return_value=(
            False, "mocked_message", {"job_details": "mocked_job_details"}, 0))
        result = obj_under_test.get_job_status(
            support_assist_job_response_mock)
        assert result == {"job_details": "mocked_job_details"}

    def test_get_job_status_failure(self, mocker, idrac_support_assist_mock):
        obj = self.get_module_mock()
        support_assist_job_response_mock = mocker.MagicMock()
        support_assist_job_response_mock.headers.get.return_value = "HTTPS_PATH/job_tracking/12345"
        mocker.patch(MODULE_PATH + "remove_key",
                     return_value={"Message": "None"})
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=[MANAGER_URI_ONE])
        obj_under_test = self.module.ExportSupportAssist(
            idrac_support_assist_mock, obj)
        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking",
                     return_value=(True, "None", {"Message": "None"}, 0))
        exit_json_mock = mocker.patch.object(obj, "exit_json")
        result = obj_under_test.get_job_status(
            support_assist_job_response_mock)
        exit_json_mock.assert_called_once_with(
            msg="None", failed=True, job_details={"Message": "None"})
        assert result == {"Message": "None"}


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
        # Scenario 1: When run is true and export is false
        idrac_default_args.update(
            {"run": True, "data_collector": ['gpu_logs'], "export": False})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        assist_class = self.module.SupportAssistType.support_assist_operation(
            idrac_connection_support_assist_mock, f_module)
        assert isinstance(assist_class, self.module.RunSupportAssist)

        # Scenario 2: When run is false and export is true
        idrac_default_args.update(
            {"export": True, "share_parameters": {"share_type": 'local', "share_name": "share"}, "run": False})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        assist_class = self.module.SupportAssistType.support_assist_operation(
            idrac_connection_support_assist_mock, f_module)
        assert isinstance(assist_class, self.module.ExportSupportAssist)

        # Scneario 3: when no operation is provided
        idrac_default_args.update(
            {"export": False, "accept_eula": False, "run": False})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        with pytest.raises(Exception) as exc:
            self.module.SupportAssistType.support_assist_operation(idrac_connection_support_assist_mock, f_module)
        assert exc.value.args[0] == NO_OPERATION_SKIP_MSG

    @pytest.mark.parametrize("exc",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_idrac_support_assist_main_exception_handling_case(self, exc, mocker, idrac_default_args):
        idrac_default_args.update(
            {"run": True, "data_collector": ['gpu_logs'], "export": False})
        # Scenario 1: HTTPError with message id SRV095
        error_string = to_text(json.dumps({"error": {MESSAGE_EXTENDED: [
            {
                'MessageId': "SRV095",
                "Message": HTTP_ERROR
            }
        ]}}))
        if exc in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + RUN_EXEC_FUNC,
                         side_effect=exc(HTTPS_PATH, 400,
                                         HTTP_ERROR,
                                         {"accept-type": APPLICATION_JSON},
                                         StringIO(error_string)))
        else:
            mocker.patch(MODULE_PATH + RUN_EXEC_FUNC,
                         side_effect=exc('test'))
        res_out = self._run_module(idrac_default_args)
        if exc == URLError:
            assert res_out['unreachable'] is True
        assert 'msg' in res_out

        # Scenario 2: HTTPError with message id SRV085
        error_string = to_text(json.dumps({"error": {MESSAGE_EXTENDED: [
            {
                'MessageId': "SRV085",
                "Message": HTTP_ERROR
            }
        ]}}))
        if exc in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + RUN_EXEC_FUNC,
                         side_effect=exc(HTTPS_PATH, 400,
                                         HTTP_ERROR,
                                         {"accept-type": APPLICATION_JSON},
                                         StringIO(error_string)))
        res_out = self._run_module(idrac_default_args)
        assert 'msg' in res_out

        # Scenario 3: HTTPError with message id LIC501
        error_string = to_text(json.dumps({"error": {MESSAGE_EXTENDED: [
            {
                'MessageId': "LIC501",
                "Message": HTTP_ERROR
            }
        ]}}))
        if exc in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + RUN_EXEC_FUNC,
                         side_effect=exc(HTTPS_PATH, 400,
                                         HTTP_ERROR,
                                         {"accept-type": APPLICATION_JSON},
                                         StringIO(error_string)))
        res_out = self._run_module(idrac_default_args)
        assert 'msg' in res_out

        # Scenario 4: HTTPError with message id SRV113
        error_string = to_text(json.dumps({"error": {MESSAGE_EXTENDED: [
            {
                'MessageId': "SRV113",
                "Message": HTTP_ERROR
            }
        ]}}))
        if exc in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + RUN_EXEC_FUNC,
                         side_effect=exc(HTTPS_PATH, 400,
                                         HTTP_ERROR,
                                         {"accept-type": APPLICATION_JSON},
                                         StringIO(error_string)))
        res_out = self._run_module(idrac_default_args)
        assert 'msg' in res_out

        # Scenario 5: HTTPError with random message id
        error_string = to_text(json.dumps({"error": {MESSAGE_EXTENDED: [
            {
                'MessageId': "123",
                "Message": HTTP_ERROR
            }
        ]}}))
        if exc in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + RUN_EXEC_FUNC,
                         side_effect=exc(HTTPS_PATH, 400,
                                         HTTP_ERROR,
                                         {"accept-type": APPLICATION_JSON},
                                         StringIO(error_string)))
        res_out = self._run_module(idrac_default_args)
        assert 'msg' in res_out

    def test_main(self, mocker):
        mock_module = mocker.MagicMock()
        mock_idrac = mocker.MagicMock()
        support_assist_mock = mocker.MagicMock()
        support_assist_mock.execute.return_value = (None, None)
        mocker.patch(MODULE_PATH + 'get_argument_spec', return_value={})
        mocker.patch(MODULE_PATH + 'IdracAnsibleModule',
                     return_value=mock_module)
        mocker.patch(MODULE_PATH + 'iDRACRedfishAPI', return_value=mock_idrac)
        mocker.patch(MODULE_PATH + 'SupportAssistType.support_assist_operation',
                     return_value=support_assist_mock)
        main()
        support_assist_mock.execute.return_value = (None, None)
        mocker.patch(MODULE_PATH + 'SupportAssistType.support_assist_operation',
                     return_value=support_assist_mock)
        main()
