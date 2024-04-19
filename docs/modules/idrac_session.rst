.. _idrac_session_module:


idrac_session -- Manage iDRAC sessions
======================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows the creation and deletion of sessions on iDRAC.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  hostname (optional, str, None)
    IP address or hostname of the iDRAC.


  username (optional, str, None)
    Username of the iDRAC.

    \ :emphasis:`username`\  is required when \ :emphasis:`state`\  is \ :literal:`present`\ .


  password (optional, str, None)
    Password of the iDRAC.

    \ :emphasis:`password`\  is required when \ :emphasis:`state`\  is \ :literal:`present`\ .


  port (optional, int, 443)
    Port of the iDRAC.


  validate_certs (optional, bool, True)
    If \ :literal:`false`\ , the SSL certificates will not be validated.

    Configure \ :literal:`false`\  only on personally controlled sites where self-signed certificates are used.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The https socket level timeout in seconds.


  state (optional, str, present)
    The state of the session in an iDRAC.

    \ :literal:`present`\  creates a session.

    \ :literal:`absent`\  deletes a session.

    Module will always report changes found to be applied when \ :emphasis:`state`\  is \ :literal:`present`\ .


  auth_token (optional, str, None)
    Authentication token.

    \ :emphasis:`auth\_token`\  is required when \ :emphasis:`state`\  is \ :literal:`absent`\ .


  session_id (optional, int, None)
    Session ID of the iDRAC.

    \ :emphasis:`session\_id`\  is required when \ :emphasis:`state`\  is \ :literal:`absent`\ .





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports IPv4 and IPv6 addresses.
   - This module supports \ :literal:`check\_mode`\ .
   - This module will always report changes found to be applied when \ :emphasis:`state`\  is \ :literal:`present`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create a session
      dellemc.openmanage.idrac_session:
        hostname: 198.162.0.1
        username: username
        password: password
        state: present

    - name: Delete a session
      dellemc.openmanage.idrac_session:
        hostname: 198.162.0.1
        state: absent
        auth_token: aed4aa802b748d2f3b31deec00a6b28a
        session_is: 2



Return Values
-------------

msg (always, str, The session has been created successfully.)
  Status of the session operation.


session_data (For session creation operation, dict, {'@Message.ExtendedInfo': [{'Message': 'The resource has been created successfully.', 'MessageArgs': [], 'MessageId': 'Base.1.12.Created', 'RelatedProperties': [], 'Resolution': 'None.', 'Severity': 'OK'}, {'Message': 'A new resource is successfully created.', 'MessageArgs': [], 'MessageId': 'IDRAC.2.9.SYS414', 'RelatedProperties': [], 'Resolution': 'No response action is required.', 'Severity': 'Informational'}], 'ClientOriginIPAddress': '100.96.37.58', 'CreatedTime': '2024-04-05T01:14:01-05:00', 'Description': 'User Session', 'Id': '74', 'Name': 'User Session', 'Password': None, 'SessionType': 'Redfish', 'UserName': 'root'})
  The session details.


x_auth_token (For session creation operation, str, d15f17f01cd627c30173b1582642497d)
  Authentication token.


error_info (On HTTP error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to complete the operation because an invalid username and/or password is entered, and therefore authentication failed.', 'MessageArgs': [], 'MessageId': 'IDRAC.2.9.SYS415', 'RelatedProperties': [], 'Resolution': 'Enter valid user name and password and retry the operation.', 'Severity': 'Warning'}], 'code': 'Base.1.12.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information'}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Rajshekar P(@rajshekarp87)

