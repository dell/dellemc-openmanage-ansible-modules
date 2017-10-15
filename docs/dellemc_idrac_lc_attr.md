# dellemc_idrac_lc_attr
Configure iDRAC Lifecycle Controller attributes

  * [Synopsis](#Synopsis)
  * [Options](#Options)
  * [Examples](#Examples)

## <a name="Synopsis"></a>Synopsis
 Configure following iDRAC Lifecycle Controller attributes:
   * CollectSystemInventoryOnRestart (CSIOR)

## <a name="Options"></a>Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| share_name  |   yes  |  | |  Network file share (either CIFS or NFS)  |
| share_user  |   yes  |  | |  Network share user in the format 'user@domain' if user is part of a domain, else 'user'  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share specified in I(share_name) with read-write permission for ansible user  |
| csior  |   no  |  'Enabled'  | <ul> <li>Enabled</li>  <li>Disabled</li> </ul> |  <ul><li>if C(Enabled), will enable the CSIOR</li><li>if C(Disabled), will disable the CSIOR</li></ul><br>NOTE: I(reboot) should be set to C(True) to apply any changes  |
| reboot  |   no  |  False  | |  <ul><li>if C(True), will restart the system after applying the changes</li><li>if C(False), will not restart the system after applying the changes</li></ul>  |

## <a name="Examples"></a>Examples

```
# Enable CollectSystemInventoryOnRestart (CSIOR) LC attribute
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
```

```
# Disable CollectSystemInventoryOnRestart (CSIOR) LC attribute
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

Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
