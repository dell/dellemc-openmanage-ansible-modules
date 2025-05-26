#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2023-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_alert_policies
short_description: Manage OME alert policies.
version_added: "8.3.0"
description: This module allows you to create, modify, or delete alert policies on OpenManage Enterprise or OpenManage Enterprise Modular.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  name:
    description:
      - Name of an alert policy or a list of alert policies.
      - More than one policy name is applicable when I(state) is C(absent) and I(state) is C(present) with only I(enable) provided.
    type: list
    elements: str
    required: true
  state:
    description:
      - C(present) allows you to create an alert policy or update if the policy name already exists.
      - C(absent) allows you to delete an alert policy.
    default: present
    choices: [present, absent]
    type: str
  enable:
    description:
      - C(true) allows you to enable an alert policy.
      - C(false) allows you to disable an alert policy.
      - This is applicable only when I(state) is C(present).
    type: bool
  new_name:
    description:
      - New name for the alert policy.
      - This is applicable only when I(state) is C(present), and an alert policy exists.
    type: str
  description:
    description:
      - Description for the alert policy.
      - This is applicable only when I(state) is C(present)
    type: str
  device_service_tag:
    description:
      - List of device service tags on which the alert policy will be applicable.
      - This option is mutually exclusive with I(device_group), I(specific_undiscovered_devices), I(any_undiscovered_devices) and I(all_devices).
      - This is applicable only when I(state) is C(present)
    type: list
    elements: str
  device_group:
    description:
      - List of device group names on which the alert policy is applicable.
      - This option is mutually exclusive with I(device_service_tag), I(specific_undiscovered_devices), I(any_undiscovered_devices) and I(all_devices) .
      - This is applicable only when I(state) is C(present)
    type: list
    elements: str
  specific_undiscovered_devices:
    description:
      - List of undiscovered IPs, hostnames, or range of IPs of devices on which the alert policy is applicable.
      - This option is mutually exclusive with I(device_service_tag), I(device_group), I(any_undiscovered_devices) and I(all_devices) .
      - This is applicable only when I(state) is C(present)
      - "Examples of valid IP range format:"
      - "     10.35.0.0"
      - "     10.36.0.0-10.36.0.255"
      - "     10.37.0.0/24"
      - "     2607:f2b1:f083:135::5500/118"
      - "     2607:f2b1:f083:135::a500-2607:f2b1:f083:135::a600"
      - "     hostname.domain.com"
      - "Examples of invalid IP range format:"
      - "     10.35.0.*"
      - "     10.36.0.0-255"
      - "     10.35.0.0/255.255.255.0"
      - These values will not be validated.
    type: list
    elements: str
  any_undiscovered_devices:
    description:
      - This option indicates whether the alert policy is applicable to any undiscovered devices or not.
      - This option is mutually exclusive with I(device_service_tag), I(specific_undiscovered_devices), I(device_group) and I(all_devices).
      - This is applicable only when I(state) is C(present).
    type: bool
  all_devices:
    description:
      - This option indicates whether the alert policy is applicable to all the discovered and undiscovered devices or not.
      - This option is mutually exclusive with I(device_service_tag), I(specific_undiscovered_devices), I(any_undiscovered_devices) and I(device_group).
      - This is applicable only when I(state) is C(present).
    type: bool
  category:
    description:
      - Category of the alerts received.
      - This is mutually exclusive with the I(message_ids), I(message_file).
      - This is fetched from the M(dellemc.openmanage.ome_alert_policies_category_info).
      - This is applicable only when I(state) is C(present).
    type: list
    elements: dict
    suboptions:
      catalog_name:
        description: Name of the catalog.
        type: str
        required: true
      catalog_category:
        description: Category of the catalog.
        type: list
        elements: dict
        suboptions:
          category_name:
            description: Name of the category.
            type: str
          sub_category_names:
            description: List of sub-categories.
            type: list
            elements: str
  message_ids:
    description:
      - List of Message ids
      - This is mutually exclusive with the I(category), I(message_file)
      - This is applicable only when I(state) is C(present)
      - This is fetched from the M(dellemc.openmanage.ome_alert_policies_message_id_info).
    type: list
    elements: str
  message_file:
    description:
      - Local path of a CSV formatted file with message IDs
      - This is mutually exclusive with the I(category), I(message_ids)
      - This is applicable only when I(state) is C(present)
      - This is fetched from the M(dellemc.openmanage.ome_alert_policies_message_id_info).
    type: path
  date_and_time:
    description:
      - Specifies the schedule for when the alert policy is applicable.
      - I(date_and_time) is mandatory for creating a policy and optional when updating a policy.
      - This is applicable only when I(state) is C(present).
    type: dict
    suboptions:
      date_from:
        description:
          - "Start date in the format YYYY-MM-DD."
          - This parameter to be provided in quotes.
        type: str
        required: true
      date_to:
        description:
          - "End date in the format YYYY-MM-DD."
          - This parameter to be provided in quotes.
        type: str
      time_from:
        description:
          - "Interval start time in the format HH:MM"
          - This parameter to be provided in quotes.
          - This is mandatory when I(time_interval) is C(true).
        type: str
      time_to:
        description:
          - "Interval end time in the format HH:MM"
          - This parameter to be provided in quotes.
          - This is mandatory when I(time_interval) is C(true)
        type: str
      days:
        description: Required days of the week on which alert policy operation must be scheduled.
        type: list
        elements: str
        choices: [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
      time_interval:
        description: Enable the time interval for which alert policy must be scheduled.
        type: bool
  severity:
    description:
      - Severity of the alert policy.
      - This is mandatory for creating a policy and optional for updating a policy.
      - This is applicable only when I(state) is C(present).
    type: list
    elements: str
    choices: [all, unknown, info, normal, warning, critical]
  actions:
    description:
      - Actions to be triggered for the alert policy.
      - This parameter is case-sensitive.
      - This is mandatory for creating a policy and optional for updating a policy.
      - This is applicable only when I(state) is C(present)
    type: list
    elements: dict
    suboptions:
      action_name:
        description:
          - Name of the action.
          - This is fetched from the M(dellemc.openmanage.ome_alert_policies_action_info).
          - This is mandatory for creating a policy and optional for updating a policy.
          - This parameter is case-sensitive.
        type: str
        required: true
      parameters:
        description:
          - Predefined parameters required to set for I(action_name).
        type: list
        elements: dict
        default: []
        suboptions:
          name:
            description:
              - Name of the predefined parameter.
              - This is fetched from the M(dellemc.openmanage.ome_alert_policies_action_info).
            type: str
          value:
            description:
             - Value of the predefined parameter.
             - These values will not be validated.
            type: str
requirements:
    - "python >= 3.9.6"
author: "Jagadeesh N V(@jagadeeshnv)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise
      or OpenManage Enterprise Modular.
    - This module supports IPv4 and IPv6 addresses.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: "Create an alert policy"
  dellemc.openamanage.ome_alert_policies:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    name: "Alert Policy One"
    device_service_tag:
      - ABCD123
      - SVC7845
    category:
      - catalog_name: Application
        catalog_category:
          - category_name: Audit
            sub_category_names:
              - Generic
              - Devices
      - catalog_name: iDRAC
        catalog_category:
          - category_name: Audit
            sub_category_names:
              - BIOS Management
              - iDRAC Service Module
    date_and_time:
      date_from: "2023-10-10"
      date_to: "2023-10-11"
      time_from: "11:00"
      time_to: "12:00"
    severity:
      - unknown
      - critical
    actions:
      - action_name: Trap
        parameters:
          - name: "192.1.2.3:162"
            value: true
          - name: "traphostname.domain.com:162"
            value: true
  tags: create_alert_policy

- name: "Update an alert Policy"
  dellemc.openamanage.ome_alert_policies:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    new_name: "Update Policy Name"
    device_group: "Group Name"
    message_ids:
      - AMP400
      - CTL201
      - BIOS101
    date_and_time:
      date_from: "2023-10-10"
      date_to: "2023-10-11"
      time_from: "11:00"
      time_to: "12:00"
      time_interval: true
    actions:
      - action_name: Trap
        parameters:
          - name: "192.1.2.3:162"
            value: true
  tags: update_alert_policy

- name: "Enable an alert policy"
  dellemc.openamanage.ome_alert_policies:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    name: "Policy Name"
    enable: true
  tags: enable_alert_policy

- name: "Disable multiple alert policies"
  dellemc.openamanage.ome_alert_policies:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    name:
      - "Policy Name 1"
      - "Policy Name 2"
    enable: false
  tags: disable_alert_policy

- name: "Delete an alert policy"
  dellemc.openamanage.ome_alert_policies:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    name:
      - "Policy Name"
    state: absent
  tags: delete_alert_policy
'''

RETURN = r'''
---
msg:
  type: str
  description: Status of the alert policies operation.
  returned: always
  sample: "Successfully created the alert policy."
status:
  type: dict
  description: The policy which was created or modified.
  returned: when state is present
  sample: {
    "Id": 12345,
    "Name": "Policy",
    "Description": "Details of the Policy",
    "Enabled": true,
    "DefaultPolicy": false,
    "Editable": true,
    "Visible": true,
    "PolicyData": {
        "Catalogs": [
        {
            "CatalogName": "iDRAC",
            "Categories": [
            4
            ],
            "SubCategories": [
            41
            ]
        },
        {
            "CatalogName": "Application",
            "Categories": [
            0
            ],
            "SubCategories": [
            0
            ]
        }
        ],
        "Severities": [
        16,
        1,
        2,
        4,
        8
        ],
        "Devices": [
        10086,
        10088
        ],
        "DeviceTypes": [
        1000,
        2000
        ],
        "Groups": [],
        "Schedule": {
        "StartTime": "2023-06-06 15:02:46.000",
        "EndTime": "2023-06-06 18:02:46.000",
        "CronString": "* * * ? * * *"
        },
        "Actions": [
        {
            "Id": 8,
            "Name": "Email",
            "ParameterDetails": [
            {
                "Id": 1,
                "Name": "subject",
                "Value": "Device Name: $name,  Device IP Address: $ip,  Severity: $severity",
                "Type": "string",
                "TypeParams": [
                {
                    "Name": "maxLength",
                    "Value": "255"
                }
                ]
            },
            {
                "Id": 1,
                "Name": "to",
                "Value": "test@org.com",
                "Type": "string",
                "TypeParams": [
                {
                    "Name": "maxLength",
                    "Value": "255"
                }
                ]
            },
            {
                "Id": 1,
                "Name": "from",
                "Value": "abc@corp.com",
                "Type": "string",
                "TypeParams": [
                {
                    "Name": "maxLength",
                    "Value": "255"
                }
                ]
            },
            {
                "Id": 1,
                "Name": "message",
                "Value": "Event occurred for Device Name: $name, Device IP Address: $ip",
                "Type": "string",
                "TypeParams": [
                {
                    "Name": "maxLength",
                    "Value": "255"
                }
                ]
            }
            ]
        }
        ],
        "UndiscoveredTargets": [],
        "State": true,
        "Owner": 10069
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
                "MessageId": "CMON7011",
                "RelatedProperties": [],
                "Message": "Unable to create or modify the alert policy because an invalid value [To Email] is entered for the action Email.",
                "MessageArgs": [
                    "[To Email]",
                    "Email"
                ],
                "Severity": "Warning",
                "Resolution": "Enter a valid value for the action identified in the message and retry the operation."
            }
        ]
    }
}
'''

import csv
import os
import json
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import get_all_data_with_pagination, strip_substr_dict
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.common.dict_transformations import recursive_diff
from datetime import datetime


POLICIES_URI = "AlertService/AlertPolicies"
MESSAGES_URI = "AlertService/AlertMessageDefinitions"
ACTIONS_URI = "AlertService/AlertActionTemplates"
SEVERITY_URI = "AlertService/AlertSeverities"
DEVICES_URI = "DeviceService/Devices"
GROUPS_URI = "GroupService/Groups"
REMOVE_URI = "AlertService/Actions/AlertService.RemoveAlertPolicies"
ENABLE_URI = "AlertService/Actions/AlertService.EnableAlertPolicies"
DISABLE_URI = "AlertService/Actions/AlertService.DisableAlertPolicies"
CATEGORY_URI = "AlertService/AlertCategories"
SUCCESS_MSG = "Successfully {0}d the alert policy."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_MSG = "Changes found to be applied."
INVALID_TIME = "The specified {0} date or {0} time `{1}` to schedule the policy is not valid. Enter a valid date and time."
END_START_TIME = "The end time `{0}` to schedule the policy must be greater than the start time `{1}`."
CATEGORY_FETCH_FAILED = "Unable to retrieve the category details from OpenManage Enterprise."
INVALID_TARGETS = "Specify target devices to apply the alert policy."
INVALID_CATEGORY_MESSAGE = "Specify  categories or message to create the alert policy."
INVALID_SCHEDULE = "Specify a date and time to schedule the alert policy."
INVALID_ACTIONS = "Specify alert actions for the alert policy."
INVALID_SEVERITY = "Specify the severity to create the alert policy."
MULTIPLE_POLICIES = "Unable to update the alert policies because the number of alert policies entered are more than " \
                    "one. The update policy operation supports only one alert policy at a time."
DISABLED_ACTION = "Action {0} is disabled. Enable it before applying to the alert policy."
ACTION_INVALID_PARAM = "The Action {0} attribute contains invalid parameter name {1}. The valid values are {2}."
ACTION_INVALID_VALUE = "The Action {0} attribute contains invalid value for {1} for parameter name {2}. The valid " \
                       "values are {3}."
ACTION_DIS_EXIST = "Action {0} does not exist."
SUBCAT_IN_CATEGORY = "The subcategory {0} does not exist in the category {1}."
CATEGORY_IN_CATALOG = "The category {0} does not exist in the catalog {1}."
OME_DATA_MSG = "The {0} with the following {1} do not exist: {2}."
CATALOG_DIS_EXIST = "The catalog {0} does not exist."
CSV_PATH = "The message file {0} does not exist."
DEFAULT_POLICY_DELETE = "The following default policies cannot be deleted: {0}."
POLICY_ENABLE_MISSING = "Unable to {0} the alert policies {1} because the policy names are invalid. Enter the valid " \
                        "alert policy names and retry the operation."
NO_POLICY_EXIST = "The alert policy does not exist."
SEPARATOR = ", "


def get_alert_policies(rest_obj, name_list):
    report = get_all_data_with_pagination(rest_obj, POLICIES_URI)
    all_policies = report.get("report_list", [])
    policies = []
    nameset = set(name_list)
    for policy in all_policies:
        if policy.get("Name") in nameset:
            policies.append(policy)
    return policies


def get_items_to_remove(filter_param, return_param_tuple, return_dict, all_items, mset):
    collector = set()
    for dev in all_items:
        k = dev.get(filter_param)
        if k in mset:
            for v in return_param_tuple:
                return_dict[v].append(dev.get(v))
            collector.add(k)
    return collector


def validate_ome_data(module, rest_obj, item_list, filter_param, return_param_tuple, ome_uri, item_name="Items"):
    mset = set(item_list)
    return_dict = {v: [] for v in return_param_tuple}
    # can be further optimized if len(mset) == 1
    resp = rest_obj.invoke_request("GET", ome_uri)
    all_items = resp.json_data.get("value", [])
    dvdr = len(all_items) if len(all_items) else 100
    collector = get_items_to_remove(filter_param, return_param_tuple, return_dict, all_items, mset)
    mset = mset - collector
    all_item_count = resp.json_data.get("@odata.count")
    next_link = resp.json_data.get("@odata.nextLink")
    if mset and next_link:
        if len(mset) < (all_item_count // dvdr):
            for item_id in mset:
                query_param = {"$filter": f"{filter_param} eq '{item_id}'"}
                resp = rest_obj.invoke_request('GET', ome_uri, query_param=query_param)
                one_item = resp.json_data.get("value", [])
                collector = collector | get_items_to_remove(filter_param, return_param_tuple, return_dict, one_item, mset)
            mset = mset - collector
        else:
            while next_link and mset:
                resp = rest_obj.invoke_request('GET', next_link.lstrip("/api"))
                all_items = resp.json_data.get("value", [])
                collector = get_items_to_remove(filter_param, return_param_tuple, return_dict, all_items, mset)
                mset = mset - collector
                next_link = resp.json_data.get("@odata.nextLink", None)
    if mset:
        module.exit_json(failed=True,
                         msg=OME_DATA_MSG.format(item_name, filter_param, SEPARATOR.join(mset)))
    ret_list = [(return_dict[id]) for id in return_param_tuple]
    return tuple(ret_list)


def get_target_payload(module, rest_obj):
    target_payload = {'AllTargets': False,
                      'DeviceTypes': [],
                      'Devices': [],
                      'Groups': [],
                      'UndiscoveredTargets': []}
    mparams = module.params
    target_provided = False
    if mparams.get('all_devices'):
        target_payload['AllTargets'] = True
        target_provided = True
    elif mparams.get('any_undiscovered_devices'):
        target_payload['UndiscoveredTargets'] = ["ALL_UNDISCOVERED_TARGETS"]
        target_provided = True
    elif mparams.get('specific_undiscovered_devices'):
        target_payload['UndiscoveredTargets'] = list(set(module.params.get('specific_undiscovered_devices')))
        target_payload['UndiscoveredTargets'].sort()
        target_provided = True
    elif mparams.get('device_service_tag'):
        devicetype, deviceids = validate_ome_data(module, rest_obj, mparams.get('device_service_tag'),
                                                  'DeviceServiceTag', ('Type', 'Id'), DEVICES_URI, 'devices')
        target_payload['Devices'] = deviceids
        target_payload['Devices'].sort()
        target_payload['DeviceTypes'] = list(set(devicetype))
        target_payload['DeviceTypes'].sort()
        target_provided = True
    elif mparams.get('device_group'):
        groups = validate_ome_data(module, rest_obj, mparams.get('device_group'), 'Name', ('Id',), GROUPS_URI, 'groups')
        target_payload['Groups'] = groups[0]
        target_payload['Groups'].sort()
        target_provided = True
    if not target_provided:
        target_payload = {}
    return target_payload


def get_category_data_tree(rest_obj):
    resp = rest_obj.invoke_request("GET", CATEGORY_URI)
    cat_raw = resp.json_data.get("value", [])
    cat_dict = dict(
        (category.get("Name"),
            dict((y.get("Name"),
                 {y.get("Id"): dict((z.get('Name'), z.get('Id')
                                     ) for z in y.get("SubCategoryDetails"))}
                  ) for y in category.get("CategoriesDetails")
                 )
         ) for category in cat_raw
    )
    return cat_dict


def get_all_actions(rest_obj):
    resp = rest_obj.invoke_request("GET", ACTIONS_URI)
    actions = resp.json_data.get("value", [])
    cmp_actions = dict((x.get("Name"), {"Id": x.get("Id"),
                                        "Disabled": x.get("Disabled"),
                                        "Parameters": dict((y.get("Name"), y.get("Value")) for y in x.get("ParameterDetails")),
                                        "Type": dict((y.get("Name"),
                                                      ["true", "false"]
                                                      if y.get("Type") == "boolean"
                                                      else [z.get("Value") for z in y.get("TemplateParameterTypeDetails")
                                                            if y.get("Type") != "string"]) for y in x.get("ParameterDetails"))
                                        }
                        ) for x in actions)
    return cmp_actions


def validate_time(module, time, time_format, time_type):
    try:
        ftime = datetime.strptime(time, time_format)
    except ValueError:
        module.exit_json(failed=True, msg=INVALID_TIME.format(time_type, time))
    return ftime


def get_ftime(module, inp_schedule, time_type, time_interval):
    def_time = "00:00"
    time_format = "%Y-%m-%d %H:%M:%S.%f"
    hhmm = inp_schedule.get(f"time_{time_type}") if time_interval else def_time
    date_x = inp_schedule.get(f"date_{time_type}")
    time_x = None
    if date_x:
        dtime = f"{date_x} {hhmm}:00.000"
        time_x = validate_time(module, dtime, time_format, time_type)
    elif time_interval:
        dtime = f"{hhmm}:00.000"
    else:
        dtime = ""
    return dtime, time_x


def get_schedule_payload(module):
    schedule_payload = {}
    inp_schedule = module.params.get('date_and_time')
    if inp_schedule:
        time_interval = bool(inp_schedule.get('time_interval'))
        schedule_payload['Interval'] = time_interval
        schedule_payload["StartTime"], start_time_x = get_ftime(module, inp_schedule, "from", time_interval)
        schedule_payload["EndTime"], end_time_x = get_ftime(module, inp_schedule, "to", time_interval)
        if inp_schedule.get('date_to') and end_time_x < start_time_x:
            module.exit_json(failed=True, msg=END_START_TIME.format(end_time_x, start_time_x))
        weekdays = {'monday': 'mon', 'tuesday': 'tue', 'wednesday': 'wed', 'thursday': 'thu', 'friday': 'fri',
                    'saturday': 'sat', 'sunday': 'sun'}
        inp_week_list = ['*']
        cron_sep = ","
        if inp_schedule.get('days'):
            week_order = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            inp_week_list = sorted(list(set(inp_schedule.get('days'))), key=week_order.index)
        schedule_payload["CronString"] = f"* * * ? * {cron_sep.join([weekdays.get(x, '*') for x in inp_week_list])} *"
    return {"Schedule": schedule_payload} if schedule_payload else {}


def create_action_payload(inp_k, inp_val, ref_actions, module):
    if ref_actions.get(inp_k).get('Disabled'):
        module.exit_json(failed=True, msg=DISABLED_ACTION.format(inp_k))
    pld = {
        'TemplateId': ref_actions.get(inp_k).get('Id'),
        'Name': inp_k,
        'ParameterDetails': {}
    }
    diff = set(inp_val.keys()) - set(ref_actions.get(inp_k).get('Parameters').keys())
    if diff:
        module.exit_json(failed=True,
                         msg=ACTION_INVALID_PARAM.format(
                             inp_k, SEPARATOR.join(diff), SEPARATOR.join(ref_actions.get(inp_k).get('Parameters').keys())))
    for sub_k, sub_val in inp_val.items():
        valid_values = ref_actions.get(inp_k).get('Type').get(sub_k)
        if valid_values:
            if str(sub_val).lower() not in valid_values:
                module.exit_json(failed=True, msg=ACTION_INVALID_VALUE.format(inp_k, sub_val, sub_k, SEPARATOR.join(valid_values)))
            else:
                inp_val[sub_k] = str(sub_val).lower() if str(sub_val).lower() in ("true", "false") else sub_val
    pld['ParameterDetails'] = inp_val
    return pld


def get_actions_payload(module, rest_obj):
    action_payload = {}
    inp_actions = module.params.get('actions')
    if inp_actions:
        ref_actions = get_all_actions(rest_obj)
        inp_dict = {x.get("action_name"): {y.get("name"): y.get("value")
                                           for y in x.get("parameters", [])} for x in inp_actions}
        if 'Ignore' in inp_dict:
            action_payload['Ignore'] = {'TemplateId': ref_actions.get('Ignore').get('Id'),
                                        'Name': "Ignore",
                                        'ParameterDetails': {}}
        else:
            for inp_k, inp_val in inp_dict.items():
                if inp_k in ref_actions:
                    action_payload[inp_k] = create_action_payload(inp_k, inp_val, ref_actions, module)
                else:
                    module.exit_json(failed=True, msg=ACTION_DIS_EXIST.format(inp_k))
    return {"Actions": action_payload} if action_payload else {}


def load_subcategory_data(module, inp_sub_cat_list, sub_cat_dict, key_id, payload_cat, payload_subcat, inp_category):
    if inp_sub_cat_list:
        for sub_cat in inp_sub_cat_list:
            if sub_cat in sub_cat_dict:
                payload_cat.append(key_id)
                payload_subcat.append(
                    sub_cat_dict.get(sub_cat))
            else:
                module.exit_json(failed=True, msg=SUBCAT_IN_CATEGORY.format(sub_cat, inp_category.get('category_name')))
    else:
        payload_cat.append(key_id)
        payload_subcat.append(0)


def load_category_data(module, catalog_name, category_list, category_det, payload_cat, payload_subcat):
    if category_list:
        for inp_category in category_list:
            if inp_category.get('category_name') in category_det:
                resp_category_dict = category_det.get(inp_category.get('category_name'))
                key_id = list(resp_category_dict.keys())[0]
                sub_cat_dict = resp_category_dict.get(key_id)
                inp_sub_cat_list = inp_category.get('sub_category_names')
                load_subcategory_data(module, inp_sub_cat_list, sub_cat_dict, key_id, payload_cat, payload_subcat, inp_category)
            else:
                module.exit_json(failed=True, msg=CATEGORY_IN_CATALOG.format(inp_category.get('category_name'), catalog_name))
    else:
        payload_cat.append(0)
        payload_subcat.append(0)


def get_category_payloadlist(module, inp_catalog_list, cdict_ref):
    payload_cat_list = []
    for inp_catalog in inp_catalog_list:
        new_dict = {}
        catalog_name = inp_catalog.get('catalog_name')
        if catalog_name in cdict_ref:
            new_dict["CatalogName"] = catalog_name
            payload_cat = []
            category_det = cdict_ref.get(catalog_name)
            payload_subcat = []
            category_list = inp_catalog.get('catalog_category')
            load_category_data(module, catalog_name, category_list, category_det, payload_cat, payload_subcat)
            new_dict["Categories"] = payload_cat
            new_dict['SubCategories'] = payload_subcat
        else:
            module.exit_json(failed=True, msg=CATALOG_DIS_EXIST.format(catalog_name))
        payload_cat_list.append(new_dict)
    return payload_cat_list


def get_category_payload(module, rest_obj):
    inp_catalog_list = module.params.get('category')
    cdict_ref = get_category_data_tree(rest_obj)
    if not cdict_ref:
        module.exit_json(failed=True, msg=CATEGORY_FETCH_FAILED)
    payload_cat_list = get_category_payloadlist(module, inp_catalog_list, cdict_ref)
    return payload_cat_list


def get_message_payload(module):
    mlist = []
    if module.params.get('message_file'):
        csvpath = module.params.get('message_file')
        if not os.path.isfile(csvpath):
            module.exit_json(
                failed=True, msg=CSV_PATH.format(csvpath))
        with open(csvpath) as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                mlist.extend(row)
            if mlist[0].lower().startswith('message'):
                mlist.pop(0)
    elif module.params.get('message_ids'):
        mlist = module.params.get('message_ids')
    return mlist


def get_category_or_message(module, rest_obj):
    cat_payload = {"Catalogs": {},
                   "MessageIds": []}
    cat_msg_provided = False
    if module.params.get('category'):
        payload_cat_list = get_category_payload(module, rest_obj)
        cat_dict = dict((x.get('CatalogName'), x) for x in payload_cat_list)
        cat_msg_provided = True
        cat_payload['Catalogs'] = cat_dict
    else:
        mlist = get_message_payload(module)
        if mlist:
            validate_ome_data(module, rest_obj, mlist, 'MessageId', ('MessageId',), MESSAGES_URI, 'messages')
            cat_msg_provided = True
            cat_payload['MessageIds'] = list(set(mlist))
            cat_payload['MessageIds'].sort()
    if not cat_msg_provided:
        cat_payload = {}
    return cat_payload


def get_severity_payload(module, rest_obj):
    try:
        resp = rest_obj.invoke_request("GET", SEVERITY_URI)
        severity_dict = dict((x.get('Name').lower(), x.get('Id'))
                             for x in resp.json_data.get("Value"))
    except Exception:
        severity_dict = {"unknown": 1, "info": 2,
                         "normal": 4, "warning": 8, "critical": 16}
    inp_sev_list = module.params.get('severity')
    sev_payload = {}
    if inp_sev_list:
        if 'all' in inp_sev_list:
            sev_payload = {"Severities": list(severity_dict.values())}
        else:
            sev_payload = {"Severities": [
                severity_dict.get(x) for x in inp_sev_list]}
        sev_payload['Severities'].sort()
    return sev_payload


def transform_existing_policy_data(policy):
    pdata = policy.get('PolicyData')
    undiscovered = pdata.get('UndiscoveredTargets')
    if undiscovered:
        pdata['UndiscoveredTargets'] = [x.get('TargetAddress') for x in undiscovered]
    actions = pdata.get('Actions')
    if actions:
        for action in actions:
            if action.get('Name') == "RemoteCommand":
                # Special case handling for RemoteCommand, appends 1 after every post call to "remotecommandaction"
                action['ParameterDetails'] = dict((str(act_param.get('Name')).rstrip('1'), act_param.get('Value'))
                                                  for act_param in action.get('ParameterDetails', []))
            else:
                action['ParameterDetails'] = dict((act_param.get('Name'), act_param.get('Value'))
                                                  for act_param in action.get('ParameterDetails', []))
            action.pop('Id', None)
        pdata['Actions'] = dict((x.get('Name'), x) for x in actions)
    catalogs = pdata.get('Catalogs')
    pdata['Catalogs'] = dict((x.get('CatalogName'), x) for x in catalogs)
    # for Devices, DeviceTypes, Groups, Severities
    for pol_data in pdata.values():
        if isinstance(pol_data, list):
            pol_data.sort()
    messages = pdata.get('MessageIds', [])
    pdata['MessageIds'] = [m.strip("'") for m in messages]


def format_payload(policy):
    pdata = policy.get('PolicyData')
    undiscovered = pdata.get('UndiscoveredTargets')
    if undiscovered:
        pdata['UndiscoveredTargets'] = [({"TargetAddress": x}) for x in undiscovered]
    actions = pdata.get('Actions')
    if actions:
        for action in actions.values():
            action['ParameterDetails'] = [
                {"Name": k, "Value": v} for k, v in action.get('ParameterDetails', {}).items()]
        pdata['Actions'] = list(actions.values())
    catalogs = pdata.get('Catalogs')
    pdata['Catalogs'] = list(catalogs.values())


def compare_policy_payload(module, rest_obj, policy):
    diff = 0
    new_payload = {}
    new_policy_data = {}
    new_payload["PolicyData"] = new_policy_data
    transform_existing_policy_data(policy)
    payload_items = []
    payload_items.append(get_target_payload(module, rest_obj))
    payload_items.append(get_category_or_message(module, rest_obj))
    payload_items.append(get_actions_payload(module, rest_obj))
    payload_items.append(get_schedule_payload(module))
    payload_items.append(get_severity_payload(module, rest_obj))
    for payload in payload_items:
        if payload:
            new_policy_data.update(payload)
            diff_tuple = recursive_diff(new_payload['PolicyData'], policy['PolicyData'])
            if diff_tuple and diff_tuple[0]:
                diff = diff + 1
                policy['PolicyData'].update(payload)
    if module.params.get('new_name'):
        new_payload['Name'] = module.params.get('new_name')
    if module.params.get('description'):
        new_payload['Description'] = module.params.get('description')
    if module.params.get('enable') is not None:
        new_payload['Enabled'] = module.params.get('enable')
    policy = strip_substr_dict(policy)
    new_payload.pop('PolicyData', None)
    diff_tuple = recursive_diff(new_payload, policy)
    if diff_tuple and diff_tuple[0]:
        diff = diff + 1
        policy.update(diff_tuple[0])
    return diff


def get_policy_data(module, rest_obj):
    policy_data = {}
    target = get_target_payload(module, rest_obj)
    if not target:
        module.exit_json(failed=True, msg=INVALID_TARGETS)
    policy_data.update(target)
    cat_msg = get_category_or_message(module, rest_obj)
    if not cat_msg:
        module.exit_json(failed=True, msg=INVALID_CATEGORY_MESSAGE)
    policy_data.update(cat_msg)
    schedule = get_schedule_payload(module)
    if not schedule:
        module.exit_json(failed=True, msg=INVALID_SCHEDULE)
    policy_data.update(schedule)
    actions = get_actions_payload(module, rest_obj)
    if not actions:
        module.exit_json(failed=True, msg=INVALID_ACTIONS)
    policy_data.update(actions)
    sev_payload = get_severity_payload(module, rest_obj)
    if not sev_payload.get('Severities'):
        module.exit_json(failed=True, msg=INVALID_SEVERITY)
    policy_data.update(sev_payload)
    return policy_data


def remove_policy(module, rest_obj, policies):
    id_list = [x.get("Id")
               for x in policies if x.get("DefaultPolicy") is False]
    if len(id_list) != len(policies):
        module.exit_json(failed=True,
                         msg=DEFAULT_POLICY_DELETE.format(SEPARATOR.join([x.get('Name') for x in policies if x.get('DefaultPolicy')])))
    if module.check_mode:
        module.exit_json(msg=CHANGES_MSG, changed=True)
    rest_obj.invoke_request("POST", REMOVE_URI, data={
                            "AlertPolicyIds": id_list})
    module.exit_json(changed=True, msg=SUCCESS_MSG.format("delete"))


def enable_toggle_policy(module, rest_obj, policies):
    enabler = module.params.get('enable')
    id_list = [x.get("Id") for x in policies if x.get("Enabled") is not enabler]
    if not id_list:
        module.exit_json(msg=NO_CHANGES_MSG)
    if module.check_mode:
        module.exit_json(msg=CHANGES_MSG, changed=True)
    uri = ENABLE_URI if enabler else DISABLE_URI
    rest_obj.invoke_request("POST", uri, data={"AlertPolicyIds": id_list})
    module.exit_json(changed=True, msg=SUCCESS_MSG.format("enable" if enabler else "disable"))


def update_policy(module, rest_obj, policy):
    diff = compare_policy_payload(module, rest_obj, policy)
    if not diff:
        module.exit_json(msg=NO_CHANGES_MSG)
    if module.check_mode:
        module.exit_json(msg=CHANGES_MSG, changed=True)
    format_payload(policy)
    resp = rest_obj.invoke_request("PUT", f"{POLICIES_URI}({policy.get('Id')})", data=policy)
    module.exit_json(changed=True, msg=SUCCESS_MSG.format("update"),
                     status=resp.json_data)


def create_policy(module, rest_obj):
    create_payload = {}
    policy_data = get_policy_data(module, rest_obj)
    create_payload['PolicyData'] = policy_data
    create_payload['Name'] = module.params.get('name')[0]
    create_payload['Description'] = module.params.get('description')
    create_payload['Enabled'] = module.params.get(
        'enable') if module.params.get('enable', True) is not None else True
    if module.check_mode:
        module.exit_json(msg=CHANGES_MSG, changed=True)
    format_payload(create_payload)
    resp = rest_obj.invoke_request("POST", POLICIES_URI, data=create_payload)
    module.exit_json(changed=True, msg=SUCCESS_MSG.format(
        "create"), status=resp.json_data)


def handle_policy_enable(module, rest_obj, policies, name_list):
    if len(policies) == len(name_list):
        enable_toggle_policy(module, rest_obj, policies)
    else:
        invalid_policies = set(name_list) - set(x.get("Name") for x in policies)
        enabler = module.params.get('enable')
        module.exit_json(failed=True, msg=POLICY_ENABLE_MISSING.format("enable" if enabler else "disable", SEPARATOR.join(invalid_policies)))


def handle_absent_state(module, rest_obj, policies):
    if policies:
        remove_policy(module, rest_obj, policies)
    else:
        module.exit_json(msg=NO_POLICY_EXIST)


def handle_present_state(module, rest_obj, policies, name_list, present_args):
    present_args.remove('enable')
    enable = module.params.get('enable')
    if not any(module.params.get(prm) is not None for prm in present_args) and enable is not None:
        handle_policy_enable(module, rest_obj, policies, name_list)
    if len(name_list) > 1:
        module.exit_json(failed=True, msg=MULTIPLE_POLICIES)
    if policies:
        update_policy(module, rest_obj, policies[0])
    else:
        create_policy(module, rest_obj)


def main():
    specs = {
        "name": {'type': 'list', 'elements': 'str', 'required': True},
        "state": {'default': 'present', 'choices': ['present', 'absent'], 'type': 'str'},
        "enable": {'type': 'bool'},
        "new_name": {'type': 'str'},
        "description": {'type': 'str'},
        "device_service_tag": {'type': 'list', 'elements': 'str'},
        "device_group": {'type': 'list', 'elements': 'str'},
        "specific_undiscovered_devices": {'type': 'list', 'elements': 'str'},
        "any_undiscovered_devices": {'type': 'bool'},
        "all_devices": {'type': 'bool'},
        "category": {'type': 'list', 'elements': 'dict',
                     'options': {'catalog_name': {'type': 'str', 'required': True},
                                 'catalog_category': {'type': 'list', 'elements': 'dict',
                                                      'options': {'category_name': {'type': 'str'},
                                                                  'sub_category_names': {'type': 'list', 'elements': 'str'}
                                                                  },
                                                      }
                                 }
                     },
        "message_ids": {'type': 'list', 'elements': 'str'},
        "message_file": {'type': 'path'},
        "date_and_time": {'type': 'dict',
                          'options': {'date_from': {'type': 'str', 'required': True},
                                      'date_to': {'type': 'str'},
                                      'time_from': {'type': 'str'},
                                      'time_to': {'type': 'str'},
                                      'days': {'type': 'list', 'elements': 'str',
                                               'choices': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']},
                                      'time_interval': {'type': 'bool'}
                                      },
                          'required_if': [['time_interval', True, ('time_from', 'time_to')]]
                          },
        "severity": {'type': 'list', 'elements': 'str', 'choices': ['info', 'normal', 'warning', 'critical', 'unknown', 'all']},
        "actions": {'type': 'list', 'elements': 'dict',
                    'options': {'action_name': {'type': 'str', 'required': True},
                                'parameters': {'type': 'list', 'elements': 'dict', 'default': [],
                                               'options': {'name': {'type': 'str'},
                                                           'value': {'type': 'str'}}
                                               }
                                }
                    }
    }

    present_args = ['enable', 'new_name', 'description', 'device_service_tag', 'device_group',
                    'specific_undiscovered_devices', 'any_undiscovered_devices', 'all_devices',
                    'category', 'message_ids', 'message_file', 'date_and_time', 'severity', 'actions']
    module = OmeAnsibleModule(
        argument_spec=specs,
        required_if=[['state', 'present', present_args, True]],
        mutually_exclusive=[('device_service_tag', 'device_group', 'any_undiscovered_devices', 'specific_undiscovered_devices', 'all_devices',),
                            ('message_ids', 'message_file', 'category',)],
        supports_check_mode=True)
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            state = module.params.get('state')
            name_list = list(set(module.params.get('name')))
            policies = get_alert_policies(rest_obj, name_list)
            if state == 'absent':
                handle_absent_state(module, rest_obj, policies)
            else:
                handle_present_state(module, rest_obj, policies, name_list, present_args)
    except HTTPError as err:
        module.exit_json(failed=True, msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(failed=True, msg=str(err))


if __name__ == '__main__':
    main()
