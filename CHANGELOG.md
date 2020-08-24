# Dell EMC OpenManage Ansible Modules

Dell EMC OpenManage Ansible Modules allows data center and IT administrators to use RedHat Ansible to automate and orchestrate the configuration, deployment, and update of Dell EMC PowerEdge Servers and modular infrastructure by leveraging the management automation capabilities in-built into the Integrated Dell Remote Access Controller (iDRAC), OpenManage Enterprise and OpenManage Enterprise Modular.

OpenManage Ansible Modules simplifies and automates provisioning, deployment, and updates of PowerEdge servers and modular infrastructure. It allows system administrators and software developers to introduce the physical infrastructure provisioning into their software provisioning stack, integrate with existing DevOps pipelines and manage their infrastructure using version-controlled playbooks, server configuration profiles, and templates in line with the Infrastructure-as-Code (IaC) principles.

# 2.1.1 (August 26, 2020)
  
  * Support for OpenManage Enterprise-Modular.
  
  * The dellemc_idrac_reset module is deprecated and replaced with the idrac_reset module.
  
  * The dellemc_setup_idrac_syslog module is deprecated and replaced with the idrac_syslog module.
  
  * The dellemc_get_lcstatus module is deprecated and replaced with the idrac_lifecycle_controller_status_info module.
  
  * The dellemc_get_lc_job_status module is deprecated and replaced with the idrac_lifecycle_controller_job_status_info
    module.
    
  * The dellemc_export_lc_logs module is deprecated and replaced with the idrac_lifecycle_controller_logs module.
  
  * The dellemc_configure_idrac_timezone module is deprecated and replaced with the idrac_timezone_ntp module.
  
  * The dellemc_configure_bios module is deprecated and replaced with the idrac_bios module.
  
  * The dellemc_configure_idrac_network module is deprecated and replaced with the idrac_network module.
  
  * The dellemc_delete_lc_job and dellemc_delete_lc_job_queue modules are deprecated and replaced with the 
    idrac_lifecycle_controller_jobs module.
  
  * 'examples' and 'samples' directories are renamed to 'playbooks' and 'output' respectively.
  

# 2.0.14 (June 09, 2020)

  * The ome_firmware_baseline_info module allows to view the list of available firmware baselines
  
  * The ome_application_certificate module allows to upload the certificate to OpenManage Enterprise.

# 2.0.13 (May 20, 2020)

  * The domain user authentication issue using a CIFS share in the dellemc_export_lc_logs module is fixed.


# 2.0.12 (May 13, 2020)

  * The ome_identity_pool module allows to create and modify an identity pool
    using FC and iSCSI settings.

  * The ome_application_certificate module allows to generate a certificate
    signing request (CSR).

# 2.0.11 (April 20, 2020)

  * The ome_application_network_webserver module allows the configuration of the network web server.

  * The ome_application_network_time module allows the configuration of network time.
  
  * The module ome_application_network_address is updated to include the following:
	- A specific NIC can be selected in case of multiple NICs,
	- A NIC can be enabled or disabled using the option enable_nic,
	- Support for the configuration of a management vLAN.
   
  * The module idrac_firmware is enhanced to support FQDN input format for
   share details.

# 2.0.10 (March 27, 2020)

  * The new OME module(ome_application_network_proxy) allows to configure a
   network proxy

  * The new OME module(ome_application_network_address) allows to configure the
   DNS and an IPv4 or IPv6 network

# 2.0.9 (March 05, 2020)

  * The option group_names in the ome_firmware_baseline and ome_firmware_baseline_compliance_info module is replaced with device_group_names.

  * The ome_firmware module allows firmware updates using a single DUP path and a baseline name.

  * The module ome_identity_pool is updated to delete an identity pool.
   
  * The new OME module(ome_template_identity_pool) allows to 
    - attach an identity pool to a template
    - detach an identity pool from a template

  * The ome_template_network_vlan module lets you select tagged and untagged VLANs to be used in the OME template. 
  
  * The installation and uninstallation scripts have been updated to display 
  the path where the modules have been installed.
  
  * Success and failure messages in the scripts now appear in green and red.


# 2.0.8 (February 07, 2020)

  * The ome_firmware module allows firmware updates using a baseline name.

  * The new OME module (ome_identity_pool) allows to create and modify an identity pool using ethernet and FCoE settings.

# 2.0.7 (January 16, 2020)

  * The module ome_template is updated to include delete, clone, import and export operations.

  * The dellemc_ome_firmware module is deprecated, and replaced with the ome_firmware module.
  
  * The ome_firmware module now supports firmware updates for groups of devices.

  * The unreachable option in the ansible play recap is enabled for the ome_template and ome_firmware module. This option allows to identify the number of hosts that were unreachable during a run.

# 2.0.6 (December 20, 2019)
  
  * In the ome_device_info module, fixed the issue that is encountered with the device inventory when the device count is more than 50.

# 2.0.5 (December 13, 2019)

  * OpenManage Ansible now allows the use of standard redfish URIs supported by iDRAC. 
    
    - The module (redfish_firmware) performs a component firmware update using an image file available on the local or remote system
    - The module (redfish_storage_volume) manages the storage volume configuration.
  
  * The iDRAC module (idrac_redfish_storage_controller) configures the settings of a storage controller.

# 2.0.4 (November 8, 2019)

  * A new OpenManage Enterprise(OME) module (ome_firmware_catalog) to
    create a firmware catalog.
  
  * A new OME module (ome_firmware_baseline) to create a firmware baseline
   from existing catalog.
  
  * A new OME module (ome_firmware_baseline_compliance_info) to retrieve:
  
    - Firmware compliance report for specified identifiers (device ids, service tags, group names).
    - Baseline compliance reports for specified baseline.

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
