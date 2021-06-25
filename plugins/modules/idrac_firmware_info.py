#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.5.0
# Copyright (C) 2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_firmware_info
short_description: Get Firmware Inventory
version_added: "3.0.0"
description: Get Firmware Inventory.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options

requirements:
    - "omsdk"
    - "python >= 2.7.5"
author: "Rajeev Arakkal (@rajeevarakkal)"
notes:
    - Run this module from a system that has direct access to DellEMC iDRAC.
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Get Installed Firmware Inventory
  dellemc.openmanage.idrac_firmware_info:
      idrac_ip:   "192.168.0.1"
      idrac_user: "user_name"
      idrac_password:  "user_password"
"""

RETURN = r'''
---
msg:
  description: "Fetching the firmware inventory details."
  returned: always
  type: str
  sample: "Successfully fetched the firmware inventory details."
firmware_info:
  type: dict
  description: Details of the firmware.
  returned: success
  sample: {
            "Firmware": [{
                "BuildNumber": "0",
                "Classifications": "10",
                "ComponentID": "102573",
                "ComponentType": "FRMW",
                "DeviceID": null,
                "ElementName": "Power Supply.Slot.1",
                "FQDD": "PSU.Slot.1",
                "HashValue": null,
                "IdentityInfoType": "OrgID:ComponentType:ComponentID",
                "IdentityInfoValue": "DCIM:firmware:102573",
                "InstallationDate": "2018-11-22T03:58:23Z",
                "InstanceID": "DCIM:INSTALLED#0x15__PSU.Slot.1",
                "IsEntity": "true",
                "Key": "DCIM:INSTALLED#0x15__PSU.Slot.1",
                "MajorVersion": "0",
                "MinorVersion": "3",
                "RevisionNumber": "67",
                "RevisionString": null,
                "Status": "Installed",
                "SubDeviceID": null,
                "SubVendorID": null,
                "Updateable": "true",
                "VendorID": null,
                "VersionString": "00.3D.67",
                "impactsTPMmeasurements": "false"
            }]
  }
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
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
'''


import json
from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
try:
    from omsdk.sdkfile import LocalFile
    from omsdk.catalog.sdkupdatemgr import UpdateManager
    from omdrivers.helpers.iDRAC.UpdateHelper import UpdateHelper
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False


# Main
def main():
    module = AnsibleModule(
        argument_spec={
            "idrac_ip": {"required": True, "type": 'str'},
            "idrac_user": {"required": True, "type": 'str'},
            "idrac_password": {"required": True, "type": 'str', "aliases": ['idrac_pwd'], "no_log": True},
            "idrac_port": {"required": False, "default": 443, "type": 'int'},
        },
        supports_check_mode=True)

    try:
        with iDRACConnection(module.params) as idrac:
            msg = idrac.update_mgr.InstalledFirmware
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, SSLValidationError, IOError, ValueError, TypeError, ConnectionError) as e:
        module.fail_json(msg=str(e))

    module.exit_json(msg="Successfully fetched the firmware inventory details.",
                     firmware_info=msg)


if __name__ == '__main__':
    main()
