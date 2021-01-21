#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.0.0
# Copyright (C) 2019-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: redfish_storage_volume
short_description: Manages the storage volume configuration
version_added: "2.1.0"
description:
   - This module allows to create, modify, initialize, or delete a single storage volume.
extends_documentation_fragment:
  - dellemc.openmanage.redfish_auth_options
options:
  controller_id:
    description:
      - Fully Qualified Device Descriptor (FQDD) of the storage controller.
      - For example- RAID.Slot.1-1.
      - This option is mandatory when I(state) is C(present) while creating a volume.
    type: str
  volume_id:
    description:
      - FQDD of existing volume.
      - For example- Disk.Virtual.4:RAID.Slot.1-1.
      - This option is mandatory in the following scenarios,
      - >-
        I(state) is C(present), when updating a volume.
      - >-
        I(state) is C(absent), when deleting a volume.
      - >-
        I(command) is C(initialize), when initializing a volume.
    type: str
  state:
    description:
      - >-
        C(present) creates a storage volume for the specified I (controller_id), or modifies the storage volume for the
        specified I (volume_id).
        "Note: Modification of an existing volume properties depends on drive and controller capabilities".
      - C(absent) deletes the volume for the specified I(volume_id).
    type: str
    choices: [present, absent]
  command:
    description:
      - C(initialize) initializes an existing storage volume for a specified I(volume_id).
    type: str
    choices: [initialize]
  volume_type:
    description:
      - One of the following volume types must be selected to create a volume.
      - >-
        C(Mirrored) The volume is a mirrored device.
      - >-
        C(NonRedundant) The volume is a non-redundant storage device.
      - >-
        C(SpannedMirrors) The volume is a spanned set of mirrored devices.
      - >-
        C(SpannedStripesWithParity) The volume is a spanned set of devices which uses parity to retain redundant
        information.
      - >-
        C(StripedWithParity) The volume is a device which uses parity to retain redundant information.
    type: str
    choices: [NonRedundant, Mirrored, StripedWithParity, SpannedMirrors, SpannedStripesWithParity]
  name:
    description:
      - Name of the volume to be created.
      - Only applicable when I(state) is C(present).
    type: str
  drives:
    description:
      - FQDD of the Physical disks.
      - For example- Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1.
      - Only applicable when I(state) is C(present) when creating a new volume.
    type: list
    elements: str
  block_size_bytes:
    description:
      - Block size in bytes.Only applicable when I(state) is C(present).
    type: int
  capacity_bytes:
    description:
      - Volume size in bytes.
      - Only applicable when I(state) is C(present).
    type: str
  optimum_io_size_bytes:
    description:
      - Stripe size value must be in multiples of 64 * 1024.
      - Only applicable when I(state) is C(present).
    type: int
  encryption_types:
    description:
      - The following encryption types can be selected.
      - C(ControllerAssisted) The volume is encrypted by the storage controller entity.
      - C(NativeDriveEncryption) The volume utilizes the native drive encryption capabilities
       of the drive hardware.
      - C(SoftwareAssisted) The volume is encrypted by the software running
       on the system or the operating system.
      - Only applicable when I(state) is C(present).
    type: str
    choices: [NativeDriveEncryption, ControllerAssisted, SoftwareAssisted]
  encrypted:
    description:
      - Indicates whether volume is currently utilizing encryption or not.
      - Only applicable when I(state) is C(present).
    type: bool
  oem:
    description:
      - Includes OEM extended payloads.
      - Only applicable when I(state) is I(present).
    type: dict
  initialize_type:
    description:
      - Initialization type of existing volume.
      - Only applicable when I(command) is C(initialize).
    type: str
    choices: [Fast, Slow]
    default: Fast

requirements:
  - "python >= 2.7.5"
author: "Sajna Shetty(@Sajna-Shetty)"
notes:
    - Run this module from a system that has direct access to Redfish APIs.
    - This module does not support C(check_mode).
