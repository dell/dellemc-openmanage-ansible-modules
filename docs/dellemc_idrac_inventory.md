# dellemc_idrac_inventory
Returns the PowerEdge Server hardware inventory

  * [Synopsis](#Synopsis)
  * [Options](#Options)
  * [Examples](#Examples)

## <a name="Synopsis"></a>Synopsis
 Returns the Dell EMC PowerEdge Server hardware inventory

## <a name="Options"></a>Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| idrac_port  |   no  |  443  | |  iDRAC port  |

## <a name="Examples"></a>Examples

```
- name: Get System Inventory
  dellemc_idrac_inventory:
    idrac_ip:   "192.168.1.1"
    idrac_user: "root"
    idrac_pwd:  "calvin"
```

---

Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
