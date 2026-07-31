# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.0
# Copyright (C) 2025-2026 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import pytest
from io import StringIO
from unittest.mock import MagicMock, patch

from ansible.module_utils._text import to_text
from urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import (
    idrac_network_attribute_registry,
)
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import (
    FakeAnsibleModule,
)

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
MODULE_UTIL_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish.'

SAMPLE_REGISTRY_DATA = {
    "RegistryEntries": {
        "Attributes": [
            {
                "AttributeName": "VLanMode",
                "Type": "Enumeration",
                "Value": [
                    {"ValueName": "Enabled"},
                    {"ValueName": "Disabled"},
                ],
                "HelpText": "Enables or disables VLAN mode.",
                "ReadOnly": False,
                "Oem": {"Dell": {}},
            },
            {
                "AttributeName": "VLanId",
                "Type": "Integer",
                "Value": [],
                "HelpText": "VLAN identifier.",
                "ReadOnly": False,
                "Oem": {"Dell": {}},
            },
            {
                "AttributeName": "VLanPriority",
                "Type": "Integer",
                "Value": [],
                "HelpText": "VLAN priority level.",
                "ReadOnly": False,
                "Oem": {"Dell": {}},
            },
            {
                "AttributeName": "LinkSpeed",
                "Type": "Enumeration",
                "Value": [
                    {"ValueName": "AutoNeg"},
                    {"ValueName": "10Mbps"},
                    {"ValueName": "100Mbps"},
                    {"ValueName": "1Gbps"},
                ],
                "HelpText": "Network link speed setting.",
                "ReadOnly": False,
            },
            {
                "AttributeName": "LinkDuplex",
                "Type": "Enumeration",
                "Value": [
                    {"ValueName": "Full"},
                    {"ValueName": "Half"},
                ],
                "HelpText": "Network link duplex mode.",
                "ReadOnly": True,
            },
            {
                "AttributeName": "MACAddress",
                "Type": "String",
                "Value": [],
                "HelpText": "MAC address of the network adapter.",
                "ReadOnly": True,
            },
        ]
    }
}

MANAGER_RESP_16G = {
    "Model": "PowerEdge R660 iDRAC 16G",
    "FirmwareVersion": "7.30.30.50",
}

MANAGER_RESP_17G = {
    "Model": "PowerEdge R770 iDRAC 17G",
    "FirmwareVersion": "1.30.30.50",
}

MANAGER_RESP_OLD_FW = {
    "Model": "PowerEdge R660 iDRAC 16G",
    "FirmwareVersion": "6.10.00.00",
}

HW_MODEL_RESP_IDRAC9 = {
    "Attributes": {"Info.1.HWModel": "iDRAC 9"},
}

HW_MODEL_RESP_IDRAC10 = {
    "Attributes": {"Info.1.HWModel": "iDRAC 10"},
}

REGISTRY_LIST_RESP = {
    "Members": [
        {"@odata.id": "/redfish/v1/Registries/NetworkAttributeRegistry_NIC.Integrated.1-1-1"}
    ]
}


