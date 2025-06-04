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

DOCUMENTATION = """
---
module: ome_groups
short_description: Manages static device groups on OpenManage Enterprise
description: This module allows to create, modify, and delete static device groups on OpenManage Enterprise.
version_added: "3.5.0"
author:
  - Jagadeesh N V(@jagadeeshnv)
extends_documentation_fragment:
  - dellemc.openmanage.oment_auth_options
options:
  state:
    type: str
    description:
      - C(present) allows to create or modify a device group.
      - C(absent) allows to delete a device group.
    choices: [present, absent]
    default: present
  name:
    type: list
    elements: str
    description:
      - Name of the device group to be created, modified, or deleted.
      - If I(state) is absent, multiple names can be provided.
      - This option is case insensitive.
      - This option is mutually exclusive with I(group_id).
  group_id:
    type: list
    elements: int
    description:
      - ID of the device group to be created, modified, or deleted.
      - If I(state) is absent, multiple IDs can be provided.
      - This option is mutually exclusive with I(name).
  new_name:
    type: str
    description:
      - New name for the existing device group.
      - This is applicable only when I(state) is C(present).
  description:
    type: str
    description:
      - Description for the device group.
      - This is applicable only when I(state) is C(present).
  parent_group_name:
    type: str
    default: "Static Groups"
    description:
      - Name of the parent device group under which the device group to be created or modified.
      - This is applicable only when I(state) is C(present).
      - C(NOTE) If device group with such a name does not exist, device group with I(parent_group_name) is created.
      - This option is case insensitive.
      - This option is mutually exclusive with I(parent_group_id).
  parent_group_id:
    type: int
    description:
      - ID of the parent device group under which the device group to be created or modified.
      - This is applicable only when I(state) is C(present).
      - This option is mutually exclusive with I(parent_group_name).
requirements:
  - "python >= 3.9.6"
notes:
  - This module manages only static device groups on Dell OpenManage Enterprise.
  - If a device group with the name I(parent_group_name) does not exist, a new device group with the same name is created.
  - Make sure the entered parent group is not the descendant of the provided group.
  - Run this module from a system that has direct access to Dell OpenManage Enterprise.
  - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Create a new device group
  dellemc.openmanage.ome_groups:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    name: "group 1"
    description: "Group 1 description"
    parent_group_name: "group parent 1"

- name: Modify a device group using the group ID
  dellemc.openmanage.ome_groups:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    group_id: 1234
    description: "Group description updated"
    parent_group_name: "group parent 2"

- name: Delete a device group using the device group name
  dellemc.openmanage.ome_groups:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: absent
    name: "group 1"

- name: Delete multiple device groups using the group IDs
  dellemc.openmanage.ome_groups:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: absent
    group_id:
      - 1234
      - 5678
"""

RETURN = """
---
msg:
  type: str
  description: Overall status of the device group operation.
  returned: always
  sample: "Successfully deleted the device group(s)."
group_status:
  description: Details of the device group operation status.
  returned: success
  type: dict
  sample: {
    "Description": "my group description",
    "Id": 12123,
    "MembershipTypeId": 12,
    "Name": "group 1",
    "ParentId": 12345,
    "TypeId": 3000,
    "IdOwner": 30,
    "CreatedBy": "admin",
    "CreationTime": "2021-01-01 10:10:10.100",
    "DefinitionDescription": "UserDefined",
    "DefinitionId": 400,
    "GlobalStatus": 5000,
    "HasAttributes": false,
    "UpdatedBy": "",
    "UpdatedTime": "2021-01-01 11:11:10.100",
    "Visible": true
  }
group_ids:
  type: list
  elements: int
  description: List of the deleted device group IDs.
  returned: when I(state) is C(absent)
  sample: [1234, 5678]
invalid_groups:
  type: list
  elements: str
  description: List of the invalid device group IDs or names.
  returned: when I(state) is C(absent)
  sample: [1234, 5678]
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
                "MessageId": "CGRP9013",
                "RelatedProperties": [],
                "Message": "Unable to update group  12345  with the provided parent  54321  because a group/parent
                relationship already exists.",
                "MessageArgs": [
                    "12345",
                    "54321"
                ],
                "Severity": "Warning",
                "Resolution": "Make sure the entered parent ID does not create a bidirectional relationship and retry
                the operation."
            }
        ]
    }
}
"""

import json
import time
from ssl import SSLError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule

