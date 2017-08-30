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

DOCUMENTATION = """
---
module: dellemc_idrac_lc_job_status
short_description: Returns the status of a Lifecycle Controller Job
version_added: "2.3"
description: Returns the status of a Lifecycle Controller job given a JOB ID
options:
    idrac_ipv4:
        required: True
        description: iDRAC IPv4 Address
    idrac_user:
        description: iDRAC user name
        default: root
    idrac_pwd:
        description: iDRAC user password
    idrac_port:
        description: iDRAC port
    job_id:
        required: True
        description: JOB ID in the format "JID_1234556789012"

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
"""

EXAMPLES = """
---
"""

RETURNS = """
---
"""

from ansible.module_utils.basic import AnsibleModule

# Delete the Job from the LC Job Queue
def delete_lc_job (idrac, module):

    msg = {}
    msg['failed'] = False
    msg['changed'] = False

    msg['msg'] = idrac.job_mgr.delete_job(module.params['job_id'])

    if msg['msg']['Status'] is not "Success":
        msg['failed'] = True

    return msg


# Main
def main():
    from ansible.module_utils.dellemc_idrac import iDRACConnection

    module = AnsibleModule (
            argument_spec = dict (

                # iDRAC handle
                idrac = dict (required = False, type = 'dict'),

                # iDRAC Credentials
                idrac_ipv4 = dict (required = True, type = 'str'),
                idrac_user = dict (required = False, default = 'root', type = 'str'),
                idrac_pwd  = dict (required = False, default = 'calvin',
                                   type = 'str', no_log = True),
                idrac_port = dict (required = False, default = None),

                # JOB ID
                job_id = dict (required = True, type = 'str')
                ),
            supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    msg = delete_lc_job(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    module.exit_json(**msg)

if __name__ == '__main__':
    main()
