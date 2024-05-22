.. _ome_session_module:


ome_session -- Manage OpenManage Enterprise and OpenManage Enterprise modular sessions
======================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows you  to create and delete sessions on OpenManage Enterprise and OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  hostname (optional, str, None)
    IP address or hostname of the OpenManage Enterprise.


  username (optional, str, None)
    Username of the OpenManage Enterprise. If the username is not provided, then the environment variable \ :envvar:`OME\_USERNAME`\  is used.

    \ :emphasis:`username`\  is required when \ :emphasis:`state`\  is \ :literal:`present`\ .


  password (optional, str, None)
    Password of the OpenManage Enterprise. If the password is not provided, then the environment variable \ :envvar:`OME\_PASSWORD`\  is used.

    \ :emphasis:`password`\  is required when \ :emphasis:`state`\  is \ :literal:`present`\ .


  port (optional, int, 443)
    Port of the OpenManage Enterprise.


  validate_certs (optional, bool, True)
    If \ :literal:`false`\ , the SSL certificates will not be validated.

    Configure \ :literal:`false`\  only on personally controlled sites where self-signed certificates are used.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The HTTPS socket level timeout in seconds.


  state (optional, str, present)
    The state of the session in OpenManage Enterprise.

    \ :literal:`present`\  creates a session.

    \ :literal:`absent`\  deletes a session.

    Module will always report changes found to be applied when \ :emphasis:`state`\  is \ :literal:`present`\ .


  x_auth_token (optional, str, None)
    Authentication token.

    \ :emphasis:`x\_auth\_token`\  is required when \ :emphasis:`state`\  is \ :literal:`absent`\ .


  session_id (optional, str, None)
    Session ID of the OpenManage Enterprise.

    \ :emphasis:`session\_id`\  is required when \ :emphasis:`state`\  is \ :literal:`absent`\ .





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.
   - This module supports IPv4 and IPv6 addresses.
   - This module supports \ :literal:`check\_mode`\ .
   - This module will always report changes found to be applied when \ :emphasis:`state`\  is \ :literal:`present`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create a session
      dellemc.openmanage.ome_session:
        hostname: 198.162.0.1
        username: username
        password: password
        ca_path: "/path/to/ca_cert.pem"
        state: present

    - name: Delete a session
      dellemc.openmanage.ome_session:
        hostname: 198.162.0.1
        ca_path: "/path/to/ca_cert.pem"
        state: absent
        x_auth_token: aed4aa802b748d2f3b31deec00a6b28a
        session_id: 4b48e9ab-809e-4087-b7c4-201a16e0143d

    - name: Create a session and execute other modules
      block:
        - name: Create a session
          dellemc.openmanage.ome_session:
            hostname: 198.162.0.1
            username: username
            password: password
            ca_path: "/path/to/ca_cert.pem"
            state: present
            register: authData

        - name: Call ome_user_info module
          dellemc.openmanage.ome_user_info:
            hostname: 198.162.0.1
            ca_path: "/path/to/ca_cert.pem"
            x_auth_token: "{{ authData.x_auth_token }}"

        - name: Call ome_network_vlan_info module
          dellemc.openmanage.ome_network_vlan_info:
            hostname: 198.162.0.1
            ca_path: "/path/to/ca_cert.pem"
            x_auth_token: "{{ authData.x_auth_token }}"
      always:
        - name: Destroy a session
          dellemc.openmanage.ome_session:
            hostname: 198.162.0.1
            ca_path: "/path/to/ca_cert.pem"
            state: absent
            x_auth_token: "{{ authData.x_auth_token }}"
            session_id: "{{ authData.session_data.Id }}"



Return Values
-------------

msg (always, str, The session has been created successfully.)
  Status of the session operation.


session_data (For session creation operation, dict, {'Id': 'd5c28d8e-1084-4055-9c01-e1051cfee2dd', 'Description': 'admin', 'Name': 'API', 'UserName': 'admin', 'UserId': 10078, 'Password': None, 'Roles': ['BACKUP_ADMINISTRATOR'], 'IpAddress': '100.198.162.0', 'StartTimeStamp': '2023-07-03 07:22:43.683', 'LastAccessedTimeStamp': '2023-07-03 07:22:43.683', 'DirectoryGroup': []})
  The session details.


x_auth_token (For session creation operation, str, d15f17f01cd627c30173b1582642497d)
  Authentication token.


error_info (On HTTP error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to complete the operation because an invalid username and/or password is entered, and therefore authentication failed.', 'MessageArgs': [], 'MessageArgs@odata.count': 0, 'MessageId': 'IDRAC.2.7.SYS415', 'RelatedProperties': [], 'RelatedProperties@odata.count': 0, 'Resolution': 'Enter valid user name and password and retry the operation.', 'Severity': 'Warning'}], 'code': 'Base.1.12.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information'}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Kritika Bhateja (@Kritika-Bhateja-03)

