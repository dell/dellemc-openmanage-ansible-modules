#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2019-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_firmware
short_description: Update firmware on PowerEdge devices and its components through OpenManage Enterprise
version_added: "2.0.0"
description: This module updates the firmware of PowerEdge devices and all its components through OpenManage Enterprise.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  device_service_tag:
    description:
      - List of service tags of the targeted devices.
      - Either I(device_id) or I(device_service_tag) can be used individually or together.
      - This option is mutually exclusive with I(device_group_names) and I(devices).
    type: list
    elements: str
  device_id:
    description:
      - List of ids of the targeted device.
      - Either I(device_id) or I(device_service_tag) can be used individually or together.
      - This option is mutually exclusive with I(device_group_names) and I(devices).
    type: list
    elements: int
  device_group_names:
    description:
      - Enter the name of the device group that contains the devices on which firmware needs to be updated.
      - This option is mutually exclusive with I(device_id) and I(device_service_tag).
    type: list
    elements: str
  dup_file:
    description:
      - "The path of the Dell Update Package (DUP) file that contains the firmware or drivers required to update the
      target system device or individual device components."
      - This is mutually exclusive with I(baseline_name), I(components), and I(devices).
    type: path
  baseline_name:
    description:
      - Enter the baseline name to update the firmware of all devices or list of devices that are not complaint.
      - This option is mutually exclusive with I(dup_file) and I(device_group_names).
    type: str
  components:
    description:
      - List of components to be updated.
      - If not provided, all components applicable are considered.
      - This option is case sensitive.
      - This is applicable to I(device_service_tag), I(device_id), and I(baseline_name).
    type: list
    default: []
    elements: str
  devices:
    description:
      - This option allows to select components on each device for firmware update.
      - This option is mutually exclusive with I(dup_file), I(device_group_names), I(device_id), and I(device_service_tag).
    type: list
    elements: dict
    suboptions:
      id:
        type: int
        description:
          - The id of the target device to be updated.
          - This option is mutually exclusive with I(service_tag).
      service_tag:
        type: str
        description:
          - The service tag of the target device to be updated.
          - This option is mutually exclusive with I(id).
      components:
        description: The target components to be updated. If not specified, all applicable device components are considered.
        type: list
        default: []
        elements: str
  schedule:
    type: str
    description:
      - Select the schedule for the firmware update.
      - if C(StageForNextReboot) is chosen, the firmware will be staged and updated during the next reboot
        of the target device.
      - if C(RebootNow) will apply the firmware updates immediately.
    choices:
      - RebootNow
      - StageForNextReboot
    default: RebootNow
  reboot_type:
    version_added: '8.3.0'
    type: str
    description:
      - This option provides the choices to reboot the server immediately after the firmware update.
      - This is applicable when I(schedule) is C(RebootNow).
      - C(GracefulRebootForce) performs a graceful reboot with forced shutdown.
      - C(GracefulReboot) performs a graceful reboot without forced shutdown.
      - C(PowerCycle) performs a power cycle for a hard reset on the device.
    choices:
      - GracefulReboot
      - GracefulRebootForce
      - PowerCycle
    default: GracefulRebootForce
requirements:
    - "python >= 3.9.6"
author:
    - "Felix Stephen (@felixs88)"
    - "Jagadeesh N V (@jagadeeshnv)"
    - "Abhishek Sinha (@ABHISHEK-SINHA10)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Update firmware from DUP file using device ids
  dellemc.openmanage.ome_firmware:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_id:
      - 11111
      - 22222
    dup_file: "/path/Chassis-System-Management_Firmware_6N9WN_WN64_1.00.01_A00.EXE"

- name: Update firmware from a DUP file using a device service tags
  dellemc.openmanage.ome_firmware:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_service_tag:
      - KLBR111
      - KLBR222
    dup_file: "/path/Network_Firmware_NTRW0_WN64_14.07.07_A00-00_01.EXE"

- name: Update firmware from a DUP file using a device group names
  dellemc.openmanage.ome_firmware:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_group_names:
      - servers
    dup_file: "/path/BIOS_87V69_WN64_2.4.7.EXE"

- name: Update firmware using baseline name
  dellemc.openmanage.ome_firmware:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    baseline_name: baseline_devices

- name: Stage firmware for the next reboot using baseline name
  dellemc.openmanage.ome_firmware:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    baseline_name: baseline_devices
    schedule: StageForNextReboot

- name: "Update firmware using baseline name and components."
  dellemc.openmanage.ome_firmware:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    baseline_name: baseline_devices
    components:
      - BIOS

