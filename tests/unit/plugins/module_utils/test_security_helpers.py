# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Copyright (C) 2024-2026 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import hashlib
import os
import tempfile
import pytest
from unittest.mock import MagicMock, patch
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    warn_if_cert_validation_disabled,
    warn_if_token_return_without_no_log,
    warn_if_insecure_firmware_transfer,
    verify_cert_fingerprint,
    check_cert_fingerprint,
    verify_local_image_checksum,
    scrub_nested_secrets,
    warn_if_credential_from_env,
    secure_write_file,
    CERT_VALIDATION_DISABLED_WARNING,
    TOKEN_NO_LOG_WARNING,
    CREDENTIAL_FROM_ENV_WARNING,
    SECRET_PLACEHOLDER,
)
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import AnsibleFailJSonException


class TestWarnIfCertValidationDisabled:
    """Tests for warn_if_cert_validation_disabled including enforce_validate_certs."""

    def _make_module(self, validate_certs=True, enforce_validate_certs=False):
        module = MagicMock()
        module.params = {
            "validate_certs": validate_certs,
            "enforce_validate_certs": enforce_validate_certs,
        }

        def fail_func(msg, **kwargs):
            raise AnsibleFailJSonException(msg, **kwargs)
        module.fail_json.side_effect = fail_func
        return module

    def test_no_warning_when_validate_certs_true(self):
        module = self._make_module(validate_certs=True)
        warn_if_cert_validation_disabled(module)
        module.warn.assert_not_called()

    def test_warning_when_validate_certs_false(self):
        module = self._make_module(validate_certs=False)
        warn_if_cert_validation_disabled(module)
        module.warn.assert_called_once_with(CERT_VALIDATION_DISABLED_WARNING)

    def test_enforce_validate_certs_fails(self):
        module = self._make_module(validate_certs=False, enforce_validate_certs=True)
        with pytest.raises(AnsibleFailJSonException):
            warn_if_cert_validation_disabled(module)

    def test_enforce_validate_certs_no_fail_when_certs_valid(self):
        module = self._make_module(validate_certs=True, enforce_validate_certs=True)
        warn_if_cert_validation_disabled(module)
        module.fail_json.assert_not_called()

    def test_no_params(self):
        module = MagicMock(spec=[])
        warn_if_cert_validation_disabled(module)


class TestWarnIfTokenReturnWithoutNoLog:
    """Tests for warn_if_token_return_without_no_log."""

    def _make_module(self, no_log=False, enforce_no_log=False):
        module = MagicMock()
        module.no_log = no_log
        module.params = {"enforce_no_log": enforce_no_log}

        def fail_func(msg, **kwargs):
            raise AnsibleFailJSonException(msg, **kwargs)
        module.fail_json.side_effect = fail_func
        return module

    def test_warning_when_no_log_false(self):
        module = self._make_module(no_log=False)
        warn_if_token_return_without_no_log(module)
        module.warn.assert_called_once_with(TOKEN_NO_LOG_WARNING)

    def test_no_warning_when_no_log_true(self):
        module = self._make_module(no_log=True)
        warn_if_token_return_without_no_log(module)
        module.warn.assert_not_called()

    def test_enforce_no_log_fails(self):
        module = self._make_module(no_log=False, enforce_no_log=True)
        with pytest.raises(AnsibleFailJSonException):
            warn_if_token_return_without_no_log(module)

    def test_enforce_no_log_no_fail_when_no_log_true(self):
        module = self._make_module(no_log=True, enforce_no_log=True)
        warn_if_token_return_without_no_log(module)
        module.fail_json.assert_not_called()


