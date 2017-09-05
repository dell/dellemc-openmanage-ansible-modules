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
module: dellemc_idrac_syslog
short_description: Configure remote system logging
version_added: "2.3"
description:
    - Configure remote system logging settings to remotely write RAC log and
      System Event Log (SEL) to an external server
options:
    idrac_ip:
        required: False
        description: iDRAC IPv4 Address
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
    server1_syslog:
        required: False
        description: IP Address of the Remote Syslog Server 1
        default: None
    server2_syslog:
        required: False
        description: IP Address of the Remote Syslog Server 2
        default: None
    server3_syslog:
        required: False
        description: IP Address of the Remote Syslog Server 3
        default: None
    port_syslog:
        required: False
        description: Port number of remote server
        default: '514'
    state:
        description:
        - if C(present), will enable the remote syslog option and add the
          remote servers
        - if C(absent), will disable the remote syslog option

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

# setup_idrac_syslog
def setup_idrac_syslog (idrac, module):

    msg = {}
    msg['changed'] = False
    msg['failed'] = False

    try:
        # Check first whether local mount point for network share is setup
        if idrac.config_mgr.liason_share is None:
            if not  _setup_idrac_nw_share (idrac, module):
                msg['msg'] = "Failed to setup local mount point for network share"
                msg['failed'] = True
                return msg

        # TODO: Check if Syslog settings exists
        exists = False

        if module.params["state"] == "present":
            if module.check_mode or exists:
                msg['changed'] = not exists
            else:
                msg['msg'] = idrac.config_mgr.enable_syslog (
                                             module.params["port_syslog"],
                                             0,
                                             module.params["server1_syslog"],
                                             module.params["server2_syslog"],
                                             module.params["server3_syslog"])
        else:
            if module.check_mode or not exists:
                msg['changed'] = exists
            else:
                msg['msg'] = idrac.config_mgr.disable_syslog()

        if "Status" in msg['msg'] and msg['msg']["Status"] is "Success":
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
                share_name = dict (required = True, default = None),
                share_user = dict (required = True, default = None),
                share_pwd  = dict (required = True, default = None),
                share_mnt  = dict (required = True, default = None),

                # Remote Syslog parameters
                server1_syslog = dict (required = False, default = None, type = 'str'),
                server2_syslog = dict (required = False, default = None, type = 'str'),
                server3_syslog = dict (required = False, default = None, type = 'str'),
                port_syslog = dict (required = False, default = 514, type = 'int'),
                state = dict (required = False,
                              choices = ['present', 'absent'],
                              default = 'present')
                ),
            supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    (msg, err) = setup_idrac_syslog (idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
