#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.0.1
# Copyright (C) 2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: ome_device_quick_deploy
short_description: Configure Quick Deploy settings on OpenManage Enterprise Modular.
description: This module allows to configure the Quick Deploy settings of the server or IOM
  on OpenManage Enterprise Modular.
version_added: "5.0.0"
extends_documentation_fragment:
  - dellemc.openmanage.omem_auth_options
options:
  device_id:
    type: int
    description:
      - The ID of the chassis for which the Quick Deploy settings to be deployed.
      - If the device ID is not specified, this module updates the Quick Deploy settings for the I(hostname).
      - I(device_id) is mutually exclusive with I(device_service_tag).
  device_service_tag:
    type: str
    description:
      - The service tag of the chassis for which the Quick Deploy settings to be deployed.
      - If the device service tag is not specified, this module updates the Quick Deploy settings for the I(hostname).
      - I(device_service_tag) is mutually exclusive with I(device_id).
  setting_type:
    type: str
    required: True
    choices: [ServerQuickDeploy, IOMQuickDeploy]
    description:
      - The type of the Quick Deploy settings to be applied.
      - C(ServerQuickDeploy) to apply the server Quick Deploy settings.
      - C(IOMQuickDeploy) to apply the IOM Quick Deploy settings.
  job_wait:
    type: bool
    description: Determines whether to wait for the job completion or not.
    default: True
  job_wait_timeout:
    type: int
    description:
      - The maximum wait time of I(job_wait) in seconds. The job is tracked only for this duration.
      - This option is applicable when I(job_wait) is C(True).
    default: 120
  quick_deploy_options:
    type: dict
    required: True
    description: The Quick Deploy settings for server and IOM quick deploy.
    suboptions:
      password:
        type: str
        description:
          - The password to login to the server or IOM.
          - The module will always report change when I(password) option is added.
      ipv4_enabled:
        type: bool
        description: Enables or disables the IPv4 network.
      ipv4_network_type:
        type: str
        choices: [Static, DHCP]
        description:
          - IPv4 network type.
          - I(ipv4_network_type) is required if I(ipv4_enabled) is C(True).
          - C(Static) to configure the static IP settings.
          - C(DHCP) to configure the Dynamic IP settings.
      ipv4_subnet_mask:
        type: str
        description:
          - IPv4 subnet mask.
          - I(ipv4_subnet_mask) is required if I(ipv4_network_type) is C(Static).
      ipv4_gateway:
        type: str
        description:
          - IPv4 gateway.
          - I(ipv4_gateway) is required if I(ipv4_network_type) is C(Static).
      ipv6_enabled:
        type: bool
        description: Enables or disables the IPv6 network.
      ipv6_network_type:
        type: str
        choices: [Static, DHCP]
        description:
          - IPv6 network type.
          - I(ipv6_network_type) is required if I(ipv6_enabled) is C(True).
          - C(Static) to configure the static IP settings.
          - C(DHCP) to configure the Dynamic IP settings.
      ipv6_prefix_length:
        type: int
        description:
          - IPV6 prefix length.
          - I(ipv6_prefix_length) is required if I(ipv6_network_type) is C(Static).
      ipv6_gateway:
        type: str
        description:
          - IPv6 gateway.
          - I(ipv6_gateway) is required if I(ipv6_network_type) is C(Static).
      slots:
        type: list
        elements: dict
        description: The slot configuration for the server or IOM.
        suboptions:
          slot_id:
            type: int
            required: True
            description: The ID of the slot.
          slot_ipv4_address:
            type: str
            description: The IPv4 address of the slot.
          slot_ipv6_address:
            type: str
            description: The IPv6 address of the slot.
          vlan_id:
            type: int
            description: The ID of the VLAN.
requirements:
  - "python >= 3.8.6"
author:
  - "Felix Stephen (@felixs88)"
notes:
  - Run this module from a system that has direct access to OpenManage Enterprise Modular.
  - This module supports C(check_mode).
  - The module will always report change when I(password) option is added.
  - If the chassis is a member of a multi-chassis group and it is assigned as a backup
    lead chassis, the operations performed on the chassis using this module may
    conflict with the management operations performed on the chassis through the lead chassis.
