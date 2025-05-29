#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2022-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
---
module: ome_devices
short_description: Perform device-specific operations on target devices
description: Perform device-specific operations such as refresh inventory, clear iDRAC job queue, and reset iDRAC from OpenManage Enterprise.
version_added: 6.1.0
extends_documentation_fragment:
  - dellemc.openmanage.oment_auth_options
options:
  device_service_tags:
    description:
      - Service tag of the target devices.
      - This is mutually exclusive with I(device_ids).
    type: list
    elements: str
  device_ids:
    description:
      - IDs of the target devices.
      - This is mutually exclusive with I(device_service_tags).
    type: list
    elements: int
  state:
    description:
      - C(present) Allows to perform the I(device_action) on the target devices.
      - "C(absent) Removes the device from OpenManage Enterprise. Job is not triggered. I(job_wait), I(job_schedule),
      I(job_name), and I(job_description) are not applicable to this operation."
    type: str
    choices: [present, absent]
    default: present
  device_action:
    description:
      - C(refresh_inventory) refreshes the inventory on the target devices.
      - C(reset_idrac) Triggers a reset on the target iDRACs.
      - C(clear_idrac_job_queue) Clears the job queue on the target iDRACs.
      - A job is triggered for each action.
    type: str
    choices: [refresh_inventory, reset_idrac, clear_idrac_job_queue]
    default: refresh_inventory
  job_wait:
    description:
      - Provides an option to wait for the job completion.
      - This option is applicable when I(state) is C(present).
      - This is applicable when I(job_schedule) is C(startnow).
    type: bool
    default: true
  job_wait_timeout:
    description:
      - The maximum wait time of I(job_wait) in seconds. The job is tracked only for this duration.
      - This option is applicable when I(job_wait) is C(true).
    type: int
    default: 1200
  job_schedule:
    description: Provide the cron string to schedule the job.
    type: str
    default: startnow
  job_name:
    description: Optional name for the job.
    type: str
  job_description:
    description: Optional description for the job.
    type: str
requirements:
  - "python >= 3.9.6"
author:
  - Jagadeesh N V(@jagadeeshnv)
  - ShivamSh3(@ShivamSh3)
notes:
  - For C(idrac_reset), the job triggers only the iDRAC reset operation and does not track the complete reset cycle.
  - Run this module from a system that has direct access to Dell OpenManage Enterprise.
  - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Refresh Inventory
  dellemc.openmanage.ome_devices:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_action: refresh_inventory
    device_service_tags:
      - SVCTAG1

- name: Clear iDRAC job queue
  dellemc.openmanage.ome_devices:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_action: clear_idrac_job_queue
    device_service_tags:
      - SVCTAG1

- name: Reset iDRAC using the service tag
  dellemc.openmanage.ome_devices:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_action: reset_idrac
    device_service_tags:
      - SVCTAG1

- name: Remove devices using servicetags
  dellemc.openmanage.ome_devices:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: absent
    device_service_tags:
      - SVCTAG1
      - SVCTAF2

- name: Remove devices using IDs
  dellemc.openmanage.ome_devices:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: absent
    device_ids:
      - 10235
"""

RETURN = """
---
msg:
  type: str
  description: Overall status of the devices operation.
  returned: always
  sample: "Successfully removed the device(s)."
