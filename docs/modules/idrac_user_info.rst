.. _idrac_user_info_module:


idrac_user_info -- Retrieve details of all users or a specific user on iDRAC.
=============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves the list and basic details of all users or details of a specific user on iDRAC



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  user_id (optional, int, None)
    Sequential user id numbers that supports from 1 to 16.

    *user_id* is mutually exclusive with *username*


  username (optional, str, None)
    Username of the account that is created in iDRAC local users.

    *username* is mutually exclusive with *user_id*


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.


  idrac_password (True, str, None)
    iDRAC user password.


  idrac_port (optional, int, 443)
    iDRAC port.


  validate_certs (optional, bool, True)
    If ``False``, the SSL certificates will not be validated.

    Configure ``False`` only on personally controlled sites where self-signed certificates are used.

    Prior to collection version ``5.0.0``, the *validate_certs* is ``False`` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module on a system that has direct access to Dell iDRAC.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Retrieve basic details of all user accounts.
      dellemc.openmanage.idrac_user_info:
        idrac_ip: 198.162.0.1
        idrac_user: idrac_user
        idrac_password: idrac_password
        ca_path: "/path/to/ca_cert.pem"

    - name: Retrieve user details using user_id
      dellemc.openmanage.idrac_user_info:
        idrac_ip: 198.162.0.1
        idrac_user: idrac_user
        idrac_password: idrac_password
        ca_path: "/path/to/ca_cert.pem"
        user_id: 1

    - name: Retrieve user details using username
      dellemc.openmanage.idrac_user_info:
        idrac_ip: 198.162.0.1
        idrac_user: idrac_user
        idrac_password: idrac_password
        ca_path: "/path/to/ca_cert.pem"
        username: user_name



Return Values
-------------

msg (always, str, Successfully retrieved the user information.)
  Status of user information retrieval.


user_info (success, list, [{'Description': 'User Account', 'Enabled': False, 'Id': '1', 'Locked': False, 'Name': 'User Account', 'Password': None, 'RoleId': 'None', 'UserName': ''}])
  Information about the user.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Husniya Hameed(@husniya_hameed)

