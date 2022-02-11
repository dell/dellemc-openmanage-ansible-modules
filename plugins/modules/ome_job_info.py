#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.0.1
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

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
    - "python >= 3.8.6"
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
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params
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
    specs = {
        "job_id": {"required": False, "type": 'int'},
        "system_query_options": {"required": False, "type": 'dict', "options": {
            "top": {"type": 'int', "required": False},
            "skip": {"type": 'int', "required": False},
            "filter": {"type": 'str', "required": False},
        }},
    }
    specs.update(ome_auth_params)
    module = AnsibleModule(
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
    except (SSLValidationError, ConnectionError, TypeError, ValueError, SSLError, OSError) as err:
        module.fail_json(msg=str(err))
    if 200 in resp_status:
        module.exit_json(msg="Successfully fetched the job info", job_info=job_facts)
    else:
        module.fail_json(msg="Failed to fetch the job info")


if __name__ == '__main__':
    main()
