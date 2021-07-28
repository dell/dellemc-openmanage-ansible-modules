# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.6.0
# Copyright (C) 2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
import pytest
from ssl import SSLError
from io import StringIO
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils._text import to_text
from ansible_collections.dellemc.openmanage.plugins.modules import ome_diagnostics
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_diagnostics.'


@pytest.fixture
def ome_conn_mock_diagnostics(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOMEDiagnostics(FakeAnsibleModule):

    module = ome_diagnostics

    def test_check_domain_service(self, ome_conn_mock_diagnostics, ome_default_args, mocker):
        f_module = self.get_module_mock()
        result = self.module.check_domain_service(f_module, ome_conn_mock_diagnostics)
        assert result is None

    def test_group_validation(self, ome_conn_mock_diagnostics, ome_response_mock, ome_default_args, mocker):
        f_module = self.get_module_mock(params={"device_group_name": "Servers"})
        ome_response_mock.json_data = {"value": []}
        with pytest.raises(Exception) as err:
            self.module.group_validation(f_module, ome_conn_mock_diagnostics)
        assert err.value.args[0] == "Unable to complete the operation because the entered target device " \
                                    "group name 'Servers' is invalid."
        ome_response_mock.json_data = {"value": [{"Id": 25011, "Type": 1000}]}
        result = self.module.group_validation(f_module, ome_conn_mock_diagnostics)
        assert result == [25011]

    def test_device_validation(self, ome_conn_mock_diagnostics, ome_response_mock, ome_default_args, mocker):
        resp = {"report_list": [{"Id": 25014, "DeviceServiceTag": "ZXCVB1", "Type": 1000}]}
        f_module = self.get_module_mock(params={"device_ids": [25011]})
        ome_conn_mock_diagnostics.get_all_report_details.return_value = resp
        with pytest.raises(Exception) as err:
            self.module.device_validation(f_module, ome_conn_mock_diagnostics)
        assert err.value.args[0] == "Unable to complete the operation because the entered target device " \
                                    "id(s) '25011' are invalid."
        resp = {"report_list": [{"Id": 25011, "DeviceServiceTag": "ZXCVB1", "Type": 1000}]}
        ome_conn_mock_diagnostics.get_all_report_details.return_value = resp
        result = self.module.device_validation(f_module, ome_conn_mock_diagnostics)
        assert result == [25011]
        f_module = self.get_module_mock(params={"device_service_tags": ["ZXCVB1"]})
        result = self.module.device_validation(f_module, ome_conn_mock_diagnostics)
        assert result == [25011]
        resp = {"report_list": [{"Id": 25019, "DeviceServiceTag": "ZXCVB1", "Type": 8000}]}
        ome_conn_mock_diagnostics.get_all_report_details.return_value = resp
        with pytest.raises(Exception) as err:
            self.module.device_validation(f_module, ome_conn_mock_diagnostics)
        assert err.value.args[0] == "The requested device service tag(s) 'ZXCVB1' " \
                                    "are not applicable for export log."

    def test_extract_log_operation(self, ome_conn_mock_diagnostics, ome_response_mock, ome_default_args, mocker):
        f_module = self.get_module_mock(params={"log_type": "application", "share_address": "192.168.0.1",
                                                "share_type": "NFS", "share_name": "iso", "share_user": "username",
                                                "share_password": "password", "share_domain": "domain",
                                                "mask_sensitive_info": "true", "log_selectors": ["OS_LOGS"]})
        ome_response_mock.json_data = {"value": [{"Id": 16011, "Type": 2000}]}
        ome_conn_mock_diagnostics.job_submission.return_value = {"Id": 16011}
        result = self.module.extract_log_operation(f_module, ome_conn_mock_diagnostics)
        assert result["Id"] == 16011

        f_module = self.get_module_mock(params={"log_type": "support_assist_collection", "share_address": "192.168.0.1",
                                                "share_type": "NFS", "share_name": "iso", "share_user": "username",
                                                "share_password": "password", "share_domain": "domain",
                                                "mask_sensitive_info": "true", "log_selectors": ["OS_LOGS"]})
        result = self.module.extract_log_operation(f_module, ome_conn_mock_diagnostics, device_lst=[25012])
        assert result["Id"] == 16011

    def test_main_succes_case(self, ome_conn_mock_diagnostics, ome_response_mock, ome_default_args, mocker):
        ome_default_args.update({"log_type": "support_assist_collection", "share_address": "192.168.0.1",
                                 "share_type": "NFS", "share_name": "iso", "share_user": "username",
                                 "share_password": "password", "share_domain": "domain",
                                 "mask_sensitive_info": "true", "log_selectors": ["OS_LOGS"],
                                 "test_connection": False, "job_wait": True, "device_ids": [25011]})
        mocker.patch(MODULE_PATH + "check_domain_service", return_value=None)
        mocker.patch(MODULE_PATH + "device_validation", return_value=[25011])
        mocker.patch(MODULE_PATH + "find_failed_jobs", return_value=("", False))
        ome_conn_mock_diagnostics.check_existing_job_state.return_value = (True, [25011])
        mocker.patch(MODULE_PATH + "extract_log_operation")
        ome_response_mock.json_data = {"value": {"Id": 25011}}
        ome_conn_mock_diagnostics.job_tracking.return_value = (False, "")
        result = self._run_module(ome_default_args)
        assert result["msg"] == "Export log job completed successfully."

        ome_conn_mock_diagnostics.check_existing_job_state.return_value = (False, [25011])
        result = self._run_module_with_fail_json(ome_default_args)
        assert result["msg"] == "An export log job is already running. Wait for the job to finish."

        ome_default_args.update({"test_connection": True, "job_wait": False})
        ome_conn_mock_diagnostics.check_existing_job_state.return_value = (True, [25011])
        ome_conn_mock_diagnostics.job_tracking.return_value = (True, "")
        result = self._run_module_with_fail_json(ome_default_args)
        assert result["msg"] == "Unable to access the share. Ensure that the share address, share name, " \
                                "share domain, and share credentials provided are correct."

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_diagnostics_main_exception_case(self, exc_type, mocker, ome_default_args,
                                                 ome_conn_mock_diagnostics, ome_response_mock):
        ome_default_args.update({"log_type": "application", "share_address": "192.168.0.1",
                                 "share_type": "NFS", "mask_sensitive_info": False})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'check_domain_service', side_effect=exc_type("url open error"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result["failed"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'check_domain_service', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'check_domain_service',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result

    def test_find_failed_jobs(self, ome_conn_mock_diagnostics, ome_response_mock, ome_default_args, mocker):
        ome_response_mock.json_data = {
            "Id": 25011,
            "value": [{"Id": 25013, "Value": "Job status for JID_255809594125 is Completed with Errors."}]
        }
        result = self.module.find_failed_jobs({"Id": 25012}, ome_conn_mock_diagnostics)
        assert result[0] == "Export log job completed with errors."
        assert result[1] is False
