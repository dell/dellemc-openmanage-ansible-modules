.. _ome_application_network_time_module:


ome_application_network_time -- Updates the network time on OpenManage Enterprise
=================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows the configuration of network time on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  enable_ntp (True, bool, None)
    Enables or disables Network Time Protocol(NTP).

    If \ :emphasis:`enable\_ntp`\  is false, then the NTP addresses reset to their default values.


  system_time (optional, str, None)
    Time in the current system.

    This option is only applicable when \ :emphasis:`enable\_ntp`\  is false.

    This option must be provided in following format 'yyyy-mm-dd hh:mm:ss'.


  time_zone (optional, str, None)
    The valid timezone ID to be used.

    This option is applicable for both system time and NTP time synchronization.


  primary_ntp_address (optional, str, None)
    The primary NTP address.

    This option is applicable when \ :emphasis:`enable\_ntp`\  is true.


  secondary_ntp_address1 (optional, str, None)
    The first secondary NTP address.

    This option is applicable when \ :emphasis:`enable\_ntp`\  is true.


  secondary_ntp_address2 (optional, str, None)
    The second secondary NTP address.

    This option is applicable when \ :emphasis:`enable\_ntp`\  is true.


  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (False, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.

    If the username is not provided, then the environment variable \ :envvar:`OME\_USERNAME`\  is used.

    Example: export OME\_USERNAME=username


  password (False, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.

    If the password is not provided, then the environment variable \ :envvar:`OME\_PASSWORD`\  is used.

    Example: export OME\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`OME\_X\_AUTH\_TOKEN`\  is used.

    Example: export OME\_X\_AUTH\_TOKEN=x\_auth\_token


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.


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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Configure system time
      dellemc.openmanage.ome_application_network_time:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        enable_ntp: false
        system_time: "2020-03-31 21:35:18"
        time_zone: "TZ_ID_11"

    - name: Configure NTP server for time synchronization
      dellemc.openmanage.ome_application_network_time:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        enable_ntp: true
        time_zone: "TZ_ID_66"
        primary_ntp_address: "192.168.0.2"
        secondary_ntp_address1: "192.168.0.2"
        secondary_ntp_address2: "192.168.0.4"



Return Values
-------------

msg (always, str, Successfully configured network time.)
  Overall status of the network time configuration change.


proxy_configuration (success, dict, {'EnableNTP': False, 'JobId': None, 'PrimaryNTPAddress': None, 'SecondaryNTPAddress1': None, 'SecondaryNTPAddress2': None, 'SystemTime': None, 'TimeSource': 'Local Clock', 'TimeZone': 'TZ_ID_1', 'TimeZoneIdLinux': None, 'TimeZoneIdWindows': None, 'UtcTime': None})
  Updated application network time configuration.


error_info (on HTTP error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to complete the request because the input value for  SystemTime  is missing or an invalid value is entered.', 'MessageArgs': ['SystemTime'], 'MessageId': 'CGEN6002', 'RelatedProperties': [], 'Resolution': 'Enter a valid value and retry the operation.', 'Severity': 'Critical'}], 'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.'}})
  Details of the HTTP error.





Status
------





Authors
~~~~~~~

- Sajna Shetty(@Sajna-Shetty)
- Mangirish Kenkare(@MangirishK)

