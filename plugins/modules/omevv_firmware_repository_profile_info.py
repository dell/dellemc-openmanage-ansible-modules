#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.8.0
# Copyright (C) 2024-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

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
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv_utils.omevv_firmware_utils import OMEVVFirmwareProfile

SUCCESS_MSG = "Successfully retrieved the firmware repository profile information."
NO_PROFILE_MSG = "'{profile_name}' firmware repository profile name does not exist in OMEVV."
ERROR_CODES = ["12027"]


class OmevvFirmwareProfileInfo:

    def __init__(self, module, rest_obj) -> None:
        """
        Initializes a new instance of the class.
        Args:
            module (object): The module object.
            rest_obj (object): The REST object.
        Returns:
            None
        """
        self.module = module
        self.obj = rest_obj

    def perform_module_operation(self) -> dict:
        """
        Retrieves the firmware repository profile information.
        Returns:
            dict: A dictionary containing the message and the firmware repository profile information.
                - msg (str): The success message or the error message.
                - profile_info (list): The list of firmware repository profile information.
        """
        profile_name = self.module.params.get("name")
        self.omevv_utils_obj = OMEVVFirmwareProfile(self.obj)
        resp = self.omevv_utils_obj.get_firmware_repository_profile(profile_name)
        result = {'msg': SUCCESS_MSG, 'profile_info': resp}
        if profile_name and not resp:
            result['msg'] = NO_PROFILE_MSG.format(profile_name=profile_name)
        return result


def main():
    """
    Retrieves the firmware repository profile information.

    Returns:
        dict: A dictionary containing the message and the firmware repository profile information.
            - msg (str): The success message or the error message.
            - profile_info (list): The list of firmware repository profile information.

    Error Codes:
        - 12027: The specified vCenter UUID is not registered in OME.
    """
    argument_spec = {
        "name": {"type": 'str'}
    }
    module = OMEVVAnsibleModule(argument_spec=argument_spec,
                                supports_check_mode=True)
    try:
        with RestOMEVV(module.params) as rest_obj:
            omevv_obj = OmevvFirmwareProfileInfo(module, rest_obj)
            resp = omevv_obj.perform_module_operation()
            module.exit_json(msg=resp['msg'], profile_info=resp['profile_info'])
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
