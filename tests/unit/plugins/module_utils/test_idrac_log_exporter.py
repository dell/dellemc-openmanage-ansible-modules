import csv
import json
import os

import pytest

from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_log_exporter import (
    ExportPathError, export_entries, export_to_csv, export_to_json,
    export_to_text, validate_export_path)


SAMPLE_ENTRIES = [
    {"Id": "1", "Created": "2026-01-01T00:00:00Z", "Severity": "Critical",
     "Message": "Disk failure", "MessageId": "STOR001", "Category": "Storage"},
    {"Id": "2", "Created": "2026-01-02T00:00:00Z", "Severity": "OK",
     "Message": "Boot complete", "MessageId": "SYS001", "Category": "SystemHealth"},
]


class TestValidateExportPath:

    def test_valid_path_new_file(self, tmp_path):
        target = tmp_path / "export.json"
        resolved = validate_export_path(str(target))
        assert resolved == os.path.realpath(str(target))

    def test_existing_file_without_force_raises(self, tmp_path):
        target = tmp_path / "export.json"
        target.write_text("{}")
        with pytest.raises(ExportPathError):
            validate_export_path(str(target), force=False)

    def test_existing_file_with_force_succeeds(self, tmp_path):
        target = tmp_path / "export.json"
        target.write_text("{}")
        resolved = validate_export_path(str(target), force=True)
        assert resolved == os.path.realpath(str(target))

    def test_path_traversal_rejected(self, tmp_path):
        traversal_path = str(tmp_path / ".." / "escape.json")
        with pytest.raises(ExportPathError):
            validate_export_path(traversal_path)

    def test_no_write_permission_raises(self, tmp_path, monkeypatch):
        target = tmp_path / "export.json"
        monkeypatch.setattr(os, "access", lambda path, mode: False)
        with pytest.raises(ExportPathError):
            validate_export_path(str(target))


class TestExportToJson:

    def test_export_to_json_writes_metadata_envelope(self, tmp_path):
        target = tmp_path / "export.json"
        metadata = {"server_model": "R740", "service_tag": "ABC1234"}
        result_path = export_to_json(SAMPLE_ENTRIES, str(target), metadata=metadata)
        with open(result_path) as handle:
            data = json.load(handle)
        assert data["server_model"] == "R740"
        assert data["service_tag"] == "ABC1234"
        assert data["entries"] == SAMPLE_ENTRIES

    def test_export_to_json_no_tmp_file_left_behind(self, tmp_path):
        target = tmp_path / "export.json"
        export_to_json(SAMPLE_ENTRIES, str(target))
        assert not os.path.exists(str(target) + ".tmp")
        assert os.path.exists(str(target))


class TestExportToCsv:

    def test_export_to_csv_writes_header_and_rows(self, tmp_path):
        target = tmp_path / "export.csv"
        result_path = export_to_csv(SAMPLE_ENTRIES, str(target))
        with open(result_path, newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
        assert rows[0]["Id"] == "1"
        assert rows[1]["Message"] == "Boot complete"


class TestExportToText:

    def test_export_to_text_one_entry_per_line(self, tmp_path):
        target = tmp_path / "export.txt"
        result_path = export_to_text(SAMPLE_ENTRIES, str(target))
        with open(result_path) as handle:
            lines = handle.readlines()
        assert len(lines) == 2
        assert "Disk failure" in lines[0]


class TestExportEntriesDispatch:

    def test_export_entries_defaults_to_json(self, tmp_path):
        target = tmp_path / "export"
        result_path = export_entries(SAMPLE_ENTRIES, str(target), export_format="json")
        with open(result_path) as handle:
            data = json.load(handle)
        assert data["entries"] == SAMPLE_ENTRIES

    def test_export_entries_invalid_format_raises(self, tmp_path):
        target = tmp_path / "export.xml"
        with pytest.raises(ValueError):
            export_entries(SAMPLE_ENTRIES, str(target), export_format="xml")

    def test_export_entries_cleans_up_tmp_on_failure(self, tmp_path, monkeypatch):
        target = tmp_path / "export.json"

        def _raise(*args, **kwargs):
            raise IOError("disk full")

        monkeypatch.setattr(json, "dump", _raise)
        with pytest.raises(IOError):
            export_to_json(SAMPLE_ENTRIES, str(target))
        assert not os.path.exists(str(target) + ".tmp")
