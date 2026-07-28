.. _idrac_session_info_module:


idrac_session_info -- Query iDRAC session information
=========================================================

.. contents::
  :local:
  :depth: 1


Synopsis
---------

This module queries active iDRAC sessions, session service configuration,
and session limits with utilization reporting. Supports client-side filtering
by session type, username, and stale threshold. This module is read-only and
does not modify any state on the iDRAC.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username. If the username is not provided, then the environment variable :envvar:`IDRAC\_USERNAME` is used.


  idrac_password (True, str, None)
    iDRAC user password. If the password is not provided, then the environment variable :envvar:`IDRAC\_PASSWORD` is used.

    Aliases: idrac\_pwd


  idrac_port (optional, int, 443)
    iDRAC port.


  validate_certs (optional, bool, True)
    If :literal:`false`\ , the SSL certificates will not be validated.

    Configure :literal:`false` only on personally controlled sites where self\-signed certificates are used.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.


  session_type (optional, str, None)
    Filter sessions by DMTF SessionType enum value.

    Case\-insensitive matching.

    Valid values include C(Redfish), C(IPMI), C(OEM), C(WebUI), etc.


  username_filter (optional, str, None)
    Filter sessions by username substring match.

    Case\-insensitive matching.


  stale_threshold_minutes (optional, int, None)
    Flag sessions older than the specified number of minutes as stale.

    Must be a positive integer.

    Session age is computed from C(CreatedTime); this is a proxy for
    idle time as iDRAC Redfish has no C(LastAccessedTime).




Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports IPv4 and IPv6 addresses.
   - This module supports :literal:`check\_mode`.
   - Minimum firmware requirements - iDRAC9 >= 7.10.90.00, iDRAC10 >= 1.20.50.50.
   - Session age is computed from C(CreatedTime) and is a proxy for idle time.
   - Output is structured JSON via C(exit_json()). To export as CSV or text,
     use Ansible native filters (C(to_json), C(to_nice_yaml)) or Jinja2 templates.



Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Query all active iDRAC sessions
      dellemc.openmanage.idrac_session_info:
        idrac_ip: 198.162.0.1
        idrac_user: admin
        idrac_password: password
        ca_path: "/path/to/ca_cert.pem"

    - name: Filter sessions by type
      dellemc.openmanage.idrac_session_info:
        idrac_ip: 198.162.0.1
        idrac_user: admin
        idrac_password: password
        session_type: Redfish

    - name: Find stale sessions older than 24 hours
      dellemc.openmanage.idrac_session_info:
        idrac_ip: 198.162.0.1
        idrac_user: admin
        idrac_password: password
        stale_threshold_minutes: 1440

    - name: Filter sessions by username
      dellemc.openmanage.idrac_session_info:
        idrac_ip: 198.162.0.1
        idrac_user: admin
        idrac_password: password
        username_filter: root

    - name: Combined filtering
      dellemc.openmanage.idrac_session_info:
        idrac_ip: 198.162.0.1
        idrac_user: admin
        idrac_password: password
        session_type: Redfish
        username_filter: admin
        stale_threshold_minutes: 60

    - name: Export session data to CSV file using Jinja2 template
      block:
        - name: Query sessions
          dellemc.openmanage.idrac_session_info:
            idrac_ip: 198.162.0.1
            idrac_user: admin
            idrac_password: password
          register: result

        - name: Write CSV report
          ansible.builtin.copy:
            content: |
              Id,UserName,SessionType,ClientOriginIPAddress,CreatedTime,AgeMinutes
              {% for s in result.sessions %}
              {{ s.Id }},{{ s.UserName }},{{ s.SessionType }},{{ s.ClientOriginIPAddress }},{{ s.CreatedTime }},{{ s.session_age_minutes }}
              {% endfor %}
            dest: /tmp/session_report.csv
          delegate_to: localhost

    - name: Display session data as YAML
      block:
        - name: Query sessions
          dellemc.openmanage.idrac_session_info:
            idrac_ip: 198.162.0.1
            idrac_user: admin
            idrac_password: password
          register: result

        - name: Show sessions in YAML format
          ansible.builtin.debug:
            msg: "{{ result.sessions | to_nice_yaml }}"



Return Values
-------------

msg (always, str, Successfully retrieved session information.)
  Status of the session query operation.


sessions (success, list, [{'client_origin_ip': '192.168.1.10', 'created_time': '2024-07-28T10:00:00+00:00', 'description': 'User Session', 'id': '1', 'is_stale': False, 'session_age_minutes': 30, 'session_type': 'Redfish', 'username': 'root'}])
  List of active sessions with details.


session_count (success, int, 2)
  Number of sessions returned (after filtering).


session_service (success, dict, {'service_enabled': True, 'session_timeout': 1800})
  Session service configuration.


session_limits (success, dict, {'active_sessions': 2, 'max_sessions': 8, 'utilization_percent': 25.0})
  Session limits and utilization.







Status
------





Authors
~~~~~~~

- Saksham Nautiyal (@Saksham-Nautiyal)

