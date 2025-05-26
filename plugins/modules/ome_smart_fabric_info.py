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
module: ome_smart_fabric_info
short_description: Retrieves the information of smart fabrics inventoried by OpenManage Enterprise Modular
version_added: "7.1.0"
description:
   - This module retrieves the list of smart fabrics in the inventory of OpenManage Enterprise Modular.
extends_documentation_fragment:
  - dellemc.openmanage.omem_auth_options
options:
  fabric_id:
    description:
      - Unique Id of the fabric.
      - I(fabric_id) is mutually exclusive with I(fabric_name).
    type: str
  fabric_name:
    description:
      - Name of the fabric.
      - I(fabric_name) is mutually exclusive with I(fabric_id).
    type: str
requirements:
    - "python >= 3.9.6"
author:
    - "Kritika Bhateja(@Kritka-Bhateja)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise Modular.
    - This module supports C(check_mode).
'''

EXAMPLES = """
---
- name: Retrieve details of all smart fabrics
  dellemc.openmanage.ome_smart_fabric_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"

- name: Retrieve details of a specific smart fabric identified by its fabric ID
  dellemc.openmanage.ome_smart_fabric_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    fabric_id: "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2"

- name: Retrieve details of a specific smart fabric identified by its fabric name
  dellemc.openmanage.ome_smart_fabric_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    fabric_name: "f1"
"""

RETURN = '''
---
msg:
  type: str
  description: Status of smart fabric information retrieval.
  returned: always
  sample: "Successfully retrieved the smart fabric information."
