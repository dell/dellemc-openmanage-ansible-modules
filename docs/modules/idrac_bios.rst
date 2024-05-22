.. _idrac_bios_module:


idrac_bios -- Modify and clear BIOS attributes, reset BIOS settings and configure boot sources
==============================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to modify the BIOS attributes. Also clears pending BIOS attributes and resets BIOS to default settings.

Boot sources can be enabled or disabled. Boot sequence can be configured.



Requirements
------------
The below requirements are needed on the host that executes this module.

- omsdk \>= 1.2.490
- python \>= 3.9.6



Parameters
----------

  share_name (optional, str, None)
    (deprecated)Network share or a local path.


  share_user (optional, str, None)
    (deprecated)Network share user name. Use the format 'user@domain' or domain//user if user is part of a domain. This option is mandatory for CIFS share.


  share_password (optional, str, None)
    (deprecated)Network share user password. This option is mandatory for CIFS share.


  share_mnt (optional, str, None)
    (deprecated)Local mount path of the network share with read-write permission for ansible user. This option is mandatory for network shares.


  apply_time (optional, str, Immediate)
    Apply time of the \ :emphasis:`attributes`\ .

    This is applicable only to \ :emphasis:`attributes`\ .

    \ :literal:`Immediate`\  Allows the user to immediately reboot the host and apply the changes. \ :emphasis:`job\_wait`\  is applicable.

    \ :literal:`OnReset`\  Allows the user to apply the changes on the next reboot of the host server.

    \ :literal:`AtMaintenanceWindowStart`\  Allows the user to apply at the start of a maintenance window as specified in \ :emphasis:`maintenance\_window`\ . A reboot job will be scheduled.

    \ :literal:`InMaintenanceWindowOnReset`\  Allows to apply after a manual reset but within the maintenance window as specified in \ :emphasis:`maintenance\_window`\ .


  maintenance_window (optional, dict, None)
    Option to schedule the maintenance window.

    This is required when \ :emphasis:`apply\_time`\  is \ :literal:`AtMaintenanceWindowStart`\  or \ :literal:`InMaintenanceWindowOnReset`\ .


    start_time (True, str, None)
      The start time for the maintenance window to be scheduled.

      The format is YYYY-MM-DDThh:mm:ss\<offset\>

      \<offset\> is the time offset from UTC that the current timezone set in iDRAC in the format: +05:30 for IST.


    duration (True, int, None)
      The duration in seconds for the maintenance window.



  attributes (optional, dict, None)
    Dictionary of BIOS attributes and value pair. Attributes should be part of the Redfish Dell BIOS Attribute Registry. Use \ https://I(idrac_ip\ /redfish/v1/Systems/System.Embedded.1/Bios) to view the Redfish URI.

    This is mutually exclusive with \ :emphasis:`boot\_sources`\ , \ :emphasis:`clear\_pending`\ , and \ :emphasis:`reset\_bios`\ .


  boot_sources (optional, list, None)
    (deprecated)List of boot devices to set the boot sources settings.

    \ :emphasis:`boot\_sources`\  is mutually exclusive with \ :emphasis:`attributes`\ , \ :emphasis:`clear\_pending`\ , and \ :emphasis:`reset\_bios`\ .

    \ :emphasis:`job\_wait`\  is not applicable. The module waits till the completion of this task.

    This feature is deprecated, please use \ :ref:`dellemc.openmanage.idrac\_boot <ansible_collections.dellemc.openmanage.idrac_boot_module>`\  for configuring boot sources.


  clear_pending (optional, bool, None)
    Allows the user to clear all pending BIOS attributes changes.

    \ :literal:`true`\  will discard any pending changes to bios attributes or remove job if in scheduled state.

    This operation will not create any job.

    \ :literal:`false`\  will not perform any operation.

    This is mutually exclusive with \ :emphasis:`boot\_sources`\ , \ :emphasis:`attributes`\ , and \ :emphasis:`reset\_bios`\ .

    \ :literal:`Note`\  Any BIOS job scheduled due to boot sources configuration will not be cleared.


  reset_bios (optional, bool, None)
    Resets the BIOS to default settings and triggers a reboot of host system.

    This is applied to the host after the restart.

    This operation will not create any job.

    \ :literal:`false`\  will not perform any operation.

    This is mutually exclusive with \ :emphasis:`boot\_sources`\ , \ :emphasis:`attributes`\ , and \ :emphasis:`clear\_pending`\ .

    When \ :literal:`true`\ , this action will always report as changes found to be applicable.


  reset_type (optional, str, graceful_restart)
    \ :literal:`force\_restart`\  Forcefully reboot the host system.

    \ :literal:`graceful\_restart`\  Gracefully reboot the host system.

    This is applicable for \ :emphasis:`reset\_bios`\ , and \ :emphasis:`attributes`\  when \ :emphasis:`apply\_time`\  is \ :literal:`Immediate`\ .


  job_wait (optional, bool, True)
    Provides the option to wait for job completion.

    This is applicable for \ :emphasis:`attributes`\  when \ :emphasis:`apply\_time`\  is \ :literal:`Immediate`\ .


  job_wait_timeout (optional, int, 1200)
    The maximum wait time of \ :emphasis:`job\_wait`\  in seconds. The job is tracked only for this duration.

    This option is applicable when \ :emphasis:`job\_wait`\  is \ :literal:`true`\ .


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
   - omsdk is required to be installed only for \ :emphasis:`boot\_sources`\  operation.
   - This module requires 'Administrator' privilege for \ :emphasis:`idrac\_user`\ .
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports both IPv4 and IPv6 address for \ :emphasis:`idrac\_ip`\ .
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Configure generic attributes of the BIOS
      dellemc.openmanage.idrac_bios:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        attributes:
          BootMode: "Bios"
          OneTimeBootMode: "Enabled"
          BootSeqRetry: "Enabled"

    - name: Configure PXE generic attributes
      dellemc.openmanage.idrac_bios:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        attributes:
          PxeDev1EnDis: "Enabled"
          PxeDev1Protocol: "IPV4"
          PxeDev1VlanEnDis: "Enabled"
          PxeDev1VlanId: 1
          PxeDev1Interface: "NIC.Embedded.1-1-1"
          PxeDev1VlanPriority: 2

    - name: Configure BIOS attributes at Maintenance window
      dellemc.openmanage.idrac_bios:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        apply_time: AtMaintenanceWindowStart
        maintenance_window:
          start_time: "2022-09-30T05:15:40-05:00"
          duration: 600
        attributes:
          BootMode: "Bios"
          OneTimeBootMode: "Enabled"
          BootSeqRetry: "Enabled"

    - name: Clear pending BIOS attributes
      dellemc.openmanage.idrac_bios:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        clear_pending: true

    - name: Reset BIOS attributes to default settings.
      dellemc.openmanage.idrac_bios:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        validate_certs: false
        reset_bios: true

    - name: Configure boot sources
      dellemc.openmanage.idrac_bios:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        boot_sources:
          - Name: "NIC.Integrated.1-2-3"
            Enabled: true
            Index: 0

    - name: Configure multiple boot sources
      dellemc.openmanage.idrac_bios:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        boot_sources:
          - Name: "NIC.Integrated.1-1-1"
            Enabled: true
            Index: 0
          - Name: "NIC.Integrated.2-2-2"
            Enabled: true
            Index: 1
          - Name: "NIC.Integrated.3-3-3"
            Enabled: true
            Index: 2

    - name: Configure boot sources - Enabling
      dellemc.openmanage.idrac_bios:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        boot_sources:
          - Name: "NIC.Integrated.1-1-1"
            Enabled: true

    - name: Configure boot sources - Index
      dellemc.openmanage.idrac_bios:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        boot_sources:
          - Name: "NIC.Integrated.1-1-1"
            Index: 0



