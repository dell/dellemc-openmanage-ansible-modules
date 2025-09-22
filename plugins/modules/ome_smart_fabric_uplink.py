#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.1.0
# Copyright (C) 2020-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_smart_fabric_uplink
short_description: Create, modify or delete a uplink for a fabric on OpenManage Enterprise Modular
version_added: "2.1.0"
description: This module allows to create, modify or delete an uplink for a fabric.
extends_documentation_fragment:
  - dellemc.openmanage.omem_auth_options
options:
  state:
    description:
      - C(present)
        - Creates a new uplink with the provided I(name).
        - Modifies an existing uplink with the provided I(name).
      - C(absent) – Deletes the uplink with the provided I(name).
      - I(WARNING) Delete operation can impact the network infrastructure.
    choices: [present, absent]
    default: present
    type: str
  fabric_name:
    type: str
    description: Provide the I(fabric_name) of the fabric for which the uplink is to be configured.
    required: true
  name:
    type: str
    description: Provide the I(name) of the uplink to be created, modified or deleted.
    required: true
  new_name:
    type: str
    description: Provide the new I(new_name) for the uplink.
  description:
    type: str
    description: Provide a short description for the uplink to be created or modified.
  uplink_type:
    description:
      - Specify the uplink type.
      - I(NOTE) The uplink type cannot be changed for an existing uplink.
    choices: ['Ethernet', 'FCoE', 'FC Gateway', 'FC Direct Attach', 'Ethernet - No Spanning Tree']
    type: str
  ufd_enable:
    description:
      - "Add or Remove the uplink to the Uplink Failure Detection (UFD) group. The UFD group identifies the loss of
      connectivity to the upstream switch and notifies the servers that are connected to the switch. During an uplink
      failure, the switch disables the corresponding downstream server ports. The downstream servers can then select
      alternate connectivity routes, if available."
      - "I(WARNING) The firmware version of the I/O Module running the Fabric Manager must support this configuration
      feature. If not, uplink creation will be successful with an appropriate error message in response."
    choices: ['Enabled', 'Disabled']
    type: str
  primary_switch_service_tag:
    description: Service tag of the primary switch.
    type: str
  primary_switch_ports:
    description:
      - The IOM slots to be connected to the primary switch.
      - I(primary_switch_service_tag) is mandatory for this option.
    type: list
    elements: str
  secondary_switch_service_tag:
    description: Service tag of the secondary switch.
    type: str
  secondary_switch_ports:
    description:
      - The IOM slots to be connected to the secondary switch.
      - I(secondary_switch_service_tag) is mandatory for this option.
    type: list
    elements: str
  tagged_networks:
    description: VLANs to be associated with the uplink I(name).
    type: list
    elements: str
  untagged_network:
    description: Specify the name of the VLAN to be added as untagged to the uplink.
    type: str
requirements:
    - "python >= 3.9.6"
author:
    - "Jagadeesh N V(@jagadeeshnv)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise Modular.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Create an Uplink
  dellemc.openmanage.ome_smart_fabric_uplink:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "present"
    fabric_name: "fabric1"
    name: "uplink1"
    description: "CREATED from OMAM"
    uplink_type: "Ethernet"
    ufd_enable: "Enabled"
    primary_switch_service_tag: "ABC1234"
    primary_switch_ports:
      - ethernet1/1/13
      - ethernet1/1/14
    secondary_switch_service_tag: "XYZ1234"
    secondary_switch_ports:
      - ethernet1/1/13
      - ethernet1/1/14
    tagged_networks:
      - vlan1
      - vlan3
    untagged_network: vlan2
  tags: create_uplink

- name: Modify an existing uplink
  dellemc.openmanage.ome_smart_fabric_uplink:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "present"
    fabric_name: "fabric1"
    name: "uplink1"
    new_name: "uplink2"
    description: "Modified from OMAM"
    uplink_type: "Ethernet"
    ufd_enable: "Disabled"
    primary_switch_service_tag: "DEF1234"
    primary_switch_ports:
      - ethernet1/2/13
      - ethernet1/2/14
    secondary_switch_service_tag: "TUV1234"
    secondary_switch_ports:
      - ethernet1/2/13
      - ethernet1/2/14
    tagged_networks:
      - vlan11
      - vlan33
    untagged_network: vlan22
  tags: modify_uplink

