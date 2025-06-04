#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2021-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
---
module: ome_diagnostics
short_description: Export technical support logs(TSR) to network share location
version_added: "3.6.0"
description: This module allows to export SupportAssist collection logs from OpenManage Enterprise and
  OpenManage Enterprise Modular and application logs from OpenManage Enterprise Modular to a CIFS or NFS share.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  device_ids:
    type: list
    description:
      - List of target device IDs.
      - This is applicable for C(support_assist_collection) and C(supportassist_collection) logs.
      - This option is mutually exclusive with I(device_service_tags) and I(device_group_name).
    elements: int
  device_service_tags:
    type: list
    description:
      - List of target identifier.
      - This is applicable for C(support_assist_collection) and C(supportassist_collection) logs.
      - This option is mutually exclusive with I(device_ids) and I(device_group_name).
    elements: str
  device_group_name:
    type: str
    description:
      - Name of the device group to export C(support_assist_collection) or C(supportassist_collection) logs of all devices within the group.
      - This is applicable for C(support_assist_collection) and C(supportassist_collection) logs.
      - This option is not applicable for OpenManage Enterprise Modular.
      - This option is mutually exclusive with I(device_ids) and I(device_service_tags).
  log_type:
    type: str
    description:
      - C(application) is applicable for OpenManage Enterprise Modular to export the application log bundle.
      - C(support_assist_collection) and C(supportassist_collection) is applicable for one or more devices to export SupportAssist logs.
      - C(support_assist_collection) and C(supportassist_collection) supports both OpenManage Enterprise and OpenManage Enterprise Modular.
      - C(support_assist_collection) and C(supportassist_collection) does not support export of C(OS_LOGS) from OpenManage Enterprise.
        If tried to export, the tasks will complete with errors, and the module fails.
    choices: [application, support_assist_collection, supportassist_collection]
    default: support_assist_collection
  mask_sensitive_info:
    type: bool
    description:
      - Select this option to mask the personal identification information such as IPAddress,
        DNS, alert destination, email, gateway, inet6, MacAddress, netmask etc.
      - This option is applicable for C(application) of I(log_type).
    default: false
  log_selectors:
    type: list
    description:
      - By default, the SupportAssist logs contain only hardware logs. To collect additional logs
        such as OS logs, RAID logs or Debug logs, specify the log types to be collected in the choices list.
      - If the log types are not specified, only the hardware logs are exported.
      - C(OS_LOGS) to collect OS Logs.
      - C(RAID_LOGS) to collect RAID controller logs.
      - C(DEBUG_LOGS) to collect Debug logs.
      - This option is applicable only for C(support_assist_collection) and C(supportassist_collection) of I(log_type).
    choices: [OS_LOGS, RAID_LOGS, DEBUG_LOGS]
    elements: str
  share_address:
    type: str
    required: true
    description: Network share IP address.
  share_name:
    type: str
    required: true
    description:
      - Network share path.
      - Filename is auto generated and should not be provided as part of I(share_name).
  share_type:
    type: str
    required: true
    description: Network share type
    choices: [NFS, CIFS]
  share_user:
    type: str
    description:
      - Network share username.
      - This option is applicable for C(CIFS) of I(share_type).
  share_password:
    type: str
    description:
      - Network share password
      - This option is applicable for C(CIFS) of I(share_type).
  share_domain:
    type: str
    description:
      - Network share domain name.
      - This option is applicable for C(CIFS) if I(share_type).
  job_wait:
    type: bool
    description:
      - Whether to wait for the Job completion or not.
      - The maximum wait time is I(job_wait_timeout).
    default: true
  job_wait_timeout:
    type: int
    description:
      - The maximum wait time of I(job_wait) in minutes.
      - This option is applicable I(job_wait) is true.
    default: 60
  test_connection:
    type: bool
    description:
      - Test the availability of the network share location.
      - I(job_wait) and I(job_wait_timeout) options are not applicable for I(test_connection).
    default: false
  lead_chassis_only:
    type: bool
    description:
      - Extract the logs from Lead chassis only.
      - I(lead_chassis_only) is only applicable when I(log_type) is C(application) on OpenManage Enterprise Modular.
    default: false
requirements:
  - "python >= 3.9.6"
author:
  - "Felix Stephen (@felixs88)"
  - "Sachin Apagundi(@sachin-apa)"
notes:
    - Run this module from a system that has direct access to OpenManage Enterprise.
    - This module performs the test connection and device validations. It does not create a job for copying the
      logs in check mode and always reports as changes found.
    - This module supports C(check_mode).
