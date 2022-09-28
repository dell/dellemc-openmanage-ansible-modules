.. _idrac_boot_module:


idrac_boot -- Configure the boot order settings.
================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to configure the boot order settings.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  boot_options (optional, list, None)
    Options to enable or disable the boot devices.

    This is mutually exclusive with *boot_order*, *boot_source_override_mode*, *boot_source_override_enabled* *boot_source_override_target*, and *uefi_target_boot_source_override*.


    boot_option_reference (optional, str, None)
      FQDD of the boot device.

      This is mutually exclusive with *display_name*.


    display_name (optional, str, None)
      Display name of the boot source device.

      This is mutually exclusive with *boot_option_reference*.


    enabled (True, bool, None)
      Enable or disable the boot device.



  boot_order (optional, list, None)
    This option allows to set the boot devices in the required boot order sequences.

    This is mutually exclusive with *boot_options*.


  boot_source_override_mode (optional, str, None)
    The BIOS boot mode (either Legacy or UEFI) to be used when *boot_source_override_target* boot source is booted from.

    ``legacy`` The system boot in non-UEF*Legacy* boot mode to the *boot_source_override_target*.

    ``uefi`` The system boot in UEFI boot mode to the *boot_source_override_target*.

    This is mutually exclusive with *boot_options*.


  boot_source_override_enabled (optional, str, None)
    The state of the Boot Source Override feature.

    ``disabled`` The system boots normally.

    ``once`` The system boots (one time) to the *boot_source_override_target*.

    ``continuous`` The system boots to the target specified in the *boot_source_override_target* until this property is set to Disabled.

    The state is set to ``once`` for the one-time boot override and ``continuous`` for the remain-active-until—canceled override. If the state is set ``once``, the value is reset to ``disabled`` after the *boot_source_override_target* actions have completed successfully.

    Changes to this options do not alter the BIOS persistent boot order configuration.

    This is mutually exclusive with *boot_options*.


  boot_source_override_target (optional, str, None)
    The boot source override target device to use during the next boot instead of the normal boot device.

    ``pxe`` performs PXE boot from the primary NIC.

    ``floppy``, ``cd``, ``hdd``, ``sd_card`` performs boot from their devices respectively.

    ``bios_setup`` performs boot into the native BIOS setup.

    ``utilities`` performs boot from the local utilities.

    ``uefi_target`` performs boot from the UEFI device path found in *uefi_target_boot_source_override*.

    If the *boot_source_override_target* is set to a value other than ``none`` then the *boot_source_override_enabled* is automatically set to ``once``.

    Changes to this options do not alter the BIOS persistent boot order configuration.

    This is mutually exclusive with *boot_options*.


  uefi_target_boot_source_override (optional, str, None)
    The UEFI device path of the device from which to boot when *boot_source_override_target* is ``uefi_target``.

    *boot_source_override_enabled* cannot be set to c(continuous) if *boot_source_override_target* set to ``uefi_target`` because this settings is defined in UEFI as a one-time-boot setting.

    Changes to this options do not alter the BIOS persistent boot order configuration.

    This is required if *boot_source_override_target* is ``uefi_target``.

    This is mutually exclusive with *boot_options*.


  reset_type (optional, str, graceful_restart)
    ``none`` Host system is not rebooted and *job_wait* is not applicable.

    ``force_reset`` Forcefully reboot the Host system.

    ``graceful_reset`` Gracefully reboot the Host system.


  job_wait (optional, bool, True)
    Provides the option to wait for job completion.

    This is applicable when *reset_type* is ``force_reset`` or ``graceful_reset``.


  job_wait_timeout (optional, int, 900)
    The maximum wait time of *job_wait* in seconds. The job is tracked only for this duration.

    This option is applicable when *job_wait* is ``True``.


  resource_id (optional, str, None)
    Redfish ID of the resource.


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





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Configure the system boot options settings.
      dellemc.openmanage.idrac_boot:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        boot_options:
          - display_name: Hard drive C
            enabled: true
          - boot_option_reference: NIC.PxeDevice.2-1
            enabled: true

    - name: Configure the boot order settings.
      dellemc.openmanage.idrac_boot:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        boot_order:
          - Boot0001
          - Boot0002
          - Boot0004
          - Boot0003

    - name: Configure the boot source override mode.
      dellemc.openmanage.idrac_boot:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        boot_source_override_mode: legacy
        boot_source_override_target: cd
        boot_source_override_enabled: once

    - name: Configure the UEFI target settings.
      dellemc.openmanage.idrac_boot:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        boot_source_override_mode: uefi
        boot_source_override_target: uefi_target
        uefi_target_boot_source_override: "VenHw(3A191845-5F86-4E78-8FCE-C4CFF59F9DAA)"

    - name: Configure the boot source override mode as pxe.
      dellemc.openmanage.idrac_boot:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        boot_source_override_mode: legacy
        boot_source_override_target: pxe
        boot_source_override_enabled: continuous



Return Values
-------------

msg (success, str, Successfully updated the boot settings.)
  Successfully updated the boot settings.


job (success, dict, {'ActualRunningStartTime': '2019-06-19T00:57:24', 'ActualRunningStopTime': '2019-06-19T01:00:27', 'CompletionTime': '2019-06-19T01:00:27', 'Description': 'Job Instance', 'EndTime': 'TIME_NA', 'Id': 'JID_609237056489', 'JobState': 'Completed', 'JobType': 'BIOSConfiguration', 'Message': 'Job completed successfully.', 'MessageArgs': [], 'MessageId': 'PR19', 'Name': 'Configure: BIOS.Setup.1-1', 'PercentComplete': 100, 'StartTime': '2019-06-19T00:55:05', 'TargetSettingsURI': None})
  Configured job details.


boot (success, dict, {'BootOptions': {'Description': 'Collection of BootOptions', 'Members': [{'BootOptionEnabled': False, 'BootOptionReference': 'HardDisk.List.1-1', 'Description': 'Current settings of the Legacy Boot option', 'DisplayName': 'Hard drive C:', 'Id': 'HardDisk.List.1-1', 'Name': 'Legacy Boot option', 'UefiDevicePath': 'VenHw(D6C0639F-C705-4EB9-AA4F-5802D8823DE6)'}], 'Name': 'Boot Options Collection'}, 'BootOrder': ['HardDisk.List.1-1'], 'BootSourceOverrideEnabled': 'Disabled', 'BootSourceOverrideMode': 'Legacy', 'BootSourceOverrideTarget': 'None', 'UefiTargetBootSourceOverride': None})
  Configured boot settings details.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)

