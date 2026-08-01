#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Module
# Version 10.0.1
# Copyright (C) 2018-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_lifecycle_controller_logs
short_description: Export Lifecycle Controller logs to a network share or local path.
version_added: "2.1.0"
description:
  - Export Lifecycle Controller logs to a given network share or local path.
  - Supports filtered log queries by date range, severity, category, and message text,
    as well as metadata-only queries, without requiring a network share.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
  share_name:
    description:
      - Network share or local path.
      - CIFS, NFS network share types are supported.
      - Required when exporting logs to a network share or local path via the legacy export flow.
      - Not used when performing a filtered log query (I(date_start), I(date_end), I(severity),
        I(category), I(message_contains), or I(fetch_metadata_only)).
    type: str
  share_user:
    type: str
    description: Network share user in the format 'user@domain' or 'domain\\user' if user is
      part of a domain else 'user'. This option is mandatory for CIFS Network Share.
  share_password:
    type: str
    description: Network share user password. This option is mandatory for CIFS Network Share.
    aliases: ['share_pwd']
  job_wait:
    description: Whether to wait for the running job completion or not.
    type: bool
    default: true
  date_start:
    type: str
    description:
      - Filter LC log entries with a C(Created) timestamp on or after this ISO 8601 date.
      - Mutually inclusive with I(date_end), I(severity), I(category), I(message_contains), and I(fetch_metadata_only)
        for a filtered log query. Cannot be combined with I(share_name).
  date_end:
    type: str
    description:
      - Filter LC log entries with a C(Created) timestamp on or before this ISO 8601 date.
      - Must not be earlier than I(date_start).
  severity:
    type: list
    elements: str
    choices: [OK, Warning, Critical]
    description: Filter LC log entries by one or more severity levels.
  category:
    type: list
    elements: str
    choices: [Storage, Updates, Audit, Configuration, WorkNotes, SystemHealth]
    description: Filter LC log entries by one or more Dell OEM categories.
  message_contains:
    type: str
    description: Filter LC log entries by a case-insensitive substring match on the C(Message) field.
  fetch_metadata_only:
    type: bool
    description:
      - When C(true), return LC log service metadata (entry count, oldest/newest timestamps,
        storage utilization, severity breakdown) without fetching individual log entries.
  max_entries:
    type: int
    description: Maximum number of LC log entries to retrieve during a filtered query.
  export_format:
    type: str
    choices: [json, csv, text]
    description:
      - Format used to export filtered LC log entries when I(export_path) is specified.
      - Defaults to C(json) when I(export_path) is set without an explicit I(export_format).
  export_path:
    type: str
    description:
      - Local file path to export the filtered LC log entries to.
      - Mutually exclusive with I(share_name) and I(fetch_metadata_only).
  force:
    type: bool
    default: false
    description: Overwrite I(export_path) if a file already exists at that location.
  clear_logs:
    type: bool
    description:
      - Explicit confirmation required to clear the LC log. Must be set to C(true) to execute the clear operation.
      - Mutually exclusive with I(share_name), I(fetch_metadata_only), and I(insert_comment).
  clear_only_if_export_succeeded:
    type: bool
    description:
      - When C(true), aborts the clear operation unless the export step (I(export_path)) completes successfully.
      - Requires I(clear_logs) to be set.
  insert_comment:
    type: str
    description:
      - Custom comment text (maximum 256 characters) to insert as a new LC log entry.
      - Mutually exclusive with I(share_name), I(fetch_metadata_only), I(clear_logs), and I(export_path).
  storage_threshold_pct:
    type: int
    default: 80
    description:
      - Storage utilization percentage threshold used to generate a capacity warning.
      - Applies to I(fetch_metadata_only) and I(clear_logs) operations.

requirements:
  - "omsdk >= 1.2.488"
  - "python >= 3.9.6"
author:
  - "Rajeev Arakkal (@rajeevarakkal)"
  - "Anooja Vardhineni (@anooja-vardhineni)"
  - "Trisha Datta (@trisha-dell)"
