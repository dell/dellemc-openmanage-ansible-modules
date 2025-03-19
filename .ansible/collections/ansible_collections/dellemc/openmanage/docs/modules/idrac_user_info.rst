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

- python \>= 3.9.6



Parameters
----------

  user_id (optional, int, None)
    Sequential user id numbers that supports from 1 to 16.

    \ :emphasis:`user\_id`\  is mutually exclusive with \ :emphasis:`username`\ 


  username (optional, str, None)
    Username of the account that is created in iDRAC local users.

    \ :emphasis:`username`\  is mutually exclusive with \ :emphasis:`user\_id`\ 


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (False, str, None)
    iDRAC username.

    If the username is not provided, then the environment variable \ :envvar:`IDRAC\_USERNAME`\  is used.

    Example: export IDRAC\_USERNAME=username


  idrac_password (False, str, None)
    iDRAC user password.

    If the password is not provided, then the environment variable \ :envvar:`IDRAC\_PASSWORD`\  is used.

    Example: export IDRAC\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`IDRAC\_X\_AUTH\_TOKEN`\  is used.

    Example: export IDRAC\_X\_AUTH\_TOKEN=x\_auth\_token


  idrac_port (optional, int, 443)
    iDRAC port.


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
   - Run this module on a system that has direct access to Dell iDRAC.
   - This module supports \ :literal:`check\_mode`\ .




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

