#!/usr/bin/python
# -*- coding: utf-8 -*-
# Dell OpenManage Ansible Modules
# Version 10.0.0
# Copyright (C) 2023-2025 Dell Inc. or its subsidiaries. All Rights Reserved.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
---
module: ome_template_network_vlan_info
short_description: Retrieves network configuration of template.
version_added: "7.2.0"
description:
   - "This module retrieves the network configuration of a template on
      OpenManage Enterprise or OpenManage Enterprise Modular."
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  template_id:
    description:
      - Id of the template.
      - This is mutually exclusive with I(template_name).
    type: int
  template_name:
    description:
      - Name of the template.
      - This is mutually exclusive with I(template_id).
      - "C(Note) If I(template_id) or I(template_name) option is not provided,
      the module retrieves network VLAN info of all templates."
    type: str
requirements:
  - "python >= 3.9.6"
author:
  - Jagadeesh N V(@jagadeeshnv)
  - Bhavneet Sharma (@Bhavneet-Sharma)
notes:
  - Run this module on a system that has direct access to Dell OpenManage
    Enterprise.
  - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Retrieve network details of all templates.
  dellemc.openmanage.ome_template_network_vlan_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"

- name: Retrieve network details using template ID
  dellemc.openmanage.ome_template_network_vlan_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    template_id: 1234

- name: Retrieve network details using template name
  dellemc.openmanage.ome_template_network_vlan_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    template_name: template1
