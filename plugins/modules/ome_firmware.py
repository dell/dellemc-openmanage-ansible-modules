#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.0.0
# Copyright (C) 2019-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_firmware
short_description: Firmware update of PowerEdge devices and its components through OpenManage Enterprise
version_added: "2.0.0"
description: "This module updates the firmware of PowerEdge devices and all its components through
OpenManage Enterprise."
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  device_service_tag:
    description:
      - List of targeted device service tags.
      - Either I(device_id) or I(device_service_tag) can be used individually or together.
      - I(device_service_tag) is mutually exclusive with I(device_group_names).
    type: list
    elements: str
  device_id:
    description:
      - List of targeted device ids.
      - Either I(device_id) or I(device_service_tag) can be used individually or together.
      - I(device_id) is mutually exclusive with I(device_group_names).
    type: list
    elements: int
  device_group_names:
    description:
      - Enter the name of the group to update the firmware of all the devices within the group.
      - I(device_group_names) is mutually exclusive with I(device_id) and I(device_service_tag).
    type: list
    elements: str
  baseline_name:
    description:
      - Enter the baseline name to update the firmware of all the devices or groups of
        devices against the available compliance report.
      - The firmware update can also be done by providing the baseline name and the path to
        the single DUP file. To update multiple baselines at once, provide the baseline
        names separated by commas.
      - I(baseline_names) is mutually exclusive with I(device_group_names), I(device_id)
        and I(device_service_tag).
    type: str
  dup_file:
    description: "Executable file to apply on the targets."
    type: str
requirements:
    - "python >= 2.7.5"
author:
    - "Felix Stephen (@felixs88)"
notes:
    - Run this module from a system that has direct access to DellEMC OpenManage Enterprise.
    - This module does not support C(check_mode).
'''

EXAMPLES = r'''
---
- name: Update firmware from DUP file using device ids
  dellemc.openmanage.ome_firmware:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    device_id:
      - 11111
      - 22222
    dup_file: "/path/Chassis-System-Management_Firmware_6N9WN_WN64_1.00.01_A00.EXE"

- name: Update firmware from a DUP file using a device service tags
  dellemc.openmanage.ome_firmware:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    device_service_tag:
      - KLBR111
      - KLBR222
    dup_file: "/path/Network_Firmware_NTRW0_WN64_14.07.07_A00-00_01.EXE"

- name: Update firmware from a DUP file using a device group names
  dellemc.openmanage.ome_firmware:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    device_group_names:
      - servers
    dup_file: "/path/BIOS_87V69_WN64_2.4.7.EXE"

- name: Update firmware using baseline name
  dellemc.openmanage.ome_firmware:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    baseline_name: baseline_devices

- name: Update firmware from a DUP file using a baseline names
  dellemc.openmanage.ome_firmware:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    baseline_name: "baseline_devices, baseline_groups"
    dup_file: "/path/BIOS_87V69_WN64_2.4.7.EXE"
'''

RETURN = r'''
---
msg:
  type: str
  description: "Overall firmware update status."
  returned: always
  sample: "Successfully submitted the firmware update job."
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
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError


def spawn_update_job(rest_obj, job_payload):
    """Spawns an update job and tracks it to completion."""
    job_uri, job_details = "JobService/Jobs", {}
    job_resp = rest_obj.invoke_request("POST", job_uri, data=job_payload)
    if job_resp.status_code == 201:
        job_details = job_resp.json_data
    return job_details


def job_payload_for_update(rest_obj, module, target_data, baseline=None):
    """Formulate the payload to initiate a firmware update job."""
    resp = rest_obj.get_job_type_id("Update_Task")
    if resp is None:
        module.fail_json(msg="Unable to fetch the job type Id.")
    payload = {
        "Id": 0, "JobName": "Firmware Update Task",
        "JobDescription": "Firmware Update Task", "Schedule": "startnow",
        "State": "Enabled", "JobType": {"Id": resp, "Name": "Update_Task"},
        "Targets": target_data,
        "Params": [{"Key": "operationName", "Value": "INSTALL_FIRMWARE"},
                   {"Key": "stagingValue", "Value": "false"},
                   {"Key": "signVerify", "Value": "true"}]
    }
    if baseline is not None:
        payload["Params"].append({"Key": "complianceReportId", "Value": "{0}".format(baseline["baseline_id"])})
        payload["Params"].append({"Key": "repositoryId", "Value": "{0}".format(baseline["repo_id"])})
        payload["Params"].append({"Key": "catalogId", "Value": "{0}".format(baseline["catalog_id"])})
        payload["Params"].append({"Key": "complianceUpdate", "Value": "true"})
    else:
        payload["Params"].append({"JobId": 0, "Key": "complianceUpdate", "Value": "false"})
    return payload