'''

EXAMPLES = r'''
---
- name: Create a volume with supported options
  dellemc.openmanage.redfish_storage_volume:
    baseuri: "192.168.0.1"
    username: "username"
    password: "password"
    state: "present"
    volume_type: "Mirrored"
    name: "VD0"
    controller_id: "RAID.Slot.1-1"
    drives:
      - Disk.Bay.5:Enclosure.Internal.0-1:RAID.Slot.1-1
      - Disk.Bay.6:Enclosure.Internal.0-1:RAID.Slot.1-1
    block_size_bytes: 512
    capacity_bytes: 299439751168
    optimum_io_size_bytes: 65536
    encryption_types: NativeDriveEncryption
    encrypted: true

- name: Create a volume with minimum options
  dellemc.openmanage.redfish_storage_volume:
    baseuri: "192.168.0.1"
    username: "username"
    password: "password"
    state: "present"
    controller_id: "RAID.Slot.1-1"
    volume_type: "NonRedundant"
    drives:
       - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1

- name: Modify a volume's encryption type settings
  dellemc.openmanage.redfish_storage_volume:
    baseuri: "192.168.0.1"
    username: "username"
    password: "password"
    state: "present"
    volume_id: "Disk.Virtual.5:RAID.Slot.1-1"
    encryption_types: "ControllerAssisted"
    encrypted: true

- name: Delete an existing volume
  dellemc.openmanage.redfish_storage_volume:
    baseuri: "192.168.0.1"
    username: "username"
    password: "password"
    state: "absent"
    volume_id: "Disk.Virtual.5:RAID.Slot.1-1"

- name: Initialize an existing volume
  dellemc.openmanage.redfish_storage_volume:
    baseuri: "192.168.0.1"
    username: "username"
    password: "password"
    command: "initialize"
    volume_id: "Disk.Virtual.6:RAID.Slot.1-1"
    initialize_type: "Slow"
'''

RETURN = r'''
---
msg:
  description: Overall status of the storage configuration operation.
  returned: always
  type: str
  sample: "Successfully submitted create volume task."
task:
  type: dict
  description: Returns ID and URI of the created task.
  returned: success
  sample: {
    "id": "JID_XXXXXXXXXXXXX",
    "uri": "/redfish/v1/TaskService/Tasks/JID_XXXXXXXXXXXXX"
  }
error_info:
  type: dict
  description: Details of a http error.
  returned: on http error
  sample:  {
    "error": {
        "@Message.ExtendedInfo": [
            {
                "Message": "Unable to perform configuration operations because a
                          configuration job for the device already exists.",
                "MessageArgs": [],
                "MessageArgs@odata.count": 0,
                "MessageId": "IDRAC.1.6.STOR023",
                "RelatedProperties": [],
                "RelatedProperties@odata.count": 0,
                "Resolution": "Wait for the current job for the device to complete
                    or cancel the current job before attempting more configuration
                     operations on the device.",
                "Severity": "Informational"
            }
        ],
        "code": "Base.1.2.GeneralError",
        "message": "A general error has occurred. See ExtendedInfo for more information"
    }
  }
