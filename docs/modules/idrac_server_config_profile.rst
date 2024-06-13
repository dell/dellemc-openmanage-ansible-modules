.. _idrac_server_config_profile_module:


idrac_server_config_profile -- Export or Import iDRAC Server Configuration Profile (SCP)
========================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Export the Server Configuration Profile (SCP) from the iDRAC or import from a network share (CIFS, NFS, HTTP, HTTPS) or a local path.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.14



Parameters
----------

  command (optional, str, export)
    If \ :literal:`import`\ , the module performs SCP import operation.

    If \ :literal:`export`\ , the module performs SCP export operation.

    If \ :literal:`preview`\ , the module performs SCP preview operation.

    \ :literal:`import\_custom\_defaults`\  allows you to import custom default iDRAC settings.

    \ :literal:`export\_custom\_defaults`\  allows you to export custom default iDRAC settings.

    \ :literal:`import\_custom\_defaults`\  and \ :literal:`export\_custom\_defaults`\  is supported only on iDRAC9 with firmware 7.00.00.00 and above.


  job_wait (True, bool, None)
    Whether to wait for job completion or not.


  share_name (optional, str, None)
    Network share or local path.

    CIFS, NFS, HTTP, and HTTPS network share types are supported.

    \ :emphasis:`share\_name`\  is mutually exclusive with \ :emphasis:`import\_buffer`\ .

    Only "local" is supported when the \ :emphasis:`command`\  is \ :literal:`import\_custom\_defaults`\  or \ :literal:`export\_custom\_defaults`\ .


  share_user (optional, str, None)
    Network share user in the format 'user@domain' or 'domain\\\\user' if user is part of a domain else 'user'. This option is mandatory for CIFS Network Share.


  share_password (optional, str, None)
    Network share user password. This option is mandatory for CIFS Network Share.


  scp_file (optional, str, None)
    Name of the server configuration profile (SCP) file.

    Only XML file format is supported when \ :emphasis:`command`\  is \ :literal:`import`\  or \ :literal:`import\_custom\_defaults`\  or \ :literal:`export\_custom\_defaults`\ .

    The default format \<idrac\_ip\>\_YYmmdd\_HHMMSS\_scp is used if this option is not specified for \ :literal:`export`\  or \ :literal:`export\_custom\_defaults`\ .

    \ :emphasis:`export\_format`\  is used if the valid extension file is not provided for \ :literal:`export`\ .


  scp_components (optional, list, ALL)
    If \ :literal:`ALL`\ , this option exports or imports all components configurations from the SCP file.

    If \ :literal:`IDRAC`\ , this option exports or imports iDRAC configuration from the SCP file.

    If \ :literal:`BIOS`\ , this option exports or imports BIOS configuration from the SCP file.

    If \ :literal:`NIC`\ , this option exports or imports NIC configuration from the SCP file.

    If \ :literal:`RAID`\ , this option exports or imports RAID configuration from the SCP file.

    If \ :literal:`FC`\ , this option exports or imports FiberChannel configurations from the SCP file.

    If \ :literal:`InfiniBand`\ , this option exports or imports InfiniBand configuration from the SCP file.

    If \ :literal:`SupportAssist`\ , this option exports or imports SupportAssist configuration from the SCP file.

    If \ :literal:`EventFilters`\ , this option exports or imports EventFilters configuration from the SCP file.

    If \ :literal:`System`\ , this option exports or imports System configuration from the SCP file.

    If \ :literal:`LifecycleController`\ , this option exports or imports SupportAssist configuration from the SCP file.

    If \ :literal:`AHCI`\ , this option exports or imports EventFilters configuration from the SCP file.

    If \ :literal:`PCIeSSD`\ , this option exports or imports PCIeSSD configuration from the SCP file.

    When \ :emphasis:`command`\  is \ :literal:`export`\  or \ :literal:`import`\  \ :emphasis:`target`\  with multiple components is supported only on iDRAC9 with firmware 6.10.00.00 and above.


  shutdown_type (optional, str, Graceful)
    This option is applicable for \ :literal:`import`\  command.

    If \ :literal:`Graceful`\ , the job gracefully shuts down the operating system and turns off the server.

    If \ :literal:`Forced`\ , it forcefully shuts down the server.

    If \ :literal:`NoReboot`\ , the job that applies the SCP will pause until you manually reboot the server.


  end_host_power_state (optional, str, On)
    This option is applicable for \ :literal:`import`\  command.

    If \ :literal:`On`\ , End host power state is on.

    If \ :literal:`Off`\ , End host power state is off.


  export_format (optional, str, XML)
    Specify the output file format. This option is applicable for \ :literal:`export`\  or \ :literal:`export\_custom\_defaults`\  command.

    The default export file format is always XML when the  \ :emphasis:`command`\  is \ :literal:`export\_custom\_defaults`\ .


  export_use (optional, str, Default)
    Specify the type of Server Configuration Profile (SCP) to be exported.

    This option is applicable when \ :emphasis:`command`\  is \ :literal:`export`\ .

    \ :literal:`Default`\  Creates a non-destructive snapshot of the configuration.

    \ :literal:`Replace`\  Replaces a server with another or restores the servers settings to a known baseline.

    \ :literal:`Clone`\  Clones settings from one server to another server with the identical hardware setup. All settings except I/O identity are updated (e.g. will reset RAID). The settings in this export will be destructive when uploaded to another system.


  ignore_certificate_warning (optional, str, ignore)
    If \ :literal:`ignore`\ , it ignores the certificate warnings.

    If \ :literal:`showerror`\ , it shows the certificate warnings.

    \ :emphasis:`ignore\_certificate\_warning`\  is considered only when \ :emphasis:`share\_name`\  is of type HTTPS and is supported only on iDRAC9.


  include_in_export (optional, str, default)
    This option is applicable when \ :emphasis:`command`\  is \ :literal:`export`\ .

    If \ :literal:`default`\ , it exports the default Server Configuration Profile.

    If \ :literal:`readonly`\ , it exports the SCP with readonly attributes.

    If \ :literal:`passwordhashvalues`\ , it exports the SCP with password hash values.

    If \ :literal:`customtelemetry`\ , exports the SCP with custom telemetry attributes supported only in the iDRAC9.


  import_buffer (optional, str, None)
    Used to import the buffer input of xml or json into the iDRAC.

    When the  \ :emphasis:`command`\  is \ :literal:`import\_custom\_defaults`\ , only XML file format is supported.

    This option is applicable when \ :emphasis:`command`\  is \ :literal:`import`\  or \ :literal:`preview`\  or \ :literal:`import\_custom\_defaults`\ .

    \ :emphasis:`import\_buffer`\  is mutually exclusive with \ :emphasis:`share\_name`\ .


  proxy_support (optional, bool, False)
    Proxy to be enabled or disabled.

    \ :emphasis:`proxy\_support`\  is considered only when \ :emphasis:`share\_name`\  is of type HTTP or HTTPS and is supported only on iDRAC9.


  proxy_type (optional, str, http)
    \ :literal:`http`\  to select HTTP type proxy.

    \ :literal:`socks4`\  to select SOCKS4 type proxy.

    \ :emphasis:`proxy\_type`\  is considered only when \ :emphasis:`share\_name`\  is of type HTTP or HTTPS and is supported only on iDRAC9.


  proxy_server (optional, str, None)
    \ :emphasis:`proxy\_server`\  is required when \ :emphasis:`share\_name`\  is of type HTTPS or HTTP and \ :emphasis:`proxy\_support`\  is \ :literal:`true`\ .

    \ :emphasis:`proxy\_server`\  is considered only when \ :emphasis:`share\_name`\  is of type HTTP or HTTPS and is supported only on iDRAC9.


  proxy_port (optional, str, 80)
    Proxy port to authenticate.

    \ :emphasis:`proxy\_port`\  is required when \ :emphasis:`share\_name`\  is of type HTTPS or HTTP and \ :emphasis:`proxy\_support`\  is \ :literal:`true`\ .

    \ :emphasis:`proxy\_port`\  is considered only when \ :emphasis:`share\_name`\  is of type HTTP or HTTPS and is supported only on iDRAC9.


  proxy_username (optional, str, None)
    Proxy username to authenticate.

    \ :emphasis:`proxy\_username`\  is considered only when \ :emphasis:`share\_name`\  is of type HTTP or HTTPS and is supported only on iDRAC9.


  proxy_password (optional, str, None)
    Proxy password to authenticate.

    \ :emphasis:`proxy\_password`\  is considered only when \ :emphasis:`share\_name`\  is of type HTTP or HTTPS and is supported only on iDRAC9.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (False, str, None)
    iDRAC username.

    If the username is not provided, then the environment variable \ :envvar:`IDRAC\_USERNAME`\  is used.

    Example: export IDRAC\_USERNAME=username


  idrac_password (False, str, None)
    iDRAC user password.

    If the password is not provided, then the environment variable \ :envvar:`IDRAC\_PASSWORD`\  is used.

    Example: export IDRAC\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`IDRAC\_X\_AUTH\_TOKEN`\  is used.

    Example: export IDRAC\_X\_AUTH\_TOKEN=x\_auth\_token


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
   - This module supports \ :literal:`check\_mode`\ .
   - To import Server Configuration Profile (SCP) on the iDRAC8-based servers, the servers must have iDRAC Enterprise license or later.
   - For \ :literal:`import`\  operation, \ :literal:`check\_mode`\  is supported only when \ :emphasis:`target`\  is \ :literal:`ALL`\ .
   - This module supports IPv4 and IPv6 addresses.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Export SCP with IDRAC components in JSON format to a local path
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        share_name: "/scp_folder"
        scp_components:
          - IDRAC
        scp_file: example_file
        export_format: JSON
        export_use: Clone
        job_wait: true

    - name: Import SCP with IDRAC components in JSON format from a local path
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        share_name: "/scp_folder"
        command: import
        scp_components:
          - IDRAC
        scp_file: example_file.json
        shutdown_type: Graceful
        end_host_power_state: "On"
        job_wait: false

    - name: Export SCP with BIOS components in XML format to a NFS share path with auto-generated file name
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        share_name: "192.168.0.2:/share"
        scp_components:
          - BIOS
        export_format: XML
        export_use: Default
        job_wait: true

    - name: Import SCP with BIOS components in XML format from a NFS share path
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        share_name: "192.168.0.2:/share"
        command: import
        scp_components:
          - BIOS
        scp_file: 192.168.0.1_20210618_162856.xml
        shutdown_type: NoReboot
        end_host_power_state: "Off"
        job_wait: false

    - name: Export SCP with RAID components in XML format to a CIFS share path with share user domain name
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        share_name: "\\\\192.168.0.2\\share"
        share_user: share_username@domain
        share_password: share_password
        scp_file: example_file.xml
        scp_components:
          - RAID
        export_format: XML
        export_use: Default
        job_wait: true

    - name: Import SCP with RAID components in XML format from a CIFS share path
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        share_name: "\\\\192.168.0.2\\share"
        share_user: share_username
        share_password: share_password
        command: import
        scp_components:
          - RAID
        scp_file: example_file.xml
        shutdown_type: Forced
        end_host_power_state: "On"
        job_wait: true

    - name: Export SCP with ALL components in JSON format to a HTTP share path
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        share_name: "http://192.168.0.3/share"
        share_user: share_username
        share_password: share_password
        scp_file: example_file.json
        scp_components:
          - ALL
        export_format: JSON
        job_wait: false

    - name: Import SCP with ALL components in JSON format from a HTTP share path
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        command: import
        share_name: "http://192.168.0.3/share"
        share_user: share_username
        share_password: share_password
        scp_file: example_file.json
        shutdown_type: Graceful
        end_host_power_state: "On"
        job_wait: true

    - name: Export SCP with ALL components in XML format to a HTTPS share path without SCP file name
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        share_name: "https://192.168.0.4/share"
        share_user: share_username
        share_password: share_password
        scp_components:
          - ALL
        export_format: XML
        export_use: Replace
        job_wait: true

    - name: Import SCP with ALL components in XML format from a HTTPS share path
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        command: import
        share_name: "https://192.168.0.4/share"
        share_user: share_username
        share_password: share_password
        scp_file: 192.168.0.1_20160618_164647.xml
        shutdown_type: Graceful
        end_host_power_state: "On"
        job_wait: false

    - name: Preview SCP with IDRAC components in XML format from a CIFS share path
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "{{ idrac_ip }}"
        idrac_user: "{{ idrac_user }}"
        idrac_password: "{{ idrac_password }}"
        ca_path: "/path/to/ca_cert.pem"
        share_name: "\\\\192.168.0.2\\share"
        share_user: share_username
        share_password: share_password
        command: preview
        scp_components:
          - ALL
        scp_file: example_file.xml
        job_wait: true

    - name: Preview SCP with IDRAC components in JSON format from a NFS share path
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "{{ idrac_ip }}"
        idrac_user: "{{ idrac_user }}"
        idrac_password: "{{ idrac_password }}"
        ca_path: "/path/to/ca_cert.pem"
        share_name: "192.168.0.2:/share"
        command: preview
        scp_components:
          - IDRAC
        scp_file: example_file.xml
        job_wait: true

    - name: Preview SCP with IDRAC components in XML format from a HTTP share path
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "{{ idrac_ip }}"
        idrac_user: "{{ idrac_user }}"
        idrac_password: "{{ idrac_password }}"
        ca_path: "/path/to/ca_cert.pem"
        share_name: "http://192.168.0.1/http-share"
        share_user: share_username
        share_password: share_password
        command: preview
        scp_components:
          - ALL
        scp_file: example_file.xml
        job_wait: true

    - name: Preview SCP with IDRAC components in XML format from a local path
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "{{ idrac_ip }}"
        idrac_user: "{{ idrac_user }}"
        idrac_password: "{{ idrac_password }}"
        ca_path: "/path/to/ca_cert.pem"
        share_name: "/scp_folder"
        command: preview
        scp_components:
          - IDRAC
        scp_file: example_file.json
        job_wait: false

    - name: Import SCP with IDRAC components in XML format from the XML content.
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "{{ idrac_ip }}"
        idrac_user: "{{ idrac_user }}"
        idrac_password: "{{ idrac_password }}"
        ca_path: "/path/to/ca_cert.pem"
        command: import
        scp_components:
          - IDRAC
        job_wait: true
        import_buffer: "<SystemConfiguration><Component FQDD='iDRAC.Embedded.1'><Attribute Name='IPMILan.1#Enable'>
          Disabled</Attribute></Component></SystemConfiguration>"

    - name: Export SCP with ALL components in XML format using HTTP proxy.
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "{{ idrac_ip }}"
        idrac_user: "{{ idrac_user }}"
        idrac_password: "{{ idrac_password }}"
        ca_path: "/path/to/ca_cert.pem"
        scp_components:
          - ALL
        share_name: "http://192.168.0.1/http-share"
        proxy_support: true
        proxy_server: 192.168.0.5
        proxy_port: 8080
        proxy_username: proxy_username
        proxy_password: proxy_password
        proxy_type: http
        include_in_export: passwordhashvalues
        job_wait: true

    - name: Import SCP with IDRAC and BIOS components in XML format using SOCKS4 proxy
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "{{ idrac_ip }}"
        idrac_user: "{{ idrac_user }}"
        idrac_password: "{{ idrac_password }}"
        ca_path: "/path/to/ca_cert.pem"
        command: import
        scp_components:
          - IDRAC
          - BIOS
        share_name: "https://192.168.0.1/http-share"
        proxy_support: true
        proxy_server: 192.168.0.6
        proxy_port: 8080
        proxy_type: socks4
        scp_file: filename.xml
        job_wait: true

    - name: Import SCP with IDRAC components in JSON format from the JSON content.
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "{{ idrac_ip }}"
        idrac_user: "{{ idrac_user }}"
        idrac_password: "{{ idrac_password }}"
        ca_path: "/path/to/ca_cert.pem"
        command: import
        scp_components:
          - IDRAC
        job_wait: true
        import_buffer: "{\"SystemConfiguration\": {\"Components\": [{\"FQDD\": \"iDRAC.Embedded.1\",\"Attributes\":
          [{\"Name\": \"SNMP.1#AgentCommunity\",\"Value\": \"public1\"}]}]}}"

    - name: Export custom default
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        job_wait: true
        share_name: "/scp_folder"
        command: export_custom_defaults
        scp_file: example_file

    - name: Import custom default
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        job_wait: true
        share_name: "/scp_folder"
        command: import_custom_defaults
        scp_file: example_file.xml

    - name: Import custom default using buffer
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        job_wait: true
        command: import_custom_defaults
        import_buffer: "<SystemConfiguration><Component FQDD='iDRAC.Embedded.1'><Attribute Name='IPMILan.1#Enable'>Disabled</Attribute>
                      </Component></SystemConfiguration>"



Return Values
-------------

msg (always, str, Successfully imported the Server Configuration Profile)
  Status of the import or export SCP job.


scp_status (success, dict, {'Id': 'JID_XXXXXXXXX', 'JobState': 'Completed', 'JobType': 'ImportConfiguration', 'Message': 'Successfully imported and applied Server Configuration Profile.', 'MessageArgs': [], 'MessageId': 'XXX123', 'Name': 'Import Configuration', 'PercentComplete': 100, 'StartTime': 'TIME_NOW', 'Status': 'Success', 'TargetSettingsURI': None, 'retval': True})
  SCP operation job and progress details from the iDRAC.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)
- Felix Stephen (@felixs88)
- Jennifer John (@Jennifer-John)
- Shivam Sharma (@ShivamSh3)
- Lovepreet Singh (@singh-lovepreet1)

