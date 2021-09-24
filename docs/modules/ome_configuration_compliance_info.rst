.. _ome_configuration_compliance_info_module:


ome_configuration_compliance_info -- Device compliance report for devices managed in OpenManage Enterprise
==========================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows the generation of a compliance report of a specific or all of devices in a configuration compliance baseline.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7.5



Parameters
----------

  baseline (True, str, None)
    The name of the created baseline.

    A compliance report is generated even when the template is not associated with the baseline.


  device_id (False, int, None)
    The ID of the target device which is associated with the *baseline*.


  device_service_tag (False, str, None)
    The device service tag of the target device associated with the *baseline*.

    *device_service_tag* is mutually exclusive with *device_id*.


  hostname (True, str, None)
    OpenManage Enterprise IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise username.


  password (True, str, None)
    OpenManage Enterprise password.


  port (optional, int, 443)
    OpenManage Enterprise HTTPS port.





Notes
-----

.. note::
   - Run this module from a system that has direct access to DellEMC OpenManage Enterprise.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Retrieve the compliance report of all of the devices in the specified configuration compliance baseline.
      dellemc.openmanage.ome_configuration_compliance_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        baseline: baseline_name

    - name: Retrieve the compliance report for a specific device associated with the baseline using the device ID.
      dellemc.openmanage.ome_configuration_compliance_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        baseline: baseline_name
        device_id: 10001

    - name: Retrieve the compliance report for a specific device associated with the baseline using the device service tag.
      dellemc.openmanage.ome_configuration_compliance_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        baseline: baseline_name
        device_service_tag: 2HFGH3



Return Values
-------------

msg (on error, str, Unable to complete the operation because the entered target baseline name 'baseline' is invalid.)
  Over all compliance report status.


compliance_info (success, dict, [{'ComplianceAttributeGroups': [{'Attributes': [], 'ComplianceReason': 'One or more attributes on the target device(s) does not match the compliance template.', 'ComplianceStatus': 2, 'ComplianceSubAttributeGroups': [{'Attributes': [{'AttributeId': 75369, 'ComplianceReason': 'Attribute has different value from template', 'ComplianceStatus': 3, 'CustomId': 0, 'Description': None, 'DisplayName': 'Workload Profile', 'ExpectedValue': 'HpcProfile', 'Value': 'NotAvailable'}], 'ComplianceReason': 'One or more attributes on the target device(s) does not match the compliance template.', 'ComplianceStatus': 2, 'ComplianceSubAttributeGroups': [], 'DisplayName': 'System Profile Settings', 'GroupNameId': 1}], 'DisplayName': 'BIOS', 'GroupNameId': 1}], 'ComplianceStatus': 'NONCOMPLIANT', 'DeviceName': 'WIN-PLOV8MPIP40', 'DeviceType': 1000, 'Id': 25011, 'InventoryTime': '2021-03-18 00:01:57.809771', 'Model': 'PowerEdge R7525', 'ServiceTag': 'JHMBX53'}])
  Returns the compliance report information.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen A (@felixs88)

