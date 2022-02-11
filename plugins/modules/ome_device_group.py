#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.0.1
# Copyright (C) 2021-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
---
module: ome_device_group
short_description: Add devices to a static device group on OpenManage Enterprise
version_added: "3.3.0"
description: This module allows to add devices to a static device group on OpenManage Enterprise.
extends_documentation_fragment:
  - dellemc.openmanage.oment_auth_options
options:
  state:
    type: str
    description:
      - C(present) allows to add the device(s) to a static device group.
      - C(absent) currently, this feature is not supported.
    choices: [present, absent]
    default: present
  name:
    type: str
    description:
      - Name of the static group to which device(s) need to be added.
      - I(name) is mutually exclusive with I(group_id).
  group_id:
    type: int
    description:
      - ID of the static device group to which device(s) need to be added.
      - I(group_id) is mutually exclusive with I(name).
  device_ids:
    type: list
    elements: int
    description:
      - List of ID(s) of the device(s) to be added to the device group.
      - I(device_ids) is mutually exclusive with I(device_service_tags) and I(ip_addresses).
  device_service_tags:
    type: list
    elements: str
    description:
      - List of service tag(s) of the device(s) to be added to the device group.
      - I(device_service_tags) is mutually exclusive with I(device_ids) and I(ip_addresses).
  ip_addresses:
    type: list
    elements: str
    description:
      - List of IPs of the device(s) to be added to the device group.
      - I(ip_addresses) is mutually exclusive with I(device_ids) and I(device_service_tags).
      - "Supported  IP address range formats:"
      - "    - 192.35.0.1"
      - "    - 10.36.0.0-192.36.0.255"
      - "    - 192.37.0.0/24"
      - "    - fe80::ffff:ffff:ffff:ffff"
      - "    - fe80::ffff:192.0.2.0/125"
      - "    - fe80::ffff:ffff:ffff:1111-fe80::ffff:ffff:ffff:ffff"
      - C(NOTE) Hostname is not supported.
      - C(NOTE) I(ip_addresses) requires python's netaddr packages to work on IP Addresses.
      - C(NOTE) This module reports success even if one of the IP addresses provided in the I(ip_addresses) list is
       available in OpenManage Enterprise.The module reports failure only if none of the IP addresses provided in the
        list are available in OpenManage Enterprise.
requirements:
  - "python >= 3.8.6"
  - "netaddr >= 0.7.19"
author:
  - "Felix Stephen (@felixs88)"
  - "Sajna Shetty(@Sajna-Shetty)"
notes:
  - Run this module from a system that has direct access to Dell EMC OpenManage Enterprise.
  - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Add devices to a static device group by using the group name and device IDs
  dellemc.openmanage.ome_device_group:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    name: "Storage Services"
    device_ids:
      - 11111
      - 11112
      - 11113

- name: Add devices to a static device group by using the group name and device service tags
  dellemc.openmanage.ome_device_group:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    name: "Storage Services"
    device_service_tags:
      - GHRT2RL
      - KJHDF3S
      - LKIJNG6

- name: Add devices to a static device group by using the group ID and device service tags
  dellemc.openmanage.ome_device_group:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    group_id: 12345
    device_service_tags:
      - GHRT2RL
      - KJHDF3S

- name: Add devices to a static device group by using the group name and IPv4 addresses
  dellemc.openmanage.ome_device_group:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    name: "Storage Services"
    ip_addresses:
      - 192.35.0.1
      - 192.35.0.5

- name: Add devices to a static device group by using the group ID and IPv6 addresses
  dellemc.openmanage.ome_device_group:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    group_id: 12345
    ip_addresses:
      - fe80::ffff:ffff:ffff:ffff
      - fe80::ffff:ffff:ffff:2222

- name: Add devices to a static device group by using the group ID and supported IPv4 and IPv6 address formats.
  dellemc.openmanage.ome_device_group:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    group_id: 12345
    ip_addresses:
      - 192.35.0.1
      - 10.36.0.0-192.36.0.255
      - 192.37.0.0/24
      - fe80::ffff:ffff:ffff:ffff
      - ::ffff:192.0.2.0/125
      - fe80::ffff:ffff:ffff:1111-fe80::ffff:ffff:ffff:ffff
"""

RETURN = """
---
msg:
  type: str
  description: Overall status of the device group settings.
  returned: always
  sample: "Successfully added member(s) to the device group."
