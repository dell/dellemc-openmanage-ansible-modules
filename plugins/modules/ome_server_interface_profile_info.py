#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.1.0
# Copyright (C) 2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: ome_server_interface_profile_info
short_description: Retrieves the information of server interface profile on OpenManage Enterprise Modular.
description: This module allows to retrieves the information of server interface profile
  on OpenManage Enterprise Modular.
version_added: "5.1.0"
extends_documentation_fragment:
  - dellemc.openmanage.omem_auth_options
options:
  device_id:
    type: list
    description:
      - The ID of the device.
      - I(device_id) is mutually exclusive with I(device_service_tag).
    elements: int
  device_service_tag:
    type: list
    description:
      - The service tag of the device.
      - I(device_service_tag) is mutually exclusive with I(device_id).
    elements: str
requirements:
  - "python >= 3.8.6"
author:
  - "Felix Stephen (@felixs88)"
notes:
  - Run this module from a system that has direct access to OpenManage Enterprise Modular.
  - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Retrieves the server interface profiles of all the device using device ID.
  dellemc.openmanage.ome_server_interface_profile_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_id:
      - 10001
      - 10002

- name: Retrieves the server interface profiles of all the device using device service tag.
  dellemc.openmanage.ome_server_interface_profile_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_service_tag:
      - 6GHH6H2
      - 6KHH6H3
"""

RETURN = """
---
msg:
  type: str
  description: Overall status of the server interface profile information.
  returned: on success
  sample: "Successfully retrieved the server interface profile information."
