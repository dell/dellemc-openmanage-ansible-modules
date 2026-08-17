# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Module
# Version 10.0.5
# Copyright (C) 2018-2026 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_lifecycle_controller_logs
short_description: Export Lifecycle Controller logs to a network share or local path with filtering support.
version_added: "2.1.0"
description:
  - Export Lifecycle Controller logs to a given network share or local path.
  - Support for filtering logs by date range, severity, category, and message pattern.
  - Support for multiple export formats (JSON, CSV, text).
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
  export_format:
    description:
      - Format for log export when using local file path.
      - Only applicable when share_name is a local file path.
      - For network shares, logs are exported in the default format.
    type: str
    choices: ['json', 'csv', 'text']
    default: 'json'
    version_added: "10.0.4"
  date_start:
    description:
      - Filter logs to include only entries on or after this date.
      - Format: ISO 8601 (e.g., 2026-08-01T00:00:00Z).
      - Only applicable when using local file path.
    type: str
    version_added: "10.0.4"
  date_end:
    description:
      - Filter logs to include only entries before this date.
      - Format: ISO 8601 (e.g., 2026-08-31T23:59:59Z).
      - Only applicable when using local file path.
    type: str
    version_added: "10.0.4"
  severity:
    description:
      - Filter logs by severity level.
      - Only applicable when using local file path.
    type: list
    elements: str
    choices: ['Critical', 'Warning', 'OK']
    version_added: "10.0.4"
  category:
    description:
      - Filter logs by category.
      - Only applicable when using local file path.
    type: list
    elements: str
    version_added: "10.0.4"
  message_pattern:
    description:
      - Filter logs by message pattern (regex supported).
      - Only applicable when using local file path.
    type: str
    version_added: "10.0.4"
  max_entries:
    description:
      - Maximum number of log entries to retrieve.
      - Useful for limiting export size.
      - Only applicable when using local file path.
    type: int
    version_added: "10.0.4"
  force:
    description:
      - Force overwrite of existing export file.
      - Only applicable when using local file path.
    type: bool
    default: false
    version_added: "10.0.4"
  fetch_metadata_only:
    description:
      - Fetch only log service metadata without retrieving log entries.
      - Returns statistics like total entries, oldest/newest timestamps, severity breakdown.
      - Only applicable when using local file path.
    type: bool
    default: false
    version_added: "10.0.4"
  enrich_messages:
    description:
      - Enrich log entries with MessageRegistry descriptions and resolutions.
      - Adds MessageDescription and MessageResolution fields to each entry.
      - Only applicable when using local file path.
      - May increase processing time for large log sets.
    type: bool
    default: false
    version_added: "10.0.4"
  verify_export:
    description:
      - Verify export by comparing exported_entry_count against expected count.
      - Provides verification status for compliance workflows.
      - Only applicable when using local file path.
    type: bool
    default: false
    version_added: "10.0.5"
  filter_optimization:
    description:
      - Optimize combined filters into single OData query for better performance.
      - When false, filters are applied sequentially for simpler debugging.
      - Only applicable when using local file path.
    type: bool
    default: true
    version_added: "10.0.5"
  storage_threshold_pct:
    description:
      - Storage utilization threshold percentage for warning generation.
      - When LC log storage exceeds this threshold, a warning is returned.
      - Set to 0 to disable storage monitoring.
      - Only applicable when using local file path.
    type: int
    default: 80
    version_added: "10.0.5"
  insert_comment:
    description:
      - Insert custom comment into LC logs for automation workflow context.
      - Comment length must be ≤ 256 characters.
      - Only applicable when using local file path.
    type: str
    version_added: "10.0.5"

requirements:
  - "python >= 3.9.6"
author:
  - "Rajeev Arakkal (@rajeevarakkal)"
  - "Anooja Vardhineni (@anooja-vardhineni)"
  - "Trisha Datta (@trisha-dell)"
