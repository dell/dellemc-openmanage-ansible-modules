.. _idrac_session_info_module:


idrac_session_info -- Query iDRAC session information
=====================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves information about active sessions on a Dell iDRAC.

It can query active sessions, session service configuration, and session limits.

Supports client\-side filtering by session type, username, and stale session detection.

This module is read\-only and does not modify any sessions.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  session_type (False, str, None)
    Filter sessions by DMTF session type.

    Case\-insensitive exact match against the :literal:`SessionType` field.


  username_filter (False, str, None)
    Filter sessions by username.

    Case\-insensitive substring match against the :literal:`UserName` field.


  stale_threshold_minutes (False, int, None)
    Flag sessions as stale if their age exceeds this threshold in minutes.

    Sessions older than this value will have :literal:`is\_stale` set to :literal:`true`.

    Must be a positive integer.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.

    If the username is not provided, then the environment variable :envvar:`IDRAC\_USERNAME` is used.

    Example: export IDRAC\_USERNAME=username


  idrac_password (True, str, None)
    iDRAC user password.

    If the password is not provided, then the environment variable :envvar:`IDRAC\_PASSWORD` is used.

    Example: export IDRAC\_PASSWORD=password


  idrac_port (optional, int, 443)
    iDRAC port.


  validate_certs (optional, bool, True)
    If :literal:`false`\ , the SSL certificates will not be validated.

    Configure :literal:`false` only on personally controlled sites where self\-signed certificates are used.

    Prior to collection version :literal:`5.0.0`\ , the :emphasis:`validate\_certs` is :literal:`false` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports IPv4 and IPv6 addresses.
   - This module supports :literal:`check\_mode`.
   - Minimum firmware versions \- iDRAC9 \>= 7.10.90.00, iDRAC10 \>= 1.20.50.50.
   - Session age is computed from :literal:`CreatedTime`\ , which reflects session creation time, not last activity. For true idle time detection, use iDRAC OEM Redfish extensions (future enhancement).
   - For fleet operations, use Ansible :literal:`forks` to parallelize queries across multiple iDRAC instances.
   - Administrator privileges are required to query all sessions. Non\-admin users may only see their own sessions.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Query all active sessions
      dellemc.openmanage.idrac_session_info:
        idrac_ip: 198.162.0.1
        idrac_user: username
        idrac_password: password
        ca_path: "/path/to/ca_cert.pem"

    - name: Filter sessions by type
      dellemc.openmanage.idrac_session_info:
        idrac_ip: 198.162.0.1
        idrac_user: username
        idrac_password: password
        ca_path: "/path/to/ca_cert.pem"
        session_type: Redfish

    - name: Find stale sessions older than 24 hours
      dellemc.openmanage.idrac_session_info:
        idrac_ip: 198.162.0.1
        idrac_user: username
        idrac_password: password
        ca_path: "/path/to/ca_cert.pem"
        stale_threshold_minutes: 1440

    - name: Filter by username and session type
      dellemc.openmanage.idrac_session_info:
        idrac_ip: 198.162.0.1
        idrac_user: username
        idrac_password: password
        ca_path: "/path/to/ca_cert.pem"
        session_type: Redfish
        username_filter: admin

    - name: Query sessions using token authentication
      dellemc.openmanage.idrac_session_info:
        idrac_ip: 198.162.0.1
        ca_path: "/path/to/ca_cert.pem"
        x_auth_token: "aed4aa802b748d2f3b31deec00a6b28a"

    - name: Troubleshoot Max Sessions Reached (UC-1)
      block:
        - name: Create a session
          dellemc.openmanage.idrac_session:
            hostname: 198.162.0.1
            username: "{{ vault_idrac_user }}"
            password: "{{ vault_idrac_password }}"
            ca_path: "/path/to/ca_cert.pem"
            state: present
          register: auth_data

        - name: Query session utilization
          dellemc.openmanage.idrac_session_info:
            idrac_ip: 198.162.0.1
            idrac_user: "{{ vault_idrac_user }}"
            idrac_password: "{{ vault_idrac_password }}"
            ca_path: "/path/to/ca_cert.pem"
          register: session_info

        - name: Display utilization
          ansible.builtin.debug:
            msg: "Session utilization: {{ session_info.session_limits.utilization_percent }}%"
      always:
        - name: Destroy the session
          dellemc.openmanage.idrac_session:
            hostname: 198.162.0.1
            ca_path: "/path/to/ca_cert.pem"
            state: absent
            x_auth_token: "{{ auth_data.x_auth_token }}"
            session_id: "{{ auth_data.session_data.Id }}"

    - name: Fleet-wide session monitoring (UC-2)
      hosts: idrac_fleet
      gather_facts: false
      tasks:
        - name: Query sessions on each iDRAC
          dellemc.openmanage.idrac_session_info:
            idrac_ip: "{{ inventory_hostname }}"
            idrac_user: "{{ vault_idrac_user }}"
            idrac_password: "{{ vault_idrac_password }}"
            ca_path: "/path/to/ca_cert.pem"
          register: session_info

        - name: Report high utilization
          ansible.builtin.debug:
            msg: "WARNING: {{ inventory_hostname }} at {{ session_info.session_limits.utilization_percent }}% utilization"
          when: session_info.session_limits.utilization_percent | default(0) > 80

    - name: Nightly stale session cleanup (UC-3)
      hosts: idrac_fleet
      gather_facts: false
      tasks:
        - name: Find stale sessions
          dellemc.openmanage.idrac_session_info:
            idrac_ip: "{{ inventory_hostname }}"
            idrac_user: "{{ vault_idrac_user }}"
            idrac_password: "{{ vault_idrac_password }}"
            ca_path: "/path/to/ca_cert.pem"
            stale_threshold_minutes: 1440
          register: session_info

        - name: Terminate stale sessions
          dellemc.openmanage.idrac_session:
            hostname: "{{ inventory_hostname }}"
            ca_path: "/path/to/ca_cert.pem"
            state: absent
            x_auth_token: "{{ vault_idrac_auth_token }}"
            session_id: "{{ item.id }}"
          loop: "{{ session_info.sessions | selectattr('is_stale', 'equalto', true) | list }}"
          when: session_info.sessions | selectattr('is_stale', 'equalto', true) | list | length > 0



Return Values
-------------

msg (always, str, Successfully retrieved session information.)
  Status of the session query operation.


sessions (success, list, [{'id': '74', 'user_name': 'root', 'client_origin_ip': '100.96.37.58', 'session_type': 'Redfish', 'created_time': '2024-04-05T01:14:01-05:00', 'description': 'User Session', 'name': 'User Session', 'session_age_minutes': 120, 'is_stale': False}])
  List of active sessions with details.


session_count (success, int, 3)
  Number of sessions returned (after filtering).


session_service (success, dict, {'session_timeout': 1800, 'service_enabled': True})
  Session service configuration.


session_limits (success, dict, {'max_sessions': 64, 'active_count': 5, 'utilization_percent': 7.81, 'source': 'idrac_attributes'})
  Session limits and utilization.


idrac_firmware_version (success, str, 7.10.90.00)
  Detected iDRAC firmware version.


idrac_model (success, str, iDRAC 9)
  Detected iDRAC model.


error_info (on HTTP error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to complete the operation.', 'MessageId': 'IDRAC.2.9.SYS415', 'Resolution': 'Enter valid credentials.', 'Severity': 'Warning'}], 'code': 'Base.1.12.GeneralError', 'message': 'A general error has occurred.'}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Saksham Nautiyal (@Saksham-Nautiyal)

