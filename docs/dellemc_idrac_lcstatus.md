# dellemc_idrac_lcstatus
Returns the Lifecycle Controller status

  * Synopsis
  * Options
  * Examples

## Synopsis
 Returns the Lifecycle Controller Status on a Dell EMC PowerEdge Server

## Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| idrac_port  |   no  |  443  | |  iDRAC port  |

## Examples

```
---
- name: Get Lifecycle Controller Status
    dellemc_idrac_lcstatus:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"

```

---

Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
