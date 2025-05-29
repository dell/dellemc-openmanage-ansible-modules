#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2023-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
---
module: ome_profile_info
short_description: Retrieve profiles with attribute details
version_added: "7.2.0"
description:
  - "This module retrieve profiles with attributes on OpenManage Enterprise or OpenManage Enterprise Modular."
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  profile_id:
    description:
      - Id of the profile.
      - This is mutually exclusive with I(profile_name), I(system_query_options), I(template_id), and I(template_name).
    type: int
  profile_name:
    description:
      - Name of the profile.
      - This is mutually exclusive with I(template_id), I(profile_id), I(system_query_options), and I(template_name).
    type: str
  template_id:
    description:
      - Provide the ID of the template to retrieve the list of profile(s) linked to it.
      - This is mutually exclusive with I(profile_name), I(profile_id), I(system_query_options), and I(template_name).
    type: int
  template_name:
    description:
      - Provide the name of the template to retrieve the list of profile(s) linked to it.
      - This is mutually exclusive with I(profile_name), I(profile_id), I(template_id), and I(system_query_options).
    type: str
  system_query_options:
    description:
      - Option for providing supported odata filters.
      - "The profile list can be fetched and sorted based on ProfileName, TemplateName, TargetTypeId, TargetName,
      ChassisName, ProfileState, LastRunStatus, or ProfileModified."
      - This is mutually exclusive with I(profile_name), I(profile_id), I(template_id), and I(template_name).
      - "C(Note) If I(profile_name), I(profile_id), I(template_id), or I(template_name) option is not provided, the
      module retrieves all the profiles."
    type: dict
requirements:
  - "python >= 3.9.6"
author:
  - Jagadeesh N V(@jagadeeshnv)
notes:
  - Run this module on a system that has direct access to Dell OpenManage Enterprise.
  - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Retrieve all profiles
  dellemc.openmanage.ome_profile_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"

- name: Retrieve profile using the name
  dellemc.openmanage.ome_profile_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    profile_name: eprof 00001

- name: Retrieve profile using the id
  dellemc.openmanage.ome_profile_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    profile_id: 10129

- name: Retrieve the profiles using the template name
  dellemc.openmanage.ome_profile_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    template_name: t2

- name: Retrieve the profiles using the template id
  dellemc.openmanage.ome_profile_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    template_id: 11

- name: Retrieve the profiles based on the odata filters
  dellemc.openmanage.ome_profile_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    system_query_options:
      filter: TemplateName eq 'mytemplate'
      orderby: ProfileState