job:
  type: dict
  description: Job details of the devices operation.
  returned: success
  sample: {
    "Id": 14874,
    "JobName": "Refresh inventory",
    "JobDescription": "The Refresh inventory task initiated from OpenManage Ansible Modules for devices with the ids '13216'.",
    "Schedule": "startnow",
    "State": "Enabled",
    "CreatedBy": "admin",
    "UpdatedBy": null,
    "Visible": true,
    "Editable": true,
    "Builtin": false,
    "UserGenerated": true,
    "Targets": [
        {
            "JobId": 14874,
            "Id": 13216,
            "Data": "",
            "TargetType": {
                "Id": 1000,
                "Name": "DEVICE"
            }
        }
    ],
    "Params": [
        {
            "JobId": 14874,
            "Key": "action",
            "Value": "CONFIG_INVENTORY"
        },
        {
            "JobId": 14874,
            "Key": "isCollectDriverInventory",
            "Value": "true"
        }
    ],
    "LastRunStatus": {
        "@odata.type": "#JobService.JobStatus",
        "Id": 2060,
        "Name": "Completed"
    },
    "JobType": {
        "@odata.type": "#JobService.JobType",
        "Id": 8,
        "Name": "Inventory_Task",
        "Internal": false
    },
    "JobStatus": {
        "@odata.type": "#JobService.JobStatus",
        "Id": 2020,
        "Name": "Scheduled"
    },
    "ExecutionHistories@odata.navigationLink": "/api/JobService/Jobs(14874)/ExecutionHistories",
    "LastExecutionDetail": {
        "@odata.id": "/api/JobService/Jobs(14874)/LastExecutionDetail"
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
                "MessageId": "CGEN1002",
                "RelatedProperties": [],
                "Message": "Unable to complete the operation because the requested URI is invalid.",
                "MessageArgs": [],
                "Severity": "Critical",
                "Resolution": "Enter a valid URI and retry the operation."
            }
        ]
    }
}
"""

import json
from ssl import SSLError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import strip_substr_dict, job_tracking
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import CHANGES_MSG, NO_CHANGES_MSG

DEVICE_URI = "DeviceService/Devices"
JOBS_URI = "JobService/Jobs"
JOB_URI = "JobService/Jobs({job_id})"
RUN_JOB_URI = "JobService/Actions/JobService.RunJobs"
LAST_EXEC = "JobService/Jobs({job_id})/LastExecutionDetail"
DELETE_DEVICES_URI = "DeviceService/Actions/DeviceService.RemoveDevices"
DELETE_SUCCESS = "The devices(s) are removed successfully."
INVALID_DEV_ST = "Unable to complete the operation because the entered target device(s) '{0}' are invalid."
JOB_DESC = "The {0} task initiated from OpenManage Ansible Modules for devices with the ids '{1}'."
APPLY_TRIGGERED = "Successfully initiated the device action job."
JOB_SCHEDULED = "The job is scheduled successfully."
SUCCESS_MSG = "The device operation is performed successfully."
TIMEOUT_NEGATIVE_MSG = "The parameter `job_wait_timeout` value cannot be negative or zero."

all_device_types = [1000, 2000, 4000, 5000, 7000, 8000, 9001]
device_type_map = {"refresh_inventory": all_device_types, "reset_idrac": [1000], "clear_idrac_job_queue": [1000]}
job_type_map = {"refresh_inventory": 8, "reset_idrac": 3, "clear_idrac_job_queue": 3}
jtype_map = {3: "DeviceAction_Task", 8: "Inventory_Task"}
job_params_map = {"refresh_inventory": {"action": "CONFIG_INVENTORY",
                                        "isCollectDriverInventory": "true"},
                  "reset_idrac": {"operationName": "RESET_IDRAC"},
                  "clear_idrac_job_queue": {"operationName": "REMOTE_RACADM_EXEC",
                                            "Command": "jobqueue delete -i JID_CLEARALL_FORCE",
                                            "CommandTimeout": "60", "deviceTypes": "1000"}}
jobname_map = {"refresh_inventory": "Refresh inventory", "reset_idrac": "Reset iDRAC",
               "clear_idrac_job_queue": "Clear iDRAC job queue"}


def get_dev_ids(module, rest_obj, types):
    invalids = set()
    sts = module.params.get('device_ids')
    param = "{0} eq {1}"
    srch = 'Id'
    if not sts:
        sts = module.params.get('device_service_tags')
        param = "{0} eq '{1}'"
        srch = 'Identifier'
    devs = []
    for st in sts:
        resp = rest_obj.invoke_request("GET", DEVICE_URI, query_param={"$filter": param.format(srch, st)})
        val = resp.json_data.get('value')
        if not val:
            invalids.add(st)
        for v in val:
            if v[srch] == st:
                if v["Type"] in types:
                    devs.extend(val)
                else:
                    invalids.add(st)
                break
        else:
            invalids.add(st)
    valids = [(dv.get('Id')) for dv in devs]
    return valids, invalids


def delete_devices(module, rest_obj, valid_ids):
    if module.check_mode:
        module.exit_json(msg=CHANGES_MSG, changed=True)
    payload = {"DeviceIds": list(valid_ids)}
    rest_obj.invoke_request('POST', DELETE_DEVICES_URI, data=payload)
    module.exit_json(msg=DELETE_SUCCESS, changed=True)


def update_common_job(module, payload, task, valid_ids):
    payload["Schedule"] = module.params.get('job_schedule')
    if module.params.get('job_name'):
        payload["JobName"] = module.params.get('job_name')
    else:
        payload["JobName"] = jobname_map.get(task)
    if module.params.get('job_description'):
        payload["JobDescription"] = module.params.get('job_description')
    else:
        payload["JobDescription"] = JOB_DESC.format(jobname_map.get(task), ",".join(map(str, valid_ids)))


def check_similar_job(rest_obj, payload):
    query_param = {"$filter": "JobType/Id eq {0}".format(payload['JobType'])}
    job_resp = rest_obj.invoke_request("GET", JOBS_URI, query_param=query_param)
    job_list = job_resp.json_data.get('value', [])
    for jb in job_list:
        if jb['JobName'] == payload['JobName'] and jb['JobDescription'] == payload['JobDescription'] and \
                jb['Schedule'] == payload['Schedule']:
            jb_prm = dict((k.get('Key'), k.get('Value')) for k in jb.get('Params'))
            if not jb_prm == payload.get('Params'):
                continue
            trgts = dict((t.get('Id'), t.get('TargetType').get('Name')) for t in jb.get('Targets'))
            if not trgts == payload.get('Targets'):
                continue
            return jb
    return {}


def job_wait(module, rest_obj, job):
    mparams = module.params
    if mparams.get('job_schedule') != 'startnow':
        module.exit_json(changed=True, msg=JOB_SCHEDULED, job=strip_substr_dict(job))
    if not module.params.get("job_wait"):
        module.exit_json(changed=True, msg=APPLY_TRIGGERED, job=strip_substr_dict(job))
    else:
        job_msg = SUCCESS_MSG
        job_failed, msg, job_dict, wait_time = job_tracking(
            rest_obj, JOB_URI.format(job_id=job['Id']), max_job_wait_sec=module.params.get('job_wait_timeout'),
            initial_wait=3)
        if job_failed:
            try:
                job_resp = rest_obj.invoke_request('GET', LAST_EXEC.format(job_id=job['Id']))
                msg = job_resp.json_data.get("Value")
                job_msg = msg.replace('\n', ' ')
            except Exception:
                job_msg = msg
        module.exit_json(failed=job_failed, msg=job_msg, job=strip_substr_dict(job), changed=True)


def get_task_payload(task):
    taskload = {}
    taskload.update({"JobType": job_type_map.get(task, 8)})
    taskload.update({"Params": job_params_map.get(task, {})})
    return taskload


def get_payload_method(task, valid_ids):
    payload = get_task_payload(task)
    targets = dict((dv, "DEVICE") for dv in valid_ids)
    payload["Targets"] = targets
    return payload, "POST", JOBS_URI


def formalize_job_payload(payload):
    payload["Id"] = 0
    payload["State"] = "Enabled"
    prms = payload['Params']
    payload['Params'] = [({"Key": k, "Value": v}) for k, v in prms.items()]
    trgts = payload['Targets']
    payload['Targets'] = [({"Id": k, "Data": "", "TargetType": {"Id": 1000, "Name": v}}) for k, v in trgts.items()]
    jtype = payload["JobType"]
    payload["JobType"] = {"Id": jtype, "Name": jtype_map.get(jtype)}


def perform_device_tasks(module, rest_obj, valid_ids):
    task = module.params.get("device_action")
    payload, method, uri = get_payload_method(task, valid_ids)
    update_common_job(module, payload, task, valid_ids)
    job = check_similar_job(rest_obj, payload)
    if not job:
        formalize_job_payload(payload)
        if module.check_mode:
            module.exit_json(msg=CHANGES_MSG, changed=True)
        resp = rest_obj.invoke_request("POST", JOBS_URI, data=payload, api_timeout=60)
        job_wait(module, rest_obj, resp.json_data)
    else:
        if module.params.get('job_schedule') == 'startnow' and job["LastRunStatus"]['Id'] != 2050:
            if module.check_mode:
                module.exit_json(msg=CHANGES_MSG, changed=True)
            resp = rest_obj.invoke_request("POST", RUN_JOB_URI, data={"JobIds": [job['Id']]})
            job_wait(module, rest_obj, job)
        module.exit_json(msg=NO_CHANGES_MSG, job=strip_substr_dict(job))


def main():
    specs = {
        "device_service_tags": {"type": "list", "elements": 'str'},
        "device_ids": {"type": "list", "elements": 'int'},
        "state": {"type": "str", "choices": ["present", "absent"], "default": "present"},
        "device_action": {"type": "str", "choices": ["refresh_inventory", "reset_idrac", "clear_idrac_job_queue"],
                          "default": 'refresh_inventory'},
        "job_wait": {"type": "bool", "default": True},
        "job_wait_timeout": {"type": "int", "default": 1200},
        "job_schedule": {"type": "str", "default": 'startnow'},
        "job_name": {"type": "str"},
        "job_description": {"type": "str"},
        # "job_params": {"type": "dict"}
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        required_if=[],
        mutually_exclusive=[
            ("device_service_tags", "device_ids"),
        ],
        required_one_of=[("device_service_tags", "device_ids")],
        supports_check_mode=True
    )
    try:
        if module.params.get("job_wait") and module.params.get("job_wait_timeout") <= 0:
            module.exit_json(msg=TIMEOUT_NEGATIVE_MSG, failed=True)
        with RestOME(module.params, req_session=True) as rest_obj:
            if module.params.get("state") == 'present':
                valids, invalids = get_dev_ids(module, rest_obj,
                                               device_type_map.get(module.params.get("device_action")))
                if invalids:
                    module.exit_json(failed=True, msg=INVALID_DEV_ST.format(",".join(map(str, invalids))))
                perform_device_tasks(module, rest_obj, valids)
            else:
                valids, invalids = get_dev_ids(module, rest_obj, all_device_types)
                if not valids:
                    module.exit_json(msg=NO_CHANGES_MSG)
                delete_devices(module, rest_obj, valids)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, AttributeError, IndexError, KeyError,
            OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
