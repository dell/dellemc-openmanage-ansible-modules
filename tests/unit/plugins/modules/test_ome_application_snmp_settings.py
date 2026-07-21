# -*- coding: utf-8 -*-
# Dell OpenManage Ansible Modules
# Version 9.12.4
# Copyright (C) 2025-2026 Dell Inc. or its subsidiaries. All Rights Reserved.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
from io import StringIO

import pytest
from unittest.mock import MagicMock, patch
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.modules import ome_application_snmp_settings
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

SUCCESS_MSG = "Successfully updated the SNMP settings."
NO_CHANGES = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_application_snmp_settings.'


@pytest.fixture
def ome_connection_mock_for_snmp(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


SAMPLE_SNMP_GET_RESPONSE = {
    "Port": 162,
    "CommunityString": "currentSecret",
}


class TestOmeApplicationSnmpSettings(FakeAnsibleModule):
    module = ome_application_snmp_settings

    # ========================================================================
    # Task 2: Read operation (GET) tests
    # ========================================================================

    def test_fetch_snmp_settings_success(self, ome_connection_mock_for_snmp, ome_response_mock):
        """Test successful GET of SNMP settings."""
        ome_response_mock.json_data = SAMPLE_SNMP_GET_RESPONSE
        result = self.module.fetch_snmp_settings(ome_connection_mock_for_snmp)
        assert result.get("Port") == 162
        assert result.get("CommunityString") == "currentSecret"
        ome_connection_mock_for_snmp.invoke_request.assert_called_once_with(
            "GET", "ApplicationService/IncomingAlertConfiguration")

    def test_fetch_snmp_settings_unreachable(self, ome_connection_mock_for_snmp):
        """Test GET when OME is unreachable raises URLError."""
        ome_connection_mock_for_snmp.invoke_request.side_effect = URLError("Connection refused")
        with pytest.raises(URLError):
            self.module.fetch_snmp_settings(ome_connection_mock_for_snmp)

    # ========================================================================
    # Task 3: Write operation (POST) with idempotency tests
    # ========================================================================

    def test_update_payload_builds_correct_dict(self):
        """Test update_payload builds desired state from module params."""
        f_module = self.get_module_mock(
            params={"community_string": "newSecret", "snmp_port": 1162})
        curr = {"Port": 162, "CommunityString": "oldSecret"}
        result = self.module.update_payload(f_module, curr)
        assert result == {"Port": 1162, "CommunityString": "newSecret"}

    def test_update_payload_uses_default_port(self):
        """Test update_payload uses the default port (162) from argspec."""
        f_module = self.get_module_mock(
            params={"community_string": "newSecret", "snmp_port": 162})
        curr = {"Port": 9999, "CommunityString": "oldSecret"}
        result = self.module.update_payload(f_module, curr)
        assert result["Port"] == 162

    def test_diff_payload_detects_port_change(self):
        """Test _diff_payload returns True when port changes."""
        curr = {"Port": 162}
        desired = {"Port": 1162, "CommunityString": "x"}
        assert self.module._diff_payload(curr, desired) is True

    def test_diff_payload_same_port_still_true(self):
        """Test _diff_payload returns True even when port is same
        (community string cannot be compared since GET masks it)."""
        curr = {"Port": 162}
        desired = {"Port": 162, "CommunityString": "x"}
        assert self.module._diff_payload(curr, desired) is True

    def test_update_snmp_settings_calls_post(self, ome_connection_mock_for_snmp, ome_response_mock):
        """Test update_snmp_settings calls POST with correct URL."""
        payload = {"Port": 162, "CommunityString": "newSecret"}
        ome_response_mock.json_data = payload
        self.module.update_snmp_settings(ome_connection_mock_for_snmp, payload)
        ome_connection_mock_for_snmp.invoke_request.assert_called_once_with(
            "POST", "ApplicationService/Actions/ApplicationService.UpdateSNMPConfiguration",
            data=payload)

    def test_module_idempotent_no_changes(self, mocker, ome_connection_mock_for_snmp,
                                          ome_response_mock, ome_default_args):
        """Test end-to-end idempotent flow — no changes needed."""
        ome_response_mock.json_data = SAMPLE_SNMP_GET_RESPONSE
        ome_default_args.update({"community_string": "testSecret", "snmp_port": 162})
        mocker.patch(MODULE_PATH + 'fetch_snmp_settings',
                     return_value=SAMPLE_SNMP_GET_RESPONSE)
        mocker.patch(MODULE_PATH + '_diff_payload', return_value=False)
        mocker.patch(MODULE_PATH + 'validate_params')
        mocker.patch(MODULE_PATH + 'warn_weak_community_string')
        result = self._run_module(ome_default_args)
        assert result["msg"] == NO_CHANGES

    # ========================================================================
    # Task 4: Input validation tests
    # ========================================================================

    def test_validate_community_string_too_long(self):
        """Test validation rejects community_string > 32 chars."""
        f_module = self.get_module_mock(
            params={"community_string": "a" * 33, "snmp_port": 162})
        with pytest.raises(Exception) as exc_info:
            self.module.validate_params(f_module)
        f_module.fail_json.assert_called_once()
        call_args = f_module.fail_json.call_args
        assert "must not exceed 32 characters" in call_args[1]["msg"]

    def test_validate_community_string_empty(self):
        """Test validation rejects empty community_string."""
        f_module = self.get_module_mock(
            params={"community_string": "", "snmp_port": 162})
        with pytest.raises(Exception) as exc_info:
            self.module.validate_params(f_module)
        f_module.fail_json.assert_called_once()
        assert "must not be empty" in f_module.fail_json.call_args[1]["msg"]

    def test_validate_snmp_port_zero(self):
        """Test validation rejects snmp_port=0."""
        f_module = self.get_module_mock(
            params={"community_string": "valid", "snmp_port": 0})
        with pytest.raises(Exception) as exc_info:
            self.module.validate_params(f_module)
        f_module.fail_json.assert_called_once()
        assert "between 1 and 65535" in f_module.fail_json.call_args[1]["msg"]

    def test_validate_snmp_port_too_high(self):
        """Test validation rejects snmp_port=65536."""
        f_module = self.get_module_mock(
            params={"community_string": "valid", "snmp_port": 65536})
        with pytest.raises(Exception) as exc_info:
            self.module.validate_params(f_module)
        f_module.fail_json.assert_called_once()
        assert "between 1 and 65535" in f_module.fail_json.call_args[1]["msg"]

    def test_validate_params_valid(self):
        """Test validation passes for valid params — no exception."""
        f_module = self.get_module_mock(
            params={"community_string": "validString", "snmp_port": 162})
        self.module.validate_params(f_module)
        f_module.fail_json.assert_not_called()

    # ========================================================================
    # Task 5: check_mode and diff_mode tests
    # ========================================================================

    def test_check_mode_reports_change(self, mocker, ome_connection_mock_for_snmp,
                                       ome_response_mock, ome_default_args):
        """Test check_mode reports change without making API POST."""
        ome_default_args.update({"community_string": "newSecret", "snmp_port": 162})
        mocker.patch(MODULE_PATH + 'fetch_snmp_settings',
                     return_value=SAMPLE_SNMP_GET_RESPONSE)
        mocker.patch(MODULE_PATH + '_diff_payload', return_value=True)
        mocker.patch(MODULE_PATH + 'validate_params')
        mocker.patch(MODULE_PATH + 'warn_weak_community_string')
        result = self._run_module(ome_default_args, check_mode=True)
        assert result["changed"] is True
        assert result["msg"] == CHANGES_FOUND

    def test_check_mode_reports_no_change(self, mocker, ome_connection_mock_for_snmp,
                                          ome_response_mock, ome_default_args):
        """Test check_mode reports no change when state matches."""
        ome_default_args.update({"community_string": "currentSecret", "snmp_port": 162})
        mocker.patch(MODULE_PATH + 'fetch_snmp_settings',
                     return_value=SAMPLE_SNMP_GET_RESPONSE)
        mocker.patch(MODULE_PATH + '_diff_payload', return_value=False)
        mocker.patch(MODULE_PATH + 'validate_params')
        mocker.patch(MODULE_PATH + 'warn_weak_community_string')
        result = self._run_module(ome_default_args, check_mode=True)
        assert result["msg"] == NO_CHANGES

    def test_diff_mode_masks_community_string(self, mocker, ome_connection_mock_for_snmp,
                                               ome_response_mock, ome_default_args):
        """Test diff_mode output masks community_string as '***' in before and after."""
        ome_default_args.update({
            "community_string": "newSecret", "snmp_port": 1162,
            "_ansible_diff": True, "_ansible_check_mode": True,
        })
        mocker.patch(MODULE_PATH + 'fetch_snmp_settings',
                     return_value=SAMPLE_SNMP_GET_RESPONSE)
        mocker.patch(MODULE_PATH + '_diff_payload', return_value=True)
        mocker.patch(MODULE_PATH + 'validate_params')
        mocker.patch(MODULE_PATH + 'warn_weak_community_string')
        result = self._run_module(ome_default_args, check_mode=True)
        assert result.get("diff") is not None
        assert result["diff"]["before"]["CommunityString"] == "***"
        assert result["diff"]["after"]["CommunityString"] == "***"

    # ========================================================================
    # Task 6: Weak-default warning and error handling tests
    # ========================================================================

    def test_warn_weak_community_string_public(self):
        """Test module.warn() is called for community_string 'public'."""
        f_module = self.get_module_mock(params={"community_string": "public"})
        f_module.warn = MagicMock()
        self.module.warn_weak_community_string(f_module)
        f_module.warn.assert_called_once()
        assert "known-weak default" in f_module.warn.call_args[0][0]

    def test_warn_weak_community_string_private(self):
        """Test module.warn() is called for community_string 'private'."""
        f_module = self.get_module_mock(params={"community_string": "private"})
        f_module.warn = MagicMock()
        self.module.warn_weak_community_string(f_module)
        f_module.warn.assert_called_once()
        assert "known-weak default" in f_module.warn.call_args[0][0]

    def test_warn_weak_community_string_case_insensitive(self):
        """Test weak-default warning is case-insensitive (e.g., 'PUBLIC')."""
        f_module = self.get_module_mock(params={"community_string": "PUBLIC"})
        f_module.warn = MagicMock()
        self.module.warn_weak_community_string(f_module)
        f_module.warn.assert_called_once()

    def test_warn_no_warning_for_strong_string(self):
        """Test no warning for non-weak community strings."""
        f_module = self.get_module_mock(params={"community_string": "strongSecret123"})
        f_module.warn = MagicMock()
        self.module.warn_weak_community_string(f_module)
        f_module.warn.assert_not_called()

    @pytest.mark.parametrize("exc,exc_args,check_key", [
        (HTTPError, ("https://host/api", 400, "Bad Request",
                     {}, StringIO(json.dumps({"error": {"code": "Base.1.0.GeneralError",
                     "message": "Error"}}))), "error_info"),
        (URLError, ("Connection refused",), "unreachable"),
    ])
    def test_error_handling(self, mocker, exc, exc_args, check_key,
                            ome_connection_mock_for_snmp, ome_response_mock, ome_default_args):
        """Test HTTPError and URLError are handled gracefully."""
        ome_default_args.update({"community_string": "testSecret", "snmp_port": 162})
        mocker.patch(MODULE_PATH + 'validate_params')
        mocker.patch(MODULE_PATH + 'warn_weak_community_string')
        mocker.patch(MODULE_PATH + 'fetch_snmp_settings', side_effect=exc(*exc_args))
        result = self._run_module_with_fail_json(ome_default_args)
        assert result.get("failed") is True

    def test_connection_error_handling(self, mocker, ome_connection_mock_for_snmp,
                                       ome_response_mock, ome_default_args):
        """Test ConnectionError is handled gracefully."""
        ome_default_args.update({"community_string": "testSecret", "snmp_port": 162})
        mocker.patch(MODULE_PATH + 'validate_params')
        mocker.patch(MODULE_PATH + 'warn_weak_community_string')
        mocker.patch(MODULE_PATH + 'fetch_snmp_settings',
                     side_effect=ConnectionError("Connection error"))
        result = self._run_module_with_fail_json(ome_default_args)
        assert result.get("failed") is True

    def test_sanitize_error_response_strips_extended_info(self):
        """Test error sanitization strips @Message.ExtendedInfo."""
        err_data = {
            "error": {
                "code": "Base.1.0.GeneralError",
                "message": "A general error has occurred.",
                "@Message.ExtendedInfo": [{"MessageId": "CAPP1106", "Message": "Details"}]
            }
        }
        result = self.module.sanitize_error_response(err_data)
        assert "@Message.ExtendedInfo" not in result.get("error", {})
        assert result["error"]["code"] == "Base.1.0.GeneralError"
        assert result["error"]["message"] == "A general error has occurred."

    # ========================================================================
    # Task 7: Main flow end-to-end tests
    # ========================================================================

    def test_main_flow_successful_update(self, mocker, ome_connection_mock_for_snmp,
                                         ome_response_mock, ome_default_args):
        """Test end-to-end successful update flow."""
        ome_default_args.update({"community_string": "newSecret", "snmp_port": 162})
        ome_response_mock.json_data = {"Port": 162, "CommunityString": "newSecret"}
        mocker.patch(MODULE_PATH + 'fetch_snmp_settings',
                     return_value=SAMPLE_SNMP_GET_RESPONSE)
        mocker.patch(MODULE_PATH + '_diff_payload', return_value=True)
        mocker.patch(MODULE_PATH + 'validate_params')
        mocker.patch(MODULE_PATH + 'warn_weak_community_string')
        result = self._run_module(ome_default_args)
        assert result["msg"] == SUCCESS_MSG
        assert result["changed"] is True
        assert result["snmp_details"]["CommunityString"] == "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"

    def test_main_flow_community_string_masked_in_return(self, mocker,
                                                          ome_connection_mock_for_snmp,
                                                          ome_response_mock, ome_default_args):
        """Test community string is always masked in return data."""
        ome_default_args.update({"community_string": "sensitiveValue", "snmp_port": 162})
        ome_response_mock.json_data = {"Port": 162, "CommunityString": "sensitiveValue"}
        mocker.patch(MODULE_PATH + 'fetch_snmp_settings',
                     return_value=SAMPLE_SNMP_GET_RESPONSE)
        mocker.patch(MODULE_PATH + '_diff_payload', return_value=True)
        mocker.patch(MODULE_PATH + 'validate_params')
        mocker.patch(MODULE_PATH + 'warn_weak_community_string')
        result = self._run_module(ome_default_args)
        assert "sensitiveValue" not in str(result)
        assert result["snmp_details"]["CommunityString"] == "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"

    def test_mask_snmp_details(self):
        """Test mask_snmp_details replaces CommunityString."""
        details = {"Port": 162, "CommunityString": "secret123"}
        result = self.module.mask_snmp_details(details)
        assert result["CommunityString"] == "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"
        assert result["Port"] == 162

    def test_build_diff_masks_community_string(self):
        """Test build_diff masks community string in both before and after."""
        curr = {"Port": 162, "CommunityString": "oldSecret"}
        desired = {"Port": 1162, "CommunityString": "newSecret"}
        result = self.module.build_diff(curr, desired)
        assert result["before"]["CommunityString"] == "***"
        assert result["after"]["CommunityString"] == "***"
        assert result["before"]["Port"] == 162
        assert result["after"]["Port"] == 1162

    def test_community_string_no_log(self):
        """Test community_string_no_log masks params."""
        f_module = self.get_module_mock(
            params={"community_string": "secret123", "snmp_port": 162})
        self.module.community_string_no_log(f_module)
        assert f_module.params["community_string"] == "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"
