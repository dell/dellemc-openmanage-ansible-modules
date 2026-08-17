# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.4
# Copyright (C) 2025 Dell Inc. or its subsidiaries. All Rights Reserved.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
iDRAC Log Export Utility Module

This module provides atomic export functionality for iDRAC Lifecycle Controller logs
in multiple formats (JSON, CSV, text) with proper error handling and metadata envelopes.
"""

import os
import json
import csv
import tempfile
from datetime import datetime
from typing import List, Dict, Any


class IDRACLogExporter:
    """Utility class for exporting iDRAC logs in multiple formats with atomic writes."""

    def __init__(self, export_path: str, export_format: str = "json"):
        """
        Initialize the log exporter.

        Args:
            export_path: Path where the export file should be written
            export_format: Format for export - 'json', 'csv', or 'text'
        """
        self.export_path = export_path
        self.export_format = export_format.lower()
        self.temp_path = f"{export_path}.tmp"

    def validate_permissions(self) -> bool:
        """
        Validate write permissions on the destination directory.

        Returns:
            bool: True if permissions are valid, False otherwise
        """
        try:
            # Resolve the absolute path to prevent path traversal
            abs_path = os.path.realpath(self.export_path)
            parent_dir = os.path.dirname(abs_path)

            # Check if parent directory exists and is writable
            if not os.path.exists(parent_dir):
                return False

            return os.access(parent_dir, os.W_OK)
        except (OSError, ValueError):
            return False

    def export_to_json(self, log_entries: List[Dict[str, Any]], metadata: Dict[str, Any]) -> int:
        """
        Export log entries to JSON format with metadata envelope.

        Args:
            log_entries: List of log entry dictionaries
            metadata: Metadata dictionary with server information

        Returns:
            int: Number of entries exported
        """
        export_data = {
            "metadata": metadata,
            "entries": log_entries
        }

        try:
            with open(self.temp_path, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)

            # Atomic rename
            os.rename(self.temp_path, self.export_path)

            # Set file permissions to 0o600 (owner read/write only)
            os.chmod(self.export_path, 0o600)

            return len(log_entries)
        except (IOError, OSError) as e:
            # Clean up temp file on failure
            if os.path.exists(self.temp_path):
                try:
                    os.remove(self.temp_path)
                except OSError:
                    pass
            raise e

    def export_to_csv(self, log_entries: List[Dict[str, Any]], metadata: Dict[str, Any]) -> int:
        """
        Export log entries to CSV format with header row.

        Args:
            log_entries: List of log entry dictionaries
            metadata: Metadata dictionary (not used in CSV but kept for consistency)

        Returns:
            int: Number of entries exported
        """
        if not log_entries:
            return 0

        try:
            # Get all unique keys from all entries for header
            fieldnames = set()
            for entry in log_entries:
                fieldnames.update(entry.keys())
            fieldnames = sorted(fieldnames)

            with open(self.temp_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(log_entries)

            # Atomic rename
            os.rename(self.temp_path, self.export_path)

            # Set file permissions to 0o600
            os.chmod(self.export_path, 0o600)

            return len(log_entries)
        except (IOError, OSError) as e:
            # Clean up temp file on failure
            if os.path.exists(self.temp_path):
                try:
                    os.remove(self.temp_path)
                except OSError:
                    pass
            raise e

    def export_to_text(self, log_entries: List[Dict[str, Any]], metadata: Dict[str, Any]) -> int:
        """
        Export log entries to text format with one entry per line.

        Format: [TIMESTAMP] [SEVERITY] [CATEGORY] MESSAGE (MessageId)

        Args:
            log_entries: List of log entry dictionaries
            metadata: Metadata dictionary (not used in text but kept for consistency)

        Returns:
            int: Number of entries exported
        """
        try:
            with open(self.temp_path, 'w') as f:
                for entry in log_entries:
                    timestamp = entry.get('Created', 'N/A')
                    severity = entry.get('Severity', 'N/A')
                    category = entry.get('Oem', {}).get('Dell', {}).get('DellLCLogEntry', {}).get('Category', 'N/A')
                    message = entry.get('Message', 'N/A')
                    message_id = entry.get('MessageId', 'N/A')

                    line = f"[{timestamp}] [{severity}] [{category}] {message} ({message_id})\n"
                    f.write(line)

            # Atomic rename
            os.rename(self.temp_path, self.export_path)

            # Set file permissions to 0o600
            os.chmod(self.export_path, 0o600)

            return len(log_entries)
        except (IOError, OSError) as e:
            # Clean up temp file on failure
            if os.path.exists(self.temp_path):
                try:
                    os.remove(self.temp_path)
                except OSError:
                    pass
            raise e

    def export(self, log_entries: List[Dict[str, Any]], metadata: Dict[str, Any]) -> int:
        """
        Export log entries in the specified format.

        Args:
            log_entries: List of log entry dictionaries
            metadata: Metadata dictionary with server information

        Returns:
            int: Number of entries exported

        Raises:
            ValueError: If export format is invalid
            OSError: If file operations fail
        """
        if not self.validate_permissions():
            raise OSError(f"Insufficient write permissions for export path: {self.export_path}")

        if self.export_format == "json":
            return self.export_to_json(log_entries, metadata)
        elif self.export_format == "csv":
            return self.export_to_csv(log_entries, metadata)
        elif self.export_format == "text":
            return self.export_to_text(log_entries, metadata)
        else:
            raise ValueError(f"Invalid export format: {self.export_format}. Must be 'json', 'csv', or 'text'")
