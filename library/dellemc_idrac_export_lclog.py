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
module: dellemc_idrac_export_lclog
short_description: Export Lifecycle Controller log file to a network share
version_added: "2.3"
description:
    - Export Lifecycle Controller log file to a given network share
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
    share_name:
        description: CIFS or NFS Network share 
    share_user:
        description: Network share user in the format user@domain
    share_pwd:
        description: Network share user password

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
"""

EXAMPLES = """
---
"""

RETURNS = """
---
"""

import sys
import os
import json
from ansible.module_utils.basic import AnsibleModule

try:
    from omsdk.sdkfile import FileOnShare
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False

# Export Lifecycle Controller Logs
def exportLifecycleControllerLogs (idrac, module):

    msg = {}
    msg['ExportLCLog'] = {}
    msg['msg'] = ''
    msg['changed'] = False
    msg['failed'] = False

    lclog_file_name = idrac.ipaddr + "_%Y%M%d_LC_Log.log"

    share_path = module.params['share_name'] + lclog_file_name

    myshare = FileOnShare(share_path)
    myshare.addcreds(UserCredentials(module.params['share_user'],
        module.params['share_pwd']))

    msg['ExportLCLog'] = idrac.log_mgr.lclog_export(myshare)

    if not msg['ExportLCLog']['retval']:
        msg['failed'] = True

    return msg

# Main()
def main():

    from ansible.module_utils.dellemc_idrac import iDRACConnection

    module = AnsibleModule (
            argument_spec = dict (
                # iDRAC handle
                idrac = dict (required = False, type = 'dict'),

                # iDRAC credentials
                idrac_ipv4 = dict (required = True, type = 'str'),
                idrac_user = dict (required = False, default = None, type = 'str'),
                idrac_pwd  = dict (required = False, default = None, type = 'str'),
                idrac_port = dict (required = False, default = None),

                # Network File Share
                share_name = dict (required = True, default = None),
                share_pwd  = dict (required = True, default = None),
                share_user = dict (required = True, default = None)
            ),

            supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    # Export LC Logs
    msg = exportLifecycleControllerLogs(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    module.exit_json(**msg)

if __name__ == '__main__':
    main()