GROUP_URI = "GroupService/Groups"
OP_URI = "GroupService/Actions/GroupService.{op}Group"
# GROUPS_HIERARCHY = "GroupService/AllGroupsHierarchy"
MULTIPLE_GROUPS_MSG = "Provide only one unique device group when state is present."
NONEXIST_GROUP_ID = "A device group with the provided ID does not exist."
NONEXIST_PARENT_ID = "A parent device group with the provided ID does not exist."
INVALID_PARENT = "The provided parent device group is not a valid user-defined static device group."
INVALID_GROUPS_DELETE = "Provide valid static device group(s) for deletion."
INVALID_GROUPS_MODIFY = "Provide valid static device group for modification."
PARENT_CREATION_FAILED = "Unable to create a parent device group with the name {pname}."
CREATE_SUCCESS = "Successfully {op}d the device group."
GROUP_PARENT_SAME = "Provided parent and the device group cannot be the same."
GROUP_NAME_EXISTS = "Unable to rename the group because a group with the provided name '{gname}' already exists."
DELETE_SUCCESS = "Successfully deleted the device group(s)."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
STATIC_ROOT = 'Static Groups'
SETTLING_TIME = 2


def get_valid_groups(module, rest_obj, group_arg, group_set):
    parent = {}
    static_root = {}
    group_dict = {}
    group_resp = rest_obj.get_all_items_with_pagination(GROUP_URI)
    if module.params.get('state') == 'absent':
        group_dict = dict([(str(g[group_arg]).lower(), g) for g in group_resp.get("value")
                           if str(g[group_arg]).lower() in group_set])
    else:
        parg = module.params.get('parent_group_id')
        if parg:  # Checking id first as name has a default value
            pkey = 'Id'
        else:
            pkey = 'Name'
            parg = module.params.get('parent_group_name')
        count = 0
        for g in group_resp.get("value"):
            if str(g[group_arg]).lower() in group_set:
                group_dict = g
                count = count + 1
            if str(g[pkey]).lower() == str(parg).lower():
                parent = g
                count = count + 1
            if g['Name'] == STATIC_ROOT:
                static_root = g
                count = count + 1
            if count == 3:
                break
    return group_dict, parent, static_root


def is_valid_static_group(grp):
    if grp['TypeId'] == 3000 and grp['MembershipTypeId'] == 12:
        return True
    return False


def create_parent(rest_obj, module, static_root):
    try:
        prt = static_root
        payload = {}
        payload['MembershipTypeId'] = 12  # Static members
        payload['Name'] = module.params.get('parent_group_name')
        payload['ParentId'] = prt['Id']
        prt_resp = rest_obj.invoke_request('POST', OP_URI.format(op='Create'), data={"GroupModel": payload})
        return int(prt_resp.json_data)
    except Exception:
        return static_root['Id']


def get_parent_id(rest_obj, module, parent, static_root):
    parent_id = module.params.get("parent_group_id")
    if parent_id:  # Checking id first as name has a default value
        if not parent:
            module.fail_json(msg=NONEXIST_PARENT_ID)
        if parent['Name'] != STATIC_ROOT:
            if not is_valid_static_group(parent):
                module.fail_json(msg=INVALID_PARENT)
        return parent['Id']
    else:
        if parent:
            if parent['Name'] != STATIC_ROOT:
                if not is_valid_static_group(parent):
                    module.fail_json(msg=INVALID_PARENT)
            return parent['Id']
        else:
            if module.check_mode:
                return 0
            else:
                prtid = create_parent(rest_obj, module, static_root)
                time.sleep(SETTLING_TIME)
                return prtid
    return static_root['Id']


def get_ome_group_by_name(rest_obj, name):
    grp = {}
    try:
        resp = rest_obj.invoke_request("GET", GROUP_URI, query_param={"$filter": "Name eq '{0}'".format(name)})
        group_resp = resp.json_data.get('value')
        if group_resp:
            grp = group_resp[0]
    except Exception:
        grp = {}
    return grp


def get_ome_group_by_id(rest_obj, id):
    grp = {}
    try:
        resp = rest_obj.invoke_request('GET', GROUP_URI + "({0})".format(id))
        grp = resp.json_data
    except Exception:
        grp = {}
    return grp


def exit_group_operation(module, rest_obj, payload, operation):
    group_resp = rest_obj.invoke_request('POST', OP_URI.format(op=operation), data={"GroupModel": payload})
    cid = int(group_resp.json_data)
    time.sleep(SETTLING_TIME)
    try:
        grp = get_ome_group_by_id(rest_obj, cid)
        group = rest_obj.strip_substr_dict(grp)
    except Exception:
        payload['Id'] = cid
        group = payload
    module.exit_json(changed=True, msg=CREATE_SUCCESS.format(op=operation.lower()), group_status=group)


