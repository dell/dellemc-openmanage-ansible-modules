# Dell EMC OpenManage Ansible Modules

Dell EMC OpenManage Ansible Modules allows Data Center and IT administrators to use RedHat Ansible to automate and orchestrate the configuration, deployment, and update of Dell EMC PowerEdge Servers (12th generation of PowerEdge servers and later) by leveraging the management automation capabilities in-built into the integrated Dell Remote Access Controller (iDRAC).

With the latest release of Dell EMC OpenManage Ansible Modules, the capabilities have improved with support for OpenManage Enterprise. OpenManage Ansible Modules allows users to retrieve device inventory information of each device discovered in the OpenManage Enterprise.

# 2.0.3 (October 16, 2019)

  * The following enhancements have been made to the idrac_firmware module:

    - Support for installing firmware from HTTP/HTTPS/FTP based repository.
    - Support for viewing individual component update job ids.
    - The apply_update option is added, which specifies if the packages from the Catalog XML are queued for update.
    - The ignore_cert_warning option is added, which specifies if certificate warnings must be ignored.

  * The following enhancements have been made to the installation script:

    - All the modules present by default in the remote_management/dellemc folder are now overwritten with updated versions.
    - Modules will be installed to the custom path, if it is set by the environment variable ANSIBLE_LIBRARY.
    - The default python interpreter is now located using #!/usr/bin/env python instead of #!/usr/bin/python.
    
# 2.0.2 (September 21, 2019)

  * The dellemc_ome_template module is deprecated and all the functionality are added to the new ome_template module.

  * The dellemc_ome_user_facts module is deprecated and all the functionality are added to the new ome_user_info module.

  * The dellemc_boot_to_network_iso module is deprecated and all the functionality are added to the new idrac_os_deployment module.

  * Support custom interval (default is 18 hours) for auto-detaching an ISO image for idrac_os_deployment.

  * The ome_template_info and ome_user_info modules are enhanced to filter records using name in system_query_options.

  * Support to modify or deploy template using parameter template_name in ome_template module.

  * Support to delete an existing user account, using name in ome_user module.

# 2.0.1 (June 6, 2019)

  * idrac_firmware and idrac_server_config_profile modules are added.

  * dellemc_idrac_firmware and dellemc_idrac_server_config_profile modules are deprecated.

# 2.0 (May 3, 2019)

  * Create, modify or delete a user account using a new OME module (ome_user).

  * A new OME module (ome_power_state) to perform the power management operations.

# 1.4 (March 28, 2019)

  * A new OME module (dellemc_ome_template_facts) to retrieve template details.

  * A new OME module (dellemc_ome_user_facts) to retrieve account details.
  
  * A new OME module (dellemc_ome_template) to create, modify and deploy templates.

# 1.3 (March 5, 2019)

  * dellemc_export_server_config_profile and 
  dellemc_import_server_config_profile modules are deprecated.
  
  * dellemc_idrac_server_config_profile is added.

  * A new OME module (dellemc_ome_job_facts) to view or track job details of 
  PowerEdge devices managed by OME.

  * A new OME module (dellemc_ome_firmware) to update the firmware of PowerEdge 
  devices and all its components.


# 1.2 (February 12, 2019)

  * dellemc_install_firmware module is deprecated.

  * A new and rich OME module (dellemc_ome_device_facts) to retrieve the list
  of all devices with the exhaustive inventory of each device.


# 1.1 (November 14, 2018)

  * New and updated playbook examples.

  * Support RAID volume creation on BOSS Controller.

  * "share_name" option made optional in dellemc_configure_bios module.


# 1.0.4 (October 1, 2018)

  * dellemc_configure_bios module enhancement. 
  Added "attributes" and "boot_sources" options.
  Existing BIOS configuration options are marked for deprecation.

  * Option name modification and defect fixes for 
  dellemc_idrac_storage_volume module.
  
  * Option "catalog_file_name" is added in dellemc_install_firmware module
  to support custom catalogs.
  
  
# 1.0.3 (August 7, 2018)

  * dellemc_idrac_storage_volume is added in the list of modules.

  * Check_mode support for modules is enabled.

  * dellemc_configure_raid module is deprecated.


# 1.0.2 (June 11, 2018)
  
  * Export a server configuration profile (SCP) of Basic Input Output System (BIOS),
  Redundant Array of Independent Disks (RAID), Network Interface Controller (NIC),
  and so on, to a local file path or a network share.

  * Import a server configuration profile SCP from a local file path or 
  a network share.

  * Support for configuration of BIOS, integrated Dell Remote Access Controller
 (iDRAC), NIC, and RAID.
  
  * Support for firmware update.
  
  * Support for viewing firmware inventory details. 
  
  * Support for Boot to OS installation media from network location.

  * Support for configuring power controls, resetting iDRAC, 
  viewing LC (LC) job status, deleting LC job, deleting LC job queue,
  exporting LC logs, and configuring system lockdown mode. 
  
  * Retrieve the system inventory details.
