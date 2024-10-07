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

DOCUMENTATION = r'''
---
module: omevv_vcenter_info
short_description: Retrieve all or specific vCenter information.
version_added: "9.8.0"
description:
  - This module retrieve all or specific vCenter information.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  vcenter_hostname:
    description:
      - vCenter IP address or hostname.
      - If I(vcenter_hostname) is provided, then module will retrieve only the specified vCenter details.
    type: str
requirements:
  - "python >= 3.9.6"
author:
  - "Lovepreet Singh (@singh-lovepreet1)"
notes:
  - This module supports C(check_mode).
  - This module supports IPv4 and IPv6 addresses.
'''

EXAMPLES = r'''
---
- name: Fetch all vCenter information
  dellemc.openmanage.omevv_vcenter_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "path/to/ca_file"

- name: Fetch specific vCenter information
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
  description: Status of the vCenter information retrieval operation.
  returned: always
  type: str
  sample: "Successfully fetched the vCenter information."
vcenter_info:
  description: Information about the vCenter.
  returned: success
  type: list
  elements: dict
  sample:
    [
        {
            "uuid": "77373c7e-d2b0-453b-9567-102484519bd1",
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
            "uuid": "77373c7e-d2b0-453b-9567-102484519bd2",
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
from ssl import SSLError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv import RestOMEVV, OMEVVAnsibleModule

BASE_URI = "/omevv/GatewayService/v1/Consoles"
SUCCESS_MSG = "Successfully fetched the vCenter information."
NO_VCENTER_MSG = "Unable to complete the operation because the '{vcenter_hostname}' is not a valid 'vcenter_hostname'."
FAILED_MSG = "Unable to fetch the vCenter information."


class OMEVVVCenterInfo:

    def __init__(self, module, rest_obj) -> None:
        self.module = module
        self.obj = rest_obj

    def get_all_vcenter_info(self) -> dict:
        resp = self.obj.invoke_request("GET", "/Consoles")
        vcenter_info = resp.json_data
        if resp.success:
            output_all = {'msg': SUCCESS_MSG, 'vcenter_info': vcenter_info, 'op': 'success'}
            return output_all
        self.module.exit_json(msg=FAILED_MSG, failed=True)

    def get_vcenter_info(self, result, vcenter_id) -> dict:
        output_not_found_or_empty = {'msg': NO_VCENTER_MSG.format(vcenter_hostname=vcenter_id),
                                     'vcenter_info': [], 'op': 'skipped'}
        if vcenter_id is not None or vcenter_id != "":
            for each_element in result.get('vcenter_info', []):
                if each_element.get('consoleAddress') == vcenter_id:
                    output_specific = {'msg': SUCCESS_MSG,
                                       'vcenter_info': [each_element], 'op': 'success'}
                    return output_specific
        return output_not_found_or_empty

    def perform_module_operation(self) -> None:
        result = self.get_all_vcenter_info()
        vcenter_id = self.module.params.get("vcenter_hostname")
        if vcenter_id:
            result = self.get_vcenter_info(result, vcenter_id)
        return result


def main():
    argument_spec = {
        "vcenter_hostname": {"type": 'str'}
    }
    module = OMEVVAnsibleModule(argument_spec=argument_spec,
                                supports_check_mode=True)
    try:
        with RestOMEVV(module.params) as rest_obj:
            omevv_obj = OMEVVVCenterInfo(module, rest_obj)
            resp = omevv_obj.perform_module_operation()
            if resp['op'] == 'success':
                module.exit_json(msg=resp['msg'], vcenter_info=resp['vcenter_info'])
            else:
                module.exit_json(msg=resp['msg'], skipped=True)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError,
            AttributeError, IndexError, KeyError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
