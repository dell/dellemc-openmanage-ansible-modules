#! /usr/bin/python
# _*_ coding: utf-8 _*_

#
# Dell EMC OpenManage Ansible Modules
#
# Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved.
# Dell, EMC, and other trademarks are trademarks of Dell Inc. or its
# subsidiaries. Other trademarks may be trademarks of their respective owners.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: dellemc_idrac_lc_attr
short_description: Configure iDRAC Lifecycle Controller attributes
version_added: "2.3"
description:
    - Configure following iDRAC Lifecycle Controller attributes:
        CollectSystemInventoryOnRestart (CSIOR)
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
  share_name:
    required: True
    description: Network file share (either CIFS or NFS)
    type: 'str'
  share_user:
    required: True
    description: Network share user in the format 'user@domain' if user is part of a domain else 'user'
  share_pwd:
    required: True
    description: Network share user password
    type: 'str'
  share_mnt:
    required: True
    description: Local mount path of the network file share specified in I(share_name) with read-write permission for ansible user
    type: 'path'
  csior:
    required: False
    choices: ['Enabled', 'Disabled']
    description:
      - if C(Enabled), will enable the CSIOR
      - if C(Disabled), will disable the CSIOR
      - I(reboot) should be set to C(True) to apply any changes
    default: 'Enabled'
  reboot:
    required: False
    description:
      - if C(True), will restart the system after applying the changes
      - if C(False), will not restart the system after applying the changes
    default: False
    type: 'bool'

requirements: ['Dell EMC OpenManage Python SDK']
author: "anupam.aloke@dell.com"
'''

EXAMPLES = '''
- name: Enable CSIOR
    dellemc_idrac_lc_attr:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      csior:      "Enabled"
      reboot:     True

- name: Disable CSIOR
    dellemc_idrac_lc_attr:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      csior:      "Disabled"
      reboot:     True
'''

RETURN = '''
'''

from ansible.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
try:
    from omsdk.sdkcenum import TypeHelper
    from omdrivers.enums.iDRAC.iDRAC import (
        CollectSystemInventoryOnRestart_LCAttributesTypes
    )
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False


def setup_idrac_lc_attr(idrac, module):
    """
    Setup iDRAC Lifecycle attributes

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
        idrac.config_mgr._sysconfig.LifecycleController.LCAttributes.\
            CollectSystemInventoryOnRestart_LCAttributes = \
                TypeHelper.convert_to_enum(module.params['csior'],
                                           CollectSystemInventoryOnRestart_LCAttributesTypes)

        msg['changed'] = idrac.config_mgr._sysconfig.is_changed()

        if module.check_mode:
            # Since it is running in check mode, reject the changes
            idrac.config_mgr._sysconfig.reject()
        else:
            msg['msg'] = idrac.config_mgr.apply_changes(reboot=module.params['reboot'])

            if "Status" in msg['msg'] and msg['msg']['Status'] != "Success":
                msg['failed'] = True
                msg['changed'] = False

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

            # Network File Share
            share_name=dict(required=True, type='str'),
            share_user=dict(required=True, type='str'),
            share_pwd=dict(required=True, type='str', no_log=True),
            share_mnt=dict(required=True, type='path'),

            # Collect System Inventory on Restart (CSIOR)
            csior=dict(required=False, choices=['Enabled', 'Disabled'],
                       default='Enabled', type='str'),

            reboot=dict(required=False, default=False, type='bool')
        ),
        supports_check_mode=True)

    if not HAS_OMSDK:
        module.fail_json(msg="Dell EMC OpenManage Python SDK required for this module")

    # Connect to iDRAC
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    # Setup network share as local mount
    if not idrac_conn.setup_nw_share_mount():
        module.fail_json(msg="Failed to setup network share local mount point")

    msg, err = setup_idrac_lc_attr(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()
