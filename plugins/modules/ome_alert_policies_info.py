#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.2.0
# Copyright (C) 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_alert_policies_info
short_description: Retrieves alert policy using policy_name.
version_added: "8.2.0"
description: Retrieves alert policy using policy_name.
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
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
    - This module supports both IPv4 and IPv6 address for *hostname*.
'''

EXAMPLES = """
---
- name: Retrieve information about all ome_alert_policies
  dellemc.openmanage.ome_alert_policies_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"

- name: Retrieve information about specific alert policy using policy name
  dellemc.openmanage.ome_alert_policies_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    policy_name: "Mobile Push Notification - Critical Alerts"
"""

RETURN = '''
---
policies:
  type: list
  description: Retrieve information of the OME alert policies.
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
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import remove_key
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


ALERT_POLICY_URI = "AlertService/AlertPolicies"


class OMEAlertPolicyInfo(object):

    def __init__(self) -> None:
        self.result = []
        self.module = get_module_parameters()

    def get_alert_policy_info(self, rest_obj) -> list:
        resp = rest_obj.invoke_request("GET", ALERT_POLICY_URI)
        value = resp.json_data["value"]

        if policy_name := self.module.params.get("policy_name"):
            for each_dict in value:
                if each_dict["Name"] == policy_name:
                    value = [each_dict]
                    break
        return value

    def perform_module_operation(self) -> None:
        try:
            with RestOME(self.module.params, req_session=True) as rest_obj:
                resp = self.get_alert_policy_info(rest_obj)
                self.result = remove_key(resp)
                self.module.exit_json(policies=self.result)
        except HTTPError as err:
            self.module.fail_json(error_info=json.load(err))
        except URLError as err:
            self.module.exit_json(error_info=json.load(err), unreachable=True)
        except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
            self.module.fail_json(json.load(err))


def get_module_parameters():
    specs = {
        "policy_name": {"type": 'str'}
    }
    specs.update(ome_auth_params)
    module = AnsibleModule(argument_spec=specs,
                           supports_check_mode=True)
    return module


def main():
    obj = OMEAlertPolicyInfo()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
