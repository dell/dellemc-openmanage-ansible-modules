#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.2.0
# Copyright (C) 2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_configuration_compliance_baseline
short_description: Create, modify, and delete a configuration compliance baseline and remediate non-compliant devices on
 OpenManage Enterprise
version_added: "3.2.0"
description: "This module allows to create, modify, and delete a configuration compliance baseline on OpenManage Enterprise.
 This module also allows to remediate devices that are non-compliant with the baseline by changing the attributes of devices
  to match with the associated baseline attributes."
extends_documentation_fragment:
  - dellemc.openmanage.oment_auth_options
options:
  command:
    description:
      - "C(create) creates a configuration baseline from an existing compliance template.C(create) supports
      C(check_mode) or idempotency checking for only I(names)."
      - "C(modify) modifies an existing baseline.Only I(names), I(description), I(device_ids), I(device_service_tags),
       and I(device_group_names) can be modified"
      - "I(WARNING) When a baseline is modified, the provided I(device_ids), I(device_group_names), and I(device_service_tags)
       replaces the devices previously present in the baseline."
      - C(delete) deletes the list of configuration compliance baselines based on the baseline name. Invalid baseline
       names are ignored.
      - "C(remediate) remediates devices that are non-compliant with the baseline by changing the attributes of devices
       to match with the associated baseline attributes."
      - "C(remediate) is performed on all the non-compliant devices if either I(device_ids), or I(device_service_tags)
      is not provided."
    choices: [create, modify, delete, remediate]
    default: create
    type: str
  names:
    description:
      - Name(s) of the configuration compliance baseline.
      - This option is applicable when I(command) is C(create), C(modify), or C(delete).
      - Provide the list of configuration compliance baselines names that are supported when I(command) is C(delete).
    required: true
    type: list
    elements: str
  new_name:
    description:
      - New name of the compliance baseline to be modified.
      - This option is applicable when I(command) is C(modify).
    type: str
  template_name:
    description:
      - Name of the compliance template for creating the compliance baseline(s).
      - Name of the deployment template to be used for creating a compliance baseline.
      - This option is applicable when I(command) is C(create) and is mutually exclusive with I(template_id).
    type: str
  template_id:
    description:
      - ID of the deployment template to be used for creating a compliance baseline.
      - This option is applicable when I(command) is C(create) and is mutually exclusive with I(template_name).
    type: int
  device_ids:
    description:
      - IDs of the target devices.
      - This option is applicable when I(command) is C(create), C(modify), or C(remediate), and is mutually exclusive
       with I(device_service_tag) and I(device_group_names).
    type: list
    elements: int
  device_service_tags:
    description:
      - Service tag of the target device.
      - This option is applicable when I(command) is C(create), C(modify), or C(remediate) and is mutually exclusive with
       I(device_ids) and I(device_group_names).
    type: list
    elements: str
  device_group_names:
    description:
      - Name of the target device group.
      - This option is applicable when I(command) is C(create), or C(modify)
       and is mutually exclusive with I(device_ids) and I(device_service_tag).
    type: list
    elements: str
  description:
    description:
      - Description of the compliance baseline.
      - This option is applicable when I(command) is C(create), or C(modify).
    type: str
  job_wait:
    description:
      - Provides the option to wait for job completion.
      - This option is applicable when I(command) is C(create), C(modify), or C(remediate).
    type: bool
    default: true
  job_wait_timeout:
    description:
      - The maximum wait time of I(job_wait) in seconds.The job will only be tracked for this duration.
      - This option is applicable when I(job_wait) is C(True).
    type: int
    default: 10800
requirements:
    - "python >= 2.7.5"
author: "Sajna Shetty(@Sajna-Shetty)"
notes:
    - This module supports C(check_mode).
    - Ensure that the devices have the required licenses to perform the baseline compliance operations.