def create_group(rest_obj, module, parent, static_root):
    payload = {}
    payload['MembershipTypeId'] = 12  # Static members
    mparams = module.params
    payload['Name'] = mparams.get('name')[0]
    if mparams.get('parent_group_name').lower() == payload['Name'].lower():
        module.fail_json(msg=GROUP_PARENT_SAME)
    parent_id = get_parent_id(rest_obj, module, parent, static_root)
    payload['ParentId'] = parent_id
    if mparams.get('description'):
        payload['Description'] = mparams.get('description')
    if module.check_mode:
        module.exit_json(changed=True, msg=CHANGES_FOUND)
    exit_group_operation(module, rest_obj, payload, 'Create')


def modify_group(rest_obj, module, valid_group_dict, parent, static_root):
    if not is_valid_static_group(valid_group_dict):
        module.fail_json(msg=INVALID_GROUPS_MODIFY)
    grp = valid_group_dict
    diff = 0
    payload = dict([(k, grp.get(k)) for k in ["Name", "Description", "MembershipTypeId", "ParentId", "Id"]])
    new_name = module.params.get('new_name')
    if new_name:
        if new_name != payload['Name']:
            dup_grp = get_ome_group_by_name(rest_obj, new_name)
            if dup_grp:
                module.fail_json(msg=GROUP_NAME_EXISTS.format(gname=new_name))
            payload['Name'] = new_name
            diff += 1
    desc = module.params.get('description')
    if desc:
        if desc != payload['Description']:
            payload['Description'] = desc
            diff += 1
    parent_id = get_parent_id(rest_obj, module, parent, static_root)
    if parent_id == payload['Id']:
        module.fail_json(msg=GROUP_PARENT_SAME)
    if parent_id != payload['ParentId']:
        payload['ParentId'] = parent_id
        diff += 1
    if diff == 0:
        gs = rest_obj.strip_substr_dict(grp)
        module.exit_json(msg=NO_CHANGES_MSG, group_status=gs)
    if module.check_mode:
        module.exit_json(changed=True, msg=CHANGES_FOUND)
    exit_group_operation(module, rest_obj, payload, 'Update')


def delete_groups(rest_obj, module, group_set, group_dict):
    deletables = []
    invalids = []
    for g in group_set:
        grp = group_dict.get(str(g).lower())
        if grp:
            if is_valid_static_group(grp):  # For Query Groups MembershipTypeId = 24
                deletables.append(grp['Id'])
            else:
                invalids.append(g)
    if invalids:
        module.fail_json(msg=INVALID_GROUPS_DELETE, invalid_groups=invalids)
    if module.check_mode:
        module.exit_json(changed=True, msg=CHANGES_FOUND, group_ids=deletables)
    rest_obj.invoke_request("POST", OP_URI.format(op='Delete'), data={"GroupIds": deletables})
    module.exit_json(changed=True, msg=DELETE_SUCCESS, group_ids=deletables)


def main():
    specs = {
        "name": {"type": "list", "elements": 'str'},
        "group_id": {"type": "list", "elements": 'int'},
        "state": {"type": "str", "choices": ["present", "absent"], "default": "present"},
        "description": {"type": "str"},
        "new_name": {"type": "str"},
        "parent_group_name": {"type": "str", "default": STATIC_ROOT},
        "parent_group_id": {"type": "int"},
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        required_if=[
            ["state", "present", ("new_name", "description", "parent_group_name", "parent_group_id"), True],
        ],
        mutually_exclusive=[
            ("name", "group_id"), ("parent_group_name", "parent_group_id"),
        ],
        required_one_of=[("name", "group_id")],
        supports_check_mode=True
    )

    try:
        if module.params.get('name'):
            group_arg = 'Name'
            group_set = set(v.lower() for v in module.params.get('name'))
        else:
            group_arg = 'Id'
            group_set = set(str(v).lower() for v in module.params.get('group_id'))
        if len(group_set) != 1 and module.params['state'] == 'present':
            module.fail_json(msg=MULTIPLE_GROUPS_MSG)
        with RestOME(module.params, req_session=True) as rest_obj:
            valid_group_dict, parent, static_root = get_valid_groups(module, rest_obj, group_arg, group_set)
            if module.params["state"] == "absent":
                if valid_group_dict:
                    delete_groups(rest_obj, module, group_set, valid_group_dict)
                module.exit_json(msg=NO_CHANGES_MSG)
            else:
                if valid_group_dict:
                    modify_group(rest_obj, module, valid_group_dict, parent, static_root)
                elif group_arg == 'Id':
                    module.fail_json(msg=NONEXIST_GROUP_ID)
                create_group(rest_obj, module, parent, static_root)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, AttributeError, IndexError, KeyError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
