#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.3.0
# Copyright (C) 2019-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_powerstate
short_description: Performs the power management operations on OpenManage Enterprise
version_added: "2.1.0"
description: This module performs the supported power management operations on OpenManage Enterprise.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  power_state:
    description: Desired end power state.
    type: str
    required: True
    choices: ['on', 'off', 'coldboot', 'warmboot', 'shutdown']
  device_service_tag:
    description:
      - Targeted device service tag.
      - I(device_service_tag) is mutually exclusive with I(device_id).
    type: str
  device_id:
    description:
      - Targeted device id.
      - I(device_id) is mutually exclusive with I(device_service_tag).
    type: int
requirements:
    - "python >= 2.7.5"
author: "Felix Stephen (@felixs88)"
notes:
    - Run this module from a system that has direct access to DellEMC OpenManage Enterprise.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Power state operation based on device id
  dellemc.openmanage.ome_powerstate:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    device_id: 11111
    power_state: "off"

- name: Power state operation based on device service tag
  dellemc.openmanage.ome_powerstate:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    device_service_tag: "KLBR111"
    power_state: "on"

- name: Power state operation based on list of device ids
  dellemc.openmanage.ome_powerstate:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    device_id: "{{ item.device_id }}"
    power_state: "{{ item.state }}"
  with_items:
    - { "device_id": 11111, "state": "on" }
    - { "device_id": 22222, "state": "off" }

- name: Power state operation based on list of device service tags
  dellemc.openmanage.ome_powerstate:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    device_service_tag: "{{ item.service_tag }}"
    power_state: "{{ item.state }}"
  with_items:
    - { "service_tag": "KLBR111", "state": "on" }
    - { "service_tag": "KLBR222", "state": "off" }
'''

RETURN = r'''
---
msg:
  type: str
  description: "Overall power state operation job status."
  returned: always
  sample: "Power State operation job submitted successfully."
job_status:
  type: dict
  description: "Power state operation job and progress details from the OME."
  returned: success
  sample: {
    "Builtin": false,
    "CreatedBy": "user",
    "Editable": true,
    "EndTime": null,
    "Id": 11111,
    "JobDescription": "DeviceAction_Task",
    "JobName": "DeviceAction_Task_PowerState",
    "JobStatus": {
      "Id": 1111,
      "Name": "New"
      },
    "JobType": {
      "Id": 1,
      "Internal": false,
      "Name": "DeviceAction_Task"
      },
    "LastRun": "2019-04-01 06:39:02.69",
    "LastRunStatus": {
      "Id": 1112,
      "Name": "Running"
      },
    "NextRun": null,
    "Params": [
      {
        "JobId": 11111,
        "Key": "powerState",
        "Value": "2"
      },
      {
        "JobId": 11111,
        "Key": "operationName",
        "Value": "POWER_CONTROL"
      }
    ],
    "Schedule": "",
    "StartTime": null,
    "State": "Enabled",
    "Targets": [
      {
        "Data": "",
        "Id": 11112,
        "JobId": 11111,
        "TargetType": {
          "Id": 1000,
          "Name": "DEVICE"
        }
      }
    ],
    "UpdatedBy": null,
    "Visible": true
  }
