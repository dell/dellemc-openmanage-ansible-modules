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
module: dellemc_delete_lc_job
short_description: Delete a Lifecycle Controller Job.
version_added: "2.3"
deprecated:
  removed_in: "2.13"
  why: Replaced with M(idrac_lifecycle_controller_job).
  alternative: Use M(idrac_lifecycle_controller_job) instead.
description:
    - Delete a Lifecycle Controller job for a given a JOB ID.
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
    job_id:
        required: True
        description: JOB ID in the format "JID_XXXXXXXX".

requirements:
    - "omsdk"
    - "python >= 2.7.5"
author: "Felix Stephen (@felixs88)"
"""

EXAMPLES = """
---
- name: Delete LC Job
  dellemc_delete_lc_job:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_password:  "xxxxxxxx"
       idrac_port: xxx
       job_id:     "JID_XXXXXXXX"
"""

RETURNS = """
dest:
    description: Deletes a Lifecycle Controller job for a given a JOB ID.
    returned: success
    type: string
"""


from ansible.module_utils.remote_management.dellemc.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule


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
    check_mode_err = False

    try:
        # idrac.use_redfish = True
        exists = False
        try:
            job = idrac.job_mgr.get_job_status(module.params['job_id'])
        except Exception as err:
            check_mode_err = True
        if 'Status' in job and (not job['Status'] == "Found Fault"):
            exists = True

        if module.check_mode:
            if check_mode_err:
                msg['msg'] = {'Status': 'Failed', 'Message': 'Failed to execute the command!',
                              'changes_applicable': False}
            else:
                if exists:
                    msg['msg'] = {'Status': 'Success', 'Message': 'Job found to delete!', 'changes_applicable': True}
                else:
                    msg['msg'] = {'Status': 'Success', 'Message': 'Job not found to delete!',
                                  'changes_applicable': False}
            msg["changed"] = exists
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

            # JOB ID
            job_id=dict(required=True, type='str')
        ),

        supports_check_mode=True)
    module.deprecate("The 'dellemc_delete_lc_job' module has been deprecated. "
                     "Use 'idrac_lifecycle_controller_job instead",
                     version=2.13)

    try:
        with iDRACConnection(module.params) as idrac:
            msg, err = run_delete_lc_job(idrac, module)
    except (ImportError, ValueError, RuntimeError) as e:
        module.fail_json(msg=str(e))

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
