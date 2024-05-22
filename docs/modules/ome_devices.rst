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

- python \>= 3.9.6



Parameters
----------

  device_service_tags (optional, list, None)
    Service tag of the target devices.

    This is mutually exclusive with \ :emphasis:`device\_ids`\ .


  device_ids (optional, list, None)
    IDs of the target devices.

    This is mutually exclusive with \ :emphasis:`device\_service\_tags`\ .


  state (optional, str, present)
    \ :literal:`present`\  Allows to perform the \ :emphasis:`device\_action`\  on the target devices.

    \ :literal:`absent`\  Removes the device from OpenManage Enterprise. Job is not triggered. \ :emphasis:`job\_wait`\ , \ :emphasis:`job\_schedule`\ , \ :emphasis:`job\_name`\ , and \ :emphasis:`job\_description`\  are not applicable to this operation.


  device_action (optional, str, refresh_inventory)
    \ :literal:`refresh\_inventory`\  refreshes the inventory on the target devices.

    \ :literal:`reset\_idrac`\  Triggers a reset on the target iDRACs.

    \ :literal:`clear\_idrac\_job\_queue`\  Clears the job queue on the target iDRACs.

    A job is triggered for each action.


  job_wait (optional, bool, True)
    Provides an option to wait for the job completion.

    This option is applicable when \ :emphasis:`state`\  is \ :literal:`present`\ .

    This is applicable when \ :emphasis:`job\_schedule`\  is \ :literal:`startnow`\ .


  job_wait_timeout (optional, int, 1200)
    The maximum wait time of \ :emphasis:`job\_wait`\  in seconds. The job is tracked only for this duration.

    This option is applicable when \ :emphasis:`job\_wait`\  is \ :literal:`true`\ .


  job_schedule (optional, str, startnow)
    Provide the cron string to schedule the job.


  job_name (optional, str, None)
    Optional name for the job.


  job_description (optional, str, None)
    Optional description for the job.


  hostname (True, str, None)
    OpenManage Enterprise IP address or hostname.


  username (False, str, None)
    OpenManage Enterprise username.

    If the username is not provided, then the environment variable \ :envvar:`OME\_USERNAME`\  is used.

    Example: export OME\_USERNAME=username


  password (False, str, None)
    OpenManage Enterprise password.

    If the password is not provided, then the environment variable \ :envvar:`OME\_PASSWORD`\  is used.

    Example: export OME\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`OME\_X\_AUTH\_TOKEN`\  is used.

    Example: export OME\_X\_AUTH\_TOKEN=x\_auth\_token


  port (optional, int, 443)
    OpenManage Enterprise HTTPS port.


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
   - For \ :literal:`idrac\_reset`\ , the job triggers only the iDRAC reset operation and does not track the complete reset cycle.
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.
   - This module supports \ :literal:`check\_mode`\ .




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
- ShivamSh3(@ShivamSh3)

