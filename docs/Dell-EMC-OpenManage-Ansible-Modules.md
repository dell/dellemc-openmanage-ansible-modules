# Dell EMC OpenManage Ansible Modules for iDRAC (BETA)

## 1. Introduction

Dell EMC OpenManage Ansible Modules provide customers the ability to automate the Out-of-Band configuration management, deployment and updates for Dell EMC PowerEdge Servers using Ansible by leeveragin the management automation built into the iDRAC with Lifecycle Controller. iDRAC provides both REST APIs based on DMTF RedFish industry standard and WS-Management (WS-MAN) for management automation of PowerEdge Servers.

With OpenManage Ansible modules, you can do:
  * Server administration
  * Configure iDRAC's settings such as:
    * iDRAC Network Settings
    * SNMP and SNMP Alert Settings
    * Timezone and NTP Settings
    * System settings such as server topology
    * LC attributes such as CSIOR etc.
  * Perform User administration
  * BIOS and Boot Order configuration
  * RAID Configuration
  * OS Deployment
  * Firmware Updates

### 1.1 How OpenManage Ansible Modules work?

OpenManage Ansible modules extensively uses the Server Configuration Profile (SCP) for most of the configuration management, deployment and update of PowerEdge Servers. Lifecycle Controller 2 version 1.4 and later adds support for SCP. A SCP contains all BIOS, iDRAC, Lifecycle Controller, Network amd Storage settings of a PowerEdge server and can be applied to multiple servers, enabling rapid, reliable and reproducible configuration.

A SCP operation can be performed using any of the following methods:
  * Export/Import to/from a remote network share via CIFS, NFS
  * Export/Import to/from a remote network share via HTTP, HTTPS (iDRAC firmware 3.00.00.00 and above)
  * Export/Import to/from via local file streaming (iDRAC firmware 3.00.00.00 and above)

**NOTE**: This BETA release of OpenManage Ansible Module supports only the first option listed above for SCP operations i.e. export/import from/to a remote network share via CIFS or NFS. Future releases will support all the options for SCP operations.

#### Setting up a local mount point for a remote network share

Since OpenManage Ansible modules extensively uses SCP to automate and orchestrate configuration, deployment and update on PowerEdge servers, you must locally mount the remote network share (CIFS or NFS) on the ansible server where you will be executing the playbook or modules. Local mount point also should have read-write privileges in order for OpenManage Ansible modules to write a SCP file to remote network share that will be imported by iDRAC.

You can use either of the following ways to setup a local mount point:

  * Use the ```mount``` command to mount a remote network share

    ```
    # Mount a remote CIFS network share on the local ansible machine.
    # In the below command, 192.168.10.10 is the IP address of the CIFS file
    # server (you can provide a hostname as well), Share is the directory that
    # is being shared, and /mnt/CIFS is the location to mount the file system
    # on the local ansible machine
    sudo mount -t cifs \\\\192.168.10.10\\Share -o username=user1,password=password,dir_mode=0777,file_mode=0666 /mnt/CIFS

    # Mount a remote NFS network share on the local ansible machine.
    # In the below command, 192.168.10.10 is the IP address of the NFS file
    # server (you can provide a hostname as well), Share is the directory that
    # is being exported, and /mnt/NFS is the location to mount the file system
    # on the local ansible machine. Please note that NFS checks access
    # permissions against user ids (UIDs). For granting the read-write
    # privileges on the local mount point, the UID and GID of the user on your
    # local ansible machine needs to match the UID and GID of the owner of the
    # folder you are trying to access on the server. Other option for granting
    # the rw privileges would be to use all_squash option.

    sudo mount -t nfs 192.168.10.11:/Share /mnt/NFS -o rw,user,auto
    ```

  * Alternate and preferred way would be to use the ```/etc/fstab``` for mounting the remote network share. That way, you won’t have to mount the network share after a reboot and remember all the options.  General syntax for mounting the network share in ```/etc/fstab``` would be as follows:

    ```
    # Mounting a CIFS network share:
    //192.168.10.10/Share /mnt/CIFS cifs username=user,password=pwd,domain=domain_name,dir_mode=0777,file_mode=0666,iocharset=utf8 0 0

    # Mounting a NFS network share:
    192.168.10.11:/Share /mnt/NFS nfs rw,user,auto 0 0
    ```

---
### 1.2 What is included in this BETA release?

