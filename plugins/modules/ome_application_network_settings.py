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

DOCUMENTATION = r'''
---
module: ome_application_network_settings
short_description: This module allows you to configure the session inactivity timeout settings
version_added: "4.4.0"
description:
  - This module allows you to configure the session inactivity timeout settings on OpenManage Enterprise
    and OpenManage Enterprise Modular.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  session_inactivity_timeout:
    description: Session inactivity timeout settings.
    type: dict
    suboptions:
      enable_universal_timeout:
        description:
          - Enable or disable the universal inactivity timeout.
        type: bool
      universal_timeout:
        description:
          - Duration of inactivity in minutes after which all sessions end.
          - This is applicable when I(enable_universal_timeout) is C(true).
          - This is mutually exclusive with I(api_timeout), I(gui_timeout), I(ssh_timeout) and I(serial_timeout).
        type: float
      api_timeout:
        description:
          - Duration of inactivity in minutes after which the API session ends.
          - This is mutually exclusive with I(universal_timeout).
        type: float
      api_sessions:
        description:
          - The maximum number of API sessions to be allowed.
        type: int
      gui_timeout:
        description:
          - Duration of inactivity in minutes after which the web interface of
            Graphical User Interface (GUI) session ends.
          - This is mutually exclusive with I(universal_timeout).
        type: float
      gui_sessions:
        description:
          - The maximum number of GUI sessions to be allowed.
        type: int
      ssh_timeout:
        description:
          - Duration of inactivity in minutes after which the SSH session ends.
          - This is applicable only for OpenManage Enterprise Modular.
          - This is mutually exclusive with I(universal_timeout).
        type: float
      ssh_sessions:
        description:
          - The maximum number of SSH sessions to be allowed.
          - This is applicable to OME-M only.
        type: int
      serial_timeout:
        description:
          - Duration of inactivity in minutes after which the serial console session ends.
          - This is applicable only for OpenManage Enterprise Modular.
          - This is mutually exclusive with I(universal_timeout).
        type: float
      serial_sessions:
        description:
          - The maximum number of serial console sessions to be allowed.
          - This is applicable only for OpenManage Enterprise Modular.
        type: int
requirements:
    - "python >= 3.9.6"
notes:
  - Run this module from a system that has direct access to Dell OpenManage Enterprise
    or OpenManage Enterprise Modular.
  - To configure other network settings such as network address, web server, and so on, refer to the respective
    OpenManage Enterprise application network setting modules.
  - This module supports C(check_mode).
author:
  - Sachin Apagundi(@sachin-apa)
  - Sapana Gupta (@sapana05)
'''

EXAMPLES = """
---
- name: Configure universal inactivity timeout
  ome_application_network_settings:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    session_inactivity_timeout:
      enable_universal_timeout: true
      universal_timeout: 30
      api_sessions: 90
      gui_sessions: 5
      ssh_sessions: 2
      serial_sessions: 1

- name: Configure API and GUI timeout and sessions
  ome_application_network_settings:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    session_inactivity_timeout:
      api_timeout: 20
      api_sessions: 100
      gui_timeout: 25
      gui_sessions: 5

- name: Configure timeout and sessions for all parameters
  ome_application_network_settings:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    session_inactivity_timeout:
      api_timeout: 20
      api_sessions: 100
      gui_timeout: 15
      gui_sessions: 5
      ssh_timeout: 30
      ssh_sessions: 2
      serial_timeout: 35
      serial_sessions: 1

- name: Disable universal timeout and configure timeout and sessions for other parameters
  ome_application_network_settings:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    session_inactivity_timeout:
      enable_universal_timeout: false
      api_timeout: 20
      api_sessions: 100
      gui_timeout: 15
      gui_sessions: 5
      ssh_timeout: 30
      ssh_sessions: 2
      serial_timeout: 35
      serial_sessions: 1
"""

RETURN = """
---
msg:
  type: str
  description: Overall status of the Session timeout settings.
  returned: always
  sample: "Successfully updated the session timeout settings."
session_inactivity_setting:
  type: dict
  description: Returned when session inactivity timeout settings are updated successfully.
  returned: success
  sample: [
    {
        "SessionType": "API",
        "MaxSessions": 32,
        "SessionTimeout": 99600,
        "MinSessionTimeout": 60000,
        "MaxSessionTimeout": 86400000,
        "MinSessionsAllowed": 1,
        "MaxSessionsAllowed": 100,
        "MaxSessionsConfigurable": true,
        "SessionTimeoutConfigurable": true
    },
    {
        "SessionType": "GUI",
        "MaxSessions": 6,
        "SessionTimeout": 99600,
        "MinSessionTimeout": 60000,
        "MaxSessionTimeout": 7200000,
        "MinSessionsAllowed": 1,
        "MaxSessionsAllowed": 6,
        "MaxSessionsConfigurable": true,
        "SessionTimeoutConfigurable": true
    },
    {
        "SessionType": "SSH",
        "MaxSessions": 4,
        "SessionTimeout": 99600,
        "MinSessionTimeout": 60000,
        "MaxSessionTimeout": 10800000,
        "MinSessionsAllowed": 1,
        "MaxSessionsAllowed": 4,
        "MaxSessionsConfigurable": true,
        "SessionTimeoutConfigurable": true
    },
    {
        "SessionType": "Serial",
        "MaxSessions": 1,
        "SessionTimeout": 99600,
        "MinSessionTimeout": 60000,
        "MaxSessionTimeout": 86400000,
        "MinSessionsAllowed": 1,
        "MaxSessionsAllowed": 1,
        "MaxSessionsConfigurable": false,
        "SessionTimeoutConfigurable": true
    },
    {
        "SessionType": "UniversalTimeout",
        "MaxSessions": 0,
        "SessionTimeout": -1,
        "MinSessionTimeout": -1,
        "MaxSessionTimeout": 86400000,
        "MinSessionsAllowed": 0,
        "MaxSessionsAllowed": 0,
        "MaxSessionsConfigurable": false,
        "SessionTimeoutConfigurable": true
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
                "MessageId": "CUSR1233",
                "RelatedProperties": [],
                "Message": "The number of allowed concurrent sessions for API must be between 1 and 100 sessions.",
                "MessageArgs": [
                    "API",
                    "1",
                    "100"
                ],
                "Severity": "Critical",
                "Resolution": "Enter values in the correct range and retry the operation."
            }
        ]
    }
  }
"""

