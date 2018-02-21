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
module: dellemc_delete_lc_job_queue
short_description: Delete the Lifecycle Controller Job Queue
version_added: "2.3"
description:
    - Delete the complete Lifecycle Controller Job Queue
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
- name: Delete LC Job Queue
  dellemc_delete_lc_job_queue:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_pwd:  "xxxxxxxx"
       idrac_port: xxx
"""

RETURNS = """
---
- dest:
    description: Deletes a Lifecycle Controller Job Queue.
    returned: success
    type: string

"""

log_root = '/var/log'
dell_emc_log_path = log_root + '/dellemc'
dell_emc_log_file = dell_emc_log_path + '/dellemc_log.conf'

logging.config.fileConfig(dell_emc_log_file,
                          defaults={'logfilename': dell_emc_log_path + '/dellemc_delete_lc_job_queue.log'})
# create logger
logger = logging.getLogger('ansible')


def run_delete_lc_job_queue(idrac, module):
    """
    Deletes the Lifecycle Controller JOB Queue

    idrac  -- iDRAC handle
    module -- Ansible module
    """

    msg = {}
    msg['failed'] = False
    msg['changed'] = False
    err = False

    try:
        if not module.check_mode:
            # TODO: Check the Job Queue to make sure there are no pending jobs
            logger.info(
                module.params['idrac_ip'] + ': STARTING: Delete LC Job Queue method: Invoking OMSDK Export SCP API')
            msg['msg'] = idrac.job_mgr.delete_all_jobs()
            logger.info(
                module.params['idrac_ip'] + ': FINISHED: Delete LC Job Queue method: Invoking OMSDK Export SCP API')
            if msg['msg']['Status'] == "Success":
                msg['changed'] = True
            else:
                msg['failed'] = True

    except Exception as e:
        logger.error(module.params['idrac_ip'] + ': EXCEPTION: Delete LC Job Queue method: ' + str(e))
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True

    return msg, err


# Main
def main():
    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC handle
            idrac=dict(required=False, type='dict'),

            # iDRAC Credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_pwd=dict(required=True, type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),
        ),

        supports_check_mode=True)

    # Connect to iDRAC
    logger.info(module.params['idrac_ip'] + ': CALLING: iDRAC Connection')
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()
    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Connection is successful with target ')
    msg, err = run_delete_lc_job_queue(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)
    logger.info(module.params['idrac_ip'] + ': FINISHED: Deleted lc Job queue ' + module.params['job_id'])


if __name__ == '__main__':
    main()
