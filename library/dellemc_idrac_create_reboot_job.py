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
module: dellemc_idrac_create_reboot_job
short_description: Create a Reboot Job
version_added: "2.3"
description:
    - Create a Reboot Job, add it to Job Queue and wait till it is complete
options:
    idrac_ip:
        required: False
        description: iDRAC IP Address
        default: None
    idrac_user:
        required: False
        description: iDRAC user name
        default: None
    idrac_pwd:
        required: False
        description: iDRAC user password
        default: None
    idrac_port:
        required: False
        description: iDRAC port
        default: None
    reboot_option:
        required: False
        description:
        - if C(PowerCycle), power cycle the server
        - if C(GracefulRebootWithoutShutdown), graceful reboot without shutdown
        - if C(GracefulRebootWithForcedShutdown), graceful reboot with PowerCycle on shutdown
        choiced: ['PowerCycle', 'GracefulRebootWithoutShutdown', GracefulRebootWithForcedShutdown']
        default: 'GracefulRebootWithForcedShutdown'

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
"""

EXAMPLES = """
---
- name: Create a Reboot Job
    dellemc_idrac_create_reboot_job:
       idrac_ip:   "192.168.1.1"
       idrac_user: "root"
       idrac_pwd:  "calvin"
"""

RETURNS = """
---
"""

from ansible.module_utils.basic import AnsibleModule

def create_reboot_job (idrac, module):
    """
    Create a Reboot Job

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    
    from omdrivers.lifecycle.iDRAC.iDRACConfig import RebootJobType

    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    err = False

    try:
        if module.check_mode:
            msg['changed'] = True
            
        else:
            reboot_option = RebootJobType.GracefulRebootWithForcedShutdown

            if module.params['reboot_option'] == 'PowerCycle':
                reboot_option = RebootJobType.PowerCycle
            elif module.params['reboot_option'] == 'GracefulRebootWithoutShutdown':
                reboot_option = RebootJobType.GracefulRebootWithoutShutdown

            msg['msg'] = idrac.config_mgr.reboot_after_config(reboot_option) 

            if "Status" in msg['msg']:
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

    from ansible.module_utils.dellemc_idrac import iDRACConnection

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

                # Reboot option
                reboot_option = dict (required = False,
                                    choices = ['PowerCycle',
                                                'GracefulRebootWithoutShutdown',
                                                'GracefulRebootWithForcedShutdown'],
                                    default = 'GracefulRebootWithForcedShutdown')
                ),

            supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    msg, err = create_reboot_job (idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()
