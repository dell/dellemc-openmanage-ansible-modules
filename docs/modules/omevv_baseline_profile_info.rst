.. _omevv_baseline_profile_info_module:


omevv_baseline_profile_info -- Retrieve OMEVV baseline profile information.
===========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows you to retrieve all or the specific OMEVV baseline profile information.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  name (optional, str, None)
    Name of the baseline profile.

    If :emphasis:`name` is provided, the module retrieves only specified baseline profile information.


  hostname (True, str, None)
    IP address or hostname of the OpenManage Enterprise Modular.


  vcenter_username (False, str, None)
    Username for OpenManage Enterprise Integration for VMware vCenter (OMEVV).

    If the username is not provided, then the environment variable :envvar:`OMEVV\_VCENTER\_USERNAME` is used.

    Example: export OMEVV\_VCENTER\_USERNAME=username


  vcenter_password (False, str, None)
    Password for OpenManage Enterprise Integration for VMware vCenter (OMEVV).

    If the password is not provided, then the environment variable :envvar:`OMEVV\_VCENTER\_PASSWORD` is used.

    Example: export OMEVV\_VCENTER\_PASSWORD=password


  vcenter_uuid (False, str, None)
    Universally Unique Identifier (UUID) of vCenter.

    vCenter UUID details can be retrieved using :ref:`dellemc.openmanage.omevv\_vcenter\_info <ansible_collections.dellemc.openmanage.omevv_vcenter_info_module>` module.

    If UUID is not provided, then the environment variable :envvar:`OMEVV\_VCENTER\_UUID` is used.

    Example: export OMEVV\_VCENTER\_UUID=uuid


  port (optional, int, 443)
    OpenManage Enterprise HTTPS port.


  validate_certs (optional, bool, True)
    Whether to check SSL certificate. - If :literal:`true`\ , the SSL certificates will be validated. - If :literal:`false`\ , the SSL certificates will not be validated.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Retrieve all baseline profile information.
      dellemc.openmanage.omevv_baseline_profile_info:
        hostname: "192.168.0.1"
        vcenter_uuid: "xxxxxx"
        vcenter_username: "username"
        vcenter_password: "password"
        ca_path: "path/to/ca_file"

    - name: Retrieve specific baseline profile information using profile name.
      dellemc.openmanage.omevv_baseline_profile_info:
        hostname: "192.168.0.1"
        vcenter_uuid: "xxxxxx"
        vcenter_username: "username"
        vcenter_password: "password"
        ca_path: "path/to/ca_file"
        name: profile-1



Return Values
-------------

msg (always, str, Successfully retrieved the baseline profile information.)
  Status of the baseline profile information for the retrieve operation.


baseline_profile_info (success, list, [{'id': 1000, 'name': 'Baseline-1', 'description': 'Baseline-1 desc', 'consoleId': 'xxxxx', 'consoleAddress': 'xx.xx.xx.xx', 'firmwareRepoId': 1000, 'firmwareRepoName': 'Dell Default Catalog', 'configurationRepoId': None, 'configurationRepoName': None, 'driverRepoId': None, 'driverRepoName': None, 'driftJobId': 1743, 'driftJobName': 'BP-Baseline-1-Host-Firmware-Drift-Detection', 'dateCreated': '2024-10-16T10:25:29.786Z', 'dateModified': None, 'lastmodifiedBy': 'Administrator@VSPHERE.LOCAL', 'version': '1.0.0-0', 'lastSuccessfulUpdatedTime': '2024-10-16T10:27:35.212Z', 'clusterGroups': [], 'datacenter_standAloneHostsGroups': [], 'baselineType': None, 'status': 'SUCCESSFUL'}, {'id': 1001, 'name': 'Baseline - 2', 'description': 'Baseline - 2 description', 'consoleId': 'xxxxx', 'consoleAddress': 'xx.xx.xx.xx', 'firmwareRepoId': 1000, 'firmwareRepoName': 'Dell Default Catalog', 'configurationRepoId': None, 'configurationRepoName': None, 'driverRepoId': None, 'driverRepoName': None, 'driftJobId': 1812, 'driftJobName': 'BP-Baseline - 2-Host-Firmware-Drift-Detection', 'dateCreated': '2024-10-16T12:38:56.581Z', 'dateModified': None, 'lastmodifiedBy': 'Administrator@VSPHERE.LOCAL', 'version': '1.0.0-0', 'lastSuccessfulUpdatedTime': '2024-10-16T12:41:02.641Z', 'clusterGroups': [], 'datacenter_standAloneHostsGroups': [{'associated_datacenterID': 'datacenter-1001', 'associated_datacenterName': 'Standalone Hosts-Test-DC', 'omevv_groupID': 1002}], 'baselineType': 'DATACENTER_NONCLUSTER', 'status': 'SUCCESSFUL'}])
  Information on the vCenter.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Kritika Bhateja (@Kritika-Bhateja-03)

