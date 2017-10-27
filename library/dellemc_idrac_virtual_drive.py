#! /usr/bin/python
# _*_ coding: utf-8 _*_

#
# Dell EMC OpenManage Ansible Modules
#
# Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved.
# Dell, EMC, and other trademarks are trademarks of Dell Inc. or its
# subsidiaries. Other trademarks may be trademarks of their respective owners.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: dellemc_idrac_virtual_drive
short_description: Create or delete virtual drives
version_added: "2.3"
description:
    - Create or delete virtual drives
options:
  idrac_ip:
    required: True
    description:
      - iDRAC IP Address
    type: 'str'
  idrac_user:
    required: True
    description:
      - iDRAC user name
    type: 'str'
  idrac_pwd:
    required: True
    description:
      - iDRAC user password
    type: 'str'
  idrac_port:
    required: False
    description:
      - iDRAC port
    type: 'int'
  share_name:
    required: True
    description:
      - Network file share
  share_user:
    required: True
    description:
      - Network share user in the format 'user@domain' if user is part of a domain, else 'user'
  share_pwd:
    required: True
    description:
      - Network share user password
  share_mnt:
    required: True
    description:
      - Local mount path of the network file share specified in I(share_name) with read-write permission for ansible user
  vd_name:
    required: True
    description:
      - Name of the Virtual Drive
    default: None
  vd_size:
    required: False
    description:
      - Size (in bytes) of the Virtual Drive. For e.g. if you want to create a virtual drive of size 1TB, then set the vd_size to 1099511627776 (1 * 1024 * 1024 * 1024 * 1024 = 1099511627776 bytes). Please make sure that the 1TB of space is available on physical drives that are to be used for creating the VD.
  controller_fqdd:
    required: True
    description:
      - Fully Qualified Device Descriptor (FQDD) of the storage controller, for e.g. 'RAID.Integrated.1-1'.
    type: 'str'
  pd_slots:
    required: False
    description:
      - List of slots for physical disk that are be used for the VD creation. For e.g. if you want to use Physical Disks in Slots 0, 1, 2 for creating a VD, then you need to set I(pd_slots) to [0, 1, 2]. Please note that I(pd_slots) and I(span_length) arguments are mutually exclusive.
    default: []
    type: 'list'
  raid_level:
    required: False
    description:
      - Select the RAID Level for the new virtual drives.
      - RAID Levels can be one of the following:
          RAID 0: Striping without parity
          RAID 1: Mirroring without parity
          RAID 5: Striping with distributed parity
          RAID 50: Combines multiple RAID 5 sets with striping
          RAID 6: Striping with dual parity
          RAID 60: Combines multiple RAID 6 sets with striping
    choices: ['RAID 0', 'RAID 1', 'RAID 5', 'RAID 6', 'RAID 10', 'RAID 50', 'RAID 60']
    default: 'RAID 0'
    type: 'str'
  read_cache_policy:
    required: False
    description:
      - Read Cache policy of the virtual disk
    choices: ["NoReadAhead", "ReadAhead", "Adaptive"]
    default: "NoReadAhead"
  write_cache_policy:
    required: False
    description:
      - Write cache policy of the virtual disk
    choices: ["WriteThrough", "WriteBack", "WriteBackForce"]
    default: "WriteThrough"
  disk_cache_policy:
    required: False
    description:
      - Physical Disk caching policy of all members of a Virtual Disk
    choices: ["Default", "Enabled", "Disabled"]
    default: "Default"
    type: 'str'
  stripe_size:
    required: False
    description:
      - Stripe size (in bytes) of the virtual disk
          65535   - 65KB
          131072  - 128KB
          262144  - 256KB
          524288  - 512KB
          1048576 - 1MB
    choices: [65535, 131072, 262144, 524288, 1048576]
    default:65535 
    type: 'int'
  span_depth:
    required: False
    description:
      - Number of spans in the virtual disk.
      - If not specified, default is single span which is used for RAID 0, 1, 5 and 6. RAID 10, 50 and 60 require a span depth of at least 2.
    default: 1
    type: 'int'
  span_length:
    required: False
    description:
      - Number of physical disks per span on a virtual disk.
      - Minimum requirements for given RAID Level must be met.
      - Either one of I(pd_slots) and I(span_length) must be specified for creating a virtual disk
    default: None
    type: 'int'
  state:
    required: False
    description:
      - if C(present), will perform create/add operations
      - if C(absent), will perform delete/remove operations
    choices: ['present', 'absent']
    default: 'present'

