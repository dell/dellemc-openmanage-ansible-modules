#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 1.3
# Copyright (C) 2019 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['deprecated'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: dellemc_ome_firmware
short_description: "Firmware update of PowerEdge devices and its components."
version_added: "2.8"
deprecated:
  removed_in: "3.2"
  why: Replaced with M(ome_firmware).
  alternative: Use M(ome_firmware) instead.
description: "This module updates the firmware of PowerEdge devices and all its components."
options:
  hostname:
    description: "Target IP Address or hostname."
    required: true
    type: str
  username:
    description: "Target username."
    required: true
    type: str
  password:
    description: "Target user password."
    required: true
    type: str
  port:
    description: "Target HTTPS port."
    default: 443
    type: int
  device_service_tag:
    description:
      - List of targeted device service tags.
      - Either I(device_id) or I(device_service_tag) is mandatory or both can be applicable.
    type: list
  device_id:
    description:
      - List of targeted device ids.
      - Either I(device_id) or I(device_service_tag) is mandatory or both can be applicable.
    type: list
  dup_file:
    description: "Executable file to apply on the targets."
    required: true
    type: str
requirements:
    - "python >= 2.7.5"
author:
    - "Felix Stephen (@felixs88)"
'''

EXAMPLES = r'''
---
- name: "Update firmware from DUP file using device ids."
  dellemc_ome_firmware:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    device_id:
      - 11111
      - 22222
    dup_file: "/path/Chassis-System-Management_Firmware_6N9WN_WN64_1.00.01_A00.EXE"

- name: "Update firmware from DUP file using device service tags."
  dellemc_ome_firmware:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    device_service_tag:
      - KLBR111
      - KLBR222
    dup_file: "/path/Network_Firmware_NTRW0_WN64_14.07.07_A00-00_01.EXE"
'''

RETURN = r'''
---
msg:
  type: str
  description: "Overall firmware update status."
  returned: always
  sample: "Successfully updated the firmware."
