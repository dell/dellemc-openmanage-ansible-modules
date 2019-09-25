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
module: dellemc_ome_template_facts
short_description: Retrieves template details.
version_added: "2.9"
deprecated:
  removed_in: "3.3"
  why: Replaced with M(ome_template_info).
  alternative: Use M(ome_template_info) instead.
description:
   - This module retrieves the list and details of all templates.
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
  template_id:
    description: Unique Id of the template.
    type: int
requirements:
    - "python >= 2.7.5"
author: "Sajna Shetty(@Sajna-Shetty)"

'''

EXAMPLES = r'''
---
- name: Retrieve basic details of all templates.
  dellemc_ome_template_facts:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"

- name: Retrieve details of a specific template identified by its template ID.
  dellemc_ome_template_facts:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    template_id: 1
'''

RETURN = r'''
---
msg:
  type: str
  description: Over all template facts status.
  returned: on error
  sample: "Failed to fetch the template facts"
ansible_facts:
  type: dict
  description: Details of the templates.
  returned: success
  sample: {
        "192.168.0.1": {
            "CreatedBy": "system",
            "CreationTime": "1970-01-31 00:00:56.372144",
            "Description": "Tune workload for Performance Optimized Virtualization",
            "HasIdentityAttributes": false,
            "Id": 1,
            "IdentityPoolId": 0,
            "IsBuiltIn": true,
            "IsPersistencePolicyValid": false,
            "IsStatelessAvailable": false,
            "LastUpdatedBy": null,
            "LastUpdatedTime": "1970-01-31 00:00:56.372144",
            "Name": "iDRAC Enable Performance Profile for Virtualization",
            "SourceDeviceId": 0,
            "Status": 0,
            "TaskId": 0,
            "TypeId": 2,
            "ViewTypeId": 4
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
            "template_id": {"type": 'int', "required": False},
        },
        supports_check_mode=False
    )
    module.deprecate("The 'dellemc_ome_template_facts' module has been deprecated. "
                     "Use 'ome_template_info' instead",
                     version=3.3)
    template_uri = "TemplateService/Templates"
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            if module.params.get("template_id") is not None:
                # Fetch specific template
                template_id = module.params.get("template_id")
                template_path = "{0}({1})".format(template_uri, template_id)
            else:
                # Fetch all templates
                template_path = template_uri
            resp = rest_obj.invoke_request('GET', template_path)
            template_facts = resp.json_data
        if resp.status_code == 200:
            module.exit_json(ansible_facts={module.params["hostname"]: template_facts})
        else:
            module.fail_json(msg="Failed to fetch the template facts")
    except HTTPError as err:
        module.fail_json(msg=json.load(err))
    except (URLError, SSLValidationError, ConnectionError, TypeError, ValueError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
