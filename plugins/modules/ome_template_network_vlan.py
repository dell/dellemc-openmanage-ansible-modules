#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2020-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_template_network_vlan
short_description: Set tagged and untagged vlans to native network card supported by a template on OpenManage Enterprise
version_added: "2.0.0"
description: "This module allows to set tagged and untagged vlans to native network card supported by a template
on OpenManage Enterprise."
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  template_name:
    description:
      - Name of the template.
      - It is mutually exclusive with I(template_id).
    type: str
  template_id:
    description:
      - Id of the template.
      - It is mutually exclusive with I(template_name).
    type: int
  nic_identifier:
    description: Display name of NIC port in the template for VLAN configuration.
    required: true
    type: str
  propagate_vlan:
    description:
      - To deploy the modified VLAN settings immediately without rebooting the server.
      - This option will be applied only when there are changes to the VLAN configuration.
    default: true
    type: bool
    version_added: 3.4.0
  untagged_networks:
    description: List of untagged networks and their corresponding NIC ports.
    elements: dict
    type: list
    suboptions:
      port:
        description: NIC port number of the untagged VLAN.
        required: true
        type: int
      untagged_network_id:
        description:
          - ID of the untagged VLAN
          - Enter 0 to clear the untagged VLAN from the port.
          - This option is mutually exclusive with I(untagged_network_name)
          - To get the VLAN network ID use the API U( https://I(hostname)/api/NetworkConfigurationService/Networks)
        type: int
      untagged_network_name:
        description:
          - name of the vlan for untagging
          - provide 0 for clearing the untagging for this I(port)
          - This parameter is mutually exclusive with I(untagged_network_id)
        type: str
  tagged_networks:
    description: List of tagged VLANs and their corresponding NIC ports.
    type: list
    elements: dict
    suboptions:
      port:
        description: NIC port number of the tagged VLAN
        required: true
        type: int
      tagged_network_ids:
        description:
          - List of IDs of the tagged VLANs
          - Enter [] to remove the tagged VLAN from a port.
          - List of I(tagged_network_ids) is combined with list of I(tagged_network_names) when adding tagged VLANs to a port.
          - To get the VLAN network ID use the API U( https://I(hostname)/api/NetworkConfigurationService/Networks)
        type: list
        elements: int
      tagged_network_names:
        description:
          - List of names of tagged VLANs
          - Enter [] to remove the tagged VLAN from a port.
          - List of I(tagged_network_names) is combined with list of I(tagged_network_ids) when adding tagged VLANs to a port.
        type: list
        elements: str
requirements:
    - "python >= 3.9.6"
author:
    - "Jagadeesh N V(@jagadeeshnv)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Add tagged or untagged VLANs to a template using VLAN ID and name
  dellemc.openmanage.ome_template_network_vlan:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    template_id: 78
    nic_identifier: NIC Slot 4
    untagged_networks:
      - port: 1
        untagged_network_id: 127656
      - port: 2
        untagged_network_name: vlan2
    tagged_networks:
      - port: 1
        tagged_network_ids:
          - 12767
          - 12768
      - port: 4
        tagged_network_ids:
          - 12767
          - 12768
        tagged_network_names:
          - vlan3
      - port: 2
        tagged_network_names:
          - vlan4
          - vlan1

- name: Clear the tagged and untagged VLANs from a template
  dellemc.openmanage.ome_template_network_vlan:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    template_id: 78
    nic_identifier: NIC Slot 4
    untagged_networks:
      # For removing the untagged VLANs for the port 1 and 2
      - port: 1
        untagged_network_id: 0
      - port: 2
        untagged_network_name: 0
    tagged_networks:
      # For removing the tagged VLANs for port 1, 4 and 2
      - port: 1
        tagged_network_ids: []
      - port: 4
        tagged_network_ids: []
        tagged_network_names: []
      - port: 2
        tagged_network_names: []
'''

RETURN = r'''
---
msg:
  type: str
  description: Overall status of the template vlan operation.
  returned: always
  sample: "Successfully applied the network settings to template."
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
        "error": {
            "@Message.ExtendedInfo": [
                {
                    "Message": "Unable to complete the request because
                    TemplateId  does not exist or is not applicable for the
                    resource URI.",
                    "MessageArgs": [
                        "TemplateId"
                    ],
                    "MessageId": "CGEN1004",
                    "RelatedProperties": [],
                    "Resolution": "Check the request resource URI. Refer to
                    the OpenManage Enterprise-Modular User's Guide for more
                    information about resource URI and its properties.",
                    "Severity": "Critical"
                }
            ],
            "code": "Base.1.0.GeneralError",
            "message": "A general error has occurred. See ExtendedInfo for more information."
        }
    }
'''

import json
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError

NETWORK_HIERARCHY_VIEW = 4  # For Network hierarchy View in a Template
UPDATE_NETWORK_CONFIG = "TemplateService/Actions/TemplateService.UpdateNetworkConfig"
TEMPLATE_ATTRIBUTE_VIEW = "TemplateService/Templates({0})/Views({1}" \
                          ")/AttributeViewDetails"
VLAN_NETWORKS = "NetworkConfigurationService/Networks?$top=9999"
TEMPLATE_VIEW = "TemplateService/Templates"  # Add ?$top=9999 if not query
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
SUCCESS_MSG = "Successfully applied the network settings to the template."
KEY_ATTR_NAME = 'DisplayName'
SUB_GRP_ATTR_NAME = 'SubAttributeGroups'
GRP_ATTR_NAME = 'Attributes'
GRP_NAME_ID_ATTR_NAME = 'GroupNameId'
CUSTOM_ID_ATTR_NAME = 'CustomId'


def get_template_details(module, rest_obj):
    id = module.params.get('template_id')
    query_param = {"$filter": "Id eq {0}".format(id)}
    srch = 'Id'
    if not id:
        id = module.params.get('template_name')
        query_param = {"$filter": "Name eq '{0}'".format(id)}
        srch = 'Name'
    resp = rest_obj.invoke_request('GET', TEMPLATE_VIEW, query_param=query_param)
    if resp.success and resp.json_data.get('value'):
        tlist = resp.json_data.get('value', [])
        for xtype in tlist:
            if xtype.get(srch) == id:
                return xtype
    module.fail_json(msg="Template with {0} '{1}' not found.".format(srch, id))


def get_vlan_name_id_map(rest_obj):
    k = "Name"
    v = "Id"
    d = {}
    resp = rest_obj.invoke_request('GET', VLAN_NETWORKS)
    if resp.success and resp.json_data.get('value'):
        tlist = resp.json_data.get('value', [])
        for xtype in tlist:
            d[xtype[k]] = xtype[v]
    return d


def get_template_vlan_info(module, rest_obj, template_id):
    port_id_map = {}
    port_untagged_map = {}
    port_tagged_map = {}
    port_nic_bond_map = {}
    nic_bonding_tech = ""
    resp = rest_obj.invoke_request('GET', TEMPLATE_ATTRIBUTE_VIEW.format(
        template_id, NETWORK_HIERARCHY_VIEW))
    if resp.success:
        nic_id = module.params.get("nic_identifier")
        nic_model = resp.json_data.get('AttributeGroups', [])
        # nic_group = nic_model[0]['SubAttributeGroups']
        for xnic in nic_model:
            if xnic.get(KEY_ATTR_NAME) == "NICModel":
                nic_group = xnic.get('SubAttributeGroups', [])
            if xnic.get(KEY_ATTR_NAME) == "NicBondingTechnology":
                nic_bonding_list = xnic.get("Attributes", [])
                for xbnd in nic_bonding_list:
                    if xbnd.get(KEY_ATTR_NAME).lower() == "nic bonding technology":
                        nic_bonding_tech = xbnd.get('Value')
        nic_found = False
        for nic in nic_group:
            if nic_id == nic.get(KEY_ATTR_NAME):
                nic_found = True
                for port in nic.get(SUB_GRP_ATTR_NAME):  # ports
                    for partition in port.get(SUB_GRP_ATTR_NAME):  # partitions
                        for attribute in partition.get(GRP_ATTR_NAME):  # attributes
                            if attribute.get(CUSTOM_ID_ATTR_NAME) != 0:
                                port_number = port.get(GRP_NAME_ID_ATTR_NAME)
                                port_id_map[port_number] = attribute.get(CUSTOM_ID_ATTR_NAME)
                                if attribute.get(KEY_ATTR_NAME).lower() == "vlan untagged":
                                    port_untagged_map[port_number] = int(attribute['Value'])
                                if attribute.get(KEY_ATTR_NAME).lower() == "vlan tagged":
                                    port_tagged_map[port_number] = []
                                    if attribute['Value']:
                                        port_tagged_map[port_number] = \
                                            list(map(int, (attribute['Value']).replace(" ", "").split(",")))
                                if attribute.get(KEY_ATTR_NAME).lower() == "nic bonding enabled":
                                    port_nic_bond_map[port_number] = attribute['Value']
        if not nic_found:
            module.fail_json(msg="NIC with name '{0}' not found for template with id {1}".format(nic_id, template_id))
    return port_id_map, port_untagged_map, port_tagged_map, port_nic_bond_map, nic_bonding_tech


def compare_nested_dict(modify_setting_payload, existing_setting_payload):
    """compare existing and requested setting values of identity pool in case of modify operations
    if both are same return True"""
    for key, val in modify_setting_payload.items():
        if existing_setting_payload.get(key) is None:
            return False
        elif isinstance(val, dict):
            if not compare_nested_dict(val, existing_setting_payload.get(key)):
                return False
        elif val != existing_setting_payload.get(key):
            return False
    return True


def get_vlan_payload(module, rest_obj, untag_dict, tagged_dict):
    payload = {}
    template = get_template_details(module, rest_obj)
    payload["TemplateId"] = template["Id"]
    payload["IdentityPoolId"] = template["IdentityPoolId"]
    # VlanAttributes
    port_id_map, port_untagged_map, port_tagged_map, port_nic_bond_map, nic_bonding_tech =\
        get_template_vlan_info(module, rest_obj, template['Id'])
    payload["BondingTechnology"] = nic_bonding_tech
    payload["PropagateVlan"] = module.params.get('propagate_vlan')
    untag_equal_dict = compare_nested_dict(untag_dict, port_untagged_map)
    tag_equal_dict = compare_nested_dict(tagged_dict, port_tagged_map)
    if untag_equal_dict and tag_equal_dict:
        module.exit_json(msg=NO_CHANGES_MSG)
    vlan_attributes = []
    for pk, pv in port_id_map.items():
        mdict = {}
        if pk in untag_dict or pk in tagged_dict:
            mdict["Untagged"] = untag_dict.pop(pk, port_untagged_map.get(pk))
            mdict["Tagged"] = tagged_dict.pop(pk, port_tagged_map.get(pk))
            mdict["ComponentId"] = port_id_map.get(pk)
            mdict["IsNicBonded"] = port_nic_bond_map.get(pk)
        if mdict:
            vlan_attributes.append(mdict)
    if untag_dict:
        module.fail_json(msg="Invalid port(s) {0} found for untagged VLAN".format(untag_dict.keys()))
    if tagged_dict:
        module.fail_json(msg="Invalid port(s) {0} found for tagged VLAN".format(tagged_dict.keys()))
    if module.check_mode:
        module.exit_json(changed=True, msg=CHANGES_FOUND)
    payload["VlanAttributes"] = vlan_attributes
    return payload


def get_key(val, my_dict):
    for key, value in my_dict.items():
        if val == value:
            return key
    return None


def validate_vlans(module, rest_obj):
    vlan_name_id_map = get_vlan_name_id_map(rest_obj)
    vlan_name_id_map["0"] = 0
    tagged_list = module.params.get("tagged_networks")
    untag_list = module.params.get("untagged_networks")
    untag_dict = {}
    if untag_list:
        for utg in untag_list:
            p = utg["port"]
            if utg.get("untagged_network_id") is not None:
                if p in untag_dict:
                    module.fail_json(msg="port {0} is repeated for "
                                         "untagged_network_id".format(p))
                vlan = utg.get("untagged_network_id")
                if vlan not in vlan_name_id_map.values():
                    module.fail_json(msg="untagged_network_id: {0} is not a "
                                         "valid vlan id for port {1}".
                                     format(vlan, p))
                untag_dict[p] = vlan
            if utg.get("untagged_network_name"):
                vlan = utg.get("untagged_network_name")
                if vlan in vlan_name_id_map:
                    if p in untag_dict:
                        module.fail_json(msg="port {0} is repeated for "
                                             "untagged_network_name".format(p))
                    untag_dict[p] = vlan_name_id_map.get(vlan)
                else:
                    module.fail_json(msg="{0} is not a valid vlan name for port {1}".format(vlan, p))
    vlan_name_id_map.pop("0")
    tagged_dict = {}
    if tagged_list:
        for tg in tagged_list:
            p = tg["port"]
            tg_list = []
            empty_list = False
            tgnids = tg.get("tagged_network_ids")
            if isinstance(tgnids, list):
                if len(tgnids) == 0:
                    empty_list = True
                for vl in tgnids:
                    if vl not in vlan_name_id_map.values():
                        module.fail_json(msg="{0} is not a valid vlan id "
                                             "port {1}".format(vl, p))
                    tg_list.append(vl)
            tgnames = tg.get("tagged_network_names")
            if isinstance(tgnames, list):
                if len(tgnames) == 0:
                    empty_list = True
                for vln in tgnames:
                    if vln not in vlan_name_id_map:
                        module.fail_json(msg="{0} is not a valid vlan name "
                                             "port {1}".format(vln, p))
                    tg_list.append(vlan_name_id_map.get(vln))
            if not tg_list and not empty_list:
                module.fail_json(msg="No tagged_networks provided or valid tagged_networks not found for port {0}"
                                 .format(p))
            tagged_dict[p] = list(set(tg_list))  # Will not report duplicates
    for k, v in untag_dict.items():
        if v in tagged_dict.get(k, []):
            module.fail_json(msg="vlan {0}('{1}') cannot be in both tagged and untagged list for port {2}".
                             format(v, get_key(v, vlan_name_id_map), k))
    return untag_dict, tagged_dict


def main():
    port_untagged_spec = {"port": {"required": True, "type": "int"},
                          "untagged_network_id": {"type": "int"},
                          "untagged_network_name": {"type": "str"}}
    port_tagged_spec = {"port": {"required": True, "type": "int"},
                        "tagged_network_ids": {"type": "list", "elements": "int"},
                        "tagged_network_names": {"type": "list", "elements": "str"}}
    specs = {
        "template_name": {"required": False, "type": "str"},
        "template_id": {"required": False, "type": "int"},
        "nic_identifier": {"required": True, "type": "str"},
        "untagged_networks": {"required": False, "type": "list", "elements": "dict", "options": port_untagged_spec,
                              "mutually_exclusive": [("untagged_network_id", "untagged_network_name")]},
        "tagged_networks": {"required": False, "type": "list", "elements": "dict", "options": port_tagged_spec},
        "propagate_vlan": {"type": "bool", "default": True}
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        required_one_of=[("template_id", "template_name"),
                         ("untagged_networks", "tagged_networks")],
        mutually_exclusive=[("template_id", "template_name")],
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            untag_dict, tagged_dict = validate_vlans(module, rest_obj)
            payload = get_vlan_payload(module, rest_obj, untag_dict, tagged_dict)
            resp = rest_obj.invoke_request("POST", UPDATE_NETWORK_CONFIG, data=payload)
            if resp.success:
                module.exit_json(msg=SUCCESS_MSG, changed=True)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, SSLValidationError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == "__main__":
    main()
