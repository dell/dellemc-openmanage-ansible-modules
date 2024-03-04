#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.1.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: idrac_storage_volume
short_description: Configures the RAID configuration attributes
version_added: "9.1.0"
description:
  - This module is responsible for configuring the RAID attributes.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
  state:
    type: str
    description:
      - C(create), performs create volume operation.
      - C(delete), performs remove volume operation.
      - C(view), returns storage view.
    choices: ['create', 'delete', 'view']
    default: 'view'
  span_depth:
    type: int
    description:
      - Number of spans in the RAID configuration.
      - I(span_depth) is required for C(create) and its value depends on I(volume_type).
    default: 1
  span_length:
    type: int
    description:
      - Number of disks in a span.
      - I(span_length) is required for C(create) and its value depends on I(volume_type).
    default: 1
  number_dedicated_hot_spare:
    type: int
    description: Number of Dedicated Hot Spare.
    default: 0
  volume_type:
    type: str
    description: Provide the the required RAID level.
    choices: ['RAID 0', 'RAID 1', 'RAID 5', 'RAID 6', 'RAID 10', 'RAID 50', 'RAID 60']
    default: 'RAID 0'
  disk_cache_policy:
    type: str
    description: Disk Cache Policy.
    choices: ["Default", "Enabled", "Disabled"]
    default: "Default"
  write_cache_policy:
    type: str
    description: Write cache policy.
    choices: ["WriteThrough", "WriteBack", "WriteBackForce"]
    default: "WriteThrough"
  read_cache_policy:
    type: str
    description: Read cache policy.
    choices: ["NoReadAhead", "ReadAhead", "AdaptiveReadAhead"]
    default: "NoReadAhead"
  stripe_size:
    type: int
    description: Stripe size value to be provided in multiples of 64 * 1024.
    default: 65536
  controller_id:
    type: str
    description:
      - >-
        Fully Qualified Device Descriptor (FQDD) of the storage controller, for example 'RAID.Integrated.1-1'.
        Controller FQDD is required for C(create) RAID configuration.
  media_type:
    type: str
    description: Media type.
    choices: ['HDD', 'SSD']
  protocol:
    type: str
    description: Bus protocol.
    choices: ['SAS', 'SATA']
  volume_id:
    type: str
    description:
      - >-
        Fully Qualified Device Descriptor (FQDD) of the virtual disk, for example 'Disk.virtual.0:RAID.Slot.1-1'.
        This option is used to get the virtual disk information.
  volumes:
    type: list
    elements: dict
    description:
      - >-
        A list of virtual disk specific iDRAC attributes. This is applicable for C(create) and C(delete) operations.
      - >-
        For C(create) operation, name and drives are applicable options, other volume options can also be specified.
      - >-
        The drives is a required option for C(create) operation and accepts either location (list of drive slot)
        or id (list of drive fqdd).
      - >-
        For C(delete) operation, only name option is applicable.
      - See the examples for more details.
  capacity:
    type: float
    description: Virtual disk size in GB.
  raid_reset_config:
    type: str
    description:
      - >-
        This option represents whether a reset config operation needs to be performed on the RAID controller.
        Reset Config operation deletes all the virtual disks present on the RAID controller.
    choices: ['True', 'False']
    default: 'False'
  raid_init_operation:
    type: str
    description: This option represents initialization configuration operation to be performed on the virtual disk.
    choices: [None, Fast]

requirements:
  - "python >= 3.9.6"
author: 
  - "Felix Stephen (@felixs88)"
  - "Kritika Bhateja (@Kritika-Bhateja-03)"
  - "Abhishek Sinha(@ABHISHEK-SINHA10)"
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports both IPv4 and IPv6 address for I(idrac_ip).
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Create single volume
  dellemc.openmanage.idrac_storage_volume:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "create"
    controller_id: "RAID.Slot.1-1"
    volumes:
      - drives:
        location: [5]

- name: Create multiple volume
  dellemc.openmanage.idrac_storage_volume:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    raid_reset_config: "True"
    state: "create"
    controller_id: "RAID.Slot.1-1"
    volume_type: "RAID 1"
    span_depth: 1
    span_length: 2
    number_dedicated_hot_spare: 1
    disk_cache_policy: "Enabled"
    write_cache_policy: "WriteBackForce"
    read_cache_policy: "ReadAhead"
    stripe_size: 65536
    capacity: 100
    raid_init_operation: "Fast"
    volumes:
      - name: "volume_1"
        drives:
          id: ["Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1", "Disk.Bay.2:Enclosure.Internal.0-1:RAID.Slot.1-1"]
      - name: "volume_2"
        volume_type: "RAID 5"
        span_length: 3
        span_depth: 1
        drives:
          location: [7, 3, 5]
        disk_cache_policy: "Disabled"
        write_cache_policy: "WriteBack"
        read_cache_policy: "NoReadAhead"
        stripe_size: 131072
        capacity: "200"
        raid_init_operation: "None"

- name: View all volume details
  dellemc.openmanage.idrac_storage_volume:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "view"

- name: View specific volume details
  dellemc.openmanage.idrac_storage_volume:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "view"
    controller_id: "RAID.Slot.1-1"
    volume_id: "Disk.Virtual.0:RAID.Slot.1-1"

- name: Delete single volume
  dellemc.openmanage.idrac_storage_volume:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "delete"
    volumes:
      - name: "volume_1"

- name: Delete multiple volume
  dellemc.openmanage.idrac_storage_volume:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "delete"
    volumes:
      - name: "volume_1"
      - name: "volume_2"
'''

RETURN = r'''
---
msg:
  type: str
  description: Overall status of the storage configuration operation.
  returned: always
  sample: "Successfully completed the view storage volume operation"