"""

EXAMPLES = """
---
- name: Configure server Quick Deploy settings of the chassis using device ID.
  dellemc.openmanage.ome_device_quick_deploy:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    device_id: 25011
    setting_type: ServerQuickDeploy
    ca_path: "/path/to/ca_cert.pem"
    quick_deploy_options:
      password: "password"
      ipv4_enabled: True
      ipv4_network_type: Static
      ipv4_subnet_mask: 255.255.255.0
      ipv4_gateway: 192.168.0.1
      ipv6_enabled: True
      ipv6_network_type: Static
      ipv6_prefix_length: 1
      ipv6_gateway: "::"
      slots:
        - slot_id: 1
          slot_ipv4_address: 192.168.0.2
          slot_ipv6_address: "::"
          vlan_id: 1
        - slot_id: 2
          slot_ipv4_address: 192.168.0.3
          slot_ipv6_address: "::"
          vlan_id: 2

- name: Configure server Quick Deploy settings of the chassis using device service tag.
  dellemc.openmanage.ome_device_quick_deploy:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    device_service_tag: GHRT2RL
    setting_type: IOMQuickDeploy
    ca_path: "/path/to/ca_cert.pem"
    quick_deploy_options:
      password: "password"
      ipv4_enabled: True
      ipv4_network_type: Static
      ipv4_subnet_mask: 255.255.255.0
      ipv4_gateway: 192.168.0.1
      ipv6_enabled: True
      ipv6_network_type: Static
      ipv6_prefix_length: 1
      ipv6_gateway: "::"
      slots:
        - slot_id: 1
          slot_ipv4_address: 192.168.0.2
          slot_ipv6_address: "::"
          vlan_id: 1
        - slot_id: 2
          slot_ipv4_address: 192.168.0.3
          slot_ipv6_address: "::"
          vlan_id: 2
"""

RETURN = """
---
msg:
  type: str
  description: Overall status of the device quick deploy settings.
  returned: always
  sample: "Successfully deployed the quick deploy settings."
job_id:
  type: int
  description: The job ID of the submitted quick deploy job.
  returned: when quick deploy job is submitted.
  sample: 1234
