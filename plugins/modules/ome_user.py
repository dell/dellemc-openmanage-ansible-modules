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
module: ome_user
short_description: Create, modify or delete a user on OpenManage Enterprise
version_added: "2.0.0"
description: This module creates, modifies or deletes a user on OpenManage Enterprise.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  state:
    type: str
    description:
      - C(present) creates a user in case the I(UserName) provided inside I(attributes) does not exist.
      - C(present) modifies a user in case the I(UserName) provided inside I(attributes) exists.
      - C(absent) deletes an existing user.
    choices: [present, absent]
    default: present
  user_id:
    description:
      - Unique ID of the user to be deleted.
      - Either I(user_id) or I(name) is mandatory for C(absent) operation.
    type: int
  name:
    type: str
    description:
      - Unique Name of the user to be deleted.
      - Either I(user_id) or I(name) is mandatory for C(absent) operation.
  attributes:
    type: dict
    default: {}
    description:
      - >-
        Payload data for the user operations. It can take the following attributes for C(present).
      - >-
        UserTypeId, DirectoryServiceId, Description, Name, Password, UserName, RoleId, Locked, Enabled.
      - >-
        OME will throw error if required parameter is not provided for operation.
      - >-
        Refer OpenManage Enterprise API Reference Guide for more details.
requirements:
    - "python >= 3.9.6"
author: "Sajna Shetty(@Sajna-Shetty)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
    - This module does not support C(check_mode).
'''

EXAMPLES = r'''
---
- name: Create user with required parameters
  dellemc.openmanage.ome_user:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    attributes:
      UserName: "user1"
      Password: "UserPassword"
      RoleId: "10"
      Enabled: true

- name: Create user with all parameters
  dellemc.openmanage.ome_user:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    attributes:
      UserName: "user2"
      Description: "user2 description"
      Password: "UserPassword"
      RoleId: "10"
      Enabled: true
      DirectoryServiceId: 0
      UserTypeId: 1
      Locked: false
      Name: "user2"

- name: Modify existing user
  dellemc.openmanage.ome_user:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "present"
    attributes:
      UserName: "user3"
      RoleId: "10"
      Enabled: true
      Description: "Modify user Description"

- name: Delete existing user using id
  dellemc.openmanage.ome_user:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "absent"
    user_id: 1234

- name: Delete existing user using name
  dellemc.openmanage.ome_user:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "absent"
    name: "name"
'''

RETURN = r'''
---
msg:
  description: Overall status of the user operation.
  returned: always
  type: str
  sample: "Successfully created a User"
user_status:
  description: Details of the user operation, when I(state) is C(present).
  returned: When I(state) is C(present).
  type: dict
  sample:
    {
        "Description": "Test user creation",
        "DirectoryServiceId": 0,
        "Enabled": true,
        "Id": "61546",
        "IsBuiltin": false,
        "Locked": false,
        "Name": "test",
        "Password": null,
        "PlainTextPassword": null,
        "RoleId": "10",
        "UserName": "test",
        "UserTypeId": 1
    }
'''

import json
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


def _validate_inputs(module):
    """both user_id and name are not acceptable in case of state is absent"""
    state = module.params['state']
    user_id = module.params.get('user_id')
    name = module.params.get('name')
    if state != 'present' and (user_id is None and name is None):
        fail_module(module, msg="One of the following 'user_id' or 'name' "
                                "option is required for state 'absent'")


def get_user_id_from_name(rest_obj, name):
    """Get the account id using account name"""
    user_id = None
    if name is not None:
        resp = rest_obj.invoke_request('GET', 'AccountService/Accounts')
        if resp.success:
            for user in resp.json_data.get('value'):
                if 'UserName' in user and user['UserName'] == name:
                    return user['Id']
    return user_id


def _get_resource_parameters(module, rest_obj):
    state = module.params["state"]
    payload = module.params.get("attributes")
    if state == "present":
        name = payload.get('UserName')
        user_id = get_user_id_from_name(rest_obj, name)
        if user_id is not None:
            payload.update({"Id": user_id})
            path = "AccountService/Accounts('{user_id}')".format(user_id=user_id)
            method = 'PUT'
        else:
            path = "AccountService/Accounts"
            method = 'POST'
    else:
        user_id = module.params.get("user_id")
        if user_id is None:
            name = module.params.get('name')
            user_id = get_user_id_from_name(rest_obj, name)
            if user_id is None:
                fail_module(module, msg="Unable to get the account because the specified account "
                                        "does not exist in the system.")
        path = "AccountService/Accounts('{user_id}')".format(user_id=user_id)
        method = 'DELETE'
    return method, path, payload


def password_no_log(attributes):
    if isinstance(attributes, dict) and 'Password' in attributes:
        attributes['Password'] = "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"


def fail_module(module, **failmsg):
    password_no_log(module.params.get("attributes"))
    module.fail_json(**failmsg)


def exit_module(module, response, http_method):
    password_no_log(module.params.get("attributes"))
    msg_dict = {'POST': "Successfully created a User",
                'PUT': "Successfully modified a User",
                'DELETE': "Successfully deleted the User"}
    state_msg = msg_dict[http_method]
    if response.status_code != 204:
        module.exit_json(msg=state_msg, changed=True, user_status=response.json_data)
    else:
        # For delete operation no response content is returned
        module.exit_json(msg=state_msg, changed=True)


def main():
    specs = {
        "state": {"required": False, "type": 'str', "default": "present",
                  "choices": ['present', 'absent']},
        "user_id": {"required": False, "type": 'int'},
        "name": {"required": False, "type": 'str'},
        "attributes": {"required": False, "type": 'dict', "default": {}},
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[['user_id', 'name'], ],
        required_if=[['state', 'present', ['attributes']], ],
        supports_check_mode=False)

    try:
        _validate_inputs(module)
        with RestOME(module.params, req_session=True) as rest_obj:
            method, path, payload = _get_resource_parameters(module, rest_obj)
            resp = rest_obj.invoke_request(method, path, data=payload)
            if resp.success:
                exit_module(module, resp, method)
    except HTTPError as err:
        fail_module(module, msg=str(err), user_status=json.load(err))
    except (URLError, SSLValidationError, ConnectionError, TypeError, ValueError, OSError, SSLError) as err:
        fail_module(module, msg=str(err))


if __name__ == '__main__':
    main()
