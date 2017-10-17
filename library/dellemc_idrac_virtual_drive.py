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
    required: False
    description:
      - iDRAC IP Address
    default: None
  idrac_user:
    required: False
    description:
      - iDRAC user name
    default: None
  idrac_pwd:
    required: False
    description:
      - iDRAC user password
    default: None
  idrac_port:
    required: False
    description:
      - iDRAC port
    default: None
  share_name:
    required: True
    description:
      - Network file share
  share_user:
    required: True
    description:
      - Network share user in the format user@domain
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
      - Size (in bytes) of the Virtual Drive
  controller_fqdd:
    required: True
    description:
      - Fully Qualified Device Descriptor (FQDD) of the storage controller
  pd_slots:
    required: False
    description:
      - List of slots for physical disk that are be used for the VD
    default: []
  raid_level:
    required: False
    description:
      - Select the RAID Level for the new virtual drives.
      - RAID Levels can be one of the following:
          RAID 0: Striping without parity
          RAID 1: Mirrorign without parity
          RAID 5: Striping with distributed parity
          RAID 50: Combines multiple RAID 5 sets with striping
          RAID 6: Striping with dual parity
          RAID 60: Combines multiple RAID 6 sets with striping
    choices: ['RAID 0', 'RAID 1', 'RAID 5', 'RAID 6', 'RAID 10', 'RAID 50', 'RAID 60']
    default: 'RAID 0'
  read_cache_policy:
    required: False
    description:
      - Read Cache polic of the virtual disk
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
  stripe_size:
    required: False
    description:
      - Stripe size of the virtual disk
    choices: ["64KB", "128KB", "256KB","512KB", "1MB"]
    default: "64KB"
  span_depth:
    required: False
    description:
      - Number of spans in the virtual disk. Required if I(status = 'present')
  span_length:
    required: False
    description:
      - Number of physical disks per span on a virtual disk. Required if I(status = 'present')
  state:
    required: False
    description:
      - if C(present), will perform create/add operations
      - if C(absent), will perform delete/remove operations
    choices: ['present', 'absent']
    default: 'present'

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
'''

EXAMPLES = '''
- name: Create Virtual Drive
    dellemc_idrac_virtual_drive:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      virtual_drive_name:  "Virtual Drive 0"
      controller_fqdd: "RAID-Integrated.1-1"
      raid_type:   "RAID 1"
      span_depth:  1
      span_length: 2
      state:       "present"

- name: Delete Virtual Drive
    dellemc_idrac_virtual_drive:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      virtual_drive_name:  "Virtual Drive 0"
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
        DiskCachePolicyTypes, RAIDTypesTypes, RAIDdefaultReadPolicyTypes,
        RAIDdefaultWritePolicyTypes, StripeSizeTypes
    )
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False

def _virtual_drive_exists(idrac, module):
    """
    check whether a virtual drive exists

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    vd = idrac.config_mgr.RaidHelper.find_virtual_disk(Name=module.params['vd_name'])

    if vd:
        return True

    return False


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
        raid_level = TypeHelper.convert_to_enum(module.params['raid_level'],
                                                RAIDTypesTypes)
        read_policy = TypeHelper.convert_to_enum(module.params['read_policy'],
                                                 RAIDdefaultReadPolicyTypes)
        write_policy = TypeHelper.convert_to_enum(module.params['write_policy'],
                                                  RAIDdefaultWritePolicyTypes)
        disk_policy = TypeHelper.convert_to_enum(module.params['disk_policy'],
                                                 DiskCachePolicyTypes)

        pd_filter = "(disk.parent.parent is Controller and disk.parent.parent.FQDD._value == \"" + module.params['controller_fqdd'] + "\")" + \
        " and disk.MediaType == \"" + module.params['media_type'] + "\"" + \
        " and disk.BusProtocol == \"" + module.params['bus_protocol'] + "\""

        if module.params['pd_slots']:
            pd_slots = ""
            for i in module.params['pd_slots']:
                pd_slots = "\"" + i + "\", "
            pd_slots_list = "[" + pd_slots[0:-1] + "]"
            pd_filter += " and disk.Slot in " + pd_slots_list

        # Check whether VD exists
        exists = _virtual_drive_exists(idrac, module)

        if module.params['state'] == 'present':
            if module.check_mode or exists:
                msg['changed'] = not exists
            else:
                msg['msg'] = idrac.config_mgr.RaidHelper.new_virtual_disk(
                    Name=module.params['vd_name'],
                    Size=module.params['vd_size'],
                    RAIDTypes=raid_level,
                    RAIDdefaultReadPolicy=read_policy,
                    RAIDdefaultWritePolicy=write_policy,
                    DiskCachePolicy=disk_policy,
                    SpanLength=module.params['span_length'],
                    SpanDepth=module.params['span_depth'],
                    StripeSize=module.params['stripe_size'],
                    NumberDedicatedHotSpare=module.params['dedicated_hot_spare'],
                    NumberGlobalHotSpare=module.params['global_hot_spare'],
                    PhysicalDiskFilter=pd_filter)

        else:
            if module.check_mode or not exists:
                msg['changed'] = exists
            else:
                msg['msg'] = idrac.config_mgr.RAIDHelper.delete_virtual_disk(
                    Name=module.params['vd_name'])

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
            span_depth=dict(required=False, type='int'),
            dedicated_hot_spare=dict(required=False, default=0, type='int'),
            global_hot_spare=dict(required=False, default=0, type='int'),
            state=dict(required=False, choices=['present', 'absent'],
                       default='present')
        ),
        required_if=[
            ["state", "present", ["raid_level", "span_length", "span_depth"]]
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
