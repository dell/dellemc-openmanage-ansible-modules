# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.1
# Copyright (C) 2018-2026 Dell Inc. or its subsidiaries. All Rights Reserved.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
Unit tests for iDRAC Log Filter Utility
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../..', 'plugins/module_utils'))
from idrac_utils.idrac_log_filters import IDRACLogFilter


class TestIDRACLogFilter:
    """Test suite for IDRACLogFilter class"""

    @pytest.fixture
    def sample_log_entries(self):
        """Sample log entries for testing"""
        return [
            {
                "Created": "2026-08-17T10:00:00Z",
                "Severity": "Critical",
                "Message": "System temperature exceeded threshold",
                "MessageId": "LC001",
                "Oem": {
                    "Dell": {
                        "DellLCLogEntry": {
                            "Category": "SystemHealth"
                        }
                    }
                }
            },
            {
                "Created": "2026-08-17T11:00:00Z",
                "Severity": "Warning",
                "Message": "Power supply redundancy lost",
                "MessageId": "LC002",
                "Oem": {
                    "Dell": {
                        "DellLCLogEntry": {
                            "Category": "Power"
                        }
                    }
                }
            },
            {
                "Created": "2026-08-17T12:00:00Z",
                "Severity": "OK",
                "Message": "System boot completed successfully",
                "MessageId": "LC003",
                "Oem": {
                    "Dell": {
                        "DellLCLogEntry": {
                            "Category": "System"
                        }
                    }
                }
            },
            {
                "Created": "2026-08-16T10:00:00Z",
                "Severity": "Critical",
                "Message": "Firmware update failed",
                "MessageId": "LC004",
                "Oem": {
                    "Dell": {
                        "DellLCLogEntry": {
                            "Category": "Updates"
                        }
                    }
                }
            }
        ]

    def test_date_filter_start_only(self, sample_log_entries):
        """Test date filter with only start date"""
        log_filter = IDRACLogFilter()
        log_filter.add_date_filter(date_start="2026-08-17T00:00:00Z")

        filtered = log_filter.apply(sample_log_entries)

        assert len(filtered) == 3  # Only entries from Aug 17
        assert all(entry["Created"] >= "2026-08-17T00:00:00Z" for entry in filtered)

    def test_date_filter_end_only(self, sample_log_entries):
        """Test date filter with only end date"""
        log_filter = IDRACLogFilter()
        log_filter.add_date_filter(date_end="2026-08-17T11:30:00Z")

        filtered = log_filter.apply(sample_log_entries)

        assert len(filtered) == 3  # All entries before 11:30 on Aug 17 (including Aug 16)
        assert all(entry["Created"] <= "2026-08-17T11:30:00Z" for entry in filtered)

    def test_date_filter_range(self, sample_log_entries):
        """Test date filter with both start and end date"""
        log_filter = IDRACLogFilter()
        log_filter.add_date_filter(
            date_start="2026-08-17T10:30:00Z",
            date_end="2026-08-17T11:30:00Z"
        )

        filtered = log_filter.apply(sample_log_entries)

        assert len(filtered) == 1  # Only the 11:00 entry
        assert filtered[0]["MessageId"] == "LC002"

    def test_date_filter_invalid_range(self):
        """Test date filter validation with invalid range"""
        log_filter = IDRACLogFilter()

        with pytest.raises(ValueError, match="date_end must not be earlier than date_start"):
            log_filter.validate_date_range(
                date_start="2026-08-17T12:00:00Z",
                date_end="2026-08-17T10:00:00Z"
            )

    def test_severity_filter_single(self, sample_log_entries):
        """Test severity filter with single severity"""
        log_filter = IDRACLogFilter()
        log_filter.add_severity_filter(["Critical"])

        filtered = log_filter.apply(sample_log_entries)

        assert len(filtered) == 2
        assert all(entry["Severity"] == "Critical" for entry in filtered)

    def test_severity_filter_multiple(self, sample_log_entries):
        """Test severity filter with multiple severities"""
        log_filter = IDRACLogFilter()
        log_filter.add_severity_filter(["Critical", "Warning"])

        filtered = log_filter.apply(sample_log_entries)

        assert len(filtered) == 3
        assert all(entry["Severity"] in ["Critical", "Warning"] for entry in filtered)

    def test_severity_filter_case_insensitive(self, sample_log_entries):
        """Test severity filter is case-insensitive"""
        log_filter = IDRACLogFilter()
        log_filter.add_severity_filter(["critical"])  # lowercase

        filtered = log_filter.apply(sample_log_entries)

        assert len(filtered) == 2
        assert all(entry["Severity"] == "Critical" for entry in filtered)

    def test_category_filter_single(self, sample_log_entries):
        """Test category filter with single category"""
        log_filter = IDRACLogFilter()
        log_filter.add_category_filter(["SystemHealth"])

        filtered = log_filter.apply(sample_log_entries)

        assert len(filtered) == 1
        assert filtered[0]["MessageId"] == "LC001"

    def test_category_filter_multiple(self, sample_log_entries):
        """Test category filter with multiple categories"""
        log_filter = IDRACLogFilter()
        log_filter.add_category_filter(["SystemHealth", "Power"])

        filtered = log_filter.apply(sample_log_entries)

        assert len(filtered) == 2
        assert all(
            entry["Oem"]["Dell"]["DellLCLogEntry"]["Category"] in ["SystemHealth", "Power"]
            for entry in filtered
        )

    def test_message_filter(self, sample_log_entries):
        """Test message content filter"""
        log_filter = IDRACLogFilter()
        log_filter.add_message_filter("temperature")

        filtered = log_filter.apply(sample_log_entries)

        assert len(filtered) == 1
        assert "temperature" in filtered[0]["Message"].lower()

    def test_message_filter_case_insensitive(self, sample_log_entries):
        """Test message filter is case-insensitive"""
        log_filter = IDRACLogFilter()
        log_filter.add_message_filter("TEMPERATURE")  # uppercase

        filtered = log_filter.apply(sample_log_entries)

        assert len(filtered) == 1
        assert "temperature" in filtered[0]["Message"].lower()

    def test_combined_filters(self, sample_log_entries):
        """Test multiple filters combined"""
        log_filter = IDRACLogFilter()
        log_filter.add_date_filter(date_start="2026-08-17T00:00:00Z")
        log_filter.add_severity_filter(["Critical", "Warning"])
        log_filter.add_category_filter(["SystemHealth", "Power"])

        filtered = log_filter.apply(sample_log_entries)

        assert len(filtered) == 2
        # Should include Critical SystemHealth and Warning Power from Aug 17
        message_ids = [entry["MessageId"] for entry in filtered]
        assert "LC001" in message_ids
        assert "LC002" in message_ids

    def test_filter_chain_method_chaining(self, sample_log_entries):
        """Test method chaining for filter operations"""
        log_filter = (IDRACLogFilter()
                      .add_date_filter(date_start="2026-08-17T00:00:00Z")
                      .add_severity_filter(["Critical"])
                      .add_category_filter(["SystemHealth"]))

        filtered = log_filter.apply(sample_log_entries)

        assert len(filtered) == 1
        assert filtered[0]["MessageId"] == "LC001"

    def test_filter_reset(self, sample_log_entries):
        """Test filter reset functionality"""
        log_filter = IDRACLogFilter()
        log_filter.add_severity_filter(["Critical"])

        first_filtered = log_filter.apply(sample_log_entries)
        assert len(first_filtered) == 2

        log_filter.reset()
        second_filtered = log_filter.apply(sample_log_entries)
        assert len(second_filtered) == 4  # All entries after reset

    def test_empty_filter_pipeline(self, sample_log_entries):
        """Test with no filters applied"""
        log_filter = IDRACLogFilter()

        filtered = log_filter.apply(sample_log_entries)

        assert len(filtered) == 4  # All entries pass through

    def test_filter_no_matching_entries(self, sample_log_entries):
        """Test filter that produces no results"""
        log_filter = IDRACLogFilter()
        log_filter.add_category_filter(["NonExistentCategory"])

        filtered = log_filter.apply(sample_log_entries)

        assert len(filtered) == 0

    def test_filter_empty_log_entries(self):
        """Test filter with empty log entries"""
        log_filter = IDRACLogFilter()
        log_filter.add_severity_filter(["Critical"])

        filtered = log_filter.apply([])

        assert len(filtered) == 0

    def test_filter_entry_missing_created_field(self):
        """Test filter handles entries missing Created field"""
        log_entries = [
            {
                "Severity": "Critical",
                "Message": "Test message"
                # Missing Created field
            }
        ]

        log_filter = IDRACLogFilter()
        log_filter.add_date_filter(date_start="2026-08-17T00:00:00Z")

        filtered = log_filter.apply(log_entries)

        assert len(filtered) == 0  # Entry without Created field is filtered out

    def test_filter_entry_missing_severity_field(self):
        """Test filter handles entries missing Severity field"""
        log_entries = [
            {
                "Created": "2026-08-17T10:00:00Z",
                "Message": "Test message"
                # Missing Severity field
            }
        ]

        log_filter = IDRACLogFilter()
        log_filter.add_severity_filter(["Critical"])

        filtered = log_filter.apply(log_entries)

        assert len(filtered) == 0  # Entry without Severity field is filtered out
