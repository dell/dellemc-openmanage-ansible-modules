#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.4
# Copyright (C) 2020-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_job_info
short_description: Get job details for a given job ID or an entire job queue on OpenMange Enterprise
version_added: "2.0.0"
description: This module retrieves job details for a given job ID or an entire job queue on OpenMange Enterprise.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  job_id:
    description: Unique ID of the job.
    type: int
  system_query_options:
    description: Options for pagination of the output.
    type: dict
    suboptions:
      top:
        description: Number of records to return. Default value is 100.
        type: int
      skip:
        description: Number of records to skip. Default value is 0.
        type: int
      filter:
        description: Filter records by the values supported.
        type: str
  fetch_execution_history:
    description:
      - Fetches the execution history of the job.
      - I(fetch_execution_history) is only applicable when valid I(job_id) is given.
      - When C(true), fetches all the execution history details.
      - When C(false), fetches only the job info and last execution details.
    type: bool
    default: false
requirements:
  - "python >= 3.9.6"
author:
  - "Jagadeesh N V (@jagadeeshnv)"
  - "Abhishek Sinha (@Abhishek-Dell)"
  - "Mangirish Kenkare(@MangirishK)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Get all jobs details
  dellemc.openmanage.ome_job_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"

- name: Get job details for id
  dellemc.openmanage.ome_job_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    job_id: 12345

- name: Get filtered job details
  dellemc.openmanage.ome_job_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    system_query_options:
      top: 2
      skip: 1
      filter: "JobType/Id eq 8"

- name: Get detail job execution history with last execution detail for a job.
  dellemc.openmanage.ome_job_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    job_id: 12345
    fetch_execution_history: true
'''

RETURN = r'''
---
msg:
  description: Overall status of the job facts operation.
  returned: always
  type: str
  sample: "Successfully fetched the job info"
