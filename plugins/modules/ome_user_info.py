#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.0.1
# Copyright (C) 2019-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_user_info
short_description: Retrieves details of all accounts or a specific account on OpenManage Enterprise
version_added: "2.0.0"
description:
   - "This module retrieves the list and basic details of all accounts or details of a specific account on
   OpenManage Enterprise."
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  account_id:
    description: Unique Id of the account.
    type: int
  system_query_options:
    description: Options for filtering the output.
    type: dict
    suboptions:
      filter:
        description: Filter records for the supported values.
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
- name: Retrieve basic details of all accounts
  dellemc.openmanage.ome_user_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"

- name: Retrieve details of a specific account identified by its account ID
  dellemc.openmanage.ome_user_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    account_id: 1

- name: Get filtered user info based on user name
  dellemc.openmanage.ome_user_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    system_query_options:
      filter: "UserName eq 'test'"
'''

RETURN = r'''
---
msg:
  type: str
  description: Over all status of fetching user facts.
  returned: on error
  sample: "Unable to retrieve the account details."
user_info:
  type: dict
  description: Details of the user.
  returned: success
  sample: {
     "192.168.0.1": {
            "Id": "1814",
            "UserTypeId": 1,
            "DirectoryServiceId": 0,
            "Description": "user name description",
            "Name": "user_name",
            "Password": null,
            "UserName": "user_name",
            "RoleId": "10",
            "Locked": false,
            "IsBuiltin": true,
            "Enabled": true
     }
  }
'''

import json
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


def _get_query_parameters(module_params):
    """Builds query parameter.

    :return: dict
    :example: {"$filter": UserName eq 'user name'}
    """
    system_query_param = module_params.get("system_query_options")
    query_param = {}
    if system_query_param:
        query_param = dict([("$" + k, v) for k, v in system_query_param.items() if v is not None])
    return query_param


def main():
    specs = {
        "account_id": {"type": 'int', "required": False},
        "system_query_options": {"required": False, "type": 'dict', "options": {
            "filter": {"type": 'str', "required": False},
        }},
    }
    specs.update(ome_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[
            ('account_id', 'system_query_options')
        ],
        supports_check_mode=True
    )
    account_uri = "AccountService/Accounts"
    query_param = None
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            if module.params.get("account_id") is not None:
                # Fetch specific account
                account_id = module.params.get("account_id")
                account_path = "{0}('{1}')".format(account_uri, account_id)
            elif module.params.get("system_query_options") is not None:
                # Fetch all the user based on UserName
                query_param = _get_query_parameters(module.params)
                account_path = account_uri
            else:
                # Fetch all users
                account_path = account_uri
            resp = rest_obj.invoke_request('GET', account_path, query_param=query_param)
            user_facts = resp.json_data
            user_exists = True
            if "value" in user_facts and len(user_facts["value"]) == 0:
                user_exists = False
            # check for 200 status as GET only returns this for success
        if resp.status_code == 200 and user_exists:
            module.exit_json(user_info={module.params["hostname"]: user_facts})
        else:
            module.fail_json(msg="Unable to retrieve the account details.")
    except HTTPError as err:
        module.fail_json(msg=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError, SSLError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
