#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.0.1
# Copyright (C) 2021-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: ome_device_local_access_configuration
short_description: Configure local access settings on OpenManage Enterprise Modular.
description: This module allows to configure the local access settings of the power button, quick sync, KVM,
  LCD, and chassis direct access on OpenManage Enterprise Modular.
version_added: "4.4.0"
extends_documentation_fragment:
 - dellemc.openmanage.omem_auth_options
options:
  device_id:
    type: int
    description:
      - The ID of the chassis for which the local access configuration to be updated.
      - If the device ID is not specified, this module updates the local access settings for the I(hostname).
      - I(device_id) is mutually exclusive with I(device_service_tag).
  device_service_tag:
    type: str
    description:
      - The service tag of the chassis for which the local access settings needs to be updated.
      - If the device service tag is not specified, this module updates the local access settings for the I(hostname).
      - I(device_service_tag) is mutually exclusive with I(device_id).
  enable_kvm_access:
    type: bool
    description: Enables or disables the keyboard, video, and mouse (KVM) interfaces.
  enable_chassis_direct_access:
    type: bool
    description: Enables or disables the access to management consoles such as iDRAC and the management module of
      the device on the chassis.
  chassis_power_button:
    type: dict
    description: The settings for the chassis power button.
    suboptions:
      enable_chassis_power_button:
        required: true
        type: bool
        description:
          - Enables or disables the chassis power button.
          - If C(False), the chassis cannot be turn on or turn off using the power button.
      enable_lcd_override_pin:
        type: bool
        description:
          - Enables or disables the LCD override pin.
          - This is required when I(enable_chassis_power_button) is C(False).
      disabled_button_lcd_override_pin:
        type: int
        description:
          - The six digit LCD override pin to change the power state of the chassis.
          - This is required when I(enable_lcd_override_pin) is C(True).
          - The module will always report change when I(disabled_button_lcd_override_pin) is C(True).
  quick_sync:
    type: dict
    description:
      - The settings for quick sync.
      - The I(quick_sync) options are ignored if the quick sync hardware is not present.
    suboptions:
      quick_sync_access:
        type: str
        choices: [READ_WRITE, READ_ONLY, DISABLED]
        description:
          - Users with administrator privileges can set the following types of I(quick_sync_access).
          - C(READ_WRITE) enables writing configuration using quick sync.
          - C(READ_ONLY) enables read only access to Wi-Fi and Bluetooth Low Energy(BLE).
          - C(DISABLED) disables reading or writing configuration through quick sync.
      enable_inactivity_timeout:
        type: bool
        description: Enables or disables the inactivity timeout.
      timeout_limit:
        type: int
        description:
          - Inactivity timeout in seconds or minutes.
          - The range is 120 to 3600 in seconds, or 2 to 60 in minutes.
          - This option is required when I(enable_inactivity_timeout) is C(True).
      timeout_limit_unit:
        type: str
        choices: [SECONDS, MINUTES]
        description:
          - Inactivity timeout limit unit.
          - C(SECONDS) to set I(timeout_limit) in seconds.
          - C(MINUTES) to set I(timeout_limit) in minutes.
          - This option is required when I(enable_inactivity_timeout) is C(True).
      enable_read_authentication:
        type: bool
        description: Enables or disables the option to log in using your user credentials and to read the
          inventory in a secure data center.
      enable_quick_sync_wifi:
        type: bool
        description: Enables or disables the Wi-Fi communication path to the chassis.
  lcd:
    type: dict
    description:
      - The settings for LCD.
      - The I(lcd) options are ignored if the LCD hardware is not present in the chassis.
    suboptions:
      lcd_access:
        type: str
        choices: [VIEW_AND_MODIFY, VIEW_ONLY, DISABLED]
        description:
          - Option to configure the quick sync settings using LCD.
          - C(VIEW_AND_MODIFY) to set access level to view and modify.
          - C(VIEW_ONLY) to set access level to view.
          - C(DISABLED) to disable the access.
      user_defined:
        type: str
        description: The text to display on the LCD Home screen. The LCD Home screen is displayed when the system
          is reset to factory default settings. The user-defined text can have a maximum of 62 characters.
      lcd_language:
        type: str
        description:
          - The language code in which the text on the LCD must be displayed.
          - en to set English language.
          - fr to set French language.
          - de to set German language.
          - es to set Spanish language.
          - ja to set Japanese language.
          - zh to set Chinese language.
requirements:
  - "python >= 3.8.6"
author:
  - "Felix Stephen (@felixs88)"
notes:
  - Run this module from a system that has direct access to OpenManage Enterprise Modular.
  - This module supports C(check_mode).
  - The module will always report change when I(enable_chassis_power_button) is C(True).
