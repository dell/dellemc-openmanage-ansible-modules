#!/usr/bin/python
# _*_ coding: utf-8 _*_

#
# Dell EMC OpenManage Ansible Modules
# Version 1.0
# Copyright (C) 2018 Dell Inc.

# GNU General Public License v3.0+ stripe_size(see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#


from __future__ import (absolute_import, division, print_function)


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_idrac_reset
short_description: Reset iDRAC.
version_added: "2.3"
description:
    - Reset the iDRAC.
options:
    idrac_ip:
        required: True
        description: iDRAC IP Address.
    idrac_user:
        required: True
        description: iDRAC username.
    idrac_pwd:
        required: True
        description: iDRAC user password.
    idrac_port:
        required: False
        description: iDRAC port.
        default: 443

requirements:
    - "omsdk"
    - "python >= 2.7.5"
author: "Felix Stephen (@felixs88)"

"""

EXAMPLES = """
---
- name: Reset iDRAC
  dellemc_idrac_reset:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_pwd:  "xxxxxxxx"
       idrac_port: "xxx"
"""

RETURNS = """
dest:
    description: This module resets iDRAC.
    returned: success
    type: string
"""


from ansible.module_utils.dellemc_idrac import iDRACConnection, logger
from ansible.module_utils.basic import AnsibleModule


# Get Lifecycle Controller status
def run_idrac_reset(idrac, module):
    """
    Get Lifecycle Controller status

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    logger.info(module.params['idrac_ip'] + ': STARTING: idrac reset Method')
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    err = False

    try:
        if module.check_mode:
            msg['msg'] = {'Status': 'Success', 'Message': 'Changes found to commit!', 'changes_applicable': True}
        else:
            idrac.use_redfish = True
            logger.info(module.params['idrac_ip'] + ': CALLING: idrac reset OMSDK API')
            msg['msg']['idracreset'] = idrac.config_mgr.reset_idrac()
            logger.info(module.params['idrac_ip'] + ': FINISHED: idrac reset OMSDK API')
        if "Status" in msg['msg']:
            if msg['msg']['Status'] == "Success":
                msg['changed'] = True
            else:
                msg['failed'] = True
    except Exception as e:
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True
        logger.error(module.params['idrac_ip'] + ': EXCEPTION: idrac reset OMSDK API')
    logger.info(module.params['idrac_ip'] + ': FINISHED: idrac reset Method')
    return msg, err


# Main
def main():
    module = AnsibleModule(
        argument_spec=dict(
            # iDRAC Handle
            idrac=dict(required=False, type='dict'),

            # iDRAC credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_pwd=dict(required=True, type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int')
        ),

        supports_check_mode=True)
    logger.info(module.params['idrac_ip'] + ': STARTING: iDRAC Reset.')
    # Connect to iDRAC
    logger.info(module.params['idrac_ip'] + ': CALLING: iDRAC Connection')
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()
    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Connection Success')
    # Get Lifecycle Controller status
    msg, err = run_idrac_reset(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)
    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Reset.')


if __name__ == '__main__':
    main()
