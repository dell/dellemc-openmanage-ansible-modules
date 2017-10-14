# dellemc_idrac_boot_to_nw_iso
Boot to a network ISO image

  * Synopsis
  * Options
  * Examples

## Synopsis
 Boot to a network ISO image. Reboot appears to be immediate

## Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| idrac_pwd  |   no  |  | |  iDRAC user password  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| share_name  |   yes  |  | |  Network file share (either CIFS or NFS)  |
| share_user  |   yes  |  | |  Network share user in the format 'user@domain' if user is part of a domain else 'user'  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share specified in I(share_name) with read-write permission for ansible user  |
| iso_image  |   yes  |  | |  Path to ISO image relative to the I(share_name)  |
| job_wait  |   no  |  True  | |  |

 
## Examples


```
- name: Boot to Network ISO
    dellemc_idrac_boot_to_nw_iso:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      iso_image:  "uninterrupted_os_installation_image.iso"

```

---

Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