"""

EXAMPLES = """
---
- name: Configure KVM, direct access and power button settings of the chassis using device ID.
  dellemc.openmanage.ome_device_local_access_configuration:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_id: 25011
    enable_kvm_access: true
    enable_chassis_direct_access: false
    chassis_power_button:
      enable_chassis_power_button: false
      enable_lcd_override_pin: true
      disabled_button_lcd_override_pin: 123456

- name: Configure Quick sync and LCD settings of the chassis using device service tag.
  dellemc.openmanage.ome_device_local_access_configuration:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_service_tag: GHRT2RL
    quick_sync:
      quick_sync_access: READ_ONLY
      enable_read_authentication: true
      enable_quick_sync_wifi: true
      enable_inactivity_timeout: true
      timeout_limit: 10
      timeout_limit_unit: MINUTES
    lcd:
      lcd_access: VIEW_ONLY
      lcd_language: en
      user_defined: "LCD Text"

- name: Configure all local access settings of the host chassis.
  dellemc.openmanage.ome_device_local_access_configuration:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    enable_kvm_access: true
    enable_chassis_direct_access: false
    chassis_power_button:
      enable_chassis_power_button: false
      enable_lcd_override_pin: true
      disabled_button_lcd_override_pin: 123456
    quick_sync:
      quick_sync_access: READ_WRITE
      enable_read_authentication: true
      enable_quick_sync_wifi: true
      enable_inactivity_timeout: true
      timeout_limit: 120
      timeout_limit_unit: SECONDS
    lcd:
      lcd_access: VIEW_MODIFY
      lcd_language: en
      user_defined: "LCD Text"
"""

RETURN = """
---
msg:
  type: str
  description: Overall status of the device local access settings.
  returned: always
  sample: "Successfully updated the local access settings."