class TestWarnIfInsecureFirmwareTransfer:
    """Tests for warn_if_insecure_firmware_transfer."""

    def _make_module(self):
        module = MagicMock()
        return module

    @pytest.mark.parametrize("protocol", ["HTTP", "FTP", "TFTP"])
    def test_warning_on_insecure_protocol(self, protocol):
        module = self._make_module()
        warn_if_insecure_firmware_transfer(module, "https://example.com/fw.exe", protocol)
        module.warn.assert_called_once()

    @pytest.mark.parametrize("protocol", ["HTTPS", "SFTP", "SCP", "CIFS"])
    def test_no_warning_on_secure_protocol(self, protocol):
        module = self._make_module()
        warn_if_insecure_firmware_transfer(module, "https://example.com/fw.exe", protocol)
        module.warn.assert_not_called()

    def test_warning_on_http_uri(self):
        # This http:// literal is test fixture data verifying that an insecure
        # scheme is correctly detected; it is never used to open a connection,
        # so it is not a clear-text-protocol usage (S5332).
        module = self._make_module()
        warn_if_insecure_firmware_transfer(module, "http://example.com/fw.exe", "HTTPS")  # NOSONAR
        module.warn.assert_called_once()

    def test_warning_on_uppercase_http_uri(self):
        # Scheme detection is case-insensitive (urlsplit + .lower()).
        module = self._make_module()
        warn_if_insecure_firmware_transfer(module, "HTTP://example.com/fw.exe", "HTTPS")  # NOSONAR
        module.warn.assert_called_once()

    def test_no_warning_on_local_path(self):
        module = self._make_module()
        warn_if_insecure_firmware_transfer(module, "/home/user/fw.exe", "HTTPS")
        module.warn.assert_not_called()


class TestVerifyCertFingerprint:
    """Tests for verify_cert_fingerprint."""

    @patch('ansible_collections.dellemc.openmanage.plugins.module_utils.utils.socket')
    @patch('ansible_collections.dellemc.openmanage.plugins.module_utils.utils.ssl')
    def test_matching_fingerprint(self, mock_ssl, mock_socket):
        fake_cert = b"fake certificate bytes"
        expected = hashlib.sha256(fake_cert).hexdigest()

        mock_ctx = MagicMock()
        mock_ssl.SSLContext.return_value = mock_ctx
        mock_sock = MagicMock()
        mock_socket.create_connection.return_value.__enter__ = MagicMock(return_value=mock_sock)
        mock_socket.create_connection.return_value.__exit__ = MagicMock(return_value=False)
        mock_tls_sock = MagicMock()
        mock_tls_sock.getpeercert.return_value = fake_cert
        mock_ctx.wrap_socket.return_value.__enter__ = MagicMock(return_value=mock_tls_sock)
        mock_ctx.wrap_socket.return_value.__exit__ = MagicMock(return_value=False)

        verify_cert_fingerprint("example.com", 443, expected)

        # The probe context must not perform hostname/chain validation -
        # that's the whole point of this fingerprint-pinning path.
        assert mock_ctx.check_hostname is False
        assert mock_ctx.verify_mode == mock_ssl.CERT_NONE

    @patch('ansible_collections.dellemc.openmanage.plugins.module_utils.utils.socket')
    @patch('ansible_collections.dellemc.openmanage.plugins.module_utils.utils.ssl')
    def test_mismatching_fingerprint(self, mock_ssl, mock_socket):
        fake_cert = b"fake certificate bytes"

        mock_ctx = MagicMock()
        mock_ssl.SSLContext.return_value = mock_ctx
        mock_sock = MagicMock()
        mock_socket.create_connection.return_value.__enter__ = MagicMock(return_value=mock_sock)
        mock_socket.create_connection.return_value.__exit__ = MagicMock(return_value=False)
        mock_tls_sock = MagicMock()
        mock_tls_sock.getpeercert.return_value = fake_cert
        mock_ctx.wrap_socket.return_value.__enter__ = MagicMock(return_value=mock_tls_sock)
        mock_ctx.wrap_socket.return_value.__exit__ = MagicMock(return_value=False)

        with pytest.raises(ValueError, match="fingerprint mismatch"):
            verify_cert_fingerprint("example.com", 443, "deadbeef" * 8)


