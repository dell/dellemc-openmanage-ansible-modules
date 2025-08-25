#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.0
# Copyright (C) 2020-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

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
  ignore_certificate_validation:
    description:
      - This option will ignore the integrated certificate checks like those used for the warranty and catalog updates.
      - C(true) ignores the certificate validation.
      - C(false) does not ignore the certificate validation.
    type: bool
    default: false
    aliases: [ssl_check_disabled]
    version_added: 9.5.0
  proxy_exclusion_list:
    description:
      - The list of IPv4 addresses, IPv6 addresses or the domain names of the devices that can bypass the proxy server to directly access the appliance.
    type: list
    elements: str
    version_added: 9.5.0
  update_password:
    description:
      - This flag is used to update the I(proxy_password).
      - This is applicable only when I(enable_authentication) is C(true).
      - C(true) will update the I(proxy_password).
      - C(false) will not update the I(proxy_password).
    type: bool
    default: false
    version_added: 9.5.0
requirements:
    - "python >= 3.9.6"
author:
    - "Sajna Shetty(@Sajna-Shetty)"
    - "Rajshekar P(@rajshekarp87)"
    - "Sapana Gupta(@sapana05)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
    - This module supports C(check_mode).
    - This module supports IPv4 and IPv6 addresses.
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

- name: Add IPv4, IPv6 and domain names of devices in proxy exclusion list
  dellemc.openmanage.ome_application_network_proxy:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    enable_proxy: true
    ip_address: "192.168.0.2"
    proxy_port: 444
    enable_authentication: false
    proxy_exclusion_list:
      - 192.168.1.0
      - 191.187.2.0
      - www.*.com
      - 191.1.168.1/24

- name: Clear the proxy exclusion list
  dellemc.openmanage.ome_application_network_proxy:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    enable_proxy: true
    ip_address: "192.168.0.2"
    proxy_port: 444
    proxy_exclusion_list: []

- name: Ignore the certificate validation
  dellemc.openmanage.ome_application_network_proxy:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    enable_proxy: true
    ip_address: "192.168.0.2"
    proxy_port: 444
    ignore_certificate_validation: true
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
  returned: On successful configuration of network proxy settings
  sample: {
        "EnableAuthentication": true,
        "EnableProxy": true,
        "IpAddress": "192.168.0.2",
        "Password": null,
        "PortNumber": 444,
        "ProxyExclusionList": ["192.168.0.1", "www.*.com", "172.1.1.1/24"],
        "SslCheckDisabled": false,
        "Username": "root",
        }
error_info:
  description: Details of the HTTP error.
  returned: On HTTP error
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
from urllib.error import HTTPError, URLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import remove_key

PROXY_CONFIG = "ApplicationService/Network/ProxyConfiguration"
CHECK_MODE_CHANGE_FOUND_MSG = "Changes found to be applied."
CHECK_MODE_CHANGE_NOT_FOUND_MSG = "No Changes found to be applied."
NO_PROXY_CONFIGURATION = "Unable to configure the proxy because proxy configuration settings " \
                         "are not provided."
NO_CHANGE_IN_CONFIGURATION = "No changes made to proxy configuration as entered values are the " \
                             "same as current configuration values."
ODATA_REGEX = "(.*?)@odata"