'''

EXAMPLES = r'''
---
- name: Create a configuration compliance baseline using device IDs
  dellemc.openmanage.ome_configuration_compliance_baseline:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    names: "baseline1"
    template_name: "template1"
    description: "description of baseline"
    device_ids:
      - 1111
      - 2222

- name: Create a configuration compliance baseline using device service tags
  dellemc.openmanage.ome_configuration_compliance_baseline:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    names: "baseline1"
    template_id: 1234
    description: "description of baseline"
    device_service_tags:
      - "SVCTAG1"
      - "SVCTAG2"

- name: Create a configuration compliance baseline using group names
  dellemc.openmanage.ome_configuration_compliance_baseline:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    names: "baseline2"
    template_id: 2
    job_wait_timeout: 1000
    description: "description of baseline"
    device_group_names:
      - "Group1"
      - "Group2"

- name: Delete the configuration compliance baselines
  dellemc.openmanage.ome_configuration_compliance_baseline:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    command: delete
    names:
      - baseline1
      - baseline2

- name: Modify a configuration compliance baseline using group names
  dellemc.openmanage.ome_configuration_compliance_baseline:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    command: modify
    names: "baseline1"
    new_name: "baseline_update"
    template_name: "template2"
    description: "new description of baseline"
    job_wait_timeout: 1000
    device_group_names:
      - Group1

- name: Remediate specific non-compliant devices to a configuration compliance baseline using device IDs
  dellemc.openmanage.ome_configuration_compliance_baseline:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    command: "remediate"
    names: "baseline1"
    device_ids:
      - 1111

- name: Remediate specific non-compliant devices to a configuration compliance baseline using device service tags
  dellemc.openmanage.ome_configuration_compliance_baseline:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    command: "remediate"
    names: "baseline1"
    device_service_tags:
      - "SVCTAG1"
      - "SVCTAG2"

- name: Remediate all the non-compliant devices to a configuration compliance baseline
  dellemc.openmanage.ome_configuration_compliance_baseline:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    command: "remediate"
    names: "baseline1"
'''

RETURN = r'''
---
msg:
  description: Overall status of the configuration compliance baseline operation.
  returned: always
  type: str
  sample: "Successfully created the configuration compliance baseline."
incompatible_devices:
  description: Details of the devices which cannot be used to perform baseline compliance operations
  returned: when I(device_service_tags) or I(device_ids) contains incompatible devices for C(create) or C(modify)
  type: list
  sample: [1234, 5678]
compliance_status:
  description: Status of compliance baseline operation.
  returned: when I(command) is C(create) or C(modify)
  type: dict
  sample:    {
            "Id": 13,
            "Name": "baseline1",
            "Description": null,
            "TemplateId": 102,
            "TemplateName": "one",
            "TemplateType": 2,
            "TaskId": 26584,
            "PercentageComplete": "100",
            "TaskStatus": 2070,
            "LastRun": "2021-02-27 13:15:13.751",
            "BaselineTargets": [
                {
                    "Id": 1111,
                    "Type": {
                        "Id": 1000,
                        "Name": "DEVICE"
                    }
                }
            ],
            "ConfigComplianceSummary": {
                "ComplianceStatus": "OK",
                "NumberOfCritical": 0,
                "NumberOfWarning": 0,
                "NumberOfNormal": 0,
                "NumberOfIncomplete": 0
            }
 }
job_id:
  description:
    - Task ID created when I(command) is C(remediate).
  returned: when I(command) is C(remediate)
  type: int
  sample: 14123
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

import json
import time
import re
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError

