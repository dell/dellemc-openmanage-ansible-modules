# dellemc_idrac_import_scp
Import SCP from a network share

  * [Synopsis](#Synopsis)
  * [Options](#Options)
  * [Examples](#Examples)

## <a name="Synopsis"></a>Synopsis
 Import a given Server Configuration Profile (SCP) file from a network share (CIFS, NFS)

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
| scp_file  |   yes  |    | |  Server Configuration Profile file name relative to I(share_mnt)  |
| scp_components  |   no  |  ALL  | <ul> <li>ALL</li>  <li>IDRAC</li>  <li>BIOS</li>  <li>NIC</li>  <li>RAID</li> </ul> |  <ul><li>if C(ALL), will import all components configurations from SCP file</li><li>if C(IDRAC), will import iDRAC comfiguration from SCP file</li><li>if C(BIOS), will import BIOS configuration from SCP file</li><li>if C(NIC), will import NIC configuration from SCP file</li><li>if C(RAID), will import RAID configuration from SCP file</li><ul>  |
| reboot  |   no  |  False  | |  Reboot after importing the SCP  |
| job_wait  |   no  |  True  | |  <ul><li>if C(True), wait for the import scp job to be completed and return the status</li><li>if C(False), return immediately after creating a import scp job</li></ul>  |

## <a name="Examples"></a>Examples

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
```

```
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

Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
