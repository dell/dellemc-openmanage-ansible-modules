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
module: ome_network_vlan
short_description: Create, modify & delete a VLAN
version_added: "2.1.0"
description:
  - This module allows to,
  - Create a VLAN on OpenManage Enterprise.
  - Modify or delete an existing VLAN on OpenManage Enterprise.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  state:
    type: str
    description:
      - C(present) creates a new VLAN or modifies an existing VLAN.
      - C(absent) deletes an existing VLAN.
      - I(WARNING) Deleting a VLAN can impact the network infrastructure.
    choices: [present, absent]
    default: present
  name:
    required: true
    type: str
    description: Provide the I(name) of the VLAN to be created, deleted or modified.
  new_name:
    type: str
    description: Provide the I(name) of the VLAN to be modified.
  description:
    type: str
    description: Short description of the VLAN to be created or modified.
  vlan_minimum:
    type: int
    description:
      - The minimum VLAN value of the range.
  vlan_maximum:
    type: int
    description:
      - The maximum VLAN value of the range.
      - A single value VLAN is created if the vlan_maximum and vlan_minmum values are the same.
  type:
    type: str
    description:
      - Types of supported VLAN networks.
      - "For the description of each network type,
      use API U(https://I(hostname)/api/NetworkConfigurationService/NetworkTypes)."
    choices: ['General Purpose (Bronze)', 'General Purpose (Silver)', 'General Purpose (Gold)',
              'General Purpose (Platinum)', 'Cluster Interconnect', 'Hypervisor Management',
              'Storage - iSCSI', 'Storage - FCoE', 'Storage - Data Replication',
              'VM Migration', 'VMWare FT Logging']
requirements:
    - "python >= 2.7.17"
author:
    - "Jagadeesh N V(@jagadeeshnv)"
notes:
    - Run this module from a system that has direct access to DellEMC OpenManage Enterprise.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Create a VLAN range
  dellemc.openmanage.ome_network_vlan:
    hostname: "{{hostname}}"
    username: "{{username}}"
    password: "{{password}}"
    state: present
    name: "vlan1"
    description: "VLAN desc"
    type: "General Purpose (Bronze)"
    vlan_minimum: 35
    vlan_maximum: 40
  tags: create_vlan_range

- name: Create a VLAN with a single value
  dellemc.openmanage.ome_network_vlan:
    hostname: "{{hostname}}"
    username: "{{username}}"
    password: "{{password}}"
    state: present
    name: "vlan2"
    description: "VLAN desc"
    type: "General Purpose (Bronze)"
    vlan_minimum: 127
    vlan_maximum: 127
  tags: create_vlan_single

- name: Modify a VLAN
  dellemc.openmanage.ome_network_vlan:
    hostname: "{{hostname}}"
    username: "{{username}}"
    password: "{{password}}"
    state: present
    name: "vlan1"
    new_name: "vlan_gold1"
    description: "new description"
    type: "General Purpose (Gold)"
    vlan_minimum: 45
    vlan_maximum: 50
  tags: modify_vlan

- name: Delete a VLAN
  dellemc.openmanage.ome_network_vlan:
    hostname: "{{hostname}}"
    username: "{{username}}"
    password: "{{password}}"
    state: "absent"
    name: "vlan1"
  tags: delete_vlan
'''

RETURN = r'''
---
msg:
  type: str
  description: Overall status of the VLAN operation.
  returned: always
  sample: "Successfully created the VLAN."
vlan_status:
  type: dict
  description: Details of the VLAN that is either created or modified.
  returned: when I(state=present)
  sample: {
        "@odata.context": "/api/$metadata#NetworkConfigurationService.Network",
        "@odata.type": "#NetworkConfigurationService.Network",
        "@odata.id": "/api/NetworkConfigurationService/Networks(1234)",
        "Id": 1234,
        "Name": "vlan1",
        "Description": "VLAN description",
        "VlanMaximum": 130,
        "VlanMinimum": 140,
        "Type": 1,
        "CreatedBy": "admin",
        "CreationTime": "2020-01-01 05:54:36.113",
        "UpdatedBy": null,
        "UpdatedTime": "2020-01-01 05:54:36.113",
        "InternalRefNWUUId": "6d6effcc-eca4-44bd-be07-1234ab5cd67e"
  }
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
        "code": "Base.1.0.GeneralError",
        "message": "A general error has occurred. See ExtendedInfo for more information.",
        "@Message.ExtendedInfo": [
            {
                "MessageId": "CTEM1043",
                "RelatedProperties": [],
                "Message": "Unable to create or update the network because the entered VLAN minimum 0
                is not within a valid range ( 1  -  4000  or  4021  -  4094 ).",
                "MessageArgs": [
                    "0",
                    "1",
                    "4000",
                    "4021",
                    "4094"
                ],
                "Severity": "Warning",
                "Resolution": "Enter a valid VLAN minimum as identified in the message and retry the operation."
            }
        ]
    }
