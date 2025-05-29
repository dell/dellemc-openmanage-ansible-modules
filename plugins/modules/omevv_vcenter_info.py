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

DOCUMENTATION = r'''
---
module: omevv_vcenter_info
short_description: Retrieve all or specific OpenManage Enterprise vCenter information.
version_added: "9.8.0"
description:
  - This module allows you to retrieve all or specific vCenter information from OpenManage Enterprise.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  vcenter_hostname:
    description:
      - vCenter IP address or hostname.
      - If I(vcenter_hostname) is provided, the module retrieves only specified vCenter information.
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
'''


EXAMPLES = r'''
---
- name: Retrieve all vCenter information.
  dellemc.openmanage.omevv_vcenter_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "path/to/ca_file"

- name: Retrieve specific vCenter information.
  dellemc.openmanage.omevv_vcenter_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "path/to/ca_file"
    vcenter_hostname: xx.xx.xx.xx
'''

RETURN = r'''
---
msg:
  description: Status of the vCenter information for the retrieve operation.
  returned: always
  type: str
  sample: "Successfully retrieved the vCenter information."
vcenter_info:
  description: Information on the vCenter.
  returned: success
  type: list
  elements: dict
  sample:
    [
        {
            "uuid": "77373c7e-d2b0-453b-9888-102499919bd1",
            "consoleAddress": vcenter_ip_or_hostname,
            "description": "vCenter 8.0",
            "registeredExtensions": [
                "PHM",
                "WEBCLIENT",
                "PHA",
                "VLCM"
            ]
        },
        {
            "uuid": "77373c7e-d2b0-453b-9888-102499919bd2",
            "consoleAddress": vcenter_ip_or_hostname,
            "description": "vCenter 8.1",
            "registeredExtensions": [
                "PHM",
                "WEBCLIENT",
                "PHA",
                "VLCM"
            ]
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
'''

import json
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv import RestOMEVV
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv_utils.omevv_info_utils import OMEVVInfo
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import OmeAnsibleModule

SUCCESS_MSG = "Successfully retrieved the vCenter information."
NO_VCENTER_MSG = "'{vcenter_hostname}' vCenter is not registered in OME."


class OMEVVVCenterInfo:

    def __init__(self, module, rest_obj) -> None:
        """
        Initializes a new instance of the class.
        Args:
            module (Module): The module object.
            rest_obj (object): The REST object.
        Returns:
            None
        """
        self.module = module
        self.obj = rest_obj

    def perform_module_operation(self) -> dict:
        """
        Perform the module operation to retrieve the vCenter information.
        Returns:
            dict: A dictionary containing the message and the vCenter information.
                - msg (str): The success message or the error message.
                - vcenter_info (list): The list of vCenter information.
        """
        vcenter_id = self.module.params.get("vcenter_hostname")
        self.omevv_utils_obj = OMEVVInfo(self.obj)
        resp = self.omevv_utils_obj.get_vcenter_info(vcenter_id)
        result = {'msg': SUCCESS_MSG, 'vcenter_info': resp}
        if vcenter_id and not resp:
            result['msg'] = NO_VCENTER_MSG.format(vcenter_hostname=vcenter_id)
        return result


def main():
    argument_spec = {
        "vcenter_hostname": {"type": 'str'}
    }
    module = OmeAnsibleModule(argument_spec=argument_spec,
                              supports_check_mode=True)
    try:
        with RestOMEVV(module.params) as rest_obj:
            rest_obj.username = module.params.get("username")
            rest_obj.password = module.params.get("password")
            omevv_obj = OMEVVVCenterInfo(module, rest_obj)
            resp = omevv_obj.perform_module_operation()
            module.exit_json(msg=resp['msg'], vcenter_info=resp['vcenter_info'])
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLValidationError, TypeError, ConnectionError,
            AttributeError, IndexError, KeyError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
