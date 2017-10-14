# dellemc_idrac_snmp
Configure SNMP settings on iDRAC

  * Synopsis
  * Options
  * Examples

## Synopsis
 Configures SNMP settings on iDRAC

## Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| share_name  |   yes  |  | |  CIFS or NFS Network share  |
| share_user  |   yes  |  | |  Network share user in the format 'user@domain' if user is part of a domain else 'user'  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share with read-write permission for ansible user  |
| snmp_enable  |   no  |  Enabled  | <ul> <li>Enabled</li>  <li>Disabled</li> </ul> | <ul><li>if C(enabled), will enable the SNMP Agent</li> <li>if C(disabled), will disable the SNMP Agent</li></ul> | 
| snmp_protocol  |   no  |  All  | <ul> <li>All</li>  <li>SNMPv3</li> </ul> | <ul><li>if C(All), will enable support for SNMPv1, v2 and v3 protocols</li><li>if C(SNMPv3), will enable support for only SNMPv3 protocol</li></ul> |
| snmp_community  |   no  |  public  | |  SNMP Agent community string  |
| snmp_port  |   no  |  161  | |  SNMP discovery port  |
| snmp_trap_port  |   no  |  162  | |  SNMP trap port  |
| snmp_trap_format  |   no  |  SNMPv1  | <ul> <li>SNMPv1</li>  <li>SNMPv2</li>  <li>SNMPv3</li> </ul> | <ul><li>if C(SNMPv1), will configure iDRAC to use SNMPv1 for sending traps</li><li>if C(SNMPv2), will configure iDRAC to use SNMPv2 for sending traps</li><li>if C(SNMPv3), will configure iDRAC to use SNMPv3 for sending traps</li></ul> |

## Examples

```
# Enable SNMP Agent and configure SNMP parameters
- name: Configure SNMP
    dellemc_idrac_snmp:
      idrac_ip:             "192.168.1.1"
      idrac_user:           "root"
      idrac_pwd:            "calvin"
      share_name:           "\\192.168.10.10\share"
      share_user:           "user1"
      share_pwd:            "password"
      share_mnt:            "/mnt/share"
      snmp_agent_enable:    "Enabled"
      snmp_protocol:        "All"
      snmp_community:       "public"
      snmp_port:            "161"
      snmp_trap_port:       "162"

# Disable SNMP Agent
- name: Configure SNMP
    dellemc_idrac_snmp:
      idrac_ip:             "192.168.1.1"
      idrac_user:           "root"
      idrac_pwd:            "calvin"
      share_name:           "\\192.168.10.10\share"
      share_user:           "user1"
      share_pwd:            "password"
      share_mnt:            "/mnt/share"
      snmp_agent_enable:    "Disabled"
```

---

Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
