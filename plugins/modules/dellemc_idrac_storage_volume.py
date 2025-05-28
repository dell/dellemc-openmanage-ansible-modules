#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.1.0
# Copyright (C) 2019-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: dellemc_idrac_storage_volume
short_description: Configures the RAID configuration attributes
version_added: "2.0.0"
deprecated:
  removed_at_date: "2026-03-31"
  why: Replaced with M(dellemc.openmanage.idrac_storage_volume).
  alternative: Use M(dellemc.openmanage.idrac_storage_volume) instead.
  removed_from_collection: dellemc.openmanage
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
  - "omsdk >= 1.2.488"
  - "python >= 3.9.6"
author: "Felix Stephen (@felixs88)"
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports both IPv4 and IPv6 address for I(idrac_ip).
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Create single volume
  dellemc.openmanage.dellemc_idrac_storage_volume:
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
  dellemc.openmanage.dellemc_idrac_storage_volume:
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
  dellemc.openmanage.dellemc_idrac_storage_volume:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "view"

- name: View specific volume details
  dellemc.openmanage.dellemc_idrac_storage_volume:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "view"
    controller_id: "RAID.Slot.1-1"
    volume_id: "Disk.Virtual.0:RAID.Slot.1-1"

- name: Delete single volume
  dellemc.openmanage.dellemc_idrac_storage_volume:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "delete"
    volumes:
      - name: "volume_1"

- name: Delete multiple volume
  dellemc.openmanage.dellemc_idrac_storage_volume:
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


import os
import tempfile
import copy
from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection, idrac_auth_params
from ansible.module_utils.basic import AnsibleModule
try:
    from omdrivers.types.iDRAC.RAID import RAIDactionTypes, RAIDdefaultReadPolicyTypes, RAIDinitOperationTypes, \
        DiskCachePolicyTypes, RAIDresetConfigTypes
    from omsdk.sdkfile import file_share_manager
except ImportError:
    pass


def error_handling_for_negative_num(option, val):
    return "{0} cannot be a negative number or zero,got {1}".format(option, val)


def set_liason_share(idrac, module):
    idrac.use_redfish = True
    share_name = tempfile.gettempdir() + os.sep
    storage_share = file_share_manager.create_share_obj(share_path=share_name,
                                                        isFolder=True)
    set_liason = idrac.config_mgr.set_liason_share(storage_share)
    if set_liason['Status'] == "Failed":
        liason_data = set_liason.get('Data', set_liason)
        module.fail_json(msg=liason_data.get('Message', "Failed to set Liason share"))


def view_storage(idrac, module):
    idrac.get_entityjson()
    storage_status = idrac.config_mgr.RaidHelper.view_storage(controller=module.params["controller_id"],
                                                              virtual_disk=module.params['volume_id'])
    if storage_status['Status'] == 'Failed':
        module.fail_json(msg="Failed to fetch storage details", storage_status=storage_status)
    return storage_status


def create_storage(idrac, module):
    pd_filter = '((disk.parent.parent is Controller and ' \
                'disk.parent.parent.FQDD._value == "{0}")' \
        .format(module.params["controller_id"])
    pd_filter += ' or (disk.parent is Controller and ' \
                 'disk.parent.FQDD._value == "{0}"))' \
        .format(module.params["controller_id"])

    vd_values = []
    if module.params['volumes'] is not None:
        for each in module.params['volumes']:
            mod_args = copy.deepcopy(module.params)
            each_vd = multiple_vd_config(mod_args=mod_args,
                                         each_vd=each, pd_filter=pd_filter)
            vd_values.append(each_vd)
    else:
        each_vd = multiple_vd_config(mod_args=module.params,
                                     pd_filter=pd_filter)
        vd_values.append(each_vd)
    storage_status = idrac.config_mgr.RaidHelper.new_virtual_disk(multiple_vd=vd_values,
                                                                  apply_changes=not module.check_mode)
    return storage_status


def delete_storage(idrac, module):
    names = [key.get("name") for key in module.params['volumes']]
    storage_status = idrac.config_mgr.RaidHelper.delete_virtual_disk(vd_names=names,
                                                                     apply_changes=not module.check_mode)
    return storage_status


def _validate_options(options):
    if options['state'] == "create":
        if options["controller_id"] is None or options["controller_id"] == "":
            raise ValueError('Controller ID is required.')
        capacity = options.get("capacity")
        if capacity is not None:
            size_check = float(capacity)
            if size_check <= 0:
                raise ValueError(error_handling_for_negative_num("capacity", capacity))
        stripe_size = options.get('stripe_size')
        if stripe_size is not None:
            stripe_size_check = int(stripe_size)
            if stripe_size_check <= 0:
                raise ValueError(error_handling_for_negative_num("stripe_size", stripe_size))
        # validating for each vd options
        if options['volumes'] is not None:
            for each in options['volumes']:
                drives = each.get("drives")
                if drives:
                    if "id" in drives and "location" in drives:
                        raise ValueError("Either {0} or {1} is allowed".format("id", "location"))
                    elif "id" not in drives and "location" not in drives:
                        raise ValueError("Either {0} or {1} should be specified".format("id", "location"))
                else:
                    raise ValueError("Drives must be defined for volume creation.")
                capacity = each.get("capacity")
                if capacity is not None:
                    size_check = float(capacity)
                    if size_check <= 0:
                        raise ValueError(error_handling_for_negative_num("capacity", capacity))
                stripe_size = each.get('stripe_size')
                if stripe_size is not None:
                    stripe_size_check = int(stripe_size)
                    if stripe_size_check <= 0:
                        raise ValueError(error_handling_for_negative_num("stripe_size", stripe_size))
    elif options['state'] == "delete":
        message = "Virtual disk name is a required parameter for remove virtual disk operations."
        if options['volumes'] is None or None in options['volumes']:
            raise ValueError(message)
        elif options['volumes']:
            if not all("name" in each for each in options['volumes']):
                raise ValueError(message)


