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
module: ome_firmware_baseline
short_description: Create a firmware baseline on OpenManage Enterprise
version_added: "2.0.0"
description: This module creates a baseline on OpenManage Enterprise.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  baseline_name:
    type: str
    required: true
    description:
      - Name for the baseline being created.
  baseline_description:
    type: str
    description:
      - Description for the baseline being created.
  catalog_name:
    type: str
    description:
      - Name of the catalog associated with the baseline.
  downgrade_enabled:
    type: bool
    description:
      - Indicates if a downgrade is allowed or not.
    default: True
  is_64_bit:
    type: bool
    description:
      - Indicate if 64 bit is supported.
    default: True
  device_ids:
    type: list
    elements: int
    description:
      - List of device ids.
      - I(device_ids) is mutually exclusive with I(device_service_tags) and I(device_group_names).
  device_service_tags:
    type: list
    elements: str
    description:
      - List of service tags.
      - I(device_service_tags) is mutually exclusive with I(device_ids) and I(device_group_names).
  device_group_names:
    type: list
    elements: str
    description:
      - List of group names.
      - I(device_group_names) is mutually exclusive with I(device_ids) and I(device_service_tags).
requirements:
    - "python >= 2.7.5"
author: "Jagadeesh N V(@jagadeeshnv)"
notes:
    - Run this module from a system that has direct access to DellEMC OpenManage Enterprise.
    - This module does not support C(check_mode).
'''

EXAMPLES = r'''
---
- name: Create baseline for device Ids
  dellemc.openmanage.ome_firmware_baseline:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    baseline_name: "baseline_name"
    baseline_description: "baseline_description"
    catalog_name: "catalog_name"
    device_ids:
      - 1010
      - 2020

- name: Create baseline for servicetags
  dellemc.openmanage.ome_firmware_baseline:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    baseline_name: "baseline_name"
    baseline_description: "baseline_description"
    catalog_name: "catalog_name"
    device_service_tags:
      - "SVCTAG1"
      - "SVCTAG2"

- name: Create baseline for device groups
  dellemc.openmanage.ome_firmware_baseline:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    baseline_name: "baseline_name"
    baseline_description: "baseline_description"
    catalog_name: "catalog_name"
    device_group_names:
      - "Group1"
      - "Group2"
'''

RETURN = r'''
---
msg:
  description: Overall status of the firmware baseline creation.
  returned: always
  type: str
  sample: "Successfully created task for creating Baseline"
baseline_status:
  description: Details of the baseline status.
  returned: success
  type: dict
  sample: {
    "CatalogId": 123,
    "Description": "BASELINE DESCRIPTION",
    "DeviceComplianceReports": [],
    "DowngradeEnabled": true,
    "Id": 0,
    "Is64Bit": true,
    "Name": "my_baseline",
    "RepositoryId": 123,
    "RepositoryName": "catalog123",
    "RepositoryType": "HTTP",
    "Targets": [
        {
            "Id": 10083,
            "Type": {
                "Id": 1000,
                "Name": "DEVICE"
            }
        },
        {
            "Id": 10076,
            "Type": {
                "Id": 1000,
                "Name": "DEVICE"
            }
        }
    ],
    "TaskId": 11235,
    "TaskStatusId": 0
  }
error_info:
  type: dict
  description: Details of http error.
  returned: on http error
  sample:  {
        "error": {
            "@Message.ExtendedInfo": [
                {
                    "Message": "Unable to retrieve baseline list either because the device ID(s) entered are invalid",
                    "Resolution": "Make sure the entered device ID(s) are valid and retry the operation.",
                    "Severity": "Critical"
                }
            ],
            "code": "Base.1.0.GeneralError",
            "message": "A general error has occurred. See ExtendedInfo for more information."
        }
    }
