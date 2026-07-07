# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Copyright (C) 2026 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import os
import stat
import pytest
from ansible_collections.dellemc.openmanage.plugins.module_utils import idrac_log_exporter


ENTRIES = [
    {"Id": "1", "Created": "2026-01-01T00:00:00", "Severity": "OK", "Message": "All good"},
    {"Id": "2", "Created": "2026-01-02T00:00:00", "Severity": "Warning", "Message": "Disk warning"},
]
METADATA = {
    "server_model": "PowerEdge R760",
    "service_tag": "ABC1234",
    "idrac_version": "7.10.90.00",
    "export_timestamp": "2026-01-03T00:00:00",
    "filters_applied": {},
}


class TestExportToJson:

    def test_export_to_json_writes_metadata_envelope(self, tmp_path):
        export_path = str(tmp_path / "logs.json")
        idrac_log_exporter.export_to_json(ENTRIES, METADATA, export_path)
        with open(export_path) as fh:
            data = json.load(fh)
        assert data["metadata"] == METADATA
        assert data["entries"] == ENTRIES

    def test_export_to_json_atomic_no_tmp_left(self, tmp_path):
        export_path = str(tmp_path / "logs.json")
        idrac_log_exporter.export_to_json(ENTRIES, METADATA, export_path)
        assert not os.path.exists(export_path + ".tmp")
        assert os.path.exists(export_path)

    def test_export_to_json_permissions_0600(self, tmp_path):
        export_path = str(tmp_path / "logs.json")
        idrac_log_exporter.export_to_json(ENTRIES, METADATA, export_path)
        mode = stat.S_IMODE(os.stat(export_path).st_mode)
        assert mode == 0o600


class TestExportToCsv:

    def test_export_to_csv_writes_header_and_rows(self, tmp_path):
        export_path = str(tmp_path / "logs.csv")
        idrac_log_exporter.export_to_csv(ENTRIES, export_path)
        with open(export_path) as fh:
            lines = fh.read().splitlines()
        assert "Id" in lines[0]
        assert len(lines) == len(ENTRIES) + 1

    def test_export_to_csv_empty_entries(self, tmp_path):
        export_path = str(tmp_path / "logs_empty.csv")
        idrac_log_exporter.export_to_csv([], export_path)
        assert os.path.exists(export_path)


class TestExportToText:

    def test_export_to_text_one_entry_per_line(self, tmp_path):
        export_path = str(tmp_path / "logs.txt")
        idrac_log_exporter.export_to_text(ENTRIES, export_path)
        with open(export_path) as fh:
            lines = fh.read().splitlines()
        assert len(lines) == len(ENTRIES)


class TestAtomicWriteAndPermissions:

    def test_write_fails_if_exists_without_force(self, tmp_path):
        export_path = str(tmp_path / "existing.json")
        idrac_log_exporter.export_to_json(ENTRIES, METADATA, export_path)
        with pytest.raises(FileExistsError):
            idrac_log_exporter.export_to_json(ENTRIES, METADATA, export_path, force=False)

    def test_write_overwrites_with_force(self, tmp_path):
        export_path = str(tmp_path / "existing.json")
        idrac_log_exporter.export_to_json(ENTRIES, METADATA, export_path)
        idrac_log_exporter.export_to_json(ENTRIES[:1], METADATA, export_path, force=True)
        with open(export_path) as fh:
            data = json.load(fh)
        assert len(data["entries"]) == 1

    def test_write_cleans_up_tmp_on_failure(self, tmp_path, monkeypatch):
        export_path = str(tmp_path / "fail.json")

        def broken_dump(*args, **kwargs):
            raise ValueError("boom")

        monkeypatch.setattr(json, "dump", broken_dump)
        with pytest.raises(ValueError):
            idrac_log_exporter.export_to_json(ENTRIES, METADATA, export_path)
        assert not os.path.exists(export_path + ".tmp")
        assert not os.path.exists(export_path)


class TestPathTraversalPrevention:

    def test_rejects_path_with_dotdot(self):
        with pytest.raises(ValueError):
            idrac_log_exporter.validate_export_path("../../etc/passwd")

    def test_accepts_normal_path(self, tmp_path):
        safe_path = str(tmp_path / "logs.json")
        assert idrac_log_exporter.validate_export_path(safe_path) == os.path.realpath(safe_path)


class TestPermissionCheck:

    def test_check_write_permission_raises_when_no_access(self, monkeypatch, tmp_path):
        export_path = str(tmp_path / "logs.json")
        monkeypatch.setattr(os, "access", lambda path, mode: False)
        with pytest.raises(PermissionError):
            idrac_log_exporter.check_write_permission(export_path)

    def test_check_write_permission_passes_when_access(self, tmp_path):
        export_path = str(tmp_path / "logs.json")
        idrac_log_exporter.check_write_permission(export_path)
