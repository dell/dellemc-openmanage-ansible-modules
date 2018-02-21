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
module: dellemc_export_lc_logs
short_description: Export Lifecycle Controller logs to a network share
version_added: "2.3"
description:
    - Export Lifecycle Controller logs  to a given network share
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
    share_name:
        required: True
        description: Network share path
    share_user:
        required: True
        description: Network share user in the format 'user@domain' if user is part of a domain else 'user'.
    share_pwd:
        required: True
        description: Network share user password
    job_wait:
        required: True
        description: Whether to wait for the running job completion or not
        choices: [True,  False]

requirements:
    - "omsdk"
    - "python >= 2.7"
author: "OpenManageAnsibleEval@dell.com"

"""

EXAMPLES = """
---
- name: Export Lifecycle Controller Logs
  dellemc_export_lc_logs:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_pwd:  "xxxxxxxx"
       idrac_port:  xxx
       share_name: "\\\\xx.xx.xx.xx\\share\\"
       share_user: "xxxx"
       share_pwd:  "xxxxxxxx"
       job_wait: True
"""

RETURNS = """
---
- dest:
    description: Exports the LC logs to the given network share.
    returned: success
    type: string
    sample: /path/to/file.txt
"""

log_root = '/var/log'
dell_emc_log_path = log_root + '/dellemc'
dell_emc_log_file = dell_emc_log_path + '/dellemc_log.conf'

logging.config.fileConfig(dell_emc_log_file,
                          defaults={'logfilename': dell_emc_log_path + '/dellemc_export_lc_logs.log'})
# create logger
logger = logging.getLogger('ansible')


def run_export_lc_logs(idrac, module):
    """
    Export Lifecycle Controller Log to the given file share

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    logger.info(module.params['idrac_ip'] + ': STARTING: Export LC logs method: Invoking OMSDK Export LC Log API')
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    err = False

    try:
        lclog_file_name_format = "%ip_%Y%m%d_%H%M%S_LC_Log.log"

        logger.info(module.params['idrac_ip'] + ': STARTING: Creating a File Share Object')
        myshare = file_share_manager.create_share_obj(share_path=module.params['share_name'],
                                                      creds=UserCredentials(module.params['share_user'],
                                                                            module.params['share_pwd']),
                                                      isFolder=True)
        logger.info(module.params['idrac_ip'] + ': FINISHED: Created a File Share Object')
        # myshare = FileOnShare(module.params['share_name'],
        #                       mount_point = '',
        #                      isFolder = True)
        # myshare.addcreds(UserCredentials(module.params['share_user'],
        #                                module.params['share_pwd']))
        lc_log_file = myshare.new_file(lclog_file_name_format)

        job_wait = module.params['job_wait']
        msg['msg'] = idrac.log_mgr.lclog_export(lc_log_file, job_wait)
        logger.info(module.params['idrac_ip'] + ': FINISHED:  Export LC logs method: Invoking OMSDK Export LC Log API')
        if "Status" in msg['msg'] and msg['msg']['Status'] != "Success":
            msg['failed'] = True

    except Exception as e:
        logger.error(module.params['idrac_ip'] + ': EXCEPTION: Export LC Logs Method: ' + str(e))
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True

    return msg, err


# Main()
def main():
    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC handle
            idrac=dict(required=False, type='dict'),

            # iDRAC credentials
            idrac_ip=dict(required=True, default=None, type='str'),
            idrac_user=dict(required=True, default=None, type='str'),
            idrac_pwd=dict(required=True, default=None,
                           type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Network File Share
            share_name=dict(required=True, type='str'),
            share_user=dict(required=True, type='str'),
            share_pwd=dict(required=True, type='str', no_log=True),
            job_wait=dict(required=True, type='bool')
        ),

        supports_check_mode=True)
    logger.info(module.params['idrac_ip'] + ': CALLING: iDRAC Connection')
    # Connect to iDRAC
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()
    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Connection is successful with target')
    # Export LC Logs
    msg, err = run_export_lc_logs(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)
    logger.info(module.params['idrac_ip'] + ': FINISHED: Exported lc logs')


if __name__ == '__main__':
    main()
