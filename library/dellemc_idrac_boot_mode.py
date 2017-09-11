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

DOCUMENTATION = """
---
module: dellemc_idrac_boot_mode
short_description: Configure Boot Mode
version_added: "2.3"
description:
    - Configure Boot Mode
options:
    idrac_ip:
        required: False
        description: iDRAC IP Address
        default: None
    idrac_user:
        required: False
        description: iDRAC user name
        default: None
    idrac_pwd:
        required: False
        description: iDRAC user password
        default: None
    idrac_port:
        required: False
        description: iDRAC port
        default: None
    share_name:
        required: True
        description: Network file share
    share_user:
        required: True
        description: Network share user in the format user@domain
    share_pwd:
        required: True
        description: Network share user password
    share_mnt:
        required: True
        description: Local mount path of the network file share specified
        in I(share_name) with read-write permission for ansible user
    boot_mode:
        required: False
        choices: ['Bios', 'Uefi']
        description:
        - if C(Bios), will set the boot mode to BIOS
        - if C(Uefi), will set the boot mode to UEFI
        default: 'Bios'

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
"""

EXAMPLES = """
---
- name: Configure Boot Mode
    dellemc_idrac_csior:
       idrac_ip:   "192.168.1.1"
       idrac_user: "root"
       idrac_pwd:  "calvin"
       share_name: "\\\\10.20.30.40\\share\\"
       share_user: "user1"
       share_pwd:  "password"
       share_mnt:  "/mnt/share"
       boot_mode:  "Uefi"
"""

RETURNS = """
---
"""

from ansible.module_utils.basic import AnsibleModule

def _setup_idrac_nw_share (idrac, module):
    """
    Setup local mount point for Network file share

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    from omsdk.sdkfile import FileOnShare
    from omsdk.sdkcreds import UserCredentials

    myshare = FileOnShare(module.params['share_name'],
                          module.params['share_mnt'],
                          isFolder=True)

    myshare.addcreds(UserCredentials(module.params['share_user'],
                                     module.params['share_pwd']))

    return idrac.config_mgr.set_liason_share(myshare)

def setup_boot_mode (idrac, module):
    """
    Setup Boot Mode on PowerEdge Servers

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    from omdrivers.lifecycle.iDRAC.iDRACConfig import BootModeEnum
    
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

        exists = False

        if module.params['boot_mode'] == 'Bios':
            if idrac.config_mgr.BootMode == BootModeEnum.Bios:
                exists = True

            if module.check_mode or exists:
                msg['changed'] = not exists
            else:
                msg['msg'] = idrac.config_mgr.change_boot_mode('Bios')

        elif module.params['boot_mode'] == 'Uefi':
            if idrac.config_mgr.BootMode == BootModeEnum.Uefi:
                exists = True

            if module.check_mode or exists:
                msg['changed'] = not exists
            else:
                msg['msg'] = idrac.config_mgr.change_boot_mode('Uefi')

        if "Status" in msg['msg']:
            if msg['msg']['Status'] is "Success":
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

    from ansible.module_utils.dellemc_idrac import iDRACConnection

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

                boot_mode  = dict (required = False,
                                    choices = ['Bios', 'Uefi'],
                                    default = 'Bios')
                ),
            supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    msg, err = setup_boot_mode (idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()
