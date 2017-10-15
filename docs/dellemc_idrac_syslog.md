# dellemc_idrac_syslog
Configure remote system logging

  * [Synopsis](#Synopsis)
  * [Options](#Options)
  * [Examples](#Examples)

## <a name="Synopsis"></a>Synopsis
 Configure remote system logging settings to remotely write RAC log and System Event Log (SEL) to an external server

## <a name="Options"></a>Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| syslog_servers  |   no  |    | |  List of IP Addresses of the Remote Syslog Servers  |
| syslog_port  |   no  |  514  | |  Port number of remote servers  |
| state  | no  |  present | <ul> <li>present</li>  <li>absent</li> </ul> |  <ul><li>if C(present), will enable the remote syslog option and add the remote servers in I(syslog_servers)</li><li>if C(absent), will disable the remote syslog option</li></ul>  |

## <a name="Examples"></a>Examples

```
- name: Configure Remote Syslog
    dellemc_idrac_syslog:
       idrac_ip:       "192.168.1.1"
       idrac_user:     "root"
       idrac_pwd:      "calvin"
       share_name:     "\\192.168.10.10\share"
       share_user:     "user1"
       share_pwd:      "password"
       share_mnt:      "/mnt/share"
       syslog_servers: ["192.168.20.1", ""192.168.20.2", ""192.168.20.3"]
       syslog_port:    514
       state:          "present"

```

```
- name: Disable Remote Syslog
    dellemc_idrac_syslog:
      idrac_ip:       "192.168.1.1"
      idrac_user:     "root"
      idrac_pwd:      "calvin"
      share_name:     "\\192.168.10.10\share"
      share_user:     "user1"
      share_pwd:      "password"
      share_mnt:      "/mnt/share"
      state:          "absent"
```

---

Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
