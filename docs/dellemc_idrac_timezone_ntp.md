# dellemc_idrac_timezone_ntp
Configure Time Zone and NTP settings

  * [Synopsis](#Synopsis)
  * [Options](#Options)
  * [Examples](#Examples)

## <a name="Synopsis"></a>Synopsis
 Configure Time Zone and NTP settings

## <a name="Options"></a>Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_ip  |   yes  |    | |  iDRAC IP Address  |
| idrac_user  |   yes  |    | |  iDRAC user name  |
| idrac_pwd  |   yes  |    | |  iDRAC user password  |
| idrac_port  |   no  |    | |  iDRAC port  |
| share_name  |   yes  |  | |  CIFS or NFS Network share  |
| share_user  |   yes  |  | |  Network share user in the format user@domain  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share with read-write permission for ansible user  |
| timezone  |   no  |    | |  time zone e.g. "Asia/Kolkata"  |
| ntp_servers  |   no  |    | |  List of IP Addresses of the NTP Servers  |
| state  |   no  |  present  | |  <ul><li>if C(present), will enable the NTP option and add the NTP servers</li><li>if C(absent), will disable the NTP option</li></ul>  |

## <a name="Examples"></a>Examples

```
# Set Timezone, Enable NTP and add NTP Servers
- name: Configure TimeZone and NTP
    dellemc_idrac_timezone_ntp:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      timezone:   "Asia/Kolkata"
      ntp_servers: ["10.10.10.10", "10.10.10.11"]
      state:      "present"
```

```
# Disable NTP
- name: Configure TimeZone and NTP
    dellemc_idrac_timezone_ntp:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      state:      "absent"
```

---

Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