"""

RETURN = r'''
---
msg:
  description: Status of template VLAN information retrieval.
  returned: always
  type: str
  sample: "Successfully retrieved the template network VLAN information."
vlan_info:
  description: Information about the template network VLAN.
  returned: success
  type: list
  elements: dict
  sample: [{
    "TemplateId": 58,
    "TemplateName": "t2",
    "NicBondingTechnology" : "LACP",
    "NicModel": {
        "NIC in Mezzanine 1B" : {
            '1' : {"Port" : 1,
                    "Vlan Tagged" : ["25367", "32656", "32658", "26898"],
                    "Vlan UnTagged" : "21474",
                    "NICBondingEnabled" : "false"},
            '2' : {"Port" : 2,
                    "Vlan Tagged" : [],
                    "Vlan UnTagged" : "32658",
                    "NIC Bonding Enabled" : "true"}
            },
        "NIC in Mezzanine 1A" : {
            '1' : {"Port" : 1,
                    "Vlan Tagged" : ["32656", "32658"],
                    "Vlan UnTagged" : "25367",
                    "NIC Bonding Enabled" : "true"},
            '2' : {"Port" : 2,
                    "Vlan Tagged" : ["21474"],
                    "Vlan UnTagged" : "32656",
                    "NIC Bonding Enabled" : "false"}
        }
    }}]
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
      "code": "Base.1.0.GeneralError",
      "message": "A general error has occurred. See ExtendedInfo for more
      information.",
      "@Message.ExtendedInfo": [
        {
          "MessageId": "GEN1234",
          "RelatedProperties": [],
          "Message": "Unable to process the request because an error occurred.",
          "MessageArgs": [],
          "Severity": "Critical",
          "Resolution": "Retry the operation. If the issue persists, contact
          your system administrator."
        }
      ]
    }
  }
'''

import json
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import (
    RestOME, OmeAnsibleModule
)

NETWORK_HIERARCHY_VIEW = 4  # For Network hierarchy View in a Template
TEMPLATE_ATTRIBUTE_VIEW = "TemplateService/Templates({0})/Views({1})/AttributeViewDetails"
TEMPLATE_VIEW = "TemplateService/Templates"  # Add ?$top=9999 if not query
KEY_ATTR_NAME = 'DisplayName'
SUB_GRP_ATTR_NAME = 'SubAttributeGroups'
GRP_ATTR_NAME = 'Attributes'
GRP_NAME_ID_ATTR_NAME = 'GroupNameId'
CUSTOM_ID_ATTR_NAME = 'CustomId'
SUCCESS_MSG = "Successfully retrieved the template network VLAN information."
NO_TEMPLATES_MSG = "No templates with network info were found."


def get_template_details(module, rest_obj):
    templt_id = module.params.get('template_id')
    query_param = {"$filter": "Id eq {0}".format(templt_id)}
    srch = 'Id'
    if not templt_id:
        templt_id = module.params.get('template_name')
        query_param = {"$filter": "Name eq '{0}'".format(templt_id)}
        srch = 'Name'
    resp = rest_obj.invoke_request('GET', TEMPLATE_VIEW, query_param=query_param)
    if resp.success and resp.json_data.get('value'):
        tlist = resp.json_data.get('value', [])
        for xtype in tlist:
            if xtype.get(srch) == templt_id:
                return xtype
    module.exit_json(
        failed=True,
        msg=f"Template with {srch.lower()} '{templt_id}' not found.")


def get_vlan_info(attribute):
    vlan_key = attribute.get(KEY_ATTR_NAME).lower()
    vlan_value = attribute.get("Value")
    if attribute.get(CUSTOM_ID_ATTR_NAME) == 0:
        return None

    if vlan_key == "vlan untagged":
        return vlan_key, int(vlan_value)
    elif vlan_key == "vlan tagged":
        return vlan_key, list(map(int, (vlan_value).replace(" ", "").split(",")))

    elif vlan_key == "nic bonding enabled":
        return vlan_key, vlan_value
    return None


def get_ports_info(port_list):
    port_data = {}
    for port in port_list:  # ports
        port_number = port.get(GRP_NAME_ID_ATTR_NAME)
        port_dict = {"Port": port_number}
        for partition in port.get(SUB_GRP_ATTR_NAME):  # partitions
            for attribute in partition.get(GRP_ATTR_NAME):  # attributes
                vlan_info = get_vlan_info(attribute)
                if vlan_info:
                    key, value = vlan_info
                    port_dict[key] = value
        port_data[port_number] = port_dict
    return port_data


def get_nic_info(nic_model):
    nic_result = {}
    for xnic in nic_model:
        attribute_key = xnic.get(KEY_ATTR_NAME)
        if attribute_key == "NICModel":
            nic_group = xnic.get('SubAttributeGroups', [])
            nic_group_dict = {}
            for nic in nic_group:
                nic_group_dict[nic.get(KEY_ATTR_NAME)] = get_ports_info(
                    nic.get(SUB_GRP_ATTR_NAME, []))
            nic_result[attribute_key] = nic_group_dict
        if attribute_key == "NicBondingTechnology":
            nic_bonding_list = xnic.get("Attributes", [])
            for xbnd in nic_bonding_list:
                if xbnd.get(KEY_ATTR_NAME).lower() == "nic bonding technology":
                    nic_result[attribute_key] = xbnd.get('Value')
    return nic_result


def get_template_vlan_info(rest_obj, template_id):
    result = {}
    try:
        resp = rest_obj.invoke_request('GET', TEMPLATE_ATTRIBUTE_VIEW.format(
            template_id, NETWORK_HIERARCHY_VIEW))
        if resp.json_data.get('AttributeGroups', []):
            nic_model = resp.json_data.get('AttributeGroups', [])
            if nic_model:
                result = get_nic_info(nic_model)
    except Exception:
        result = {}
    return result


def main():
    argument_spec = {
        "template_id": {"type": 'int'},
        "template_name": {"type": 'str'}
    }
    module = OmeAnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[('template_id', 'template_name')],
        supports_check_mode=True)
    try:
        templates = []
        with RestOME(module.params, req_session=True) as rest_obj:
            if module.params.get("template_id") or module.params.get("template_name"):
                tmplt = get_template_details(module, rest_obj)
                templates.append(tmplt)
            else:
                resp = rest_obj.get_all_items_with_pagination(TEMPLATE_VIEW)
                templates = resp.get("value")
            vlan_info = []
            for xtmp in templates:
                if xtmp.get("ViewTypeId") != 4:
                    result = get_template_vlan_info(rest_obj, xtmp['Id'])
                    result["TemplateId"] = xtmp['Id']
                    result["TemplateName"] = xtmp['Name']
                    vlan_info.append(result)

            module.exit_json(msg=SUCCESS_MSG, vlan_info=vlan_info)

    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, TypeError, ConnectionError,
            AttributeError, IndexError, KeyError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