class TestIdracNetworkAttributeRegistry(FakeAnsibleModule):
    module = idrac_network_attribute_registry

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
        return idrac_obj

    @pytest.fixture
    def idrac_connection_mock(self, mocker, idrac_mock):
        idrac_conn_mock = mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.iDRACRedfishAPI',
            return_value=idrac_mock
        )
        idrac_conn_mock.return_value.__enter__.return_value = idrac_mock
        return idrac_conn_mock

    def _make_response(self, data, status_code=200):
        resp = MagicMock()
        resp.json_data = data
        resp.status_code = status_code
        return resp

    # --- Argument spec validation tests ---

    def test_default_query_type(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test that default query_type is 'all'."""
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.get_idrac_firmware_info',
            return_value=(16, "7.30.30.50", "iDRAC 9")
        )
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.fetch_registry_attributes',
            return_value=SAMPLE_REGISTRY_DATA
        )
        result = self._run_module(idrac_default_args)
        assert result['changed'] is False
        assert result['msg'] == "Successfully retrieved network attribute registry."
        assert result['attribute_count'] == 6

    def test_validate_requires_validate_attributes(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test that query_type=validate without validate_attributes fails."""
        idrac_default_args.update({"query_type": "validate"})
        result = self._run_module_with_fail_json(idrac_default_args)
        assert "validate_attributes" in result['msg']

    def test_invalid_query_type_rejected(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test that an invalid query_type is rejected by argument spec."""
        idrac_default_args.update({"query_type": "invalid_type"})
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result['failed'] is True

    def test_invalid_output_format_rejected(self, idrac_default_args, idrac_connection_mock, idrac_mock):
        """Test that an invalid output_format is rejected by argument spec."""
        idrac_default_args.update({"output_format": "xml"})
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result['failed'] is True

    # --- iDRAC connection initialization tests ---

    def test_idrac_connection_setup(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test that iDRACRedfishAPI is initialized with req_session=True."""
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.get_idrac_firmware_info',
            return_value=(16, "7.30.30.50", "iDRAC 9")
        )
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.fetch_registry_attributes',
            return_value=SAMPLE_REGISTRY_DATA
        )
        self._run_module(idrac_default_args)
        idrac_connection_mock.assert_called_once()
        call_args = idrac_connection_mock.call_args
        assert call_args[1].get('req_session') is True or call_args[0][1] is True

    # --- Firmware version check tests ---

    def test_firmware_check_idrac9_pass(self):
        """Test firmware check passes for iDRAC9 at minimum version."""
        result, min_ver = idrac_network_attribute_registry.check_firmware_version("7.30.30.50", "iDRAC 9")
        assert result is True
        assert min_ver == "7.30.30.50"

    def test_firmware_check_idrac9_above_minimum(self):
        """Test firmware check passes for iDRAC9 above minimum version."""
        result, min_ver = idrac_network_attribute_registry.check_firmware_version("7.30.31.00", "iDRAC 9")
        assert result is True

    def test_firmware_check_idrac9_fail(self):
        """Test firmware check fails for iDRAC9 below minimum version."""
        result, min_ver = idrac_network_attribute_registry.check_firmware_version("6.10.00.00", "iDRAC 9")
        assert result is False
        assert min_ver == "7.30.30.50"

    def test_firmware_check_idrac10_pass(self):
        """Test firmware check passes for iDRAC10 at minimum version."""
        result, min_ver = idrac_network_attribute_registry.check_firmware_version("1.30.30.50", "iDRAC 10")
        assert result is True
        assert min_ver == "1.30.30.50"

    def test_firmware_check_idrac10_fail(self):
        """Test firmware check fails for iDRAC10 below minimum version."""
        result, min_ver = idrac_network_attribute_registry.check_firmware_version("1.20.00.00", "iDRAC 10")
        assert result is False
        assert min_ver == "1.30.30.50"

    def test_firmware_below_minimum_fails_module(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test that firmware below minimum causes module to fail with descriptive error."""
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.get_idrac_firmware_info',
            return_value=(16, "6.10.00.00", "iDRAC 9")
        )
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result['failed'] is True
        assert "6.10.00.00" in result['msg']
        assert "7.30.30.50" in result['msg']
        assert "firmware" in result['msg'].lower()

    # --- Registry query tests ---

    def test_query_all_returns_all_attributes(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test query_type=all returns all attributes."""
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.get_idrac_firmware_info',
            return_value=(16, "7.30.30.50", "iDRAC 9")
        )
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.fetch_registry_attributes',
            return_value=SAMPLE_REGISTRY_DATA
        )
        result = self._run_module(idrac_default_args)
        assert result['attribute_count'] == 6
        attr_names = [a['name'] for a in result['attributes']]
        assert "VLanMode" in attr_names
        assert "LinkSpeed" in attr_names
        assert "MACAddress" in attr_names

    def test_query_all_attribute_fields(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test that each attribute has the required fields."""
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.get_idrac_firmware_info',
            return_value=(16, "7.30.30.50", "iDRAC 9")
        )
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.fetch_registry_attributes',
            return_value=SAMPLE_REGISTRY_DATA
        )
        result = self._run_module(idrac_default_args)
        for attr in result['attributes']:
            assert 'name' in attr
            assert 'data_type' in attr
            assert 'valid_values' in attr
            assert 'description' in attr
            assert 'read_only' in attr

    def test_no_registry_data_fails(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test that missing registry data causes failure."""
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.get_idrac_firmware_info',
            return_value=(16, "7.30.30.50", "iDRAC 9")
        )
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.fetch_registry_attributes',
            return_value=None
        )
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result['failed'] is True
        assert "No network attribute registry data found" in result['msg']

    # --- Parse helper tests ---

    def test_parse_registry_attributes_empty(self):
        """Test parse_registry_attributes returns empty list for None."""
        result = idrac_network_attribute_registry.parse_registry_attributes(None)
        assert result == []

    def test_parse_registry_attributes_valid(self):
        """Test parse_registry_attributes correctly parses sample data."""
        result = idrac_network_attribute_registry.parse_registry_attributes(SAMPLE_REGISTRY_DATA)
        assert len(result) == 6
        vlan = next(a for a in result if a['name'] == 'VLanMode')
        assert vlan['data_type'] == 'Enumeration'
        assert vlan['valid_values'] == ['Enabled', 'Disabled']
        assert vlan['read_only'] is False
        assert vlan['oem_vendor'] == 'Dell'

    def test_parse_registry_attributes_malformed(self):
        """Test parse_registry_attributes handles malformed data."""
        malformed = {"RegistryEntries": {}}
        result = idrac_network_attribute_registry.parse_registry_attributes(malformed)
        assert result == []

    # --- OEM and Redfish query type module-level tests (AC2) ---

    def test_query_oem_returns_only_oem(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test query_type=oem returns only Dell OEM attributes through module."""
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.get_idrac_firmware_info',
            return_value=(16, "7.30.30.50", "iDRAC 9")
        )
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.fetch_registry_attributes',
            return_value=SAMPLE_REGISTRY_DATA
        )
        idrac_default_args.update({"query_type": "oem"})
        result = self._run_module(idrac_default_args)
        assert result['changed'] is False
        for attr in result['attributes']:
            assert attr['oem_vendor'] == 'Dell'
        assert result['attribute_count'] == 3

    def test_query_redfish_excludes_oem(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test query_type=redfish returns only standard Redfish attributes through module."""
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.get_idrac_firmware_info',
            return_value=(16, "7.30.30.50", "iDRAC 9")
        )
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.fetch_registry_attributes',
            return_value=SAMPLE_REGISTRY_DATA
        )
        idrac_default_args.update({"query_type": "redfish"})
        result = self._run_module(idrac_default_args)
        assert result['changed'] is False
        for attr in result['attributes']:
            assert attr['oem_vendor'] is None

    # --- Wildcard pattern module-level tests (AC4) ---

    def test_wildcard_pattern_through_module(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test attribute_pattern filtering through module."""
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.get_idrac_firmware_info',
            return_value=(16, "7.30.30.50", "iDRAC 9")
        )
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.fetch_registry_attributes',
            return_value=SAMPLE_REGISTRY_DATA
        )
        idrac_default_args.update({"attribute_pattern": "VLan*"})
        result = self._run_module(idrac_default_args)
        assert result['attribute_count'] == 3
        for attr in result['attributes']:
            assert attr['name'].startswith("VLan")

    def test_wildcard_pattern_no_match_through_module(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test attribute_pattern with no matches returns empty list."""
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.get_idrac_firmware_info',
            return_value=(16, "7.30.30.50", "iDRAC 9")
        )
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.fetch_registry_attributes',
            return_value=SAMPLE_REGISTRY_DATA
        )
        idrac_default_args.update({"attribute_pattern": "NonExistent*"})
        result = self._run_module(idrac_default_args)
        assert result['attribute_count'] == 0
        assert result['attributes'] == []

    # --- Validate query type module-level test (AC3) ---

    def test_validate_through_module(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test query_type=validate returns validation results through module."""
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.get_idrac_firmware_info',
            return_value=(16, "7.30.30.50", "iDRAC 9")
        )
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.fetch_registry_attributes',
            return_value=SAMPLE_REGISTRY_DATA
        )
        idrac_default_args.update({
            "query_type": "validate",
            "validate_attributes": {"VLanMode": "Enabled", "VLanMod": "Enabled"},
        })
        result = self._run_module(idrac_default_args)
        assert result['changed'] is False
        assert result['msg'] == "Attribute validation completed."
        assert len(result['validation_results']) == 2
        statuses = {r['attribute_name']: r['status'] for r in result['validation_results']}
        assert statuses['VLanMode'] == 'pass'
        assert statuses['VLanMod'] == 'fail'

    # --- Check mode test ---

    def test_check_mode(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test that check_mode does not query registry."""
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.get_idrac_firmware_info',
            return_value=(16, "7.30.30.50", "iDRAC 9")
        )
        fetch_mock = mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.fetch_registry_attributes',
        )
        result = self._run_module(idrac_default_args, check_mode=True)
        assert result['changed'] is False
        assert "Check mode" in result['msg']
        fetch_mock.assert_not_called()

    # --- Error handling tests ---

    def test_http_error_handling(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test that HTTPError is handled gracefully."""
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.get_idrac_firmware_info',
            side_effect=HTTPError(
                'https://test', 401, 'Unauthorized', {},
                StringIO('{"error": "unauthorized"}')
            )
        )
        result = self._run_module(idrac_default_args)
        assert result['failed'] is True

    def test_url_error_handling(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test that URLError is handled gracefully."""
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.get_idrac_firmware_info',
            side_effect=URLError('Connection refused')
        )
        result = self._run_module(idrac_default_args)
        assert result.get('unreachable') is True

    def test_connection_error_handling(self, idrac_default_args, idrac_connection_mock, idrac_mock, mocker):
        """Test that ConnectionError is handled gracefully."""
        mocker.patch(
            MODULE_PATH + 'idrac_network_attribute_registry.get_idrac_firmware_info',
            side_effect=ConnectionError('Connection failed')
        )
        result = self._run_module(idrac_default_args)
        assert result['failed'] is True


