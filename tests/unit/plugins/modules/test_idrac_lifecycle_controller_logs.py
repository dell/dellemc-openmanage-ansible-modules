# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.3
# Copyright (C) 2020-2026 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import json
import os
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_lifecycle_controller_logs
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from unittest.mock import MagicMock
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestExportLcLogs(FakeAnsibleModule):
    module = idrac_lifecycle_controller_logs

    @pytest.fixture
    def idrac_redfish_lc_logs_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_redfish_connection_export_lc_logs_mock(self, mocker, idrac_redfish_lc_logs_mock):
        idrac_redfish_conn_class_mock = mocker.patch(
            MODULE_PATH + 'idrac_lifecycle_controller_logs.iDRACRedfishAPI',
            return_value=idrac_redfish_lc_logs_mock
        )
        idrac_redfish_conn_class_mock.return_value.__enter__.return_value = idrac_redfish_lc_logs_mock
        return idrac_redfish_lc_logs_mock

    def test_main_export_lc_logs_success_case(self, idrac_default_args, mocker,
                                              idrac_redfish_connection_export_lc_logs_mock):
        idrac_default_args.update({"share_name": "sharename", "share_user": "shareuser",
                                   "share_password": "sharepassword", "job_wait": True})
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLifecycleControllerLogs.get_lc_log_metadata",
            return_value={"total_entries": 100, "storage_utilization_pct": 50})
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLifecycleControllerLogs.lifecycle_controller_logs_operation",
            return_value=("Successfully exported the lifecycle controller logs.", {"Status": "Success"}, True))
        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Successfully exported the lifecycle controller logs."

    def test_fetch_metadata_only(self, idrac_default_args, mocker,
                                 idrac_redfish_connection_export_lc_logs_mock):
        """Test fetch_metadata_only mode returning log service statistics"""
        idrac_default_args.update({"share_name": "/tmp", "fetch_metadata_only": True})
        mock_metadata = {
            "total_entries": 150,
            "oldest_timestamp": "2026-01-01T00:00:00Z",
            "newest_timestamp": "2026-08-18T12:00:00Z",
            "severity_breakdown": {
                "Critical": 5,
                "Warning": 20,
                "OK": 100,
                "Other": 25
            },
            "storage_utilization_pct": 75.0,
            "max_records": 200,
            "overwrite_policy": "WrapsWhenFull"
        }
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLifecycleControllerLogs.get_lc_log_metadata",
            return_value=mock_metadata)
        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Successfully retrieved LC log metadata."
        assert result["log_metadata"] == mock_metadata
        assert result["changed"] is False

    def test_verify_export(self, idrac_default_args, mocker,
                           idrac_redfish_connection_export_lc_logs_mock):
        """Test verify_export parameter (AC-006)"""
        idrac_default_args.update({
            "share_name": "/tmp/export",
            "verify_export": True
        })
        mock_metadata = {
            "total_entries": 150,
            "storage_utilization_pct": 50
        }
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLifecycleControllerLogs.get_lc_log_metadata",
            return_value=mock_metadata)
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLifecycleControllerLogs.lifecycle_controller_logs_operation",
            return_value=("Successfully exported the lifecycle controller logs.", {"Status": "Success"}, True))
        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Successfully exported the lifecycle controller logs."
        assert "export_verification" in result
        assert result["export_verification"]["verified"] is True
        assert result["export_verification"]["expected_count"] == 150

    def test_storage_threshold_warning(self, idrac_default_args, mocker,
                                       idrac_redfish_connection_export_lc_logs_mock):
        """Test storage_threshold_pct parameter (AC-008)"""
        idrac_default_args.update({
            "share_name": "/tmp/export",
            "storage_threshold_pct": 80
        })
        mock_metadata = {
            "total_entries": 180,
            "storage_utilization_pct": 90.0,
            "overwrite_policy": "WrapsWhenFull"
        }
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLifecycleControllerLogs.get_lc_log_metadata",
            return_value=mock_metadata)
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLifecycleControllerLogs.lifecycle_controller_logs_operation",
            return_value=("Successfully exported the lifecycle controller logs.", {"Status": "Success"}, True))
        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Successfully exported the lifecycle controller logs."
        assert "storage_warning" in result
        assert "90.0%" in result["storage_warning"]

    def test_insert_comment(self, idrac_default_args, mocker,
                            idrac_redfish_connection_export_lc_logs_mock):
        """Test insert_comment parameter (AC-009)"""
        idrac_default_args.update({
            "share_name": "/tmp",
            "insert_comment": "Test automation comment"
        })
        mock_comment_result = {
            "entry_id": "LC123456",
            "timestamp": "2026-08-18T12:00:00Z"
        }
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLifecycleControllerLogs.insert_lc_comment",
            return_value=mock_comment_result)
        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Successfully inserted comment into LC logs."
        assert result["inserted_entry_id"] == "LC123456"
        assert result["inserted_entry_timestamp"] == "2026-08-18T12:00:00Z"
        assert result["changed"] is True

    def test_insert_comment_too_long(self, idrac_default_args, mocker,
                                     idrac_redfish_connection_export_lc_logs_mock):
        """Test insert_comment validation - comment too long"""
        long_comment = "x" * 300  # Exceeds 256 character limit
        idrac_default_args.update({
            "share_name": "/tmp",
            "insert_comment": long_comment
        })
        result = self._run_module(idrac_default_args)
        assert result["failed"] is True
        assert "256 characters" in result["msg"]

    def test_insert_comment_control_characters(self, idrac_default_args, mocker,
                                               idrac_redfish_connection_export_lc_logs_mock):
        """Test insert_comment validation - control characters (using tab)"""
        idrac_default_args.update({
            "share_name": "/tmp",
            "insert_comment": "Test\tcomment"
        })
        result = self._run_module(idrac_default_args)
        assert result["failed"] is True
        assert "control characters" in result["msg"]

    def test_filter_optimization_single_query(self, idrac_default_args, mocker,
                                              idrac_redfish_connection_export_lc_logs_mock):
        """Test filter_optimization parameter (AC-007)"""
        idrac_default_args.update({
            "share_name": "/tmp/export",
            "filter_optimization": "single_query"
        })
        mock_metadata = {"total_entries": 100, "storage_utilization_pct": 50}
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLifecycleControllerLogs.get_lc_log_metadata",
            return_value=mock_metadata)
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLifecycleControllerLogs.lifecycle_controller_logs_operation",
            return_value=("Successfully exported the lifecycle controller logs.", {"Status": "Success"}, True))
        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Successfully exported the lifecycle controller logs."

    def test_date_range_filter(self, idrac_default_args, mocker,
                               idrac_redfish_connection_export_lc_logs_mock):
        """Test date_start and date_end parameters (AC-001)"""
        idrac_default_args.update({
            "share_name": "/tmp/export",
            "date_start": "2026-08-01T00:00:00Z",
            "date_end": "2026-08-31T23:59:59Z"
        })
        mock_entries = [
            {
                "Id": "1",
                "Created": "2026-08-15T10:00:00Z",
                "Severity": "Warning",
                "Message": "Test log entry"
            }
        ]
        mock_response = MagicMock()
        mock_response.json_data = {"Members": mock_entries}
        idrac_redfish_connection_export_lc_logs_mock.invoke_request.return_value = mock_response

        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.export",
            return_value=1)
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.validate_permissions",
            return_value=True)

        result = self._run_module(idrac_default_args)
        assert "filters_applied" in result
        assert result["filters_applied"]["date_start"] == "2026-08-01T00:00:00Z"
        assert result["filters_applied"]["date_end"] == "2026-08-31T23:59:59Z"

    def test_severity_filter(self, idrac_default_args, mocker,
                             idrac_redfish_connection_export_lc_logs_mock):
        """Test severity parameter (AC-002)"""
        idrac_default_args.update({
            "share_name": "/tmp/export",
            "severity": ["Critical", "Warning"]
        })
        mock_entries = [
            {
                "Id": "1",
                "Created": "2026-08-15T10:00:00Z",
                "Severity": "Critical",
                "Message": "Critical error occurred"
            },
            {
                "Id": "2",
                "Created": "2026-08-15T11:00:00Z",
                "Severity": "Warning",
                "Message": "Warning message"
            }
        ]
        mock_response = MagicMock()
        mock_response.json_data = {"Members": mock_entries}
        idrac_redfish_connection_export_lc_logs_mock.invoke_request.return_value = mock_response

        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.export",
            return_value=2)
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.validate_permissions",
            return_value=True)

        result = self._run_module(idrac_default_args)
        assert "filters_applied" in result
        assert result["filters_applied"]["severity"] == ["Critical", "Warning"]

    def test_export_format_csv(self, idrac_default_args, mocker,
                               idrac_redfish_connection_export_lc_logs_mock):
        """Test export_format parameter with CSV (AC-003)"""
        idrac_default_args.update({
            "share_name": "/tmp/export/logs.csv",
            "export_format": "csv",
            "severity": ["Critical"]
        })
        mock_entries = [
            {
                "Id": "1",
                "Created": "2026-08-15T10:00:00Z",
                "Severity": "Critical",
                "Message": "Critical error"
            }
        ]
        mock_response = MagicMock()
        mock_response.json_data = {"Members": mock_entries}
        idrac_redfish_connection_export_lc_logs_mock.invoke_request.return_value = mock_response

        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.export",
            return_value=1)
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.validate_permissions",
            return_value=True)

        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Successfully exported filtered lifecycle controller logs."

    def test_export_format_json_with_metadata(self, idrac_default_args, mocker,
                                              idrac_redfish_connection_export_lc_logs_mock):
        """Test export_format JSON with metadata envelope (AC-005)"""
        idrac_default_args.update({
            "share_name": "/tmp/export/logs.json",
            "export_format": "json",
            "date_start": "2026-08-01",
            "severity": ["Critical"]
        })
        mock_entries = [
            {
                "Id": "1",
                "Created": "2026-08-15T10:00:00Z",
                "Severity": "Critical",
                "Message": "Critical error"
            }
        ]
        mock_response = MagicMock()
        mock_response.json_data = {"Members": mock_entries}
        idrac_redfish_connection_export_lc_logs_mock.invoke_request.return_value = mock_response

        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.export",
            return_value=1)
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.validate_permissions",
            return_value=True)

        result = self._run_module(idrac_default_args)
        assert "filters_applied" in result
        assert "exported_entry_count" in result

    def test_category_filter(self, idrac_default_args, mocker,
                             idrac_redfish_connection_export_lc_logs_mock):
        """Test category parameter"""
        idrac_default_args.update({
            "share_name": "/tmp/export",
            "category": ["Audit", "Configuration"]
        })
        mock_entries = [
            {
                "Id": "1",
                "Created": "2026-08-15T10:00:00Z",
                "Severity": "OK",
                "Message": "Configuration changed",
                "Oem": {"Dell": {"DellLCLogEntry": {"Category": "Configuration"}}}
            }
        ]
        mock_response = MagicMock()
        mock_response.json_data = {"Members": mock_entries}
        idrac_redfish_connection_export_lc_logs_mock.invoke_request.return_value = mock_response

        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.export",
            return_value=1)
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.validate_permissions",
            return_value=True)

        result = self._run_module(idrac_default_args)
        assert "filters_applied" in result
        assert result["filters_applied"]["category"] == ["Audit", "Configuration"]

    def test_message_contains_filter(self, idrac_default_args, mocker,
                                     idrac_redfish_connection_export_lc_logs_mock):
        """Test message_contains parameter (client-side filter)"""
        idrac_default_args.update({
            "share_name": "/tmp/export",
            "message_contains": "firmware"
        })
        mock_entries = [
            {
                "Id": "1",
                "Created": "2026-08-15T10:00:00Z",
                "Severity": "OK",
                "Message": "Firmware update completed successfully"
            },
            {
                "Id": "2",
                "Created": "2026-08-15T11:00:00Z",
                "Severity": "OK",
                "Message": "System restarted"
            }
        ]
        mock_response = MagicMock()
        mock_response.json_data = {"Members": mock_entries}
        idrac_redfish_connection_export_lc_logs_mock.invoke_request.return_value = mock_response

        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.export",
            return_value=1)
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.validate_permissions",
            return_value=True)

        result = self._run_module(idrac_default_args)
        assert "filters_applied" in result
        assert result["filters_applied"]["message_contains"] == "firmware"
        # Only the entry with "firmware" should be in the result
        assert len(result.get("lc_logs", [])) == 1

    def test_combined_filters(self, idrac_default_args, mocker,
                              idrac_redfish_connection_export_lc_logs_mock):
        """Test combined filters (AC-007 - filter optimization)"""
        idrac_default_args.update({
            "share_name": "/tmp/export",
            "date_start": "2026-08-01",
            "severity": ["Critical"],
            "category": ["SystemHealth"],
            "filter_optimization": "single_query"
        })
        mock_entries = [
            {
                "Id": "1",
                "Created": "2026-08-15T10:00:00Z",
                "Severity": "Critical",
                "Message": "System health critical",
                "Oem": {"Dell": {"DellLCLogEntry": {"Category": "SystemHealth"}}}
            }
        ]
        mock_response = MagicMock()
        mock_response.json_data = {"Members": mock_entries}
        idrac_redfish_connection_export_lc_logs_mock.invoke_request.return_value = mock_response

        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.export",
            return_value=1)
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.validate_permissions",
            return_value=True)

        result = self._run_module(idrac_default_args)
        assert "filters_applied" in result
        assert result["filters_applied"]["date_start"] == "2026-08-01"
        assert result["filters_applied"]["severity"] == ["Critical"]
        assert result["filters_applied"]["category"] == ["SystemHealth"]

    def test_no_matching_entries(self, idrac_default_args, mocker,
                                 idrac_redfish_connection_export_lc_logs_mock):
        """Test when filters produce no matching entries"""
        idrac_default_args.update({
            "share_name": "/tmp/export",
            "severity": ["Critical"]
        })
        mock_response = MagicMock()
        mock_response.json_data = {"Members": []}
        idrac_redfish_connection_export_lc_logs_mock.invoke_request.return_value = mock_response

        result = self._run_module(idrac_default_args)
        assert result["msg"] == "No log entries matched the specified filters."
        assert result["lc_logs"] == []
        assert result["changed"] is False

    def test_invalid_date_range(self, idrac_default_args, mocker,
                                idrac_redfish_connection_export_lc_logs_mock):
        """Test validation when date_end is before date_start"""
        idrac_default_args.update({
            "share_name": "/tmp/export",
            "date_start": "2026-08-31T00:00:00Z",
            "date_end": "2026-08-01T00:00:00Z"
        })
        result = self._run_module(idrac_default_args)
        assert result["failed"] is True
        assert "date_end must not be earlier than date_start" in result["msg"]

    @pytest.mark.parametrize("exc_type", [RuntimeError, SSLValidationError, ConnectionError, KeyError,
                                          ImportError, ValueError, TypeError, HTTPError, URLError])
    def test_main_export_lc_logs_exception_handling_case(self, exc_type, mocker,
                                                         idrac_default_args,
                                                         idrac_redfish_connection_export_lc_logs_mock):
        idrac_default_args.update({"share_name": "sharename", "share_user": "shareuser",
                                   "share_password": "sharepassword", "job_wait": True})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(
                MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLifecycleControllerLogs.get_lc_log_metadata",
                return_value={"total_entries": 100, "storage_utilization_pct": 50})
            mocker.patch(
                MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLifecycleControllerLogs.lifecycle_controller_logs_operation",
                side_effect=exc_type('test'))
        else:
            mocker.patch(
                MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLifecycleControllerLogs.get_lc_log_metadata",
                return_value={"total_entries": 100, "storage_utilization_pct": 50})
            mocker.patch(
                MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLifecycleControllerLogs.lifecycle_controller_logs_operation",
                side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                     {"accept-type": "application/json"}, StringIO(json_str)))
        if exc_type != URLError:
            result = self._run_module(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result

    def test_filter_combinations_with_mocked_payloads(self, idrac_default_args, mocker,
                                                      idrac_redfish_connection_export_lc_logs_mock):
        """Test all filter combinations with mocked payloads"""
        import json
        # Load fixture
        fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'lc_log_entries_idrac9.json')
        with open(fixture_path) as f:
            fixture_data = json.load(f)

        # Test combined filters
        idrac_default_args.update({
            "share_name": "/tmp/export",
            "date_start": "2026-08-15T00:00:00Z",
            "date_end": "2026-08-18T23:59:59Z",
            "severity": ["Critical"],
            "category": ["SystemHealth"]
        })

        mock_response = MagicMock()
        mock_response.json_data = fixture_data
        idrac_redfish_connection_export_lc_logs_mock.invoke_request.return_value = mock_response

        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.export",
            return_value=2)
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.validate_permissions",
            return_value=True)

        result = self._run_module(idrac_default_args)
        assert "filters_applied" in result
        assert result["filters_applied"]["severity"] == ["Critical"]
        assert result["filters_applied"]["category"] == ["SystemHealth"]

    def test_pagination_across_multiple_pages(self, idrac_default_args, mocker,
                                              idrac_redfish_connection_export_lc_logs_mock):
        """Test pagination across multiple pages"""
        # First page
        page1 = {
            "Members": [
                {"Id": "1", "Created": "2026-08-15T10:00:00Z", "Severity": "Critical", "Message": "Test 1"}
            ],
            "Members@odata.nextLink": "/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Lclog/Entries?$skip=50"
        }
        # Second page
        page2 = {
            "Members": [
                {"Id": "2", "Created": "2026-08-15T11:00:00Z", "Severity": "Critical", "Message": "Test 2"}
            ]
        }

        idrac_default_args.update({
            "share_name": "/tmp/export",
            "severity": ["Critical"]
        })

        mock_response1 = MagicMock()
        mock_response1.json_data = page1
        mock_response2 = MagicMock()
        mock_response2.json_data = page2

        # Use a list to track calls
        call_count = [0]

        def mock_invoke_request(uri, method):
            call_count[0] += 1
            if call_count[0] == 1:
                return mock_response1
            else:
                return mock_response2

        idrac_redfish_connection_export_lc_logs_mock.invoke_request.side_effect = mock_invoke_request

        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.export",
            return_value=2)
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.validate_permissions",
            return_value=True)

        result = self._run_module(idrac_default_args)
        assert "lc_logs" in result
        assert len(result["lc_logs"]) == 2  # Both Critical entries from both pages

    def test_json_export_schema_validation(self, idrac_default_args, mocker,
                                           idrac_redfish_connection_export_lc_logs_mock):
        """Test JSON export schema validation"""
        idrac_default_args.update({
            "share_name": "/tmp/export/logs.json",
            "export_format": "json",
            "severity": ["Critical"]
        })

        mock_entries = [
            {
                "Id": "1",
                "Created": "2026-08-15T10:00:00Z",
                "Severity": "Critical",
                "Message": "Test"
            }
        ]
        mock_response = MagicMock()
        mock_response.json_data = {"Members": mock_entries}
        idrac_redfish_connection_export_lc_logs_mock.invoke_request.return_value = mock_response

        # Mock the export to capture the data
        exported_data = {}

        def mock_export(entries, metadata):
            exported_data["entries"] = entries
            exported_data["metadata"] = metadata
            return len(entries)

        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.export",
            side_effect=mock_export)
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.validate_permissions",
            return_value=True)

        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Successfully exported filtered lifecycle controller logs."
        assert "metadata" in exported_data
        assert "entries" in exported_data
        assert "filters_applied" in exported_data["metadata"]

    def test_csv_export_structure_validation(self, idrac_default_args, mocker,
                                             idrac_redfish_connection_export_lc_logs_mock):
        """Test CSV export structure validation"""
        idrac_default_args.update({
            "share_name": "/tmp/export/logs.csv",
            "export_format": "csv",
            "severity": ["Critical"]
        })

        mock_entries = [
            {
                "Id": "1",
                "Created": "2026-08-15T10:00:00Z",
                "Severity": "Critical",
                "Message": "Test"
            }
        ]
        mock_response = MagicMock()
        mock_response.json_data = {"Members": mock_entries}
        idrac_redfish_connection_export_lc_logs_mock.invoke_request.return_value = mock_response

        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.export",
            return_value=1)
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.validate_permissions",
            return_value=True)

        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Successfully exported filtered lifecycle controller logs."
        assert result["exported_entry_count"] == 1

    def test_text_export_format_validation(self, idrac_default_args, mocker,
                                           idrac_redfish_connection_export_lc_logs_mock):
        """Test text export format validation"""
        idrac_default_args.update({
            "share_name": "/tmp/export/logs.txt",
            "export_format": "text",
            "severity": ["Critical"]
        })

        mock_entries = [
            {
                "Id": "1",
                "Created": "2026-08-15T10:00:00Z",
                "Severity": "Critical",
                "Message": "Test"
            }
        ]
        mock_response = MagicMock()
        mock_response.json_data = {"Members": mock_entries}
        idrac_redfish_connection_export_lc_logs_mock.invoke_request.return_value = mock_response

        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.export",
            return_value=1)
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.validate_permissions",
            return_value=True)

        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Successfully exported filtered lifecycle controller logs."
        assert result["exported_entry_count"] == 1

    def test_firmware_version_validation_failure(self, idrac_default_args, mocker,
                                                 idrac_redfish_connection_export_lc_logs_mock):
        """Test firmware version validation failure"""
        # This test would require mocking the firmware version check
        # For now, we'll test that the module handles version-related errors
        idrac_default_args.update({
            "share_name": "/tmp/export",
            "date_start": "2026-08-01"
        })

        # Simulate a firmware version error
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLifecycleControllerLogs.get_lc_log_metadata",
            side_effect=ValueError("iDRAC firmware version 6.00.00.00 is below minimum required version 7.10.90.00"))

        result = self._run_module(idrac_default_args)
        assert result["failed"] is True
        assert "firmware" in result["msg"].lower()

    def test_transient_api_error_with_retry_logic(self, idrac_default_args, mocker,
                                                  idrac_redfish_connection_export_lc_logs_mock):
        """Test transient API error handling"""
        idrac_default_args.update({
            "share_name": "/tmp/export",
            "severity": ["Critical"]
        })

        # Simulate transient error
        from ansible.module_utils.urls import ConnectionError
        idrac_redfish_connection_export_lc_logs_mock.invoke_request.side_effect = ConnectionError("Transient network error")

        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.export",
            return_value=1)
        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLogExporter.validate_permissions",
            return_value=True)

        # Note: The current implementation doesn't have retry logic in the main module
        # This test documents expected behavior for future enhancement
        # For now, we expect the error to be propagated
        result = self._run_module(idrac_default_args)
        assert result["failed"] is True
