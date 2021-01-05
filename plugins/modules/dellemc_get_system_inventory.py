#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.5
# Copyright (C) 2018-2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_get_system_inventory
short_description: Get the PowerEdge Server System Inventory.
version_added: "2.3.0"
description:
    - Get the PowerEdge Server System Inventory.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options

requirements:
    - "omsdk"
    - "python >= 2.7.5"
author: "Rajeev Arakkal (@rajeevarakkal)"

"""

EXAMPLES = """
---
- name: Get System Inventory
  dellemc.openmanage.dellemc_get_system_inventory:
    idrac_ip: "xx.xx.xx.xx"
    idrac_user: "xxxx"
    idrac_password: "xxxxxxxx"
"""

RETURNS = """
dest:
    description: Displays the Dell EMC PowerEdge Server System Inventory.
    returned: success
    type: string
"""


from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule


# Get System Inventory
def run_get_system_inventory(idrac, module):
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    err = False

    try:
        # idrac.use_redfish = True
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
        argument_spec=dict(

            # iDRAC credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_password=dict(required=True, type='str', aliases=['idrac_pwd'], no_log=True),
            idrac_port=dict(required=False, type='int', default=443)
        ),
        supports_check_mode=False)

    try:
        with iDRACConnection(module.params) as idrac:
            msg, err = run_get_system_inventory(idrac, module)
    except (ImportError, ValueError, RuntimeError) as e:
        module.fail_json(msg=str(e))

    if err:
        module.fail_json(**msg)
    module.exit_json(ansible_facts={idrac.ipaddr: {'SystemInventory': msg['msg']}})


if __name__ == '__main__':
    main()
