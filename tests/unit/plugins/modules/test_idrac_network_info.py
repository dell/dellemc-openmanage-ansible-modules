# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.0
# Copyright (C) 2026 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""Unit tests for idrac_network_info module."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from unittest.mock import MagicMock, patch, call
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_network_info
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_network_info'

# --- Mock Redfish payloads ---

MOCK_CHASSIS_RESP = {
    'Members': [{'@odata.id': '/redfish/v1/Chassis/System.Embedded.1'}]
}

MOCK_CHASSIS_DETAIL = {
    'NetworkAdapters': {'@odata.id': '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters'}
}

MOCK_ADAPTERS_RESP = {
    'Members': [
        {'@odata.id': '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1'},
    ]
}

MOCK_ADAPTER_DETAIL = {
    'NetworkDeviceFunctions': {
        '@odata.id': '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1/NetworkDeviceFunctions'
    }
}

MOCK_NDF_RESP = {
    'Members': [
        {'@odata.id': '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1/NetworkDeviceFunctions/NIC.Embedded.1-1-1'},
        {'@odata.id': '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1/NetworkDeviceFunctions/NIC.Embedded.1-1-2'},
    ]
}

MOCK_NDF_DETAIL_1 = {
    'Id': 'NIC.Embedded.1-1-1',
    'NetDevFuncType': 'Ethernet',
    'Ethernet': {'MACAddress': 'B0:26:28:E4:95:60'},
    'Status': {'Health': 'OK'},
    'Oem': {
        'Dell': {
            'DellNIC': {
                'LinkStatus': 'LinkUp',
                'DeviceDescription': 'Embedded NIC 1 Port 1 Partition 1',
                'LinkSpeed': '10000 Mbps',
                'MediaType': 'Base-T',
            }
        }
    }
}

MOCK_NDF_DETAIL_2 = {
    'Id': 'NIC.Embedded.1-1-2',
    'NetDevFuncType': 'Ethernet',
    'Ethernet': {'MACAddress': 'B0:26:28:E4:95:61'},
    'Status': {'Health': 'OK'},
    'Oem': {
        'Dell': {
            'DellNIC': {
                'LinkStatus': 'LinkDown',
                'DeviceDescription': 'Embedded NIC 1 Port 1 Partition 2',
                'LinkSpeed': '1000 Mbps',
                'MediaType': 'Base-T',
            }
        }
    }
}


def make_mock_response(json_data):
    """Create a mock response object with json_data attribute."""
    resp = MagicMock()
    resp.json_data = json_data
    return resp


def build_invoke_side_effect(uri_map):
    """Build a side_effect function for invoke_request based on a URI-to-response map."""
    def side_effect(uri, method='GET', **kwargs):
        if uri in uri_map:
            return make_mock_response(uri_map[uri])
        raise KeyError(f"Unexpected URI: {uri}")
    return side_effect


