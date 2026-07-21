#!/usr/bin/python
# -*- coding: utf-8 -*-
# Dell OpenManage Ansible Modules
# Version 9.12.4
# Copyright (C) 2025-2026 Dell Inc. or its subsidiaries. All Rights Reserved.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_application_snmp_settings
short_description: Manage OME SNMP listener configuration
version_added: "9.13.0"
description:
  - This module reads and updates the SNMP listener configuration (community string, port) on
    OpenManage Enterprise and OpenManage Enterprise Modular via REST API.
  - Use this module to set the community string before running M(dellemc.openmanage.ome_discovery)
    with C(community_string=true) to push the configured value to discovered devices.
  - This module supports C(check_mode).
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  community_string:
    description:
      - The SNMP community string to configure on the OME appliance.
      - Must be between 1 and 32 characters in length.
      - This value is treated as sensitive and will never appear in plaintext in module output.
      - It is recommended to use Ansible Vault to store this value, for example
        C(community_string={{ vault_community_string }}).
    type: str
    required: true
  snmp_port:
    description:
      - The SNMP listener port number on the OME appliance.
      - Must be between 1 and 65535.
    type: int
    default: 162
requirements:
    - "python >= 3.9.6"
notes:
  - This module supports C(check_mode).
  - Run this module from a system that has direct access to Dell OpenManage Enterprise
    or OpenManage Enterprise Modular.
  - The community string is never included in plaintext in the module output, diff output,
    or debug messages.
  - A warning is emitted when the community string matches a known-weak default value
    such as C(public) or C(private).
  - This module always reports C(changed=True) because OME masks the community
    string in API responses, making server-side comparison impossible. The OME
    API is itself idempotent — resending the same value is a no-op.
seealso:
  - module: dellemc.openmanage.ome_discovery
    description: Use C(ome_discovery) with C(community_string=true) and C(trap_destination=true) after
      setting the community string with this module.
author:
  - Mangirish Wagle (@mangirish)
