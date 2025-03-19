.. _ome_firmware_baseline_compliance_info_module:


ome_firmware_baseline_compliance_info -- Retrieves baseline compliance details on OpenManage Enterprise
=======================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to retrieve firmware compliance for a list of devices, or against a specified baseline on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  baseline_name (optional, str, None)
    Name of the baseline, for which the device compliance report is generated.

    This option is mandatory for generating baseline based device compliance report.

    \ :emphasis:`baseline\_name`\  is mutually exclusive with \ :emphasis:`device\_ids`\ , \ :emphasis:`device\_service\_tags`\  and \ :emphasis:`device\_group\_names`\ .


  device_ids (optional, list, None)
    A list of unique identifier for device based compliance report.

    Either \ :emphasis:`device\_ids`\ , \ :emphasis:`device\_service\_tags`\  or \ :emphasis:`device\_group\_names`\  is required to generate device based compliance report.

    \ :emphasis:`device\_ids`\  is mutually exclusive with \ :emphasis:`device\_service\_tags`\ , \ :emphasis:`device\_group\_names`\  and \ :emphasis:`baseline\_name`\ .

    Devices without reports are ignored.


  device_service_tags (optional, list, None)
    A list of service tags for device based compliance report.

    Either \ :emphasis:`device\_ids`\ , \ :emphasis:`device\_service\_tags`\  or \ :emphasis:`device\_group\_names`\  is required to generate device based compliance report.

    \ :emphasis:`device\_service\_tags`\  is mutually exclusive with \ :emphasis:`device\_ids`\ , \ :emphasis:`device\_group\_names`\  and \ :emphasis:`baseline\_name`\ .

    Devices without reports are ignored.


  device_group_names (optional, list, None)
    A list of group names for device based compliance report.

    Either \ :emphasis:`device\_ids`\ , \ :emphasis:`device\_service\_tags`\  or \ :emphasis:`device\_group\_names`\  is required to generate device based compliance report.

    \ :emphasis:`device\_group\_names`\  is mutually exclusive with \ :emphasis:`device\_ids`\ , \ :emphasis:`device\_service\_tags`\  and \ :emphasis:`baseline\_name`\ .

    Devices without reports are ignored.


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
    - name: Retrieves device based compliance report for specified device IDs
      dellemc.openmanage.ome_firmware_baseline_compliance_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_ids:
          - 11111
          - 22222

    - name: Retrieves device based compliance report for specified service Tags
      dellemc.openmanage.ome_firmware_baseline_compliance_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_service_tags:
          - MXL1234
          - MXL4567

    - name: Retrieves device based compliance report for specified group names
      dellemc.openmanage.ome_firmware_baseline_compliance_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_group_names:
          - "group1"
          - "group2"

    - name: Retrieves device compliance report for a specified baseline
      dellemc.openmanage.ome_firmware_baseline_compliance_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        baseline_name: "baseline_name"



Return Values
-------------

msg (on error, str, Failed to fetch the compliance baseline information.)
  Overall baseline compliance report status.


baseline_compliance_info (success, dict, [{'CatalogId': 53, 'ComplianceSummary': {'ComplianceStatus': 'CRITICAL', 'NumberOfCritical': 2, 'NumberOfDowngrade': 0, 'NumberOfNormal': 0, 'NumberOfWarning': 0}, 'Description': '', 'DeviceComplianceReports': [{'ComplianceStatus': 'CRITICAL', 'ComponentComplianceReports': [{'ComplianceDependencies': [], 'ComplianceStatus': 'DOWNGRADE', 'Criticality': 'Ok', 'CurrentVersion': 'OSC_1.1', 'Id': 1258, 'ImpactAssessment': '', 'Name': 'OS COLLECTOR 2.1', 'Path': 'FOLDER04118304M/2/Diagnostics_Application_JCCH7_WN64_4.0_A00_01.EXE', 'PrerequisiteInfo': '', 'RebootRequired': False, 'SourceName': 'DCIM:INSTALLED#802__OSCollector.Embedded.1', 'TargetIdentifier': '101734', 'UniqueIdentifier': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'UpdateAction': 'DOWNGRADE', 'Uri': 'http://www.dell.com/support/home/us/en/19/Drivers/DriversDetails?driverId=XXXXX', 'Version': '4.0'}, {'ComplianceDependencies': [], 'ComplianceStatus': 'CRITICAL', 'Criticality': 'Recommended', 'CurrentVersion': 'DN02', 'Id': 1259, 'ImpactAssessment': '', 'Name': 'TOSHIBA AL14SE 1.8 TB 2.5 12Gb 10K 512n SAS HDD Drive', 'Path': 'FOLDER04086111M/1/SAS-Drive_Firmware_VDGFM_WN64_DN03_A00.EXE', 'PrerequisiteInfo': '', 'RebootRequired': True, 'SourceName': 'DCIM:INSTALLED#304_C_Disk.Bay.1:Enclosure.Internal.0-1:RAID.Integrated.1-1', 'TargetIdentifier': '103730', 'UniqueIdentifier': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'UpdateAction': 'UPGRADE', 'Uri': 'http://www.dell.com/support/home/us/en/19/Drivers/DriversDetails?driverId=XXXXX', 'Version': 'DN03'}], 'DeviceId': 11603, 'DeviceModel': 'PowerEdge R630', 'DeviceName': None, 'DeviceTypeId': 1000, 'DeviceTypeName': 'CPGCGS', 'FirmwareStatus': 'Non-Compliant', 'Id': 194, 'RebootRequired': True, 'ServiceTag': 'MXL1234'}], 'DowngradeEnabled': True, 'Id': 53, 'Is64Bit': False, 'LastRun': '2019-09-27 05:08:16.301', 'Name': 'baseline1', 'RepositoryId': 43, 'RepositoryName': 'catalog2', 'RepositoryType': 'CIFS', 'Targets': [{'Id': 11603, 'Type': {'Id': 1000, 'Name': 'DEVICE'}}], 'TaskId': 11710, 'TaskStatusId': 0}])
  Details of the baseline compliance report.


error_info (on http error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to retrieve baseline list either because the device ID(s) entered are invalid', 'Resolution': 'Make sure the entered device ID(s) are valid and retry the operation.', 'Severity': 'Critical'}], 'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.'}})
  Details of http error.





Status
------





Authors
~~~~~~~

- Sajna Shetty(@Sajna-Shetty)

