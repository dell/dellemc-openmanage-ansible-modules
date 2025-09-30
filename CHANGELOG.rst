=============================================
Dell OpenManage Ansible Modules Release Notes
=============================================

.. contents:: Topics

v10.0.1
=======

Release Summary
---------------

'The OpenManage Enterprise, OpenManage Enterprise Modular and OpenManage Enterprise Integration for VMware vCenter modules are now compatible with Ansible Core version 2.19.'

Major Changes
-------------

- The OpenManage Enterprise, OpenManage Enterprise Modular and OpenManage Enterprise Integration for VMware vCenter modules are now compatible with Ansible Core version 2.19..

Minor Changes
-------------

- idrac_support_assist - Introduced aliases for the module parameters share_username and share_password to align with the naming conventions used across other modules, ensuring consistency and improving usability.

Bugfixes
--------

- idrac_system_info - (Issue 1017) - System info not being returned on gen17s with v10.0.0 (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/1017)
- redfish_storage_volume - (Issue 1027) Module fails on force reboot. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/1027)
- idrac_support_assist - Updated module playbook examples to use the correct casing for protocol names, for CIFS and HTTPS.
- Fixed the UT test execution through ansible-test - (Issue 1003) - Tests Pass Using Tox But Not Ansible-Test (https://github.com/dell/dellemc-openmanage-ansible-modules)

Known Issues
------------

- idrac_diagnostics - This module does not support export of diagnostics file to HTTP and HTTPS share via SOCKS proxy.
- idrac_license - The module will give different error messages for iDRAC9 and iDRAC10 when user imports license with invalid share name.
- idrac_license - Due to API limitation, proxy parameters are ignored during the import operation.
- idrac_os_deployment - The module continues to return a 200 response and marks the job as completed, even when an outdated date is supplied in the Expose duration.
- idrac_redfish_storage_controller - PatrolReadRatePercent attribute cannot be set in iDRAC10.
- idrac_server_config_profile - When attempting to revert iDRAC settings using a previously exported SCP file, the import operation will complete with errors if a new user was created after the export (Instead of restoring the system to its previous state, including the removal of newly added users).
- idrac_system_info - The module will show empty video list despite having Embedded VIDEO controller.
- Redfish_storage_volume - Encryption type and block_io_size bytes will be read only property in iDRAC 9 and iDRAC 10 and hence the module ignores these parameters.
- ome_smart_fabric_uplink - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.
- ome_smart_fabric_info - Formal qualification of module for Ansible Core version 2.19 is still pending.

v10.0.0
=======

Release Summary
---------------

'The ``idrac_license``, ``idrac_os_deployment``, ``idrac_redfish_storage_controller``, ``idrac_server_config_profile``, ``idrac_storage_volume``, ``redfish_firmware_rollback``, ``redfish_storage_volume`` modules and ``idrac_certificate``, ``idrac_export_server_config_profile``, ``idrac_firmware``, ``idrac_import_server_config_profile``, ``idrac_os_deployment``, ``idrac_storage_controller``, ``redfish_firmware``, ``redfish_storage_volume`` roles are enhanced to support iDRAC10.'

Major Changes
-------------

- idrac_license - This module is enhanced to support iDRAC10.
- idrac_os_deployment - This module is enhanced to support iDRAC10.
- idrac_redfish_storage_controller - This module is enhanced to support iDRAC10.
- idrac_server_config_profile - This module is enhanced to support iDRAC10.
- idrac_storage_volume - This module is enhanced to support iDRAC10.
- redfish_firmware_rollback - This module is enhanced to support iDRAC10.
- redfish_storage_volume - This module is enhanced to support iDRAC10.
- idrac_certificate - This role is enhanced to support iDRAC10.
- idrac_export_server_config_profile - This role is enhanced to support iDRAC10.
- idrac_firmware - This role is enhanced to support iDRAC10.
- idrac_import_server_config_profile - This role is enhanced to support iDRAC10.
- idrac_os_deployment - This role is enhanced to support iDRAC10.
- idrac_storage_controller - This role is enhanced to support iDRAC10.
- redfish_firmware - This role is enhanced to support iDRAC10.
- redfish_storage_volume - This role is enhanced to support iDRAC10.

Bugfixes
--------

- idrac_system_info - (Issue 967) - idrac_system_info fails oniDRAC10 with GPU. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/967)
- idrac_server_config_profile - (Issue 959) Can't export SCP (Server configuration profile) on iDRAC 10. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/959)

Known Issues
------------

- idrac_attributes - The module accepts both the string as well as integer value for the field "SNMP.1.AgentCommunity" for iDRAC10.
- idrac_diagnostics - This module does not support export of diagnostics file to HTTP and HTTPS share via SOCKS proxy.
- idrac_license - The module will fail to export license to NFS Share.
- idrac_license - The module will give different error messages for iDRAC9 and iDRAC10 when user imports license with invalid share name.
- idrac_license - Due to API limitation, proxy parameters are ignored during the import operation.
- idrac_os_deployment - The module continues to return a 200 response and marks the job as completed, even when an outdated date is supplied in the Expose duration.
- idrac_redfish_storage_controller - PatrolReadRatePercent attribute cannot be set in iDRAC10.
- idrac_server_config_profile - When attempting to revert iDRAC settings using a previously exported SCP file, the import operation will complete with errors if a new user was created after the export (Instead of restoring the system to its previous state, including the removal of newly added users).
- idrac_system_info - The module will show empty video list despite having Embedded VIDEO controller.
- Redfish_storage_volume - Encryption type and block_io_size bytes will be read only property in iDRAC 9 and iDRAC 10 and hence the module ignores these parameters.
- ome_smart_fabric_uplink - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.

v9.12.3
=======

Release Summary
---------------

The ``idrac_boot``,``idrac_certificates`` ``idrac_reset``, ``idrac_support_assist``, ``idrac_user``, ``redfish_firmware`` modules and ``idrac_bios``, ``idrac_boot``, ``idrac_reset``, ``idrac_user`` roles are enhanced to support iDRAC10. Furthermore, the ``ome_firmware``, ``ome_firmware_baseline``, ``ome_firmware_catalog``, ``ome_firmware_baseline_compliance_info``, and ``ome_firmware_baseline_info`` modules now support OME 4.5. OpenManage iDRAC Ansible modules are now compatible with Ansible Core version 2.19.

Major Changes
-------------

- idrac_boot - This module is enhanced to support iDRAC10.
- idrac_certificates - This module is enhanced to support iDRAC10.
- idrac_reset - This module is enhanced to support iDRAC10.
- idrac_support_assist - This module is enhanced to support iDRAC10.
- idrac_user - This module is enhanced to support iDRAC10.
- redfish_firmware - This module is enhanced to support iDRAC10.
- idrac_bios - This role is enhanced to support iDRAC10.
- idrac_boot - This role is enhanced to support iDRAC10.
- idrac_reset - This role is enhanced to support iDRAC10.
- idrac_user - This role is enhanced to support iDRAC10.
- ome_firmware - This module is enhanced to support OME 4.5.
- ome_firmware_baseline - This module is enhanced to support OME 4.5.
- ome_firmware_catalog - This module is enhanced to support OME 4.5.
- ome_firmware_baseline_info - This module is enhanced to support OME 4.5.
- ome_firmware_baseline_compliance_info - This module is enhanced to support OME 4.5.
- OpenManage iDRAC Ansible modules are now compatible with Ansible Core version 2.19.

Known Issues
------------

- idrac_attributes - The module accepts both the string as well as integer value for the field "SNMP.1.AgentCommunity" for iDRAC10.
- idrac_diagnostics - This module does not support export of diagnostics file to HTTP and HTTPS share via SOCKS proxy.
- ome_smart_fabric_uplink - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.

v9.12.2
=======

Release Summary
---------------

The ``idrac_bios``, ``idrac_diagnostics``, ``idrac_session``, ``idrac_firmware``, ``idrac_secure_boot``, ``idrac_system_erase``, ``idrac_network_attributes``, ``idrac_lifecycle_controller_logs``, ``redfish_power_state``, ``redfish_event_subscription`` modules and ``idrac_server_powerstate``, ``idrac_job_queue`` roles are enhanced to support iDRAC10.

Major Changes
-------------

- idrac_bios - This module is enhanced to support iDRAC10.
- idrac_diagnostics - This module is enhanced to support iDRAC10.
- idrac_firmware - This module is enhanced to support iDRAC10.
- idrac_job_queue - This role is enhanced to support iDRAC10.
- idrac_lifecycle_controller_logs - This module is enhanced to support iDRAC10.
- idrac_network_attributes - This module is enhanced to support iDRAC10.
- idrac_secure_boot - This module is enhanced to support iDRAC10.
- idrac_server_powerstate - This role is enhanced to support iDRAC10.
- idrac_session - This module is enhanced to support iDRAC10.
- idrac_system_erase - This module is enhanced to support iDRAC10.
- redfish_event_subscription - This module is enhanced to support iDRAC10.
- redfish_power_state - This module is enhanced to support iDRAC10.

Known Issues
------------

- idrac_attributes - The module accepts both the string as well as integer value for the field "SNMP.1.AgentCommunity" for iDRAC10.
- idrac_diagnostics - This module doesn't support export of diagnostics file to HTTP and HTTPS share via SOCKS proxy.
- ome_smart_fabric_uplink - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.