from ssl import SSLError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule

SUCCESS_MSG = "Successfully updated the session timeout settings."
SESSION_INACTIVITY_GET = "SessionService/SessionConfiguration"
SESSION_INACTIVITY_POST = "SessionService/Actions/SessionService.SessionConfigurationUpdate"
NO_CHANGES = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
session_type_map = {
    "UniversalTimeout": {"SessionTimeout": "universal_timeout", "MaxSessions": None},
    "API": {"SessionTimeout": "api_timeout", "MaxSessions": "api_sessions"},
    "GUI": {"SessionTimeout": "gui_timeout", "MaxSessions": "gui_sessions"},
    "SSH": {"SessionTimeout": "ssh_timeout", "MaxSessions": "ssh_sessions"},
    "Serial": {"SessionTimeout": "serial_timeout", "MaxSessions": "serial_sessions"}
}


def fetch_session_inactivity_settings(rest_obj):
    final_resp = rest_obj.invoke_request("GET", SESSION_INACTIVITY_GET)
    ret_data = final_resp.json_data.get('value')
    return ret_data


def update_session_inactivity_settings(rest_obj, payload):
    final_resp = rest_obj.invoke_request("POST", SESSION_INACTIVITY_POST, data=payload)
    return final_resp


def update_payload(module, curr_payload):
    diff = 0
    sit_param = module.params.get("session_inactivity_timeout").copy()
    eut = sit_param.get("enable_universal_timeout")
    eut_enabled = is_universal_timeout_enabled(curr_payload)
    if eut is False:
        sit_param["universal_timeout"] = -1  # to disable universal timeout set value to -1
    for up in curr_payload:
        stm = session_type_map.get(up.get("SessionType"), None)
        if stm and not ((up.get("SessionType") == "UniversalTimeout") and (eut is None)):
            sess_time = get_value(sit_param, up, stm.get("SessionTimeout", None), "SessionTimeout")
            if sess_time != up.get("SessionTimeout") and ((not eut_enabled) or eut is not None):
                diff += 1
                up["SessionTimeout"] = sess_time
            max_sess = get_value(sit_param, up, stm.get("MaxSessions", None), "MaxSessions")
            if max_sess != up.get("MaxSessions"):
                diff += 1
                up["MaxSessions"] = max_sess
    return curr_payload, diff


def is_universal_timeout_enabled(payload):
    u_sess_timeout = -1
    for up in payload:
        if up.get("SessionType") == "UniversalTimeout":
            u_sess_timeout = up.get("SessionTimeout")
            break
    return u_sess_timeout > 0


def get_value(input_module, resp, mod_key, attr_key):
    ret_value = input_module.get(mod_key)
    if ret_value is None:
        ret_value = resp.get(attr_key)
    elif attr_key == "SessionTimeout" and ret_value != -1:
        ret_value = ret_value * 60000
    return ret_value


def process_check_mode(module, diff):
    if not diff:
        module.exit_json(msg=NO_CHANGES)
    elif module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)


def main():
    session_inactivity_options = {
        "enable_universal_timeout": {"type": "bool", "required": False},
        "universal_timeout": {"type": "float", "required": False},
        "api_timeout": {"type": "float", "required": False},
        "api_sessions": {"type": "int", "required": False},
        "gui_timeout": {"type": "float", "required": False},
        "gui_sessions": {"type": "int", "required": False},
        "ssh_timeout": {"type": "float", "required": False},
        "ssh_sessions": {"type": "int", "required": False},
        "serial_timeout": {"type": "float", "required": False},
        "serial_sessions": {"type": "int", "required": False},
    }
    specs = {
        "session_inactivity_timeout": {
            "required": False,
            "type": "dict",
            "options": session_inactivity_options,
            "mutually_exclusive": [
                ['universal_timeout', 'api_timeout'],
                ['universal_timeout', 'gui_timeout'],
                ['universal_timeout', 'ssh_timeout'],
                ['universal_timeout', 'serial_timeout']
            ],
            "required_if": [
                ['enable_universal_timeout', True, ['universal_timeout']]
            ]
        }
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            curr_resp = fetch_session_inactivity_settings(rest_obj)
            payload, diff = update_payload(module, curr_resp)
            process_check_mode(module, diff)
            resp = update_session_inactivity_settings(rest_obj, payload)
            module.exit_json(msg=SUCCESS_MSG,
                             session_inactivity_setting=resp.json_data, changed=True)

    except HTTPError as err:
        module.exit_json(msg=str(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (
            IOError, ValueError, SSLError, TypeError, ConnectionError, AttributeError, IndexError, KeyError,
            OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
