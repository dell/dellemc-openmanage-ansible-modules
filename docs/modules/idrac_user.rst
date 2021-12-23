.. _idrac_user_module:


idrac_user -- Configure settings for user accounts
==================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to perform the following,

Add a new user account.

Edit a user account.

Enable or Disable a user account.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7.5



Parameters
----------

  state (optional, str, present)
    Select ``present`` to create or modify a user account.

    Select ``absent`` to remove a user account.

    Ensure Lifecycle Controller is available because the user operation uses the capabilities of Lifecycle Controller.


  user_name (True, str, None)
    Provide the *user_name* of the account to be created, deleted or modified.


  user_password (optional, str, None)
    Provide the password for the user account. The password can be changed when the user account is modified.

    To ensure security, the *user_password* must be at least eight characters long and must contain lowercase and upper-case characters, numbers, and special characters.


  new_user_name (optional, str, None)
    Provide the *user_name* for the account to be modified.


  privilege (optional, str, None)
    Following are the role-based privileges.

    A user with ``Administrator`` privilege can log in to iDRAC, and then configure iDRAC, configure users, clear logs, control and configure system, access virtual console, access virtual media, test alerts, and execute debug commands.

    A user with ``Operator`` privilege can log in to iDRAC, and then configure iDRAC, control and configure system, access virtual console, access virtual media, and execute debug commands.

    A user with ``ReadOnly`` privilege can only log in to iDRAC.

    A user with ``None``, no privileges assigned.


  ipmi_lan_privilege (optional, str, None)
    The Intelligent Platform Management Interface LAN privilege level assigned to the user.


  ipmi_serial_privilege (optional, str, None)
    The Intelligent Platform Management Interface Serial Port privilege level assigned to the user.

    This option is only applicable for rack and tower servers.


  enable (optional, bool, None)
    Provide the option to enable or disable a user from logging in to iDRAC.


  sol_enable (optional, bool, None)
    Enables Serial Over Lan (SOL) for an iDRAC user.


  protocol_enable (optional, bool, None)
    Enables protocol for the iDRAC user.


  authentication_protocol (optional, str, None)
    This option allows to configure one of the following authentication protocol types to authenticate the iDRAC user.

    Secure Hash Algorithm ``SHA``.

    Message Digest 5 ``MD5``.

    An authentication protocol is not configured if ``None`` is selected.


  privacy_protocol (optional, str, None)
    This option allows to configure one of the following privacy encryption protocols for the iDRAC user.

    Data Encryption Standard ``DES``.

    Advanced Encryption Standard ``AES``.

    A privacy protocol is not configured if ``None`` is selected.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.


  idrac_password (True, str, None)
    iDRAC user password.


  idrac_port (optional, int, 443)
    iDRAC port.





Notes
-----

.. note::
   - Run this module from a system that has direct access to DellEMC iDRAC.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Configure a new iDRAC user
      dellemc.openmanage.idrac_user:
        idrac_ip: 198.162.0.1
        idrac_user: idrac_user
        idrac_password: idrac_password
        state: present
        user_name: user_name
        user_password: user_password
        privilege: Administrator
        ipmi_lan_privilege: Administrator
        ipmi_serial_privilege: Administrator
        enable: true
        sol_enable: true
        protocol_enable: true
        authentication_protocol: SHA
        privacy_protocol: AES

    - name: Modify existing iDRAC user username and password
      dellemc.openmanage.idrac_user:
        idrac_ip: 198.162.0.1
        idrac_user: idrac_user
        idrac_password: idrac_password
        state: present
        user_name: user_name
        new_user_name: new_user_name
        user_password: user_password

    - name: Delete existing iDRAC user account
      dellemc.openmanage.idrac_user:
        idrac_ip: 198.162.0.1
        idrac_user: idrac_user
        idrac_password: idrac_password
        state: absent
        user_name: user_name



Return Values
-------------

msg (always, str, Successfully created user account details.)
  Status of the iDRAC user configuration.


status (success, dict, {'@Message.ExtendedInfo': [{'Message': 'Successfully Completed Request', 'MessageArgs': [], 'MessageArgs@odata.count': 0, 'MessageId': 'Base.1.5.Success', 'RelatedProperties': [], 'RelatedProperties@odata.count': 0, 'Resolution': 'None', 'Severity': 'OK'}, {'Message': 'The operation successfully completed.', 'MessageArgs': [], 'MessageArgs@odata.count': 0, 'MessageId': 'IDRAC.2.1.SYS413', 'RelatedProperties': [], 'RelatedProperties@odata.count': 0, 'Resolution': 'No response action is required.', 'Severity': 'Informational'}]})
  Configures the iDRAC users attributes.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)