v9.12.1
=======

Release Summary
---------------

- The ``idrac_user_info`` module is enhanced to support iDRAC10. - The ``idrac_lifecycle_controller_status_info`` module is enhanced to support iDRAC10. - The ``idrac_lifecycle_controller_jobs`` module is enhanced to support iDRAC10. - The ``idrac_virtual_media`` module is enhanced to support iDRAC10. - The ``idrac_attributes`` module is enhanced to support iDRAC10. - The ``idrac_attributes`` role is enhanced to support iDRAC10. - The ``idrac_syslog`` module is deprecated.

Major Changes
-------------

- idrac_attributes - This module is enhanced to support iDRAC10.
- idrac_attributes - This role is enhanced to support iDRAC10.
- idrac_lifecycle_controller_jobs - This module is enhanced to support iDRAC10.
- idrac_lifecycle_controller_status_info - This module is enhanced to support iDRAC10.
- idrac_syslog - This module is deprecated.
- idrac_user_info - This module is enhanced to support iDRAC10.
- idrac_virtual_media - This module is enhanced to support iDRAC10.

Known Issues
------------

- idrac_diagnostics - Issue(285322) - This module doesn't support export of diagnostics file to HTTP and HTTPS share via SOCKS proxy.
- idrac_firmware - Issue(279282) - This module does not support firmware update using HTTP, HTTPS, and FTP shares with authentication on iDRAC8.
- ome_smart_fabric_uplink - Issue(186024) - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.

v9.12.0
=======

Release Summary
---------------

- The ``idrac_system_info`` module is enhanced to support iDRAC10. - The ``idrac_lifecycle_controller_job_status_info`` module is enhanced to support iDRAC10. - The ``idrac_gather_facts`` role is enhanced to support iDRAC10.

Major Changes
-------------

- idrac_gather_facts - This role is enhanced to support iDRAC10.
- idrac_lifecycle_controller_job_status_info - This module is enhanced to support iDRAC10.
- idrac_system_info - This module is enhanced to support iDRAC10.

Bugfixes
--------

- idrac_system_info - (Issue 812) - idrac_system_info fails on iDRAC10.

Known Issues
------------

- idrac_diagnostics - Issue(285322) - This module doesn't support export of diagnostics file to HTTP and HTTPS share via SOCKS proxy.
- idrac_firmware - Issue(279282) - This module does not support firmware update using HTTP, HTTPS, and FTP shares with authentication on iDRAC8.
- ome_smart_fabric_uplink - Issue(186024) - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.

v9.11.0
=======

Release Summary
---------------

- The modules ``idrac_network_attributes``, ``idrac_certificates``, ``idrac_redfish_storage_controller``, ``idrac_boot`` and ``idrac_firmware`` have been enhanced to resolve all internal defects. - The ``idrac_redfish_storage_volume`` module is enhanced to prevent a 404 error during job creation when enabling encryption for virtual drives.

Bugfixes
--------

- Internal defect fixes were done for the following modules - ``idrac_network_attributes``, ``idrac_certificates``, ``idrac_redfish_storage_controller``, ``idrac_boot_order`` and ``idrac_firmware``
- Resolved the issue in ``idrac_redfish_storage_volume`` module where it returns 404 error on job creation when enabling encryption for virtual drives. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues /713)

Known Issues
------------

- idrac_diagnostics - Issue(285322) - This module doesn't support export of diagnostics file to HTTP and HTTPS share via SOCKS proxy.
- idrac_firmware - Issue(279282) - This module does not support firmware update using HTTP, HTTPS, and FTP shares with authentication on iDRAC8.
- ome_smart_fabric_uplink - Issue(186024) - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.

v9.10.0
=======

Release Summary
---------------

- The ``omevv_firmware`` module is added to support the firmware update of the single host and single cluster. - The ``omevv_firmware_repository_profile`` module is enhanced to support resync of repository profiles from the OpenManage Update Manager Plug-in. - The ``idrac_certificates`` module is enhanced to support SSL CSR generation for 4096 key size.

Major Changes
-------------

- omevv_firmware - This module allows to update firmware of the single host and single cluster.

Minor Changes
-------------

- idrac_certificates -  This module is enhanced to support SSL CSR generation for 4096 key size.
- omevv_firmware_repository_profile - This module allows to resync the repository profiles from the OpenManage Update Manager Plug-in.

Bugfixes
--------

- idrac_certificates - (Issue 737) - Fixed SSL CSR generation for 4096 key size.

Known Issues
------------

- idrac_diagnostics - Issue(285322) - This module doesn't support export of diagnostics file to HTTP and HTTPS share via SOCKS proxy.
- idrac_firmware - Issue(279282) - This module does not support firmware update using HTTP, HTTPS, and FTP shares with authentication on iDRAC8.
- ome_smart_fabric_uplink - Issue(186024) - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.

v9.9.0
======

Release Summary
---------------

- Modules are added to support OpenManage Enterprise Integration for VMWare vCenter Plug-in. - The ``omevv_baseline_profile_info`` module is added to support retrieval of baseline profile information. - The ``omevv_compliance_info`` module is added to support retrieval of firmware compliance reports. - The ``omevv_baseline_profile`` module is added to support management of baseline profile.

Major Changes
-------------

- omevv_baseline_profile - This module allows to manage baseline profile.
- omevv_baseline_profile_info - This module allows to retrieve baseline profile information.
- omevv_compliance_info - This module allows to retrieve firmware compliance reports.

Known Issues
------------

- idrac_diagnostics - Issue(285322) - This module doesn't support export of diagnostics file to HTTP and HTTPS share via SOCKS proxy.
- idrac_firmware - Issue(279282) - This module does not support firmware update using HTTP, HTTPS, and FTP shares with authentication on iDRAC8.
- ome_smart_fabric_uplink - Issue(186024) - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.

v9.8.0
======

Release Summary
---------------

- Modules are added to support OpenManage Enterprise Integration for VMWare vCenter Plug-in. - The ``omevv_vcenter_info`` module is added to support retrieval of vCenter information. - The ``omevv_firmware_repository_profile_info`` module is added to support retrieval of firmware repository profile information. - The ``omevv_firmware_repository_profile`` module is added to support management of firmware repository profile. - The ``idrac_firmware_info`` module is enhanced to support iDRAC10.

Major Changes
-------------

- omevv_firmware_repository_profile - This module allows to manage firmware repository profile.
- omevv_firmware_repository_profile_info - This module allows to retrieve firmware repository profile information.
- omevv_vcenter_info - This module allows to retrieve vCenter information.

Minor Changes
-------------

- idrac_firmware_info - This module is enhanced to support iDRAC10.

Bugfixes
--------

- idrac_storage_volume - Issue(290766) - The module will report success instead of showing failure for new virtual creation on the BOSS-N1 controller if a virtual disk is already present on the same controller.
- idrac_support_assist - Issue(308550) - This module fails when the NFS share path contains sub directory.
- ome_diagnostics - Issue(279193) - Export of SupportAssist collection logs to the share location fails on OME version 4.0.0.

Known Issues
------------

- idrac_diagnostics - Issue(285322) - This module doesn't support export of diagnostics file to HTTP and HTTPS share via SOCKS proxy.
- idrac_firmware - Issue(279282) - This module does not support firmware update using HTTP, HTTPS, and FTP shares with authentication on iDRAC8.
- ome_smart_fabric_uplink - Issue(186024) - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.

v9.7.0
======

Release Summary
---------------

- The ``idrac_secure_boot`` module is enhanced to export, reset and configure the attributes of boot certificate. - The ``idrac_system_erase`` module is added to add support to erase system and storage components of the server.

Major Changes
-------------

- idrac_secure_boot - This module allows to Configure attributes, import, or export secure boot certificate, and reset keys.
- idrac_system_erase - This module allows to Erase system and storage components of the server on iDRAC.

Bugfixes
--------

- Resolved the issue in ``idrac_gather_facts`` role where it was failing for some component in iDRAC8. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/718)

Known Issues
------------

- idrac_diagnostics - Issue(285322) - This module doesn't support export of diagnostics file to HTTP and HTTPS share via SOCKS proxy.
- idrac_firmware - Issue(279282) - This module does not support firmware update using HTTP, HTTPS, and FTP shares with authentication on iDRAC8.
- idrac_storage_volume - Issue(290766) - The module will report success instead of showing failure for new virtual creation on the BOSS-N1 controller if a virtual disk is already present on the same controller.
- idrac_support_assist - Issue(308550) - This module fails when the NFS share path contains sub directory.
- ome_diagnostics - Issue(279193) - Export of SupportAssist collection logs to the share location fails on OME version 4.0.0.
- ome_smart_fabric_uplink - Issue(186024) - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.

v9.6.0
======

Release Summary
---------------

- The ``ome_application_certificate`` module is enhanced to support the upload of certificate chain.
- The ``idrac_support_assist`` module is added to add support to run and export SupportAssist collection logs on iDRAC.
- The ``idrac_secure_boot`` module is added to import the secure boot certificate.

Major Changes
-------------

- idrac_secure_boot - This module allows to import the secure boot certificate.
- idrac_support_assist - This module allows to run and export SupportAssist collection logs on iDRAC.

Minor Changes
-------------

- ome_application_certificate - This module is enhanced to support the upload of certificate chain.

Known Issues
------------

