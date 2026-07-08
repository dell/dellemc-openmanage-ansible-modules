# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.0
# Copyright (C) 2021-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from unittest.mock import MagicMock, patch

import pytest
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_bios_registry_info
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_bios_registry_info'


class TestFirmwareVersionComparison:
    """Test firmware version comparison logic via centralized utility."""

    def test_compare_firmware_version_equal(self):
        """Test firmware version comparison with equal versions."""
        assert iDRACRedfishAPI.compare_firmware_version("7.10.90.00", "7.10.90.00") is True

    def test_compare_firmware_version_greater(self):
        """Test firmware version comparison with greater version."""
        assert iDRACRedfishAPI.compare_firmware_version("7.10.91.00", "7.10.90.00") is True

    def test_compare_firmware_version_lesser(self):
        """Test firmware version comparison with lesser version."""
        assert iDRACRedfishAPI.compare_firmware_version("7.10.89.00", "7.10.90.00") is False

    def test_compare_firmware_version_iDRAC10_valid(self):
        """Test iDRAC10 firmware version comparison with valid version."""
        assert iDRACRedfishAPI.compare_firmware_version("1.20.50.50", "1.20.50.50") is True

    def test_compare_firmware_version_iDRAC10_below_minimum(self):
        """Test iDRAC10 firmware version comparison below minimum."""
        assert iDRACRedfishAPI.compare_firmware_version("1.20.49.99", "1.20.50.50") is False


