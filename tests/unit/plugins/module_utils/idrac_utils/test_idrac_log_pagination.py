# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.1
# Copyright (C) 2025 Dell Inc. or its subsidiaries. All Rights Reserved.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
Unit tests for iDRAC Log Pagination Utility
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../..', 'plugins/module_utils'))
from idrac_utils.idrac_log_pagination import IDRACLogPagination
from unittest.mock import MagicMock, Mock
from datetime import datetime


class TestIDRACLogPagination:
    """Test suite for IDRACLogPagination class"""

    @pytest.fixture
    def mock_idrac_client(self):
        """Mock iDRAC client"""
        client = MagicMock()
        return client

    @pytest.fixture
    def sample_log_entries(self):
        """Sample log entries for testing"""
        return [
            {
                "Created": "2026-08-17T10:00:00Z",
                "Severity": "Critical",
                "Message": "System temperature exceeded threshold",
                "MessageId": "LC001"
            },
            {
                "Created": "2026-08-17T11:00:00Z",
                "Severity": "Warning",
                "Message": "Power supply redundancy lost",
                "MessageId": "LC002"
            },
            {
                "Created": "2026-08-17T12:00:00Z",
                "Severity": "OK",
                "Message": "System boot completed successfully",
                "MessageId": "LC003"
            }
        ]

    @pytest.fixture
    def mock_response(self, sample_log_entries):
        """Mock API response"""
        response = MagicMock()
        response.json_data = {
            "Members": sample_log_entries,
            "Members@odata.nextLink": None
        }
        return response

    def test_paginate_single_page(self, mock_idrac_client, sample_log_entries, mock_response):
        """Test pagination with single page of results"""
        mock_idrac_client.invoke_request.return_value = mock_response

        pagination = IDRACLogPagination(mock_idrac_client)
        entries = list(pagination.paginate_lc_logs("/redfish/v1/LogServices/Lclog/Entries"))

        assert len(entries) == 3
        assert entries[0]["MessageId"] == "LC001"
        assert pagination.entries_retrieved == 3

    def test_paginate_multiple_pages(self, mock_idrac_client, sample_log_entries):
        """Test pagination with multiple pages"""
        # First page
        first_response = MagicMock()
        first_response.json_data = {
            "Members": sample_log_entries[:2],
            "Members@odata.nextLink": "/redfish/v1/LogServices/Lclog/Entries?$skip=2"
        }

        # Second page
        second_response = MagicMock()
        second_response.json_data = {
            "Members": sample_log_entries[2:],
            "Members@odata.nextLink": None
        }

        mock_idrac_client.invoke_request.side_effect = [first_response, second_response]

        pagination = IDRACLogPagination(mock_idrac_client)
        entries = list(pagination.paginate_lc_logs("/redfish/v1/LogServices/Lclog/Entries"))

        assert len(entries) == 3
        assert pagination.entries_retrieved == 3
        assert mock_idrac_client.invoke_request.call_count == 2

    def test_circuit_breaker_max_entries(self, mock_idrac_client, sample_log_entries, mock_response):
        """Test circuit breaker with max_entries limit"""
        mock_idrac_client.invoke_request.return_value = mock_response

        pagination = IDRACLogPagination(mock_idrac_client, max_entries=2)
        entries = list(pagination.paginate_lc_logs("/redfish/v1/LogServices/Lclog/Entries"))

        assert len(entries) == 2  # Only 2 entries due to circuit breaker
        assert pagination.entries_retrieved == 2

    def test_early_termination_date_start(self, mock_idrac_client, sample_log_entries):
        """Test early pagination termination when date_start is reached"""
        # Create entries with different timestamps
        entries_early = [
            {
                "Created": "2026-08-16T10:00:00Z",  # Before date_start
                "Severity": "Critical",
                "Message": "Old entry",
                "MessageId": "LC000"
            }
        ]
        entries_late = sample_log_entries  # After date_start

        first_response = MagicMock()
        first_response.json_data = {
            "Members": entries_early,
            "Members@odata.nextLink": "/redfish/v1/LogServices/Lclog/Entries?$skip=1"
        }

        second_response = MagicMock()
        second_response.json_data = {
            "Members": entries_late,
            "Members@odata.nextLink": None
        }

        mock_idrac_client.invoke_request.side_effect = [first_response, second_response]

        pagination = IDRACLogPagination(mock_idrac_client)
        entries = list(pagination.paginate_lc_logs(
            "/redfish/v1/LogServices/Lclog/Entries",
            date_start="2026-08-17T00:00:00Z"
        ))

        # Should stop at early entry before date_start
        assert len(entries) == 0

    def test_retry_on_transient_failure(self, mock_idrac_client, sample_log_entries, mock_response):
        """Test exponential backoff retry on transient failures"""
        # First call fails, second succeeds
        mock_idrac_client.invoke_request.side_effect = [
            Exception("Connection timeout"),
            mock_response
        ]

        pagination = IDRACLogPagination(mock_idrac_client)
        entries = list(pagination.paginate_lc_logs(
            "/redfish/v1/LogServices/Lclog/Entries",
            retry_count=2,
            retry_delay=0.1  # Short delay for testing
        ))

        assert len(entries) == 3
        assert mock_idrac_client.invoke_request.call_count == 2

    def test_retry_exhaustion(self, mock_idrac_client):
        """Test failure after retry exhaustion"""
        mock_idrac_client.invoke_request.side_effect = Exception("Connection timeout")

        pagination = IDRACLogPagination(mock_idrac_client)

        with pytest.raises(Exception, match="Failed to retrieve LC logs after 3 attempts"):
            list(pagination.paginate_lc_logs(
                "/redfish/v1/LogServices/Lclog/Entries",
                retry_count=3,
                retry_delay=0.1
            ))

    def test_get_total_entries_count(self, mock_idrac_client):
        """Test getting total entries count"""
        response = MagicMock()
        response.json_data = {"Members@odata.count": 42}
        mock_idrac_client.invoke_request.return_value = response

        pagination = IDRACLogPagination(mock_idrac_client)
        count = pagination.get_total_entries_count("/redfish/v1/LogServices/Lclog/Entries")

        assert count == 42
        mock_idrac_client.invoke_request.assert_called_once()

    def test_get_total_entries_count_error(self, mock_idrac_client):
        """Test getting total entries count on error"""
        mock_idrac_client.invoke_request.side_effect = Exception("API error")

        pagination = IDRACLogPagination(mock_idrac_client)
        count = pagination.get_total_entries_count("/redfish/v1/LogServices/Lclog/Entries")

        assert count == 0

    def test_get_oldest_entry_timestamp(self, mock_idrac_client):
        """Test getting oldest entry timestamp"""
        response = MagicMock()
        response.json_data = {
            "Members": [
                {
                    "Created": "2026-08-16T10:00:00Z",
                    "MessageId": "LC000"
                }
            ]
        }
        mock_idrac_client.invoke_request.return_value = response

        pagination = IDRACLogPagination(mock_idrac_client)
        timestamp = pagination.get_oldest_entry_timestamp("/redfish/v1/LogServices/Lclog/Entries")

        assert timestamp == "2026-08-16T10:00:00Z"

    def test_get_oldest_entry_timestamp_error(self, mock_idrac_client):
        """Test getting oldest entry timestamp on error"""
        mock_idrac_client.invoke_request.side_effect = Exception("API error")

        pagination = IDRACLogPagination(mock_idrac_client)
        timestamp = pagination.get_oldest_entry_timestamp("/redfish/v1/LogServices/Lclog/Entries")

        assert timestamp is None

    def test_get_newest_entry_timestamp(self, mock_idrac_client):
        """Test getting newest entry timestamp"""
        response = MagicMock()
        response.json_data = {
            "Members": [
                {
                    "Created": "2026-08-17T12:00:00Z",
                    "MessageId": "LC003"
                }
            ]
        }
        mock_idrac_client.invoke_request.return_value = response

        pagination = IDRACLogPagination(mock_idrac_client)
        timestamp = pagination.get_newest_entry_timestamp("/redfish/v1/LogServices/Lclog/Entries")

        assert timestamp == "2026-08-17T12:00:00Z"

    def test_get_newest_entry_timestamp_error(self, mock_idrac_client):
        """Test getting newest entry timestamp on error"""
        mock_idrac_client.invoke_request.side_effect = Exception("API error")

        pagination = IDRACLogPagination(mock_idrac_client)
        timestamp = pagination.get_newest_entry_timestamp("/redfish/v1/LogServices/Lclog/Entries")

        assert timestamp is None

    def test_get_severity_breakdown(self, mock_idrac_client):
        """Test getting severity breakdown"""
        # Mock responses for each severity query
        critical_response = MagicMock()
        critical_response.json_data = {"Members@odata.count": 5}

        warning_response = MagicMock()
        warning_response.json_data = {"Members@odata.count": 3}

        ok_response = MagicMock()
        ok_response.json_data = {"Members@odata.count": 12}

        mock_idrac_client.invoke_request.side_effect = [
            critical_response,
            warning_response,
            ok_response
        ]

        pagination = IDRACLogPagination(mock_idrac_client)
        breakdown = pagination.get_severity_breakdown("/redfish/v1/LogServices/Lclog/Entries")

        assert breakdown == {
            'Critical': 5,
            'Warning': 3,
            'OK': 12
        }

    def test_get_severity_breakdown_error(self, mock_idrac_client):
        """Test getting severity breakdown on error"""
        mock_idrac_client.invoke_request.side_effect = Exception("API error")

        pagination = IDRACLogPagination(mock_idrac_client)
        breakdown = pagination.get_severity_breakdown("/redfish/v1/LogServices/Lclog/Entries")

        assert breakdown == {
            'Critical': 0,
            'Warning': 0,
            'OK': 0
        }

    def test_empty_entries_response(self, mock_idrac_client):
        """Test pagination with empty entries response"""
        response = MagicMock()
        response.json_data = {
            "Members": [],
            "Members@odata.nextLink": None
        }
        mock_idrac_client.invoke_request.return_value = response

        pagination = IDRACLogPagination(mock_idrac_client)
        entries = list(pagination.paginate_lc_logs("/redfish/v1/LogServices/Lclog/Entries"))

        assert len(entries) == 0
        assert pagination.entries_retrieved == 0

    def test_pagination_with_both_circuit_breakers(self, mock_idrac_client):
        """Test pagination with both max_entries and date_start circuit breakers"""
        # Create entries spanning multiple days - all after date_start
        entries = [
            {
                "Created": "2026-08-17T10:00:00Z",
                "Severity": "Warning",
                "Message": "New entry",
                "MessageId": "LC001"
            },
            {
                "Created": "2026-08-17T11:00:00Z",
                "Severity": "Critical",
                "Message": "Another new entry",
                "MessageId": "LC002"
            }
        ]

        response = MagicMock()
        response.json_data = {
            "Members": entries,
            "Members@odata.nextLink": None
        }
        mock_idrac_client.invoke_request.return_value = response

        pagination = IDRACLogPagination(mock_idrac_client, max_entries=1)
        entries = list(pagination.paginate_lc_logs(
            "/redfish/v1/LogServices/Lclog/Entries",
            date_start="2026-08-17T00:00:00Z"
        ))

        # Should stop at max_entries (1) after date_start filter
        assert len(entries) == 1
        assert entries[0]["MessageId"] == "LC001"
