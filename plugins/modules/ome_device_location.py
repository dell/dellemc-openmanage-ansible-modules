#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.1
# Copyright (C) 2021-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: ome_device_location
short_description: Configure device location settings on OpenManage Enterprise Modular
description: This module allows to configure the device location settings of the chassis
  on OpenManage Enterprise Modular.
version_added: "4.2.0"
extends_documentation_fragment:
  - dellemc.openmanage.omem_auth_options
options:
  device_id:
    type: int
    description:
      - The ID of the chassis for which the settings need to be updated.
      - If the device ID is not specified, this module updates
        the location settings for the I(hostname).
      - I(device_id) is mutually exclusive with I(device_service_tag).
  device_service_tag:
    type: str
    description:
      - The service tag of the chassis for which the settings need to be updated.
      - If the device service tag is not specified, this module updates
        the location settings for the I(hostname).
      - I(device_service_tag) is mutually exclusive with I(device_id).
  data_center:
    type: str
    description: The data center name of the chassis.
  room:
    type: str
    description: The room of the chassis.
  aisle:
    type: str
    description: The aisle of the chassis.
  rack:
    type: str
    description: The rack name of the chassis.
  rack_slot:
    type: int
    description: The rack slot number of the chassis.
  location:
    type: str
    description: The physical location of the chassis.
requirements:
  - "python >= 3.9.6"
author:
  - "Felix Stephen (@felixs88)"
notes:
  - Run this module from a system that has direct access to Dell OpenManage Enterprise Modular.
  - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Update device location settings of a chassis using the device ID.
  dellemc.openmanage.ome_device_location:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_id: 25011
    data_center: data center 1
    room: room 1
    aisle: aisle 1
    rack: rack 1
    rack_slot: 2
    location: location 1

- name: Update device location settings of a chassis using the device service tag.
  dellemc.openmanage.ome_device_location:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_service_tag: GHRT2RL
    data_center: data center 2
    room: room 7
    aisle: aisle 4
    rack: rack 6
    rack_slot: 22
    location: location 5

- name: Update device location settings of the host chassis.
  dellemc.openmanage.ome_device_location:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    data_center: data center 3
    room: room 3
    aisle: aisle 1
    rack: rack 7
    rack_slot: 10
    location: location 9
"""

RETURN = """
---
msg:
  type: str
  description: Overall status of the device location settings.
  returned: always
  sample: "Successfully updated the location settings."
