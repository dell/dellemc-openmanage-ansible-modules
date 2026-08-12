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

MOCK_NDF_DETAIL = {
    'Id': 'NIC.Embedded.1-1-1',
    'Links': {
        'Oem': {
            'Dell': {
                'DellNetworkAttributes': {
                    '@odata.id': '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1/NetworkDeviceFunctions/NIC.Embedded.1-1-1/Oem/Dell/DellNetworkAttributes/NIC.Embedded.1-1-1'
                }
            }
        }
    }
}

MOCK_OEM_ATTRS_RESP = {
    'Attributes': {
        'VLanMode': 'Disabled',
        'VLanId': '1',
        'WakeOnLan': 'Enabled',
        'IscsiInitiatorName': 'iqn.2026-01.com.dell:server1',
    },
    'AttributeRegistry': 'NetworkAttributeRegistry_NIC.Embedded.1-1-1',
}

MOCK_REGISTRIES_RESP = {
    'Members': [
        {'@odata.id': '/redfish/v1/Registries/NetworkAttributeRegistry_NIC.Embedded.1-1-1'},
    ]
}

MOCK_REGISTRY_DETAIL = {
    'Location': [
        {'Uri': '/redfish/v1/Registries/NetworkAttributeRegistry_NIC.Embedded.1-1-1/NetworkAttributeRegistry_NIC.Embedded.1-1-1.json'}
    ]
}

