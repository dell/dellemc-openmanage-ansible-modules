#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.3.0
# Copyright (C) 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import get_all_data_with_pagination
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import remove_key
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
import json
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_alert_policies
short_description: Manage OME alert policies.
version_added: "8.3.0"
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
author: "Jagadeesh N V(@jagadeeshnv)"
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
  sample: []
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

POLICIES_URI = "AlertService/AlertPolicies"
REMOVE_URI = "AlertService/Actions/AlertService.RemoveAlertPolicies"
SUCCESS_MSG = "Successfully retrieved all the OME alert policies information."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_MSG = "Changes found to be applied."

# Get alert policies


def get_alert_policies(rest_obj, name_list):
    report = get_all_data_with_pagination(rest_obj, POLICIES_URI)
    all_policies = report.get("report_list", [])
    policies = []
    for policy in all_policies:
        if policy.get("Name") in name_list:
            policies.append(policy)
    # TODO take care of DefaultPolicy
    return policies


def remove_policy(module, rest_obj, policies):
    id_list = [x.get("Id")
               for x in policies if x.get("DefaultPolicy") is False]
    if len(id_list) != len(policies):
        module.exit_json(
            failed=True, msg="Default Policies cannot be deleted.")
    if module.check_mode:
        module.exit_json(msg=CHANGES_MSG)
    rest_obj.invoke_request("POST", REMOVE_URI, data={
                            "AlertPolicyIds": id_list})
    module.exit_json(changed=True, msg=SUCCESS_MSG)


def update_policy(module, rest_obj, policy):
    pass


def create_policy(module, rest_obj):
    pass


def main():
    specs = {
        "name": {'type': 'list', 'elements': 'str', 'required': True},
        "state": {'default': 'present', 'choices': ['present', 'absent'], 'type': 'str'},
        "enable": {'type': 'bool'},
        "new_name": {'type': 'str'},
        "description": {'type': 'str'},
        "device_service_tag": {'type': 'list', 'elements': 'str'},
        "device_group": {'type': 'list', 'elements': 'str'},
        "specific_undiscovered_devices": {'type': 'list', 'elements': 'str'},
        "any_undiscovered_devices": {'type': 'bool'},
        "category": {'type': 'list', 'elements': 'dict',
                     'options': {'catalog_name': {'type': 'str', 'required': True},
                                 'catalog_category': {'type': 'list', 'elements': 'dict',
                                                      'options': {'category_name': {'type': 'str'},
                                                                  'sub_category_names': {'type': 'list', 'elements': 'str'}
                                                                  },
                                                      }
                                 }
                     },
        "message_ids": {'type': 'list', 'elements': 'str'},
        "message_file": {'type': 'path'},
        "date_and_time": {'type': 'dict',
                          'options': {'date_from': {'type': 'str'},
                                      'date_to': {'type': 'str'},
                                      'time_from': {'type': 'str'},
                                      'time_to': {'type': 'str'},
                                      'days': {'type': 'list', 'elements': 'str',
                                               'choices': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']},
                                      'time_interval': {'type': 'bool'}
                                      },
                          },
        "severity": {'type': 'list', 'elements': 'str', 'choices': ['info', 'normal', 'warning', 'critical', 'unknown', 'all']},
        "actions": {'type': 'list', 'elements': 'dict',
                    'options': {'action_name': {'type': 'str', 'choices': ['email', 'trap', 'syslog', 'ignore', 'power_control', 'sms', 'remote_command', 'mobile']},
                                'parameters': {'type': 'list', 'elements': 'dict',
                                               'options': {'name': {'type': 'str'},
                                                           'value': {'type': 'str'}}
                                               }
                                }
                    }
    }
    specs.update(ome_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        required_if=[],
        required_one_of=[],
        mutually_exclusive=[('device_service_tag', 'device_group', 'any_undiscovered_devices', 'specific_undiscovered_devices'),
                            ('message_ids', 'message_file', 'category')],
        supports_check_mode=True)
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            state = module.params.get('state')
            name_list = module.params.get('name')
            policies = get_alert_policies(rest_obj, name_list)
            if state == 'absent':
                if policies:
                    remove_policy(module, rest_obj, policies)
                else:
                    module.exit_json(msg=NO_CHANGES_MSG)
            else:
                if len(name_list) > 1:
                    module.exit_json(
                        failed=True, msg="More than one policy name provided.")
                if policies:
                    update_policy(module, rest_obj, policies[0])
                else:
                    create_policy(module, rest_obj)
                module.exit_json(msg=SUCCESS_MSG)
    except HTTPError as err:
        module.exit_json(failed=True, msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(failed=True, msg=str(err))


if __name__ == '__main__':
    main()