notes:
  - This module requires 'Administrator' privilege for I(idrac_user).
  - Exporting data to a local share is supported only on iDRAC9-based PowerEdge Servers and later.
  - Run this module from a system that has direct access to Dell iDRAC.
  - This module supports both IPv4 and IPv6 address for I(idrac_ip).
  - This module does not support C(check_mode).
  - No job will be created when exporting data to a local share in iDRAC9 and iDRAC 10.
  - "Filter syntax reference:"
  - "  - I(date_start) / I(date_end): ISO 8601 format, e.g. C(2026-01-15T00:00:00Z)."
  - "  - I(severity): one or more of C(OK), C(Warning), C(Critical)."
  - "  - I(category): one or more of C(Storage), C(Updates), C(Audit), C(Configuration), C(WorkNotes), C(SystemHealth)."
  - "Troubleshooting:"
  - "  - No logs returned: verify I(date_start)/I(date_end) bound an actual log window."
  - "  - No logs returned: verify I(severity)/I(category)/I(message_contains) are not overly restrictive."
  - "  - Filter syntax errors: confirm I(date_start)/I(date_end) are valid ISO 8601 strings and I(date_end) is not earlier than I(date_start)."
  - "  - Export failures: verify the destination directory in I(export_path) exists and is writable; use I(force) to overwrite an existing file."
  - "  - Permission errors: log clear and comment insertion require 'Administrator' privilege; the iDRAC returns HTTP 403 if the account lacks permission."
  - "  - Firmware version incompatibility: filtered queries and management operations require iDRAC9 >= 7.10.90.00 or iDRAC10 >= 1.20.50.50."
"""

EXAMPLES = r'''
---
- name: Export lifecycle controller logs to NFS share.
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "192.168.0.0:/nfsfileshare"

- name: Export lifecycle controller logs to CIFS share.
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "\\\\192.168.0.2\\share"
    share_user: "share_user_name"
    share_password: "share_user_pwd"

- name: Export lifecycle controller logs to LOCAL path.
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/example/export_lc"

- name: (UC-1) Incident log collection - query LC logs filtered by date range and severity.
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    date_start: "2026-01-01T00:00:00Z"
    date_end: "2026-01-31T23:59:59Z"
    severity:
      - Critical
      - Warning

- name: (UC-2) Fleet firmware audit - query LC logs filtered by category and message text.
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    category:
      - Storage
    message_contains: "disk failure"
    max_entries: 500

- name: Fetch LC log service metadata only.
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    fetch_metadata_only: true

- name: (UC-3) SIEM export - export filtered LC logs to a local JSON file for SIEM ingestion.
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    date_start: "2026-01-01T00:00:00Z"
    export_format: "json"
    export_path: "/tmp/lc_logs_export.json"

- name: Export filtered LC logs to CSV, overwriting any existing file.
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    severity:
      - Critical
    export_format: "csv"
    export_path: "/tmp/lc_logs_export.csv"
    force: true

- name: (UC-4) Compliance log rotation - export LC logs before clearing them (safety gate enabled).
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    export_path: "/tmp/lc_logs_archive.json"
    clear_logs: true
    clear_only_if_export_succeeded: true

- name: Insert a custom comment into the LC log.
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    insert_comment: "Maintenance window started at 02:00 UTC"
'''

RETURN = """
---
msg:
  type: str
  description: Status of the export lifecycle controller logs job.
  returned: always
  sample: "Successfully exported the lifecycle controller logs."
lc_logs_status:
  description: Status of the export operation along with job details and file path.
  returned: success
  type: dict
  sample: {
    "ElapsedTimeSinceCompletion": "0",
    "InstanceID": "JID_274774785395",
    "JobStartTime": "NA",
    "JobStatus": "Completed",
    "JobUntilTime": "NA",
    "Message": "LCL Export was successful",
    "MessageArguments": "NA",
    "MessageID": "LC022",
    "Name": "LC Export",
    "PercentComplete": "100",
    "Status": "Success",
    "file": "192.168.0.0:/nfsfileshare/190.168.0.1_20210728_133437_LC_Log.log",
    "retval": true
  }
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
      "code": "Base.1.0.GeneralError",
      "message": "A general error has occurred. See ExtendedInfo for more information.",
      "@Message.ExtendedInfo": [
        {
          "MessageId": "GEN1234",
          "RelatedProperties": [],
          "Message": "Unable to process the request because an error occurred.",
          "MessageArgs": [],
          "Severity": "Critical",
          "Resolution": "Retry the operation. If the issue persists, contact your system administrator."
        }
      ]
    }
  }
lc_logs:
  description: List of LC log entries matching the applied filters. Returned only for a filtered log query.
  returned: success, when I(fetch_metadata_only) is not set
  type: list
  sample: [
    {
      "Id": "1",
      "Created": "2026-01-15T10:00:00Z",
      "Severity": "Critical",
      "Message": "Disk failure detected",
      "MessageId": "STOR001"
    }
  ]
