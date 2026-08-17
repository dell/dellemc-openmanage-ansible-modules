# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.4
# Copyright (C) 2025 Dell Inc. or its subsidiaries. All Rights Reserved.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
iDRAC Message Registry Utility Module

This module provides MessageRegistry resolution for iDRAC log entries,
enriching them with message descriptions and resolutions.
"""

from typing import Dict, Any, Optional


class IDRACMessageRegistry:
    """Utility class for MessageRegistry resolution and enrichment."""

    def __init__(self, idrac_client):
        """
        Initialize the MessageRegistry utility.

        Args:
            idrac_client: iDRAC Redfish API client
        """
        self.idrac_client = idrac_client
        self.registry_cache: Dict[str, Dict[str, Any]] = {}

    def discover_registries(self) -> list:
        """
        Discover available MessageRegistry resources.

        Returns:
            list: List of registry URIs
        """
        try:
            response = self.idrac_client.invoke_request('/redfish/v1/Registries', 'GET')
            response_data = response.json_data

            members = response_data.get('Members', [])
            registries = []
            for member in members:
                uri = member.get('@odata.id')
                if uri:
                    registries.append(uri)

            return registries
        except Exception:
            return []

    def fetch_idrac_registry(self) -> Optional[Dict[str, Any]]:
        """
        Fetch the IDRAC MessageRegistry.

        Returns:
            Optional[Dict[str, Any]]: Registry data or None if unavailable
        """
        # Try common IDRAC registry paths
        registry_paths = [
            '/redfish/v1/Registries/IDRAC',
            '/redfish/v1/Registries/Base',
            '/redfish/v1/Registries/Manager',
        ]

        for path in registry_paths:
            try:
                response = self.idrac_client.invoke_request(path, 'GET')
                response_data = response.json_data

                # Check if this is an IDRAC registry
                if 'IDRAC' in response_data.get('Id', '') or 'Idrac' in response_data.get('Name', ''):
                    # Get the location URI
                    location = response_data.get('Location', [])
                    if location and isinstance(location, list):
                        location_uri = location[0].get('Uri') or location[0].get('Language', {}).get('Uri')
                        if location_uri:
                            # Fetch the actual registry data
                            registry_response = self.idrac_client.invoke_request(location_uri, 'GET')
                            registry_data = registry_response.json_data
                            self.registry_cache[path] = registry_data
                            return registry_data
            except Exception:
                continue

        return None

    def get_message_info(self, message_id: str) -> Dict[str, Any]:
        """
        Get message information (description, resolution) for a given MessageId.

        Args:
            message_id: The MessageId from a log entry (e.g., "LC001", "IDRAC.2.16.LOG007")

        Returns:
            Dict[str, Any]: Dictionary with 'description' and 'resolution' keys
        """
        # Ensure registry is loaded
        if not self.registry_cache:
            self.fetch_idrac_registry()

        # Search all cached registries
        for registry_data in self.registry_cache.values():
            messages = registry_data.get('Messages', {})
            if message_id in messages:
                message_info = messages[message_id]
                return {
                    'description': message_info.get('Description', ''),
                    'resolution': message_info.get('Resolution', ''),
                    'severity': message_info.get('Severity', ''),
                    'message': message_info.get('Message', '')
                }

        # Return empty info if not found
        return {
            'description': '',
            'resolution': '',
            'severity': '',
            'message': ''
        }

    def enrich_log_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich a log entry with MessageRegistry information.

        Args:
            entry: Log entry dictionary

        Returns:
            Dict[str, Any]: Enriched log entry with additional fields
        """
        message_id = entry.get('MessageId', '')
        if not message_id:
            return entry

        message_info = self.get_message_info(message_id)

        # Add enriched fields
        enriched_entry = entry.copy()
        enriched_entry['MessageDescription'] = message_info.get('description')
        enriched_entry['MessageResolution'] = message_info.get('resolution')

        return enriched_entry

    def enrich_log_entries(self, entries: list) -> list:
        """
        Enrich multiple log entries with MessageRegistry information.

        Args:
            entries: List of log entry dictionaries

        Returns:
            list: List of enriched log entries
        """
        return [self.enrich_log_entry(entry) for entry in entries]