- idrac_diagnostics - Issue(285322) - This module doesn't support export of diagnostics file to HTTP and HTTPS share via SOCKS proxy.
- idrac_firmware - Issue(279282) - This module does not support firmware update using HTTP, HTTPS, and FTP shares with authentication on iDRAC8.
- idrac_storage_volume - Issue(290766) - The module will report success instead of showing failure for new virtual creation on the BOSS-N1 controller if a virtual disk is already present on the same controller.
- idrac_support_assist - Issue(308550) - This module fails when the NFS share path contains sub directory.
- ome_diagnostics - Issue(279193) - Export of SupportAssist collection logs to the share location fails on OME version 4.0.0.
- ome_smart_fabric_uplink - Issue(186024) - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.

v9.5.0
======

Release Summary
---------------

- The ``idrac_redfish_storage_controller`` module is enhanced to support secure and/or cryptographic erase of the physical disk.
- The ``ome_application_network_proxy`` module is enhanced to manage the Proxy Exclusion List and Certificate Validation.
- The ``idrac_redfish_powerstate`` module is enhanced to support full virtual A/C power cycle.

Minor Changes
-------------

- idrac_redfish_powerstate - This module is enhanced to support full virtual A/C power cycle.
- idrac_redfish_storage_controller - This module is enhanced to support secure and/or cryptographic erase of the physical disk.
- ome_application_network_proxy - This module is enhanced to manage the Proxy Exclusion List and Certificate Validation.

Known Issues
------------

- idrac_diagnostics - Issue(285322) - This module doesn't support export of diagnostics file to HTTP and HTTPS share via SOCKS proxy.
- idrac_firmware - Issue(279282) - This module does not support firmware update using HTTP, HTTPS, and FTP shares with authentication on iDRAC8.
- idrac_storage_volume - Issue(290766) - The module will report success instead of showing failure for new virtual creation on the BOSS-N1 controller if a virtual disk is already present on the same controller.
- ome_diagnostics - Issue(279193) - Export of SupportAssist collection logs to the share location fails on OME version 4.0.0.
- ome_smart_fabric_uplink - Issue(186024) - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.

v9.4.0
======

Release Summary
---------------

- The ``idrac_server_config_profile`` module is enhanced to allow you to export and import custom defaults on iDRAC.
- The ``ome_configuration_compliance_baseline`` module is enhanced to schedule the remediation job and stage the reboot.
- The ``idrac_reset`` module is enhanced to provide default username and defaut password for the reset operation.

Major Changes
-------------

- idrac_server_config_profile - This module is enhanced to allow you to export and import custom defaults on iDRAC.
- ome_configuration_compliance_baseline - This module is enhanced to schedule the remediation job and stage the reboot.

Minor Changes
-------------

- idrac_reset - This module is enhanced to provide default username and default password for the reset operation.

Bugfixes
--------

- Resolved the issue in ``idrac_reset`` module where it fails when iDRAC is in busy state. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/652)

Known Issues
------------

- idrac_diagnostics - Issue(285322) - This module doesn't support export of diagnostics file to HTTP and HTTPS share via SOCKS proxy.
- idrac_firmware - Issue(279282) - This module does not support firmware update using HTTP, HTTPS, and FTP shares with authentication on iDRAC8.
- idrac_storage_volume - Issue(290766) - The module will report success instead of showing failure for new virtual creation on the BOSS-N1 controller if a virtual disk is already present on the same controller.
- ome_diagnostics - Issue(279193) - Export of SupportAssist collection logs to the share location fails on OME version 4.0.0.
- ome_smart_fabric_uplink - Issue(186024) - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.

v9.3.0
======

Release Summary
---------------

- The ``ome_session`` module is added to allow you to create and delete the sessions on OpenManage Enterprise and OpenManage Enterprise Modular.
- Added support to use session ID for authentication of iDRAC, OpenManage Enterprise and OpenManage Enterprise Modular modules.
- Added time_to_wait option in ``idrac_storage_volume`` module.
- Added support for Python 3.12.

Major Changes
-------------

- Added support to use session ID for authentication of iDRAC, OpenManage Enterprise and OpenManage Enterprise Modular.
- ome_session - This module allows you to create and delete the sessions on OpenManage Enterprise and OpenManage Enterprise Modular.

Minor Changes
-------------

- Added support for Python 3.12.
- Added time_to_wait option in ``idrac_storage_volume`` module.

Bugfixes
--------

- Resolved the issue in ``idrac_certificates`` module where subject_alt_name parameter was only accepting first item in list. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/584)
- Resolved the issue in ``idrac_virtual_media`` module where the Authorization request header was included in the request. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/612)
- Resolved the issue in ``ome_application_certificate`` module related to a padding error in generated CSR file. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/370)

Known Issues
------------

- idrac_diagnostics - Issue(285322) - This module doesn't support export of diagnostics file to HTTP and HTTPS share via SOCKS proxy.
- idrac_firmware - Issue(279282) - This module does not support firmware update using HTTP, HTTPS, and FTP shares with authentication on iDRAC8.
- idrac_storage_volume - Issue(290766) - The module will report success instead of showing failure for new virtual creation on the BOSS-N1 controller if a virtual disk is already present on the same controller.
- ome_diagnostics - Issue(279193) - Export of SupportAssist collection logs to the share location fails on OME version 4.0.0.
- ome_smart_fabric_uplink - Issue(186024) - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_session - This module allows you to create and delete sessions on OpenManage Enterprise and OpenManage Enterprise Modular.

v9.2.0
======

Release Summary
---------------

- The idrac_session module is added to allow you to create and delete the sessions on iDRAC.
- The idrac_reset module is enhanced to allow you to reset the iDRAC to factory default settings.

Major Changes
-------------

- idrac_session - This module allows you to create and delete the sessions on iDRAC.

Minor Changes
-------------

- idrac_reset - This module allows you to reset the iDRAC to factory default settings.

Known Issues
------------

- idrac_diagnostics - Issue(285322) - This module doesn't support export of diagnostics file to HTTP and HTTPS share via SOCKS proxy.
- idrac_firmware - Issue(279282) - This module does not support firmware update using HTTP, HTTPS, and FTP shares with authentication on iDRAC8.
- idrac_storage_volume - Issue(290766) - The module will report success instead of showing failure for new virtual creation on the BOSS-N1 controller if a virtual disk is already present on the same controller.
- ome_diagnostics - Issue(279193) - Export of SupportAssist collection logs to the share location fails on OME version 4.0.0.
- ome_smart_fabric_uplink - Issue(186024) - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.idrac_session - Allows you to create and delete the sessions on iDRAC.

v9.1.0
======

Release Summary
---------------

- ``redfish_storage_volume`` is enhanced to support iDRAC8.
- ``dellemc_idrac_storage_module`` is deprecated and replaced with ``idrac_storage_volume``.

Minor Changes
-------------

- redfish_storage_volume - This module is enhanced to support iDRAC8.

Deprecated Features
-------------------

- The ``dellemc_idrac_storage_volume`` module is deprecated and replaced with ``idrac_storage_volume``.

Bugfixes
--------

