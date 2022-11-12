.. _ome_diagnostics_module:


ome_diagnostics -- Export technical support logs(TSR) to network share location
===============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to export SupportAssist collection logs from OpenManage Enterprise and OpenManage Enterprise Modular and application logs from OpenManage Enterprise Modular to a CIFS or NFS share.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  device_ids (optional, list, None)
    List of target device IDs.

    This is applicable for ``support_assist_collection`` and ``supportassist_collection`` logs.

    This option is mutually exclusive with *device_service_tags* and *device_group_name*.


  device_service_tags (optional, list, None)
    List of target identifier.

    This is applicable for ``support_assist_collection`` and ``supportassist_collection`` logs.

    This option is mutually exclusive with *device_ids* and *device_group_name*.


  device_group_name (optional, str, None)
    Name of the device group to export ``support_assist_collection`` or ``supportassist_collection`` logs of all devices within the group.

    This is applicable for ``support_assist_collection`` and ``supportassist_collection`` logs.

    This option is not applicable for OpenManage Enterprise Modular.

    This option is mutually exclusive with *device_ids* and *device_service_tags*.


  log_type (optional, str, support_assist_collection)
    ``application`` is applicable for OpenManage Enterprise Modular to export the application log bundle.

    ``support_assist_collection`` and ``supportassist_collection`` is applicable for one or more devices to export SupportAssist logs.

    ``support_assist_collection`` and ``supportassist_collection`` supports both OpenManage Enterprise and OpenManage Enterprise Modular.

    ``support_assist_collection`` and ``supportassist_collection`` does not support export of ``OS_LOGS`` from OpenManage Enterprise. If tried to export, the tasks will complete with errors, and the module fails.


  mask_sensitive_info (optional, bool, False)
    Select this option to mask the personal identification information such as IPAddress, DNS, alert destination, email, gateway, inet6, MacAddress, netmask etc.

    This option is applicable for ``application`` of *log_type*.


  log_selectors (optional, list, None)
    By default, the SupportAssist logs contain only hardware logs. To collect additional logs such as OS logs, RAID logs or Debug logs, specify the log types to be collected in the choices list.

    If the log types are not specified, only the hardware logs are exported.

    ``OS_LOGS`` to collect OS Logs.

    ``RAID_LOGS`` to collect RAID controller logs.

    ``DEBUG_LOGS`` to collect Debug logs.

    This option is applicable only for ``support_assist_collection`` and ``supportassist_collection`` of *log_type*.


  share_address (True, str, None)
    Network share IP address.


  share_name (True, str, None)
    Network share path.

    Filename is auto generated and should not be provided as part of *share_name*.


  share_type (True, str, None)
    Network share type


  share_user (optional, str, None)
    Network share username.

    This option is applicable for ``CIFS`` of *share_type*.


  share_password (optional, str, None)
    Network share password

    This option is applicable for ``CIFS`` of *share_type*.


  share_domain (optional, str, None)
    Network share domain name.

    This option is applicable for ``CIFS`` if *share_type*.


  job_wait (optional, bool, True)
    Whether to wait for the Job completion or not.

    The maximum wait time is *job_wait_timeout*.


  job_wait_timeout (optional, int, 60)
    The maximum wait time of *job_wait* in minutes.

    This option is applicable *job_wait* is true.


  test_connection (optional, bool, False)
    Test the availability of the network share location.

    *job_wait* and *job_wait_timeout* options are not applicable for *test_connection*.


  lead_chassis_only (optional, bool, False)
    Extract the logs from Lead chassis only.

    *lead_chassis_only* is only applicable when *log_type* is ``application`` on OpenManage Enterprise Modular.


  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.


  password (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.


  validate_certs (optional, bool, True)
    If ``False``, the SSL certificates will not be validated.

    Configure ``False`` only on personally controlled sites where self-signed certificates are used.

    Prior to collection version ``5.0.0``, the *validate_certs* is ``False`` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to OpenManage Enterprise.
   - This module performs the test connection and device validations. It does not create a job for copying the logs in check mode and always reports as changes found.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Export application log using CIFS share location
      dellemc.openmanage.ome_diagnostics:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        share_type: CIFS
        share_address: "192.168.0.2"
        share_user: share_username
        share_password: share_password
        share_name: cifs_share
        log_type: application
        mask_sensitive_info: false
        test_connection: true

    - name: Export application log using NFS share location
      dellemc.openmanage.ome_diagnostics:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        share_address: "192.168.0.3"
        share_type: NFS
        share_name: nfs_share
        log_type: application
        mask_sensitive_info: true
        test_connection: true

    - name: Export SupportAssist log using CIFS share location
      dellemc.openmanage.ome_diagnostics:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        share_address: "192.168.0.3"
        share_user: share_username
        share_password: share_password
        share_name: cifs_share
        share_type: CIFS
        log_type: support_assist_collection
        device_ids: [10011, 10022]
        log_selectors: [OS_LOGS]
        test_connection: true

    - name: Export SupportAssist log using NFS share location
      dellemc.openmanage.ome_diagnostics:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        share_address: "192.168.0.3"
        share_type: NFS
        share_name: nfs_share
        log_type: support_assist_collection
        device_group_name: group_name
        test_connection: true



Return Values
-------------

msg (always, str, Export log job completed successfully.)
  Overall status of the export log.


jog_status (success, dict, {'Builtin': False, 'CreatedBy': 'root', 'Editable': True, 'EndTime': 'None', 'Id': 12778, 'JobDescription': 'Export device log', 'JobName': 'Export Log', 'JobStatus': {'Id': 2080, 'Name': 'New'}, 'JobType': {'Id': 18, 'Internal': False, 'Name': 'DebugLogs_Task'}, 'LastRun': '2021-07-06 10:52:50.519', 'LastRunStatus': {'Id': 2060, 'Name': 'Completed'}, 'NextRun': 'None', 'Schedule': 'startnow', 'StartTime': 'None', 'State': 'Enabled', 'UpdatedBy': 'None', 'UserGenerated': True, 'Visible': True, 'Params': [{'JobId': 12778, 'Key': 'maskSensitiveInfo', 'Value': 'FALSE'}, {'JobId': 12778, 'Key': 'password', 'Value': 'tY86w7q92u0QzvykuF0gQQ'}, {'JobId': 12778, 'Key': 'userName', 'Value': 'administrator'}, {'JobId': 12778, 'Key': 'shareName', 'Value': 'iso'}, {'JobId': 12778, 'Key': 'OPERATION_NAME', 'Value': 'EXTRACT_LOGS'}, {'JobId': 12778, 'Key': 'shareType', 'Value': 'CIFS'}, {'JobId': 12778, 'Key': 'shareAddress', 'Value': '100.96.32.142'}], 'Targets': [{'Data': '', 'Id': 10053, 'JobId': 12778, 'TargetType': {'Id': 1000, 'Name': 'DEVICE'}}]})
  Details of the export log operation status.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)
- Sachin Apagundi(@sachin-apa)

