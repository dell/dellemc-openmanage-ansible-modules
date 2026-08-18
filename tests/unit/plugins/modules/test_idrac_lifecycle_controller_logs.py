# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.5
# Copyright (C) 2020-2026 Dell Inc. or its subsidiaries. All Rights Reserved.

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
        """Test insert_comment validation - control characters"""
        idrac_default_args.update({
            "share_name": "/tmp",
            "insert_comment": "Test\x00comment"
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
