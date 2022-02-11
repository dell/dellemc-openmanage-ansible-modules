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
module: ome_device_power_settings
short_description: Configure chassis power settings on OpenManage Enterprise Modular
description: This module allows to configure the chassis power settings on OpenManage Enterprise Modular.
version_added: "4.2.0"
extends_documentation_fragment:
  - dellemc.openmanage.omem_auth_options
options:
  device_id:
    type: int
    description:
      - The ID of the chassis for which the settings need to be updated.
      - If the device ID is not specified, this module updates the power settings for the I(hostname).
      - I(device_id) is mutually exclusive with I(device_service_tag).
  device_service_tag:
    type: str
    description:
      - The service tag of the chassis for which the setting needs to be updated.
      - If the device service tag is not specified, this module updates the power settings for the I(hostname).
      - I(device_service_tag) is mutually exclusive with I(device_id).
  power_configuration:
    description: The settings for Power configuration.
    type: dict
    suboptions:
      enable_power_cap:
        type: bool
        description: Enables or disables the Power Cap Settings.
        required: true
      power_cap:
        type: int
        description:
          - The maximum power consumption limit of the device. Specify the consumption limit in Watts.
          - This is required if I(enable_power_cap) is set to true.
  redundancy_configuration:
    description: The settings for Redundancy configuration.
    type: dict
    suboptions:
      redundancy_policy:
        type: str
        description:
          - The choices to configure the redundancy policy.
          - C(NO_REDUNDANCY) no redundancy policy is used.
          - C(GRID_REDUNDANCY) to distributes power by dividing the PSUs into two grids.
          - C(PSU_REDUNDANCY) to distribute power between all the PSUs.
        choices: ['NO_REDUNDANCY', 'GRID_REDUNDANCY', 'PSU_REDUNDANCY']
        default: NO_REDUNDANCY
  hot_spare_configuration:
    description: The settings for Hot Spare configuration.
    type: dict
    suboptions:
      enable_hot_spare:
        type: bool
        description: Enables or disables Hot Spare configuration to facilitate voltage regulation when power
          utilized by the Power Supply Unit (PSU) is low.
        required: true
      primary_grid:
        type: str
        description:
          - The choices for PSU grid.
          - C(GRID_1) Hot Spare on Grid 1.
          - C(GRID_2) Hot Spare on Grid 2.
        choices: ['GRID_1', 'GRID_2']
        default: GRID_1
requirements:
  - "python >= 3.8.6"
author:
  - "Felix Stephen (@felixs88)"
notes:
  - Run this module from a system that has direct access to Dell EMC OpenManage Enterprise Modular.
  - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Update power configuration settings of a chassis using the device ID.
  dellemc.openmanage.ome_device_power_settings:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_id: 25011
    power_configuration:
      enable_power_cap: true
      power_cap: 3424

- name: Update redundancy configuration settings of a chassis using the device service tag.
  dellemc.openmanage.ome_device_power_settings:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_service_tag: GHRT2RL
    redundancy_configuration:
      redundancy_policy: GRID_REDUNDANCY

- name: Update hot spare configuration settings of a chassis using device ID.
  dellemc.openmanage.ome_device_power_settings:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_id: 25012
    hot_spare_configuration:
      enable_hot_spare: true
      primary_grid: GRID_1
"""

RETURN = """
---
msg:
  type: str
  description: Overall status of the device power settings.
  returned: always
  sample: "Successfully updated the power settings."
