#! /usr/bin/python
# _*_ coding: utf-8 _*_

#
# Dell EMC OpenManage Ansible Modules
#
# Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved.
# Dell, EMC, and other trademarks are trademarks of Dell Inc. or its
# subsidiaries. Other trademarks may be trademarks of their respective owners.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: dellemc_idrac_snmp_alert
short_description: Configure SNMP Alert destination settings on iDRAC
version_added: "2.3"
description:
    - Configures SNMP Alert destination settings on iDRAC
options:
  idrac_ip:
    required: True
    description:
      - iDRAC IP Address
    type: 'str'
  idrac_user:
    required: True
    description:
      - iDRAC user name
    type: 'str'
  idrac_pwd:
    required: True
    description:
      - iDRAC user password
    type: 'str'
  idrac_port:
    required: False
    description:
      - iDRAC port
    default: 443
    type: 'int'
  share_name:
    required: True
    description:
      - Network file share (either CIFS or NFS)
    type: 'str'
  share_user:
    required: True
    description:
      - Network share user in the format "user@domain" if user is part of a domain else 'user'
    type: 'str'
  share_pwd:
    required: True
    description:
      - Network share user password
    type: 'str'
  share_mnt:
    required: True
    description:
      - Local mount path of the network file share with read-write permission for ansible user
    type:'path'
  snmp_alert_dest:
    required: True
    description:
      - List of hashes of SNMP Alert destination
    type: 'list'
  state:
    description:
      - if C(present), will create/add/enable SNMP alert destination
      - if C(absent), will delete/remove a SNMP alert destination
    choices: ['present', 'absent']
    default: 'present'

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
'''

EXAMPLES = '''
- name: Configure SNMP Alert Destination
    dellemc_idrac_snmp_alert:
      idrac_ip:        "192.168.1.1"
      idrac_user:      "root"
      idrac_pwd:       "calvin"
      share_name:      "\\\\192.168.10.10\\share\\"
      share_user:      "user1"
      share_pwd:       "password"
      share_mnt:       "/mnt/share"
      snmp_alert_dest:
        - {"dest_address": "192.168.2.1", "state":"Enabled"}
        - {"dest_address": "192.168.2.2", "state":"Enabled"}
      state:           "present"

'''

RETURN = '''
'''

import traceback
from ansible.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
try:
    from omsdk.sdkcenum import TypeHelper
    from omdrivers.enums.iDRAC.iDRAC import State_SNMPAlertTypes
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False


def setup_idrac_snmp_alert(idrac, module):
    """
    Setup iDRAC SNMP Alert Destinations

    idrac  -- iDRAC handle
    module -- Ansible module
    """

    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    error = False

    try:
        if not module.params['snmp_alert_dest']:
            module.fail_json(msg="At least one SNMP alert destination must be provided")

        for alert_dest in module.params['snmp_alert_dest']:
            if not isinstance(alert_dest, dict):
                # reject any changes that are already done
                idrac.config_mgr._sysconfig.reject()
                module.fail_json(msg="Invalid SNMP Alert, should be of type \
                                 dict: " + str(alert_dest))

            dest_address = alert_dest.get('dest_address')

            state = alert_dest.get('state')
            if state and state.lower() == 'enabled':
                state = TypeHelper.convert_to_enum('Enabled',
                                                   State_SNMPAlertTypes)
            else:
                state = TypeHelper.convert_to_enum('Disabled',
                                                   State_SNMPAlertTypes)
            snmpv3_user_name = alert_dest.get('snmpv3_user_name')

            if dest_address:
                # check if the destination already exists
                alert = idrac.config_mgr._sysconfig.iDRAC.SNMPAlert.find_first(
                    Destination_SNMPAlert=dest_address)

                if module.params['state'] == 'present':
                    if not alert:
                        idrac.config_mgr._sysconfig.iDRAC.SNMPAlert.new(
                            Destination_SNMPAlert=dest_address,
                            State_SNMPAlert=state,
                            SNMPv3Username_SNMPAlert=snmpv3_user_name)
                    else:
                        if state:
                            alert.State_SNMPAlert = state

                        if snmpv3_user_name:
                            alert.SNMPv3Username_SNMPAlert = snmpv3_user_name
                else:
                    if alert:
                        idrac.config_mgr._sysconfig.iDRAC.SNMPAlert.remove(
                            Destination_SNMPAlert=dest_address)
                    else:
                        # Reject all changes
                        idrac.config_mgr._sysconfig.reject()
                        module.fail_json(msg="Alert Dest: " + dest_address + " does not exist")
            else:
                # Reject all changes
                idrac.config_mgr._sysconfig.reject()
                module.fail_json(msg="No \"dest_address\" key found:" + str(alert_dest))

        msg['changed'] = idrac.config_mgr._sysconfig.is_changed()

        if module.check_mode:
            # since it is running in check mode, reject all changes
            idrac.config_mgr._sysconfig.reject()
        else:
            msg['msg'] = idrac.config_mgr.apply_changes()
            if 'Status' in msg['msg']:
                if msg['msg']['Status'] == 'Success':
                    msg['changed'] = True
                else:
                    msg['failed'] = True
                    msg['changed'] = False

    except Exception as err:
        error = True
        msg['msg'] = "Error: %s" % str(err)
        msg['exception'] = traceback.format_exc()
        msg['failed'] = True

    return msg, error

# Main
def main():

    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC Handle
            idrac=dict(required=False, type='dict'),

            # iDRAC Credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_pwd=dict(required=True, type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Network File Share
            share_name=dict(required=True, type='str'),
            share_user=dict(required=True, type='str'),
            share_pwd=dict(required=True, type='str', no_log=True),
            share_mnt=dict(required=True, type='path'),

            # SNMP Alert Destinations Configuration Options
            snmp_alert_dest=dict(required=True, type='list'),
            state=dict(required=False, choice=['present', 'absent'], default='present')
        ),
        supports_check_mode=True)

    if not HAS_OMSDK:
        module.fail_json(msg="Dell EMC OpenManage Python SDK required for this module")

    # Connect to iDRAC
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    # Setup network share as local mount
    if not idrac_conn.setup_nw_share_mount():
        module.fail_json(msg="Failed to setup network share local mount point")

    # setup snmp alert destinations
    msg, err = setup_idrac_snmp_alert(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()