class TestFilterFunctions:
    """Test filter helper functions independently."""

    def _get_parsed_attrs(self):
        return idrac_network_attribute_registry.parse_registry_attributes(SAMPLE_REGISTRY_DATA)

    def test_filter_by_query_type_all(self):
        attrs = self._get_parsed_attrs()
        result = idrac_network_attribute_registry.filter_by_query_type(attrs, "all")
        assert len(result) == 6

    def test_filter_by_query_type_oem(self):
        attrs = self._get_parsed_attrs()
        result = idrac_network_attribute_registry.filter_by_query_type(attrs, "oem")
        oem_names = [a['name'] for a in result]
        assert "VLanMode" in oem_names
        assert "VLanId" in oem_names
        for attr in result:
            assert attr['oem_vendor'] == 'Dell'

    def test_filter_by_query_type_redfish(self):
        attrs = self._get_parsed_attrs()
        result = idrac_network_attribute_registry.filter_by_query_type(attrs, "redfish")
        for attr in result:
            assert attr['oem_vendor'] is None

    def test_filter_by_pattern_vlan(self):
        attrs = self._get_parsed_attrs()
        result = idrac_network_attribute_registry.filter_by_pattern(attrs, "VLan*")
        assert len(result) == 3
        for attr in result:
            assert attr['name'].startswith("VLan")

    def test_filter_by_pattern_link(self):
        attrs = self._get_parsed_attrs()
        result = idrac_network_attribute_registry.filter_by_pattern(attrs, "Link*")
        assert len(result) == 2
        names = [a['name'] for a in result]
        assert "LinkSpeed" in names
        assert "LinkDuplex" in names

    def test_filter_by_pattern_no_match(self):
        attrs = self._get_parsed_attrs()
        result = idrac_network_attribute_registry.filter_by_pattern(attrs, "NonExistent*")
        assert len(result) == 0

    def test_filter_by_pattern_wildcard_all(self):
        attrs = self._get_parsed_attrs()
        result = idrac_network_attribute_registry.filter_by_pattern(attrs, "*")
        assert len(result) == 6


