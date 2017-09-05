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

DOCUMENTATION = """
---
module: dellemc_idrac_inventory
short_description: Returns the PowerEdge Server system inventory
version_added: "2.3"
description:
    - Returns the Dell EMC PowerEdge Server system inventory
options:
    idrac_ip:
        required: True
        description: iDRAC IP Address
    idrac_user:
        description: iDRAC user name
        default: root
    idrac_pwd:
        description: iDRAC user password
        default: calvin
    idrac_port:
        description: iDRAC port
requirements: ['omsdk']

author: "anupam.aloke@dell.com"

"""

EXAMPLES = """
---
"""

RETURNS = """
---
"""

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

    from ansible.module_utils.dellemc_idrac import iDRACConnection

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
