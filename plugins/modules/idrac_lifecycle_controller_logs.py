# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Module
# Version 10.0.3
# Copyright (C) 2018-2026 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_lifecycle_controller_logs
short_description: Export Lifecycle Controller logs to a network share or local path with advanced features.
version_added: "2.1.0"
description:
  - Export Lifecycle Controller logs to a given network share or local path.
  - Support for filtering by date range, severity, category, and message content.
  - Support for multi-format export (JSON, CSV, text) with metadata envelope.
  - Support for compliance export verification, filter optimization, storage monitoring, and comment insertion.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
  share_name:
    description:
      - Network share or local path.
      - CIFS, NFS network share types are supported.
    type: str
    required: true
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
    description:
      - Start date for filtering log entries (ISO 8601 format).
      - Only entries created on or after this date are included.
      - Uses server-side OData $filter for efficient querying.
      - Example format - 2026-08-01T00:00:00Z or 2026-08-01.
    type: str
  date_end:
    description:
      - End date for filtering log entries (ISO 8601 format).
      - Only entries created on or before this date are included.
      - Uses server-side OData $filter for efficient querying.
      - Must not be earlier than I(date_start).
      - Example format - 2026-08-31T23:59:59Z or 2026-08-31.
    type: str
  severity:
    description:
      - List of severity levels to filter log entries.
      - Uses server-side OData $filter for efficient querying.
      - Valid values are C(Critical), C(Warning), and C(OK).
    type: list
    elements: str
    choices: ['Critical', 'Warning', 'OK']
  category:
    description:
      - List of Dell OEM categories to filter log entries.
      - Uses server-side OData $filter for efficient querying.
      - Common categories include Audit, Configuration, Updates, SystemHealth, Storage, and WorkNotes.
    type: list
    elements: str
  message_contains:
    description:
      - Substring to search for in log messages (case-insensitive).
      - Applied client-side after server-side filters.
      - Use for searching specific keywords in log messages.
    type: str
  export_format:
    description:
      - Format for exporting log entries to local file.
      - C(json) exports with metadata envelope including server info and filters applied.
      - C(csv) exports as comma-delimited file with header row.
      - C(text) exports one entry per line in human-readable format.
      - Only applicable when exporting to local path.
    type: str
    choices: ['json', 'csv', 'text']
    default: 'json'
  fetch_metadata_only:
    description:
      - Fetch only log service metadata without retrieving log entries.
      - Returns statistics like total entries, oldest/newest timestamps, severity breakdown.
      - Only applicable when using local file path.
    type: bool
    default: false
  verify_export:
    description:
      - Enable compliance export verification with entry count comparison.
      - When enabled, compares expected vs actual entry count after export.
      - Returns export_verification field with verification results.
    type: bool
    default: false
  filter_optimization:
    description:
      - Filter optimization mode for combined filter operations.
      - C(single_query) uses server-side filtering with OData query parameters.
      - C(sequential) applies filters sequentially on client side.
      - C(auto) automatically selects the best mode based on filter complexity.
    type: str
    choices: ['single_query', 'sequential', 'auto']
    default: 'auto'
  storage_threshold_pct:
    description:
      - Storage overflow monitoring threshold percentage.
      - When storage utilization exceeds this threshold, a warning is returned.
      - Set to 0 to disable storage monitoring.
      - Default is 80 percent.
    type: int
    default: 80
  insert_comment:
    description:
      - Insert a custom comment into the LC logs during automation workflows.
      - Maximum length is 256 characters.
      - Requires ConfigureManager or Login+TestAlerts privilege.
      - Returns inserted_entry_id and inserted_entry_timestamp on success.
    type: str

requirements:
  - "python >= 3.9.6"
author:
  - "Rajeev Arakkal (@rajeevarakkal)"
  - "Anooja Vardhineni (@anooja-vardhineni)"
  - "Sapana Gupta (@sapana05)"