group_id:
  type: int
  description: ID of the group.
  returned: success
  sample: 21078
ip_addresses_added:
  type: list
  description: IP Addresses which are added to the device group.
  returned: success
  sample: 21078
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
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError

try:
    from netaddr import IPAddress, IPNetwork, IPRange
    from netaddr.core import AddrFormatError

    HAS_NETADDR = True
except ImportError:
    HAS_NETADDR = False

GROUP_URI = "GroupService/Groups"
DEVICE_URI = "DeviceService/Devices"
ADD_MEMBER_URI = "GroupService/Actions/GroupService.AddMemberDevices"
ADD_STATIC_GROUP_MESSAGE = "Devices can be added only to the static device groups created using OpenManage Enterprise."
NETADDR_ERROR = "The module requires python's netaddr be installed on the ansible controller to work on IP Addresses."
INVALID_IP_FORMAT = "The format {0} of the IP address provided is not supported or invalid."
IP_NOT_EXISTS = "The IP addresses provided do not exist in OpenManage Enterprise."


def validate_group(group_resp, module, identifier, identifier_val):
    if not group_resp:
        module.fail_json(msg="Unable to complete the operation because the entered "
                             "target group {identifier} '{val}' is invalid.".format(identifier=identifier,
                                                                                    val=identifier_val))
    system_groups = group_resp["TypeId"]
    membership_id = group_resp["MembershipTypeId"]
    if system_groups != 3000 or (system_groups == 3000 and membership_id == 24):
        module.fail_json(msg=ADD_STATIC_GROUP_MESSAGE)


def get_group_id(rest_obj, module):
    group_name = module.params.get("name")
    group_id = module.params.get("group_id")
    if group_name is not None:
        group_resp = rest_obj.invoke_request("GET", GROUP_URI,
                                             query_param={"$filter": "Name eq '{0}'".format(group_name)})
        value = group_resp.json_data.get("value")
        if value:
            value = value[0]
        else:
            value = []
        validate_group(value, module, "name", group_name)
        group_id = value["Id"]

    else:
        uri = GROUP_URI + "(" + str(group_id) + ")"
        try:
            group_resp = rest_obj.invoke_request("GET", uri)
            validate_group(group_resp.json_data, module, "Id", group_id)
        except HTTPError:
            validate_group({}, module, "Id", group_id)
    return group_id


def get_all_ips(ip_addresses, module):
    ip_addresses_list = []
    for ip in ip_addresses:
        try:
            if "/" in ip:
                cidr_list = IPNetwork(ip)
                ip_addresses_list.append(cidr_list)
            elif "-" in ip and ip.count("-") == 1:
                range_addr = ip.split("-")
                range_list = IPRange(range_addr[0], range_addr[1])
                ip_addresses_list.append(range_list)
            else:
                single_ip = IPAddress(ip)
                ip_addresses_list.append(single_ip)
        except (AddrFormatError, ValueError):
            module.fail_json(msg=INVALID_IP_FORMAT.format(ip))
    return ip_addresses_list


def get_device_id_from_ip(ip_addresses, device_list, module):
    ip_map = dict(
        [(each_device["DeviceManagement"][0]["NetworkAddress"], each_device["Id"]) for each_device in device_list
         if each_device["DeviceManagement"]])
    device_id_list_map = {}
    for available_ip, device_id in ip_map.items():
        for ip_formats in ip_addresses:
            if isinstance(ip_formats, IPAddress):
                try:
                    ome_ip = IPAddress(available_ip)
                except AddrFormatError:
                    ome_ip = IPAddress(available_ip.replace(']', '').replace('[', ''))
                if ome_ip == ip_formats:
                    device_id_list_map.update({device_id: str(ip_formats)})
            if not isinstance(ip_formats, IPAddress):
                try:
                    ome_ip = IPAddress(available_ip)
                except AddrFormatError:
                    ome_ip = IPAddress(available_ip.replace(']', '').replace('[', ''))
                if ome_ip in ip_formats:
                    device_id_list_map.update({device_id: str(ome_ip)})
    if len(device_id_list_map) == 0:
        module.fail_json(msg=IP_NOT_EXISTS)
    return device_id_list_map