"""


EXAMPLES = r"""
---
- name: Export application log using CIFS share location
  dellemc.openmanage.ome_diagnostics:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    share_type: CIFS
    share_address: "192.168.0.2"
    share_user: share_username
    share_password: share_password
    share_name: cifs_share
    log_type: application
    mask_sensitive_info: false
    test_connection: true

- name: Export application log using NFS share location
  dellemc.openmanage.ome_diagnostics:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    share_address: "192.168.0.3"
    share_type: NFS
    share_name: nfs_share
    log_type: application
    mask_sensitive_info: true
    test_connection: true

- name: Export SupportAssist log using CIFS share location
  dellemc.openmanage.ome_diagnostics:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    share_address: "192.168.0.3"
    share_user: share_username
    share_password: share_password
    share_name: cifs_share
    share_type: CIFS
    log_type: support_assist_collection
    device_ids: [10011, 10022]
    log_selectors: [OS_LOGS]
    test_connection: true

- name: Export SupportAssist log using NFS share location
  dellemc.openmanage.ome_diagnostics:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    share_address: "192.168.0.3"
    share_type: NFS
    share_name: nfs_share
    log_type: support_assist_collection
    device_group_name: group_name
    test_connection: true
"""

RETURN = r"""
---
msg:
  type: str
  description: "Overall status of the export log."
  returned: always
  sample: "Export log job completed successfully."
