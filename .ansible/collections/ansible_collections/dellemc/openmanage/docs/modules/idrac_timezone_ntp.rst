.. _idrac_timezone_ntp_module:


idrac_timezone_ntp -- Configures time zone and NTP on iDRAC
===========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to configure time zone and NTP on iDRAC.



Requirements
------------
The below requirements are needed on the host that executes this module.

- omsdk \>= 1.2.488
- python \>= 3.9.6



Parameters
----------

  setup_idrac_timezone (optional, str, None)
    Allows to configure time zone on iDRAC.


  enable_ntp (optional, str, None)
    Allows to enable or disable NTP on iDRAC.


  ntp_server_1 (optional, str, None)
    The IP address of the NTP server 1.


  ntp_server_2 (optional, str, None)
    The IP address of the NTP server 2.


  ntp_server_3 (optional, str, None)
    The IP address of the NTP server 3.


  share_name (optional, str, None)
    (deprecated)Network share or a local path.

    This option is deprecated and will be removed in the later version.


  share_user (optional, str, None)
    (deprecated)Network share user name. Use the format 'user@domain' or 'domain\\user' if user is part of a domain. This option is mandatory for CIFS share.

    This option is deprecated and will be removed in the later version.


  share_password (optional, str, None)
    (deprecated)Network share user password. This option is mandatory for CIFS share.

    This option is deprecated and will be removed in the later version.


  share_mnt (optional, str, None)
    (deprecated)Local mount path of the network share with read-write permission for ansible user. This option is mandatory for network shares.

    This option is deprecated and will be removed in the later version.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.

    If the username is not provided, then the environment variable \ :envvar:`IDRAC\_USERNAME`\  is used.

    Example: export IDRAC\_USERNAME=username


  idrac_password (True, str, None)
    iDRAC user password.

    If the password is not provided, then the environment variable \ :envvar:`IDRAC\_PASSWORD`\  is used.

    Example: export IDRAC\_PASSWORD=password


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
   - This module requires 'Administrator' privilege for \ :emphasis:`idrac\_user`\ .
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports both IPv4 and IPv6 address for \ :emphasis:`idrac\_ip`\ .
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Configure time zone and NTP on iDRAC
      dellemc.openmanage.idrac_timezone_ntp:
           idrac_ip: "190.168.0.1"
           idrac_user: "user_name"
           idrac_password: "user_password"
           ca_path: "/path/to/ca_cert.pem"
           setup_idrac_timezone: "UTC"
           enable_ntp: Enabled
           ntp_server_1: "190.168.0.1"
           ntp_server_2: "190.168.0.2"
           ntp_server_3: "190.168.0.3"



Return Values
-------------

msg (always, str, Successfully configured the iDRAC time settings.)
  Overall status of the timezone and ntp configuration.


timezone_ntp_status (success, dict, {'@odata.context': '/redfish/v1/$metadata#DellJob.DellJob', '@odata.id': '/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_861801613971', '@odata.type': '#DellJob.v1_0_0.DellJob', 'CompletionTime': '2020-04-06T19:06:01', 'Description': 'Job Instance', 'EndTime': None, 'Id': 'JID_861801613971', 'JobState': 'Completed', 'JobType': 'ImportConfiguration', 'Message': 'Successfully imported and applied Server Configuration Profile.', 'MessageArgs': [], 'MessageId': 'SYS053', 'Name': 'Import Configuration', 'PercentComplete': 100, 'StartTime': 'TIME_NOW', 'Status': 'Success', 'TargetSettingsURI': None, 'retval': True})
  Job details of the time zone setting operation.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------


- This module will be removed in version
  .
  *[deprecated]*


Authors
~~~~~~~

- Felix Stephen (@felixs88)
- Anooja Vardhineni (@anooja-vardhineni)

