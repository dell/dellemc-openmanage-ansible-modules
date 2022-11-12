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

- python >= 3.8.6



Parameters
----------

  command (optional, str, create)
    ``create`` creates a configuration baseline from an existing compliance template.``create`` supports ``check_mode`` or idempotency checking for only *names*.

    ``modify`` modifies an existing baseline.Only *names*, *description*, *device_ids*, *device_service_tags*, and *device_group_names* can be modified

    *WARNING* When a baseline is modified, the provided *device_ids*, *device_group_names*, and *device_service_tags* replaces the devices previously present in the baseline.

    ``delete`` deletes the list of configuration compliance baselines based on the baseline name. Invalid baseline names are ignored.

    ``remediate`` remediates devices that are non-compliant with the baseline by changing the attributes of devices to match with the associated baseline attributes.

    ``remediate`` is performed on all the non-compliant devices if either *device_ids*, or *device_service_tags* is not provided.


  names (True, list, None)
    Name(s) of the configuration compliance baseline.

    This option is applicable when *command* is ``create``, ``modify``, or ``delete``.

    Provide the list of configuration compliance baselines names that are supported when *command* is ``delete``.


  new_name (optional, str, None)
    New name of the compliance baseline to be modified.

    This option is applicable when *command* is ``modify``.


  template_name (optional, str, None)
    Name of the compliance template for creating the compliance baseline(s).

    Name of the deployment template to be used for creating a compliance baseline.

    This option is applicable when *command* is ``create`` and is mutually exclusive with *template_id*.


  template_id (optional, int, None)
    ID of the deployment template to be used for creating a compliance baseline.

    This option is applicable when *command* is ``create`` and is mutually exclusive with *template_name*.


  device_ids (optional, list, None)
    IDs of the target devices.

    This option is applicable when *command* is ``create``, ``modify``, or ``remediate``, and is mutually exclusive with *device_service_tag* and *device_group_names*.


  device_service_tags (optional, list, None)
    Service tag of the target device.

    This option is applicable when *command* is ``create``, ``modify``, or ``remediate`` and is mutually exclusive with *device_ids* and *device_group_names*.


  device_group_names (optional, list, None)
    Name of the target device group.

    This option is applicable when *command* is ``create``, or ``modify`` and is mutually exclusive with *device_ids* and *device_service_tag*.


  description (optional, str, None)
    Description of the compliance baseline.

    This option is applicable when *command* is ``create``, or ``modify``.


  job_wait (optional, bool, True)
    Provides the option to wait for job completion.

    This option is applicable when *command* is ``create``, ``modify``, or ``remediate``.


  job_wait_timeout (optional, int, 10800)
    The maximum wait time of *job_wait* in seconds.The job will only be tracked for this duration.

    This option is applicable when *job_wait* is ``True``.


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
   - This module supports ``check_mode``.
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



Return Values
-------------

msg (always, str, Successfully created the configuration compliance baseline.)
  Overall status of the configuration compliance baseline operation.


incompatible_devices (when I(device_service_tags) or I(device_ids) contains incompatible devices for C(create) or C(modify), list, [1234, 5678])
  Details of the devices which cannot be used to perform baseline compliance operations


compliance_status (when I(command) is C(create) or C(modify), dict, {'Id': 13, 'Name': 'baseline1', 'Description': None, 'TemplateId': 102, 'TemplateName': 'one', 'TemplateType': 2, 'TaskId': 26584, 'PercentageComplete': '100', 'TaskStatus': 2070, 'LastRun': '2021-02-27 13:15:13.751', 'BaselineTargets': [{'Id': 1111, 'Type': {'Id': 1000, 'Name': 'DEVICE'}}], 'ConfigComplianceSummary': {'ComplianceStatus': 'OK', 'NumberOfCritical': 0, 'NumberOfWarning': 0, 'NumberOfNormal': 0, 'NumberOfIncomplete': 0}})
  Status of compliance baseline operation.


job_id (when I(command) is C(remediate), int, 14123)
  Task ID created when *command* is ``remediate``.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Sajna Shetty(@Sajna-Shetty)

