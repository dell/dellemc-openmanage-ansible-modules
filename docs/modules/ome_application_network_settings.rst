.. _ome_application_network_settings_module:


ome_application_network_settings -- This module allows you to configure the session inactivity timeout settings
===============================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows you to configure the session inactivity timeout settings on OpenManage Enterprise and OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  session_inactivity_timeout (optional, dict, None)
    Session inactivity timeout settings.


    enable_universal_timeout (optional, bool, None)
      Enable or disable the universal inactivity timeout.


    universal_timeout (optional, float, None)
      Duration of inactivity in minutes after which all sessions end.

      This is applicable when *enable_universal_timeout* is ``true``.

      This is mutually exclusive with *api_timeout*, *gui_timeout*, *ssh_timeout* and *serial_timeout*.


    api_timeout (optional, float, None)
      Duration of inactivity in minutes after which the API session ends.

      This is mutually exclusive with *universal_timeout*.


    api_sessions (optional, int, None)
      The maximum number of API sessions to be allowed.


    gui_timeout (optional, float, None)
      Duration of inactivity in minutes after which the web interface of Graphical User Interface (GUI) session ends.

      This is mutually exclusive with *universal_timeout*.


    gui_sessions (optional, int, None)
      The maximum number of GUI sessions to be allowed.


    ssh_timeout (optional, float, None)
      Duration of inactivity in minutes after which the SSH session ends.

      This is applicable only for OpenManage Enterprise Modular.

      This is mutually exclusive with *universal_timeout*.


    ssh_sessions (optional, int, None)
      The maximum number of SSH sessions to be allowed.

      This is applicable to OME-M only.


    serial_timeout (optional, float, None)
      Duration of inactivity in minutes after which the serial console session ends.

      This is applicable only for OpenManage Enterprise Modular.

      This is mutually exclusive with *universal_timeout*.


    serial_sessions (optional, int, None)
      The maximum number of serial console sessions to be allowed.

      This is applicable only for OpenManage Enterprise Modular.



  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.


  password (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.


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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise or OpenManage Enterprise Modular.
   - To configure other network settings such as network address, web server, and so on, refer to the respective OpenManage Enterprise application network setting modules.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Configure universal inactivity timeout
      ome_application_network_settings:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        session_inactivity_timeout:
          enable_universal_timeout: true
          universal_timeout: 30
          api_sessions: 90
          gui_sessions: 5
          ssh_sessions: 2
          serial_sessions: 1

    - name: Configure API and GUI timeout and sessions
      ome_application_network_settings:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        session_inactivity_timeout:
          api_timeout: 20
          api_sessions: 100
          gui_timeout: 25
          gui_sessions: 5

    - name: Configure timeout and sessions for all parameters
      ome_application_network_settings:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        session_inactivity_timeout:
          api_timeout: 20
          api_sessions: 100
          gui_timeout: 15
          gui_sessions: 5
          ssh_timeout: 30
          ssh_sessions: 2
          serial_timeout: 35
          serial_sessions: 1

    - name: Disable universal timeout and configure timeout and sessions for other parameters
      ome_application_network_settings:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        session_inactivity_timeout:
          enable_universal_timeout: false
          api_timeout: 20
          api_sessions: 100
          gui_timeout: 15
          gui_sessions: 5
          ssh_timeout: 30
          ssh_sessions: 2
          serial_timeout: 35
          serial_sessions: 1



Return Values
-------------

msg (always, str, Successfully updated the session timeout settings.)
  Overall status of the Session timeout settings.


session_inactivity_setting (success, dict, [{'SessionType': 'API', 'MaxSessions': 32, 'SessionTimeout': 99600, 'MinSessionTimeout': 60000, 'MaxSessionTimeout': 86400000, 'MinSessionsAllowed': 1, 'MaxSessionsAllowed': 100, 'MaxSessionsConfigurable': True, 'SessionTimeoutConfigurable': True}, {'SessionType': 'GUI', 'MaxSessions': 6, 'SessionTimeout': 99600, 'MinSessionTimeout': 60000, 'MaxSessionTimeout': 7200000, 'MinSessionsAllowed': 1, 'MaxSessionsAllowed': 6, 'MaxSessionsConfigurable': True, 'SessionTimeoutConfigurable': True}, {'SessionType': 'SSH', 'MaxSessions': 4, 'SessionTimeout': 99600, 'MinSessionTimeout': 60000, 'MaxSessionTimeout': 10800000, 'MinSessionsAllowed': 1, 'MaxSessionsAllowed': 4, 'MaxSessionsConfigurable': True, 'SessionTimeoutConfigurable': True}, {'SessionType': 'Serial', 'MaxSessions': 1, 'SessionTimeout': 99600, 'MinSessionTimeout': 60000, 'MaxSessionTimeout': 86400000, 'MinSessionsAllowed': 1, 'MaxSessionsAllowed': 1, 'MaxSessionsConfigurable': False, 'SessionTimeoutConfigurable': True}, {'SessionType': 'UniversalTimeout', 'MaxSessions': 0, 'SessionTimeout': -1, 'MinSessionTimeout': -1, 'MaxSessionTimeout': 86400000, 'MinSessionsAllowed': 0, 'MaxSessionsAllowed': 0, 'MaxSessionsConfigurable': False, 'SessionTimeoutConfigurable': True}])
  Returned when session inactivity timeout settings are updated successfully.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'CUSR1233', 'RelatedProperties': [], 'Message': 'The number of allowed concurrent sessions for API must be between 1 and 100 sessions.', 'MessageArgs': ['API', '1', '100'], 'Severity': 'Critical', 'Resolution': 'Enter values in the correct range and retry the operation.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Sachin Apagundi(@sachin-apa)

