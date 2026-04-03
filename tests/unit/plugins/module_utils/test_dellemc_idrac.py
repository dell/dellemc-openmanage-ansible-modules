# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.1
# Copyright (C) 2025 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from unittest.mock import MagicMock, patch

MODULE_UTIL_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac.'


class TestIDRACConnection:
    """Tests for the iDRACConnection context manager class."""

    def _get_default_params(self):
        return {
            "idrac_ip": "192.168.1.100",
            "idrac_user": "admin",
            "idrac_password": "password",
            "idrac_port": 443,
            "validate_certs": True,
            "ca_path": None,
            "timeout": 30,
        }

    def test_init_success(self):
        from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection
        params = self._get_default_params()
        conn = iDRACConnection(params)
        assert conn.idrac_ip == "192.168.1.100"
        assert conn.idrac_user == "admin"
        assert conn.idrac_pwd == "password"
        assert conn.idrac_port == 443
        assert conn.validate_certs is True
        assert conn.ca_path is None
        assert conn.timeout == 30
        assert conn.redfish_api is None

    def test_init_missing_ip_raises(self):
        from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection
        params = self._get_default_params()
        params["idrac_user"] = None
        params["idrac_password"] = None
        with pytest.raises((ValueError, TypeError)):
            iDRACConnection(params)

    def test_init_missing_user_raises(self):
        from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection
        params = self._get_default_params()
        params["idrac_user"] = ""
        with pytest.raises(ValueError, match="hostname, username and password required"):
            iDRACConnection(params)

    def test_init_missing_password_raises(self):
        from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection
        params = self._get_default_params()
        params["idrac_password"] = ""
        with pytest.raises(ValueError, match="hostname, username and password required"):
            iDRACConnection(params)

    @patch(MODULE_UTIL_PATH + 'iDRACRedfishAPI')
    def test_enter_creates_redfish_api(self, mock_redfish_cls):
        from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection
        mock_api = MagicMock()
        mock_redfish_cls.return_value = mock_api
        params = self._get_default_params()
        conn = iDRACConnection(params)
        result = conn.__enter__()
        assert result is mock_api
        assert conn.redfish_api is mock_api
        mock_redfish_cls.assert_called_once_with(
            idrac_ip="192.168.1.100",
            idrac_user="admin",
            idrac_password="password",
            idrac_port=443,
            validate_certs=True,
            ca_path=None,
            timeout=30
        )

    @patch(MODULE_UTIL_PATH + 'iDRACRedfishAPI')
    def test_exit_calls_logout(self, mock_redfish_cls):
        from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection
        mock_api = MagicMock()
        mock_redfish_cls.return_value = mock_api
        params = self._get_default_params()
        conn = iDRACConnection(params)
        conn.__enter__()
        result = conn.__exit__(None, None, None)
        assert result is False
        mock_api.logout.assert_called_once()

    def test_exit_without_enter(self):
        from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection
        params = self._get_default_params()
        conn = iDRACConnection(params)
        result = conn.__exit__(None, None, None)
        assert result is False

    @patch(MODULE_UTIL_PATH + 'iDRACRedfishAPI')
    def test_context_manager_with_statement(self, mock_redfish_cls):
        from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection
        mock_api = MagicMock()
        mock_redfish_cls.return_value = mock_api
        params = self._get_default_params()
        with iDRACConnection(params) as api:
            assert api is mock_api
        mock_api.logout.assert_called_once()

    def test_init_default_port(self):
        from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection
        params = {
            "idrac_ip": "192.168.1.100",
            "idrac_user": "admin",
            "idrac_password": "password",
        }
        conn = iDRACConnection(params)
        assert conn.idrac_port == 443
        assert conn.validate_certs is True
        assert conn.ca_path is None
        assert conn.timeout == 30
