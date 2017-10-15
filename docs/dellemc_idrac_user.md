# dellemc_idrac_user
Configures an iDRAC local User

  * [Synopsis](#Synopsis)
  * [Options](#Options)
  * [Examples](#Examples)

## <a name="Synopsis"></a>Synopsis
 Configures an iDRAC local user

## <a name="Options"></a>Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_ip  |   yes  |    | |  iDRAC IP Address  |
| idrac_user  |   yes  |    | |  iDRAC user name  |
| idrac_pwd  |   yes  |    | |  iDRAC user password  |
| idrac_port  |   no  | 443 | |  iDRAC port  |
| share_name  |   yes  |  | |  CIFS or NFS Network share  |
| share_user  |   yes  |  | |  Network share user in the format 'user@domain' if user is part of domain, else 'user'  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share with read-write permission for ansible user  |
| user_name  |   yes  |  | |  User name to be configured  |
| user_pwd  |   no  |    | |  User password  |
| user_priv |  no  |  | <ul><li>Administrator</li><li>Operator</li><li>ReadOnly</li></ul> | User privileges |
| state  |   |  present  | <ul> <li>present</li>  <li>absent</li>  <li>enable</li>  <li>disable</li> </ul> |  <ul<li>if C(present), will create/add/modify an user</li><li>if C(absent), will delete the user</li><li>if C(enable), will enable the user</li><li>if C(disable), will disable the user</li></ul>  |
 
## <a name="Examples"></a>Examples

```
# Add a new iDRAC Local User "newuser"
- name: Add a new iDRAC User
    dellemc_idrac_user:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      user_name:  "newuser"
      user_pwd:   "password"
      user_priv:  "Administrator"
      state:      "present"
```

```
- name: Change password for the "newuser"
    dellemc_idrac_user:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      user_name:  "newuser"
      user_pwd:   "newpassword"
      state:      "present"
```

```
- name: Change privilege for the "newuser"
    dellemc_idrac_user:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      user_name:  "newuser"
      user_priv:  "Operator"
      state:      "present"
```

```
- name: Delete "newuser"
    dellemc_idrac_user:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      user_name:  "newuser"
      state:      "absent"
```

---

Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
