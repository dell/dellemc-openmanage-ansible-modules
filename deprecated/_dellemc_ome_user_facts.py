#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 1.4
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
module: dellemc_ome_user_facts
short_description: Retrieves details of all accounts or a specific account.
version_added: "2.9"
deprecated:
  removed_in: "3.3"
  why: Replaced with M(ome_user_info).
  alternative: Use M(ome_user_info) instead.
description:
   - This module retrieves the list and basic details of all accounts or details of a specific account.
options:
  hostname:
    description: Target IP address or hostname.
    type: str
    required: True
  username:
    description: Target username.
    type: str
    required: True
  password:
    description: Target user password.
    type: str
    required: True
  port:
    description: Target HTTPS port.
    type: int
    default: 443
  account_id:
    description: Unique Id of the account
    type: int
requirements:
    - "python >= 2.7.5"
author: "Jagadeesh N V(@jagadeeshnv)"
'''

EXAMPLES = r'''
---
- name: Retrieve basic details of all accounts.
  dellemc_ome_user_facts:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"

- name: Retrieve details of a specific account identified by its account ID.
  dellemc_ome_user_facts:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    account_id: 1
'''

RETURN = r'''
---
msg:
  type: str
  description: Over all status of fetching user facts.
  returned: on error
  sample: "Failed to fetch the user facts"
ansible_facts:
  type: dict
  description: Details of the users.
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
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.remote_management.dellemc.ome import RestOME
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


def main():
    module = AnsibleModule(
        argument_spec={
            "hostname": {"required": True, "type": 'str'},
            "username": {"required": True, "type": 'str'},
            "password": {"required": True, "type": 'str', "no_log": True},
            "port": {"required": False, "type": 'int', "default": 443},
            "account_id": {"type": 'int', "required": False},
        },
        supports_check_mode=False
    )
    module.deprecate("The 'dellemc_ome_user_facts' module has been deprecated. "
                     "Use 'ome_user_info' instead",
                     version=3.3)
    account_uri = "AccountService/Accounts"
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            if module.params.get("account_id") is not None:
                # Fetch specific account
                account_id = module.params.get("account_id")
                account_path = "{0}('{1}')".format(account_uri, account_id)
            else:
                # Fetch all users
                account_path = account_uri
            resp = rest_obj.invoke_request('GET', account_path)
            user_facts = resp.json_data
            # check for 200 status as GET only returns this for success
        if resp.status_code == 200:
            module.exit_json(ansible_facts={module.params["hostname"]: user_facts})
        else:
            module.fail_json(msg="Failed to fetch user facts")
    except HTTPError as err:
        module.fail_json(msg=json.load(err))
    except (URLError, SSLValidationError, ConnectionError, TypeError, ValueError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
