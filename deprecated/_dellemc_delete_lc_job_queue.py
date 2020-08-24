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
module: dellemc_delete_lc_job_queue
short_description: Delete the Lifecycle Controller Job Queue.
version_added: "2.3"
deprecated:
  removed_in: "2.13"
  why: Replaced with M(idrac_lifecycle_controller_jobs).
  alternative: Use M(idrac_lifecycle_controller_jobs) instead.
description:
    - Delete the complete Lifecycle Controller Job Queue.
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
author: "Felix Stephen (@felixs88)"

"""

EXAMPLES = """
---
- name: Delete LC Job Queue
  dellemc_delete_lc_job_queue:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_password:  "xxxxxxxx"
       idrac_port: xxx
"""

RETURNS = """
dest:
    description: Deletes a Lifecycle Controller Job Queue.
    returned: success
    type: string
"""


from ansible.module_utils.remote_management.dellemc.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule


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
            msg['msg'] = idrac.job_mgr.delete_all_jobs()
            if msg['msg']['Status'] == "Success":
                msg['changed'] = True
            else:
                msg['failed'] = True

    except Exception as e:
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True

    return msg, err


# Main
def main():
    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC Credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_password=dict(required=True, type='str', aliases=['idrac_pwd'], no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),
        ),

        supports_check_mode=False)
    module.deprecate("The 'dellemc_delete_lc_job_queue' module has been deprecated. "
                     "Use 'idrac_lifecycle_controller_jobs instead",
                     version=2.13)

    try:
        with iDRACConnection(module.params) as idrac:
            msg, err = run_delete_lc_job_queue(idrac, module)
    except (ImportError, ValueError, RuntimeError) as e:
        module.fail_json(msg=str(e))

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
