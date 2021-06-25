=================================================
Dell EMC OpenManage Ansible Modules Release Notes
=================================================

.. contents:: Topics


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

- dellemc.openmanage.ome_device_group - Manages device group settings on OpenManage Enterprise
- dellemc.openmanage.ome_discovery - Create, modify or delete a discovery job on OpenManage Enterprise

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

- dellemc.openmanage.ome_configuration_compliance_baseline - Create, modify, delete and remediate a compliance configuration baseline on OpenManage Enterprise
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

- dellemc.openmanage.ome_smart_fabric - Create, modify or delete a fabric on OpenManage Enterprise Modular.
- dellemc.openmanage.ome_smart_fabric_uplink - Create, modify or delete a uplink for a fabric on OpenManage Enterprise Modular.

v2.1.3
======

Release Summary
---------------

Network configuration service related modules ome_network_vlan, ome_network_port_breakout and ome_network_vlan_info are added.

New Modules
-----------

- dellemc.openmanage.ome_network_port_breakout - This module allows to automate the port partitioning or breaking out to logical sub ports.
- dellemc.openmanage.ome_network_vlan - Create, modify & delete a VLAN.
- dellemc.openmanage.ome_network_vlan_info - Retrieves the information about networks VLAN(s) present in OpenManage Enterprise.

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

- dellemc.openmanage.idrac_user - Configure settings for user accounts.
- dellemc.openmanage.redfish_powerstate - Manage device power state.

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

- dellemc.openmanage.idrac_bios - Configure the BIOS attributes.
- dellemc.openmanage.idrac_lifecycle_controller_job_status_info - Get the status of a Lifecycle Controller job.
- dellemc.openmanage.idrac_lifecycle_controller_jobs - Delete the Lifecycle Controller Jobs.
- dellemc.openmanage.idrac_lifecycle_controller_logs - Export Lifecycle Controller logs to a network share.
- dellemc.openmanage.idrac_lifecycle_controller_status_info - Get the status of the Lifecycle Controller.
- dellemc.openmanage.idrac_network - Configures the iDRAC network attributes.
- dellemc.openmanage.idrac_reset - Reset iDRAC.
- dellemc.openmanage.idrac_syslog - Enable or disable the syslog on iDRAC.
- dellemc.openmanage.idrac_timezone_ntp - Configures time zone and NTP on iDRAC.

v2.1.0
======

Release Summary
---------------

The `Dell EMC OpenManage Ansible Modules <https://github.com/dell/dellemc-openmanage-ansible-modules>`_ are available on Ansible Galaxy as a collection.