def multiple_vd_config(mod_args=None, pd_filter="", each_vd=None):
    if mod_args is None:
        mod_args = {}
    if each_vd is None:
        each_vd = {}
    if each_vd:
        mod_args.update(each_vd)
    disk_size = None
    location_list = []
    id_list = []
    size = mod_args.get("capacity")
    drives = mod_args.get("drives")
    if drives:
        if "location" in drives:
            location_list = drives.get("location")
        elif "id" in drives:
            id_list = drives.get("id")
    if size is not None:
        size_check = float(size)
        disk_size = "{0}".format(int(size_check * 1073741824))

    if mod_args['media_type'] is not None:
        pd_filter += ' and disk.MediaType == "{0}"'.format(mod_args['media_type'])
    if mod_args["protocol"] is not None:
        pd_filter += ' and disk.BusProtocol == "{0}"'.format(mod_args["protocol"])
    pd_selection = pd_filter

    if location_list:
        slots = ""
        for i in location_list:
            slots += "\"" + str(i) + "\","
        slots_list = "[" + slots[0:-1] + "]"
        pd_selection += " and disk.Slot._value in " + slots_list
    elif id_list:
        pd_selection += " and disk.FQDD._value in " + str(id_list)

    raid_init_operation, raid_reset_config = "None", "False"
    if mod_args['raid_init_operation'] == "None":
        raid_init_operation = RAIDinitOperationTypes.T_None
    if mod_args['raid_init_operation'] == "Fast":
        raid_init_operation = RAIDinitOperationTypes.Fast

    if mod_args['raid_reset_config'] == "False":
        raid_reset_config = RAIDresetConfigTypes.T_False
    if mod_args['raid_reset_config'] == "True":
        raid_reset_config = RAIDresetConfigTypes.T_True

    vd_value = dict(
        Name=mod_args.get("name"),
        SpanDepth=int(mod_args['span_depth']),
        SpanLength=int(mod_args['span_length']),
        NumberDedicatedHotSpare=int(mod_args['number_dedicated_hot_spare']),
        RAIDTypes=mod_args["volume_type"],
        DiskCachePolicy=DiskCachePolicyTypes[mod_args['disk_cache_policy']],
        RAIDdefaultWritePolicy=mod_args['write_cache_policy'],
        RAIDdefaultReadPolicy=RAIDdefaultReadPolicyTypes[mod_args['read_cache_policy']],
        StripeSize=int(mod_args['stripe_size']),
        RAIDforeignConfig="Clear",
        RAIDaction=RAIDactionTypes.Create,
        PhysicalDiskFilter=pd_selection,
        Size=disk_size,
        RAIDresetConfig=raid_reset_config,
        RAIDinitOperation=raid_init_operation,
        PDSlots=location_list,
        ControllerFQDD=mod_args.get("controller_id"),
        mediatype=mod_args['media_type'],
        busprotocol=mod_args["protocol"],
        FQDD=id_list
    )
    return vd_value


def run_server_raid_config(idrac, module):
    if module.params['state'] == "view":
        storage_status = view_storage(idrac, module)
    if module.params['state'] == "create":
        set_liason_share(idrac, module)
        storage_status = create_storage(idrac, module)
    if module.params['state'] == "delete":
        set_liason_share(idrac, module)
        storage_status = delete_storage(idrac, module)
    return storage_status


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
        _validate_options(module.params)
        with iDRACConnection(module.params) as idrac:
            storage_status = run_server_raid_config(idrac, module)
            changed = False
            if 'changes_applicable' in storage_status:
                changed = storage_status['changes_applicable']
            elif module.params['state'] != 'view':
                if storage_status.get("Status", "") == "Success":
                    changed = True
                    if storage_status.get("Message", "") == "No changes found to commit!" \
                            or storage_status.get("Message", "") == "Unable to find the virtual disk":
                        changed = False
                        module.exit_json(msg=storage_status.get('Message', ""),
                                         changed=changed, storage_status=storage_status)
                elif storage_status.get("Status") == "Failed":
                    module.fail_json(msg=storage_status.get("Message"))
                else:
                    module.fail_json(msg="Failed to perform storage operation")
    except (ImportError, ValueError, RuntimeError, TypeError) as e:
        module.fail_json(msg=str(e))
    msg = "Successfully completed the {0} storage volume operation".format(module.params['state'])
    if module.check_mode and module.params['state'] != 'view':
        msg = storage_status.get("Message", "")
    module.exit_json(msg=msg, changed=changed, storage_status=storage_status)


if __name__ == '__main__':
    main()
