#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2022-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_smart_fabric_uplink_info
short_description: Retrieve details of fabric uplink on OpenManage Enterprise Modular.
version_added: "7.1.0"
description: This module retrieve details of fabric uplink on OpenManage Enterprise Modular.
extends_documentation_fragment:
  - dellemc.openmanage.omem_auth_options
options:
  fabric_id:
    type: str
    description:
      - Unique id of the fabric.
      - I(fabric_id) is mutually exclusive with I(fabric_name).
  fabric_name:
    type: str
    description:
      - Unique name of the fabric.
      - I(fabric_name) is mutually exclusive with I(fabric_id).
  uplink_id:
    type: str
    description:
      - Unique id of the uplink.
      - I(uplink_id) is mutually exclusive with I(uplink_name).
      - I(fabric_id) or I(fabric_name) is required along with I(uplink_id).
  uplink_name:
    type: str
    description:
      - Unique name of the uplink.
      - I(uplink_name) is mutually exclusive with I(uplink_id).
      - I(fabric_id) or I(fabric_name) is required along with I(uplink_name).
requirements:
    - "python >= 3.9.6"
author:
    - "Husniya Hameed(@husniya_hameed)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise Modular.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Retrieve all fabric uplink information using fabric_id.
  dellemc.openmanage.ome_smart_fabric_uplink_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    fabric_id: "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2"

- name: Retrieve all fabric uplink information using fabric_name.
  dellemc.openmanage.ome_smart_fabric_uplink_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    fabric_name: "f1"

- name: Retrieve specific fabric information using uplink_id.
  dellemc.openmanage.ome_smart_fabric_uplink_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    fabric_id: "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2"
    uplink_id: "1ad54420-b145-49a1-9779-21a579ef6f2d"

- name: Retrieve specific fabric information using uplink_name.
  dellemc.openmanage.ome_smart_fabric_uplink_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    fabric_id: "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2"
    uplink_name: "u1"
'''

RETURN = r'''
---
msg:
  type: str
  description: Status of fabric uplink information retrieval.
  returned: always
  sample: "Successfully retrieved the fabric uplink information."
uplink_info:
  type: list
  description: Information about the fabric uplink.
  returned: on success
  sample: [{
    "Description": "",
    "Id": "1ad54420-b145-49a1-9779-21a579ef6f2d",
    "MediaType": "Ethernet",
    "Name": "u1",
    "NativeVLAN": 1,
    "Networks": [{
      "CreatedBy": "system",
      "CreationTime": "2018-09-25 14:46:12.374",
      "Description": null,
      "Id": 10155,
      "InternalRefNWUUId": "f15a36b6-e3d3-46b2-9e7d-bf9cd66e180d",
      "Name": "testvlan",
      "Type": 1,
      "UpdatedBy": "root",
      "UpdatedTime": "2019-06-27 15:06:22.836",
      "VlanMaximum": 143,
      "VlanMinimum": 143
    }],
    "Ports": [{
      "AdminStatus": "Enabled",
      "BlinkStatus": "OFF",
      "ConfiguredSpeed": "0",
      "CurrentSpeed": "0",
      "Description": "",
      "Id": "SVCTAG1:ethernet1/1/35",
      "MaxSpeed": "0",
      "MediaType": "Ethernet",
      "Name": "",
      "NodeServiceTag": "SVCTAG1",
      "OpticsType": "NotPresent",
      "PortNumber": "ethernet1/1/35",
      "Role": "Uplink",
      "Status": "Down",
      "Type": "PhysicalEthernet"
    },
    {
      "AdminStatus": "Enabled",
      "BlinkStatus": "OFF",
      "ConfiguredSpeed": "0",
      "CurrentSpeed": "0",
      "Description": "",
      "Id": "SVCTAG1:ethernet1/1/35",
      "MaxSpeed": "0",
      "MediaType": "Ethernet",
      "Name": "",
      "NodeServiceTag": "SVCTAG1",
      "OpticsType": "NotPresent",
      "PortNumber": "ethernet1/1/35",
      "Role": "Uplink",
      "Status": "Down",
      "Type": "PhysicalEthernet"
    }],
    "Summary": {
      "NetworkCount": 1,
      "PortCount": 2
    },
    "UfdEnable": "Disabled"
  }]
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
                "MessageId": "CGEN1006",
                "RelatedProperties": [],
                "Message": "Unable to complete the request because the resource URI does not exist or is not implemented.",
                "MessageArgs": [],
                "Severity": "Critical",
                "Resolution": "Check the request resource URI. Refer to the OpenManage Enterprise-Modular User's Guide
                for more information about resource URI and its properties."
            }
        ]
    }
  }
