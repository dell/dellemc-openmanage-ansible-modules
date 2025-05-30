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
module: ome_alert_policies_actions_info
short_description: Get information on actions of alert policies.
version_added: "8.2.0"
description:
  - This module retrieves the information on actions of alert policies for OpenManage Enterprise
    and OpenManage Enterprise Modular.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
requirements:
  - "python >= 3.9.6"
author:
  - "Kritika Bhateja (@Kritika-Bhateja-03)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise
      or OpenManage Enterprise Modular.
    - This module supports both IPv4 and IPv6 addresses.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Get action details of all alert policies.
  dellemc.openmanage.ome_alert_policies_actions_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
'''

RETURN = r'''
---
actions:
  type: list
  description: Returns the alert policies action information collected from the Device.
  returned: success
  sample: [
  {
  "Name": "Email",
  "Description": "Email",
  "Disabled": false,
  "ParameterDetails": [
    {
      "Id": 1,
      "Name": "subject",
      "Value": "Device Name: $name,  Device IP Address: $ip,  Severity: $severity",
      "Type": "string",
      "TemplateParameterTypeDetails": [
        {
          "Name": "maxLength",
          "Value": "255"
        }
      ]
    },
    {
      "Id": 2,
      "Name": "to",
      "Value": "",
      "Type": "string",
      "TemplateParameterTypeDetails": [
        {
          "Name": "maxLength",
          "Value": "255"
        }
      ]
    },
    {
      "Id": 3,
      "Name": "from",
      "Value": "admin1@dell.com",
      "Type": "string",
      "TemplateParameterTypeDetails": [
        {
          "Name": "maxLength",
          "Value": "255"
        }
      ]
    },
    {
      "Id": 4,
      "Name": "message",
      "Value": "Event occurred for Device Name: $name,
       Device IP Address: $ip, Service Tag: $identifier, UTC Time: $time, Severity: $severity, Message ID: $messageId, $message",
      "Type": "string",
      "TemplateParameterTypeDetails": [
        {
          "Name": "maxLength",
          "Value": "255"
        }
      ]
    },
    {
      "Id": 60,
      "Name": "Trap",
      "Description": "Trap",
      "Disabled": false,
      "ParameterDetails": [
        {
          "Id": 1,
          "Name": "localhost:162",
          "Value": "true",
          "Type": "boolean",
          "TemplateParameterTypeDetails": []
        }
      ]
    },
    {
      "Id": 90,
      "Name": "Syslog",
      "Description": "Syslog",
      "Disabled": false,
      "ParameterDetails": [
        {
          "Id": 1,
          "Name": "localhost.scomdev.com:555",
          "Value": "true",
          "Type": "boolean",
          "TemplateParameterTypeDetails": []
        },
        {
          "Id": 2,
          "Name": "localhost.scomdev.com:555",
          "Value": "true",
          "Type": "boolean",
          "TemplateParameterTypeDetails": []
        }
      ]
    },
    {
      "Id": 100,
      "Name": "Ignore",
      "Description": "Ignore",
      "Disabled": false,
      "ParameterDetails": []
    },
    {
      "Id": 70,
      "Name": "SMS",
      "Description": "SMS",
      "Disabled": false,
      "ParameterDetails": [
        {
          "Id": 1,
          "Name": "to",
          "Value": "",
          "Type": "string",
          "TemplateParameterTypeDetails": [
            {
              "Name": "maxLength",
              "Value": "255"
            }
          ]
        }
      ]
    },
    {
      "Id": 110,
      "Name": "PowerControl",
      "Description": "Power Control Action Template",
      "Disabled": false,
      "ParameterDetails": [
        {
          "Id": 1,
          "Name": "powercontrolaction",
          "Value": "poweroff",
          "Type": "singleSelect",
          "TemplateParameterTypeDetails": [
            {
              "Name": "option",
              "Value": "powercycle"
            },
            {
              "Name": "option",
              "Value": "poweroff"
            },
            {
              "Name": "option",
              "Value": "poweron"
            },
            {
              "Name": "option",
              "Value": "gracefulshutdown"
            }
          ]
        }
      ]
    },
    {
      "Id": 111,
      "Name": "RemoteCommand",
      "Description": "RemoteCommand",
      "Disabled": true,
      "ParameterDetails": [
        {
          "Id": 1,
          "Name": "remotecommandaction",
          "Value": null,
          "Type": "singleSelect",
          "TemplateParameterTypeDetails": []
        }
      ]
    },
    {
      "Id": 112,
      "Name": "Mobile",
      "Description": "Mobile",
      "Disabled": false,
      "ParameterDetails": []
    }
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
msg:
  description: Status of the alert policies actions fetch operation.
  returned: always
  type: str
  sample: Successfully retrieved alert policies actions information.
'''

import json
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import remove_key
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import get_all_data_with_pagination

ACTIONS_URI = "AlertService/AlertActionTemplates"
SUCCESSFUL_MSG = "Successfully retrieved alert policies actions information."
EMPTY_ALERT_POLICY_ACTION_MSG = "No alert policies action information were found."


def main():
    """ function to retrieve the information on actions of alert policies """
    specs = {}
    module = OmeAnsibleModule(
        argument_spec=specs,
        supports_check_mode=True)
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            actions_info = get_all_data_with_pagination(rest_obj, ACTIONS_URI)
            if not actions_info.get("report_list", []):
                module.exit_json(msg=EMPTY_ALERT_POLICY_ACTION_MSG, actions=[])
            actions = remove_key(actions_info['report_list'])
            module.exit_json(msg=SUCCESSFUL_MSG, actions=actions)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