COMPLIANCE_BASELINE = "TemplateService/Baselines"
REMEDIATE_BASELINE = "TemplateService/Actions/TemplateService.Remediate"
DELETE_COMPLIANCE_BASELINE = "TemplateService/Actions/TemplateService.RemoveBaseline"
MODIFY_COMPLIANCE_BASELINE = "api/TemplateService/Baselines({baseline_id})"
TEMPLATE_VIEW = "TemplateService/Templates"
DEVICE_VIEW = "DeviceService/Devices"
GROUP_VIEW = "GroupService/Groups"
OME_INFO = "ApplicationService/Info"
CONFIG_COMPLIANCE_URI = "TemplateService/Baselines({0})/DeviceConfigComplianceReports"
INVALID_DEVICES = "{identifier} details are not available."
TEMPLATE_ID_ERROR_MSG = "Template with ID '{template_id}' not found."
TEMPLATE_NAME_ERROR_MSG = "Template '{template_name}' not found."
NAMES_ERROR = "Only delete operations accept multiple baseline names. All the other operations accept only a single " \
              "baseline name."
BASELINE_CHECK_MODE_CHANGE_MSG = "Baseline '{name}' already exists."
CHECK_MODE_CHANGES_MSG = "Changes found to be applied."
CHECK_MODE_NO_CHANGES_MSG = "No changes found to be applied."
BASELINE_CHECK_MODE_NOCHANGE_MSG = "Baseline '{name}' does not exist."
CREATE_MSG = "Successfully created the configuration compliance baseline."
DELETE_MSG = "Successfully deleted the configuration compliance baseline(s)."
MODIFY_MSG = "Successfully modified the configuration compliance baseline."
TASK_PROGRESS_MSG = "The initiated task for the configuration compliance baseline is in progress."
INVALID_IDENTIFIER = "Target with {identifier} {invalid_val} not found."
IDEMPOTENCY_MSG = "The specified configuration compliance baseline details are the same as the existing settings."
INVALID_COMPLIANCE_IDENTIFIER = "Unable to complete the operation because the entered target {0} {1}" \
                                " is not associated or complaint with the baseline '{2}'."
INVALID_TIME = "job_wait_timeout {0} is not valid."
REMEDIATE_MSG = "Successfully completed the remediate operation."
JOB_FAILURE_PROGRESS_MSG = "The initiated task for the configuration compliance baseline has failed."
NO_CAPABLE_DEVICES = "Target {0} contains devices which cannot be used for a baseline compliance operation."


def validate_identifiers(available_values, requested_values, identifier_types, module):
    """
    Validate if requested group/device ids are valid
    """
    val = set(requested_values) - set(available_values)
    if val:
        module.fail_json(msg=INVALID_IDENTIFIER.format(identifier=identifier_types, invalid_val=",".join(map(str, val))))


def get_identifiers(available_identifiers_map, requested_values):
    """
    Get the device id from service tag
    or Get the group id from Group names
    or get the id from baseline names
    """
    id_list = []
    for key, val in available_identifiers_map.items():
        if val in requested_values:
            id_list.append(key)
    return id_list


def get_template_details(module, rest_obj):
    """
    Validate the template.
    """
    template_identifier = module.params.get('template_id')
    query_param = {"$filter": "Id eq {0}".format(template_identifier)}
    identifier = 'Id'
    if not template_identifier:
        template_identifier = module.params.get('template_name')
        query_param = {"$filter": "Name eq '{0}'".format(template_identifier)}
        identifier = 'Name'
    resp = rest_obj.invoke_request('GET', TEMPLATE_VIEW, query_param=query_param)
    if resp.success and resp.json_data.get('value'):
        template_list = resp.json_data.get('value', [])
        for each_template in template_list:
            if each_template.get(identifier) == template_identifier:
                return each_template
    if identifier == "Id":
        module.fail_json(msg=TEMPLATE_ID_ERROR_MSG.format(template_id=template_identifier))
    else:
        module.fail_json(msg=TEMPLATE_NAME_ERROR_MSG.format(template_name=template_identifier))


