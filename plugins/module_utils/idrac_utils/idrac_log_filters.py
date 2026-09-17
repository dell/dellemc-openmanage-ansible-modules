# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 11.0.0
# Copyright (C) 2018-2026 Dell Inc. or its subsidiaries. All Rights Reserved.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
iDRAC Log Filter Utility Module

This module provides chainable filter functions for iDRAC Lifecycle Controller logs
with support for date range, severity, category, and message content filtering.
"""

from typing import List, Dict, Any, Callable, Optional
from datetime import datetime

UTC_OFFSET = '+00:00'


def _parse_iso_datetime(value: Optional[str]) -> Optional[datetime]:
    """Parse an ISO 8601 string (with optional trailing 'Z') into a datetime."""
    return datetime.fromisoformat(value.replace('Z', UTC_OFFSET)) if value else None


def _build_date_filter(
    start_dt: Optional[datetime], end_dt: Optional[datetime]
) -> Callable[[Dict[str, Any]], bool]:
    """Build a filter function that keeps entries within the given date range."""
    def date_filter(entry: Dict[str, Any]) -> bool:
        entry_time_str = entry.get('Created', '')
        if not entry_time_str:
            return False

        try:
            entry_dt = datetime.fromisoformat(entry_time_str.replace('Z', UTC_OFFSET))
        except (ValueError, TypeError):
            return False

        if start_dt and entry_dt < start_dt:
            return False
        if end_dt and entry_dt > end_dt:
            return False

        return True

    return date_filter


class IDRACLogFilter:
    """Utility class for filtering iDRAC log entries with chainable operations."""

    def __init__(self):
        """Initialize the log filter."""
        self.filters: List[Callable[[Dict[str, Any]], bool]] = []

    def add_date_filter(self, date_start: Optional[str] = None, date_end: Optional[str] = None) -> 'IDRACLogFilter':
        """
        Add date range filter to the pipeline.

        Args:
            date_start: ISO 8601 string for start date (inclusive)
            date_end: ISO 8601 string for end date (inclusive)

        Returns:
            IDRACLogFilter: Self for method chaining
        """
        if not (date_start or date_end):
            return self

        start_dt = _parse_iso_datetime(date_start)
        end_dt = _parse_iso_datetime(date_end)
        self.filters.append(_build_date_filter(start_dt, end_dt))

        return self

    def add_severity_filter(self, severity_list: List[str]) -> 'IDRACLogFilter':
        """
        Add severity filter to the pipeline.

        Args:
            severity_list: List of severity values to include (e.g., ['Critical', 'Warning'])

        Returns:
            IDRACLogFilter: Self for method chaining
        """
        if severity_list:
            severity_list_upper = [s.upper() for s in severity_list]

            def severity_filter(entry: Dict[str, Any]) -> bool:
                entry_severity = entry.get('Severity', '').upper()
                return entry_severity in severity_list_upper

            self.filters.append(severity_filter)

        return self

    def add_category_filter(self, category_list: List[str]) -> 'IDRACLogFilter':
        """
        Add Dell OEM category filter to the pipeline.

        Args:
            category_list: List of Dell OEM category values to include

        Returns:
            IDRACLogFilter: Self for method chaining
        """
        if category_list:
            def category_filter(entry: Dict[str, Any]) -> bool:
                entry_category = entry.get('Oem', {}).get('Dell', {}).get(
                    'DellLCLogEntry', {}).get('Category', '')
                return entry_category in category_list

            self.filters.append(category_filter)

        return self

    def add_message_filter(self, message_contains: str) -> 'IDRACLogFilter':
        """
        Add message content filter to the pipeline (case-insensitive substring match).

        Args:
            message_contains: Substring to search for in log messages

        Returns:
            IDRACLogFilter: Self for method chaining
        """
        if message_contains:
            search_term = message_contains.lower()

            def message_filter(entry: Dict[str, Any]) -> bool:
                entry_message = entry.get('Message', '').lower()
                return search_term in entry_message

            self.filters.append(message_filter)

        return self

    def apply(self, log_entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Apply all registered filters to the log entries.

        Args:
            log_entries: List of log entry dictionaries

        Returns:
            List[Dict[str, Any]]: Filtered log entries
        """
        filtered_entries = log_entries

        for filter_func in self.filters:
            filtered_entries = [entry for entry in filtered_entries if filter_func(entry)]

        return filtered_entries

    def validate_date_range(self, date_start: Optional[str], date_end: Optional[str]) -> bool:
        """
        Validate that date_end is not earlier than date_start.

        Args:
            date_start: ISO 8601 string for start date
            date_end: ISO 8601 string for end date

        Returns:
            bool: True if date range is valid, False otherwise

        Raises:
            ValueError: If date_end is earlier than date_start
        """
        if date_start and date_end:
            start_dt = datetime.fromisoformat(date_start.replace('Z', UTC_OFFSET))
            end_dt = datetime.fromisoformat(date_end.replace('Z', UTC_OFFSET))

            if end_dt < start_dt:
                raise ValueError("date_end must not be earlier than date_start")

        return True

    def reset(self) -> 'IDRACLogFilter':
        """
        Reset all filters from the pipeline.

        Returns:
            IDRACLogFilter: Self for method chaining
        """
        self.filters = []
        return self
