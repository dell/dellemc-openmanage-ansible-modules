#!/usr/bin/python
# -*- coding: utf-8 -*-
# Dell OpenManage Ansible Modules
# Version 9.12.4
# Copyright (C) 2020-2025 Dell Inc. or its subsidiaries.  All Rights Reserved.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_identity_pool
short_description: Manages identity pool settings on OpenManage Enterprise
version_added: "2.1.0"
description: This module allows to create, modify, or delete a single identity pool on OpenManage Enterprise.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  state:
    description:
      - C(present) modifies an existing identity pool. If the provided I (pool_name) does not exist,
       it creates an identity pool.
       - C(absent) deletes an existing identity pool.
    type: str
    default: present
    choices: [present, absent]
  pool_name:
    type: str
    required: true
    description:
      - This option is mandatory for I(state) when creating, modifying and deleting an identity pool.
  new_pool_name:
    type: str
    description:
      - After creating an identity pool, I(pool_name) can be changed to I(new_pool_name).
      - This option is ignored when creating an identity pool.
  pool_description:
    type: str
    description:
      - Description of the identity pool.
  ethernet_settings:
    type: dict
    description:
      - Applicable for creating and modifying an identity pool using Ethernet settings.
      - I(starting_mac_address) and I(identity_count) are required to create an identity pool.
    suboptions:
      starting_mac_address:
        description: Starting MAC address of the ethernet setting.
        type: str
      identity_count:
        description: Number of MAC addresses.
        type: int
  fcoe_settings:
    type: dict
    description:
       - Applicable for creating and modifying an identity pool using FCoE settings.
       - I(starting_mac_address) and I(identity_count) are required to create an identity pool.
    suboptions:
      starting_mac_address:
        description: Starting MAC Address of the FCoE setting.
        type: str
      identity_count:
        description: Number of MAC addresses.
        type: int
  iscsi_settings:
    type: dict
    description:
      - Applicable for creating and modifying an identity pool using ISCSI settings.
      - I(starting_mac_address), I(identity_count), I(iqn_prefix), I(ip_range) and I(subnet_mask) are
       required to create an identity pool.
    suboptions:
      starting_mac_address:
        description: Starting MAC address of the iSCSI setting.This is required option for iSCSI setting.
        type: str
      identity_count:
        description: Number of MAC addresses.
        type: int
      initiator_config:
        type: dict
        description:
          - Applicable for creating and modifying an identity pool using iSCSI Initiator settings.
        suboptions:
          iqn_prefix:
            description: IQN prefix addresses.
            type: str
      initiator_ip_pool_settings:
        type: dict
        description:
           - Applicable for creating and modifying an identity pool using ISCSI Initiator IP pool settings.
        suboptions:
          ip_range:
            description: Range of non-multicast IP addresses.
            type: str
          subnet_mask:
            description: Subnet mask for I(ip_range).
            type: str
          gateway:
            description: IP address of gateway.
            type: str
          primary_dns_server:
            description: IP address of the primary DNS server.
            type: str
          secondary_dns_server:
            description: IP address of the secondary DNS server.
            type: str
  fc_settings:
    type: dict
    description:
       - Applicable for creating and modifying an identity pool using fibre channel(FC) settings.
       - This option allows OpenManage Enterprise to generate a Worldwide port name (WWPN) and Worldwide node name (WWNN) address.
       - The value 0x2001 is beginning to the starting address for the generation of a WWPN, and 0x2000 for a WWNN.
       - I(starting_address) and I(identity_count) are required to create an identity pool.
    suboptions:
      starting_address:
        description: Starting MAC Address of FC setting.I(starting_address) is required to option to create FC settings.
        type: str
      identity_count:
        description: Number of MAC addresses.I(identity_count) is required to option to create FC settings.
        type: int
requirements:
    - "python >= 3.9.6"
author:
    - "Sajna Shetty(@Sajna-Shetty)"
    - "Deepak Joshi(@Dell-Deepak-Joshi))"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Create an identity pool using ethernet, FCoE, iSCSI and FC settings
  dellemc.openmanage.ome_identity_pool:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: present
    pool_name: "pool1"
    pool_description: "Identity pool with Ethernet, FCoE, iSCSI and FC settings"
    ethernet_settings:
      starting_mac_address: "50:50:50:50:50:00"
      identity_count: 60
    fcoe_settings:
      starting_mac_address: "70:70:70:70:70:00"
      identity_count: 75
    iscsi_settings:
      starting_mac_address: "60:60:60:60:60:00"
      identity_count: 30
      initiator_config:
        iqn_prefix: "iqn.myprefix."
      initiator_ip_pool_settings:
        ip_range: "10.33.0.1-10.33.0.255"
        subnet_mask: "255.255.255.0"
        gateway: "192.168.4.1"
        primary_dns_server: "10.8.8.8"
        secondary_dns_server: "8.8.8.8"
    fc_settings:
      starting_address: "30:30:30:30:30:00"
      identity_count: 45