location_details:
  type: dict
  description: returned when local access settings are updated successfully.
  returned: success
  sample: {
    "SettingType": "LocalAccessConfiguration",
    "EnableChassisDirect": false,
    "EnableChassisPowerButton": false,
    "EnableKvmAccess": true,
    "EnableLcdOverridePin": false,
    "LcdAccess": "VIEW_ONLY",
    "LcdCustomString": "LCD Text",
    "LcdLanguage": "en",
    "LcdOverridePin": "",
    "LcdPinLength": null,
    "LcdPresence": "Present",
    "LedPresence": null,
    "QuickSync": {
      "EnableInactivityTimeout": true,
      "EnableQuickSyncWifi": false,
      "EnableReadAuthentication": false,
      "QuickSyncAccess": "READ_ONLY",
      "QuickSyncHardware": "Present",
      "TimeoutLimit": 7,
      "TimeoutLimitUnit": "MINUTES"
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
"""


import json
import socket
import copy
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params

DOMAIN_URI = "ManagementDomainService/Domains"
DEVICE_URI = "DeviceService/Devices"
LAC_API = "DeviceService/Devices({0})/Settings('LocalAccessConfiguration')"
CONFIG_FAIL_MSG = "one of the following is required: enable_kvm_access, enable_chassis_direct_access, " \
                  "chassis_power_button, quick_sync, lcd"
DOMAIN_FAIL_MSG = "The operation to configure the local access is supported only on " \
                  "OpenManage Enterprise Modular."
FETCH_FAIL_MSG = "Unable to retrieve the device information."
DEVICE_FAIL_MSG = "Unable to complete the operation because the entered target device {0} '{1}' is invalid."
LAC_FAIL_MSG = "Unable to complete the operation because the local access configuration settings " \
               "are not supported on the specified device."
CHANGES_FOUND = "Changes found to be applied."
NO_CHANGES_FOUND = "No changes found to be applied."
SUCCESS_MSG = "Successfully updated the local access settings."


def get_ip_from_host(hostname):
    ipaddr = hostname
    try:
        result = socket.getaddrinfo(hostname, None)
        last_element = result[-1]
        ip_address = last_element[-1][0]
        if ip_address:
            ipaddr = ip_address
    except socket.gaierror:
        ipaddr = hostname
    except Exception:
        ipaddr = hostname
    return ipaddr


def get_chassis_device(module, rest_obj):
    key, value = None, None
    ipaddress = get_ip_from_host(module.params["hostname"])
    resp = rest_obj.invoke_request("GET", DOMAIN_URI)
    for data in resp.json_data["value"]:
        if ipaddress in data["PublicAddress"]:
            key, value = ("Id", data["DeviceId"])
            break
    else:
        module.fail_json(msg=FETCH_FAIL_MSG)
    return key, value


def check_domain_service(module, rest_obj):
    try:
        rest_obj.invoke_request("GET", DOMAIN_URI, api_timeout=5)
    except HTTPError as err:
        err_message = json.load(err)
        if err_message["error"]["@Message.ExtendedInfo"][0]["MessageId"] == "CGEN1006":
            module.fail_json(msg=DOMAIN_FAIL_MSG)
    return


def check_mode_validation(module, loc_resp):
    exist_config = {
        "EnableKvmAccess": loc_resp["EnableKvmAccess"], "EnableChassisDirect": loc_resp["EnableChassisDirect"],
        "EnableChassisPowerButton": loc_resp["EnableChassisPowerButton"],
        "EnableLcdOverridePin": loc_resp["EnableLcdOverridePin"], "LcdAccess": loc_resp["LcdAccess"],
        "LcdCustomString": loc_resp["LcdCustomString"], "LcdLanguage": loc_resp["LcdLanguage"]}
    quick_sync = loc_resp["QuickSync"]
    exist_quick_config = {
        "QuickSyncAccess": quick_sync["QuickSyncAccess"], "TimeoutLimit": quick_sync["TimeoutLimit"],
        "EnableInactivityTimeout": quick_sync["EnableInactivityTimeout"],
        "TimeoutLimitUnit": quick_sync["TimeoutLimitUnit"],
        "EnableReadAuthentication": quick_sync["EnableReadAuthentication"],
        "EnableQuickSyncWifi": quick_sync["EnableQuickSyncWifi"]}
    req_config, req_quick_config, payload = {}, {}, {}
    lcd_options, chassis_power = module.params.get("lcd"), module.params.get("chassis_power_button")
    if loc_resp["LcdPresence"] == "Present" and lcd_options is not None:
        req_config["LcdCustomString"] = lcd_options.get("user_defined")
        req_config["LcdAccess"] = lcd_options.get("lcd_access")
        req_config["LcdLanguage"] = lcd_options.get("lcd_language")
    req_config["EnableKvmAccess"] = module.params.get("enable_kvm_access")
    req_config["EnableChassisDirect"] = module.params.get("enable_chassis_direct_access")
    if chassis_power is not None:
        power_button = chassis_power["enable_chassis_power_button"]
        if power_button is False:
            chassis_pin = chassis_power.get("enable_lcd_override_pin")
            if chassis_pin is True:
                exist_config["LcdOverridePin"] = loc_resp["LcdOverridePin"]
                req_config["LcdOverridePin"] = chassis_power["disabled_button_lcd_override_pin"]
            req_config["EnableLcdOverridePin"] = chassis_pin
        req_config["EnableChassisPowerButton"] = power_button
    q_sync = module.params.get("quick_sync")
    if q_sync is not None and loc_resp["QuickSync"]["QuickSyncHardware"] == "Present":
        req_quick_config["QuickSyncAccess"] = q_sync.get("quick_sync_access")
        req_quick_config["EnableReadAuthentication"] = q_sync.get("enable_read_authentication")
        req_quick_config["EnableQuickSyncWifi"] = q_sync.get("enable_quick_sync_wifi")
        if q_sync.get("enable_inactivity_timeout") is True:
            time_limit, time_unit = q_sync.get("timeout_limit"), q_sync.get("timeout_limit_unit")
            if q_sync.get("timeout_limit_unit") == "MINUTES":
                time_limit, time_unit = time_limit * 60, "SECONDS"
            req_quick_config["TimeoutLimit"] = time_limit
            req_quick_config["TimeoutLimitUnit"] = time_unit
        req_quick_config["EnableInactivityTimeout"] = q_sync.get("enable_inactivity_timeout")
    req_config = dict([(k, v) for k, v in req_config.items() if v is not None])
    req_quick_config = dict([(k, v) for k, v in req_quick_config.items() if v is not None])
    cloned_req_config = copy.deepcopy(exist_config)
    cloned_req_config.update(req_config)
    cloned_req_quick_config = copy.deepcopy(exist_quick_config)
    cloned_req_quick_config.update(req_quick_config)
    diff_changes = [bool(set(exist_config.items()) ^ set(cloned_req_config.items())) or
                    bool(set(exist_quick_config.items()) ^ set(cloned_req_quick_config.items()))]
    if module.check_mode and any(diff_changes) is True:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    elif (module.check_mode and all(diff_changes) is False) or \
            (not module.check_mode and all(diff_changes) is False):
        module.exit_json(msg=NO_CHANGES_FOUND)
    payload.update(cloned_req_config)
    payload["QuickSync"] = cloned_req_quick_config
    payload["QuickSync"]["QuickSyncHardware"] = loc_resp["QuickSync"]["QuickSyncHardware"]
    payload["SettingType"] = "LocalAccessConfiguration"
    payload["LcdPresence"] = loc_resp["LcdPresence"]
    return payload


def get_device_details(rest_obj, module):
    device_id, tag = module.params.get("device_id"), module.params.get("device_service_tag")
    if device_id is None and tag is None:
        key, value = get_chassis_device(module, rest_obj)
        device_id = value
    else:
        key, value = ("Id", device_id) if device_id is not None else ("DeviceServiceTag", tag)
        param_value = "{0} eq {1}".format(key, value) if key == "Id" else "{0} eq '{1}'".format(key, value)
        resp = rest_obj.invoke_request("GET", DEVICE_URI, query_param={"$filter": param_value})
        resp_data = resp.json_data.get("value")
        rename_key = "id" if key == "Id" else "service tag"
        if not resp_data:
            module.fail_json(msg=DEVICE_FAIL_MSG.format(rename_key, value))
        if key == "DeviceServiceTag" and resp_data[0]["DeviceServiceTag"] == tag:
            device_id = resp_data[0]["Id"]
        elif key == "Id" and resp_data[0]["Id"] == device_id:
            device_id = resp_data[0]["Id"]
        else:
            module.fail_json(msg=DEVICE_FAIL_MSG.format(rename_key, value))
    try:
        loc_resp = rest_obj.invoke_request("GET", LAC_API.format(device_id))
    except HTTPError as err:
        err_message = json.load(err)
        error_msg = err_message.get('error', {}).get('@Message.ExtendedInfo')
        if error_msg and error_msg[0].get("MessageId") == "CGEN1004":
            module.fail_json(msg=LAC_FAIL_MSG)
    else:
        payload = check_mode_validation(module, loc_resp.json_data)
        final_resp = rest_obj.invoke_request("PUT", LAC_API.format(device_id), data=payload)
    return final_resp


def main():
    chassis_power = {
        "enable_chassis_power_button": {"type": "bool", "required": True},
        "enable_lcd_override_pin": {"type": "bool", "required": False},
        "disabled_button_lcd_override_pin": {"type": "int", "required": False, "no_log": True}}
    quick_sync_options = {
        "quick_sync_access": {"type": "str", "required": False, "choices": ["DISABLED", "READ_ONLY", "READ_WRITE"]},
        "enable_inactivity_timeout": {"type": "bool", "required": False},
        "timeout_limit": {"type": "int", "required": False},
        "timeout_limit_unit": {"type": "str", "required": False, "choices": ["SECONDS", "MINUTES"]},
        "enable_read_authentication": {"type": "bool", "required": False},
        "enable_quick_sync_wifi": {"type": "bool", "required": False}}
    lcd_options = {
        "lcd_access": {"type": "str", "required": False, "choices": ["VIEW_AND_MODIFY", "VIEW_ONLY", "DISABLED"]},
        "user_defined": {"type": "str", "required": False},
        "lcd_language": {"type": "str", "required": False}}
    specs = {
        "device_id": {"required": False, "type": "int"},
        "device_service_tag": {"required": False, "type": "str"},
        "enable_kvm_access": {"required": False, "type": "bool"},
        "enable_chassis_direct_access": {"required": False, "type": "bool"},
        "chassis_power_button": {
            "required": False, "type": "dict", "options": chassis_power,
            "required_if": [["enable_lcd_override_pin", True, ("disabled_button_lcd_override_pin",)]],
        },
        "quick_sync": {
            "required": False, "type": "dict", "options": quick_sync_options,
            "required_if": [["enable_inactivity_timeout", True, ("timeout_limit", "timeout_limit_unit")]]
        },
        "lcd": {
            "required": False, "type": "dict", "options": lcd_options,
        },
    }
    specs.update(ome_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[('device_id', 'device_service_tag')],
        required_one_of=[["enable_kvm_access", "enable_chassis_direct_access",
                          "chassis_power_button", "quick_sync", "lcd"]],
        supports_check_mode=True,
    )
    try:
        if not any([module.params.get("chassis_power_button"), module.params.get("quick_sync"),
                    module.params.get("lcd"), module.params.get("enable_kvm_access") is not None,
                    module.params.get("enable_chassis_direct_access") is not None]):
            module.fail_json(msg=CONFIG_FAIL_MSG)
        with RestOME(module.params, req_session=True) as rest_obj:
            check_domain_service(module, rest_obj)
            resp = get_device_details(rest_obj, module)
            resp_data = resp.json_data
            quick_sync = module.params.get("quick_sync")
            if quick_sync is not None and quick_sync.get("enable_inactivity_timeout") is True and \
                    quick_sync.get("timeout_limit_unit") == "MINUTES":
                resp_data["QuickSync"]["TimeoutLimit"] = int(resp_data["QuickSync"]["TimeoutLimit"] / 60)
                resp_data["QuickSync"]["TimeoutLimitUnit"] = "MINUTES"
            module.exit_json(msg=SUCCESS_MSG, local_access_settings=resp_data, changed=True)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, AttributeError, IndexError, KeyError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
