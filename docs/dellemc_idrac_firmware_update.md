# dellemc_idrac_firmware_update
Firmware update from a repository on a network share (CIFS, NFS)

  * [Synopsis](#Synopsis)
  * [Options](#Options)
  * [Examples](#Examples)

## <a name="Synopsis"></a>Synopsis
  * Update the Firmware by connecting to a network repository (either CIFS or NFS network share) that contains a catalog of available updates
  * Network share should contain a valid repository of Update Packages (DUPs) and a catalog file describing the DUPs
  * All applicable updates contained in the repository is applied to the system
  * This feature is only available with iDRAC Enterprise License

## <a name="Options"></a>Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| share_name  |   yes  |  | |  Network file share (either CIFS or NFS) containing the Catalog file and Update Packages (DUPs)  |
| share_user  |   yes  |  | |  Network share user in the format 'user@domain' if user is part of a domain else 'user'  |
| share_pwd  |   yes  |  | |  Network share user password  |
| catalog_file_name  |   no  |  Catalog.xml  | |  Catalog file name relative to the I(share_name)  |
| apply_updates  |   no  |  True  | |  <ul><li>if C(True), Install Updates</li><li>if C(False), do not Install Updates</li></ul>  |
| reboot  |   no  |  False  | |  <ul><li>if C(True), reboot for applying the updates</li><li>if C(False), do not reboot for applying the update<li><ul>  |
| job_wait  |   no  |  True  | |  <ul><li>if C(True), will wait for update JOB to get completed</li><li>if C(False), return immediately after creating the update job in job queue</li></ul>  |

## <a name="Examples"></a>Examples

```
# Update firmware from a repository on a CIFS Network Share, Reboot = False
- name: Update firmware from repository on a Network Share
    dellemc_idrac_firmware_update:
       idrac_ip:   "192.168.1.1"
       idrac_user: "root"
       idrac_pwd:  "calvin"
       share_name: "\\192.168.10.10\share"
       share_user: "user1"
       share_pwd:  "password"
       catalog_file_name:  "Catalog.xml"
       apply_updates: True
       reboot:     False
       job_wait:   True
```

---

Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