- name: Create an identity pool using only ethernet settings
  dellemc.openmanage.ome_identity_pool:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    pool_name: "pool2"
    pool_description: "create identity pool with ethernet"
    ethernet_settings:
      starting_mac_address: "aa-bb-cc-dd-ee-aa"
      identity_count: 80

- name: Modify an identity pool
  dellemc.openmanage.ome_identity_pool:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    pool_name: "pool2"
    new_pool_name: "pool3"
    pool_description: "modifying identity pool with ethernet and fcoe settings"
    ethernet_settings:
      starting_mac_address: "90-90-90-90-90-90"
      identity_count: 61
    fcoe_settings:
      starting_mac_address: "aabb.ccdd.5050"
      identity_count: 77

- name: Modify an identity pool using iSCSI and FC settings
  dellemc.openmanage.ome_identity_pool:
    hostname: "{{hostname}}"
    username: "{{username}}"
    password: "{{password}}"
    ca_path: "/path/to/ca_cert.pem"
    pool_name: "pool_new"
    new_pool_name: "pool_new2"
    pool_description: "modifying identity pool with iscsi and fc settings"
    iscsi_settings:
      identity_count: 99
      initiator_config:
        iqn_prefix: "iqn1.myprefix2."
      initiator_ip_pool_settings:
        gateway: "192.168.4.5"
    fc_settings:
      starting_address: "10:10:10:10:10:10"
      identity_count: 98

- name: Delete an identity pool
  dellemc.openmanage.ome_identity_pool:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "absent"
    pool_name: "pool2"
'''

RETURN = r'''
---
msg:
  type: str
  description: Overall status of the identity pool operation.
  returned: always
  sample: "Successfully created an identity pool."