storage_status:
  type: dict
  description: Storage configuration job and progress details from the iDRAC.
  returned: success
  sample:
    {
      "Id": "JID_XXXXXXXXX",
      "JobState": "Completed",
      "JobType": "ImportConfiguration",
      "Message": "Successfully imported and applied Server Configuration Profile.",
      "MessageId": "XXX123",
      "Name": "Import Configuration",
      "PercentComplete": 100,
      "StartTime": "TIME_NOW",
      "Status": "Success",
      "TargetSettingsURI": null,
      "retval": true
    }
'''

import json
import time
from urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, idrac_auth_params
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    get_dynamic_uri, validate_and_get_first_resource_id_uri, check_specified_identifier_exists_in_the_system)


SYSTEMS_URI = "/redfish/v1/Systems"
CONTROLLER_NOT_EXIST_ERROR = "Specified Controller {controller_id} does not exist in the System."
SUCCESSFUL_OPERATION_MSG = "Successfully completed the {operation} storage volume operation"
DRIVES_NOT_EXIST_ERROR = "No Drive(s) are attached to the specified Controller Id: {controller_id}."
DRIVES_NOT_MATCHED = "Following Drive(s) {specified_drives} are not attached to the specified Controller Id: {controller_id}"

class StorageBase:
    def __init__(self, idrac, module):
      self.module = module
      self.idrac = idrac

    def module_extend_input(self):
        volume_related_input = ['volume_type', 'span_length', 'span_depth',
                                'number_dedicated_hot_spare', 'disk_cache_policy',
                                'write_cache_policy', 'read_cache_policy', 'stripe_size',
                                'capacity', 'raid_init_operation']
        if self.module.params.get('volumes'):
            for each_member in self.module.params.get('volumes'):
                for key in volume_related_input:
                    if key in each_member:
                        each_member[key] = self.module.params.get(key)
        return self.module.params
              

class StorageValidation:
    def validate(self):
        pass
    
    def execute(self):
        pass

class StorageView(StorageBase):
    def validate(self):
        pass
    
    def execute(self):
        pass

class StorageCreate(StorageBase):
    def validate(self):
        pass
    
    def execute(self):
        pass

class StorageUpdate(StorageBase):
    def validate(self):
        pass
    
    def execute(self):
        pass

class StorageDelete(StorageBase):
    def validate(self):
        pass
    
    def execute(self):
        pass


class StorageDataAndValidation:
    def __init__(self, idrac, module):
        self.module = module
        self.idrac = idrac
        self.controller_id = self.module.params.get("controller_id")

    def fetch_storage_data(self):
        storage_info = {}
        storage_controllers = self.fetch_controllers_uri()
        controllers_details_uri = (
            f"{storage_controllers['@odata.id']}?$expand=*($levels=1)"
        )
        controllers_list = get_dynamic_uri(self.idrac, controllers_details_uri)
        for member in controllers_list['Members']:
            controllers = member.get("Controllers")
            if controllers:
                controller_name = (controllers["@odata.id"].split("/")[-2])
                storage_info[controller_name] = {}
                drives = [
                    drive['@odata.id'].split("/")[-1] 
                    for drive in member['Drives']
                ]
                if drives:
                    storage_info[controller_name]['PhysicalDisk'] = drives
        return storage_info
    
def main():
    specs = {
        "state": {"required": False, "choices": ['create', 'delete', 'view'], "default": 'view'},
        "volume_id": {"required": False, "type": 'str'},
        "volumes": {"required": False, "type": 'list', "elements": 'dict'},
        "span_depth": {"required": False, "type": 'int', "default": 1},
        "span_length": {"required": False, "type": 'int', "default": 1},
        "number_dedicated_hot_spare": {"required": False, "type": 'int', "default": 0},
        "volume_type": {"required": False,
                        "choices": ['RAID 0', 'RAID 1', 'RAID 5', 'RAID 6', 'RAID 10', 'RAID 50', 'RAID 60'],
                        "default": 'RAID 0'},
        "disk_cache_policy": {"required": False, "choices": ["Default", "Enabled", "Disabled"],
                              "default": "Default"},
        "write_cache_policy": {"required": False, "choices": ["WriteThrough", "WriteBack", "WriteBackForce"],
                               "default": "WriteThrough"},
        "read_cache_policy": {"required": False, "choices": ["NoReadAhead", "ReadAhead", "AdaptiveReadAhead"],
                              "default": "NoReadAhead"},
        "stripe_size": {"required": False, "type": 'int', "default": 64 * 1024},
        "capacity": {"required": False, "type": 'float'},
        "controller_id": {"required": False, "type": 'str'},
        "media_type": {"required": False, "choices": ['HDD', 'SSD']},
        "protocol": {"required": False, "choices": ['SAS', 'SATA']},
        "raid_reset_config": {"required": False, "choices": ['True', 'False'], "default": 'False'},
        "raid_init_operation": {"required": False, "choices": ['None', 'Fast']}
    }
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        supports_check_mode=True)
    
    try:
        with iDRACRedfishAPI(module.params) as idrac:
            changed = False
            storage_obj = StorageDataAndValidation(idrac, module)
            storage_output = {}
            if module.params['state'] == 'view':
                storage_output = storage_obj.fetch_storage_data()
    except (ImportError, ValueError, RuntimeError, TypeError) as e:
        module.exit_json(msg=str(e), failed=True)
    msg = SUCCESSFUL_OPERATION_MSG.format(operation = module.params['state'])
    module.exit_json(msg=msg, changed=changed, storage_status=storage_output)


if __name__ == '__main__':
    main()
