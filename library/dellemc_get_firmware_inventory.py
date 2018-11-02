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
module: dellemc_get_firmware_inventory
short_description: Get Firmware Inventory.
version_added: "2.3"
description: Get Firmware Inventory.
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
requirements:
    - "omsdk"
    - "python >= 2.7.5"
author: "Rajeev Arakkal (@rajeevarakkal)"

"""

EXAMPLES = """
---
- name: Get Installed Firmware Inventory
  dellemc_get_firmware_inventory:
      idrac_ip:   "xx.xx.xx.xx"
      idrac_user: "xxxx"
      idrac_pwd:  "xxxxxxxx"
"""

RETURN = """
dest:
    description: Displays components and their firmware versions. Also, list of the firmware
        dictionaries (one dictionary per firmware).
    returned: success
    type: string
"""


import traceback
from ansible.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
try:
    from omsdk.sdkfile import LocalFile
    from omsdk.catalog.sdkupdatemgr import UpdateManager
    from omdrivers.helpers.iDRAC.UpdateHelper import UpdateHelper
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False


def run_get_firmware_inventory(idrac, module):
    """
    Get Firmware Inventory
    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    msg = {}
    # msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    error = False

    try:
        # idrac.use_redfish = True
        msg['msg'] = idrac.update_mgr.InstalledFirmware
        if "Status" in msg['msg']:
            if msg['msg']['Status'] != "Success":
                msg['failed'] = True

    except Exception as err:
        error = True
        msg['msg'] = "Error: %s" % str(err)
        msg['exception'] = traceback.format_exc()
        msg['failed'] = True

    return msg, error


# Main
def main():
    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC Credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_pwd=dict(required=True, type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),
        ),

        supports_check_mode=False)

    if not HAS_OMSDK:
        module.fail_json(msg="Dell EMC OpenManage Python SDK required for this module")

    # Connect to iDRAC
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    # get software inventory
    msg, err = run_get_firmware_inventory(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(ansible_facts={idrac.ipaddr: {'Firmware Inventory': msg['msg']}})
    # module.exit_json(**msg)


if __name__ == '__main__':
    main()