job_info:
  description: Details of the OpenManage Enterprise jobs.
  returned: success
  type: dict
  sample: {
    "value": [
    {
      "Id": 10429,
      "JobName": "Discovery-201",
      "JobDescription": "Discovery-201",
      "NextRun": null,
      "LastRun": "2023-06-07 09:33:07.161",
      "StartTime": null,
      "EndTime": null,
      "Schedule": "startnow",
      "State": "Enabled",
      "CreatedBy": "admin",
      "UpdatedBy": "admin",
      "Visible": true,
      "Editable": true,
      "Builtin": false,
      "UserGenerated": true,
      "Targets": [],
      "Params": [],
      "LastRunStatus": {
        "Id": 2070,
        "Name": "Failed"
      },
      "JobType": {
        "Id": 101,
        "Name": "Discovery_Task",
        "Internal": false
      },
      "JobStatus": {
        "Id": 2080,
        "Name": "New"
      },
      "ExecutionHistories": [
        {
          "Id": 1243224,
          "JobName": "Discovery-201",
          "Progress": "100",
          "StartTime": "2023-06-07 09:33:07.148",
          "EndTime": "2023-06-07 09:33:08.403",
          "LastUpdateTime": "2023-06-07 09:33:08.447185",
          "ExecutedBy": "admin",
          "JobId": 10429,
          "JobStatus": {
            "Id": 2070,
            "Name": "Failed"
          },
          "ExecutionHistoryDetails": [
            {
              "Id": 1288519,
              "Progress": "100",
              "StartTime": "2023-06-07 09:33:07.525",
              "EndTime": "2023-06-07 09:33:08.189",
              "ElapsedTime": "00:00:00",
              "Key": "198.168.0.1",
              "Value": "Running\nDiscovery of target 198.168.0.1 started
              .\nDiscovery target resolved to IP  198.168.0.1 .\n:
              ========== EEMI Code: CGEN1009 ==========\nMessage:
              Unable to perform the requested action because the device
              management endpoint authentication over WSMAN, REDFISH failed.
              \nRecommended actions: Make sure the credentials associated
              with the device management endpoint are valid and retry the
              operation.\n=======================================\nTask Failed.
              Completed With Errors.",
              "ExecutionHistoryId": 1243224,
              "IdBaseEntity": 0,
              "JobStatus": {
                "Id": 2070,
                "Name": "Failed"
              }
            },
            {
              "Id": 1288518,
              "Progress": "100",
              "StartTime": "2023-06-07 09:33:07.521",
              "EndTime": "2023-06-07 09:33:08.313",
              "ElapsedTime": "00:00:00",
              "Key": "198.168.0.2",
              "Value": "Running\nDiscovery of target 198.168.0.2 started.
              \nDiscovery target resolved to IP  198.168.0.2 .\n:
              ========== EEMI Code: CGEN1009 ==========\nMessage:
              Unable to perform the requested action because the device
              management endpoint authentication over WSMAN, REDFISH failed.
              \nRecommended actions: Make sure the credentials associated
              with the device management endpoint are valid and retry the
              operation.\n=======================================\nTask Failed.
              Completed With Errors.",
              "ExecutionHistoryId": 1243224,
              "IdBaseEntity": 0,
              "JobStatus": {
                "Id": 2070,
                "Name": "Failed"
              }
            }
          ]
        },
        {
          "Id": 1243218,
          "JobName": "Discovery-201",
          "Progress": "100",
          "StartTime": "2023-06-07 09:30:55.064",
          "EndTime": "2023-06-07 09:30:56.338",
          "LastUpdateTime": "2023-06-07 09:30:56.365294",
          "ExecutedBy": "admin",
          "JobId": 10429,
          "JobStatus": {
            "Id": 2070,
            "Name": "Failed"
          },
          "ExecutionHistoryDetails": [
            {
              "Id": 1288512,
              "Progress": "100",
              "StartTime": "2023-06-07 09:30:55.441",
              "EndTime": "2023-06-07 09:30:56.085",
              "ElapsedTime": "00:00:00",
              "Key": "198.168.0.1",
              "Value": "Running\nDiscovery of target 198.168.0.1 started.
              \nDiscovery target resolved to IP  198.168.0.1 .\n:
              ========== EEMI Code: CGEN1009 ==========\nMessage:
              Unable to perform the requested action because the device
              management endpoint authentication over WSMAN, REDFISH failed.
              \nRecommended actions: Make sure the credentials associated
              with the device management endpoint are valid and retry the
              operation.\n=======================================\nTask Failed.
              Completed With Errors.",
              "ExecutionHistoryId": 1243218,
              "IdBaseEntity": 0,
              "JobStatus": {
                "Id": 2070,
                "Name": "Failed"
              }
            },
            {
              "Id": 1288511,
              "Progress": "100",
              "StartTime": "2023-06-07 09:30:55.439",
              "EndTime": "2023-06-07 09:30:56.21",
              "ElapsedTime": "00:00:00",
              "Key": "198.168.0.2",
              "Value": "Running\nDiscovery of target 198.168.0.2 started.
              \nDiscovery target resolved to IP  198.168.0.2 .\n:
              ========== EEMI Code: CGEN1009 ==========\nMessage:
              Unable to perform the requested action because the device
              management endpoint authentication over WSMAN, REDFISH failed.
              \nRecommended actions: Make sure the credentials associated
              with the device management endpoint are valid and retry
              the operation.\n=======================================\nTask Failed.
              Completed With Errors.",
              "ExecutionHistoryId": 1243218,
              "IdBaseEntity": 0,
              "JobStatus": {
                "Id": 2070,
                "Name": "Failed"
              }
            }
          ]
        }
      ],
      "LastExecutionDetail": {
        "Id": 1288519,
        "Progress": "100",
        "StartTime": "2023-06-07 09:33:07.525",
        "EndTime": "2023-06-07 09:33:08.189",
        "ElapsedTime": null,
        "Key": "198.168.0.1",
        "Value": "Running\nDiscovery of target 198.168.0.1 started.
        \nDiscovery target resolved to IP  198.168.0.1 .\n:
        ========== EEMI Code: CGEN1009 ==========\nMessage:
        Unable to perform the requested action because the device
        management endpoint authentication over WSMAN, REDFISH failed.
        \nRecommended actions: Make sure the credentials associated
        with the device management endpoint are valid and retry the operation.
        \n=======================================\nTask Failed.
        Completed With Errors.",
        "ExecutionHistoryId": 1243224,
        "IdBaseEntity": 0,
        "JobStatus": {
          "Id": 2070,
          "Name": "Failed"
        }
      }
    }
]
}
'''

import json
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import strip_substr_dict, remove_key
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError

JOBS_URI = "JobService/Jobs"
EXECUTION_HISTORIES_URI = "JobService/Jobs({0})/ExecutionHistories"
LAST_EXECUTION_DETAIL_URI = "JobService/Jobs({0})/LastExecutionDetail"


def _get_query_parameters(module_params):
    """Builds query parameter
    :returns: dictionary, which builds the query format
     eg : {"$filter": "JobType/Id eq 8"}
     """
    system_query_options_param = module_params.get("system_query_options")
    query_parameter = {}
    if system_query_options_param:
        query_parameter = dict([("$" + k, v) for k, v in system_query_options_param.items() if v is not None])
    return query_parameter


def get_uri_detail(rest_obj, uri):
    try:
        result = []
        resp = rest_obj.invoke_request('GET', uri)
        json_data = resp.json_data
        if value := json_data.get('value'):
            for each_element in value:
                each_element.get('JobStatus', {}).pop('@odata.type', None)
                execution_history_detail_uri = each_element.get('ExecutionHistoryDetails@odata.navigationLink', '')[5:]
                if execution_history_detail_uri:
                    execution_history_detail = get_uri_detail(rest_obj, execution_history_detail_uri)
                    each_element.update({"ExecutionHistoryDetails": execution_history_detail})
                result.append(strip_substr_dict(each_element))
        else:
            json_data.get('JobStatus', {}).pop('@odata.type', None)
            result = strip_substr_dict(json_data)
    except Exception:
        pass
    return result


def get_execution_history_of_a_job(rest_obj, job_id):
    try:
        execution_histories = get_uri_detail(
            rest_obj, EXECUTION_HISTORIES_URI.format(job_id))
    except Exception:
        pass
    return execution_histories


def last_execution_detail_of_a_job(rest_obj, job_id):
    try:
        last_execution_detail = get_uri_detail(
            rest_obj, LAST_EXECUTION_DETAIL_URI.format(job_id))
    except Exception:
        pass
    return last_execution_detail


def main():
    specs = {
        "job_id": {"required": False, "type": 'int'},
        "system_query_options": {"required": False, "type": 'dict', "options": {
            "top": {"type": 'int', "required": False},
            "skip": {"type": 'int', "required": False},
            "filter": {"type": 'str', "required": False},
        }},
        "fetch_execution_history": {"type": 'bool', "default": False},
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        supports_check_mode=True
    )

    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            resp_status = []
            if module.params.get("job_id") is not None:
                # Fetch specific job
                job_id = module.params.get("job_id")
                jpath = "{0}({1})".format(JOBS_URI, job_id)
                resp = rest_obj.invoke_request('GET', jpath)
                job_facts = remove_key(resp.json_data)
                execution_detail = []
                if module.params.get("fetch_execution_history"):
                    execution_detail = get_execution_history_of_a_job(rest_obj, job_id)
                last_execution = last_execution_detail_of_a_job(rest_obj, job_id)
                job_facts.update({'ExecutionHistories': execution_detail,
                                  'LastExecutionDetail': last_execution})
                resp_status.append(resp.status_code)
            else:
                # query applicable only for all jobs list fetching
                query_param = _get_query_parameters(module.params)
                if query_param:
                    resp = rest_obj.invoke_request('GET', JOBS_URI, query_param=query_param)
                    job_facts = resp.json_data
                    job_facts = remove_key(job_facts)
                    resp_status.append(resp.status_code)
                else:
                    # Fetch all jobs, filter and pagination options
                    job_report = rest_obj.get_all_report_details(JOBS_URI)
                    job_facts = {"value": job_report["report_list"]}
                    job_facts = remove_key(job_facts)
                    if len(job_facts["value"]) > 0:
                        resp_status.append(200)
                for each_value in job_facts["value"]:
                    job_id = each_value["Id"] if "Id" in each_value else None
                    last_execution = last_execution_detail_of_a_job(rest_obj, job_id)
                    each_value.update({'ExecutionHistories': [],
                                       'LastExecutionDetail': last_execution})
    except HTTPError as httperr:
        module.exit_json(msg=str(httperr), job_info=json.load(httperr), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)
    if 200 in resp_status:
        module.exit_json(msg="Successfully fetched the job info", job_info=job_facts)
    else:
        module.exit_json(msg="Failed to fetch the job info", failed=True)


if __name__ == '__main__':
    main()