- name: Update firmware of device components from a DUP file using a device ids in a baseline
  dellemc.openmanage.ome_firmware:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    baseline_name: baseline_devices
    device_id:
      - 11111
      - 22222
    components:
      - iDRAC with Lifecycle Controller

- name: Update firmware of device components from a baseline using a device service tags under a baseline
  dellemc.openmanage.ome_firmware:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    baseline_name: baseline_devices
    device_service_tag:
      - KLBR111
      - KLBR222
    components:
      - IOM-SAS

- name: Update firmware using baseline name with a device id and required components
  dellemc.openmanage.ome_firmware:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    baseline_name: baseline_devices
    devices:
      - id: 12345
        components:
          - Lifecycle Controller
      - id: 12346
        components:
          - Enterprise UEFI Diagnostics
          - BIOS

- name: "Update firmware using baseline name with a device service tag and required components."
  dellemc.openmanage.ome_firmware:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    baseline_name: baseline_devices
    devices:
      - service_tag: ABCDE12
        components:
          - PERC H740P Adapter
          - BIOS
      - service_tag: GHIJK34
        components:
          - OS Drivers Pack

- name: "Update firmware using baseline name with a device service tag or device id and required components."
  dellemc.openmanage.ome_firmware:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    baseline_name: baseline_devices
    devices:
      - service_tag: ABCDE12
        components:
          - BOSS-S1 Adapter
          - PowerEdge Server BIOS
      - id: 12345
        components:
          - iDRAC with Lifecycle Controller

- name: "Update firmware using baseline name and components and perform Powercycle."
  dellemc.openmanage.ome_firmware:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    baseline_name: baseline_devices
    components:
      - BIOS
    reboot_type: PowerCycle
'''

RETURN = r'''
---
msg:
  type: str
  description: "Overall firmware update status."
  returned: always
  sample: Successfully submitted the firmware update job.
update_status:
  type: dict
  description: The firmware update job and progress details from the OME.
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
      'Data': 'DCIM:INSTALLED#701__NIC.Mezzanine.1A-1-1=1234567654321',
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
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.urls import ConnectionError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError


COMPLIANCE_URI = "UpdateService/Baselines({0})/DeviceComplianceReports"
BASELINE_URI = "UpdateService/Baselines"
FW_JOB_DESC = "Firmware update task initiated from OpenManage Ansible Module collections"
NO_CHANGES_MSG = "No changes found to be applied. Either there are no updates present or components specified are not" \
                 " found in the baseline."