lc_log_metadata:
  description: LC log service metadata. Returned only when I(fetch_metadata_only) is C(true).
  returned: success, when I(fetch_metadata_only) is set
  type: dict
  sample: {
    "total_entries": 1250,
    "oldest_entry_timestamp": "2025-01-01T00:00:00Z",
    "newest_entry_timestamp": "2026-01-15T10:00:00Z",
    "storage_utilization_pct": 62.5,
    "severity_breakdown": {"OK": 900, "Warning": 300, "Critical": 50}
  }
export_path:
  description: Resolved file path the filtered LC log entries were exported to. Returned only when I(export_path) is set.
  returned: success, when I(export_path) is set
  type: str
  sample: "/tmp/lc_logs_export.json"
lc_log_clear_status:
  description: Status of the log clear operation. Returned only when I(clear_logs) is C(true).
  returned: success, when I(clear_logs) is set
  type: dict
  sample: {
    "pre_clear_count": 1250,
    "post_clear_count": 0,
    "entries_cleared": 1250,
    "pre_clear_utilization_pct": 62.5,
    "post_clear_utilization_pct": 0.0
  }
lc_log_comment:
  description: Details of the inserted LC log comment entry. Returned only when I(insert_comment) is set.
  returned: success, when I(insert_comment) is set
  type: dict
  sample: {"Id": "12345", "Created": "2026-01-15T10:00:00Z"}
"""


import socket
import json
import copy
import datetime
from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection, idrac_auth_params
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.\
    idrac_lifecycle_controller_logs_utils import (
        IDRACLifecycleControllerLogs, validate_lc_log_firmware_version,
        check_lc_log_service_available, fetch_lc_logs, fetch_lc_log_metadata,
        discover_message_registry, enrich_with_message_registry,
        clear_lc_logs, insert_lc_log_comment, DEFAULT_STORAGE_THRESHOLD_PCT)
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_log_exporter import (
    export_entries, ExportPathError)
try:
    from omsdk.sdkfile import file_share_manager
    from omsdk.sdkcreds import UserCredentials
except ImportError:
    pass
EXPORT_LC_LOGS = '/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellLCService/Actions/DellLCService.ExportLCLog'
SUCCESS_MSG = "Successfully exported the lifecycle controller logs."
SCHEDULE_MSG = "The export lifecycle controller log job is submitted successfully."
NO_CHANGES_FOUND_MSG = "No changes found to be applied."
CHANGES_FOUND_MSG = "Changes found to be applied."


def get_user_credentials(module):
    share_username = module.params['share_user']
    share_password = module.params['share_password']
    work_group = None
    if share_username is not None and "@" in share_username:
        username_domain = share_username.split("@")
        share_username = username_domain[0]
        work_group = username_domain[1]
    elif share_username is not None and "\\" in share_username:
        username_domain = share_username.split("\\")
        work_group = username_domain[0]
        share_username = username_domain[1]
    share = file_share_manager.create_share_obj(share_path=module.params['share_name'],
                                                creds=UserCredentials(share_username, share_password,
                                                                      work_group=work_group), isFolder=True)
    return share


def run_export_lc_logs(idrac, module):
    """
    Export Lifecycle Controller Log to the given file share

    Args:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    lclog_file_name_format = "%ip_%Y%m%d_%H%M%S_LC_Log.log"
    share_username = module.params.get('share_user')
    if (share_username is not None) and ("@" in share_username or "\\" in share_username):
        myshare = get_user_credentials(module)
    else:
        myshare = file_share_manager.create_share_obj(share_path=module.params['share_name'],
                                                      creds=UserCredentials(module.params['share_user'],
                                                                            module.params['share_password']),
                                                      isFolder=True)
    data = socket.getaddrinfo(module.params["idrac_ip"], module.params["idrac_port"])
    if "AF_INET6" == data[0][0]._name_:
        lclog_file_name_format = get_file_name(module)
    lc_log_file = myshare.new_file(lclog_file_name_format)
    job_wait = module.params['job_wait']
    msg = idrac.log_mgr.lclog_export(lc_log_file, job_wait)
    return msg


def get_file_name(module):
    file_name = None
    ip = copy.deepcopy(module.params["idrac_ip"])
    file_format = "{ip}_%Y%m%d_%H%M%S_LC_Log.log".format(ip=ip.replace(":", ".").replace("..", "."))
    current_date = datetime.datetime.now()
    current_date_str = current_date.strftime("%Y%m%d_%H%M%S")
    file_name = file_format.replace("%Y%m%d_%H%M%S", current_date_str)
    return file_name


