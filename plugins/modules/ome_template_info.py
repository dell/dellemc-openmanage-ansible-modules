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
module: ome_template_info
short_description: Retrieves template details from OpenManage Enterprise
version_added: "2.0.0"
description:
   - This module retrieves the list and details of all the templates on OpenManage Enterprise.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  template_id:
    description: Unique Id of the template.
    type: int
  system_query_options:
    description: Options for pagination of the output.
    type: dict
    suboptions:
      filter:
        description: Filter records by the supported values.
        type: str
requirements:
    - "python >= 3.9.6"
author: "Sajna Shetty(@Sajna-Shetty)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
    - This module supports C(check_mode).

'''

EXAMPLES = r'''
---
- name: Retrieve basic details of all templates
  dellemc.openmanage.ome_template_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"

- name: Retrieve details of a specific template identified by its template ID
  dellemc.openmanage.ome_template_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    template_id: 1

- name: Get filtered template info based on name
  dellemc.openmanage.ome_template_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    system_query_options:
      filter: "Name eq 'new template'"
'''

RETURN = r'''
---
msg:
  type: str
  description: Overall template facts status.
  returned: on error
  sample: "Failed to fetch the template facts"
template_info:
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
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


def _get_query_parameters(module_params):
    """Builds query parameter.

    :return: dict
    :example: {"$filter": Name eq 'template name'}
    """
    system_query_param = module_params.get("system_query_options")
    query_param = {}
    if system_query_param:
        query_param = dict([("$" + k, v) for k, v in system_query_param.items() if v is not None])
    return query_param


def main():
    specs = {
        "template_id": {"type": 'int', "required": False},
        "system_query_options": {"required": False, "type": 'dict',
                                 "options": {"filter": {"type": 'str', "required": False}}
                                 },
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[['template_id', 'system_query_options']],
        supports_check_mode=True
    )
    template_uri = "TemplateService/Templates"
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            query_param = None
            if module.params.get("template_id") is not None:
                # Fetch specific template
                template_id = module.params.get("template_id")
                template_path = "{0}({1})".format(template_uri, template_id)
            elif module.params.get("system_query_options") is not None:
                # Fetch all the templates based on Name
                query_param = _get_query_parameters(module.params)
                template_path = template_uri
            else:
                # Fetch all templates
                template_path = template_uri
            resp = rest_obj.invoke_request('GET', template_path, query_param=query_param)
            template_facts = resp.json_data
        if resp.status_code == 200:
            module.exit_json(template_info={module.params["hostname"]: template_facts})
        else:
            module.fail_json(msg="Failed to fetch the template facts")
    except HTTPError as err:
        module.fail_json(msg=json.load(err))
    except (URLError, SSLValidationError, ConnectionError, TypeError, ValueError, OSError, SSLError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