def get_applicable_components(rest_obj, dup_payload, module):
    """Get the target array to be used in spawning jobs for update."""
    target_data = []
    dup_url = "UpdateService/Actions/UpdateService.GetSingleDupReport"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    dup_resp = rest_obj.invoke_request("POST", dup_url, data=dup_payload,
                                       headers=headers, api_timeout=60)
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


def get_dup_applicability_payload(file_token, device_ids=None, group_ids=None, baseline_ids=None):
    """Returns the DUP applicability JSON payload."""
    dup_applicability_payload = {'SingleUpdateReportBaseline': [],
                                 'SingleUpdateReportGroup': [],
                                 'SingleUpdateReportTargets': [],
                                 'SingleUpdateReportFileToken': file_token}
    if device_ids is not None:
        dup_applicability_payload.update(
            {"SingleUpdateReportTargets": list(map(int, device_ids))}
        )
    elif group_ids is not None:
        dup_applicability_payload.update(
            {"SingleUpdateReportGroup": list(map(int, group_ids))}
        )
    elif baseline_ids is not None:
        dup_applicability_payload.update(
            {"SingleUpdateReportBaseline": list(map(int, baseline_ids))}
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
        response = rest_obj.invoke_request("POST", upload_uri, data=payload, headers=headers,
                                           api_timeout=100, dump=False)
        if response.status_code == 200:
            upload_success = True
            token = str(response.json_data)
        else:
            module.fail_json(msg="Unable to upload {0} to {1}".format(module.params['dup_file'],
                                                                      module.params['hostname']))
    return upload_success, token


def get_device_ids(rest_obj, module, device_id_tags):
    """Getting the list of device ids filtered from the device inventory."""
    device_id = []
    resp = rest_obj.get_all_report_details("DeviceService/Devices")
    if resp["report_list"]:
        device_resp = dict([(str(device['Id']), device['DeviceServiceTag']) for device in resp["report_list"]])
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


def get_dup_baseline(rest_obj, module):
    """Getting the list of baseline ids filtered from the baselines."""
    resp = rest_obj.get_all_report_details("UpdateService/Baselines")
    baseline = module.params.get('baseline_name').split(",")
    if resp["report_list"]:
        baseline_ids = [bse['Id'] for bse in resp["report_list"] for name in baseline if bse['Name'] == name]
        if len(set(baseline)) != len(set(baseline_ids)):
            module.fail_json(
                msg="Unable to complete the operation because the entered target baseline name(s)"
                    " '{0}' are invalid.".format(",".join(set(baseline))))
    else:
        module.fail_json(msg="Unable to complete the operation because the entered"
                             "target baseline name(s) does not exists.")
    return baseline_ids


def get_group_ids(rest_obj, module):
    """Getting the list of group ids filtered from the groups."""
    resp = rest_obj.get_all_report_details("GroupService/Groups")
    group_name = module.params.get('device_group_names')
    if resp["report_list"]:
        grp_ids = [grp['Id'] for grp in resp["report_list"] for grpname in group_name if grp['Name'] == grpname]
        if len(set(group_name)) != len(set(grp_ids)):
            module.fail_json(
                msg="Unable to complete the operation because the entered target device group name(s)"
                    " '{0}' are invalid.".format(",".join(set(group_name))))
    return grp_ids


def get_baseline_ids(rest_obj, module):
    """Getting the list of group ids filtered from the groups."""
    resp = rest_obj.get_all_report_details("UpdateService/Baselines")
    baseline, baseline_details = module.params.get('baseline_name'), {}
    if resp["report_list"]:
        for bse in resp["report_list"]:
            if bse['Name'] == baseline:
                baseline_details["baseline_id"] = bse["Id"]
                baseline_details["repo_id"] = bse["RepositoryId"]
                baseline_details["catalog_id"] = bse["CatalogId"]
        if not baseline_details:
            module.fail_json(
                msg="Unable to complete the operation because the entered target baseline name"
                    " '{0}' is invalid.".format(baseline))
    else:
        module.fail_json(msg="Unable to complete the operation because the entered"
                             "target baseline name does not exist.")
    return baseline_details


def single_dup_update(rest_obj, module):
    target_data, device_ids, group_ids, baseline_ids = None, None, None, None
    if module.params.get("device_group_names") is not None:
        group_ids = get_group_ids(rest_obj, module)
    elif module.params.get("baseline_name") is not None \
            and module.params.get("dup_file") is not None:
        baseline_ids = get_dup_baseline(rest_obj, module)
    else:
        device_id_tags = _validate_device_attributes(module)
        device_ids = get_device_ids(rest_obj, module, device_id_tags)
    upload_status, token = upload_dup_file(rest_obj, module)
    if upload_status:
        report_payload = get_dup_applicability_payload(token, device_ids=device_ids, group_ids=group_ids,
                                                       baseline_ids=baseline_ids)
        if report_payload:
            target_data = get_applicable_components(rest_obj, report_payload, module)
    return target_data


def baseline_based_update(rest_obj, module, baseline):
    compliance_uri = "UpdateService/Baselines({0})/DeviceComplianceReports".format(baseline["baseline_id"])
    resp = rest_obj.get_all_report_details(compliance_uri)
    compliance_report_list = []
    if resp["report_list"]:
        for each in resp["report_list"]:
            compliance_report = each.get("ComponentComplianceReports")
            if compliance_report is not None:
                data_dict = {}
                for component in compliance_report:
                    if component["UpdateAction"] in ["UPGRADE", "DOWNGRADE"]:
                        if data_dict.get("Id") == each["DeviceId"]:
                            data_dict["Data"] = "{0};{1}".format(data_dict["Data"], component["SourceName"])
                        else:
                            data_dict["Id"] = each["DeviceId"]
                            data_dict["Data"] = component["SourceName"]
                            data_dict["TargetType"] = {"Id": each["DeviceTypeId"], "Name": each["DeviceTypeName"]}
                if data_dict:
                    compliance_report_list.append(data_dict)
    if not compliance_report_list or not resp["report_list"]:
        module.fail_json(msg="No components available for update.")
    return compliance_report_list


def _validate_device_attributes(module):
    service_tag = module.params.get('device_service_tag')
    device_id = module.params.get('device_id')
    device_id_tags = []
    if device_id is not None:
        device_id_tags.extend(device_id)
    if service_tag is not None:
        device_id_tags.extend(service_tag)
    return device_id_tags


def validate_inputs(module):
    param = module.params
    if any([param.get("device_id") is not None,
            param.get("device_service_tag") is not None,
            param.get("device_group_names") is not None]) \
            and param.get("dup_file") is None:
        module.fail_json(msg="Parameter 'dup_file' to be provided along with "
                             "'device_id'|'device_service_tag'"
                             "|'device_group_names'")


def main():
    module = AnsibleModule(
        argument_spec={
            "hostname": {"required": True, "type": "str"},
            "username": {"required": True, "type": "str"},
            "password": {"required": True, "type": "str", "no_log": True},
            "port": {"required": False, "type": "int", "default": 443},
            "device_service_tag": {"required": False, "type": "list", "elements": 'str'},
            "device_id": {"required": False, "type": "list", "elements": 'int'},
            "dup_file": {"required": False, "type": "str"},
            "device_group_names": {"required": False, "type": "list", "elements": 'str'},
            "baseline_name": {"required": False, "type": "str"},
        },
        required_one_of=[["device_id", "device_service_tag", "device_group_names", "baseline_name"]],
        mutually_exclusive=[["device_group_names", "device_id"],
                            ["device_group_names", "device_service_tag"],
                            ["baseline_name", "device_id"],
                            ["baseline_name", "device_service_tag"],
                            ["baseline_name", "device_group_names"]],
        supports_check_mode=False
    )
    validate_inputs(module)
    update_status, baseline_details = {}, None
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            if module.params.get("baseline_name") is not None and module.params.get("dup_file") is None:
                baseline_details = get_baseline_ids(rest_obj, module)
                target_data = baseline_based_update(rest_obj, module, baseline_details)
            else:
                target_data = single_dup_update(rest_obj, module)
            job_payload = job_payload_for_update(rest_obj, module, target_data, baseline=baseline_details)
            update_status = spawn_update_job(rest_obj, job_payload)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, AttributeError) as err:
        module.fail_json(msg=str(err))
    module.exit_json(msg="Successfully submitted the firmware update job.", update_status=update_status, changed=True)


if __name__ == "__main__":
    main()