class TestCheckCertFingerprint:
    """Tests for check_cert_fingerprint."""

    def _make_module(self, validate_certs=False, cert_fingerprint=None):
        module = MagicMock()
        module.params = {
            "validate_certs": validate_certs,
            "cert_fingerprint": cert_fingerprint,
        }

        def fail_func(msg, **kwargs):
            raise AnsibleFailJSonException(msg, **kwargs)
        module.fail_json.side_effect = fail_func
        return module

    def test_noop_when_validate_certs_true(self):
        module = self._make_module(validate_certs=True, cert_fingerprint="abc123")
        check_cert_fingerprint(module, "host", 443)
        module.fail_json.assert_not_called()

    def test_noop_when_no_fingerprint(self):
        module = self._make_module(validate_certs=False, cert_fingerprint=None)
        check_cert_fingerprint(module, "host", 443)
        module.fail_json.assert_not_called()

    @patch('ansible_collections.dellemc.openmanage.plugins.module_utils.utils.verify_cert_fingerprint')
    def test_calls_verify_when_conditions_met(self, mock_verify):
        module = self._make_module(validate_certs=False, cert_fingerprint="abc123")
        check_cert_fingerprint(module, "host", 443)
        mock_verify.assert_called_once_with("host", 443, "abc123")

    @patch('ansible_collections.dellemc.openmanage.plugins.module_utils.utils.verify_cert_fingerprint')
    def test_fails_on_mismatch(self, mock_verify):
        mock_verify.side_effect = ValueError("mismatch")
        module = self._make_module(validate_certs=False, cert_fingerprint="abc123")
        with pytest.raises(AnsibleFailJSonException):
            check_cert_fingerprint(module, "host", 443)


class TestVerifyLocalImageChecksum:
    """Tests for verify_local_image_checksum."""

    def _make_module(self):
        module = MagicMock()

        def fail_func(msg, **kwargs):
            raise AnsibleFailJSonException(msg, **kwargs)
        module.fail_json.side_effect = fail_func
        return module

    def test_noop_when_no_checksum(self):
        module = self._make_module()
        fake_path = os.path.join(tempfile.gettempdir(), "fw.exe")
        verify_local_image_checksum(module, fake_path, None)
        module.fail_json.assert_not_called()

    def test_matching_checksum(self):
        module = self._make_module()
        content = b"firmware image content"
        expected = hashlib.sha256(content).hexdigest()
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(content)
            f.flush()
            try:
                verify_local_image_checksum(module, f.name,
                                            {"algorithm": "sha256", "value": expected})
                module.fail_json.assert_not_called()
            finally:
                os.unlink(f.name)

    def test_mismatching_checksum(self):
        module = self._make_module()
        content = b"firmware image content"
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(content)
            f.flush()
            try:
                with pytest.raises(AnsibleFailJSonException, match="checksum mismatch"):
                    verify_local_image_checksum(module, f.name,
                                                {"algorithm": "sha256", "value": "deadbeef" * 8})
            finally:
                os.unlink(f.name)

    def test_unsupported_algorithm(self):
        module = self._make_module()
        fake_path = os.path.join(tempfile.gettempdir(), "fw.exe")
        with pytest.raises(AnsibleFailJSonException, match="Unsupported checksum"):
            verify_local_image_checksum(module, fake_path,
                                        {"algorithm": "bogus", "value": "abc123"})

    def test_missing_value(self):
        module = self._make_module()
        fake_path = os.path.join(tempfile.gettempdir(), "fw.exe")
        with pytest.raises(AnsibleFailJSonException, match="value is required"):
            verify_local_image_checksum(module, fake_path,
                                        {"algorithm": "sha256"})

    def test_file_not_found(self):
        module = self._make_module()
        with pytest.raises(AnsibleFailJSonException, match="Cannot read"):
            verify_local_image_checksum(module, "/nonexistent/fw.exe",
                                        {"algorithm": "sha256", "value": "abc123"})


