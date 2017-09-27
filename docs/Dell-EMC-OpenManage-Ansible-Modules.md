# Dell EMC OpenManage Ansible Modules for iDRAC

---
### Requirements
* python >= '2.6'
* Dell EMC OpenManage Python SDK

---
### Modules

  * [dellemc_idrac_boot_to_nw_iso - boot to a network iso image](#dellemc_idrac_boot_to_nw_iso)
  * [dellemc_idrac_timezone - configure time zone](#dellemc_idrac_timezone)
  * [dellemc_idrac_nic_ipv4 - configure idrac network ipv4 settings](#dellemc_idrac_nic_ipv4)
  * [dellemc_idrac_virtual_drive - create or delete virtual drives](#dellemc_idrac_virtual_drive)
  * [dellemc_idrac_lc_job_status - get the status of a lifecycle controller job](#dellemc_idrac_lc_job_status)
  * [dellemc_idrac_nic_vlan - configure idrac network vlan settings](#dellemc_idrac_nic_vlan)
  * [dellemc_idrac_snmp_alert - configure snmp alert destination settings on idrac](#dellemc_idrac_snmp_alert)
  * [dellemc_idrac_import_scp - import scp from a network share](#dellemc_idrac_import_scp)
  * [dellemc_idrac_delete_lc_job_queue - deletes the lifecycle controller job queue](#dellemc_idrac_delete_lc_job_queue)
  * [dellemc_idrac_nic - configure idrac network settings](#dellemc_idrac_nic)
  * [dellemc_idrac_tls - configure tls protocol options and ssl encryption bits](#dellemc_idrac_tls)
  * [dellemc_idrac_export_scp - export server configuration profile (scp) to network share](#dellemc_idrac_export_scp)
  * [dellemc_idrac_delete_lc_job - deletes a lifecycle controller job given a job id](#dellemc_idrac_delete_lc_job)
  * [dellemc_idrac_syslog - configure remote system logging](#dellemc_idrac_syslog)
  * [dellemc_idrac_syslog - configure remote system logging](#dellemc_idrac_syslog)
  * [dellemc_idrac_export_tsr - export tsr logs to a network share](#dellemc_idrac_export_tsr)
  * [dellemc_idrac_firmware_update - firmware update from a repository](#dellemc_idrac_firmware_update)
  * [dellemc_idrac_export_lclog - export lifecycle controller log file to a network share](#dellemc_idrac_export_lclog)
  * [dellemc_idrac_boot_mode - configure boot mode](#dellemc_idrac_boot_mode)
  * [dellemc_idrac_power - configure the power cycle options on poweredge server](#dellemc_idrac_power)
  * [dellemc_idrac_csior - enable or disble collect system inventory on restart (csior)](#dellemc_idrac_csior)
  * [dellemc_idrac_user - configures an idrac local user](#dellemc_idrac_user)
  * [dellemc_idrac_sw_inventory - get firmware inventory](#dellemc_idrac_sw_inventory)
  * [dellemc_idrac_snmp - configure snmp settings on idrac](#dellemc_idrac_snmp)
  * [dellemc_idrac_lcstatus - returns the lifecycle controller status](#dellemc_idrac_lcstatus)
  * [dellemc_idrac_ntp - configure ntp settings](#dellemc_idrac_ntp)
  * [dellemc_idrac_inventory - returns the poweredge server system inventory](#dellemc_idrac_inventory)
  * [dellemc_idrac_location - configure system location fields](#dellemc_idrac_location)

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
| idrac_user  |   no  |    | |  iDRAC user name  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  Network file share  |
| idrac_port  |   no  |    | |  iDRAC port  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| iso_image  |   yes  |    | |  Path to ISO image relative to the I(share_name)  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share specified in I(share_name) with read-write permission for ansible user  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| share_user  |   yes  |  | |  Network share user in the format user@domain  |


 
#### Examples

```
- name: Boot to Network ISO
    dellemc_idrac_boot_to_nw_iso:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      iso_image:  "uninterrupted_os_installation_image.iso"

```



---


## dellemc_idrac_timezone
Configure Time Zone

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Configure time zone

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   no  |    | |  iDRAC user name  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  CIFS or NFS Network share  |
| idrac_port  |   no  |    | |  iDRAC port  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| timezone  |   no  |    | |  time zone e.g. "Asia/Kolkata"  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share with read-write permission for ansible user  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| share_user  |   yes  |  | |  Network share user in the format user@domain  |


 
#### Examples

```
- name: Configure TimeZone
    dellemc_idrac_timezone:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      timezone:   "Asia/Kolkata"

```



---


## dellemc_idrac_nic_ipv4
Configure iDRAC Network IPv4 Settings

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Configure iDRAC Network IPv4 Settings

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   no  |    | |  i  D  R  A  C     u  s  e  r     n  a  m  e  |
| dns_from_dhcp  |   no  |  | |  if C(True), will enable the use of DHCP server for obtaining the primary and secondary DNS servers addresses  if C(False), will disable the use of DHCP server for obtaining the primary and secondary DNS servers addresses  |
| static_netmask  |   no  |    | |  Static IPv4 subnet mask for iDRAC NIC  Required if I(dhcp_enable=False)  |
| dhcp_enable  |   no  |  False  | |  E  n  a  b  l  e     o  r     d  i  s  a  b  l  e     D  H  C  P     f  o  r     a  s  s  i  g  n  i  n  g     i  D  R  A  C     I  P  v  4     a  d  d  r  e  s  s  |
| share_name  |   yes  |  | |  C  I  F  S     o  r     N  F  S     N  e  t  w  o  r  k     s  h  a  r  e  |
| idrac_port  |   no  |    | |  i  D  R  A  C     p  o  r  t  |
| enable_ipv4  |   no  |  True  | |  E  n  a  b  l  e     o  r     d  i  s  a  b  l  e     t  h  e     i  D  R  A  C     I  P  v  4     s  t  a  c  k  |
| static_ipv4  |   no  |    | |  iDRAC NIC static IPv4 address  Required if I(dhcp_enable=False)  |
| share_mnt  |   yes  |  | |  L  o  c  a  l     m  o  u  n  t     p  a  t  h     o  f     t  h  e     n  e  t  w  o  r  k     f  i  l  e     s  h  a  r  e     w  i  t  h     r  e  a  d  -  w  r  i  t  e     p  e  r  m  i  s  s  i  o  n     f  o  r     a  n  s  i  b  l  e     u  s  e  r  |
| alternate_dns  |   no  |    | |  Alternate DNS Server static IPv4 Address  Required if I(dns_from_dhcp=False)  |
| share_pwd  |   yes  |  | |  N  e  t  w  o  r  k     s  h  a  r  e     u  s  e  r     p  a  s  s  w  o  r  d  |
| idrac_pwd  |   no  |    | |  i  D  R  A  C     u  s  e  r     p  a  s  s  w  o  r  d  |
| static_ipv4_gw  |   no  |    | |  Static IPv4 gateway address for iDRAC NIC  Required if I(dhcp_enable=False)  |
| idrac_ip  |   no  |    | |  i  D  R  A  C     I  P     A  d  d  r  e  s  s  |
| preferred_dns  |   no  |    | |  Preferred DNS Server static IPv4 Address  Required if I(dns_from_dhcp=False)  |
| share_user  |   yes  |  | |  N  e  t  w  o  r  k     s  h  a  r  e     u  s  e  r     i  n     t  h  e     f  o  r  m  a  t     u  s  e  r  @  d  o  m  a  i  n  |


 
#### Examples

```
- name: Configure NIC IPv4
    dellemc_idrac_nic_ipv4:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      enable_ipv4: True
      dhcp_enable: False

```



---


## dellemc_idrac_virtual_drive
Create or delete virtual drives

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Create or delete virtual drives

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   no  |    | |  iDRAC user name  |
| stripe_size  |   no  |  64KB  | <ul> <li>64KB</li>  <li>128KB</li>  <li>256KB</li>  <li>512KB</li>  <li>1MB</li> </ul> |  Stripe size of the virtual disk  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  Network file share  |
| disk_cache_policy  |   no  |  Default  | <ul> <li>Default</li>  <li>Enabled</li>  <li>Disabled</li> </ul> |  Physical Disk caching policy of all members of a Virtual Disk  |
| idrac_port  |   no  |    | |  iDRAC port  |
| virtual_drive_name  |   yes  |    | |  Name of the Virtual Drive  |
| span_depth  |   no  |  | |  Number of spans in the virtual disk. Required if I(status = 'present')  |
| raid_type  |   no  |  RAID 0  | <ul> <li>RAID 0</li>  <li>RAID 1</li>  <li>RAID 5</li>  <li>RAID 6</li>  <li>RAID 10</li>  <li>RAID 50</li>  <li>RAID 60</li> </ul> |  RAID type  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  if C(present), will perform create/add operations  if C(absent), will perform delete/remove operations  |
| span_length  |   no  |  | |  Number of physical disks per span on a virtual disk. Required if I(status = 'absent')  |
| read_cache_policy  |   no  |  NoReadAhead  | <ul> <li>NoReadAhead</li>  <li>ReadAhead</li>  <li>Adaptive</li> </ul> |  Read Cache polic of the virtual disk  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share specified in I(share_name) with read-write permission for ansible user  |
| write_cache_policy  |   no  |  WriteThrough  | <ul> <li>WriteThrough</li>  <li>WriteBack</li>  <li>WriteBackForce</li> </ul> |  Write cache policy of the virtual disk  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| share_user  |   yes  |  | |  Network share user in the format user@domain  |


 
#### Examples

```
- name: Create Virtual Drive
    dellemc_idrac_virtual_drive:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      virtual_drive_name:  "Virtual Drive 0"
      raid_type:   "RAID_1"
      span_depth:  1
      span_length: 2
      state:       "present"

- name: Delete Virtual Drive
    dellemc_idrac_boot_to_nw_iso:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      virtual_drive_name:  "Virtual Drive 0"
      state:       "absent"

```



---


## dellemc_idrac_lc_job_status
Get the status of a Lifecycle Controller Job

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Get the status of a Lifecycle Controller Job given a JOB ID

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_port  |   no  |    | |  iDRAC port  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| idrac_user  |   no  |    | |  iDRAC user name  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| job_id  |   yes  |    | |  JOB ID in the format JID_123456789012  |


 
#### Examples

```
# LC Job Status example
- name: Get LC Job Stattus
    dellemc_idrac_lc_job_status:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      job_id:     "JID_1234556789012"

```



---


## dellemc_idrac_nic_vlan
Configure iDRAC Network VLAN settings

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Configure iDRAC Network VLAN settings.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   no  |    | |  iDRAC user name  |
| vlan_priority  |   no  |  0  | |  VLAN priority  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  CIFS or NFS Network share  |
| idrac_port  |   no  |    | |  iDRAC port  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| state  |   no  |  disable  | |  if C(enable), will enable the VLAN settings and add/change VLAN ID and VLAN priority  if C(disable), will disable the VLAN settings  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share with read-write permission for ansible user  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| vlan_id  |   no  |  1  | |  VLAN ID  |
| share_user  |   yes  |  | |  Network share user in the format user@domain  |


 
#### Examples

```
- name: Configure NIC VLAN
    dellemc_idrac_nic_vlan:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      state:      "enable"

```



---


## dellemc_idrac_snmp_alert
Configure SNMP Alert destination settings on iDRAC

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Configures SNMP Alert destination settings on iDRAC

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   no  |    | |  iDRAC user name  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  Network file share  |
| idrac_port  |   no  |    | |  iDRAC port  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| state  |   |  present  | <ul> <li>present</li>  <li>absent</li>  <li>enable</li>  <li>disable</li> </ul> |  if C(present), will create/add a SNMP alert destination  if C(absent), will delete/remove a SNMP alert destination  if C(enable), will enable a SNMP alert destination  if C(disable), will disable a SNMP alert destination  |
| snmp_alert_dest  |   yes  |  | |  SNMP Alert destination IPv4 address  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share with read-write permission for ansible user  |
| snmpv3_user_name  |   no  |    | |  SNMPv3 user name for the SNMP alert destination  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| share_user  |   yes  |  | |  Network share user in the format "user@domain"  |


 
#### Examples

```
- name: Configure SNMP Alert Destination
    dellemc_idrac_snmp_alert:
      idrac_ip:        "192.168.1.1"
      idrac_user:      "root"
      idrac_pwd:       "calvin"
      share_name:      "\\\\192.168.10.10\\share"
      share_user:      "user1"
      share_pwd:       "password"
      share_mnt:       "/mnt/share"
      snmp_alert_dest: "192.168.2.1"
      state:           "present"


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
| idrac_user  |   no  |    | |  i  D  R  A  C     u  s  e  r     n  a  m  e  |
| scp_file  |   yes  |    | |  S  e  r  v  e  r     C  o  n  f  i  g  u  r  a  t  i  o  n     P  r  o  f  i  l  e     f  i  l  e     n  a  m  e  |
| share_pwd  |   yes  |  | |  N  e  t  w  o  r  k     s  h  a  r  e     u  s  e  r     p  a  s  s  w  o  r  d  |
| share_name  |   yes  |  | |  N  e  t  w  o  r  k     f  i  l  e     s  h  a  r  e  |
| idrac_port  |   no  |    | |  i  D  R  A  C     p  o  r  t  |
| scp_components  |   no  |  ALL  | <ul> <li>ALL</li>  <li>IDRAC</li>  <li>BIOS</li>  <li>NIC</li>  <li>RAID</li> </ul> |  if C(ALL), will import all components configurations from SCP file  if C(IDRAC), will import iDRAC comfiguration from SCP file  if C(BIOS), will import BIOS configuration from SCP file  if C(NIC), will import NIC configuration from SCP file  if C(RAID), will import RAID configuration from SCP file  |
| reboot  |   no  |  False  | |  R  e  b  o  o  t     a  f  t  e  r     i  m  p  o  r  t  i  n  g     t  h  e     S  C  P  |
| idrac_ip  |   no  |    | |  i  D  R  A  C     I  P     A  d  d  r  e  s  s  |
| share_mnt  |   yes  |  | |  L  o  c  a  l     m  o  u  n  t     p  a  t  h     o  f     t  h  e     n  e  t  w  o  r  k     f  i  l  e     s  h  a  r  e     s  p  e  c  i  f  i  e  d     i  n     I  (  s  h  a  r  e  _  n  a  m  e  )     w  i  t  h     r  e  a  d  -  w  r  i  t  e     p  e  r  m  i  s  s  i  o  n     f  o  r     a  n  s  i  b  l  e     u  s  e  r  |
| idrac_pwd  |   no  |    | |  i  D  R  A  C     u  s  e  r     p  a  s  s  w  o  r  d  |
| share_user  |   yes  |  | |  N  e  t  w  o  r  k     s  h  a  r  e     u  s  e  r     i  n     t  h  e     f  o  r  m  a  t     u  s  e  r  @  d  o  m  a  i  n  |


 
#### Examples

```
# Import Server Configuration Profile from a CIFS Network Share
- name: Import Server Configuration Profile
    dellemc_idrac_import_scp:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
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


## dellemc_idrac_delete_lc_job_queue
Deletes the Lifecycle Controller Job Queue

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Deletes the Lifecycle Controller Job Queue

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   no  |    | |  iDRAC user name  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| idrac_port  |   no  |    | |  iDRAC port  |


 
#### Examples

```
---
- name: Delete LC Job Queue
    dellemc_idrac_delete_lc_job_queue:
       idrac_ip:   "192.168.1.1"
       idrac_user: "root"
       idrac_pwd:  "calvin"

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
| idrac_user  |   no  |    | |  iDRAC user name  |
| nic_autodedicated  |   no  |  False  | |  if C(True), will enable the auto-dedicated NIC option  if C(False), will disable the auto-dedicated NIC option  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  CIFS or NFS Network share  |
| idrac_port  |   no  |    | |  iDRAC port  |
| nic_failover  |   no  |    | <ul> <li>None</li>  <li>LOM1</li>  <li>LOM2</li>  <li>LOM3</li>  <li>LOM4</li>  <li>All</li> </ul> |  Failover network if NIC selection fails  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| nic_duplex  |   no  |  Full  | <ul> <li>Full</li>  <li>Half</li> </ul> |  if C(Full), will enable the Full-Duplex mode  if C(Half), will enable the Half-Duplex mode  |
| nic_speed  |   no  |  1000  | <ul> <li>10</li>  <li>100</li>  <li>1000</li> </ul> |  Network Speed  |
| nic_autoneg  |   no  |  False  | |  if C(True), will enable auto negotiation  if C(False), will disable auto negotiation  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share with read-write permission for ansible user  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| share_user  |   yes  |  | |  Network share user in the format user@domain  |


 
#### Examples

```
# Configure NIC Selection using a CIFS Network share
- name: Configure NIC Selection
    dellemc_idrac_nic:
      idrac_ip:      "192.168.1.1"
      idrac_user:    "root"
      idrac_pwd:     "calvin"
      share_name:    "\\\\192.168.10.10\\share"
      share_user:    "user1"
      share_pwd:     "password"
      share_mnt:     "/mnt/share"
      nic_selection: "Dedicated"
      state:         "enable"

```



---


## dellemc_idrac_tls
Configure TLS protocol options and SSL Encryption Bits

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Configure Transport Layer Security (TLS) protocol options
 Configure Secure Socket Layer (SSL) Encryption Bits options

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   no  |    | |  iDRAC user name  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  Network file share  |
| idrac_port  |   no  |    | |  iDRAC port  |
| tls_protocol  |   no  |  TLS 1.1 and Higher  | <ul> <li>TLS 1.0 and Higher</li>  <li>TLS 1.1 and Higher</li>  <li>TLS 1.2 Only</li> </ul> |  if C(TLS 1.0 and Higher), will set the TLS protocol to TLS 1.0 and higher  if C(TLS 1.1 and Higher), will set the TLS protocol to TLS 1.1 and higher  if C(TLS 1.2 Only), will set the TLS protocol option to TLS 1.2 Only  |
| ssl_bits  |   no  |  128-Bit or higher  | <ul> <li>Auto-Negotiate</li>  <li>128-Bit or higher</li>  <li>168-Bit or higher</li>  <li>256-Bit or higher</li> </ul> |  if C(128-Bit or higher), will set the SSL Encryption Bits to 128-Bit or higher  if C(168-Bit or higher), will set the SSL Encryption Bits to 168-Bit or higher  if C(256-Bit or higher), will set the SSL Encryption Bits to 256-Bit or higher  if C(Auto-Negotiate), will set the SSL Encryption Bits to Auto-Negotiate  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share with read-write permission for ansible user  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| share_user  |   yes  |  | |  Network share user in the format user@domain  |


 
#### Examples

```
- name: Configure TLS
    dellemc_idrac_tls:
      idrac_ip:     "192.168.1.1"
      idrac_user:   "root"
      idrac_pwd:    "calvin"
      share_name:   "\\\\192.168.10.10\\share"
      share_user:   "user1"
      share_pwd:    "password"
      share_mnt:    "/mnt/share"
      tls_protocol: "TLS 1.0 and Higher"
      ssl_bits:     "128-Bit or higher"

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
| idrac_user  |   no  |    | |  iDRAC user name  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  CIFS or NFS Network share  |
| idrac_port  |   no  |    | |  iDRAC port  |
| scp_components  |   no  |  ALL  | <ul> <li>ALL</li>  <li>IDRAC</li>  <li>BIOS</li>  <li>NIC</li>  <li>RAID</li> </ul> |  if C(ALL), will export all components configurations in SCP file  if C(IDRAC), will export iDRAC configuration in SCP file  if C(BIOS), will export BIOS configuration in SCP file  if C(NIC), will export NIC configuration in SCP file  if C(RAID), will export RAID configuration in SCP file  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| share_user  |   yes  |  | |  Network share user in the format user@domain  |


 
#### Examples

```
# Export SCP to a CIFS network share
- name: Export Server Configuration Profile (SCP)
    dellemc_idrac_export_scp:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_pwd:  "password"
      share_user: "user1"

# Export SCP to a NFS network shre
- name: Export Server Configuration Profile (SCP)
    dellemc_idrac_export_scp:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "192.168.10.10:/share"
      share_pwd:  "password"
      share_user: "user1"


```



---


## dellemc_idrac_delete_lc_job
Deletes a Lifecycle Controller Job given a JOB ID

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Deletes a Lifecycle Controller job given a JOB ID

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_port  |   no  |    | |  iDRAC port  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| idrac_user  |   no  |    | |  iDRAC user name  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| job_id  |   yes  |  | |  J  O  B     I  D     i  n     t  h  e     f  o  r  m  a  t     "  J  I  D  _  1  2  3  4  5  5  6  7  8  9  0  1  2  "  |


 
#### Examples

```
---
- name: Delete LC Job
    dellemc_idrac_delete_lc_job:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      job_id:     "JID_1234556789012"

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
| idrac_user  |   no  |    | |  iDRAC user name  |
| syslog_servers  |   no  |    | |  List of IP Addresses of the Remote Syslog Servers  |
| idrac_port  |   no  |    | |  iDRAC port  |
| state  |   |  | |  if C(present), will enable the remote syslog option and add the remote servers  if C(absent), will disable the remote syslog option  |
| syslog_port  |   no  |  514  | |  Port number of remote server  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |


 
#### Examples

```
---
- name: Configure Remote Syslog
    dellemc_idrac_syslog:
       idrac_ip:       "192.168.1.1"
       idrac_user:     "root"
       idrac_pwd:      "calvin"
       share_name:     "\\\\192.168.10.10\\share"
       share_user:     "user1"
       share_pwd:      "password"
       share_mnt:      "/mnt/share"
       syslog_servers: ["192.168.20.1", ""192.168.20.2", ""192.168.20.3"]
       syslog_port:    "514"
       state:          "present"

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
| idrac_user  |   no  |    | |  iDRAC user name  |
| syslog_servers  |   no  |    | |  List of IP Addresses of the Remote Syslog Servers  |
| idrac_port  |   no  |    | |  iDRAC port  |
| state  |   |  | |  if C(present), will enable the remote syslog option and add the remote servers  if C(absent), will disable the remote syslog option  |
| syslog_port  |   no  |  514  | |  Port number of remote server  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |


 
#### Examples

```
---
- name: Configure Remote Syslog
    dellemc_idrac_syslog:
       idrac_ip:       "192.168.1.1"
       idrac_user:     "root"
       idrac_pwd:      "calvin"
       share_name:     "\\\\192.168.10.10\\share"
       share_user:     "user1"
       share_pwd:      "password"
       share_mnt:      "/mnt/share"
       syslog_servers: ["192.168.20.1", ""192.168.20.2", ""192.168.20.3"]
       syslog_port:    "514"
       state:          "present"

```



---


## dellemc_idrac_export_tsr
Export TSR logs to a network share

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Export TSR logs to a given network share

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   no  |    | |  iDRAC user name  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  CIFS or NFS Network share  |
| idrac_port  |   no  |    | |  iDRAC port  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| share_user  |   yes  |  | |  Network share user in the format user@domain  |


 
#### Examples

```
---
# Export TSR to a CIFS Network Share
- name: Export TSR to a CIFS network share
    dellemc_idrac_export_tsr:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
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
Firmware update from a repository

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Update the Firmware by connecting to a network repository that contains a catalog of available updates
 Network share should contain a valid repository of Update Packages (DUPs) and a catalog file describing the DUPs
 All applicable updates contained in the repository is applied to the system
 This feature is only available with iDRAC Enterprise License

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   no  |    | |  iDRAC user name  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  Network file share containing the Update Packages (DUPs)  |
| idrac_port  |   no  |    | |  iDRAC port  |
| reboot  |   no  |  False  | |  if C(True), reboot after applying the update  if C(False), do not reboot after applying the update  |
| catalog_file_name  |   no  |  Catalog.xml  | |  Catalog file name relative to the I(share_name)  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| share_user  |   yes  |  | |  Network share user in the format user@domain  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| apply_updates  |   no  |  True  | |  if C(True), Install Updates  if C(False), do not Install Updates  |
| job_wait  |   no  |  True  | |  W  a  i  t     f  o  r     u  p  d  a  t  e     J  O  B  |


 
#### Examples

```
---
- name: Update firmware from repository on a Network Share
    dellemc_idrac_virtual_drive:
       idrac_ip:   "192.168.1.1"
       idrac_user: "root"
       idrac_pwd:  "calvin"
       share_name: "\\\\192.168.10.10\\share"
       share_user: "user1"
       share_pwd:  "password"
       catalog_file_name:  "Catalog.xml"
       apply_updates:   True
       reboot:     False
       job_wait:   True


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
| idrac_user  |   no  |    | |  iDRAC user name  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  CIFS or NFS Network share  |
| idrac_port  |   no  |    | |  iDRAC port  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| share_user  |   yes  |  | |  Network share user in the format user@domain  |


 
#### Examples

```
---
- name: Export Lifecycle Controller Log
    dellemc_idrac_export_lclog:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_user: "user1"
      share_pwd:  "password"

```



---


## dellemc_idrac_boot_mode
Configure Boot Mode

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Configure Boot Mode

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   no  |    | |  iDRAC user name  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  Network file share  |
| idrac_port  |   no  |    | |  iDRAC port  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share specified in I(share_name) with read-write permission for ansible user  |
| share_user  |   yes  |  | |  Network share user in the format user@domain  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| boot_mode  |   no  |  Bios  | <ul> <li>Bios</li>  <li>Uefi</li> </ul> |  if C(Bios), will set the boot mode to BIOS  if C(Uefi), will set the boot mode to UEFI  |


 
#### Examples

```
- name: Configure Boot Mode
    dellemc_idrac_boot_mode:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      boot_mode:  "Uefi"

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
| idrac_port  |   no  |    | |  iDRAC port  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| idrac_user  |   no  |    | |  iDRAC user name  |
| state  |   yes  |  | <ul> <li>PowerOn</li>  <li>SoftPowerCycle</li>  <li>SoftPowerOff</li>  <li>HardReset</li>  <li>DiagnosticInterrupt</li>  <li>GracefulPowerOff</li> </ul> |  if C(PowerOn), will Power On the server  if C(SoftPowerCycle), will close the running applications and Reboot the Server  if C(SoftPowerOff), will close the running applications and Power Off the server  if C(HardReset), will Reboot the Server immediately  if C(DiagnosticInterrupt), will reboot the Server for troubleshooting  if C(GracefulPowerOff), will close the running applications and Power Off the server  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |


 
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


## dellemc_idrac_csior
Enable or disble Collect System Inventory on Restart (CSIOR)

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Enable or Disable Collect System Inventory on Restart (CSIOR)

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   no  |    | |  i  D  R  A  C     u  s  e  r     n  a  m  e  |
| share_pwd  |   yes  |  | |  N  e  t  w  o  r  k     s  h  a  r  e     u  s  e  r     p  a  s  s  w  o  r  d  |
| share_name  |   yes  |  | |  N  e  t  w  o  r  k     f  i  l  e     s  h  a  r  e  |
| idrac_port  |   no  |    | |  i  D  R  A  C     p  o  r  t  |
| idrac_ip  |   no  |    | |  i  D  R  A  C     I  P     A  d  d  r  e  s  s  |
| state  |   no  |  enable  | <ul> <li>enable</li>  <li>disable</li> </ul> |  if C(enable), will enable the CSIOR  if C(disable), will disable the CSIOR  |
| share_mnt  |   yes  |  | |  L  o  c  a  l     m  o  u  n  t     p  a  t  h     o  f     t  h  e     n  e  t  w  o  r  k     f  i  l  e     s  h  a  r  e     s  p  e  c  i  f  i  e  d     i  n     I  (  s  h  a  r  e  _  n  a  m  e  )     w  i  t  h     r  e  a  d  -  w  r  i  t  e     p  e  r  m  i  s  s  i  o  n     f  o  r     a  n  s  i  b  l  e     u  s  e  r  |
| idrac_pwd  |   no  |    | |  i  D  R  A  C     u  s  e  r     p  a  s  s  w  o  r  d  |
| share_user  |   yes  |  | |  N  e  t  w  o  r  k     s  h  a  r  e     u  s  e  r     i  n     t  h  e     f  o  r  m  a  t     u  s  e  r  @  d  o  m  a  i  n  |


 
#### Examples

```
- name: Configure CSIOR
    dellemc_idrac_csior:
       idrac_ip:   "192.168.1.1"
       idrac_user: "root"
       idrac_pwd:  "calvin"
       share_name: "\\\\192.168.10.10\\share"
       share_user: "user1"
       share_pwd:  "password"
       share_mnt:  "/mnt/share"
       state:      "enable"


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
| user_priv  |   no  |  NoPrivilege  | <ul> <li>Administrator</li>  <li>Operator</li>  <li>ReadOnly</li>  <li>NoPrivilege</li> </ul> |  U  s  e  r     p  r  i  v  i  l  e  g  e  s  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share with read-write permission for ansible user  |
| user_name  |   yes  |  | |  U  s  e  r     n  a  m  e     t  o     b  e     c  o  n  f  i  g  u  r  e  d  |
| idrac_pwd  |   no  |    | |  i  D  R  A  C     u  s  e  r     p  a  s  s  w  o  r  d  |
| share_user  |   yes  |  | |  N  e  t  w  o  r  k     s  h  a  r  e     u  s  e  r     i  n     t  h  e     f  o  r  m  a  t     u  s  e  r  @  d  o  m  a  i  n  |


 
#### Examples

```
---
- name: Setup iDRAC Users
    dellemc_idrac_user:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      user_name:  "admin"
      user_pwd:   "password"
      user_priv:  "Administrator"
      state:      "present"

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
| idrac_user  |   no  |    | |  iDRAC user name  |
| idrac_port  |   no  |    | |  iDRAC port  |
| serialize  |   no  |  False  | |  if C(True), create '_inventory' and '_master' folders relative to I(share_mnt) and save the installed firmware inventory in a file in the '_inventory' directory  if C(True), then I(share_mnt) must be provided  |
| choice  |   no  |  installed  | |  if C(all), get both installed and available (if any) firmware inventory  if C(installed), get installed firmware inventory  |
| share_mnt  |   no  |    | |  Local mount path of the Network share (CIFS, NFS) where the inventory file is going to be saved  Required if I(serialize = True)  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |


 
#### Examples

```
---
- name: Get SW Inventory
    dellemc_idrac_sw_inventory:
       idrac_ip:   "192.168.1.1"
       idrac_user: "root"
       idrac_pwd:  "calvin"
       share_mnt:  "/mnt/NFS/"
       choice:     "installed"
       serialize:  True

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
| idrac_user  |   no  |    | |  iDRAC user name  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  CIFS or NFS Network share  |
| idrac_port  |   no  |    | |  iDRAC port  |
| snmp_protocol  |   no  |  All  | <ul> <li>All</li>  <li>SNMPv3</li> </ul> |  S  N  M  P     p  r  o  t  o  c  o  l     s  u  p  p  o  r  t  e  d     -     i  f     C  (  A  l  l  )  ,     w  i  l  l     e  n  a  b  l  e     s  u  p  p  o  r  t     f  o  r     S  N  M  P  v  1  ,     v  2     a  n  d     v  3     p  r  o  t  o  c  o  l  s     -     i  f     C  (  S  N  M  P  v  3  )  ,     w  i  l  l     e  n  a  b  l  e     s  u  p  p  o  r  t     f  o  r     o  n  l  y     S  N  M  P  v  3     p  r  o  t  o  c  o  l  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| snmp_enable  |   no  |  enabled  | <ul> <li>enabled</li>  <li>disabled</li> </ul> |  S  N  M  P     A  g  e  n  t     s  t  a  t  u  s     -     i  f     C  (  e  n  a  b  l  e  d  )  ,     w  i  l  l     e  n  a  b  l  e     t  h  e     S  N  M  P     A  g  e  n  t     -     i  f     C  (  d  i  s  a  b  l  e  d  )  ,     w  i  l  l     d  i  s  a  b  l  e     t  h  e     S  N  M  P     A  g  e  n  t  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  if C(present), will perform create/add/enable operations  if C(absent), will perform delete/remove/disable operations  |
| snmp_discover_port  |   no  |  161  | |  SNMP discovery port  |
| snmp_community  |   no  |  public  | |  SNMP Agent community string  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share with read-write permission for ansible user  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| snmp_trap_port  |   no  |  162  | |  SNMP trap port  |
| share_user  |   yes  |  | |  Network share user in the format user@domain  |


 
#### Examples

```
- name: Configure SNMP
    dellemc_idrac_snmp:
      idrac_ip:             "192.168.1.1"
      idrac_user:           "root"
      idrac_pwd:            "calvin"
      share_name:           "\\\\192.168.10.10\\share"
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
| idrac_user  |   no  |    | |  iDRAC user name  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| idrac_port  |   no  |    | |  iDRAC port  |


 
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


## dellemc_idrac_ntp
Configure NTP settings

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Configure Network Time Protocol settings on iDRAC for synchronizing the iDRAC time using NTP instead of BIOS or host system times

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   no  |    | |  iDRAC user name  |
| ntp_servers  |   no  |    | |  List of IP Addresses of the NTP Servers  |
| idrac_port  |   no  |    | |  iDRAC port  |
| state  |   no  |  present  | |  if C(present), will enable the NTP option and add the NTP servers  if C(absent), will disable the NTP option  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |


 
#### Examples

```
---
- name: Configure NTP
    dellemc_idrac_ntp:
       idrac_ip:    "192.168.1.1"
       idrac_user:  "root"
       idrac_pwd:   "calvin"
       share_name:  "\\\\192.168.10.10\\share"
       share_user:  "user1"
       share_pwd:   "password"
       share_mnt:   "/mnt/share"
       ntp_server1: "10.20.30.40"
       ntp_server2: "20.30.40.50"
       ntp_server3: "30.40.50.60"
       state:       "present"

```



---


## dellemc_idrac_inventory
Returns the PowerEdge Server system inventory

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Returns the Dell EMC PowerEdge Server system inventory

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   no  |    | |  iDRAC user name  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| idrac_port  |   no  |    | |  i  D  R  A  C     p  o  r  t  |


 
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


## dellemc_idrac_location
Configure System location fields

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Configure System location fields

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_user  |   no  |    | |  iDRAC user name  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  Network file share  |
| idrac_port  |   no  |    | |  iDRAC port  |
| room_name  |   no  |    | |  Name of the Room in Data Center  |
| data_center_name  |   no  |    | |  Name of the Data Center where this system is located  |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| rack_name  |   no  |    | |  Rack Name  |
| rack_slot  |   no  |    | |  Rack slot number  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share with read-write permission for ansible user  |
| aisle_name  |   no  |    | |  Name of the Aisle in Data Center  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| share_user  |   yes  |  | |  Network share user in the format user@domain  |


 
#### Examples

```
# Configure System Location
- name: Configure System Location
    dellemc_idrac_location:
      idrac_ip:     "192.168.1.1"
      idrac_user:   "root"
      idrac_pwd:    "calvin"
      share_name:   "\\\\192.168.10.10\\share"
      share_user:   "user1"
      share_pwd:    "password"
      share_mnt:    "/mnt/share"
      data_center_name: "Data Center 1"
      aisle_name:   "Aisle 1"
      rack_name:    "Rack 1"
      rack_slot:    "Slot 1"
      room_name:    "Room 1"

```



---


---
Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
