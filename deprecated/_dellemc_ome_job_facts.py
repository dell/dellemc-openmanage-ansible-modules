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
module: dellemc_ome_job_facts
short_description: Get job details for a given job ID or entire job queue.
version_added: "2.9"
deprecated:
  removed_in: "2.13"
  why: Replaced with M(ome_job_info).
  alternative: Use M(ome_job_info) instead.
description: This module retrieves job details for a given job ID or entire job queue.
options:
  hostname:
    description: Target IP Address or hostname.
    type: str
    required: true
  username:
    description: Target username.
    type: str
    required: true
  password:
    description: Target user password.
    type: str
    required: true
  port:
    description: Target HTTPS port.
    type: int
    default: 443
  job_id:
    description: Unique ID of the job
    type: int
  system_query_options:
    description: Options for pagination of the output
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

'''

EXAMPLES = r'''
---
- name: Get all jobs details.
  dellemc_ome_job_facts:
    hostname:  "192.168.0.1"
    username: "username"
    password:  "password"

- name: Get job details for id.
  dellemc_ome_job_facts:
    hostname:  "192.168.0.1"
    username: "username"
    password:  "password"
    job_id: 12345

- name: Get filtered job details.
  dellemc_ome_job_facts:
    hostname:  "192.168.0.1"
    username: "username"
    password:  "password"
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
job_facts:
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
from ansible.module_utils.remote_management.dellemc.ome import RestOME
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


def _get_query_parameters(module_params):
    """Builds query parameter

    :returns: dictionary, which builds the query format
     eg : {"$filter": "JobType/Id eq 8"}
     """
    system_query_options_param = module_params.get("system_query_options")
    query_parameter = {}
    if system_query_options_param:
        query_parameter = {'$' + k: v for k, v in system_query_options_param.items() if v is not None}
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
        supports_check_mode=False
    )
    module.deprecate("The 'dellemc_ome_job_facts' module has been deprecated. "
                     "Use 'ome_job_info' instead",
                     version=2.13)
    joburi = "JobService/Jobs"
    resp = None
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            if module.params.get("job_id") is not None:
                # Fetch specific job
                job_id = module.params.get("job_id")
                jpath = "{0}({1})".format(joburi, job_id)
                query_param = None
            else:
                # Fetch all jobs, filter and pagination options
                # query applicable only for all jobs list fetching
                query_param = _get_query_parameters(module.params)
                jpath = joburi
            resp = rest_obj.invoke_request('GET', jpath, query_param=query_param)
            job_facts = resp.json_data
    except HTTPError as httperr:
        module.fail_json(msg=str(httperr), job_facts=json.load(httperr))
    except (URLError, SSLValidationError, ConnectionError, TypeError, ValueError) as err:
        module.fail_json(msg=str(err))

    # check for 200 status as GET only returns this for success
    if resp and resp.status_code == 200:
        module.exit_json(msg="Successfully fetched the job facts", job_facts=job_facts)
    else:
        module.fail_json(msg="Failed to fetch the job facts")


if __name__ == '__main__':
    main()