'''

EXAMPLES = """
---
- name: Read current OME SNMP configuration
  dellemc.openmanage.ome_application_snmp_settings:
    hostname: "{{ hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    ca_path: "/path/to/ca_cert.pem"
    community_string: "{{ vault_community_string }}"
  check_mode: true

- name: Update the OME SNMP community string
  dellemc.openmanage.ome_application_snmp_settings:
    hostname: "{{ hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    ca_path: "/path/to/ca_cert.pem"
    community_string: "{{ vault_community_string }}"

- name: Update the OME SNMP community string and listener port
  dellemc.openmanage.ome_application_snmp_settings:
    hostname: "{{ hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    ca_path: "/path/to/ca_cert.pem"
    community_string: "{{ vault_community_string }}"
    snmp_port: 1162

- name: Two-step workflow - set community string then discover with SNMP enabled
  block:
    - name: Set SNMP community string on OME
      dellemc.openmanage.ome_application_snmp_settings:
        hostname: "{{ hostname }}"
        username: "{{ username }}"
        password: "{{ password }}"
        ca_path: "/path/to/ca_cert.pem"
        community_string: "{{ vault_community_string }}"

    - name: Discover servers with SNMP trap configuration enabled
      dellemc.openmanage.ome_discovery:
        hostname: "{{ hostname }}"
        username: "{{ username }}"
        password: "{{ password }}"
        ca_path: "/path/to/ca_cert.pem"
        discovery_job_name: "Server Discovery with SNMP"
        discovery_config_targets:
          - network_address_detail:
              - "192.168.1.0/24"
            device_types:
              - SERVER
        trap_destination: true
        community_string: true
"""

RETURN = """
---
msg:
  type: str
  description: Overall status of the SNMP settings operation.
  returned: always
  sample: "Successfully updated the SNMP settings."
snmp_details:
  type: dict
  description: The SNMP listener configuration after the operation.
  returned: success
  sample: {
    "Port": 162,
    "CommunityString": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"
  }
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
        "code": "Base.1.0.GeneralError",
        "message": "A general error has occurred."
    }
  }
"""

import json
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import (
    RestOME, OmeAnsibleModule
)

SUCCESS_MSG = "Successfully updated the SNMP settings."
NO_CHANGES = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
SNMP_GET_URL = "ApplicationService/IncomingAlertConfiguration"
SNMP_POST_URL = "ApplicationService/Actions/ApplicationService.UpdateSNMPConfiguration"
WEAK_COMMUNITY_STRINGS = ("public", "private")
COMMUNITY_STRING_MAX_LENGTH = 32


def community_string_no_log(module):
    if isinstance(module.params, dict) and 'community_string' in module.params:
        module.params['community_string'] = "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"


def exit_module(module, **kwargs):
    community_string_no_log(module)
    if kwargs.get('failed'):
        module.fail_json(**kwargs)
    else:
        module.exit_json(**kwargs)


def fetch_snmp_settings(rest_obj):
    resp = rest_obj.invoke_request("GET", SNMP_GET_URL)
    return resp.json_data


def update_snmp_settings(rest_obj, payload):
    resp = rest_obj.invoke_request("POST", SNMP_POST_URL, data=payload)
    return resp


def update_payload(module, curr_payload):
    payload = {
        "Port": module.params.get("snmp_port"),
        "CommunityString": module.params.get("community_string"),
    }
    return payload


def _diff_payload(curr_resp, desired_payload):
    compare_curr = {
        "Port": curr_resp.get("Port"),
    }
    compare_desired = {
        "Port": desired_payload.get("Port"),
    }
    is_change = compare_curr != compare_desired
    if not is_change:
        # Port is same; community string is always treated as changed since we
        # cannot read the current value from GET (it is masked by OME).
        # The API is idempotent on its own — sending the same value is a no-op.
        is_change = True
    return is_change


def validate_params(module):
    community_string = module.params.get("community_string")
    snmp_port = module.params.get("snmp_port")
    if not community_string:
        exit_module(module,
                    msg="The community_string parameter must not be empty.",
                    failed=True)
    if len(community_string) > COMMUNITY_STRING_MAX_LENGTH:
        exit_module(module,
                    msg="The community_string parameter must not exceed "
                        "{0} characters. Current length: {1}.".format(
                            COMMUNITY_STRING_MAX_LENGTH,
                            len(community_string)),
                    failed=True)
    if snmp_port is not None and (snmp_port < 1 or snmp_port > 65535):
        exit_module(module,
                    msg="The snmp_port parameter must be between 1 and "
                        "65535. Provided value: {0}.".format(snmp_port),
                    failed=True)


def warn_weak_community_string(module):
    community_string = module.params.get("community_string", "")
    if community_string.lower() in WEAK_COMMUNITY_STRINGS:
        module.warn(
            "The provided community_string is a known-weak default. "
            "Consider using a stronger community string for production "
            "environments.")


def sanitize_error_response(err_data):
    if isinstance(err_data, dict) and "error" in err_data:
        error = err_data["error"]
        sanitized = {
            "error": {
                "code": error.get("code", "Unknown"),
                "message": error.get("message", str(err_data)),
            }
        }
        return sanitized
    return err_data


def build_diff(curr_resp, desired_payload):
    return {
        "before": {
            "Port": curr_resp.get("Port"),
            "CommunityString": "***",
        },
        "after": {
            "Port": desired_payload.get("Port"),
            "CommunityString": "***",
        },
    }


def mask_snmp_details(details):
    if isinstance(details, dict) and "CommunityString" in details:
        details["CommunityString"] = "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"
    return details


def process_check_mode(module, diff, curr_resp, desired_payload):
    if not diff:
        exit_module(module, msg=NO_CHANGES,
                    snmp_details=mask_snmp_details(dict(curr_resp)))
    elif module.check_mode:
        result = {"msg": CHANGES_FOUND, "changed": True}
        if module._diff:
            result["diff"] = build_diff(curr_resp, desired_payload)
        exit_module(module, **result)


def main():
    specs = {
        "community_string": {"required": True, "type": "str", "no_log": True},
        "snmp_port": {"required": False, "type": "int", "default": 162},
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        supports_check_mode=True,
    )

    validate_params(module)
    warn_weak_community_string(module)

    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            curr_resp = fetch_snmp_settings(rest_obj)
            desired_payload = update_payload(module, curr_resp)
            diff = _diff_payload(curr_resp, desired_payload)
            process_check_mode(module, diff, curr_resp, desired_payload)
            update_snmp_settings(rest_obj, desired_payload)
            updated_resp = fetch_snmp_settings(rest_obj)
            result = {"msg": SUCCESS_MSG, "changed": True,
                      "snmp_details": mask_snmp_details(dict(updated_resp))}
            if module._diff:
                result["diff"] = build_diff(curr_resp, desired_payload)
            exit_module(module, **result)
    except HTTPError as err:
        err_data = {}
        try:
            err_data = json.load(err)
        except Exception:
            err_data = {"error": {"code": "Unknown", "message": str(err)}}
        exit_module(module, msg=str(err),
                    error_info=sanitize_error_response(err_data), failed=True)
    except URLError as err:
        exit_module(module, msg=str(err), unreachable=True, failed=True)
    except (IOError, ValueError, TypeError, ConnectionError, AttributeError,
            IndexError, KeyError, OSError, SSLValidationError) as err:
        exit_module(module, msg=str(err), failed=True)


if __name__ == '__main__':
    main()