def get_group_ids(module, rest_obj):
    """
    Get the group ids
    """
    params = module.params
    resp_data = rest_obj.get_all_items_with_pagination(GROUP_VIEW)
    values = resp_data["value"]
    device_group_names_list = params.get("device_group_names")
    final_target_list = []
    if values:
        available_ids_tag_map = dict([(item["Id"], item["Name"]) for item in values])
        available_device_tags = available_ids_tag_map.values()
        tags_identifier = "device_group_names"
        validate_identifiers(available_device_tags, device_group_names_list, tags_identifier, module)
        final_target_list = get_identifiers(available_ids_tag_map, device_group_names_list)
    else:
        module.fail_json(msg=INVALID_DEVICES.format(identifier="Group"))
    return final_target_list


def get_device_capabilities(devices_list, identifier):
    if identifier == "device_ids":
        available_ids_capability_map = dict([(item["Id"], item.get("DeviceCapabilities", [])) for item in devices_list])
    else:
        available_ids_capability_map = dict(
            [(item["Identifier"], item.get("DeviceCapabilities", [])) for item in devices_list])
    capable_devices = []
    noncapable_devices = []
    for key, val in available_ids_capability_map.items():
        if 33 in val:
            capable_devices.append(key)
        else:
            noncapable_devices.append(key)
    return {"capable": capable_devices, "non_capable": noncapable_devices}


def get_device_ids(module, rest_obj):
    """
    Get the requested device ids
    """
    params = module.params
    resp_data = rest_obj.get_all_report_details(DEVICE_VIEW)
    values = resp_data["report_list"]
    id_list = params.get("device_ids")
    service_tags_list = params.get("device_service_tags")
    final_target_list = []
    device_capability_map = {}
    identifier = "device_ids"
    if values:
        available_ids_tag_map = dict([(item["Id"], item["Identifier"]) for item in values])
        if id_list:
            available_device_ids = available_ids_tag_map.keys()
            validate_identifiers(available_device_ids, id_list, "device_ids", module)
            final_target_list = id_list
        if service_tags_list:
            available_device_tags = available_ids_tag_map.values()
            validate_identifiers(available_device_tags, service_tags_list, "device_service_tags", module)
            id_list = get_identifiers(available_ids_tag_map, service_tags_list)
            identifier = "device_service_tags"
            final_target_list = id_list
    else:
        module.fail_json(msg=INVALID_DEVICES.format(identifier="Device"))
    if final_target_list:
        device_capability_map = get_device_capabilities(values, identifier)
    return final_target_list, device_capability_map


def validate_capability(module, device_capability_map):
    """
    For any non capable devices return the module with failure with list of
    non capable devices
    """
    if module.params.get("device_ids"):
        device_id_list = module.params.get("device_ids")
        identifier_types = "device_ids"
    else:
        device_id_list = module.params.get("device_service_tags")
        identifier_types = "device_service_tags"
    capable_devices = set(device_id_list) & set(device_capability_map.get("capable", []))
    if len(capable_devices) == 0 or capable_devices and len(capable_devices) != len(device_id_list):
        non_capable_devices = list(set(device_id_list) - capable_devices)
        module.fail_json(msg=NO_CAPABLE_DEVICES.format(identifier_types),
                         incompatible_devices=non_capable_devices)


def create_payload(module, rest_obj):
    """
    create the compliance baseline payload
    """
    params = module.params
    device_id_list = params.get("device_ids")
    device_service_tags_list = params.get("device_service_tags")
    group_service_tags_list = params.get("device_group_names")
    final_target_list = []
    if device_id_list or device_service_tags_list:
        device_id_list, device_capability_map = get_device_ids(module, rest_obj)
        validate_capability(module, device_capability_map)
        final_target_list = device_id_list
    if group_service_tags_list:
        group_id_list = get_group_ids(module, rest_obj)
        final_target_list.extend(group_id_list)
    payload = {
        "Name": params["names"][0]
    }
    if module.params.get("template_id") or module.params.get("template_name"):
        template = get_template_details(module, rest_obj)
        payload["TemplateId"] = template["Id"]
    if module.params.get("description"):
        payload["Description"] = module.params["description"]
    if final_target_list:
        payload["BaselineTargets"] = [{"Id": item} for item in final_target_list]
    return payload