notes:
  - This module requires 'Administrator' privilege for I(idrac_user).
  - Exporting data to a local share is supported only on iDRAC9-based PowerEdge Servers and later.
  - Run this module from a system that has direct access to Dell iDRAC.
  - This module supports both IPv4 and IPv6 address for I(idrac_ip).
  - This module does not support C(check_mode).
  - No job will be created when exporting data to a local share in iDRAC9 and iDRAC 10.
  - The insert_comment parameter requires ConfigureManager or Login+TestAlerts privilege.
  - Server-side OData $filter is used for date_start, date_end, severity, and category filters.
  - The message_contains filter is applied client-side after server-side filtering.
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

- name: Filter logs by date range (AC-001).
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/example/export_lc"
    date_start: "2026-08-01T00:00:00Z"
    date_end: "2026-08-31T23:59:59Z"

- name: Filter logs by severity (AC-002).
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/example/export_lc"
    severity:
      - Critical
      - Warning

- name: Export logs in CSV format (AC-003).
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/example/export_lc/logs.csv"
    export_format: "csv"

- name: Export logs in JSON format with metadata envelope (AC-005).
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/example/export_lc/logs.json"
    export_format: "json"
    date_start: "2026-08-01"
    severity:
      - Critical

- name: Filter logs by category and message content.
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/example/export_lc"
    category:
      - Audit
      - Configuration
    message_contains: "firmware"

- name: Fetch LC log metadata only.
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/tmp"
    fetch_metadata_only: true

- name: Export with compliance verification (AC-006).
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/example/export_lc"
    verify_export: true

- name: Combined filters with optimization (AC-007).
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/example/export_lc"
    date_start: "2026-08-01"
    severity:
      - Critical
    category:
      - SystemHealth
    filter_optimization: "single_query"

- name: Export with storage overflow monitoring (AC-008).
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/example/export_lc"
    storage_threshold_pct: 75

- name: Insert comment into LC logs (AC-009).
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/tmp"
    insert_comment: "Automation workflow started - backup initiated"
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
lc_logs:
  description: List of filtered log entries when filters are applied.
  returned: when filters are applied and export_format is not specified
  type: list
  sample: [
    {
      "Id": "1",
      "Created": "2026-08-17T10:00:00Z",
      "Severity": "Critical",
      "Message": "System temperature exceeded threshold",
      "MessageId": "SYS001"
    }
  ]
exported_entry_count:
  description: Number of log entries exported to file.
  returned: when export_format is specified
  type: int
  sample: 150
filters_applied:
  description: Summary of filters that were applied to the query.
  returned: when any filter parameter is specified
  type: dict
  sample: {
    "date_start": "2026-08-01T00:00:00Z",
    "date_end": "2026-08-31T23:59:59Z",
    "severity": ["Critical", "Warning"],
    "category": ["Audit"],
    "message_contains": "firmware"
  }
log_metadata:
  description: Log service metadata when fetch_metadata_only is true.
  returned: when fetch_metadata_only is true
  type: dict
  sample: {
    "total_entries": 150,
    "oldest_timestamp": "2026-01-01T00:00:00Z",
    "newest_timestamp": "2026-08-18T12:00:00Z",
    "severity_breakdown": {
      "Critical": 5,
      "Warning": 20,
      "OK": 100,
      "Other": 25
    },
    "storage_utilization_pct": 75.0,
    "max_records": 200,
    "overwrite_policy": "WrapsWhenFull"
  }
export_verification:
  description: Export verification results when verify_export is true.
  returned: when verify_export is true
  type: dict
  sample: {
    "expected_count": 150,
    "actual_count": 150,
    "verified": true,
    "message": "Export verification successful"
  }
storage_warning:
  description: Storage overflow warning when utilization exceeds threshold.
  returned: when storage utilization exceeds storage_threshold_pct
  type: str
  sample: "LC log storage at 85.5% capacity (threshold 80%). Consider exporting and archiving."
