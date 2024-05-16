.. _ome_firmware_module:


ome_firmware -- Update firmware on PowerEdge devices and its components through OpenManage Enterprise
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

- python \>= 3.9.6



Parameters
----------

  device_service_tag (optional, list, None)
    List of service tags of the targeted devices.

    Either \ :emphasis:`device\_id`\  or \ :emphasis:`device\_service\_tag`\  can be used individually or together.

    This option is mutually exclusive with \ :emphasis:`device\_group\_names`\  and \ :emphasis:`devices`\ .


  device_id (optional, list, None)
    List of ids of the targeted device.

    Either \ :emphasis:`device\_id`\  or \ :emphasis:`device\_service\_tag`\  can be used individually or together.

    This option is mutually exclusive with \ :emphasis:`device\_group\_names`\  and \ :emphasis:`devices`\ .


  device_group_names (optional, list, None)
    Enter the name of the device group that contains the devices on which firmware needs to be updated.

    This option is mutually exclusive with \ :emphasis:`device\_id`\  and \ :emphasis:`device\_service\_tag`\ .


  dup_file (optional, path, None)
    The path of the Dell Update Package (DUP) file that contains the firmware or drivers required to update the target system device or individual device components.

    This is mutually exclusive with \ :emphasis:`baseline\_name`\ , \ :emphasis:`components`\ , and \ :emphasis:`devices`\ .


  baseline_name (optional, str, None)
    Enter the baseline name to update the firmware of all devices or list of devices that are not complaint.

    This option is mutually exclusive with \ :emphasis:`dup\_file`\  and \ :emphasis:`device\_group\_names`\ .


  components (optional, list, [])
    List of components to be updated.

    If not provided, all components applicable are considered.

    This option is case sensitive.

    This is applicable to \ :emphasis:`device\_service\_tag`\ , \ :emphasis:`device\_id`\ , and \ :emphasis:`baseline\_name`\ .


  devices (optional, list, None)
    This option allows to select components on each device for firmware update.

    This option is mutually exclusive with \ :emphasis:`dup\_file`\ , \ :emphasis:`device\_group\_names`\ , \ :emphasis:`device\_id`\ , and \ :emphasis:`device\_service\_tag`\ .


    id (optional, int, None)
      The id of the target device to be updated.

      This option is mutually exclusive with \ :emphasis:`service\_tag`\ .


    service_tag (optional, str, None)
      The service tag of the target device to be updated.

      This option is mutually exclusive with \ :emphasis:`id`\ .


    components (optional, list, [])
      The target components to be updated. If not specified, all applicable device components are considered.



  schedule (optional, str, RebootNow)
    Select the schedule for the firmware update.

    if \ :literal:`StageForNextReboot`\  is chosen, the firmware will be staged and updated during the next reboot of the target device.

    if \ :literal:`RebootNow`\  will apply the firmware updates immediately.


  reboot_type (optional, str, GracefulRebootForce)
    This option provides the choices to reboot the server immediately after the firmware update.

    This is applicable when \ :emphasis:`schedule`\  is \ :literal:`RebootNow`\ .

    \ :literal:`GracefulRebootForce`\  performs a graceful reboot with forced shutdown.

    \ :literal:`GracefulReboot`\  performs a graceful reboot without forced shutdown.

    \ :literal:`PowerCycle`\  performs a power cycle for a hard reset on the device.


  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (False, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.

    If the username is not provided, then the environment variable \ :envvar:`OME\_USERNAME`\  is used.

    Example: export OME\_USERNAME=username


  password (False, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.

    If the password is not provided, then the environment variable \ :envvar:`OME\_PASSWORD`\  is used.

    Example: export OME\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`OME\_X\_AUTH\_TOKEN`\  is used.

    Example: export OME\_X\_AUTH\_TOKEN=x\_auth\_token


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.


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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Update firmware from DUP file using device ids
      dellemc.openmanage.ome_firmware:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_id:
          - 11111
          - 22222
        dup_file: "/path/Chassis-System-Management_Firmware_6N9WN_WN64_1.00.01_A00.EXE"

    - name: Update firmware from a DUP file using a device service tags
      dellemc.openmanage.ome_firmware:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_service_tag:
          - KLBR111
          - KLBR222
        dup_file: "/path/Network_Firmware_NTRW0_WN64_14.07.07_A00-00_01.EXE"

    - name: Update firmware from a DUP file using a device group names
      dellemc.openmanage.ome_firmware:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_group_names:
          - servers
        dup_file: "/path/BIOS_87V69_WN64_2.4.7.EXE"

    - name: Update firmware using baseline name
      dellemc.openmanage.ome_firmware:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        baseline_name: baseline_devices

    - name: Stage firmware for the next reboot using baseline name
      dellemc.openmanage.ome_firmware:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        baseline_name: baseline_devices
        schedule: StageForNextReboot

    - name: "Update firmware using baseline name and components."
      dellemc.openmanage.ome_firmware:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        baseline_name: baseline_devices
        components:
          - BIOS

    - name: Update firmware of device components from a DUP file using a device ids in a baseline
      dellemc.openmanage.ome_firmware:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        baseline_name: baseline_devices
        device_id:
          - 11111
          - 22222
        components:
          - iDRAC with Lifecycle Controller

    - name: Update firmware of device components from a baseline using a device service tags under a baseline
      dellemc.openmanage.ome_firmware:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        baseline_name: baseline_devices
        device_service_tag:
          - KLBR111
          - KLBR222
        components:
          - IOM-SAS

    - name: Update firmware using baseline name with a device id and required components
      dellemc.openmanage.ome_firmware:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        baseline_name: baseline_devices
        devices:
          - id: 12345
            components:
              - Lifecycle Controller
          - id: 12346
            components:
              - Enterprise UEFI Diagnostics
              - BIOS

    - name: "Update firmware using baseline name with a device service tag and required components."
      dellemc.openmanage.ome_firmware:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        baseline_name: baseline_devices
        devices:
          - service_tag: ABCDE12
            components:
              - PERC H740P Adapter
              - BIOS
          - service_tag: GHIJK34
            components:
              - OS Drivers Pack

    - name: "Update firmware using baseline name with a device service tag or device id and required components."
      dellemc.openmanage.ome_firmware:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        baseline_name: baseline_devices
        devices:
          - service_tag: ABCDE12
            components:
              - BOSS-S1 Adapter
              - PowerEdge Server BIOS
          - id: 12345
            components:
              - iDRAC with Lifecycle Controller

    - name: "Update firmware using baseline name and components and perform Powercycle."
      dellemc.openmanage.ome_firmware:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        baseline_name: baseline_devices
        components:
          - BIOS
        reboot_type: PowerCycle



Return Values
-------------

msg (always, str, Successfully submitted the firmware update job.)
  Overall firmware update status.


update_status (success, dict, {'LastRun': 'None', 'CreatedBy': 'user', 'Schedule': 'startnow', 'LastRunStatus': {'Id': 1111, 'Name': 'NotRun'}, 'Builtin': False, 'Editable': True, 'NextRun': 'None', 'JobStatus': {'Id': 1111, 'Name': 'New'}, 'JobName': 'Firmware Update Task', 'Visible': True, 'State': 'Enabled', 'JobDescription': 'dup test', 'Params': [{'Value': 'true', 'Key': 'signVerify', 'JobId': 11111}, {'Value': 'false', 'Key': 'stagingValue', 'JobId': 11112}, {'Value': 'false', 'Key': 'complianceUpdate', 'JobId': 11113}, {'Value': 'INSTALL_FIRMWARE', 'Key': 'operationName', 'JobId': 11114}], 'Targets': [{'TargetType': {'Id': 1000, 'Name': 'DEVICE'}, 'Data': 'DCIM:INSTALLED#701__NIC.Mezzanine.1A-1-1=1234567654321', 'Id': 11115, 'JobId': 11116}], 'StartTime': 'None', 'UpdatedBy': 'None', 'EndTime': 'None', 'Id': 11117, 'JobType': {'Internal': False, 'Id': 5, 'Name': 'Update_Task'}})
  The firmware update job and progress details from the OME.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)
- Jagadeesh N V (@jagadeeshnv)
- Abhishek Sinha (@ABHISHEK-SINHA10)

