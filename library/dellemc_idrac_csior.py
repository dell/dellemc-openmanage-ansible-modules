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
module: dellemc_idrac_csior
short_description: Enable or disble Collect System Inventory on Restart (CSIOR)
version_added: "2.3"
description:
    - Enable or Disable Collect System Inventory on Restart (CSIOR)
options:
    idrac_ip:
        required: True
        description: iDRAC IPv4 Address
    idrac_user:
        description: iDRAC user name
        default: root
    idrac_pwd:
        description: iDRAC user password
    idrac_port:
        description: iDRAC port
    share_name:
        required: True
    share_user:
        required: True
        description: Network share user in the format user@domain
    share_pwd:
        required: True
        description: Network share user password
    share_mnt:
        required: True
        description: Local mount path of the network file share with
        read-write permission for ansible user 
    state:
        required: False
        description:
        - if C(present), will enable the CSIOR
        - if C(absent), will disable the CSIOR

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
"""

from ansible.module_utils.basic import AnsibleModule

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

# Setup iDRAC Network File Share
# idrac: iDRAC handle
# module: Ansible module
#
def _setup_idrac_nw_share (idrac, module):
    from omsdk.sdkfile import FileOnShare
    from omsdk.sdkcreds import UserCredentials

    myshare = FileOnShare(module.params['share_name'],
                          module.params['share_mnt'],
                          isFolder=True)

    myshare.addcreds(UserCredentials(module.params['share_user'],
                                     module.params['share_pwd']))

    return idrac.config_mgr.set_liason_share(myshare)


# setup_idrac_csior
def setup_idrac_csior (idrac, module):

    msg = {}
    msg['msg'] = ''
    msg['changed'] = False
    msg['failed'] = False

    # Check first whether local mount point for network share is setup
    if idrac.config_mgr.liason_share is None:
        if not  _setup_idrac_nw_share (idrac, module):
            msg['msg'] = "Failed to setup local mount point for network share"
            msg['failed'] = True
            return msg

    if module.params["state"] == "present":
        if module.check_mode:
            msg['changed'] = False
        else:
            msg['msg'] = idrac.config_mgr.enable_csior()
    else:
        if module.check_mode:
            msg['changed'] = False
        else:
            msg ['msg'] = idrac.config_mgr.disable_csior()

    if msg['msg']['Status'] == "Failed":
        msg['changed'] = False
        msg['failed'] = True

    return msg

# Main
def main():
    from ansible.module_utils.dellemc_idrac import iDRACConnection

    module = AnsibleModule (
            argument_spec = dict (

                # iDRAC handle
                idrac = dict (required = False, type = 'dict'),

                # iDRAC Credentials
                idrac_ip   = dict (required = True, type = 'str'),
                idrac_user = dict (required = False, default = 'root', type = 'str'),
                idrac_pwd  = dict (required = False, default = None, type = 'str'),
                idrac_port = dict (required = False, default = None),

                # Network File Share
                share_name = dict (required = True, default = None),
                share_user = dict (required = True, default = None),
                share_pwd  = dict (required = True, default = None),
                share_mnt  = dict (required = True, default = None),

                state = dict (required = False, choices = ['enable', 'disable'])
                ),
            supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    msg = setup_idrac_csior (idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    module.exit_json(**msg)

if __name__ == '__main__':
    main()