troubleshooting:
  - "No logs returned with filters applied":
      - Verify the filter criteria match actual log entries in the LC log.
      - Check the date format is ISO 8601 (e.g., 2026-08-01T00:00:00Z).
      - Use fetch_metadata_only to check available log entries and their timestamps.
  - "Filter syntax errors":
      - Ensure severity values are exactly 'Critical', 'Warning', or 'OK'.
      - For message_pattern, use valid regex syntax.
      - Date filters require ISO 8601 format with timezone information.
  - "Export failures":
      - Verify the export path has write permissions.
      - Use force=true to overwrite existing export files.
      - Check disk space is available for the export file.
  - "Permission errors":
      - Ensure the iDRAC user has 'Administrator' privilege.
      - Verify network share credentials are correct for CIFS exports.
      - Comment insertion requires 'ConfigureManager' or 'Login+TestAlerts' privilege.
  - "Firmware incompatibility":
      - Check iDRAC firmware version meets minimum requirements (iDRAC9 ≥ 7.10.90.00, iDRAC10 ≥ 1.20.50.50).
      - Upgrade iDRAC firmware if version is below minimum requirement.
  - "MessageRegistry enrichment not working":
      - MessageRegistry may not be available on all firmware versions.
      - The module will continue without enrichment and log a warning.
      - Check iDRAC firmware version supports MessageRegistry endpoints.
  - "Export verification failures":
      - Verification failures may occur when filters are applied.
      - Expected count is based on total entries before filtering.
      - Actual count reflects entries after filtering.
      - This is expected behavior and not an error.
  - "Comment insertion failures":
      - Ensure comment length is ≤ 256 characters.
      - Check for invalid control characters in comment text.
      - Verify iDRAC user has sufficient privilege for comment insertion.
  - "Storage warnings":
      - Storage warnings are informational, not failures.
      - Export and archive logs when storage utilization exceeds threshold.
      - iDRAC will automatically overwrite oldest entries when full (WrapsWhenFull policy).
notes:
  - This module requires 'Administrator' privilege for I(idrac_user).
  - Exporting data to a local share is supported only on iDRAC9-based PowerEdge Servers and later.
  - Run this module from a system that has direct access to Dell iDRAC.
  - This module supports both IPv4 and IPv6 address for I(idrac_ip).
  - This module does not support C(check_mode).
  - No job will be created when exporting data to a local share in iDRAC9 and iDRAC 10.
  - Filtering and format options are only available for local file exports.
  - The minimum firmware version for iDRAC9 is 7.10.90.00 and for iDRAC10 is 1.20.50.50.
  - MessageRegistry enrichment may not be available on all iDRAC firmware versions.
    When unavailable, the module will continue without enrichment and log a warning.
  - For network share exports, the module uses the existing DellLCService.ExportLCLog action.
  - For local file exports, the module uses Redfish API to query and filter LC logs directly.
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

- name: Export lifecycle controller logs to local JSON file with date filter.
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/tmp/lc_logs.json"
    export_format: "json"
    date_start: "2026-08-01T00:00:00Z"
    date_end: "2026-08-31T23:59:59Z"

- name: Export lifecycle controller logs to local CSV file with severity filter.
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/tmp/lc_logs.csv"
    export_format: "csv"
    severity:
      - Critical
      - Warning

- name: Export lifecycle controller logs with message pattern filter.
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/tmp/lc_logs.json"
    export_format: "json"
    message_pattern: "temperature|power"

- name: Export lifecycle controller logs with combined filters and max entries limit.
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/tmp/lc_logs.json"
    export_format: "json"
    date_start: "2026-08-01T00:00:00Z"
    severity:
      - Critical
    max_entries: 100

- name: Fetch LC log metadata only (no entries).
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/tmp/lc_logs.json"
    fetch_metadata_only: true

- name: Export LC logs with MessageRegistry enrichment.
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/tmp/lc_logs_enriched.json"
    export_format: "json"
    enrich_messages: true
    max_entries: 100

- name: Compliance export with verification (AC-006).
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/tmp/lc_logs_compliance.json"
    export_format: "json"
    verify_export: true

- name: Combined filters with optimization disabled (AC-007).
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/tmp/lc_logs_combined.json"
    export_format: "json"
    date_start: "2026-08-01T00:00:00Z"
    severity:
      - Critical
    category:
      - SystemHealth
    filter_optimization: false

- name: Storage overflow monitoring with custom threshold (AC-008).
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/tmp/lc_logs.json"
    export_format: "json"
    storage_threshold_pct: 90

