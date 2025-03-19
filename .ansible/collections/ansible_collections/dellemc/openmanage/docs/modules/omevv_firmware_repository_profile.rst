.. _omevv_firmware_repository_profile_module:


omevv_firmware_repository_profile -- Create, modify, or delete OMEVV firmware repository profile
================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows you to create, modify, or delete an OpenManage Enterprise Integration for VMware Center (OMEVV) firmware repository profile.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  state (optional, str, present)
    \ :literal:`present`\  creates an OMEVV firmware repository profile or modifies an existing profile if the profile with the same name exists.

    \ :literal:`absent`\  deletes the OMEVV firmware repository profile.

    Either \ :emphasis:`profile\_name`\  or \ :emphasis:`profile\_id`\  is required when \ :emphasis:`state`\  is \ :literal:`absent`\ .


  name (optional, str, None)
    Name of the OMEVV firmware repository profile.

    This parameter is required for modification operation when \ :emphasis:`state`\  is \ :literal:`absent`\ .


  description (optional, str, None)
    Description of OMEVV firmware repository profile.


  new_name (optional, str, None)
    Name of the new OMEVV profile name when modify operation is performed.


  protocol_type (optional, str, None)
    \ :literal:`NFS`\  represents the NFS share path.

    \ :literal:`CIFS`\  represents the NFS share path.

    \ :literal:`HTTP`\  represents the HTTP share path.

    \ :literal:`HTTPS`\  represents the HTTPS share path.

    This parameter is required when \ :emphasis:`state`\  is \ :literal:`present`\  and a new profile is created.


  catalog_path (optional, str, None)
    Absolute path of the catalog.

    HTTP, HTTPS, NFS, and CIFS paths are supported.

    This parameter is required when \ :emphasis:`state`\  is \ :literal:`present`\ .


  share_username (optional, str, None)
    Username of the share.

    This parameter is required when \ :emphasis:`catalog\_path`\  is HTTPS or CIFS.


  share_password (optional, str, None)
    Password of the share.

    This parameter is required when \ :emphasis:`catalog\_path`\  is HTTPS or CIFS.


  share_domain (optional, str, None)
    Domain of the share.


  hostname (True, str, None)
    IP address or hostname of the OpenManage Enterprise Modular.


  vcenter_username (False, str, None)
    Username for OpenManage Enterprise Integration for VMware vCenter (OMEVV).

    If the username is not provided, then the environment variable \ :envvar:`OMEVV\_VCENTER\_USERNAME`\  is used.

    Example: export OMEVV\_VCENTER\_USERNAME=username


  vcenter_password (False, str, None)
    Password for OpenManage Enterprise Integration for VMware vCenter (OMEVV).

    If the password is not provided, then the environment variable \ :envvar:`OMEVV\_VCENTER\_PASSWORD`\  is used.

    Example: export OMEVV\_VCENTER\_PASSWORD=password


  vcenter_uuid (False, str, None)
    Universally Unique Identifier (UUID) of vCenter.

    vCenter UUID details can be retrieved using \ :ref:`dellemc.openmanage.omevv\_vcenter\_info <ansible_collections.dellemc.openmanage.omevv_vcenter_info_module>`\  module.

    If UUID is not provided, then the environment variable \ :envvar:`OMEVV\_VCENTER\_UUID`\  is used.

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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create an OMEVV firmware repository profile
      dellemc.openmanage.omevv_firmware_repository_profile:
        hostname: "192.168.0.1"
        vcenter_uuid: "xxxxx"
        vcenter_username: "username"
        vcenter_password: "password"
        ca_path: "path/to/ca_file"
        state: present
        name: profile-1
        catalog_path: http://xx.xx.xx.xx/share/Catalog/Catalog.xml

    - name: Modify an OMEVV firmware repository profile
      dellemc.openmanage.omevv_firmware_repository_profile:
        hostname: "192.168.0.1"
        vcenter_uuid: "xxxxx"
        vcenter_username: "username"
        vcenter_password: "password"
        ca_path: "path/to/ca_file"
        state: present
        name: profile-1
        new_name: profile-2
        catalog_path: http://xx.xx.xx.xx/new_share/Catalog/Catalog.xml

    - name: Delete an OMEVV firmware repository profile
      dellemc.openmanage.omevv_firmware_repository_profile:
        hostname: "192.168.0.1"
        vcenter_uuid: "xxxxx"
        vcenter_username: "username"
        vcenter_password: "password"
        ca_path: "path/to/ca_file"
        state: absent
        name: profile-1



Return Values
-------------

msg (always, str, Successfully created the OMEVV firmware repository profile.)
  Status of the profile operation.


error_info (on HTTP error, dict, {'errorCode': '18001', 'message': 'Repository profile with name Test already exists.'})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Shivam Sharma(@ShivamSh3)

