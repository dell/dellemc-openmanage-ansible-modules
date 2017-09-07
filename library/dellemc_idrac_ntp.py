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
module: dellemc_idrac_ntp
short_description: Configure NTP settings
version_added: "2.3"
description:
    - Configure Network Time Protocol settings on iDRAC for synchronizing the
      iDRAC time using NTP instead of BIOS or host system times
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
    ntp_server1:
        required: False
        description: IP Address of the NTP Server 1
        default: None
    ntp_server2:
        required: False
        description: IP Address of the NTP Server 2
        default: None
    ntp_server3:
        required: False
        description: IP Address of the NTP Server 3
        default: None
    state:
        required: False
        description:
        - if C(present), will enable the NTP option and add the NTP servers
        - if C(absent), will disable the NTP option
        default: 'present'

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
"""

EXAMPLES = """
---
- name: Configure NTP
    dellemc_idrac_ntp:
       idrac_ip:    "192.168.1.1"
       idrac_user:  "root"
       idrac_pwd:   "calvin"
       share_name:  "\\\\100.100.100.100\\share\\"
       share_user:  "user1"
       share_pwd:   "password"
       share_mnt:   "/mnt/share"
       ntp_server1: "10.20.30.40"
       ntp_server2: "20.30.40.50"
       ntp_server3: "30.40.50.60"
       state:       "present"
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

# setup_idrac_ntp
def setup_idrac_ntp (idrac, module):

    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    err = False

    # Check first whether local mount point for network share is setup
    try:
        if idrac.config_mgr.liason_share is None:
            if not  _setup_idrac_nw_share (idrac, module):
                msg['msg'] = "Failed to setup local mount point for network share"
                msg['failed'] = True
                return msg

        # TODO: Check if NTP settings exists
        exists = False

        if module.params["state"] == "present":
            if module.check_mode or exists:
                msg['changed'] = not exists
            else:
                msg['msg'] = idrac.config_mgr.enable_ntp (
                                                 module.params["ntp_server1"],
                                                 module.params["ntp_server2"],
                                                 module.params["ntp_server3"])
        else:
            if module.check_mode or not exists:
                msg['changed'] = exists
            else:
                msg['msg'] = idrac.config_mgr.disable_ntp()

        if "Status" in msg['msg']:
            if msg['msg']["Status"] == "Success":
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
                idrac_ip   = dict (required = True, type = 'str'),
                idrac_user = dict (required = False, default = None, type = 'str'),
                idrac_pwd  = dict (required = False, default = None,
                                   type = 'str', no_log = True),
                idrac_port = dict (required = False, default = None),

                # Network File Share
                share_name = dict (required = True, default = None),
                share_user = dict (required = True, default = None),
                share_pwd  = dict (required = True, default = None),
                share_mnt  = dict (required = True, default = None),

                # NTP parameters
                ntp_server1 = dict (required = False, default = None, type = 'str'),
                ntp_server2 = dict (required = False, default = None, type = 'str'),
                ntp_server3 = dict (required = False, default = None, type = 'str'),
                state = dict (required = False,
                              choices = ['present', 'absent'],
                              default = 'present')
                ),
            supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    (msg, err) = setup_idrac_ntp (idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
