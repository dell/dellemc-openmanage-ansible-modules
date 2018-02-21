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
module: dellemc_delete_lc_job
short_description: Delete a Lifecycle Controller Job
version_added: "2.3"
description:
    - Delete a Lifecycle Controller job for a given a JOB ID
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
    job_id:
        required: True
        description: JOB ID in the format "JID_XXXXXXXX"

requirements:
    - "omsdk"
    - "python >= 2.7"
author: "OpenManageAnsibleEval@dell.com"
    
"""

EXAMPLES = """
---
- name: Delete LC Job
  dellemc_delete_lc_job:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_pwd:  "xxxxxxxx"
       idrac_port: xxx
       job_id:     "JID_XXXXXXXX"
"""

RETURNS = """
---
- dest:
    description: Deletes a Lifecycle Controller job for a given a JOB ID.
    returned: success
    type: string

"""

log_root = '/var/log'
dell_emc_log_path = log_root + '/dellemc'
dell_emc_log_file = dell_emc_log_path + '/dellemc_log.conf'

logging.config.fileConfig(dell_emc_log_file, defaults={'logfilename': dell_emc_log_path + '/dellemc_delete_lc_job.log'})
# create logger
logger = logging.getLogger('ansible')


def run_delete_lc_job(idrac, module):
    """
    Deletes a Lifecycle Controller Job

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    msg = {}
    msg['failed'] = False
    msg['changed'] = False
    err = False

    try:
        # idrac.use_redfish = True
        exists = False
        logger.info(module.params['idrac_ip'] + ': STARTING: Delete LC Job method: Invoking OMSDK Export SCP API')
        job = idrac.job_mgr.get_job_status(module.params['job_id'])
        logger.info(module.params['idrac_ip'] + ': FINISHED: Delete LC Job method: Invoking OMSDK Export SCP API')
        if 'Status' in job and job['Status'] == "Success":
            exists = True

        if module.check_mode:
            msg['changed'] = not exists
        elif exists:
            msg['msg'] = idrac.job_mgr.delete_job(module.params['job_id'])

            if 'Status' in msg['msg'] and msg['msg']['Status'] == "Success":
                msg['changed'] = True
            else:
                msg['failed'] = True
        else:
            msg['msg'] = "Invalid Job ID: " + module.params['job_id']
            msg['failed'] = True

    except Exception as e:
        logger.error(module.params['idrac_ip'] + ': EXCEPTION: Delete LC Job method: ' + str(e))
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

            # JOB ID
            job_id=dict(required=True, type='str')
        ),

        supports_check_mode=True)

    # Connect to iDRAC

    logger.info(module.params['idrac_ip'] + ': CALLING: iDRAC Connection')
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()
    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Connection is successful with target ')
    (msg, err) = run_delete_lc_job(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)
    logger.info(module.params['idrac_ip'] + ': FINISHED: Deleted lc Job ' + module.params['job_id'])


if __name__ == '__main__':
    main()
