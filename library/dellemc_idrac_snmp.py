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
module: dellemc_idrac_snmp
short_description: Configure SNMP settings on iDRAC 
version_added: "2.3"
description:
    - Configures SNMP settings on iDRAC
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
        description: Local mount path of the network file share with
        read-write permission for ansible user
    snmp_agent_enable:
        description: SNMP Agent status
        choices: ['enabled', 'disabled']
        default: 'enabled'
    snmp_protocol:
        description: SNMP protocol supported
        choices: ['all', 'SNMPv3']
        default: 'all'
    snmp_agent_community:
        description: SNMP Agent community string
        default: 'public'
    snmp_discover_port:
        description: SNMP discovery port
        default: '161'
    snmp_trap_port:
        description: SNMP trap port
        default: '162'
    snmp_trap_format:
        description: SNMP trap format
        choices: ['SNMPv1', 'SNMPv2', 'SNMPv3']
        default: 'SNMPv1'
    state:
        description:
        - if C(present), will perform create/add/enable operations
        - if C(absent), will perform delete/remove/disable operations
        choices: ['present', 'absent']
        default: 'present'

requirements: ['omsdk']
author: "anupam.aloke@dell.com"

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

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

# Setup iDRAC Network Share Local Mount point
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

# iDRAC SNMP Configuration
# idrac: iDRAC handle
# module: Ansible module
#
# Supports check_mode
def setup_idrac_snmp (idrac, module):

    msg = {}
    msg['msg'] = ''
    msg['changed'] = False
    msg['failed'] = False

    # TODO : Check if the SNMP configuration parameters already exists
    exists = False

    if module.params["state"] == "present":
        if module.check_mode or exists:
            msg['changed'] = False
        else:
            msg['msg'] = idrac.config_mgr.enable_snmp(
                                         module.params['snmp_discovery_port'],
                                         module.params['snmp_trap_port'],
                                         module.params['snmp_trap_format'])
    else:
        if module.check_mode or not exists:
            msg['changed'] = False
        else:
            msg['msg'] = idrac.config_mgr.disable_snmp()

    if msg['msg']['Status'] == "Failed":
        msg['changed'] = False
        msg['failed'] = True

    return msg


def main():
    from ansible.module_utils.dellemc_idrac import iDRACConnection

    module = AnsibleModule (
            argument_spec = dict (

                # iDRAC Handle
                idrac = dict (required = False, type = 'dict'),

                # iDRAC Credentials
                idrac_ipv4 = dict (required = True, type = 'str'),
                idrac_user = dict (required = False, default = None, type = 'str'),
                idrac_pwd  = dict (required = False, default = None, type = 'str'),
                idrac_port = dict (required = False, default = None),

                # Network File Share
                share_name = dict (required = True, default = None),
                share_user = dict (required = True, default = None),
                share_pwd  = dict (required = True, default = None),
                share_mnt  = dict (required = True, default = None),

                # SNMP Configuration
                snmp_agent_enable = dict (required = False,
                                     choice = ['enabled', 'disabled'],
                                     default = 'enabled',
                                     type = 'str'),
                snmp_protocol = dict (required = False,
                                      choice = ['all', 'SNMPv3'],
                                      default = 'all',
                                      type = 'str'),
                snmp_agent_community = dict (required = False,
                                             default = 'public', type = 'str'),
                snmp_discovery_port = dict (required = False, default = '161'),
                snmp_trap_port = dict (required = False, default = '162'),
                snmp_trap_format = dict (required = False,
                                         choice = ['SNMPv1','SNMPv2','SNMPv3'],
                                         default = 'SNMPv1',
                                         type = 'str'),

                state = dict (required = False, choice = ['present','absent'])
            ),

            supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    msg = {}

    # Configure SNMP 
    try:
        if _setup_idrac_nw_share (idrac, module):
            msg = setup_idrac_snmp (idrac, module)
        else:
            msg['failed'] = True
            msg['changed'] = False
            msg['msg'] = "No local mount point setup for the Network File Share"
    except Exception as e:
        msg['msg'] = "setup error: %s" % str(e)
        msg['changed'] = False
        msg['failed'] = True

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    module.exit_json(**msg)

if __name__ == '__main__':
    main()
