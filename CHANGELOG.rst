=================================================
Dell EMC OpenManage Ansible Modules Release Notes
=================================================

.. contents:: Topics


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