"""

RETURN = r'''
---
msg:
  description: Status of profile information retrieval.
  returned: always
  type: str
  sample: "Successfully retrieved the profile information."
profile_info:
  description: Information about the profile.
  returned: success
  type: list
  elements: dict
  sample:
    [
      {
        "Id": 71460,
        "ProfileName": "Profile 00001",
        "ProfileDescription": "from source template: (Template)",
        "TemplateId": 8,
        "TemplateName": "Template",
        "DataSchemaId": 8,
        "TargetId": 0,
        "TargetName": null,
        "TargetTypeId": 0,
        "DeviceIdInSlot": 0,
        "ChassisId": 0,
        "ChassisName": null,
        "GroupId": 0,
        "GroupName": null,
        "NetworkBootToIso": null,
        "ProfileState": 0,
        "DeploymentTaskId": 0,
        "LastRunStatus": 2200,
        "ProfileModified": 0,
        "CreatedBy": "admin",
        "EditedBy": null,
        "CreatedDate": "2019-09-26 13:56:41.924966",
        "LastEditDate": "2020-12-11 08:27:20.500564",
        "LastDeployDate": "",
        "AttributeIdMap": {
          "4965": {
            "Value": "hostname",
            "IsReadOnly": false,
            "IsIgnored": true
          },
          "4963": {
            "Value": "second floor",
            "IsReadOnly": false,
            "IsIgnored": true
          },
          "4960": {
            "Value": "10A",
            "IsReadOnly": false,
            "IsIgnored": true
          },
          "4959": {
            "Value": "OMAMDEV",
            "IsReadOnly": false,
            "IsIgnored": true
          },
          "4957": {
            "Value": "Dell LAB",
            "IsReadOnly": false,
            "IsIgnored": true
          },
          "4958": {
            "Value": null,
            "IsReadOnly": false,
            "IsIgnored": true
          },
          "4066": {
            "Value": null,
            "IsReadOnly": false,
            "IsIgnored": true
          },
          "4231": {
            "Value": "1",
            "IsReadOnly": false,
            "IsIgnored": false
          },
          "4229": {
            "Value": "Disabled",
            "IsReadOnly": false,
            "IsIgnored": false
          }
        },
        "AttributeDetails": {
          "System": {
            "Server Operating System": {
              "ServerOS 1 Server Host Name": 4965
            },
            "Server Topology": {
              "ServerTopology 1 Room Name": 4963,
              "ServerTopology 1 Rack Slot": 4960,
              "ServerTopology 1 Rack Name": 4959,
              "ServerTopology 1 Data Center Name": 4957,
              "ServerTopology 1 Aisle Name": 4958
            }
          },
          "iDRAC": {
            "Active Directory": {
              "ActiveDirectory 1 Active Directory RAC Name": 4066
            },
            "NIC Information": {
              "NIC 1 VLAN ID": 4231,
              "NIC 1 Enable VLAN": 4229
            }
          }
        }
      }
    ]
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
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import strip_substr_dict


PROFILE_VIEW = "ProfileService/Profiles"
TEMPLATE_VIEW = "TemplateService/Templates"
SUCCESS_MSG = "Successfully retrieved the profile information."
NO_PROFILES_MSG = "Profiles with {0} {1} not found."
SEPRTR = ','


def get_template_details(module, rest_obj):
    id = module.params.get('template_id')
    query_param = {"$filter": "Id eq {0}".format(id)}
    srch = 'Id'
    t_id = 'template_id'
    if not id:
        id = module.params.get('template_name')
        query_param = {"$filter": "Name eq '{0}'".format(id)}
        srch = 'Name'
        t_id = 'template_name'
    resp = rest_obj.invoke_request('GET', TEMPLATE_VIEW, query_param=query_param)
    if resp.success and resp.json_data.get('value'):
        tlist = resp.json_data.get('value', [])
        for xtype in tlist:
            if xtype.get(srch) == id:
                return xtype, id, t_id
    module.exit_json(failed=True, msg="Template with {0} '{1}' not found.".format(srch.lower(), id))


def get_profile_query(rest_obj, query, url_prm):
    prof_list = []
    try:
        if query:
            resp = rest_obj.get_all_items_with_pagination(PROFILE_VIEW, query_param=query)
            prof_list = resp.get("value")
        if url_prm:
            url_resp = rest_obj.invoke_request("GET", "{0}{1}".format(PROFILE_VIEW, url_prm))
            prof_list = [url_resp.json_data]
    except Exception:
        prof_list = []
    return prof_list


def construct_tree_str(nprfx, attr_detailed):
    str_lst = nprfx.split(SEPRTR)
    br = attr_detailed
    for xs in str_lst:
        if xs not in br:
            br[xs] = {}
        br = br.get(xs)
    return br


def recurse_subattr_list(subgroup, prefix, attr_detailed, attr_map):
    rq_attr = ["Value", "IsReadOnly", "IsIgnored"]
    if isinstance(subgroup, list):
        for each_sub in subgroup:
            nprfx = "{0}{1}{2}".format(prefix, SEPRTR, each_sub.get("DisplayName"))
            if each_sub.get("SubAttributeGroups"):
                recurse_subattr_list(each_sub.get("SubAttributeGroups"), nprfx, attr_detailed, attr_map)
            else:
                for attr in each_sub.get('Attributes'):
                    nd = construct_tree_str(nprfx, attr_detailed)
                    nd[attr['DisplayName']] = attr['AttributeId']
                    vlist = dict((xf, attr.get(xf)) for xf in rq_attr)
                    attr_map[attr['AttributeId']] = vlist


def get_subattr_all(attr_dtls):
    attr_detailed = {}
    attr_map = {}
    for each in attr_dtls:
        recurse_subattr_list(each.get('SubAttributeGroups'), each.get('DisplayName'), attr_detailed, attr_map)
    return attr_detailed, attr_map


def get_attribute_detail_tree(rest_obj, prof_id):
    try:
        resp = rest_obj.invoke_request('GET', "{0}({1})/AttributeDetails".format(PROFILE_VIEW, prof_id))
        attr_list = resp.json_data.get("AttributeGroups")
        attr_detailed, attr_map = get_subattr_all(attr_list)
    except Exception:
        attr_detailed, attr_map = {}, {}
    return attr_detailed, attr_map


def main():
    argument_spec = {
        "profile_id": {"type": 'int'},
        "profile_name": {"type": 'str'},
        "template_id": {"type": 'int'},
        "template_name": {"type": 'str'},
        "system_query_options": {"type": 'dict'}
    }
    module = OmeAnsibleModule(argument_spec=argument_spec,
                              mutually_exclusive=[('profile_id', 'profile_name', 'template_name', 'template_id',
                                                   'system_query_options')],
                              supports_check_mode=True)
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            query = {}
            url_prm = None
            prof_list = []
            if module.params.get("template_id") or module.params.get("template_name"):
                tmplt, value, name = get_template_details(module, rest_obj)
                query["$filter"] = "TemplateName eq '{0}'".format(tmplt.get('Name'))
            elif module.params.get("profile_id"):
                url_prm = "({0})".format(module.params.get("profile_id"))
                name = "profile_id"
                value = module.params.get("profile_id")
            elif module.params.get("profile_name"):
                query["$filter"] = "ProfileName eq '{0}'".format(module.params.get("profile_name"))
                name = "profile_name"
                value = module.params.get("profile_name")
            elif module.params.get("system_query_options"):
                name = "provided"
                value = "system_query_options"
                for k, v in module.params.get("system_query_options").items():
                    query["${0}".format(k)] = v
            if query or url_prm:
                prof_list = get_profile_query(rest_obj, query, url_prm)
                if module.params.get("profile_name"):
                    xprofs = []
                    pname = module.params.get("profile_name")
                    for xp in prof_list:
                        if xp.get("ProfileName") == pname:
                            xprofs.append(xp)
                            break
                    prof_list = xprofs
            else:
                resp = rest_obj.get_all_items_with_pagination(PROFILE_VIEW)
                prof_list = resp.get("value")
                if not bool(prof_list):
                    module.exit_json(msg=SUCCESS_MSG, profile_info=prof_list)
            for xp in prof_list:
                attr_tree, attr_map = get_attribute_detail_tree(rest_obj, xp["Id"])
                xp["AttributeIdMap"] = attr_map
                xp["AttributeDetails"] = attr_tree
                strip_substr_dict(xp)
        if prof_list:
            module.exit_json(msg=SUCCESS_MSG, profile_info=prof_list)  # ,xcount=len(prof_list))
        else:
            module.exit_json(msg=NO_PROFILES_MSG.format(name, value), failed=True)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError,
            AttributeError, IndexError, KeyError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
