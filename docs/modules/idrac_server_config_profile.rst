.. _idrac_server_config_profile_module:


idrac_server_config_profile -- Export or Import iDRAC Server Configuration Profile (SCP)
========================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Export the Server Configuration Profile (SCP) from the iDRAC or import from a network share (CIFS, NFS, HTTP, HTTPS) or a local file.



Requirements
------------
The below requirements are needed on the host that executes this module.

- omsdk
- python >= 2.7.5



Parameters
----------

  command (optional, str, export)
    If ``import``, will perform SCP import operations.

    If ``export``, will perform SCP export operations.


  job_wait (True, bool, None)
    Whether to wait for job completion or not.


  share_name (True, str, None)
    Network share or local path.

    CIFS, NFS, HTTP, and HTTPS network share types are supported.

    OMSDK is not required if HTTP or HTTPS location is used for *share_name*.


  share_user (optional, str, None)
    Network share user in the format 'user@domain' or 'domain\\user' if user is part of a domain else 'user'. This option is mandatory for CIFS Network Share.


  share_password (optional, str, None)
    Network share user password. This option is mandatory for CIFS Network Share.


  scp_file (optional, str, None)
    Name of the server configuration profile (SCP) file.

    This option is mandatory if *command* is ``import``.

    The default format <idrac_ip>_YYmmdd_HHMMSS_scp is used if this option is not specified for ``import``.

    *export_format* is used if the valid extension file is not provided for ``import``.


  scp_components (optional, str, ALL)
    If ``ALL``, this module exports or imports all components configurations from SCP file.

    If ``IDRAC``, this module exports or imports iDRAC configuration from SCP file.

    If ``BIOS``, this module exports or imports BIOS configuration from SCP file.

    If ``NIC``, this module exports or imports NIC configuration from SCP file.

    If ``RAID``, this module exports or imports RAID configuration from SCP file.


  shutdown_type (optional, str, Graceful)
    This option is applicable for ``import`` command.

    If ``Graceful``, it gracefully shuts down the server.

    If ``Forced``,  it forcefully shuts down the server.

    If ``NoReboot``, it does not reboot the server.


  end_host_power_state (optional, str, On)
    This option is applicable for ``import`` command.

    If ``On``, End host power state is on.

    If ``Off``, End host power state is off.


  export_format (optional, str, XML)
    Specify the output file format. This option is applicable for ``export`` command.


  export_use (optional, str, Default)
    Specify the type of server configuration profile (SCP) to be exported. This option is applicable for ``export`` command.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.


  idrac_password (True, str, None)
    iDRAC user password.


  idrac_port (optional, int, 443)
    iDRAC port.





Notes
-----

.. note::
   - This module requires 'Administrator' privilege for *idrac_user*.
   - Run this module from a system that has direct access to Dell EMC iDRAC.
   - This module does not support ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Export SCP with IDRAC components in JSON format to a local path
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        share_name: "/scp_folder"
        scp_components: IDRAC
        scp_file: example_file
        export_format: JSON
        export_use: Clone
        job_wait: True

    - name: Import SCP with IDRAC components in JSON format from a local path
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        share_name: "/scp_folder"
        command: import
        scp_components: "IDRAC"
        scp_file: example_file.json
        shutdown_type: Graceful
        end_host_power_state: "On"
        job_wait: False

    - name: Export SCP with BIOS components in XML format to a NFS share path with auto-generated file name
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        share_name: "192.168.0.2:/share"
        scp_components: "BIOS"
        export_format: XML
        export_use: Default
        job_wait: True

    - name: Import SCP with BIOS components in XML format from a NFS share path
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        share_name: "192.168.0.2:/share"
        command: import
        scp_components: "BIOS"
        scp_file: 192.168.0.1_20210618_162856.xml
        shutdown_type: NoReboot
        end_host_power_state: "Off"
        job_wait: False

    - name: Export SCP with RAID components in XML format to a CIFS share path with share user domain name
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        share_name: "\\\\192.168.0.2\\share"
        share_user: share_username@domain
        share_password: share_password
        share_mnt: /mnt/cifs
        scp_file: example_file.xml
        scp_components: "RAID"
        export_format: XML
        export_use: Default
        job_wait: True

    - name: Import SCP with RAID components in XML format from a CIFS share path
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        share_name: "\\\\192.168.0.2\\share"
        share_user: share_username
        share_password: share_password
        share_mnt: /mnt/cifs
        command: import
        scp_components: "RAID"
        scp_file: example_file.xml
        shutdown_type: Forced
        end_host_power_state: "On"
        job_wait: True

    - name: Export SCP with ALL components in JSON format to a HTTP share path
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        share_name: "http://192.168.0.3/share"
        share_user: share_username
        share_password: share_password
        scp_file: example_file.json
        scp_components: ALL
        export_format: JSON
        job_wait: False

    - name: Import SCP with ALL components in JSON format from a HTTP share path
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        command: import
        share_name: "http://192.168.0.3/share"
        share_user: share_username
        share_password: share_password
        scp_file: example_file.json
        shutdown_type: Graceful
        end_host_power_state: "On"
        job_wait: True

    - name: Export SCP with ALL components in XML format to a HTTPS share path without SCP file name
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        share_name: "https://192.168.0.4/share"
        share_user: share_username
        share_password: share_password
        scp_components: ALL
        export_format: XML
        export_use: Replace
        job_wait: True

    - name: Import SCP with ALL components in XML format from a HTTPS share path
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        command: import
        share_name: "https://192.168.0.4/share"
        share_user: share_username
        share_password: share_password
        scp_file: 192.168.0.1_20160618_164647.xml
        shutdown_type: Graceful
        end_host_power_state: "On"
        job_wait: False



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

