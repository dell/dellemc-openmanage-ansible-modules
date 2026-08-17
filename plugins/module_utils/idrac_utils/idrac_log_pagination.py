# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.1
# Copyright (C) 2025 Dell Inc. or its subsidiaries. All Rights Reserved.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
iDRAC Log Pagination Utility Module

This module provides streaming pagination for iDRAC Lifecycle Controller logs
with circuit breaker support and exponential backoff retry for transient failures.
"""

import time
from typing import Generator, Dict, Any, Optional, Callable
from datetime import datetime
from dateutil import parser as date_parser


class IDRACLogPagination:
    """Utility class for paginated iDRAC log retrieval with circuit breaker."""

    def __init__(self, idrac_client, max_entries: Optional[int] = None):
        """
        Initialize the log pagination utility.

        Args:
            idrac_client: iDRAC Redfish API client
            max_entries: Maximum number of entries to retrieve (circuit breaker)
        """
        self.idrac_client = idrac_client
        self.max_entries = max_entries
        self.entries_retrieved = 0

    def paginate_lc_logs(
        self,
        base_uri: str,
        date_start: Optional[str] = None,
        retry_count: int = 3,
        retry_delay: int = 1
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Generator function for paginated LC log retrieval.

        Args:
            base_uri: Base URI for LC log entries (e.g., /redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Lclog/Entries)
            date_start: Optional ISO 8601 string for early pagination termination
            retry_count: Number of retry attempts for transient failures
            retry_delay: Initial delay in seconds (exponential backoff)

        Yields:
            Dict[str, Any]: Individual log entries

        Raises:
            Exception: If all retry attempts fail
        """
        current_uri = base_uri
        retry_attempts = 0
        current_delay = retry_delay

        while current_uri:
            # Check circuit breaker
            if self.max_entries and self.entries_retrieved >= self.max_entries:
                break

            # Fetch current page with retry logic
            try:
                response = self.idrac_client.invoke_request(current_uri, 'GET')
                response_data = response.json_data

                # Process entries
                entries = response_data.get('Members', [])

                for entry in entries:
                    # Check circuit breaker
                    if self.max_entries and self.entries_retrieved >= self.max_entries:
                        return

                    # Early termination for date_start
                    if date_start:
                        entry_time_str = entry.get('Created', '')
                        if entry_time_str:
                            try:
                                entry_dt = date_parser.parse(entry_time_str)
                                start_dt = date_parser.parse(date_start)
                                if entry_dt < start_dt:
                                    return  # Stop pagination
                            except (ValueError, TypeError):
                                pass  # Continue if date parsing fails

                    self.entries_retrieved += 1
                    yield entry

                # Get next page link
                current_uri = response_data.get('Members@odata.nextLink')

                # Reset retry counter on success
                retry_attempts = 0
                current_delay = retry_delay

            except Exception as e:
                retry_attempts += 1

                if retry_attempts >= retry_count:
                    raise Exception(f"Failed to retrieve LC logs after {retry_count} attempts: {str(e)}")

                # Exponential backoff
                time.sleep(current_delay)
                current_delay *= 2

    def get_total_entries_count(self, base_uri: str) -> int:
        """
        Get total number of LC log entries without fetching all entries.

        Args:
            base_uri: Base URI for LC log entries

        Returns:
            int: Total number of entries
        """
        try:
            # Use $top=0 to get count without entries
            uri = f"{base_uri}?$top=0"
            response = self.idrac_client.invoke_request(uri, 'GET')
            response_data = response.json_data

            return response_data.get('Members@odata.count', 0)
        except Exception:
            return 0

    def get_oldest_entry_timestamp(self, base_uri: str) -> Optional[str]:
        """
        Get the oldest entry timestamp.

        Args:
            base_uri: Base URI for LC log entries

        Returns:
            Optional[str]: ISO 8601 timestamp of oldest entry, or None
        """
        try:
            # Use $top=1 with ascending order
            uri = f"{base_uri}?$top=1&$orderby=Created asc"
            response = self.idrac_client.invoke_request(uri, 'GET')
            response_data = response.json_data

            entries = response_data.get('Members', [])
            if entries:
                return entries[0].get('Created')
        except Exception:
            pass

        return None

    def get_newest_entry_timestamp(self, base_uri: str) -> Optional[str]:
        """
        Get the newest entry timestamp.

        Args:
            base_uri: Base URI for LC log entries

        Returns:
            Optional[str]: ISO 8601 timestamp of newest entry, or None
        """
        try:
            # Use $top=1 (default is descending)
            uri = f"{base_uri}?$top=1"
            response = self.idrac_client.invoke_request(uri, 'GET')
            response_data = response.json_data

            entries = response_data.get('Members', [])
            if entries:
                return entries[0].get('Created')
        except Exception:
            pass

        return None

    def get_severity_breakdown(self, base_uri: str) -> Dict[str, int]:
        """
        Get count of entries per severity level.

        Args:
            base_uri: Base URI for LC log entries

        Returns:
            Dict[str, int]: Dictionary with severity counts
        """
        severity_counts = {
            'Critical': 0,
            'Warning': 0,
            'OK': 0
        }

        try:
            for severity in ['Critical', 'Warning', 'OK']:
                uri = f"{base_uri}?$top=0&$filter=Severity eq '{severity}'"
                response = self.idrac_client.invoke_request(uri, 'GET')
                response_data = response.json_data
                count = response_data.get('Members@odata.count', 0)
                severity_counts[severity] = count
        except Exception:
            pass

        return severity_counts