quick_deploy_settings:
  type: dict
  description: returned when quick deploy settings are deployed successfully.
  returned: success
  sample: {
    "DeviceId": 25011,
    "SettingType": "ServerQuickDeploy",
    "ProtocolTypeV4": true,
    "NetworkTypeV4": "Static",
    "IpV4Gateway": 192.168.0.1,
    "IpV4SubnetMask": "255.255.255.0",
    "ProtocolTypeV6": true,
    "NetworkTypeV6": "Static",
    "PrefixLength": "2",
    "IpV6Gateway": "::",
    "slots": [
      {
        "DeviceId": 25011,
        "DeviceCapabilities": [18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 41, 8, 7, 4, 3, 2, 1, 31, 30],
        "DeviceIPV4Address": "192.168.0.2",
        "DeviceIPV6Address": "::",
        "Dhcpipv4": "Disabled",
        "Dhcpipv6": "Disabled",
        "Ipv4Enabled": "Enabled",
        "Ipv6Enabled": "Enabled",
        "Model": "PowerEdge MX840c",
        "SlotIPV4Address": "192.168.0.2",
        "SlotIPV6Address": "::",
        "SlotId": 1,
        "SlotSelected": true,
        "SlotSettingsApplied": true,
        "SlotType": "2000",
        "Type": "1000",
        "VlanId": "1"
      },
      {
        "DeviceId": 0,
        "Model": "",
        "SlotIPV4Address": "0.0.0.0",
        "SlotIPV6Address": "::",
        "SlotId": 2,
        "SlotSelected": false,
        "SlotSettingsApplied": false,
        "SlotType": "2000",
        "Type": "0"
      },
      {
        "DeviceId": 0,
        "Model": "",
        "SlotIPV4Address": "0.0.0.0",
        "SlotIPV6Address": "::",
        "SlotId": 3,
        "SlotSelected": false,
        "SlotSettingsApplied": false,
        "SlotType": "2000",
        "Type": "0"
      },
      {
        "DeviceId": 0,
        "Model": "",
        "SlotIPV4Address": "0.0.0.0",
        "SlotIPV6Address": "::",
        "SlotId": 4,
        "SlotSelected": false,
        "SlotSettingsApplied": false,
        "SlotType": "2000",
        "Type": "0"
      },
      {
        "DeviceId": 0,
        "Model": "",
        "SlotIPV4Address": "0.0.0.0",
        "SlotIPV6Address": "::",
        "SlotId": 5,
        "SlotSelected": false,
        "SlotSettingsApplied": false,
        "SlotType": "2000",
        "Type": "0"
      },
      {
        "DeviceId": 0,
        "Model": "",
        "SlotIPV4Address": "0.0.0.0",
        "SlotIPV6Address": "::",
        "SlotId": 6,
        "SlotSelected": false,
        "SlotSettingsApplied": false,
        "SlotType": "2000",
        "Type": "0"
      },
      {
        "DeviceId": 0,
        "Model": "",
        "SlotIPV4Address": "0.0.0.0",
        "SlotIPV6Address": "::",
        "SlotId": 7,
        "SlotSelected": false,
        "SlotSettingsApplied": false,
        "SlotType": "2000",
        "Type": "0"
      },
      {
        "DeviceId": 0,
        "Model": "",
        "SlotIPV4Address": "0.0.0.0",
        "SlotIPV6Address": "::",
        "SlotId": 8,
        "SlotSelected": false,
        "SlotSettingsApplied": false,
        "SlotType": "2000",
        "Type": "0"
      }
    ]
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


import copy
import json
import socket
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params

DOMAIN_URI = "ManagementDomainService/Domains"
DEVICE_URI = "DeviceService/Devices"
QUICK_DEPLOY_API = "DeviceService/Devices({0})/Settings('{1}')"

DOMAIN_FAIL_MSG = "The operation to configure the Quick Deploy settings is supported only on " \
                  "OpenManage Enterprise Modular."
IP_FAIL_MSG = "Invalid '{0}' address provided for the {1}."
FETCH_FAIL_MSG = "Unable to retrieve the device information."
DEVICE_FAIL_MSG = "Unable to complete the operation because the entered target device {0} '{1}' is invalid."
QUICK_DEPLOY_FAIL_MSG = "Unable to complete the operation because the {0} configuration settings " \
                        "are not supported on the specified device."
INVALID_SLOT_MSG = "Unable to complete the operation because the entered slot(s) '{0}' does not exist."
CHANGES_FOUND = "Changes found to be applied."
NO_CHANGES_FOUND = "No changes found to be applied."
SUCCESS_MSG = "Successfully deployed the Quick Deploy settings."
FAIL_MSG = "Unable to deploy the Quick Deploy settings."
QUICK_DEPLOY_JOB_DESC = "The Quick Deploy job is initiated from the OpenManage Ansible Module collections."
JOB_MSG = "Successfully submitted the Quick Deploy job settings."


def validate_ip_address(address, flag):
    value = True
    try:
        if flag == "IPV4":
            socket.inet_aton(address)
            value = address.count('.') == 3
        else:
            socket.inet_pton(socket.AF_INET6, address)
    except socket.error:
        value = False
    return value


def ip_address_field(module, field, deploy_options, slot=False):
    module_params = deploy_options
    if slot:
        module_params = deploy_options
    for val in field:
        field_value = module_params.get(val[0])
        if field_value is not None:
            valid = validate_ip_address(module_params.get(val[0]), val[1])
            if valid is False:
                module.fail_json(msg=IP_FAIL_MSG.format(field_value, val[0]))
    return


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


def check_mode_validation(module, deploy_data):
    deploy_options = module.params.get("quick_deploy_options")
    req_data, req_payload = {}, {}
    if deploy_options.get("password") is not None:
        req_data["rootCredential"] = deploy_options.get("password")
    ipv4_enabled = deploy_options.get("ipv4_enabled")
    ipv4_enabled_deploy = deploy_data["ProtocolTypeV4"]
    ipv6_enabled_deploy = deploy_data["ProtocolTypeV6"]
    ipv4_nt_deploy = deploy_data.get("NetworkTypeV4")
    ipv6_nt_deploy = deploy_data.get("NetworkTypeV6")
    if ipv4_enabled is not None and ipv4_enabled is True or \
            ipv4_enabled_deploy is not None and ipv4_enabled_deploy is True:
        req_data["ProtocolTypeV4"] = None
        if ipv4_enabled is not None:
            req_data["ProtocolTypeV4"] = str(ipv4_enabled).lower()
        ipv4_network_type = deploy_options.get("ipv4_network_type")
        req_data["NetworkTypeV4"] = ipv4_network_type
        if ipv4_network_type == "Static" or ipv4_nt_deploy is not None and ipv4_nt_deploy == "Static":
            req_data["IpV4SubnetMask"] = deploy_options.get("ipv4_subnet_mask")
            req_data["IpV4Gateway"] = deploy_options.get("ipv4_gateway")
    elif ipv4_enabled is not None and ipv4_enabled is False:
        req_data["ProtocolTypeV4"] = str(ipv4_enabled).lower()
    ipv6_enabled = deploy_options.get("ipv6_enabled")
    if ipv6_enabled is not None and ipv6_enabled is True or \
            ipv6_enabled_deploy is not None and ipv6_enabled_deploy is True:
        req_data["ProtocolTypeV6"] = None
        if ipv6_enabled is not None:
            req_data["ProtocolTypeV6"] = str(ipv6_enabled).lower()
        ipv6_network_type = deploy_options.get("ipv6_network_type")
        req_data["NetworkTypeV6"] = ipv6_network_type
        if ipv6_network_type == "Static" or ipv6_nt_deploy is not None and ipv6_nt_deploy == "Static":
            req_data["PrefixLength"] = deploy_options.get("ipv6_prefix_length")
            if deploy_options.get("ipv6_prefix_length") is not None:
                req_data["PrefixLength"] = str(deploy_options.get("ipv6_prefix_length"))
            req_data["IpV6Gateway"] = deploy_options.get("ipv6_gateway")
    elif ipv6_enabled is not None and ipv6_enabled is False:
        req_data["ProtocolTypeV6"] = str(ipv6_enabled).lower()
    resp_data = {
        "ProtocolTypeV4": str(ipv4_enabled_deploy).lower(), "NetworkTypeV4": deploy_data.get("NetworkTypeV4"),
        "IpV4SubnetMask": deploy_data.get("IpV4SubnetMask"), "IpV4Gateway": deploy_data.get("IpV4Gateway"),
        "ProtocolTypeV6": str(ipv6_enabled_deploy).lower(), "NetworkTypeV6": deploy_data.get("NetworkTypeV6"),
        "PrefixLength": deploy_data.get("PrefixLength"), "IpV6Gateway": deploy_data.get("IpV6Gateway")}
    resp_filter_data = dict([(k, v) for k, v in resp_data.items() if v is not None])
    req_data_filter = dict([(k, v) for k, v in req_data.items() if v is not None])
    diff_changes = [bool(set(resp_filter_data.items()) ^ set(req_data_filter.items()))]
    req_slot_payload, invalid_slot = [], []
    slots = deploy_options.get("slots")
    if slots is not None:
        exist_slot = deploy_data.get("Slots")
        for each in slots:
            exist_filter_slot = list(filter(lambda d: d["SlotId"] in [each["slot_id"]], exist_slot))
            if exist_filter_slot:
                req_slot_1 = {"SlotId": each["slot_id"], "SlotIPV4Address": each.get("slot_ipv4_address"),
                              "SlotIPV6Address": each.get("slot_ipv6_address"), "VlanId": each.get("vlan_id")}
                if each.get("vlan_id") is not None:
                    req_slot_1.update({"VlanId": str(each.get("vlan_id"))})
                req_filter_slot = dict([(k, v) for k, v in req_slot_1.items() if v is not None])
                exist_slot_1 = {"SlotId": exist_filter_slot[0]["SlotId"],
                                "SlotIPV4Address": exist_filter_slot[0]["SlotIPV4Address"],
                                "SlotIPV6Address": exist_filter_slot[0]["SlotIPV6Address"],
                                "VlanId": exist_filter_slot[0]["VlanId"]}
                exist_filter_slot = dict([(k, v) for k, v in exist_slot_1.items() if v is not None])
                cp_exist_filter_slot = copy.deepcopy(exist_filter_slot)
                cp_exist_filter_slot.update(req_filter_slot)
                diff_changes.append(bool(set(cp_exist_filter_slot.items()) ^ set(exist_filter_slot.items())))
                req_slot_payload.append(cp_exist_filter_slot)
            else:
                invalid_slot.append(each["slot_id"])
        if invalid_slot:
            module.fail_json(msg=INVALID_SLOT_MSG.format(", ".join(map(str, invalid_slot))))
    if module.check_mode and any(diff_changes) is True:
        module.exit_json(msg=CHANGES_FOUND, changed=True, quick_deploy_settings=deploy_data)
    elif (module.check_mode and any(diff_changes) is False) or \
            (not module.check_mode and any(diff_changes) is False):
        module.exit_json(msg=NO_CHANGES_FOUND, quick_deploy_settings=deploy_data)
    req_payload.update(resp_filter_data)
    req_payload.update(req_data_filter)
    return req_payload, req_slot_payload


def job_payload_submission(rest_obj, payload, slot_payload, settings_type, device_id, resp_data):
    job_params = []
    job_params.append({"Key": "protocolTypeV4", "Value": payload["ProtocolTypeV4"]})
    job_params.append({"Key": "protocolTypeV6", "Value": payload["ProtocolTypeV6"]})
    s_type = "SERVER_QUICK_DEPLOY" if settings_type == "ServerQuickDeploy" else "IOM_QUICK_DEPLOY"
    job_params.append({"Key": "operationName", "Value": "{0}".format(s_type)})
    job_params.append({"Key": "deviceId", "Value": "{0}".format(device_id)})
    if payload.get("rootCredential") is not None:
        job_params.append({"Key": "rootCredential", "Value": payload["rootCredential"]})
    if payload.get("NetworkTypeV4") is not None:
        job_params.append({"Key": "networkTypeV4", "Value": payload["NetworkTypeV4"]})
    if payload.get("IpV4SubnetMask") is not None:
        job_params.append({"Key": "subnetMaskV4", "Value": payload["IpV4SubnetMask"]})
    if payload.get("IpV4Gateway") is not None:
        job_params.append({"Key": "gatewayV4", "Value": payload["IpV4Gateway"]})
    if payload.get("NetworkTypeV6") is not None:
        job_params.append({"Key": "networkTypeV6", "Value": payload["NetworkTypeV6"]})
    if payload.get("PrefixLength") is not None:
        job_params.append({"Key": "prefixLength", "Value": payload["PrefixLength"]})
    if payload.get("IpV6Gateway") is not None:
        job_params.append({"Key": "gatewayV6", "Value": payload["IpV6Gateway"]})
    updated_slot = []
    if slot_payload:
        for each in slot_payload:
            updated_slot.append(each.get("SlotId"))
            job_params.append(
                {"Key": "slotId={0}".format(each.get("SlotId")),
                 "Value": "SlotSelected=true;IPV4Address={0};IPV6Address={1};VlanId={2}".format(
                     each.get("SlotIPV4Address"), each.get("SlotIPV6Address"), each.get("VlanId"))})
    slots = resp_data["Slots"]
    if updated_slot is not None:
        slots = list(filter(lambda d: d["SlotId"] not in updated_slot, slots))
    for each in slots:
        key = "slot_id={0}".format(each["SlotId"])
        value = "SlotSelected={0};".format(each["SlotSelected"])
        if each.get("SlotIPV4Address") is not None:
            value = value + "IPV4Address={0};".format(each["SlotIPV4Address"])
        if each.get("SlotIPV6Address") is not None:
            value = value + "IPV6Address={0};".format(each["SlotIPV6Address"])
        if each.get("VlanId") is not None:
            value = value + "VlanId={0}".format(each["VlanId"])
        job_params.append({"Key": key, "Value": value})
    job_sub_resp = rest_obj.job_submission("Quick Deploy", QUICK_DEPLOY_JOB_DESC, [], job_params,
                                           {"Id": 42, "Name": "QuickDeploy_Task"})
    return job_sub_resp.json_data.get('Id')


def get_device_details(rest_obj, module):
    job_success_data, job_id = None, None
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
    settings_type, settings_key = "IOMQuickDeploy", "IOM Quick Deploy"
    if module.params["setting_type"] == "ServerQuickDeploy":
        settings_type, settings_key = "ServerQuickDeploy", "Server Quick Deploy"
    try:
        deploy_resp = rest_obj.invoke_request("GET", QUICK_DEPLOY_API.format(device_id, settings_type))
    except HTTPError as err:
        err_message = json.load(err)
        error_msg = err_message.get('error', {}).get('@Message.ExtendedInfo')
        if error_msg and error_msg[0].get("MessageId") == "CGEN1004":
            module.fail_json(msg=QUICK_DEPLOY_FAIL_MSG.format(settings_key))
    else:
        resp_data = rest_obj.strip_substr_dict(deploy_resp.json_data)
        payload, slot_payload = check_mode_validation(module, resp_data)
        job_id = job_payload_submission(rest_obj, payload, slot_payload, settings_type, device_id, resp_data)
        if module.params["job_wait"]:
            job_failed, job_msg = rest_obj.job_tracking(job_id, job_wait_sec=module.params["job_wait_timeout"])
            if job_failed is True:
                module.fail_json(msg=FAIL_MSG)
            job_success_resp = rest_obj.invoke_request("GET", QUICK_DEPLOY_API.format(device_id, settings_type))
            job_success_data = rest_obj.strip_substr_dict(job_success_resp.json_data)
    return job_id, job_success_data


def main():
    slots = {
        "slot_id": {"required": True, "type": "int"},
        "slot_ipv4_address": {"type": "str"},
        "slot_ipv6_address": {"type": "str"},
        "vlan_id": {"type": "int"},
    }
    quick_deploy = {
        "password": {"type": "str", "no_log": True},
        "ipv4_enabled": {"type": "bool"},
        "ipv4_network_type": {"type": "str", "choices": ["Static", "DHCP"]},
        "ipv4_subnet_mask": {"type": "str"},
        "ipv4_gateway": {"type": "str"},
        "ipv6_enabled": {"type": "bool"},
        "ipv6_network_type": {"type": "str", "choices": ["Static", "DHCP"]},
        "ipv6_prefix_length": {"type": "int"},
        "ipv6_gateway": {"type": "str"},
        "slots": {"type": "list", "elements": "dict", "options": slots},
    }
    specs = {
        "device_id": {"required": False, "type": "int"},
        "device_service_tag": {"required": False, "type": "str"},
        "setting_type": {"required": True, "choices": ["ServerQuickDeploy", "IOMQuickDeploy"]},
        "quick_deploy_options": {
            "type": "dict", "required": True, "options": quick_deploy,
            "required_if": [
                ["ipv4_enabled", True, ["ipv4_network_type"]],
                ["ipv4_network_type", "Static", ["ipv4_subnet_mask", "ipv4_gateway"]],
                ["ipv6_enabled", True, ["ipv6_network_type"]],
                ["ipv6_network_type", "Static", ["ipv6_prefix_length", "ipv6_gateway"]],
            ],
        },
        "job_wait": {"type": "bool", "default": True},
        "job_wait_timeout": {"type": "int", "default": 120},
    }
    specs.update(ome_auth_params)
    module = AnsibleModule(argument_spec=specs,
                           mutually_exclusive=[('device_id', 'device_service_tag')],
                           supports_check_mode=True,)
    if module.params["quick_deploy_options"] is None:
        module.fail_json(msg="missing required arguments: quick_deploy_options")
    fields = [("ipv4_subnet_mask", "IPV4"), ("ipv4_gateway", "IPV4"), ("ipv6_gateway", "IPV6")]
    ip_address_field(module, fields, module.params["quick_deploy_options"], slot=False)
    slot_options = module.params["quick_deploy_options"].get("slots")
    if slot_options is not None:
        slot_field = [("slot_ipv4_address", "IPV4"), ("slot_ipv6_address", "IPV6")]
        for dep_opt in slot_options:
            ip_address_field(module, slot_field, dep_opt, slot=True)
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            check_domain_service(module, rest_obj)
            job_id, data = get_device_details(rest_obj, module)
            if job_id is not None and data is not None:
                module.exit_json(msg=SUCCESS_MSG, job_id=job_id, quick_deploy_settings=data, changed=True)
            module.exit_json(msg=JOB_MSG, job_id=job_id)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError,
            AttributeError, IndexError, KeyError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