def get_baseline_compliance_info(rest_obj, baseline_identifier_val, attribute="Id"):
    """
    Get the baseline info for the created compliance baseline
    """
    data = rest_obj.get_all_items_with_pagination(COMPLIANCE_BASELINE)
    value = data["value"]
    baseline_info = {}
    for item in value:
        if item[attribute] == baseline_identifier_val:
            baseline_info = item
            baseline_info.pop("@odata.type", None)
            baseline_info.pop("@odata.id", None)
            baseline_info.pop("DeviceConfigComplianceReports@odata.navigationLink", None)
            break
    return baseline_info


def track_compliance_task_completion(rest_obj, baseline_identifier_val, module):
    """
    wait for the compliance configuration task to complete
    """
    baseline_info = get_baseline_compliance_info(rest_obj, baseline_identifier_val)
    command = module.params["command"]
    if module.params.get("job_wait"):
        wait_time = 5
        retries_count_limit = module.params["job_wait_timeout"] / wait_time
        retries_count = 0
        time.sleep(wait_time)
        if command == "create":
            msg = CREATE_MSG
        else:
            msg = MODIFY_MSG
        while retries_count <= retries_count_limit:
            if baseline_info["PercentageComplete"] == "100":
                break
            retries_count += 1
            time.sleep(wait_time)
            baseline_info = get_baseline_compliance_info(rest_obj, baseline_identifier_val)
        if baseline_info["PercentageComplete"] != "100":
            msg = TASK_PROGRESS_MSG
    else:
        msg = TASK_PROGRESS_MSG
    return msg, baseline_info


def validate_create_baseline_idempotency(module, rest_obj):
    """
    Idempotency check for compliance baseline create.
    Return error message if baseline name already exists in the system
    """
    name = module.params["names"][0]
    baseline_info = get_baseline_compliance_info(rest_obj, name, attribute="Name")
    if any(baseline_info):
        module.exit_json(msg=BASELINE_CHECK_MODE_CHANGE_MSG.format(name=name), changed=False)
    if not any(baseline_info) and module.check_mode:
        module.exit_json(msg=CHECK_MODE_CHANGES_MSG, changed=True)


def create_baseline(module, rest_obj):
    """
    Create the compliance baseline.
    update the response by getting compliance info.
    Note: The response is updated from GET info reason many attribute values are gving null
    value. which can be retrieved by getting the created compliance info.
    """
    payload = create_payload(module, rest_obj)
    validate_create_baseline_idempotency(module, rest_obj)
    resp = rest_obj.invoke_request('POST', COMPLIANCE_BASELINE, data=payload)
    data = resp.json_data
    compliance_id = data["Id"]
    baseline_info = get_baseline_compliance_info(rest_obj, compliance_id)
    if module.params.get("job_wait"):
        job_failed, message = rest_obj.job_tracking(baseline_info["TaskId"],
                                                    job_wait_sec=module.params["job_wait_timeout"],
                                                    sleep_time=5)
        baseline_updated_info = get_baseline_compliance_info(rest_obj, compliance_id)
        if job_failed is True:
            module.fail_json(msg=message, compliance_status=baseline_updated_info, changed=False)
        else:
            if "successfully" in message:
                module.exit_json(msg=CREATE_MSG, compliance_status=baseline_updated_info, changed=True)
            else:
                module.exit_json(msg=message, compliance_status=baseline_updated_info, changed=False)
    else:
        module.exit_json(msg=TASK_PROGRESS_MSG, compliance_status=baseline_info, changed=True)


def validate_names(command, module):
    """
    The command create, remediate and modify doest not supports more than one name
    """
    names = module.params["names"]
    if command != "delete" and len(names) > 1:
        module.fail_json(msg=NAMES_ERROR)


