#!/usr/bin/python
# _*_ coding: utf-8 _*_

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0
# Copyright (C) 2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['deprecated'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_export_lc_logs
short_description: Export Lifecycle Controller logs to a network share.
version_added: "2.3"
deprecated:
  removed_in: "2.13"
  why: Replaced with M(idrac_lifecycle_controller_logs).
  alternative: Use M(idrac_lifecycle_controller_logs) instead.
description:
    - Export Lifecycle Controller logs  to a given network share.
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
    share_name:
        required: True
        description: Network share path.
    share_user:
        required: False
        description: Network share user in the format 'user@domain' or 'domain\\user' if user is
            part of a domain else 'user'. This option is mandatory for CIFS Network Share.
    share_password:
        required: False
        description: Network share user password. This option is mandatory for CIFS Network Share.
        aliases: ['share_pwd']
    job_wait:
        required: True
        description: Whether to wait for the running job completion or not.
        type: bool

requirements:
    - "omsdk"
    - "python >= 2.7.5"
author: "Rajeev Arakkal (@rajeevarakkal)"

"""

EXAMPLES = """
---
- name: Export Lifecycle Controller Logs
  dellemc_export_lc_logs:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_password:  "xxxxxxxx"
       idrac_port:  xxx
       share_name: "xx.xx.xx.xx:/share"
       share_user: "xxxx"
       share_password:  "xxxxxxxx"
       job_wait: True
"""

RETURNS = """
dest:
    description: Exports the LC logs to the given network share.
    returned: success
    type: string
    sample: /path/to/file.txt
"""


from ansible.module_utils.remote_management.dellemc.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
try:
    from omsdk.sdkfile import file_share_manager
    from omsdk.sdkcreds import UserCredentials
except ImportError:
    pass


def run_export_lc_logs(idrac, module):
    """
    Export Lifecycle Controller Log to the given file share

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    err = False

    try:
        lclog_file_name_format = "%ip_%Y%m%d_%H%M%S_LC_Log.log"

        myshare = file_share_manager.create_share_obj(share_path=module.params['share_name'],
                                                      creds=UserCredentials(module.params['share_user'],
                                                                            module.params['share_password']),
                                                      isFolder=True)

        lc_log_file = myshare.new_file(lclog_file_name_format)

        job_wait = module.params['job_wait']
        msg['msg'] = idrac.log_mgr.lclog_export(lc_log_file, job_wait)
        if "Status" in msg['msg'] and msg['msg']['Status'] != "Success":
            msg['failed'] = True

    except Exception as e:
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True

    return msg, err


# Main()
def main():
    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_password=dict(required=True, type='str',
                                aliases=['idrac_pwd'], no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Network File Share
            share_name=dict(required=True, type='str'),
            share_user=dict(required=False, type='str'),
            share_password=dict(required=False, type='str',
                                aliases=['share_pwd'], no_log=True),
            job_wait=dict(required=True, type='bool')
        ),

        supports_check_mode=False)
    module.deprecate("The 'dellemc_export_lc_logs' module has been deprecated. "
                     "Use 'idrac_lifecycle_controller_logs' instead",
                     version=2.13)

    try:
        with iDRACConnection(module.params) as idrac:
            msg, err = run_export_lc_logs(idrac, module)
    except (ImportError, ValueError, RuntimeError) as e:
        module.fail_json(msg=str(e))

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
