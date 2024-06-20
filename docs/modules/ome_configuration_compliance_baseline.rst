.. _ome_configuration_compliance_baseline_module:


ome_configuration_compliance_baseline -- Create, modify, and delete a configuration compliance baseline and remediate non-compliant devices on OpenManage Enterprise
====================================================================================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to create, modify, and delete a configuration compliance baseline on OpenManage Enterprise. This module also allows to remediate devices that are non-compliant with the baseline by changing the attributes of devices to match with the associated baseline attributes.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  command (optional, str, create)
    \ :literal:`create`\  creates a configuration baseline from an existing compliance template.\ :literal:`create`\  supports \ :literal:`check\_mode`\  or idempotency checking for only \ :emphasis:`names`\ .

    \ :literal:`modify`\  modifies an existing baseline.Only \ :emphasis:`names`\ , \ :emphasis:`description`\ , \ :emphasis:`device\_ids`\ , \ :emphasis:`device\_service\_tags`\ , and \ :emphasis:`device\_group\_names`\  can be modified

    \ :emphasis:`WARNING`\  When a baseline is modified, the provided \ :emphasis:`device\_ids`\ , \ :emphasis:`device\_group\_names`\ , and \ :emphasis:`device\_service\_tags`\  replaces the devices previously present in the baseline.

    \ :literal:`delete`\  deletes the list of configuration compliance baselines based on the baseline name. Invalid baseline names are ignored.

    \ :literal:`remediate`\  remediates devices that are non-compliant with the baseline by changing the attributes of devices to match with the associated baseline attributes.

    \ :literal:`remediate`\  is performed on all the non-compliant devices if either \ :emphasis:`device\_ids`\ , or \ :emphasis:`device\_service\_tags`\  is not provided.


  names (True, list, None)
    Name(s) of the configuration compliance baseline.

    This option is applicable when \ :emphasis:`command`\  is \ :literal:`create`\ , \ :literal:`modify`\ , or \ :literal:`delete`\ .

    Provide the list of configuration compliance baselines names that are supported when \ :emphasis:`command`\  is \ :literal:`delete`\ .


  new_name (optional, str, None)
    New name of the compliance baseline to be modified.

    This option is applicable when \ :emphasis:`command`\  is \ :literal:`modify`\ .


  template_name (optional, str, None)
    Name of the compliance template for creating the compliance baseline(s).

    Name of the deployment template to be used for creating a compliance baseline.

    This option is applicable when \ :emphasis:`command`\  is \ :literal:`create`\  and is mutually exclusive with \ :emphasis:`template\_id`\ .


  template_id (optional, int, None)
    ID of the deployment template to be used for creating a compliance baseline.

    This option is applicable when \ :emphasis:`command`\  is \ :literal:`create`\  and is mutually exclusive with \ :emphasis:`template\_name`\ .


  device_ids (optional, list, None)
    IDs of the target devices.

    This option is applicable when \ :emphasis:`command`\  is \ :literal:`create`\ , \ :literal:`modify`\ , or \ :literal:`remediate`\ , and is mutually exclusive with \ :emphasis:`device\_service\_tag`\  and \ :emphasis:`device\_group\_names`\ .


  device_service_tags (optional, list, None)
    Service tag of the target device.

    This option is applicable when \ :emphasis:`command`\  is \ :literal:`create`\ , \ :literal:`modify`\ , or \ :literal:`remediate`\  and is mutually exclusive with \ :emphasis:`device\_ids`\  and \ :emphasis:`device\_group\_names`\ .


  device_group_names (optional, list, None)
    Name of the target device group.

    This option is applicable when \ :emphasis:`command`\  is \ :literal:`create`\ , or \ :literal:`modify`\  and is mutually exclusive with \ :emphasis:`device\_ids`\  and \ :emphasis:`device\_service\_tag`\ .


  description (optional, str, None)
    Description of the compliance baseline.

    This option is applicable when \ :emphasis:`command`\  is \ :literal:`create`\ , or \ :literal:`modify`\ .


  run_later (optional, bool, None)
    Indicates whether to remediate immediately or in the future.

    This is applicable when \ :emphasis:`command`\  is \ :literal:`remediate`\ .

    If \ :emphasis:`run\_later`\  is \ :literal:`true`\ , then \ :emphasis:`staged\_at\_reboot`\  is ignored.

    If \ :emphasis:`run\_later`\  is \ :literal:`true`\ , then \ :emphasis:`job\_wait`\  is not applicable.

    If \ :emphasis:`run\_later`\  is \ :literal:`true`\ , then \ :emphasis:`cron`\  must be specified.


  cron (optional, str, None)
    Provide a cron expression based on Quartz cron format.

    Time format is "%S %M %H %d %m ? %Y".

    This is applicable when \ :emphasis:`run\_later`\  is \ :literal:`true`\ .


  staged_at_reboot (optional, bool, None)
    Indicates whether remediate has to be executed on next reboot.

    If \ :emphasis:`staged\_at\_reboot`\  is \ :literal:`true`\ , then remediation will occur during the next reboot.


  job_wait (optional, bool, True)
    Provides the option to wait for job completion.

    This option is applicable when \ :emphasis:`command`\  is \ :literal:`create`\ , \ :literal:`modify`\ , or \ :literal:`remediate`\ .


  job_wait_timeout (optional, int, 10800)
    The maximum wait time of \ :emphasis:`job\_wait`\  in seconds.The job will only be tracked for this duration.

    This option is applicable when \ :emphasis:`job\_wait`\  is \ :literal:`true`\ .


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
   - This module supports \ :literal:`check\_mode`\ .
   - Ensure that the devices have the required licenses to perform the baseline compliance operations.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create a configuration compliance baseline using device IDs
      dellemc.openmanage.ome_configuration_compliance_baseline:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        names: "baseline1"
        template_name: "template1"
        description: "description of baseline"
        device_ids:
          - 1111
          - 2222

    - name: Create a configuration compliance baseline using device service tags
      dellemc.openmanage.ome_configuration_compliance_baseline:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        names: "baseline1"
        template_id: 1234
        description: "description of baseline"
        device_service_tags:
          - "SVCTAG1"
          - "SVCTAG2"

    - name: Create a configuration compliance baseline using group names
      dellemc.openmanage.ome_configuration_compliance_baseline:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        names: "baseline2"
        template_id: 2
        job_wait_timeout: 1000
        description: "description of baseline"
        device_group_names:
          - "Group1"
          - "Group2"

    - name: Delete the configuration compliance baselines
      dellemc.openmanage.ome_configuration_compliance_baseline:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: delete
        names:
          - baseline1
          - baseline2

    - name: Modify a configuration compliance baseline using group names
      dellemc.openmanage.ome_configuration_compliance_baseline:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: modify
        names: "baseline1"
        new_name: "baseline_update"
        template_name: "template2"
        description: "new description of baseline"
        job_wait_timeout: 1000
        device_group_names:
          - Group1

    - name: Remediate specific non-compliant devices to a configuration compliance baseline using device IDs
      dellemc.openmanage.ome_configuration_compliance_baseline:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: "remediate"
        names: "baseline1"
        device_ids:
          - 1111

    - name: Remediate specific non-compliant devices to a configuration compliance baseline using device service tags
      dellemc.openmanage.ome_configuration_compliance_baseline:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: "remediate"
        names: "baseline1"
        device_service_tags:
          - "SVCTAG1"
          - "SVCTAG2"

    - name: Remediate all the non-compliant devices to a configuration compliance baseline
      dellemc.openmanage.ome_configuration_compliance_baseline:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: "remediate"
        names: "baseline1"

    - name: Remediate specific non-compliant devices to a configuration compliance baseline using device IDs at scheduled time
      dellemc.openmanage.ome_configuration_compliance_baseline:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: "remediate"
        names: "baseline1"
        device_ids:
          - 1111
        run_later: true
        cron: "0 10 11 14 02 ? 2032"  # Feb 14,2032 11:10:00

    - name: Remediate specific non-compliant devices to a configuration compliance baseline using device service tags on next reboot
      dellemc.openmanage.ome_configuration_compliance_baseline:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: "remediate"
        names: "baseline1"
        device_service_tags:
          - "SVCTAG1"
          - "SVCTAG2"
        staged_at_reboot: true



