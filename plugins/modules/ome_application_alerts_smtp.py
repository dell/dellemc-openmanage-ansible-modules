#!/usr/bin/python
# -*- coding: utf-8 -*-
# Dell OpenManage Ansible Modules
# Version 9.12.4
# Copyright (C) 2021-2025 Dell Inc. or its subsidiaries. All Rights Reserved.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_application_alerts_smtp
short_description: This module allows to configure SMTP or email configurations
version_added: "4.3.0"
description:
  - This module allows to configure SMTP or email configurations on OpenManage Enterprise
    and OpenManage Enterprise Modular.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  destination_address:
    description: The IP address or FQDN of the SMTP destination server.
    type: str
    required: true
  port_number:
    description: The port number of the SMTP destination server.
    type: int
  use_ssl:
    description: Use SSL to connect with the SMTP server.
    type: bool
  enable_authentication:
    description:
      - Enable or disable authentication to access the SMTP server.
      - The I(credentials) are mandatory if I(enable_authentication) is C(true).
      - The module will always report change when this is C(true).
    type: bool
    required: true
  credentials:
    description: The credentials for the SMTP server
    type: dict
    suboptions:
      username:
        description:
          - The username to access the SMTP server.
        type: str
        required: true
      password:
        description:
          - The password to access the SMTP server.
        type: str
        required: true
requirements:
    - "python >= 3.9.6"
notes:
  - The module will always report change when I(enable_authentication) is C(true).
  - Run this module from a system that has direct access to Dell OpenManage Enterprise
    or OpenManage Enterprise Modular.
  - This module support C(check_mode).
author:
  - Sachin Apagundi(@sachin-apa)
  - Bhavneet Sharma (@Bhavneet-Sharma)
'''

EXAMPLES = """
---
- name: Update SMTP destination server configuration with authentication
  dellemc.openmanage.ome_application_alerts_smtp:
    hostname: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    destination_address: "localhost"
    port_number: 25
    use_ssl: true
    enable_authentication: true
    credentials:
      username: "username"
      password: "password"
- name: Update SMTP destination server configuration without authentication
  dellemc.openmanage.ome_application_alerts_smtp:
    hostname: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    destination_address: "localhost"
    port_number: 25
    use_ssl: false
    enable_authentication: false
"""

RETURN = """
---
msg:
  type: str
  description: Overall status of the SMTP settings update.
  returned: always
  sample: "Successfully updated the SMTP settings."
smtp_details:
  type: dict
  description: returned when SMTP settings are updated successfully.
  returned: success
  sample: {
    "DestinationAddress": "localhost",
    "PortNumber": 25,
    "UseCredentials": true,
    "UseSSL": false,
    "Credential": {
        "User": "admin",
        "Password": null
    }
  }

error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
        "code": "Base.1.0.GeneralError",
        "message": "A general error has occurred. See ExtendedInfo for more information.",
        "@Message.ExtendedInfo": [{
                "MessageId": "CAPP1106",
                "RelatedProperties": [],
                "Message": "Unable to update the SMTP settings because the entered credential is invalid or empty.",
                "MessageArgs": [],
                "Severity": "Critical",
                "Resolution": "Either enter valid credentials or disable the Use Credentials option and retry the operation."
            }
        ]
    }
  }
"""

import json
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.common.dict_transformations import recursive_diff

SUCCESS_MSG = "Successfully updated the SMTP settings."
SMTP_URL = "AlertService/AlertDestinations/SMTPConfiguration"
NO_CHANGES = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."


def fetch_smtp_settings(rest_obj):
    final_resp = rest_obj.invoke_request("GET", SMTP_URL)
    ret_data = final_resp.json_data.get('value')[0]
    ret_data.pop("@odata.type")
    return ret_data


def update_smtp_settings(rest_obj, payload):
    final_resp = rest_obj.invoke_request("POST", SMTP_URL, data=payload)
    return final_resp


def update_payload(module, curr_payload):
    smtp_data_payload = {
        "DestinationAddress": get_value(module, curr_payload, "destination_address", "DestinationAddress"),
        "UseCredentials": get_value(module, curr_payload, "enable_authentication", "UseCredentials"),
        "PortNumber": get_value(module, curr_payload, "port_number", "PortNumber"),
        "UseSSL": get_value(module, curr_payload, "use_ssl", "UseSSL")
    }
    if module.params.get("credentials") and smtp_data_payload.get("UseCredentials"):
        cred_payload = {
            "Credential": {
                "User": module.params.get("credentials").get("username"),
                "Password": module.params.get("credentials").get("password")
            }
        }
        smtp_data_payload.update(cred_payload)
    return smtp_data_payload


def get_value(module, resp, mod_key, attr_key):
    ret_value = module.params.get(mod_key)
    if module.params.get(mod_key) is None:
        ret_value = resp.get(attr_key)
    return ret_value


def _diff_payload(curr_resp, update_resp):
    is_change = False
    if update_resp:
        diff = recursive_diff(update_resp, curr_resp)
        if diff and diff[0]:
            is_change = True
    return is_change


def password_no_log(attributes):
    if isinstance(attributes, dict) and 'password' in attributes:
        attributes['password'] = "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"


def exit_module(module, **existmsg):
    password_no_log(module.params.get("credentials"))
    module.exit_json(**existmsg)


def process_check_mode(module, diff):
    if not diff:
        exit_module(module, msg=NO_CHANGES)
    elif module.check_mode:
        exit_module(module, msg=CHANGES_FOUND, changed=True)


def main():
    credentials_options = {"username": {"type": "str", "required": True},
                           "password": {"type": "str", "required": True, "no_log": True}}

    specs = {
        "destination_address": {"required": True, "type": "str"},
        "port_number": {"required": False, "type": "int"},
        "use_ssl": {"required": False, "type": "bool"},
        "enable_authentication": {"required": True, "type": "bool"},
        "credentials":
            {"required": False, "type": "dict",
             "options": credentials_options,
             },
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        required_if=[['enable_authentication', True, ['credentials']], ],
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            curr_resp = fetch_smtp_settings(rest_obj)
            payload = update_payload(module, curr_resp)
            diff = _diff_payload(curr_resp, payload)
            process_check_mode(module, diff)
            resp = update_smtp_settings(rest_obj, payload)
            exit_module(module, msg=SUCCESS_MSG,
                        smtp_details=resp.json_data, changed=True)

    except HTTPError as err:
        exit_module(module, msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        exit_module(module, msg=str(err), unreachable=True)
    except (
            IOError, ValueError, TypeError, ConnectionError, AttributeError, IndexError, KeyError,
            OSError) as err:
        exit_module(module, msg=str(err), error_info={"error": str(err)}, failed=True)


if __name__ == '__main__':
    main()