def delete_idempotency_check(module, rest_obj):
    delete_names = module.params["names"]
    data = rest_obj.get_all_items_with_pagination(COMPLIANCE_BASELINE)
    available_baseline_map = dict([(item["Id"], item["Name"]) for item in data["value"]])
    valid_names = set(delete_names) & set(available_baseline_map.values())
    valid_id_list = get_identifiers(available_baseline_map, valid_names)
    if module.check_mode and len(valid_id_list) > 0:
        module.exit_json(msg=CHECK_MODE_CHANGES_MSG, changed=True)
    if len(valid_id_list) == 0:
        module.exit_json(msg=CHECK_MODE_NO_CHANGES_MSG, changed=False)
    return valid_id_list


def delete_compliance(module, rest_obj):
    """
    Deletes the list of baselines
    """
    valid_id_list = delete_idempotency_check(module, rest_obj)
    rest_obj.invoke_request('POST', DELETE_COMPLIANCE_BASELINE, data={"BaselineIds": valid_id_list})
    module.exit_json(msg=DELETE_MSG, changed=True)


def compare_payloads(modify_payload, current_payload):
    """
    :param modify_payload: payload created to update existing setting
    :param current_payload: already existing payload for specified baseline
    :return: bool - compare existing and requested setting values of baseline in case of modify operations
    if both are same return True
    """
    diff = False
    for key, val in modify_payload.items():
        if current_payload is None or current_payload.get(key) is None:
            return True
        elif isinstance(val, dict):
            if compare_payloads(val, current_payload.get(key)):
                return True
        elif val != current_payload.get(key):
            return True
    return diff


def idempotency_check_for_command_modify(current_payload, expected_payload, module):
    """
    idempotency check in case of modify operation
    :param current_payload: payload modify
    :param expected_payload: already existing payload for specified.
    :param module: ansible module object
    :return: None
    """
    payload_diff = compare_payloads(expected_payload, current_payload)
    if module.check_mode:
        if payload_diff:
            module.exit_json(msg=CHECK_MODE_CHANGES_MSG, changed=True)
        else:
            module.exit_json(msg=CHECK_MODE_NO_CHANGES_MSG, changed=False)
    elif not module.check_mode and not payload_diff:
        module.exit_json(msg=IDEMPOTENCY_MSG, changed=False)


def modify_baseline(module, rest_obj):
    name = module.params["names"][0]
    baseline_info = get_baseline_compliance_info(rest_obj, name, attribute="Name")
    if not any(baseline_info):
        module.fail_json(msg=BASELINE_CHECK_MODE_NOCHANGE_MSG.format(name=name))
    current_payload = create_payload(module, rest_obj)
    current_payload["Id"] = baseline_info["Id"]
    if module.params.get("new_name"):
        new_name = module.params.get("new_name")
        if name != new_name:
            baseline_info_new = get_baseline_compliance_info(rest_obj, new_name, attribute="Name")
            if any(baseline_info_new):
                module.fail_json(msg=BASELINE_CHECK_MODE_CHANGE_MSG.format(name=new_name))
        current_payload["Name"] = new_name
    required_attributes = ["Id", "Name", "Description", "TemplateId", "BaselineTargets"]
    existing_payload = dict([(key, val) for key, val in baseline_info.items() if key in required_attributes and val])
    if existing_payload.get("BaselineTargets"):
        target = [{"Id": item["Id"]} for item in existing_payload["BaselineTargets"]]
        existing_payload["BaselineTargets"] = target
    idempotency_check_for_command_modify(existing_payload, current_payload, module)
    existing_payload.update(current_payload)
    baseline_update_uri = COMPLIANCE_BASELINE + "({baseline_id})".format(baseline_id=existing_payload["Id"])
    resp = rest_obj.invoke_request('PUT', baseline_update_uri, data=existing_payload)
    data = resp.json_data
    compliance_id = data["Id"]
    baseline_info = get_baseline_compliance_info(rest_obj, compliance_id)
    if module.params.get("job_wait"):
        job_failed, message = rest_obj.job_tracking(baseline_info["TaskId"],
                                                    job_wait_sec=module.params["job_wait_timeout"], sleep_time=5)
        baseline_updated_info = get_baseline_compliance_info(rest_obj, compliance_id)
        if job_failed is True:
            module.fail_json(msg=message, compliance_status=baseline_updated_info, changed=False)
        else:
            if "successfully" in message:
                module.exit_json(msg=MODIFY_MSG, compliance_status=baseline_updated_info, changed=True)
            else:
                module.exit_json(msg=message, compliance_status=baseline_updated_info, changed=False)
    else:
        module.exit_json(msg=TASK_PROGRESS_MSG, compliance_status=baseline_info, changed=True)


