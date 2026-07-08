#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.9.0
# Copyright (C) 2026 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: idrac_storage_info
short_description: Get the storage controller, physical disk, and virtual disk information
version_added: "9.9.0"
description:
  - This module allows you to query storage controllers, physical disks, and virtual disks on iDRAC.
  - Returns merged Redfish and Dell OEM attributes for the requested resource type.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_x_auth_options
options:
  resource_type:
    type: str
    required: true
    description:
      - C(controller), returns details of all storage controllers.
      - C(physical_disk), returns details of all physical disks attached to the specified I(controller_id).
      - C(virtual_disk), returns details of all virtual disks on the specified I(controller_id).
    choices: ['controller', 'physical_disk', 'virtual_disk']
  controller_id:
    type: str
    description:
      - Fully Qualified Device Descriptor (FQDD) of the storage controller, for example 'RAID.Integrated.1-1'.
      - This is required when I(resource_type) is C(physical_disk) or C(virtual_disk).

requirements:
  - "python >= 3.9.6"
author:
  - "Dell OpenManage Ansible Team"
notes:
    - Run this module from a system that has direct access to Integrated Dell Remote Access Controller.
    - This module supports both IPv4 and IPv6 address for I(idrac_ip).
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Get all storage controllers
  dellemc.openmanage.idrac_storage_info:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    resource_type: "controller"

- name: Get all physical disks for a controller
  dellemc.openmanage.idrac_storage_info:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    resource_type: "physical_disk"
    controller_id: "RAID.Slot.1-1"

- name: Get all virtual disks for a controller
  dellemc.openmanage.idrac_storage_info:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    resource_type: "virtual_disk"
    controller_id: "RAID.Slot.1-1"
'''

RETURN = r'''
---
msg:
  type: str
  description: Overall status of the storage information query operation.
  returned: always
  sample: "Successfully fetched the storage information."
storage_info:
  type: dict
  description: Details of the requested storage resource(s).
  returned: success
  sample:
    {
      "resource_count": 1,
      "resources": [
        {
          "Id": "RAID.Slot.1-1",
          "Model": "PERC H755",
          "FirmwareVersion": "25.5.9.0001",
          "Status": {"Health": "OK"}
        }
      ]
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
from urllib.error import HTTPError, URLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, IdracAnsibleModule
from ansible.module_utils.urls import ConnectionError, SSLValidationError

CONTROLLER_ID_REQUIRED_MSG = "controller_id is required when resource_type is '{resource_type}'."
SUCCESS_MSG = "Successfully fetched the storage information."


class StorageInfo:
    def __init__(self, idrac, module):
        self.idrac = idrac
        self.module = module

    def validate_params(self):
        resource_type = self.module.params.get("resource_type")
        controller_id = self.module.params.get("controller_id")
        if resource_type in ("physical_disk", "virtual_disk") and not controller_id:
            self.module.exit_json(
                msg=CONTROLLER_ID_REQUIRED_MSG.format(resource_type=resource_type), failed=True)


def main():
    specs = {
        "resource_type": {"type": "str", "required": True,
                           "choices": ["controller", "physical_disk", "virtual_disk"]},
        "controller_id": {"type": "str"},
    }
    module = IdracAnsibleModule(
        argument_spec=specs,
        supports_check_mode=True)
    try:
        with iDRACRedfishAPI(module.params) as idrac:
            storage_info_obj = StorageInfo(idrac, module)
            storage_info_obj.validate_params()
            storage_info = {"resource_count": 0, "resources": []}
        module.exit_json(msg=SUCCESS_MSG, storage_info=storage_info)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