- Added support for RAID creation using NVMe disks.(https://github.com/dell/dellemc-openmanage-ansible-modules/issues/635)
- redfish_storage_volume is enhanced to support iDRAC8.(https://github.com/dell/dellemc-openmanage-ansible-modules/issues/625)

Known Issues
------------

- idrac_diagnostics - Issue(285322) - This module doesn't support export of diagnostics file to HTTP and HTTPS share via SOCKS proxy.
- idrac_firmware - Issue(279282) - This module does not support firmware update using HTTP, HTTPS, and FTP shares with authentication on iDRAC8.
- idrac_storage_volume - Issue(290766) - The module will report success instead of showing failure for new virtual creation on the BOSS-N1 controller if a virtual disk is already present on the same controller.
- ome_diagnostics - Issue(279193) - Export of SupportAssist collection logs to the share location fails on OME version 4.0.0.
- ome_smart_fabric_uplink - Issue(186024) - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.idrac_storage_volume - Configures the RAID configuration attributes.

v9.0.0
======

Release Summary
---------------

- idrac_diagnostics module is added to run and export diagnostics on iDRAC.
- idrac_user role is added to manage local users of iDRAC.

Major Changes
-------------

- idrac_diagnostics - The module is introduced to run and export diagnostics on iDRAC.
- idrac_user - This role is introduced to manage local users of iDRAC.

Bugfixes
--------

- idrac_network_attributes - Issue(279049) -  If unsupported values are provided for the parameter ``ome_network_attributes``, then this module does not provide a correct error message.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the following parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``

Known Issues
------------

- idrac_diagnostics - Issue(285322) - This module doesn't support export of diagnostics file to HTTP and HTTPS share via SOCKS proxy.
- idrac_firmware - Issue(279282) - This module does not support firmware update using HTTP, HTTPS, and FTP shares with authentication on iDRAC8.
- ome_diagnostics - Issue(279193) - Export of SupportAssist collection logs to the share location fails on OME version 4.0.0.
- ome_smart_fabric_uplink - Issue(186024) - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.idrac_diagnostics - This module allows to run and export diagnostics on iDRAC.

New Roles
---------

- dellemc.openmanage.idrac_user - Role to manage local users of iDRAC.

v8.7.0
======

Release Summary
---------------

- Module to manage iDRAC licenses.
- idrac_gather_facts role is enhanced to add storage controller details in the role output and provide support for secure boot.

Major Changes
-------------

- idrac_gather_facts - This role is enhanced to support secure boot.
- idrac_license - The module is introduced to configure iDRAC licenses.

Minor Changes
-------------

- For idrac_gather_facts role, added storage controller details in the role output.

Bugfixes
--------

- Issue is fixed for deploying a new configuration on quick deploy slot when IPv6 is disabled.(https://github.com/dell/dellemc-openmanage-ansible-modules/issues/533)

Known Issues
------------

- idrac_firmware - Issue(279282) - This module does not support firmware update using HTTP, HTTPS, and FTP shares with authentication on iDRAC8.
- idrac_network_attributes - Issue(279049) -  If unsupported values are provided for the parameter ``ome_network_attributes``, then this module does not provide a correct error message.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the following parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_diagnostics - Issue(279193) - Export of SupportAssist collection logs to the share location fails on OME version 4.0.0.
- ome_smart_fabric_uplink - Issue(186024) - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.idrac_license - This module allows to import, export, and delete licenses on iDRAC.

v8.6.0
======

Release Summary
---------------

- Added support for the environment variables as fallback for credentials for all modules of iDRAC, OME, and Redfish.
- Enhanced idrac_certificates module and idrac_certificate role to support `CUSTOMCERTIFICATE` and import `HTTPS` certificate with the SSL key.

Major Changes
-------------

- All OME modules are enhanced to support the environment variables `OME_USERNAME` and `OME_PASSWORD` as fallback for credentials.
- All iDRAC and Redfish modules are enhanced to support the environment variables `IDRAC_USERNAME` and `IDRAC_PASSWORD` as fallback for credentials.
- idrac_certificates - The module is enhanced to support the import and export of `CUSTOMCERTIFICATE`.

Minor Changes
-------------

- For idrac_certificate role, added support for import operation of `HTTPS` certificate with the SSL key.
- For idrac_certificates module, below enhancements are made: Added support for import operation of `HTTPS` certificate with the SSL key. The `email_address` has been made as an optional parameter.

Bugfixes
--------

- Fixed the issue for ignoring the environment variable `NO_PROXY` earlier. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/554)
- For idrac_certificates module, the `email_address` has been made as an optional parameter. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/582).

Known Issues
------------

- idrac_firmware - Issue(279282) - This module does not support firmware update using HTTP, HTTPS, and FTP shares with authentication on iDRAC8.
- idrac_network_attributes - Issue(279049) -  If unsupported values are provided for the parameter ``ome_network_attributes``, then this module does not provide a correct error message.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the following parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_device_quick_deploy - Issue(275231) - This module does not deploy a new configuration to a slot that has disabled IPv6.
- ome_diagnostics - Issue(279193) - Export of SupportAssist collection logs to the share location fails on OME version 4.0.0.
- ome_smart_fabric_uplink - Issue(186024) - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.

v8.5.0
======

Release Summary
---------------

- Ansible lint issues are fixed for the collections.
- redfish_storage_volume module is enhanced to support reboot options and job tracking operation.

Minor Changes
-------------

- Ansible lint issues are fixed for the collections.
- Module ``redfish_storage_volume`` is enhanced to support reboot options and job tracking operation.

Bugfixes
--------

- ome_inventory - The plugin returns 50 results when a group is specified. No results are shown when a group is not specified. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/575).

Known Issues
------------

- idrac_firmware - Issue(279282) - This module does not support firmware update using HTTP, HTTPS, and FTP shares with authentication on iDRAC8.
- idrac_network_attributes - Issue(279049) -  If unsupported values are provided for the parameter ``ome_network_attributes``, then this module does not provide a correct error message.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the following parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_device_quick_deploy - Issue(275231) - This module does not deploy a new configuration to a slot that has disabled IPv6.
- ome_diagnostics - Issue(279193) - Export of SupportAssist collection logs to the share location fails on OME version 4.0.0.
- ome_smart_fabric_uplink - Issue(186024) - The module supported by OpenManage Enterprise Modular, however it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, then the existing uplink is modified.

v8.4.0
======

Release Summary
---------------

Module to manage iDRAC network attributes.

Bugfixes
--------

- idrac_firmware - Issue(276335) - This module fails on the Python 3.11.x version with NFS share. Use a different Python version or Share type.
- idrac_server_config_profile - The import for Server Configuration Profile (SCP) operation fails to handle the absence of a file and incorrectly reports success instead of the expected failure. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/544).

Known Issues
------------

- ca_path missing - Issue(275740) - The roles idrac_attributes, redfish_storage_volume, and idrac_server_powerstate have a missing parameter ca_path.
- idrac_firmware - Issue(279282) - This module does not support firmware update using HTTP, HTTPS, and FTP shares with authentication on iDRAC8.
- idrac_network_attributes - Issue(279049) -  If unsupported values are provided for the parameter ``ome_network_attributes``, then this module does not provide a correct error message.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the following parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_device_quick_deploy - Issue(275231) - This module does not deploy a new configuration to a slot that has disabled IPv6.
- ome_smart_fabric_uplink - Issue(186024) - Despite the module supported by OpenManage Enterprise Modular, it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.idrac_network_attributes - This module allows you to configure the port and partition network attributes on the network interface cards.

v8.3.0
======

Release Summary
---------------

- Module to manage OME alert policies.
- Support for RAID6 and RAID60 for module ``redfish_storage_volume``.
- Support for reboot type options for module ``ome_firmware``.

Minor Changes
-------------

- Module ``ome_firmware`` is enhanced to support reboot type options.
- Module ``redfish_storage_volume`` is enhanced to support RAID6 and RAID60.

Bugfixes
--------

- ome_device_quick_deploy - If the blade is not present, then the module can assign a static IP to the slot (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/532).

Known Issues
------------

- ca_path missing - Issue(275740) - The roles idrac_attributes, redfish_storage_volume, and idrac_server_powerstate have a missing parameter ca_path.
- idrac_firmware - Issue(276335) - This module fails on the Python 3.11.x version with NFS shares. Use a different Python version or Share type.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the following parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_device_quick_deploy - Issue(275231) - This module does not deploy a new configuration to a slot that has disabled IPv6.
- ome_smart_fabric_uplink - Issue(186024) - Despite the module supported by OpenManage Enterprise Modular, it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_alert_policies - Manage OME alert policies.

v8.2.0
======

Release Summary
---------------

- redfish_firmware and ome_firmware_catalog module is enhanced to support IPv6 address.
- Module to support firmware rollback of server components.
- Support for retrieving alert policies, actions, categories and message id information of alert policies for OME and OME Modular.
- ome_diagnostics module is enhanced to update changed flag status in response.

Minor Changes
-------------

- Module ``ome_diagnostics`` is enhanced to update changed flag status in response.
- Module ``ome_firmware_catalog`` is enhanced to support IPv6 address.
- Module ``redfish_firmware`` is enhanced to support IPv6 address.

Bugfixes
--------

- Update document on how to use with ansible. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/393).

Known Issues
------------

- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the following parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) - Despite the module supported by OpenManage Enterprise Modular, it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_alert_policies_action_info - Get information on actions of alert policies.
- dellemc.openmanage.ome_alert_policies_category_info - Retrieves information of all OME alert policy categories.
- dellemc.openmanage.ome_alert_policies_info - Retrieves information of one or more OME alert policies.
- dellemc.openmanage.ome_alert_policies_message_id_info - Get message ID information of alert policies.
- dellemc.openmanage.redfish_firmware_rollback - To perform a component firmware rollback using component name.

v8.1.0
======

Release Summary
---------------

- Support for subject alternative names while generating certificate signing requests on OME.
- Create a user on iDRAC using custom privileges.
- Create a firmware baseline on OME with the filter option of no reboot required.
- Retrieve all server items in the output for ome_device_info.
- Enhancement to add detailed job information for ome_discovery and ome_job_info.

Minor Changes
-------------

- Module ``idrac_user`` is enhanced to configure custom privileges for an user.
- Module ``ome_application_certificate`` is enhanced to support subject alternative names.
- Module ``ome_discovery`` is enhanced to add detailed job information of each IP discovered.
- Module ``ome_firmware_baseline`` is enhanced to support the option to select only components with no reboot required.
- Module ``ome_job_info`` is enhanced to return last execution details and execution histories.

Bugfixes
--------

- The Chassis Power PIN value must be of six numerical digits input from the module. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/492).
- idrac_attributes module can now support modification of IPv6 attributes on iDRAC 8. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/488).
- ome_device_info is limited to 50 responses with a query filter. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/499).

Known Issues
------------

- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the following parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) - Despite the module supported by OpenManage Enterprise Modular, it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

v8.0.0
======

Release Summary
---------------

Role ``idrac_boot`` and ``idrac_job_queue`` is added to manage the boot order settings and iDRAC lifecycle controller job queue respectively. ``Role idrac_os_deployment`` is enhanced to remove the auto installations of required libraries and to support custom ISO and kickstart file as input. Dropped support for iDRAC7 based Dell PowerEdge Servers.

Minor Changes
-------------

- All the module documentation and examples are updated to use true or false for Boolean values.
- Role ``idrac_os_deployment`` is enhanced to remove the auto installation of required libraries and to support custom ISO and kickstart file as input.

Removed Features (previously deprecated)
----------------------------------------

