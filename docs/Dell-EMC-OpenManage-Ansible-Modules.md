# Dell EMC OpenManage Ansible Modules for iDRAC

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

### 1.1 What is included in this BETA release?
|Use Cases| | Included in this BETA release | Planned for V1.0 (in addition to BETA features) |
|---------|-|-------------------------------|-------------------------------------------------|
| Protocol Support | | <ul><li>WS-Management</li></ul> | <ul><li>RedFish</li></ul> |
| Server Administration | Power and Thermal | <ul><li>Power Control</li></ul>|<ul><li>Power Configuration - such as power cap policy, power supply options etc.</li></ul>|
| | iDRAC Reset| <ul><li>Yes</li></ul> | <ul><li>Yes</li></ul> |
|iDRAC Configuration| User and Password Management | <ul><li>Local user and password management<ul><li>Create User</li><li>Change Password</li><li>Change User Privileges</li><li><Remove an user</li></ul></li></ul> | <ul><li>Active Directory (AD) support</li><li>LDAP Support</li></ul> |
| | iDRAC Network Configuration | <ul><li>NIC Selection</li><li>Zero-Touch Auto-Config settings</li><li>IPv4 Address settings:<ul><li>Enable/Disable IPv4</li><li>Static IPv4 Address settings (IPv4 address, gateway and netmask)</li><li>Enable/Disable DNS from DHCP</li><li>Preferred/Alternate DNS Server</li></ul></li><li>VLAN Configuration</li></ul> | <ul><li>Same as in BETA release</li></ul> |
| | SNMP and SNMP Alert Configuration| <ul><li>SNMP Agent configuration</li><li>SNMP Alert Destination Configuration<ul><li>Add, Modify and Delete an alert destination</li></ul></li></ul> | <ul><li>Alert and Alerts filter</li><li>Alerts and Remote System Log configuration</li><li>Alert Recurrence configuration</li><li>RedFish Event settings</li></ul> |
| | Server Configuration Profile (SCP) | <ul><li>Export SCP to remote network share (CIFS, NFS)</li><li>Import SCP from a remote network share (CIFS, NFS)</li></ul> | <ul><li>Export SCP to Local, HTTP/HTTPS</li><li>Import SCP from Local, HTTP/HTTPS</li></ul> |
| | iDRAC Services | <ul><li>iDRAC Web Server configuration<ul><li>Enable/Disable Web server</li><li>TLS protocol version</li><li>SSL Encryption Bits</li><li>HTTP/HTTPS port</li><li>Time out period</li></ul></li></ul> | <ul><li>SSH settings</li><li>Telnet settings</li><li>Remote RACADM Services</li><li>VNC Server</li></ul> |
| | Lifecycle Controller (LC) attributes | <ul><li>Enable/Disable CSIOR (Collect System Inventory on Restart)</li></ul> | <ul><li>Same as in BETA</li></ul>|
| BIOS Configuration | Boot Order Settings | <ul><li>Change Boot Mode (Bios, Uefi)</li><li>Change Bios/Uefi Boot Sequence</li><li>One-Time Bios/Uefi Boot Configuration settings</li></ul> | |
| | Secure Boot Configuration | <ul><li>Not available in BETA</li></ul> | <ul><li>Yes</li></ul> |
| Deployment | OS Deployment | <ul><li>OS Deployment from: <ul><li>Remote Network Share (CIFS, NFS)</li></ul></li></ul> | <ul><li>OS Deployment from:<ul><li>Virtual Media</li><li>SD Card</li></ul></li></ul> | |
| Storage | Virtual Drive | <ul><li>Create and Delete virtual drives</li></ul> | <ul><li>Same as in BETA release</li></ul> |
| Update | Firmware Update | <ul><li>Firmware update from:<ul><li>Remote network share (CIFS, NFS)</li></ul></li></ul> | <ul><li>Same as in BETA release</li></ul> |
| Monitor | Logs | <ul><li>Export Lifecycle Controller (LC) Logs to:<ul><li>Remote network share (CIFS, NFS)</li></ul></li><li>Export Tech Support Report (TSR) to:<ul><li>Remote network share (CIFS, NFS)</li></ul></li></ul> | <ul><li>Same as in BETA release</li></ul> |