def is_filtered_query_requested(module):
    """Return True when any filtered-log-query parameter has been supplied."""
    return any([
        module.params.get('date_start'), module.params.get('date_end'),
        module.params.get('severity'), module.params.get('category'),
        module.params.get('message_contains'), module.params.get('fetch_metadata_only'),
        module.params.get('export_path'), module.params.get('clear_logs'),
        module.params.get('insert_comment')])


def build_export_metadata(idrac, module):
    """Build the metadata envelope attached to JSON exports.

    Args:
    idrac -- iDRAC Redfish connection handle.
    module -- Ansible module instance.
    """
    generation, firmware_version, hw_model = idrac.get_server_generation
    return {
        "server_model": hw_model,
        "idrac_version": firmware_version,
        "export_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "filters_applied": {
            "date_start": module.params.get('date_start'),
            "date_end": module.params.get('date_end'),
            "severity": module.params.get('severity'),
            "category": module.params.get('category'),
            "message_contains": module.params.get('message_contains'),
        },
    }


def run_clear_logs(idrac, module):
    """Execute the log clear operation, applying the export-before-clear safety gate.

    Args:
    idrac -- iDRAC Redfish connection handle.
    module -- Ansible module instance.
    """
    exported_path = None
    export_path = module.params.get('export_path')
    if export_path:
        entries = fetch_lc_logs(
            idrac,
            date_start=module.params.get('date_start'),
            date_end=module.params.get('date_end'),
            severity=module.params.get('severity'),
            category=module.params.get('category'),
            message_contains=module.params.get('message_contains'),
            max_entries=module.params.get('max_entries'))
        message_registry = discover_message_registry(idrac)
        entries = enrich_with_message_registry(entries, message_registry)
        export_format = module.params.get('export_format') or 'json'
        metadata_envelope = build_export_metadata(idrac, module)
        try:
            exported_path = export_entries(
                entries, export_path, export_format=export_format,
                metadata=metadata_envelope, force=module.params.get('force'))
        except ExportPathError:
            if module.params.get('clear_only_if_export_succeeded'):
                module.exit_json(
                    msg="Clear aborted: export validation failed. Logs preserved to prevent data loss.",
                    failed=True)
                return
            raise
    elif module.params.get('clear_only_if_export_succeeded'):
        module.exit_json(
            msg="Clear aborted: export validation failed. Logs preserved to prevent data loss.",
            failed=True)
        return
    clear_result = clear_lc_logs(
        idrac, clear_logs=True,
        storage_threshold_pct=module.params.get('storage_threshold_pct') or DEFAULT_STORAGE_THRESHOLD_PCT)
    if exported_path:
        clear_result["export_path"] = exported_path
    module.exit_json(
        msg="Successfully cleared the lifecycle controller logs.",
        lc_log_clear_status=clear_result, changed=True)


def run_filtered_log_query(idrac, module):
    """Validate prerequisites and execute a filtered LC log query, metadata
    query, or filtered-log export.

    Args:
    idrac -- iDRAC Redfish connection handle.
    module -- Ansible module instance.
    """
    validate_lc_log_firmware_version(idrac)
    check_lc_log_service_available(idrac)
    storage_threshold_pct = module.params.get('storage_threshold_pct') or DEFAULT_STORAGE_THRESHOLD_PCT
    if module.params.get('fetch_metadata_only'):
        metadata = fetch_lc_log_metadata(idrac, storage_threshold_pct=storage_threshold_pct)
        module.exit_json(
            msg="Successfully fetched the lifecycle controller log metadata.",
            lc_log_metadata=metadata, changed=False)
        return
    if module.params.get('clear_logs'):
        run_clear_logs(idrac, module)
        return
    if module.params.get('insert_comment'):
        comment_result = insert_lc_log_comment(idrac, module.params.get('insert_comment'))
        module.exit_json(
            msg="Successfully inserted the comment into the lifecycle controller logs.",
            lc_log_comment=comment_result, changed=True)
        return
    entries = fetch_lc_logs(
        idrac,
        date_start=module.params.get('date_start'),
        date_end=module.params.get('date_end'),
        severity=module.params.get('severity'),
        category=module.params.get('category'),
        message_contains=module.params.get('message_contains'),
        max_entries=module.params.get('max_entries'))
    message_registry = discover_message_registry(idrac)
    entries = enrich_with_message_registry(entries, message_registry)
    export_path = module.params.get('export_path')
    if export_path:
        export_format = module.params.get('export_format') or 'json'
        metadata_envelope = build_export_metadata(idrac, module)
        exported_path = export_entries(
            entries, export_path, export_format=export_format,
            metadata=metadata_envelope, force=module.params.get('force'))
        module.exit_json(
            msg="Successfully exported the lifecycle controller logs.",
            lc_logs=entries, export_path=exported_path, changed=True)
        return
    module.exit_json(
        msg="Successfully fetched the lifecycle controller logs.",
        lc_logs=entries, changed=False)


