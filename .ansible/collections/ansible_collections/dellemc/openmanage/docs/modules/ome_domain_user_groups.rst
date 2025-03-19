.. _ome_domain_user_groups_module:


ome_domain_user_groups -- Create, modify, or delete an Active Directory/LDAP user group on OpenManage Enterprise and OpenManage Enterprise Modular
==================================================================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to create, modify, or delete an Active Directory/LDAP user group on OpenManage Enterprise and OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  state (optional, str, present)
    \ :literal:`present`\  imports or modifies the Active Directory/LDAP user group.

    \ :literal:`absent`\  deletes an existing Active Directory/LDAP user group.


  group_name (True, str, None)
    The desired Active Directory/LDAP user group name to be imported or removed.

    Examples for user group name: Administrator or Account Operators or Access Control Assistance Operator.

    \ :emphasis:`group\_name`\  value is case insensitive.


  role (optional, str, None)
    The desired roles and privilege for the imported Active Directory/LDAP user group.

    OpenManage Enterprise Modular Roles: CHASSIS ADMINISTRATOR, COMPUTE MANAGER, STORAGE MANAGER, FABRIC MANAGER, VIEWER.

    OpenManage Enterprise Roles: ADMINISTRATOR, DEVICE MANAGER, VIEWER.

    \ :emphasis:`role`\  value is case insensitive.


  directory_name (optional, str, None)
    The directory name set while adding the Active Directory/LDAP.

    \ :emphasis:`directory\_name`\  is mutually exclusive with \ :emphasis:`directory\_id`\ .


  directory_type (optional, str, AD)
    Type of the account.


  directory_id (optional, int, None)
    The ID of the Active Directory/LDAP.

    \ :emphasis:`directory\_id`\  is mutually exclusive with \ :emphasis:`directory\_name`\ .


  domain_username (optional, str, None)
    Active Directory/LDAP domain username.

    Example: username@domain or domain\\username.


  domain_password (optional, str, None)
    Active Directory/LDAP domain password.


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
   - This module supports \ :literal:`check\_mode`\  and idempotency.
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
        ca_path: "/path/to/ca_cert.pem"
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
        ca_path: "/path/to/ca_cert.pem"
        state: present
        group_name: account operators
        role: viewer

    - name: Delete active directory user group
      dellemc.openmanage.ome_domain_user_groups:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: absent
        group_name: administrators

    - name: Import LDAP directory group.
      dellemc.openmanage.ome_domain_user_groups:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        directory_type: LDAP
        state: present
        group_name: account operators
        directory_name: directory_name
        role: administrator
        domain_username: username@domain
        domain_password: domain_password

    - name: Remove LDAP directory group.
      dellemc.openmanage.ome_domain_user_groups:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: absent
        group_name: account operators



Return Values
-------------

msg (always, str, Successfully imported the Active Directory/LDAP user group.)
  Overall status of the Active Directory/LDAP user group operation.


domain_user_status (When I(state) is C(present)., dict, {'Description': None, 'DirectoryServiceId': 16097, 'Enabled': True, 'Id': '16617', 'IsBuiltin': False, 'IsVisible': True, 'Locked': False, 'Name': 'Account Operators', 'ObjectGuid': 'a491859c-031e-42a3-ae5e-0ab148ecf1d6', 'ObjectSid': None, 'Oem': None, 'Password': None, 'PlainTextPassword': None, 'RoleId': '16', 'UserName': 'Account Operators', 'UserTypeId': 2})
  Details of the domain user operation, when \ :emphasis:`state`\  is \ :literal:`present`\ .


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)
- Abhishek Sinha (@Abhishek-Dell)

