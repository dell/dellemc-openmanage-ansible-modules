# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Copyright (C) 2026 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Reusable multi-format export utility for iDRAC log-related modules."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import csv
import json
import os

EXPORT_FILE_MODE = 0o600


def validate_export_path(export_path):
    """
    Resolve export_path and reject paths containing '../' traversal sequences.

    :param export_path: user-supplied destination file path
    :return: the resolved real path
    :raises ValueError: if the path contains traversal sequences
    """
    if ".." in export_path.split(os.sep):
        raise ValueError("export_path must not contain '..' path traversal sequences")
    return os.path.realpath(export_path)


def check_write_permission(export_path):
    """
    Validate write permission on the destination directory using os.access().

    :param export_path: destination file path
    :raises PermissionError: if the directory is not writable
    """
    directory = os.path.dirname(export_path) or "."
    if not os.access(directory, os.W_OK):
        raise PermissionError("No write permission for directory: {0}".format(directory))


def _atomic_write(export_path, write_func, force=False):
    """
    Write to export_path atomically via a .tmp file and rename, cleaning up
    the .tmp file on any failure.

    :param export_path: destination file path
    :param write_func: callable(file_handle) performing the actual write
    :param force: overwrite export_path if it already exists
    :raises FileExistsError: if export_path exists and force is False
    """
    resolved_path = validate_export_path(export_path)
    if os.path.exists(resolved_path) and not force:
        raise FileExistsError("export_path already exists: {0}".format(resolved_path))
    check_write_permission(resolved_path)
    tmp_path = resolved_path + ".tmp"
    try:
        with open(tmp_path, "w") as file_handle:
            write_func(file_handle)
        os.chmod(tmp_path, EXPORT_FILE_MODE)
        os.replace(tmp_path, resolved_path)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def export_to_json(entries, metadata, export_path, force=False):
    """
    Export LC log entries to JSON with a metadata envelope.

    :param entries: list of LC log entry dicts
    :param metadata: dict with server_model, service_tag, idrac_version,
                      export_timestamp, filters_applied
    :param export_path: destination file path
    :param force: overwrite export_path if it already exists
    """
    envelope = {"metadata": metadata, "entries": entries}

    def write_func(file_handle):
        json.dump(envelope, file_handle, indent=2)

    _atomic_write(export_path, write_func, force=force)


def export_to_csv(entries, export_path, force=False):
    """
    Export LC log entries to CSV with a header row and all fields.

    :param entries: list of LC log entry dicts
    :param export_path: destination file path
    :param force: overwrite export_path if it already exists
    """
    fieldnames = []
    for entry in entries:
        for key in entry.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    if not fieldnames:
        fieldnames = ["Id", "Created", "Severity", "Message"]

    def write_func(file_handle):
        writer = csv.DictWriter(file_handle, fieldnames=fieldnames)
        writer.writeheader()
        for entry in entries:
            writer.writerow(entry)

    _atomic_write(export_path, write_func, force=force)


def export_to_text(entries, export_path, force=False):
    """
    Export LC log entries to plain text, one entry per line.

    :param entries: list of LC log entry dicts
    :param export_path: destination file path
    :param force: overwrite export_path if it already exists
    """
    def write_func(file_handle):
        for entry in entries:
            file_handle.write("{0}\n".format(json.dumps(entry)))

    _atomic_write(export_path, write_func, force=force)
