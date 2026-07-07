# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 10.0.1
# Copyright (C) 2026 Dell Inc. or its subsidiaries. All Rights Reserved.

# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:

#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.

#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

"""Reusable export utility for writing iDRAC log entries to JSON, CSV, or text files.

This module is intentionally generic so it can be reused by future iDRAC
log-related Ansible modules beyond idrac_lifecycle_controller_logs.
"""

import csv
import json
import os

EXPORT_FORMAT_JSON = "json"
EXPORT_FORMAT_CSV = "csv"
EXPORT_FORMAT_TEXT = "text"
SUPPORTED_EXPORT_FORMATS = (EXPORT_FORMAT_JSON, EXPORT_FORMAT_CSV, EXPORT_FORMAT_TEXT)
EXPORT_FILE_MODE = 0o600
CSV_FIELD_NAMES = [
    "Id", "Created", "Severity", "Message", "MessageId",
    "Category", "message_description", "message_resolution",
]


class ExportPathError(ValueError):
    """Raised when the export path fails validation (permissions or traversal)."""


def validate_export_path(export_path, force=False):
    """Resolve and validate the export destination path before writing.

    Args:
    export_path -- user-supplied destination file path.
    force -- when False, raises if a file already exists at export_path.

    Raises:
    ExportPathError -- on path traversal, missing write permission, or
        pre-existing file without force=True.

    Returns:
    The resolved real path to write to.
    """
    resolved_path = os.path.realpath(export_path)
    if ".." in export_path.split(os.sep):
        raise ExportPathError("export_path must not contain '..' path traversal sequences.")
    destination_dir = os.path.dirname(resolved_path) or "."
    if not os.access(destination_dir, os.W_OK):
        raise ExportPathError(
            "No write permission for destination directory: {0}".format(destination_dir))
    if os.path.exists(resolved_path) and not force:
        raise ExportPathError(
            "export_path already exists: {0}. Set force=true to overwrite.".format(resolved_path))
    return resolved_path


def _atomic_write(resolved_path, write_fn):
    """Write content atomically via a temporary file and rename-on-success.

    Args:
    resolved_path -- final destination path for the export file.
    write_fn -- callable accepting an open file handle to write content.
    """
    tmp_path = "{0}.tmp".format(resolved_path)
    try:
        with open(tmp_path, "w", newline="") as tmp_file:
            write_fn(tmp_file)
        os.chmod(tmp_path, EXPORT_FILE_MODE)
        os.replace(tmp_path, resolved_path)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def export_to_json(entries, export_path, metadata=None, force=False):
    """Export log entries to a JSON file with a metadata envelope.

    Args:
    entries -- list of log entry dictionaries to export.
    export_path -- destination file path.
    metadata -- optional dict merged into the envelope (server_model, service_tag,
        idrac_version, export_timestamp, filters_applied, etc.).
    force -- overwrite export_path if it already exists.
    """
    resolved_path = validate_export_path(export_path, force=force)
    envelope = dict(metadata or {})
    envelope["entries"] = entries

    def _write(handle):
        json.dump(envelope, handle, indent=2, default=str)

    _atomic_write(resolved_path, _write)
    return resolved_path


def export_to_csv(entries, export_path, force=False, field_names=None):
    """Export log entries to a CSV file with a header row and all fields.

    Args:
    entries -- list of log entry dictionaries to export.
    export_path -- destination file path.
    force -- overwrite export_path if it already exists.
    field_names -- optional override of the CSV column order.
    """
    resolved_path = validate_export_path(export_path, force=force)
    columns = field_names or CSV_FIELD_NAMES

    def _write(handle):
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for entry in entries:
            writer.writerow(entry)

    _atomic_write(resolved_path, _write)
    return resolved_path


def export_to_text(entries, export_path, force=False, line_template=None):
    """Export log entries to a plain text file, one entry per line.

    Args:
    entries -- list of log entry dictionaries to export.
    export_path -- destination file path.
    force -- overwrite export_path if it already exists.
    line_template -- optional format string using entry field names.
    """
    resolved_path = validate_export_path(export_path, force=force)
    template = line_template or "{Created} [{Severity}] {Message}"

    def _write(handle):
        for entry in entries:
            safe_entry = {key: entry.get(key, "") for key in
                          ("Created", "Severity", "Message", "Id", "Category")}
            handle.write(template.format(**safe_entry))
            handle.write("\n")

    _atomic_write(resolved_path, _write)
    return resolved_path


def export_entries(entries, export_path, export_format=EXPORT_FORMAT_JSON,
                   metadata=None, force=False):
    """Dispatch to the appropriate export function based on export_format.

    Args:
    entries -- list of log entry dictionaries to export.
    export_path -- destination file path.
    export_format -- one of 'json', 'csv', 'text'.
    metadata -- optional metadata envelope for JSON export.
    force -- overwrite export_path if it already exists.

    Raises:
    ValueError -- when export_format is not supported.
    """
    if export_format not in SUPPORTED_EXPORT_FORMATS:
        raise ValueError(
            "Unsupported export_format '{0}'. Must be one of {1}.".format(
                export_format, SUPPORTED_EXPORT_FORMATS))
    if export_format == EXPORT_FORMAT_JSON:
        return export_to_json(entries, export_path, metadata=metadata, force=force)
    if export_format == EXPORT_FORMAT_CSV:
        return export_to_csv(entries, export_path, force=force)
    return export_to_text(entries, export_path, force=force)
