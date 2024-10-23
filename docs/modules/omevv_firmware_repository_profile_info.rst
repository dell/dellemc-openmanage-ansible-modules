.. _omevv_firmware_repository_profile_info_module:


omevv_firmware_repository_profile_info -- Retrieve OMEVV firmware repository profile information.
=================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows you to retrieve the OMEVV firmware repository profile information.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  name (optional, str, None)
    Name of the OMEVV firmware repository profile.

    If \ :emphasis:`name`\  is provided, the module retrieves only specified firmware repository profile information.


  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  vcenter_username (False, str, None)
    OpenManage Enterprise Integration for VMware vCenter username.

    If the username is not provided, then the environment variable \ :envvar:`OMEVV\_VCENTER\_USERNAME`\  is used.

    Example: export OMEVV\_VCENTER\_USERNAME=username


  vcenter_password (False, str, None)
    OpenManage Enterprise Integration for VMware vCenter password.

    If the password is not provided, then the environment variable \ :envvar:`OMEVV\_VCENTER\_PASSWORD`\  is used.

    Example: export OMEVV\_VCENTER\_PASSWORD=password


  vcenter_uuid (False, str, None)
    Universally unique identifier (uuid) of vCenter.

    vCenter uuid details can be fetched using \ :ref:`dellemc.openmanage.omevv\_vcenter\_info <ansible_collections.dellemc.openmanage.omevv_vcenter_info_module>`\  module.

    If the uuid is not provided, then the environment variable \ :envvar:`OMEVV\_VCENTER\_UUID`\  is used.

    Example: export OMEVV\_VCENTER\_UUID=uuid


  port (optional, int, 443)
    OpenManage Enterprise HTTPS port.


  validate_certs (optional, bool, True)
    Whether to check SSL certificate. - If \ :literal:`true`\ , the SSL certificates will be validated. - If \ :literal:`false`\ , the SSL certificates will not be validated.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - This module supports IPv4 and IPv6 addresses.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Retrieve all firmware repository profile information.
      dellemc.openmanage.omevv_firmware_repository_profile_info:
        hostname: "192.168.0.1"
        vcenter_uuid: "xxxxxx"
        vcenter_username: "username"
        vcenter_password: "password"
        ca_path: "path/to/ca_file"

    - name: Retrieve specific firmware repository profile information using profile name.
      dellemc.openmanage.omevv_firmware_repository_profile_info:
        hostname: "192.168.0.1"
        vcenter_uuid: "xxxxxx"
        vcenter_username: "username"
        vcenter_password: "password"
        ca_path: "path/to/ca_file"
        name: profile-1



Return Values
-------------

msg (always, str, Successfully retrieved the firmware repository profile information.)
  Status of the firmare repository profile information for the retrieve operation.


profile_info (success, list, [{'id': 1000, 'profileName': 'Dell Default Catalog', 'description': 'Latest Firmware From Dell', 'profileType': 'Firmware', 'sharePath': 'https://downloads.dell.com//catalog/catalog.xml.gz', 'fileName': 'catalog.xml', 'status': 'Success', 'factoryCreated': True, 'factoryType': 'Default', 'catalogCreatedDate': '2024-08-27T01:58:10Z', 'catalogLastChecked': '2024-09-09T19:30:16Z', 'checkCertificate': None, 'protocolType': 'HTTPS', 'createdBy': 'OMEVV Default', 'modifiedBy': None, 'owner': 'OMEVV'}, {'id': 1001, 'profileName': 'Dell Default Catalog', 'description': 'Latest Firmware From Dell', 'profileType': 'Firmware', 'sharePath': 'https://downloads.dell.com//catalog/catalog.xml.gz', 'fileName': 'catalog.xml', 'status': 'Success', 'factoryCreated': True, 'factoryType': 'Default', 'catalogCreatedDate': '2024-08-27T01:58:10Z', 'catalogLastChecked': '2024-09-09T19:30:16Z', 'checkCertificate': None, 'protocolType': 'HTTPS', 'createdBy': 'OMEVV Default', 'modifiedBy': None, 'owner': 'OMEVV'}])
  Information on the vCenter.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Lovepreet Singh (@singh-lovepreet1)

