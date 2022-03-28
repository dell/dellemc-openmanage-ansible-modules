#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.2.0
# Copyright (C) 2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_application_console_preferences
short_description: Configure console preferences on OpenManage Enterprise.
description: This module allows user to configure the console preferences on OpenManage Enterprise.
version_added: "5.2.0"
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  report_row_limit:
    description: The maximum number of rows that you can view on OpenManage Enterprise reports.
    type: int
  device_health:
    description: The time after which the health of the devices must be automatically monitored and updated
      on the OpenManage Enterprise dashboard.
    type: dict
    suboptions:
      health_check_interval:
        description: The frequency at which the device health must be recorded and data stored.
        type: int
      health_check_interval_unit:
        description:
          - The time unit of the frequency at which the device health must be recorded and data stored.
          - C(Hourly) to set the frequency in hours.
          - C(Minutes) to set the frequency in minutes.
        type: str
        choices: [Hourly, Minutes]
      health_and_power_state_on_connection_lost:
        description:
          - The latest recorded device health.
          - C(last_known) to display the latest recorded device health when the power connection was lost.
          - C(unknown) to display the latest recorded device health when the device status moved to unknown.
        type: str
        choices: [last_known, unknown]
  discovery_settings:
    description: The device naming to be used by the OpenManage Enterprise to identify the discovered iDRACs
      and other devices.
    type: dict
    suboptions:
      general_device_naming:
        description:
          - Applicable to all the discovered devices other than the iDRACs.
          - C(DNS) to use the DNS name.
          - C(NETBIOS) to use the NetBIOS name.
        type: str
        choices: [DNS, NETBIOS]
        default: DNS
      server_device_naming:
        description:
          - Applicable to iDRACs only.
          - C(IDRAC_HOSTNAME) to use the iDRAC hostname.
          - C(IDRAC_SYSTEM_HOSTNAME) to use the system hostname.
        type: str
        choices: [IDRAC_HOSTNAME, IDRAC_SYSTEM_HOSTNAME]
        default: IDRAC_SYSTEM_HOSTNAME
      invalid_device_hostname:
        description: The invalid hostnames separated by a comma.
        type: str
      common_mac_addresses:
        description: The common MAC addresses separated by a comma.
        type: str
  server_initiated_discovery:
    description: Server initiated discovery settings.
    type: dict
    suboptions:
      device_discovery_approval_policy:
        description:
          - Discovery approval policies.
          - "C(Automatic) allows servers with iDRAC Firmware version 4.00.00.00, which are on the same network as the
            console, to be discovered automatically by the console."
          - C(Manual) for the servers to be discovered by the user manually.
        type: str
        choices: [Automatic, Manual]
      set_trap_destination:
        description: Trap destination settings.
        type: bool
  mx7000_onboarding_preferences:
    description:
      - Alert-forwarding behavior on chassis when they are onboarded.
      - C(all) to receive all alert.
      - C(chassis) to receive chassis category alerts only.
    type: str
    choices: [all, chassis]
  builtin_appliance_share:
    description: The external network share that the appliance must access to complete operations.
    type: dict
    suboptions:
      share_options:
        description:
          - The share options.
          - C(CIFS) to select CIFS share type.
          - C(HTTPS) to select HTTPS share type.
        type: str
        choices: [CIFS, HTTPS]
      cifs_options:
        description:
          - The SMB protocol version.
          - I(cifs_options) is required I(share_options) is C(CIFS).
          - C(V1) to enable SMBv1.
          - C(V2) to enable SMBv2
        type: str
        choices: [V1, V2]
  email_sender_settings:
    description: The email address of the user who is sending an email message.
    type: str
  trap_forwarding_format:
    description:
      - The trap forwarding format.
      - C(Original) to retain the trap data as is.
      - C(Normalized) to normalize the trap data.
    type: str
    choices: [Original, Normalized]
  metrics_collection_settings:
    description: The frequency of the PowerManager extension data maintenance and purging.
    type: int
requirements:
  - "python >= 3.8.6"
notes:
  - This module supports C(check_mode).
author:
  - Sachin Apagundi(@sachin-apa)
  - Husniya Hameed (@husniya-hameed)
