#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.3.0
# Copyright (C) 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_alert_policies
short_description: Manage OME alert policies.
version_added: "8.3.0"
description: This module allows you to create, modify, or delete Alert policies on OpenManage Enterprise or OpenManage Enterprise Modular.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  name:
    description:
      - Name for the alert policy.
      - This is applicable only when I(state) is C(present) and first one is picked if multiple values is provided.
      - List is Applicable when I(state) is C(absent).
    type: list
    elements: str
    required: true
  state:
    description:
      - C(present) allows to create an alert policy or update if the policy name already exists.
      - C(absent) allows to delete an alert policy.
    default: present
    choices: [present, absent]
    type: str
  enable:
    description:
      - C(True) allows to enable an alert policy.
      - C(False) allows to disable an alert policy.
      - This is applicable only when I(state) is C(present).
    type: bool
  new_name:
    description:
      - New name for the alert policy.
      - This is applicable only when I(state) is C(present) and a policy exists.
    type: str
  description:
    description:
      - Description for the alert policy.
      - This is applicable only when I(state) is C(present)
    type: str
  device_service_tag:
    description:
      - List of device service tags on which the alert policy will be applicable.
      - This option is mutually exclusive with I(device_group), I(undiscovered_devices), I(any_undiscovered_devices) and I(all_devices).
      - This is applicable only when I(state) is C(present)
    type: list
    elements: str
  device_group:
    description:
      - List of Group name on which the alert policy will be applicable.
      - This option is mutually exclusive with I(device_service_tag), I(undiscovered_devices), I(any_undiscovered_devices) and I(all_devices) .
      - This is applicable only when I(state) is C(present)
    type: list
    elements: str
  specific_undiscovered_devices:
    description:
      - Undiscovered IP's, hostnames or range of IP's of a devices on which the alert policy will be applicable.
      - This option is mutually exclusive with I(device_service_tag), I(device_group), I(any_undiscovered_devices) and I(all_devices) .
      - This is applicable only when I(state) is C(present)
      - "Sample Valid IP Range Format:"
      - "     10.35.0.0"
      - "     10.36.0.0-10.36.0.255"
      - "     10.37.0.0/24"
      - "     2607:f2b1:f083:135::5500/118"
      - "     2607:f2b1:f083:135::a500-2607:f2b1:f083:135::a600"
      - "     hostname.domain.com"
      - "Sample Invalid IP Range Format:"
      - "     10.35.0.*"
      - "     10.36.0.0-255"
      - "     10.35.0.0/255.255.255.0"
    type: list
    elements: str
  any_undiscovered_devices:
    description:
      - Any Undiscovered devices on which the alert policy will be applicable.
      - This option is mutually exclusive with I(device_service_tag), I(undiscovered_devices), I(device_group) and I(all_devices).
      - This is applicable only when I(state) is C(present).
    type: bool
  all_devices:
    description:
      - All the discovered and undiscovered devices on which the alert policy will be applicable.
      - This option is mutually exclusive with I(device_service_tag), I(undiscovered_devices), I(any_undiscovered_devices) and I(device_group).
      - This is applicable only when I(state) is C(present).
    type: bool
  category:
    description:
      - Category of the alerts received.
      - This is mutually exclusive with the I(message_ids), I(message_file).
      - To be fetch from the M(dellemc.openmanage.ome_alert_policies_category_info).
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
            description: List of sub categories.
            type: list
            elements: str
  message_ids:
    description:
      - List of Message ids
      - This is mutually exclusive with the I(category), I(message_file)
      - This is applicable only when I(state) is C(present)
      - To be fetched from the M(dellemc.openmanage.ome_alert_policies_message_id_info)
    type: list
    elements: str
  message_file:
    description:
      - Local path of a CSV formatted file with message ids
      - This is mutually exclusive with the I(category), I(message_ids)
      - This is applicable only when I(state) is C(present)
      - To be fetched from the M(dellemc.openmanage.ome_alert_policies_message_id_info)
    type: path
  date_and_time:
    description:
      - Specify the schedule for when the alert policy is applicable.
      - I(date_and_time) is mandatory for creating a policy and optional when updating a poicy.
      - This is applicable only when I(state) is C(present)
    type: dict
    suboptions:
      date_from:
        description: "Start date in the format YYYY-MM-DD."
        type: str
        required: true
      date_to:
        description: "End date in the format YYYY-MM-DD."
        type: str
      time_from:
        description:
          - "Interval start time in the format HH:MM"
          - This is mandatory when I(time_interval) is C(True)
        type: str
      time_to:
        description:
          - "Interval end time in the format HH:MM"
          - This is mandatory when I(time_interval) is C(True)
        type: str
      days:
        description: Days of the week to be scheduled.
        type: list
        elements: str
        choices: [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
      time_interval:
        description: Enable time interval to be scheduled.
        type: bool
  severity:
    description:
      - Severity of the alert.
      - This is mandatory when creating a policy and optional updating a policy.
      - This is applicable only when I(state) is C(present).
    type: list
    elements: str
    choices: [info, normal, warning, critical, unknown, all]
  actions:
    description:
      - Actions to be triggered for the policy.
      - This parameter is case-sensitive.
      - This is mandatory when creating a policy and optional updating a policy.
      - This is applicable only when I(state) is C(present)
    type: list
    elements: dict
    suboptions:
      action_name:
        description:
          - Name of the action.
          - To be fetched from the M(dellemc.openmanage.ome_alert_policies_action_info)
        type: str
        required: true
      parameters:
        description:
          - Predefined parameters to be set for the I(action_name).
        type: list
        elements: dict
        default: []
        suboptions:
          name:
            description:
              - Name of the parameter.
              - To be fetched from the M(dellemc.openmanage.ome_alert_policies_action_info)
            type: str
          value:
            description:
             - Value of the parameter.
            type: str
requirements:
    - "python >= 3.9.6"
author: "Jagadeesh N V(@jagadeeshnv)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise
      or OpenManage Enterprise Modular.
    - This module supports both IPv4 and IPv6 addresses.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: "Create a Alert Policy"
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
              - idrac
              - Generic
              - Device
          - category_name: Storage
            sub_category_names:
              - Other
    date_and_time:
      - date_from: 2022-10-10
    severity:
      - unknown
      - critical
    actions:
      - action_name: trap
        parameters:
          - name: "192.1.2.3:162"
            value: true
          - name: "traphostname.domain.com:162"
            value: true
  tags: create_alert_policy

- name: "Update a Alert Policies"
  dellemc.openamanage.ome_alert_policies:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    new_name: "Update Policy Name"
    device_group: "Group Name"
    category:
    - catalog_name: Application
      catalog_category:
        - category_name: Audit
          sub_category_names:
            - idrac
            - Generic
    date_and_time:
      - date_from: 2022-10-10
    actions:
      - action_name: Trap
        parameters:
          - name: "192.1.2.3:162"
            value: true
  tags: update_alert_policy

- name: "Enable a Policy"
  dellemc.openamanage.ome_alert_policies:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    new_name: "Policy Name"
    device_group: "Group Name"
    enable: True
  tags: enable_alert_policy

- name: "Disable a Policy"
  dellemc.openamanage.ome_alert_policies:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    name: "Policy Name"
    enable: False
  tags: disable_alert_policy

- name: "Delete a Policy"
  dellemc.openamanage.ome_alert_policies:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    name: "Policy Name"
    state: absent
  tags: delete_alert_policy
'''

RETURN = r'''
---
msg:
  type: str
  description: Status of the alert policies operation.
  returned: always
  sample: "Successfully performed the create policy operation."
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
        "EndTime": "2023-06-06 15:02:46.000",
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
'''

import csv
import os
import json
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import get_all_data_with_pagination
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from datetime import datetime


POLICIES_URI = "AlertService/AlertPolicies"
MESSAGES_URI = "AlertService/AlertMessageDefinitions"
ACTIONS_URI = "AlertService/AlertActionTemplates"
SEVERITY_URI = "AlertService/AlertSeverities"
DEVICES_URI = "DeviceService/Devices"
GROUPS_URI = "GroupService/Groups"
REMOVE_URI = "AlertService/Actions/AlertService.RemoveAlertPolicies"
CATEGORY_URI = "AlertService/AlertCategories"
SUCCESS_MSG = "Successfully performed the {0} operation."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_MSG = "Changes found to be applied."
SEPARATOR = ","


def get_alert_policies(rest_obj, name_list):
    report = get_all_data_with_pagination(rest_obj, POLICIES_URI)
    all_policies = report.get("report_list", [])
    policies = []
    for policy in all_policies:
        if policy.get("Name") in name_list:
            policies.append(policy)
    # TODO take care of DefaultPolicy
    return policies


def get_device_data(module, rest_obj):
    svc_tags = set(module.params.get('device_service_tag'))
    # TODO take care of single service tag
    report = get_all_data_with_pagination(rest_obj, DEVICES_URI)
    all_devices = report.get("report_list", [])
    devs = []
    dev_types = []
    for dev in all_devices:
        st = dev.get("DeviceServiceTag")
        if st in svc_tags:
            svc_tags.remove(st)
            devs.append(dev.get("Id"))
            dev_types.append(dev.get("Type"))
        if not svc_tags:
            break
    if len(svc_tags) > 0:
        module.exit_json(failed=True,
                         msg=f"Devices with service tag '{SEPARATOR.join(svc_tags)}' are not found.")
    return list(set(dev_types)), devs


def get_group_data(module, rest_obj):
    grps = set(module.params.get('device_group'))
    # TODO take care of single group
    report = get_all_data_with_pagination(rest_obj, GROUPS_URI)
    all_devices = report.get("report_list", [])
    group_ids = []
    for dev in all_devices:
        st = dev.get("Name")
        if st in grps:
            grps.remove(st)
            group_ids.append(dev.get("Id"))
        if not grps:
            break
    if len(grps) > 0:
        module.exit_json(failed=True,
                         msg=f"Groups with names '{SEPARATOR.join(grps)}' are not found.")
    return group_ids


def get_target_payload(module, rest_obj):
    target_payload = {}
    mparams = module.params
    if mparams.get('all_devices'):
        target_payload['AllTargets'] = True
    elif mparams.get('any_undiscovered_devices'):
        target_payload['UndiscoveredTargets'] = [
            {"TargetAddress": "ALL_UNDISCOVERED_TARGETS"}]
    elif mparams.get('specific_undiscovered_devices'):
        target_payload['UndiscoveredTargets'] = [
            ({"TargetAddress": x}) for x in module.params.get('specific_undiscovered_devices')]
    elif mparams.get('device_service_tag'):
        devicetype, deviceids = get_device_data(module, rest_obj)
        target_payload['Devices'] = deviceids
        target_payload['DeviceTypes'] = devicetype
    elif mparams.get('device_group'):
        target_payload['Groups'] = get_group_data(module, rest_obj)
    if not target_payload:
        module.exit_json(
            failed=True, msg="No valid targets provided for policy creation.")
    return target_payload


def get_category_data_tree(rest_obj):
    """
    Get the constructed category data tree.

    :param rest_obj: The REST object to use for making the request.
    :type rest_obj: RestObject
    :return: The category data tree.
    :rtype: dict
    """
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


def get_all_message_ids(rest_obj):
    report = get_all_data_with_pagination(rest_obj, MESSAGES_URI)
    all_messages = report.get("report_list", [])
    return {x.get("MessageId") for x in all_messages}


def get_all_actions(rest_obj):
    """
    Retrieves all actions from the specified REST object.

    Parameters:
        rest_obj (object): The REST object to retrieve actions from.

    Returns:
        dict: A dictionary containing information about each action. The keys are the names of the actions, and the values are dictionaries with the following keys:
            - "Id" (str): The ID of the action.
            - "Disabled" (bool): Indicates whether the action is disabled.
            - "Parameters" (dict): A dictionary containing the parameters of the action. The keys are the names of the parameters, and the values are the corresponding values of the parameters.
    """
    resp = rest_obj.invoke_request("GET", ACTIONS_URI)
    actions = resp.json_data.get("value", [])
    cmp_actions = dict((x.get("Name"), {"Id": x.get("Id"),
                                        "Disabled": x.get("Disabled"),
                                        "Parameters": dict(
                                            (y.get("Name"), y.get("Value")) for y in x.get("ParameterDetails")
    )}) for x in actions)
    return cmp_actions


def get_schedule_payload(module):
    """
    Generates the payload for scheduling a task.

    Args:
        module (object): The module object containing the parameters for scheduling.

    Returns:
        dict: The payload for scheduling a task.
    """
    schedule_payload = {}
    inp_schedule = module.params.get('date_and_time')
    if inp_schedule:
        def_time = "00:00"
        time_format = "%Y-%m-%d %H:%M:%S.%f"
        time_interval = inp_schedule.get('time_interval', False)
        schedule_payload['Interval'] = time_interval
        time_from = inp_schedule.get(
            'time_from') if time_interval else def_time
        time_to = inp_schedule.get('time_to') if time_interval else def_time
        start_time = f"{inp_schedule.get('date_from')} {time_from}:00.000"
        try:
            start_time_x = datetime.strptime(start_time, time_format)
            if start_time_x < datetime.now():
                module.exit_json(
                    failed=True, msg="Start time must be greater than current time.")
            schedule_payload["StartTime"] = start_time
        except ValueError:
            module.exit_json(failed=True, msg="Invalid start date or time.")
        if inp_schedule.get('date_to'):
            end_time = f"{inp_schedule.get('date_to')} {time_to}:00.000"
            try:
                end_time_x = datetime.strptime(end_time, time_format)
                if end_time_x < start_time_x:
                    module.exit_json(
                        failed=True, msg="End time must be greater than start time.")
                schedule_payload["EndTime"] = end_time
            except ValueError:
                module.exit_json(failed=True, msg="Invalid end date or time.")
        weekdays = {'monday': 'mon', 'tuesday': 'tue', 'wednesday': 'wed', 'thursday': 'thu', 'friday': 'fri',
                    'saturday': 'sat', 'sunday': 'sun'}
        inp_week_list = ['*']
        if inp_schedule.get('days'):
            inp_week_list = set(inp_schedule.get('days'))
        schedule_payload["CronString"] = f"* * * ? * {SEPARATOR.join([weekdays.get(x, '*') for x in inp_week_list])} *"
    return {"Schedule": schedule_payload}


def get_actions_payload(module, rest_obj):
    """
    Generates the payload for the actions to be performed.

    Args:
        module (object): The module object.
        rest_obj (object): The REST object.

    Returns:
        dict: The dictionary containing the actions payload.
    """
    action_payload = []
    inp_actions = module.params.get('actions')
    if inp_actions:
        ref_actions = get_all_actions(rest_obj)
        inp_dict = dict((x.get("action_name"), dict((y.get("name"), y.get(
            "value")) for y in x.get("parameters", []))) for x in inp_actions)
        if 'Ignore' in inp_dict:
            pld = {}
            pld['TemplateId'] = ref_actions.get('Ignore').get('Id')
            pld['Name'] = "Ignore"
            pld['ParameterDetails'] = []
            action_payload.append(pld)
        else:
            for inp_k, inp_val in inp_dict.items():
                if inp_k in ref_actions:
                    pld = {}
                    if ref_actions.get(inp_k).get('Disabled'):
                        module.exit_json(
                            failed=True, msg=f"Action '{inp_k}' is disabled.")
                    pld['TemplateId'] = ref_actions.get(inp_k).get('Id')
                    pld['Name'] = inp_k
                    diff = set(inp_val.keys()) - \
                        set(ref_actions.get(inp_k).get('Parameters').keys())
                    if diff:
                        module.exit_json(
                            failed=True, msg=f"Action '{inp_k}' has invalid parameters: {SEPARATOR.join(diff)}")
                    pld['ParameterDetails'] = [
                        {"Name": k, "Value": v} for k, v in inp_val.items()]
                    action_payload.append(pld)
                else:
                    module.exit_json(
                        failed=True, msg=f"Action '{inp_k}' does not exist.")
        # module.exit_json(z=action_payload)
    return {"Actions": action_payload}


def get_category_or_message(module, rest_obj):
    """
    Retrieves a category or message based on the provided module and REST object.

    Args:
        module: The module containing the parameters for the API call.
        rest_obj: The REST object used to retrieve the category data tree.

    Returns:
        cat_payload: The retrieved category or message payload.

    Raises:
        ExitJSON: If the category, sub-category or message does not exist.
    """
    cat_payload = {}
    if module.params.get('category'):
        inp_catalog_list = module.params.get('category')
        cdict_ref = get_category_data_tree(rest_obj)
        if not cdict_ref:
            module.exit_json(
                failed=True, msg="Failed to fetch Category details.")
        payload_cat_list = []
        for inp_catalog in inp_catalog_list:
            new_dict = {}
            catalog_name = inp_catalog.get('catalog_name')
            if catalog_name in cdict_ref:
                new_dict["CatalogName"] = catalog_name
                payload_cat = []
                category_det = cdict_ref.get(catalog_name)
                key_id = list(category_det.keys())[0]
                payload_subcat = []
                for inp_category in inp_catalog.get('catalog_category'):
                    if inp_category.get('category_name') in category_det:
                        resp_category_dict = category_det.get(
                            inp_category.get('category_name'))
                        key_id = list(resp_category_dict.keys())[0]
                        sub_cat_dict = resp_category_dict.get(key_id)
                        inp_sub_cat_list = inp_category.get(
                            'sub_category_names')
                        for sub_cat in inp_sub_cat_list:
                            if sub_cat in sub_cat_dict:
                                payload_cat.append(key_id)
                                payload_subcat.append(
                                    sub_cat_dict.get(sub_cat))
                            else:
                                module.exit_json(
                                    failed=True, msg=f"Sub category '{sub_cat}' in category '{inp_category.get('category_name')}' does not exist.")
                        new_dict['SubCategories'] = payload_subcat
                    else:
                        module.exit_json(
                            failed=True, msg=f"Category '{inp_category.get('category_name')}' in catalog '{catalog_name}' does not exist.")
                new_dict["Categories"] = payload_cat
            else:
                module.exit_json(
                    failed=True, msg=f"Catalog '{catalog_name}' does not exist.")
            payload_cat_list.append(new_dict)
        cat_payload['Catalogs'] = payload_cat_list
    else:
        mlist = []
        if module.params.get('message_file'):
            csvpath = module.params.get('message_file')
            if not os.path.isfile(csvpath):
                module.exit_json(
                    failed=True, msg=f"Message file '{csvpath}' does not exist.")
            with open(csvpath) as csvfile:
                spamreader = csv.reader(csvfile)
                for row in spamreader:
                    mlist.extend(row)
                if mlist[0].lower().startswith('message'):
                    mlist.pop(0)
        elif module.params.get('message_ids'):
            mlist = module.params.get('message_ids')
        if mlist:
            all_msg_id_set = get_all_message_ids(rest_obj)
            if not all_msg_id_set:
                module.exit_json(
                    failed=True, msg="Failed to fetch Message Id details.")
            diff = set(mlist) - all_msg_id_set
            if diff:
                module.exit_json(
                    failed=True, msg=f"Message Ids '{SEPARATOR.join(diff)}' do not exist.")
            cat_payload['MessageIds'] = list(set(mlist))
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
    if not inp_sev_list:
        module.exit_json(failed=True, msg="Severity is required.")
    if 'all' in inp_sev_list:
        sev_payload = {"Severities": list(severity_dict.values())}
    else:
        sev_payload = {"Severities": [
            severity_dict.get(x) for x in inp_sev_list]}
    return sev_payload


def remove_policy(module, rest_obj, policies):
    id_list = [x.get("Id")
               for x in policies if x.get("DefaultPolicy") is False]
    if len(id_list) != len(policies):
        module.exit_json(failed=True,
                         msg=f"Default Policies '{SEPARATOR.join([x.get('Name') for x in policies if x.get('DefaultPolicy')])}' cannot be deleted.")
    if module.check_mode:
        module.exit_json(msg=CHANGES_MSG, changed=True)
    rest_obj.invoke_request("POST", REMOVE_URI, data={
                            "AlertPolicyIds": id_list})
    module.exit_json(changed=True, msg=SUCCESS_MSG.format("remove policy"))


def update_policy(module, rest_obj, policy):
    module.exit_json(changed=True, msg="WIP: Update policy coming soon :)")


def get_policy_data(module, rest_obj):
    policy_data = {}
    target = get_target_payload(module, rest_obj)
    policy_data.update(target)
    cat_msg = get_category_or_message(module, rest_obj)
    policy_data.update(cat_msg)
    schedule = get_schedule_payload(module)
    policy_data.update(schedule)
    actions = get_actions_payload(module, rest_obj)
    policy_data.update(actions)
    sev_payload = get_severity_payload(module, rest_obj)
    policy_data.update(sev_payload)
    return policy_data


def create_policy(module, rest_obj):
    create_payload = {}
    policy_data = get_policy_data(module, rest_obj)
    create_payload['PolicyData'] = policy_data
    create_payload['Name'] = module.params.get('name')[0]
    create_payload['Description'] = module.params.get('description')
    create_payload['Enabled'] = module.params.get(
        'enable') if module.params.get('enable', True) is not None else True
    resp = rest_obj.invoke_request("POST", POLICIES_URI, data=create_payload)
    module.exit_json(changed=True, msg=SUCCESS_MSG.format(
        "create policy"), status=resp.json_data)


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
    specs.update(ome_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        required_if=[['state', 'present', ('enable', 'new_name', 'description', 'device_service_tag', 'device_group',
                                           'specific_undiscovered_devices', 'any_undiscovered_devices', 'all_devices',
                                           'category', 'message_ids', 'message_file',
                                           'date_and_time', 'severity', 'actions',), True]],
        mutually_exclusive=[('device_service_tag', 'device_group', 'any_undiscovered_devices', 'specific_undiscovered_devices'),
                            ('message_ids', 'message_file', 'category')],
        supports_check_mode=True)
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            state = module.params.get('state')
            name_list = module.params.get('name')
            policies = get_alert_policies(rest_obj, name_list)
            if state == 'absent':
                if policies:
                    remove_policy(module, rest_obj, policies)
                else:
                    module.exit_json(msg=NO_CHANGES_MSG)
            else:
                if len(name_list) > 1:
                    module.exit_json(
                        failed=True, msg="More than one policy name provided.")
                if policies:
                    update_policy(module, rest_obj, policies[0])
                else:
                    create_policy(module, rest_obj)
                module.exit_json(msg=SUCCESS_MSG)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(failed=True, msg=str(err))


if __name__ == '__main__':
    main()