requirements: ['Dell EMC OpenManage Python SDK']
author: "OpenManageAnsibleEval@Dell.com"
'''

EXAMPLES = '''
# Create a virtual drive with RAID 5 and a span length of 5 physical disks
# if no slot numbers are provided, then virtual drive will be created using the
# physical disks that are available. If no Virual Disk size is specified, then
# the size of the virtual disks will be auto-determined based on the RAID level
# For e.g., in the below example, if all the Physical Disks are of capacity of
# 200GB and no vd_size is specified, then the Virtual Disk will be created with
# space efficiency of (1-1/n = 1-1/5 = 80% of 1000GB = 800GB)

- name: Create VD
    dellemc_idrac_virtual_drive:
      idrac_ip:      "192.168.1.1"
      idrac_user:    "root"
      idrac_pwd:     "calvin"
      share_name:    "\\\\192.168.10.10\\share"
      share_user:    "user1"
      share_pwd:     "password"
      share_mnt:     "/mnt/share"
      vd_name:       "Virtual_Drive_0"
      controller_fqdd: "RAID.Integrated.1-1"
      raid_level:    "RAID 5"
      media_type:    "HDD"
      bus_protocol:  "SAS"
      stripe_size:   65536
      span_depth:    1
      span_length:   5
      state:         "present"

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
      media_type:   "HDD"
      bus_protocol: "SAS"
      stripe_size:  65536
      span_depth:   1
      state:        "present"

# Delete a virtual drive

- name: Delete Virtual Drive
    dellemc_idrac_virtual_drive:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      virtual_drive_name:  "Virtual_Drive_0"
      controller_fqdd: "RAID.Integrated.1-1"
      state:       "absent"
