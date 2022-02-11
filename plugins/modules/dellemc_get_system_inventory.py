#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.0.1
# Copyright (C) 2018-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: dellemc_get_system_inventory
short_description: Get the PowerEdge Server System Inventory
version_added: "1.0.0"
deprecated:
  removed_at_date: "2023-01-15"
  why: Replaced with M(dellemc.openmanage.idrac_system_info).
  alternative: Use M(dellemc.openmanage.idrac_system_info) instead.
  removed_from_collection: dellemc.openmanage
description:
    - Get the PowerEdge Server System Inventory.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options

requirements:
    - "omsdk >= 1.2.488"
    - "python >= 3.8.6"
author: "Rajeev Arakkal (@rajeevarakkal)"
notes:
    - Run this module from a system that has direct access to DellEMC iDRAC.
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Get System Inventory
  dellemc.openmanage.dellemc_get_system_inventory:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
"""

RETURNS = """
ansible_facts:
    description: Displays the Dell EMC PowerEdge Server System Inventory.
    returned: success
    type: complex
    sample: {
       "SystemInventory": {
            "BIOS": [
            {
                "BIOSReleaseDate": "10/19/2017",
                "FQDD": "BIOS.Setup.1-1",
                "InstanceID": "DCIM:INSTALLED#741__BIOS.Setup.00",
                "Key": "DCIM:INSTALLED#741__BIOS.Setup.00",
                "SMBIOSPresent": "True",
                "VersionString": "1.2.11"
            }
        ],
        "CPU": [
            {
                "CPUFamily": "Intel(R) Xeon(TM)",
                "Characteristics": "64-bit capable",
                "CurrentClockSpeed": "2.3 GHz",
                "DeviceDescription": "CPU 1",
                "ExecuteDisabledCapable": "Yes",
            }
        ]
    }
}
msg:
  description: Details of the Error occurred.
  returned: on error
  type: dict
  sample: {
    "error": {
      "code": "Base.1.0.GeneralError",
      "message": "A general error has occurred. See ExtendedInfo for more information.",
      "@Message.ExtendedInfo": [
        {
          "MessageId": "GEN1234",
          "RelatedProperties": [],
          "Message": "Unable to process the request because an error occurred.",
          "MessageArgs": [],
          "Severity": "Critical",
          "Resolution": "Retry the operation. If the issue persists, contact your system administrator."
        }
      ]
    }
  }
"""


from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection, idrac_auth_params
from ansible.module_utils.basic import AnsibleModule


# Get System Inventory
def run_get_system_inventory(idrac, module):
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    err = False

    try:
        # idrac.use_redfish = True
        idrac.get_entityjson()
        msg['msg'] = idrac.get_json_device()
    except Exception as e:
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True
    return msg, err


# Main
def main():
    module = AnsibleModule(
        argument_spec=idrac_auth_params,
        supports_check_mode=True)

    try:
        with iDRACConnection(module.params) as idrac:
            msg, err = run_get_system_inventory(idrac, module)
    except (ImportError, ValueError, RuntimeError) as e:
        module.fail_json(msg=str(e))

    if err:
        module.fail_json(**msg)
    module.exit_json(ansible_facts={idrac.ipaddr: {'SystemInventory': msg['msg']}})


if __name__ == '__main__':
    main()