class TestIdracNetworkInfo(FakeAnsibleModule):
    """Test class for idrac_network_info module."""

    module = idrac_network_info

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

    @pytest.fixture(autouse=True)
    def clear_cache(self):
        """Clear the module-level cache before each test."""
        idrac_network_info._NIC_CACHE.clear()
        yield
        idrac_network_info._NIC_CACHE.clear()

    # --- Phase 2 Tests: NIC Discovery ---

    def test_discover_all_nics_successfully(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Discover all NICs — mock NetworkAdapters and NetworkDeviceFunctions Redfish
        responses, assert list contains expected fields."""
        uri_map = {
            '/redfish/v1/Chassis': MOCK_CHASSIS_RESP,
            '/redfish/v1/Chassis/System.Embedded.1': MOCK_CHASSIS_DETAIL,
            '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters': MOCK_ADAPTERS_RESP,
            '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1': MOCK_ADAPTER_DETAIL,
            '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1/NetworkDeviceFunctions': MOCK_NDF_RESP,
            '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1/NetworkDeviceFunctions/NIC.Embedded.1-1-1': MOCK_NDF_DETAIL_1,
            '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1/NetworkDeviceFunctions/NIC.Embedded.1-1-2': MOCK_NDF_DETAIL_2,
        }
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(uri_map)

        result = self._run_module(idrac_default_args)

        assert result['changed'] is False
        assert result['msg'] == "Successfully discovered network device functions."
        nics = result['network_device_functions']
        assert len(nics) == 2

        # Verify first NIC has all expected fields
        nic1 = nics[0]
        assert nic1['id'] == 'NIC.Embedded.1-1-1'
        assert nic1['net_dev_func_type'] == 'Ethernet'
        assert nic1['mac_address'] == 'B0:26:28:E4:95:60'
        assert nic1['link_status'] == 'LinkUp'
        assert nic1['device_description'] == 'Embedded NIC 1 Port 1 Partition 1'
        assert nic1['link_speed'] == '10000 Mbps'
        assert nic1['media_type'] == 'Base-T'

        # Verify second NIC
        nic2 = nics[1]
        assert nic2['id'] == 'NIC.Embedded.1-1-2'
        assert nic2['mac_address'] == 'B0:26:28:E4:95:61'

    def test_no_nics_found_empty_chassis(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: No NICs found — mock empty chassis, assert empty list with changed=false."""
        mock_resp = make_mock_response({'Members': []})
        idrac_mock.invoke_request.return_value = mock_resp

        result = self._run_module(idrac_default_args)

        assert result['changed'] is False
        assert result['network_device_functions'] == []
        assert result['msg'] == "Successfully discovered network device functions."

    def test_no_nics_found_no_network_adapters(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Chassis exists but no NetworkAdapters link."""
        uri_map = {
            '/redfish/v1/Chassis': MOCK_CHASSIS_RESP,
            '/redfish/v1/Chassis/System.Embedded.1': {},  # No NetworkAdapters key
        }
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(uri_map)

        result = self._run_module(idrac_default_args)

        assert result['changed'] is False
        assert result['network_device_functions'] == []

    def test_idrac_generation_detection_16g(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: iDRAC9 (16G) generation detection — assert generation info in response."""
        idrac_mock.get_server_generation = (16, "7.30.30.50", "iDRAC 9")
        mock_resp = make_mock_response({'Members': []})
        idrac_mock.invoke_request.return_value = mock_resp

        result = self._run_module(idrac_default_args)

        assert result['idrac_generation'] == 16
        assert result['idrac_firmware_version'] == "7.30.30.50"
        assert result['idrac_model'] == "iDRAC 9"

    def test_idrac_generation_detection_17g(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: iDRAC10 (17G) generation detection — assert generation info in response."""
        idrac_mock.get_server_generation = (17, "1.30.30.50", "iDRAC 10")
        mock_resp = make_mock_response({'Members': []})
        idrac_mock.invoke_request.return_value = mock_resp

        result = self._run_module(idrac_default_args)

        assert result['idrac_generation'] == 17
        assert result['idrac_firmware_version'] == "1.30.30.50"
        assert result['idrac_model'] == "iDRAC 10"

    def test_network_adapters_404_firmware_error(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: NetworkAdapters endpoint 404 — assert failed=true with firmware guidance."""
        from ansible.module_utils.six.moves.urllib.error import HTTPError
        import io

        def raise_404(uri, method='GET', **kwargs):
            if uri == '/redfish/v1/Chassis':
                return make_mock_response(MOCK_CHASSIS_RESP)
            if uri == '/redfish/v1/Chassis/System.Embedded.1':
                return make_mock_response(MOCK_CHASSIS_DETAIL)
            if 'NetworkAdapters' in uri:
                raise HTTPError(uri, 404, 'Not Found', {}, io.BytesIO(b''))
            return make_mock_response({})

        idrac_mock.invoke_request.side_effect = raise_404

        result = self._run_module_with_fail_json(idrac_default_args)

        assert result['failed'] is True
        assert 'NetworkAdapters' in result['msg'] or 'firmware' in result['msg'].lower()

    def test_check_mode(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Check mode support — module exits cleanly without changes."""
        mock_resp = make_mock_response({'Members': []})
        idrac_mock.invoke_request.return_value = mock_resp

        result = self._run_module(idrac_default_args, check_mode=True)

        assert result['changed'] is False

    # --- Phase 2 Tests: Caching ---

    def test_cache_returns_cached_result(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Second call returns cached result without API call."""
        uri_map = {
            '/redfish/v1/Chassis': MOCK_CHASSIS_RESP,
            '/redfish/v1/Chassis/System.Embedded.1': MOCK_CHASSIS_DETAIL,
            '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters': MOCK_ADAPTERS_RESP,
            '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1': MOCK_ADAPTER_DETAIL,
            '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1/NetworkDeviceFunctions': MOCK_NDF_RESP,
            '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1/NetworkDeviceFunctions/NIC.Embedded.1-1-1': MOCK_NDF_DETAIL_1,
            '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1/NetworkDeviceFunctions/NIC.Embedded.1-1-2': MOCK_NDF_DETAIL_2,
        }
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(uri_map)

        # First call populates cache
        result1 = self._run_module(idrac_default_args)
        assert len(result1['network_device_functions']) == 2
        call_count_after_first = idrac_mock.invoke_request.call_count

        # Second call should use cache (no new API calls)
        result2 = self._run_module(idrac_default_args)
        assert len(result2['network_device_functions']) == 2
        assert idrac_mock.invoke_request.call_count == call_count_after_first

    def test_force_refresh_bypasses_cache(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: force_refresh=True bypasses cache and re-queries."""
        uri_map = {
            '/redfish/v1/Chassis': MOCK_CHASSIS_RESP,
            '/redfish/v1/Chassis/System.Embedded.1': MOCK_CHASSIS_DETAIL,
            '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters': MOCK_ADAPTERS_RESP,
            '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1': MOCK_ADAPTER_DETAIL,
            '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1/NetworkDeviceFunctions': MOCK_NDF_RESP,
            '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1/NetworkDeviceFunctions/NIC.Embedded.1-1-1': MOCK_NDF_DETAIL_1,
            '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1/NetworkDeviceFunctions/NIC.Embedded.1-1-2': MOCK_NDF_DETAIL_2,
        }
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(uri_map)

        # First call populates cache
        result1 = self._run_module(idrac_default_args)
        call_count_after_first = idrac_mock.invoke_request.call_count

        # Second call with force_refresh should make new API calls
        idrac_default_args['force_refresh'] = True
        result2 = self._run_module(idrac_default_args)
        assert idrac_mock.invoke_request.call_count > call_count_after_first
        assert len(result2['network_device_functions']) == 2

    # --- Error handling ---

    def test_authentication_failure_401(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Authentication failure (401) returns failed=true."""
        from ansible.module_utils.six.moves.urllib.error import HTTPError
        import io
        idrac_mock.invoke_request.side_effect = HTTPError(
            '/redfish/v1/Chassis', 401, 'Unauthorized', {}, io.BytesIO(b''))

        result = self._run_module_with_fail_json(idrac_default_args)

        assert result['failed'] is True
        assert 'Authentication failed' in result['msg']

    def test_connection_error(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Connection error returns failed=true with descriptive message."""
        from ansible.module_utils.urls import ConnectionError as AnsibleConnectionError
        idrac_mock.invoke_request.side_effect = AnsibleConnectionError("Connection refused")

        result = self._run_module_with_fail_json(idrac_default_args)

        assert result['failed'] is True
        assert 'Connection error' in result['msg']


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
        'force_refresh': False,
    }