MOCK_REGISTRY_FULL = {
    'RegistryEntries': {
        'Attributes': [
            {
                'AttributeName': 'VLanMode',
                'Type': 'Enumeration',
                'DefaultValue': 'Disabled',
                'Value': [
                    {'ValueName': 'Disabled'},
                    {'ValueName': 'Enabled'},
                ],
                'HelpText': 'Enable or disable VLAN mode.',
                'ReadOnly': False,
                'Oem': {'Dell': {'RequiresReboot': False}},
                'Dependency': [],
            },
            {
                'AttributeName': 'VLanId',
                'Type': 'Integer',
                'DefaultValue': '1',
                'Value': [],
                'HelpText': 'VLAN ID number.',
                'ReadOnly': False,
                'LowerBound': 1,
                'UpperBound': 4094,
                'Oem': {'Dell': {'RequiresReboot': False}},
                'Dependency': [],
            },
            {
                'AttributeName': 'WakeOnLan',
                'Type': 'Enumeration',
                'DefaultValue': 'Enabled',
                'Value': [
                    {'ValueName': 'Enabled'},
                    {'ValueName': 'Disabled'},
                ],
                'HelpText': 'Enable or disable Wake-on-LAN.',
                'ReadOnly': False,
                'Oem': {},
                'Dependency': [],
            },
            {
                'AttributeName': 'IscsiInitiatorName',
                'Type': 'String',
                'DefaultValue': '',
                'Value': [],
                'HelpText': 'iSCSI initiator name (IQN format).',
                'ReadOnly': False,
                'MinLength': 0,
                'MaxLength': 223,
                'Oem': {'Dell': {}},
                'Dependency': [],
            },
        ]
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


# Full URI map for successful attribute query
FULL_URI_MAP = {
    '/redfish/v1/Chassis': MOCK_CHASSIS_RESP,
    '/redfish/v1/Chassis/System.Embedded.1': MOCK_CHASSIS_DETAIL,
    '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters': MOCK_ADAPTERS_RESP,
    '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1': MOCK_ADAPTER_DETAIL,
    '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1/NetworkDeviceFunctions': MOCK_NDF_RESP,
    '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1/NetworkDeviceFunctions/NIC.Embedded.1-1-1': MOCK_NDF_DETAIL,
    '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1/NetworkDeviceFunctions/NIC.Embedded.1-1-1/Oem/Dell/DellNetworkAttributes/NIC.Embedded.1-1-1': MOCK_OEM_ATTRS_RESP,
    '/redfish/v1/Registries': MOCK_REGISTRIES_RESP,
    '/redfish/v1/Registries/NetworkAttributeRegistry_NIC.Embedded.1-1-1': MOCK_REGISTRY_DETAIL,
    '/redfish/v1/Registries/NetworkAttributeRegistry_NIC.Embedded.1-1-1/NetworkAttributeRegistry_NIC.Embedded.1-1-1.json': MOCK_REGISTRY_FULL,
}


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

    @pytest.fixture(autouse=True)
    def clear_cache(self):
        """Clear the module-level cache before each test."""
        idrac_network_attributes_info._REGISTRY_CACHE.clear()
        yield
        idrac_network_attributes_info._REGISTRY_CACHE.clear()

    # --- Phase 3 Tests: Attribute Registry Query ---

    def test_query_all_attributes_for_valid_nic(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Query all attributes for valid NIC — assert merged output with expected fields."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)

        result = self._run_module(idrac_default_args)

        assert result['changed'] is False
        assert result['msg'] == "Successfully queried network attribute registry."
        assert result['network_device_function_id'] == 'NIC.Embedded.1-1-1'
        assert result['attribute_registry'] == 'NetworkAttributeRegistry_NIC.Embedded.1-1-1'
        assert result['attribute_count'] == 4

        attrs = result['network_attributes']
        assert len(attrs) == 4

        # Verify VLanMode attribute has all expected fields
        vlan_mode = next(a for a in attrs if a['name'] == 'VLanMode')
        assert vlan_mode['type'] == 'Enumeration'
        assert vlan_mode['current_value'] == 'Disabled'
        assert vlan_mode['default_value'] == 'Disabled'
        assert vlan_mode['valid_values'] == ['Disabled', 'Enabled']
        assert vlan_mode['description'] == 'Enable or disable VLAN mode.'
        assert vlan_mode['is_oem'] is True
        assert vlan_mode['read_only'] is False

        # Verify VLanId attribute (Integer type)
        vlan_id = next(a for a in attrs if a['name'] == 'VLanId')
        assert vlan_id['type'] == 'Integer'
        assert vlan_id['current_value'] == '1'
        assert vlan_id['lower_bound'] == 1
        assert vlan_id['upper_bound'] == 4094

    def test_nic_id_not_found_with_auto_discovery(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: NIC ID not found — assert error message contains list of valid NIC IDs."""
        idrac_default_args['network_device_function_id'] = 'NIC.Fake.1-1-1'
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)

        result = self._run_module_with_fail_json(idrac_default_args)

        assert result['failed'] is True
        assert 'NIC.Fake.1-1-1' in result['msg']
        assert 'not found' in result['msg']
        # Should include discovered valid NIC IDs
        assert 'NIC.Embedded.1-1-1' in result['msg']

    def test_oem_link_not_present_on_nic(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: OEM link not present on NIC — assert failed=true."""
        ndf_detail_no_oem = {
            'Id': 'NIC.Embedded.1-1-1',
            'Links': {},  # No OEM links
        }
        uri_map = dict(FULL_URI_MAP)
        ndf_uri = '/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Embedded.1/NetworkDeviceFunctions/NIC.Embedded.1-1-1'
        uri_map[ndf_uri] = ndf_detail_no_oem
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(uri_map)

        result = self._run_module_with_fail_json(idrac_default_args)

        assert result['failed'] is True
        assert 'OEM' in result['msg'] or 'not found' in result['msg']

    def test_registry_endpoint_resolution(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Module follows AttributeRegistry field to locate registry JSON."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)

        result = self._run_module(idrac_default_args)

        # Verify the module resolved the registry via the Registries endpoint
        assert result['attribute_registry'] == 'NetworkAttributeRegistry_NIC.Embedded.1-1-1'
        assert result['attribute_count'] == 4
        # Verify current values were merged from the OEM attributes response
        attrs = result['network_attributes']
        vlan_mode = next(a for a in attrs if a['name'] == 'VLanMode')
        assert vlan_mode['current_value'] == 'Disabled'

    def test_idrac_generation_in_response(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: iDRAC generation info is included in attribute query response."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)

        result = self._run_module(idrac_default_args)

        assert result['idrac_generation'] == 16
        assert result['idrac_firmware_version'] == "7.30.30.50"
        assert result['idrac_model'] == "iDRAC 9"

    # --- Caching tests ---

    def test_cache_returns_cached_result(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Second call returns cached result without API calls."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)

        # First call populates cache
        result1 = self._run_module(idrac_default_args)
        call_count_after_first = idrac_mock.invoke_request.call_count

        # Second call should use cache
        result2 = self._run_module(idrac_default_args)
        assert result2['attribute_count'] == 4
        assert idrac_mock.invoke_request.call_count == call_count_after_first

    def test_force_refresh_bypasses_cache(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: force_refresh=True bypasses cache and re-queries."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)

        # First call populates cache
        result1 = self._run_module(idrac_default_args)
        call_count_after_first = idrac_mock.invoke_request.call_count

        # Second call with force_refresh should make new API calls
        idrac_default_args['force_refresh'] = True
        result2 = self._run_module(idrac_default_args)
        assert idrac_mock.invoke_request.call_count > call_count_after_first

    # --- Error handling ---

    def test_authentication_failure_401(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Authentication failure returns failed=true."""
        from ansible.module_utils.six.moves.urllib.error import HTTPError
        import io
        idrac_mock.invoke_request.side_effect = HTTPError(
            '/redfish/v1/Chassis', 401, 'Unauthorized', {}, io.BytesIO(b''))

        result = self._run_module_with_fail_json(idrac_default_args)
        assert result['failed'] is True
        assert 'Authentication failed' in result['msg']

    def test_check_mode(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Check mode exits cleanly."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)

        result = self._run_module(idrac_default_args, check_mode=True)
        assert result['changed'] is False

    # --- Phase 4 Tests: Attribute Filtering ---

    def test_glob_pattern_filter(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Glob pattern filter — provide attribute_name='VLan*', assert only matching."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)
        idrac_default_args['attribute_name'] = 'VLan*'

        result = self._run_module(idrac_default_args)

        assert result['changed'] is False
        attrs = result['network_attributes']
        assert len(attrs) == 2  # VLanMode and VLanId
        names = [a['name'] for a in attrs]
        assert 'VLanMode' in names
        assert 'VLanId' in names
        assert 'WakeOnLan' not in names
        assert result['attribute_count'] == 2

    def test_exact_name_filter(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Exact name filter — provide exact attribute name, assert single result."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)
        idrac_default_args['attribute_name'] = 'VLanMode'

        result = self._run_module(idrac_default_args)

        attrs = result['network_attributes']
        assert len(attrs) == 1
        assert attrs[0]['name'] == 'VLanMode'
        assert result['attribute_count'] == 1

    def test_no_match_filter(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: No match — provide non-existent pattern, assert empty list."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)
        idrac_default_args['attribute_name'] = 'NonExistent*'

        result = self._run_module(idrac_default_args)

        assert result['changed'] is False
        assert result['network_attributes'] == []
        assert result['attribute_count'] == 0

    def test_oem_filter(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: OEM filter — attribute_source='oem', assert all results have is_oem=true."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)
        idrac_default_args['attribute_source'] = 'oem'

        result = self._run_module(idrac_default_args)

        for attr in result['network_attributes']:
            assert attr['is_oem'] is True

    def test_standard_filter(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Standard filter — attribute_source='standard', assert all results have is_oem=false."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)
        idrac_default_args['attribute_source'] = 'standard'

        result = self._run_module(idrac_default_args)

        for attr in result['network_attributes']:
            assert attr['is_oem'] is False
        # WakeOnLan has empty Oem.Dell, so is_oem=false
        names = [a['name'] for a in result['network_attributes']]
        assert 'WakeOnLan' in names

    def test_combined_filters(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Combined filters — attribute_name + attribute_source, assert both applied."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)
        idrac_default_args['attribute_name'] = 'VLan*'
        idrac_default_args['attribute_source'] = 'oem'

        result = self._run_module(idrac_default_args)

        # VLanMode and VLanId match 'VLan*' pattern and both have is_oem=True
        attrs = result['network_attributes']
        assert len(attrs) == 2
        for attr in attrs:
            assert attr['is_oem'] is True
            assert attr['name'].startswith('VLan')


    # --- Validation Tests ---

    def test_valid_enum_value_returns_valid(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Valid enumeration value returns status=valid."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)
        idrac_default_args['validate'] = True
        idrac_default_args['attributes'] = {'VLanMode': 'Enabled'}

        result = self._run_module(idrac_default_args)

        assert result['valid'] is True
        assert result['valid_count'] == 1
        assert result['invalid_count'] == 0
        vr = result['validation_results']
        assert len(vr) == 1
        assert vr[0]['attribute'] == 'VLanMode'
        assert vr[0]['status'] == 'valid'

    def test_invalid_enum_value_returns_invalid(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Invalid enumeration value returns status=invalid with reason and allowed values."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)
        idrac_default_args['validate'] = True
        idrac_default_args['attributes'] = {'VLanMode': 'True'}

        result = self._run_module(idrac_default_args)

        assert result['valid'] is False
        assert result['invalid_count'] == 1
        vr = result['validation_results']
        assert vr[0]['status'] == 'invalid'
        assert 'True' in vr[0]['reason']
        # Reason should mention allowed values
        assert 'Disabled' in vr[0]['reason'] or 'Enabled' in vr[0]['reason']

    def test_enum_case_sensitive_matching(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Case-sensitive matching for enumeration values."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)
        idrac_default_args['validate'] = True
        idrac_default_args['attributes'] = {'VLanMode': 'enabled'}  # lowercase

        result = self._run_module(idrac_default_args)

        assert result['valid'] is False
        vr = result['validation_results']
        assert vr[0]['status'] == 'invalid'

    def test_valid_integer_within_bounds(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Valid integer within LowerBound/UpperBound returns valid."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)
        idrac_default_args['validate'] = True
        idrac_default_args['attributes'] = {'VLanId': '100'}

        result = self._run_module(idrac_default_args)

        assert result['valid'] is True
        vr = result['validation_results']
        assert vr[0]['status'] == 'valid'
        assert vr[0]['attribute'] == 'VLanId'

    def test_integer_out_of_range_returns_invalid(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Out-of-range integer returns invalid with range details."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)
        idrac_default_args['validate'] = True
        idrac_default_args['attributes'] = {'VLanId': '99999'}

        result = self._run_module(idrac_default_args)

        assert result['valid'] is False
        vr = result['validation_results']
        assert vr[0]['status'] == 'invalid'
        assert '1' in vr[0]['reason']
        assert '4094' in vr[0]['reason']

    def test_non_numeric_integer_returns_invalid(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Non-numeric string for integer attribute returns invalid."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)
        idrac_default_args['validate'] = True
        idrac_default_args['attributes'] = {'VLanId': 'abc'}

        result = self._run_module(idrac_default_args)

        assert result['valid'] is False
        vr = result['validation_results']
        assert vr[0]['status'] == 'invalid'
        assert 'not numeric' in vr[0]['reason'].lower() or 'integer' in vr[0]['reason'].lower()

    # --- String Validation Tests ---

    def test_string_within_maxlength_is_valid(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: String within MinLength/MaxLength bounds is valid."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)
        idrac_default_args['validate'] = True
        idrac_default_args['attributes'] = {'IscsiInitiatorName': 'iqn.2026-01.com.dell:test'}

        result = self._run_module(idrac_default_args)

        assert result['valid'] is True
        vr = result['validation_results']
        assert vr[0]['status'] == 'valid'
        assert vr[0]['attribute'] == 'IscsiInitiatorName'

    def test_string_exceeding_maxlength_is_invalid(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: String violating MaxLength is invalid."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)
        idrac_default_args['validate'] = True
        # MaxLength is 223 for IscsiInitiatorName; use 250 chars
        idrac_default_args['attributes'] = {'IscsiInitiatorName': 'x' * 250}

        result = self._run_module(idrac_default_args)

        assert result['valid'] is False
        vr = result['validation_results']
        assert vr[0]['status'] == 'invalid'
        assert '223' in vr[0]['reason']

    # --- Fuzzy Match Suggestion Tests ---

    def test_fuzzy_match_suggestions_for_misspelled_name(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Non-existent attribute name returns suggestions list with up to 3 close matches."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)
        idrac_default_args['validate'] = True
        idrac_default_args['attributes'] = {'VLanMoed': 'Enabled'}

        result = self._run_module(idrac_default_args)

        assert result['valid'] is False
        vr = result['validation_results']
        assert vr[0]['status'] == 'invalid'
        assert vr[0]['reason'] == 'Attribute not found.'
        assert len(vr[0]['suggestions']) > 0
        assert len(vr[0]['suggestions']) <= 3
        # VLanMode is close to VLanMoed
        assert 'VLanMode' in vr[0]['suggestions']

    def test_fuzzy_match_no_suggestions_for_unrelated_name(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Completely unrelated name returns empty suggestions."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)
        idrac_default_args['validate'] = True
        idrac_default_args['attributes'] = {'XyzNotAnAttribute123': 'value'}

        result = self._run_module(idrac_default_args)

        assert result['valid'] is False
        vr = result['validation_results']
        assert vr[0]['status'] == 'invalid'
        assert vr[0]['reason'] == 'Attribute not found.'
        assert vr[0]['suggestions'] == []

    # --- Batch Validation Tests ---

    def test_batch_all_valid(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: All valid attributes → valid=true, valid_count=N, invalid_count=0."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)
        idrac_default_args['validate'] = True
        idrac_default_args['attributes'] = {
            'VLanMode': 'Enabled',
            'VLanId': '100',
            'WakeOnLan': 'Disabled',
        }

        result = self._run_module(idrac_default_args)

        assert result['valid'] is True
        assert result['valid_count'] == 3
        assert result['invalid_count'] == 0
        assert len(result['validation_results']) == 3

    def test_batch_mixed_valid_invalid(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: Mix of valid and invalid → valid=false, counts correct, per-attribute status."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)
        idrac_default_args['validate'] = True
        idrac_default_args['attributes'] = {
            'VLanMode': 'Enabled',       # valid
            'VLanId': '99999',           # invalid (out of range)
            'VLanMoed': 'Enabled',       # invalid (not found)
        }

        result = self._run_module(idrac_default_args)

        assert result['valid'] is False
        assert result['valid_count'] == 1
        assert result['invalid_count'] == 2
        assert len(result['validation_results']) == 3
        statuses = {vr['attribute']: vr['status'] for vr in result['validation_results']}
        assert statuses['VLanMode'] == 'valid'
        assert statuses['VLanId'] == 'invalid'
        assert statuses['VLanMoed'] == 'invalid'

    def test_batch_all_invalid(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: All invalid attributes → valid=false, valid_count=0, invalid_count=N."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)
        idrac_default_args['validate'] = True
        idrac_default_args['attributes'] = {
            'VLanMode': 'BadValue',
            'NonExistent': 'something',
        }

        result = self._run_module(idrac_default_args)

        assert result['valid'] is False
        assert result['valid_count'] == 0
        assert result['invalid_count'] == 2

    def test_validate_true_empty_attributes_fails(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: validate=true with empty attributes dict → failed=true."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)
        idrac_default_args['validate'] = True
        idrac_default_args['attributes'] = {}

        result = self._run_module_with_fail_json(idrac_default_args)

        assert result['failed'] is True

    def test_validate_false_omits_validation_keys(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test: validate=false omits validation keys from response."""
        idrac_mock.invoke_request.side_effect = build_invoke_side_effect(FULL_URI_MAP)

        result = self._run_module(idrac_default_args)

        assert 'valid' not in result
        assert 'valid_count' not in result
        assert 'invalid_count' not in result
        assert 'validation_results' not in result


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
        'validate': False,
        'attributes': None,
    }
