#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2022-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_user_info
short_description: Retrieve details of all users or a specific user on iDRAC.
version_added: "7.0.0"
description:
   - "This module retrieves the list and basic details of all users or details of a specific user on
   iDRAC"
extends_documentation_fragment:
  - dellemc.openmanage.idrac_x_auth_options
options:
  user_id:
    description:
      - Sequential user id numbers that supports from 1 to 16.
      - I(user_id) is mutually exclusive with I(username)
    type: int
  username:
    type: str
    description:
      - Username of the account that is created in iDRAC local users.
      - I(username) is mutually exclusive with I(user_id)
requirements:
  - "python >= 3.9.6"
author: "Husniya Hameed(@husniya_hameed)"
notes:
    - Run this module on a system that has direct access to Dell iDRAC.
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Retrieve basic details of all user accounts.
  dellemc.openmanage.idrac_user_info:
    idrac_ip: 198.162.0.1
    idrac_user: idrac_user
    idrac_password: idrac_password
    ca_path: "/path/to/ca_cert.pem"

- name: Retrieve user details using user_id
  dellemc.openmanage.idrac_user_info:
    idrac_ip: 198.162.0.1
    idrac_user: idrac_user
    idrac_password: idrac_password
    ca_path: "/path/to/ca_cert.pem"
    user_id: 1

- name: Retrieve user details using username
  dellemc.openmanage.idrac_user_info:
    idrac_ip: 198.162.0.1
    idrac_user: idrac_user
    idrac_password: idrac_password
    ca_path: "/path/to/ca_cert.pem"
    username: user_name
"""

RETURN = r'''
---
msg:
  description: Status of user information retrieval.
  returned: always
  type: str
  sample: "Successfully retrieved the user information."
user_info:
  description: Information about the user.
  returned: success
  type: list
  sample: [{
    "Description": "User Account",
    "Enabled": false,
    "Id": "1",
    "Locked": false,
    "Name": "User Account",
    "Password": null,
    "RoleId": "None",
    "UserName": ""
  }]
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
'''


import json
from ssl import SSLError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, IdracAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import strip_substr_dict


ACCOUNT = "/redfish/v1"
SUCCESS_MSG = "Successfully retrieved the information of {0} user(s)."
UNSUCCESS_MSG = "Unable to retrieve the user information."
INVALID_USERID = "'user_id' is not valid."
INVALID_USERNAME = "'username' is not valid."
SUCCESSFUL_MSG = "Successfully retrieved the user information."


def get_accounts_uri(idrac):
    try:
        account_path = idrac.invoke_request(ACCOUNT, 'GET')
        account_service = account_path.json_data.get("AccountService").get("@odata.id")
        accounts = idrac.invoke_request(account_service, "GET")
        accounts_uri = accounts.json_data.get("Accounts").get("@odata.id")
    except HTTPError:
        accounts_uri = "/redfish/v1/AccountService/Accounts"
    return accounts_uri


def fetch_all_accounts(idrac, accounts_uri):
    all_accounts = idrac.invoke_request("{0}?$expand=*($levels=1)".format(accounts_uri), 'GET')
    all_accs = all_accounts.json_data.get("Members")
    return all_accs


def get_user_id_accounts(idrac, module, accounts_uri, user_id):
    acc_dets_json_data = {}
    try:
        acc_uri = accounts_uri + "/{0}".format(user_id)
        acc_dets = idrac.invoke_request(acc_uri, "GET")
        acc_dets_json_data = strip_substr_dict(acc_dets.json_data)
        if acc_dets_json_data.get("Oem") is not None:
            acc_dets_json_data["Oem"]["Dell"] = strip_substr_dict(acc_dets_json_data["Oem"]["Dell"])
        acc_dets_json_data.pop("Links", None)
    except HTTPError:
        module.exit_json(msg=INVALID_USERID, failed=True)
    return acc_dets_json_data


def get_user_name_accounts(idrac, module, accounts_uri, user_name):
    all_accs = fetch_all_accounts(idrac, accounts_uri)
    acc_dets_json_data = {}
    for acc in all_accs:
        if acc.get("UserName") == user_name:
            acc.pop("Links", None)
            acc_dets_json_data = strip_substr_dict(acc)
            if acc_dets_json_data.get("Oem") is not None:
                acc_dets_json_data["Oem"]["Dell"] = strip_substr_dict(acc_dets_json_data["Oem"]["Dell"])
            break
    if not bool(acc_dets_json_data):
        module.fail_json(msg=INVALID_USERNAME, failed=True)
    return acc_dets_json_data


def get_all_accounts(idrac, account_uri):
    all_accs = fetch_all_accounts(idrac, account_uri)
    idrac_list = []
    for acc in all_accs:
        if acc.get("UserName") != "":
            acc.pop("Links", None)
            acc_dets_json_data = strip_substr_dict(acc)
            if acc_dets_json_data.get("Oem") is not None:
                acc_dets_json_data["Oem"]["Dell"] = strip_substr_dict(acc_dets_json_data["Oem"]["Dell"])
            idrac_list.append(acc_dets_json_data)
    return idrac_list


def main():
    specs = {
        "user_id": {"type": 'int'},
        "username": {"type": 'str'}
    }

    module = IdracAnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[
            ('user_id', 'username')
        ],
        supports_check_mode=True
    )
    try:
        with iDRACRedfishAPI(module.params, req_session=True) as idrac:
            resp = []
            msg = SUCCESSFUL_MSG
            accounts_uri = get_accounts_uri(idrac)
            user_id = module.params.get("user_id")
            user_name = module.params.get("username")
            if user_id is not None:
                resp.append(get_user_id_accounts(idrac, module, accounts_uri, user_id))
            elif user_name is not None:
                resp.append(get_user_name_accounts(idrac, module, accounts_uri, user_name))
            else:
                resp.extend(get_all_accounts(idrac, accounts_uri))
                resp_len = len(resp)
                msg = SUCCESS_MSG.format(resp_len)
            if resp:
                module.exit_json(msg=msg, user_info=resp)
            else:
                module.fail_json(msg=UNSUCCESS_MSG, failed=True)
    except HTTPError as err:
        module.fail_json(msg=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError, SSLError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
