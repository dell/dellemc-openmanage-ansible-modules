# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.0
# Copyright (C) 2024-2026 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from unittest.mock import MagicMock, patch
from datetime import datetime, timezone, timedelta
import pytest
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_session_info
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_session_info'

# --- Test Fixtures ---

IDRAC9_SESSION_DATA = [
    {
        "Id": "74",
        "UserName": "root",
        "ClientOriginIPAddress": "100.96.37.58",
        "SessionType": "Redfish",
        "CreatedTime": (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat(),
        "Description": "User Session",
        "Name": "User Session",
    },
    {
        "Id": "75",
        "UserName": "admin",
        "ClientOriginIPAddress": "100.96.37.59",
        "SessionType": "WebUI",
        "CreatedTime": (datetime.now(timezone.utc) - timedelta(hours=48)).isoformat(),
        "Description": "User Session",
        "Name": "User Session",
    },
    {
        "Id": "76",
        "UserName": "operator",
        "ClientOriginIPAddress": "100.96.37.60",
        "SessionType": "IPMI",
        "CreatedTime": (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat(),
        "Description": "User Session",
        "Name": "User Session",
    },
]

IDRAC10_SESSION_DATA = [
    {
        "Id": "1",
        "UserName": "root",
        "ClientOriginIPAddress": "192.168.1.100",
        "SessionType": "Redfish",
        "CreatedTime": (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat(),
        "Description": "User Session",
        "Name": "User Session",
    },
]

IDRAC9_MISSING_FIELDS_DATA = [
    {
        "Id": "80",
        "UserName": "root",
        "Description": "User Session",
        "Name": "User Session",
    },
]

SESSION_SERVICE_DATA = {
    "SessionTimeout": 1800,
    "ServiceEnabled": True,
}

SESSION_SERVICE_DISABLED_DATA = {
    "SessionTimeout": 1800,
    "ServiceEnabled": False,
}

IDRAC_ATTRIBUTES_DATA = {
    "Attributes": {
        "WebServer.1.MaxNumberOfSessions": "64",
    }
}


@pytest.fixture
def idrac_default_args():
    return {
        "idrac_ip": "192.168.0.1",
        "idrac_user": "user",
        "idrac_password": "password",
        "idrac_port": 443,
        "validate_certs": True,
        "ca_path": None,
        "timeout": 30,
    }


# --- Test Suite 1: Firmware Version Gate ---

class TestFirmwareVersionGate(FakeAnsibleModule):
    module = idrac_session_info

    @pytest.fixture
    def idrac_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_mock(self, mocker, idrac_mock):
        with patch(MODULE_PATH + '.iDRACRedfishAPI') as mock_class:
            mock_class.return_value.__enter__.return_value = idrac_mock
            mock_class.return_value.__exit__.return_value = False
            mock_class.check_minimum_firmware_requirement = iDRACRedfishAPI.check_minimum_firmware_requirement
            mock_class.compare_firmware_version = iDRACRedfishAPI.compare_firmware_version
            yield mock_class

    def test_firmware_version_idrac9_compliant(self, idrac_default_args, idrac_mock, idrac_connection_mock):
        """Test 1.1: iDRAC9 firmware meets minimum requirement."""
        idrac_mock.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
        sessions_resp = MagicMock()
        sessions_resp.status_code = 200
        sessions_resp.json_data = {"Members": []}
        svc_resp = MagicMock()
        svc_resp.status_code = 200
        svc_resp.json_data = SESSION_SERVICE_DATA
        attr_resp = MagicMock()
        attr_resp.status_code = 200
        attr_resp.json_data = IDRAC_ATTRIBUTES_DATA
        idrac_mock.invoke_request.side_effect = [sessions_resp, svc_resp, attr_resp]

        result = self._run_module(idrac_default_args)
        assert result['changed'] is False
        assert result['msg'] == "Successfully retrieved session information."

    def test_firmware_version_idrac10_compliant(self, idrac_default_args, idrac_mock, idrac_connection_mock):
        """Test 1.2: iDRAC10 firmware meets minimum requirement."""
        idrac_mock.get_server_generation = (16, "1.20.50.50", "iDRAC 10")
        sessions_resp = MagicMock()
        sessions_resp.status_code = 200
        sessions_resp.json_data = {"Members": []}
        svc_resp = MagicMock()
        svc_resp.status_code = 200
        svc_resp.json_data = SESSION_SERVICE_DATA
        attr_resp = MagicMock()
        attr_resp.status_code = 200
        attr_resp.json_data = IDRAC_ATTRIBUTES_DATA
        idrac_mock.invoke_request.side_effect = [sessions_resp, svc_resp, attr_resp]

        result = self._run_module(idrac_default_args)
        assert result['changed'] is False

    def test_firmware_version_below_minimum(self, idrac_default_args, idrac_mock, idrac_connection_mock):
        """Test 1.3: Firmware below minimum requirement."""
        idrac_mock.get_server_generation = (14, "6.00.00.00", "iDRAC 9")

        result = self._run_module_with_fail_json(idrac_default_args)
        assert result['failed'] is True
        assert "Minimum firmware requirement not met" in result['msg']
        assert "6.00.00.00" in result['msg']


# --- Test Suite 2: Active Session Query ---

class TestActiveSessionQuery(FakeAnsibleModule):
    module = idrac_session_info

    @pytest.fixture
    def idrac_mock(self):
        idrac_obj = MagicMock()
        idrac_obj.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
        return idrac_obj

    @pytest.fixture
    def idrac_connection_mock(self, mocker, idrac_mock):
        with patch(MODULE_PATH + '.iDRACRedfishAPI') as mock_class:
            mock_class.return_value.__enter__.return_value = idrac_mock
            mock_class.return_value.__exit__.return_value = False
            mock_class.check_minimum_firmware_requirement = iDRACRedfishAPI.check_minimum_firmware_requirement
            mock_class.compare_firmware_version = iDRACRedfishAPI.compare_firmware_version
            yield mock_class

    def test_retrieve_all_active_sessions(self, idrac_default_args, idrac_mock, idrac_connection_mock):
        """Test 2.1: Retrieve all active sessions."""
        sessions_resp = MagicMock()
        sessions_resp.status_code = 200
        sessions_resp.json_data = {"Members": IDRAC9_SESSION_DATA}
        svc_resp = MagicMock()
        svc_resp.status_code = 200
        svc_resp.json_data = SESSION_SERVICE_DATA
        attr_resp = MagicMock()
        attr_resp.status_code = 200
        attr_resp.json_data = IDRAC_ATTRIBUTES_DATA
        idrac_mock.invoke_request.side_effect = [sessions_resp, svc_resp, attr_resp]

        result = self._run_module(idrac_default_args)
        assert result['changed'] is False
        assert result['session_count'] == 3
        assert len(result['sessions']) == 3
        for session in result['sessions']:
            assert 'id' in session
            assert 'user_name' in session
            assert 'client_origin_ip' in session
            assert 'session_type' in session
            assert 'created_time' in session
            assert 'session_age_minutes' in session

    def test_no_active_sessions(self, idrac_default_args, idrac_mock, idrac_connection_mock):
        """Test 2.2: No active sessions."""
        sessions_resp = MagicMock()
        sessions_resp.status_code = 200
        sessions_resp.json_data = {"Members": []}
        svc_resp = MagicMock()
        svc_resp.status_code = 200
        svc_resp.json_data = SESSION_SERVICE_DATA
        attr_resp = MagicMock()
        attr_resp.status_code = 200
        attr_resp.json_data = IDRAC_ATTRIBUTES_DATA
        idrac_mock.invoke_request.side_effect = [sessions_resp, svc_resp, attr_resp]

        result = self._run_module(idrac_default_args)
        assert result['changed'] is False
        assert result['session_count'] == 0
        assert result['sessions'] == []

    def test_missing_properties_older_firmware(self, idrac_default_args, idrac_mock, idrac_connection_mock):
        """Test 2.3: Missing properties on older firmware."""
        sessions_resp = MagicMock()
        sessions_resp.status_code = 200
        sessions_resp.json_data = {"Members": IDRAC9_MISSING_FIELDS_DATA}
        svc_resp = MagicMock()
        svc_resp.status_code = 200
        svc_resp.json_data = SESSION_SERVICE_DATA
        attr_resp = MagicMock()
        attr_resp.status_code = 200
        attr_resp.json_data = IDRAC_ATTRIBUTES_DATA
        idrac_mock.invoke_request.side_effect = [sessions_resp, svc_resp, attr_resp]

        result = self._run_module(idrac_default_args)
        assert result['changed'] is False
        assert result['sessions'][0]['session_type'] is None
        assert result['sessions'][0]['session_age_minutes'] is None


# --- Test Suite 3: Session Service Configuration ---

class TestSessionServiceConfig(FakeAnsibleModule):
    module = idrac_session_info

    @pytest.fixture
    def idrac_mock(self):
        idrac_obj = MagicMock()
        idrac_obj.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
        return idrac_obj

    @pytest.fixture
    def idrac_connection_mock(self, mocker, idrac_mock):
        with patch(MODULE_PATH + '.iDRACRedfishAPI') as mock_class:
            mock_class.return_value.__enter__.return_value = idrac_mock
            mock_class.return_value.__exit__.return_value = False
            mock_class.check_minimum_firmware_requirement = iDRACRedfishAPI.check_minimum_firmware_requirement
            mock_class.compare_firmware_version = iDRACRedfishAPI.compare_firmware_version
            yield mock_class

    def test_session_service_config(self, idrac_default_args, idrac_mock, idrac_connection_mock):
        """Test 3.1: SessionService configuration retrieved."""
        sessions_resp = MagicMock()
        sessions_resp.status_code = 200
        sessions_resp.json_data = {"Members": []}
        svc_resp = MagicMock()
        svc_resp.status_code = 200
        svc_resp.json_data = SESSION_SERVICE_DATA
        attr_resp = MagicMock()
        attr_resp.status_code = 200
        attr_resp.json_data = IDRAC_ATTRIBUTES_DATA
        idrac_mock.invoke_request.side_effect = [sessions_resp, svc_resp, attr_resp]

        result = self._run_module(idrac_default_args)
        assert result['session_service']['session_timeout'] == 1800
        assert result['session_service']['service_enabled'] is True

    def test_session_service_disabled(self, idrac_default_args, idrac_mock, idrac_connection_mock):
        """Test 3.2: SessionService disabled."""
        sessions_resp = MagicMock()
        sessions_resp.status_code = 200
        sessions_resp.json_data = {"Members": []}
        svc_resp = MagicMock()
        svc_resp.status_code = 200
        svc_resp.json_data = SESSION_SERVICE_DISABLED_DATA
        attr_resp = MagicMock()
        attr_resp.status_code = 200
        attr_resp.json_data = IDRAC_ATTRIBUTES_DATA
        idrac_mock.invoke_request.side_effect = [sessions_resp, svc_resp, attr_resp]

        result = self._run_module(idrac_default_args)
        assert result['session_service']['service_enabled'] is False
        assert any("disabled" in w.lower() for w in result.get('warnings', []))


# --- Test Suite 4: Session Age Computation ---

class TestSessionAgeComputation:
    """Pure function tests — no module run needed."""

    def test_session_age_computed(self):
        """Test 4.1: Session age computed from CreatedTime."""
        created = (datetime.now(timezone.utc) - timedelta(minutes=60)).isoformat()
        age = idrac_session_info.compute_session_age(created)
        assert age is not None
        assert 59 <= age <= 61

    def test_created_time_null(self):
        """Test 4.2: CreatedTime unavailable."""
        age = idrac_session_info.compute_session_age(None)
        assert age is None

    def test_created_time_invalid(self):
        """Test invalid CreatedTime string."""
        age = idrac_session_info.compute_session_age("not-a-date")
        assert age is None


# --- Test Suite 5: Client-Side Filtering ---

class TestClientSideFiltering:
    """Pure function tests for filter logic."""

    def _make_sessions(self):
        return [
            {"id": "1", "user_name": "root", "session_type": "Redfish", "is_stale": False},
            {"id": "2", "user_name": "admin", "session_type": "WebUI", "is_stale": False},
            {"id": "3", "user_name": "admin_backup", "session_type": "Redfish", "is_stale": True},
            {"id": "4", "user_name": "operator", "session_type": "IPMI", "is_stale": False},
        ]

    def test_filter_by_session_type(self):
        """Test 5.1: Filter by session type."""
        sessions = self._make_sessions()
        filtered = idrac_session_info.filter_sessions(sessions, session_type="Redfish")
        assert len(filtered) == 2
        assert all(s["session_type"] == "Redfish" for s in filtered)

    def test_filter_by_username_substring(self):
        """Test 5.2: Filter by username substring."""
        sessions = self._make_sessions()
        filtered = idrac_session_info.filter_sessions(sessions, username_filter="admin")
        assert len(filtered) == 2
        assert all("admin" in s["user_name"] for s in filtered)

    def test_case_insensitive_username(self):
        """Test 5.3: Case-insensitive username matching."""
        sessions = self._make_sessions()
        filtered = idrac_session_info.filter_sessions(sessions, username_filter="ADMIN")
        assert len(filtered) == 2

    def test_stale_threshold_flagging(self):
        """Test 5.4: Stale sessions flagged."""
        now = datetime.now(timezone.utc)
        raw_sessions = [
            {"Id": "1", "UserName": "root", "SessionType": "Redfish",
             "CreatedTime": (now - timedelta(hours=48)).isoformat(),
             "Description": "old", "Name": "old", "ClientOriginIPAddress": "1.1.1.1"},
            {"Id": "2", "UserName": "admin", "SessionType": "WebUI",
             "CreatedTime": (now - timedelta(minutes=5)).isoformat(),
             "Description": "new", "Name": "new", "ClientOriginIPAddress": "2.2.2.2"},
        ]
        sessions = [idrac_session_info.extract_session_fields(s, stale_threshold=1440) for s in raw_sessions]
        assert sessions[0]["is_stale"] is True
        assert sessions[1]["is_stale"] is False

    def test_combined_type_and_username_filter(self):
        """Test 5.5: Combined type and username filter."""
        sessions = self._make_sessions()
        filtered = idrac_session_info.filter_sessions(sessions, session_type="Redfish", username_filter="admin")
        assert len(filtered) == 1
        assert filtered[0]["user_name"] == "admin_backup"

    def test_combined_all_filters(self):
        """Test 5.6: Combined type, username, and stale filter."""
        sessions = self._make_sessions()
        filtered = idrac_session_info.filter_sessions(sessions, session_type="Redfish", username_filter="admin")
        stale_only = [s for s in filtered if s.get("is_stale")]
        assert len(stale_only) == 1


# --- Test Suite 6: Session Limits Query ---

class TestSessionLimitsQuery(FakeAnsibleModule):
    module = idrac_session_info

    @pytest.fixture
    def idrac_mock(self):
        idrac_obj = MagicMock()
        idrac_obj.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
        return idrac_obj

    @pytest.fixture
    def idrac_connection_mock(self, mocker, idrac_mock):
        with patch(MODULE_PATH + '.iDRACRedfishAPI') as mock_class:
            mock_class.return_value.__enter__.return_value = idrac_mock
            mock_class.return_value.__exit__.return_value = False
            mock_class.check_minimum_firmware_requirement = iDRACRedfishAPI.check_minimum_firmware_requirement
            mock_class.compare_firmware_version = iDRACRedfishAPI.compare_firmware_version
            yield mock_class

    def test_session_limits_from_attributes(self, idrac_default_args, idrac_mock, idrac_connection_mock):
        """Test 6.1: Session limits from iDRAC Attributes (iDRAC10 primary)."""
        sessions_resp = MagicMock()
        sessions_resp.status_code = 200
        sessions_resp.json_data = {"Members": IDRAC10_SESSION_DATA}
        svc_resp = MagicMock()
        svc_resp.status_code = 200
        svc_resp.json_data = SESSION_SERVICE_DATA
        attr_resp = MagicMock()
        attr_resp.status_code = 200
        attr_resp.json_data = IDRAC_ATTRIBUTES_DATA
        idrac_mock.invoke_request.side_effect = [sessions_resp, svc_resp, attr_resp]

        result = self._run_module(idrac_default_args)
        assert result['session_limits']['max_sessions'] == 64
        assert result['session_limits']['source'] == "idrac_attributes"
        assert result['session_limits']['utilization_percent'] == round((1 / 64) * 100, 2)

    def test_session_limits_fallback_manager(self, idrac_default_args, idrac_mock, idrac_connection_mock):
        """Test 6.2: Attributes endpoint 403, falls back to Manager."""
        sessions_resp = MagicMock()
        sessions_resp.status_code = 200
        sessions_resp.json_data = {"Members": IDRAC10_SESSION_DATA}
        svc_resp = MagicMock()
        svc_resp.status_code = 200
        svc_resp.json_data = SESSION_SERVICE_DATA
        attr_error = HTTPError("https://test", 403, "Forbidden", {}, None)
        mgr_resp = MagicMock()
        mgr_resp.status_code = 200
        mgr_resp.json_data = {"MaxSessions": 32}
        idrac_mock.invoke_request.side_effect = [sessions_resp, svc_resp, attr_error, mgr_resp]

        result = self._run_module(idrac_default_args)
        assert result['session_limits']['max_sessions'] == 32
        assert result['session_limits']['source'] == "manager_endpoint"

    def test_session_limits_both_fail(self, idrac_default_args, idrac_mock, idrac_connection_mock):
        """Test 6.3: Both endpoints fail — session listing still succeeds."""
        sessions_resp = MagicMock()
        sessions_resp.status_code = 200
        sessions_resp.json_data = {"Members": IDRAC10_SESSION_DATA}
        svc_resp = MagicMock()
        svc_resp.status_code = 200
        svc_resp.json_data = SESSION_SERVICE_DATA
        attr_error = HTTPError("https://test", 403, "Forbidden", {}, None)
        mgr_error = HTTPError("https://test", 500, "Internal Error", {}, None)
        idrac_mock.invoke_request.side_effect = [sessions_resp, svc_resp, attr_error, mgr_error]

        result = self._run_module(idrac_default_args)
        assert result['session_limits'] is None
        assert result['session_count'] == 1
        assert any("Unable to determine session limits" in w for w in result.get('warnings', []))


# --- Test Suite 9: Error Handling ---

class TestErrorHandling(FakeAnsibleModule):
    module = idrac_session_info

    @pytest.fixture
    def idrac_connection_mock(self, mocker):
        with patch(MODULE_PATH + '.iDRACRedfishAPI') as mock_class:
            mock_class.check_minimum_firmware_requirement = iDRACRedfishAPI.check_minimum_firmware_requirement
            mock_class.compare_firmware_version = iDRACRedfishAPI.compare_firmware_version
            yield mock_class

    def test_authentication_failure(self, idrac_default_args, idrac_connection_mock):
        """Test: Authentication failure returns descriptive error."""
        idrac_connection_mock.return_value.__enter__.side_effect = HTTPError(
            "https://192.168.0.1", 401, "Unauthorized", {}, None
        )
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result['failed'] is True
        assert "Authentication failed" in result['msg']

    def test_ssl_validation_error(self, idrac_default_args, idrac_connection_mock):
        """Test: SSL validation error."""
        idrac_connection_mock.return_value.__enter__.side_effect = SSLValidationError(
            "Certificate verify failed"
        )
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result['failed'] is True
        assert "SSL validation error" in result['msg']

    def test_connection_error(self, idrac_default_args, idrac_connection_mock):
        """Test: Connection error."""
        idrac_connection_mock.return_value.__enter__.side_effect = ConnectionError(
            "Connection refused"
        )
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result['failed'] is True
        assert "Connection error" in result['msg']

    def test_network_error(self, idrac_default_args, idrac_connection_mock):
        """Test: Network error."""
        idrac_connection_mock.return_value.__enter__.side_effect = URLError("timeout")
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result['failed'] is True
        assert "Network error" in result['msg']

    def test_negative_stale_threshold(self, idrac_default_args, idrac_connection_mock):
        """Test: Negative stale_threshold_minutes rejected."""
        idrac_default_args['stale_threshold_minutes'] = -1
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result['failed'] is True
        assert "positive integer" in result['msg']
