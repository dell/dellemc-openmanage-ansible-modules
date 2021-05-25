#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.3.0
# Copyright (C) 2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: ome_device_group
short_description: Manages device group settings on OpenManage Enterprise
version_added: "3.3.0"
description: This module allows to add devices to a device group on OpenManage Enterprise.
extends_documentation_fragment:
  - dellemc.openmanage.oment_auth_options
options:
  state:
    type: str
    description:
      - C(present) allows to add the device(s) to a device group.
      - C(absent) currently, this feature is not supported.
    choices: [present, absent]
    default: present
  name:
    type: str
    required: True
    description: Name of the group to which device(s) need to be added.
  device_ids:
    type: list
    elements: int
    description:
      - List of device ID(s) of the device(s) to be added to the device group.
      - I(device_ids) is mutually exclusive with I(device_service_tags).
  device_service_tags:
    type: list
    elements: str
    description:
      - List of device service tag(s) of the device(s) to be added to the device group.
      - I(device_service_tags) is mutually exclusive with I(device_ids).
requirements:
  - "python >= 2.7.5"
author: "Felix Stephen (@felixs88)"
notes:
  - Run this module from a system that has direct access to DellEMC OpenManage Enterprise.
  - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Adding a set of devices to a group using device ids
  dellemc.openmanage.ome_device_group:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    name: "Storage Services"
    device_ids:
      - 11111
      - 11112
      - 11113

- name: Adding a set of devices to a group using device service tags
  dellemc.openmanage.ome_device_group:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    name: "Storage Services"
    device_service_tags:
      - GHRT2RL
      - KJHDF3S
      - LKIJNG6
"""

RETURN = """
---
msg:
  type: str
  description: Overall status of the device group settings.
  returned: always
  sample: "Successfully added member(s) to the device group."
group_id:
  type: int
  description: ID of the group.
  returned: success
  sample: 21078
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
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


GROUP_URI = "GroupService/Groups"
DEVICE_URI = "DeviceService/Devices"
ADD_MEMBER_URI = "GroupService/Actions/GroupService.AddMemberDevices"


def get_group_id(rest_obj, module):
    group_name = module.params["name"]
    group_resp = rest_obj.invoke_request("GET", GROUP_URI,
                                         query_param={"$filter": "Name eq '{0}'".format(group_name)})
    if not group_resp.json_data.get("value"):
        module.fail_json(msg="Unable to complete the operation because the entered "
                             "target group name '{0}' is invalid.".format(group_name))
    system_groups = group_resp.json_data.get("value")[0]["CreatedBy"]
    if system_groups == "system":
        module.fail_json(msg="Devices cannot be added to the default groups created by OpenManage Enterprise.")
    group_id = group_resp.json_data.get("value")[0]["Id"]
    return group_id


def get_device_id(rest_obj, module):
    device_id_list = module.params.get("device_ids")
    device_tag_list = module.params.get("device_service_tags")
    device_list = rest_obj.get_all_report_details(DEVICE_URI)
    invalid, each_device_list, each_tag_to_id, key = [], [], [], None
    if device_id_list:
        key = "Id"
        each_device_list = device_id_list
    elif device_tag_list:
        key = "DeviceServiceTag"
        each_device_list = device_tag_list

    for each in each_device_list:
        each_device = list(filter(lambda d: d[key] in [each], device_list["report_list"]))
        if key == "DeviceServiceTag" and each_device:
            each_tag_to_id.append(each_device[0]["Id"])
        if not each_device:
            invalid.append(str(each))
    if invalid:
        value = "id" if key == "Id" else "service tag"
        module.fail_json(msg="Unable to complete the operation because the entered "
                             "target device {0}(s) '{1}' are invalid.".format(value, ",".join(set(invalid))))
    if each_tag_to_id:
        each_device_list = each_tag_to_id
    return each_device_list, key


def add_member_to_group(module, rest_obj, group_id, device_id, key):
    group_device = rest_obj.get_all_report_details("{0}({1})/Devices".format(GROUP_URI, group_id))
    device_exists, device_not_exists = [], []
    for each in device_id:
        each_device = list(filter(lambda d: d["Id"] in [each], group_device["report_list"]))
        if each_device:
            tag_or_id = each_device[0][key] if key == "DeviceServiceTag" else each
            device_exists.append(str(tag_or_id))
        else:
            device_not_exists.append(each)

    if module.check_mode and device_not_exists:
        module.exit_json(msg="Changes found to commit!", changed=True, group_id=group_id)
    elif module.check_mode and not device_not_exists:
        module.exit_json(msg="No changes found to commit!", group_id=group_id)

    if device_exists and not device_not_exists:
        module.exit_json(
            msg="Requested device(s) '{0}' are already present in the group.".format(",".join(set(device_exists))),
            group_id=group_id
        )
    payload = {"GroupId": group_id, "MemberDeviceIds": device_not_exists}
    response = rest_obj.invoke_request("POST", ADD_MEMBER_URI, data=payload)
    return response


def main():
    module = AnsibleModule(
        argument_spec={
            "hostname": {"required": True, "type": "str"},
            "username": {"required": True, "type": "str"},
            "password": {"required": True, "type": "str", "no_log": True},
            "port": {"required": False, "type": "int", "default": 443},
            "name": {"required": True, "type": "str"},
            "state": {"required": False, "type": "str", "choices": ["present", "absent"], "default": "present"},
            "device_service_tags": {"required": False, "type": "list", "elements": 'str'},
            "device_ids": {"required": False, "type": "list", "elements": 'int'},
        },
        required_if=(
            ("state", "present", ("device_ids", "device_service_tags"), True),
        ),
        mutually_exclusive=(
            ("device_ids", "device_service_tags"),
        ),
        supports_check_mode=True
    )

    try:
        if module.params.get("device_ids") is None and module.params.get("device_service_tags") is None:
            module.fail_json(msg="state is present but the device_ids|device_service_tags value is missing.")
        with RestOME(module.params, req_session=True) as rest_obj:
            group_id = get_group_id(rest_obj, module)
            device_id, key = get_device_id(rest_obj, module)
            if module.params["state"] == "present":
                response = add_member_to_group(module, rest_obj, group_id, device_id, key)
                if response.status_code == 204:
                    module.exit_json(msg="Successfully added member(s) to the device group.",
                                     group_id=group_id, changed=True)
            elif module.params["state"] == "absent":
                module.fail_json(msg="Currently, this feature is not supported.")
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, AttributeError,
            IndexError, KeyError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