'''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError

VALID_OPERATION = {"on": 2, "off": 12, "coldboot": 5, "warmboot": 10, "shutdown": 8}
POWER_STATE_MAP = {"on": 17, "off": 18, "poweringon": 20, "poweringoff": 21}
NOT_APPLICABLE_OPTIONS = ["coldboot", "warmboot", "shutdown"]


def spawn_update_job(rest_obj, payload):
    """Spawns an update job and tracks it to completion."""
    job_uri, job_details = "JobService/Jobs", {}
    job_resp = rest_obj.invoke_request("POST", job_uri, data=payload)
    if job_resp.status_code == 201:
        job_details = job_resp.json_data
    return job_details


def build_power_state_payload(device_id, device_type, valid_option):
    """Build the payload for requested device."""
    payload = {
        "Id": 0,
        "JobName": "DeviceAction_Task_PowerState",
        "JobDescription": "DeviceAction_Task",
        "Schedule": "startnow",
        "State": "Enabled",
        "JobType": {"Id": 3, "Name": "DeviceAction_Task"},
        "Params": [{"Key": "operationName", "Value": "POWER_CONTROL"},
                   {"Key": "powerState", "Value": str(valid_option)}],
        "Targets": [{"Id": int(device_id), "Data": "",
                     "TargetType": {"Id": device_type, "Name": "DEVICE"}}],
    }
    return payload


def get_device_state(module, resp, device_id):
    """Get the current state and device type from response."""
    current_state, device_type, invalid_device = None, None, True
    for device in resp['report_list']:
        if device['Id'] == int(device_id):
            current_state = device.get('PowerState', None)
            device_type = device['Type']
            invalid_device = False
            break
    if invalid_device:
        module.fail_json(msg="Unable to complete the operation because the entered target"
                             " device id '{0}' is invalid.".format(device_id))
    if device_type not in (1000, 2000):
        module.fail_json(msg="Unable to complete the operation because power"
                             " state supports device type 1000 and 2000.")
    return current_state, device_type


def get_device_resource(module, rest_obj):
    """Getting the device id filtered from the device inventory."""
    power_state = module.params['power_state']
    device_id = module.params['device_id']
    service_tag = module.params['device_service_tag']
    resp_data = rest_obj.get_all_report_details("DeviceService/Devices")
    if resp_data['report_list'] and service_tag is not None:
        device_resp = dict([(device.get('DeviceServiceTag'), str(device.get('Id'))) for device in resp_data['report_list']])
        if service_tag in device_resp:
            device_id = device_resp[service_tag]
        else:
            module.fail_json(msg="Unable to complete the operation because the entered target"
                                 " device service tag '{0}' is invalid.".format(service_tag))
    current_state, device_type = get_device_state(module, resp_data, device_id)

    # For check mode changes.
    valid_option, valid_operation = VALID_OPERATION[power_state], False
    if power_state in NOT_APPLICABLE_OPTIONS and current_state != POWER_STATE_MAP["on"]:
        valid_operation = True
    elif (valid_option == current_state) or \
            (power_state == "on" and current_state in (POWER_STATE_MAP["on"], POWER_STATE_MAP['poweringon'])) or \
            (power_state in ("off", "shutdown") and
             current_state in (POWER_STATE_MAP["off"], POWER_STATE_MAP['poweringoff'])):
        valid_operation = True

    if module.check_mode and valid_operation:
        module.exit_json(msg="No changes found to commit.")
    elif module.check_mode and not valid_operation:
        module.exit_json(msg="Changes found to commit.", changed=True)
    payload = build_power_state_payload(device_id, device_type, valid_option)
    return payload


def main():
    module = AnsibleModule(
        argument_spec={
            "hostname": {"required": True, "type": "str"},
            "username": {"required": True, "type": "str"},
            "password": {"required": True, "type": "str", "no_log": True},
            "port": {"required": False, "type": "int", "default": 443},
            "power_state": {"required": True, "type": "str",
                            "choices": ["on", "off", "coldboot", "warmboot", "shutdown"]},
            "device_service_tag": {"required": False, "type": "str"},
            "device_id": {"required": False, "type": "int"},
        },
        required_one_of=[["device_service_tag", "device_id"]],
        mutually_exclusive=[["device_service_tag", "device_id"]],
        supports_check_mode=True
    )
    try:
        if module.params['device_id'] is None and module.params['device_service_tag'] is None:
            module.fail_json(msg="device_id and device_service_tag attributes should not be None.")
        job_status = {}
        with RestOME(module.params, req_session=True) as rest_obj:
            payload = get_device_resource(module, rest_obj)
            job_status = spawn_update_job(rest_obj, payload)
    except HTTPError as err:
        module.fail_json(msg=str(err), job_status=json.load(err))
    except (URLError, SSLValidationError, ConnectionError, TypeError, ValueError) as err:
        module.fail_json(msg=str(err))
    module.exit_json(msg="Power State operation job submitted successfully.",
                     job_status=job_status, changed=True)


if __name__ == '__main__':
    main()