- The ``dellemc_get_firmware_inventory`` module is removed and replaced with the module ``idrac_firmware_info``.
- The ``dellemc_get_system_inventory`` module is removed and replaced with the module ``idrac_system_info``.

Bugfixes
--------

- Job tracking is fixed for iDRAC SCP import (https://github.com/dell/dellemc-openmanage-ansible-modules/pull/504).
- OMSDK is handled for import error ``SNIMissingWarning`` that is undefined (https://github.com/dell/omsdk/issues/33).

Known Issues
------------

- idrac_redfish_storage_controller - Issue(256164) - If incorrect value is provided for one of the attributes in the provided attribute list for controller configuration, then this module does not exit with error.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the following parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) - Despite the module supported by OpenManage Enterprise Modular, it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Roles
---------

- dellemc.openmanage.idrac_boot - Configure the boot order settings
- dellemc.openmanage.idrac_job_queue - Role to manage the iDRAC lifecycle controller job queue.

v7.6.1
======

Release Summary
---------------

Removed the dependency of community general collections.

Minor Changes
-------------

- Updated the idrac_gather_facts role to use jinja template filters.

Known Issues
------------

- idrac_redfish_storage_controller - Issue(256164) - If incorrect value is provided for one of the attributes in the provided attribute list for controller configuration, then this module does not exit with error.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the following parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) - Despite the module supported by OpenManage Enterprise Modular, it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

v7.6.0
======

Release Summary
---------------

- Role to configure the iDRAC system, manager, and lifecycle attributes for Dell PowerEdge servers.
- Role to modify BIOS attributes, clear pending BIOS attributes, and reset the BIOS to default settings.
- Role to reset and restart iDRAC (iDRAC8 and iDRAC9 only) for Dell PowerEdge servers.
- Role to configure the physical disk, virtual disk, and storage controller settings on iDRAC9 based PowerEdge servers.

Known Issues
------------

- idrac_redfish_storage_controller - Issue(256164) - If incorrect value is provided for one of the attributes in the provided attribute list for controller configuration, then this module does not exit with error.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the following parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) - Despite the module supported by OpenManage Enterprise Modular, it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Roles
---------

- dellemc.openmanage.idrac_attributes - Role to configure iDRAC attributes.
- dellemc.openmanage.idrac_bios - Role to modify BIOS attributes, clear pending BIOS attributes, and reset the BIOS to default settings.
- dellemc.openmanage.idrac_reset - Role to reset and restart iDRAC (iDRAC8 and iDRAC9 only) for Dell PowerEdge servers.
- dellemc.openmanage.idrac_storage_controller - Role to configure the physical disk, virtual disk, and storage controller settings on iDRAC9 based PowerEdge servers.

v7.5.0
======

Release Summary
---------------

- redfish_firmware - This module is enhanced to include job tracking.
- ome_template - This module is enhanced to include job tracking.
- Role to support the iDRAC and Redfish firmware update and manage storage volume configuration is added.
- Role to deploy the iDRAC operating system is enhanced to support ESXi version 8.X and HTTP or HTTPS for the destination.

Known Issues
------------

- idrac_os_deployment- Issue(260496) - OS installation will support only NFS and CIFS share to store the custom ISO in the destination_path, HTTP/HTTPS/FTP not supported
- idrac_redfish_storage_controller - Issue(256164) - If incorrect value is provided for one of the attributes in the provided attribute list for controller configuration, then this module does not exit with error.
- idrac_user - Issue(192043) The module may error out with the message ``Unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the following parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) - Despite the module supported by OpenManage Enterprise Modular, it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Roles
---------

- dellemc.openmanage.idrac_firmware - Firmware update from a repository on a network share (CIFS, NFS, HTTP, HTTPS, FTP).
- dellemc.openmanage.redfish_firmware - To perform a component firmware update using the image file available on the local or remote system.
- dellemc.openmanage.redfish_storage_volume - Role to manage the storage volume configuration.

v7.4.0
======

Release Summary
---------------

- Role to support the Import server configuration profile, Manage iDRAC power states, Manage iDRAC certificate,
  Gather facts from iDRAC and Deploy operating system is added.
- Plugin OME inventory is enhanced to support the environment variables for the input parameters.

Known Issues
------------

- idrac_os_deployment- Issue(260496) - OS installation will support only NFS and CIFS share to store the custom ISO in the destination_path, HTTP/HTTPS/FTP not supported
- idrac_redfish_storage_controller - Issue(256164) - If incorrect value is provided for one of the attributes in the provided attribute list for controller configuration, then this module does not exit with error.
- idrac_user - Issue(192043) The module may error out with the message ``Unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the following parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) - Despite the module supported by OpenManage Enterprise Modular, it does not allow the creation of multiple uplinks of the same name. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Roles
---------

- dellemc.openmanage.idrac_certificate - Role to manage the iDRAC certificates - generate CSR, import/export certificates, and reset configuration - for PowerEdge servers.
- dellemc.openmanage.idrac_gather_facts - Role to gather facts from the iDRAC Server.
- dellemc.openmanage.idrac_import_server_config_profile - Role to import iDRAC Server Configuration Profile (SCP).
- dellemc.openmanage.idrac_os_deployment - Role to deploy specified operating system and version on the servers.
- dellemc.openmanage.idrac_server_powerstate - Role to manage the different power states of the specified device.

v7.3.0
======

Release Summary
---------------

Support for iDRAC export Server Configuration Profile role and proxy settings, import buffer, include in export, and ignore certificate warning.

Major Changes
-------------

- idrac_server_config_profile - This module is enhanced to support proxy settings, import buffer, include in export, and ignore certificate warning.

Known Issues
------------

- idrac_redfish_storage_controller - Issue(256164) - If incorrect value is provided for one of the attributes in the provided attribute list for controller configuration, then this module does not exit with error.
- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_inventory - Issue(256257) - All hosts are not retrieved for ``Modular System`` group and corresponding child groups.
- ome_inventory - Issue(256589) - All hosts are not retrieved for ``Custom Groups`` group and corresponding child groups.
- ome_inventory - Issue(256593) - All hosts are not retrieved for ``PLUGIN GROUPS`` group and corresponding child groups.
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Roles
---------

- dellemc.openmanage.idrac_export_server_config_profile - Role to export iDRAC Server Configuration Profile (SCP).

v7.2.0
======

Release Summary
---------------

Support for retrieving the inventory and host details of all child groups using parent groups, retrieving inventory of System and Plugin Groups, retrieving profiles with attributes, retrieving network configuration of a template, configuring controller attributes, configuring online capacity expansion, and importing the LDAP directory.

Major Changes
-------------

- idrac_redfish_storage_controller - This module is enhanced to configure controller attributes and online capacity expansion.
- ome_domian_user_groups - This module allows to import the LDAP directory groups.
- ome_inventory - This plugin is enhanced to support inventory retrieval of System and Plugin Groups of OpenManage Enterprise.
- ome_profile_info - This module allows to retrieve profiles with attributes on OpenManage Enterprise or OpenManage Enterprise Modular.
- ome_template_network_vlan_info - This module allows to retrieve the network configuration of a template on OpenManage Enterprise or OpenManage Enterprise Modular.

Known Issues
------------

- idrac_redfish_storage_controller - Issue(256164) - If incorrect value is provided for one of the attributes in the provided attribute list for controller configuration, then this module does not exit with error.
- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_inventory - Issue(256257) - All hosts are not retrieved for ``Modular System`` group and corresponding child groups.
- ome_inventory - Issue(256589) - All hosts are not retrieved for ``Custom Groups`` group and corresponding child groups.
- ome_inventory - Issue(256593) - All hosts are not retrieved for ``PLUGIN GROUPS`` group and corresponding child groups.
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_profile_info - Retrieve profiles with attribute details
- dellemc.openmanage.ome_template_network_vlan_info - Retrieves network configuration of template.

v7.1.0
======

Release Summary
---------------

Support for retrieving smart fabric and smart fabric uplink information and support for IPv6 address for OMSDK dependent iDRAC modules.

Major Changes
-------------

- Support for IPv6 address for OMSDK dependent iDRAC modules.
- ome_inventory - This plugin allows to create a inventory from the group on OpenManage Enterprise.
- ome_smart_fabric_info - This module retrieves the list of smart fabrics in the inventory of OpenManage Enterprise Modular.
- ome_smart_fabric_uplink_info - This module retrieve details of fabric uplink on OpenManage Enterprise Modular.

Minor Changes
-------------

- redfish_firmware - This module supports timeout option.

Known Issues
------------

- idrac_firmware - Issue(249879) - Firmware update of iDRAC9-based Servers fails if SOCKS proxy with authentication is used.
- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Plugins
-----------

Inventory
~~~~~~~~~

- dellemc.openmanage.ome_inventory - Group inventory plugin on OpenManage Enterprise.

New Modules
-----------

- dellemc.openmanage.ome_smart_fabric_info - Retrieves the information of smart fabrics inventoried by OpenManage Enterprise Modular
- dellemc.openmanage.ome_smart_fabric_uplink_info - Retrieve details of fabric uplink on OpenManage Enterprise Modular.

v7.0.0
======

Release Summary
---------------

Rebranded from Dell EMC to Dell, enhanced idrac_firmware module to support proxy, and added support to retrieve iDRAC local user details.

Major Changes
-------------

