#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.0.1
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_application_network_proxy
short_description: Updates the proxy configuration on OpenManage Enterprise
version_added: "2.1.0"
description: This module allows to configure a network proxy on OpenManage Enterprise.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  enable_proxy:
    description:
      - Enables or disables the HTTP proxy configuration.
      - If I(enable proxy) is false, then the HTTP proxy configuration is set to its default value.
    required: true
    type: bool
  ip_address:
    description:
      - Proxy server address.
      - This option is mandatory when I(enable_proxy) is true.
    type: str
  proxy_port:
    description:
      - Proxy server's port number.
      - This option is mandatory when I(enable_proxy) is true.
    type: int
  enable_authentication:
    description:
      - Enable or disable proxy authentication.
      - If I(enable_authentication) is true, I(proxy_username) and I(proxy_password) must be provided.
      - If I(enable_authentication) is false, the proxy username and password are set to its default values.
    type: bool
  proxy_username:
    description:
      - Proxy server username.
      - This option is mandatory when I(enable_authentication) is true.
    type: str
  proxy_password:
    description:
      - Proxy server password.
      - This option is mandatory when I(enable_authentication) is true.
    type: str
requirements:
    - "python >= 3.8.6"
author:
    - "Sajna Shetty(@Sajna-Shetty)"
notes:
    - Run this module from a system that has direct access to DellEMC OpenManage Enterprise.
    - This module does not support C(check_mode).
'''

EXAMPLES = r'''
---
- name: Update proxy configuration and enable authentication
  dellemc.openmanage.ome_application_network_proxy:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    enable_proxy: true
    ip_address: "192.168.0.2"
    proxy_port: 444
    enable_authentication: true
    proxy_username: "proxy_username"
    proxy_password: "proxy_password"

- name: Reset proxy authentication
  dellemc.openmanage.ome_application_network_proxy:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    enable_proxy: true
    ip_address: "192.168.0.2"
    proxy_port: 444
    enable_authentication: false

- name: Reset proxy configuration
  dellemc.openmanage.ome_application_network_proxy:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    enable_proxy: false
'''

RETURN = r'''
---
msg:
  type: str
  description: Overall status of the network proxy configuration change.
  returned: always
  sample: "Successfully updated network proxy configuration."
proxy_configuration:
  type: dict
  description: Updated application network proxy configuration.
  returned: success
  sample: {
        "EnableAuthentication": true,
        "EnableProxy": true,
        "IpAddress": "192.168.0.2",
        "Password": null,
        "PortNumber": 444,
        "Username": "root"
        }
error_info:
  description: Details of the HTTP error.
  returned: on HTTP error
  type: dict
  sample: {
        "error": {
            "@Message.ExtendedInfo": [
                {
                   "Message": "Unable to complete the request because the input value
                    for  PortNumber  is missing or an invalid value is entered.",
                    "MessageArgs": [
                        "PortNumber"
                    ],
                    "MessageId": "CGEN6002",
                    "RelatedProperties": [],
                    "Resolution": "Enter a valid value and retry the operation.",
                    "Severity": "Critical"
                }
            ],
            "code": "Base.1.0.GeneralError",
            "message": "A general error has occurred. See ExtendedInfo for more information."
        }
    }
'''

import json
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError

PROXY_CONFIG = "ApplicationService/Network/ProxyConfiguration"
CHECK_MODE_CHANGE_FOUND_MSG = "Changes found to be applied."
CHECK_MODE_CHANGE_NOT_FOUND_MSG = "No Changes found to be applied."


def remove_unwanted_keys(key_list, payload):
    [payload.pop(key) for key in key_list if key in payload]


def validate_check_mode_for_network_proxy(payload_diff, module):
    """
    check mode support validation
    :param payload_diff: payload difference
    :param module: ansible module object
    :return: None
    """
    if module.check_mode:
        if payload_diff:
            module.exit_json(msg=CHECK_MODE_CHANGE_FOUND_MSG, changed=True)
        else:
            module.exit_json(msg=CHECK_MODE_CHANGE_NOT_FOUND_MSG, changed=False)


def get_payload(module):
    params = module.params
    proxy_payload_map = {
        "ip_address": "IpAddress",
        "proxy_port": "PortNumber",
        "enable_proxy": "EnableProxy",
        "proxy_username": "Username",
        "proxy_password": "Password",
        "enable_authentication": "EnableAuthentication"
    }
    backup_params = params.copy()
    remove_keys = ["hostname", "username", "password", "port", "ca_path", "validate_certs", "timeout"]
    remove_unwanted_keys(remove_keys, backup_params)
    payload = dict([(proxy_payload_map[key], val) for key, val in backup_params.items() if val is not None])
    return payload


def get_updated_payload(rest_obj, module, payload):
    current_setting = {}
    if not any(payload):
        module.fail_json(msg="Unable to configure the proxy because proxy configuration settings are not provided.")
    else:
        params = module.params
        remove_keys = ["@odata.context", "@odata.type", "@odata.id", "Password"]
        enable_authentication = params.get("enable_authentication")
        if enable_authentication is False:
            """when enable auth is disabled, ignore proxy username and password """
            remove_keys.append("Username")
            payload.pop('Username', None)
            payload.pop('Password', None)
        resp = rest_obj.invoke_request("GET", PROXY_CONFIG)
        current_setting = resp.json_data
        remove_unwanted_keys(remove_keys, current_setting)
        diff = any(key in current_setting and val != current_setting[key] for key, val in payload.items())
        validate_check_mode_for_network_proxy(diff, module)
        if not diff:
            module.exit_json(msg="No changes made to proxy configuration as entered values are the same as current "
                                 "configuration values.")
        else:
            current_setting.update(payload)
    return current_setting


def main():
    specs = {
        "ip_address": {"required": False, "type": "str"},
        "proxy_port": {"required": False, "type": "int"},
        "enable_proxy": {"required": True, "type": "bool"},
        "proxy_username": {"required": False, "type": "str"},
        "proxy_password": {"required": False, "type": "str", "no_log": True},
        "enable_authentication": {"required": False, "type": "bool"},
    }
    specs.update(ome_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        required_if=[['enable_proxy', True, ['ip_address', 'proxy_port']],
                     ['enable_authentication', True, ['proxy_username', 'proxy_password']], ],
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            payload = get_payload(module)
            updated_payload = get_updated_payload(rest_obj, module, payload)
            resp = rest_obj.invoke_request("PUT", PROXY_CONFIG, data=updated_payload)
            module.exit_json(msg="Successfully updated network proxy configuration.",
                             proxy_configuration=resp.json_data,
                             changed=True)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, SSLValidationError, OSError) as err:
        module.fail_json(msg=str(err))
    except Exception as err:
        module.fail_json(msg=str(err))


if __name__ == "__main__":
    main()