update_status:
  type: dict
  description: "Firmware Update job and progress details from the OME."
  returned: success
  sample: {
    'LastRun': None,
    'CreatedBy': 'user',
    'Schedule': 'startnow',
    'LastRunStatus': {
      'Id': 1111,
      'Name': 'NotRun'
    },
    'Builtin': False,
    'Editable': True,
    'NextRun': None,
    'JobStatus': {
      'Id': 1111,
      'Name': 'New'
    },
    'JobName': 'Firmware Update Task',
    'Visible': True,
    'State': 'Enabled',
    'JobDescription': 'dup test',
    'Params': [{
      'Value': 'true',
      'Key': 'signVerify',
      'JobId': 11111}, {
      'Value': 'false',
      'Key': 'stagingValue',
      'JobId': 11112}, {
      'Value': 'false',
      'Key': 'complianceUpdate',
      'JobId': 11113}, {
      'Value': 'INSTALL_FIRMWARE',
      'Key': 'operationName',
      'JobId': 11114}],
    'Targets': [{
      'TargetType': {
      'Id': 1000,
      'Name': 'DEVICE'},
      'Data': 'DCIM:INSTALLED#701__NIC.Mezzanine.1A-1-1=1111111111111',
      'Id': 11115,
      'JobId': 11116}],
    'StartTime': None,
    'UpdatedBy': None,
    'EndTime': None,
    'Id': 11117,
    'JobType': {
      'Internal': False,
      'Id': 5,
      'Name': 'Update_Task'}
}
'''


import json
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.remote_management.dellemc.ome import RestOME
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError


def spawn_update_job(rest_obj, job_payload):
    """Spawns an update job and tracks it to completion."""
    job_uri, job_details = "JobService/Jobs", {}
    job_resp = rest_obj.invoke_request("POST", job_uri, data=job_payload)
    if job_resp.status_code == 201:
        job_details = job_resp.json_data
    return job_details


def job_payload_for_update(target_data):
    """Formulate the payload to initiate a firmware update job."""
    payload = {
        "Id": 0, "JobName": "Firmware Update Task",
        "JobDescription": "Firmware Update Task", "Schedule": "startnow",
        "State": "Enabled", "CreatedBy": "admin",
        "JobType": {"Id": 5, "Name": "Update_Task"},
        "Targets": target_data,
        "Params": [{"JobId": 0, "Key": "operationName", "Value": "INSTALL_FIRMWARE"},
                   {"JobId": 0, "Key": "complianceUpdate", "Value": "false"},
                   {"JobId": 0, "Key": "stagingValue", "Value": "false"},
                   {"JobId": 0, "Key": "signVerify", "Value": "true"}]
    }
    return payload


def get_applicable_components(rest_obj, dup_payload, module):
    """Get the target array to be used in spawning jobs for update."""
    target_data = []
    dup_url = "UpdateService/Actions/UpdateService.GetSingleDupReport"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    try:
        dup_resp = rest_obj.invoke_request("POST", dup_url, data=dup_payload,
                                           headers=headers, api_timeout=60)
    except HTTPError as err:
        module.fail_json(msg=str(err), update_status=json.load(err))
    if dup_resp.status_code == 200:
        dup_data = dup_resp.json_data
        file_token = str(dup_payload['SingleUpdateReportFileToken'])
        for device in dup_data:
            for component in device['DeviceReport']['Components']:
                temp_map = {}
                temp_map['Id'] = device['DeviceId']
                temp_map['Data'] = "{0}={1}".format(component['ComponentSourceName'], file_token)
                temp_map['TargetType'] = {}
                temp_map['TargetType']['Id'] = int(device['DeviceReport']['DeviceTypeId'])
                temp_map['TargetType']['Name'] = str(device['DeviceReport']['DeviceTypeName'])
                target_data.append(temp_map)
    else:
        module.fail_json(msg="Unable to get components DUP applies.")
    return target_data


def get_dup_applicability_payload(file_token, device_ids):
    """Returns the DUP applicability JSON payload."""
    dup_applicability_payload = {'SingleUpdateReportBaseline': [],
                                 'SingleUpdateReportGroup': [],
                                 'SingleUpdateReportTargets': [],
                                 'SingleUpdateReportFileToken': file_token}
    if device_ids:
        dup_applicability_payload.update(
            {"SingleUpdateReportTargets": list(map(int, device_ids))}
        )
    return dup_applicability_payload


def upload_dup_file(rest_obj, module):
    """Upload DUP file to OME and get a file token."""
    upload_uri = "UpdateService/Actions/UpdateService.UploadFile"
    headers = {"Content-Type": "application/octet-stream",
               "Accept": "application/octet-stream"}
    upload_success, token = False, None
    dup_file = module.params['dup_file']
    if not isinstance(dup_file, str):
        module.fail_json(
            msg="argument {0} is type of {1} and we were unable to convert to string: {1} cannot be "
                "converted to a string".format("dup_file", type(dup_file)))
    with open(module.params['dup_file'], 'rb') as payload:
        payload = payload.read()
        response = rest_obj.invoke_request("POST", upload_uri, data=payload,
                                           headers=headers, api_timeout=100, dump=False)
        if response.status_code == 200:
            upload_success = True
            token = str(response.json_data)
        else:
            module.fail_json(msg="Unable to upload {0} to {1}".format(module.params['dup_file'],
                                                                      module.params['hostname']))
    return upload_success, token


def get_device_ids(rest_obj, module, device_id_tags):
    """Getting the list of device ids filtered from the device inventory."""
    device_uri, device_id = "DeviceService/Devices", []
    resp = rest_obj.invoke_request('GET', device_uri)
    if resp.success and resp.json_data['value']:
        device_resp = {str(device['Id']): device['DeviceServiceTag'] for device in resp.json_data['value']}
        device_tags = map(str, device_id_tags)
        invalid_tags = []
        for tag in device_tags:
            if tag in device_resp.keys() or tag.isdigit():
                device_id.append(tag)
            elif tag in device_resp.values():
                ids = list(device_resp.keys())[list(device_resp.values()).index(tag)]
                device_id.append(ids)
            else:
                invalid_tags.append(tag)
        if invalid_tags:
            module.fail_json(
                msg="Unable to complete the operation because the entered target device service"
                    " tag(s) or device id(s) '{0}' are invalid.".format(",".join(set(invalid_tags))))
    else:
        module.fail_json(msg="Failed to fetch the device facts.")
    return device_id


def _validate_device_attributes(module):
    service_tag = module.params['device_service_tag']
    device_id = module.params['device_id']
    device_id_tags = []
    if not isinstance(service_tag, list) and not isinstance(device_id, list):
        module.fail_json(msg="Either device_id or device_service_tag should be specified.")
    else:
        if device_id is not None:
            device_id_tags.extend(device_id)
        if service_tag is not None:
            device_id_tags.extend(service_tag)
    return device_id_tags


def main():
    module = AnsibleModule(
        argument_spec={
            "hostname": {"required": True, "type": "str"},
            "username": {"required": True, "type": "str"},
            "password": {"required": True, "type": "str", "no_log": True},
            "port": {"required": False, "type": "int", "default": 443},
            "device_service_tag": {"required": False, "type": "list"},
            "device_id": {"required": False, "type": "list"},
            "dup_file": {"required": True, "type": "str"},
        },
    )
    module.deprecate("The 'dellemc_ome_firmware' module has been deprecated. "
                     "Use 'ome_firmware' instead",
                     version=3.2)
    update_status = {}
    try:
        device_id_tags = _validate_device_attributes(module)
        with RestOME(module.params, req_session=True) as rest_obj:
            device_ids = get_device_ids(rest_obj, module, device_id_tags)
            upload_status, token = upload_dup_file(rest_obj, module)
            if upload_status:
                report_payload = get_dup_applicability_payload(token, device_ids)
                if report_payload:
                    target_data = get_applicable_components(rest_obj, report_payload, module)
                    if target_data:
                        job_payload = job_payload_for_update(target_data)
                        update_status = spawn_update_job(rest_obj, job_payload)
                    else:
                        module.fail_json(msg="No components available for update.")
    except (IOError, ValueError, SSLError, TypeError, URLError, ConnectionError) as err:
        module.fail_json(msg=str(err))
    except HTTPError as err:
        module.fail_json(msg=str(err), update_status=json.load(err))
    module.exit_json(msg="Successfully updated the firmware.", update_status=update_status, changed=True)


if __name__ == "__main__":
    main()
