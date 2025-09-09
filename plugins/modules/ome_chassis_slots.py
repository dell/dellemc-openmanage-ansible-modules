#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.1
# Copyright (C) 2021-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: ome_chassis_slots
short_description: Rename sled slots on OpenManage Enterprise Modular
description: "This module allows to rename sled slots on OpenManage Enterprise Modular either using device id or device
service tag or using chassis service tag and slot number."
version_added: "3.6.0"
author:
  - Jagadeesh N V(@jagadeeshnv)
  - Akash Shendge(@shenda1)
extends_documentation_fragment:
  - dellemc.openmanage.omem_auth_options
options:
  device_options:
    type: list
    elements: dict
    description:
      - The ID or service tag of the sled in the slot and the new name for the slot.
      -  I(device_options) is mutually exclusive with I(slot_options).
    suboptions:
      device_id:
        type: int
        description:
          - Device ID of the sled in the slot.
          - This is mutually exclusive with I(device_service_tag).
      device_service_tag:
        type: str
        description:
          - Service tag of the sled in the slot.
          - This is mutually exclusive with I(device_id).
      slot_name:
        type: str
        description: Provide name for the slot.
        required: true
  slot_options:
    type: list
    elements: dict
    description:
      - The service tag of the chassis, slot number of the slot to be renamed, and the new name for the slot.
      - I(slot_options) is mutually exclusive with I(device_options).
    suboptions:
      chassis_service_tag:
        type: str
        description: Service tag of the chassis.
        required: true
      slots:
        type: list
        elements: dict
        description:
          - The slot number and the new name for the slot.
        required: true
        suboptions:
          slot_number:
            type: int
            description: The slot number of the slot to be renamed.
            required: true
          slot_name:
            type: str
            description: Provide name for the slot.
            required: true
requirements:
  - "python >= 3.9.6"
notes:
  - "This module initiates the refresh inventory task. It may take a minute for new names to be reflected.
  If the task exceeds 300 seconds to refresh, the task times out."
  - Run this module from a system that has direct access to Dell OpenManage Enterprise Modular.
  - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Rename the slots in multiple chassis using slot number and chassis service tag
  dellemc.openmanage.ome_chassis_slots:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    slot_options:
      - chassis_service_tag: ABC1234
        slots:
          - slot_number: 1
            slot_name: sled_name_1
          - slot_number: 2
            slot_name: sled_name_2
      - chassis_service_tag: ABC1235
        slots:
          - slot_number: 1
            slot_name: sled_name_1
          - slot_number: 2
            slot_name: sled_name_2

- name: Rename single slot name of the sled using sled ID
  dellemc.openmanage.ome_chassis_slots:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_options:
      - device_id: 10054
        slot_name: slot_device_name_1

- name: Rename single slot name of the sled using sled service tag
  dellemc.openmanage.ome_chassis_slots:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_options:
      - device_service_tag: ABC1234
        slot_name: service_tag_slot

- name: Rename multiple slot names of the devices
  dellemc.openmanage.ome_chassis_slots:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_options:
      - device_id: 10054
        slot_name: sled_name_1
      - device_service_tag: ABC1234
        slot_name: sled_name_2
      - device_id: 10055
        slot_name: sled_name_3
      - device_service_tag: PQR1234
        slot_name: sled_name_4
"""

RETURN = """
---
msg:
  type: str
  description: Overall status of the slot rename operation.
  returned: always
  sample: "Successfully renamed the slot(s)."
slot_info:
  description:
    - Information of the slots that are renamed successfully.
    - The C(DeviceServiceTag) and C(DeviceId) options are available only if I(device_options) is used.
    - C(NOTE) Only the slots which were renamed are listed.
  type: list
  elements: dict
  returned: if at least one slot renamed
  sample: [
    {
        "ChassisId": 10053,
        "ChassisServiceTag": "ABCD123",
        "DeviceName": "",
        "DeviceType": 1000,
        "JobId": 15746,
        "SlotId": "10072",
        "SlotName": "slot_op2",
        "SlotNumber": "6",
        "SlotType": 2000
    },
    {
        "ChassisId": 10053,
        "ChassisName": "MX-ABCD123",
        "ChassisServiceTag": "ABCD123",
        "DeviceType": "3000",
        "JobId": 15747,
        "SlotId": "10070",
        "SlotName": "slot_op2",
        "SlotNumber": "4",
        "SlotType": "2000"
    },
    {
        "ChassisId": "10053",
        "ChassisName": "MX-PQRS123",
        "ChassisServiceTag": "PQRS123",
        "DeviceId": "10054",
        "DeviceServiceTag": "XYZ5678",
        "DeviceType": "1000",
        "JobId": 15761,
        "SlotId": "10067",
        "SlotName": "a1",
        "SlotNumber": "1",
        "SlotType": "2000"
    }
  ]
