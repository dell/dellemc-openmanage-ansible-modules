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
#

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: dellemc_idrac_inventory
short_description: Returns the PowerEdge Server system inventory
version_added: "2.3"
description:
    - Returns the Dell EMC PowerEdge Server system inventory
options:
  idrac_ip:
    required: False
    description:
      - iDRAC IP Address
    default: None
  idrac_user:
    required: False
    description:
      - iDRAC user name
    default: None
  idrac_pwd:
    required: False
    description:
      - iDRAC user password
    default: None
  idrac_port:
    required: False
    description: iDRAC port
    default: None

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
'''

EXAMPLES = '''
---
- name: Get System Inventory
  dellemc_idrac_inventory:
    idrac_ip:   "192.168.1.1"
    idrac_user: "root"
    idrac_pwd:  "calvin"
'''

RETURN = '''
---
'''

from ansible.module_utils.dellemc_idrac import *
from ansible.module_utils.basic import AnsibleModule

# Get System Inventory
def get_system_inventory(idrac):
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    err = False

    try:
        idrac.get_entityjson()
        msg['msg'] = idrac.get_json_device()
    except Exception as e:
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True

    return msg, err

# Main
def main():

    module = AnsibleModule(
            argument_spec = dict(

                # iDRAC Handle
                idrac = dict(required=False, type='dict'),

                # iDRAC credentials
                idrac_ip   = dict(required = False, default = None, type='str'),
                idrac_user = dict(required = False, default = None, type='str'),
                idrac_pwd  = dict(required = False, default = None,
                                  type='str', no_log = True),
                idrac_port = dict(required = False, default = None)
            ),

            supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    # Get System Inventory
    msg, err = get_system_inventory(idrac)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(ansible_facts = {idrac.ipaddr: {'SystemInventory': msg['msg']}})

if __name__ == '__main__':
    main()
