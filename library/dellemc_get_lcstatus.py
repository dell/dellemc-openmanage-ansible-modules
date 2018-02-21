#!/usr/bin/python
# _*_ coding: utf-8 _*_

#
# Dell EMC OpenManage Ansible Modules
# Version 1.0
# Copyright (C) 2018 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
from ansible.module_utils.dellemc_idrac import *
from ansible.module_utils.basic import AnsibleModule
import logging.config

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_get_lcstatus
short_description: Get the Lifecycle Controller status
version_added: "2.3"
description:
    - Get the Lifecycle Controller Status on a Dell EMC PowerEdge Server
options:
    idrac_ip:
        required: True
        description: iDRAC IP Address
        default: None
    idrac_user:
        required: True
        description: iDRAC username
        default: None
    idrac_pwd:
        required: True
        description: iDRAC user password
        default: None
    idrac_port:
        required: False
        description: iDRAC port
        default: 443

requirements:
    - "omsdk"
    - "python >= 2.7"
author: "OpenManageAnsibleEval@dell.com"

"""

EXAMPLES = """
---
- name: Get Lifecycle Controller Status
  dellemc_get_lcstatus:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_pwd:  "xxxxxxxx"
"""

RETURNS = """
---
- dest:
    description: Displays the Lifecycle Controller Status on a Dell EMC PowerEdge Server.
    returned: success
    type: string

"""

log_root = '/var/log'
dell_emc_log_path = log_root + '/dellemc'
dell_emc_log_file = dell_emc_log_path + '/dellemc_log.conf'

logging.config.fileConfig(dell_emc_log_file, defaults={'logfilename': dell_emc_log_path + '/dellemc_lcstatus.log'})
# create logger
logger = logging.getLogger('ansible')


# Get Lifecycle Controller status
def run_get_lc_status(idrac, module):
    """
    Get Lifecycle Controller status

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    logger.info(module.params['idrac_ip'] + ': STARTING: Get LC Status Method')
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    err = False

    try:
        # idrac.use_redfish = True
        logger.info(module.params['idrac_ip'] + ': CALLING: Get LC Status OMSDK API')
        msg['msg']['LCReady'] = idrac.config_mgr.LCReady
        msg['msg']['LCStatus'] = idrac.config_mgr.LCStatus
        logger.info(module.params['idrac_ip'] + ': FINISHED: Get LC Status OMSDK API')
    except Exception as e:
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True
        logger.error(module.params['idrac_ip'] + ': EXCEPTION: Get LC Status OMSDK API')
    logger.info(module.params['idrac_ip'] + ': FINISHED: Get LC Status Method')
    return msg, err


# Main
def main():
    from ansible.module_utils.dellemc_idrac import iDRACConnection

    module = AnsibleModule(
        argument_spec=dict(
            # iDRAC Handle
            idrac=dict(required=False, type='dict'),

            # iDRAC credentials
            idrac_ip=dict(required=True, default=None, type='str'),
            idrac_user=dict(required=True, default=None, type='str'),
            idrac_pwd=dict(required=True, default=None,
                           type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int')
        ),

        supports_check_mode=True)

    # Connect to iDRAC
    logger.info(module.params['idrac_ip'] + ': CALLING: iDRAC Connection')
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()
    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Connection Success')
    # Get Lifecycle Controller status
    msg, err = run_get_lc_status(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