class TestCheckCertFingerprintModuleCoverage:
    """Regression guard for the NET-01 Tier 2 coverage gap: modules that build a
    plain AnsibleModule() (rather than IdracAnsibleModule) and merge in
    idrac_auth_params directly must still call check_cert_fingerprint() themselves,
    since the plain AnsibleModule constructor never does this on their behalf.
    If a new module is added following this pattern without wiring the call in,
    this test will fail and flag the gap."""

    # Modules that build iDRACRedfishAPI/similar client from a plain AnsibleModule
    # (i.e. do NOT go through IdracAnsibleModule, whose __init__ already calls
    # check_cert_fingerprint on their behalf).
    PLAIN_MODULE_FILES = [
        "idrac_session_info.py",
        "idrac_network_info.py",
        "idrac_network_attributes_info.py",
        "idrac_lifecycle_controller_status_info.py",
        "idrac_lifecycle_controller_jobs.py",
        "idrac_lifecycle_controller_logs.py",
        "idrac_lifecycle_controller_job_status_info.py",
        "idrac_firmware_info.py",
        "idrac_bios_registry_info.py",
        "idrac_firmware.py",
        "idrac_bios.py",
    ]

    def _modules_dir(self):
        import ansible_collections.dellemc.openmanage.plugins.modules as modules_pkg
        return os.path.dirname(modules_pkg.__file__)

    @pytest.mark.parametrize("filename", PLAIN_MODULE_FILES)
    def test_module_wires_in_check_cert_fingerprint(self, filename):
        module_path = os.path.join(self._modules_dir(), filename)
        with open(module_path, "r", encoding="utf-8") as f:
            source = f.read()
        assert "check_cert_fingerprint" in source, (
            "{0} merges idrac_auth_params into a plain AnsibleModule but does not "
            "call check_cert_fingerprint(); users setting cert_fingerprint on this "
            "module would get no MITM verification.".format(filename))


class TestScrubNestedSecrets:
    """Tests for EE-02: scrub_nested_secrets recursively masks known-sensitive
    keys inside free-form dict/list module parameters before they can be
    echoed back in exit_json()/fail_json() output."""

    def test_top_level_password_scrubbed(self):
        data = {"username": "admin", "password": "supersecret"}
        result = scrub_nested_secrets(data)
        assert result["password"] == SECRET_PLACEHOLDER
        assert result["username"] == "admin"

    def test_nested_password_scrubbed_regardless_of_depth(self):
        data = {
            "NetworkBootIsoModel": {
                "ShareDetail": {"Password": "supersecret", "UserName": "admin"}
            }
        }
        result = scrub_nested_secrets(data)
        assert result["NetworkBootIsoModel"]["ShareDetail"]["Password"] == SECRET_PLACEHOLDER
        assert result["NetworkBootIsoModel"]["ShareDetail"]["UserName"] == "admin"

    def test_secrets_inside_list_of_dicts_scrubbed(self):
        data = {"credentials": [{"token": "abc123"}, {"token": "def456"}]}
        result = scrub_nested_secrets(data)
        assert result["credentials"][0]["token"] == SECRET_PLACEHOLDER
        assert result["credentials"][1]["token"] == SECRET_PLACEHOLDER

    def test_non_dict_input_returned_unchanged(self):
        assert scrub_nested_secrets(None) is None
        assert scrub_nested_secrets("a string") == "a string"

    def test_non_string_secret_value_left_untouched(self):
        # Guard against crashing/mangling if a "password" key ever holds
        # something other than a string (e.g. None from an optional field).
        data = {"password": None}
        result = scrub_nested_secrets(data)
        assert result["password"] is None

    def test_custom_sensitive_keys_and_placeholder(self):
        data = {"my_secret_field": "hunter2"}
        result = scrub_nested_secrets(data, sensitive_keys={"my_secret_field"}, placeholder="***")
        assert result["my_secret_field"] == "***"


