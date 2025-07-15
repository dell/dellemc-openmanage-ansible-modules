#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.4
# Copyright (C) 2021-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
---
module: ome_application_alerts_syslog
short_description: Configure syslog forwarding settings on OpenManage Enterprise and OpenManage Enterprise Modular
description: This module allows to configure syslog forwarding settings on OpenManage Enterprise and OpenManage Enterprise Modular.
version_added: 4.3.0
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  syslog_servers:
    description: List of servers to forward syslog.
    type: list
    elements: dict
    suboptions:
      id:
        description: The ID of the syslog server.
        type: int
        choices: [1, 2, 3, 4]
        required: true
      enabled:
        description: Enable or disable syslog forwarding.
        type: bool
      destination_address:
        description:
          - The IP address, FQDN or hostname of the syslog server.
          - This is required if I(enabled) is C(true).
        type: str
      port_number:
        description: The UDP port number of the syslog server.
        type: int
requirements:
  - "python >= 3.9.6"
author:
  - Jagadeesh N V(@jagadeeshnv)
  - Mangirish Kenkare(@MangirishK)
notes:
  - Run this module from a system that has direct access to Dell OpenManage Enterprise or Dell OpenManage Enterprise Modular.
  - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Configure single server to forward syslog
  dellemc.openmanage.ome_application_alerts_syslog:
    hostname: 192.168.0.1
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    syslog_servers:
      - id: 1
        enabled: true
        destination_address: 192.168.0.2
        port_number: 514

- name: Configure multiple server to forward syslog
  dellemc.openmanage.ome_application_alerts_syslog:
    hostname: 192.168.0.1
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    syslog_servers:
      - id: 1
        port_number: 523
      - id: 2
        enabled: true
        destination_address: sysloghost1.lab.com
      - id: 3
        enabled: false
      - id: 4
        enabled: true
        destination_address: 192.168.0.4
        port_number: 514
"""

RETURN = """
---
msg:
  type: str
  description: Overall status of the syslog forwarding operation.
  returned: always
  sample: Successfully updated the syslog forwarding settings.
syslog_details:
  type: list
  description: Syslog forwarding settings list applied.
  returned: on success
  sample: [
    {
        "DestinationAddress": "192.168.10.43",
        "Enabled": false,
        "Id": 1,
        "PortNumber": 514
    },
    {
        "DestinationAddress": "192.168.10.46",
        "Enabled": true,
        "Id": 2,
        "PortNumber": 514
    },
    {
        "DestinationAddress": "192.168.10.44",
        "Enabled": true,
        "Id": 3,
        "PortNumber": 514
    },
    {
        "DestinationAddress": "192.168.10.42",
        "Enabled": true,
        "Id": 4,
        "PortNumber": 515
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
                "MessageId": "CAPP1108",
                "RelatedProperties": [],
                "Message": "Unable to update the Syslog settings because the request contains an invalid number of
                configurations. The request must contain no more than 4 configurations but contains 5.",
                "MessageArgs": [
                    "4",
                    "5"
                ],
                "Severity": "Warning",
                "Resolution": "Enter only the required number of configurations as identified in the message and
                retry the operation."
            }
        ]
    }
}
"""

import json
from ssl import SSLError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.common.dict_transformations import recursive_diff
from ansible.module_utils.common.dict_transformations import snake_dict_to_camel_dict

SYSLOG_GET = "AlertService/AlertDestinations/SyslogConfiguration"
SYSLOG_SET = "AlertService/AlertDestinations/Actions/AlertDestinations.ApplySyslogConfig"
SUCCESS_MSG = "Successfully updated the syslog forwarding settings."
DUP_ID_MSG = "Duplicate server IDs are provided."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
SYSLOG_UDP = 514


def validate_input(module):
    mparams = module.params
    syslog_list = mparams.get("syslog_servers")
    if not syslog_list:
        module.exit_json(msg=NO_CHANGES_MSG)
    syslog_dict = {}
    for sys in syslog_list:
        trim_sys = dict((k, v) for k, v in sys.items() if v is not None)
        syslog_dict[sys.get('id')] = snake_dict_to_camel_dict(trim_sys, capitalize_first=True)
    if len(syslog_dict) < len(syslog_list):
        module.exit_json(msg=DUP_ID_MSG, failed=True)
    return syslog_dict


def strip_substr_dict(odata_dict, chkstr='@odata.'):
    cp = odata_dict.copy()
    klist = cp.keys()
    for k in klist:
        if chkstr in str(k).lower():
            odata_dict.pop(k)
    if not odata_dict.get('PortNumber'):
        odata_dict['PortNumber'] = SYSLOG_UDP
    return odata_dict


def get_current_syslog(rest_obj):
    resp = rest_obj.invoke_request("GET", SYSLOG_GET)
    syslog_list = resp.json_data.get('value')
    return syslog_list


def compare_get_payload(module, current_list, input_config):
    payload_list = [strip_substr_dict(sys) for sys in current_list]  # preserving list order
    current_config = dict([(sys.get('Id'), sys) for sys in payload_list])
    diff = 0
    for k, v in current_config.items():
        i_dict = input_config.get(k)
        if i_dict:
            d = recursive_diff(i_dict, v)
            if d and d[0]:
                v.update(d[0])
                diff = diff + 1
        v.pop("Id", None)  # not mandatory
        payload_list[int(k) - 1] = v  # The order in list needs to be maintained
    if not diff:
        module.exit_json(msg=NO_CHANGES_MSG)
    if module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    return payload_list


def main():
    specs = {
        "syslog_servers":
            {"type": 'list', "elements": 'dict', "options":
                {"id": {"type": 'int', "choices": [1, 2, 3, 4], "required": True},
                 "enabled": {"type": 'bool'},
                 "destination_address": {"type": 'str'},
                 "port_number": {"type": 'int'}
                 },
             "required_one_of": [("enabled", "destination_address", "port_number")],
             "required_if": [("enabled", True, ("destination_address",))]
             }
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            input_config = validate_input(module)
            current_list = get_current_syslog(rest_obj)
            payload = compare_get_payload(module, current_list, input_config)
            resp = rest_obj.invoke_request("POST", SYSLOG_SET, data=payload, api_timeout=120)
            # POST Call taking average 50-60 seconds so api_timeout=120
            module.exit_json(msg=SUCCESS_MSG, syslog_details=resp.json_data, changed=True)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (
            IOError, ValueError, SSLError, TypeError, ConnectionError, AttributeError, IndexError, KeyError,
            OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