class TestIDRACBIOSRegistryInfo(FakeAnsibleModule):
    module = idrac_bios_registry_info

    @pytest.fixture
    def idrac_mock(self):
        """Create a mock iDRACRedfishAPI instance."""
        idrac_obj = MagicMock()
        idrac_obj.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
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

    def test_successful_connection_initialization(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test successful iDRAC connection initialization."""
        idrac_mock.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
        mock_response = MagicMock()
        mock_response.json_data = {
            '@odata.type': '#AttributeRegistry.v1_3_9.AttributeRegistry',
            'RegistryVersion': '1.0.0',
            'Language': 'en',
            'OwningEntity': 'Dell',
            'RegistryEntries': {
                'Attributes': []
            }
        }
        idrac_mock.invoke_request.return_value = mock_response
        # Mock cache to return None to ensure invoke_request is called
        mocker.patch(MODULE_PATH + '.get_from_cache', return_value=None)
        result = self._run_module(idrac_default_args)
        assert result['changed'] is False
        assert 'Successfully queried BIOS attribute registry' in result['msg']
        assert 'bios_attributes' in result
        assert 'registry_version' in result

    def test_authentication_failure_401(self, idrac_default_args, mocker):
        """Test authentication failure with 401 error."""
        http_error = HTTPError(
            url="https://192.168.0.1",
            code=401,
            msg="Unauthorized",
            hdrs={},
            fp=None
        )
        with patch(MODULE_PATH + '.iDRACRedfishAPI') as mock_class:
            mock_class.return_value.__enter__.side_effect = http_error
            mock_class.return_value.__enter__.return_value.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
            assert 'Authentication failed' in result['msg']

    def test_authentication_failure_403(self, idrac_default_args, mocker):
        """Test authentication failure with 403 error."""
        http_error = HTTPError(
            url="https://192.168.0.1",
            code=403,
            msg="Forbidden",
            hdrs={},
            fp=None
        )
        with patch(MODULE_PATH + '.iDRACRedfishAPI') as mock_class:
            mock_class.return_value.__enter__.side_effect = http_error
            mock_class.return_value.__enter__.return_value.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
            assert 'Authentication failed' in result['msg']

    def test_network_timeout_handling(self, idrac_default_args, mocker):
        """Test network timeout handling."""
        url_error = URLError("timeout")
        with patch(MODULE_PATH + '.iDRACRedfishAPI') as mock_class:
            mock_class.return_value.__enter__.side_effect = url_error
            mock_class.return_value.__enter__.return_value.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
            assert 'Network error' in result['msg']

    def test_connection_error_handling(self, idrac_default_args, mocker):
        """Test connection error handling."""
        conn_error = ConnectionError("Connection refused")
        with patch(MODULE_PATH + '.iDRACRedfishAPI') as mock_class:
            mock_class.return_value.__enter__.side_effect = conn_error
            mock_class.return_value.__enter__.return_value.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
            assert 'Connection error' in result['msg']

    def test_ssl_validation_error_handling(self, idrac_default_args, mocker):
        """Test SSL validation error handling."""
        ssl_error = SSLValidationError("Certificate verify failed")
        with patch(MODULE_PATH + '.iDRACRedfishAPI') as mock_class:
            mock_class.return_value.__enter__.side_effect = ssl_error
            mock_class.return_value.__enter__.return_value.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
            assert 'SSL validation error' in result['msg']

    def test_idrac_generation_detection_14g(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test iDRAC generation detection for 14G servers."""
        idrac_mock.get_server_generation = (14, "7.10.90.00", "iDRAC 9")
        # Mock cache to return None to ensure invoke_request is called
        mocker.patch(MODULE_PATH + '.get_from_cache', return_value=None)
        result = self._run_module(idrac_default_args)
        assert result['idrac_generation'] == 14
        assert result['idrac_firmware_version'] == "7.10.90.00"

    def test_idrac_generation_detection_15g(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test iDRAC generation detection for 15G servers."""
        idrac_mock.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
        # Mock cache to return None to ensure invoke_request is called
        mocker.patch(MODULE_PATH + '.get_from_cache', return_value=None)
        result = self._run_module(idrac_default_args)
        assert result['idrac_generation'] == 15

    def test_firmware_version_below_minimum_idrac9(self, idrac_default_args, mocker):
        """Test firmware version below minimum for iDRAC9."""
        idrac_mock = MagicMock()
        idrac_mock.get_server_generation = (15, "7.10.89.99", "iDRAC 9")
        with patch(MODULE_PATH + '.iDRACRedfishAPI') as mock_class:
            mock_class.return_value.__enter__.return_value = idrac_mock
            mock_class.check_minimum_firmware_requirement = iDRACRedfishAPI.check_minimum_firmware_requirement
            mock_class.compare_firmware_version = iDRACRedfishAPI.compare_firmware_version
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
            assert 'Minimum firmware requirement not met' in result['msg']
            assert '7.10.90.00' in result['msg']

    def test_successful_registry_query(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test successful BIOS attribute registry query."""
        mock_response = MagicMock()
        mock_response.json_data = {
            '@odata.type': '#AttributeRegistry.v1_3_9.AttributeRegistry',
            'RegistryVersion': '1.0.0',
            'Language': 'en',
            'OwningEntity': 'Dell',
            'RegistryEntries': {
                'Attributes': [
                    {
                        'AttributeName': 'ProcVirtualization',
                        'DisplayName': 'Virtualization Technology',
                        'Type': 'Enumeration',
                        'CurrentValue': 'Enabled',
                        'DefaultValue': 'Enabled',
                        'Value': [{'ValueName': 'Enabled', 'ValueDisplayName': 'Enabled'},
                                  {'ValueName': 'Disabled', 'ValueDisplayName': 'Disabled'}],
                        'HelpText': 'Enable or disable virtualization.',
                        'MenuPath': './ProcSettingsRef',
                        'ReadOnly': False,
                        'Immutable': False,
                        'WriteOnly': False,
                        'GrayOut': False,
                        'Hidden': False,
                        'DisplayOrder': 1,
                        'Oem': {'Dell': {'@odata.type': '#DellOemAttributeRegistry.v1_0_0.Attributes',
                                         'GroupDisplayName': 'Processor Settings', 'GroupName': 'ProcSettings'}}
                    }
                ]
            }
        }
        idrac_mock.invoke_request.return_value = mock_response
        idrac_mock.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
        # Mock cache to return None to ensure invoke_request is called
        mocker.patch(MODULE_PATH + '.get_from_cache', return_value=None)
        result = self._run_module(idrac_default_args)
        assert result['changed'] is False
        assert len(result['bios_attributes']) == 1
        assert result['bios_attributes'][0]['name'] == 'ProcVirtualization'
        assert result['attribute_count'] == 1

    def test_registry_endpoint_not_supported_404(self, idrac_default_args, mocker):
        """Test registry endpoint not supported (404)."""
        idrac_mock = MagicMock()
        idrac_mock.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
        http_error = HTTPError(
            url="https://192.168.0.1/redfish/v1/Systems/System.Embedded.1/Bios/BiosRegistry",
            code=404,
            msg="Not Found",
            hdrs={},
            fp=None
        )
        idrac_mock.invoke_request.side_effect = http_error
        # Mock cache to return None to ensure invoke_request is called
        mocker.patch(MODULE_PATH + '.get_from_cache', return_value=None)
        # Set force_refresh to True to bypass cache and ensure invoke_request is called
        idrac_default_args['force_refresh'] = True
        with patch(MODULE_PATH + '.iDRACRedfishAPI') as mock_class:
            mock_class.return_value.__enter__.return_value = idrac_mock
            mock_class.check_minimum_firmware_requirement = iDRACRedfishAPI.check_minimum_firmware_requirement
            mock_class.compare_firmware_version = iDRACRedfishAPI.compare_firmware_version
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
            assert 'BIOS attribute registry endpoint not supported' in result['msg']

    def test_attribute_metadata_mapping(self):
        """Test attribute metadata mapping accuracy."""
        attr_data = {
            'AttributeName': 'ProcVirtualization',
            'DisplayName': 'Virtualization Technology',
            'Type': 'Enumeration',
            'CurrentValue': 'Enabled',
            'DefaultValue': 'Enabled',
            'Value': ['Enabled', 'Disabled'],
            'HelpText': 'Enable or disable virtualization.',
            'MenuPath': './Processor',
            'ReadOnly': False,
            'Immutable': False,
            'WriteOnly': False,
            'GrayOut': False,
            'Hidden': False,
            'DisplayOrder': 1
        }
        mapped = idrac_bios_registry_info.map_attribute_to_dict(attr_data)
        assert mapped['name'] == 'ProcVirtualization'
        assert mapped['display_name'] == 'Virtualization Technology'
        assert mapped['type'] == 'Enumeration'
        assert mapped['current_value'] == 'Enabled'
        assert mapped['valid_values'] == ['Enabled', 'Disabled']
        assert mapped['group'] == 'Processor'
        assert mapped['menu_path'] == './Processor'
        assert mapped['read_only'] is False

    def test_pattern_based_filtering_glob(self):
        """Test pattern-based filtering with glob patterns."""
        attributes = [
            {'name': 'ProcVirtualization', 'menu_path': './Processor'},
            {'name': 'MemTest', 'menu_path': './Memory'},
            {'name': 'ProcTurboMode', 'menu_path': './Processor'}
        ]
        filtered = idrac_bios_registry_info.filter_attributes_by_name(attributes, 'Proc*')
        assert len(filtered) == 2
        assert all(attr['name'].startswith('Proc') for attr in filtered)

    def test_exact_match_filtering(self):
        """Test exact match filtering (no wildcard)."""
        attributes = [
            {'name': 'ProcVirtualization', 'menu_path': './Processor'},
            {'name': 'MemTest', 'menu_path': './Memory'}
        ]
        filtered = idrac_bios_registry_info.filter_attributes_by_name(attributes, 'ProcVirtualization')
        assert len(filtered) == 1
        assert filtered[0]['name'] == 'ProcVirtualization'

    def test_oem_attribute_identification(self):
        """Test OEM attribute identification."""
        attributes = [
            {'name': 'OemDellAttribute', 'is_oem': True, 'menu_path': './Oem'},
            {'name': 'StandardAttribute', 'is_oem': False, 'menu_path': './Processor'}
        ]
        oem_filtered = idrac_bios_registry_info.filter_attributes_by_source(attributes, 'oem')
        assert len(oem_filtered) == 1
        assert oem_filtered[0]['is_oem'] is True

        standard_filtered = idrac_bios_registry_info.filter_attributes_by_source(attributes, 'standard')
        assert len(standard_filtered) == 1
        assert standard_filtered[0]['is_oem'] is False

    def test_category_based_filtering(self):
        """Test category-based filtering."""
        attributes = [
            {'name': 'ProcVirtualization', 'group': 'Processor Settings', 'menu_path': './ProcSettingsRef'},
            {'name': 'MemTest', 'group': 'Memory Settings', 'menu_path': './MemSettingsRef'},
            {'name': 'ProcTurboMode', 'group': 'Processor Settings', 'menu_path': './ProcSettingsRef'}
        ]
        filtered = idrac_bios_registry_info.filter_attributes_by_category(attributes, 'Processor')
        assert len(filtered) == 2
        assert all('Processor' in attr['group'] for attr in filtered)

    def test_valid_enumeration_validation(self):
        """Test valid enumeration value validation."""
        bios_attributes = [
            {
                'name': 'ProcVirtualization',
                'type': 'Enumeration',
                'valid_values': ['Enabled', 'Disabled'],
                'read_only': False
            }
        ]
        result = idrac_bios_registry_info.validate_attribute('ProcVirtualization', 'Enabled', bios_attributes)
        assert result['status'] == 'valid'
        assert result['reason'] == 'Value is valid'

    def test_invalid_enumeration_with_suggestions(self):
        """Test invalid enumeration value with suggestions."""
        bios_attributes = [
            {
                'name': 'ProcVirtualization',
                'type': 'Enumeration',
                'valid_values': ['Enabled', 'Disabled'],
                'read_only': False
            }
        ]
        result = idrac_bios_registry_info.validate_attribute('ProcVirtualization', 'enable', bios_attributes)
        assert result['status'] == 'invalid'
        assert 'not a valid enumeration value' in result['reason']
        assert 'Enabled' in result['suggestions']

    def test_non_existent_attribute_name(self):
        """Test validation for non-existent attribute name."""
        bios_attributes = [
            {
                'name': 'ProcVirtualization',
                'type': 'Enumeration',
                'valid_values': ['Enabled', 'Disabled'],
                'read_only': False
            }
        ]
        result = idrac_bios_registry_info.validate_attribute('NonExistentAttr', 'Enabled', bios_attributes)
        assert result['status'] == 'invalid'
        assert 'not found in BIOS registry' in result['reason']

    def test_integer_range_validation(self):
        """Test integer range validation."""
        bios_attributes = [
            {
                'name': 'ProcCores',
                'type': 'Integer',
                'lower_bound': 1,
                'upper_bound': 64,
                'read_only': False
            }
        ]
        result = idrac_bios_registry_info.validate_attribute('ProcCores', 32, bios_attributes)
        assert result['status'] == 'valid'

        result = idrac_bios_registry_info.validate_attribute('ProcCores', 100, bios_attributes)
        assert result['status'] == 'invalid'
        assert 'exceeds maximum' in result['reason']

    def test_batch_validation_mixed_results(self):
        """Test batch validation with mixed valid and invalid results."""
        bios_attributes = [
            {
                'name': 'ProcVirtualization',
                'type': 'Enumeration',
                'valid_values': ['Enabled', 'Disabled'],
                'read_only': False
            },
            {
                'name': 'MemTest',
                'type': 'Enumeration',
                'valid_values': ['Enabled', 'Disabled'],
                'read_only': False
            }
        ]
        attributes_to_validate = {
            'ProcVirtualization': 'Enabled',
            'MemTest': 'InvalidValue'
        }
        result = idrac_bios_registry_info.validate_attributes(attributes_to_validate, bios_attributes)
        assert result['valid'] is False
        assert result['valid_count'] == 1
        assert result['invalid_count'] == 1
        assert len(result['validation_results']) == 2

    def test_return_value_schema_validation(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test return value schema validation."""
        mock_response = MagicMock()
        mock_response.json_data = {
            '@odata.type': '#AttributeRegistry.v1_3_9.AttributeRegistry',
            'RegistryVersion': '1.0.0',
            'Language': 'en',
            'OwningEntity': 'Dell',
            'RegistryEntries': {
                'Attributes': [
                    {
                        'AttributeName': 'ProcVirtualization',
                        'DisplayName': 'Virtualization Technology',
                        'Type': 'Enumeration',
                        'CurrentValue': 'Enabled',
                        'DefaultValue': 'Enabled',
                        'Value': [{'ValueName': 'Enabled', 'ValueDisplayName': 'Enabled'},
                                  {'ValueName': 'Disabled', 'ValueDisplayName': 'Disabled'}],
                        'HelpText': 'Enable or disable virtualization.',
                        'MenuPath': './ProcSettingsRef',
                        'ReadOnly': False,
                        'Immutable': False,
                        'WriteOnly': False,
                        'GrayOut': False,
                        'Hidden': False,
                        'DisplayOrder': 1,
                        'Oem': {'Dell': {'@odata.type': '#DellOemAttributeRegistry.v1_0_0.Attributes',
                                         'GroupDisplayName': 'Processor Settings', 'GroupName': 'ProcSettings'}}
                    }
                ]
            }
        }
        idrac_mock.invoke_request.return_value = mock_response
        idrac_mock.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
        # Mock cache to return None to ensure invoke_request is called
        mocker.patch(MODULE_PATH + '.get_from_cache', return_value=None)
        result = self._run_module(idrac_default_args)
        assert 'bios_attributes' in result
        assert 'registry_version' in result
        assert 'attribute_count' in result
        assert 'language' in result
        assert 'owning_entity' in result
        assert 'idrac_generation' in result
        assert 'idrac_firmware_version' in result
        assert 'idrac_model' in result
        assert result['changed'] is False

    def test_all_24_attribute_properties_present(self):
        """Test all 24 attribute properties are present in mapping."""
        attr_data = {
            'AttributeName': 'TestAttr',
            'DisplayName': 'Test Display',
            'Type': 'String',
            'CurrentValue': 'TestValue',
            'DefaultValue': 'Default',
            'Value': ['TestValue'],
            'HelpText': 'Help text',
            'MenuPath': './Test',
            'ReadOnly': False,
            'Immutable': False,
            'WriteOnly': False,
            'GrayOut': False,
            'Hidden': False,
            'LowerBound': 0,
            'UpperBound': 100,
            'MinLength': 1,
            'MaxLength': 10,
            'ScalarIncrement': 1,
            'Regex': '^[a-z]+$',
            'ValueExpression': 'expr',
            'WarningText': 'Warning',
            'DisplayOrder': 1,
            'IsSystemUniqueProperty': False
        }
        mapped = idrac_bios_registry_info.map_attribute_to_dict(attr_data)
        expected_keys = [
            'name', 'display_name', 'type', 'current_value', 'default_value',
            'valid_values', 'description', 'is_oem', 'read_only', 'immutable',
            'write_only', 'gray_out', 'hidden', 'group', 'menu_path',
            'lower_bound', 'upper_bound', 'min_length', 'max_length',
            'scalar_increment', 'regex', 'value_expression', 'warning_text',
            'display_order', 'is_system_unique_property'
        ]
        for key in expected_keys:
            assert key in mapped

    def test_metadata_fields_present(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test metadata fields are present in return value."""
        mock_response = MagicMock()
        mock_response.json_data = {
            '@odata.type': '#AttributeRegistry.v1_3_9.AttributeRegistry',
            'RegistryVersion': '1.0.0',
            'Language': 'en',
            'OwningEntity': 'Dell',
            'RegistryEntries': {
                'Attributes': []
            }
        }
        idrac_mock.invoke_request.return_value = mock_response
        idrac_mock.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
        # Mock cache to return None to ensure invoke_request is called
        mocker.patch(MODULE_PATH + '.get_from_cache', return_value=None)
        result = self._run_module(idrac_default_args)
        assert result['registry_version'] == '1.0.0'
        assert result['attribute_count'] == 0
        assert result['language'] == 'en'
        assert result['owning_entity'] == 'Dell'
        assert result['idrac_generation'] == 15
        assert result['idrac_firmware_version'] == '7.10.90.00'
        assert result['idrac_model'] == 'iDRAC 9'

    def test_404_error_handling(self, idrac_default_args, mocker):
        """Test 404 error handling for endpoint not supported."""
        idrac_mock = MagicMock()
        idrac_mock.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
        http_error = HTTPError(
            url="https://192.168.0.1/redfish/v1/Systems/System.Embedded.1/Bios/BiosRegistry",
            code=404,
            msg="Not Found",
            hdrs={},
            fp=None
        )
        idrac_mock.invoke_request.side_effect = http_error
        # Mock cache to return None to ensure invoke_request is called
        mocker.patch(MODULE_PATH + '.get_from_cache', return_value=None)
        # Set force_refresh to True to bypass cache and ensure invoke_request is called
        idrac_default_args['force_refresh'] = True
        with patch(MODULE_PATH + '.iDRACRedfishAPI') as mock_class:
            mock_class.return_value.__enter__.return_value = idrac_mock
            mock_class.check_minimum_firmware_requirement = iDRACRedfishAPI.check_minimum_firmware_requirement
            mock_class.compare_firmware_version = iDRACRedfishAPI.compare_firmware_version
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
            assert 'endpoint not supported' in result['msg']

    def test_500_error_handling(self, idrac_default_args, mocker):
        """Test 500 error handling for server errors."""
        idrac_mock = MagicMock()
        idrac_mock.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
        http_error = HTTPError(
            url="https://192.168.0.1/redfish/v1/Systems/System.Embedded.1/Bios/BiosRegistry",
            code=500,
            msg="Internal Server Error",
            hdrs={},
            fp=None
        )
        idrac_mock.invoke_request.side_effect = http_error
        # Mock cache to return None to ensure invoke_request is called
        mocker.patch(MODULE_PATH + '.get_from_cache', return_value=None)
        # Set force_refresh to True to bypass cache and ensure invoke_request is called
        idrac_default_args['force_refresh'] = True
        with patch(MODULE_PATH + '.iDRACRedfishAPI') as mock_class:
            mock_class.return_value.__enter__.return_value = idrac_mock
            mock_class.check_minimum_firmware_requirement = iDRACRedfishAPI.check_minimum_firmware_requirement
            mock_class.compare_firmware_version = iDRACRedfishAPI.compare_firmware_version
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
            assert 'HTTP error 500' in result['msg']


@pytest.fixture
def idrac_default_args():
    """Default module arguments for testing."""
    return {
        'idrac_ip': '192.168.0.1',
        'idrac_user': 'user',
        'idrac_password': 'password',
        'idrac_port': 443,
        'validate_certs': True,
        'ca_path': None,
        'timeout': 30,
        'attribute_name': None,
        'attribute_source': 'all',
        'category': None,
        'validate': False,
        'attributes': None,
        'force_refresh': False,
    }
