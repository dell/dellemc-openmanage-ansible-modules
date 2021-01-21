#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.0.0
# Copyright (C) 2020-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_smart_fabric
short_description: Create, modify or delete a fabric on OpenManage Enterprise Modular
version_added: "2.1.0"
description:
  - This module allows to create a fabric, and modify or delete an existing fabric
   on OpenManage Enterprise Modular.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  state:
    type: str
    description:
      - C(present) creates a new fabric or modifies an existing fabric.
      - C(absent) deletes an existing fabric.
      - "Notes: The create, modify, or delete fabric operation takes around 15-20 minutes to complete. It is recommended
      not to start an another operation until the current operation is completed."
    choices: [present, absent]
    default: present
  name:
    required: true
    type: str
    description: Provide the I(name) of the fabric to be created, deleted or modified.
  new_name:
    type: str
    description: Provide the I(name) of the fabric to be modified.
  description:
    type: str
    description: Provide a short description of the fabric to be created or modified.
  fabric_design:
    type: str
    description:
      - "Specify the fabric topology.See the use API
      U(https://www.dell.com/support/manuals/en-in/poweredge-mx7000/omem_1_20_10_ug/smartfabric-network-topologies)
      to know why its topology."
      - I(fabric_design) is mandatory for fabric creation.
    choices: [2xMX5108n_Ethernet_Switches_in_same_chassis,
    2xMX9116n_Fabric_Switching_Engines_in_same_chassis,
    2xMX9116n_Fabric_Switching_Engines_in_different_chassis]
  primary_switch_service_tag:
    type: str
    description:
      - Service tag of the first switch.
      - I(primary_switch_service_tag) is mandatory for fabric creation.
      - I(primary_switch_service_tag) must belong to the model selected in I(fabric_design).
  secondary_switch_service_tag:
    type: str
    description:
      - Service tag of the second switch.
      - I(secondary_switch_service_tag) is mandatory for fabric creation.
      - I(secondary_switch_service_tag) must belong to the model selected in I(fabric_design).
  override_LLDP_configuration:
    type: str
    description:
      - Enable this configuration to allow Fabric Management Address to be included in LLDP messages.
      - "Notes: OpenManage Enterprise Modular 1.0 does not support this option.
      Some software networking solutions require a single management address to be transmitted by all Ethernet switches
       to represent the entire fabric. Enable this feature only when connecting to such a solution."
    choices: ['Enabled', 'Disabled']
requirements:
    - "python >= 2.7.17"
author:
    - "Sajna Shetty(@Sajna-Shetty)"
notes:
    - Run this module from a system that has direct access to DellEMC OpenManage Enterprise Modular.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Create a fabric
  dellemc.openmanage.ome_smart_fabric:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    state: present
    name: "fabric1"
    description: "fabric desc"
    fabric_design: "2xMX9116n_Fabric_Switching_Engines_in_different_chassis"
    primary_switch_service_tag: "SVTG123"
    secondary_switch_service_tag: "PXYT456"
    override_LLDP_configuration: "Enabled"

- name: Modify a fabric
  dellemc.openmanage.ome_smart_fabric:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    state: present
    name: "fabric1"
    new_name: "fabric_gold1"
    description: "new description"

- name: Delete a fabric
  dellemc.openmanage.ome_smart_fabric:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    state: "absent"
    name: "fabric1"
'''

RETURN = r'''
---
msg:
  type: str
  description: Overall status of the fabric operation.
  returned: always
  sample: "Fabric creation operation is initiated."
fabric_id:
  type: str
  description: Returns the ID when an fabric is created, modified or deleted.
  returned: success
  sample: "1312cceb-c3dd-4348-95c1-d8541a17d776"
additional_info:
  type: dict
  description: Additional details of the fabric operation.
  returned: when I(state=present) and additional information present in response.
  sample: {
    "error": {
        "code": "Base.1.0.GeneralError",
        "message": "A general error has occurred. See ExtendedInfo for more information.",
        "@Message.ExtendedInfo": [
            {
                "RelatedProperties": [],
                "Message":  "Fabric update is successful. The OverrideLLDPConfiguration attribute is not provided in the
                 payload, so it preserves the previous value.",
                "MessageArgs": [],
                "Severity": "Informational",
                "Resolution": "Please update the Fabric with the OverrideLLDPConfiguration as Disabled or Enabled if
                 necessary."
            }
        ]
    }
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
                "RelatedProperties": [],
                "Message": "Unable to perform operation, because the fabric manager was not reachable.",
                "MessageArgs": [],
                "Severity": "Warning",
                "Resolution": "Make sure of the following and retry the operation: 1) There is at least one advanced
                 I/O Module in power-on mode. For example, MX9116n Ethernet Switch and MX5108n Ethernet Switch. However,
                  if an advanced I/O Module is available in the power-on mode, make sure that the network profile is not
                   set when the fabric manager is in the switch-over mode. 2) If the issue persists, wait for few minutes and retry the operation."
            }
        ]
    }
}
'''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ssl import SSLError

FABRIC_URI = "NetworkService/Fabrics"
FABRIC_ID_URI = "NetworkService/Fabrics('{fabric_id}')"
DOMAIN_URI = "ManagementDomainService/Domains"
DEVICE_URI = "DeviceService/Devices"

MSM_URI = "DeviceService/Devices({lead_chassis_device_id})/InventoryDetails('deviceSoftware')"

CHECK_MODE_CHANGE_FOUND_MSG = "Changes found to be applied."
CHECK_MODE_CHANGE_NOT_FOUND_MSG = "No Changes found to be applied."
FABRIC_NOT_FOUND_ERROR_MSG = "The smart fabric '{0}' is not present in the system."
DOMAIN_SERVICE_TAG_ERROR_MSG = "Unable to retrieve the domain information because the" \
                               " domain of the provided service tag {0} is not available."
LEAD_CHASSIS_ERROR_MSG = "System should be a lead chassis if the assigned fabric topology type is {0}."
SYSTEM_NOT_SUPPORTED_ERROR_MSG = "Fabric management is not supported on the specified system."
DESIGN_MODEL_ERROR_MSG = "The network type of the {0} must be {1}."
DEVICE_SERVICE_TAG_TYPE_ERROR_MSG = "The {0} type must be {1}."
DEVICE_SERVICE_TAG_NOT_FOUND_ERROR_MSG = "Unable to retrieve the device information because the device" \
                                         " with the provided service tag {0} is not available."
IDEMPOTENCY_MSG = "Specified fabric details are the same as the existing settings."
REQUIRED_FIELD = "Options 'fabric_design', 'primary_switch_service_tag' and 'secondary_switch_service_tag'" \
                 " are required for fabric creation."
DUPLICATE_TAGS = "The switch details of the primary switch overlaps with the secondary switch details."
PRIMARY_SWITCH_OVERLAP_MSG = "The primary switch service tag is overlapping with existing secondary switch details."
SECONDARY_SWITCH_OVERLAP_MSG = "The switch details of the secondary switch overlaps with the existing primary" \
                               " switch details."


def get_service_tag_with_fqdn(rest_obj, module):
    """
    get the service tag, if hostname is dnsname
    """
    hostname = module.params["hostname"]
    service_tag = None
    device_details = rest_obj.get_all_items_with_pagination(DEVICE_URI)
    for each_device in device_details["value"]:
        for item in each_device["DeviceManagement"]:
            if item["DnsName"] == hostname:
                return each_device["DeviceServiceTag"]
    return service_tag


def validate_lead_msm_version(each_domain, module, fabric_design=None):
    """
    validate lead chassis for design type
    and find the msm version of the domain
    """
    role_type = each_domain["DomainRoleTypeValue"].upper()
    if fabric_design and fabric_design == "2xMX9116n_Fabric_Switching_Engines_in_different_chassis" and \
            role_type != "LEAD":
        module.fail_json(msg=LEAD_CHASSIS_ERROR_MSG.format(fabric_design))
    msm_version = each_domain["Version"]
    return msm_version


def get_msm_device_details(rest_obj, module):
    """
    Get msm details
    :param rest_obj: session object
    :param module: Ansible module object
    :return: tuple
    1st item: service tag of the domain
    2nd item: msm version of ome-M device
    """
    hostname = module.params["hostname"]
    fabric_design = module.params.get("fabric_design")
    msm_version = ""
    service_tag = get_service_tag_with_fqdn(rest_obj, module)
    domain_details = rest_obj.get_all_items_with_pagination(DOMAIN_URI)
    for each_domain in domain_details["value"]:
        if service_tag and service_tag == each_domain["Identifier"]:
            msm_version = validate_lead_msm_version(each_domain, module, fabric_design)
            break
        if hostname in each_domain["PublicAddress"]:
            msm_version = validate_lead_msm_version(each_domain, module, fabric_design)
            service_tag = each_domain["Identifier"]
            break
    else:
        module.fail_json(msg=SYSTEM_NOT_SUPPORTED_ERROR_MSG)
    return service_tag, msm_version


def compare_payloads(modify_payload, current_payload):
    """
    :param modify_payload: payload created to update existing setting
    :param current_payload: already existing payload for specified fabric
    :return: bool - compare existing and requested setting values of fabric in case of modify operations
    if both are same return True
    """
    diff = False
    for key, val in modify_payload.items():
        if current_payload is None or current_payload.get(key) is None:
            return True
        elif isinstance(val, dict):
            if compare_payloads(val, current_payload.get(key)):
                return True
        elif val != current_payload.get(key):
            return True
    return diff


def idempotency_check_for_state_present(fabric_id, current_payload, expected_payload, module):
    """
    idempotency check in case of state present
    :param fabric_id: fabric id
    :param current_payload: payload created
    :param expected_payload: already existing payload for specified fabric
    :param module: ansible module object
    :return: None
    """
    if fabric_id:
        payload_diff = compare_payloads(expected_payload, current_payload)
        if module.check_mode:
            if payload_diff:
                module.exit_json(msg=CHECK_MODE_CHANGE_FOUND_MSG, changed=True)
            else:
                module.exit_json(msg=CHECK_MODE_CHANGE_NOT_FOUND_MSG, changed=False)
        elif not module.check_mode and not payload_diff:
            module.exit_json(msg=IDEMPOTENCY_MSG, changed=False)
    else:
        if module.check_mode:
            module.exit_json(msg=CHECK_MODE_CHANGE_FOUND_MSG, changed=True)


def design_node_dict_update(design_node_map):
    """
    make one level dictionary for design map for easy processing
    :param design_node_map: design node map content
    :return: dict
    """
    d = {}
    for item in design_node_map:
        if item["DesignNode"] == "Switch-A" and item.get('PhysicalNode'):
            d.update({'PhysicalNode1': item['PhysicalNode']})
        if item["DesignNode"] == "Switch-B" and item.get('PhysicalNode'):
            d.update({'PhysicalNode2': item['PhysicalNode']})
    return d


def validate_switches_overlap(current_dict, modify_dict, module):
    """
    Validation in case of modify operation when current setting user provided switches details overlaps
    :param current_dict: modify payload created
    :param modify_dict: current payload of specified fabric
    :param module: Ansible module object
    """
    modify_primary_switch = modify_dict.get("PhysicalNode1")
    current_secondary_switch = current_dict.get("PhysicalNode2")
    modify_secondary_switch = modify_dict.get("PhysicalNode2")
    current_primary_switch = current_dict.get("PhysicalNode1")
    flag = all([modify_primary_switch, modify_secondary_switch, current_primary_switch,
                current_secondary_switch]) and (modify_primary_switch == current_secondary_switch and
                                                modify_secondary_switch == current_primary_switch)
    if not flag and modify_primary_switch == current_secondary_switch:
        module.fail_json(PRIMARY_SWITCH_OVERLAP_MSG)
    if not flag and modify_secondary_switch == current_primary_switch:
        module.fail_json(SECONDARY_SWITCH_OVERLAP_MSG)


def fabric_design_map_payload_creation(design_map_modify_payload, design_map_current_payload, module):
    """
    process FabricDesignMapping contents
    :param design_map_modify_payload: modify payload created
    :param design_map_current_payload: current payload of specified fabric
    :param module: Ansible module object
    :return: list
    """
    modify_dict = design_node_dict_update(design_map_modify_payload)
    current_dict = design_node_dict_update(design_map_current_payload)
    validate_switches_overlap(current_dict, modify_dict, module)
    current_dict.update(modify_dict)
    design_list = []
    for key, val in current_dict.items():
        if key == "PhysicalNode1":
            design_list.append({'DesignNode': 'Switch-A', 'PhysicalNode': val})
        else:
            design_list.append({'DesignNode': 'Switch-B', 'PhysicalNode': val})
    return design_list


def merge_payload(modify_payload, current_payload, module):
    """
    :param modify_payload: payload created to update existing setting
    :param current_payload: already existing payload for specified fabric
    :param module: Ansible module object
    :return: bool - compare existing and requested setting values of fabric in case of modify operations
    if both are same return True
    """
    _current_payload = dict(current_payload)
    _current_payload.update(modify_payload)
    if modify_payload.get("FabricDesign") and current_payload.get("FabricDesign"):
        _current_payload["FabricDesign"].update(modify_payload["FabricDesign"])
    elif modify_payload.get("FabricDesign") and not current_payload.get("FabricDesign"):
        _current_payload["FabricDesign"] = modify_payload["FabricDesign"]
    fabric_design_map_list = fabric_design_map_payload_creation(modify_payload.get("FabricDesignMapping", []),
                                                                current_payload.get("FabricDesignMapping", []), module)
    if fabric_design_map_list:
        _current_payload.update({"FabricDesignMapping": fabric_design_map_list})
    return _current_payload


def get_fabric_design(fabric_design_uri, rest_obj):
    """
    Get the fabric design name from the fabric design uri which is returned from GET request
    :param fabric_design_uri: fabric design uri
    :param rest_obj: session object
    :return: dict
    """
    fabric_design = {}
    if fabric_design_uri:
        resp = rest_obj.invoke_request("GET", fabric_design_uri.split('/api/')[-1])
        design_type = resp.json_data.get("Name")
        fabric_design = {"Name": design_type}
    return fabric_design


def get_current_payload(fabric_details, rest_obj):
    """
    extract payload from existing fabric details, which is
     obtained from GET request of existing fabric, to match with payload created
    :param fabric_details: dict - specified fabric details
    :return: dict
    """
    if fabric_details.get("OverrideLLDPConfiguration") and fabric_details.get("OverrideLLDPConfiguration") not in\
            ["Enabled", "Disabled"]:
        fabric_details.pop("OverrideLLDPConfiguration", None)
    payload = {
        "Id": fabric_details["Id"],
        "Name": fabric_details["Name"],
        "Description": fabric_details.get("Description"),
        "OverrideLLDPConfiguration": fabric_details.get("OverrideLLDPConfiguration"),
        "FabricDesignMapping": fabric_details.get("FabricDesignMapping", []),
        "FabricDesign": get_fabric_design(fabric_details["FabricDesign"].get("@odata.id"), rest_obj)

    }
    return dict([(k, v) for k, v in payload.items() if v])


def create_modify_payload(module_params, fabric_id, msm_version):
    """
    payload creation for fabric management in case of create/modify operations
    :param module_params: ansible module parameters
    :param fabric_id: fabric id in case of modify operation
    :param msm_version: msm version details
    :return: dict
    """
    backup_params = dict([(k, v) for k, v in module_params.items() if v])
    _payload = {
        "Name": backup_params["name"],
        "Description": backup_params.get("description"),
        "OverrideLLDPConfiguration": backup_params.get("override_LLDP_configuration"),
        "FabricDesignMapping": [
        ],
        "FabricDesign": {
        }
    }
    if backup_params.get("primary_switch_service_tag"):
        _payload["FabricDesignMapping"].append({
            "DesignNode": "Switch-A",
            "PhysicalNode": backup_params["primary_switch_service_tag"]
        })
    if backup_params.get("secondary_switch_service_tag"):
        _payload["FabricDesignMapping"].append({
            "DesignNode": "Switch-B",
            "PhysicalNode": backup_params["secondary_switch_service_tag"]
        })
    if backup_params.get("fabric_design"):
        _payload.update({"FabricDesign": {"Name": backup_params["fabric_design"]}})
    if msm_version.startswith("1.0"):  # OverrideLLDPConfiguration attribute not supported in msm 1.0 version
        _payload.pop("OverrideLLDPConfiguration", None)
    if fabric_id:  # update id/name in case of modify operation
        _payload["Name"] = backup_params.get("new_name", backup_params["name"])
        _payload["Id"] = fabric_id
    payload = dict([(k, v) for k, v in _payload.items() if v])
    return payload


def get_fabric_id_details(name, all_fabrics):
    """
    obtain the fabric id using fabric name
    :param name: fabric name
    :param all_fabrics: All available fabric in the system
    :return: tuple
    1st item: fabric id
    2nd item: all details of fabric specified in dict
    """
    fabric_id, fabric_details = None, None
    for fabric_each in all_fabrics:
        if fabric_each["Name"] == name:
            fabric_id = fabric_each["Id"]
            fabric_details = fabric_each
            break
    return fabric_id, fabric_details


def validate_device_type(device_type_name, identifier, device_details, module):
    """
    Validation for iom and chassis device type and also design modes of model
    :param device_type_name: device type name eg: NETWORK_IOM, CHASSIS
    :param identifier: identifier to access device type name
    :param device_details: all details of device
    :param module: ansible module object
    :return: None
    """
    device_map = {
        "primary_switch_service_tag": "NETWORK_IOM",
        "secondary_switch_service_tag": "NETWORK_IOM",
        "hostname": "CHASSIS"
    }
    design_mode = module.params.get("fabric_design")
    if device_type_name != device_map[identifier]:
        module.fail_json(
            msg=DEVICE_SERVICE_TAG_TYPE_ERROR_MSG.format(identifier, device_map[identifier]))
    if device_type_name != "CHASSIS" and design_mode:
        design_model = design_mode.split("_")[0].split('2x')[-1]
        identifier_model = device_details["Model"]
        if design_model not in identifier_model:
            module.fail_json(
                msg=DESIGN_MODEL_ERROR_MSG.format(identifier, design_model))


def validate_service_tag(device_service_tag, identifier, device_type_map, rest_obj, module):
    """
    Validate the service tag and device type of device
    :param identifier: identifier options which required find service tag from module params
    primary_switch_service_tag, secondary_switch_service_tag, hostname
    :param device_service_tag: device service tag
    :param device_type_map: map to get the
    :param rest_obj: session object
    :param module: ansible module object
    :return: None
    """
    if device_service_tag is not None:
        device_id_details = rest_obj.get_device_id_from_service_tag(device_service_tag)
        device_details = device_id_details["value"]
        if device_id_details["Id"] is None:
            module.fail_json(msg=DEVICE_SERVICE_TAG_NOT_FOUND_ERROR_MSG.format(device_service_tag))
        identifier_device_type = device_details["Type"]
        validate_device_type(device_type_map[identifier_device_type], identifier, device_details, module)


def validate_devices(host_service_tag, rest_obj, module):
    """
    validate domain, primary switch and secondary switch devices
    :param host_service_tag: service tag of the hostname provided
    :param rest_obj: session object
    :param module: Ansible module object
    :return: None
    """
    primary = module.params.get("primary_switch_service_tag")
    secondary = module.params.get("secondary_switch_service_tag")
    if primary and secondary and primary == secondary:
        module.fail_json(msg=DUPLICATE_TAGS)
    device_type_map = rest_obj.get_device_type()
    validate_service_tag(host_service_tag, "hostname", device_type_map, rest_obj, module)
    validate_service_tag(primary,
                         "primary_switch_service_tag",
                         device_type_map, rest_obj, module)
    validate_service_tag(secondary,
                         "secondary_switch_service_tag",
                         device_type_map, rest_obj,
                         module)


def required_field_check_for_create(fabric_id, module):
    params = module.params
    if not fabric_id and not all([params.get("fabric_design"), params.get("primary_switch_service_tag"),
                                  params.get("secondary_switch_service_tag")]):
        module.fail_json(msg=REQUIRED_FIELD)


def process_output(name, fabric_resp, msg, fabric_id, rest_obj, module):
    """
    fabric management actions creation/update of smart fabric output details processing
    :param name: fabric name specified
    :param fabric_resp: json response from ome
    :param msg: specific message of create and modify operation
    :param fabric_id: fabric id in case of modify
    :param rest_obj: current session object
    :param module: Ansible module object
    :return: None
    """
    identifier = fabric_resp
    if fabric_id:
        identifier = fabric_id
    if isinstance(fabric_resp, dict):
        all_fabrics = rest_obj.get_all_items_with_pagination(FABRIC_URI)["value"]
        identifier, current_fabric_details = get_fabric_id_details(name, all_fabrics)
        if not identifier:
            identifier = ""
        module.exit_json(msg=msg, fabric_id=identifier, additional_info=fabric_resp, changed=True)
    module.exit_json(msg=msg, fabric_id=identifier, changed=True)


def create_modify_fabric(name, all_fabric, rest_obj, module):
    """
    fabric management actions creation/update of smart fabric
    :param all_fabric: all available fabrics in system
    :param rest_obj: current session object
    :param module: ansible module object
    :param name: fabric name specified
    :return: None
    """
    fabric_id, current_fabric_details = get_fabric_id_details(name, all_fabric)
    required_field_check_for_create(fabric_id, module)
    host_service_tag, msm_version = get_msm_device_details(rest_obj, module)
    validate_devices(host_service_tag, rest_obj, module)
    uri = FABRIC_URI
    expected_payload = create_modify_payload(module.params, fabric_id, msm_version)
    payload = dict(expected_payload)
    method = "POST"
    msg = "Fabric creation operation is initiated."
    current_payload = {}
    if fabric_id:
        current_payload = get_current_payload(current_fabric_details, rest_obj)
        method = "PUT"
        msg = "Fabric modification operation is initiated."
        uri = FABRIC_ID_URI.format(fabric_id=fabric_id)
        payload = merge_payload(expected_payload, current_payload, module)
    idempotency_check_for_state_present(fabric_id, current_payload, expected_payload, module)
    resp = rest_obj.invoke_request(method, uri, data=payload)
    fabric_resp = resp.json_data
    process_output(name, fabric_resp, msg, fabric_id, rest_obj, module)


def check_fabric_exits_for_state_absent(fabric_values, module, fabric_name):
    """
    idempotency check in case of state absent
    :param fabric_values: fabric details of existing fabric
    :param module: ansible module object
    :param fabric_name: fabric name
    :return: str -  fabric id
    """
    fabric_id, fabric_details = get_fabric_id_details(fabric_name, fabric_values)
    if module.check_mode and fabric_id is None:
        module.exit_json(msg=CHECK_MODE_CHANGE_NOT_FOUND_MSG)
    if module.check_mode and fabric_id is not None:
        module.exit_json(msg=CHECK_MODE_CHANGE_FOUND_MSG, changed=True)
    if not module.check_mode and fabric_id is None:
        module.exit_json(msg=FABRIC_NOT_FOUND_ERROR_MSG.format(fabric_name))
    return fabric_id


def delete_fabric(all_fabrics, rest_obj, module, name):
    """
    deletes the fabric specified
    :param all_fabrics: All available fabric in system
    :param rest_obj: session object
    :param module: ansible module object
    :param name: fabric name specified
    :return: None
    """
    fabric_id = check_fabric_exits_for_state_absent(all_fabrics, module, name)
    rest_obj.invoke_request("DELETE", FABRIC_ID_URI.format(fabric_id=fabric_id))
    module.exit_json(msg="Fabric deletion operation is initiated.", fabric_id=fabric_id, changed=True)


def fabric_actions(rest_obj, module):
    """
    fabric management actions
    :param rest_obj: session object
    :param module: ansible module object
    :return: None
    """
    module_params = module.params
    state = module_params["state"]
    name = module_params["name"]
    all_fabrics = rest_obj.get_all_items_with_pagination(FABRIC_URI)["value"]
    if state == "present":
        create_modify_fabric(name, all_fabrics, rest_obj, module)
    else:
        delete_fabric(all_fabrics, rest_obj, module, name)


def main():
    design_choices = ['2xMX5108n_Ethernet_Switches_in_same_chassis',
                      '2xMX9116n_Fabric_Switching_Engines_in_same_chassis',
                      '2xMX9116n_Fabric_Switching_Engines_in_different_chassis'
                      ]
    module = AnsibleModule(
        argument_spec={
            "hostname": {"required": True, "type": "str"},
            "username": {"required": True, "type": "str"},
            "password": {"required": True, "type": "str", "no_log": True},
            "port": {"required": False, "type": "int", "default": 443},
            "state": {"type": "str", "required": False, "default": "present", "choices": ['present', 'absent']},
            "name": {"required": True, "type": "str"},
            "new_name": {"required": False, "type": "str"},
            "description": {"required": False, "type": "str"},
            "fabric_design": {"required": False, "type": "str",
                              "choices": design_choices},
            "primary_switch_service_tag": {"required": False, "type": "str"},
            "secondary_switch_service_tag": {"required": False, "type": "str"},
            "override_LLDP_configuration": {"required": False, "type": "str", "choices": ['Enabled', 'Disabled']},
        },
        required_if=[['state', 'present', ('new_name', 'description', 'fabric_design', 'primary_switch_service_tag',
                                           'secondary_switch_service_tag', 'override_LLDP_configuration',), True]],
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            fabric_actions(rest_obj, module)
    except HTTPError as err:
        if err.code == 501:
            module.fail_json(msg=SYSTEM_NOT_SUPPORTED_ERROR_MSG, error_info=json.load(err))
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, TypeError, SSLError, ConnectionError, SSLValidationError) as err:
        module.fail_json(msg=str(err))


if __name__ == "__main__":
    main()
