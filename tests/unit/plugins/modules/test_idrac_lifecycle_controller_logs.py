# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.2
# Copyright (C) 2020-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_lifecycle_controller_logs
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from unittest.mock import MagicMock
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
EXPORT_LOGS = 'idrac_lifecycle_controller_logs.run_export_lc_logs'
server_generation_info = (13, "2.8", "iDRAC 8")


class TestExportLcLogs(FakeAnsibleModule):
    module = idrac_lifecycle_controller_logs

    @pytest.fixture
    def idrac_export_lc_logs_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.file_share_manager = idrac_obj
        omsdk_mock.log_mgr = idrac_obj
        return idrac_obj

    @pytest.fixture
    def idrac_lc_logs_mock(self, idrac_export_lc_logs_mock):
        return idrac_export_lc_logs_mock()

    @pytest.fixture
    def idrac_redfish_lc_logs_mock(self, idrac_export_lc_logs_mock):
        return idrac_export_lc_logs_mock()

    @pytest.fixture
    def idrac_redfish_connection_export_lc_logs_mock(self, mocker, idrac_redfish_lc_logs_mock):
        idrac_redfish_conn_class_mock = mocker.patch(
            MODULE_PATH + 'idrac_lifecycle_controller_logs.iDRACRedfishAPI',
            return_value=idrac_redfish_lc_logs_mock
        )
        idrac_redfish_conn_class_mock.return_value.__enter__.return_value = idrac_redfish_lc_logs_mock
        idrac_redfish_lc_logs_mock.get_server_generation.return_value = "iDRAC9"
        return idrac_redfish_lc_logs_mock

    @pytest.fixture
    def idrac_connection_export_lc_logs_mock(self, mocker, idrac_export_lc_logs_mock):
        idrac_conn_class_mock = mocker.patch(MODULE_PATH + 'idrac_lifecycle_controller_logs.iDRACConnection',
                                             return_value=idrac_export_lc_logs_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_export_lc_logs_mock
        return idrac_export_lc_logs_mock

    @pytest.fixture
    def idrac_file_manager_export_lc_logs_mock(self, mocker):
        try:
            lclog_file_name_format = "%ip_%Y%m%d_%H%M%S_LC_Log.log"
            file_manager_obj = mocker.patch(MODULE_PATH + 'idrac_lifecycle_controller_logs.file_share_manager')
        except AttributeError:
            file_manager_obj = MagicMock()
        obj = MagicMock()
        file_manager_obj.create_share_obj.return_value = obj
        file_manager_obj.myshare.new_file(lclog_file_name_format).return_value = obj
        return file_manager_obj

    def test_main_export_lc_logs_success_case(self, idrac_connection_export_lc_logs_mock, idrac_default_args, mocker,
                                              idrac_file_manager_export_lc_logs_mock, idrac_redfish_connection_export_lc_logs_mock):

        idrac_redfish_connection_export_lc_logs_mock.get_server_generation = server_generation_info
        idrac_default_args.update({"share_name": "sharename", "share_user": "shareuser",
                                   "share_password": "sharepassword", "job_wait": True})
        message = {"Status": "Success", "JobStatus": "Success"}
        mocker.patch(MODULE_PATH + EXPORT_LOGS, return_value=message)
        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Successfully exported the lifecycle controller logs."

        idrac_default_args.update({"job_wait": False})
        mocker.patch(MODULE_PATH + EXPORT_LOGS, return_value=message)
        result = self._run_module(idrac_default_args)
        assert result["msg"] == "The export lifecycle controller log job is submitted successfully."

        message = {"Status": "Failed", "JobStatus": "Failed"}
        mocker.patch(MODULE_PATH + EXPORT_LOGS, return_value=message)
        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Unable to export the lifecycle controller logs."
        assert result["failed"] is True

    @pytest.mark.parametrize("exc_type", [RuntimeError, SSLValidationError, ConnectionError, KeyError,
                                          ImportError, ValueError, TypeError, HTTPError, URLError])
    def test_main_export_lc_logs_exception_handling_case(self, exc_type, mocker, idrac_connection_export_lc_logs_mock,
                                                         idrac_default_args, idrac_file_manager_export_lc_logs_mock,
                                                         idrac_redfish_connection_export_lc_logs_mock):
        idrac_redfish_connection_export_lc_logs_mock.get_server_generation = server_generation_info
        idrac_default_args.update({"share_name": "sharename", "share_user": "shareuser",
                                   "share_password": "sharepassword", "job_wait": True})
        idrac_connection_export_lc_logs_mock.log_mgr.lclog_export.return_value = {"Status": "Failed"}
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + EXPORT_LOGS,
                         side_effect=exc_type('test'))
        else:
            mocker.patch(MODULE_PATH + EXPORT_LOGS,
                         side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
        if exc_type != URLError:
            result = self._run_module(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result

    @pytest.mark.parametrize("args_update", [{"share_user": "share@user"}, {"share_user": "shareuser"}, {"share_user": "share\\user"}])
    def test_get_user_credentials(self, args_update, idrac_connection_export_lc_logs_mock, idrac_default_args, idrac_file_manager_export_lc_logs_mock, mocker):
        idrac_default_args.update({"share_name": "sharename",
                                   "share_password": "sharepassword", "job_wait": True})
        obj = MagicMock()
        obj.IsValid = True
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.file_share_manager.create_share_obj", return_value=(obj))
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idrac_default_args.update(args_update)
        share = self.module.get_user_credentials(f_module)
        assert share.IsValid is True

    def test_run_export_lc_logs(self, idrac_connection_export_lc_logs_mock, idrac_default_args, idrac_file_manager_export_lc_logs_mock, mocker):
        idrac_default_args.update({"idrac_port": 443, "share_name": "sharename", "share_user": "share@user",
                                   "share_password": "sharepassword", "job_wait": True})
        obj = MagicMock()
        obj._name_ = "AF_INET6"
        my_share = MagicMock()
        my_share.new_file.return_value = "idrac_ip_file"
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.file_share_manager.create_share_obj", return_value=(my_share))
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.get_user_credentials", return_value=(my_share))
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.socket.getaddrinfo", return_value=([[obj]]))
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.copy.deepcopy", return_value=("idrac_ip"))
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.copy.deepcopy", return_value=("idrac_ip"))
        idrac_connection_export_lc_logs_mock.log_mgr.lclog_export.return_value = {
            "Status": "Success"}
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        msg = self.module.run_export_lc_logs(
            idrac_connection_export_lc_logs_mock, f_module)
        assert msg['Status'] == "Success"

        idrac_default_args.update({"idrac_port": 443, "share_name": "sharename", "share_user": "shareuser",
                                   "share_password": "sharepassword", "job_wait": True})
        obj._name_ = "AF_INET4"
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.socket.getaddrinfo", return_value=([[obj]]))
        msg = self.module.run_export_lc_logs(
            idrac_connection_export_lc_logs_mock, f_module)
        assert msg['Status'] == "Success"


class TestFilteredLogQuery:

    def test_is_filtered_query_requested_true_for_date_start(self):
        module_mock = MagicMock()
        module_mock.params = {
            "date_start": "2026-01-01T00:00:00Z", "date_end": None,
            "severity": None, "category": None, "message_contains": None,
            "fetch_metadata_only": None}
        assert idrac_lifecycle_controller_logs.is_filtered_query_requested(module_mock) is True

    def test_is_filtered_query_requested_false_when_no_params(self):
        module_mock = MagicMock()
        module_mock.params = {
            "date_start": None, "date_end": None, "severity": None,
            "category": None, "message_contains": None,
            "fetch_metadata_only": None}
        assert idrac_lifecycle_controller_logs.is_filtered_query_requested(module_mock) is False

    def test_run_filtered_log_query_metadata_only(self, mocker):
        idrac_mock = MagicMock()
        module_mock = MagicMock()
        module_mock.params = {"fetch_metadata_only": True}
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_logs.validate_lc_log_firmware_version")
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_logs.check_lc_log_service_available")
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.fetch_lc_log_metadata",
            return_value={"total_entries": 5})
        idrac_lifecycle_controller_logs.run_filtered_log_query(idrac_mock, module_mock)
        module_mock.exit_json.assert_called_once_with(
            msg="Successfully fetched the lifecycle controller log metadata.",
            lc_log_metadata={"total_entries": 5}, changed=False)

    def test_run_filtered_log_query_entries(self, mocker):
        idrac_mock = MagicMock()
        module_mock = MagicMock()
        module_mock.params = {
            "fetch_metadata_only": None, "date_start": None, "date_end": None,
            "severity": ["Critical"], "category": None, "message_contains": None,
            "max_entries": None, "export_path": None}
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_logs.validate_lc_log_firmware_version")
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_logs.check_lc_log_service_available")
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.fetch_lc_logs",
            return_value=[{"Id": "1"}])
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.discover_message_registry",
            return_value=None)
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.enrich_with_message_registry",
            return_value=[{"Id": "1", "message_description": None, "message_resolution": None}])
        idrac_lifecycle_controller_logs.run_filtered_log_query(idrac_mock, module_mock)
        module_mock.exit_json.assert_called_once_with(
            msg="Successfully fetched the lifecycle controller logs.",
            lc_logs=[{"Id": "1", "message_description": None, "message_resolution": None}], changed=False)

    def test_run_filtered_log_query_with_export(self, mocker):
        idrac_mock = MagicMock()
        idrac_mock.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
        module_mock = MagicMock()
        module_mock.params = {
            "fetch_metadata_only": None, "date_start": None, "date_end": None,
            "severity": None, "category": None, "message_contains": None,
            "max_entries": None, "export_path": "/tmp/export.json",
            "export_format": None, "force": False}
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_logs.validate_lc_log_firmware_version")
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_logs.check_lc_log_service_available")
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.fetch_lc_logs",
            return_value=[{"Id": "1"}])
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.discover_message_registry",
            return_value=None)
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.enrich_with_message_registry",
            return_value=[{"Id": "1", "message_description": None, "message_resolution": None}])
        export_mock = mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.export_entries",
            return_value="/tmp/export.json")
        idrac_lifecycle_controller_logs.run_filtered_log_query(idrac_mock, module_mock)
        assert export_mock.call_args.kwargs["export_format"] == "json"
        module_mock.exit_json.assert_called_once_with(
            msg="Successfully exported the lifecycle controller logs.",
            lc_logs=[{"Id": "1", "message_description": None, "message_resolution": None}],
            export_path="/tmp/export.json", changed=True)

    def test_is_filtered_query_requested_true_for_export_path(self):
        module_mock = MagicMock()
        module_mock.params = {
            "date_start": None, "date_end": None, "severity": None,
            "category": None, "message_contains": None,
            "fetch_metadata_only": None, "export_path": "/tmp/out.json"}
        assert idrac_lifecycle_controller_logs.is_filtered_query_requested(module_mock) is True

    def test_build_export_metadata_contains_expected_fields(self):
        idrac_mock = MagicMock()
        idrac_mock.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
        module_mock = MagicMock()
        module_mock.params = {
            "date_start": "2026-01-01T00:00:00Z", "date_end": None,
            "severity": ["Critical"], "category": None, "message_contains": None}
        metadata = idrac_lifecycle_controller_logs.build_export_metadata(idrac_mock, module_mock)
        assert metadata["server_model"] == "iDRAC 9"
        assert metadata["idrac_version"] == "7.10.90.00"
        assert metadata["filters_applied"]["date_start"] == "2026-01-01T00:00:00Z"
        assert metadata["filters_applied"]["severity"] == ["Critical"]


