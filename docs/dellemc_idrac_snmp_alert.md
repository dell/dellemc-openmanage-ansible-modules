# dellemc_idrac_snmp_alert
Configure SNMP Alert destination

  * [Synopsis](#Synopsis)
  * [Options](#Options)
  * [Examples](#Examples)

## <a name="Synopsis"></a>Synopsis
  Configure Alert destination settings on iDRAC:
    * Add an Alert destination
    * Modify an Alert destination settings
    * Delete an Alert destination

## <a name="Options"></a>Options

| Parameter    |  required  |  default  |  choices  |  comments |
|--------------|------------|-----------|-----------|-----------|
| idrac_ip    |  yes  |  |  |  iDRAC IP Address  |
| idrac_user  |  yes  |  |  |  iDRAC user name  |
| idrac_pwd   |  yes  |  |  |  iDRAC user password  |
| idrac_port  |  no   |  443  |  |  iDRAC port  |
| share_name  |   yes  |  | |  CIFS or NFS Network share  |
| share_user  |   yes  |  | |  Network share user in the format user@domain  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share with read-write permission for ansible user  |
| snmp_alert_dest |  yes  |  |  | List of hashes of SNMP Alert destinations |
| state  |  no  |  'present'  |  <ul><li>'present'</li><li>'absent'</li></ul>  | <ul><li>if C(present), will create/add/enable SNMP alert destination</li><li>if C(absent), will delete/remove a SNMP alert destination |

## <a name="Examples"></a>Examples

```
# Add SNMP alert destinations
- name: Add SNMP alert destinations
    dellemc_idrac_snmp_alert:
      idrac_ip:        "192.168.1.1"
      idrac_user:      "root"
      idrac_pwd:       "calvin"
      share_name:      "\\\\192.168.10.10\\share\\"
      share_user:      "user1"
      share_pwd:       "password"
      share_mnt:       "/mnt/share"
      snmp_alert_dest:
        - {"dest_address": "192.168.2.1", "state":"Enabled", "snmpv3_user_name": "admin"}
        - {"dest_address": "192.168.2.2", "state":"Enabled"}
      state:           "present"
```

```
# Disable the SNMP alert destination
- name: Disable SNMP alert destination
    dellemc_idrac_snmp_alert:
      idrac_ip:    "192.168.1.1"
      idrac_user:      "root"
      idrac_pwd:       "calvin"
      share_name:      "\\\\192.168.10.10\\share\\"
      share_user:      "user1"
      share_pwd:       "password"
      share_mnt:       "/mnt/share"
      snmp_alert_dest:
        - {"dest_address": "192.168.2.1", "state":"Disabled"}
      state:           "present"
```

```
# Delete the SNMP alert destination
- name: Delete SNMP alert destination
    dellemc_idrac_snmp_alert:
      idrac_ip:    "192.168.1.1"
      idrac_user:      "root"
      idrac_pwd:       "calvin"
      share_name:      "\\\\192.168.10.10\\share\\"
      share_user:      "user1"
      share_pwd:       "password"
      share_mnt:       "/mnt/share"
      snmp_alert_dest:
        - {"dest_address": "192.168.2.2"}
      state:           "absent"
```

---

Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