- name: Delete an Uplink
  dellemc.openmanage.ome_smart_fabric_uplink:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "absent"
    fabric_name: "fabric1"
    name: "uplink1"
  tags: delete_uplink

- name: Modify an Uplink name
  dellemc.openmanage.ome_smart_fabric_uplink:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "present"
    fabric_name: "fabric1"
    name: "uplink1"
    new_name: "uplink2"
  tags: modify_uplink_name

- name: Modify Uplink ports
  dellemc.openmanage.ome_smart_fabric_uplink:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "present"
    fabric_name: "fabric1"
    name: "uplink1"
    description: "uplink ports modified"
    primary_switch_service_tag: "ABC1234"
    primary_switch_ports:
      - ethernet1/1/6
      - ethernet1/1/7
    secondary_switch_service_tag: "XYZ1234"
    secondary_switch_ports:
      - ethernet1/1/9
      - ethernet1/1/10
  tags: modify_ports

- name: Modify Uplink networks
  dellemc.openmanage.ome_smart_fabric_uplink:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "present"
    fabric_name: "fabric1"
    name: "create1"
    description: "uplink networks modified"
    tagged_networks:
      - vlan4
  tags: modify_networks
'''

RETURN = r'''
---
msg:
  type: str
  description: Overall status of the uplink operation.
  returned: always
  sample: "Successfully modified the uplink."
uplink_id:
  type: str
  description: Returns the ID when an uplink is created or modified.
  returned: when I(state=present)
  sample: "ddc3d260-fd71-46a1-97f9-708e12345678"