'''

import json
from ansible_collections.dellemc.openmanage.plugins.module_utils.redfish import Redfish
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


VOLUME_INITIALIZE_URI = "{storage_base_uri}/Volumes/{volume_id}/Actions/Volume.Initialize"
DRIVES_URI = "{storage_base_uri}/Drives/{driver_id}"
CONTROLLER_URI = "{storage_base_uri}/{controller_id}"
SETTING_VOLUME_ID_URI = "{storage_base_uri}/Volumes/{volume_id}/Settings"
CONTROLLER_VOLUME_URI = "{storage_base_uri}/{controller_id}/Volumes"
VOLUME_ID_URI = "{storage_base_uri}/Volumes/{volume_id}"
storage_collection_map = {}


def fetch_storage_resource(module, session_obj):
    try:
        system_uri = "{0}{1}".format(session_obj.root_uri, "Systems")
        system_resp = session_obj.invoke_request("GET", system_uri)
        system_members = system_resp.json_data.get("Members")
        if system_members:
            system_id_res = system_members[0]["@odata.id"]
            system_id_res_resp = session_obj.invoke_request("GET", system_id_res)
            system_id_res_data = system_id_res_resp.json_data.get("Storage")
            if system_id_res_data:
                storage_collection_map.update({"storage_base_uri": system_id_res_data["@odata.id"]})
            else:
                module.fail_json(msg="Target out-of-band controller does not support storage feature using Redfish API.")
        else:
            module.fail_json(msg="Target out-of-band controller does not support storage feature using Redfish API.")
    except HTTPError as err:
        if err.code in [404, 405]:
            module.fail_json(msg="Target out-of-band controller does not support storage feature using Redfish API.",
                             error_info=json.load(err))
        raise err
    except (URLError, SSLValidationError, ConnectionError, TypeError, ValueError) as err:
        raise err


def volume_payload(module):
    params = module.params
    drives = params.get("drives")
    capacity_bytes = params.get("capacity_bytes")
    physical_disks = []
    oem = params.get("oem")
    encrypted = params.get("encrypted")
    encryption_types = params.get("encryption_types")
    if capacity_bytes:
        capacity_bytes = int(capacity_bytes)
    if drives:
        storage_base_uri = storage_collection_map["storage_base_uri"]
        physical_disks = [{"@odata.id": DRIVES_URI.format(storage_base_uri=storage_base_uri,
                                                          driver_id=drive_id)} for drive_id in drives]

    raid_mapper = {
        "Name": params.get("name"),
        "VolumeType": params.get("volume_type"),
        "BlockSizeBytes": params.get("block_size_bytes"),
        "CapacityBytes": capacity_bytes,
        "OptimumIOSizeBytes": params.get("optimum_io_size_bytes"),
        "Drives": physical_disks
    }
    raid_payload = dict([(k, v) for k, v in raid_mapper.items() if v])
    if oem:
        raid_payload.update(params.get("oem"))
    if encrypted is not None:
        raid_payload.update({"Encrypted": encrypted})
    if encryption_types:
        raid_payload.update({"EncryptionTypes": [encryption_types]})

    return raid_payload


def check_physical_disk_exists(module, drives):
    """
    validation to check if physical disks(drives) available for the specified controller
    """
    specified_drives = module.params.get("drives")
    if specified_drives:
        existing_drives = []
        specified_controller_id = module.params.get("controller_id")
        if drives:
            for drive in drives:
                drive_uri = drive['@odata.id']
                drive_id = drive_uri.split("/")[-1]
                existing_drives.append(drive_id)
        else:
            module.fail_json(msg="No Drive(s) are attached to the specified "
                                 "Controller Id: {0}.".format(specified_controller_id))
        invalid_drives = list(set(specified_drives) - set(existing_drives))
        if invalid_drives:
            invalid_drive_msg = ",".join(invalid_drives)
            module.fail_json(msg="Following Drive(s) {0} are not attached to the "
                                 "specified Controller Id: {1}.".format(invalid_drive_msg, specified_controller_id))
    return True


def check_specified_identifier_exists_in_the_system(module, session_obj, uri, err_message):
    """
    common validation to check if , specified volume or controller id exist in the system or not
    """
    try:
        resp = session_obj.invoke_request('GET', uri)
        return resp
    except HTTPError as err:
        if err.code == 404:
            module.fail_json(msg=err_message)
        raise err
    except (URLError, SSLValidationError, ConnectionError, TypeError, ValueError) as err:
        raise err


def check_controller_id_exists(module, session_obj):
    """
    Controller availability Validation
    """
    specified_controller_id = module.params.get("controller_id")
    uri = CONTROLLER_URI.format(storage_base_uri=storage_collection_map["storage_base_uri"], controller_id=specified_controller_id)
    err_message = "Specified Controller {0} does " \
                  "not exist in the System.".format(specified_controller_id)
    resp = check_specified_identifier_exists_in_the_system(module, session_obj, uri, err_message)
    if resp.success:
        return check_physical_disk_exists(module, resp.json_data["Drives"])
    else:
        module.fail_json(msg="Failed to retrieve the details of the specified Controller Id "
                             "{0}.".format(specified_controller_id))


def check_volume_id_exists(module, session_obj, volume_id):
    """
    validation to check if volume id is valid in case of modify, delete, initialize operation
    """
    uri = VOLUME_ID_URI.format(storage_base_uri=storage_collection_map["storage_base_uri"], volume_id=volume_id)
    err_message = "Specified Volume Id {0} does not exist in the System.".format(volume_id)
    resp = check_specified_identifier_exists_in_the_system(module, session_obj, uri, err_message)
    return resp


def check_initialization_progress(module, session_obj, volume_id):
    """
    validation check if any operation is running in specified volume id.
    """
    operations = []
    resp = check_volume_id_exists(module, session_obj, volume_id)
    if resp.success:
        operations = resp.json_data["Operations"]
    return operations


def perform_storage_volume_action(method, uri, session_obj, action, payload=None):
    """
    common request call for raid creation update delete and initialization
    """
    try:
        resp = session_obj.invoke_request(method, uri, data=payload)
        task_uri = resp.headers["Location"]
        return get_success_message(action, task_uri)
    except (HTTPError, URLError, SSLValidationError, ConnectionError,
            TypeError, ValueError) as err:
        raise err


def perform_volume_create_modify(module, session_obj):
    """
    perform volume creation and modification for state present
    """
    specified_controller_id = module.params.get("controller_id")
    volume_id = module.params.get("volume_id")
    if specified_controller_id is not None:
        check_controller_id_exists(module, session_obj)
        uri = CONTROLLER_VOLUME_URI.format(storage_base_uri=storage_collection_map["storage_base_uri"],
                                           controller_id=specified_controller_id)
        method = "POST"
        action = "create"
    else:
        resp = check_volume_id_exists(module, session_obj, volume_id)
        if resp.success:
            uri = SETTING_VOLUME_ID_URI.format(storage_base_uri=storage_collection_map["storage_base_uri"],
                                               volume_id=volume_id)
            method = "PATCH"
            action = "modify"
    payload = volume_payload(module)
    if not payload:
        module.fail_json(msg="Input options are not provided for the {0} volume task.".format(action))
    return perform_storage_volume_action(method, uri, session_obj, action, payload)


def perform_volume_deletion(module, session_obj):
    """
    perform volume deletion for state absent
    """
    volume_id = module.params.get("volume_id")
    if volume_id:
        resp = check_volume_id_exists(module, session_obj, volume_id)
        if resp.success:
            uri = VOLUME_ID_URI.format(storage_base_uri=storage_collection_map["storage_base_uri"], volume_id=volume_id)
            method = "DELETE"
            return perform_storage_volume_action(method, uri, session_obj, "delete")
    else:
        module.fail_json(msg="'volume_id' option is a required property for deleting a volume.")


def perform_volume_initialization(module, session_obj):
    """
    perform volume initialization for command initialize
    """
    specified_volume_id = module.params.get("volume_id")
    if specified_volume_id:
        operations = check_initialization_progress(module, session_obj, specified_volume_id)
        if operations:
            operation_message = "Cannot perform the configuration operations because a " \
                                "configuration job for the device already exists."
            operation_name = operations[0].get("OperationName")
            percentage_complete = operations[0].get("PercentageComplete")
            if operation_name and percentage_complete:
                operation_message = "Cannot perform the configuration operation because the configuration job '{0}'" \
                                    " in progress is at '{1}' percentage.".format(operation_name, percentage_complete)
            module.fail_json(msg=operation_message)
        else:
            method = "POST"
            uri = VOLUME_INITIALIZE_URI.format(storage_base_uri=storage_collection_map["storage_base_uri"],
                                               volume_id=specified_volume_id)
            payload = {"InitializeType": module.params["initialize_type"]}
            return perform_storage_volume_action(method, uri, session_obj, "initialize", payload)
    else:
        module.fail_json(msg="'volume_id' option is a required property for initializing a volume.")


def configure_raid_operation(module, session_obj):
    """
    configure raid action based on state and command input
    """
    module_params = module.params
    state = module_params.get("state")
    command = module_params.get("command")
    if state is not None and state == "present":
        return perform_volume_create_modify(module, session_obj)
    elif state is not None and state == "absent":
        return perform_volume_deletion(module, session_obj)
    elif command is not None and command == "initialize":
        return perform_volume_initialization(module, session_obj)


def get_success_message(action, task_uri):
    """
    message for different types of raid actions
    """
    msg = "Successfully submitted {0} volume task.".format(action)
    status_message = {"msg": msg}
    if task_uri is not None:
        task_id = task_uri.split("/")[-1]
        status_message.update({"task_uri": task_uri, "task_id": task_id})
    return status_message


def validate_inputs(module):
    """
    validation check for state and command input for null values.
    """
    module_params = module.params
    state = module_params.get("state")
    command = module_params.get("command")
    if state is None and command is None:
        module.fail_json(msg="Either state or command should be provided to further actions.")
    elif state == "present" and\
            module_params.get("controller_id") is None and\
            module_params.get("volume_id") is None:
        module.fail_json(msg="When state is present, either controller_id or"
                         " volume_id must be specified to perform further actions.")


def main():
    module = AnsibleModule(
        argument_spec={
            "baseuri": {"required": True, "type": "str"},
            "username": {"required": True, "type": "str"},
            "password": {"required": True, "type": "str", "no_log": True},
            "state": {"type": "str", "required": False, "choices": ['present', 'absent']},
            "command": {"type": "str", "required": False, "choices": ['initialize']},
            "volume_type": {"type": "str", "required": False,
                            "choices": ['NonRedundant', 'Mirrored',
                                        'StripedWithParity', 'SpannedMirrors',
                                        'SpannedStripesWithParity']},
            "name": {"required": False, "type": "str"},
            "controller_id": {"required": False, "type": "str"},
            "drives": {"elements": "str", "required": False, "type": "list"},
            "block_size_bytes": {"required": False, "type": "int"},
            "capacity_bytes": {"required": False, "type": "str"},
            "optimum_io_size_bytes": {"required": False, "type": "int"},
            "encryption_types": {"type": "str", "required": False,
                                 "choices": ['NativeDriveEncryption', 'ControllerAssisted', 'SoftwareAssisted']},
            "encrypted": {"required": False, "type": "bool"},
            "volume_id": {"required": False, "type": "str"},
            "oem": {"required": False, "type": "dict"},
            "initialize_type": {"type": "str", "required": False, "choices": ['Fast', 'Slow'], "default": "Fast"},

        },
        mutually_exclusive=[['state', 'command']],
        required_one_of=[['state', 'command']],
        required_if=[['command', 'initialize', ['volume_id']],
                     ['state', 'absent', ['volume_id']], ],
        supports_check_mode=False)

    try:
        validate_inputs(module)
        with Redfish(module.params, req_session=True) as session_obj:
            fetch_storage_resource(module, session_obj)
            status_message = configure_raid_operation(module, session_obj)
            task_status = {"uri": status_message.get("task_uri"), "id": status_message.get("task_id")}
            module.exit_json(msg=status_message["msg"], task=task_status, changed=True)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except (URLError, SSLValidationError, ConnectionError, ImportError, ValueError,
            RuntimeError, TypeError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