rename_failed_slots:
  description:
    - Information of the valid slots that are not renamed.
    - C(JobStatus) is shown if rename job fails.
    - C(NOTE) Only slots which were not renamed are listed.
  type: list
  elements: dict
  returned: if at least one slot renaming fails
  sample: [
      {
        "ChassisId": "12345",
        "ChassisName": "MX-ABCD123",
        "ChassisServiceTag": "ABCD123",
        "DeviceType": "4000",
        "JobId": 1234,
        "JobStatus": "Aborted",
        "SlotId": "10061",
        "SlotName": "c2",
        "SlotNumber": "1",
        "SlotType": "4000"
    },
    {
        "ChassisId": "10053",
        "ChassisName": "MX-PQRS123",
        "ChassisServiceTag": "PQRS123",
        "DeviceType": "1000",
        "JobId": 0,
        "JobStatus": "HTTP Error 400: Bad Request",
        "SlotId": "10069",
        "SlotName": "b2",
        "SlotNumber": "3",
        "SlotType": "2000"
    }
  ]
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
                "MessageId": "CGEN1014",
                "RelatedProperties": [],
                "Message": "Unable to complete the operation because an invalid value is entered for the property
                Invalid json type: STRING for Edm.Int64 property: Id .",
                "MessageArgs": [
                    "Invalid json type: STRING for Edm.Int64 property: Id"
                ],
                "Severity": "Critical",
                "Resolution": "Enter a valid value for the property and retry the operation. For more information about
                valid values, see the OpenManage Enterprise-Modular User's Guide available on the support site."
            }
        ]
    }
}
"""

import json
import time
from ssl import SSLError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.common.dict_transformations import recursive_diff

DEVICE_URI = "DeviceService/Devices"
JOB_URI = "JobService/Jobs"
DEVICE_REPEATED = "Duplicate device entry found for devices with identifiers {0}."
INVALID_SLOT_DEVICE = "Unable to rename one or more slots because either the specified device is invalid or slots " \
                      "cannot be configured. The devices for which the slots cannot be renamed are: {0}."
JOBS_TRIG_FAIL = "Unable to initiate the slot name rename jobs."
SUCCESS_MSG = "Successfully renamed the slot(s)."
SUCCESS_REFRESH_MSG = "The rename slot job(s) completed successfully. " \
                      "For changes to reflect, refresh the inventory task manually."
FAILED_MSG = "Failed to rename {0} of {1} slot names."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
SLOT_JOB_DESC = "The rename slot task initiated from OpenManage Ansible Module collections"
REFRESH_JOB_DESC = "The refresh inventory task initiated from OpenManage Ansible Module collections"
CHASSIS_TAG_INVALID = "Provided chassis {0} is invalid."
INVALID_SLOT_NUMBERS = "Unable to rename one or more slots because the slot number(s) are invalid: {0}."
SLOT_NUM_DUP = "Slot numbers are repeated for chassis {0}."
CHASSIS_REPEATED = "Duplicate chassis entry found for chassis with service tags {0}."
SETTLING_TIME = 2  # time gap between so consecutive job trigger
JOB_TIMEOUT = 300
JOB_INTERVAL = 5


def get_device_slot_config(module, rest_obj):
    ids, tags = {}, {}
    dvc_list = []
    for dvc in module.params.get('device_options'):
        sn = dvc.get('slot_name')
        id = dvc.get('device_id')
        st = dvc.get('device_service_tag')
        if id:
            ids[str(id)] = sn
            dvc_list.append(str(id))
        else:
            tags[st] = sn
            dvc_list.append(st)
    duplicate = [x for i, x in enumerate(dvc_list) if i != dvc_list.index(x)]
    if duplicate:
        module.exit_json(msg=DEVICE_REPEATED.format((';'.join(set(duplicate)))), failed=True)
    resp = rest_obj.get_all_items_with_pagination(DEVICE_URI)
    devices = resp.get('value')
    all_dvcs = {}
    invalid_slots = set()
    ident_map, name_map = {}, {}
    for dvc in devices:
        if not ids and not tags:
            break
        id = str(dvc.get('Id'))
        tag = dvc.get('Identifier')
        slot_cfg = dvc.get('SlotConfiguration')
        all_dvcs[tag] = slot_cfg
        if id in ids:
            if not slot_cfg or not slot_cfg.get("SlotNumber"):
                invalid_slots.add(id)
            else:
                ident_map[id] = tag
                name_map[id] = slot_cfg['SlotName']
                slot_cfg['new_name'] = ids[id]
                slot_cfg['DeviceServiceTag'] = tag
                slot_cfg['DeviceId'] = id
        if tag in tags:
            if not slot_cfg or not slot_cfg.get("SlotNumber"):
                invalid_slots.add(tag)
            else:
                ident_map[tag] = tag
                name_map[tag] = slot_cfg['SlotName']
                slot_cfg['new_name'] = tags[tag]
                slot_cfg['DeviceServiceTag'] = tag
                slot_cfg['DeviceId'] = id
    idf_list = list(ident_map.values())
    duplicate = [x for i, x in enumerate(idf_list) if i != idf_list.index(x)]
    if duplicate:
        module.exit_json(msg=DEVICE_REPEATED.format((';'.join(set(duplicate)))), failed=True)
    invalid_slots.update(set(ids.keys()) - set(ident_map.keys()))
    invalid_slots.update(set(tags.keys()) - set(ident_map.keys()))
    if invalid_slots:
        module.exit_json(msg=INVALID_SLOT_DEVICE.format(';'.join(invalid_slots)), failed=True)
    slot_dict_diff = {}
    id_diff = recursive_diff(ids, name_map)
    if id_diff and id_diff[0]:
        diff = dict([(int(k), all_dvcs[ident_map[k]]) for k, v in (id_diff[0]).items()])
        slot_dict_diff.update(diff)
    tag_diff = recursive_diff(tags, name_map)
    if tag_diff and tag_diff[0]:
        diff = dict([(ident_map[k], all_dvcs[k]) for k, v in (tag_diff[0]).items()])
        slot_dict_diff.update(diff)
    if not slot_dict_diff:
        module.exit_json(msg=NO_CHANGES_MSG)
    if module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    return slot_dict_diff


def start_slot_name_jobs(rest_obj, slot_data):
    slot_type = {'2000': "Sled Slot", '4000': "IO Module Slot", '2100': "Storage Sled"}
    failed_jobs = {}
    job_description = SLOT_JOB_DESC
    job_type = {"Id": 3, "Name": "DeviceAction_Task"}
    for k, slot in slot_data.items():
        job_params, target_param = [{"Key": "operationName", "Value": "UPDATE_SLOT_DATA"}], []
        num = slot.get('SlotNumber')
        type_id = str(slot.get('SlotType'))
        job_name = "Rename {0} {1}".format(slot_type.get(type_id, 'Slot'), num)
        target_param.append({"Id": int(slot.get('ChassisId')), "Data": "",
                             "TargetType": {"Id": 1000, "Name": "DEVICE"}})
        slot_config = "{0}|{1}|{2}".format(num, type_id, slot.get('new_name'))
        job_params.append({'Key': 'slotConfig', 'Value': slot_config})
        try:
            job_resp = rest_obj.job_submission(job_name, job_description, target_param,
                                               job_params, job_type)
            slot['JobId'] = job_resp.json_data.get('Id', 0)
            time.sleep(SETTLING_TIME)
        except HTTPError as err:
            slot['JobId'] = 0
            slot['JobStatus'] = str(err)
            failed_jobs[k] = slot
    [slot_data.pop(key) for key in failed_jobs.keys()]
    return failed_jobs


def get_job_states(module, rest_obj, slot_data):
    job_dict = dict([(slot['JobId'], k) for k, slot in slot_data.items() if slot['JobId']])
    query_params = {"$filter": "JobType/Id eq 3"}  # optimize this
    count = JOB_TIMEOUT // SETTLING_TIME
    job_incomplete = [2050, 2030, 2040, 2080]  # Running, Queued, Starting, New
    while count > 0 and job_dict:
        try:
            job_resp = rest_obj.invoke_request("GET", JOB_URI, query_param=query_params)
            jobs = job_resp.json_data.get('value')
        except HTTPError:
            count = count - 50  # 3 times retry for HTTP error
            time.sleep(SETTLING_TIME)
            continue
        job_over = []
        for job in jobs:
            id = job.get('Id')
            if id in job_dict:
                lrs = job.get('LastRunStatus')
                slot = slot_data[job_dict[id]]
                if lrs.get('Id') in job_incomplete:  # Running, not failed, not completed state
                    job_over.append(False)
                elif lrs.get('Id') == 2060:
                    job_over.append(True)
                    slot['SlotName'] = slot.pop('new_name')
                    job_dict.pop(id)
                else:
                    slot['JobStatus'] = lrs.get('Name')
                    job_over.append(True)  # Failed states - job not running
        if all(job_over) or not job_dict:
            break
        count = count - 1
        time.sleep(SETTLING_TIME)
    failed_jobs = dict([(k, slot_data.pop(k)) for k in job_dict.values()])
    return failed_jobs


def trigger_refresh_inventory(rest_obj, slot_data):
    chassis_dict = dict([(slot['ChassisId'], slot['ChassisServiceTag']) for slot in slot_data.values()])
    jobs = []
    for chassis in chassis_dict:
        job_type = {"Id": 8, "Name": "Inventory_Task"}
        job_name = "Refresh Inventory Chassis {0}".format(chassis_dict[chassis])
        job_description = REFRESH_JOB_DESC
        target_param = [{"Id": int(chassis), "Data": "''", "TargetType": {"Id": 1000, "Name": "DEVICE"}}]
        job_params = [{"Key": "operationName", "Value": "EC_SLOT_DEVICE_INVENTORY_REFRESH"}]
        job_resp = rest_obj.job_submission(job_name, job_description, target_param, job_params, job_type)
        job_id = job_resp.json_data.get('Id')
        jobs.append(int(job_id))
        time.sleep(SETTLING_TIME)
    return jobs


def trigger_all_inventory_task(rest_obj):
    job_type = {"Id": 8, "Name": "Inventory_Task"}
    job_name = "Refresh Inventory All Devices"
    job_description = REFRESH_JOB_DESC
    target_param = [{"Id": 500, "Data": "All-Devices", "TargetType": {"Id": 6000, "Name": "GROUP"}}]
    job_params = [{"Key": "defaultInventoryTask", "Value": "TRUE"}]
    job_resp = rest_obj.job_submission(job_name, job_description, target_param, job_params, job_type)
    job_id = job_resp.json_data.get('Id')
    return job_id


def get_formatted_slotlist(slot_dict):
    slot_list = list(slot_dict.values())
    req_tup = ('slot', 'job', 'chassis', 'device')
    for slot in slot_list:
        cp = slot.copy()
        klist = cp.keys()
        for k in klist:
            if not str(k).lower().startswith(req_tup):
                slot.pop(k)
    return slot_list


def exit_slot_config(module, rest_obj, failed_jobs, invalid_jobs, slot_data):
    failed_jobs.update(invalid_jobs)
    if failed_jobs:
        f = len(failed_jobs)
        s = len(slot_data)
        slot_info = get_formatted_slotlist(slot_data)
        failed_jobs_list = get_formatted_slotlist(failed_jobs)
        module.exit_json(msg=FAILED_MSG.format(f, s + f),
                         slot_info=slot_info, rename_failed_slots=failed_jobs_list, failed=True)
    if slot_data:
        job_failed_list = []
        try:
            rfrsh_job_list = trigger_refresh_inventory(rest_obj, slot_data)
            for job in rfrsh_job_list:
                job_failed, job_message = rest_obj.job_tracking(
                    job, job_wait_sec=JOB_TIMEOUT, sleep_time=JOB_INTERVAL)
                job_failed_list.append(job_failed)
            all_dv_rfrsh = trigger_all_inventory_task(rest_obj)
            job_failed, job_message = rest_obj.job_tracking(
                all_dv_rfrsh, job_wait_sec=JOB_TIMEOUT, sleep_time=JOB_INTERVAL)
            job_failed_list.append(job_failed)
        except Exception:  # Refresh is secondary task hence not failing module
            job_failed_list = [True]
        if any(job_failed_list) is True:
            slot_info = get_formatted_slotlist(slot_data)
            failed_jobs_list = get_formatted_slotlist(failed_jobs)
            module.exit_json(changed=True, msg=SUCCESS_REFRESH_MSG, slot_info=slot_info,
                             rename_failed_slots=failed_jobs_list)
    slot_info = get_formatted_slotlist(slot_data)
    module.exit_json(changed=True, msg=SUCCESS_MSG, slot_info=slot_info,
                     rename_failed_slots=list(failed_jobs.values()))


def get_device_type(rest_obj, type):
    filter = {"$filter": "Type eq {0}".format(str(type))}
    resp = rest_obj.invoke_request("GET", DEVICE_URI, query_param=filter)
    return resp.json_data


def get_slot_data(module, rest_obj, ch_slots, chass_id):
    uri = DEVICE_URI + "({0})/DeviceBladeSlots".format(chass_id)
    chsvc_tag = ch_slots.get('chassis_service_tag')
    resp = rest_obj.invoke_request("GET", uri)
    blade_slots = resp.json_data.get('value')
    if len(blade_slots) < 8:
        # Storage type 3000
        resp = get_device_type(rest_obj, 3000)
        storage = resp.get('value')
        for stx in storage:
            if stx.get('ChassisServiceTag') == chsvc_tag:
                blade_slots.append(stx.get('SlotConfiguration'))
    blade_dict = {}
    for slot in blade_slots:
        slot["ChassisId"] = chass_id
        slot["ChassisServiceTag"] = chsvc_tag
        if slot.get('Id'):
            slot["SlotId"] = str(slot.get('Id'))
        blade_dict[slot['SlotNumber']] = slot
        rest_obj.strip_substr_dict(slot)
    inp_slots = ch_slots.get('slots')
    existing_dict = dict([(slot['SlotNumber'], slot['SlotName']) for slot in blade_slots])
    input_dict = dict([(str(slot['slot_number']), slot['slot_name']) for slot in inp_slots])
    invalid_slot_number = set(input_dict.keys()) - set(existing_dict.keys())
    if invalid_slot_number:
        module.exit_json(msg=INVALID_SLOT_NUMBERS.format(';'.join(invalid_slot_number)), failed=True)
    if len(input_dict) < len(inp_slots):
        module.exit_json(msg=SLOT_NUM_DUP.format(chsvc_tag), failed=True)
    slot_dict_diff = {}
    slot_diff = recursive_diff(input_dict, existing_dict)
    if slot_diff and slot_diff[0]:
        diff = {}
        for k, v in (slot_diff[0]).items():
            blade_dict[k]['new_name'] = input_dict.get(k)
            diff["{0}_{1}".format(chsvc_tag, k)] = blade_dict[k]
        slot_dict_diff.update(diff)
    return slot_dict_diff


def slot_number_config(module, rest_obj):
    chslots = module.params.get("slot_options")
    resp = get_device_type(rest_obj, 2000)
    chassi_dict = dict([(chx['Identifier'], chx['Id']) for chx in resp.get('value')])
    slot_data = {}
    input_chassi_list = list(chx.get('chassis_service_tag') for chx in chslots)
    duplicate = [x for i, x in enumerate(input_chassi_list) if i != input_chassi_list.index(x)]
    if duplicate:
        module.exit_json(msg=CHASSIS_REPEATED.format((';'.join(set(duplicate)))), failed=True)
    for chx in chslots:
        chsvc_tag = chx.get('chassis_service_tag')
        if chsvc_tag not in chassi_dict.keys():
            module.exit_json(msg=CHASSIS_TAG_INVALID.format(chsvc_tag), failed=True)
        slot_dict = get_slot_data(module, rest_obj, chx, chassi_dict[chsvc_tag])
        slot_data.update(slot_dict)
    if not slot_data:
        module.exit_json(msg=NO_CHANGES_MSG)
    if module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    return slot_data


def main():
    specs = {
        "device_options": {"type": 'list', "elements": 'dict',
                           "options": {
                               "slot_name": {"required": True, 'type': 'str'},
                               "device_id": {"type": 'int'},
                               "device_service_tag": {"type": 'str'}
                           },
                           "mutually_exclusive": [('device_id', 'device_service_tag')],
                           "required_one_of": [('device_id', 'device_service_tag')]
                           },
        "slot_options": {"type": 'list', "elements": 'dict',
                         "options": {
                             "chassis_service_tag": {"required": True, 'type': 'str'},
                             "slots": {"required": True, "type": 'list', "elements": 'dict',
                                       "options": {
                                           "slot_number": {"required": True, 'type': 'int'},
                                           "slot_name": {"required": True, "type": 'str'}
                                       },
                                       },
                         },
                         },
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        required_one_of=[('slot_options', 'device_options')],
        mutually_exclusive=[('slot_options', 'device_options')],
        supports_check_mode=True
    )

    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            if module.params.get("slot_options"):
                slot_data = slot_number_config(module, rest_obj)
            else:
                slot_data = get_device_slot_config(module, rest_obj)
            invalid_jobs = start_slot_name_jobs(rest_obj, slot_data)
            failed_jobs = {}
            if slot_data:
                failed_jobs = get_job_states(module, rest_obj, slot_data)
            else:
                module.exit_json(msg=JOBS_TRIG_FAIL, rename_failed_slots=list(invalid_jobs.values()), failed=True)
            exit_slot_config(module, rest_obj, failed_jobs, invalid_jobs, slot_data)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, AttributeError, IndexError, KeyError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