class TestValidation:
    """Test validation helper functions."""

    def _get_parsed_attrs(self):
        return idrac_network_attribute_registry.parse_registry_attributes(SAMPLE_REGISTRY_DATA)

    def test_validate_valid_enum_attribute(self):
        attrs = self._get_parsed_attrs()
        results = idrac_network_attribute_registry.validate_attributes_against_registry(
            attrs, {"VLanMode": "Enabled"}
        )
        assert len(results) == 1
        assert results[0]['status'] == 'pass'
        assert results[0]['error_message'] is None

    def test_validate_invalid_attribute_name(self):
        attrs = self._get_parsed_attrs()
        results = idrac_network_attribute_registry.validate_attributes_against_registry(
            attrs, {"VLanMod": "Enabled"}
        )
        assert len(results) == 1
        assert results[0]['status'] == 'fail'
        assert "does not exist" in results[0]['error_message']
        assert results[0]['suggested_corrections'] is not None
        assert "VLanMode" in results[0]['suggested_corrections']

    def test_validate_invalid_enum_value(self):
        attrs = self._get_parsed_attrs()
        results = idrac_network_attribute_registry.validate_attributes_against_registry(
            attrs, {"VLanMode": "Invalid"}
        )
        assert len(results) == 1
        assert results[0]['status'] == 'fail'
        assert "Valid values" in results[0]['error_message']
        assert "Enabled" in results[0]['error_message']

    def test_validate_mixed_batch(self):
        attrs = self._get_parsed_attrs()
        results = idrac_network_attribute_registry.validate_attributes_against_registry(
            attrs, {
                "VLanMode": "Enabled",
                "VLanMod": "Enabled",
                "LinkSpeed": "InvalidSpeed",
            }
        )
        assert len(results) == 3
        statuses = {r['attribute_name']: r['status'] for r in results}
        assert statuses['VLanMode'] == 'pass'
        assert statuses['VLanMod'] == 'fail'
        assert statuses['LinkSpeed'] == 'fail'

    def test_validate_nonexistent_no_close_match(self):
        attrs = self._get_parsed_attrs()
        results = idrac_network_attribute_registry.validate_attributes_against_registry(
            attrs, {"ZZZZZZ": "value"}
        )
        assert len(results) == 1
        assert results[0]['status'] == 'fail'
        assert "does not exist" in results[0]['error_message']


class TestOutputFormats:
    """Test output format functions."""

    def _get_parsed_attrs(self):
        return idrac_network_attribute_registry.parse_registry_attributes(SAMPLE_REGISTRY_DATA)

    def test_json_format(self):
        attrs = self._get_parsed_attrs()
        result = idrac_network_attribute_registry.format_output(attrs, "json")
        assert isinstance(result, list)
        assert len(result) == 6

    def test_yaml_format(self):
        attrs = self._get_parsed_attrs()
        result = idrac_network_attribute_registry.format_output(attrs, "yaml")
        assert isinstance(result, str)
        assert "VLanMode" in result
        import yaml
        parsed = yaml.safe_load(result)
        assert isinstance(parsed, list)

    def test_table_format(self):
        attrs = self._get_parsed_attrs()
        result = idrac_network_attribute_registry.format_output(attrs, "table")
        assert isinstance(result, str)
        assert "Name" in result
        assert "Type" in result
        assert "VLanMode" in result

    def test_table_format_empty(self):
        result = idrac_network_attribute_registry.format_output([], "table")
        assert result == "No attributes found."
