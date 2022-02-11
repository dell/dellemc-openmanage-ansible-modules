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
module: dellemc_get_firmware_inventory
short_description: Get Firmware Inventory
version_added: "1.0.0"
deprecated:
  removed_at_date: "2023-01-15"
  why: Replaced with M(dellemc.openmanage.idrac_firmware_info).
  alternative: Use M(dellemc.openmanage.idrac_firmware_info) instead.
  removed_from_collection: dellemc.openmanage
description: Get Firmware Inventory.
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
- name: Get Installed Firmware Inventory
  dellemc.openmanage.dellemc_get_firmware_inventory:
      idrac_ip:   "192.168.0.1"
      idrac_user: "user_name"
      idrac_password:  "user_password"
      ca_path: "/path/to/ca_cert.pem"
"""

RETURNS = """
ansible_facts:
    description: Displays components and their firmware versions. Also, list of the firmware
        dictionaries (one dictionary per firmware).
    returned: success
    type: complex
    sample: {
        [
            {
                "BuildNumber": "0",
                "Classifications": "10",
                "ComponentID": "101100",
                "ComponentType": "FRMW",
                "DeviceID": null,
                "ElementName": "Power Supply.Slot.1",
                "FQDD": "PSU.Slot.1",
                "IdentityInfoType": "OrgID:ComponentType:ComponentID",
                "IdentityInfoValue": "DCIM:firmware:101100",
                "InstallationDate": "2018-01-18T07:25:08Z",
                "InstanceID": "DCIM:INSTALLED#0x15__PSU.Slot.1",
                "IsEntity": "true",
                "Key": "DCIM:INSTALLED#0x15__PSU.Slot.1",
                "MajorVersion": "0",
                "MinorVersion": "1",
                "RevisionNumber": "7",
                "RevisionString": null,
                "Status": "Installed",
                "SubDeviceID": null,
                "SubVendorID": null,
                "Updateable": "true",
                "VendorID": null,
                "VersionString": "00.1D.7D",
                "impactsTPMmeasurements": "false"
            }
        ]
    }
"""


import traceback
from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection, idrac_auth_params
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
        argument_spec=idrac_auth_params,
        supports_check_mode=True)

    try:
        with iDRACConnection(module.params) as idrac:
            msg, err = run_get_firmware_inventory(idrac, module)
    except (ImportError, ValueError, RuntimeError) as e:
        module.fail_json(msg=str(e))

    if err:
        module.fail_json(**msg)
    module.exit_json(ansible_facts={idrac.ipaddr: {'Firmware Inventory': msg['msg']}})


if __name__ == '__main__':
    main()
