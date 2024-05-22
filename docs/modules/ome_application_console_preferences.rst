.. _ome_application_console_preferences_module:


ome_application_console_preferences -- Configure console preferences on OpenManage Enterprise.
==============================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows user to configure the console preferences on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  report_row_limit (optional, int, None)
    The maximum number of rows that you can view on OpenManage Enterprise reports.


  device_health (optional, dict, None)
    The time after which the health of the devices must be automatically monitored and updated on the OpenManage Enterprise dashboard.


    health_check_interval (optional, int, None)
      The frequency at which the device health must be recorded and data stored.


    health_check_interval_unit (optional, str, None)
      The time unit of the frequency at which the device health must be recorded and data stored.

      \ :literal:`Hourly`\  to set the frequency in hours.

      \ :literal:`Minutes`\  to set the frequency in minutes.


    health_and_power_state_on_connection_lost (optional, str, None)
      The latest recorded device health.

      \ :literal:`last\_known`\  to display the latest recorded device health when the power connection was lost.

      \ :literal:`unknown`\  to display the latest recorded device health when the device status moved to unknown.



  discovery_settings (optional, dict, None)
    The device naming to be used by the OpenManage Enterprise to identify the discovered iDRACs and other devices.


    general_device_naming (optional, str, DNS)
      Applicable to all the discovered devices other than the iDRACs.

      \ :literal:`DNS`\  to use the DNS name.

      \ :literal:`NETBIOS`\  to use the NetBIOS name.


    server_device_naming (optional, str, IDRAC_SYSTEM_HOSTNAME)
      Applicable to iDRACs only.

      \ :literal:`IDRAC\_HOSTNAME`\  to use the iDRAC hostname.

      \ :literal:`IDRAC\_SYSTEM\_HOSTNAME`\  to use the system hostname.


    invalid_device_hostname (optional, str, None)
      The invalid hostnames separated by a comma.


    common_mac_addresses (optional, str, None)
      The common MAC addresses separated by a comma.



  server_initiated_discovery (optional, dict, None)
    Server initiated discovery settings.


    device_discovery_approval_policy (optional, str, None)
      Discovery approval policies.

      \ :literal:`Automatic`\  allows servers with iDRAC Firmware version 4.00.00.00, which are on the same network as the console, to be discovered automatically by the console.

      \ :literal:`Manual`\  for the servers to be discovered by the user manually.


    set_trap_destination (optional, bool, None)
      Trap destination settings.



  mx7000_onboarding_preferences (optional, str, None)
    Alert-forwarding behavior on chassis when they are onboarded.

    \ :literal:`all`\  to receive all alert.

    \ :literal:`chassis`\  to receive chassis category alerts only.


  builtin_appliance_share (optional, dict, None)
    The external network share that the appliance must access to complete operations.


    share_options (optional, str, None)
      The share options.

      \ :literal:`CIFS`\  to select CIFS share type.

      \ :literal:`HTTPS`\  to select HTTPS share type.


    cifs_options (optional, str, None)
      The SMB protocol version.

      \ :emphasis:`cifs\_options`\  is required \ :emphasis:`share\_options`\  is \ :literal:`CIFS`\ .

      \ :literal:`V1`\  to enable SMBv1.

      \ :literal:`V2`\  to enable SMBv2



  email_sender_settings (optional, str, None)
    The email address of the user who is sending an email message.


  trap_forwarding_format (optional, str, None)
    The trap forwarding format.

    \ :literal:`Original`\  to retain the trap data as is.

    \ :literal:`Normalized`\  to normalize the trap data.


  metrics_collection_settings (optional, int, None)
    The frequency of the PowerManager extension data maintenance and purging.


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
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Update Console preferences with all the settings.
      dellemc.openmanage.ome_application_console_preferences:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        report_row_limit: 123
        device_health:
          health_check_interval: 1
          health_check_interval_unit: Hourly
          health_and_power_state_on_connection_lost: last_known
        discovery_settings:
          general_device_naming: DNS
          server_device_naming: IDRAC_HOSTNAME
          invalid_device_hostname: "localhost"
          common_mac_addresses: "::"
        server_initiated_discovery:
          device_discovery_approval_policy: Automatic
          set_trap_destination: true
        mx7000_onboarding_preferences: all
        builtin_appliance_share:
          share_options: CIFS
          cifs_options: V1
        email_sender_settings: "admin@dell.com"
        trap_forwarding_format: Normalized
        metrics_collection_settings: 31

    - name: Update Console preferences with report and device health settings.
      dellemc.openmanage.ome_application_console_preferences:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        report_row_limit: 236
        device_health:
          health_check_interval: 10
          health_check_interval_unit: Hourly
          health_and_power_state_on_connection_lost: last_known

    - name: Update Console preferences with invalid device health settings.
      dellemc.openmanage.ome_application_console_preferences:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_health:
          health_check_interval: 65
          health_check_interval_unit: Minutes

    - name: Update Console preferences with discovery and built in appliance share settings.
      dellemc.openmanage.ome_application_console_preferences:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        discovery_settings:
          general_device_naming: DNS
          server_device_naming: IDRAC_SYSTEM_HOSTNAME
          invalid_device_hostname: "localhost"
          common_mac_addresses: "00:53:45:00:00:00"
        builtin_appliance_share:
          share_options: CIFS
          cifs_options: V1

    - name: Update Console preferences with server initiated discovery, mx7000 onboarding preferences, email sender,
        trap forwarding format, and metrics collection settings.
      dellemc.openmanage.ome_application_console_preferences:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        server_initiated_discovery:
          device_discovery_approval_policy: Automatic
          set_trap_destination: true
        mx7000_onboarding_preferences: chassis
        email_sender_settings: "admin@dell.com"
        trap_forwarding_format: Original
        metrics_collection_settings: 365



