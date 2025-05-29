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
module: ome_domain_user_groups
short_description: Create, modify, or delete an Active Directory/LDAP user group on
  OpenManage Enterprise and OpenManage Enterprise Modular
version_added: "4.0.0"
description: This module allows to create, modify, or delete an Active Directory/LDAP user group on
  OpenManage Enterprise and OpenManage Enterprise Modular.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  state:
    type: str
    description:
      - C(present) imports or modifies the Active Directory/LDAP user group.
      - C(absent) deletes an existing Active Directory/LDAP user group.
    choices: [present, absent]
    default: present
  group_name:
    type: str
    required: true
    description:
      - The desired Active Directory/LDAP user group name to be imported or removed.
      - "Examples for user group name: Administrator or Account Operators or Access Control Assistance Operator."
      - I(group_name) value is case insensitive.
  role:
    type: str
    description:
      - The desired roles and privilege for the imported Active Directory/LDAP user group.
      - "OpenManage Enterprise Modular Roles: CHASSIS ADMINISTRATOR, COMPUTE MANAGER, STORAGE MANAGER,
        FABRIC MANAGER, VIEWER."
      - "OpenManage Enterprise Roles: ADMINISTRATOR, DEVICE MANAGER, VIEWER."
      - I(role) value is case insensitive.
  directory_name:
    type: str
    description:
      - The directory name set while adding the Active Directory/LDAP.
      - I(directory_name) is mutually exclusive with I(directory_id).
  directory_type:
    type: str
    description:
      - Type of the account.
    choices: ['AD', 'LDAP']
    default: 'AD'
  directory_id:
    type: int
    description:
      - The ID of the Active Directory/LDAP.
      - I(directory_id) is mutually exclusive with I(directory_name).
  domain_username:
    type: str
    description:
      - Active Directory/LDAP domain username.
      - "Example: username@domain or domain\\username."
  domain_password:
    type: str
    description:
      - Active Directory/LDAP domain password.
requirements:
  - "python >= 3.9.6"
author:
  - "Felix Stephen (@felixs88)"
  - "Abhishek Sinha (@Abhishek-Dell)"
notes:
  - This module supports C(check_mode) and idempotency.
  - Run this module from a system that has direct access to OpenManage Enterprise
    or OpenManage Enterprise Modular.
"""

EXAMPLES = r"""
---
- name: Create Active Directory user group
  dellemc.openmanage.ome_domain_user_groups:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: present
    group_name: account operators
    directory_name: directory_name
    role: administrator
    domain_username: username@domain
    domain_password: domain_password

- name: Update Active Directory user group
  dellemc.openmanage.ome_domain_user_groups:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: present
    group_name: account operators
    role: viewer

- name: Delete active directory user group
  dellemc.openmanage.ome_domain_user_groups:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: absent
    group_name: administrators

- name: Import LDAP directory group.
  dellemc.openmanage.ome_domain_user_groups:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    directory_type: LDAP
    state: present
    group_name: account operators
    directory_name: directory_name
    role: administrator
    domain_username: username@domain
    domain_password: domain_password

- name: Remove LDAP directory group.
  dellemc.openmanage.ome_domain_user_groups:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: absent
    group_name: account operators
"""

RETURN = r"""
---
msg:
  type: str
  description: Overall status of the Active Directory/LDAP user group operation.
  returned: always
  sample: Successfully imported the Active Directory/LDAP user group.