'''

import json
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


def get_catrepo_ids(cat_name, rest_obj):
    if cat_name is not None:
        resp = rest_obj.invoke_request('GET', 'UpdateService/Catalogs')
        if resp.success:
            for catalog in resp.json_data.get('value', []):
                repo = catalog.get("Repository")
                if repo.get("Name") == cat_name:
                    return catalog.get("Id"), repo.get("Id")
    return None, None


def get_dev_ids(module, rest_obj, param, devkey):
    paramlist = module.params[param]
    resp = rest_obj.invoke_request('GET', "DeviceService/Devices")
    targets = []
    if resp.success:
        devlist = resp.json_data['value']
        device_resp = dict([(device[devkey], device) for device in devlist])
        for st in paramlist:
            if st in device_resp:
                djson = device_resp[st]
                target = {}
                device_type = {}
                device_type['Id'] = djson['Type']
                device_type['Name'] = "DEVICE"
                target['Id'] = djson['Id']
                target['Type'] = device_type
                targets.append(target)
            else:
                module.fail_json(msg="Unable to complete the operation because the entered target"
                                     " {0} '{1}' is invalid.".format(devkey, st))
    return targets


def get_group_ids(module, rest_obj):
    grp_name_list = module.params.get("device_group_names")
    resp = rest_obj.invoke_request('GET', "GroupService/Groups")
    targets = []
    if resp.success:
        grplist = resp.json_data['value']
        device_resp = dict([(str(grp['Name']), grp) for grp in grplist])
        for st in grp_name_list:
            if st in device_resp:
                djson = device_resp[st]
                target = {}
                device_type = {}
                device_type['Id'] = djson['TypeId']
                device_type['Name'] = "GROUP"
                target['Id'] = djson['Id']
                target['Type'] = device_type
                targets.append(target)
            else:
                module.fail_json(msg="Unable to complete the operation because the entered target"
                                     " Group Name '{0}' is invalid.".format(st))
    return targets


def get_target_list(module, rest_obj):
    target_list = None
    if module.params.get("device_service_tags"):
        target_list = get_dev_ids(module, rest_obj, "device_service_tags", "DeviceServiceTag")
    elif module.params.get("device_group_names"):
        target_list = get_group_ids(module, rest_obj)
    elif module.params.get("device_ids"):
        target_list = get_dev_ids(module, rest_obj, "device_ids", "Id")
    return target_list


def _get_baseline_payload(module, rest_obj):
    cat_name = module.params.get("catalog_name")
    cat_id, repo_id = get_catrepo_ids(cat_name, rest_obj)
    if cat_id is None or repo_id is None:
        module.fail_json(msg="No Catalog with name {0} found".format(cat_name))
    targets = get_target_list(module, rest_obj)
    if targets is None:
        module.fail_json(msg="No Targets specified")
    baseline_name = module.params.get("baseline_name")  # + time.strftime(":%Y:%m:%d-%H:%M:%S")#DEBUG
    baseline_payload = {
        "Name": baseline_name,
        # "Description": baseline_desc,
        "CatalogId": cat_id,
        "RepositoryId": repo_id,
        # "DowngradeEnabled": module.params.get("downgrade_enabled"),
        # "Is64Bit": module.params.get("is_64_bit"),
        "Targets": targets
    }
    # module.exit_json(debug=module.params)
    if module.params.get("baseline_description") is not None:
        baseline_payload['Description'] = module.params.get("baseline_description")
    if module.params.get("downgrade_enabled") is not None:
        baseline_payload['DowngradeEnabled'] = module.params.get("downgrade_enabled")
    if module.params.get("is_64_bit") is not None:
        baseline_payload['Is64Bit'] = module.params.get("is_64_bit")

    return baseline_payload


def main():
    module = AnsibleModule(
        argument_spec={
            "hostname": {"required": True, "type": 'str'},
            "username": {"required": True, "type": 'str'},
            "password": {"required": True, "type": 'str', "no_log": True},
            "port": {"required": False, "default": 443, "type": 'int'},
            # "state": {"required": False, "default": "present",
            #           "choices": ['present', 'absent']},
            "baseline_name": {"required": True, "type": 'str'},
            "baseline_description": {"required": False, "type": 'str'},
            "catalog_name": {"required": False, "type": 'str'},
            "downgrade_enabled": {"required": False, "type": 'bool', "default": True},
            "is_64_bit": {"required": False, "type": 'bool', "default": True},
            "device_ids": {"required": False, "type": 'list', "elements": 'int'},
            "device_service_tags": {"required": False, "type": 'list', "elements": 'str'},
            "device_group_names": {"required": False, "type": 'list', "elements": 'str'},
        },
        mutually_exclusive=[
            ('device_ids', 'device_service_tags', 'device_group_names')
        ],
        # required_if=[['state', 'present', ['device_id', 'device_service_tags', 'group_name']]],
        supports_check_mode=False)

    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            myparams = module.params
            if not any([myparams.get("device_ids"), myparams.get("device_service_tags"),
                        myparams.get("device_group_names")]):
                module.fail_json(msg="No Targets Specified for baseline creation")
            payload = _get_baseline_payload(module, rest_obj)
            resp = rest_obj.invoke_request("POST", "UpdateService/Baselines", data=payload)
            if resp.success:
                module.exit_json(changed=True, msg="Successfully created task for creating Baseline",
                                 baseline_status=resp.json_data)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except (URLError, SSLValidationError, SSLError, ConnectionError, TypeError, ValueError, KeyError) as err:
        module.fail_json(msg=str(err))
    module.fail_json(msg="Failed to perform baseline operation, no response received from host")


if __name__ == '__main__':
    main()
