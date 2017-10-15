# dellemc_idrac_nic
Configure iDRAC Network settings

  * [Synopsis](#Synopsis)
  * [Options](#Options)
  * [Examples](#Examples)

## <a name="Synopsis"></a>Synopsis
 Configure following iDRAC Network settings:
   * NIC Selection
   * IPv4 Settings
   * Auto-Config Settings
   * DNS Settings

## <a name="Options"></a>Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| idrac_pwd  |   no  |  | |  iDRAC user password  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| share_name  |   yes  |  | |  CIFS or NFS Network share  |
| share_user  |   yes  |  | |  Network share user in the format user@domain if user is part of a domain else 'user'  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share with read-write permission for ansible user  |
| nic_selection  |   no  |  Dedicated  | <ul> <li>Dedicated</li>  <li>LOM1</li>  <li>LOM2</li>  <li>LOM3</li>  <li>LOM4</li> </ul> |  NIC Selection mode  |
| nic_failover  |   no  |    | <ul> <li>None</li>  <li>LOM1</li>  <li>LOM2</li>  <li>LOM3</li>  <li>LOM4</li>  <li>All</li> </ul> |  Failover network if NIC selection fails  |
| nic_autodedicated  |   no  |  False  | |  <ul><li>if C(True), will enable the auto-dedicated NIC option</li><li>if C(False), will disable the auto-dedicated NIC option</li></ul>  |
| nic_duplex  |   no  |  Full  | <ul> <li>Full</li>  <li>Half</li> </ul> |  <ul><li>if C(Full), will enable the Full-Duplex mode</li><li>if C(Half), will enable the Half-Duplex mode</li></ul>  |
| nic_speed  |   no  |  1000  | <ul> <li>10</li>  <li>100</li>  <li>1000</li> </ul> |  Network Speed  |
| nic_autoneg  |  no  |  False  | |  <ul><li>if C(True), will enable auto negotiation</li><li>if C(False), will disable auto negotiation</li></ul>  |
| dns_register |  no  |  'Disabled' | <ul><li>'Enabled'</li><li>'Disabled'</li></ul> | <ul><li>if C(Enabled), will enable the DNS registration option for iDRAC</li><li>if C(Disabled), will disable the DNS registration option for iDRAC</li></ul> |
| dns_idrac_name |  no  |  |  | DNS name of iDRAC |
| dns_domain_from_dhcp | no | 'Disabled' | <ul><li>'Enabled'</li><li>'Disabled'</li></ul> | <ul><li>if C(Enabled), will use the DHCP server for assigning the DNS Domain Name for iDRAC</li><li>if C(Disabled), will not use the DHCP server for assigning the DNS Domain Name</li></ul> |
| dns_domain_name |  no  | | | iDRAC DNS Domain Name |
| nic_auto_config |  no  | 'Disabled' | <ul><li>'Disabled'</li><li>'Enable Once'</li><li>'Enable Once After Reset'</li></ul> | <ul><li>if C(Disabled), will disable the DHCP Auto-Configuration option</li><li>if C(Enable Once), will enable the DHCP Auto-Configuration option only once</li><li>if C(Enable Once After Reset), will enable the DHCP Auto-Configuration option only once after iDRAC reset</li></ul> |
| ipv4_enable | no | 'Enabled' | <ul><li>'Enabled'</li><li>'Disabled'</li></ul> | <ul><li>if C(Enabled), will enable the IPv4 stack</li><li>if C(Disabled), will disable the IPv4 stack</li></ul> |
| ipv4_dhcp_enable | no | 'Disabled' | <ul><li>'Enabled'<li><li>'Disabled'</li></ul> | <ul><li>if C(Enabled), will use DHCP to assign the IPv4 address</li><li>if C(Disabled), will not use DHCP to assign the IPv4 address</li></ul> |
| ipv4_static | no |  |  | iDRAC Static IPv4 Address |
| ipv4_static_gw | no |  |  | iDRAC Static IPv4 gateway |
| ipv4_static_mask | no |  |  | iDRAC Static IPv4 subnet mask |
| ipv4_dns_from_dhcp | no | 'Disabled'  | <ul><li>'Enabled'</li><li>'Disabled'</li></ul> | <ul><li>if C(Enabled), will use DHCP server for assigning the DNS server IPv4 adresses</li><li>if C(Disabled), will not use DHCP server for assigning DNS server IPv4 addresses</li></ul> |
| ipv4_preferred_dns | no |  |  | Preferred DNS Server IPv4 address |
| ipv4_alternate_dns | no |  |  | Alternate DNS Server IPv4 address |
| vlan_enable | no | 'Disabled' | <ul><li>Enabled</li><li>Disabled</li></ul> | <ul><li>if C(Enabled), will enable the VLAN capabilities</li><li>if C(Disable), will disable the VLAN capabilities</li></ul>NOTE: This is only applicable to iDRACs on Racks and Towers. |
| vlan_id | no | 1 |  | VLAN ID for the network VLAN configuration<br>Integer values: 1 - 4096 <br> NOTE: This is only applicable to iDRAC on Racks and Towers  |
| vlan_priority | no | 0 |  | VLAN Priority for the network VLAN configuration<br>Integer values: 0 - 7 <br> NOTE: This is only applicable to iDRACs on Racks and Towers |

## <a name="Examples"></a>Examples

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

Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
