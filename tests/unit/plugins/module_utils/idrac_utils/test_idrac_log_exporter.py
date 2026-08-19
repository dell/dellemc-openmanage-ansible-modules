# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.1
# Copyright (C) 2018-2026 Dell Inc. or its subsidiaries. All Rights Reserved.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
Unit tests for iDRAC Log Export Utility
"""

import pytest
import os
import json
import csv
import tempfile
import shutil
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../..', 'plugins/module_utils'))
from idrac_utils.idrac_log_exporter import IDRACLogExporter


class TestIDRACLogExporter:
    """Test suite for IDRACLogExporter class"""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

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
            }
        ]

    @pytest.fixture
    def sample_metadata(self):
        """Sample metadata for testing"""
        return {
            "server_model": "PowerEdge R760",
            "service_tag": "SVCTAG123",
            "idrac_version": "2.00.05.10",
            "export_timestamp": datetime.now().isoformat(),
            "filters_applied": {"severity": ["Critical"]},
            "exported_entry_count": 2
        }

    def test_validate_permissions_valid_directory(self, temp_dir):
        """Test permission validation on valid writable directory"""
        export_path = os.path.join(temp_dir, "test_export.json")
        exporter = IDRACLogExporter(export_path, "json")
        assert exporter.validate_permissions() is True

    def test_validate_permissions_invalid_directory(self):
        """Test permission validation on non-existent directory"""
        export_path = "/nonexistent/directory/test_export.json"
        exporter = IDRACLogExporter(export_path, "json")
        assert exporter.validate_permissions() is False

    def test_export_to_json_with_metadata(self, temp_dir, sample_log_entries, sample_metadata):
        """Test JSON export with metadata envelope"""
        export_path = os.path.join(temp_dir, "test_export.json")
        exporter = IDRACLogExporter(export_path, "json")

        count = exporter.export_to_json(sample_log_entries, sample_metadata)

        assert count == 2
        assert os.path.exists(export_path)

        # Verify file permissions
        file_stat = os.stat(export_path)
        assert oct(file_stat.st_mode)[-3:] == "600"

        # Verify content structure
        with open(export_path, 'r') as f:
            data = json.load(f)

        assert "metadata" in data
        assert "entries" in data
        assert data["metadata"]["server_model"] == "PowerEdge R760"
        assert len(data["entries"]) == 2

    def test_export_to_csv_with_header(self, temp_dir, sample_log_entries, sample_metadata):
        """Test CSV export with header row"""
        export_path = os.path.join(temp_dir, "test_export.csv")
        exporter = IDRACLogExporter(export_path, "csv")

        count = exporter.export_to_csv(sample_log_entries, sample_metadata)

        assert count == 2
        assert os.path.exists(export_path)

        # Verify file permissions
        file_stat = os.stat(export_path)
        assert oct(file_stat.st_mode)[-3:] == "600"

        # Verify CSV structure
        with open(export_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 2
        assert "Created" in rows[0]
        assert "Severity" in rows[0]

    def test_export_to_text_format(self, temp_dir, sample_log_entries, sample_metadata):
        """Test text export with one entry per line format"""
        export_path = os.path.join(temp_dir, "test_export.txt")
        exporter = IDRACLogExporter(export_path, "text")

        count = exporter.export_to_text(sample_log_entries, sample_metadata)

        assert count == 2
        assert os.path.exists(export_path)

        # Verify file permissions
        file_stat = os.stat(export_path)
        assert oct(file_stat.st_mode)[-3:] == "600"

        # Verify text format
        with open(export_path, 'r') as f:
            lines = f.readlines()

        assert len(lines) == 2
        assert "[2026-08-17T10:00:00Z] [Critical] [SystemHealth]" in lines[0]
        assert "(LC001)" in lines[0]

    def test_export_atomic_write_semantics(self, temp_dir, sample_log_entries, sample_metadata):
        """Test atomic write semantics - temp file renamed on success"""
        export_path = os.path.join(temp_dir, "test_export.json")
        exporter = IDRACLogExporter(export_path, "json")

        exporter.export_to_json(sample_log_entries, sample_metadata)

        # Temp file should not exist after successful export
        assert not os.path.exists(exporter.temp_path)
        # Final file should exist
        assert os.path.exists(export_path)

    def test_export_temp_file_cleanup_on_failure(self, temp_dir, sample_log_entries, sample_metadata):
        """Test temp file cleanup on write failure"""
        # Create a file at the export path to simulate failure
        export_path = os.path.join(temp_dir, "test_export.json")
        os.makedirs(os.path.dirname(export_path), exist_ok=True)

        # Create a directory at the export path to cause write failure
        os.makedirs(export_path, exist_ok=True)

        exporter = IDRACLogExporter(export_path, "json")

        # This should fail and clean up temp file
        with pytest.raises(OSError):
            exporter.export_to_json(sample_log_entries, sample_metadata)

        # Temp file should be cleaned up
        assert not os.path.exists(exporter.temp_path)

    def test_export_invalid_format(self, temp_dir, sample_log_entries, sample_metadata):
        """Test export with invalid format raises ValueError"""
        export_path = os.path.join(temp_dir, "test_export.xyz")
        exporter = IDRACLogExporter(export_path, "xyz")

        with pytest.raises(ValueError, match="Invalid export format"):
            exporter.export(sample_log_entries, sample_metadata)

    def test_export_empty_entries(self, temp_dir, sample_metadata):
        """Test export with empty log entries"""
        export_path = os.path.join(temp_dir, "test_export.json")
        exporter = IDRACLogExporter(export_path, "json")

        count = exporter.export_to_json([], sample_metadata)

        assert count == 0
        assert os.path.exists(export_path)

        with open(export_path, 'r') as f:
            data = json.load(f)

        assert data["entries"] == []

    def test_export_method_format_selection(self, temp_dir, sample_log_entries, sample_metadata):
        """Test export method correctly selects format"""
        # Test JSON
        json_path = os.path.join(temp_dir, "test.json")
        json_exporter = IDRACLogExporter(json_path, "json")
        json_count = json_exporter.export(sample_log_entries, sample_metadata)
        assert json_count == 2
        assert os.path.exists(json_path)

        # Test CSV
        csv_path = os.path.join(temp_dir, "test.csv")
        csv_exporter = IDRACLogExporter(csv_path, "csv")
        csv_count = csv_exporter.export(sample_log_entries, sample_metadata)
        assert csv_count == 2
        assert os.path.exists(csv_path)

        # Test text
        txt_path = os.path.join(temp_dir, "test.txt")
        txt_exporter = IDRACLogExporter(txt_path, "text")
        txt_count = txt_exporter.export(sample_log_entries, sample_metadata)
        assert txt_count == 2
        assert os.path.exists(txt_path)