power_details:
  type: dict
  description: returned when power settings are updated successfully.
  returned: success
  sample: {
    "EnableHotSpare": true,
    "EnablePowerCapSettings": true,
    "MaxPowerCap": "3424",
    "MinPowerCap": "3291",
    "PowerCap": "3425",
    "PrimaryGrid": "GRID_1",
    "RedundancyPolicy": "NO_REDUNDANCY",
    "SettingType": "Power"
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
POWER_API = "DeviceService/Devices({0})/Settings('Power')"
DEVICE_URI = "DeviceService/Devices"
DOMAIN_URI = "ManagementDomainService/Domains"
DEVICE_FAIL_MSG = "Unable to complete the operation because the entered target device {0} '{1}' is invalid."
CONFIG_FAIL_MSG = "one of the following is required: power_configuration, " \
                  "redundancy_configuration, hot_spare_configuration"
CHANGES_FOUND = "Changes found to be applied."
NO_CHANGES_FOUND = "No changes found to be applied."
SUCCESS_MSG = "Successfully updated the power settings."
FETCH_FAIL_MSG = "Failed to fetch the device information."
POWER_FAIL_MSG = "Unable to complete the operation because the power settings " \
                 "are not supported on the specified device."
DOMAIN_FAIL_MSG = "The device location settings operation is supported only on " \
                  "OpenManage Enterprise Modular."


def check_domain_service(module, rest_obj):
    try:
        rest_obj.invoke_request("GET", DOMAIN_URI, api_timeout=5)
    except HTTPError as err:
        err_message = json.load(err)
        if err_message["error"]["@Message.ExtendedInfo"][0]["MessageId"] == "CGEN1006":
            module.fail_json(msg=DOMAIN_FAIL_MSG)
    return


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


def check_mode_validation(module, loc_data):
    power_data = {"PowerCap": loc_data.get("PowerCap"), "MinPowerCap": loc_data["MinPowerCap"],
                  "MaxPowerCap": loc_data["MaxPowerCap"], "RedundancyPolicy": loc_data.get("RedundancyPolicy"),
                  "EnablePowerCapSettings": loc_data["EnablePowerCapSettings"],
                  "EnableHotSpare": loc_data["EnableHotSpare"], "PrimaryGrid": loc_data.get("PrimaryGrid")}
    cloned_data = copy.deepcopy(power_data)
    if module.params.get("power_configuration") is not None:
        if module.params["power_configuration"]["enable_power_cap"] is None:
            module.fail_json(msg="missing parameter: enable_power_cap")
        enable_power_cap = module.params["power_configuration"]["enable_power_cap"]
        power_cap = module.params["power_configuration"].get("power_cap")
        if enable_power_cap is True:
            cloned_data.update({"EnablePowerCapSettings": enable_power_cap, "PowerCap": str(power_cap)})
        else:
            cloned_data.update({"EnablePowerCapSettings": enable_power_cap})
    if module.params.get("redundancy_configuration") is not None:
        cloned_data.update({"RedundancyPolicy": module.params["redundancy_configuration"]["redundancy_policy"]})
    if module.params.get("hot_spare_configuration") is not None:
        if module.params["hot_spare_configuration"]["enable_hot_spare"] is None:
            module.fail_json(msg="missing parameter: enable_hot_spare")
        enable_hot_spare = module.params["hot_spare_configuration"]["enable_hot_spare"]
        primary_grid = module.params["hot_spare_configuration"].get("primary_grid")
        if enable_hot_spare is True:
            cloned_data.update({"EnableHotSpare": enable_hot_spare, "PrimaryGrid": primary_grid})
        else:
            cloned_data.update({"EnableHotSpare": enable_hot_spare})
    power_diff = bool(set(power_data.items()) ^ set(cloned_data.items()))
    if not power_diff and not module.check_mode:
        module.exit_json(msg=NO_CHANGES_FOUND)
    elif not power_diff and module.check_mode:
        module.exit_json(msg=NO_CHANGES_FOUND)
    elif power_diff and module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    cloned_data.update({"SettingType": "Power"})
    return cloned_data


def fetch_device_details(module, rest_obj):
    device_id, tag, final_resp = module.params.get("device_id"), module.params.get("device_service_tag"), {}
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
        loc_resp = rest_obj.invoke_request("GET", POWER_API.format(device_id))
    except HTTPError as err:
        if err.code == 404:
            module.fail_json(msg=POWER_FAIL_MSG)
        err_message = json.load(err)
        error_msg = err_message.get('error', {}).get('@Message.ExtendedInfo')
        if error_msg and error_msg[0].get("MessageId") == "CGEN1004":
            module.fail_json(msg=POWER_FAIL_MSG)
    else:
        payload = check_mode_validation(module, loc_resp.json_data)
        final_resp = rest_obj.invoke_request("PUT", POWER_API.format(device_id), data=payload)
    return final_resp


def main():
    power_options = {"enable_power_cap": {"type": "bool", "required": True},
                     "power_cap": {"type": "int", "required": False}}
    redundancy_options = {"redundancy_policy": {"type": "str", "default": "NO_REDUNDANCY",
                          "choices": ["NO_REDUNDANCY", "GRID_REDUNDANCY", "PSU_REDUNDANCY"]}}
    hot_spare_options = {"enable_hot_spare": {"required": True, "type": "bool"},
                         "primary_grid": {"required": False, "type": "str", "default": "GRID_1",
                                          "choices": ["GRID_1", "GRID_2"]}}
    specs = {
        "device_id": {"required": False, "type": "int"},
        "device_service_tag": {"required": False, "type": "str"},
        "power_configuration": {"type": "dict", "required": False, "options": power_options,
                                "required_if": [["enable_power_cap", True, ("power_cap",), True]]},
        "redundancy_configuration": {"type": "dict", "required": False, "options": redundancy_options},
        "hot_spare_configuration": {"type": "dict", "required": False, "options": hot_spare_options,
                                    "required_if": [["enable_hot_spare", True, ("primary_grid",)]]},
    }
    specs.update(ome_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[('device_id', 'device_service_tag')],
        required_one_of=[["power_configuration", "redundancy_configuration", "hot_spare_configuration"]],
        supports_check_mode=True,
    )
    try:
        if not any([module.params.get("power_configuration"), module.params.get("redundancy_configuration"),
                    module.params.get("hot_spare_configuration")]):
            module.fail_json(msg=CONFIG_FAIL_MSG)
        with RestOME(module.params, req_session=True) as rest_obj:
            check_domain_service(module, rest_obj)
            resp = fetch_device_details(module, rest_obj)
            module.exit_json(msg=SUCCESS_MSG, power_details=resp.json_data, changed=True)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, AttributeError, IndexError, KeyError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