Return Values
-------------

status_msg (success, str, Successfully cleared pending BIOS attributes.)
  Overall status of the bios operation.


msg (success, dict, {'CompletionTime': '2020-04-20T18:50:20', 'Description': 'Job Instance', 'EndTime': None, 'Id': 'JID_873888162305', 'JobState': 'Completed', 'JobType': 'ImportConfiguration', 'Message': 'Successfully imported and applied Server Configuration Profile.', 'MessageArgs': [], 'MessageId': 'SYS053', 'Name': 'Import Configuration', 'PercentComplete': 100, 'StartTime': 'TIME_NOW', 'Status': 'Success', 'TargetSettingsURI': None, 'retval': True})
  Status of the job for \ :emphasis:`boot\_sources`\  or status of the action performed on bios.


invalid_attributes (on invalid attributes or values., dict, {'PxeDev1VlanId': 'Not a valid integer.', 'AcPwrRcvryUserDelay': 'Integer out of valid range.', 'BootSeqRetry': 'Invalid value for Enumeration.', 'Proc1Brand': 'Read only Attribute cannot be modified.', 'AssetTag': 'Attribute does not exist.'})
  Dict of invalid attributes provided.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)
- Anooja Vardhineni (@anooja-vardhineni)
- Jagadeesh N V (@jagadeeshnv)
- Shivam Sharma (@shivam-sharma)