domain_user_status:
  description: Details of the domain user operation, when I(state) is C(present).
  returned: When I(state) is C(present).
  type: dict
  sample: {
    "Description": null,
    "DirectoryServiceId": 16097,
    "Enabled": true,
    "Id": "16617",
    "IsBuiltin": false,
    "IsVisible": true,
    "Locked": false,
    "Name": "Account Operators",
    "ObjectGuid": "a491859c-031e-42a3-ae5e-0ab148ecf1d6",
    "ObjectSid": null,
    "Oem": null,
    "Password": null,
    "PlainTextPassword": null,
    "RoleId": "16",
    "UserName": "Account Operators",
    "UserTypeId": 2
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
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
ROLE_URI = "AccountService/Roles"
ACCOUNT_URI = "AccountService/Accounts"
GET_AD_ACC = "AccountService/ExternalAccountProvider/ADAccountProvider"
GET_LDAP_ACC = "AccountService/ExternalAccountProvider/LDAPAccountProvider"
IMPORT_ACC_PRV = "AccountService/Actions/AccountService.ImportExternalAccountProvider"
SEARCH_GROUPS = "AccountService/ExternalAccountProvider/Actions/ExternalAccountProvider.SearchGroups"
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."


def get_directory(module, rest_obj):
    user_dir_name = module.params.get("directory_name")
    user_dir_id = module.params.get("directory_id")
    key = "name" if user_dir_name is not None else "id"
    value = user_dir_name if user_dir_name is not None else user_dir_id
    dir_id = None
    if user_dir_name is None and user_dir_id is None:
        module.fail_json(msg="missing required arguments: directory_name or directory_id")
    URI = GET_AD_ACC if module.params.get("directory_type") == "AD" else GET_LDAP_ACC
    directory_resp = rest_obj.invoke_request("GET", URI)
    for dire in directory_resp.json_data["value"]:
        if user_dir_name is not None and dire["Name"] == user_dir_name:
            dir_id = dire["Id"]
            break
        if user_dir_id is not None and dire["Id"] == user_dir_id:
            dir_id = dire["Id"]
            break
    else:
        module.fail_json(msg="Unable to complete the operation because the entered "
                             "directory {0} '{1}' does not exist.".format(key, value))
    return dir_id


def search_directory(module, rest_obj, dir_id):
    group_name, obj_gui_id, common_name = module.params["group_name"], None, None
    payload = {"DirectoryServerId": dir_id,
               "Type": module.params["directory_type"],
               "UserName": module.params["domain_username"],
               "Password": module.params["domain_password"],
               "CommonName": group_name}
    try:
        resp = rest_obj.invoke_request("POST", SEARCH_GROUPS, data=payload)
        for key in resp.json_data:
            if key["CommonName"].lower() == group_name.lower():
                obj_gui_id = key["ObjectGuid"]
                common_name = key["CommonName"]
                break
        else:
            module.fail_json(msg="Unable to complete the operation because the entered "
                                 "group name '{0}' does not exist.".format(group_name))
    except HTTPError as err:
        error = json.load(err)
        if error['error']['@Message.ExtendedInfo'][0]['MessageId'] in ["CGEN1004", "CSEC5022"]:
            module.fail_json(msg="Unable to complete the operation because the entered "
                                 "domain username or domain password are invalid.")
    return obj_gui_id, common_name


def directory_user(module, rest_obj):
    user = get_directory_user(module, rest_obj)
    new_role_id = get_role(module, rest_obj)
    dir_id = get_directory(module, rest_obj)
    domain_resp, local_msg, msg = None, '', ''
    if user is None:
        obj_gui_id, common_name = search_directory(module, rest_obj, dir_id)
        if module.check_mode:
            module.exit_json(msg=CHANGES_FOUND, changed=True)
        payload = [
            {"UserTypeId": 2, "DirectoryServiceId": dir_id, "Description": None,
             "Name": common_name, "Password": "", "UserName": common_name, "RoleId": new_role_id, "Locked": False,
             "IsBuiltin": False, "Enabled": True, "ObjectGuid": obj_gui_id}
        ]
        domain_resp = rest_obj.invoke_request("POST", IMPORT_ACC_PRV, data=payload)
        local_msg, msg = 'import', 'imported'
    else:
        if (int(user["RoleId"]) == new_role_id):
            user = rest_obj.strip_substr_dict(user)
            module.exit_json(msg=NO_CHANGES_MSG, domain_user_status=user)
        else:
            payload = {"Id": str(user["Id"]), "UserTypeId": 2, "DirectoryServiceId": dir_id,
                       "UserName": user["UserName"], "RoleId": str(new_role_id), "Enabled": user["Enabled"]}
            update_uri = "{0}('{1}')".format(ACCOUNT_URI, user['Id'])
            if module.check_mode:
                module.exit_json(msg=CHANGES_FOUND, changed=True, domain_user_status=payload)
            domain_resp = rest_obj.invoke_request("PUT", update_uri, data=payload)
            local_msg, msg = 'update', 'updated'
    if domain_resp is None:
        module.fail_json(msg="Unable to {0} the domain user group.".format(local_msg))
    return domain_resp.json_data, msg


def get_role(module, rest_obj):
    role_name, role_id = module.params.get("role"), None
    if role_name is None:
        module.fail_json(msg="missing required arguments: role")
    resp_role = rest_obj.invoke_request("GET", ROLE_URI)
    role_list = resp_role.json_data["value"]
    for role in role_list:
        if role["Name"] == role_name.upper().replace(" ", "_"):
            role_id = int(role["Id"])
            break
    else:
        module.fail_json(msg="Unable to complete the operation because the entered "
                             "role name '{0}' does not exist.".format(role_name))
    return role_id


def get_directory_user(module, rest_obj):
    user_group_name, user = module.params.get("group_name"), None
    state = module.params["state"]
    if user_group_name is None:
        module.fail_json(msg="missing required arguments: group_name")
    user_resp = rest_obj.invoke_request('GET', ACCOUNT_URI)
    for usr in user_resp.json_data["value"]:
        if usr["UserName"].lower() == user_group_name.lower() and usr["UserTypeId"] == 2:
            user = usr
            if module.check_mode and state == "absent":
                user = rest_obj.strip_substr_dict(usr)
                module.exit_json(msg=CHANGES_FOUND, changed=True, domain_user_status=user)
            break
    else:
        if state == "absent":
            module.exit_json(msg=NO_CHANGES_MSG)
    return user


def delete_directory_user(rest_obj, user_id):
    delete_uri, changed = "{0}('{1}')".format(ACCOUNT_URI, user_id), False
    msg = "Invalid domain user group name provided."
    resp = rest_obj.invoke_request('DELETE', delete_uri)
    if resp.status_code == 204:
        changed = True
        msg = "Successfully deleted the domain user group."
    return msg, changed


def main():
    specs = {
        "state": {"required": False, "type": 'str', "default": "present",
                  "choices": ['present', 'absent']},
        "group_name": {"required": True, "type": 'str'},
        "role": {"required": False, "type": 'str'},
        "directory_name": {"required": False, "type": 'str'},
        "directory_type": {"type": 'str', "choices": ['AD', 'LDAP'], "default": "AD"},
        "directory_id": {"required": False, "type": 'int'},
        "domain_username": {"required": False, "type": 'str'},
        "domain_password": {"required": False, "type": 'str', "no_log": True},
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[['directory_name', 'directory_id'], ],
        supports_check_mode=True)
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            if module.params["state"] == "present":
                resp, msg = directory_user(module, rest_obj)
                if isinstance(resp, list):
                    resp = resp[0]
                module.exit_json(
                    msg="Successfully {0} the domain user group.".format(msg),
                    domain_user_status=resp, changed=True
                )
            else:
                user = get_directory_user(module, rest_obj)
                msg, changed = delete_directory_user(rest_obj, int(user["Id"]))
                user = rest_obj.strip_substr_dict(user)
                module.exit_json(msg=msg, changed=changed, domain_user_status=user)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, TypeError, SSLError, ConnectionError, SSLValidationError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