Return Values
-------------

msg (always, str, Successfully update the console preferences.)
  Overall status of the console preferences.


console_preferences (on success, list, [{'Name': 'DEVICE_PREFERRED_NAME', 'DefaultValue': 'SLOT_NAME', 'Value': 'PREFER_DNS,PREFER_IDRAC_SYSTEM_HOSTNAME', 'DataType': 'java.lang.String', 'GroupName': 'DISCOVERY_SETTING'}, {'Name': 'INVALID_DEVICE_HOSTNAME', 'DefaultValue': '', 'Value': 'localhost,localhost.localdomain,not defined,pv132t,pv136t,default,dell,idrac-', 'DataType': 'java.lang.String', 'GroupName': 'DISCOVERY_SETTING'}, {'Name': 'COMMON_MAC_ADDRESSES', 'DefaultValue': '', 'Value': '00:53:45:00:00:00,33:50:6F:45:30:30,50:50:54:50:30:30,00:00:FF:FF:FF:FF,20:41:53:59:4E:FF,00:00:00:00:00:00,20:41:53:59:4e:ff,00:00:00:00:00:00', 'DataType': 'java.lang.String', 'GroupName': 'DISCOVERY_SETTING'}, {'Name': 'SHARE_TYPE', 'DefaultValue': 'CIFS', 'Value': 'CIFS', 'DataType': 'java.lang.String', 'GroupName': 'BUILT_IN_APPLIANCE_SHARE_SETTINGS'}, {'Name': 'TRAP_FORWARDING_SETTING', 'DefaultValue': 'AsIs', 'Value': 'Normalized', 'DataType': 'java.lang.String', 'GroupName': ''}, {'Name': 'DATA_PURGE_INTERVAL', 'DefaultValue': '365', 'Value': '3650000', 'DataType': 'java.lang.Integer', 'GroupName': ''}, {'Name': 'CONSOLE_CONNECTION_SETTING', 'DefaultValue': 'last_known', 'Value': 'last_known', 'DataType': 'java.lang.String', 'GroupName': 'CONSOLE_CONNECTION_SETTING'}, {'Name': 'MIN_PROTOCOL_VERSION', 'DefaultValue': 'V2', 'Value': 'V1', 'DataType': 'java.lang.String', 'GroupName': 'CIFS_PROTOCOL_SETTINGS'}, {'Name': 'ALERT_ACKNOWLEDGEMENT_VIEW', 'DefaultValue': '2000', 'Value': '2000', 'DataType': 'java.lang.Integer', 'GroupName': ''}, {'Name': 'AUTO_CONSOLE_UPDATE_AFTER_DOWNLOAD', 'DefaultValue': 'false', 'Value': 'false', 'DataType': 'java.lang.Boolean', 'GroupName': 'CONSOLE_UPDATE_SETTING_GROUP'}, {'Name': 'NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION', 'DefaultValue': 'false', 'Value': 'false', 'DataType': 'java.lang.Boolean', 'GroupName': ''}, {'Name': 'REPORTS_MAX_RESULTS_LIMIT', 'DefaultValue': '0', 'Value': '2000000000000000000000000', 'DataType': 'java.lang.Integer', 'GroupName': ''}, {'Name': 'EMAIL_SENDER', 'DefaultValue': 'omcadmin@dell.com', 'Value': 'admin1@dell.com@dell.com@dell.com', 'DataType': 'java.lang.String', 'GroupName': ''}, {'Name': 'MX7000_ONBOARDING_PREF', 'DefaultValue': 'all', 'Value': 'test_chassis', 'DataType': 'java.lang.String', 'GroupName': ''}, {'Name': 'DISCOVERY_APPROVAL_POLICY', 'DefaultValue': 'Automatic', 'Value': 'Automatic_test', 'DataType': 'java.lang.String', 'GroupName': ''}])
  Details of the console preferences.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'CGEN1006', 'RelatedProperties': [], 'Message': 'Unable to complete the request because the resource URI does not exist or is not implemented.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Enter a valid URI and retry the operation.'}]}})
  Details of the HTTP error.





Status
------





Authors
~~~~~~~

- Sachin Apagundi(@sachin-apa)
- Husniya Hameed (@husniya-hameed)
- ShivamSh3 (@ShivamSh3)

