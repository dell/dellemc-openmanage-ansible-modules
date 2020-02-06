#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0.8
# Copyright (C) 2020 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ome_identity_pool
short_description: Manages identity pool settings.
version_added: "2.8"
description: This module allows to create, modify, or delete a single identity pool.
options:
  hostname:
    description: Target IP Address or hostname.
    required: true
    type: str
  username:
    description: Target username.
    required: true
    type: str
  password:
    description: Target user password.
    required: true
    type: str
  port:
    description: Target HTTPS port.
    default: 443
    type: int
  state:
    description:
      - C(present) modifies an existing identity pool. If the provided I (pool_name) does not exist,
       it creates a new identity pool.
    type: str
    required: False
    default: present
    choices: [present]
  pool_name:
    type: str
    required: True
    description:
      - This option is mandatory if I(command) is C(present) when creating and modifying an identity pool.
  new_pool_name:
    type: str
    required: False
    description:
      - After creating an identity pool, I(pool_name) can be changed to I(new_pool_name).
      - This option is ignored when creating an identity pool.
  pool_description:
    type: str
    required: False
    description:
      - Description of the identity pool.
  ethernet_settings:
    type: dict
    required: False
    description: Applicable for creating and modifying an identity pool using Ethernet settings.
    suboptions:
      starting_mac_address:
        description: Starting MAC Address.
        type: str
        required: False
      identity_count:
        description: Number of MAC addresses.
        type: int
        required: False
  fcoe_settings:
    type: dict
    required: False
    description: Applicable for creating and modifying an identity pool using Fcoe settings.
    suboptions:
      starting_mac_address:
        description: Starting MAC Address.
        type: str
        required: False
      identity_count:
        description: Number of MAC addresses.
        type: int
        required: False
requirements:
    - "python >= 2.7.5"
author:
    - "Sajna Shetty(@Sajna-Shetty)"
'''

EXAMPLES = r'''
---
- name: "Create an identity pool with ethernet_settings and fcoe_settings."
  ome_identity_pool:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    state: present
    pool_name: "pool1"
    pool_description: "Identity pool with ethernet and fcoe settings"
    ethernet_settings:
        starting_mac_address: "50:50:50:50:50:00"
        identity_count: 60
    fcoe_settings:
        starting_mac_address: "70:70:70:70:70:00"
        identity_count: 75

- name: "Create an identity pool with only ethernet_settings"
  ome_identity_pool:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    pool_name: "pool2"
    pool_description: "create identity pool with ethernet"
    ethernet_settings:
        starting_mac_address: "aa-bb-cc-dd-ee-aa"
        identity_count: 80

- name: "Modify an identity pool"
  ome_identity_pool:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    pool_name: "pool2"
    new_pool_name: "pool3"
    pool_description: "modifying identity pool with ethernet and fcoe settings"
    ethernet_settings:
        starting_mac_address: "90-90-90-90-90-90"
        identity_count: 61
    fcoe_settings:
        starting_mac_address: "aabb.ccdd.5050"
        identity_count: 77
'''

RETURN = r'''
---
msg:
  type: str
  description: "Overall status of the identity pool operation"
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
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.remote_management.dellemc.ome import RestOME
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError

identity_uri = "IdentityPoolService/IdentityPools"


def get_identity_pool_id_by_name(pool_name, rest_obj):
    pool_id = 0
    attributes = None
    identity_list = rest_obj.get_all_report_details(identity_uri)["report_list"]
    for item in identity_list:
        if pool_name == item["Name"]:
            pool_id = item["Id"]
            attributes = item
            break
    return pool_id, attributes


def mac_validation(mac_input):
    match_found = re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$|"
                           "([0-9a-f]{4}([.])[0-9a-f]{4}([.])[0-9a-f]{4})$", mac_input.lower())
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
        module.fail_json(msg='Encoding of mac address {0} to base64 '
                             'failed'.format(mac_address))


def update_modify_setting(modify_payload, existing_payload, type_setting):
    """update current pool setting values to ethernet and fcoe setting if not provided
     in the payload to avoid the null update from ome"""
    modify_setting = modify_payload[type_setting]["Mac"]
    existing_setting_payload = existing_payload[type_setting]["Mac"]
    diff_item = list(set(existing_setting_payload) - set(modify_setting))
    for key in diff_item:
        modify_payload[type_setting]["Mac"][key] = existing_setting_payload[key]


