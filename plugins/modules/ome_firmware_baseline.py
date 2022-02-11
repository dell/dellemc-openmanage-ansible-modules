#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.0.1
# Copyright (C) 2019-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_firmware_baseline
short_description: Create, modify, or delete a firmware baseline on OpenManage Enterprise or OpenManage Enterprise Modular
description: This module allows to create, modify, or delete a firmware baseline on OpenManage Enterprise or OpenManage Enterprise Modular.
version_added: "2.0.0"
author:
  - Jagadeesh N V(@jagadeeshnv)
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  state:
    description:
      - C(present) creates or modifies a baseline.
      - C(absent) deletes an existing baseline.
    choices:
      - present
      - absent
    default: present
    type: str
    version_added: 3.4.0
  baseline_name:
    type: str
    description:
      - Name of the the baseline.
      - This option is mutually exclusive with I(baseline_id).
  baseline_id:
    type: int
    description:
      - ID of the existing baseline.
      - This option is mutually exclusive with I(baseline_name).
    version_added: 3.4.0
  new_baseline_name:
    description: New name of the baseline.
    type: str
    version_added: 3.4.0
  baseline_description:
    type: str
    description:
      - Description for the baseline being created.
  catalog_name:
    type: str
    description:
      - Name of the catalog to be associated with the baseline.
  downgrade_enabled:
    type: bool
    description:
      - Indicates whether firmware downgrade is allowed for the devices in the baseline.
      - This value will be set to C(True) by default, if not provided during baseline creation.
  is_64_bit:
    type: bool
    description:
      - Indicates if the repository contains 64-bit DUPs.
      - This value will be set to C(True) by default, if not provided during baseline creation.
  device_ids:
    type: list
    elements: int
    description:
      - List of device IDs.
      - This option is mutually exclusive with I(device_service_tags) and I(device_group_names).
  device_service_tags:
    type: list
    elements: str
    description:
      - List of device service tags.
      - This option is mutually exclusive with I(device_ids) and I(device_group_names).
  device_group_names:
    type: list
    elements: str
    description:
      - List of group names.
      - This option is mutually exclusive with I(device_ids) and I(device_service_tags).
  job_wait:
    description:
      - Provides the option to wait for job completion.
      - This option is applicable when I(state) is C(present).
    type: bool
    default: true
    version_added: 3.4.0
  job_wait_timeout:
    description:
      - The maximum wait time of I(job_wait) in seconds. The job is tracked only for this duration.
      - This option is applicable when I(job_wait) is C(True).
    type: int
    default: 600
    version_added: 3.4.0
requirements:
    - "python >= 3.8.6"
notes:
    - Run this module from a system that has direct access to DellEMC OpenManage Enterprise or OpenManage Enterprise Modular.
    - I(device_group_names) option is not applicable for OpenManage Enterprise Modular.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Create baseline for device IDs
  dellemc.openmanage.ome_firmware_baseline:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    baseline_name: "baseline_name"
    baseline_description: "baseline_description"
    catalog_name: "catalog_name"
    device_ids:
      - 1010
      - 2020

- name: Create baseline for servicetags
  dellemc.openmanage.ome_firmware_baseline:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    baseline_name: "baseline_name"
    baseline_description: "baseline_description"
    catalog_name: "catalog_name"
    device_service_tags:
      - "SVCTAG1"
      - "SVCTAG2"

- name: Create baseline for device groups without job tracking
  dellemc.openmanage.ome_firmware_baseline:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    baseline_name: "baseline_name"
    baseline_description: "baseline_description"
    catalog_name: "catalog_name"
    device_group_names:
      - "Group1"
      - "Group2"
    job_wait: no

- name: Modify an existing baseline
  dellemc.openmanage.ome_firmware_baseline:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    baseline_name: "existing_baseline_name"
    new_baseline_name: "new_baseline_name"
    baseline_description: "new baseline_description"
    catalog_name: "catalog_other"
    device_group_names:
      - "Group3"
      - "Group4"
      - "Group5"
    downgrade_enabled: no
    is_64_bit: yes

- name: Delete a baseline
  dellemc.openmanage.ome_firmware_baseline:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: absent
    baseline_name: "baseline_name"
'''

RETURN = r'''
---
msg:
  description: Overall status of the firmware baseline operation.
  returned: always
  type: str
  sample: "Successfully created the firmware baseline."