location_details:
  type: dict
  description: returned when location settings are updated successfully.
  returned: success
  sample: {
    "Aisle": "aisle 1",
    "DataCenter": "data center 1",
    "Location": "location 1",
    "RackName": "rack 1",
    "RackSlot": 2,
    "Room": "room 1",
    "SettingType": "Location"
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
"""


import json
import socket
from ssl import SSLError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule

LOCATION_API = "DeviceService/Devices({0})/Settings('Location')"
DEVICE_URI = "DeviceService/Devices"
DOMAIN_URI = "ManagementDomainService/Domains"
DEVICE_FAIL_MSG = "Unable to complete the operation because the entered target device {0} '{1}' is invalid."


def check_domain_service(module, rest_obj):
    try:
        rest_obj.invoke_request("GET", DOMAIN_URI, api_timeout=5)
    except HTTPError as err:
        err_message = json.load(err)
        if err_message["error"]["@Message.ExtendedInfo"][0]["MessageId"] == "CGEN1006":
            module.exit_json(msg="The device location settings operation is supported only on "
                                 "OpenManage Enterprise Modular systems.", failed=True)
    return


def validate_dictionary(module, loc_resp):
    data_center = module.params.get("data_center")
    room = module.params.get("room")
    aisle = module.params.get("aisle")
    rack = module.params.get("rack")
    rack_slot = module.params.get("rack_slot")
    location = module.params.get("location")
    req_dict = {"DataCenter": data_center, "Room": room, "Aisle": aisle, "RackName": rack, "Location": location}
    req_filter_none = dict((k, v) for k, v in req_dict.items() if v is not None)
    keys = list(req_filter_none.keys())
    exit_dict = dict((k, v) for k, v in loc_resp.items() if k in keys and v is not None)
    if rack_slot is not None:
        req_dict.update({"RackSlot": rack_slot})
        req_filter_none.update({"RackSlot": rack_slot})
        exit_dict.update({"RackSlot": loc_resp["RackSlot"]})
    diff = bool(set(req_filter_none.items()) ^ set(exit_dict.items()))
    if not diff and not module.check_mode:
        module.exit_json(msg="No changes found to be applied.")
    elif not diff and module.check_mode:
        module.exit_json(msg="No changes found to be applied.")
    elif diff and module.check_mode:
        module.exit_json(msg="Changes found to be applied.", changed=True)
    payload_dict = {"SettingType": "Location"}
    payload_dict.update(dict((k, v) for k, v in loc_resp.items() if k in req_dict.keys()))
    payload_dict.update(req_filter_none)
    if req_filter_none.get("RackSlot") is None:
        payload_dict.update({"RackSlot": loc_resp.get("RackSlot")})
    return payload_dict


def get_ip_from_host(hostname):
    ipaddr = hostname
    try:
        result = socket.getaddrinfo(hostname, None)
        last_element = result[-1]
        ip_address = last_element[-1][0]
        if ip_address:
            ipaddr = ip_address
    except socket.gaierror:
        ipaddr = hostname
    except Exception:
        ipaddr = hostname
    return ipaddr


def standalone_chassis(module, rest_obj):
    key, value = None, None
    ipaddress = get_ip_from_host(module.params["hostname"])
    resp = rest_obj.invoke_request("GET", DOMAIN_URI)
    for data in resp.json_data["value"]:
        if ipaddress in data["PublicAddress"]:
            key, value = ("Id", data["DeviceId"])
            break
    else:
        module.exit_json(msg="Failed to fetch the device information.", failed=True)
    return key, value


def device_validation(module, rest_obj):
    final_resp = {}
    device_id, tag = module.params.get("device_id"), module.params.get("device_service_tag")
    if device_id is None and tag is None:
        key, value = standalone_chassis(module, rest_obj)
        device_id = value
    else:
        key, value = ("Id", device_id) if device_id is not None else ("DeviceServiceTag", tag)
        param_value = "{0} eq {1}".format(key, value) if key == "Id" else "{0} eq '{1}'".format(key, value)
        resp = rest_obj.invoke_request("GET", DEVICE_URI, query_param={"$filter": param_value})
        resp_data = resp.json_data.get("value")
        rename_key = "id" if key == "Id" else "service tag"
        if not resp_data:
            module.exit_json(msg=DEVICE_FAIL_MSG.format(rename_key, value), failed=True)
        if key == "DeviceServiceTag" and resp_data[0]["DeviceServiceTag"] == tag:
            device_id = resp_data[0]["Id"]
        elif key == "Id" and resp_data[0]["Id"] == device_id:
            device_id = resp_data[0]["Id"]
        else:
            module.exit_json(msg=DEVICE_FAIL_MSG.format(rename_key, value), failed=True)
    try:
        loc_resp = rest_obj.invoke_request("GET", LOCATION_API.format(device_id))
    except HTTPError as err:
        err_message = json.load(err)
        error_msg = err_message.get('error', {}).get('@Message.ExtendedInfo')
        if error_msg and error_msg[0].get("MessageId") == "CGEN1004":
            module.exit_json(msg="Unable to complete the operation because the location settings "
                                 "are not supported on the specified device.", failed=True)
    else:
        payload = validate_dictionary(module, loc_resp.json_data)
        final_resp = rest_obj.invoke_request("PUT", LOCATION_API.format(device_id), data=payload)
    return final_resp


def main():
    specs = {
        "device_id": {"required": False, "type": "int"},
        "device_service_tag": {"required": False, "type": "str"},
        "data_center": {"required": False, "type": "str"},
        "room": {"required": False, "type": "str"},
        "aisle": {"required": False, "type": "str"},
        "rack": {"required": False, "type": "str"},
        "rack_slot": {"required": False, "type": "int"},
        "location": {"required": False, "type": "str"},
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[('device_id', 'device_service_tag')],
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            check_domain_service(module, rest_obj)
            resp = device_validation(module, rest_obj)
            module.exit_json(msg="Successfully updated the location settings.",
                             location_details=resp.json_data, changed=True)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, AttributeError, IndexError, KeyError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