Return Values
-------------

msg (always, str, Successfully created the configuration compliance baseline.)
  Overall status of the configuration compliance baseline operation.


incompatible_devices (when I(device_service_tags) or I(device_ids) contains incompatible devices for C(create) or C(modify), list, [1234, 5678])
  Details of the devices which cannot be used to perform baseline compliance operations


compliance_status (when I(command) is C(create) or C(modify), dict, {'Id': 13, 'Name': 'baseline1', 'Description': None, 'TemplateId': 102, 'TemplateName': 'one', 'TemplateType': 2, 'TaskId': 26584, 'PercentageComplete': '100', 'TaskStatus': 2070, 'LastRun': '2021-02-27 13:15:13.751', 'BaselineTargets': [{'Id': 1111, 'Type': {'Id': 1000, 'Name': 'DEVICE'}}], 'ConfigComplianceSummary': {'ComplianceStatus': 'OK', 'NumberOfCritical': 0, 'NumberOfWarning': 0, 'NumberOfNormal': 0, 'NumberOfIncomplete': 0}})
  Status of compliance baseline operation.


job_id (when I(command) is C(remediate), int, 14123)
  Task ID created when \ :emphasis:`command`\  is \ :literal:`remediate`\ .


job_details (on job failure, list, [{'ElapsedTime': '00:22:17', 'EndTime': '2024-06-19 13:42:41.285', 'ExecutionHistoryId': 797320, 'Id': 14123, 'IdBaseEntity': 19559, 'JobStatus': {'Id': 2070, 'Name': 'Failed'}, 'Key': 'SVCTAG1', 'Progress': '100', 'StartTime': '2024-06-19 13:20:23.495', 'Value': 'Starting Pre-checks....LC status is : InUse, wait for 30 seconds and retry ...(1)'}])
  Details of the failed job.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Sajna Shetty(@Sajna-Shetty)
- Abhishek Sinha(@Abhishek-Dell)
- Shivam Sharma(@ShivamSh3)

