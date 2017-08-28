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
module: dellemc_idrac_snmp_alert
short_description: Configure SNMP Alert destination settings on iDRAC
version_added: "2.3"
description:
    - Configures SNMP Alert destination settings on iDRAC
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
    snmp_alert_dest:
        required: True
        description: SNMP Alert destination
    snmp_alert_state:
        required: False
        description: State of the SNMP Alert Destination
        choices: ['enabled', 'disabled']
    snmpv3_user:
        required: False
        description: SNMPv3 user name for the SNMP alert destination
    state:
        description:
        - if C(present), will perform create/add/enable operations
        - if C(absent), will perform delete/remove/disable operations
        choices: ['present', 'absent']
        default: 'present'

requirements: ['omsdk']
author: "anupam.aloke@dell.com"

"""

import sys
import os
import json
sys.path.append("/home/anupam/workspace/ansible_idrac_py2.7/omsdk")
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


# Check if SNMP Alert destination exists
def _snmp_alert_destination_exists (idrac, module):

    exists = False
    enabled = False

    for item in idrac.config_mgr.SNMPTrapDestination:
        if item["Destination"] == module.params["snmp_alert_dest"]:
            exists = True
            if item["State"] == "Enabled":
                enabled = True
            break

    return exists, enabled

# setup_idrac_snmp_alert
def setup_idrac_snmp_alert (idrac, module):

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

    # TODO: Check if the SNMP Trap configuration parameters already exists
    (exists, enabled) = _snmp_alert_destination_exists (idrac, module)

    if module.params["state"] = "present":
        if module.check_mode or exists:
            msg['changed'] = False
        elif not exists:
            msg['msg'] = idrac.config_mgr.add_trap_destination(
                                        module.params['snmp_alert_dest'],
                                        module.params['snmpv3_user'])
        elif not enabled:
            msg['msg'] = idrac.config_mgr.enable_trap_destination(
                                        module.params['snmp_alert_dest'])
    else:
        if module.check_mode or not exists:
            msg['changed'] = False
        else:
            msg['msg'] = idrac.config_mgr.remove_trap_destination(
                                        module.params['snmp_alert_dest'])

    if msg['msg']['Status'] = "Failed":
        msg['changed'] = False
        msg['failed'] = True

    return msg

# Main
def main():
    from ansible.module_utils.dellemc_idrac import iDRACConnection

    module = AnsibleModule (
            argument_spec = dict (

                # iDRAC Handle
                idrac = dict (required = False, type = 'dict'),

                # iDRAC Credentials
                idrac_ipv4 = dict (required = True, type = 'str'),
                idrac_user = dict (required = False, default = 'root', type = 'str'),
                idrac_pwd  = dict (required = False, default = None, type = 'str'),
                idrac_port = dict (required = False, default = None),

                # Network File Share
                share_name = dict (required = True, default = None),
                share_user = dict (required = True, default = None),
                share_pwd  = dict (required = True, default = None),
                share_mnt  = dict (required = True, default = None),

                # SNMP Alert Configuration Options
                snmp_alert_dest = dict (required = False, default = None),
                snmp_alert_state = dict (required = False,
                                         choice = ['enabled', 'disabled'],
                                         default = None),
                snmpv3_user = dict (required = False, default = None),
                state = dict (required = False, choice = ['present', 'absent'])
                ),

            supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    msg = setup_idrac_snmp_alert(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    module.exit_json(**msg)

if __name__ == '__main__':
    main()