# Main()
def main():
    specs = {
        "share_name": {"required": False, "type": 'str'},
        "share_user": {"required": False, "type": 'str'},
        "share_password": {"required": False, "type": 'str', "aliases": ['share_pwd'], "no_log": True},
        "job_wait": {"required": False, "type": 'bool', "default": True},
        "date_start": {"required": False, "type": 'str'},
        "date_end": {"required": False, "type": 'str'},
        "severity": {"required": False, "type": 'list', "elements": 'str',
                     "choices": ['OK', 'Warning', 'Critical']},
        "category": {"required": False, "type": 'list', "elements": 'str',
                     "choices": ['Storage', 'Updates', 'Audit', 'Configuration', 'WorkNotes', 'SystemHealth']},
        "message_contains": {"required": False, "type": 'str'},
        "fetch_metadata_only": {"required": False, "type": 'bool'},
        "max_entries": {"required": False, "type": 'int'},
        "export_format": {"required": False, "type": 'str', "choices": ['json', 'csv', 'text']},
        "export_path": {"required": False, "type": 'str'},
        "force": {"required": False, "type": 'bool', "default": False},
        "clear_logs": {"required": False, "type": 'bool'},
        "clear_only_if_export_succeeded": {"required": False, "type": 'bool'},
        "insert_comment": {"required": False, "type": 'str'},
        "storage_threshold_pct": {"required": False, "type": 'int', "default": DEFAULT_STORAGE_THRESHOLD_PCT},
    }
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        required_one_of=[[
            'share_name', 'date_start', 'date_end', 'severity', 'category',
            'message_contains', 'fetch_metadata_only', 'export_path',
            'clear_logs', 'insert_comment']],
        mutually_exclusive=[[
            'share_name', 'date_start'], [
            'share_name', 'date_end'], [
            'share_name', 'severity'], [
            'share_name', 'category'], [
            'share_name', 'message_contains'], [
            'share_name', 'fetch_metadata_only'], [
            'share_name', 'export_path'], [
            'share_name', 'clear_logs'], [
            'share_name', 'insert_comment'], [
            'fetch_metadata_only', 'export_path'], [
            'fetch_metadata_only', 'clear_logs'], [
            'fetch_metadata_only', 'insert_comment'], [
            'insert_comment', 'clear_logs'], [
            'insert_comment', 'export_path'], [
            'insert_comment', 'date_start'], [
            'insert_comment', 'date_end'], [
            'insert_comment', 'severity'], [
            'insert_comment', 'category'], [
            'insert_comment', 'message_contains']],
        required_by={
            'export_format': 'export_path',
            'clear_only_if_export_succeeded': 'clear_logs'},
        supports_check_mode=False)

    try:
        with iDRACRedfishAPI(module.params) as idrac:
            if is_filtered_query_requested(module):
                run_filtered_log_query(idrac, module)
                return
            server_det = idrac.get_server_generation
            server_hw_model = server_det[2]
            if server_hw_model != "iDRAC 8":
                lifecycle_controller_logs_obj = IDRACLifecycleControllerLogs(idrac)
                msg, job_dict, changed = lifecycle_controller_logs_obj.lifecycle_controller_logs_operation(idrac, module)
                module.exit_json(msg=msg, lc_logs_status=job_dict, changed=changed)
            else:
                with iDRACConnection(module.params) as idrac:
                    msg = run_export_lc_logs(idrac, module)
                    if msg.get("Status") in ["Failed", "Failure"] or msg.get("JobStatus") in ["Failed", "Failure"]:
                        msg.pop("file", None)
                        module.exit_json(
                            msg="Unable to export the lifecycle controller logs.",
                            lc_logs_status=msg, failed=True)
                    message = "Successfully exported the lifecycle controller logs."
                    if module.params['job_wait'] is False:
                        message = "The export lifecycle controller log job is submitted successfully."
                    module.exit_json(msg=message, lc_logs_status=msg)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError) as e:
        module.exit_json(msg=str(e), failed=True)


if __name__ == '__main__':
    main()