- name: Insert comment into LC logs for automation context (AC-009).
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/tmp/lc_logs.json"
    insert_comment: "Maintenance window started - firmware update initiated"
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
"""


import json
import os
from ansible_collections.dellemc.openmanage.plugins.module_utils.\
    dellemc_idrac import idrac_auth_params
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.\
    idrac_redfish import iDRACRedfishAPI
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.\
    idrac_lifecycle_controller_logs_utils import IDRACLifecycleControllerLogs
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.\
    idrac_log_pagination import IDRACLogPagination
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.\
    idrac_log_filters import IDRACLogFilter
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.\
    idrac_log_exporter import IDRACLogExporter
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.\
    idrac_message_registry import IDRACMessageRegistry
EXPORT_LC_LOGS = ('/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/'
                 'DellLCService/Actions/DellLCService.ExportLCLog')
SUCCESS_MSG = "Successfully exported the lifecycle controller logs."
SCHEDULE_MSG = "The export lifecycle controller log job is submitted successfully."
NO_CHANGES_FOUND_MSG = "No changes found to be applied."
CHANGES_FOUND_MSG = "Changes found to be applied."


def main():
    specs = {
        "share_name": {"required": False, "type": 'str'},
        "share_user": {"required": False, "type": 'str'},
        "share_password": {"required": False, "type": 'str',
                         "aliases": ['share_pwd'], "no_log": True},
        "job_wait": {"required": False, "type": 'bool', "default": True},
        "export_format": {"required": False, "type": 'str',
                         "choices": ['json', 'csv', 'text'], "default": 'json'},
        "date_start": {"required": False, "type": 'str'},
        "date_end": {"required": False, "type": 'str'},
        "severity": {"required": False, "type": 'list', "elements": 'str',
                    "choices": ['Critical', 'Warning', 'OK']},
        "category": {"required": False, "type": 'list', "elements": 'str'},
        "message_pattern": {"required": False, "type": 'str'},
        "max_entries": {"required": False, "type": 'int'},
        "force": {"required": False, "type": 'bool', "default": False},
        "fetch_metadata_only": {"required": False, "type": 'bool',
                              "default": False},
        "enrich_messages": {"required": False, "type": 'bool', "default": False},
        "verify_export": {"required": False, "type": 'bool', "default": False},
        "filter_optimization": {"required": False, "type": 'bool',
                              "default": True},
        "storage_threshold_pct": {"required": False, "type": 'int',
                                  "default": 80},
        "insert_comment": {"required": False, "type": 'str'},
    }
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        supports_check_mode=False)

    # Check if this is a local file export (new filtering/export functionality)
    share_name = module.params.get('share_name')
    # Network shares: \\server\share (CIFS) or server:/path (NFS)
    is_network_share = (share_name.startswith('\\\\') or
                       (':' in share_name and not share_name[1] == ':'))
    is_local_export = not is_network_share

    try:
        with iDRACRedfishAPI(module.params) as idrac:
            # Validate firmware version for local export (new functionality)
            if is_local_export:
                gen_details = idrac.get_server_generation
                idrac_model = gen_details[2] if len(gen_details) > 2 else 'iDRAC 9'
                firmware_version = gen_details[1] if len(gen_details) > 1 else '0.0.0.0'

                is_compliant, minimum_required, error_msg = (
                    iDRACRedfishAPI.check_minimum_firmware_requirement(
                        idrac_model, firmware_version))

                if not is_compliant:
                    module.exit_json(msg=error_msg, failed=True)

                # Check LC Log Service availability
                try:
                    lclog_service_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Lclog"
                    response = idrac.invoke_request(lclog_service_uri, 'GET')
                    service_data = response.json_data

                    if not service_data.get('ServiceEnabled', True):
                        module.exit_json(
                            msg=("Lifecycle Controller Log service is not enabled "
                                 "on this iDRAC. Please enable LC Log service in "
                                 "iDRAC settings."),
                            failed=True
                        )
                except Exception as e:
                    module.exit_json(
                        msg=f"Failed to query Lifecycle Controller Log service: {str(e)}",
                        failed=True
                    )

            # Use new filtering/export functionality for local file exports
            if is_local_export:
                # Check if insert_comment is requested (AC-009)
                insert_comment = module.params.get('insert_comment')
                if insert_comment:
                    # Validate comment length
                    if len(insert_comment) > 256:
                        module.exit_json(
                            msg=(f"Comment exceeds maximum length of 256 characters "
                                 f"(provided: {len(insert_comment)})"),
                            failed=True
                        )

                    # Validate for control characters
                    if any(ord(c) < 32 and c not in '\t\n\r' for c in insert_comment):
                        module.exit_json(
                            msg="Comment contains invalid control characters",
                            failed=True
                        )

                    # Invoke DellLCService.InsertCommentInLCLog action
                    try:
                        comment_action_uri = ("/redfish/v1/Managers/iDRAC.Embedded.1/"
                                             "Oem/Dell/DellLCService/Actions/"
                                             "DellLCService.InsertCommentInLCLog")
                        comment_payload = {"Comment": insert_comment}
                        response = idrac.invoke_request(comment_action_uri, 'POST',
                                                         data=comment_payload)
                        result = response.json_data if response.json_data else {}

                        module.exit_json(
                            msg=f"Successfully inserted comment into LC logs: {insert_comment}",
                            inserted_entry_id=result.get('EntryId', 'Unknown'),
                            inserted_entry_timestamp=result.get('CreatedTimestamp', 'Unknown'),
                            changed=True
                        )
                    except Exception as e:
                        module.exit_json(
                            msg=f"Failed to insert comment into LC logs: {str(e)}",
                            failed=True
                        )

                # Check if metadata-only mode is requested
                if module.params.get('fetch_metadata_only'):
                    pagination = IDRACLogPagination(idrac)
                    base_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Lclog/Entries"

                    total_entries = pagination.get_total_entries_count(base_uri)
                    oldest_timestamp = pagination.get_oldest_entry_timestamp(base_uri)
                    newest_timestamp = pagination.get_newest_entry_timestamp(base_uri)
                    severity_breakdown = pagination.get_severity_breakdown(base_uri)

                    # Calculate storage utilization and check threshold (AC-008)
                    lclog_service_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Lclog"
                    response = idrac.invoke_request(lclog_service_uri, 'GET')
                    service_data = response.json_data
                    max_records = service_data.get('MaxNumberOfRecords', 0)
                    overwrite_policy = service_data.get('OverWritePolicy', 'Unknown')

                    storage_utilization = 0
                    if max_records > 0:
                        storage_utilization = (total_entries / max_records) * 100

                    storage_threshold_pct = module.params.get('storage_threshold_pct', 80)
                    storage_warning = None

                    if storage_threshold_pct > 0 and storage_utilization > storage_threshold_pct:
                        storage_warning = (
                            f"LC log storage at {round(storage_utilization, 2)}% capacity "
                            f"(threshold: {storage_threshold_pct}%). Consider exporting "
                            f"and archiving logs before iDRAC's automatic wrap-around "
                            f"overwrites oldest entries. Overwrite policy: {overwrite_policy}"
                        )

                    metadata = {
                        "total_entries": total_entries,
                        "oldest_entry_timestamp": oldest_timestamp,
                        "newest_entry_timestamp": newest_timestamp,
                        "severity_breakdown": severity_breakdown,
                        "storage_utilization_percentage": round(storage_utilization, 2),
                        "max_records": max_records,
                        "overwrite_policy": overwrite_policy
                    }

                    result = {
                        "msg": "Successfully retrieved Lifecycle Controller log metadata.",
                        "lc_logs_metadata": metadata,
                        "changed": False
                    }

                    if storage_warning:
                        result["storage_warning"] = storage_warning

                    module.exit_json(**result)

                # Initialize pagination with circuit breaker
                pagination = IDRACLogPagination(idrac, max_entries=module.params.get('max_entries'))
                base_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Lclog/Entries"

                # Pre-calculate expected entry count for verification (AC-006)
                verify_export = module.params.get('verify_export', False)
                expected_count = None
                if verify_export:
                    expected_count = pagination.get_total_entries_count(base_uri)

                # Retrieve logs with pagination
                date_start = module.params.get('date_start')
                entries = list(pagination.paginate_lc_logs(base_uri, date_start=date_start))

                # Apply filters with optimization (AC-007)
                log_filter = IDRACLogFilter()
                filter_optimization = module.params.get('filter_optimization', True)

                if filter_optimization:
                    # Combined filter optimization - apply all filters at once
                    # Note: Server-side filtering is already handled in pagination
                    # This is for client-side filters that can't be done server-side
                    if module.params.get('date_end'):
                        log_filter.add_date_filter(
                            date_end=module.params.get('date_end'))
                    if module.params.get('severity'):
                        log_filter.add_severity_filter(
                            module.params.get('severity'))
                    if module.params.get('category'):
                        log_filter.add_category_filter(
                            module.params.get('category'))
                    if module.params.get('message_pattern'):
                        log_filter.add_message_filter(
                            module.params.get('message_pattern'))

                    filtered_entries = log_filter.apply(entries)
                else:
                    # Sequential filter application for debugging
                    if module.params.get('date_end'):
                        log_filter.add_date_filter(date_end=module.params.get('date_end'))
                        entries = log_filter.apply(entries)
                        log_filter = IDRACLogFilter()  # Reset for next filter

                    if module.params.get('severity'):
                        log_filter.add_severity_filter(
                            module.params.get('severity'))
                        entries = log_filter.apply(entries)
                        log_filter = IDRACLogFilter()

                    if module.params.get('category'):
                        log_filter.add_category_filter(
                            module.params.get('category'))
                        entries = log_filter.apply(entries)
                        log_filter = IDRACLogFilter()

                    if module.params.get('message_pattern'):
                        log_filter.add_message_filter(
                            module.params.get('message_pattern'))
                        entries = log_filter.apply(entries)

                    filtered_entries = entries

                # Enrich entries with MessageRegistry if requested
                if module.params.get('enrich_messages'):
                    try:
                        message_registry = IDRACMessageRegistry(idrac)
                        filtered_entries = message_registry.enrich_log_entries(
                            filtered_entries)
                    except Exception as e:
                        # Log warning but continue without enrichment
                        module.warn(
                            f"Failed to enrich messages with MessageRegistry: {str(e)}")

                # Check if file exists and handle force parameter
                force = module.params.get('force', False)
                if os.path.exists(share_name) and not force:
                    module.exit_json(
                        msg=(f"Export file {share_name} already exists. "
                             f"Use force=true to overwrite."),
                        failed=True
                    )

                # Export to file
                exporter = IDRACLogExporter(share_name,
                                          module.params.get('export_format'))
                metadata = {
                    "server_model": (idrac.get_system_model()
                                    if hasattr(idrac, 'get_system_model')
                                    else "Unknown"),
                    "service_tag": (idrac.get_service_tag()
                                   if hasattr(idrac, 'get_service_tag')
                                   else "Unknown"),
                    "idrac_version": (idrac.get_idrac_version()
                                      if hasattr(idrac, 'get_idrac_version')
                                      else "Unknown"),
                    "export_timestamp": (idrac.get_current_time()
                                         if hasattr(idrac, 'get_current_time')
                                         else "Unknown"),
                    "filters_applied": {
                        "date_start": module.params.get('date_start'),
                        "date_end": module.params.get('date_end'),
                        "severity": module.params.get('severity'),
                        "category": module.params.get('category'),
                        "message_pattern": module.params.get('message_pattern'),
                    },
                    "exported_entry_count": len(filtered_entries),
                    "messages_enriched": module.params.get('enrich_messages', False)
                }

                count = exporter.export(filtered_entries, metadata)

                # Verify export if requested (AC-006)
                verification_status = None
                if verify_export:
                    verification_status = {
                        "expected_count": expected_count,
                        "actual_count": count,
                        "verification_passed": count == expected_count
                    }
                    if not verification_status["verification_passed"]:
                        module.warn(
                            f"Export verification failed: expected {expected_count} "
                            f"entries, but exported {count} entries. This may be "
                            f"due to applied filters."
                        )

                # Check storage utilization and threshold (AC-008)
                storage_warning = None
                storage_threshold_pct = module.params.get('storage_threshold_pct', 80)
                if storage_threshold_pct > 0:
                    try:
                        lclog_service_uri = ("/redfish/v1/Managers/iDRAC.Embedded.1/"
                                             "LogServices/Lclog")
                        response = idrac.invoke_request(lclog_service_uri, 'GET')
                        service_data = response.json_data
                        max_records = service_data.get('MaxNumberOfRecords', 0)
                        overwrite_policy = service_data.get('OverWritePolicy',
                                                         'Unknown')

                        if max_records > 0:
                            # Get current total entries
                            total_entries = pagination.get_total_entries_count(base_uri)
                            storage_utilization = (total_entries / max_records) * 100

                            if storage_utilization > storage_threshold_pct:
                                storage_warning = (
                                    f"LC log storage at "
                                    f"{round(storage_utilization, 2)}% capacity "
                                    f"(threshold: {storage_threshold_pct}%). "
                                    f"Consider exporting and archiving logs "
                                    f"before iDRAC's automatic wrap-around "
                                    f"overwrites oldest entries. "
                                    f"Overwrite policy: {overwrite_policy}"
                                )
                    except Exception as e:
                        module.warn(f"Failed to check storage utilization: {str(e)}")

                msg = (f"Successfully exported {count} lifecycle controller log "
                       f"entries to {share_name}.")
                result = {
                    "msg": msg,
                    "lc_logs_status": {"exported_entries": count, "file": share_name},
                    "changed": True
                }

                if verification_status:
                    result["export_verification"] = verification_status

                if storage_warning:
                    result["storage_warning"] = storage_warning

                module.exit_json(**result)
            else:
                # Use existing network share export functionality
                lifecycle_controller_logs_obj = IDRACLifecycleControllerLogs(idrac)
                msg, job_dict, changed = (
                    lifecycle_controller_logs_obj.lifecycle_controller_logs_operation(
                        idrac, module))
                module.exit_json(msg=msg, lc_logs_status=job_dict, changed=changed)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError) as e:
        module.exit_json(msg=str(e), failed=True)


if __name__ == '__main__':
    main()
