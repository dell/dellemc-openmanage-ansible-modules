# dellemc_idrac_virtual_drive
Create/delete virtual drives

  * [Synopsis](#Synopsis)
  * [Options](#Options)
  * [Examples](#Examples)

## <a name="Synopsis"></a>Synopsis
  * Create and delete virtual drives

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
| vd_name | yes |  |  | Name of the Virtual Drive |
| vd_size | no  |  |  | Size (in bytes) of the Virtual Drive. For e.g. if you want to create a virtual drive of size 1TB, then set the vd_size to 1099511627776 (1&ast;1024&ast;1024&ast;1024&ast;1024 = 1099511627776). Please make sure that the 1TB of space is available on physical drives that are to be used for creating the VD. |
| controller_fqdd |  yes  | | | FQDD of the storage controller, for e.g. "RAID.Integrated-1.1" |
| pd_slots | no | [] |  | List of slot numbers of Physical Disks that are to be used for the VD creation. For e.g. if you want to use Physical Disks in Slots 0, 1, 2 for creating a VD, then you need to set ```pd_slots``` to ```[0, 1, 2]```. Please note that ```pd_slots``` and ```span_length``` arguments are mutually exclusive. |
| raid_level | no | 'RAID 0' | <ul><li>'RAID 0'</li><li>'RAID 1'</li><li>'RAID 5'</li><li>'RAID 50'</li><li>'RAID 6'</li><li>'RAID 60'</li></ul> | <ul><li>Select the RAID level for the new virtual drives.</li><li>RAID Levels can be one of the following:<ul><li>'RAID 0': Striping without parity</li><li>'RAID 1': Mirroring without parity</li><li>'RAID 5': Striping with distributed parity</li><li>'RAID 50': Combines multiple RAID 5 sets with striping</li><li>'RAID 6': Striping with dual parity</li><li>'RAID 60': Combines multiple RAID 6 sets with striping</li></ul></li></ul> |
| read_cache_policy | no | 'NoReadAhead' | <ul><li>'NoReadAhead'</li><li>'ReadAhead'</li><li>'Adaptive'</li></ul> | Read cache policy of the virtual disk |
| write_cache_policy | no | 'WriteThrough' | <ul><li>'WriteThrough'</li><li>'WriteBack'</li><li>'WriteBackForce'</li></ul> | Write cache policy of the virtual disk |
| disk_cache_policy | no | 'Default' | <ul><li>'Default'</li><li>'Enabled'</li><li>'Disabled'</li></ul> | Physical Disk caching policy of all members of a Virtual Disk |
| stripe_size | no | 65535 | <ul><li>65535</li><li>131072</li><li>262144</li><li>524288</li><li>1048576</li></ul> | Stripe size (in bytes) of the virtual disk |
| span_depth | no | | | Number of spans in the virtual disk. Required if I(status == 'present') |
| span_length | no | | | Number of physical disks per span on a virtual disk. Required if I(status == 'present') |
| state | no | 'present' | <ul><li>'present'</li><li>'absent'</li></ul> | <ul><li>if C(present), will perform create/add operations</li><li>if C(absent), will perform delete/remove operations</li></ul> |

## <a name="Examples"></a>Examples

```
# Create a virtual drive with RAID 5 and a span length of 5 physical disks
# if no slot numbers are provided, then virtual drive will be created using the
# physical disks that are available
- name: Create VD
    dellemc_idrac_virtual_drive:
      idrac_ip:     "192.168.1.1"
      idrac_user:   "root"
      idrac_pwd:    "calvin"
      share_name:   "\\\\192.168.10.10\\share"
      share_user:   "user1@domain"
      share_pwd:    "password"
      share_mnt:    "/mnt/share"
      vd_name:      "Virtual_Drive_0"
      controller_fqdd: "RAID.Integrated.1-1"
      raid_level:   "RAID 5"
      stripe_size:  65535
      span_depth:   1
      span_length:  5
      state:        "present"
```

```
# Create a virtual drive with RAID 5 and physical disks having slot numbers
# 0, 1, 2, 3, 4 and 5.
- name: Create VD
    dellemc_idrac_virtual_drive:
      idrac_ip:     "192.168.1.1"
      idrac_user:   "root"
      idrac_pwd:    "calvin"
      share_name:   "\\\\192.168.10.10\\share"
      share_user:   "user1@domain"
      share_pwd:    "password"
      share_mnt:    "/mnt/share"
      vd_name:      "Virtual_Drive_0"
      controller_fqdd: "RAID.Integrated.1-1"
      pd_slots:     [0, 1, 2, 3, 4, 5]
      raid_level:   "RAID 5"
      stripe_size:  65535
      span_depth:   1
      state:        "present"
```

```
# Delete a virtual drive
- name: Create VD
    dellemc_idrac_virtual_drive:
      idrac_ip:     "192.168.1.1"
      idrac_user:   "root"
      idrac_pwd:    "calvin"
      share_name:   "\\\\192.168.10.10\\share"
      share_user:   "user1@domain"
      share_pwd:    "password"
      share_mnt:    "/mnt/share"
      vd_name:      "Virtual_Drive_0"
      controller_fqdd: "RAID.Integrated.1-1"
      state:        "absent"
```

---

Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