---
## 2. Requirements
* python >= '2.7'
* [Dell EMC OpenManage Python SDK](https://github.com/vaideesg/omsdk)

---
## 3. Modules
Following is the list of OpenManage Ansible Modules:

### 3.1 

  * [dellemc_idrac_boot_to_nw_iso - boot to a network iso image](#dellemc_idrac_boot_to_nw_iso)
  * [dellemc_idrac_import_scp - import scp from a network share](#dellemc_idrac_import_scp)
  * [dellemc_idrac_boot_order - configure bios boot settings](#dellemc_idrac_boot_order)
  * [dellemc_idrac_nic - configure idrac network settings](#dellemc_idrac_nic)
  * [dellemc_idrac_export_scp - export server configuration profile (scp) to network share](#dellemc_idrac_export_scp)
  * [dellemc_idrac_syslog - configure remote system logging](#dellemc_idrac_syslog)
  * [dellemc_idrac_lc_attr - configure idrac lifecycle controller attributes](#dellemc_idrac_lc_attr)
  * [dellemc_idrac_export_tsr - export tsr logs to a network share](#dellemc_idrac_export_tsr)
  * [dellemc_idrac_firmware_update - Update firmware from a network share (cifs, nfs)](#dellemc_idrac_firmware_update)
  * [dellemc_idrac_export_lclog - export lifecycle controller log file to a network share](#dellemc_idrac_export_lclog)
  * [dellemc_idrac_power - configure the power cycle options on poweredge server](#dellemc_idrac_power)
  * [dellemc_idrac_lc_job - get the status of a lifecycle controller job, delete a lc job](#dellemc_idrac_lc_job)
  * [dellemc_idrac_user - configures an idrac local user](#dellemc_idrac_user)
  * [dellemc_idrac_sw_inventory - get firmware inventory](#dellemc_idrac_sw_inventory)
  * [dellemc_idrac_timezone_ntp - configure time zone and ntp settings](#dellemc_idrac_timezone_ntp)
  * [dellemc_idrac_snmp - configure snmp settings on idrac](#dellemc_idrac_snmp)
  * [dellemc_idrac_web_server - configure idrac web server service interface settings](#dellemc_idrac_web_server)
  * [dellemc_idrac_lcstatus - returns the lifecycle controller status](#dellemc_idrac_lcstatus)
  * [dellemc_idrac_inventory - returns the poweredge server hardware inventory](#dellemc_idrac_inventory)

---

## dellemc_idrac_boot_to_nw_iso
Boot to a network ISO image

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Boot to a network ISO image. Reboot appears to be immediate

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  Network file share (either CIFS or NFS)  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| iso_image  |   yes  |  | |  Path to ISO image relative to the I(share_name)  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share specified in I(share_name) with read-write permission for ansible user  |
| share_user  |   yes  |  | |  Network share user in the format 'user@domain' if user is part of a domain else 'user'  |
| idrac_pwd  |   no  |  | |  iDRAC user password  |
| job_wait  |   no  |  True  | |  |


 
#### Examples

```
- name: Boot to Network ISO
    dellemc_idrac_boot_to_nw_iso:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      iso_image:  "uninterrupted_os_installation_image.iso"

```


---


## dellemc_idrac_import_scp
Import SCP from a network share

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Import a given Server Configuration Profile (SCP) file from a network share

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| scp_file  |   yes  |    | |  Server Configuration Profile file name relative to I(share_mnt)  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  Network file share (either CIFS or NFS)  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| scp_components  |   no  |  ALL  | <ul> <li>ALL</li>  <li>IDRAC</li>  <li>BIOS</li>  <li>NIC</li>  <li>RAID</li> </ul> |  if C(ALL), will import all components configurations from SCP file  if C(IDRAC), will import iDRAC comfiguration from SCP file  if C(BIOS), will import BIOS configuration from SCP file  if C(NIC), will import NIC configuration from SCP file  if C(RAID), will import RAID configuration from SCP file  |
| reboot  |   no  |  False  | |  Reboot after importing the SCP  |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share specified in I(share_name) with read-write permission for ansible user  |
| share_user  |   yes  |  | |  Network share user in the format 'user@domain' if user is part of a domain else 'user'  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| job_wait  |   no  |  True  | |  if C(True), wait for the import scp job to be completed and return the status  if C(False), return immediately after creating a import scp job  |


 
#### Examples

```
# Import Server Configuration Profile from a CIFS Network Share
- name: Import Server Configuration Profile
    dellemc_idrac_import_scp:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      scp_file:   "scp_file.xml"
      scp_components: "ALL"
      reboot:      False

# Import Server Configuration Profile from a NFS Network Share
- name: Import Server Configuration Profile
    dellemc_idrac_import_scp:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "192.168.10.10:/share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      scp_file:   "scp_file.xml"
      scp_components: "ALL"
      reboot:      False

```



---


## dellemc_idrac_boot_order
Configure BIOS Boot Settings

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Configure Bios/Uefi Boot Settings
 Changing the boot mode, Bios/Uefi boot sequence will reboot the system

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| boot_mode  |   no  |    | <ul> <li>Bios</li>  <li>Uefi</li> </ul> |  if C(Bios), will set the boot mode to BIOS  if C(Uefi), will set the boot mode to UEFI  |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| one_time_bios_boot_seq  |   no  |  []  | |  List of boot devices' FQDDs in the sequential order for the One-Time Boot only  |
| share_pwd  |   yes  |  | |  Network share user password  |
| uefi_boot_seq  |   no  |  []  | |  List of boot devices' FQDDs in the sequential order for Uefi Boot Sequence. Please make sure that the boot mode is set to C(Uefi) before setting the Uefi boot sequence  |
| share_name  |   yes  |  | |  Network file share (CIFS, NFS)  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| share_user  |   yes  |  | |  Network share user in the format "user@domain" if user is part of a domain else "user"  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share specified in I(share_name) with read-write permission for ansible user  |
| boot_seq_retry  |   no  |    | <ul> <li>Enabled</li>  <li>Disabled</li> </ul> |  if C(Enabled), and the system fails to boot, the system will re-attempt the boot sequence after 30 seconds  if C(Disabled), will disable the Boot Sequence retry feature  |
| bios_boot_seq  |   no  |  []  | |  List of boot devices' FQDDs in the sequential order for BIOS Boot Sequence. Please make sure that the boot mode is set to C(Bios) before setting the BIOS boot sequence.  Changing the BIOS Boot Sequence will restart the server  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| one_time_uefi_boot_seq  |   no  |  []  | |  List of boot devices's FQDDs in the sequential order for One-Time Boot only  |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| first_boot_device  |   no  |  Normal  | <ul> <li>BIOS</li>  <li>CD-DVD</li>  <li>F10</li>  <li>F11</li>  <li>FDD</li>  <li>HDD</li>  <li>Normal</li>  <li>PXE</li>  <li>SD</li>  <li>UEFIDevicePath</li>  <li>VCD-DVD</li>  <li>vFDD</li> </ul> |  Sets the boot device for the next boot operations  The system will boot from the selected device on the next and subsequent reboots, and remains as the first boot device in the BIOS boot order, until it is changed again either from the iDRAC Web Interface or from the BIOS boot sequence.  If I(boot_once) is set to C(Enabled), the system boots from the selected device only once. Subsequently, the system boots according to the BIOS Boot sequence.  The C(F11), C(BIOS), C(F10), and C(UEFIDevicePath) options only support boot once, that is, when any of these devices are set as the boot device, the server boots into the selected device and from the second reboot onwards, the system boots as per the boot order. When any of these options are selected, the I(boot_once) option is set to C(Enabled) by default and you cannot disable it.  |
| boot_once  |   |  Enabled  | <ul> <li>Enabled</li>  <li>Disabled</li> </ul> |  if C(Enabled), boots from the selected device only once on next reboot. Subsequently, the system will boot according to Bios/Uefi boot sequence  if C(Disabled), system will boot from the selected first boot device on next and subsequent reboots  |


 
#### Examples

```
# Configure UEFI Boot Sequence
- name: Change Boot Mode to UEFI
    dellemc_idrac_boot_order:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      boot_mode:  "Uefi"

- name: Configure UEFI Boot Sequence
    dellemc_idrac_boot_order:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      boot_mode:  "Uefi"
      uefi_boot_seq:  ["Optical.SATAEmbedded.E-1", "NIC.Integrated.1-1-1", "NIC.Integrated.1-2-1", "NIC.Integrated.1-3-1", "NIC.Integrated.1-4-1", "HardDisk.List.1-1"]

- name: Configure First Boot device to PXE
    dellemc_idrac_bot_order:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      first_boot_device: "PXE"
      boot_once:  "Enabled"


```



---


## dellemc_idrac_login
Login to iDRAC

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Login to iDRAC

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   yes  |    | |  i  D  R  A  C     u  s  e  r     n  a  m  e  |
| idrac_pwd  |   yes  |    | |  i  D  R  A  C     u  s  e  r     p  a  s  s  w  o  r  d  |
| idrac_ip  |   yes  |    | |  i  D  R  A  C     I  P     A  d  d  r  e  s  s  |
| idrac_port  |   no  |    | |  i  D  R  A  C     p  o  r  t  |


 
#### Examples

```
- name: Login to iDRAC
    dellemc_idrac_login:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
    register: idrac


```



---


## dellemc_idrac_nic
Configure iDRAC Network settings

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Configure iDRAC Network settings

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| nic_selection  |   no  |  Dedicated  | <ul> <li>Dedicated</li>  <li>LOM1</li>  <li>LOM2</li>  <li>LOM3</li>  <li>LOM4</li> </ul> |  NIC Selection mode  |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| nic_autodedicated  |   no  |  False  | |  if C(True), will enable the auto-dedicated NIC option  if C(False), will disable the auto-dedicated NIC option  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  CIFS or NFS Network share  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| nic_failover  |   no  |    | <ul> <li>None</li>  <li>LOM1</li>  <li>LOM2</li>  <li>LOM3</li>  <li>LOM4</li>  <li>All</li> </ul> |  Failover network if NIC selection fails  |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| nic_duplex  |   no  |  Full  | <ul> <li>Full</li>  <li>Half</li> </ul> |  if C(Full), will enable the Full-Duplex mode  if C(Half), will enable the Half-Duplex mode  |
| nic_speed  |   no  |  1000  | <ul> <li>10</li>  <li>100</li>  <li>1000</li> </ul> |  Network Speed  |
| nic_autoneg  |   no  |  False  | |  if C(True), will enable auto negotiation  if C(False), will disable auto negotiation  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share with read-write permission for ansible user  |
| idrac_pwd  |   no  |  | |  iDRAC user password  |
| share_user  |   yes  |  | |  Network share user in the format user@domain if user is part of a domain else 'user'  |


 
#### Examples

```
# Configure NIC Selection using a CIFS Network share
- name: Configure NIC Selection
    dellemc_idrac_nic:
      idrac_ip:      "192.168.1.1"
      idrac_user:    "root"
      idrac_pwd:     "calvin"
      share_name:    "\\192.168.10.10\share"
      share_user:    "user1"
      share_pwd:     "password"
      share_mnt:     "/mnt/share"
      nic_selection: "Dedicated"
      state:         "enable"

```



---


## dellemc_idrac_export_scp
Export Server Configuration Profile (SCP) to network share

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Export Server Configuration Profile to a given network share (CIFS, NFS)

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  CIFS or NFS Network share  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| scp_components  |   no  |  ALL  | <ul> <li>ALL</li>  <li>IDRAC</li>  <li>BIOS</li>  <li>NIC</li>  <li>RAID</li> </ul> |  if C(ALL), will export all components configurations in SCP file  if C(IDRAC), will export iDRAC configuration in SCP file  if C(BIOS), will export BIOS configuration in SCP file  if C(NIC), will export NIC configuration in SCP file  if C(RAID), will export RAID configuration in SCP file  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| share_user  |   yes  |  | |  Network share user in the format 'user@domain' if user is part of a domain else 'user'  |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| job_wait  |   no  |  True  | |  if C(True), will wait for the SCP export job to finish and return the job completion status  if C(False), will return immediately with a JOB ID after queueing the SCP export jon in LC job queue  |


 
#### Examples

```
# Export SCP to a CIFS network share
- name: Export Server Configuration Profile (SCP)
    dellemc_idrac_export_scp:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"

# Export SCP to a NFS network shre
- name: Export Server Configuration Profile (SCP)
    dellemc_idrac_export_scp:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "192.168.10.10:/share"
      share_user: "user1"
      share_pwd:  "password"


```



---


## dellemc_idrac_syslog
Configure remote system logging

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Configure remote system logging settings to remotely write RAC log and System Event Log (SEL) to an external server

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| syslog_servers  |   no  |    | |  List of IP Addresses of the Remote Syslog Servers  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| state  |   |  absent  | <ul> <li>present</li>  <li>absent</li> </ul> |  if C(present), will enable the remote syslog option and add the remote servers in I(syslog_servers)  if C(absent), will disable the remote syslog option  |
| syslog_port  |   no  |  514  | |  Port number of remote servers  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |


 
#### Examples

```
---
- name: Configure Remote Syslog
    dellemc_idrac_syslog:
       idrac_ip:       "192.168.1.1"
       idrac_user:     "root"
       idrac_pwd:      "calvin"
       share_name:     "\\192.168.10.10\share"
       share_user:     "user1"
       share_pwd:      "password"
       share_mnt:      "/mnt/share"
       syslog_servers: ["192.168.20.1", ""192.168.20.2", ""192.168.20.3"]
       syslog_port:    514
       state:          "present"

- name: Disable Remote Syslog
    dellemc_idrac_syslog:
      idrac_ip:       "192.168.1.1"
      idrac_user:     "root"
      idrac_pwd:      "calvin"
      share_name:     "\\192.168.10.10\share"
      share_user:     "user1"
      share_pwd:      "password"
      share_mnt:      "/mnt/share"
      state:          "absent"


```



---


## dellemc_idrac_syslog
Configure remote system logging

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Configure remote system logging settings to remotely write RAC log and System Event Log (SEL) to an external server

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| syslog_servers  |   no  |    | |  List of IP Addresses of the Remote Syslog Servers  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| state  |   |  absent  | <ul> <li>present</li>  <li>absent</li> </ul> |  if C(present), will enable the remote syslog option and add the remote servers in I(syslog_servers)  if C(absent), will disable the remote syslog option  |
| syslog_port  |   no  |  514  | |  Port number of remote servers  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |


 
#### Examples

```
---
- name: Configure Remote Syslog
    dellemc_idrac_syslog:
       idrac_ip:       "192.168.1.1"
       idrac_user:     "root"
       idrac_pwd:      "calvin"
       share_name:     "\\192.168.10.10\share"
       share_user:     "user1"
       share_pwd:      "password"
       share_mnt:      "/mnt/share"
       syslog_servers: ["192.168.20.1", ""192.168.20.2", ""192.168.20.3"]
       syslog_port:    514
       state:          "present"

- name: Disable Remote Syslog
    dellemc_idrac_syslog:
      idrac_ip:       "192.168.1.1"
      idrac_user:     "root"
      idrac_pwd:      "calvin"
      share_name:     "\\192.168.10.10\share"
      share_user:     "user1"
      share_pwd:      "password"
      share_mnt:      "/mnt/share"
      state:          "absent"


```



---


## dellemc_idrac_lc_attr
Configure iDRAC Lifecycle Controller attributes

  * Synopsis
  * Options
  * Examples

#### Synopsis
 {u'Configure following iDRAC Lifecycle Controller attributes': u'CollectSystemInventoryOnRestart (CSIOR)'}

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| share_pwd  |   yes  |  | |  N  e  t  w  o  r  k     s  h  a  r  e     u  s  e  r     p  a  s  s  w  o  r  d  |
| share_name  |   yes  |  | |  N  e  t  w  o  r  k     f  i  l  e     s  h  a  r  e     (  e  i  t  h  e  r     C  I  F  S     o  r     N  F  S  )  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| reboot  |   no  |  False  | |  if C(True), will restart the system after applying the changes  if C(False), will not restart the system after applying the changes  |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| csior  |   no  |  Enabled  | <ul> <li>Enabled</li>  <li>Disabled</li> </ul> |  if C(Enabled), will enable the CSIOR  if C(Disabled), will disable the CSIOR  I(reboot) should be set to C(True) to apply any changes  |
| share_mnt  |   yes  |  | |  L  o  c  a  l     m  o  u  n  t     p  a  t  h     o  f     t  h  e     n  e  t  w  o  r  k     f  i  l  e     s  h  a  r  e     s  p  e  c  i  f  i  e  d     i  n     I  (  s  h  a  r  e  _  n  a  m  e  )     w  i  t  h     r  e  a  d  -  w  r  i  t  e     p  e  r  m  i  s  s  i  o  n     f  o  r     a  n  s  i  b  l  e     u  s  e  r  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| share_user  |   yes  |  | |  N  e  t  w  o  r  k     s  h  a  r  e     u  s  e  r     i  n     t  h  e     f  o  r  m  a  t     '  u  s  e  r  @  d  o  m  a  i  n  '     i  f     u  s  e  r     i  s     p  a  r  t     o  f     a     d  o  m  a  i  n     e  l  s  e     '  u  s  e  r  '  |


 
#### Examples

```
- name: Enable CSIOR
    dellemc_idrac_lc_attr:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      csior:      "Enabled"
      reboot:     True

- name: Disable CSIOR
    dellemc_idrac_lc_attr:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      csior:      "Disabled"
      reboot:     True

```



---


## dellemc_idrac_export_tsr
Export TSR logs to a network share

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Export TSR logs to a network share (CIFS, NFS)

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  CIFS or NFS Network share  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| share_user  |   yes  |  | |  Network share user in the format 'user@domain' if user is part of a domain else 'user'  |


 
#### Examples

```
---
# Export TSR to a CIFS Network Share
- name: Export TSR to a CIFS network share
    dellemc_idrac_export_tsr:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"

# Export TSR to a NFS Network Share
- name: Export TSR to a NFS network share
    dellemc_idrac_export_tsr:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "192.168.10.10:/share"
      share_user: "user1"
      share_pwd:  "password"


```



---


## dellemc_idrac_firmware_update
Firmware update from a repository on a network share (CIFS, NFS)

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Update the Firmware by connecting to a network repository (either CIFS or NFS) that contains a catalog of available updates
 Network share should contain a valid repository of Update Packages (DUPs) and a catalog file describing the DUPs
 All applicable updates contained in the repository is applied to the system
 This feature is only available with iDRAC Enterprise License

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  Network file share (either CIFS or NFS) containing the Catalog file and Update Packages (DUPs)  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| reboot  |   no  |  False  | |  if C(True), reboot for applying the updates  if C(False), do not reboot for applying the update  |
| catalog_file_name  |   no  |  Catalog.xml  | |  Catalog file name relative to the I(share_name)  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| share_user  |   yes  |  | |  Network share user in the format 'user@domain' if user is part of a domain else 'user'  |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| apply_updates  |   no  |  True  | |  if C(True), Install Updates  if C(False), do not Install Updates  |
| job_wait  |   no  |  True  | |  if C(True), will wait for update JOB to get completed  if C(False), return immediately after creating the update job in job queue  |


 
#### Examples

```
---
- name: Update firmware from repository on a Network Share
    dellemc_idrac_virtual_drive:
       idrac_ip:   "192.168.1.1"
       idrac_user: "root"
       idrac_pwd:  "calvin"
       share_name: "\\192.168.10.10\share"
       share_user: "user1"
       share_pwd:  "password"
       catalog_file_name:  "Catalog.xml"
       apply_updates:   True
       reboot:     False
       job_wait:   True


```



---


## dellemc_idrac_logout
Log out of a iDRAC

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Log out of a iDRAC

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac  |   yes  |    | |  i  D  R  A  C     h  a  n  d  l  e  |


 
#### Examples

```
- name: Login to a iDRAC
    dellemc_idrac_idrac:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
    register: idrac

- name: Log out of a iDRAC
    dellemc_idrac_logout:
      idrac:   {{idrac}}


```



---


## dellemc_idrac_export_lclog
Export Lifecycle Controller log file to a network share

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Export Lifecycle Controller log file to a given network s/hare

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  CIFS or NFS Network share  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| share_user  |   yes  |  | |  Network share user in the format 'user@domain' if user is part of a domain else 'user'  |


 
#### Examples

```
---
- name: Export Lifecycle Controller Log
    dellemc_idrac_export_lclog:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share\"
      share_user: "user1"
      share_pwd:  "password"

```



---


## dellemc_idrac_power
Configure the Power Cycle options on PowerEdge Server

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Configure the Power Cycle options on a Dell EMC PowerEdge Server

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| state  |   yes  |  | <ul> <li>PowerOn</li>  <li>SoftPowerCycle</li>  <li>SoftPowerOff</li>  <li>HardReset</li>  <li>DiagnosticInterrupt</li>  <li>GracefulPowerOff</li> </ul> |  if C(PowerOn), will Power On the server  if C(SoftPowerCycle), will close the running applications and Reboot the Server  if C(SoftPowerOff), will close the running applications and Power Off the server  if C(HardReset), will Reboot the Server immediately  if C(DiagnosticInterrupt), will reboot the Server for troubleshooting  if C(GracefulPowerOff), will close the running applications and Power Off the server  |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |


 
#### Examples

```
---
- name: Power On the Server
    dellemc_idrac_power:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      state:      "PowerOn"

```



---


## dellemc_idrac_lc_job
Get the status of a Lifecycle Controller Job, delete a LC Job

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Get the status of a Lifecycle Controller job given a JOB ID
 Delete a LC Job from the Job queue given a JOB ID
 Delete LC Job Queue

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| job_id  |   yes  |  | |  JOB ID in the format JID_123456789012  if C(JID_CLEARALL), then all jobs will be cleared from the LC job queue  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| state  |   no  |  present  | |  if C(present), returns the status of the associated job having the job id provided in I(job_id)  if C(present) and I(job_id) == C(JID_CLEARALL), then delete the job queue  if C(absent), then delete the associated job having the job id provided in I(job_id) from LC job queue  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |


 
#### Examples

```
# Get Job Status for a valid JOB ID
- name: Get LC Job Stattus
    dellemc_idrac_lc_job:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      job_id:     "JID_1234556789012"
      state:      "present"

# Delete the JOB from the LC Job Queue
- name: Delete the LC Job
    dellemc_idrac_lc_job:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      job_id:     "JID_1234556789012"
      state:      "absent"

# Clear the LC Job queue
- name: Clear the LC Job queue
    dellemc_idrac_lc_job:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      job_id:     "JID_CLEARALL"
      state:      "present"


```



---


## dellemc_idrac_user
Configures an iDRAC local User

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Configures an iDRAC local user

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   no  |    | |  i  D  R  A  C     u  s  e  r     n  a  m  e  |
| share_pwd  |   yes  |  | |  N  e  t  w  o  r  k     s  h  a  r  e     u  s  e  r     p  a  s  s  w  o  r  d  |
| share_name  |   yes  |  | |  C  I  F  S     o  r     N  F  S     N  e  t  w  o  r  k     s  h  a  r  e  |
| idrac_port  |   no  |    | |  i  D  R  A  C     p  o  r  t  |
| user_pwd  |   no  |    | |  U  s  e  r     p  a  s  s  w  o  r  d  |
| idrac_ip  |   no  |    | |  i  D  R  A  C     I  P     A  d  d  r  e  s  s  |
| state  |   |  present  | <ul> <li>present</li>  <li>absent</li>  <li>enable</li>  <li>disable</li> </ul> |  if C(present), will create/add/modify an user  if C(absent), will delete the user  if C(enable), will enable the user  if C(disable), will disable the user  |
| user_priv  |   no  |    | <ul> <li>Administrator</li>  <li>Operator</li>  <li>ReadOnly</li>  <li>NoAccess</li> </ul> |  U  s  e  r     p  r  i  v  i  l  e  g  e  s  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share with read-write permission for ansible user  |
| user_name  |   yes  |  | |  U  s  e  r     n  a  m  e     t  o     b  e     c  o  n  f  i  g  u  r  e  d  |
| idrac_pwd  |   no  |    | |  i  D  R  A  C     u  s  e  r     p  a  s  s  w  o  r  d  |
| share_user  |   yes  |  | |  N  e  t  w  o  r  k     s  h  a  r  e     u  s  e  r     i  n     t  h  e     f  o  r  m  a  t     '  u  s  e  r  @  d  o  m  a  i  n  '     i  f     u  s  e  r     i  s     p  a  r  t     o  f     d  o  m  a  i  n     e  l  s  e     '  u  s  e  r  '  |


 
#### Examples

```
---
- name: Add a new iDRAC User
    dellemc_idrac_user:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      user_name:  "newuser"
      user_pwd:   "password"
      user_priv:  "Administrator"
      state:      "present"

- name: Change password for the "newuser"
    dellemc_idrac_user:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      user_name:  "newuser"
      user_pwd:   "newpassword"
      state:      "present"

- name: Change privilege for the "newuser"
    dellemc_idrac_user:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      user_name:  "newuser"
      user_priv:  "Operator"
      state:      "present"

- name: Delete "newuser"
    dellemc_idrac_user:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      user_name:  "newuser"
      state:      "absent"

```



---


## dellemc_idrac_sw_inventory
Get Firmware Inventory

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Get Firmware Inventory

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| serialize  |   no  |  False  | |  if C(True), create '_inventory' and '_master' folders relative to I(share_mnt) and save the installed firmware inventory in a file named 'config.xml' in the '_inventory' directory  if C(True), then I(share_mnt) must be provided  |
| choice  |   no  |  installed  | |  if C(all), get both installed and available (if any) firmware inventory  if C(installed), get installed firmware inventory  |
| share_mnt  |   no  |    | |  Locally mounted absolute path of the Network share (CIFS, NFS) where the inventory file is going to be saved. You can also provide a local folder if you want to save the firmware inventory on local file system  Required if I(serialize = True)  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |


 
#### Examples

```
---
- name: Get Installed Firmware Inventory
    dellemc_idrac_sw_inventory:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_mnt:  "/mnt/NFS/"
      choice:     "installed"

```



---


## dellemc_idrac_timezone_ntp
Configure Time Zone and NTP settings

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Configure Time Zone and NTP settings

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   no  |    | |  iDRAC user name  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  CIFS or NFS Network share  |
| ntp_servers  |   no  |    | |  List of IP Addresses of the NTP Servers  |
| idrac_port  |   no  |    | |  iDRAC port  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| state  |   no  |  present  | |  if C(present), will enable the NTP option and add the NTP servers  if C(absent), will disable the NTP option  |
| timezone  |   no  |    | |  time zone e.g. "Asia/Kolkata"  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share with read-write permission for ansible user  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| share_user  |   yes  |  | |  Network share user in the format user@domain  |


 
#### Examples

```
# Set Timezone, Enable NTP and add NTP Servers
- name: Configure TimeZone and NTP
    dellemc_idrac_timezone_ntp:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      timezone:   "Asia/Kolkata"
      ntp_servers: ["10.10.10.10", "10.10.10.11"]
      state:      "present"

# Disable NTP
- name: Configure TimeZone and NTP
    dellemc_idrac_timezone_ntp:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      state:      "absent"

```



---


## dellemc_idrac_snmp
Configure SNMP settings on iDRAC

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Configures SNMP settings on iDRAC

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| snmp_trap_format  |   no  |  SNMPv1  | <ul> <li>SNMPv1</li>  <li>SNMPv2</li>  <li>SNMPv3</li> </ul> |  S  N  M  P     t  r  a  p     f  o  r  m  a  t     -     i  f     C  (  S  N  M  P  v  1  )  ,     w  i  l  l     c  o  n  f  i  g  u  r  e     i  D  R  A  C     t  o     u  s  e     S  N  M  P  v  1     f  o  r     s  e  n  d  i  n  g     t  r  a  p  s     -     i  f     C  (  S  N  M  P  v  2  )  ,     w  i  l  l     c  o  n  f  i  g  u  r  e     i  D  R  A  C     t  o     u  s  e     S  N  M  P  v  2     f  o  r     s  e  n  d  i  n  g     t  r  a  p  s     -     i  f     C  (  S  N  M  P  v  3  )  ,     w  i  l  l     c  o  n  f  i  g  u  r  e     i  D  R  A  C     t  o     u  s  e     S  N  M  P  v  3     f  o  r     s  e  n  d  i  n  g     t  r  a  p  s  |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  CIFS or NFS Network share  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| snmp_protocol  |   no  |  All  | <ul> <li>All</li>  <li>SNMPv3</li> </ul> |  S  N  M  P     p  r  o  t  o  c  o  l     s  u  p  p  o  r  t  e  d     -     i  f     C  (  A  l  l  )  ,     w  i  l  l     e  n  a  b  l  e     s  u  p  p  o  r  t     f  o  r     S  N  M  P  v  1  ,     v  2     a  n  d     v  3     p  r  o  t  o  c  o  l  s     -     i  f     C  (  S  N  M  P  v  3  )  ,     w  i  l  l     e  n  a  b  l  e     s  u  p  p  o  r  t     f  o  r     o  n  l  y     S  N  M  P  v  3     p  r  o  t  o  c  o  l  |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| snmp_enable  |   no  |  Enabled  | <ul> <li>Enabled</li>  <li>Disabled</li> </ul> |  S  N  M  P     A  g  e  n  t     s  t  a  t  u  s     -     i  f     C  (  e  n  a  b  l  e  d  )  ,     w  i  l  l     e  n  a  b  l  e     t  h  e     S  N  M  P     A  g  e  n  t     -     i  f     C  (  d  i  s  a  b  l  e  d  )  ,     w  i  l  l     d  i  s  a  b  l  e     t  h  e     S  N  M  P     A  g  e  n  t  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  if C(present), will perform create/add/enable operations  if C(absent), will perform delete/remove/disable operations  |
| snmp_discover_port  |   no  |  161  | |  SNMP discovery port  |
| snmp_community  |   no  |  public  | |  SNMP Agent community string  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share with read-write permission for ansible user  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| snmp_trap_port  |   no  |  162  | |  SNMP trap port  |
| share_user  |   yes  |  | |  Network share user in the format 'user@domain' if user is part of a domain else 'user'  |


 
#### Examples

```
- name: Configure SNMP
    dellemc_idrac_snmp:
      idrac_ip:             "192.168.1.1"
      idrac_user:           "root"
      idrac_pwd:            "calvin"
      share_name:           "\\192.168.10.10\share"
      share_user:           "user1"
      share_pwd:            "password"
      share_mnt:            "/mnt/share"
      snmp_agent_enable:    "enabled"
      snmp_protocol:        "all"
      snmp_community:       "public"
      snmp_port:            "161"
      snmp_trap_port:       "162"
      state:                "present"

```



---


## dellemc_idrac_web_server
Configure iDRAC Web Server service interface settings

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Configure iDRAC Web Server Service interface settings such as minimum supprted levels of Transport Layer Security (TLS) protocol and levels of Secure Socket Layer (SSL) Encryption

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   no  |    | |  iDRAC user name  |
| http_port  |   no  |  80  | |  iDRAC Web Server HTTP port  |
| share_pwd  |   yes  |  | |  Network share user password  |
| https_port  |   no  |  443  | |  iDRAC Web Server HTTPS port  |
| share_name  |   yes  |  | |  Network file share  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| tls_protocol  |   no  |  TLS 1.1 and Higher  | <ul> <li>TLS 1.0 and Higher</li>  <li>TLS 1.1 and Higher</li>  <li>TLS 1.2 Only</li> </ul> |  if C(TLS 1.0 and Higher), will set the TLS protocol to TLS 1.0 and higher  if C(TLS 1.1 and Higher), will set the TLS protocol to TLS 1.1 and higher  if C(TLS 1.2 Only), will set the TLS protocol option to TLS 1.2 Only  |
| ssl_bits  |   no  |  128-Bit or higher  | <ul> <li>Auto-Negotiate</li>  <li>128-Bit or higher</li>  <li>168-Bit or higher</li>  <li>256-Bit or higher</li> </ul> |  if C(128-Bit or higher), will set the SSL Encryption Bits to 128-Bit or higher  if C(168-Bit or higher), will set the SSL Encryption Bits to 168-Bit or higher  if C(256-Bit or higher), will set the SSL Encryption Bits to 256-Bit or higher  if C(Auto-Negotiate), will set the SSL Encryption Bits to Auto-Negotiate  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  if C(present), will enable the Web Server and configure the Web Server parameters  if C(absent), will disable the Web Server. Please note that you will not be able to use the iDRAC Web Interface if you disable the Web server.  |
| timeout  |   no  |  1800  | |  Time (in seconds) that a connection is allowed to remain idle  Changes to the timeout settings do not affect the current session  If you change the timeout value, you must log out and log in again for the new settings to take effect  Timeout range is 60 to 10800 seconds  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share with read-write permission for ansible user  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| share_user  |   yes  |  | |  Network share user in the format user@domain  |


 
#### Examples

```
- name: Configure Web Server TLS and SSL settings (using CIFS network share)
    dellemc_idrac_web_server:
      idrac_ip:     "192.168.1.1"
      idrac_user:   "root"
      idrac_pwd:    "calvin"
      share_name:   "\\192.168.10.10\share"
      share_user:   "user1"
      share_pwd:    "password"
      share_mnt:    "/mnt/share"
      tls_protocol: "TLS 1.2 Only"
      ssl_bits:     "256-Bit or higher"

- name: Configure Web Server TLS and SSL settings (using NFS network share)
    dellemc_idrac_web_server:
      idrac_ip:     "192.168.1.1"
      idrac_user:   "root"
      idrac_pwd:    "calvin"
      share_name:   "192.168.10.10:/share"
      share_user:   "user1"
      share_pwd:    "password"
      share_mnt:    "/mnt/share"
      tls_protocol: "TLS 1.2 Only"
      ssl_bits:     "256-Bit or higher"

```



---


## dellemc_idrac_lcstatus
Returns the Lifecycle Controller status

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Returns the Lifecycle Controller Status on a Dell EMC PowerEdge Server

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| idrac_port  |   no  |  443  | |  iDRAC port  |


 
#### Examples

```
---
- name: Get Lifecycle Controller Status
    dellemc_idrac_lcstatus:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"

```



---


## dellemc_idrac_inventory
Returns the PowerEdge Server hardware inventory

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Returns the Dell EMC PowerEdge Server hardware inventory

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| idrac_port  |   no  |  443  | |  iDRAC port  |


 
#### Examples

```
---
- name: Get System Inventory
  dellemc_idrac_inventory:
    idrac_ip:   "192.168.1.1"
    idrac_user: "root"
    idrac_pwd:  "calvin"

```



---


---
Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
