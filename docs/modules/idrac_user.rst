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

- python \>= 3.9.6



Parameters
----------

  state (optional, str, present)
    Select :literal:`present` to create or modify a user account.

    Select :literal:`absent` to remove a user account.


  user_name (True, str, None)
    Provide the :emphasis:`user\_name` of the account to be created, deleted or modified.


  user_password (optional, str, None)
    Provide the password for the user account. The password can be changed when the user account is modified.

    To ensure security, the :emphasis:`user\_password` must be at least eight characters long and must contain lowercase and upper-case characters, numbers, and special characters.


  new_user_name (optional, str, None)
    Provide the :emphasis:`user\_name` for the account to be modified.


  privilege (optional, str, None)
    Following are the role-based privileges.

    A user with :literal:`Administrator` privilege can log in to iDRAC, and then configure iDRAC, configure users, clear logs, control and configure system, access virtual console, access virtual media, test alerts, and execute debug commands.

    A user with :literal:`Operator` privilege can log in to iDRAC, and then configure iDRAC, control and configure system, access virtual console, access virtual media, and execute debug commands.

    A user with :literal:`ReadOnly` privilege can only log in to iDRAC.

    A user with :literal:`None`\ , no privileges assigned.

    Will be ignored, if custom\_privilege parameter is provided.


  custom_privilege (optional, int, None)
    The privilege level assigned to the user.


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

    Secure Hash Algorithm :literal:`SHA`. Not applicable for iDRAC10.

    Message Digest 5 :literal:`MD5`. Not applicable for iDRAC10.

    Secure Hash Algorithm 384-bit :literal:`SHA-384`. Only applicable for iDRAC10.

    Secure Hash Algorithm 512-bit :literal:`SHA-512`. Only applicable for iDRAC10.

    An authentication protocol is not configured if :literal:`None` is selected.


  privacy_protocol (optional, str, None)
    This option allows to configure one of the following privacy encryption protocols for the iDRAC user.

    Data Encryption Standard :literal:`DES`. Not applicable for iDRAC10.

    Advanced Encryption Standard :literal:`AES`. Not applicable for iDRAC10.

    Advanced Encryption Standard 256-bit :literal:`AES-256`. Only applicable for iDRAC9 and iDRAC10.

    A privacy protocol is not configured if :literal:`None` is selected.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (False, str, None)
    iDRAC username.

    If the username is not provided, then the environment variable :envvar:`IDRAC\_USERNAME` is used.

    Example: export IDRAC\_USERNAME=username


  idrac_password (False, str, None)
    iDRAC user password.

    If the password is not provided, then the environment variable :envvar:`IDRAC\_PASSWORD` is used.

    Example: export IDRAC\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable :envvar:`IDRAC\_X\_AUTH\_TOKEN` is used.

    Example: export IDRAC\_X\_AUTH\_TOKEN=x\_auth\_token


  idrac_port (optional, int, 443)
    iDRAC port.


  validate_certs (optional, bool, True)
    If :literal:`false`\ , the SSL certificates will not be validated.

    Configure :literal:`false` only on personally controlled sites where self-signed certificates are used.

    Prior to collection version :literal:`5.0.0`\ , the :emphasis:`validate\_certs` is :literal:`false` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports :literal:`check\_mode`.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Configure a new iDRAC user
      dellemc.openmanage.idrac_user:
        idrac_ip: 198.162.0.1
        idrac_user: idrac_user
        idrac_password: idrac_password
        ca_path: "/path/to/ca_cert.pem"
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
        ca_path: "/path/to/ca_cert.pem"
        state: present
        user_name: user_name
        new_user_name: new_user_name
        user_password: user_password

    - name: Delete existing iDRAC user account
      dellemc.openmanage.idrac_user:
        idrac_ip: 198.162.0.1
        idrac_user: idrac_user
        idrac_password: idrac_password
        ca_path: "/path/to/ca_cert.pem"
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
- Kritika Bhateja (@Kritika-Bhateja-03)

