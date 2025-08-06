#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.4
# Copyright (C) 2020-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_network_vlan_info
short_description: Retrieves the information about networks VLAN(s) present in OpenManage Enterprise
version_added: "2.1.0"
description:
    This module allows to retrieve the following.
    - A list of all the network VLANs with their detailed information.
    - Information about a specific network VLAN using VLAN I(id) or VLAN I(name).
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
    id:
        description:
            - A unique identifier of the network VLAN available in the device.
            - I(id) and I(name) are mutually exclusive.
        type: int
    name:
        description:
            - A unique name of the network VLAN available in the device.
            - I(name) and I(id) are mutually exclusive.
        type: str

requirements:
    - "python >= 3.9.6"
author:
    - "Deepak Joshi(@deepakjoshishri)"
    - "Meenakshi Dembi(@meenakshidembi691)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
    - This module supports C(check_mode).
'''

EXAMPLES = """
---
- name: Retrieve information about all network VLANs(s) available in the device
  dellemc.openmanage.ome_network_vlan_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"

- name: Retrieve information about a network VLAN using the VLAN ID
  dellemc.openmanage.ome_network_vlan_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    id: 12345

- name: Retrieve information about a network VLAN using the VLAN name
  dellemc.openmanage.ome_network_vlan_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    name: "Network VLAN - 1"
"""

RETURN = '''
---
msg:
  type: str
  description: Detailed information of the network VLAN(s).
  returned: success
  sample: {
  "msg": "Successfully retrieved the network VLAN information.",
  "network_vlan_info": [
        {
            "CreatedBy": "admin",
            "CreationTime": "2020-09-02 18:48:42.129",
            "Description": "Description of Logical Network - 1",
            "Id": 20057,
            "InternalRefNWUUId": "42b9903d-93f8-4184-adcf-0772e4492f71",
            "Name": "Network VLAN - 1",
            "Type": {
                "Description": "This is the network for general purpose traffic. QOS Priority : Bronze.",
                "Id": 1,
                "Name": "General Purpose (Bronze)",
                "NetworkTrafficType": "Ethernet",
                "QosType": {
                    "Id": 4,
                    "Name": "Bronze"
                },
                "VendorCode": "GeneralPurpose"
            },
            "UpdatedBy": null,
            "UpdatedTime": "2020-09-02 18:48:42.129",
            "VlanMaximum": 111,
            "VlanMinimum": 111
        },
        {
            "CreatedBy": "admin",
            "CreationTime": "2020-09-02 18:49:11.507",
            "Description": "Description of Logical Network - 2",
            "Id": 20058,
            "InternalRefNWUUId": "e46ccb3f-ef57-4617-ac76-46c56594005c",
            "Name": "Network VLAN - 2",
            "Type": {
                "Description": "This is the network for general purpose traffic. QOS Priority : Silver.",
                "Id": 2,
                "Name": "General Purpose (Silver)",
                "NetworkTrafficType": "Ethernet",
                "QosType": {
                    "Id": 3,
                    "Name": "Silver"
                },
                "VendorCode": "GeneralPurpose"
            },
            "UpdatedBy": null,
            "UpdatedTime": "2020-09-02 18:49:11.507",
            "VlanMaximum": 112,
            "VlanMinimum": 112
        }
    ]
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
'''

import json
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError

# Base URI to fetch all logical networks information
NETWORK_VLAN_BASE_URI = "NetworkConfigurationService/Networks"
NETWORK_TYPE_BASE_URI = "NetworkConfigurationService/NetworkTypes"
QOS_TYPE_BASE_URI = "NetworkConfigurationService/QosTypes"

# Module Success Message
MODULE_SUCCESS_MESSAGE = "Successfully retrieved the network VLAN information."

# Module Failure Messages
MODULE_FAILURE_MESSAGE = "Failed to retrieve the network VLAN information."
NETWORK_VLAN_NAME_NOT_FOUND = "Provided network VLAN with name - '{0}' does not exist."

SAFE_MAX_LIMIT = 9999


def clean_data(data):
    """
    data: A dictionary.
    return: A data dictionary after removing items that are not required for end user.
    """
    for k in ['@odata.id', '@odata.type', '@odata.context', '@odata.count']:
        data.pop(k, None)
    return data


def get_type_information(rest_obj, uri):
    """
    rest_obj: Object containing information about connection to device.
    return: dict with information retrieved from URI.
    """
    type_info_dict = {}
    resp = rest_obj.invoke_request('GET', uri)
    if resp.status_code == 200:
        type_info = resp.json_data.get('value') if isinstance(resp.json_data.get('value'), list) \
            else [resp.json_data]
        for item in type_info:
            item = clean_data(item)
            type_info_dict[item['Id']] = item
    return type_info_dict


def get_network_type_and_qos_type_information(rest_obj):
    """
    rest_obj: Object containing information about connection to device.
    return: Dictionary with information for "Type" and "QosType" keys.
    """
    # Fetch network type and qos type information once
    network_type_dict = get_type_information(rest_obj, NETWORK_TYPE_BASE_URI)
    qos_type_dict = get_type_information(rest_obj, QOS_TYPE_BASE_URI)
    # Update each network type with qos type info
    for key, item in network_type_dict.items():
        item['QosType'] = qos_type_dict[item['QosType']]
    return network_type_dict


def main():
    specs = {
        "id": {"required": False, "type": 'int'},
        "name": {"required": False, "type": 'str'}
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[["id", "name"]],
        supports_check_mode=True)
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            # Form URI to fetch network VLAN information
            network_vlan_uri = "{0}({1})".format(NETWORK_VLAN_BASE_URI, module.params.get("id")) if module.params.get(
                "id") else "{0}?$top={1}".format(NETWORK_VLAN_BASE_URI, SAFE_MAX_LIMIT)
            resp = rest_obj.invoke_request('GET', network_vlan_uri)
            if resp.status_code == 200:
                network_vlan_info = resp.json_data.get('value') if isinstance(resp.json_data.get('value'), list) else [
                    resp.json_data]
                if module.params.get("name"):
                    network_vlan_name = module.params.get("name")
                    network_vlan = []
                    for item in network_vlan_info:
                        if item["Name"] == network_vlan_name.strip():
                            network_vlan = [item]
                            break
                    if not network_vlan:
                        module.exit_json(msg=NETWORK_VLAN_NAME_NOT_FOUND.format(network_vlan_name), failed=True)
                    network_vlan_info = network_vlan
                # Get network type and Qos Type information
                network_type_dict = get_network_type_and_qos_type_information(rest_obj)
                # Update each network VLAN with network type and wos type information
                for network_vlan in network_vlan_info:
                    network_vlan = clean_data(network_vlan)
                    network_vlan['Type'] = network_type_dict[network_vlan['Type']]
                module.exit_json(msg=MODULE_SUCCESS_MESSAGE, network_vlan_info=network_vlan_info, changed=False)
            else:
                module.exit_json(msg=MODULE_FAILURE_MESSAGE, failed=True)
    except HTTPError as err:
        if err.getcode() == 404:
            module.exit_json(msg=str(err), failed=True)
        module.exit_json(msg=str(MODULE_FAILURE_MESSAGE), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, KeyError, ConnectionError, SSLValidationError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