def get_device_id(rest_obj, module):
    device_id_list = module.params.get("device_ids")
    device_tag_list = module.params.get("device_service_tags")
    ip_addresses = module.params.get("ip_addresses")
    device_list = rest_obj.get_all_report_details(DEVICE_URI)
    invalid, each_device_list, each_tag_to_id = [], [], []
    if device_id_list or device_tag_list:
        if device_id_list:
            key = "Id"
            each_device_list = device_id_list
        elif device_tag_list:
            key = "DeviceServiceTag"
            each_device_list = device_tag_list

        for each in each_device_list:
            each_device = list(filter(lambda d: d[key] in [each], device_list["report_list"]))
            if key == "DeviceServiceTag" and each_device:
                each_tag_to_id.append(each_device[0]["Id"])
            if not each_device:
                invalid.append(str(each))
        if invalid:
            value = "id" if key == "Id" else "service tag"
            module.fail_json(msg="Unable to complete the operation because the entered "
                                 "target device {0}(s) '{1}' are invalid.".format(value, ",".join(set(invalid))))
        if each_tag_to_id:
            each_device_list = each_tag_to_id
    else:
        all_ips = get_all_ips(ip_addresses, module)
        each_device_list = get_device_id_from_ip(all_ips, device_list["report_list"], module)
        key = "IPAddresses"
    return each_device_list, key


def add_member_to_group(module, rest_obj, group_id, device_id, key):
    group_device = rest_obj.get_all_report_details("{0}({1})/Devices".format(GROUP_URI, group_id))
    device_exists, device_not_exists, added_ips = [], [], []
    if key != "IPAddresses":
        for each in device_id:
            each_device = list(filter(lambda d: d["Id"] in [each], group_device["report_list"]))
            if each_device:
                tag_or_id = each_device[0][key] if key == "DeviceServiceTag" else each
                device_exists.append(str(tag_or_id))
            else:
                device_not_exists.append(each)
    else:
        already_existing_id = []
        for device in group_device["report_list"]:
            if device["Id"] in device_id:
                device_exists.append(device_id[device["Id"]])
                already_existing_id.append(device["Id"])
        device_not_exists = list(set(device_id.keys()) - set(already_existing_id))
        added_ips = [ip for d_id, ip in device_id.items() if d_id in device_not_exists]
    if module.check_mode and device_not_exists:
        module.exit_json(msg="Changes found to be applied.", changed=True, group_id=group_id)
    elif module.check_mode and not device_not_exists:
        module.exit_json(msg="No changes found to be applied.", group_id=group_id)

    if device_exists and not device_not_exists:
        module.exit_json(
            msg="No changes found to be applied.",
            group_id=group_id
        )
    payload = {"GroupId": group_id, "MemberDeviceIds": device_not_exists}
    response = rest_obj.invoke_request("POST", ADD_MEMBER_URI, data=payload)
    return response, added_ips


def main():
    specs = {
        "name": {"type": "str"},
        "group_id": {"type": "int"},
        "state": {"required": False, "type": "str", "choices": ["present", "absent"], "default": "present"},
        "device_service_tags": {"required": False, "type": "list", "elements": 'str'},
        "device_ids": {"required": False, "type": "list", "elements": 'int'},
        "ip_addresses": {"required": False, "type": "list", "elements": 'str'},
    }
    specs.update(ome_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        required_if=(
            ["state", "present", ("device_ids", "device_service_tags", "ip_addresses"), True],
        ),
        mutually_exclusive=(
            ("name", "group_id"),
            ("device_ids", "device_service_tags", "ip_addresses"),
        ),
        required_one_of=[("name", "group_id"),
                         ("device_ids", "device_service_tags", "ip_addresses")],
        supports_check_mode=True
    )

    try:
        if module.params.get("ip_addresses") and not HAS_NETADDR:
            module.fail_json(msg=NETADDR_ERROR)
        with RestOME(module.params, req_session=True) as rest_obj:
            group_id = get_group_id(rest_obj, module)
            device_id, key = get_device_id(rest_obj, module)
            if module.params["state"] == "present":
                response, added_ips = add_member_to_group(module, rest_obj, group_id, device_id, key)
                if added_ips:
                    module.exit_json(msg="Successfully added member(s) to the device group.",
                                     group_id=group_id, changed=True, ip_addresses_added=added_ips)
                module.exit_json(msg="Successfully added member(s) to the device group.",
                                 group_id=group_id, changed=True)
            elif module.params["state"] == "absent":
                module.fail_json(msg="Currently, this feature is not supported.")
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, AttributeError,
            IndexError, KeyError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