def remove_unwanted_keys(key_list, payload):
    """
    Remove unwanted keys from the payload dictionary.

    Args:
        key_list (list): A list of keys to remove from the payload dictionary.
        payload (dict): The payload dictionary from which unwanted keys will be removed.

    Returns:
        None

    """
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
    """
    Generates a payload for the network proxy configuration.

    Args:
        module (object): The Ansible module object.

    Returns:
        dict: The payload for the network proxy configuration.
    """
    params = module.params
    proxy_payload_map = {
        "ip_address": "IpAddress",
        "proxy_port": "PortNumber",
        "enable_proxy": "EnableProxy",
        "proxy_username": "Username",
        "proxy_password": "Password",
        "enable_authentication": "EnableAuthentication",
        "ignore_certificate_validation": "SslCheckDisabled",
        "proxy_exclusion_list": "ProxyExclusionList"
    }
    backup_params = params.copy()
    remove_keys = ["hostname", "username", "password", "port", "ca_path", "validate_certs",
                   "timeout", "update_password"]
    remove_unwanted_keys(remove_keys, backup_params)
    payload = dict([(proxy_payload_map[key], val) for key, val in backup_params.items() if val
                    is not None])
    if backup_params.get("proxy_exclusion_list") or backup_params.get("proxy_exclusion_list") == []:
        temp_proxy_exclusion_list = backup_params.get("proxy_exclusion_list")
        converted_proxy_exclusion_list = ";".join(temp_proxy_exclusion_list)
        payload["ProxyExclusionList"] = converted_proxy_exclusion_list
    return payload


def get_updated_payload(rest_obj, module, payload):
    """
    Generates a payload for the network proxy configuration.

    Args:
        rest_obj (object): The REST object.
        module (object): The Ansible module object.
        payload (dict): The payload for the network proxy configuration.

    Returns:
        dict: The updated payload for the network proxy configuration.
    """
    current_setting = {}
    if not any(payload):
        module.exit_json(msg=NO_PROXY_CONFIGURATION, failed=True)
    else:
        params = module.params
        if params.get("update_password"):
            remove_keys = ["@odata.context", "@odata.type", "@odata.id"]
        else:
            remove_keys = ["@odata.context", "@odata.type", "@odata.id", "Password"]
        enable_authentication = params.get("enable_authentication")
        if enable_authentication is False:
            remove_keys.append("Username")
            payload.pop('Username', None)
            payload.pop('Password', None)
        else:
            if params.get("update_password"):
                payload['Username'] = params.get("proxy_username")
                payload['Password'] = params.get("proxy_password")
        resp = rest_obj.invoke_request("GET", PROXY_CONFIG)
        current_setting = resp.json_data
        remove_unwanted_keys(remove_keys, current_setting)
        diff = any(key in current_setting and val != current_setting[key] for key, val in
                   payload.items())
        validate_check_mode_for_network_proxy(diff, module)
        if not diff:
            module.exit_json(msg=NO_CHANGE_IN_CONFIGURATION)
        else:
            current_setting.update(payload)
    return current_setting


def main():
    """
    Main function that serves as the entry point for the module.

    Returns:
      None
    """
    specs = {
        "ip_address": {"required": False, "type": "str"},
        "proxy_port": {"required": False, "type": "int"},
        "enable_proxy": {"required": True, "type": "bool"},
        "proxy_username": {"required": False, "type": "str"},
        "proxy_password": {"required": False, "type": "str", "no_log": True},
        "enable_authentication": {"required": False, "type": "bool"},
        "ignore_certificate_validation": {"required": False, "type": "bool", "default": False,
                                          "aliases": ["ssl_check_disabled"]},
        "proxy_exclusion_list": {"required": False, "type": "list", "elements": "str"},
        "update_password": {"required": False, "type": "bool", "default": False},
    }

    module = OmeAnsibleModule(
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
            response_data = resp.json_data
            proxy_configuration_details = response_data.copy()
            if not response_data.get("ProxyExclusionList"):
                proxy_exclusion_list_list = []
            else:
                proxy_exclusion_list_str = response_data.get("ProxyExclusionList")
                proxy_exclusion_list_list = proxy_exclusion_list_str.split(';')
            proxy_configuration_details["ProxyExclusionList"] = proxy_exclusion_list_list
            module.exit_json(msg="Successfully updated network proxy configuration.",
                             proxy_configuration=proxy_configuration_details,
                             changed=True)
    except HTTPError as err:
        filter_err = remove_key(json.load(err), regex_pattern=ODATA_REGEX)
        module.exit_json(msg=str(err), error_info=filter_err, failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (ValueError, TypeError, ConnectionError, SSLValidationError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == "__main__":
    main()