- Rebranded from Dell EMC to Dell.
- idrac_firmware - This module is enhanced to support proxy.
- idrac_user_info - This module allows to retrieve iDRAC Local user information details.

Known Issues
------------

- idrac_firmware - Issue(249879) - Firmware update of iDRAC9-based Servers fails if SOCKS proxy with authentication is used.
- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.idrac_user_info - Retrieve iDRAC Local user details.

v6.3.0
======

Release Summary
---------------

Support for LockVirtualDisk operation and to configure Remote File Share settings using idrac_virtual_media module.

Major Changes
-------------

- idrac_redfish_storage_controller - This module is enhanced to support LockVirtualDisk operation.
- idrac_virtual_media - This module allows to configure Remote File Share settings.

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.idrac_virtual_media - Configure the virtual media settings.

v6.2.0
======

Release Summary
---------------

Added clear pending BIOS attributes, reset BIOS to default settings, and configure BIOS attribute using Redfish enhancements for idrac_bios.

Major Changes
-------------

- idrac_bios - The module is enhanced to support clear pending BIOS attributes, reset BIOS to default settings, and configure BIOS attribute using Redfish.

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

v6.1.0
======

Release Summary
---------------

Support for device-specific operations on OpenManage Enterprise and configuring boot settings on iDRAC.

Major Changes
-------------

- idrac_boot - Support for configuring the boot settings on iDRAC.
- ome_device_group - The module is enhanced to support the removal of devices from a static device group.
- ome_devices - Support for performing device-specific operations on OpenManage Enterprise.

Minor Changes
-------------

- ome_configuration_compliance_info - The module is enhanced to report single device compliance information.

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_local_access_configuration - Issue(215035) - The module reports ``Successfully updated the local access setting`` if an unsupported value is provided for the parameter timeout_limit. However, this value is not actually applied on OpenManage Enterprise Modular.
- ome_device_local_access_configuration - Issue(217865) - The module does not display a proper error message if an unsupported value is provided for the user_defined and lcd_language parameters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_device_quick_deploy - Issue(216352) - The module does not display a proper error message if an unsupported value is provided for the ipv6_prefix_length and vlan_id parameters.
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.idrac_boot - Configure the boot order settings.
- dellemc.openmanage.ome_devices - Perform device-specific operations on target devices

v6.0.0
======

Release Summary
---------------

Added collection metadata for creating execution environments, deprecation of share parameters, and support for configuring iDRAC attributes using idrac_attributes module.

Major Changes
-------------

- Added collection metadata for creating execution environments.
- Refactored the Markdown (MD) files and content for better readability.
- The share parameters are deprecated from the following modules - idrac_network, idrac_timezone_ntp, dellemc_configure_idrac_eventing, dellemc_configure_idrac_services, dellemc_idrac_lc_attributes, dellemc_system_lockdown_mode.

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_local_access_configuration - Issue(215035) - The module reports ``Successfully updated the local access setting`` if an unsupported value is provided for the parameter timeout_limit. However, this value is not actually applied on OpenManage Enterprise Modular.
- ome_device_local_access_configuration - Issue(217865) - The module does not display a proper error message if an unsupported value is provided for the user_defined and lcd_language parameters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_device_quick_deploy - Issue(216352) - The module does not display a proper error message if an unsupported value is provided for the ipv6_prefix_length and vlan_id parameters.
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.idrac_attributes - Configure the iDRAC attributes

v5.5.0
======

Release Summary
---------------

Support to generate certificate signing request, import, and export certificates on iDRAC.

Minor Changes
-------------

- idrac_redfish_storage_controller - This module is updated to use the Job Service URL instead of Task Service URL for job tracking.
- idrac_server_config_profile - This module is updated to use the Job Service URL instead of Task Service URL for job tracking.
- redfish_firmware - This module is updated to use the Job Service URL instead of Task Service URL for job tracking.

Bugfixes
--------

- idrac_server_config_profile - Issue(234817) – When an XML format is exported using the SCP, the module breaks while waiting for the job completion.
- ome_application_console_preferences - Issue(224690) - The module does not display a proper error message when an unsupported value is provided for the parameters report_row_limit, email_sender_settings, and metric_collection_settings, and the value is applied on OpenManage Enterprise

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_local_access_configuration - Issue(215035) - The module reports ``Successfully updated the local access setting`` if an unsupported value is provided for the parameter timeout_limit. However, this value is not actually applied on OpenManage Enterprise Modular.
- ome_device_local_access_configuration - Issue(217865) - The module does not display a proper error message if an unsupported value is provided for the user_defined and lcd_language parameters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_device_quick_deploy - Issue(216352) - The module does not display a proper error message if an unsupported value is provided for the ipv6_prefix_length and vlan_id parameters.
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.idrac_certificates - Configure certificates for iDRAC.

v5.4.0
======

Release Summary
---------------

Support for export, import, and preview the Server Configuration Profile (SCP) configuration using Redfish and added support for check mode.

Major Changes
-------------

- idrac_server_config_profile - The module is enhanced to support export, import, and preview the SCP configuration using Redfish and added support for check mode.

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_console_preferences - Issue(224690) - The module does not display a proper error message when an unsupported value is provided for the parameters report_row_limit, email_sender_settings, and metric_collection_settings, and the value is applied on OpenManage Enterprise.
- ome_device_local_access_configuration - Issue(215035) - The module reports ``Successfully updated the local access setting`` if an unsupported value is provided for the parameter timeout_limit. However, this value is not actually applied on OpenManage Enterprise Modular.
- ome_device_local_access_configuration - Issue(217865) - The module does not display a proper error message if an unsupported value is provided for the user_defined and lcd_language parameters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_device_quick_deploy - Issue(216352) - The module does not display a proper error message if an unsupported value is provided for the ipv6_prefix_length and vlan_id parameters.
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

v5.3.0
======

Release Summary
---------------

Added check mode and idempotency support for redfish_storage_volume and idempotency support for ome_smart_fabric_uplink. For ome_diagnostics, added support for debug logs and added supportassist_collection as a choice for the log_type argument to export SupportAssist logs.

Minor Changes
-------------

- ome_diagnostics - Added "supportassist_collection" as a choice for the log_type argument to export SupportAssist logs. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/309)
- ome_diagnostics - The module is enhanced to support debug logs. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/308)
- ome_smart_fabric_uplink - The module is enhanced to support idempotency. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/253)
- redfish_storage_volume - The module is enhanced to support check mode and idempotency. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/245)

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_console_preferences - Issue(224690) - The module does not display a proper error message when an unsupported value is provided for the parameters report_row_limit, email_sender_settings, and metric_collection_settings, and the value is applied on OpenManage Enterprise.
- ome_device_local_access_configuration - Issue(215035) - The module reports ``Successfully updated the local access setting`` if an unsupported value is provided for the parameter timeout_limit. However, this value is not actually applied on OpenManage Enterprise Modular.
- ome_device_local_access_configuration - Issue(217865) - The module does not display a proper error message if an unsupported value is provided for the user_defined and lcd_language parameters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_device_quick_deploy - Issue(216352) - The module does not display a proper error message if an unsupported value is provided for the ipv6_prefix_length and vlan_id parameters.
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

v5.2.0
======

Release Summary
---------------

Support to configure console preferences on OpenManage Enterprise.

Minor Changes
-------------

- idrac_redfish_storage_controller - This module is enhanced to support the following settings with check mode and idempotency - UnassignSpare, EnableControllerEncryption, BlinkTarget, UnBlinkTarget,  ConvertToRAID, ConvertToNonRAID, ChangePDStateToOnline, ChangePDStateToOffline.
- ome_diagnostics - The module is enhanced to support check mode and idempotency. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/345)
- ome_diagnostics - This module is enhanced to extract log from lead chassis. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/310)
- ome_profile - The module is enhanced to support check mode and idempotency.
- ome_profile - The module is enhanced to support modifying a profile based on the attribute names instead of the ID.
- ome_template - The module is enhanced to support check mode and idempotency. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/255)
- ome_template - The module is enhanced to support modifying a template based on the attribute names instead of the ID. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/358)

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_console_preferences - Issue(224690) - The module does not display a proper error message when an unsupported value is provided for the parameters report_row_limit, email_sender_settings, and metric_collection_settings, and the value is applied on OpenManage Enterprise.
- ome_device_local_access_configuration - Issue(215035) - The module reports ``Successfully updated the local access setting`` if an unsupported value is provided for the parameter timeout_limit. However, this value is not actually applied on OpenManage Enterprise Modular.
- ome_device_local_access_configuration - Issue(217865) - The module does not display a proper error message if an unsupported value is provided for the user_defined and lcd_language parameters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_device_quick_deploy - Issue(216352) - The module does not display a proper error message if an unsupported value is provided for the ipv6_prefix_length and vlan_id parameters.
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_application_console_preferences - Configures console preferences on OpenManage Enterprise.

v5.1.0
======

Release Summary
---------------

Support for OpenManage Enterprise Modular server interface management.

Minor Changes
-------------

- ome_application_network_address - The module is enhanced to support check mode and idempotency.
- ome_device_info - The module is enhanced to return a blank list when devices or baselines are not present in the system.
- ome_firmware_baseline_compliance_info - The module is enhanced to return a blank list when devices or baselines are not present in the system.
- ome_firmware_baseline_info - The module is enhanced to return a blank list when devices or baselines are not present in the system.
- ome_identity_pool - The iSCSI Initiator and Initiator IP Pool attributes are not mandatory to create an identity pool. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/329)
- ome_identity_pool - The module is enhanced to support check mode and idempotency. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/328)
- ome_template_identity_pool - The module is enhanced to support check mode and idempotency.
- redfish_event_subscription - The module is enhanced to support check mode and idempotency.