def get_ome_version(rest_obj):
    resp = rest_obj.invoke_request('GET', OME_INFO)
    data = resp.json_data
    return data["Version"]


def validate_remediate_idempotency(module, rest_obj):
    name = module.params["names"][0]
    baseline_info = get_baseline_compliance_info(rest_obj, name, attribute="Name")
    if not any(baseline_info):
        module.fail_json(msg=BASELINE_CHECK_MODE_NOCHANGE_MSG.format(name=name))
    valid_id_list, device_capability_map = get_device_ids(module, rest_obj)
    compliance_reports = rest_obj.get_all_items_with_pagination(CONFIG_COMPLIANCE_URI.format(baseline_info["Id"]))
    device_id_list = module.params.get("device_ids")
    device_service_tags_list = module.params.get("device_service_tags")
    if device_id_list:
        compliance_report_map = dict([(item["Id"], item["ComplianceStatus"]) for item in compliance_reports["value"]])
        if not any(compliance_report_map):
            module.exit_json(msg=CHECK_MODE_NO_CHANGES_MSG)
        invalid_values = list(set(device_id_list) - set(compliance_report_map.keys()))
        if invalid_values:
            module.fail_json(
                INVALID_COMPLIANCE_IDENTIFIER.format("device_ids", ",".join(map(str, invalid_values)), name))
        report_devices = list(set(device_id_list) & set(compliance_report_map.keys()))
        noncomplaint_devices = [device for device in report_devices if compliance_report_map[device] == "NONCOMPLIANT"
                                or compliance_report_map[device] == 2]
    elif device_service_tags_list:
        compliance_report_map = dict(
            [(item["ServiceTag"], item["ComplianceStatus"]) for item in compliance_reports["value"]])
        if not any(compliance_report_map):
            module.exit_json(msg=CHECK_MODE_NO_CHANGES_MSG)
        invalid_values = list(set(device_service_tags_list) - set(compliance_report_map.keys()))
        if invalid_values:
            module.fail_json(
                INVALID_COMPLIANCE_IDENTIFIER.format("device_service_tags", ",".join(map(str, invalid_values)), name))
        report_devices = list(set(device_service_tags_list) & set(compliance_report_map.keys()))
        service_tag_id_map = dict(
            [(item["ServiceTag"], item["Id"]) for item in compliance_reports["value"]])
        noncomplaint_devices = [service_tag_id_map[device] for device in report_devices if compliance_report_map[device] == "NONCOMPLIANT"
                                or compliance_report_map[device] == 2]
    else:
        compliance_report_map = dict([(item["Id"], item["ComplianceStatus"]) for item in compliance_reports["value"]])
        if not any(compliance_report_map):
            module.exit_json(msg=CHECK_MODE_NO_CHANGES_MSG)
        noncomplaint_devices = [device for device, compliance_status in compliance_report_map.items() if
                                compliance_status == "NONCOMPLIANT" or compliance_status == 2]
    if len(noncomplaint_devices) == 0:
        module.exit_json(msg=CHECK_MODE_NO_CHANGES_MSG)
    if module.check_mode and noncomplaint_devices:
        module.exit_json(msg=CHECK_MODE_CHANGES_MSG, changed=True)
    return noncomplaint_devices, baseline_info


