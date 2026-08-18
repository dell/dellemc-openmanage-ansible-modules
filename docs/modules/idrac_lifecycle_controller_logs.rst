.. _idrac_lifecycle_controller_logs_module:


idrac_lifecycle_controller_logs -- Export Lifecycle Controller logs to a network share or local path with advanced features.
=============================================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Export Lifecycle Controller logs to a given network share or local path.

Support for filtering by date range, severity, category, and message content.

Support for multi-format export (JSON, CSV, text) with metadata envelope.

Support for compliance export verification, filter optimization, storage monitoring, and comment insertion.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  share_name (True, str, None)
    Network share or local path.

    CIFS, NFS network share types are supported.


  share_user (optional, str, None)
    Network share user in the format 'user@domain' or 'domain\\user' if user is part of a domain else 'user'. This option is mandatory for CIFS Network Share.


  share_password (optional, str, None)
    Network share user password. This option is mandatory for CIFS Network Share.


  job_wait (optional, bool, True)
    Whether to wait for the running job completion or not.


  date_start (optional, str, None)
    Start date for filtering log entries (ISO 8601 format).

    Only entries created on or after this date are included.

    Uses server-side OData $filter for efficient querying.

    Example format - 2026-08-01T00:00:00Z or 2026-08-01.


  date_end (optional, str, None)
    End date for filtering log entries (ISO 8601 format).

    Only entries created on or before this date are included.

    Uses server-side OData $filter for efficient querying.

    Must not be earlier than \ :emphasis:`date\_start`\ .

    Example format - 2026-08-31T23:59:59Z or 2026-08-31.


  severity (optional, list, None)
    List of severity levels to filter log entries.

    Uses server-side OData $filter for efficient querying.

    Valid values are \ :literal:`Critical`\ , \ :literal:`Warning`\ , and \ :literal:`OK`\ .


  category (optional, list, None)
    List of Dell OEM categories to filter log entries.

    Uses server-side OData $filter for efficient querying.

    Common categories include Audit, Configuration, Updates, SystemHealth, Storage, and WorkNotes.


  message_contains (optional, str, None)
    Substring to search for in log messages (case-insensitive).

    Applied client-side after server-side filters.

    Use for searching specific keywords in log messages.


  export_format (optional, str, json)
    Format for exporting log entries to local file.

    \ :literal:`json`\  exports with metadata envelope including server info and filters applied.

    \ :literal:`csv`\  exports as comma-delimited file with header row.

    \ :literal:`text`\  exports one entry per line in human-readable format.

    Only applicable when exporting to local path.


  fetch_metadata_only (optional, bool, False)
    Fetch only log service metadata without retrieving log entries.

    Returns statistics like total entries, oldest/newest timestamps, severity breakdown.

    Only applicable when using local file path.


  verify_export (optional, bool, False)
    Enable compliance export verification with entry count comparison.

    When enabled, compares expected vs actual entry count after export.

    Returns export_verification field with verification results.


  filter_optimization (optional, str, auto)
    Filter optimization mode for combined filter operations.

    \ :literal:`single_query`\  uses server-side filtering with OData query parameters.

    \ :literal:`sequential`\  applies filters sequentially on client side.

    \ :literal:`auto`\  automatically selects the best mode based on filter complexity.


  storage_threshold_pct (optional, int, 80)
    Storage overflow monitoring threshold percentage.

    When storage utilization exceeds this threshold, a warning is returned.

    Set to 0 to disable storage monitoring.

    Default is 80 percent.


  insert_comment (optional, str, None)
    Insert a custom comment into the LC logs during automation workflows.

    Maximum length is 256 characters.

    Requires ConfigureManager or Login+TestAlerts privilege.

    Returns inserted_entry_id and inserted_entry_timestamp on success.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.

    If the username is not provided, then the environment variable \ :envvar:`IDRAC\_USERNAME`\  is used.

    Example: export IDRAC\_USERNAME=username


  idrac_password (True, str, None)
    iDRAC user password.

    If the password is not provided, then the environment variable \ :envvar:`IDRAC\_PASSWORD`\  is used.

    Example: export IDRAC\_PASSWORD=password


  idrac_port (optional, int, 443)
    iDRAC port.


  validate_certs (optional, bool, True)
    If \ :literal:`false`\ , the SSL certificates will not be validated.

    Configure \ :literal:`false`\  only on personally controlled sites where self-signed certificates are used.

    Prior to collection version \ :literal:`5.0.0`\ , the \ :emphasis:`validate\_certs`\  is \ :literal:`false`\  by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.



