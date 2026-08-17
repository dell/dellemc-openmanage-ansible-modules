# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.1
# Copyright (C) 2025 Dell Inc. or its subsidiaries. All Rights Reserved.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
Unit tests for iDRAC Message Registry Utility
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../..', 'plugins/module_utils'))
from idrac_utils.idrac_message_registry import IDRACMessageRegistry
from unittest.mock import MagicMock


class TestIDRACMessageRegistry:
    """Test suite for IDRACMessageRegistry class"""

    @pytest.fixture
    def mock_idrac_client(self):
        """Mock iDRAC client"""
        client = MagicMock()
        return client

    @pytest.fixture
    def sample_registry_data(self):
        """Sample MessageRegistry data"""
        return {
            "Id": "IDRAC",
            "Name": "IDRAC Message Registry",
            "Messages": {
                "LC001": {
                    "Description": "System temperature exceeded threshold",
                    "Resolution": "Check cooling system and reduce ambient temperature",
                    "Severity": "Critical",
                    "Message": "The system temperature has exceeded the threshold."
                },
                "LC002": {
                    "Description": "Power supply redundancy lost",
                    "Resolution": "Replace failed power supply or check power connections",
                    "Severity": "Warning",
                    "Message": "Power supply redundancy has been lost."
                }
            }
        }

    def test_discover_registries_success(self, mock_idrac_client):
        """Test successful registry discovery"""
        response = MagicMock()
        response.json_data = {
            "Members": [
                {"@odata.id": "/redfish/v1/Registries/IDRAC"},
                {"@odata.id": "/redfish/v1/Registries/Base"}
            ]
        }
        mock_idrac_client.invoke_request.return_value = response

        registry = IDRACMessageRegistry(mock_idrac_client)
        registries = registry.discover_registries()

        assert len(registries) == 2
        assert "/redfish/v1/Registries/IDRAC" in registries
        assert "/redfish/v1/Registries/Base" in registries

    def test_discover_registries_error(self, mock_idrac_client):
        """Test registry discovery on error"""
        mock_idrac_client.invoke_request.side_effect = Exception("API error")

        registry = IDRACMessageRegistry(mock_idrac_client)
        registries = registry.discover_registries()

        assert registries == []

    def test_fetch_idrac_registry_success(self, mock_idrac_client, sample_registry_data):
        """Test successful IDRAC registry fetch"""
        # Mock registry index response
        index_response = MagicMock()
        index_response.json_data = {
            "Id": "IDRAC",
            "Name": "IDRAC Message Registry",
            "Location": [
                {"Uri": "/redfish/v1/Registries/IDRAC/IDRAC.json"}
            ]
        }

        # Mock registry data response
        registry_response = MagicMock()
        registry_response.json_data = sample_registry_data

        mock_idrac_client.invoke_request.side_effect = [index_response, registry_response]

        registry = IDRACMessageRegistry(mock_idrac_client)
        result = registry.fetch_idrac_registry()

        assert result is not None
        assert result["Id"] == "IDRAC"
        assert "LC001" in result["Messages"]

    def test_fetch_idrac_registry_not_found(self, mock_idrac_client):
        """Test IDRAC registry fetch when not found"""
        mock_idrac_client.invoke_request.side_effect = Exception("Not found")

        registry = IDRACMessageRegistry(mock_idrac_client)
        result = registry.fetch_idrac_registry()

        assert result is None

    def test_get_message_info_cached(self, mock_idrac_client, sample_registry_data):
        """Test getting message info from cached registry"""
        registry = IDRACMessageRegistry(mock_idrac_client)
        registry.registry_cache["/redfish/v1/Registries/IDRAC"] = sample_registry_data

        message_info = registry.get_message_info("LC001")

        assert message_info["description"] == "System temperature exceeded threshold"
        assert message_info["resolution"] == "Check cooling system and reduce ambient temperature"
        assert message_info["severity"] == "Critical"

    def test_get_message_info_not_found(self, mock_idrac_client):
        """Test getting message info when MessageId not found"""
        registry = IDRACMessageRegistry(mock_idrac_client)
        registry.registry_cache["/redfish/v1/Registries/IDRAC"] = {"Messages": {}}

        message_info = registry.get_message_info("UNKNOWN")

        assert message_info["description"] == ""
        assert message_info["resolution"] == ""
        assert message_info["severity"] == ""

    def test_enrich_log_entry(self, mock_idrac_client, sample_registry_data):
        """Test enriching a single log entry"""
        registry = IDRACMessageRegistry(mock_idrac_client)
        registry.registry_cache["/redfish/v1/Registries/IDRAC"] = sample_registry_data

        entry = {
            "MessageId": "LC001",
            "Message": "System temperature exceeded threshold",
            "Severity": "Critical"
        }

        enriched = registry.enrich_log_entry(entry)

        assert "MessageDescription" in enriched
        assert "MessageResolution" in enriched
        assert enriched["MessageDescription"] == "System temperature exceeded threshold"
        assert enriched["MessageResolution"] == "Check cooling system and reduce ambient temperature"

    def test_enrich_log_entry_no_message_id(self, mock_idrac_client):
        """Test enriching log entry without MessageId"""
        registry = IDRACMessageRegistry(mock_idrac_client)

        entry = {
            "Message": "Some message",
            "Severity": "Warning"
        }

        enriched = registry.enrich_log_entry(entry)

        assert enriched == entry  # Should return unchanged

    def test_enrich_log_entries(self, mock_idrac_client, sample_registry_data):
        """Test enriching multiple log entries"""
        registry = IDRACMessageRegistry(mock_idrac_client)
        registry.registry_cache["/redfish/v1/Registries/IDRAC"] = sample_registry_data

        entries = [
            {"MessageId": "LC001", "Message": "Temp exceeded"},
            {"MessageId": "LC002", "Message": "Power lost"},
            {"MessageId": "UNKNOWN", "Message": "Unknown message"}
        ]

        enriched = registry.enrich_log_entries(entries)

        assert len(enriched) == 3
        assert enriched[0]["MessageDescription"] == "System temperature exceeded threshold"
        assert enriched[1]["MessageDescription"] == "Power supply redundancy lost"
        assert enriched[2]["MessageDescription"] == ""  # Unknown message

    def test_registry_cache_persistence(self, mock_idrac_client, sample_registry_data):
        """Test that registry cache persists across calls"""
        registry = IDRACMessageRegistry(mock_idrac_client)
        registry.registry_cache["/redfish/v1/Registries/IDRAC"] = sample_registry_data

        # First call should use cache
        info1 = registry.get_message_info("LC001")

        # Second call should also use cache (no additional API calls)
        info2 = registry.get_message_info("LC001")

        assert info1 == info2
        assert mock_idrac_client.invoke_request.call_count == 0  # No API calls made
