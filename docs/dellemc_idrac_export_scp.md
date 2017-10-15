# dellemc_idrac_export_scp
Export Server Configuration Profile (SCP) to network share

  * [Synopsis](#Synopsis)
  * [Options](#Options)
  * [Examples](#Examples)

## <a name="Synopsis"></a>Synopsis
 Export Server Configuration Profile to a given network share (CIFS, NFS)

## <a name="Options"></a>Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| share_name  |   yes  |  | |  CIFS or NFS Network share  |
| share_user  |   yes  |  | |  Network share user in the format 'user@domain' if user is part of a domain else 'user'  |
| share_pwd  |   yes  |  | |  Network share user password  |
| scp_components  |   no  |  ALL  | <ul> <li>ALL</li>  <li>IDRAC</li>  <li>BIOS</li>  <li>NIC</li>  <li>RAID</li> </ul> |  <ul><li>if C(ALL), will export all components configurations in SCP file</li><li>if C(IDRAC), will export iDRAC configuration in SCP file</li><li>if C(BIOS), will export BIOS configuration in SCP file</li><li>if C(NIC), will export NIC configuration in SCP file</li><li>if C(RAID), will export RAID configuration in SCP file</li></ul>  |
| job_wait  |   no  |  True  | |  <ul><li>if C(True), will wait for the SCP export job to finish and return the job completion status</li><li>if C(False), will return immediately with a JOB ID after queueing the SCP export jon in LC job queue</li></ul>  |

## <a name="Examples"></a>Examples

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
```

```
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

Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
