#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.8.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: omevv_firmware_repository_profile_info
short_description: Retrieve OMEVV firmware repository profile information.
version_added: "9.8.0"
description:
  - This module allows you to retrieve the OMEVV firmware repository profile information.
extends_documentation_fragment:
  - dellemc.openmanage.omevv_auth_options
options:
  name:
    description:
      - Name of the OMEVV firmware repository profile.
      - If I(name) is provided, the module retrieves only specified firmware repository profile information.
    type: str
requirements:
  - "python >= 3.9.6"
author:
  - "Lovepreet Singh (@singh-lovepreet1)"
attributes:
    check_mode:
        description: Runs task to validate without performing action on the target machine.
        support: full
notes:
  - This module supports IPv4 and IPv6 addresses.
"""


EXAMPLES = r"""
---
- name: Retrieve all firmware repository profile information.
  dellemc.openmanage.omevv_firmware_repository_profile_info:
    hostname: "192.168.0.1"
    vcenter_uuid: "xxxxxx"
    vcenter_username: "username"
    vcenter_password: "password"
    ca_path: "path/to/ca_file"

- name: Retrieve specific firmware repository profile information using profile name.
  dellemc.openmanage.omevv_firmware_repository_profile_info:
    hostname: "192.168.0.1"
    vcenter_uuid: "xxxxxx"
    vcenter_username: "username"
    vcenter_password: "password"
    ca_path: "path/to/ca_file"
    name: profile-1
"""

RETURN = r"""
---
msg:
  description: Status of the firmare repository profile information for the retrieve operation.
  returned: always
  type: str
  sample: "Successfully retrieved the firmware repository profile information."
profile_info:
  description: Information on the vCenter.
  returned: success
  type: list
  elements: dict
  sample:
    [
        {
            "id": 1000,
            "profileName": "Dell Default Catalog",
            "description": "Latest Firmware From Dell",
            "profileType": "Firmware",
            "sharePath": "https://downloads.dell.com//catalog/catalog.xml.gz",
            "fileName": "catalog.xml",
            "status": "Success",
            "factoryCreated": true,
            "factoryType": "Default",
            "catalogCreatedDate": "2024-08-27T01:58:10Z",
            "catalogLastChecked": "2024-09-09T19:30:16Z",
            "checkCertificate": null,
            "protocolType": "HTTPS",
            "createdBy": "OMEVV Default",
            "modifiedBy": null,
            "owner": "OMEVV"
        },
        {
            "id": 1001,
            "profileName": "Dell Default Catalog",
            "description": "Latest Firmware From Dell",
            "profileType": "Firmware",
            "sharePath": "https://downloads.dell.com//catalog/catalog.xml.gz",
            "fileName": "catalog.xml",
            "status": "Success",
            "factoryCreated": true,
            "factoryType": "Default",
            "catalogCreatedDate": "2024-08-27T01:58:10Z",
            "catalogLastChecked": "2024-09-09T19:30:16Z",
            "checkCertificate": null,
            "protocolType": "HTTPS",
            "createdBy": "OMEVV Default",
            "modifiedBy": null,
            "owner": "OMEVV"
        }
    ]
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
"""

import json
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv import RestOMEVV, OMEVVAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv_utils import OMEVVINFO

SUCCESS_MSG = "Successfully retrieved the firmware repository profile information."
NO_PROFILE_MSG = "Unable to complete the operation because the '{profile_name}' is not a valid 'profile_name'."
FAILED_MSG = "Unable to fetch the firmware repository profile information."
ERROR_CODES = ["11008", "12027"]


class OmevvFirmwareProfileInfo:

    def __init__(self, module, rest_obj) -> None:
        self.module = module
        self.obj = rest_obj

    def search_profile_name(self, profiles_data, profile_name):
        for profile in profiles_data:
            if profile.get('profileName') == profile_name:
                return profile
        return {}

    def get_profile_info(self, profiles_data, profile_name) -> dict:
        output_not_found_or_empty = {'msg': NO_PROFILE_MSG.format(profile_name=profile_name),
                                     'profile_info': [], 'op': 'skipped'}
        if profile_name is not None or profile_name != "":
            data = self.search_profile_name(profiles_data, profile_name)
            if data:
                output_specific = {'msg': SUCCESS_MSG,
                                   'profile_info': data, 'op': 'success'}
                return output_specific
        return output_not_found_or_empty

    def perform_module_operation(self) -> dict:
        self.omevv_utils_obj = OMEVVINFO(self.obj, self.module)
        resp = self.omevv_utils_obj.get_firmware_repository_profile()
        result = {'msg': FAILED_MSG, 'op': 'failed'}
        if resp.success:
            result = {'msg': SUCCESS_MSG, 'profile_info': resp.json_data, 'op': 'success'}
        profile_name = self.module.params.get("name")
        if profile_name is None or result['op'] == 'failed':
            return result
        result = self.get_profile_info(resp.json_data, profile_name)
        return result


def main():
    argument_spec = {
        "name": {"type": 'str'}
    }
    module = OMEVVAnsibleModule(argument_spec=argument_spec,
                                supports_check_mode=True)
    try:
        with RestOMEVV(module.params) as rest_obj:
            omevv_obj = OmevvFirmwareProfileInfo(module, rest_obj)
            resp = omevv_obj.perform_module_operation()
            if resp['op'] == 'success':
                module.exit_json(msg=resp['msg'], profile_info=resp['profile_info'])
            elif resp['op'] == 'skipped':
                module.exit_json(msg=resp['msg'], profile_info=resp['profile_info'], skipped=True)
            else:
                module.exit_json(msg=resp['msg'], failed=True)
    except HTTPError as err:
        error_info = json.load(err)
        code = error_info.get('errorCode')
        message = error_info.get('message')
        if code in ERROR_CODES:
            module.exit_json(msg=message, skipped=True)
        module.exit_json(msg=str(err), error_info=error_info, failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLValidationError, TypeError, ConnectionError,
            AttributeError, IndexError, KeyError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