COMPLIANCE_READ_FAIL = "Failed to read compliance report."
DUP_REQ_MSG = "Parameter 'dup_file' to be provided along with 'device_id'|'device_service_tag'|'device_group_names'"
APPLICABLE_DUP = "Unable to get applicable components DUP."
CHANGES_FOUND = "Changes found to be applied."


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
        module.exit_json(msg="Unable to fetch the job type Id.", failed=True)
    stage_dict = {"StageForNextReboot": 'true', "RebootNow": 'false'}
    schedule = module.params["schedule"]
    params = [{"Key": "operationName", "Value": "INSTALL_FIRMWARE"},
              {"Key": "stagingValue", "Value": stage_dict[schedule]},
              {"Key": "signVerify", "Value": "true"}]
    # reboot applicable only if staging false
    if schedule == "RebootNow":
        reboot_dict = {"PowerCycle": "1",
                       "GracefulReboot": "2",
                       "GracefulRebootForce": "3"}
        reboot_type = module.params["reboot_type"]
        params.append({"Key": "rebootType", "Value": reboot_dict[reboot_type]})
    payload = {
        "Id": 0, "JobName": "Firmware Update Task",
        "JobDescription": FW_JOB_DESC, "Schedule": "startnow",
        "State": "Enabled", "JobType": {"Id": resp, "Name": "Update_Task"},
        "Targets": target_data,
        "Params": params
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
        module.exit_json(msg=APPLICABLE_DUP, failed=True)
    return target_data


def get_dup_applicability_payload(file_token, device_ids=None, group_ids=None, baseline_ids=None):
    """Returns the DUP applicability JSON payload."""
    dup_applicability_payload = {'SingleUpdateReportBaseline': [],
                                 'SingleUpdateReportGroup': [],
                                 'SingleUpdateReportTargets': [],
                                 'SingleUpdateReportFileToken': file_token}
    if device_ids is not None:
        dup_applicability_payload.update({"SingleUpdateReportTargets": list(map(int, device_ids))})
    elif group_ids is not None:
        dup_applicability_payload.update({"SingleUpdateReportGroup": list(map(int, group_ids))})
    elif baseline_ids is not None:
        dup_applicability_payload.update({"SingleUpdateReportBaseline": list(map(int, baseline_ids))})
    return dup_applicability_payload


def upload_dup_file(rest_obj, module):
    """Upload DUP file to OME and get a file token."""
    upload_uri = "UpdateService/Actions/UpdateService.UploadFile"
    headers = {"Content-Type": "application/octet-stream", "Accept": "application/octet-stream"}
    upload_success, token = False, None
    dup_file = module.params['dup_file']
    with open(dup_file, 'rb') as payload:
        payload = payload.read()
        response = rest_obj.invoke_request("POST", upload_uri, data=payload, headers=headers,
                                           api_timeout=100, dump=False)
        if response.status_code == 200:
            upload_success = True
            token = str(response.json_data)
        else:
            module.exit_json(msg="Unable to upload {0} to {1}".format(dup_file, module.params['hostname']), failed=True)
    return upload_success, token


def get_device_ids(rest_obj, module, device_id_tags):
    """Getting the list of device ids filtered from the device inventory."""
    device_id = []
    resp = rest_obj.get_all_report_details("DeviceService/Devices")
    if resp.get("report_list"):
        device_resp = dict([(str(device['Id']), device['DeviceServiceTag']) for device in resp["report_list"]])
        device_tags = map(str, device_id_tags)
        invalid_tags = []
        for tag in device_tags:
            if tag in device_resp.keys():
                device_id.append(tag)
            elif tag in device_resp.values():
                ids = list(device_resp.keys())[list(device_resp.values()).index(tag)]
                device_id.append(ids)
            else:
                invalid_tags.append(tag)
        if invalid_tags:
            module.exit_json(
                msg="Unable to complete the operation because the entered target device service"
                    " tag(s) or device id(s) '{0}' are invalid.".format(",".join(set(invalid_tags))), failed=True)
    else:
        module.exit_json(msg="Failed to fetch the device facts.", failed=True)
    return device_id, device_resp


def get_group_ids(rest_obj, module):
    """Getting the list of group ids filtered from the groups."""
    resp = rest_obj.get_all_report_details("GroupService/Groups")
    group_name = module.params.get('device_group_names')
    if resp["report_list"]:
        grp_ids = [grp['Id'] for grp in resp["report_list"] for grpname in group_name if grp['Name'] == grpname]
        if len(set(group_name)) != len(set(grp_ids)):
            module.exit_json(
                msg="Unable to complete the operation because the entered target device group name(s)"
                    " '{0}' are invalid.".format(",".join(set(group_name))), failed=True)
    return grp_ids


def get_baseline_ids(rest_obj, module):
    """Getting the list of group ids filtered from the groups."""
    resp = rest_obj.get_all_report_details(BASELINE_URI)
    baseline, baseline_details = module.params.get('baseline_name'), {}
    if resp["report_list"]:
        for bse in resp["report_list"]:
            if bse['Name'] == baseline:
                baseline_details["baseline_id"] = bse["Id"]
                baseline_details["repo_id"] = bse["RepositoryId"]
                baseline_details["catalog_id"] = bse["CatalogId"]
        if not baseline_details:
            module.exit_json(
                msg="Unable to complete the operation because the entered target baseline name"
                    " '{0}' is invalid.".format(baseline), failed=True)
    else:
        module.exit_json(msg="Unable to complete the operation because the entered "
                             "target baseline name does not exist.", failed=True)
    return baseline_details


def single_dup_update(rest_obj, module):
    target_data, device_ids, group_ids, baseline_ids = None, None, None, None
    if module.params.get("device_group_names") is not None:
        group_ids = get_group_ids(rest_obj, module)
    else:
        device_id_tags = _validate_device_attributes(module)
        device_ids, id_tag_map = get_device_ids(rest_obj, module, device_id_tags)
    if module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    upload_status, token = upload_dup_file(rest_obj, module)
    if upload_status:
        report_payload = get_dup_applicability_payload(token, device_ids=device_ids, group_ids=group_ids,
                                                       baseline_ids=baseline_ids)
        if report_payload:
            target_data = get_applicable_components(rest_obj, report_payload, module)
    return target_data


def baseline_based_update(rest_obj, module, baseline, dev_comp_map):
    compliance_uri = COMPLIANCE_URI.format(baseline["baseline_id"])
    resp = rest_obj.get_all_report_details(compliance_uri)
    compliance_report_list = []
    update_actions = ["UPGRADE", "DOWNGRADE"]
    if resp["report_list"]:
        comps = []
        if not dev_comp_map:
            comps = module.params.get('components')
            dev_comp_map = dict([(str(dev["DeviceId"]), comps) for dev in resp["report_list"]])
        for dvc in resp["report_list"]:
            dev_id = dvc["DeviceId"]
            if str(dev_id) in dev_comp_map:
                comps = dev_comp_map.get(str(dev_id), [])
                compliance_report = dvc.get("ComponentComplianceReports")
                if compliance_report is not None:
                    data_dict = {}
                    comp_list = []
                    if not comps:
                        comp_list = list(icomp["SourceName"] for icomp in compliance_report
                                         if icomp["UpdateAction"] in update_actions)
                    else:
                        comp_list = list(icomp["SourceName"] for icomp in compliance_report
                                         if ((icomp["UpdateAction"] in update_actions) and
                                         (icomp.get('Name').strip() in comps)))  # regex filtering ++
                    if comp_list:
                        data_dict["Id"] = dev_id
                        data_dict["Data"] = str(";").join(comp_list)
                        data_dict["TargetType"] = {"Id": dvc['DeviceTypeId'], "Name": dvc["DeviceTypeName"]}
                        compliance_report_list.append(data_dict)
    else:
        module.exit_json(msg=COMPLIANCE_READ_FAIL, changed=True)
    if not compliance_report_list:
        module.exit_json(msg=NO_CHANGES_MSG)
    if module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    return compliance_report_list


def _validate_device_attributes(module):
    device_id_tags = []
    service_tag = module.params.get('device_service_tag')
    device_id = module.params.get('device_id')
    devices = module.params.get('devices')
    if devices:
        for dev in devices:
            if dev.get('id'):
                device_id_tags.append(dev.get('id'))
            else:
                device_id_tags.append(dev.get('service_tag'))
    if device_id is not None:
        device_id_tags.extend(device_id)
    if service_tag is not None:
        device_id_tags.extend(service_tag)
    return device_id_tags


def get_device_component_map(rest_obj, module):
    device_id_tags = _validate_device_attributes(module)
    device_ids, id_tag_map = get_device_ids(rest_obj, module, device_id_tags)
    comps = module.params.get('components')
    dev_comp_map = {}
    if device_ids:
        dev_comp_map = dict([(dev, comps) for dev in device_ids])
    devices = module.params.get('devices')
    if devices:
        for dev in devices:
            if dev.get('id'):
                dev_comp_map[str(dev.get('id'))] = dev.get('components')
            else:
                id = list(id_tag_map.keys())[list(id_tag_map.values()).index(dev.get('service_tag'))]
                dev_comp_map[str(id)] = dev.get('components')
    return dev_comp_map


def validate_inputs(module):
    param = module.params
    if param.get("dup_file"):
        if not any([param.get("device_id"), param.get("device_service_tag"), param.get("device_group_names")]):
            module.exit_json(msg=DUP_REQ_MSG, failed=True)


def main():
    specs = {
        "device_service_tag": {"type": "list", "elements": 'str'},
        "device_id": {"type": "list", "elements": 'int'},
        "dup_file": {"type": "path"},
        "device_group_names": {"type": "list", "elements": 'str'},
        "components": {"type": "list", "elements": 'str', "default": []},
        "baseline_name": {"type": "str"},
        "schedule": {"type": 'str', "choices": ['RebootNow', 'StageForNextReboot'], "default": 'RebootNow'},
        "reboot_type": {"type": 'str',
                        "choices": ['PowerCycle', 'GracefulReboot', 'GracefulRebootForce'],
                        "default": 'GracefulRebootForce'},
        "devices": {
            "type": 'list', "elements": 'dict',
            "options": {
                "id": {'type': 'int'},
                "service_tag": {"type": 'str'},
                "components": {"type": "list", "elements": 'str', "default": []},
            },
            "mutually_exclusive": [('id', 'service_tag')],
            "required_one_of": [('id', 'service_tag')]
        },
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        required_one_of=[["dup_file", "baseline_name"]],
        mutually_exclusive=[
            ["baseline_name", "dup_file"],
            ["device_group_names", "device_id", "devices"],
            ["device_group_names", "device_service_tag", "devices"],
            ["baseline_name", "device_group_names"],
            ["dup_file", "components", "devices"]],
        supports_check_mode=True
    )
    validate_inputs(module)
    update_status, baseline_details = {}, None
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            if module.params.get("baseline_name"):
                baseline_details = get_baseline_ids(rest_obj, module)
                device_comp_map = get_device_component_map(rest_obj, module)
                target_data = baseline_based_update(rest_obj, module, baseline_details, device_comp_map)
            else:
                target_data = single_dup_update(rest_obj, module)
            job_payload = job_payload_for_update(rest_obj, module, target_data, baseline=baseline_details)
            update_status = spawn_update_job(rest_obj, job_payload)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, AttributeError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)
    module.exit_json(msg="Successfully submitted the firmware update job.", update_status=update_status, changed=True)


if __name__ == "__main__":
    main()
