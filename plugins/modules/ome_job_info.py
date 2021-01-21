#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.0.0
# Copyright (C) 2020-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

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
requirements:
    - "python >= 2.7.5"
author: "Jagadeesh N V(@jagadeeshnv)"
notes:
    - Run this module from a system that has direct access to DellEMC OpenManage Enterprise.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Get all jobs details
  dellemc.openmanage.ome_job_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"

- name: Get job details for id
  dellemc.openmanage.ome_job_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    job_id: 12345

- name: Get filtered job details
  dellemc.openmanage.ome_job_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    system_query_options:
      top: 2
      skip: 1
      filter: "JobType/Id eq 8"

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
      "Builtin": false,
      "CreatedBy": "system",
      "Editable": true,
      "EndTime": null,
      "Id": 12345,
      "JobDescription": "Refresh Inventory for Device",
      "JobName": "Refresh Inventory for Device",
      "JobStatus": {
        "Id": 2080,
        "Name": "New"
      },
      "JobType": {
        "Id": 8,
        "Internal": false,
        "Name": "Inventory_Task"
      },
      "LastRun": "2000-01-29 10:51:34.776",
      "LastRunStatus": {
        "Id": 2060,
        "Name": "Completed"
      },
      "NextRun": null,
      "Params": [],
      "Schedule": "",
      "StartTime": null,
      "State": "Enabled",
      "Targets": [
        {
          "Data": "''",
          "Id": 123123,
          "JobId": 12345,
          "TargetType": {
            "Id": 1000,
            "Name": "DEVICE"
          }
        }
      ],
      "UpdatedBy": null,
      "Visible": true
    }
  ]}
'''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError

JOBS_URI = "JobService/Jobs"


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


def main():
    module = AnsibleModule(
        argument_spec={
            "hostname": {"required": True, "type": 'str'},
            "username": {"required": True, "type": 'str'},
            "password": {"required": True, "type": 'str', "no_log": True},
            "port": {"required": False, "type": 'int', "default": 443},
            "job_id": {"required": False, "type": 'int'},
            "system_query_options": {"required": False, "type": 'dict', "options": {
                "top": {"type": 'int', "required": False},
                "skip": {"type": 'int', "required": False},
                "filter": {"type": 'str', "required": False},
            }},
        },
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
                job_facts = resp.json_data
                resp_status.append(resp.status_code)
            else:
                # query applicable only for all jobs list fetching
                query_param = _get_query_parameters(module.params)
                if query_param:
                    resp = rest_obj.invoke_request('GET', JOBS_URI, query_param=query_param)
                    job_facts = resp.json_data
                    resp_status.append(resp.status_code)
                else:
                    # Fetch all jobs, filter and pagination options
                    job_report = rest_obj.get_all_report_details(JOBS_URI)
                    job_facts = {"@odata.context": job_report["resp_obj"].json_data["@odata.context"],
                                 "@odata.count": len(job_report["report_list"]),
                                 "value": job_report["report_list"]}
                    if job_facts["@odata.count"] > 0:
                        resp_status.append(200)
    except HTTPError as httperr:
        module.fail_json(msg=str(httperr), job_info=json.load(httperr))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError) as err:
        module.fail_json(msg=str(err))
    if 200 in resp_status:
        module.exit_json(msg="Successfully fetched the job info", job_info=job_facts)
    else:
        module.fail_json(msg="Failed to fetch the job info")


if __name__ == '__main__':
    main()
