.. _ome_devices_module:


ome_devices -- Perform device-specific operations on target devices
===================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Perform device-specific operations such as refresh inventory, clear iDRAC job queue, and reset iDRAC from OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  device_service_tags (optional, list, None)
    Service tag of the target devices.

    This is mutually exclusive with *device_ids*.


  device_ids (optional, list, None)
    IDs of the target devices.

    This is mutually exclusive with *device_service_tags*.


  state (optional, str, present)
    ``present`` Allows to perform the *device_action* on the target devices.

    ``absent`` Removes the device from OpenManage Enterprise. Job is not triggered. *job_wait*, *job_schedule*, *job_name*, and *job_description* are not applicable to this operation.


  device_action (optional, str, refresh_inventory)
    ``refresh_inventory`` refreshes the inventory on the target devices.

    ``reset_idrac`` Triggers a reset on the target iDRACs.

    ``clear_idrac_job_queue`` Clears the job queue on the target iDRACs.

    A job is triggered for each action.


  job_wait (optional, bool, True)
    Provides an option to wait for the job completion.

    This option is applicable when *state* is ``present``.

    This is applicable when *job_schedule* is ``startnow``.


  job_wait_timeout (optional, int, 1200)
    The maximum wait time of *job_wait* in seconds. The job is tracked only for this duration.

    This option is applicable when *job_wait* is ``True``.


  job_schedule (optional, str, startnow)
    Provide the cron string to schedule the job.


  job_name (optional, str, None)
    Optional name for the job.


  job_description (optional, str, None)
    Optional description for the job.


  hostname (True, str, None)
    OpenManage Enterprise IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise username.


  password (True, str, None)
    OpenManage Enterprise password.


  port (optional, int, 443)
    OpenManage Enterprise HTTPS port.


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
   - For ``idrac_reset``, the job triggers only the iDRAC reset operation and does not track the complete reset cycle.
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Refresh Inventory
      dellemc.openmanage.ome_devices:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_action: refresh_inventory
        device_service_tags:
          - SVCTAG1

    - name: Clear iDRAC job queue
      dellemc.openmanage.ome_devices:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_action: clear_idrac_job_queue
        device_service_tags:
          - SVCTAG1

    - name: Reset iDRAC using the service tag
      dellemc.openmanage.ome_devices:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_action: reset_idrac
        device_service_tags:
          - SVCTAG1

    - name: Remove devices using servicetags
      dellemc.openmanage.ome_devices:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: absent
        device_service_tags:
          - SVCTAG1
          - SVCTAF2

    - name: Remove devices using IDs
      dellemc.openmanage.ome_devices:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: absent
        device_ids:
          - 10235



Return Values
-------------

msg (always, str, Successfully removed the device(s).)
  Overall status of the devices operation.


job (success, dict, {'Id': 14874, 'JobName': 'Refresh inventory', 'JobDescription': "The Refresh inventory task initiated from OpenManage Ansible Modules for devices with the ids '13216'.", 'Schedule': 'startnow', 'State': 'Enabled', 'CreatedBy': 'admin', 'UpdatedBy': None, 'Visible': True, 'Editable': True, 'Builtin': False, 'UserGenerated': True, 'Targets': [{'JobId': 14874, 'Id': 13216, 'Data': '', 'TargetType': {'Id': 1000, 'Name': 'DEVICE'}}], 'Params': [{'JobId': 14874, 'Key': 'action', 'Value': 'CONFIG_INVENTORY'}, {'JobId': 14874, 'Key': 'isCollectDriverInventory', 'Value': 'true'}], 'LastRunStatus': {'@odata.type': '#JobService.JobStatus', 'Id': 2060, 'Name': 'Completed'}, 'JobType': {'@odata.type': '#JobService.JobType', 'Id': 8, 'Name': 'Inventory_Task', 'Internal': False}, 'JobStatus': {'@odata.type': '#JobService.JobStatus', 'Id': 2020, 'Name': 'Scheduled'}, 'ExecutionHistories@odata.navigationLink': '/api/JobService/Jobs(14874)/ExecutionHistories', 'LastExecutionDetail': {'@odata.id': '/api/JobService/Jobs(14874)/LastExecutionDetail'}})
  Job details of the devices operation.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'CGEN1002', 'RelatedProperties': [], 'Message': 'Unable to complete the operation because the requested URI is invalid.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Enter a valid URI and retry the operation.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

