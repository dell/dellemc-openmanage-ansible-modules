#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.3
# Copyright (C) 2020-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_firmware_baseline_info
short_description: Retrieves baseline details from OpenManage Enterprise
version_added: "2.0.0"
description:
   - This module retrieves the list and details of all the baselines on OpenManage Enterprise.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  baseline_name:
    description: Name of the baseline.If I(baseline_name) is not provided,
     all the available firmware baselines are returned.
    type: str
requirements:
    - "python >= 3.9.6"
author:
    - "Sajna Shetty(@Sajna-Shetty)"
    - "Mangirish Kenkare(@MangirishK)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Retrieve details of all the available firmware baselines
  dellemc.openmanage.ome_firmware_baseline_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"

- name: Retrieve details of a specific firmware baseline identified by its baseline name
  dellemc.openmanage.ome_firmware_baseline_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    baseline_name: "baseline_name"
'''

RETURN = r'''
---
msg:
  type: str
  description: Overall baseline information.
  returned: on error
  sample: "Successfully fetched firmware baseline information."
baseline_info:
  type: dict
  description: Details of the baselines.
  returned: success
  sample: {
        "@odata.id": "/api/UpdateService/Baselines(239)",
        "@odata.type": "#UpdateService.Baselines",
        "CatalogId": 22,
        "ComplianceSummary": {
            "ComplianceStatus": "CRITICAL",
            "NumberOfCritical": 1,
            "NumberOfDowngrade": 0,
            "NumberOfNormal": 0,
            "NumberOfWarning": 0
        },
        "Description": "baseline_description",
        "DeviceComplianceReports@odata.navigationLink": "/api/UpdateService/Baselines(239)/DeviceComplianceReports",
        "DowngradeEnabled": true,
        "Id": 239,
        "Is64Bit": true,
        "LastRun": "2020-05-22 16:42:40.307",
        "Name": "baseline_name",
        "RepositoryId": 12,
        "RepositoryName": "HTTP DELL",
        "RepositoryType": "DELL_ONLINE",
        "Targets": [
            {
                "Id": 10342,
                "Type": {
                    "Id": 1000,
                    "Name": "DEVICE"
                }
            }
        ],
        "TaskId": 41415,
        "TaskStatusId": 2060
    }
'''

import json
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError


def get_specific_baseline(module, baseline_name, resp_data):
    """Get specific baseline."""
    baseline = None
    for each in resp_data["value"]:
        if each['Name'] == baseline_name:
            baseline = each
            break
    else:
        module.exit_json(msg="Unable to complete the operation because the requested baseline"
                             " with name '{0}' does not exist.".format(baseline_name), baseline_info=[])
    return baseline


def main():
    specs = {
        "baseline_name": {"type": 'str', "required": False},
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=False) as rest_obj:
            baseline_name = module.params.get("baseline_name")
            resp = rest_obj.invoke_request('GET', "UpdateService/Baselines")
            data = resp.json_data
            if len(data["value"]) == 0 and not baseline_name:
                module.exit_json(msg="No baselines present.", baseline_info=[])
            if baseline_name is not None:
                data = get_specific_baseline(module, baseline_name, data)
            module.exit_json(msg="Successfully fetched firmware baseline information.", baseline_info=data)
    except HTTPError as err:
        if err.getcode() == 404:
            module.exit_json(msg="404 Not Found.The requested resource is not available.", failed=True)
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