additional_info:
  type: dict
  description: Additional details of the fabric operation.
  returned: when I(state=present) and additional information present in response.
  sample: {
    "error": {
        "@Message.ExtendedInfo": [
            {
                "Message": "Unable to configure the Uplink Failure Detection mode on the uplink because the firmware
                version of the I/O Module running the Fabric Manager does not support the configuration feature.",
                "MessageArgs": [],
                "MessageId": "CDEV7151",
                "RelatedProperties": [],
                "Resolution": "Update the firmware version of the I/O Module running the Fabric Manager and retry
                the operation. For information about the recommended I/O Module firmware versions, see the
                OpenManage Enterprise-Modular User's Guide available on the support site.",
                "Severity": "Informational"
            }
        ],
        "code": "Base.1.0.GeneralError",
        "message": "A general error has occurred. See ExtendedInfo for more information."
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
from ansible.module_utils.common.dict_transformations import recursive_diff
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import get_item_and_list

FABRIC_URI = "NetworkService/Fabrics"
UPLINKS_URI = "NetworkService/Fabrics('{fabric_id}')/Uplinks"
UPLINK_URI = "NetworkService/Fabrics('{fabric_id}')/Uplinks('{uplink_id}')"
APPLICABLE_NETWORKS = "NetworkService/Fabrics('{fabric_id}')/NetworkService.GetApplicableUplinkNetworks"
APPLICABLE_UNTAGGED = "NetworkService/Fabrics('{fabric_id}')/NetworkService.GetApplicableUplinkUntaggedNetworks"
IOM_DEVICES = "DeviceService/Devices?$filter=Type%20eq%204000"
PORT_INFO = "DeviceService/Devices({device_id})/InventoryDetails('portInformation')"
MEDIA_TYPES = "NetworkService/UplinkTypes"
VLAN_CONFIG = "NetworkConfigurationService/Networks"
#  Messages
CHECK_MODE_MSG = "Changes found to be applied."
NO_CHANGES_MSG = "No changes found to be applied to the uplink configuration."
SAME_SERVICE_TAG_MSG = "Primary and Secondary service tags must not be the same."


def get_item_id(rest_obj, name, uri, key='Name', attr='Id', value='value'):
    resp = rest_obj.invoke_request('GET', uri)
    tlist = []
    if resp.success and resp.json_data.get(value):
        tlist = resp.json_data.get(value, [])
        for xtype in tlist:
            if xtype.get(key, "") == name:
                return xtype.get(attr), tlist
    return 0, tlist


def get_all_uplink_ports(uplinks):
    portlist = []
    for uplink in uplinks:
        portlist = portlist + uplink.get("Ports")
    return portlist


def validate_ioms(module, rest_obj, uplinks):
    uplinkports = get_all_uplink_ports(uplinks)
    payload_ports = []
    occupied_ports = []
    used_ports = []
    for idx in uplinkports:
        used_ports.append(idx["Id"])
    iomsts = ("primary", "secondary")
    for iom in iomsts:
        prim_st = module.params.get(iom + "_switch_service_tag")
        if prim_st:
            prim_ports = list(str(port).strip() for port in module.params.get(iom + "_switch_ports"))
            id, ioms = get_item_id(rest_obj, prim_st, IOM_DEVICES, key="DeviceServiceTag")
            if not id:
                module.exit_json(msg="Device with service tag {0} does not exist.".format(prim_st),
                                 failed=True)
            resp = rest_obj.invoke_request("GET", PORT_INFO.format(device_id=id))
            port_info_data = resp.json_data.get("InventoryInfo", [])
            port_info_list = []
            for port in port_info_data:
                if port.get("SubPorts"):
                    for subport in port.get("SubPorts"):
                        port_info_list.append(subport["PortNumber"])
                else:
                    port_info_list.append(port["PortNumber"])
                # All ports are listed but with "OpticsType": "NotPresent" are shown on UI.
            non_exist_ports = []
            for port in prim_ports:
                if port not in port_info_list:
                    non_exist_ports.append(port)
                st_port = prim_st + ':' + port
                payload_ports.append(st_port)
                if st_port in used_ports:
                    occupied_ports.append(st_port)
            if non_exist_ports:
                module.exit_json(msg="{0} Port Numbers {1} does not exist for IOM {2}."
                                 .format(iom, (",".join(set(non_exist_ports))), prim_st),
                                 failed=True)
    if occupied_ports:
        module.exit_json(msg="Ports {0} are already occupied.".format(",".join(set(occupied_ports))),
                         failed=True)
    return payload_ports


def validate_networks(module, rest_obj, fabric_id, media_id):
    resp = rest_obj.invoke_request('POST', APPLICABLE_NETWORKS.format(fabric_id=fabric_id),
                                   data={"UplinkType": media_id})
    vlans = []
    if resp.json_data.get('ApplicableUplinkNetworks'):
        vlans = resp.json_data.get('ApplicableUplinkNetworks', [])
    vlan_payload = []
    vlan_dict = {}
    for vlan in vlans:
        vlan_dict[vlan["Name"]] = vlan["Id"]
    networks = list(str(net).strip() for net in module.params.get("tagged_networks"))
    invalids = []
    for ntw in networks:
        if vlan_dict.get(ntw):
            vlan_payload.append(vlan_dict.get(ntw))
        else:
            invalids.append(ntw)
    if invalids:
        module.exit_json(msg="Networks with names {0} are not applicable or valid.".format(",".join(set(invalids))),
                         failed=True)
    return vlan_payload


def validate_native_vlan(module, rest_obj, fabric_id, media_id):
    resp = rest_obj.invoke_request('POST', APPLICABLE_UNTAGGED.format(fabric_id=fabric_id),
                                   data={"UplinkType": media_id})
    vlans = []
    if resp.json_data.get('ApplicableUplinkNetworks'):
        vlans = resp.json_data.get('ApplicableUplinkNetworks', [])
    vlan_id = 0
    vlan_name = module.params.get("untagged_network")
    for vlan in vlans:
        if vlan["Name"] == vlan_name:
            vlan_id = vlan["VlanMaximum"]  # considering tagged vlans take the 'Id'
            break
    if not vlan_id:
        module.exit_json(msg="Native VLAN name {0} is not applicable or valid.".format(vlan_name),
                         failed=True)
    return vlan_id


def create_uplink(module, rest_obj, fabric_id, uplinks):
    mparams = module.params
    mandatory_parmas = ["name", "uplink_type", "tagged_networks"]
    for prm in mandatory_parmas:
        if not mparams.get(prm):
            module.exit_json(msg="Mandatory parameter {0} not provided for uplink creation.".format(prm),
                             failed=True)
    media_id, mtypes = get_item_id(rest_obj, mparams["uplink_type"], MEDIA_TYPES)
    if not media_id:
        module.exit_json(msg="Uplink Type {0} does not exist.".format(mparams["uplink_type"]),
                         failed=True)
    if mparams.get("primary_switch_service_tag") or mparams.get("secondary_switch_service_tag"):
        if mparams.get("primary_switch_service_tag") == mparams.get("secondary_switch_service_tag"):
            module.exit_json(msg=SAME_SERVICE_TAG_MSG, failed=True)
        payload_port_list = validate_ioms(module, rest_obj, uplinks)
    else:
        module.exit_json(msg="Provide port details.", failed=True)
    tagged_networks = validate_networks(module, rest_obj, fabric_id, media_id)
    create_payload = {
        "Name": mparams["name"],
        "MediaType": mparams["uplink_type"],
        "Ports": [{"Id": port} for port in payload_port_list],
        "Networks": [{"Id": net} for net in tagged_networks]
    }
    if mparams.get("untagged_network"):
        untagged_id = validate_native_vlan(module, rest_obj, fabric_id, media_id)
        create_payload["NativeVLAN"] = untagged_id
    if mparams.get("ufd_enable"):
        create_payload["UfdEnable"] = mparams.get("ufd_enable")
    if mparams.get("description"):
        create_payload["Description"] = mparams.get("description")
    if module.check_mode:
        module.exit_json(changed=True, msg=CHECK_MODE_MSG)
    resp = rest_obj.invoke_request("POST", UPLINKS_URI.format(fabric_id=fabric_id), data=create_payload)
    uplink_id = resp.json_data
    if isinstance(resp.json_data, dict):
        uplink_id, tmp = get_item_id(rest_obj, mparams["name"], UPLINKS_URI.format(fabric_id=fabric_id))
        if not uplink_id:
            uplink_id = ""
        module.exit_json(changed=True, msg="Successfully created the uplink.", uplink_id=uplink_id,
                         additional_info=resp.json_data)
    module.exit_json(changed=True, msg="Successfully created the uplink.", uplink_id=uplink_id)


def delete_uplink(module, rest_obj, fabric_id, uplink_id):
    if module.check_mode:
        module.exit_json(changed=True, msg=CHECK_MODE_MSG)
    rest_obj.invoke_request("DELETE", UPLINK_URI.format(fabric_id=fabric_id, uplink_id=uplink_id))
    module.exit_json(msg="Successfully deleted the uplink.", changed=True)


def modify_uplink(module, rest_obj, fabric_id, uplink, uplinks):
    mparams = module.params
    pload_keys = ["Id", "Name", "Description", "MediaType", "NativeVLAN", "UfdEnable", "Ports", "Networks"]
    modify_payload = dict((pload_key, uplink.get(pload_key)) for pload_key in pload_keys)
    port_list = list(port["Id"] for port in modify_payload["Ports"])
    modify_payload["Ports"] = sorted(list(set(port_list)))
    network_list = list(network["Id"] for network in modify_payload["Networks"])
    modify_payload["Networks"] = sorted(network_list)
    modify_data = {}
    if mparams.get("new_name"):
        modify_data["Name"] = mparams.get("new_name")
    if mparams.get("description"):
        modify_data["Description"] = mparams.get("description")
    if mparams.get("ufd_enable"):
        modify_data["UfdEnable"] = mparams.get("ufd_enable")
    if mparams.get("uplink_type"):
        if mparams.get("uplink_type") != uplink.get("MediaType"):
            module.exit_json(msg="Uplink Type cannot be modified.", failed=True)
        modify_data["MediaType"] = mparams["uplink_type"]
    if mparams.get("primary_switch_service_tag") or mparams.get("secondary_switch_service_tag"):
        if mparams.get("primary_switch_service_tag") == mparams.get("secondary_switch_service_tag"):
            module.exit_json(msg=SAME_SERVICE_TAG_MSG, failed=True)
        payload_port_list = validate_ioms(module, rest_obj, uplinks)
        modify_data["Ports"] = sorted(list(set(payload_port_list)))
    media_id, mtypes = get_item_id(rest_obj, uplink.get("MediaType"), MEDIA_TYPES)
    if mparams.get("tagged_networks") and media_id:
        tagged_networks = validate_networks(module, rest_obj, fabric_id, media_id)
        modify_data["Networks"] = sorted(tagged_networks)
    if mparams.get("untagged_network") and media_id:
        untagged_id = validate_native_vlan(module, rest_obj, fabric_id, media_id)
        modify_data["NativeVLAN"] = untagged_id
    diff = recursive_diff(modify_data, modify_payload)
    if diff and diff[0]:
        modify_payload.update(diff[0])
        if module.check_mode:
            module.exit_json(changed=True, msg=CHECK_MODE_MSG)
        modify_payload["Ports"] = list({"Id": port} for port in modify_payload["Ports"])
        modify_payload["Networks"] = list({"Id": net} for net in modify_payload["Networks"])
        resp = rest_obj.invoke_request("PUT", UPLINK_URI.format(fabric_id=fabric_id, uplink_id=uplink['Id']),
                                       data=modify_payload)
        if isinstance(resp.json_data, dict):
            module.exit_json(changed=True, msg="Successfully modified the uplink.", uplink_id=uplink['Id'],
                             additional_info=resp.json_data)
        module.exit_json(changed=True, msg="Successfully modified the uplink.", uplink_id=uplink['Id'])
    module.exit_json(msg=NO_CHANGES_MSG)


def main():
    specs = {
        "state": {"choices": ['present', 'absent'], "default": "present"},
        "fabric_name": {"required": True, "type": "str"},
        "name": {"required": True, "type": "str"},
        "new_name": {"type": "str"},
        "description": {"type": "str"},
        "uplink_type": {
            "choices": ['Ethernet', 'FCoE', 'FC Gateway', 'FC Direct Attach', 'Ethernet - No Spanning Tree']},
        "ufd_enable": {"choices": ['Enabled', 'Disabled']},
        "primary_switch_service_tag": {"type": "str"},
        "primary_switch_ports": {"type": "list", "elements": "str"},
        "secondary_switch_service_tag": {"type": "str"},
        "secondary_switch_ports": {"type": "list", "elements": "str"},
        "tagged_networks": {"type": "list", "elements": "str"},
        "untagged_network": {"type": "str"}
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        required_if=[['state', 'present',
                      ('new_name', 'description', 'uplink_type', 'ufd_enable',
                       'primary_switch_service_tag', 'primary_switch_ports', 'secondary_switch_service_tag',
                       'secondary_switch_ports', 'tagged_networks', 'untagged_network',), True]],
        required_together=[["primary_switch_service_tag", "primary_switch_ports"],
                           ["secondary_switch_service_tag", "secondary_switch_ports"]],
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            fabric_id, fabrics = get_item_id(rest_obj, module.params["fabric_name"], FABRIC_URI)
            if not fabric_id:
                module.exit_json(msg="Fabric with name {0} does not exist.".format(module.params["fabric_name"]),
                                 failed=True)
            uplink, uplinks = get_item_and_list(rest_obj, module.params["name"],
                                                UPLINKS_URI.format(fabric_id=fabric_id) + '?$expand=Ports,Networks')
            if module.params["state"] == "present":
                if uplink:
                    uplinks.remove(uplink)
                    modify_uplink(module, rest_obj, fabric_id, uplink, uplinks)
                create_uplink(module, rest_obj, fabric_id, uplinks)
            else:
                if uplink:
                    delete_uplink(module, rest_obj, fabric_id, uplink['Id'])
                if module.check_mode:
                    module.exit_json(msg=NO_CHANGES_MSG)
                module.exit_json(msg="Uplink {0} does not exist.".format(module.params["name"]))
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True, failed=True)
    except (IOError, ValueError, TypeError, ConnectionError, SSLValidationError, SSLError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == "__main__":
    main()