'''

EXAMPLES = r'''
---
- name: Update Console preferences with all the settings.
  dellemc.openmanage.ome_application_console_preferences:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    report_row_limit: 123
    device_health:
      health_check_interval: 1
      health_check_interval_unit: Hourly
      health_and_power_state_on_connection_lost: last_known
    discovery_settings:
      general_device_naming: DNS
      server_device_naming: IDRAC_HOSTNAME
      invalid_device_hostname: "localhost"
      common_mac_addresses: "::"
    server_initiated_discovery:
      device_discovery_approval_policy: Automatic
      set_trap_destination: True
    mx7000_onboarding_preferences: all
    builtin_appliance_share:
      share_options: CIFS
      cifs_options: V1
    email_sender_settings: "admin@dell.com"
    trap_forwarding_format: Normalized
    metrics_collection_settings: 31

- name: Update Console preferences with report and device health settings.
  dellemc.openmanage.ome_application_console_preferences:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    report_row_limit: 236
    device_health:
      health_check_interval: 10
      health_check_interval_unit: Hourly
      health_and_power_state_on_connection_lost: last_known

- name: Update Console preferences with invalid device health settings.
  dellemc.openmanage.ome_application_console_preferences:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_health:
      health_check_interval: 65
      health_check_interval_unit: Minutes

- name: Update Console preferences with discovery and built in appliance share settings.
  dellemc.openmanage.ome_application_console_preferences:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    discovery_settings:
      general_device_naming: DNS
      server_device_naming: IDRAC_SYSTEM_HOSTNAME
      invalid_device_hostname: "localhost"
      common_mac_addresses: "00:53:45:00:00:00"
    builtin_appliance_share:
      share_options: CIFS
      cifs_options: V1

- name: Update Console preferences with server initiated discovery, mx7000 onboarding preferences, email sender,
    trap forwarding format, and metrics collection settings.
  dellemc.openmanage.ome_application_console_preferences:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    server_initiated_discovery:
      device_discovery_approval_policy: Automatic
      set_trap_destination: True
    mx7000_onboarding_preferences: chassis
    email_sender_settings: "admin@dell.com"
    trap_forwarding_format: Original
    metrics_collection_settings: 365
'''

RETURN = r'''
---
msg:
  type: str
  description: Overall status of the console preferences.
  returned: always
  sample: "Successfully update the console preferences."
console_preferences:
  type: list
  description: Details of the console preferences.
  returned: on success
  sample:
   [
   {
    "Name": "DEVICE_PREFERRED_NAME",
    "DefaultValue": "SLOT_NAME",
    "Value": "PREFER_DNS,PREFER_IDRAC_SYSTEM_HOSTNAME",
    "DataType": "java.lang.String",
    "GroupName": "DISCOVERY_SETTING"
    },
    {
    "Name": "INVALID_DEVICE_HOSTNAME",
    "DefaultValue": "",
    "Value": "localhost,localhost.localdomain,not defined,pv132t,pv136t,default,dell,idrac-",
    "DataType": "java.lang.String",
    "GroupName": "DISCOVERY_SETTING"
   },
   {
    "Name": "COMMON_MAC_ADDRESSES",
    "DefaultValue": "",
    "Value": "00:53:45:00:00:00,33:50:6F:45:30:30,50:50:54:50:30:30,00:00:FF:FF:FF:FF,20:41:53:59:4E:FF,00:00:00:00:00:00,20:41:53:59:4e:ff,00:00:00:00:00:00",
    "DataType": "java.lang.String",
    "GroupName": "DISCOVERY_SETTING"
   },
   {
    "Name": "SHARE_TYPE",
    "DefaultValue": "CIFS",
    "Value": "CIFS",
    "DataType": "java.lang.String",
    "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"
   },
   {
    "Name": "TRAP_FORWARDING_SETTING",
    "DefaultValue": "AsIs",
    "Value": "Normalized",
    "DataType": "java.lang.String",
    "GroupName": ""
   },
   {
    "Name": "DATA_PURGE_INTERVAL",
    "DefaultValue": "365",
    "Value": "3650000",
    "DataType": "java.lang.Integer",
    "GroupName": ""
   },
   {
    "Name": "CONSOLE_CONNECTION_SETTING",
    "DefaultValue": "last_known",
    "Value": "last_known",
    "DataType": "java.lang.String",
    "GroupName": "CONSOLE_CONNECTION_SETTING"
   },
   {
    "Name": "MIN_PROTOCOL_VERSION",
    "DefaultValue": "V2",
    "Value": "V1",
    "DataType": "java.lang.String",
    "GroupName": "CIFS_PROTOCOL_SETTINGS"
   },
   {
    "Name": "ALERT_ACKNOWLEDGEMENT_VIEW",
    "DefaultValue": "2000",
    "Value": "2000",
    "DataType": "java.lang.Integer",
    "GroupName": ""
   },
   {
    "Name": "AUTO_CONSOLE_UPDATE_AFTER_DOWNLOAD",
    "DefaultValue": "false",
    "Value": "false",
    "DataType": "java.lang.Boolean",
    "GroupName": "CONSOLE_UPDATE_SETTING_GROUP"
   },
   {
    "Name": "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION",
    "DefaultValue": "false",
    "Value": "false",
    "DataType": "java.lang.Boolean",
    "GroupName": ""
   },
   {
    "Name": "REPORTS_MAX_RESULTS_LIMIT",
    "DefaultValue": "0",
    "Value": "2000000000000000000000000",
    "DataType": "java.lang.Integer",
    "GroupName": ""
   },
   {
    "Name": "EMAIL_SENDER",
    "DefaultValue": "omcadmin@dell.com",
    "Value": "admin1@dell.com@dell.com@dell.com",
    "DataType": "java.lang.String",
    "GroupName": ""
   },
   {
    "Name": "MX7000_ONBOARDING_PREF",
    "DefaultValue": "all",
    "Value": "test_chassis",
    "DataType": "java.lang.String",
    "GroupName": ""
   },
   {
    "Name": "DISCOVERY_APPROVAL_POLICY",
    "DefaultValue": "Automatic",
    "Value": "Automatic_test",
    "DataType": "java.lang.String",
    "GroupName": ""
   }
   ]
