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
    CERT_VALIDATION_DISABLED_WARNING,
    TOKEN_NO_LOG_WARNING,
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
        module = self._make_module()
        warn_if_insecure_firmware_transfer(module, "http://example.com/fw.exe", "HTTPS")
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
        mock_ssl._create_unverified_context.return_value = mock_ctx
        mock_sock = MagicMock()
        mock_socket.create_connection.return_value.__enter__ = MagicMock(return_value=mock_sock)
        mock_socket.create_connection.return_value.__exit__ = MagicMock(return_value=False)
        mock_tls_sock = MagicMock()
        mock_tls_sock.getpeercert.return_value = fake_cert
        mock_ctx.wrap_socket.return_value.__enter__ = MagicMock(return_value=mock_tls_sock)
        mock_ctx.wrap_socket.return_value.__exit__ = MagicMock(return_value=False)

        verify_cert_fingerprint("example.com", 443, expected)

    @patch('ansible_collections.dellemc.openmanage.plugins.module_utils.utils.socket')
    @patch('ansible_collections.dellemc.openmanage.plugins.module_utils.utils.ssl')
    def test_mismatching_fingerprint(self, mock_ssl, mock_socket):
        fake_cert = b"fake certificate bytes"

        mock_ctx = MagicMock()
        mock_ssl._create_unverified_context.return_value = mock_ctx
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
        verify_local_image_checksum(module, "/tmp/fw.exe", None)
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
        with pytest.raises(AnsibleFailJSonException, match="Unsupported checksum"):
            verify_local_image_checksum(module, "/tmp/fw.exe",
                                        {"algorithm": "bogus", "value": "abc123"})

    def test_missing_value(self):
        module = self._make_module()
        with pytest.raises(AnsibleFailJSonException, match="value is required"):
            verify_local_image_checksum(module, "/tmp/fw.exe",
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