'''

import json
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError

VLAN_CONFIG = "NetworkConfigurationService/Networks"
VLAN_ID_CONFIG = "NetworkConfigurationService/Networks({Id})"
VLAN_TYPES = "NetworkConfigurationService/NetworkTypes"
VLAN_RANGE_OVERLAP = "Unable to create or update the VLAN because the entered range" \
                     " overlaps with {vlan_name} with the range {vlan_min}-{vlan_max}."
VLAN_VALUE_MSG = "VLAN-minimum value is greater than VLAN-maximum value."
CHECK_MODE_MSG = "Changes found to be applied."


def format_payload(src_dict):
    address_payload_map = {
        "name": "Name",
        "vlan_maximum": "VlanMaximum",
        "vlan_minimum": "VlanMinimum",
        "type": "Type"
    }
    if src_dict:
        return dict([(address_payload_map[key], val) for key, val in src_dict.items() if key in address_payload_map])


def get_item_id(rest_obj, name, uri):
    resp = rest_obj.invoke_request('GET', uri)
    tlist = []
    if resp.success and resp.json_data.get('value'):
        tlist = resp.json_data.get('value', [])
        for xtype in tlist:
            if xtype.get('Name', "") == name:
                return xtype.get('Id'), tlist
    return 0, tlist


def check_overlapping_vlan_range(payload, vlans):
    current_vlan = None
    for xtype in vlans:
        overlap = list(range(max(xtype.get('VlanMinimum', 0), payload["VlanMinimum"]),
                             min(xtype.get('VlanMaximum', 0), payload["VlanMaximum"]) + 1))
        if overlap:
            current_vlan = xtype
            break
    return current_vlan


def create_vlan(module, rest_obj, vlans):
    payload = format_payload(module.params)
    if not all(payload.values()):
        module.fail_json(msg="The vlan_minimum, vlan_maximum and type values are required for creating a VLAN.")
    if payload["VlanMinimum"] > payload["VlanMaximum"]:
        module.fail_json(msg=VLAN_VALUE_MSG)
    overlap = check_overlapping_vlan_range(payload, vlans)
    if overlap:
        module.fail_json(msg=VLAN_RANGE_OVERLAP.format(vlan_name=overlap["Name"], vlan_min=overlap["VlanMinimum"],
                                                       vlan_max=overlap["VlanMaximum"]))
    if module.check_mode:
        module.exit_json(changed=True, msg=CHECK_MODE_MSG)
    if module.params.get("description"):
        payload["Description"] = module.params.get("description")
    payload["Type"], types = get_item_id(rest_obj, module.params["type"], VLAN_TYPES)
    if not payload["Type"]:
        module.fail_json(msg="Network type '{0}' not found.".format(module.params["type"]))
    resp = rest_obj.invoke_request("POST", VLAN_CONFIG, data=payload)
    module.exit_json(msg="Successfully created the VLAN.", vlan_status=resp.json_data, changed=True)


def delete_vlan(module, rest_obj, vlan_id):
    if module.check_mode:
        module.exit_json(changed=True, msg=CHECK_MODE_MSG)
    resp = rest_obj.invoke_request("DELETE", VLAN_ID_CONFIG.format(Id=vlan_id))
    module.exit_json(msg="Successfully deleted the VLAN.", changed=True)


def modify_vlan(module, rest_obj, vlan_id, vlans):
    payload = format_payload(module.params)
    payload["Description"] = module.params.get("description")
    if module.params.get("type"):
        payload["Type"], types = get_item_id(rest_obj, module.params["type"], VLAN_TYPES)
        if not payload["Type"]:
            module.fail_json(msg="Network type '{0}' not found.".format(module.params["type"]))
    if module.params.get("new_name"):
        payload["Name"] = module.params["new_name"]
    current_setting = {}
    for i in range(len(vlans)):
        if vlans[i]['Id'] == vlan_id:
            current_setting = vlans.pop(i)
            break
    diff = 0
    for config, pload in payload.items():
        pval = payload.get(config)
        if pval is not None:
            if current_setting.get(config) != pval:
                payload[config] = pval
                diff += 1
        else:
            payload[config] = current_setting.get(config)
    if payload["VlanMinimum"] > payload["VlanMaximum"]:
        module.fail_json(msg=VLAN_VALUE_MSG)
    overlap = check_overlapping_vlan_range(payload, vlans)
    if overlap:
        module.fail_json(msg=VLAN_RANGE_OVERLAP.format(vlan_name=overlap["Name"], vlan_min=overlap["VlanMinimum"],
                                                       vlan_max=overlap["VlanMaximum"]))
    if diff == 0:  # Idempotency
        if module.check_mode:
            module.exit_json(msg="No changes found to be applied to the VLAN configuration.")
        module.exit_json(msg="No changes found to be applied as the entered values are the same as the"
                             " current configuration.", vlan_status=current_setting)
    if module.check_mode:
        module.exit_json(changed=True, msg=CHECK_MODE_MSG)
    payload["Id"] = vlan_id
    resp = rest_obj.invoke_request("PUT", VLAN_ID_CONFIG.format(Id=vlan_id), data=payload)
    module.exit_json(msg="Successfully updated the VLAN.", vlan_status=resp.json_data, changed=True)


def check_existing_vlan(module, rest_obj):
    vlan_id, vlans = get_item_id(rest_obj, module.params["name"], VLAN_CONFIG + "?$top=9999")
    return vlan_id, vlans


def main():
    module = AnsibleModule(
        argument_spec={
            "hostname": {"required": True, "type": "str"},
            "username": {"required": True, "type": "str"},
            "password": {"required": True, "type": "str", "no_log": True},
            "port": {"required": False, "type": "int", "default": 443},
            "state": {"required": False, "choices": ['present', 'absent'], "default": "present"},
            "name": {"required": True, "type": "str"},
            "new_name": {"required": False, "type": "str"},
            "description": {"required": False, "type": "str"},
            "vlan_minimum": {"required": False, "type": "int"},
            "vlan_maximum": {"required": False, "type": "int"},
            "type": {"required": False, "type": "str",
                     "choices": ['General Purpose (Bronze)', 'General Purpose (Silver)', 'General Purpose (Gold)',
                                 'General Purpose (Platinum)', 'Cluster Interconnect', 'Hypervisor Management',
                                 'Storage - iSCSI', 'Storage - FCoE', 'Storage - Data Replication', 'VM Migration',
                                 'VMWare FT Logging']}
        },
        required_if=[['state', 'present', ('new_name', 'description', 'vlan_minimum', 'vlan_maximum', 'type',), True]],
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            vlan_id, vlans = check_existing_vlan(module, rest_obj)
            if module.params["state"] == "present":
                if vlan_id:
                    modify_vlan(module, rest_obj, vlan_id, vlans)
                create_vlan(module, rest_obj, vlans)
            else:
                if vlan_id:
                    delete_vlan(module, rest_obj, vlan_id)
                if module.check_mode:
                    module.exit_json(msg="No changes found to be applied to the VLAN configuration.")
                module.exit_json(msg="VLAN {0} does not exist.".format(module.params["name"]))
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, TypeError, ConnectionError, SSLValidationError, SSLError) as err:
        module.fail_json(msg=str(err))
    except Exception as err:
        module.fail_json(msg=str(err))


if __name__ == "__main__":
    main()
