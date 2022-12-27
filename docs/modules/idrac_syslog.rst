.. _idrac_syslog_module:


idrac_syslog -- Enable or disable the syslog on iDRAC
=====================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to enable or disable the iDRAC syslog.



Requirements
------------
The below requirements are needed on the host that executes this module.

- omsdk >= 1.2.488
- python >= 3.9.6



Parameters
----------

  syslog (optional, str, Enabled)
    Enables or disables an iDRAC syslog.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.


  idrac_password (True, str, None)
    iDRAC user password.


  idrac_port (optional, int, 443)
    iDRAC port.


  validate_certs (optional, bool, True)
    If ``False``, the SSL certificates will not be validated.

    Configure ``False`` only on personally controlled sites where self-signed certificates are used.

    Prior to collection version ``5.0.0``, the *validate_certs* is ``False`` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.


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
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports both IPv4 and IPv6 address for *idrac_ip*.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Enable iDRAC syslog
      dellemc.openmanage.idrac_syslog:
           idrac_ip:  "192.168.0.1"
           idrac_user:  "user_name"
           idrac_password:  "user_password"
           ca_path: "/path/to/ca_cert.pem"
           share_name:  "192.168.0.2:/share"
           share_password:  "share_user_pwd"
           share_user:  "share_user_name"
           share_mnt:  "/mnt/share"
           syslog:  "Enabled"

    - name: Disable iDRAC syslog
      dellemc.openmanage.idrac_syslog:
           idrac_ip:  "192.168.0.1"
           idrac_user:  "user_name"
           idrac_password:  "user_password"
           ca_path: "/path/to/ca_cert.pem"
           share_name:  "192.168.0.2:/share"
           share_password:  "share_user_pwd"
           share_user:  "share_user_name"
           share_mnt:  "/mnt/share"
           syslog:  "Disabled"



Return Values
-------------

msg (always, str, Successfully fetch the syslogs.)
  Overall status of the syslog export operation.


syslog_status (success, dict, {'@odata.context': '/redfish/v1/$metadata#DellJob.DellJob', '@odata.id': '/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_852940632485', '@odata.type': '#DellJob.v1_0_2.DellJob', 'CompletionTime': '2020-03-27T02:27:45', 'Description': 'Job Instance', 'EndTime': None, 'Id': 'JID_852940632485', 'JobState': 'Completed', 'JobType': 'ImportConfiguration', 'Message': 'Successfully imported and applied Server Configuration Profile.', 'MessageArgs': [], 'MessageArgs@odata.count': 0, 'MessageId': 'SYS053', 'Name': 'Import Configuration', 'PercentComplete': 100, 'StartTime': 'TIME_NOW', 'Status': 'Success', 'TargetSettingsURI': None, 'retval': True})
  Job details of the syslog operation.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)
- Anooja Vardhineni (@anooja-vardhineni)