def create_remediate_payload(noncomplaint_devices, baseline_info, rest_obj):
    ome_version = get_ome_version(rest_obj)
    payload = {
        "Id": baseline_info["Id"],
        "Schedule": {
            "RunNow": True,
            "RunLater": False
        }
    }
    pattern = re.compile(r'(1|2|3)\.(0|1|2|3|4)\.?')
    if pattern.match(ome_version):
        payload["TargetIds"] = noncomplaint_devices
    else:
        payload["DeviceIds"] = noncomplaint_devices
    return payload


def remediate_baseline(module, rest_obj):
    noncomplaint_devices, baseline_info = validate_remediate_idempotency(module, rest_obj)
    remediate_payload = create_remediate_payload(noncomplaint_devices, baseline_info, rest_obj)
    resp = rest_obj.invoke_request('POST', REMEDIATE_BASELINE, data=remediate_payload)
    job_id = resp.json_data
    if module.params.get("job_wait"):
        job_failed, message = rest_obj.job_tracking(job_id, job_wait_sec=module.params["job_wait_timeout"])
        if job_failed is True:
            module.fail_json(msg=message, job_id=job_id, changed=False)
        else:
            if "successfully" in message:
                module.exit_json(msg=REMEDIATE_MSG, job_id=job_id, changed=True)
            else:
                module.exit_json(msg=message, job_id=job_id, changed=False)
    else:
        module.exit_json(msg=TASK_PROGRESS_MSG, job_id=job_id, changed=True)


def validate_job_time(command, module):
    """
    The command create, remediate and modify time validation
    """
    job_wait = module.params["job_wait"]
    if command != "delete" and job_wait:
        job_wait_timeout = module.params["job_wait_timeout"]
        if job_wait_timeout <= 0:
            module.fail_json(msg=INVALID_TIME.format(job_wait_timeout))


def compliance_operation(module, rest_obj):
    command = module.params.get("command")
    validate_names(command, module)
    validate_job_time(command, module)
    if command == "create":
        create_baseline(module, rest_obj)
    if command == "modify":
        modify_baseline(module, rest_obj)
    if command == "delete":
        delete_compliance(module, rest_obj)
    if command == "remediate":
        remediate_baseline(module, rest_obj)


def main():
    module = AnsibleModule(
        argument_spec={
            "hostname": {"required": True, "type": 'str'},
            "username": {"required": True, "type": 'str'},
            "password": {"required": True, "type": 'str', "no_log": True},
            "port": {"required": False, "default": 443, "type": 'int'},
            "command": {"default": "create",
                        "choices": ['create', 'modify', 'delete', 'remediate']},
            "names": {"required": True, "type": 'list', "elements": 'str'},
            "template_name": {"type": 'str'},
            "template_id": {"type": 'int'},
            "device_ids": {"required": False, "type": 'list', "elements": 'int'},
            "device_service_tags": {"required": False, "type": 'list', "elements": 'str'},
            "device_group_names": {"required": False, "type": 'list', "elements": 'str'},
            "description": {"type": 'str'},
            "job_wait": {"required": False, "type": 'bool', "default": True},
            "job_wait_timeout": {"required": False, "type": 'int', "default": 10800},
            "new_name": {"type": 'str'},
        },
        required_if=[
            ['command', 'create', ['template_name', 'template_id'], True],
            ['command', 'remediate', ['device_ids', 'device_service_tags', 'job_wait', 'job_wait_timeout'], True],
            ['command', 'modify',
             ['new_name', 'description', 'template_name', 'template_id', 'device_ids', 'device_service_tags',
              'device_group_names'], True],
        ],
        mutually_exclusive=[
            ('device_ids', 'device_service_tags'),
            ('device_ids', 'device_group_names'),
            ('device_service_tags', 'device_group_names'),
            ('template_id', 'template_name')],

        supports_check_mode=True)
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            compliance_operation(module, rest_obj)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, TypeError, SSLError, ConnectionError, SSLValidationError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
