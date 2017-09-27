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

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: dellemc_idrac_lc_job_status
short_description: Get the status of a Lifecycle Controller Job
version_added: "2.3"
description: Get the status of a Lifecycle Controller job given a JOB ID
options:
  idrac_ip:
    required: False
    description:
      - iDRAC IP Address
    default: None
  idrac_user:
    required: False
    description:
      - iDRAC user name
    default: None
  idrac_pwd:
    required: False
    description:
      - iDRAC user password
    default: None
  idrac_port:
    required: False
    description:
      - iDRAC port
    default: None
  job_id:
    required: True
    description:
      - JOB ID in the format JID_123456789012
      - if C(JID_CLEARALL), then all jobs will be cleared from the LC job queue
    default: None
  state:
    required: False
    description:
      - if C(present) then return the status of the associated job having the job id provided in I(job_id)
      - if C(absent), then delete the associated job having the job id provided in I(job_id) from LC job queue
    default: 'present'

requirements: ['omsdk']
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
      state:      "absent"

'''

RETURN = '''
'''

from ansible.module_utils.dellemc_idrac import *
from ansible.module_utils.basic import AnsibleModule

def lc_job_status (idrac, module):
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

def delete_lc_job (idrac, module):
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
        msg[failed] = True

    return msg, err

def delete_lc_job_queue (idrac, module):
    """
    Deletes LC Job Queue

    Keyword arguments:
    idrac  -- iDRAC handler
    module -- Ansible module
    """

    msg = {}
    msg['failed'] = False
    msg['changed'] = False

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

    module = AnsibleModule (
            argument_spec = dict (

                # iDRAC handle
                idrac = dict (required = False, type = 'dict'),

                # iDRAC Credentials
                idrac_ip   = dict (required = False, default = None, type = 'str'),
                idrac_user = dict (required = False, default = None, type = 'str'),
                idrac_pwd  = dict (required = False, default = None,
                                   type = 'str', no_log = True),
                idrac_port = dict (required = False, default = None, type = 'int'),
                # JOB ID
                job_id = dict (required = True, type = 'str'),

                # state
                state = dict (required = False,
                              choices = ['present', 'absent'],
                              default = 'present')
                ),

            supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    msg = {}
    err = False

    if module.params['state'] == "present":
        msg, err = lc_job_status(idrac, module)
    elif module.params['state'] == "absent":
        if module.params['job_id'] == 'JID_CLEARALL':
            msg, err = delete_lc_job_queue(idrac)
        else:
            msg, err = delete_lc_job(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()
