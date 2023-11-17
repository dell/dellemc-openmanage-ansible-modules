.. _ome_job_info_module:


ome_job_info -- Get job details for a given job ID or an entire job queue on OpenMange Enterprise
=================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves job details for a given job ID or an entire job queue on OpenMange Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  job_id (optional, int, None)
    Unique ID of the job.


  system_query_options (optional, dict, None)
    Options for pagination of the output.


    top (optional, int, None)
      Number of records to return. Default value is 100.


    skip (optional, int, None)
      Number of records to skip. Default value is 0.


    filter (optional, str, None)
      Filter records by the values supported.



  fetch_execution_history (optional, bool, False)
    Fetches the execution history of the job.

    *fetch_execution_history* is only applicable when valid *job_id* is given.

    When ``true``, fetches all the execution history details.

    When ``false``, fetches only the job info and last execution details.


  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.


  password (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.


  validate_certs (optional, bool, True)
    If ``false``, the SSL certificates will not be validated.

    Configure ``false`` only on personally controlled sites where self-signed certificates are used.

    Prior to collection version ``5.0.0``, the *validate_certs* is ``false`` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Get all jobs details
      dellemc.openmanage.ome_job_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"

    - name: Get job details for id
      dellemc.openmanage.ome_job_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        job_id: 12345

    - name: Get filtered job details
      dellemc.openmanage.ome_job_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        system_query_options:
          top: 2
          skip: 1
          filter: "JobType/Id eq 8"

    - name: Get detail job execution history with last execution detail for a job.
      dellemc.openmanage.ome_job_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        job_id: 12345
        fetch_execution_history: true



Return Values
-------------

msg (always, str, Successfully fetched the job info)
  Overall status of the job facts operation.


job_info (success, dict, {'value': [{'Id': 10429, 'JobName': 'Discovery-201', 'JobDescription': 'Discovery-201', 'NextRun': None, 'LastRun': '2023-06-07 09:33:07.161', 'StartTime': None, 'EndTime': None, 'Schedule': 'startnow', 'State': 'Enabled', 'CreatedBy': 'admin', 'UpdatedBy': 'admin', 'Visible': True, 'Editable': True, 'Builtin': False, 'UserGenerated': True, 'Targets': [], 'Params': [], 'LastRunStatus': {'Id': 2070, 'Name': 'Failed'}, 'JobType': {'Id': 101, 'Name': 'Discovery_Task', 'Internal': False}, 'JobStatus': {'Id': 2080, 'Name': 'New'}, 'ExecutionHistories': [{'Id': 1243224, 'JobName': 'Discovery-201', 'Progress': '100', 'StartTime': '2023-06-07 09:33:07.148', 'EndTime': '2023-06-07 09:33:08.403', 'LastUpdateTime': '2023-06-07 09:33:08.447185', 'ExecutedBy': 'admin', 'JobId': 10429, 'JobStatus': {'Id': 2070, 'Name': 'Failed'}, 'ExecutionHistoryDetails': [{'Id': 1288519, 'Progress': '100', 'StartTime': '2023-06-07 09:33:07.525', 'EndTime': '2023-06-07 09:33:08.189', 'ElapsedTime': '00:00:00', 'Key': '198.168.0.1', 'Value': 'Running\nDiscovery of target 198.168.0.1 started .\nDiscovery target resolved to IP  198.168.0.1 .\n: ========== EEMI Code: CGEN1009 ==========\nMessage: Unable to perform the requested action because the device management endpoint authentication over WSMAN, REDFISH failed. \nRecommended actions: Make sure the credentials associated with the device management endpoint are valid and retry the operation.\n=======================================\nTask Failed. Completed With Errors.', 'ExecutionHistoryId': 1243224, 'IdBaseEntity': 0, 'JobStatus': {'Id': 2070, 'Name': 'Failed'}}, {'Id': 1288518, 'Progress': '100', 'StartTime': '2023-06-07 09:33:07.521', 'EndTime': '2023-06-07 09:33:08.313', 'ElapsedTime': '00:00:00', 'Key': '198.168.0.2', 'Value': 'Running\nDiscovery of target 198.168.0.2 started. \nDiscovery target resolved to IP  198.168.0.2 .\n: ========== EEMI Code: CGEN1009 ==========\nMessage: Unable to perform the requested action because the device management endpoint authentication over WSMAN, REDFISH failed. \nRecommended actions: Make sure the credentials associated with the device management endpoint are valid and retry the operation.\n=======================================\nTask Failed. Completed With Errors.', 'ExecutionHistoryId': 1243224, 'IdBaseEntity': 0, 'JobStatus': {'Id': 2070, 'Name': 'Failed'}}]}, {'Id': 1243218, 'JobName': 'Discovery-201', 'Progress': '100', 'StartTime': '2023-06-07 09:30:55.064', 'EndTime': '2023-06-07 09:30:56.338', 'LastUpdateTime': '2023-06-07 09:30:56.365294', 'ExecutedBy': 'admin', 'JobId': 10429, 'JobStatus': {'Id': 2070, 'Name': 'Failed'}, 'ExecutionHistoryDetails': [{'Id': 1288512, 'Progress': '100', 'StartTime': '2023-06-07 09:30:55.441', 'EndTime': '2023-06-07 09:30:56.085', 'ElapsedTime': '00:00:00', 'Key': '198.168.0.1', 'Value': 'Running\nDiscovery of target 198.168.0.1 started. \nDiscovery target resolved to IP  198.168.0.1 .\n: ========== EEMI Code: CGEN1009 ==========\nMessage: Unable to perform the requested action because the device management endpoint authentication over WSMAN, REDFISH failed. \nRecommended actions: Make sure the credentials associated with the device management endpoint are valid and retry the operation.\n=======================================\nTask Failed. Completed With Errors.', 'ExecutionHistoryId': 1243218, 'IdBaseEntity': 0, 'JobStatus': {'Id': 2070, 'Name': 'Failed'}}, {'Id': 1288511, 'Progress': '100', 'StartTime': '2023-06-07 09:30:55.439', 'EndTime': '2023-06-07 09:30:56.21', 'ElapsedTime': '00:00:00', 'Key': '198.168.0.2', 'Value': 'Running\nDiscovery of target 198.168.0.2 started. \nDiscovery target resolved to IP  198.168.0.2 .\n: ========== EEMI Code: CGEN1009 ==========\nMessage: Unable to perform the requested action because the device management endpoint authentication over WSMAN, REDFISH failed. \nRecommended actions: Make sure the credentials associated with the device management endpoint are valid and retry the operation.\n=======================================\nTask Failed. Completed With Errors.', 'ExecutionHistoryId': 1243218, 'IdBaseEntity': 0, 'JobStatus': {'Id': 2070, 'Name': 'Failed'}}]}], 'LastExecutionDetail': {'Id': 1288519, 'Progress': '100', 'StartTime': '2023-06-07 09:33:07.525', 'EndTime': '2023-06-07 09:33:08.189', 'ElapsedTime': None, 'Key': '198.168.0.1', 'Value': 'Running\nDiscovery of target 198.168.0.1 started. \nDiscovery target resolved to IP  198.168.0.1 .\n: ========== EEMI Code: CGEN1009 ==========\nMessage: Unable to perform the requested action because the device management endpoint authentication over WSMAN, REDFISH failed. \nRecommended actions: Make sure the credentials associated with the device management endpoint are valid and retry the operation. \n=======================================\nTask Failed. Completed With Errors.', 'ExecutionHistoryId': 1243224, 'IdBaseEntity': 0, 'JobStatus': {'Id': 2070, 'Name': 'Failed'}}}]})
  Details of the OpenManage Enterprise jobs.





Status
------





Authors
~~~~~~~

- Jagadeesh N V (@jagadeeshnv)
- Abhishek Sinha (@Abhishek-Dell)