|Use Cases| | Included in this BETA release |
|---------|-|-------------------------------|
| Protocol Support | | <ul><li>WS-Management</li></ul> |
| Server Administration | Power and Thermal | <ul><li>Power Control</li></ul>|
| | iDRAC Reset| <ul><li>Yes</li></ul> |
|iDRAC Configuration| User and Password Management | <ul><li>Local user and password management<ul><li>Create User</li><li>Change Password</li><li>Change User Privileges</li><li>Remove an user</li></ul></li></ul> |
| | iDRAC Network Configuration | <ul><li>NIC Selection</li><li>Zero-Touch Auto-Config settings</li><li>IPv4 Address settings:<ul><li>Enable/Disable IPv4</li><li>Static IPv4 Address settings (IPv4 address, gateway and netmask)</li><li>Enable/Disable DNS from DHCP</li><li>Preferred/Alternate DNS Server</li></ul></li><li>VLAN Configuration</li></ul> |
| | SNMP and SNMP Alert Configuration| <ul><li>SNMP Agent configuration</li><li>SNMP Alert Destination Configuration<ul><li>Add, Modify and Delete an alert destination</li></ul></li></ul> |
| | Server Configuration Profile (SCP) | <ul><li>Export SCP to remote network share (CIFS, NFS)</li><li>Import SCP from a remote network share (CIFS, NFS)</li></ul> |
| | iDRAC Services | <ul><li>iDRAC Web Server configuration<ul><li>Enable/Disable Web server</li><li>TLS protocol version</li><li>SSL Encryption Bits</li><li>HTTP/HTTPS port</li><li>Time out period</li></ul></li></ul> |
| | Lifecycle Controller (LC) attributes | <ul><li>Enable/Disable CSIOR (Collect System Inventory on Restart)</li></ul> |
| BIOS Configuration | Boot Order Settings | <ul><li>Change Boot Mode (Bios, Uefi)</li><li>Change Bios/Uefi Boot Sequence</li><li>One-Time Bios/Uefi Boot Configuration settings</li></ul> |
| Deployment | OS Deployment | <ul><li>OS Deployment from: <ul><li>Remote Network Share (CIFS, NFS)</li></ul></li></ul> |
| Storage | Virtual Drive | <ul><li>Create and Delete virtual drives</li></ul> |
| Update | Firmware Update | <ul><li>Firmware update from:<ul><li>Remote network share (CIFS, NFS)</li></ul></li></ul> |
| Monitor | Logs | <ul><li>Export Lifecycle Controller (LC) Logs to:<ul><li>Remote network share (CIFS, NFS)</li></ul></li><li>Export Tech Support Report (TSR) to:<ul><li>Remote network share (CIFS, NFS)</li></ul></li></ul> |

---
## 2. Requirements

  * Ansible >= '2.3'
  * Python >= '2.7.9'
  * [Dell EMC OpenManage Python SDK](https://github.com/vaideesg/omsdk)

---
## 3. Modules

OpenManage Ansible modules can be broadly categorized under the following sections. Each section describes the modules that are currently implemented including examples.

## 3.1 Server Administration

### Power Control

  * [dellemc_idrac_power - Configure the Power Control options on a PowerEdge Server](./dellemc_idrac_power.md)

### Lifecycle Controller (LC) and Server Status

  * [dellemc_idrac_lcstatus - Returns the lifecycle controller and server status](./dellemc_idrac_lcstatus.md)

### Hardware Inventory

  * [dellemc_idrac_inventory - Returns the PowerEdge Server's hardware inventory](./dellemc_idrac_inventory.md) 

### Firmware Inventory

  * [dellemc_idrac_sw_inventory - Returns the PowerEdge Server's firmware inventory](./dellemc_idrac_sw_inventory.md)

## 3.2 iDRAC Configuration

### User Administration

  * [dellemc_idrac_user - Configure an iDRAC Local User](./dellemc_idrac_user.md)

### iDRAC Network Settings

  * [dellemc_idrac_nic - Configure iDRAC Network Settings](./dellemc_idrac_nic.md)

### SNMP and SNMP Alerts

  * [dellemc_idrac_snmp - Configure SNMP settings on iDRAC](./dellemc_idrac_snmp.md)
  * [dellemc_idrac_snmp_alert - Configure Alert destinations](./dellemc_idrac_snmp_alert.md)

### Server Configuration Profile (SCP)

  * [dellemc_idrac_export_scp - Export Server Configuration Profile (SCP) to Network Share](./dellemc_idrac_export_scp.md)
  * [dellemc_idrac_import_scp - Import Server configuration Profile (SCP) from a Network Share](./dellemc_idrac_import_scp.md)

### Timezone and NTP

  * [dellemc_idrac_timezone_ntp - Configure Time Zone and NTP](./dellemc_idrac_timezone_ntp.md)

### iDRAC Web Server

  * [dellemc_idrac_web_server - Configure iDRAC Web Server Service Interface](./dellemc_idrac_web_server.md)

### Remote Syslog

  * [dellemc_idrac_syslog - Configure Remote System Logging](./dellemc_idrac_syslog.md)

### Lifecycle Controller Job Management

  * [dellemc_idrac_lc_job - Lifecycle controller job management](./dellemc_idrac_lc_job.md)

### Lifecycle Controller Attributes

  * [dellemc_idrac_lc_attr - Configure iDRAC Lifecycle Controller attributes](./dellemc_idrac_lc_attr.md)

## 3.3 BIOS Configuration

### Boot Order

  * [dellemc_idrac_boot_order - Configure BIOS Boot Settings](./dellemc_idrac_boot_order.md)

## 3.4 Storage Configuration

### Virtual Drives

  * [dellemc_idrac_virtual_drive - Create and delete virtual drives](./dellemc_idrac_virtual_drive.md)

## 3.5 OS Deployment

### Boot to Network ISO

  * [dellemc_idrac_boot_to_nw_iso - Boot to a Network ISO image](./dellemc_idrac_boot_to_nw_iso.md)

## 3.6 Firmware Update

### Update Firmware from a Network Share

  * [dellemc_idrac_firmware_update - Update firmware from a network share](./dellemc_idrac_firmware_update.md)

## 3.7 Monitor 

### Lifecycle Controller Logs

  * [dellemc_idrac_export_lclog - Export Lifecycle Controller log file to a network share](./dellemc_idrac_export_lclog.md)

### Tech Support Report (TSR)

  * [dellemc_idrac_export_tsr - Export TSR to a network share](./dellemc_idrac_export_tsr.md)


---

Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