def update_settings(modify_payload, existing_payload):
    settings = ["EthernetSettings", "FcoeSettings"]
    for setting_type in settings:
        if existing_payload.get(setting_type) is not None:
            if setting_type in modify_payload:
                update_modify_setting(modify_payload, existing_payload, setting_type)
            else:
                modify_payload.update({setting_type: existing_payload[setting_type]})


def update_modify_payload(modify_payload, existing_payload):
    """pass the existing setting value for modify operation
     if not passed to avoid update of null values from ome"""
    if "Description" not in modify_payload and existing_payload.get("Description") is not None:
        modify_payload.update({"Description": existing_payload["Description"]})
    update_settings(modify_payload, existing_payload)


def update_ethernet_fcoe_settings(payload, settings_params, setting_type, module):
    """payload update for ethernet and fcoe settings
    and convert to mac address to base 64 format"""
    mac_address = settings_params.get("starting_mac_address")
    mac_base_64_format = None
    if mac_address:
        match_found = mac_validation(mac_address)
        if match_found:
            mac_base_64_format = mac_to_base64_conversion(mac_address, module)
        else:
            module.fail_json(msg="Please provide valid mac address format for {0}"
                             .format(setting_type).lower())
    sub_setting_mapper = {"StartingMacAddress": mac_base_64_format,
                          "IdentityCount": settings_params.get("identity_count")}
    sub_settings_payload = {k: v for k, v in sub_setting_mapper.items() if v is not None}
    if any(sub_settings_payload):
        payload.update({setting_type: {"Mac": sub_settings_payload}})


def get_payload(module, pool_id=None):
    """create payload for create and modify operations"""
    module_params = module.params
    setting_payload = {
        "Description": module_params.get("pool_description"),
        "Name": module_params["pool_name"]
    }
    fcoe_settings_params = module_params.get("fcoe_settings")
    ethernet_settings_params = module_params.get("ethernet_settings")
    if fcoe_settings_params:
        update_ethernet_fcoe_settings(setting_payload, fcoe_settings_params, "FcoeSettings", module)
    if ethernet_settings_params:
        update_ethernet_fcoe_settings(setting_payload, ethernet_settings_params, "EthernetSettings", module)
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
        if existing_setting_payload.get(key) is None:
            return False
        elif isinstance(val, dict):
            if not compare_nested_dict(val, existing_setting_payload.get(key)):
                return False
        elif val != existing_setting_payload.get(key):
            return False
    return True


def pool_create_modify(module, rest_obj):
    try:
        pool_name = module.params["pool_name"]
        pool_id, existing_payload = get_identity_pool_id_by_name(pool_name, rest_obj)
        method = "POST"
        uri = identity_uri
        action = "create"
        setting_payload = get_payload(module, pool_id)
        if pool_id:
            action = "modify"
            method = "PUT"
            uri = uri + "({0})".format(pool_id)
            if compare_nested_dict(setting_payload, existing_payload):
                module.exit_json(msg="No changes are to be applied for specified pool name: {0},"
                                     " as requested setting values are the same as the current"
                                     " setting values.".format(setting_payload["Name"]))
            else:
                update_modify_payload(setting_payload, existing_payload)
        resp = rest_obj.invoke_request(method, uri, data=setting_payload)
        msg = get_success_message(action, resp.json_data)
        return msg
    except (URLError, HTTPError, SSLValidationError, SSLError, ConnectionError, TypeError, ValueError) as err:
        raise err


def get_success_message(action, resp_data):
    message = {
        "create": "Successfully created an identity pool.",
        "modify": "Successfully modified the identity pool."
    }
    return {"msg": message[action], "result": resp_data}


def main():
    settings_options = {"starting_mac_address": {"type": 'str'},
                        "identity_count": {"type": 'int'}}
    module = AnsibleModule(
        argument_spec={
            "hostname": {"required": True, "type": "str"},
            "username": {"required": True, "type": "str"},
            "password": {"required": True, "type": "str", "no_log": True},
            "port": {"required": False, "type": "int", "default": 443},
            "state": {"type": "str",
                      "required": False,
                      "default": "present",
                      "choices": ['present']},
            "pool_name": {"required": True, "type": "str"},
            "new_pool_name": {"required": False, "type": "str"},
            "pool_description": {"required": False, "type": "str"},
            "ethernet_settings": {"required": False, "type": "dict",
                                  "options": settings_options},
            "fcoe_settings": {"required": False, "type": "dict", "options": settings_options},
        },
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            message = pool_create_modify(module, rest_obj)
            module.exit_json(msg=message["msg"], pool_status=message["result"], changed=True)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError) as err:
        module.fail_json(msg=str(err))


if __name__ == "__main__":
    main()