jog_status:
  type: dict
  description: Details of the export log operation status.
  returned: success
  sample: {
    "Builtin": false,
    "CreatedBy": "root",
    "Editable": true,
    "EndTime": None,
    "Id": 12778,
    "JobDescription": "Export device log",
    "JobName": "Export Log",
    "JobStatus": {"Id": 2080, "Name": "New"},
    "JobType": {"Id": 18, "Internal": false, "Name": "DebugLogs_Task"},
    "LastRun": "2021-07-06 10:52:50.519",
    "LastRunStatus": {"Id": 2060, "Name": "Completed"},
    "NextRun": None,
    "Schedule": "startnow",
    "StartTime": None,
    "State": "Enabled",
    "UpdatedBy": None,
    "UserGenerated": true,
    "Visible": true,
    "Params": [
      {"JobId": 12778, "Key": "maskSensitiveInfo", "Value": "FALSE"},
      {"JobId": 12778, "Key": "password", "Value": "tY86w7q92u0QzvykuF0gQQ"},
      {"JobId": 12778, "Key": "userName", "Value": "administrator"},
      {"JobId": 12778, "Key": "shareName", "Value": "iso"},
      {"JobId": 12778, "Key": "OPERATION_NAME", "Value": "EXTRACT_LOGS"},
      {"JobId": 12778, "Key": "shareType", "Value": "CIFS"},
      {"JobId": 12778, "Key": "shareAddress", "Value": "100.96.32.142"}
    ],
    "Targets": [{"Data": "", "Id": 10053, "JobId": 12778, "TargetType": {"Id": 1000, "Name": "DEVICE"}}]
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
"""


import json
import re
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
LOG_SELECTOR = {"OS_LOGS": 1, "RAID_LOGS": 2, "DEBUG_LOGS": 3}
JOB_URI = "JobService/Jobs"
GROUP_URI = "GroupService/Groups"
GROUP_DEVICE_URI = "GroupService/Groups({0})/Devices"
DEVICE_URI = "DeviceService/Devices"
DOMAIN_URI = "ManagementDomainService/Domains"
EXE_HISTORY_URI = "JobService/Jobs({0})/ExecutionHistories"
CHANGES_FOUND = "Changes found to be applied."


def group_validation(module, rest_obj):
    group_name, group_device = module.params.get('device_group_name'), []
    query_param = {"$filter": "Name eq '{0}'".format(group_name)}
    group_resp = rest_obj.invoke_request("GET", GROUP_URI, query_param=query_param)
    group = group_resp.json_data["value"]
    if group:
        group_id = group[0]["Id"]
        resp = rest_obj.invoke_request("GET", GROUP_DEVICE_URI.format(group_id))
        device_group_resp = resp.json_data["value"]
        if device_group_resp:
            for device in device_group_resp:
                if device["Type"] == 1000:
                    group_device.append(device["Id"])
        else:
            module.fail_json(msg="There are no device(s) present in this group.")
    else:
        module.fail_json(msg="Unable to complete the operation because the entered target "
                             "device group name '{0}' is invalid.".format(group_name))
    if not group_device:
        module.fail_json(msg="The requested group '{0}' does not contain devices that "
                             "support export log.".format(group_name))
    return group_device


def device_validation(module, rest_obj):
    device_lst, invalid_lst, other_types = [], [], []
    devices, tags = module.params.get("device_ids"), module.params.get("device_service_tags")
    all_device = rest_obj.get_all_report_details(DEVICE_URI)
    key = "Id" if devices is not None else "DeviceServiceTag"
    value = "id" if key == "Id" else "service tag"
    req_device = devices if devices is not None else tags
    for each in req_device:
        device = list(filter(lambda d: d[key] in [each], all_device["report_list"]))
        if device and device[0]["Type"] == 1000:
            device_lst.append(device[0]["Id"])
        elif device and not device[0]["Type"] == 1000:
            other_types.append(str(each))
        else:
            invalid_lst.append(str(each))
    if invalid_lst:
        module.fail_json(msg="Unable to complete the operation because the entered "
                             "target device {0}(s) '{1}' are invalid.".format(value, ",".join(set(invalid_lst))))
    if not device_lst and other_types:
        module.fail_json(msg="The requested device {0}(s) '{1}' are "
                             "not applicable for export log.".format(value, ",".join(set(other_types))))
    return device_lst


def extract_log_operation(module, rest_obj, device_lst=None):
    payload_params, target_params = [], []
    log_type = module.params["log_type"]
    if log_type == "application":
        lead_only = module.params["lead_chassis_only"]
        resp_data = None
        if lead_only:
            domain_details = rest_obj.get_all_items_with_pagination(DOMAIN_URI)
            key = "Id"
            ch_device_id = None
            for each_domain in domain_details["value"]:
                if each_domain["DomainRoleTypeValue"] in ["LEAD", "STANDALONE"]:
                    ch_device_id = each_domain["DeviceId"]
            if ch_device_id:
                resp = rest_obj.invoke_request("GET", DEVICE_URI,
                                               query_param={"$filter": "{0} eq {1}".format(key, ch_device_id)})
                resp_data = resp.json_data["value"]
        else:
            resp = rest_obj.invoke_request("GET", DEVICE_URI, query_param={"$filter": "Type eq 2000"})
            resp_data = resp.json_data["value"]
        if resp_data:
            for dev in resp_data:
                target_params.append({"Id": dev["Id"], "Data": "",
                                      "TargetType": {"Id": dev["Type"], "Name": "CHASSIS"}})
        else:
            module.fail_json(msg="There is no device(s) available to export application log.")
    else:
        for device in device_lst:
            target_params.append({"Id": device, "Data": "",
                                  "TargetType": {"Id": 1000, "Name": "DEVICE"}})
    payload_params.append({"Key": "shareAddress", "Value": module.params["share_address"]})
    payload_params.append({"Key": "shareType", "Value": module.params["share_type"]})
    payload_params.append({"Key": "OPERATION_NAME", "Value": "EXTRACT_LOGS"})
    if module.params.get("share_name") is not None:
        payload_params.append({"Key": "shareName", "Value": module.params["share_name"]})
    if module.params.get("share_user") is not None:
        payload_params.append({"Key": "userName", "Value": module.params["share_user"]})
    if module.params.get("share_password") is not None:
        payload_params.append({"Key": "password", "Value": module.params["share_password"]})
    if module.params.get("share_domain") is not None:
        payload_params.append({"Key": "domainName", "Value": module.params["share_domain"]})
    if module.params.get("mask_sensitive_info") is not None and log_type == "application":
        payload_params.append({"Key": "maskSensitiveInfo", "Value": str(module.params["mask_sensitive_info"]).upper()})
    if module.params.get("log_selectors") is not None and (log_type == "support_assist_collection" or log_type == "supportassist_collection"):
        log_lst = [LOG_SELECTOR[i] for i in module.params["log_selectors"]]
        log_lst.sort()
        log_selector = ",".join(map(str, log_lst))
        payload_params.append({"Key": "logSelector", "Value": "0,{0}".format(log_selector)})
    response = rest_obj.job_submission("Export Log", "Export device log", target_params,
                                       payload_params, {"Id": 18, "Name": "DebugLogs_Task"})
    return response


def check_domain_service(module, rest_obj):
    try:
        rest_obj.invoke_request("GET", DOMAIN_URI, api_timeout=5)
    except HTTPError as err:
        err_message = json.load(err)
        if err_message["error"]["@Message.ExtendedInfo"][0]["MessageId"] == "CGEN1006":
            module.fail_json(msg="Export log operation is not supported on the specified system.")
    return


def find_failed_jobs(resp, rest_obj):
    msg, fail = "Export log job completed with errors.", False
    history = rest_obj.invoke_request("GET", EXE_HISTORY_URI.format(resp["Id"]))
    if history.json_data["value"]:
        hist = history.json_data["value"][0]
        history_details = rest_obj.invoke_request(
            "GET",
            "{0}({1})/ExecutionHistoryDetails".format(EXE_HISTORY_URI.format(resp["Id"]), hist["Id"])
        )
        for hd in history_details.json_data["value"]:
            if not re.findall(r"Job status for JID_\d+ is Completed with Errors.", hd["Value"]):
                fail = True
                break
        else:
            fail = False
    return msg, fail


def main():
    specs = {
        "device_ids": {"required": False, "type": "list", "elements": "int"},
        "device_service_tags": {"required": False, "type": "list", "elements": "str"},
        "device_group_name": {"required": False, "type": "str"},
        "log_type": {"required": False, "type": "str", "default": "support_assist_collection",
                     "choices": ["support_assist_collection", "application", "supportassist_collection"]},
        "mask_sensitive_info": {"required": False, "type": "bool", "default": False},
        "log_selectors": {"required": False, "type": "list",
                          "choices": ["RAID_LOGS", "OS_LOGS", "DEBUG_LOGS"], "elements": "str"},
        "share_address": {"required": True, "type": "str"},
        "share_name": {"required": True, "type": "str"},
        "share_type": {"required": True, "type": "str", "choices": ["NFS", "CIFS"]},
        "share_user": {"required": False, "type": "str"},
        "share_password": {"required": False, "type": "str", "no_log": True},
        "share_domain": {"required": False, "type": "str"},
        "job_wait": {"required": False, "type": "bool", "default": True},
        "job_wait_timeout": {"required": False, "type": "int", "default": 60},
        "test_connection": {"required": False, "type": "bool", "default": False},
        "lead_chassis_only": {"required": False, "type": "bool", "default": False},
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        required_if=[
            ['log_type', 'application', ['mask_sensitive_info']],
            ['log_type', 'support_assist_collection',
             ['device_ids', 'device_service_tags', 'device_group_name'], True],
            ['log_type', 'supportassist_collection',
             ['device_ids', 'device_service_tags', 'device_group_name'], True],
            ['share_type', 'CIFS', ['share_user', 'share_password']]
        ],
        mutually_exclusive=[('device_ids', 'device_service_tags', 'device_group_name')],
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            # checking the domain service
            if module.params["log_type"] == "application":
                check_domain_service(module, rest_obj)

            # checking any existing running job
            job_allowed, job_lst = rest_obj.check_existing_job_state("DebugLogs_Task")
            if not job_allowed:
                module.fail_json(msg="An export log job is already running. Wait for the job to finish.")

            # test network connection
            if module.params["test_connection"]:
                conn_resp = rest_obj.test_network_connection(module.params["share_address"],
                                                             module.params["share_name"],
                                                             module.params["share_type"],
                                                             module.params["share_user"],
                                                             module.params["share_password"],
                                                             module.params["share_domain"])
                job_failed, job_message = rest_obj.job_tracking(conn_resp.json_data["Id"], job_wait_sec=5,
                                                                sleep_time=5)
                if job_failed:
                    module.fail_json(msg="Unable to access the share. Ensure that the share address, share name, "
                                         "share domain, and share credentials provided are correct.")

            # validation for device id/tag/group
            valid_device = []
            if (module.params["log_type"] == "support_assist_collection" or module.params["log_type"] == "supportassist_collection") and \
                    module.params.get("device_group_name") is not None:
                valid_device = group_validation(module, rest_obj)
            elif (module.params["log_type"] == "support_assist_collection" or module.params["log_type"] == "supportassist_collection") and \
                    module.params.get("device_group_name") is None:
                valid_device = device_validation(module, rest_obj)

            # exit if running in check mode
            if module.check_mode:
                module.exit_json(msg=CHANGES_FOUND, changed=True)

            # extract log job operation
            response = extract_log_operation(module, rest_obj, device_lst=valid_device)
            message = "Export log job submitted successfully."
            if module.params["job_wait"]:
                seconds = module.params["job_wait_timeout"] * 60
                job_failed, job_message = rest_obj.job_tracking(response.json_data["Id"],
                                                                job_wait_sec=seconds,
                                                                sleep_time=5)
                message = "Export log job completed successfully."
                if job_message == "The job is not complete after {0} seconds.".format(seconds):
                    module.fail_json(
                        msg="The export job is not complete because it has exceeded the configured timeout period.",
                        job_status=response.json_data
                    )
                if job_failed:
                    message, failed_job = find_failed_jobs(response.json_data, rest_obj)
                    if failed_job:
                        module.fail_json(msg=message, job_status=response.json_data)
                response = rest_obj.invoke_request("GET", "{0}({1})".format(JOB_URI, response.json_data["Id"]))
            resp = response.json_data
            if resp:
                resp = rest_obj.strip_substr_dict(resp)
            module.exit_json(msg=message, job_status=resp, changed=True)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, TypeError, SSLError, ConnectionError, SSLValidationError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
