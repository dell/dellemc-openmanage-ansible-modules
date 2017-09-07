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
        - if C(present), will create/add/modify an user
        - if C(absent), will delete the user
        - if C(enable), will enable the user
        - if C(disable), will disable the user
        choices: ['present', 'absent', 'enable','disable']
        default: 'present'

requirements: ['omsdk']
author: anupam.aloke@dell.com
"""

EXAMPLES = """
---
- name: Setup iDRAC Users
    dellemc_idrac_user:
       idrac_ip:   "192.168.1.1"
       idrac_user: "root"
       idrac_pwd:  "calvin"
       share_name: "\\\\10.20.30.40\\share\\"
       share_user: "user1"
       share_pwd:  "password"
       share_mnt:  "/mnt/share"
       user_name:  "admin"
       user_pwd:   "password"
       user_priv:  "Administrator"
       state:      "present"
"""

RETURNS = """
---
"""

from ansible.module_utils.basic import AnsibleModule

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
    msg['msg'] = {}
    err = False

    user_name = module.params['user_name']
    user_pwd = module.params['user_pwd']
    user_priv = idrac.user_mgr.eUserPrivilegeEnum.NoPrivilege

    if module.params['user_priv'] == "Administrator":
        user_priv = idrac.user_mgr.eUserPrivilegeEnum.Administrator
    elif module.params['user_priv'] == "Operator":
        user_priv = idrac.user_mgr.eUserPrivilegeEnum.Operator
    elif module.params['user_priv'] == "ReadOnly":
        user_priv = idrac.user_mgr.eUserPrivilegeEnum.ReadOnly

    try:
        # Check first whether local mount point for network share is setup
        if idrac.config_mgr.liason_share is None:
            if not  _setup_idrac_nw_share (idrac, module):
                msg['msg'] = "Failed to setup local mount point for network share"
                msg['failed'] = True
                return msg

        # Check if user exists
        if user_name is not None:
            exists, enabled = False, False
            user_priv_change, user_pwd_change = False, False

            user = idrac.user_mgr.get_user(user_name.lower())

            if user is not None:
                exists = True

                if user['Enable'] == 'Enabled':
                    enabled = True

                if user['Privilege'] != user_priv:
                    user_priv_change = True

                if user_pwd is not None:
                    user_pwd_change = True

        if module.params["state"] == "present":
            if module.check_mode:
                if exists:
                    msg['changed'] = user_priv_change or user_pwd_change
            else:
                if not exists:
                    msg['msg'] = idrac.user_mgr.create_user(
                                                user_name, user_pwd, user_priv)
                elif user_priv_change:
                    msg['msg'] = idrac.user_mgr.change_privilege(
                                                user_name, user_priv)
                elif user_pwd_change:
                    msg['msg'] = idrac.user_mgr.change_password(
                                                user_name, "", user_pwd)

        elif module.params["state"] == "enable":
            if module.check_mode:
                if exists:
                    msg['changed'] = not enabled
            else:
                if exists and not enabled:
                    msg['msg'] = idrac.user_mgr.enable_user(user_name)
                elif not exists:
                    msg['msg'] = "User: " + user_name + " does not exist"

        elif module.params["state"] == "disable":
            if module.check_mode:
                if exists:
                    msg['changed'] = enabled
            else:
                if exists and enabled:
                    msg['msg'] = idrac.user_mgr.disable_user(user_name)
                elif not exists:
                    msg['msg'] = "User: " + user_name + " does not exist"

        elif module.params["state"] == "absent":
            if module.check_mode or not exists:
                msg['changed'] = exists
            else:
                msg['msg'] = idrac.user_mgr.delete_user(user_name)

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
                state = dict (required = False,
                              choices = ['present', 'absent', 'enable', 'disable'],
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
