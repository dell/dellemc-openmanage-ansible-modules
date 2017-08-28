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
module: dellemc_idrac_lcstatus
short_description: Returns the Lifecycle Controller status
version_added: "2.3"
description:
    - Returns the Lifecycle Controller Status on a Dell EMC PowerEdge Server
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

# Get Lifecycle Controller status
def get_lc_status (idrac, module):

    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['LCReady'] = idrac.config_mgr.LCReady
    msg['LCStatus'] = idrac.config_mgr.LCStatus
    msg['ServerStatus'] = idrac.config_mgr.ServerStatus

    return msg

# Main

def main():

    from ansible.module_utils.dellemc_idrac import iDRACConnection

    module = AnsibleModule (
                 argument_spec = dict (
                     # iDRAC Handle
                     idrac = dict(required=False, type='dict'),

                     # iDRAC credentials
                     idrac_ipv4 = dict(required=True, type='str'),
                     idrac_user = dict(required=False, default='root', type='str'),
                     idrac_pwd = dict(required=False, type='str'),
                     idrac_port = dict(required=False, default=None)
                 ),
                 supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    # Get Lifecycle Controller status
    msg = get_lc_status(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    module.exit_json(**msg)

if __name__ == '__main__':
    main()