error_info:
  description: Details of the HTTP error.
  returned: on HTTP error
  type: dict
  sample:
    {
  "error": {
    "code": "Base.1.0.GeneralError",
    "message": "A general error has occurred. See ExtendedInfo for more information.",
    "@Message.ExtendedInfo": [
      {
        "MessageId": "CGEN1006",
        "RelatedProperties": [],
        "Message": "Unable to complete the request because the resource URI does not exist or is not implemented.",
        "MessageArgs": [],
        "Severity": "Critical",
        "Resolution": "Enter a valid URI and retry the operation."
      }
      ]
      }
      }
'''

import json
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import strip_substr_dict

SUCCESS_MSG = "Successfully updated the Console Preferences settings."
SETTINGS_URL = "ApplicationService/Settings"
NO_CHANGES = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
HEALTH_CHECK_UNIT_REQUIRED = "The health check unit is required when health check interval is specified."
HEALTH_CHECK_INTERVAL_REQUIRED = "The health check interval is required when health check unit is specified."
HEALTH_CHECK_INTERVAL_INVALID = "The health check interval specified is invalid for the {0}"
JOB_URL = "JobService/Jobs"
CIFS_URL = "ApplicationService/Actions/ApplicationService.UpdateShareTypeSettings"
CONSOLE_SETTINGS_VALUES = ["DATA_PURGE_INTERVAL", "EMAIL_SENDER", "TRAP_FORWARDING_SETTING",
                           "MX7000_ONBOARDING_PREF", "REPORTS_MAX_RESULTS_LIMIT",
                           "DISCOVERY_APPROVAL_POLICY", "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION",
                           "DEVICE_PREFERRED_NAME", "INVALID_DEVICE_HOSTNAME", "COMMON_MAC_ADDRESSES",
                           "CONSOLE_CONNECTION_SETTING", "MIN_PROTOCOL_VERSION", "SHARE_TYPE"]


def job_details(rest_obj):
    query_param = {"$filter": "JobType/Id eq 6"}
    job_resp = rest_obj.invoke_request("GET", JOB_URL, query_param=query_param)
    job_data = job_resp.json_data.get('value')
    tmp_list = [x["Id"] for x in job_data]
    sorted_id = sorted(tmp_list)
    latest_job = [val for val in job_data if val["Id"] == sorted_id[-1]]
    return latest_job[0]


def create_job(module):
    schedule = None
    job_payload = None
    device_health = module.params.get("device_health")
    if device_health:
        if device_health.get("health_check_interval_unit") == "Hourly":
            schedule = "0 0 0/" + str(device_health.get("health_check_interval")) + " 1/1 * ? *"
        elif device_health.get("health_check_interval_unit") == "Minutes":
            schedule = "0 0/" + str(device_health.get("health_check_interval")) + " * 1/1 * ? *"
        job_payload = {"Id": 0,
                       "JobName": "Global Health Task",
                       "JobDescription": "Global Health Task",
                       "Schedule": schedule,
                       "State": "Enabled",
                       "JobType": {"Id": 6, "Name": "Health_Task"},
                       "Params": [{"Key": "metricType", "Value": "40, 50"}],
                       "Targets": [{"Id": 500, "Data": "", "TargetType": {"Id": 6000, "Name": "GROUP"}}]}
    return job_payload, schedule


def fetch_cp_settings(rest_obj):
    final_resp = rest_obj.invoke_request("GET", SETTINGS_URL)
    ret_data = final_resp.json_data.get('value')
    return ret_data


def create_payload_dict(curr_payload):
    payload = {}
    for pay in curr_payload:
        payload[pay["Name"]] = pay
    return payload


def create_payload(module, curr_payload):
    console_setting_list = []
    updated_payload = {"ConsoleSetting": []}
    payload_dict = create_payload_dict(curr_payload)
    get_sid = module.params.get("server_initiated_discovery")
    get_ds = module.params.get("discovery_settings")
    get_mcs = module.params.get("metrics_collection_settings")
    get_email = module.params.get("email_sender_settings")
    get_tff = module.params.get("trap_forwarding_format")
    get_mx = module.params.get("mx7000_onboarding_preferences")
    get_rrl = module.params.get("report_row_limit")
    get_dh = module.params.get("device_health")
    get_bas = module.params.get("builtin_appliance_share")
    if get_mcs:
        payload1 = payload_dict["DATA_PURGE_INTERVAL"].copy()
        payload1["Value"] = get_mcs
        console_setting_list.append(payload1)
    if get_email:
        payload2 = payload_dict["EMAIL_SENDER"].copy()
        payload2["Value"] = get_email
        console_setting_list.append(payload2)
    if get_tff:
        dict1 = {"Original": "AsIs", "Normalized": "Normalized"}
        payload3 = payload_dict["TRAP_FORWARDING_SETTING"].copy()
        payload3["Value"] = dict1.get(get_tff)
        console_setting_list.append(payload3)
    if get_mx:
        payload4 = payload_dict["MX7000_ONBOARDING_PREF"].copy()
        payload4["Value"] = get_mx
        console_setting_list.append(payload4)
    if get_rrl:
        payload5 = payload_dict["REPORTS_MAX_RESULTS_LIMIT"].copy()
        payload5["Value"] = get_rrl
        console_setting_list.append(payload5)
    if get_sid:
        if get_sid.get("device_discovery_approval_policy"):
            payload6 = payload_dict["DISCOVERY_APPROVAL_POLICY"].copy()
            payload6["Value"] = get_sid.get("device_discovery_approval_policy")
            console_setting_list.append(payload6)
        if get_sid.get("set_trap_destination") is not None:
            payload7 = payload_dict["NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION"].copy()
            payload7["Value"] = get_sid.get("set_trap_destination")
            console_setting_list.append(payload7)
    if get_ds:
        if get_ds.get("general_device_naming") and get_ds.get("server_device_naming"):
            value = "PREFER_" + module.params["discovery_settings"]["general_device_naming"] + "," + "PREFER_" +\
                    get_ds["server_device_naming"]
            payload8 = payload_dict["DEVICE_PREFERRED_NAME"].copy()
            payload8["Value"] = value
            console_setting_list.append(payload8)
        elif get_ds.get("general_device_naming"):
            payload9 = payload_dict["DEVICE_PREFERRED_NAME"].copy()
            payload9["Value"] = "PREFER_" + get_ds["general_device_naming"]
            console_setting_list.append(payload9)
        elif get_ds.get("server_device_naming"):
            payload10 = payload_dict["DEVICE_PREFERRED_NAME"].copy()
            payload10["Value"] = "PREFER_" + get_ds["server_device_naming"]
            console_setting_list.append(payload10)
        if get_ds.get("invalid_device_hostname"):
            payload11 = payload_dict["INVALID_DEVICE_HOSTNAME"].copy()
            payload11["Value"] = get_ds.get("invalid_device_hostname")
            console_setting_list.append(payload11)
        if get_ds.get("common_mac_addresses"):
            payload12 = payload_dict["COMMON_MAC_ADDRESSES"].copy()
            payload12["Value"] = get_ds.get("common_mac_addresses")
            console_setting_list.append(payload12)
    if get_dh and get_dh.get("health_and_power_state_on_connection_lost"):
        payload13 = payload_dict["CONSOLE_CONNECTION_SETTING"].copy()
        payload13["Value"] = get_dh.get("health_and_power_state_on_connection_lost")
        console_setting_list.append(payload13)
    if get_bas and get_bas.get("share_options") == "CIFS":
        payload14 = payload_dict["MIN_PROTOCOL_VERSION"].copy()
        payload14["Value"] = get_bas.get("cifs_options")
        console_setting_list.append(payload14)
    updated_payload["ConsoleSetting"] = console_setting_list
    return updated_payload, payload_dict


def create_cifs_payload(module, curr_payload):
    console_setting_list = []
    updated_payload = {"ConsoleSetting": []}
    payload_dict = create_payload_dict(curr_payload)
    get_bas = module.params.get("builtin_appliance_share")
    if get_bas and get_bas.get("share_options"):
        payload = payload_dict["SHARE_TYPE"].copy()
        payload["Value"] = get_bas.get("share_options")
        console_setting_list.append(payload)
    updated_payload["ConsoleSetting"] = console_setting_list
    return updated_payload


def update_console_preferences(module, rest_obj, payload, payload_cifs, job_payload, job, payload_dict, schedule):
    cifs_resp = None
    job_final_resp = None
    get_bas = module.params.get("builtin_appliance_share")
    device_health = module.params.get("device_health")
    [payload["ConsoleSetting"].remove(i) for i in payload["ConsoleSetting"] if i["Name"] == "SHARE_TYPE"]
    if device_health and device_health.get("health_check_interval_unit") and job["Schedule"] != schedule:
        job_final_resp = rest_obj.invoke_request("POST", JOB_URL, data=job_payload)
    if get_bas and get_bas.get("share_options") and payload_dict["SHARE_TYPE"]["Value"] != \
            get_bas.get("share_options"):
        cifs_resp = rest_obj.invoke_request("POST", CIFS_URL, data=payload_cifs)
    final_resp = rest_obj.invoke_request("POST", SETTINGS_URL, data=payload)
    return final_resp, cifs_resp, job_final_resp


def _diff_payload(curr_resp, update_resp, payload_cifs, schedule, job_det):
    diff = 0
    update_resp["ConsoleSetting"].extend(payload_cifs["ConsoleSetting"])
    if schedule and job_det["Schedule"] != schedule:
        diff += 1
    for i in curr_resp:
        for j in update_resp["ConsoleSetting"]:
            if i["Name"] == j["Name"]:
                if isinstance(j["Value"], bool):
                    j["Value"] = str(j["Value"]).lower()
                if isinstance(j["Value"], int):
                    j["Value"] = str(j["Value"])
                if i["Value"] != j["Value"]:
                    diff += 1
    return diff


def process_check_mode(module, diff):
    if not diff:
        module.exit_json(msg=NO_CHANGES)
    elif diff and module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)


def _validate_params(module):
    error_message = _validate_health_check_interval(module)
    if error_message:
        module.fail_json(msg=error_message)


def _validate_health_check_interval(module):
    error_message = None
    device_health = module.params.get("device_health")
    if device_health:
        hci = device_health.get("health_check_interval")
        hciu = device_health.get("health_check_interval_unit")
        if hci and not hciu:
            error_message = HEALTH_CHECK_UNIT_REQUIRED
        if hciu and not hci:
            error_message = HEALTH_CHECK_INTERVAL_REQUIRED
        if hciu and hci:
            if hciu == "Hourly" and (hci < 1 or hci > 23):
                error_message = HEALTH_CHECK_INTERVAL_INVALID.format(hciu)
            if hciu == "Minutes" and (hci < 1 or hci > 59):
                error_message = HEALTH_CHECK_INTERVAL_INVALID.format(hciu)
    return error_message


def main():
    device_health_opt = {"health_check_interval": {"type": "int", "required": False},
                         "health_check_interval_unit": {"type": "str", "required": False,
                                                        "choices": ["Hourly", "Minutes"]},
                         "health_and_power_state_on_connection_lost": {"type": "str", "required": False,
                                                                       "choices": ["last_known", "unknown"]}
                         }
    discovery_settings_opt = {
        "general_device_naming": {"type": "str", "required": False, "default": "DNS",
                                  "choices": ["DNS", "NETBIOS"]},
        "server_device_naming": {"type": "str", "required": False, "default": "IDRAC_SYSTEM_HOSTNAME",
                                 "choices": ["IDRAC_HOSTNAME", "IDRAC_SYSTEM_HOSTNAME"]},
        "invalid_device_hostname": {"type": "str", "required": False},
        "common_mac_addresses": {"type": "str", "required": False}
    }
    server_initiated_discovery_opt = {
        "device_discovery_approval_policy": {"type": "str", "required": False, "choices": ["Automatic", "Manual"]},
        "set_trap_destination": {"type": "bool", "required": False, },
    }
    builtin_appliance_share_opt = {
        "share_options": {"type": "str", "required": False,
                          "choices": ["CIFS", "HTTPS"]},
        "cifs_options": {"type": "str", "required": False,
                         "choices": ["V1", "V2"]
                         },
    }

    specs = {
        "report_row_limit": {"required": False, "type": "int"},
        "device_health": {"required": False, "type": "dict",
                          "options": device_health_opt
                          },
        "discovery_settings": {"required": False, "type": "dict",
                               "options": discovery_settings_opt
                               },
        "server_initiated_discovery": {"required": False, "type": "dict",
                                       "options": server_initiated_discovery_opt
                                       },
        "mx7000_onboarding_preferences": {"required": False, "type": "str", "choices": ["all", "chassis"]},
        "builtin_appliance_share": {"required": False, "type": "dict",
                                    "options": builtin_appliance_share_opt,
                                    "required_if": [['share_options', "CIFS", ('cifs_options',)]]
                                    },
        "email_sender_settings": {"required": False, "type": "str"},
        "trap_forwarding_format": {"required": False, "type": "str", "choices": ["Normalized", "Original"]},
        "metrics_collection_settings": {"required": False, "type": "int"},
    }
    specs.update(ome_auth_params)
    module = AnsibleModule(argument_spec=specs,
                           required_one_of=[["report_row_limit", "device_health", "discovery_settings",
                                             "server_initiated_discovery", "mx7000_onboarding_preferences",
                                             "builtin_appliance_share", "email_sender_settings",
                                             "trap_forwarding_format", "metrics_collection_settings"]],
                           supports_check_mode=True, )

    try:
        _validate_params(module)
        with RestOME(module.params, req_session=True) as rest_obj:
            job = job_details(rest_obj)
            job_payload, schedule = create_job(module)
            curr_resp = fetch_cp_settings(rest_obj)
            payload, payload_dict = create_payload(module, curr_resp)
            cifs_payload = create_cifs_payload(module, curr_resp)
            diff = _diff_payload(curr_resp, payload, cifs_payload, schedule, job)
            process_check_mode(module, diff)
            resp, cifs_resp, job_resp = update_console_preferences(module, rest_obj, payload, cifs_payload,
                                                                   job_payload, job, payload_dict, schedule)
            resp_req = fetch_cp_settings(rest_obj)
            cp_list = []
            resp_data = list(filter(lambda d: d['Name'] in CONSOLE_SETTINGS_VALUES, resp_req))
            for cp in resp_data:
                cp_data = strip_substr_dict(cp)
                cp_list.append(cp_data)
            module.exit_json(msg=SUCCESS_MSG, console_preferences=cp_list)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, AttributeError, IndexError, KeyError, OSError) as err:
        module.fail_json(msg=str(err), error_info=json.load(err))


if __name__ == '__main__':
    main()