pool_status:
  type: dict
  description: Details of the user operation, when I(state) is C(present).
  returned: success
  sample: {
            "Id":29,
            "IsSuccessful":True,
            "Issues":[]
        }
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample:  {
  "error": {
           "@Message.ExtendedInfo": [{
           "Message": "Unable to process the request because an error occurred:
            Ethernet-MAC Range overlap found (in this Identity Pool or in a different one) .",
           "MessageArgs": [Ethernet-MAC Range overlap found (in this Identity Pool or in a different one)"],
           "MessageId": "CGEN6001",
           "RelatedProperties": [],
           "Resolution": "Retry the operation. If the issue persists, contact your system administrator.",
           "Severity": "Critical"
           }],
  "code": "Base.1.0.GeneralError",
  "message": "A general error has occurred. See ExtendedInfo for more information."
  }}
'''

import re
import json
import codecs
import binascii
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.urls import ConnectionError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError

IDENTITY_URI = "IdentityPoolService/IdentityPools"
CHANGES_FOUND = "Changes found to be applied."
NO_CHANGES_FOUND = "No changes found to be applied."


def get_identity_pool_id_by_name(pool_name, rest_obj):
    pool_id = 0
    attributes = None
    identity_list = rest_obj.get_all_report_details(IDENTITY_URI)["report_list"]
    for item in identity_list:
        if pool_name == item["Name"]:
            pool_id = item["Id"]
            attributes = item
            break
    return pool_id, attributes


def mac_validation(mac_input):
    match_found = re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$|"
                           "([0-9a-f]{4}([.])[0-9a-f]{4}([.])[0-9a-f]{4})$",
                           mac_input.lower())
    return match_found


def mac_to_base64_conversion(mac_address, module):
    try:
        if mac_address:
            allowed_mac_separators = [':', '-', '.']
            for sep in allowed_mac_separators:
                if sep in mac_address:
                    b64_mac_address = codecs.encode(codecs.decode(
                        mac_address.replace(sep, ''), 'hex'), 'base64')
                    address = codecs.decode(b64_mac_address, 'utf-8').rstrip()
                    return address
    except binascii.Error:
        module.exit_json(msg='Encoding of MAC address {0} to base64 '
                             'failed'.format(mac_address), failed=True)


def update_modify_setting(modify_payload, existing_payload, setting_type, sub_keys):
    """update current pool sub setting to modify payload if not provided
     in the options to avoid the null update from ome"""
    for sub_key in sub_keys:
        if sub_key not in modify_payload[setting_type] and sub_key in existing_payload[setting_type]:
            modify_payload[setting_type][sub_key] = existing_payload[setting_type][sub_key]
        elif existing_payload[setting_type]:
            if modify_payload[setting_type].get(sub_key) and existing_payload[setting_type].get(sub_key):
                modify_setting = modify_payload[setting_type][sub_key]
                existing_setting_payload = existing_payload[setting_type][sub_key]
                diff_item = list(set(existing_setting_payload) - set(modify_setting))
                for key in diff_item:
                    modify_payload[setting_type][sub_key][key] = existing_setting_payload[key]


def get_updated_modify_payload(modify_payload, existing_payload):
    """update current pool setting to modify payload if not provided
     in the options to avoid the null update from ome"""
    remove_unwanted_key_list = ['@odata.type', '@odata.id', 'CreatedBy', 'CreationTime', 'LastUpdatedBy',
                                'LastUpdateTime', 'UsageCounts', 'UsageIdentitySets@odata.navigationLink']
    [existing_payload.pop(key) for key in remove_unwanted_key_list if key in existing_payload]
    for key, val in existing_payload.items():
        if key not in modify_payload:
            modify_payload[key] = val
        else:
            if existing_payload.get(key) and key == "EthernetSettings" or key == "FcoeSettings":
                update_modify_setting(modify_payload, existing_payload, key, ["Mac"])
            elif existing_payload.get(key) and key == "FcSettings":
                update_modify_setting(modify_payload, existing_payload, key, ["Wwnn", "Wwpn"])
            elif existing_payload.get(key) and key == "IscsiSettings":
                update_modify_setting(modify_payload, existing_payload, key,
                                      ["Mac", "InitiatorConfig", "InitiatorIpPoolSettings"])
    modify_payload = {k: v for k, v in modify_payload.items() if v is not None}
    return modify_payload


def update_mac_settings(payload, settings_params, setting_type, module):
    """payload update for ethernet and fcoe settings and isci settings
    and convert to MAC address to base 64 format"""
    mac_address = settings_params.get("starting_mac_address")
    mac_base_64_format = None
    if mac_address:
        match_found = mac_validation(mac_address)
        if match_found:
            mac_base_64_format = mac_to_base64_conversion(mac_address, module)
        else:
            module.exit_json(msg="Please provide the valid MAC address format for {0} settings."
                             .format(setting_type.split('Settings')[0]), failed=True)
    sub_setting_mapper = {"StartingMacAddress": mac_base_64_format,
                          "IdentityCount": settings_params.get("identity_count")}
    sub_settings_payload = {k: v for k, v in sub_setting_mapper.items() if v is not None}
    if any(sub_settings_payload):
        payload.update({setting_type: {"Mac": sub_settings_payload}})


def update_iscsi_specific_settings(payload, settings_params, setting_type):
    """payload update for Iscsi specific settings"""
    sub_setting_mapper = {}
    initiator_config = settings_params.get("initiator_config")
    if initiator_config and initiator_config.get("iqn_prefix"):
        sub_setting_mapper.update({
            "InitiatorConfig": {"IqnPrefix": initiator_config.get("iqn_prefix")}})
    if settings_params.get("initiator_ip_pool_settings"):
        initiator_ip_pool_settings = settings_params["initiator_ip_pool_settings"]
        initiator_ip_pool_settings = {"IpRange": initiator_ip_pool_settings.get("ip_range"),
                                      "SubnetMask": initiator_ip_pool_settings.get("subnet_mask"),
                                      "Gateway": initiator_ip_pool_settings.get("gateway"),
                                      "PrimaryDnsServer": initiator_ip_pool_settings.get("primary_dns_server"),
                                      "SecondaryDnsServer": initiator_ip_pool_settings.get("secondary_dns_server")}
        initiator_ip_pool_settings = {k: v for k, v in initiator_ip_pool_settings.items() if v is not None}
        sub_setting_mapper.update({
            "InitiatorIpPoolSettings": initiator_ip_pool_settings})
    if any(sub_setting_mapper):
        if "IscsiSettings" in payload:
            """update MAC address setting"""
            sub_setting_mapper.update(payload[setting_type])
        sub_setting_mapper = {key: val for key, val in sub_setting_mapper.items() if any(val)}
        payload.update({setting_type: sub_setting_mapper})


def get_wwn_address_prefix(starting_address):
    """Prefix wwnn and wwpn MAC address with 20x00 and 20x01 respectively"""
    delimiter, wwnn_prefix, wwpn_prefix = None, None, None
    if "." in starting_address:
        delimiter = "."
    elif ":" in starting_address:
        delimiter = ":"
    elif "-" in starting_address:
        delimiter = "-"
    length = len(starting_address.split(delimiter)[0])
    if length == 4:
        wwnn_prefix = "2000{0}".format(delimiter)
        wwpn_prefix = "2001{0}".format(delimiter)
    else:
        wwnn_prefix = "20{0}00{0}".format(delimiter)
        wwpn_prefix = "20{0}01{0}".format(delimiter)
    return wwnn_prefix, wwpn_prefix


def update_fc_settings(payload, settings_params, setting_type, module):
    """payload update for Fibre Channel specific settings
    payload: other setting payload
    settings_params: fc setting parameters
    setting_type: "FcSettings"
    """
    sub_setting_mapper = {}
    starting_address = settings_params.get("starting_address")
    identity_count = settings_params.get("identity_count")
    wwnn_payload = {}
    wwpn_payload = {}
    if starting_address:
        if not mac_validation(starting_address):
            module.exit_json(msg="Please provide the valid starting address format for FC settings.",
                             failed=True)
        wwnn_prefix, wwpn_prefix = get_wwn_address_prefix(starting_address)
        wwnn_address = mac_to_base64_conversion(wwnn_prefix + starting_address, module)
        wwpn_address = mac_to_base64_conversion(wwpn_prefix + starting_address, module)
        wwnn_payload.update({"StartingAddress": wwnn_address})
        wwpn_payload.update({"StartingAddress": wwpn_address})
    if identity_count is not None:
        wwnn_payload.update({"IdentityCount": identity_count})
        wwpn_payload.update({"IdentityCount": identity_count})
    sub_setting_mapper.update({"Wwnn": wwnn_payload,
                               "Wwpn": wwpn_payload})
    sub_setting_mapper = {key: val for key, val in sub_setting_mapper.items() if any(val)}
    if any(sub_setting_mapper):
        payload.update({setting_type: sub_setting_mapper})


def get_payload(module, pool_id=None):
    """create payload for create and modify operations"""
    module_params = module.params
    setting_payload = {
        "Description": module_params.get("pool_description"),
        "Name": module_params["pool_name"]
    }
    fcoe_settings_params = module_params.get("fcoe_settings")
    ethernet_settings_params = module_params.get("ethernet_settings")
    iscsi_settings_params = module_params.get("iscsi_settings")
    fc_settings_params = module_params.get("fc_settings")
    if fcoe_settings_params:
        update_mac_settings(setting_payload, fcoe_settings_params, "FcoeSettings", module)
    if ethernet_settings_params:
        update_mac_settings(setting_payload, ethernet_settings_params, "EthernetSettings", module)
    if iscsi_settings_params:
        update_mac_settings(setting_payload, iscsi_settings_params, "IscsiSettings", module)
        update_iscsi_specific_settings(setting_payload, iscsi_settings_params, "IscsiSettings")
    if fc_settings_params:
        update_fc_settings(setting_payload, fc_settings_params, "FcSettings", module)
    if pool_id:
        new_name = module_params.get("new_pool_name")
        if new_name is not None:
            setting_payload.update({"Name": new_name})
        setting_payload["Id"] = pool_id
    payload = {k: v for k, v in setting_payload.items() if v is not None}
    return payload


def compare_nested_dict(modify_setting_payload, existing_setting_payload):
    """compare existing and requested setting values of identity pool in case of modify operations
    if both are same return True"""
    for key, val in modify_setting_payload.items():
        if existing_setting_payload is None or existing_setting_payload.get(key) is None:
            return False
        elif isinstance(val, dict):
            if not compare_nested_dict(val, existing_setting_payload.get(key)):
                return False
        elif val != existing_setting_payload.get(key):
            return False
    return True


def validate_modify_create_payload(setting_payload, module, action):
    for key, val in setting_payload.items():
        if key in ["EthernetSettings", "FcoeSettings"] and val:
            sub_config = val.get("Mac")
            if sub_config is None or not all([sub_config.get("IdentityCount"), sub_config.get("StartingMacAddress")]):
                module.exit_json(msg="Both starting MAC address and identity "
                                     "count is required to {0} an identity pool "
                                     "using {1} settings.".format(action, ''.join(key.split('Settings'))),
                                 failed=True)
        elif key == "FcSettings" and val:
            sub_config = val.get("Wwnn")
            validate_fc_settings(sub_config, module, action)
        elif key == "IscsiSettings" and val:
            validate_iscsi_settings(val, module, action, key)


def validate_fc_settings(sub_config, module, action):
    if sub_config is None or not all([sub_config.get("IdentityCount"), sub_config.get("StartingAddress")]):
        module.exit_json(msg="Both starting MAC address and identity count is "
                             "required to {0} an identity pool using Fc settings.".format(action),
                         failed=True)


def validate_iscsi_settings(val, module, action, key):
    """
    Validate iscsi settings for modify and create operations.
    """
    sub_config1 = val.get("Mac")
    sub_config2 = val.get("InitiatorIpPoolSettings")
    if sub_config1 is None or not all([sub_config1.get("IdentityCount"), sub_config1.get("StartingMacAddress")]):
        module.exit_json(msg="Both starting MAC address and identity count is "
                             "required to {0} an identity pool using {1} "
                             "settings.".format(action, ''.join(key.split('Settings'))),
                         failed=True)
    elif sub_config2:
        if not all([sub_config2.get("IpRange"), sub_config2.get("SubnetMask")]):
            module.exit_json(msg="Both ip range and subnet mask in required to"
                                 " {0} an identity pool using iSCSI settings.".format(action),
                             failed=True)


def pool_create_modify(module, rest_obj):
    pool_name = module.params["pool_name"]
    pool_id, existing_payload = get_identity_pool_id_by_name(pool_name, rest_obj)
    method = "POST"
    uri = IDENTITY_URI
    action = "create"
    setting_payload = get_payload(module, pool_id)
    if pool_id:
        action = "modify"
        method = "PUT"
        uri = uri + "({0})".format(pool_id)
        if compare_nested_dict(setting_payload, existing_payload):
            module.exit_json(msg=NO_CHANGES_FOUND)
        else:
            setting_payload = get_updated_modify_payload(setting_payload, existing_payload)
    validate_modify_create_payload(setting_payload, module, action)
    if module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    resp = rest_obj.invoke_request(method, uri, data=setting_payload)
    msg = get_success_message(action, resp.json_data)
    return msg


def pool_delete(module, rest_obj):
    pool_name = module.params["pool_name"]
    pool_id, _ = get_identity_pool_id_by_name(pool_name, rest_obj)  # pylint: disable=disallowed-name
    if not pool_id:
        message = "The identity pool '{0}' is not present in the system.".format(pool_name)
        module.exit_json(msg=message)
    method = "DELETE"
    uri = IDENTITY_URI + "({0})".format(pool_id)
    if module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    rest_obj.invoke_request(method, uri)
    return {"msg": "Successfully deleted the identity pool."}


def get_success_message(action, resp_data):
    message = {
        "create": "Successfully created an identity pool.",
        "modify": "Successfully modified the identity pool."
    }
    return {"msg": message[action], "result": resp_data}


def main():
    settings_options = {"starting_mac_address": {"type": 'str'},
                        "identity_count": {"type": 'int'}}
    iscsi_specific_settings = {"starting_mac_address": {"type": 'str'},
                               "identity_count": {"type": 'int'},
                               "initiator_config": {"options": {"iqn_prefix": {"type": 'str'}}, "type": "dict"},
                               "initiator_ip_pool_settings": {"options": {"ip_range": {"type": 'str'},
                                                                          "subnet_mask": {"type": 'str'},
                                                                          "gateway": {"type": 'str'},
                                                                          "primary_dns_server": {"type": 'str'},
                                                                          "secondary_dns_server": {"type": 'str'}},
                                                              "type": "dict"}}
    fc_settings = {"starting_address": {"type": "str"}, "identity_count": {"type": "int"}}

    specs = {
        "state": {"type": "str", "required": False, "default": "present", "choices": ['present', 'absent']},
        "pool_name": {"required": True, "type": "str"},
        "new_pool_name": {"required": False, "type": "str"},
        "pool_description": {"required": False, "type": "str"},
        "ethernet_settings": {"required": False, "type": "dict",
                              "options": settings_options},
        "fcoe_settings": {"required": False, "type": "dict", "options": settings_options},
        "iscsi_settings": {"required": False, "type": "dict",
                           "options": iscsi_specific_settings},
        "fc_settings": {"required": False, "type": "dict", "options": fc_settings},
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            state = module.params["state"]
            if state == "present":
                message = pool_create_modify(module, rest_obj)
                module.exit_json(msg=message["msg"], pool_status=message["result"], changed=True)
            else:
                message = pool_delete(module, rest_obj)
                module.exit_json(msg=message["msg"], changed=True)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True, failed=True)
    except (IOError, ValueError, TypeError, ConnectionError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == "__main__":
    main()
