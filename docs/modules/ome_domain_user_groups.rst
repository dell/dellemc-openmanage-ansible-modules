.. _ome_domain_user_groups_module:


ome_domain_user_groups -- Create, modify, or delete an Active Directory user group on OpenManage Enterprise and OpenManage Enterprise Modular
=============================================================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to create, modify, or delete an Active Directory user group on OpenManage Enterprise and OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7.17



Parameters
----------

  state (optional, str, present)
    ``present`` imports or modifies the Active Directory user group.

    ``absent`` deletes an existing Active Directory user group.


  group_name (True, str, None)
    The desired Active Directory user group name to be imported or removed.

    Examples for user group name: Administrator or Account Operators or Access Control Assistance Operator.

    *group_name* value is case insensitive.


  role (optional, str, None)
    The desired roles and privilege for the imported Active Directory user group.

    OpenManage Enterprise Modular Roles: CHASSIS ADMINISTRATOR, COMPUTE MANAGER, STORAGE MANAGER, FABRIC MANAGER, VIEWER.

    OpenManage Enterprise Roles: ADMINISTRATOR, DEVICE MANAGER, VIEWER.

    *role* value is case insensitive.


  directory_name (optional, str, None)
    The directory name set while adding the Active Directory.

    *directory_name* is mutually exclusive with *directory_id*.


  directory_id (optional, int, None)
    The ID of the Active Directory.

    *directory_id* is mutually exclusive with *directory_name*.


  domain_username (optional, str, None)
    Active directory domain username.

    Example: username@domain or domain\username.


  domain_password (optional, str, None)
    Active directory domain password.


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
   - This module supports ``check_mode`` and idempotency.
   - Run this module from a system that has direct access to OpenManage Enterprise or OpenManage Enterprise Modular.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create Active Directory user group
      dellemc.openmanage.ome_domain_user_groups:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        state: present
        group_name: account operators
        directory_name: directory_name
        role: administrator
        domain_username: username@domain
        domain_password: domain_password

    - name: Update Active Directory user group
      dellemc.openmanage.ome_domain_user_groups:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        state: present
        group_name: account operators
        role: viewer

    - name: Delete active directory user group
      dellemc.openmanage.ome_domain_user_groups:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        state: absent
        group_name: administrators



Return Values
-------------

msg (always, str, Successfully imported the active directory user group.)
  Overall status of the Active Directory user group operation.


domain_user_status (When I(state) is C(present)., dict, {'Description': None, 'DirectoryServiceId': 16097, 'Enabled': True, 'Id': '16617', 'IsBuiltin': False, 'IsVisible': True, 'Locked': False, 'Name': 'Account Operators', 'ObjectGuid': 'a491859c-031e-42a3-ae5e-0ab148ecf1d6', 'ObjectSid': None, 'Oem': None, 'Password': None, 'PlainTextPassword': None, 'RoleId': '16', 'UserName': 'Account Operators', 'UserTypeId': 2})
  Details of the domain user operation, when *state* is ``present``.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)