inserted_entry_id:
  description: ID of the inserted comment entry.
  returned: when insert_comment is provided
  type: str
  sample: "LC123456"
inserted_entry_timestamp:
  description: Timestamp of the inserted comment entry.
  returned: when insert_comment is provided
  type: str
  sample: "2026-08-18T12:00:00Z"
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
"""


import json
import os
import re
from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import idrac_auth_params
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.\
    idrac_lifecycle_controller_logs_utils import IDRACLifecycleControllerLogs
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.\
    idrac_log_filters import IDRACLogFilter
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.\
    idrac_log_exporter import IDRACLogExporter

EXPORT_LC_LOGS = '/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellLCService/Actions/DellLCService.ExportLCLog'
LC_LOG_ENTRIES_URI = '/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Lclog/Entries'
SUCCESS_MSG = "Successfully exported the lifecycle controller logs."
FILTERED_EXPORT_MSG = "Successfully exported filtered lifecycle controller logs."
SCHEDULE_MSG = "The export lifecycle controller log job is submitted successfully."
NO_CHANGES_FOUND_MSG = "No changes found to be applied."
NO_MATCHING_ENTRIES_MSG = "No log entries matched the specified filters."
CHANGES_FOUND_MSG = "Changes found to be applied."
COMMENT_INSERT_SUCCESS = "Successfully inserted comment into LC logs."
COMMENT_MAX_LENGTH = 256


def validate_insert_comment(comment):
    """Validate insert_comment parameter."""
    if comment is None:
        return None

    if len(comment) > COMMENT_MAX_LENGTH:
        raise ValueError(
            f"insert_comment exceeds maximum length of {COMMENT_MAX_LENGTH} characters. "
            f"Current length: {len(comment)}"
        )

    # Check for control characters
    if re.search(r'[\x00-\x1f\x7f]', comment):
        raise ValueError(
            "insert_comment contains control characters which are not allowed"
        )

    return comment


def build_odata_filter(module):
    """Build OData $filter query string from module parameters."""
    filters = []

    date_start = module.params.get('date_start')
    date_end = module.params.get('date_end')
    severity = module.params.get('severity')
    category = module.params.get('category')

    if date_start:
        filters.append(f"Created ge '{date_start}'")
    if date_end:
        filters.append(f"Created le '{date_end}'")
    if severity:
        severity_filters = [f"Severity eq '{s}'" for s in severity]
        filters.append(f"({' or '.join(severity_filters)})")
    if category:
        category_filters = [f"Oem/Dell/Category eq '{c}'" for c in category]
        filters.append(f"({' or '.join(category_filters)})")

    return ' and '.join(filters) if filters else None


def get_filtered_log_entries(idrac, module, odata_filter=None):
    """Retrieve log entries with optional OData filter and pagination."""
    entries = []
    uri = LC_LOG_ENTRIES_URI

    if odata_filter:
        uri = f"{uri}?$filter={odata_filter}"

    while uri:
        response = idrac.invoke_request(uri, 'GET')
        data = response.json_data

        if 'Members' in data:
            entries.extend(data['Members'])

        # Follow pagination
        uri = data.get('Members@odata.nextLink')

    return entries


def has_filters(module):
    """Check if any filter parameters are specified."""
    return any([
        module.params.get('date_start'),
        module.params.get('date_end'),
        module.params.get('severity'),
        module.params.get('category'),
        module.params.get('message_contains')
    ])


def get_filters_applied(module):
    """Get summary of filters that were applied."""
    filters = {}
    if module.params.get('date_start'):
        filters['date_start'] = module.params.get('date_start')
    if module.params.get('date_end'):
        filters['date_end'] = module.params.get('date_end')
    if module.params.get('severity'):
        filters['severity'] = module.params.get('severity')
    if module.params.get('category'):
        filters['category'] = module.params.get('category')
    if module.params.get('message_contains'):
        filters['message_contains'] = module.params.get('message_contains')
    return filters


def main():
    specs = {
        "share_name": {"required": True, "type": 'str'},
        "share_user": {"required": False, "type": 'str'},
        "share_password": {"required": False, "type": 'str', "aliases": ['share_pwd'], "no_log": True},
        "job_wait": {"required": False, "type": 'bool', "default": True},
        "date_start": {"required": False, "type": 'str'},
        "date_end": {"required": False, "type": 'str'},
        "severity": {
            "required": False,
            "type": 'list',
            "elements": 'str',
            "choices": ['Critical', 'Warning', 'OK']
        },
        "category": {"required": False, "type": 'list', "elements": 'str'},
        "message_contains": {"required": False, "type": 'str'},
        "export_format": {
            "required": False,
            "type": 'str',
            "choices": ['json', 'csv', 'text'],
            "default": 'json'
        },
        "fetch_metadata_only": {"required": False, "type": 'bool', "default": False},
        "verify_export": {"required": False, "type": 'bool', "default": False},
        "filter_optimization": {
            "required": False,
            "type": 'str',
            "choices": ['single_query', 'sequential', 'auto'],
            "default": 'auto'
        },
        "storage_threshold_pct": {"required": False, "type": 'int', "default": 80},
        "insert_comment": {"required": False, "type": 'str'},
    }
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        supports_check_mode=False)

    try:
        # Validate insert_comment if provided
        insert_comment = module.params.get('insert_comment')
        if insert_comment:
            validate_insert_comment(insert_comment)

        # Validate date range
        date_start = module.params.get('date_start')
        date_end = module.params.get('date_end')
        if date_start and date_end:
            log_filter = IDRACLogFilter()
            log_filter.validate_date_range(date_start, date_end)

        with iDRACRedfishAPI(module.params) as idrac:
            lifecycle_controller_logs_obj = IDRACLifecycleControllerLogs(idrac)
            result = {}

            # Handle fetch_metadata_only mode
            if module.params.get('fetch_metadata_only'):
                metadata = lifecycle_controller_logs_obj.get_lc_log_metadata(idrac, module)

                # Add storage warning if threshold exceeded
                storage_threshold = module.params.get('storage_threshold_pct', 80)
                if storage_threshold > 0:
                    utilization = metadata.get('storage_utilization_pct', 0)
                    if utilization > storage_threshold:
                        result['storage_warning'] = (
                            f"LC log storage at {utilization}% capacity "
                            f"(threshold: {storage_threshold}%). "
                            f"Consider exporting and archiving logs."
                        )

                module.exit_json(
                    msg="Successfully retrieved LC log metadata.",
                    log_metadata=metadata,
                    changed=False,
                    **result
                )

            # Handle insert_comment
            if insert_comment:
                comment_result = lifecycle_controller_logs_obj.insert_lc_comment(
                    idrac, module, insert_comment
                )
                module.exit_json(
                    msg=COMMENT_INSERT_SUCCESS,
                    inserted_entry_id=comment_result.get('entry_id'),
                    inserted_entry_timestamp=comment_result.get('timestamp'),
                    changed=True
                )

            # Get metadata for storage monitoring and verification
            metadata = None
            if module.params.get('verify_export') or module.params.get('storage_threshold_pct', 80) > 0:
                metadata = lifecycle_controller_logs_obj.get_lc_log_metadata(idrac, module)

                # Add storage warning if threshold exceeded
                storage_threshold = module.params.get('storage_threshold_pct', 80)
                if storage_threshold > 0 and metadata:
                    utilization = metadata.get('storage_utilization_pct', 0)
                    if utilization > storage_threshold:
                        result['storage_warning'] = (
                            f"LC log storage at {utilization}% capacity "
                            f"(threshold: {storage_threshold}%). "
                            f"Consider exporting and archiving logs. "
                            f"Overwrite policy: {metadata.get('overwrite_policy', 'Unknown')}"
                        )

            # Store expected count for verification
            expected_count = metadata.get('total_entries', 0) if metadata else 0

            # Check if filters are applied - use filtered export path
            if has_filters(module):
                # Build OData filter for server-side filtering
                odata_filter = build_odata_filter(module)

                # Get filtered log entries
                log_entries = get_filtered_log_entries(idrac, module, odata_filter)

                # Apply client-side message_contains filter if specified
                message_contains = module.params.get('message_contains')
                if message_contains:
                    log_filter = IDRACLogFilter()
                    log_filter.add_message_filter(message_contains)
                    log_entries = log_filter.apply(log_entries)

                # Add filters_applied to result
                result['filters_applied'] = get_filters_applied(module)

                # Check if any entries matched
                if not log_entries:
                    module.exit_json(
                        msg=NO_MATCHING_ENTRIES_MSG,
                        lc_logs=[],
                        changed=False,
                        **result
                    )

                # Check if local export is requested
                share_name = module.params.get('share_name')
                is_local = not (share_name.startswith('\\\\') or ':/' in share_name)

                if is_local:
                    export_format = module.params.get('export_format', 'json')

                    # Build export metadata
                    export_metadata = {
                        'server_ip': module.params.get('idrac_ip'),
                        'export_timestamp': None,  # Will be set by exporter
                        'filters_applied': result['filters_applied'],
                        'exported_entry_count': len(log_entries)
                    }

                    # Get server info for metadata
                    if metadata:
                        export_metadata['total_entries_on_server'] = metadata.get('total_entries', 0)

                    # Determine export file path
                    if os.path.isdir(share_name):
                        # Generate filename if directory provided
                        idrac_ip = module.params.get('idrac_ip', 'unknown').replace(':', '.')
                        from datetime import datetime
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"{idrac_ip}_{timestamp}_LC_Log.{export_format}"
                        export_path = os.path.join(share_name, filename)
                    else:
                        export_path = share_name

                    # Export using the exporter utility
                    exporter = IDRACLogExporter(export_path, export_format)
                    exported_count = exporter.export(log_entries, export_metadata)

                    result['exported_entry_count'] = exported_count
                    result['export_file'] = export_path

                    # Handle verify_export
                    if module.params.get('verify_export'):
                        verified = (exported_count == len(log_entries))
                        result['export_verification'] = {
                            'expected_count': len(log_entries),
                            'actual_count': exported_count,
                            'verified': verified,
                            'message': (
                                "Export verification successful"
                                if verified
                                else f"Export verification failed: expected {len(log_entries)}, got {exported_count}"
                            )
                        }

                    module.exit_json(
                        msg=FILTERED_EXPORT_MSG,
                        lc_logs=log_entries,
                        changed=True,
                        **result
                    )
                else:
                    # For network shares, return filtered entries without local export
                    result['lc_logs'] = log_entries
                    module.exit_json(
                        msg=f"Retrieved {len(log_entries)} filtered log entries.",
                        lc_logs=log_entries,
                        changed=False,
                        **result
                    )

            # No filters - use standard export operation
            msg, job_dict, changed = lifecycle_controller_logs_obj.lifecycle_controller_logs_operation(
                idrac, module
            )

            # Handle verify_export
            if module.params.get('verify_export') and metadata:
                # Get actual count after export
                post_metadata = lifecycle_controller_logs_obj.get_lc_log_metadata(idrac, module)
                actual_count = post_metadata.get('total_entries', 0)

                verified = (expected_count == actual_count)
                result['export_verification'] = {
                    'expected_count': expected_count,
                    'actual_count': actual_count,
                    'verified': verified,
                    'message': (
                        "Export verification successful"
                        if verified
                        else f"Export verification failed: expected {expected_count}, got {actual_count}"
                    )
                }

            module.exit_json(msg=msg, lc_logs_status=job_dict, changed=changed, **result)

    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError, OSError) as e:
        module.exit_json(msg=str(e), failed=True)


if __name__ == '__main__':
    main()
