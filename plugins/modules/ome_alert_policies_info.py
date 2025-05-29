#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2023-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_alert_policies_info
short_description: Retrieves information of one or more OME alert policies.
version_added: "8.2.0"
description:
  - This module retrieves the information of alert policies for OpenManage Enterprise
    and OpenManage Enterprise Modular.
  - A list of information about a specific OME alert policy using the policy name.
  - A list of all the OME alert policies with their information when the policy name is not provided.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
    policy_name:
        description: Name of the policy.
        type: str
requirements:
    - "python >= 3.9.6"
author: "Abhishek Sinha(@ABHISHEK-SINHA10)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise
      or OpenManage Enterprise Modular.
    - This module supports both IPv4 and IPv6 addresses.
    - This module supports C(check_mode).
'''

EXAMPLES = """
---
- name: Retrieve information about all OME alert policies.
  dellemc.openmanage.ome_alert_policies_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"

- name: Retrieve information about a specific OME alert policy using the policy name.
  dellemc.openmanage.ome_alert_policies_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    policy_name: "Mobile Push Notification - Critical Alerts"
"""

RETURN = '''
---
msg:
  type: str
  description: Status of the alert policies info fetch operation.
  returned: always
  sample: "Successfully retrieved all the OME alert policies information."
policies:
  type: list
  description: Retrieve information about all the OME alert policies.
  returned: success
  sample: [
    {
        "Id": 10006,
        "Name": "Mobile Push Notification - Critical Alerts",
        "Description": "This policy is applicable to critical alerts. Associated actions will be taken when a critical alert is received.",
        "Enabled": true,
        "DefaultPolicy": true,
        "PolicyData": {
            "Catalogs": [],
            "Severities": [
                16
            ],
            "MessageIds": [],
            "Devices": [],
            "DeviceTypes": [],
            "Groups": [],
            "AllTargets": false,
            "Schedule": {
                "StartTime": null,
                "EndTime": null,
                "CronString": null,
                "Interval": false
            },
            "Actions": [
                {
                    "Id": 5,
                    "Name": "Mobile",
                    "ParameterDetails": [],
                    "TemplateId": 112
                }
            ],
            "UndiscoveredTargets": []
        },
        "State": true,
        "Visible": true,
        "Owner": null,
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
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import remove_key
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


ALERT_POLICY_URI = "AlertService/AlertPolicies"
MODULE_SUCCESS_MESSAGE_ALL = "Successfully retrieved all the OME alert policies information."
MODULE_SUCCESS_MESSAGE_SPECIFIC = "Successfully retrieved {0} OME alert policy information."
POLICY_NAME_NOT_FOUND_OR_EMPTY = "The OME alert policy name {0} provided does not exist or empty."


class OMEAlertPolicyInfo:

    def __init__(self) -> None:
        self.module = get_module_parameters()

    def get_all_alert_policy_info(self, rest_obj) -> dict:
        resp = rest_obj.invoke_request("GET", ALERT_POLICY_URI)
        value = resp.json_data["value"]
        output_all = {'msg': MODULE_SUCCESS_MESSAGE_ALL, 'value': remove_key(value)}
        return output_all

    def get_alert_policy_info(self, rest_obj) -> dict:
        policy_name = self.module.params.get("policy_name")
        if policy_name is not None:
            output_not_found_or_empty = {'msg': POLICY_NAME_NOT_FOUND_OR_EMPTY.format(policy_name),
                                         'value': []}
            if policy_name == "":
                return output_not_found_or_empty
            policies = self.get_all_alert_policy_info(rest_obj)
            for each_element in policies["value"]:
                if each_element["Name"] == policy_name:
                    output_specific = {'msg': MODULE_SUCCESS_MESSAGE_SPECIFIC.format(policy_name),
                                       'value': [each_element]}
                    return output_specific
            return output_not_found_or_empty
        return self.get_all_alert_policy_info(rest_obj)

    def perform_module_operation(self) -> None:
        try:
            with RestOME(self.module.params, req_session=True) as rest_obj:
                result = self.get_alert_policy_info(rest_obj)
                self.module.exit_json(msg=result['msg'], policies=result['value'])
        except HTTPError as err:
            self.module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
        except URLError as err:
            self.module.exit_json(msg=str(err), unreachable=True)
        except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
            self.module.exit_json(msg=str(err), failed=True)


def get_module_parameters() -> OmeAnsibleModule:
    specs = {
        "policy_name": {"type": 'str'}
    }

    module = OmeAnsibleModule(argument_spec=specs,
                              supports_check_mode=True)
    return module


def main():
    obj = OMEAlertPolicyInfo()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
