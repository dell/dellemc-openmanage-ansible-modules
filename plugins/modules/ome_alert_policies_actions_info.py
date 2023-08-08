#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.2.0
# Copyright (C) 2020-2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_alert_policies_actions_info
short_description: Get information on actions of alert policies for OpenManage Enterprise.
version_added: "8.2.0"
description: This module retrieves the information on actions of alert policies for OpenManage Enterprise.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
requirements:
  - "python >= 3.9.6"
author:
  - "Kritika Bhateja (@Kritika-Bhateja-03)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
    - This module supports both IPv4 and IPv6 address.
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
  type: str
  description: Error description in case of error.
  returned: on error
  sample: "HTTP Error 501: 501"
'''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import remove_key
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError

ACTIONS_URI = "AlertService/AlertActionTemplates"


def main():
    """ function to retrieve the information on actions of alert policies """
    specs = {}
    specs.update(ome_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        supports_check_mode=True)
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            resp = rest_obj.invoke_request('GET', ACTIONS_URI)
            actions = remove_key(resp.json_data)
            module.exit_json(actions=actions["value"])
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