'''

RETURN = '''
'''

import traceback
from ansible.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
try:
    from omsdk.sdkcenum import TypeHelper
    from omdrivers.lifecycle.iDRAC.RAIDHelper import RAIDHelper
    from omdrivers.enums.iDRAC.RAID import (
        DiskCachePolicyTypes, RAIDactionTypes, RAIDTypesTypes,
        RAIDdefaultReadPolicyTypes, RAIDdefaultWritePolicyTypes,
        StripeSizeTypes
    )
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False

MIN_SPAN_LENGTH = {
    "RAID 0": 2,
    "RAID 1": 2,
    "RAID 5": 3,
    "RAID 6": 4,
    "RAID 10": 4,
    "RAID 50": 6,
    "RAID 60": 8
}

def _virtual_drive_exists(idrac, module):
    """
    check whether a virtual drive exists

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    vd = idrac.config_mgr.RaidHelper.find_virtual_disk(
            Name=module.params['vd_name'])

    if vd:
        return True

    return False


def _create_virtual_drive(idrac, module):
    """
    Create a virtual drive

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    msg = {}

    span_length = module.params.get('span_length')
    span_depth = module.params.get('span_depth')
    pd_slots = module.params.get('pd_slots')
    raid_level = TypeHelper.convert_to_enum(module.params['raid_level'],
                                            RAIDTypesTypes)
    read_policy = TypeHelper.convert_to_enum(module.params['read_policy'],
                                             RAIDdefaultReadPolicyTypes)
    disk_policy = TypeHelper.convert_to_enum(module.params['disk_policy'],
                                             DiskCachePolicyTypes)

    # Physical Disk filter
    pd_filter = '((disk.parent.parent is Controller and disk.parent.parent.FQDD._value == "{0}")'.format(module.params['controller_fqdd'])
    pd_filter += ' or (disk.parent is Controller and disk.parent.FQDD._value == "{0}"))'.format(module.params['controller_fqdd'])
    pd_filter += ' and disk.MediaType == "{0}"'.format(module.params['media_type'])
    pd_filter += ' and disk.BusProtocol == "{0}"'.format(module.params['bus_protocol'])

    # Either one of Span Length and Physical Disks Slots must be defined
    if not (span_length or pd_slots):
        module.fail_json(msg="Either one of span_length and pd_slots must be defined for VD creation")
    elif pd_slots:
        slots = ""
        for i in pd_slots:
            slots += "\"" + str(i) + "\","
        slots_list = "[" + slots[0:-1] + "]"
        pd_filter += " and disk.Slot._value in " + slots_list
        span_length = len(pd_slots)

    # check span_length
    if span_length < MIN_SPAN_LENGTH[TypeHelper.resolve(raid_level)]:
        module.fail_json(msg="Invalid span length for RAID Level: "+ TypeHelper.resolve(raid_level))

    # Span depth must be at least 1 which is used for RAID 0, 1, 5 and 6
    span_depth = 1 if (span_depth < 1) else span_depth

    # Span depth must be at least 2 for RAID levels 10, 50 and 60
    if raid_level in [RAIDTypesTypes.RAID_10, RAIDTypesTypes.RAID_50, RAIDTypesTypes.RAID_60]:
        span_depth = 2 if (span_depth < 2) else span_depth

    msg = idrac.config_mgr.RaidHelper.new_virtual_disk(
            Name=module.params['vd_name'],
            Size=module.params['vd_size'],
            RAIDaction=RAIDactionTypes.Create,
            RAIDTypes=raid_level,
            RAIDdefaultReadPolicy=read_policy,
            RAIDdefaultWritePolicy=write_policy,
            DiskCachePolicy=disk_policy,
            SpanLength=span_length,
            SpanDepth=span_depth,
            StripeSize=module.params['stripe_size'],
            NumberDedicatedHotSpare=module.params['dedicated_hot_spare'],
            NumberGlobalHotSpare=module.params['global_hot_spare'],
            PhysicalDiskFilter=pd_filter)

    return msg

def _delete_virtual_drive(idrac, module):
    """
    Delete virtual drive

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    msg = idrac.config_mgr.RaidHelper.delete_virtual_disk(
            Name=module.params['vd_name'])

    return msg

def virtual_drive(idrac, module):
    """
    Create or delete a virtual drive

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    err = False

    try:
        # Check whether VD exists
        exists = _virtual_drive_exists(idrac, module)

        if module.params['state'] == 'present':
            if module.check_mode or exists:
                msg['changed'] = not exists
            else:
                msg['msg'] = _create_virtual_drive(idrac, module)
        else:
            if module.check_mode or not exists:
                msg['changed'] = exists
            else:
                msg['msg'] = _delete_virtual_drive(idrac, module)

        if "Status" in msg['msg']:
            if msg['msg']['Status'] == "Success":
                msg['changed'] = True
            else:
                msg['failed'] = True

    except Exception as e:
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['exception'] = traceback.format_exc()
        msg['failed'] = True

    return msg, err

# Main
def main():

    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC handle
            idrac=dict(required=False, type='dict'),

            # iDRAC Credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_pwd=dict(required=True, type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Network File Share
            share_name=dict(required=True, type='str'),
            share_user=dict(required=True, type='str'),
            share_pwd=dict(required=True, type='str', no_log=True),
            share_mnt=dict(required=True, type='path'),

            # Virtual drive parameters
            vd_name=dict(required=True, type='str'),
            vd_size=dict(required=False, default=None, type='int'),
            controller_fqdd=dict(required=True, type='str'),
            pd_slots=dict(required=False, default=[], type='list'),
            media_type=dict(required=False, choices=['HDD', 'SSD'],
                            default='HDD', type='str'),
            bus_protocol=dict(required=False, choices=['SAS', 'SATA'],
                              default='SATA', type='str'),
            raid_level=dict(required=False,
                            choices=['RAID 0', 'RAID 1', 'RAID 10', 'RAID 5',
                                     'RAID 50', 'RAID 6', 'RAID 60'],
                            default=None, type='str'),
            read_policy=dict(requird=False,
                             choices=["NoReadAhead", "ReadAhead", "AdaptiveReadAhead", "Adaptive"],
                             default="Adaptive", type='str'),
            write_policy=dict(requird=False,
                              choices=["WriteThrough", "WriteBack", "WriteBackForce"],
                              default="WriteThrough", type='str'),
            disk_policy=dict(requird=False,
                             choices=["Default", "Enabled", "Disabled"],
                             default="Default", type='str'),
            stripe_size=dict(requird=False,
                             choices=[65536, 131072, 262144, 524288, 1048576],
                             default=65536, type='int'),
            span_length=dict(required=False, type='int'),
            span_depth=dict(required=False, default=1, type='int'),
            dedicated_hot_spare=dict(required=False, default=0, type='int'),
            global_hot_spare=dict(required=False, default=0, type='int'),
            state=dict(required=False, choices=['present', 'absent'],
                       default='present')
        ),
        required_if=[
            ["state", "present", ["raid_level"]]
        ],
        mutually_exclusive=[
            ["pd_slots", "span_length"]
        ],

        supports_check_mode=True)

    if not HAS_OMSDK:
        module.fail_json(msg="Dell EMC OpenManage Python SDK required for this module")

    # Connect to iDRAC
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    # Setup network share as local mount
    if not idrac_conn.setup_nw_share_mount():
        module.fail_json(msg="Failed to setup network share local mount point")

    msg, err = virtual_drive(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()
