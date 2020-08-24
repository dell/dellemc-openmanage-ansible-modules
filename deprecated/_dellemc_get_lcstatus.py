#!/usr/bin/python
# _*_ coding: utf-8 _*_

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0
# Copyright (C) 2018-2019 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['deprecated'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_get_lcstatus
short_description: Get the Lifecycle Controller status.
version_added: "2.3"
deprecated:
  removed_in: "2.13"
  why: Replaced with M(idrac_lifecycle_controller_status_info).
  alternative: Use M(idrac_lifecycle_controller_status_info) instead.
description:
    - Get the Lifecycle Controller Status on a Dell EMC PowerEdge Server.
options:
    idrac_ip:
        required: True
        description: iDRAC IP Address.
    idrac_user:
        required: True
        description: iDRAC username.
    idrac_password:
        required: True
        description: iDRAC user password.
        aliases: ['idrac_pwd']
    idrac_port:
        required: False
        description: iDRAC port.
        default: 443

requirements:
    - "omsdk"
    - "python >= 2.7.5"
author: "Rajeev Arakkal (@rajeevarakkal)"

"""

EXAMPLES = """
---
- name: Get Lifecycle Controller Status
  dellemc_get_lcstatus:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_password:  "xxxxxxxx"
"""

RETURNS = """
dest:
    description: Displays the Lifecycle Controller Status on a Dell EMC PowerEdge Server.
    returned: success
    type: string
"""


from ansible.module_utils.remote_management.dellemc.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule


# Get Lifecycle Controller status
def run_get_lc_status(idrac, module):
    """
    Get Lifecycle Controller status

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    err = False

    try:
        # idrac.use_redfish = True
        msg['msg']['LCReady'] = idrac.config_mgr.LCReady
        msg['msg']['LCStatus'] = idrac.config_mgr.LCStatus
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
            idrac_password=dict(required=True, type='str',
                                aliases=['idrac_pwd'], no_log=True),
            idrac_port=dict(required=False, default=443, type='int')
        ),

        supports_check_mode=False)
    module.deprecate("The 'dellemc_get_lcstatus' module has been deprecated. "
                     "Use 'idrac_lifecycle_controller_status_info instead",
                     version=2.13)

    try:
        with iDRACConnection(module.params) as idrac:
            msg, err = run_get_lc_status(idrac, module)
    except (ImportError, ValueError, RuntimeError) as e:
        module.fail_json(msg=str(e))

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
