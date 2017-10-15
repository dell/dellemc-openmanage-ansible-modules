# dellemc_idrac_export_tsr
Export TSR logs to a network share

  * [Synopsis](#Synopsis)
  * [Options](#Options)
  * [Examples](#Options)

## <a name="Synopsis"></a>Synopsis
 Export TSR logs to a network share (CIFS, NFS)

## <a name="Options"></a>Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_name  |   yes  |  | |  CIFS or NFS Network share  |
| share_user  |   yes  |  | |  Network share user in the format 'user@domain' if user is part of a domain, else 'user'  |

## <a name="Examples"></a>Examples

```
# Export TSR to a CIFS Network Share
- name: Export TSR to a CIFS network share
    dellemc_idrac_export_tsr:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
```

```
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

Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
