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
module: dellemc_idrac_user
short_description: Configures an iDRAC User
version_added: "2.3"
description:
    - Configures an iDRAC user
options:
    idrac_ipv4:
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
        description: CIFS or NFS Network share 
    share_user:
        required: True
        description: Network share user in the format user@domain
    share_pwd:
        required: True
        description: Network share user password
    share_mnt:
        required: True
        description:
        - Local mount path of the network file share with read-write
          permission for ansible user
    user_name:
        required: True
        description: User name to be configured
    user_pwd:
        required: True
        description: User password
    user_priv:
        description: User privileges
        choices: ['Administrator', 'Operator', 'ReadOnly']
        default: 'ReadOnly'
    state:
        description:
        - if C(present), will perform create/add/enable operations
        - if C(absent), will perform delete/remove/disable operations
        choices: ['present', 'absent']
        default: 'present'

requirements: ['omsdk']
author: anupam.aloke@dell.com
"""

EXAMPLES = """
---
"""

RETURNS = """
---
"""

import sys
import os
import json
from ansible.module_utils.basic import AnsibleModule

# Get iDRAC Users
def getiDRACUsers (idrac):

    return idrac.user_mgr.Users


# Setup iDRAC Users
# idrac: iDRAC handle
# module: Ansible module
#
# supports check_mode
def setupiDRACUser (idrac, module):

    msg = {}
    msg['msg'] = ''
    msg['changed'] = False
    msg['failed'] = False

    if module.params['user_priv'] == "Administrator":
        user_priv = idrac.user_mgr.eUserPrivilegeEnum.Administrator
    elif module.params['user_priv'] == "Operator":
        user_priv = idrac.user_mgr.eUserPrivilegeEnum.Operator
    elif module.params['user_priv'] == "ReadOnly":
        user_priv = idrac.user_mgr.eUserPrivilegeEnum.ReadOnly
    else:
        user_priv = idrac.user_mgr.eUserPrivilegeEnum.NoPrivilege

    # TODO: Check if username, pwd, and privilege parameters exists
    exists = False

    if module.params["state"] == "present":
        if module.check_mode or exists:
            msg['changed'] = False
            msg['failed'] = False
        elif module.params['user_name'] is not None:
            msg['msg'] = idrac.user_mgr.create_user(
                                            module.params['user_name'],
                                            module.params['user_pwd'],
                                            user_priv)
    else:
        if module.check_mode or not exists:
            msg['changed'] = False
            msg['Failed'] = False

        else:
            msg['msg'] = idrac.user_mgr.delete_user(module.params['user_name'])

    msg['Users'] = getiDRACUsers(idrac)

    return msg


# Main
def main():

    from ansible.module_utils.dellemc_idrac import iDRACConnection

    module = AnsibleModule (
                 argument_spec = dict (
                     # iDRAC handle
                     idrac      = dict(required=False, type='dict'),

                     # iDRAC credentials
                     idrac_ipv4 = dict(required=True,  type='str'),
                     idrac_user = dict(required=False, default='root', type='str'),
                     idrac_pwd  = dict(required=False, type='str'),
                     idrac_port = dict(required=False, default=None),

                     # Network File Share
                     share_name = dict (required = True, default = None),
                     share_user = dict (required = True, default = None),
                     share_pwd  = dict (required = True, default = None),
                     share_mnt  = dict (required = True, default = None),

                     # Local user credentials
                     user_name  = dict(required=False, default=None, type='str'),
                     user_pwd   = dict(required=False, default=None, type='str'),
                     user_priv  = dict(required=False,
                                       choices=['Administrator',
                                                'Operator',
                                                'ReadOnly'],
                                       default='ReadOnly'),

                     # State
                     state      = dict(required=False,
                                       choices=['present', 'absent'],
                                       default="absent")
                 ),

                 supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    # Setup User
    msg = setupiDRACUser(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    module.exit_json(**msg)


if __name__ == '__main__':
    main()