'''

import json
from ssl import SSLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import strip_substr_dict

ALL_UPLINKS_URI = "NetworkService/Fabrics('{0}')/Uplinks?$expand=Networks,Ports"
FABRIC_URI = "NetworkService/Fabrics"
UPLINK_URI = "NetworkService/Fabrics('{0}')/Uplinks('{1}')?$expand=Networks,Ports"
#  Messages
SUCCESS_MSG = "Successfully retrieved the fabric uplink information."
UNSUCCESS_MSG = "Unable to retrieve smart fabric uplink information."
INVALID_FABRIC_ID = "Unable to retrieve smart fabric uplink information with fabric ID {0}."
INVALID_FABRIC_NAME = "Unable to retrieve smart fabric uplink information with fabric name {0}."
INVALID_UPLINK_ID = "Unable to retrieve smart fabric uplink information with uplink ID {0}."
INVALID_UPLINK_NAME = "Unable to retrieve smart fabric uplink information with uplink name {0}."
ID_UNAVAILABLE = "fabric_id or fabric_name is required along with uplink_id."
NAME_UNAVAILABLE = "fabric_id or fabric_name is required along with uplink_name."


def get_all_uplink_details(module, rest_obj):
    resp = []
    try:
        fabric_det = rest_obj.invoke_request("GET", FABRIC_URI)
        fabric_resp = fabric_det.json_data.get("value")
        for each in fabric_resp:
            if each.get("Uplinks@odata.navigationLink"):
                uplink_det = each.get("Uplinks@odata.navigationLink")
                uplink = uplink_det[5:] + "?$expand=Networks,Ports"
                uplink_details = rest_obj.invoke_request("GET", uplink)
                for val in uplink_details.json_data.get("value"):
                    resp.append(val)
    except HTTPError:
        module.exit_json(msg=UNSUCCESS_MSG, failed=True)
    return resp


def get_uplink_details_from_fabric_id(module, rest_obj, fabric_id):
    resp = []
    try:
        resp_det = rest_obj.invoke_request("GET", ALL_UPLINKS_URI.format(fabric_id))
        resp = resp_det.json_data.get("value")
    except HTTPError:
        module.exit_json(msg=INVALID_FABRIC_ID.format(fabric_id), failed=True)
    return resp


def get_fabric_id_from_name(module, rest_obj, fabric_name):
    fabric_id = ""
    try:
        resp_det = rest_obj.invoke_request("GET", FABRIC_URI)
        resp = resp_det.json_data.get("value")
        for each in resp:
            if each["Name"] == fabric_name:
                fabric_id = each["Id"]
                break
    except HTTPError:
        module.exit_json(msg=UNSUCCESS_MSG, failed=True)
    if not fabric_id:
        module.exit_json(msg=INVALID_FABRIC_NAME.format(fabric_name), failed=True)
    return fabric_id


def get_uplink_details(module, rest_obj, fabric_id, uplink_id):
    resp = []
    try:
        resp_det = rest_obj.invoke_request("GET", UPLINK_URI.format(fabric_id, uplink_id))
        resp = [resp_det.json_data]
    except HTTPError:
        module.exit_json(msg=INVALID_UPLINK_ID.format(uplink_id), failed=True)
    return resp


def get_uplink_id_from_name(module, rest_obj, uplink_name, fabric_id):
    uplink_id = ""
    try:
        resp_det = rest_obj.invoke_request("GET", ALL_UPLINKS_URI.format(fabric_id))
        resp = resp_det.json_data.get("value")
        for each in resp:
            if each["Name"] == uplink_name:
                uplink_id = each["Id"]
                break
    except HTTPError:
        module.exit_json(msg=UNSUCCESS_MSG, failed=True)
    if not uplink_id:
        module.exit_json(msg=INVALID_UPLINK_NAME.format(uplink_name), failed=True)
    return uplink_id


def strip_uplink_info(uplink_info):
    for item in uplink_info:
        item = strip_substr_dict(item)
        if item["Networks"]:
            for net in item["Networks"]:
                net = strip_substr_dict(net)
        if item["Ports"]:
            for port in item["Ports"]:
                port = strip_substr_dict(port)
    return uplink_info


def main():
    specs = {
        "fabric_id": {"type": "str"},
        "fabric_name": {"type": "str"},
        "uplink_id": {"type": "str"},
        "uplink_name": {"type": "str"}
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[('fabric_id', 'fabric_name'), ('uplink_id', 'uplink_name')],
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            uplink_info = []
            fabric_id = module.params["fabric_id"]
            fabric_name = module.params["fabric_name"]
            uplink_id = module.params["uplink_id"]
            uplink_name = module.params["uplink_name"]

            if fabric_id:
                uplink_info = get_uplink_details_from_fabric_id(module, rest_obj, fabric_id)
            elif fabric_name:
                fabric_id = get_fabric_id_from_name(module, rest_obj, fabric_name)
                if fabric_id:
                    uplink_info = get_uplink_details_from_fabric_id(module, rest_obj, fabric_id)

            if uplink_id and not (fabric_id or fabric_name):
                module.exit_json(msg=ID_UNAVAILABLE, failed=True)
            elif uplink_id:
                uplink_info = get_uplink_details(module, rest_obj, fabric_id, uplink_id)
            elif uplink_name and not (fabric_id or fabric_name):
                module.exit_json(msg=NAME_UNAVAILABLE, failed=True)
            elif uplink_name:
                uplink_id = get_uplink_id_from_name(module, rest_obj, uplink_name, fabric_id)
                if uplink_id:
                    uplink_info = get_uplink_details(module, rest_obj, fabric_id, uplink_id)

            if fabric_id is None and fabric_name is None and uplink_id is None and uplink_name is None:
                uplink_info = get_all_uplink_details(module, rest_obj)
                if not bool(uplink_info):
                    module.exit_json(msg=SUCCESS_MSG, uplink_info=uplink_info)

            uplink_info_strip = strip_uplink_info(uplink_info)
            module.exit_json(msg=SUCCESS_MSG, uplink_info=uplink_info_strip)

    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, TypeError, ConnectionError, SSLValidationError, SSLError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == "__main__":
    main()