baseline_status:
  description: Details of the baseline status.
  returned: success
  type: dict
  sample: {
    "CatalogId": 123,
    "Description": "BASELINE DESCRIPTION",
    "DeviceComplianceReports": [],
    "DowngradeEnabled": true,
    "Id": 23,
    "Is64Bit": true,
    "Name": "my_baseline",
    "RepositoryId": 123,
    "RepositoryName": "catalog123",
    "RepositoryType": "HTTP",
    "Targets": [
        {
            "Id": 10083,
            "Type": {
                "Id": 1000,
                "Name": "DEVICE"
            }
        },
        {
            "Id": 10076,
            "Type": {
                "Id": 1000,
                "Name": "DEVICE"
            }
        }
    ],
    "TaskId": 11235,
    "TaskStatusId": 2060
  }
job_id:
  description: Job ID of the baseline task.
  returned: When baseline job is in running state
  type: int
  sample: 10123
baseline_id:
  description: ID of the deleted baseline.
  returned: When I(state) is C(absent)
  type: int
  sample: 10123
error_info:
  type: dict
  description: Details of http error.
  returned: on http error
  sample:  {
    "error": {
      "@Message.ExtendedInfo": [
        {
          "Message": "Unable to retrieve baseline list either because the device ID(s) entered are invalid",
          "Resolution": "Make sure the entered device ID(s) are valid and retry the operation.",
          "Severity": "Critical"
        }
      ],
      "code": "Base.1.0.GeneralError",
      "message": "A general error has occurred. See ExtendedInfo for more information."
    }
  }