class TestWarnIfCredentialFromEnv:
    """Tests for EE-03: warn_if_credential_from_env warns only when the
    relevant environment variable is actually set (i.e. env_fallback was
    used to source a credential for this task)."""

    def _make_module(self):
        module = MagicMock()
        return module

    def test_no_warning_when_env_vars_unset(self, monkeypatch):
        monkeypatch.delenv("OME_USERNAME", raising=False)
        monkeypatch.delenv("OME_PASSWORD", raising=False)
        module = self._make_module()
        warn_if_credential_from_env(module, ["OME_USERNAME", "OME_PASSWORD"])
        module.warn.assert_not_called()

    def test_warning_when_one_env_var_set(self, monkeypatch):
        monkeypatch.setenv("OME_PASSWORD", "supersecret")
        monkeypatch.delenv("OME_USERNAME", raising=False)
        module = self._make_module()
        warn_if_credential_from_env(module, ["OME_USERNAME", "OME_PASSWORD"])
        module.warn.assert_called_once_with(CREDENTIAL_FROM_ENV_WARNING)

    def test_no_warning_for_unrelated_env_vars(self, monkeypatch):
        monkeypatch.setenv("SOME_UNRELATED_VAR", "value")
        module = self._make_module()
        warn_if_credential_from_env(module, ["OME_USERNAME", "OME_PASSWORD"])
        module.warn.assert_not_called()


class TestSecureWriteFile:
    """Tests for FS-01: secure_write_file writes via a temp file, chmods it to
    0o600, then atomically renames it into place - regardless of process umask."""

    def test_writes_content_and_sets_restrictive_permissions(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            export_path = os.path.join(tmp_dir, "export.txt")
            old_umask = os.umask(0o022)
            try:
                secure_write_file(export_path, lambda f: f.write("hello world"))
            finally:
                os.umask(old_umask)
            assert os.path.exists(export_path)
            assert not os.path.exists(export_path + ".tmp")
            with open(export_path, "r") as f:
                assert f.read() == "hello world"
            mode = os.stat(export_path).st_mode & 0o777
            assert mode == 0o600

    def test_binary_write(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            export_path = os.path.join(tmp_dir, "export.bin")
            secure_write_file(export_path, lambda f: f.write(b"\x00\x01\x02"), binary=True)
            with open(export_path, "rb") as f:
                assert f.read() == b"\x00\x01\x02"

    def test_temp_file_cleaned_up_on_write_failure(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            export_path = os.path.join(tmp_dir, "export.txt")

            def failing_write(f):
                f.write("partial")
                raise ValueError("simulated failure")

            with pytest.raises(ValueError):
                secure_write_file(export_path, failing_write)
            assert not os.path.exists(export_path)
            assert not os.path.exists(export_path + ".tmp")


class TestOdataFilterEscapeCoverage:
    """Regression guard for INJ-01: modules that build an OData $filter clause
    by interpolating a user-supplied value into a single-quoted string literal
    must escape it via _escape_odata_string(), or a value containing a single
    quote can widen/manipulate the query. If a new unescaped call site is
    introduced, this test will fail and flag the gap."""

    FILTER_BUILDING_MODULES = [
        "ome_groups.py",
        "ome_device_group.py",
        "ome_template_network_vlan_info.py",
        "ome_template_network_vlan.py",
        "ome_template_identity_pool.py",
        "ome_configuration_compliance_baseline.py",
        "ome_device_mgmt_network.py",
        "ome_devices.py",
        "ome_alert_policies.py",
    ]

    def _modules_dir(self):
        import ansible_collections.dellemc.openmanage.plugins.modules as modules_pkg
        return os.path.dirname(modules_pkg.__file__)

    @pytest.mark.parametrize("filename", FILTER_BUILDING_MODULES)
    def test_module_imports_escape_helper(self, filename):
        module_path = os.path.join(self._modules_dir(), filename)
        with open(module_path, "r", encoding="utf-8") as f:
            source = f.read()
        assert "_escape_odata_string" in source, (
            "{0} builds an OData $filter clause with a quoted string value but "
            "does not import/use _escape_odata_string(); a value containing a "
            "single quote could manipulate the query.".format(filename))
