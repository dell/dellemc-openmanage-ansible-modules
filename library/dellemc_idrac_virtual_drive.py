#! /usr/bin/python
# _*_ coding: utf-8 _*_

#
# Copyright (c) 2017 Dell Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

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
  virtual_drive_name:
    required: True
    description:
      - Name of the Virtual Drive
    default: None
  raid_type:
    required: False
    description:
      - RAID type
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
      - Number of physical disks per span on a virtual disk. Required if I(status = 'absent')
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
      share_name: "\\10.20.30.40\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      virtual_drive_name:  "Virtual Drive 0"
      raid_type:   "RAID_1"
      span_depth:  1
      span_length: 2
      state:       "present"

- name: Delete Virtual Drive
    dellemc_idrac_boot_to_nw_iso:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\10.20.30.40\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      virtual_drive_name:  "Virtual Drive 0"
      state:       "absent"
'''

RETURN = '''
'''

from ansible.module_utils.dellemc_idrac import *
from ansible.module_utils.basic import AnsibleModule

def _setup_idrac_nw_share (idrac, module):
    """
    Setup local mount point for Network file share

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    myshare = FileOnShare(module.params['share_name'],
                          module.params['share_mnt'],
                          isFolder=True)

    myshare.addcreds(UserCredentials(module.params['share_user'],
                                     module.params['share_pwd']))

    return idrac.config_mgr.set_liason_share(myshare)

def _virtual_drive_exists (idrac, module):
    """
    check whether a virtual drive exists

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    vd = idrac.config_mgr.get_virtual_disk(
                        module.params['virtual_drive_name'])

    if vd:
        return True, vd

    return False, None


def virtual_drive (idrac, module):
    """
    Create or delete a virtual drive

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    from omsdk.sdkcenum import TypeHelper
    from omdrivers.enums.iDRAC.iDRACEnums import RAIDLevelsEnum
    
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    err = False

    try:
        # Check first whether local mount point for network share is setup
        if idrac.config_mgr.liason_share is None:
            if not  _setup_idrac_nw_share (idrac, module):
                msg['msg'] = "Failed to setup local mount point for network share"
                msg['failed'] = True
                return msg

        # Check whether VD exists
        exists, vd = _virtual_drive_exists(idrac, module)

        if module.params['state'] == 'present':
            if module.check_mode or exists:
                msg['changed'] = not exists
                
            else:
                raid_type = TypeHelper.convert_to_enum(module.params['raid_type'],
                                                       RAIDLevelsEnum)

                msg['msg'] = idrac.config_mgr.create_virtual_disk(
                                            module.params['virtual_drive_name'],
                                            module.params['span_depth'],
                                            module.params['span_length'],
                                            raid_type) 

        else:
            if module.check_mode or not exists:
                msg['changed'] = exists
            else:
                msg['msg'] = idrac.config_mgr.delete_virtual_disk(
                                            module.params['virtual_drive_name'])

        if "Status" in msg['msg']:
            if msg['msg']['Status'] == "Success":
                msg['changed'] = True
            else:
                msg['failed'] = True

    except Exception as e:
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True

    return msg, err

# Main
def main():

    module = AnsibleModule (
            argument_spec = dict (

                # iDRAC handle
                idrac = dict (required = False, type = 'dict'),

                # iDRAC Credentials
                idrac_ip   = dict (required = False, default = None, type = 'str'),
                idrac_user = dict (required = False, default = None, type = 'str'),
                idrac_pwd  = dict (required = False, default = None,
                                    type = 'str', no_log = True),
                idrac_port = dict (required = False, default = None, type = 'int'),

                # Network File Share
                share_name = dict (required = True, type = 'str'),
                share_user = dict (required = True, type = 'str'),
                share_pwd  = dict (required = True, type = 'str', no_log = True),
                share_mnt  = dict (required = True, type = 'str'),

                # Virtual drive parameters
                virtual_drive_name  = dict (required = True, type = 'str'),
                raid_type = dict (required = False,
                                  choices = ['RAID 0', 'RAID 1', 'RAID 5', 'RAID 6',
                                             'RAID 10', 'RAID 50','RAID 60'],
                                  default = 'RAID 0',
                                  type = 'str'),
                read_cache_policy = dict (requird = False,
                                          choices = ["NoReadAhead", "ReadAhead", "Adaptive"],
                                          default = "NoReadAhead",
                                          type = 'str'),
                write_cache_policy = dict (requird = False,
                                          choices = ["WriteThrough", "WriteBack", "WriteBackForce"],
                                          default = "WriteThrough",
                                          type = 'str'),
                disk_cache_policy = dict (requird = False,
                                          choices = ["Default", "Enabled", "Disabled"],
                                          default = "Default",
                                          type = 'str'),
                stripe_size = dict (requird = False,
                                    choices = ["64KB", "128KB", "256KB","512KB", "1MB"],
                                    default = "64KB",
                                    type = 'str'),
                span_length = dict (required = True, type = 'int'),
                span_depth = dict (required = True, type = 'int'),
                state = dict (required = False, 
                              choices = ['present', 'absent'],
                              default = 'present')
                ),

            supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    msg, err = virtual_drive (idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()
