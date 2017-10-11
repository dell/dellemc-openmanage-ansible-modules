#! /usr/bin/python
# _*_ coding: utf-8 _*_

#
# Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved.
# Dell, EMC, and other trademarks are trademarks of Dell Inc. or its
# subsidiaries. Other trademarks may be trademarks of their respective owners.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: dellemc_idrac_lc_job
short_description: Get the status of a Lifecycle Controller Job, delete a LC Job
version_added: "2.3"
description:
  - Get the status of a Lifecycle Controller job given a JOB ID
  - Delete a LC Job from the Job queue given a JOB ID
  - Delete LC Job Queue
options:
  idrac_ip:
    required: True
    description:
      - iDRAC IP Address
    type: 'str'
  idrac_user:
    required: True
    description:
      - iDRAC user name
    type: 'str'
  idrac_pwd:
    required: True
    description:
      - iDRAC user password
    type: 'str'
  idrac_port:
    required: False
    description:
      - iDRAC port
    default: 443
    type: 'int'
  job_id:
    required: True
    description:
      - JOB ID in the format JID_123456789012
      - if C(JID_CLEARALL), then all jobs will be cleared from the LC job queue
    type: 'str'
  state:
    required: False
    description:
      - if C(present), returns the status of the associated job having the job id provided in I(job_id)
      - if C(present) and I(job_id) == C(JID_CLEARALL), then delete the job queue
      - if C(absent), then delete the associated job having the job id provided in I(job_id) from LC job queue
    default: 'present'

requirements: ['Dell EMC OpenManage Python SDK']
author: "anupam.aloke@dell.com"
'''

EXAMPLES = '''
# Get Job Status for a valid JOB ID
- name: Get LC Job Stattus
    dellemc_idrac_lc_job:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      job_id:     "JID_1234556789012"
      state:      "present"

# Delete the JOB from the LC Job Queue
- name: Delete the LC Job
    dellemc_idrac_lc_job:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      job_id:     "JID_1234556789012"
      state:      "absent"

# Clear the LC Job queue
- name: Clear the LC Job queue
    dellemc_idrac_lc_job:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      job_id:     "JID_CLEARALL"
      state:      "present"

'''

RETURN = '''
'''

from ansible.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule

def lc_job_status(idrac, module):
    """
    Get status of a Lifecycle Controller Job given a JOB ID

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    msg = {}
    msg['failed'] = False
    msg['changed'] = False
    err = False

    try:
        msg['msg'] = idrac.job_mgr.get_job_status(module.params['job_id'])

        if "Status" in msg['msg'] and msg['msg']['Status'] != "Success":
            msg['failed'] = True

    except Exception as e:
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True

    return msg, err

def delete_lc_job(idrac, module):
    """
    Delete a Job from the LC Job queue give an Job ID

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    msg = {}
    msg['failed'] = False
    msg['changed'] = False
    err = False

    try:
        exists = False

        job = idrac.job_mgr.get_job_details(module.params['job_id'])

        if 'Status' in job and job['Status'] == "Success":
            exists = True

        if module.check_mode:
            msg['changed'] = exists
        elif exists:
            msg['msg'] = idrac.job_mgr.delete_job(module.params['job_id'])

            if 'Status' in msg['msg']:
                if msg['msg']['Status'] == "Success":
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

def delete_lc_job_queue(idrac, module):
    """
    Deletes LC Job Queue

    Keyword arguments:
    idrac  -- iDRAC handler
    module -- Ansible module
    """

    msg = {}
    msg['failed'] = False
    msg['changed'] = False
    err = False

    try:
        # TODO: Check the Job Queue to make sure there are no pending jobs
        exists = False

        job = idrac.job_mgr.get_job_details('JID_CLEARALL')

        if 'Status' in job and job['Status'] == "Success":
            exists = True

        if module.check_mode or exists:
            msg['changed'] = not exists
        else:
            msg['msg'] = idrac.job_mgr.delete_all_jobs()

            if 'Status' in msg['msg'] and msg['msg']['Status'] == "Success":
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

            # iDRAC handle
            idrac=dict(required=False, type='dict'),

            # iDRAC Credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_pwd=dict(required=True, type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # JOB ID
            job_id=dict(required=True, type='str'),

            # state
            state=dict(required=False, choices=['present', 'absent'],
                       default='present')
        ),

        supports_check_mode=True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    msg = {}
    err = False

    if module.params['state'] == "present":
        if module.params['job_id'] != 'JID_CLEARALL':
            msg, err = lc_job_status(idrac, module)
        else:
            msg, err = delete_lc_job_queue(idrac, module)
    elif module.params['state'] == "absent":
        msg, err = delete_lc_job(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()
