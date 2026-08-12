# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.0
# Copyright (C) 2026 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""Unit tests for idrac_network_attributes_info module."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from unittest.mock import MagicMock, patch
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_network_attributes_info
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_network_attributes_info'


class TestIdracNetworkAttributesInfo(FakeAnsibleModule):
    """Test class for idrac_network_attributes_info module."""

    module = idrac_network_attributes_info

    @pytest.fixture
    def idrac_mock(self):
        """Create a mock iDRACRedfishAPI instance."""
        idrac_obj = MagicMock()
        idrac_obj.get_server_generation = (16, "7.30.30.50", "iDRAC 9")
        return idrac_obj

    @pytest.fixture
    def idrac_connection_mock(self, mocker, idrac_mock):
        """Mock the iDRACRedfishAPI context manager."""
        with patch(MODULE_PATH + '.iDRACRedfishAPI') as mock_class:
            mock_class.return_value.__enter__.return_value = idrac_mock
            mock_class.return_value.__exit__.return_value = False
            mock_class.check_minimum_firmware_requirement = iDRACRedfishAPI.check_minimum_firmware_requirement
            mock_class.compare_firmware_version = iDRACRedfishAPI.compare_firmware_version
            yield mock_class

    def test_module_scaffold_loads(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test that the module scaffold loads and exits with fail for non-existent NIC."""
        idrac_default_args['network_device_function_id'] = 'NIC.Fake.1-1-1'

        # Mock empty chassis response so NIC is not found
        mock_resp = MagicMock()
        mock_resp.json_data = {'Members': []}
        idrac_mock.invoke_request.return_value = mock_resp

        result = self._run_module_with_fail_json(idrac_default_args)
        assert result['failed'] is True
        assert 'not found' in result['msg']


@pytest.fixture
def idrac_default_args():
    """Override default args with module-specific parameters."""
    return {
        'idrac_ip': '192.168.0.1',
        'idrac_user': 'user',
        'idrac_password': 'password',
        'idrac_port': 443,
        'validate_certs': True,
        'ca_path': None,
        'timeout': 30,
        'network_device_function_id': 'NIC.Embedded.1-1-1',
        'attribute_name': None,
        'attribute_source': 'all',
        'force_refresh': False,
    }
