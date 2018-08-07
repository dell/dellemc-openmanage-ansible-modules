# Dell EMC OpenManage Ansible Modules

Dell EMC OpenManage Ansible Modules allows Data Center and IT administrators to use RedHat Ansible to automate and orchestrate the configuration, deployment, and update of Dell EMC PowerEdge Servers (12th generation of PowerEdge servers and later) by leveraging the management automation capabilities in-built into the integrated Dell Remote Access Controller (iDRAC).

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