smart_fabric_info:
  type: list
  description: Returns the information about smart fabric.
  returned: success
  sample: [
        {
            "Description": "Fabric f1",
            "FabricDesign": [
                {
                    "Actions": {
                        "#NetworkService.GetApplicableNodes": {
                            "target": "/api/NetworkService/Fabrics('61c20a59-9ed5-4ae5-b850-5e5acf42d2f2')/FabricDesign/NetworkService.GetApplicableNodes"
                        },
                        "Oem": {}
                    },
                    "FabricDesignNode": [
                        {
                            "ChassisName": "Chassis-X",
                            "NodeName": "Switch-B",
                            "Slot": "Slot-A2",
                            "Type": "WeaverSwitch"
                        },
                        {
                            "ChassisName": "Chassis-X",
                            "NodeName": "Switch-A",
                            "Slot": "Slot-A1",
                            "Type": "WeaverSwitch"
                        }
                    ],
                    "Name": "2xMX9116n_Fabric_Switching_Engines_in_same_chassis",
                    "NetworkLink": [
                        {
                            "DestinationInterface": "ethernet1/1/38",
                            "DestinationNode": "Switch-B",
                            "SourceInterface": "ethernet1/1/38",
                            "SourceNode": "Switch-A"
                        },
                        {
                            "DestinationInterface": "ethernet1/1/37",
                            "DestinationNode": "Switch-B",
                            "SourceInterface": "ethernet1/1/37",
                            "SourceNode": "Switch-A"
                        },
                        {
                            "DestinationInterface": "ethernet1/1/39",
                            "DestinationNode": "Switch-B",
                            "SourceInterface": "ethernet1/1/39",
                            "SourceNode": "Switch-A"
                        },
                        {
                            "DestinationInterface": "ethernet1/1/40",
                            "DestinationNode": "Switch-B",
                            "SourceInterface": "ethernet1/1/40",
                            "SourceNode": "Switch-A"
                        }
                    ]
                }
            ],
            "FabricDesignMapping": [
                {
                    "DesignNode": "Switch-A",
                    "PhysicalNode": "NODEID1"
                },
                {
                    "DesignNode": "Switch-B",
                    "PhysicalNode": "NODEID2"
                }
            ],
            "Health": {
                "Issues": [
                    {
                        "Category": "Audit",
                        "DetailedDescription": "The SmartFabric is not healthy because the interface for an uplink
                         mentioned in the message is not in operational status.",
                        "Message": "The SmartFabric is not healthy because the interface JRWSV43:ethernet1/1/35 for uplink
                         1ad54420-b145-49a1-9779-21a579ef6f2d is not in operational status.",
                        "MessageArgs": [],
                        "MessageId": "NFAB0016",
                        "Resolution": "Make sure that all the uplink interfaces are in operational status.",
                        "Severity": "Warning",
                        "TimeStamp": "2019-09-25T11:50:06Z"
                    },
                    {
                        "Category": "Audit",
                        "DetailedDescription": "The SmartFabric is not healthy because one or more VLTi links are not connected.",
                        "Message": "The SmartFabric is not healthy because all InterSwitch Links are not connected.",
                        "MessageArgs": [],
                        "MessageId": "NFAB0017",
                        "Resolution": "Make sure that the VLTi cables for all ISLs are connected and operational as per the selected fabric design.",
                        "Severity": "Warning",
                        "TimeStamp": "2019-09-25T11:50:06Z"
                    },
                    {
                        "Category": "Audit",
                        "DetailedDescription": "The SmartFabric is not healthy because the interface for an uplink
                         mentioned in the message is not in operational status.",
                        "Message": "The SmartFabric is not healthy because the interface 6H7J6Z2:ethernet1/1/35 for uplink
                         1ad54420-b145-49a1-9779-21a579ef6f2d is not in operational status.",
                        "MessageArgs": [],
                        "MessageId": "NFAB0016",
                        "Resolution": "Make sure that all the uplink interfaces are in operational status.",
                        "Severity": "Warning",
                        "TimeStamp": "2019-09-25T11:50:06Z"
                    },
                    {
                        "Category": "Audit",
                        "DetailedDescription": "The SmartFabric is not healthy because one or more of the uplink interfaces are not bonded.",
                        "Message": "The SmartFabric is not healthy because the uplink 1ad54420-b145-49a1-9779-21a579ef6f2d
                         interface 6H7J6Z2:ethernet1/1/35 is not bonded to the other interfaces in the uplink.",
                        "MessageArgs": [],
                        "MessageId": "NFAB0019",
                        "Resolution": "Make sure that the Link Aggregation Control Protocol (LACP) is enabled on all ports on the remote
                         switch to which the uplink ports from the fabric are connected.",
                        "Severity": "Warning",
                        "TimeStamp": "2019-09-25T11:50:06Z"
                    },
                    {
                        "Category": "Audit",
                        "DetailedDescription": "The SmartFabric is not healthy because one or more of the uplink interfaces are not bonded.",
                        "Message": "The SmartFabric is not healthy because the uplink 1ad54420-b145-49a1-9779-21a579ef6f2d
                         interface JRWSV43:ethernet1/1/35 is not bonded to the other interfaces in the uplink.",
                        "MessageArgs": [],
                        "MessageId": "NFAB0019",
                        "Resolution": "Make sure that the Link Aggregation Control Protocol (LACP) is enabled on all ports
                         on the remote switch to which the uplink ports from the fabric are connected.",
                        "Severity": "Warning",
                        "TimeStamp": "2019-09-25T11:50:06Z"
                    }
                ],
                "Status": "4000"
            },
            "Id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2",
            "LifeCycleStatus": [
                {
                    "Activity": "Create",
                    "Status": "2060"
                }
            ],
            "Multicast": [
                {
                    "FloodRestrict": true,
                    "IgmpVersion": "3",
                    "MldVersion": "2"
                }
            ],
            "Name": "f1",
            "OverrideLLDPConfiguration": "Disabled",
            "ScaleVLANProfile": "Enabled",
            "Servers": [
                {
                    "ChassisServiceTag": "6H5S6Z2",
                    "ConnectionState": true,
                    "ConnectionStateReason": 101,
                    "DeviceCapabilities": [
                        1,
                        2,
                        3,
                        4,
                        7,
                        8,
                        9,
                        41,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        208,
                        16,
                        17,
                        18,
                        212,
                        30,
                        31
                    ],
                    "DeviceManagement": [
                        {
                            "DnsName": "iDRAC-6GZK6Z2",
                            "InstrumentationName": "",
                            "MacAddress": "4c:d9:8f:7a:7c:43",
                            "ManagementId": 135185,
                            "ManagementProfile": [
                                {
                                    "AgentName": "iDRAC",
                                    "HasCreds": 0,
                                    "ManagementId": 135185,
                                    "ManagementProfileId": 135185,
                                    "ManagementURL": "https://[2607:f2b1:f081:9:4ed9:8fff:fe7a:7c43]:443/",
                                    "ProfileId": "WSMAN_OOB",
                                    "Status": 1000,
                                    "StatusDateTime": "2019-10-29 09:30:38.552",
                                    "Version": "3.20.21.20"
                                }
                            ],
                            "ManagementType": 2,
                            "NetworkAddress": "100.96.24.28"
                        },
                        {
                            "DnsName": "iDRAC-6GZK6Z2",
                            "InstrumentationName": "",
                            "MacAddress": "4c:d9:8f:7a:7c:43",
                            "ManagementId": 135186,
                            "ManagementProfile": [
                                {
                                    "AgentName": "iDRAC",
                                    "HasCreds": 0,
                                    "ManagementId": 135186,
                                    "ManagementProfileId": 135186,
                                    "ManagementURL": "https://[2607:f2b1:f081:9:4ed9:8fff:fe7a:7c43]:443/",
                                    "ProfileId": "WSMAN_OOB",
                                    "Status": 1000,
                                    "StatusDateTime": "2019-10-29 09:30:38.552",
                                    "Version": "3.20.21.20"
                                }
                            ],
                            "ManagementType": 2,
                            "NetworkAddress": "[2607:f2b1:f081:9:4ed9:8fff:fe7a:7c43]"
                        }
                    ],
                    "DeviceName": "MX-6H5S6Z2:Sled-1",
                    "DeviceServiceTag": "6GZK6Z2",
                    "Enabled": true,
                    "Id": 10071,
                    "Identifier": "6GZK6Z2",
                    "LastInventoryTime": "2019-10-29 09:30:38.552",
                    "LastStatusTime": "2019-10-29 09:41:51.051",
                    "ManagedState": 3000,
                    "Model": "PowerEdge MX840c",
                    "PowerState": 17,
                    "SlotConfiguration": {
                        "ChassisId": "10072",
                        "ChassisName": "MX-6H5S6Z2",
                        "ChassisServiceTag": "6H5S6Z2",
                        "DeviceType": "1000",
                        "SledBlockPowerOn": "None blocking",
                        "SlotId": "10084",
                        "SlotName": "Sled-1",
                        "SlotNumber": "1",
                        "SlotType": "2000"
                    },
                    "Status": 1000,
                    "SystemId": 1894,
                    "Type": 1000
                }
            ],
            "Summary": {
                "NodeCount": 2,
                "ServerCount": 1,
                "UplinkCount": 1
            },
            "Switches": [
                {
                    "ChassisServiceTag": "6H5S6Z2",
                    "ConnectionState": true,
                    "ConnectionStateReason": 101,
                    "DeviceCapabilities": [
                        1,
                        2,
                        3,
                        5,
                        7,
                        8,
                        9,
                        207,
                        18,
                        602,
                        603,
                        604,
                        605,
                        606,
                        607,
                        608,
                        609,
                        610,
                        611,
                        612,
                        613,
                        614,
                        615,
                        616,
                        617,
                        618,
                        619,
                        620,
                        621,
                        622
                    ],
                    "DeviceManagement": [
                        {
                            "DnsName": "",
                            "InstrumentationName": "MX9116n Fabric Engine",
                            "MacAddress": "20:04:0F:4F:4E:04",
                            "ManagementId": 135181,
                            "ManagementProfile": [
                                {
                                    "HasCreds": 0,
                                    "ManagementId": 135181,
                                    "ManagementProfileId": 135181,
                                    "ManagementURL": "",
                                    "ProfileId": "",
                                    "Status": 1000,
                                    "StatusDateTime": "2019-10-29 09:30:36.273"
                                }
                            ],
                            "ManagementType": 2,
                            "NetworkAddress": "100.96.24.36"
                        },
                        {
                            "DnsName": "",
                            "InstrumentationName": "MX9116n Fabric Engine",
                            "MacAddress": "20:04:0F:4F:4E:04",
                            "ManagementId": 135182,
                            "ManagementProfile": [
                                {
                                    "HasCreds": 0,
                                    "ManagementId": 135182,
                                    "ManagementProfileId": 135182,
                                    "ManagementURL": "",
                                    "ProfileId": "",
                                    "Status": 1000,
                                    "StatusDateTime": "2019-10-29 09:30:36.273"
                                }
                            ],
                            "ManagementType": 2,
                            "NetworkAddress": ""
                        }
                    ],
                    "DeviceName": "MX-6H5S6Z2:IOM-A2",
                    "DeviceServiceTag": "6H7J6Z2",
                    "Enabled": true,
                    "Id": 10074,
                    "Identifier": "6H7J6Z2",
                    "LastInventoryTime": "2019-10-29 09:30:36.332",
                    "LastStatusTime": "2019-10-29 09:31:00.931",
                    "ManagedState": 3000,
                    "Model": "MX9116n Fabric Engine",
                    "PowerState": 17,
                    "SlotConfiguration": {
                        "ChassisId": "10072",
                        "ChassisName": "MX-6H5S6Z2",
                        "ChassisServiceTag": "6H5S6Z2",
                        "DeviceType": "4000",
                        "SledBlockPowerOn": "null",
                        "SlotId": "10079",
                        "SlotName": "IOM-A2",
                        "SlotNumber": "2",
                        "SlotType": "4000"
                    },
                    "Status": 1000,
                    "SystemId": 2031,
                    "Type": 4000
                },
                {
                    "ChassisServiceTag": "6H5S6Z2",
                    "ConnectionState": true,
                    "ConnectionStateReason": 101,
                    "DeviceCapabilities": [
                        1,
                        2,
                        3,
                        5,
                        7,
                        8,
                        9,
                        207,
                        18,
                        602,
                        603,
                        604,
                        605,
                        606,
                        607,
                        608,
                        609,
                        610,
                        611,
                        612,
                        613,
                        614,
                        615,
                        616,
                        617,
                        618,
                        619,
                        620,
                        621,
                        622
                    ],
                    "DeviceManagement": [
                        {
                            "DnsName": "",
                            "InstrumentationName": "MX9116n Fabric Engine",
                            "MacAddress": "E8:B5:D0:52:61:46",
                            "ManagementId": 135183,
                            "ManagementProfile": [
                                {
                                    "HasCreds": 0,
                                    "ManagementId": 135183,
                                    "ManagementProfileId": 135183,
                                    "ManagementURL": "",
                                    "ProfileId": "",
                                    "Status": 1000,
                                    "StatusDateTime": "2019-10-29 09:30:37.115"
                                }
                            ],
                            "ManagementType": 2,
                            "NetworkAddress": "100.96.24.37"
                        },
                        {
                            "DnsName": "",
                            "InstrumentationName": "MX9116n Fabric Engine",
                            "MacAddress": "E8:B5:D0:52:61:46",
                            "ManagementId": 135184,
                            "ManagementProfile": [
                                {
                                    "HasCreds": 0,
                                    "ManagementId": 135184,
                                    "ManagementProfileId": 135184,
                                    "ManagementURL": "",
                                    "ProfileId": "",
                                    "Status": 1000,
                                    "StatusDateTime": "2019-10-29 09:30:37.115"
                                }
                            ],
                            "ManagementType": 2,
                            "NetworkAddress": ""
                        }
                    ],
                    "DeviceName": "MX-6H5S6Z2:IOM-A1",
                    "DeviceServiceTag": "JRWSV43",
                    "Enabled": true,
                    "Id": 20881,
                    "Identifier": "JRWSV43",
                    "LastInventoryTime": "2019-10-29 09:30:37.172",
                    "LastStatusTime": "2019-10-29 09:31:00.244",
                    "ManagedState": 3000,
                    "Model": "MX9116n Fabric Engine",
                    "PowerState": 17,
                    "SlotConfiguration": {
                        "ChassisId": "10072",
                        "ChassisName": "MX-6H5S6Z2",
                        "ChassisServiceTag": "6H5S6Z2",
                        "DeviceType": "4000",
                        "SledBlockPowerOn": "null",
                        "SlotId": "10078",
                        "SlotName": "IOM-A1",
                        "SlotNumber": "1",
                        "SlotType": "4000"
                    },
                    "Status": 1000,
                    "SystemId": 2031,
                    "Type": 4000
                }
            ],
            "Uplinks": [
                {
                    "Id": "1ad54420-b145-49a1-9779-21a579ef6f2d",
                    "MediaType": "Ethernet",
                    "Name": "u1",
                    "NativeVLAN": 1,
                    "Summary": {
                        "NetworkCount": 1,
                        "PortCount": 2
                    },
                    "UfdEnable": "Disabled"
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
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import strip_substr_dict


FABRIC_URI = "NetworkService/Fabrics"
# messages
SUCCESS_MSG = "Successfully retrieved the smart fabric information."
UNSUCCESS_MSG = "Unable to retrieve smart fabric information."
INVALID_FABRIC_ID = "Unable to retrieve smart fabric information with fabric ID {0}."
INVALID_FABRIC_NAME = "Unable to retrieve smart fabric information with fabric name {0}."


def get_smart_fabric_details_via_id(module, rest_obj, fabric_id):
    resp = []
    try:
        fabric_path = "{0}('{1}')".format(FABRIC_URI, fabric_id)
        resp_det = rest_obj.invoke_request("GET", fabric_path)
        resp = [resp_det.json_data]
    except HTTPError:
        module.exit_json(msg=INVALID_FABRIC_ID.format(fabric_id), failed=True)
    return resp


def fetch_smart_fabric_link_details(module, rest_obj, fabric_details_dict):
    info_dict = {"Switches": "Switches@odata.navigationLink", "Servers": "Servers@odata.navigationLink",
                 "ISLLinks": "ISLLinks@odata.navigationLink", "Uplinks": "Uplinks@odata.navigationLink",
                 "Multicast": None, "FabricDesign": None}
    info_list = ["Multicast", "FabricDesign"]
    details = None
    try:
        for key in info_dict:
            link = info_dict[key]
            if key in info_list:
                fabric_info_dict = fabric_details_dict[key]["@odata.id"]
                uri = fabric_info_dict.strip("/api")
                response = rest_obj.invoke_request('GET', uri)
                if response.json_data:
                    details = [response.json_data]
            else:
                fabric_info_dict = fabric_details_dict.get(link)
                uri = fabric_info_dict.strip("/api")
                response = rest_obj.invoke_request('GET', uri)
                if response.json_data:
                    details = response.json_data.get("value")
            for item in details:
                item = strip_substr_dict(item)
                item = clean_data(item)
                fabric_details_dict[key] = details
    except HTTPError:
        module.exit_json(msg=UNSUCCESS_MSG, failed=True)
    return fabric_details_dict


def strip_smart_fabric_info(module, rest_obj, smart_fabric_info):
    for i in range(len(smart_fabric_info)):
        fabrics_details = smart_fabric_info[i]
        fabrics_details = fetch_smart_fabric_link_details(module, rest_obj, fabrics_details)
        fabrics_details = strip_substr_dict(fabrics_details)
        fabrics_details = clean_data(fabrics_details)
        smart_fabric_info[i] = fabrics_details
    return smart_fabric_info


def clean_data(data):
    """
    data: A dictionary.
    return: A data dictionary after removing items that are not required for end user.
    """
    for k in data.copy():
        if isinstance(data[k], dict):
            if data[k].get("@odata.id"):
                del data[k]["@odata.id"]
        if not data[k]:
            del data[k]
    return data


def main():

    specs = {
        "fabric_id": {"type": 'str', "required": False},
        "fabric_name": {"type": 'str', "required": False}
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[
            ('fabric_id', 'fabric_name')
        ],
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            if module.params.get("fabric_id") is not None:
                fabric_id = module.params.get("fabric_id")
                smart_fabric_info = get_smart_fabric_details_via_id(module, rest_obj, fabric_id)
                smart_fabric_info = strip_smart_fabric_info(module, rest_obj, smart_fabric_info)
                module.exit_json(msg=SUCCESS_MSG, smart_fabric_info=smart_fabric_info)
            else:
                resp = rest_obj.invoke_request('GET', FABRIC_URI)
                if resp.json_data:
                    smart_fabric_info = resp.json_data.get("value")
                    if module.params.get("fabric_name") is not None:
                        fabric_name_found = False
                        for fabric in smart_fabric_info:
                            fabric_name = module.params.get("fabric_name")
                            if fabric['Name'] == fabric_name:
                                smart_fabric_info = [fabric]
                                fabric_name_found = True
                        if not fabric_name_found:
                            module.exit_json(msg=INVALID_FABRIC_NAME.format(fabric_name), failed=True)
                    smart_fabric_info = strip_smart_fabric_info(module, rest_obj, smart_fabric_info)
                    module.exit_json(msg=SUCCESS_MSG, smart_fabric_info=smart_fabric_info)
                else:
                    module.exit_json(msg=UNSUCCESS_MSG, failed=True)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError, SSLError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
