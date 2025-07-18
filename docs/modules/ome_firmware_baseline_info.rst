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

- python \>= 3.9.6



Parameters
----------

  baseline_name (optional, str, None)
    Name of the baseline.If \ :emphasis:`baseline\_name`\  is not provided, all the available firmware baselines are returned.


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
    - name: Retrieve details of all the available firmware baselines
      dellemc.openmanage.ome_firmware_baseline_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"

    - name: Retrieve details of a specific firmware baseline identified by its baseline name
      dellemc.openmanage.ome_firmware_baseline_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
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
- Mangirish Kenkare(@MangirishK)

