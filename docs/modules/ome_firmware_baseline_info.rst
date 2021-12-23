.. _ome_firmware_baseline_info_module:


ome_firmware_baseline_info -- Retrieves baseline details from OpenManage Enterprise
===================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves the list and details of all the baselines on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7.5



Parameters
----------

  baseline_name (optional, str, None)
    Name of the baseline.If *baseline_name* is not provided, all the available firmware baselines are returned.


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
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Retrieve details of all the available firmware baselines
      dellemc.openmanage.ome_firmware_baseline_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"

    - name: Retrieve details of a specific firmware baseline identified by its baseline name
      dellemc.openmanage.ome_firmware_baseline_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        baseline_name: "baseline_name"



Return Values
-------------

msg (on error, str, Successfully fetched firmware baseline information.)
  Overall baseline information.


baseline_info (success, dict, {'@odata.id': '/api/UpdateService/Baselines(239)', '@odata.type': '#UpdateService.Baselines', 'CatalogId': 22, 'ComplianceSummary': {'ComplianceStatus': 'CRITICAL', 'NumberOfCritical': 1, 'NumberOfDowngrade': 0, 'NumberOfNormal': 0, 'NumberOfWarning': 0}, 'Description': 'baseline_description', 'DeviceComplianceReports@odata.navigationLink': '/api/UpdateService/Baselines(239)/DeviceComplianceReports', 'DowngradeEnabled': True, 'Id': 239, 'Is64Bit': True, 'LastRun': '2020-05-22 16:42:40.307', 'Name': 'baseline_name', 'RepositoryId': 12, 'RepositoryName': 'HTTP DELL', 'RepositoryType': 'DELL_ONLINE', 'Targets': [{'Id': 10342, 'Type': {'Id': 1000, 'Name': 'DEVICE'}}], 'TaskId': 41415, 'TaskStatusId': 2060})
  Details of the baselines.





Status
------





Authors
~~~~~~~

- Sajna Shetty(@Sajna-Shetty)