Bugfixes
--------

- idrac_firmware - Issue (220130) The socket.timout issue that occurs during the wait_for_job_completion() job is fixed.

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_local_access_configuration - Issue(215035) - The module reports ``Successfully updated the local access setting`` if an unsupported value is provided for the parameter timeout_limit. However, this value is not actually applied on OpenManage Enterprise Modular.
- ome_device_local_access_configuration - Issue(217865) - The module does not display a proper error message if an unsupported value is provided for the user_defined and lcd_language parameters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module errors out with the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_server_interface_profile_info - Retrieves the information of server interface profile on OpenManage Enterprise Modular.
- dellemc.openmanage.ome_server_interface_profiles - Configures server interface profiles on OpenManage Enterprise Modular.

v5.0.1
======

Release Summary
---------------

Support to provide custom or organizational CA signed certificate for SSL validation from the environment variable.

Major Changes
-------------

- All modules can read custom or organizational CA signed certificate from the environment variables. Please refer to `SSL Certificate Validation <https://github.com/dell/dellemc-openmanage-ansible-modules#ssl-certificate-validation>` _ section in the `README.md <https://github.com/dell/dellemc-openmanage-ansible-modules /blob/collections/README.md#SSL-Certificate-Validation>` _ for modification to existing playbooks or setting environment variable.

Bugfixes
--------

- All playbooks require modification because the validate_certs argument is set to True by default (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/357)
- The ome_application_network_time and ome_application_network_proxy modules are breaking due to the changes introduced for SSL validation.(https://github.com/dell/dellemc-openmanage-ansible-modules/issues/360)

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_local_access_configuration - Issue(215035) - The module reports ``Successfully updated the local access setting`` if an unsupported value is provided for the parameter timeout_limit. However, this value is not actually applied on OpenManage Enterprise Modular.
- ome_device_local_access_configuration - Issue(217865) - The module does not display a proper error message if an unsupported value is provided for the user_defined and lcd_language parameters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module errors out with the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not  exist or is not applicable for the resource URI.``
- ome_device_quick_deploy - Issue(216352) - The module does not display a proper error message if an unsupported value is provided for the ipv6_prefix_length and vlan_id parameters.
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

v5.0.0
======

Release Summary
---------------

HTTPS SSL support for all modules and quick deploy settings.

Major Changes
-------------

- All modules now support SSL over HTTPS and socket level timeout.

Breaking Changes / Porting Guide
--------------------------------

- HTTPS SSL certificate validation is a **breaking change** and will require modification in the existing playbooks. Please refer to `SSL Certificate Validation <https://github.com/dell/dellemc-openmanage-ansible-modules#ssl-certificate-validation>`_ section in the `README.md <https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/README.md#SSL-Certificate-Validation>`_ for modification to existing playbooks.

Bugfixes
--------

- idrac_bios - The issue while configuring boot sources is fixed (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/347)

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_local_access_configuration - Issue(215035) - The module reports ``Successfully updated the local access setting`` if an unsupported value is provided for the parameter timeout_limit. However, this value is not actually applied on OpenManage Enterprise Modular.
- ome_device_local_access_configuration - Issue(217865) - The module does not display a proper error message if an unsupported value is provided for the user_defined and lcd_language parameters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module errors out with the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not  exist or is not applicable for the resource URI.``
- ome_device_quick_deploy - Issue(216352) - The module does not display a proper error message if an unsupported value is provided for the ipv6_prefix_length and vlan_id parameters.
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_device_quick_deploy - Configure Quick Deploy settings on OpenManage Enterprise Modular

v4.4.0
======

Release Summary
---------------

Support to configure login security, session inactivity timeout, and local access settings.

Minor Changes
-------------

- ome_firmware - The module is enhanced to support check mode and idempotency (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/274)
- ome_template - An example task is added to create a compliance template from reference device (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/339)

Bugfixes
--------

- ome_device_location - The issue that applies values of the location settings only in lowercase is fixed (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/341)

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_local_access_configuration - Issue(215035) - The module reports ``Successfully updated the local access setting`` if an unsupported value is provided for the parameter timeout_limit. However, this value is not actually applied on OpenManage Enterprise Modular.
- ome_device_local_access_configuration - Issue(217865) - The module does not display a proper error message if an unsupported value is provided for the user_defined and lcd_language parameters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module errors out with the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not  exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_application_network_settings - This module allows you to configure the session inactivity timeout settings
- dellemc.openmanage.ome_application_security_settings - Configure the login security properties
- dellemc.openmanage.ome_device_local_access_configuration - Configure local access settings on OpenManage Enterprise Modular

v4.3.0
======

Release Summary
---------------

Support to configure network services, syslog forwarding, and SMTP settings.

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module errors out with the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not  exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_application_alerts_smtp - This module allows to configure SMTP or email configurations
- dellemc.openmanage.ome_application_alerts_syslog - Configure syslog forwarding settings on OpenManage Enterprise and OpenManage Enterprise Modular
- dellemc.openmanage.ome_device_network_services - Configure chassis network services settings on OpenManage Enterprise Modular

v4.2.0
======

Release Summary
---------------

Support to configure OME Modular devices network, power, and location settings.

Known Issues
------------

- idrac_user - Issue(192043) Module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_device_power_settings - Issue(212679) The ome_device_power_settings module errors out with the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not  exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_device_location - Configure device location settings on OpenManage Enterprise Modular
- dellemc.openmanage.ome_device_mgmt_network - Configure network settings of devices on OpenManage Enterprise Modular
- dellemc.openmanage.ome_device_power_settings - Configure chassis power settings on OpenManage Enterprise Modular

v4.1.0
======

Release Summary
---------------

Support for Redfish event subscriptions and enhancements to ome_firmware module.

Major Changes
-------------

- ome_firmware - Added option to stage the firmware update and support for selecting components and devices for baseline-based firmware update.

Minor Changes
-------------

- ome_template_network_vlan - Enabled check_mode support.

Known Issues
------------

- idrac_user - Issue(192043) Module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_smart_fabric_uplink - Issue(186024) ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.redfish_event_subscription - Manage Redfish Subscriptions

v4.0.0
======

Release Summary
---------------

Support for configuring active directory user group on OpenManage Enterprise and OpenManage Enterprise Modular.

Known Issues
------------

- idrac_user - Issue(192043) Module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_smart_fabric_uplink - Issue(186024) ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though this is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_active_directory - Configure Active Directory groups to be used with Directory Services on OpenManage Enterprise and OpenManage Enterprise Modular
- dellemc.openmanage.ome_domain_user_groups - Create, modify, or delete an Active Directory user group on OpenManage Enterprise and OpenManage Enterprise Modular

v3.6.0
======

Release Summary
---------------

Support for configuring device slot name and export SupportAssist device collections from OpenManage Enterprise and OpenManage Enterprise Modular.

Bugfixes
--------

- dellemc_idrac_storage_volume - Module fails if the BlockSize, FreeSize, or Size state of the physical disk is set to "Not Available".

Known Issues
------------

- idrac_user - Issue(192043) Module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_smart_fabric_uplink - Issue(186024) ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though this is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_chassis_slots - Rename sled slots on OpenManage Enterprise Modular
- dellemc.openmanage.ome_diagnostics - Export technical support logs(TSR) to network share location

v3.5.0
======

Release Summary
---------------

Support for managing static device groups on OpenManage Enterprise.

Major Changes
-------------

- idrac_server_config_profile - Added support for exporting and importing Server Configuration Profile through HTTP/HTTPS share.
- ome_device_group - Added support for adding devices to a group using the IP addresses of the devices and group ID.

Bugfixes
--------

- Handled invalid share and unused imports cleanup for iDRAC modules (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/268)

Known Issues
------------

- idrac_user - Issue(192043) Module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_smart_fabric_uplink - Issue(186024) ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though this is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_groups - Manages static device groups on OpenManage Enterprise

v3.4.0
======

Release Summary
---------------

OpenManage Enterprise firmware baseline and firmware catalog modules updated to support checkmode.

Major Changes
-------------

- ome_firmware_baseline - Module supports check mode, and allows the modification and deletion of firmware baselines.
- ome_firmware_catalog - Module supports check mode, and allows the modification and deletion of firmware catalogs.

Minor Changes
-------------

- ome_firmware_catalog - Added support for repositories available on the Dell support site.
- ome_template_network_vlan - Added the input option which allows to apply the modified VLAN settings immediately on the associated modular-system servers.

Known Issues
------------

- idrac_user - Issue(192043) Module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_smart_fabric_uplink - Issue(186024) ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though this is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

v3.3.0
======

Release Summary
---------------

OpenManage Enterprise device group and device discovery support added

Minor Changes
-------------

- ome_firmware_baseline - Allows to retrieve the device even if it not in the first 50 device IDs

Known Issues
------------

- idrac_user - Issue(192043) Module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_configuration_compliance_info - Issue(195592) Module may error out with the message ``unable to process the request because an error occurred``. If the issue persists, report it to the system administrator.
- ome_smart_fabric - Issue(185322) Only three design types are supported by OpenManage Enterprise Modular but the module successfully creates a fabric when the design type is not supported.
- ome_smart_fabric_uplink - Issue(186024) ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though this is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_device_group - Add devices to a static device group on OpenManage Enterprise
- dellemc.openmanage.ome_discovery - Create, modify, or delete a discovery job on OpenManage Enterprise

v3.2.0
======

Release Summary
---------------

Configuration compliance related modules added

Minor Changes
-------------

- ome_template - Allows to deploy a template on device groups.

Known Issues
------------

- idrac_user - Issue(192043) Module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_configuration_compliance_info - Issue(195592) Module may error out with the message ``unable to process the request because an error occurred``. If the issue persists, report it to the system administrator.
- ome_smart_fabric - Issue(185322) Only three design types are supported by OpenManage Enterprise Modular but the module successfully creates a fabric when the design type is not supported.
- ome_smart_fabric_uplink - Issue(186024) ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though this is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_configuration_compliance_baseline - Create, modify, and delete a configuration compliance baseline and remediate non-compliant devices on OpenManage Enterprise
- dellemc.openmanage.ome_configuration_compliance_info - Device compliance report for devices managed in OpenManage Enterprise

v3.1.0
======

Release Summary
---------------

OpenManage Enterprise profiles management support added.

Bugfixes
--------

- ome_firmware_baseline_compliance_info - OMEnt firmware baseline compliance info pagination support added (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/171)
- ome_network_proxy - OMEnt network proxy check mode support added (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/187)

Known Issues
------------

- ome_smart_fabric - Issue(185322) Only three design types are supported by OpenManage Enterprise Modular but the module successfully creates a fabric when the design type is not supported.
- ome_smart_fabric_uplink - Issue(186024) ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though this is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_profile - Create, modify, delete, assign, unassign and migrate a profile on OpenManage Enterprise

v3.0.0
======

Release Summary
---------------

Deprecations, issue fixes, and standardization of modules as per ansible guidelines.

Major Changes
-------------

- Removed the existing deprecated modules.

Minor Changes
-------------

- Coding Guidelines, Contributor Agreement, and Code of Conduct files are added to the collection.
- New deprecation changes for ``dellemc_get_system_inventory`` and ``dellemc_get_firmware_inventory`` ignored for ansible 2.9 sanity test.
- The modules are standardized as per ansible guidelines.

Deprecated Features
-------------------

- The ``dellemc_get_firmware_inventory`` module is deprecated and replaced with ``idrac_firmware_info``.
- The ``dellemc_get_system_inventory`` module is deprecated and replaced with ``idrac_system_info``.

Bugfixes
--------

- GitHub issue fix - Module dellemc_idrac_storage_volume.py broken. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/212)
- GitHub issue fix - ome_smart_fabric Fabric management is not supported on the specified system. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/179)
- Known issue fix #187956: If an invalid job_id is provided, the idrac_lifecycle_controller_job_status_info module returns an error message with the description of the issue.
- Known issue fix #188267: No error message is displayed when the target iDRAC with firmware version less than 3.30.30.30 is updated.
- Sanity fixes as per ansible guidelines to all modules.

