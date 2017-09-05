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
    idrac_ip:
        required: False
        description: iDRAC IP Address
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

# Setup iDRAC Users
# idrac: iDRAC handle
# module: Ansible module
#
# supports check_mode
def setup_idrac_user (idrac, module):

    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    err = False

    if module.params['user_priv'] == "Administrator":
        user_priv = idrac.user_mgr.eUserPrivilegeEnum.Administrator
    elif module.params['user_priv'] == "Operator":
        user_priv = idrac.user_mgr.eUserPrivilegeEnum.Operator
    elif module.params['user_priv'] == "ReadOnly":
        user_priv = idrac.user_mgr.eUserPrivilegeEnum.ReadOnly
    else:
        user_priv = idrac.user_mgr.eUserPrivilegeEnum.NoPrivilege

    try:
        # Check first whether local mount point for network share is setup
        if idrac.config_mgr.liason_share is None:
            if not  _setup_idrac_nw_share (idrac, module):
                msg['msg'] = "Failed to setup local mount point for network share"
                msg['failed'] = True
                return msg

        # TODO: Check if username, pwd, and privilege parameters exists
        exists = False

        if module.params["state"] == "present":
            if module.check_mode or exists:
                msg['changed'] = not exists
            else:
                if module.params['user_name'] is not None:
                    msg['msg'] = idrac.user_mgr.create_user(
                                                module.params['user_name'],
                                                module.params['user_pwd'],
                                                user_priv)
        else:
            if module.check_mode or not exists:
                msg['changed'] = exists
            else:
                msg['msg'] = idrac.user_mgr.delete_user(module.params['user_name'])

        if "Status" in msg['msg']:
            if msg['msg']['Status'] is "Success":
                msg['changed'] = True
            else:
                msg['failed'] = True

        # Add the user list to the return msg as well
        msg['users'] = idrac.user_mgr.Users

    except Exception as e:
        err = False
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True

    return msg, err

# Main
def main():

    from ansible.module_utils.dellemc_idrac import iDRACConnection

    module = AnsibleModule (
            argument_spec = dict (
                # iDRAC handle
                idrac      = dict(required=False, type='dict'),

                # iDRAC credentials
                idrac_ip   = dict (required = False, default = None, type='str'),
                idrac_user = dict (required = False, default = None, type='str'),
                idrac_pwd  = dict (required = False, default = None,
                                   type='str', no_log = True),
                idrac_port = dict (required = False, default = None, type = 'int'),

                # Network File Share
                share_name = dict (required = True, default = None),
                share_user = dict (required = True, default = None),
                share_pwd  = dict (required = True, default = None),
                share_mnt  = dict (required = True, default = None),

                # Local user credentials
                user_name  = dict (required = False, default = None, type='str'),
                user_pwd   = dict (required = False, default = None,
                                   type='str', no_log = True),
                user_priv  = dict (required = False,
                                   choices = ['Administrator',
                                              'Operator',
                                              'ReadOnly'],
                                   default = 'ReadOnly'),

                # State
                state      = dict (required = False,
                                   choices = ['present', 'absent'],
                                   default = 'present')
                ),

            supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    # Setup User
    msg, err = setup_idrac_user (idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
