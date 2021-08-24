.. _ome_firmware_module:


ome_firmware -- Firmware update of PowerEdge devices and its components through OpenManage Enterprise
=====================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module updates the firmware of PowerEdge devices and all its components through OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7.5



Parameters
----------

  device_service_tag (optional, list, None)
    List of targeted device service tags.

    Either *device_id* or *device_service_tag* can be used individually or together.

    *device_service_tag* is mutually exclusive with *device_group_names*.


  device_id (optional, list, None)
    List of targeted device ids.

    Either *device_id* or *device_service_tag* can be used individually or together.

    *device_id* is mutually exclusive with *device_group_names*.


  device_group_names (optional, list, None)
    Enter the name of the group to update the firmware of all the devices within the group.

    *device_group_names* is mutually exclusive with *device_id* and *device_service_tag*.


  baseline_name (optional, str, None)
    Enter the baseline name to update the firmware of all the devices or groups of devices against the available compliance report.

    The firmware update can also be done by providing the baseline name and the path to the single DUP file. To update multiple baselines at once, provide the baseline names separated by commas.

    *baseline_names* is mutually exclusive with *device_group_names*, *device_id* and *device_service_tag*.


  dup_file (optional, str, None)
    Executable file to apply on the targets.


  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.


  password (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.





Notes
-----

.. note::
   - Run this module from a system that has direct access to DellEMC OpenManage Enterprise.
   - This module does not support ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Update firmware from DUP file using device ids
      dellemc.openmanage.ome_firmware:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        device_id:
          - 11111
          - 22222
        dup_file: "/path/Chassis-System-Management_Firmware_6N9WN_WN64_1.00.01_A00.EXE"

    - name: Update firmware from a DUP file using a device service tags
      dellemc.openmanage.ome_firmware:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        device_service_tag:
          - KLBR111
          - KLBR222
        dup_file: "/path/Network_Firmware_NTRW0_WN64_14.07.07_A00-00_01.EXE"

    - name: Update firmware from a DUP file using a device group names
      dellemc.openmanage.ome_firmware:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        device_group_names:
          - servers
        dup_file: "/path/BIOS_87V69_WN64_2.4.7.EXE"

    - name: Update firmware using baseline name
      dellemc.openmanage.ome_firmware:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        baseline_name: baseline_devices

    - name: Update firmware from a DUP file using a baseline names
      dellemc.openmanage.ome_firmware:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        baseline_name: "baseline_devices, baseline_groups"
        dup_file: "/path/BIOS_87V69_WN64_2.4.7.EXE"



Return Values
-------------

msg (always, str, Successfully submitted the firmware update job.)
  Overall firmware update status.


update_status (success, dict, AnsibleMapping([('LastRun', 'None'), ('CreatedBy', 'user'), ('Schedule', 'startnow'), ('LastRunStatus', AnsibleMapping([('Id', 1111), ('Name', 'NotRun')])), ('Builtin', False), ('Editable', True), ('NextRun', 'None'), ('JobStatus', AnsibleMapping([('Id', 1111), ('Name', 'New')])), ('JobName', 'Firmware Update Task'), ('Visible', True), ('State', 'Enabled'), ('JobDescription', 'dup test'), ('Params', [AnsibleMapping([('Value', 'true'), ('Key', 'signVerify'), ('JobId', 11111)]), AnsibleMapping([('Value', 'false'), ('Key', 'stagingValue'), ('JobId', 11112)]), AnsibleMapping([('Value', 'false'), ('Key', 'complianceUpdate'), ('JobId', 11113)]), AnsibleMapping([('Value', 'INSTALL_FIRMWARE'), ('Key', 'operationName'), ('JobId', 11114)])]), ('Targets', [AnsibleMapping([('TargetType', AnsibleMapping([('Id', 1000), ('Name', 'DEVICE')])), ('Data', 'DCIM:INSTALLED#701__NIC.Mezzanine.1A-1-1=1111111111111'), ('Id', 11115), ('JobId', 11116)])]), ('StartTime', 'None'), ('UpdatedBy', 'None'), ('EndTime', 'None'), ('Id', 11117), ('JobType', AnsibleMapping([('Internal', False), ('Id', 5), ('Name', 'Update_Task')]))]))
  Firmware Update job and progress details from the OME.


error_info (on HTTP error, dict, AnsibleMapping([('error', AnsibleMapping([('code', 'Base.1.0.GeneralError'), ('message', 'A general error has occurred. See ExtendedInfo for more information.'), ('@Message.ExtendedInfo', [AnsibleMapping([('MessageId', 'GEN1234'), ('RelatedProperties', []), ('Message', 'Unable to process the request because an error occurred.'), ('MessageArgs', []), ('Severity', 'Critical'), ('Resolution', 'Retry the operation. If the issue persists, contact your system administrator.')])])]))]))
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)

