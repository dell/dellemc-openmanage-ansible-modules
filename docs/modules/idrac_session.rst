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
    Username of the iDRAC. If the username is not provided, then the environment variable :envvar:`IDRAC\_USERNAME` is used.

    :emphasis:`username` is required when :emphasis:`state` is :literal:`present`.


  password (optional, str, None)
    Password of the iDRAC. If the password is not provided, then the environment variable :envvar:`IDRAC\_PASSWORD` is used.

    :emphasis:`password` is required when :emphasis:`state` is :literal:`present`.


  port (optional, int, 443)
    Port of the iDRAC.


  validate_certs (optional, bool, True)
    If :literal:`false`\ , the SSL certificates will not be validated.

    Configure :literal:`false` only on personally controlled sites where self-signed certificates are used.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The https socket level timeout in seconds.


  state (optional, str, present)
    The state of the session in an iDRAC.

    :literal:`present` creates a session.

    :literal:`absent` deletes a session.

    Module will always report changes found to be applied when :emphasis:`state` is :literal:`present`.


  x_auth_token (optional, str, None)
    Authentication token.

    :emphasis:`x\_auth\_token` is required when :emphasis:`state` is :literal:`absent`.


  session_id (optional, str, None)
    Session ID of the iDRAC.

    :emphasis:`session\_id` is required when :emphasis:`state` is :literal:`absent`.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports IPv4 and IPv6 addresses.
   - This module supports :literal:`check\_mode`.
   - This module will always report changes found to be applied when :emphasis:`state` is :literal:`present`.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create a session
      dellemc.openmanage.idrac_session:
        hostname: 198.162.0.1
        username: username
        password: password
        ca_path: "/path/to/ca_cert.pem"
        state: present

    - name: Delete a session
      dellemc.openmanage.idrac_session:
        hostname: 198.162.0.1
        ca_path: "/path/to/ca_cert.pem"
        state: absent
        x_auth_token: aed4aa802b748d2f3b31deec00a6b28a
        session_id: 2

    - name: Create a session and execute other modules
      block:
        - name: Create a session
          dellemc.openmanage.idrac_session:
            hostname: 198.162.0.1
            username: username
            password: password
            ca_path: "/path/to/ca_cert.pem"
            state: present
            register: authData

        - name: Call idrac_firmware_info module
          dellemc.openmanage.idrac_firmware_info:
            idrac_ip: 198.162.0.1
            ca_path: "/path/to/ca_cert.pem"
            x_auth_token: "{{ authData.x_auth_token }}"

        - name: Call idrac_user_info module
          dellemc.openmanage.idrac_user_info:
            idrac_ip: 198.162.0.1
            ca_path: "/path/to/ca_cert.pem"
            x_auth_token: "{{ authData.x_auth_token }}"
      always:
        - name: Destroy a session
          dellemc.openmanage.idrac_session:
            hostname: 198.162.0.1
            ca_path: "/path/to/ca_cert.pem"
            state: absent
            x_auth_token: "{{ authData.x_auth_token }}"
            session_id: "{{ authData.session_data.Id }}"



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
- Kritika Bhateja (@Kritika-Bhateja-03)
- Saksham Nautiyal (@Saksham-Nautiyal)

