# dellemc_idrac_sw_inventory
Get Firmware Inventory

  * [Synopsis](#Synopsis)
  * [Options](#Options)
  * [Examples](#Examples)
  * [Return Values](#Return Values)

## Synopsis
 Get Firmware Inventory

## Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| choice  |   no  |  installed  | |  if C(all), get both installed and available (if any) firmware inventory  if C(installed), get installed firmware inventory  |
| serialize  |   no  |  False  | |  if C(True), create '_inventory' and '_master' folders relative to I(share_mnt) and save the installed firmware inventory in a file named 'config.xml' in the '_inventory' directory  if C(True), then I(share_mnt) must be provided  |
| share_mnt  |   no  |    | |  Locally mounted absolute path of the Network share (CIFS, NFS) where the inventory file is going to be saved. You can also provide a local folder if you want to save the firmware inventory on local file system  Required if I(serialize = True)  |

## Examples

```
# Get Available as well as Installed Firmware Inventory
- name: Get Available and Installed Firmware Inventory
    dellemc_idrac_sw_inventory:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      choice:     "all"

# Get Installed Firmware Inventory
- name: Get Installed Firmware Inventory
    dellemc_idrac_sw_inventory:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      choice:     "installed"

# Serialize the FW inventory to a file
- name: Serialize the FW inventory
    dellemc_idrac_sw_inventory:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_mnt:  "/mnt/NFS/share"
      choice:     "installed"
      serialize:  True
```
## Return Values

Common return values are documented here [Return Values](http://docs.ansible.com/ansible/latest/common_return_values.html), the following are the fields unique to this module:

|  name |  description  |  returned  |  type  |  sample  |
|-------|---------------|------------|--------|----------|
| Firmware | Components and their Firmware versions. List of dictionaries, one dict per Firmware | always | list | [{"BuildNumber": "40", "Classifications": "10", "ComponentID": "25227", "ComponentType": "FRMW", "DeviceID": null, "ElementName": "Integrated Dell Remote Access Controller", "FQDD": "iDRAC.Embedded.1-1", "IdentityInfoType": "OrgID:ComponentType:ComponentID", "IdentityInfoValue": "DCIM:firmware:25227", "InstallationDate": "2017-06-03T23:05:47Z", "InstanceID": "DCIM:INSTALLED#iDRAC.Embedded.1-1#IDRACinfo", "IsEntity": "true", "Key": "DCIM:INSTALLED#iDRAC.Embedded.1-1#IDRACinfo", "MajorVersion": "2", "MinorVersion": "41", "RevisionNumber": "40", "RevisionString": null, "Status": "Installed", "SubDeviceID": null, "SubVendorID": null, "Updateable": "true", "VendorID": null, "VersionString": "2.41.40.40", "impactsTPMmeasurements": "false" }]  |

---

Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
