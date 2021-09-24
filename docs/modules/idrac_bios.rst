.. _idrac_bios_module:


idrac_bios -- Configure the BIOS attributes
===========================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to configure the BIOS attributes.



Requirements
------------
The below requirements are needed on the host that executes this module.

- omsdk
- python >= 2.7.5



Parameters
----------

  share_name (optional, str, None)
    Network share or a local path.


  share_user (optional, str, None)
    Network share user name. Use the format 'user@domain' or 'domain\user' if user is part of a domain. This option is mandatory for CIFS share.


  share_password (optional, str, None)
    Network share user password. This option is mandatory for CIFS share.


  share_mnt (optional, str, None)
    Local mount path of the network share with read-write permission for ansible user. This option is mandatory for network shares.


  boot_mode (optional, str, None)
    (deprecated)Sets boot mode to BIOS or UEFI.

    This option is deprecated, and will be removed in later version. Use *attributes* for configuring the BIOS attributes.

    *boot_mode* is mutually exclusive with *boot_sources*.


  nvme_mode (optional, str, None)
    (deprecated)Configures the NVME mode in the iDRAC 9 based PowerEdge Servers.

    This option is deprecated, and will be removed in later version. Use *attributes* for configuring the BIOS attributes.

    *nvme_mode* is mutually exclusive with *boot_sources*.


  secure_boot_mode (optional, str, None)
    (deprecated)Configures how the BIOS uses the Secure Boot Policy Objects in iDRAC 9 based PowerEdge Servers.

    This option is deprecated, and will be removed in later version. Use *attributes* for configuring the BIOS attributes.

    *secure_boot_mode* is mutually exclusive with *boot_sources*.


  onetime_boot_mode (optional, str, None)
    (deprecated)Configures the one time boot mode setting.

    This option is deprecated, and will be removed in later version. Use *attributes* for configuring the BIOS attributes.

    *onetime_boot_mode* is mutually exclusive with *boot_sources*.


  boot_sequence (optional, str, None)
    (deprecated)Allows to set the boot sequence in  BIOS boot mode or Secure UEFI boot mode by rearranging the boot entries in Fully Qualified Device Descriptor (FQDD).

    TThis option is deprecated, and will be removed in later version. Use *attributes* for configuring the BIOS attributes.

    *boot_sequence* is mutually exclusive with *boot_sources*.


  attributes (optional, dict, None)
    Dictionary of BIOS attributes and value pair. Attributes should be part of the Redfish Dell BIOS Attribute Registry. Use https://*idrac_ip*/redfish/v1/Systems/System.Embedded.1/Bios to view the Redfish URI.

    If deprecated options are provided and the same is repeated in *attributes* then values in *attributes* will take precedence.

    *attributes* is mutually exclusive with *boot_sources*.


  boot_sources (optional, list, None)
    List of boot devices to set the boot sources settings.

    *boot_sources* is mutually exclusive with *attributes*, *boot_sequence*, *onetime_boot_mode*, *secure_boot_mode*, *nvme_mode*, *boot_mode*.


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
   - Run this module from a system that has direct access to DellEMC iDRAC.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Configure generic attributes of the BIOS
      dellemc.openmanage.idrac_bios:
        idrac_ip:   "192.168.0.1"
        idrac_user: "user_name"
        idrac_password:  "user_password"
        attributes:
          BootMode : "Bios"
          OneTimeBootMode: "Enabled"
          BootSeqRetry: "Enabled"

    - name: Configure PXE generic attributes
      dellemc.openmanage.idrac_bios:
        idrac_ip:   "192.168.0.1"
        idrac_user: "user_name"
        idrac_password:  "user_password"
        attributes:
          PxeDev1EnDis: "Enabled"
          PxeDev1Protocol: "IPV4"
          PxeDev1VlanEnDis: "Enabled"
          PxeDev1VlanId: 1
          PxeDev1Interface: "NIC.Embedded.1-1-1"
          PxeDev1VlanPriority: 2

    - name: Configure boot sources
      dellemc.openmanage.idrac_bios:
        idrac_ip:   "192.168.0.1"
        idrac_user: "user_name"
        idrac_password:  "user_password"
        boot_sources:
          - Name : "NIC.Integrated.1-2-3"
            Enabled : true
            Index : 0

    - name: Configure multiple boot sources
      dellemc.openmanage.idrac_bios:
        idrac_ip:   "192.168.0.1"
        idrac_user: "user_name"
        idrac_password:  "user_password"
        boot_sources:
          - Name : "NIC.Integrated.1-1-1"
            Enabled : true
            Index : 0
          - Name : "NIC.Integrated.2-2-2"
            Enabled : true
            Index : 1
          - Name : "NIC.Integrated.3-3-3"
            Enabled : true
            Index : 2

    - name: Configure boot sources - Enabling
      dellemc.openmanage.idrac_bios:
        idrac_ip:   "192.168.0.1"
        idrac_user: "user_name"
        idrac_password:  "user_password"
        boot_sources:
          - Name : "NIC.Integrated.1-1-1"
            Enabled : true

    - name: Configure boot sources - Index
      dellemc.openmanage.idrac_bios:
        idrac_ip:   "192.168.0.1"
        idrac_user: "user_name"
        idrac_password:  "user_password"
        boot_sources:
          - Name : "NIC.Integrated.1-1-1"
            Index : 0



Return Values
-------------

msg (success, dict, {'@odata.context': '/redfish/v1/$metadata#DellJob.DellJob', '@odata.id': '/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_873888162305', '@odata.type': '#DellJob.v1_0_0.DellJob', 'CompletionTime': '2020-04-20T18:50:20', 'Description': 'Job Instance', 'EndTime': None, 'Id': 'JID_873888162305', 'JobState': 'Completed', 'JobType': 'ImportConfiguration', 'Message': 'Successfully imported and applied Server Configuration Profile.', 'MessageArgs': [], 'MessageId': 'SYS053', 'Name': 'Import Configuration', 'PercentComplete': 100, 'StartTime': 'TIME_NOW', 'Status': 'Success', 'TargetSettingsURI': None, 'retval': True})
  Configures the BIOS configuration attributes.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)
- Anooja Vardhineni (@anooja-vardhineni)