server_profiles:
  type: list
  description: Returns the information of collected server interface profile information.
  returned: success
  sample: [
    {
      "BondingTechnology": "LACP",
      "Id": "6KZK6K2",
      "ServerInterfaceProfile": [
        {
          "FabricId": "1ea6bf64-3cf0-4e06-a136-5046d874d1e7",
          "Id": "NIC.Mezzanine.1A-1-1",
          "NativeVLAN": 0,
          "Networks": [
            {
              "CreatedBy": "system",
              "CreationTime": "2018-11-27 10:22:14.140",
              "Description": "VLAN 1",
              "Id": 10001,
              "InternalRefNWUUId": "add035b9-a971-400d-a3fa-bb365df1d476",
              Name": "VLAN 1",
              "Type": 2,
              "UpdatedBy": null,
              "UpdatedTime": "2018-11-27 10:22:14.140",
              "VlanMaximum": 1,
              "VlanMinimum": 1
            }
          ],
          "NicBonded": true,
          "OnboardedPort": "59HW8X2:ethernet1/1/1"
        },
        {
          "FabricId": "3ea6be04-5cf0-4e05-a136-5046d874d1e6",
          "Id": "NIC.Mezzanine.1A-2-1",
          "NativeVLAN": 0,
          "Networks": [
            {
              "CreatedBy": "system",
              "CreationTime": "2018-09-25 14:46:12.374",
              "Description": null,
              "Id": 10155,
              "InternalRefNWUUId": "f15a36b6-e3d3-46b2-9e7d-bf9cd66e180d",
              "Name": "jagvlan",
              "Type": 1,
              "UpdatedBy": null,
              "UpdatedTime": "2018-09-25 14:46:12.374",
              "VlanMaximum": 143,
              "VlanMinimum": 143
            }
          ],
          "NicBonded": false,
          "OnboardedPort": "6H7J6Z2:ethernet1/1/1"
        }
      ]
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
"""


import json
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params

DOMAIN_URI = "ManagementDomainService/Domains"
PROFILE_URI = "NetworkService/ServerProfiles"
DEVICE_URI = "DeviceService/Devices"
NETWORK_PROFILE_URI = "NetworkService/ServerProfiles('{0}')/ServerInterfaceProfiles"

DOMAIN_FAIL_MSG = "The information retrieval operation of server interface profile is supported only on " \
                  "OpenManage Enterprise Modular."
CONFIG_FAIL_MSG = "one of the following is required: device_id, device_service_tag."
INVALID_DEVICE = "Unable to complete the operation because the entered " \
                 "target device {0}(s) '{1}' are invalid."
PROFILE_ERR_MSG = "Unable to complete the operation because the server " \
                  "profile(s) for {0} do not exist in the Fabric Manager."
SUCCESS_MSG = "Successfully retrieved the server interface profile information."


def check_domain_service(module, rest_obj):
    try:
        rest_obj.invoke_request("GET", DOMAIN_URI, api_timeout=5)
    except HTTPError as err:
        err_message = json.load(err)
        if err_message["error"]["@Message.ExtendedInfo"][0]["MessageId"] == "CGEN1006":
            module.fail_json(msg=DOMAIN_FAIL_MSG)
    return


def get_sip_info(module, rest_obj):
    invalid, valid_service_tag, device_map = [], [], {}
    device_id, tag = module.params.get("device_id"), module.params.get("device_service_tag")
    key, value = ("Id", device_id) if device_id is not None else ("DeviceServiceTag", tag)
    resp_data = rest_obj.get_all_report_details(DEVICE_URI)
    if resp_data['report_list']:
        for each in value:
            each_device = list(filter(lambda d: d[key] in [each], resp_data["report_list"]))
            if each_device and key == "DeviceServiceTag":
                valid_service_tag.append(each)
            elif each_device and key == "Id":
                valid_service_tag.append(each_device[0]["DeviceServiceTag"])
                device_map[each_device[0]["DeviceServiceTag"]] = each
            if not each_device:
                invalid.append(each)
    if invalid:
        err_value = "id" if key == "Id" else "service tag"
        module.fail_json(msg=INVALID_DEVICE.format(err_value, ",".join(map(str, set(invalid)))))

    invalid_fabric_tag, sip_info = [], []
    for pro_id in valid_service_tag:
        profile_dict = {}
        try:
            profile_resp = rest_obj.invoke_request("GET", "{0}('{1}')".format(PROFILE_URI, pro_id))
        except HTTPError as err:
            err_message = json.load(err)
            if err_message.get('error', {}).get('@Message.ExtendedInfo')[0]["MessageId"] == "CDEV5008":
                if key == "Id":
                    invalid_fabric_tag.append(device_map[pro_id])
                else:
                    invalid_fabric_tag.append(pro_id)
        else:
            profile_data = rest_obj.strip_substr_dict(profile_resp.json_data)
            profile_dict.update(profile_data)
            np_resp = rest_obj.invoke_request("GET", NETWORK_PROFILE_URI.format(pro_id))
            sip_strip = []
            for each in np_resp.json_data["value"]:
                np_strip_data = rest_obj.strip_substr_dict(each)
                np_strip_data["Networks"] = [rest_obj.strip_substr_dict(each) for each in np_strip_data["Networks"]]
                sip_strip.append(np_strip_data)
            profile_dict["ServerInterfaceProfile"] = sip_strip
            sip_info.append(profile_dict)

    if invalid_fabric_tag:
        module.fail_json(msg=PROFILE_ERR_MSG.format(", ".join(set(map(str, invalid_fabric_tag)))))
    return sip_info


def main():
    argument_spec = {
        "device_id": {"required": False, "type": "list", "elements": "int"},
        "device_service_tag": {"required": False, "type": "list", "elements": "str"},
    }
    argument_spec.update(ome_auth_params)
    module = AnsibleModule(argument_spec=argument_spec,
                           mutually_exclusive=[('device_id', 'device_service_tag')],
                           required_one_of=[["device_id", "device_service_tag"]],
                           supports_check_mode=True, )
    if not any([module.params.get("device_id"), module.params.get("device_service_tag")]):
        module.fail_json(msg=CONFIG_FAIL_MSG)
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            check_domain_service(module, rest_obj)
            sip_info = get_sip_info(module, rest_obj)
            module.exit_json(msg=SUCCESS_MSG, server_profiles=sip_info)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError,
            AttributeError, IndexError, KeyError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
