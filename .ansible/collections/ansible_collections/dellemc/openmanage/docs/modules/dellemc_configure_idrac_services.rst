.. _dellemc_configure_idrac_services_module:


dellemc_configure_idrac_services -- Configures the iDRAC services related attributes
====================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to configure the iDRAC services related attributes.



Requirements
------------
The below requirements are needed on the host that executes this module.

- omsdk >= 1.2.488
- python >= 3.9.6



Parameters
----------

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


  enable_web_server (optional, str, None)
    Whether to Enable or Disable webserver configuration for iDRAC.


  ssl_encryption (optional, str, None)
    Secure Socket Layer encryption for webserver.


  tls_protocol (optional, str, None)
    Transport Layer Security for webserver.


  https_port (optional, int, None)
    HTTPS access port.


  http_port (optional, int, None)
    HTTP access port.


  timeout (optional, str, None)
    Timeout value.


  snmp_enable (optional, str, None)
    Whether to Enable or Disable SNMP protocol for iDRAC.


  snmp_protocol (optional, str, None)
    Type of the SNMP protocol.


  community_name (optional, str, None)
    SNMP community name for iDRAC. It is used by iDRAC to validate SNMP queries received from remote systems requesting SNMP data access.


  alert_port (optional, int, 162)
    The iDRAC port number that must be used for SNMP traps. The default value is 162, and the acceptable range is between 1 to 65535.


  discovery_port (optional, int, 161)
    The SNMP agent port on the iDRAC. The default value is 161, and the acceptable range is between 1 to 65535.


  trap_format (optional, str, None)
    SNMP trap format for iDRAC.


  ipmi_lan (optional, dict, None)
    Community name set on iDRAC for SNMP settings.


    community_name (optional, str, None)
      This option is used by iDRAC when it sends out SNMP and IPMI traps. The community name is checked by the remote system to which the traps are sent.






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
    - name: Configure the iDRAC services attributes
      dellemc.openmanage.dellemc_configure_idrac_services:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        enable_web_server: "Enabled"
        http_port: 80
        https_port: 443
        ssl_encryption: "Auto_Negotiate"
        tls_protocol: "TLS_1_2_Only"
        timeout: "1800"
        snmp_enable: "Enabled"
        snmp_protocol: "SNMPv3"
        community_name: "public"
        alert_port: 162
        discovery_port: 161
        trap_format: "SNMPv3"
        ipmi_lan:
          community_name: "public"



Return Values
-------------

msg (always, str, Successfully configured the iDRAC services settings.)
  Overall status of iDRAC service attributes configuration.


service_status (success, dict, {'CompletionTime': '2020-04-02T02:43:28', 'Description': 'Job Instance', 'EndTime': None, 'Id': 'JID_12345123456', 'JobState': 'Completed', 'JobType': 'ImportConfiguration', 'Message': 'Successfully imported and applied Server Configuration Profile.', 'MessageArgs': [], 'MessageId': 'SYS053', 'Name': 'Import Configuration', 'PercentComplete': 100, 'StartTime': 'TIME_NOW', 'Status': 'Success', 'TargetSettingsURI': None, 'retval': True})
  Details of iDRAC services attributes configuration.


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

