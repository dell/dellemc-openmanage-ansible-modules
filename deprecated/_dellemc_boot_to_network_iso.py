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
module: dellemc_boot_to_network_iso
short_description: Boot to a network ISO image.
version_added: "2.3"
deprecated:
  removed_in: "3.3"
  why: Replaced with M(idrac_os_deployment).
  alternative: Use M(idrac_os_deployment) instead.
description: Boot to a network ISO image.
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
        description: CIFS or NFS Network share.
    share_user:
        required: False
        description: Network share user in the format 'user@domain' or 'domain\\user' if user is
            part of a domain else 'user'. This option is mandatory for CIFS Network Share.
    share_password:
        required: False
        description: Network share user password. This option is mandatory for CIFS Network Share.
        aliases: ['share_pwd']
    iso_image:
        required: True
        description: Network ISO name.
requirements:
    - "omsdk"
    - "python >= 2.7.5"
author: "Felix Stephen (@felixs88)"
"""

EXAMPLES = """
---
- name: Boot to Network ISO
  dellemc_boot_to_network_iso:
      idrac_ip:   "xx.xx.xx.xx"
      idrac_user: "xxxx"
      idrac_password:  "xxxxxxxx"
      share_name: "xx.xx.xx.xx:/share"
      share_user: "xxxx"
      share_password:  "xxxxxxxx"
      iso_image:  "uninterrupted_os_installation_image.iso"
"""

RETURN = """
dest:
    description: Boots to a network ISO image.
    returned: success
    type: string
"""


import os
from ansible.module_utils.remote_management.dellemc.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
try:
    from omsdk.sdkfile import FileOnShare
    from omsdk.sdkcreds import UserCredentials
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False


def run_boot_to_network_iso(idrac, module):
    """
    Boot to a network ISO image
    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    err = False

    try:
        share_name = module.params['share_name']
        if share_name is None:
            share_name = ''
        myshare = FileOnShare(remote="{}{}{}".format(share_name, os.sep, module.params['iso_image']),
                              isFolder=False,
                              creds=UserCredentials(
                                  module.params['share_user'],
                                  module.params['share_password'])
                              )
        msg['msg'] = idrac.config_mgr.boot_to_network_iso(myshare, "")

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
    module = AnsibleModule(
        argument_spec=dict(
            # iDRAC Credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_password=dict(required=True, type='str', aliases=['idrac_pwd'], no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Network File Share
            share_name=dict(required=True, type='str'),
            share_user=dict(required=False, type='str'),
            share_password=dict(required=False, type='str', aliases=['share_pwd'], no_log=True),

            # ISO Image relative to Network File Share
            iso_image=dict(required=True, type='str'),

        ),
        supports_check_mode=False)
    module.deprecate("The 'dellemc_boot_to_network_iso' module has been deprecated. "
                     "Use 'idrac_os_deployment' instead",
                     version=3.3)
    try:
        with iDRACConnection(module.params) as idrac:
            msg, err = run_boot_to_network_iso(idrac, module)
    except (ImportError, ValueError, RuntimeError) as e:
        module.fail_json(msg=str(e))

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
