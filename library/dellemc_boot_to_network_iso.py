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


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_boot_to_network_iso
short_description: Boot to a network ISO image.
version_added: "2.3"
description: Boot to a network ISO image.
options:
    idrac_ip:
        required: True
        description: iDRAC IP Address.
    idrac_user:
        required: True
        description: iDRAC username.
    idrac_pwd:
        required: True
        description: iDRAC user password.
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
    share_pwd:
        required: False
        description: Network share user password. This option is mandatory for CIFS Network Share.
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
      idrac_pwd:  "xxxxxxxx"
      share_name: "xx.xx.xx.xx:/share"
      share_user: "xxxx"
      share_pwd:  "xxxxxxxx"
      iso_image:  "uninterrupted_os_installation_image.iso"
"""

RETURN = """
dest:
    description: Boots to a network ISO image.
    returned: success
    type: string
"""


from ansible.module_utils.dellemc_idrac import iDRACConnection
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
        myshare = FileOnShare(remote=module.params['share_name'] + "/" + module.params['iso_image'],
                              isFolder=False,
                              creds=UserCredentials(
                                  module.params['share_user'],
                                  module.params['share_pwd'])
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
            idrac_pwd=dict(required=True, type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Network File Share
            share_name=dict(required=True, type='str'),
            share_user=dict(required=False, type='str'),
            share_pwd=dict(required=False, type='str', no_log=True),

            # ISO Image relative to Network File Share
            iso_image=dict(required=True, type='str'),

        ),
        supports_check_mode=False)

    if not HAS_OMSDK:
        module.fail_json(msg="Dell EMC OpenManage Python SDK required for this module")

    # Connect to iDRAC
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    msg, err = run_boot_to_network_iso(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