class TestClearLogsAndCommentDispatch:

    def test_run_clear_logs_without_export(self, mocker):
        idrac_mock = MagicMock()
        module_mock = MagicMock()
        module_mock.params = {
            "export_path": None, "clear_only_if_export_succeeded": None,
            "storage_threshold_pct": 80}
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.clear_lc_logs",
            return_value={"pre_clear_count": 5, "post_clear_count": 0, "entries_cleared": 5})
        idrac_lifecycle_controller_logs.run_clear_logs(idrac_mock, module_mock)
        module_mock.exit_json.assert_called_once_with(
            msg="Successfully cleared the lifecycle controller logs.",
            lc_log_clear_status={"pre_clear_count": 5, "post_clear_count": 0, "entries_cleared": 5},
            changed=True)

    def test_run_clear_logs_safety_gate_aborts_without_export_path(self, mocker):
        idrac_mock = MagicMock()
        module_mock = MagicMock()
        module_mock.params = {
            "export_path": None, "clear_only_if_export_succeeded": True,
            "storage_threshold_pct": 80}
        idrac_lifecycle_controller_logs.run_clear_logs(idrac_mock, module_mock)
        module_mock.exit_json.assert_called_once_with(
            msg="Clear aborted: export validation failed. Logs preserved to prevent data loss.",
            failed=True)

    def test_run_clear_logs_safety_gate_aborts_on_export_failure(self, mocker):
        idrac_mock = MagicMock()
        idrac_mock.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
        module_mock = MagicMock()
        module_mock.params = {
            "export_path": "/tmp/export.json", "clear_only_if_export_succeeded": True,
            "date_start": None, "date_end": None, "severity": None, "category": None,
            "message_contains": None, "max_entries": None, "export_format": None,
            "force": False, "storage_threshold_pct": 80}
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.fetch_lc_logs", return_value=[])
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.discover_message_registry",
            return_value=None)
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.enrich_with_message_registry",
            return_value=[])
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.export_entries",
            side_effect=idrac_lifecycle_controller_logs.ExportPathError("no permission"))
        idrac_lifecycle_controller_logs.run_clear_logs(idrac_mock, module_mock)
        module_mock.exit_json.assert_called_once_with(
            msg="Clear aborted: export validation failed. Logs preserved to prevent data loss.",
            failed=True)

    def test_run_clear_logs_with_export_success(self, mocker):
        idrac_mock = MagicMock()
        idrac_mock.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
        module_mock = MagicMock()
        module_mock.params = {
            "export_path": "/tmp/export.json", "clear_only_if_export_succeeded": False,
            "date_start": None, "date_end": None, "severity": None, "category": None,
            "message_contains": None, "max_entries": None, "export_format": None,
            "force": False, "storage_threshold_pct": 80}
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.fetch_lc_logs", return_value=[{"Id": "1"}])
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.discover_message_registry",
            return_value=None)
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.enrich_with_message_registry",
            return_value=[{"Id": "1"}])
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.export_entries",
            return_value="/tmp/export.json")
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.clear_lc_logs",
            return_value={"pre_clear_count": 1, "post_clear_count": 0, "entries_cleared": 1})
        idrac_lifecycle_controller_logs.run_clear_logs(idrac_mock, module_mock)
        module_mock.exit_json.assert_called_once_with(
            msg="Successfully cleared the lifecycle controller logs.",
            lc_log_clear_status={
                "pre_clear_count": 1, "post_clear_count": 0, "entries_cleared": 1,
                "export_path": "/tmp/export.json"},
            changed=True)

    def test_run_filtered_log_query_dispatches_to_clear_logs(self, mocker):
        idrac_mock = MagicMock()
        module_mock = MagicMock()
        module_mock.params = {
            "fetch_metadata_only": None, "clear_logs": True, "storage_threshold_pct": 80}
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_logs.validate_lc_log_firmware_version")
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_logs.check_lc_log_service_available")
        run_clear_mock = mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.run_clear_logs")
        idrac_lifecycle_controller_logs.run_filtered_log_query(idrac_mock, module_mock)
        run_clear_mock.assert_called_once_with(idrac_mock, module_mock)

    def test_run_filtered_log_query_dispatches_to_insert_comment(self, mocker):
        idrac_mock = MagicMock()
        module_mock = MagicMock()
        module_mock.params = {
            "fetch_metadata_only": None, "clear_logs": None,
            "insert_comment": "Maintenance window", "storage_threshold_pct": 80}
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_logs.validate_lc_log_firmware_version")
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_logs.check_lc_log_service_available")
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.insert_lc_log_comment",
            return_value={"Id": "1", "Created": "2026-01-15T10:00:00Z"})
        idrac_lifecycle_controller_logs.run_filtered_log_query(idrac_mock, module_mock)
        module_mock.exit_json.assert_called_once_with(
            msg="Successfully inserted the comment into the lifecycle controller logs.",
            lc_log_comment={"Id": "1", "Created": "2026-01-15T10:00:00Z"}, changed=True)

    def test_is_filtered_query_requested_true_for_clear_logs(self):
        module_mock = MagicMock()
        module_mock.params = {
            "date_start": None, "date_end": None, "severity": None,
            "category": None, "message_contains": None,
            "fetch_metadata_only": None, "export_path": None,
            "clear_logs": True, "insert_comment": None}
        assert idrac_lifecycle_controller_logs.is_filtered_query_requested(module_mock) is True

    def test_is_filtered_query_requested_true_for_insert_comment(self):
        module_mock = MagicMock()
        module_mock.params = {
            "date_start": None, "date_end": None, "severity": None,
            "category": None, "message_contains": None,
            "fetch_metadata_only": None, "export_path": None,
            "clear_logs": None, "insert_comment": "note"}
        assert idrac_lifecycle_controller_logs.is_filtered_query_requested(module_mock) is True
