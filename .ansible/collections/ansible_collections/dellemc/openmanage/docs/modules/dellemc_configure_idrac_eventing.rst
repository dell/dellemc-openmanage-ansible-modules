.. _dellemc_configure_idrac_eventing_module:


dellemc_configure_idrac_eventing -- Configures the iDRAC eventing related attributes
====================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to configure the iDRAC eventing related attributes.



Requirements
------------
The below requirements are needed on the host that executes this module.

- omsdk >= 1.2.503
- python >= 3.9.6



Parameters
----------

  share_name (optional, str, None)
    (deprecated)Network share or a local path.

    This option is deprecated and will be removed in the later version.


  share_user (optional, str, None)
    (deprecated)Network share user in the format 'user@domain' or 'domain\user' if user is part of a domain else 'user'. This option is mandatory for CIFS Network Share.

    This option is deprecated and will be removed in the later version.


  share_password (optional, str, None)
    (deprecated)Network share user password. This option is mandatory for CIFS Network Share.

    This option is deprecated and will be removed in the later version.


  share_mnt (optional, str, None)
    (deprecated)Local mount path of the network share with read-write permission for ansible user. This option is mandatory for Network Share.

    This option is deprecated and will be removed in the later version.


  destination_number (optional, int, None)
    Destination number for SNMP Trap.


  destination (optional, str, None)
    Destination for SNMP Trap.


  snmp_v3_username (optional, str, None)
    SNMP v3 username for SNMP Trap.


  snmp_trap_state (optional, str, None)
    Whether to Enable or Disable SNMP alert.


  email_alert_state (optional, str, None)
    Whether to Enable or Disable Email alert.


  alert_number (optional, int, None)
    Alert number for Email configuration.


  address (optional, str, None)
    Email address for SNMP Trap.


  custom_message (optional, str, None)
    Custom message for SNMP Trap reference.


  enable_alerts (optional, str, None)
    Whether to Enable or Disable iDRAC alerts.


  authentication (optional, str, None)
    Simple Mail Transfer Protocol Authentication.


  smtp_ip_address (optional, str, None)
    Enter the IPv4 or IPv6 address of the SMTP server or the FQDN or DNS name.


  smtp_port (optional, str, None)
    SMTP Port number for access.


  username (optional, str, None)
    Username for SMTP authentication.


  password (optional, str, None)
    Password for SMTP authentication.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.


  idrac_password (True, str, None)
    iDRAC user password.


  idrac_port (optional, int, 443)
    iDRAC port.


  validate_certs (optional, bool, True)
    If ``false``, the SSL certificates will not be validated.

    Configure ``false`` only on personally controlled sites where self-signed certificates are used.

    Prior to collection version ``5.0.0``, the *validate_certs* is ``false`` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





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
    - name: Configure the iDRAC eventing attributes
      dellemc.openmanage.dellemc_configure_idrac_eventing:
           idrac_ip: "192.168.0.1"
           idrac_user: "user_name"
           idrac_password: "user_password"
           ca_path: "/path/to/ca_cert.pem"
           destination_number: "2"
           destination: "1.1.1.1"
           snmp_v3_username: "None"
           snmp_trap_state: "Enabled"
           email_alert_state: "Disabled"
           alert_number: "1"
           address: "alert_email@company.com"
           custom_message: "Custom Message"
           enable_alerts: "Disabled"
           authentication: "Enabled"
           smtp_ip_address: "192.168.0.1"
           smtp_port: "25"
           username: "username"
           password: "password"



Return Values
-------------

msg (always, str, Successfully configured the iDRAC eventing settings.)
  Successfully configured the iDRAC eventing settings.


eventing_status (success, dict, {'CompletionTime': '2020-04-02T02:43:28', 'Description': 'Job Instance', 'EndTime': None, 'Id': 'JID_12345123456', 'JobState': 'Completed', 'JobType': 'ImportConfiguration', 'Message': 'Successfully imported and applied Server Configuration Profile.', 'MessageArgs': [], 'MessageId': 'SYS053', 'Name': 'Import Configuration', 'PercentComplete': 100, 'StartTime': 'TIME_NOW', 'Status': 'Success', 'TargetSettingsURI': None, 'retval': True})
  Configures the iDRAC eventing attributes.


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