Notes
-----

.. note::
   - This module requires 'Administrator' privilege for \ :emphasis:`idrac\_user`\ .
   - Exporting data to a local share is supported only on iDRAC9-based PowerEdge Servers and later.
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports both IPv4 and IPv6 address for \ :emphasis:`idrac\_ip`\ .
   - This module does not support \ :literal:`check\_mode`\ .
   - No job will be created when exporting data to a local share in iDRAC9 and iDRAC 10.
   - The insert_comment parameter requires ConfigureManager or Login+TestAlerts privilege.
   - Server-side OData $filter is used for date_start, date_end, severity, and category filters.
   - The message_contains filter is applied client-side after server-side filtering.




Examples
--------

.. code-block:: yaml+jinja

    
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



Return Values
-------------

msg (always, str, Successfully exported the lifecycle controller logs.)
  Status of the export lifecycle controller logs job.


lc_logs_status (success, dict, {'ElapsedTimeSinceCompletion': '0', 'InstanceID': 'JID_274774785395', 'JobStartTime': 'NA', 'JobStatus': 'Completed', 'JobUntilTime': 'NA', 'Message': 'LCL Export was successful', 'MessageArguments': 'NA', 'MessageID': 'LC022', 'Name': 'LC Export', 'PercentComplete': '100', 'Status': 'Success', 'file': '192.168.0.0:/nfsfileshare/190.168.0.1_20210728_133437_LC_Log.log', 'retval': True})
  Status of the export operation along with job details and file path.


lc_logs (when filters are applied, list, [{'Id': '1', 'Created': '2026-08-17T10:00:00Z', 'Severity': 'Critical', 'Message': 'System temperature exceeded threshold', 'MessageId': 'SYS001'}])
  List of filtered log entries when filters are applied.


exported_entry_count (when export_format is specified, int, 150)
  Number of log entries exported to file.


filters_applied (when any filter parameter is specified, dict, {'date_start': '2026-08-01T00:00:00Z', 'date_end': '2026-08-31T23:59:59Z', 'severity': ['Critical', 'Warning'], 'category': ['Audit'], 'message_contains': 'firmware'})
  Summary of filters that were applied to the query.


log_metadata (when fetch_metadata_only is true, dict, {'total_entries': 150, 'oldest_timestamp': '2026-01-01T00:00:00Z', 'newest_timestamp': '2026-08-18T12:00:00Z', 'severity_breakdown': {'Critical': 5, 'Warning': 20, 'OK': 100, 'Other': 25}, 'storage_utilization_pct': 75.0, 'max_records': 200, 'overwrite_policy': 'WrapsWhenFull'})
  Log service metadata when fetch_metadata_only is true.


export_verification (when verify_export is true, dict, {'expected_count': 150, 'actual_count': 150, 'verified': True, 'message': 'Export verification successful'})
  Export verification results when verify_export is true.


storage_warning (when storage utilization exceeds storage_threshold_pct, str, LC log storage at 85.5% capacity (threshold 80%). Consider exporting and archiving.)
  Storage overflow warning when utilization exceeds threshold.


inserted_entry_id (when insert_comment is provided, str, LC123456)
  ID of the inserted comment entry.


inserted_entry_timestamp (when insert_comment is provided, str, 2026-08-18T12:00:00Z)
  Timestamp of the inserted comment entry.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Rajeev Arakkal (@rajeevarakkal)
- Anooja Vardhineni (@anooja-vardhineni)
- Sapana Gupta (@sapana05)