'''

BASELINE_URI = "UpdateService/Baselines"
ID_BASELINE_URI = "UpdateService/Baselines({Id})"
DELETE_BASELINE_URI = "UpdateService/Actions/UpdateService.RemoveBaselines"
CATALOG_URI = "UpdateService/Catalogs"
BASELINE_JOB_RUNNING = "Firmware baseline '{name}' with ID {id} is running. Please retry after job completion."
BASELINE_DEL_SUCCESS = "Successfully deleted the firmware baseline."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
INVALID_BASELINE_ID = "Invalid baseline ID provided."
BASELINE_TRIGGERED = "Successfully triggered the firmware baseline task."
NO_CATALOG_MESSAGE = "Catalog name not provided for baseline creation."
NO_TARGETS_MESSAGE = "Targets not specified for baseline creation."
CATALOG_STATUS_MESSAGE = "Unable to create the firmware baseline as the catalog is in {status} status."
BASELINE_UPDATED = "Successfully {op} the firmware baseline."
SETTLING_TIME = 3
JOB_POLL_INTERVAL = 10
GROUP_ID = 6000


import json
import time
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.common.dict_transformations import recursive_diff


def get_baseline_from_name(rest_obj, baseline):
    resp = rest_obj.get_all_items_with_pagination(BASELINE_URI)
    baselines_list = resp.get("value")
    bsln = baseline
    for d in baselines_list:
        if d['Name'] == baseline.get('Name'):
            bsln = d
            break
    nlist = list(bsln)
    for k in nlist:
        if str(k).lower().startswith('@odata'):
            bsln.pop(k)
    return bsln


def check_existing_baseline(module, rest_obj):
    baseline_id = module.params.get("baseline_id")
    srch_key = "Name"
    srch_val = module.params.get("baseline_name")
    if baseline_id:
        srch_key = "Id"
        srch_val = module.params.get("baseline_id")
    baseline_cfgs = []
    resp = rest_obj.get_all_items_with_pagination(BASELINE_URI)
    baselines = resp.get("value")
    for d in baselines:
        if d[srch_key] == srch_val:
            baseline_cfgs.append(d)
            if baseline_id:
                break
    return baseline_cfgs


def get_catrepo_ids(module, cat_name, rest_obj):
    if cat_name is not None:
        resp_data = rest_obj.get_all_items_with_pagination(CATALOG_URI)
        values = resp_data["value"]
        if values:
            for catalog in values:
                repo = catalog.get("Repository")
                if repo.get("Name") == cat_name:
                    if catalog.get('Status') != 'Completed':
                        module.fail_json(msg=CATALOG_STATUS_MESSAGE.format(status=catalog.get('Status')))
                    return catalog.get("Id"), repo.get("Id")
    return None, None


def get_dev_ids(module, rest_obj, param, devkey):
    paramlist = module.params[param]
    resp_data = rest_obj.get_all_items_with_pagination("DeviceService/Devices")
    values = resp_data["value"]
    targets = []
    if values:
        devlist = values
        device_resp = dict([(device[devkey], device) for device in devlist])
        for st in paramlist:
            if st in device_resp:
                djson = device_resp[st]
                target = {}
                device_type = {}
                device_type['Id'] = djson['Type']
                device_type['Name'] = "DEVICE"
                target['Id'] = djson['Id']
                target['Type'] = device_type
                targets.append(target)
            else:
                module.fail_json(msg="Unable to complete the operation because the entered target"
                                     " {0} '{1}' is invalid.".format(devkey, st))
    return targets


def get_group_ids(module, rest_obj):
    grp_name_list = module.params.get("device_group_names")
    resp_data = rest_obj.get_all_items_with_pagination("GroupService/Groups")
    values = resp_data["value"]
    targets = []
    if values:
        grplist = values
        device_resp = dict([(str(grp['Name']), grp) for grp in grplist])
        for st in grp_name_list:
            if st in device_resp:
                djson = device_resp[st]
                target = {}
                device_type = {}
                device_type['Id'] = GROUP_ID
                device_type['Name'] = "GROUP"
                target['Id'] = djson['Id']
                target['Type'] = device_type
                targets.append(target)
            else:
                module.fail_json(msg="Unable to complete the operation because the entered target"
                                     " Group Name '{0}' is invalid.".format(st))
    return targets


def get_target_list(module, rest_obj):
    target_list = None
    if module.params.get("device_service_tags"):
        target_list = get_dev_ids(module, rest_obj, "device_service_tags", "DeviceServiceTag")
    elif module.params.get("device_group_names"):
        target_list = get_group_ids(module, rest_obj)
    elif module.params.get("device_ids"):
        target_list = get_dev_ids(module, rest_obj, "device_ids", "Id")
    return target_list


def exit_baseline(module, rest_obj, baseline, op):
    msg = BASELINE_TRIGGERED
    time.sleep(SETTLING_TIME)
    try:
        bsln = get_baseline_from_name(rest_obj, baseline)
    except Exception:
        bsln = baseline
    if module.params.get("job_wait"):
        job_failed, job_message = rest_obj.job_tracking(
            baseline.get('TaskId'), job_wait_sec=module.params["job_wait_timeout"], sleep_time=JOB_POLL_INTERVAL)
        if job_failed is True:
            module.fail_json(msg=job_message, baseline_status=bsln)
        msg = BASELINE_UPDATED.format(op=op)
    module.exit_json(msg=msg, baseline_status=bsln, changed=True)


def _get_baseline_payload(module, rest_obj):
    cat_name = module.params.get("catalog_name")
    cat_id, repo_id = get_catrepo_ids(module, cat_name, rest_obj)
    if cat_id is None or repo_id is None:
        module.fail_json(msg="No Catalog with name {0} found".format(cat_name))
    targets = get_target_list(module, rest_obj)
    if targets is None:
        module.fail_json(msg=NO_TARGETS_MESSAGE)
    baseline_name = module.params.get("baseline_name")
    baseline_payload = {
        "Name": baseline_name,
        "CatalogId": cat_id,
        "RepositoryId": repo_id,
        "Targets": targets
    }
    baseline_payload['Description'] = module.params.get("baseline_description")
    de = module.params.get("downgrade_enabled")
    baseline_payload['DowngradeEnabled'] = de if de is not None else True
    sfb = module.params.get("is_64_bit")
    baseline_payload['Is64Bit'] = sfb if sfb is not None else True
    return baseline_payload


def create_baseline(module, rest_obj):
    myparams = module.params
    if not any([myparams.get("device_ids"), myparams.get("device_service_tags"), myparams.get("device_group_names")]):
        module.fail_json(msg=NO_TARGETS_MESSAGE)
    if not myparams.get("catalog_name"):
        module.fail_json(msg=NO_CATALOG_MESSAGE)
    payload = _get_baseline_payload(module, rest_obj)
    if module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    resp = rest_obj.invoke_request("POST", BASELINE_URI, data=payload)
    exit_baseline(module, rest_obj, resp.json_data, 'created')


def update_modify_payload(module, rest_obj, modify_payload, current_baseline):
    paylist = ['Name', "CatalogId", "RepositoryId", 'Description', 'DowngradeEnabled', 'Is64Bit']
    diff_tuple = recursive_diff(modify_payload, current_baseline)
    diff = 0
    payload = dict([(item, current_baseline.get(item)) for item in paylist])
    if diff_tuple:
        if diff_tuple[0]:
            diff += 1
            payload.update(diff_tuple[0])
    payload['Targets'] = current_baseline.get('Targets', [])
    inp_targets_list = get_target_list(module, rest_obj)
    if inp_targets_list:
        inp_target_dict = dict([(item['Id'], item['Type']['Id']) for item in inp_targets_list])
        cur_target_dict = dict([(item['Id'], item['Type']['Id']) for item in current_baseline.get('Targets', [])])
        diff_tuple = recursive_diff(inp_target_dict, cur_target_dict)
        if diff_tuple:
            diff += 1
            payload['Targets'] = inp_targets_list
    if diff == 0:
        module.exit_json(msg=NO_CHANGES_MSG)
    payload['Id'] = current_baseline['Id']
    return payload


def modify_baseline(module, rest_obj, baseline_list):
    d = baseline_list[0]
    if d["TaskStatusId"] == 2050:
        module.fail_json(msg=BASELINE_JOB_RUNNING.format(name=d["Name"], id=d["Id"]), job_id=d['TaskId'])
    mparam = module.params
    current_baseline = baseline_list[0]
    modify_payload = {}
    if mparam.get('catalog_name'):
        cat_id, repo_id = get_catrepo_ids(module, mparam.get('catalog_name'), rest_obj)
        if cat_id is None or repo_id is None:
            module.fail_json(msg="No Catalog with name {0} found".format(mparam.get('catalog_name')))
        modify_payload["CatalogId"] = cat_id
        modify_payload["RepositoryId"] = repo_id
    if mparam.get('new_baseline_name'):
        modify_payload['Name'] = mparam.get('new_baseline_name')
    if mparam.get("baseline_description"):
        modify_payload['Description'] = mparam.get("baseline_description")
    if module.params.get("downgrade_enabled") is not None:
        modify_payload['DowngradeEnabled'] = module.params.get("downgrade_enabled")
    if module.params.get("is_64_bit") is not None:
        modify_payload['Is64Bit'] = module.params.get("is_64_bit")
    payload = update_modify_payload(module, rest_obj, modify_payload, current_baseline)
    if module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    resp = rest_obj.invoke_request("PUT", ID_BASELINE_URI.format(Id=str(payload["Id"])), data=payload)
    exit_baseline(module, rest_obj, resp.json_data, 'modified')


def delete_baseline(module, rest_obj, baseline_list):
    delete_ids = []
    d = baseline_list[0]
    if d["TaskStatusId"] == 2050:
        module.fail_json(msg=BASELINE_JOB_RUNNING.format(name=d["Name"], id=d["Id"]), job_id=d['TaskId'])
    delete_ids.append(d["Id"])
    delete_payload = {"BaselineIds": delete_ids}
    if module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    rest_obj.invoke_request('POST', DELETE_BASELINE_URI, data=delete_payload)
    module.exit_json(msg=BASELINE_DEL_SUCCESS, changed=True, baseline_id=delete_ids[0])


def main():
    specs = {
        "state": {"default": "present", "choices": ['present', 'absent']},
        "baseline_name": {"type": 'str'},
        "baseline_id": {"type": 'int'},
        "baseline_description": {"type": 'str'},
        "new_baseline_name": {"type": 'str'},
        "catalog_name": {"type": 'str'},
        "downgrade_enabled": {"type": 'bool'},
        "is_64_bit": {"type": 'bool'},
        "device_ids": {"type": 'list', "elements": 'int'},
        "device_service_tags": {"type": 'list', "elements": 'str'},
        "device_group_names": {"type": 'list', "elements": 'str'},
        "job_wait": {"type": 'bool', "default": True},
        "job_wait_timeout": {"type": 'int', "default": 600}
    }
    specs.update(ome_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[
            ('device_ids', 'device_service_tags', 'device_group_names'),
            ('baseline_name', 'baseline_id')
        ],
        required_one_of=[('baseline_name', 'baseline_id')],
        supports_check_mode=True)

    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            baseline_list = check_existing_baseline(module, rest_obj)
            if module.params.get('state') == 'absent':
                if baseline_list:
                    delete_baseline(module, rest_obj, baseline_list)
                module.exit_json(msg=NO_CHANGES_MSG)
            else:
                if baseline_list:
                    modify_baseline(module, rest_obj, baseline_list)
                else:
                    if module.params.get('baseline_id'):
                        module.fail_json(msg=INVALID_BASELINE_ID)
                    create_baseline(module, rest_obj)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, TypeError, SSLError, ConnectionError, SSLValidationError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