Known Issues
------------

- Issue 1(186024): ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though this is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

v2.1.5
======

Release Summary
---------------

The idrac_firmware module is enhanced to include checkmode support and job tracking.

Minor Changes
-------------

- The idrac_server_config_profile module supports IPv6 address format.

Bugfixes
--------

- Identity pool does not reset when a network VLAN is added to a template in the ome_template_network_vlan module. `#169 <https://github.com/dell/dellemc-openmanage-ansible-modules/issues /169>`_
- Missing parameter added in ome_smart_fabric_uplink module documenation. `#181 <https://github.com/dell/dellemc-openmanage-ansible-modules/issues/181>`_

Known Issues
------------

- Issue 1(186024): ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though this is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.
- Issue 2(187956): If an invalid job_id is provided, idrac_lifecycle_controller_job_status_info returns an error message. This error message does not contain information about the exact issue with the invalid job_id.
- Issue 3(188267): While updating the iDRAC firmware, the idrac_firmware module completes execution before the firmware update job is completed. An incorrect message is displayed in the task output as 'DRAC WSMAN endpoint returned HTTP code '400' Reason 'Bad Request''. This issue may occur if the target iDRAC firmware version is less than 3.30.30.30

v2.1.4
======

Release Summary
---------------

Fabric management related modules ome_smart_fabric and ome_smart_fabric_uplink are added.

Known Issues
------------

- Issue 1(186024): ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though this is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_smart_fabric - Create, modify or delete a fabric on OpenManage Enterprise Modular
- dellemc.openmanage.ome_smart_fabric_uplink - Create, modify or delete a uplink for a fabric on OpenManage Enterprise Modular

v2.1.3
======

Release Summary
---------------

Network configuration service related modules ome_network_vlan, ome_network_port_breakout and ome_network_vlan_info are added.

New Modules
-----------

- dellemc.openmanage.ome_network_port_breakout - This module allows to automate the port portioning or port breakout to logical sub ports
- dellemc.openmanage.ome_network_vlan - Create, modify & delete a VLAN
- dellemc.openmanage.ome_network_vlan_info - Retrieves the information about networks VLAN(s) present in OpenManage Enterprise

v2.1.2
======

Release Summary
---------------

The dellemc_change_power_state and dellemc_configure_idrac_users modules are standardized as per ansible guidelines. 8 GitHub issues are fixed.

Minor Changes
-------------

- The idrac_server_config_profile module supports a user provided file name for an export operation.

Deprecated Features
-------------------

- The dellemc_change_power_state module is deprecated and replaced with the redfish_powerstate module.
- The dellemc_configure_idrac_users module is deprecated and replaced with the idrac_user module.

Bugfixes
--------

- Documentation improvement request `#140 <https://github.com/dell/dellemc-openmanage-ansible-modules/issues/140>`_
- Executing dellemc_configure_idrac_users twice fails the second attempt `#100 <https://github.com/dell/dellemc-openmanage-ansible-modules/issues/100>`_
- dellemc_change_power_state fails if host is already on `#132 <https://github.com/dell/dellemc-openmanage-ansible-modules/issues/132>`_
- dellemc_change_power_state not idempotent `#115 <https://github.com/dell/dellemc-openmanage-ansible-modules/issues/115>`_
- dellemc_configure_idrac_users error `#26 <https://github.com/dell/dellemc-openmanage-ansible-modules/issues/26>`_
- dellemc_configure_idrac_users is unreliable - errors `#113 <https://github.com/dell/dellemc-openmanage-ansible-modules/issues/113>`_
- idrac_server_config_profile improvement requested (request) `#137 <https://github.com/dell/dellemc-openmanage-ansible-modules/issues/137>`_
- ome_firmware_catalog.yml example errors `#145 <https://github.com/dell/dellemc-openmanage-ansible-modules/issues/145>`_

New Modules
-----------

- dellemc.openmanage.idrac_user - Configure settings for user accounts
- dellemc.openmanage.redfish_powerstate - Manage device power state

v2.1.1
======

Release Summary
---------------

Support for OpenManage Enterprise Modular and other enhancements.

Major Changes
-------------

- Standardization of ten iDRAC ansible modules based on ansible guidelines.
- Support for OpenManage Enterprise Modular.

Deprecated Features
-------------------

- The dellemc_configure_bios module is deprecated and replaced with the idrac_bios module.
- The dellemc_configure_idrac_network module is deprecated and replaced with the idrac_network module.
- The dellemc_configure_idrac_timezone module is deprecated and replaced with the idrac_timezone_ntp module.
- The dellemc_delete_lc_job and dellemc_delete_lc_job_queue modules are deprecated and replaced with the idrac_lifecycle_controller_jobs module.
- The dellemc_export_lc_logs module is deprecated and replaced with the idrac_lifecycle_controller_logs module.
- The dellemc_get_lc_job_status module is deprecated and replaced with the idrac_lifecycle_controller_job_status_info module.
- The dellemc_get_lcstatus module is deprecated and replaced with the idrac_lifecycle_controller_status_info module.
- The dellemc_idrac_reset module is deprecated and replaced with the idrac_reset module.
- The dellemc_setup_idrac_syslog module is deprecated and replaced  with the idrac_syslog module.

New Modules
-----------

- dellemc.openmanage.idrac_bios - Configure the BIOS attributes
- dellemc.openmanage.idrac_lifecycle_controller_job_status_info - Get the status of a Lifecycle Controller job
- dellemc.openmanage.idrac_lifecycle_controller_jobs - Delete the Lifecycle Controller Jobs
- dellemc.openmanage.idrac_lifecycle_controller_logs - Export Lifecycle Controller logs to a network share or local path.
- dellemc.openmanage.idrac_lifecycle_controller_status_info - Get the status of the Lifecycle Controller
- dellemc.openmanage.idrac_network - Configures the iDRAC network attributes
- dellemc.openmanage.idrac_reset - Reset iDRAC
- dellemc.openmanage.idrac_syslog - Enable or disable the syslog on iDRAC
- dellemc.openmanage.idrac_timezone_ntp - Configures time zone and NTP on iDRAC

v2.1.0
======

Release Summary
---------------

The `Dell OpenManage Ansible Modules <https://github.com/dell/dellemc-openmanage-ansible-modules>`_ are available on Ansible Galaxy as a collection.
