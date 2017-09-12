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
        description: Network share user in the format "user@domain"
    share_pwd:
        required: True
        description: Network share user password
    share_mnt:
        required: True
        description: Local mount path of the network file share with
        read-write permission for ansible user
    snmp_alert_dest:
        required: True
        description: SNMP Alert destination IPv4 address
    snmpv3_user_name:
        required: False
        description: SNMPv3 user name for the SNMP alert destination
        default: None
    state:
        description:
        - if C(present), will create/add a SNMP alert destination
        - if C(absent), will delete/remove a SNMP alert destination
        - if C(enable), will enable a SNMP alert destination
        - if C(disable), will disable a SNMP alert destination
        choices: ['present', 'absent', 'enable', 'disable']
        default: 'present'

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
"""

EXAMPLES = """
---
- name: Configure SNMP Alert Destination
    dellemc_idrac_snmp_alert:
       idrac_ip:        "192.168.1.1"
       idrac_user:      "root"
       idrac_pwd:       "calvin"
       share_name:      "\\\\10.20.30.40\\share\\"
       share_user:      "user1"
       share_pwd:       "password"
       share_mnt:       "/mnt/share"
       snmp_alert_dest: "192.168.2.1"
       state:           "present"

"""

RETURNS = """
---
"""

from ansible.module_utils.dellemc_idrac import *
from ansible.module_utils.basic import AnsibleModule

def _setup_idrac_nw_share (idrac, module):
    """
    Setup local mount point for network file share

    idrac -- iDRAC handle
    module -- Ansible module
    """

    myshare = FileOnShare(module.params['share_name'],
                          module.params['share_mnt'],
                          isFolder=True)

    myshare.addcreds(UserCredentials(module.params['share_user'],
                                     module.params['share_pwd']))

    return idrac.config_mgr.set_liason_share(myshare)

def _snmp_alert_destination_exists (idrac, snmp_alert_dest):
    """
    Check if SNMP Alert destination IPv address already exists

    Keyword arguments:
    idrac           -- iDRAC handle
    snmp_alert_dest -- SNMP Alert destination IP address
    """

    if idrac.config_mgr.SNMPTrapDestination is not None:
        for item in idrac.config_mgr.SNMPTrapDestination:
            if item['Destination'] == snmp_alert_dest:
                return True, item

    return False, None

def setup_idrac_snmp_alert (idrac, module):
    """
    Setup iDRAC SNMP Alert Destinations

    idrac  -- iDRAC handle
    module -- Ansible module
    """

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

        # Check if the SNMP Trap configuration parameters already exists
        dest = {}
        exists, enabled, snmpv3_user_change = False, False, False

        if module.params['snmp_alert_dest'] is not None:
            exists, dest = _snmp_alert_destination_exists (
                                idrac, module.params['snmp_alert_dest'])

            if exists:
                if dest['State'] == 'Enabled':
                    enabled = True
                if dest['SNMPv3Username'] != module.params['snmpv3_user_name']:
                    snmpv3_user_change = True

        if module.params['state'] == 'present':
            if module.check_mode:
                if exists:
                    msg['changed'] = not enabled | snmpv3_user_change
                else:
                    msg['changed'] = not exists
            else:
                if exists and not enabled:
                    msg['msg'] = idrac.config_mgr.enable_trap_destination(
                                    module.params['snmp_alert_dest'])

                elif not exists:
                    msg['msg'] = idrac.config_mgr.add_trap_destination(
                                    module.params['snmp_alert_dest'],
                                    module.params['snmpv3_user_name'])

        elif module.params['state'] == 'enable':
            if module.check_mode or enabled:
                msg['changed'] = not enabled
            else:
                if exists and not enabled:
                    msg['msg'] = idrac.config_mgr.enable_trap_destination(
                                    module.params['snmp_alert_dest'])
                elif not exists:
                    msg['msg'] = "SNMP Alert Dest: " + \
                                  module.params['snmp_alert_dest'] + \
                                  " does not exist"

        elif module.params['state'] == 'disable':
            if module.check_mode:
                if exists:
                    msg['changed'] = enabled
            else:
                if exists and enabled:
                    msg['msg'] = idrac.config_mgr.disable_trap_destination(
                                    module.params['snmp_alert_dest'])
                elif not exists:
                    msg['msg'] = "SNMP Alert Dest: " + \
                                 module.params['snmp_alert_dest'] + \
                                 " does not exist"

        elif module.params['state'] == 'absent':
            if module.check_mode or not exists:
                msg['changed'] = exists
            else:
                msg['msg'] = idrac.config_mgr.remove_trap_destination(
                                module.params['snmp_alert_dest'])

        if 'Status' in msg['msg']:
            if msg['msg']['Status'] == 'Success':
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

                # iDRAC Handle
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

                # SNMP Alert Configuration Options
                snmp_alert_dest = dict (required = True, type = 'str'),
                snmpv3_user_name = dict (required = False, default = None,
                                        type = 'str'),
                state = dict (required = False,
                            choice = ['present', 'absent', 'enable', 'disable'],
                            default = 'present')
                ),

            supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    msg, err = setup_idrac_snmp_alert(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()
