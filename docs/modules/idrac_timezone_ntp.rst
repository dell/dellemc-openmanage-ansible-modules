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

- omsdk
- python >= 2.7.5



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


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.


  idrac_password (True, str, None)
    iDRAC user password.


  idrac_port (optional, int, 443)
    iDRAC port.


  share_name (True, str, None)
    Network share or a local path.


  share_user (optional, str, None)
    Network share user name. Use the format 'user@domain' or 'domain\\user' if user is part of a domain. This option is mandatory for CIFS share.


  share_password (optional, str, None)
    Network share user password. This option is mandatory for CIFS share.


  share_mnt (optional, str, None)
    Local mount path of the network share with read-write permission for ansible user. This option is mandatory for network shares.





Notes
-----

.. note::
   - This module requires 'Administrator' privilege for *idrac_user*.
   - Run this module from a system that has direct access to Dell EMC iDRAC.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Configure time zone and NTP on iDRAC
      dellemc.openmanage.idrac_timezone_ntp:
           idrac_ip:   "190.168.0.1"
           idrac_user: "user_name"
           idrac_password:  "user_password"
           share_name: "user_name:/share"
           share_password:  "share_password"
           share_user: "user_name"
           share_mnt: "/mnt/share"
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





Authors
~~~~~~~

- Felix Stephen (@felixs88)
- Anooja Vardhineni (@anooja-vardhineni)

