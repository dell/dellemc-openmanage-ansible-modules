# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.1
# Copyright (C) 2024-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

from datetime import datetime, timedelta, timezone
from io import StringIO
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

import pytest
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import (
    iDRACRedfishAPI,
)
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_session_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import (
    FakeAnsibleModule,
)

MODULE_PATH = "ansible_collections.dellemc.openmanage.plugins.modules.idrac_session_info"

# --- Fixtures: shared test data ---

IDRAC9_SESSION_DATA = [
    {
        "Id": "1",
        "UserName": "root",
        "ClientOriginIPAddress": "192.168.1.10",
        "SessionType": "Redfish",
        "CreatedTime": (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat(),
        "Description": "User Session",
        "Name": "User Session 1",
    },
    {
        "Id": "2",
        "UserName": "admin",
        "ClientOriginIPAddress": "192.168.1.20",
        "SessionType": "IPMI",
        "CreatedTime": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
        "Description": "User Session",
        "Name": "User Session 2",
    },
]

IDRAC10_SESSION_DATA = [
    {
        "Id": "1",
        "UserName": "root",
        "ClientOriginIPAddress": "10.0.0.1",
        "SessionType": "Redfish",
        "CreatedTime": (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat(),
        "Description": "User Session",
        "Name": "User Session 1",
    },
]

SESSION_SERVICE_DATA = {
    "SessionTimeout": 1800,
    "ServiceEnabled": True,
}

IDRAC_ATTRIBUTES_DATA = {
    "Attributes": {
        "WebServer.1.MaxSessions": 8,
    }
}

MANAGER_DATA = {
    "Links": {
        "Sessions": {
            "@odata.id": "/redfish/v1/SessionService/Sessions"
        }
    }
}


class TestIdracSessionInfo(FakeAnsibleModule):
    module = idrac_session_info

    @pytest.fixture
    def idrac_default_args(self):
        return {
            "idrac_ip": "192.168.0.1",
            "idrac_user": "admin",
            "idrac_password": "password",
            "idrac_port": 443,
            "validate_certs": False,
            "ca_path": None,
            "timeout": 30,
        }

    @pytest.fixture
    def idrac_mock(self):
        idrac_obj = MagicMock()
        idrac_obj.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
        return idrac_obj

    @pytest.fixture
    def idrac_connection_mock(self, mocker, idrac_mock):
        with patch(MODULE_PATH + ".iDRACRedfishAPI") as mock_class:
            mock_class.return_value.__enter__.return_value = idrac_mock
            mock_class.return_value.__exit__.return_value = False
            mock_class.check_minimum_firmware_requirement = (
                iDRACRedfishAPI.check_minimum_firmware_requirement
            )
            mock_class.compare_firmware_version = (
                iDRACRedfishAPI.compare_firmware_version
            )
            yield mock_class

    # --- Test Suite: Session Query (AC-001) ---

    def test_query_all_sessions_idrac9(
        self, idrac_default_args, idrac_mock, idrac_connection_mock
    ):
        """Test: Query all active sessions on iDRAC9 returns session list."""
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
        assert result["changed"] is False
        assert len(result["sessions"]) == 2
        assert result["sessions"][0]["id"] == "1"
        assert result["sessions"][0]["username"] == "root"
        assert result["sessions"][0]["session_type"] == "Redfish"
        assert "session_age_minutes" in result["sessions"][0]

    def test_query_all_sessions_idrac10(
        self, idrac_default_args, idrac_mock, idrac_connection_mock
    ):
        """Test: Query all sessions on iDRAC10."""
        idrac_mock.get_server_generation = (17, "1.20.50.50", "iDRAC 10")
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
        assert result["changed"] is False
        assert len(result["sessions"]) == 1

    def test_no_active_sessions(
        self, idrac_default_args, idrac_mock, idrac_connection_mock
    ):
        """Test: No active sessions returns empty list."""
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
        assert result["sessions"] == []
        assert result["session_count"] == 0

    def test_missing_properties_degradation(
        self, idrac_default_args, idrac_mock, idrac_connection_mock
    ):
        """Test: Missing session properties degrade gracefully to None."""
        sparse_session = {
            "Id": "1",
            "UserName": "root",
        }
        sessions_resp = MagicMock()
        sessions_resp.status_code = 200
        sessions_resp.json_data = {"Members": [sparse_session]}
        svc_resp = MagicMock()
        svc_resp.status_code = 200
        svc_resp.json_data = SESSION_SERVICE_DATA
        attr_resp = MagicMock()
        attr_resp.status_code = 200
        attr_resp.json_data = IDRAC_ATTRIBUTES_DATA
        idrac_mock.invoke_request.side_effect = [sessions_resp, svc_resp, attr_resp]

        result = self._run_module(idrac_default_args)
        session = result["sessions"][0]
        assert session["client_origin_ip"] is None
        assert session["session_type"] is None

    # --- Test Suite: Session Limits (AC-002) ---

    def test_session_limits_from_attributes(
        self, idrac_default_args, idrac_mock, idrac_connection_mock
    ):
        """Test: Session limits retrieved from iDRAC Attributes."""
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
        assert result["session_service"]["session_timeout"] == 1800
        assert result["session_service"]["service_enabled"] is True
        assert result["session_limits"]["max_sessions"] == 8
        assert "utilization_percent" in result["session_limits"]

    def test_session_limits_attributes_403_fallback(
        self, idrac_default_args, idrac_mock, idrac_connection_mock
    ):
        """Test: 403 on Attributes endpoint falls back to Manager endpoint."""
        sessions_resp = MagicMock()
        sessions_resp.status_code = 200
        sessions_resp.json_data = {"Members": IDRAC10_SESSION_DATA}
        svc_resp = MagicMock()
        svc_resp.status_code = 200
        svc_resp.json_data = SESSION_SERVICE_DATA
        attr_error = HTTPError(
            "https://192.168.0.1", 403, "Forbidden", {}, StringIO("{}")
        )
        mgr_resp = MagicMock()
        mgr_resp.status_code = 200
        mgr_resp.json_data = {
            "Links": {"Sessions": {"@odata.id": "/redfish/v1/SessionService/Sessions"}},
            "Oem": {"Dell": {"MaxSessions": 4}},
        }
        idrac_mock.invoke_request.side_effect = [
            sessions_resp, svc_resp, attr_error, mgr_resp
        ]

        result = self._run_module(idrac_default_args)
        assert result["session_limits"]["max_sessions"] == 4

    # --- Test Suite: Filtering (AC-005) ---

    def test_filter_by_session_type(
        self, idrac_default_args, idrac_mock, idrac_connection_mock
    ):
        """Test: Filter sessions by session_type."""
        idrac_default_args["session_type"] = "Redfish"
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
        assert len(result["sessions"]) == 1
        assert result["sessions"][0]["session_type"] == "Redfish"

    def test_filter_by_username(
        self, idrac_default_args, idrac_mock, idrac_connection_mock
    ):
        """Test: Filter sessions by username substring."""
        idrac_default_args["username_filter"] = "adm"
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
        assert len(result["sessions"]) == 1
        assert result["sessions"][0]["username"] == "admin"

    def test_stale_sessions_flagged(
        self, idrac_default_args, idrac_mock, idrac_connection_mock
    ):
        """Test: Stale sessions detected with stale_threshold_minutes."""
        idrac_default_args["stale_threshold_minutes"] = 60
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
        stale_sessions = [s for s in result["sessions"] if s.get("is_stale")]
        non_stale = [s for s in result["sessions"] if not s.get("is_stale")]
        assert len(stale_sessions) == 1
        assert stale_sessions[0]["username"] == "admin"
        assert len(non_stale) == 1

    def test_combined_filters(
        self, idrac_default_args, idrac_mock, idrac_connection_mock
    ):
        """Test: Combined session_type + username filter."""
        idrac_default_args["session_type"] = "Redfish"
        idrac_default_args["username_filter"] = "root"
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
        assert len(result["sessions"]) == 1
        assert result["sessions"][0]["username"] == "root"
        assert result["sessions"][0]["session_type"] == "Redfish"

    # --- Test Suite: Error Handling (AC-006) ---

    def test_authentication_failure(
        self, idrac_default_args, idrac_connection_mock
    ):
        """Test: Authentication failure returns descriptive error."""
        idrac_connection_mock.return_value.__enter__.side_effect = HTTPError(
            "https://192.168.0.1", 401, "Unauthorized", {}, StringIO("{}")
        )
        result = self._run_module(idrac_default_args)
        assert result["failed"] is True

    def test_ssl_validation_error(
        self, idrac_default_args, idrac_connection_mock
    ):
        """Test: SSL validation error."""
        idrac_connection_mock.return_value.__enter__.side_effect = (
            SSLValidationError("Certificate verify failed")
        )
        result = self._run_module(idrac_default_args)
        assert result["failed"] is True

    def test_connection_error(
        self, idrac_default_args, idrac_connection_mock
    ):
        """Test: Connection error."""
        idrac_connection_mock.return_value.__enter__.side_effect = ConnectionError(
            "Connection refused"
        )
        result = self._run_module(idrac_default_args)
        assert result["failed"] is True

    def test_url_error(
        self, idrac_default_args, idrac_connection_mock
    ):
        """Test: URL error."""
        idrac_connection_mock.return_value.__enter__.side_effect = URLError("timeout")
        result = self._run_module(idrac_default_args)
        assert result["failed"] is True

    def test_negative_stale_threshold(
        self, idrac_default_args, idrac_mock, idrac_connection_mock
    ):
        """Test: Negative stale_threshold_minutes rejected."""
        idrac_default_args["stale_threshold_minutes"] = -1
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
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result["failed"] is True

    # --- Test Suite: Security ---

    def test_credentials_not_in_output(
        self, idrac_default_args, idrac_mock, idrac_connection_mock
    ):
        """Test: Credentials not exposed in successful output."""
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
        result_str = str(result)
        assert "password" not in result_str.lower() or "idrac_password" not in result_str
        assert "x_auth_token" not in result_str

    def test_response_only_allowed_fields(
        self, idrac_default_args, idrac_mock, idrac_connection_mock
    ):
        """Test: Only allow-listed fields in session response."""
        raw_session = {
            "Id": "1",
            "UserName": "root",
            "ClientOriginIPAddress": "1.1.1.1",
            "SessionType": "Redfish",
            "CreatedTime": (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat(),
            "Description": "User Session",
            "Name": "User Session",
            "@odata.id": "/redfish/v1/SessionService/Sessions/1",
            "@odata.type": "#Session.v1_3_0.Session",
            "InternalToken": "secret-token-value",
        }
        sessions_resp = MagicMock()
        sessions_resp.status_code = 200
        sessions_resp.json_data = {"Members": [raw_session]}
        svc_resp = MagicMock()
        svc_resp.status_code = 200
        svc_resp.json_data = SESSION_SERVICE_DATA
        attr_resp = MagicMock()
        attr_resp.status_code = 200
        attr_resp.json_data = IDRAC_ATTRIBUTES_DATA
        idrac_mock.invoke_request.side_effect = [sessions_resp, svc_resp, attr_resp]

        result = self._run_module(idrac_default_args)
        session = result["sessions"][0]
        assert "@odata.id" not in session
        assert "@odata.type" not in session
        assert "InternalToken" not in session
        assert "secret-token-value" not in str(session)

    # --- Test Suite: Check Mode ---

    def test_check_mode(
        self, idrac_default_args, idrac_mock, idrac_connection_mock
    ):
        """Test: Check mode returns no changes (read-only module)."""
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

        result = self._run_module(idrac_default_args, check_mode=True)
        assert result["changed"] is False
