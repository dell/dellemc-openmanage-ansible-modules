#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2019-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

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
      - C(NonRedundant) The volume is a non-redundant storage device.
      - C(Mirrored) The volume is a mirrored device.
      - C(StripedWithParity) The volume is a device which uses parity to retain redundant information.
      - C(SpannedMirrors) The volume is a spanned set of mirrored devices.
      - C(SpannedStripesWithParity) The volume is a spanned set of devices which uses parity to retain redundant
        information.
      - I(volume_type) is mutually exclusive with I(raid_type).
    type: str
    choices: [NonRedundant, Mirrored, StripedWithParity, SpannedMirrors, SpannedStripesWithParity]
  name:
    description:
      - Name of the volume to be created.
      - Only applicable when I(state) is C(present).
    type: str
    aliases: ['volume_name']
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
  raid_type:
    description:
      - C(RAID0) to create a RAID0 type volume.
      - C(RAID1) to create a RAID1 type volume.
      - C(RAID5) to create a RAID5 type volume.
      - C(RAID6) to create a RAID6 type volume.
      - C(RAID10) to create a RAID10 type volume.
      - C(RAID50) to create a RAID50 type volume.
      - C(RAID60) to create a RAID60 type volume.
      - I(raid_type) is mutually exclusive with I(volume_type).
    type: str
    choices: [RAID0, RAID1, RAID5, RAID6, RAID10, RAID50, RAID60]
    version_added: 8.3.0
  apply_time:
    description:
      - Apply time of the Volume configuration.
      - C(Immediate) allows you to apply the volume configuration on the host server immediately and apply the changes. This is applicable for I(job_wait).
      - C(OnReset) allows you to apply the changes on the next reboot of the host server.
      - I(apply_time) has a default value based on the different types of the controller.
        For example, BOSS-S1 and BOSS-N1 controllers have a default value of I(apply_time) as C(OnReset),
        and PERC controllers have a default value of I(apply_time) as C(Immediate).
    type: str
    choices: [Immediate, OnReset]
    version_added: 8.5.0
  reboot_server:
    description:
      - Reboot the server to apply the changes.
      - I(reboot_server) is applicable only when I(apply_timeout) is C(OnReset) or when the default value for the apply time of the controller is C(OnReset).
    type: bool
    default: false
    version_added: 8.5.0
  force_reboot:
    description:
      - Reboot the server forcefully to apply the changes when the normal reboot fails.
      - I(force_reboot) is applicable only when I(reboot_server) is C(true).
    type: bool
    default: false
    version_added: 8.5.0
  job_wait:
    description:
      - This parameter provides the option to wait for the job completion.
      - This is applicable when I(apply_time) is C(Immediate).
      - This is applicable when I(apply_time) is C(OnReset) and I(reboot_server) is C(true).
    type: bool
    default: false
    version_added: 8.5.0
  job_wait_timeout:
    description:
      - This parameter is the maximum wait time of I(job_wait) in seconds.
      - This option is applicable when I(job_wait) is C(true).
    type: int
    default: 1200
    version_added: 8.5.0


requirements:
  - "python >= 3.9.6"
author:
  - "Sajna Shetty(@Sajna-Shetty)"
  - "Kritika Bhateja(@Kritika-Bhateja-03)"
  - "Shivam Sharma(@ShivamSh3)"
notes:
    - Run this module from a system that has direct access to Redfish APIs.
    - This module supports C(check_mode).
    - This module always reports changes when I(name) and I(volume_id) are not specified.
      Either I(name) or I(volume_id) is required to support C(check_mode).
    - This module does not support the create operation of RAID6 and RAID60 storage volume on iDRAC8
    - This module supports IPv4 and IPv6 addresses.
'''

EXAMPLES = r'''
---
- name: Create a volume with supported options
  dellemc.openmanage.redfish_storage_volume:
    baseuri: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
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
    ca_path: "/path/to/ca_cert.pem"
    state: "present"
    controller_id: "RAID.Slot.1-1"
    volume_type: "NonRedundant"
    drives:
      - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1

- name: Create a RAID0 on PERC controller on reset
  dellemc.openmanage.redfish_storage_volume:
    baseuri: "192.168.0.1"
    username: "username"
    password: "password"
    state: "present"
    controller_id: "RAID.Slot.1-1"
    raid_type: "RAID0"
    drives:
      - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1
      - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-2
    apply_time: OnReset

- name: Create a RAID0 on BOSS controller with restart
  dellemc.openmanage.redfish_storage_volume:
    baseuri: "192.168.0.1"
    username: "username"
    password: "password"
    state: "present"
    controller_id: "RAID.Slot.1-1"
    raid_type: "RAID0"
    drives:
      - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1
      - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-2
    apply_time: OnReset
    reboot_server: true

- name: Create a RAID0 on BOSS controller with force restart
  dellemc.openmanage.redfish_storage_volume:
    baseuri: "192.168.0.1"
    username: "username"
    password: "password"
    state: "present"
    controller_id: "RAID.Slot.1-1"
    raid_type: "RAID0"
    drives:
      - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1
      - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-2
    reboot_server: true
    force_reboot: true

- name: Modify a volume's encryption type settings
  dellemc.openmanage.redfish_storage_volume:
    baseuri: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "present"
    volume_id: "Disk.Virtual.5:RAID.Slot.1-1"
    encryption_types: "ControllerAssisted"
    encrypted: true

- name: Delete an existing volume
  dellemc.openmanage.redfish_storage_volume:
    baseuri: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "absent"
    volume_id: "Disk.Virtual.5:RAID.Slot.1-1"

- name: Initialize an existing volume
  dellemc.openmanage.redfish_storage_volume:
    baseuri: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: "initialize"
    volume_id: "Disk.Virtual.6:RAID.Slot.1-1"
    initialize_type: "Slow"

- name: Create a RAID6 volume
  dellemc.openmanage.redfish_storage_volume:
    baseuri: "192.168.0.1"
    username: "username"
    password: "password"
    state: "present"
    controller_id: "RAID.Slot.1-1"
    raid_type: "RAID6"
    drives:
      - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1
      - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-2
      - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-3
      - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-4

- name: Create a RAID60 volume
  dellemc.openmanage.redfish_storage_volume:
    baseuri: "192.168.0.1"
    username: "username"
    password: "password"
    state: "present"
    controller_id: "RAID.Slot.1-1"
    raid_type: "RAID60"
    drives:
      - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1
      - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-2
      - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-3
      - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-4
      - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-5
      - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-6
      - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-7
      - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-8
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
    "uri": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_XXXXXXXXXXXXX"
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
import copy
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.redfish import Redfish, RedfishAnsibleModule
from ansible.module_utils.compat.version import LooseVersion
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import MANAGER_JOB_ID_URI, wait_for_redfish_reboot_job, \
    strip_substr_dict, wait_for_job_completion


VOLUME_INITIALIZE_URI = "{storage_base_uri}/Volumes/{volume_id}/Actions/Volume.Initialize"
DRIVES_URI = "{storage_base_uri}/Drives/{driver_id}"
CONTROLLER_URI = "{storage_base_uri}/{controller_id}"
SETTING_VOLUME_ID_URI = "{storage_base_uri}/Volumes/{volume_id}/Settings"
CONTROLLER_VOLUME_URI = "{storage_base_uri}/{controller_id}/Volumes"
VOLUME_ID_URI = "{storage_base_uri}/Volumes/{volume_id}"
APPLY_TIME_INFO_API = CONTROLLER_URI + "/Volumes"
REBOOT_API = "Actions/ComputerSystem.Reset"
storage_collection_map = {}
CHANGES_FOUND = "Changes found to be applied."
NO_CHANGES_FOUND = "No changes found to be applied."
RAID_TYPE_NOT_SUPPORTED_MSG = "RAID Type {raid_type} is not supported."
APPLY_TIME_NOT_SUPPORTED_MSG = "Apply time {apply_time} is not supported. The supported values \
are {supported_apply_time_values}. Enter the valid values and retry the operation."
JOB_COMPLETION = "The job is successfully completed."
JOB_SUBMISSION = "The job is successfully submitted."
JOB_FAILURE_PROGRESS_MSG = "Unable to complete the task initiated for creating the storage volume."
REBOOT_FAIL = "Failed to reboot the server."
CONTROLLER_NOT_EXIST_ERROR = "Specified Controller {controller_id} does not exist in the System."
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The parameter job_wait_timeout value cannot be negative or zero."
SYSTEM_ID = "System.Embedded.1"
GET_IDRAC_FIRMWARE_VER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1?$select=FirmwareVersion"
ODATA_ID = "@odata.id"
TARGET_OUT_OF_BAND = "Target out-of-band controller does not support storage feature using Redfish API."
volume_type_map = {"NonRedundant": "RAID0",
                   "Mirrored": "RAID1",
                   "StripedWithParity": "RAID5",
                   "SpannedMirrors": "RAID10",
                   "SpannedStripesWithParity": "RAID50"}


def fetch_storage_resource(module, session_obj):
    try:
        system_uri = "{0}{1}".format(session_obj.root_uri, "Systems")
        system_resp = session_obj.invoke_request("GET", system_uri)
        system_members = system_resp.json_data.get("Members")
        if system_members:
            system_id_res = system_members[0][ODATA_ID]
            _SYSTEM_ID = system_id_res.split('/')[-1]
            system_id_res_resp = session_obj.invoke_request("GET", system_id_res)
            system_id_res_data = system_id_res_resp.json_data.get("Storage")
            if system_id_res_data:
                storage_collection_map.update({"storage_base_uri": system_id_res_data[ODATA_ID]})
            else:
                module.fail_json(msg=TARGET_OUT_OF_BAND)
        else:
            module.fail_json(msg=TARGET_OUT_OF_BAND)
    except HTTPError as err:
        if err.code in [404, 405]:
            module.fail_json(msg=TARGET_OUT_OF_BAND,
                             error_info=json.load(err))
        raise err
    except (URLError, SSLValidationError, ConnectionError, TypeError, ValueError) as err:
        raise err


def volume_payload(module, greater_version):
    params = module.params
    drives = params.get("drives")
    capacity_bytes = params.get("capacity_bytes")
    physical_disks = []
    oem = params.get("oem")
    encrypted = params.get("encrypted")
    encryption_types = params.get("encryption_types")
    volume_type = params.get("volume_type")
    raid_type = params.get("raid_type")
    apply_time = params.get("apply_time")
    if capacity_bytes:
        capacity_bytes = int(capacity_bytes)
    if drives:
        storage_base_uri = storage_collection_map["storage_base_uri"]
        physical_disks = [{ODATA_ID: DRIVES_URI.format(storage_base_uri=storage_base_uri,
                           driver_id=drive_id)} for drive_id in drives]
    raid_mapper = {
        "Name": params.get("name"),
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
    if volume_type and greater_version:
        raid_payload.update({"RAIDType": volume_type_map.get(volume_type)})
    if raid_type and greater_version:
        raid_payload.update({"RAIDType": raid_type})
    if volume_type and greater_version is False:
        raid_payload.update({"VolumeType": volume_type})
    if raid_type and greater_version is False:
        raid_map = {value: key for key, value in volume_type_map.items()}
        raid_payload.update({"VolumeType": raid_map.get(raid_type)})
    if apply_time is not None:
        raid_payload.update({"@Redfish.OperationApplyTime": apply_time})
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
            if module.params.get("state") == "absent" and module.params.get("volume_id"):
                module.exit_json(msg=NO_CHANGES_FOUND)
            module.exit_json(msg=err_message, failed=True)
        raise err
    except (URLError, SSLValidationError, ConnectionError, TypeError, ValueError) as err:
        raise err


def check_controller_id_exists(module, session_obj):
    """
    Controller availability Validation
    """
    specified_controller_id = module.params.get("controller_id")
    uri = CONTROLLER_URI.format(storage_base_uri=storage_collection_map["storage_base_uri"], controller_id=specified_controller_id)
    err_message = CONTROLLER_NOT_EXIST_ERROR.format(controller_id=specified_controller_id)
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
        if not task_uri:
            msg = resp.json_data["@Message.ExtendedInfo"][1]["Message"]
            status_message = {"msg": msg}
            return status_message
        return get_success_message(action, task_uri)
    except (HTTPError, URLError, SSLValidationError, ConnectionError,
            TypeError, ValueError) as err:
        raise err


def check_mode_validation(module, session_obj, action, uri, greater_version):
    volume_id = module.params.get('volume_id')
    name = module.params.get("name")
    block_size_bytes = module.params.get("block_size_bytes")
    capacity_bytes = module.params.get("capacity_bytes")
    optimum_io_size_bytes = module.params.get("optimum_io_size_bytes")
    encryption_types = module.params.get("encryption_types")
    encrypted = module.params.get("encrypted")
    volume_type = module.params.get("volume_type")
    raid_type = module.params.get("raid_type")
    drives = module.params.get("drives")
    if name is None and volume_id is None and module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    if action == "create" and name is not None:
        volume_id = _create_name(module, session_obj, uri, name, volume_id)
    if volume_id is not None:
        _volume_id_check_mode(module, session_obj, greater_version, volume_id,
                              name, block_size_bytes, capacity_bytes, optimum_io_size_bytes,
                              encryption_types, encrypted, volume_type, raid_type, drives)
    return None


def _volume_id_check_mode(module, session_obj, greater_version, volume_id, name,
                          block_size_bytes, capacity_bytes, optimum_io_size_bytes,
                          encryption_types, encrypted, volume_type, raid_type, drives):
    resp = session_obj.invoke_request("GET", SETTING_VOLUME_ID_URI.format(
        storage_base_uri=storage_collection_map["storage_base_uri"],
        volume_id=volume_id))
    resp_data = resp.json_data
    exist_value = _get_payload_for_version(greater_version, resp_data)
    exit_value_filter = dict(
        [(k, v) for k, v in exist_value.items() if v is not None])
    cp_exist_value = copy.deepcopy(exit_value_filter)
    req_value = get_request_value(greater_version, name, block_size_bytes, optimum_io_size_bytes, encryption_types, encrypted, volume_type, raid_type)
    if capacity_bytes is not None:
        req_value["CapacityBytes"] = int(capacity_bytes)
    req_value_filter = dict([(k, v)
                            for k, v in req_value.items() if v is not None])
    cp_exist_value.update(req_value_filter)
    exist_drive, req_drive = [], []
    if resp_data["Links"]:
        exist_drive = [
            disk[ODATA_ID].split("/")[-1] for disk in resp_data["Links"]["Drives"]]
    if drives is not None:
        req_drive = sorted(drives)
    diff_changes = [bool(set(exit_value_filter.items()) ^ set(cp_exist_value.items())) or
                    bool(set(exist_drive) ^ set(req_drive))]
    if module.check_mode and any(diff_changes) is True:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    elif (module.check_mode and any(diff_changes) is False) or \
            (not module.check_mode and any(diff_changes) is False):
        module.exit_json(msg=NO_CHANGES_FOUND)


def get_request_value(greater_version, name, block_size_bytes, optimum_io_size_bytes, encryption_types, encrypted, volume_type, raid_type):
    if greater_version:
        req_value = {"Name": name, "BlockSizeBytes": block_size_bytes,
                     "Encrypted": encrypted, "OptimumIOSizeBytes": optimum_io_size_bytes,
                     "RAIDType": raid_type, "EncryptionTypes": encryption_types}
    else:
        req_value = {"Name": name, "BlockSizeBytes": block_size_bytes,
                     "Encrypted": encrypted, "OptimumIOSizeBytes": optimum_io_size_bytes,
                     "VolumeType": volume_type, "EncryptionTypes": encryption_types}
    return req_value


def _get_payload_for_version(greater_version, resp_data):
    if greater_version:
        exist_value = {"Name": resp_data["Name"], "BlockSizeBytes": resp_data["BlockSizeBytes"],
                       "CapacityBytes": resp_data["CapacityBytes"], "Encrypted": resp_data["Encrypted"],
                       "EncryptionTypes": resp_data["EncryptionTypes"][0],
                       "OptimumIOSizeBytes": resp_data["OptimumIOSizeBytes"], "RAIDType": resp_data["RAIDType"]}
    else:
        exist_value = {"Name": resp_data["Name"], "BlockSizeBytes": resp_data["BlockSizeBytes"],
                       "CapacityBytes": resp_data["CapacityBytes"], "Encrypted": resp_data["Encrypted"],
                       "EncryptionTypes": resp_data["EncryptionTypes"][0],
                       "OptimumIOSizeBytes": resp_data["OptimumIOSizeBytes"], "VolumeType": resp_data["VolumeType"]}
    return exist_value


def _create_name(module, session_obj, uri, name, volume_id):
    volume_resp = session_obj.invoke_request("GET", uri)
    volume_resp_data = volume_resp.json_data
    if volume_resp_data.get("Members@odata.count") == 0 and module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    elif 0 < volume_resp_data.get("Members@odata.count"):
        for mem in volume_resp_data.get("Members"):
            mem_resp = session_obj.invoke_request("GET", mem[ODATA_ID])
            if mem_resp.json_data["Name"] == name:
                volume_id = mem_resp.json_data["Id"]
                break
    if name is not None and module.check_mode and volume_id is None:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    return volume_id


def check_raid_type_supported(module, session_obj):
    volume_type = module.params.get("volume_type")
    if volume_type:
        raid_type = volume_type_map.get(volume_type)
    else:
        raid_type = module.params.get("raid_type")
    if raid_type:
        try:
            specified_controller_id = module.params.get("controller_id")
            uri = CONTROLLER_URI.format(storage_base_uri=storage_collection_map["storage_base_uri"], controller_id=specified_controller_id)
            resp = session_obj.invoke_request("GET", uri)
            supported_raid_types = resp.json_data['StorageControllers'][0]['SupportedRAIDTypes']
            if raid_type not in supported_raid_types:
                module.exit_json(msg=RAID_TYPE_NOT_SUPPORTED_MSG.format(raid_type=raid_type), failed=True)
        except (HTTPError, URLError, SSLValidationError, ConnectionError, TypeError, ValueError) as err:
            raise err


def get_apply_time(module, session_obj, controller_id, greater_version):
    """
    gets the apply time from user if given otherwise fetches from server
    """
    apply_time = module.params.get("apply_time")
    try:
        uri = APPLY_TIME_INFO_API.format(storage_base_uri=storage_collection_map["storage_base_uri"], controller_id=controller_id)
        resp = session_obj.invoke_request("GET", uri)
        if greater_version:
            supported_apply_time_values = resp.json_data['@Redfish.OperationApplyTimeSupport']['SupportedValues']
        else:
            return apply_time
        if apply_time:
            if apply_time not in supported_apply_time_values:
                module.exit_json(msg=APPLY_TIME_NOT_SUPPORTED_MSG.format(apply_time=apply_time, supported_apply_time_values=supported_apply_time_values),
                                 failed=True)
        else:
            apply_time = supported_apply_time_values[0]
        return apply_time
    except (HTTPError, URLError, SSLValidationError, ConnectionError, TypeError, ValueError) as err:
        raise err


def check_apply_time_supported_and_reboot_required(module, session_obj, controller_id, greater_version):
    """
    checks whether the apply time is supported and reboot operation is required or not.
    """
    apply_time = get_apply_time(module, session_obj, controller_id, greater_version)
    reboot_server = module.params.get("reboot_server")
    if reboot_server and apply_time == "OnReset":
        return True
    return False


def perform_volume_create_modify(module, session_obj, greater_version):
    """
    perform volume creation and modification for state present
    """
    specified_controller_id = module.params.get("controller_id")
    volume_id = module.params.get("volume_id")
    if greater_version:
        check_raid_type_supported(module, session_obj)
    action, uri, method = None, None, None
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
    payload = volume_payload(module, greater_version)
    check_mode_validation(module, session_obj, action, uri, greater_version)
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
        if hasattr(resp, "success") and resp.success and not module.check_mode:
            uri = VOLUME_ID_URI.format(storage_base_uri=storage_collection_map["storage_base_uri"], volume_id=volume_id)
            method = "DELETE"
            return perform_storage_volume_action(method, uri, session_obj, "delete")
        elif hasattr(resp, "success") and resp.success and module.check_mode:
            module.exit_json(msg=CHANGES_FOUND, changed=True)
        elif hasattr(resp, "code") and resp.code == 404 and module.check_mode:
            module.exit_json(msg=NO_CHANGES_FOUND)
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


def configure_raid_operation(module, session_obj, greater_version):
    """
    configure raid action based on state and command input
    """
    module_params = module.params
    state = module_params.get("state")
    command = module_params.get("command")
    if state is not None and state == "present":
        return perform_volume_create_modify(module, session_obj, greater_version)
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


def perform_force_reboot(module, session_obj):
    payload = {"ResetType": "ForceRestart"}
    job_resp_status, reset_status, reset_fail = wait_for_redfish_reboot_job(session_obj, SYSTEM_ID, payload=payload)
    if reset_status and job_resp_status:
        job_uri = MANAGER_JOB_ID_URI.format(job_resp_status["Id"])
        resp, msg = wait_for_job_completion(session_obj, job_uri, wait_timeout=module.params.get("job_wait_timeout"))
        if resp:
            job_data = strip_substr_dict(resp.json_data)
            if job_data["JobState"] == "Failed":
                module.exit_json(msg=REBOOT_FAIL, job_status=job_data, failed=True)
        else:
            resp = session_obj.invoke_request("GET", job_uri)
            job_data = strip_substr_dict(resp.json_data)
            module.exit_json(msg=msg, job_status=job_data)


def perform_reboot(module, session_obj):
    payload = {"ResetType": "GracefulRestart"}
    force_reboot = module.params.get("force_reboot")
    job_resp_status, reset_status, reset_fail = wait_for_redfish_reboot_job(session_obj, SYSTEM_ID, payload=payload)
    if reset_status and job_resp_status:
        job_uri = MANAGER_JOB_ID_URI.format(job_resp_status["Id"])
        resp, msg = wait_for_job_completion(session_obj, job_uri, wait_timeout=module.params.get("job_wait_timeout"))
        if resp:
            job_data = strip_substr_dict(resp.json_data)
            if force_reboot and job_data["JobState"] == "Failed":
                perform_force_reboot(module, session_obj)
        else:
            resp = session_obj.invoke_request("GET", job_uri)
            job_data = strip_substr_dict(resp.json_data)
            module.exit_json(msg=msg, job_status=job_data)


def check_job_tracking_required(module, session_obj, reboot_required, controller_id, greater_version):
    job_wait = module.params.get("job_wait")
    apply_time = None
    if controller_id:
        apply_time = get_apply_time(module, session_obj, controller_id, greater_version)
    if job_wait:
        if apply_time == "OnReset" and not reboot_required:
            return False
        return True
    return False


def track_job(module, session_obj, job_id, job_url):
    resp, msg = wait_for_job_completion(session_obj, job_url,
                                        wait_timeout=module.params.get("job_wait_timeout"))
    if resp:
        job_data = strip_substr_dict(resp.json_data)
        if job_data["JobState"] == "Failed":
            changed, failed = False, True
            module.exit_json(msg=JOB_FAILURE_PROGRESS_MSG, task={"id": job_id, "uri": job_url},
                             changed=changed, job_status=job_data, failed=failed)
        elif job_data["JobState"] == "Scheduled":
            task_status = {"uri": job_url, "id": job_id}
            module.exit_json(msg=JOB_SUBMISSION, task=task_status, job_status=job_data, changed=True)
        else:
            changed, failed = True, False
            module.exit_json(msg=JOB_COMPLETION, task={"id": job_id, "uri": job_url},
                             changed=changed, job_status=job_data, failed=failed)
    else:
        module.exit_json(msg=msg)


def validate_negative_job_time_out(module):
    if module.params.get("job_wait") and module.params.get("job_wait_timeout") <= 0:
        module.exit_json(msg=TIMEOUT_NEGATIVE_OR_ZERO_MSG, failed=True)


def is_fw_ver_greater(session_obj):
    firm_version = session_obj.invoke_request('GET', GET_IDRAC_FIRMWARE_VER_URI)
    version = firm_version.json_data.get('FirmwareVersion', '')
    if LooseVersion(version) <= '3.0':
        return False
    else:
        return True


def main():
    specs = {
        "state": {"type": "str", "required": False, "choices": ['present', 'absent']},
        "command": {"type": "str", "required": False, "choices": ['initialize']},
        "volume_type": {"type": "str", "required": False,
                        "choices": ['NonRedundant', 'Mirrored',
                                    'StripedWithParity', 'SpannedMirrors',
                                    'SpannedStripesWithParity']},
        "raid_type": {"type": "str", "required": False,
                      "choices": ['RAID0', 'RAID1', 'RAID5',
                                  'RAID6', 'RAID10', 'RAID50', 'RAID60']},
        "name": {"required": False, "type": "str", "aliases": ['volume_name']},
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
        "apply_time": {"required": False, "type": "str", "choices": ['Immediate', 'OnReset']},
        "reboot_server": {"required": False, "type": "bool", "default": False},
        "force_reboot": {"required": False, "type": "bool", "default": False},
        "job_wait": {"required": False, "type": "bool", "default": False},
        "job_wait_timeout": {"required": False, "type": "int", "default": 1200}
    }
    module = RedfishAnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[['state', 'command'], ['volume_type', 'raid_type']],
        required_one_of=[['state', 'command']],
        required_if=[['command', 'initialize', ['volume_id']],
                     ['state', 'absent', ['volume_id']], ],
        supports_check_mode=True)

    try:
        validate_inputs(module)
        validate_negative_job_time_out(module)
        with Redfish(module.params, req_session=True) as session_obj:
            greater_version = is_fw_ver_greater(session_obj)
            fetch_storage_resource(module, session_obj)
            controller_id = module.params.get("controller_id")
            volume_id = module.params.get("volume_id")
            reboot_server = module.params.get("reboot_server")
            reboot_required = module.params.get("reboot_required")
            if controller_id:
                uri = CONTROLLER_URI.format(storage_base_uri=storage_collection_map["storage_base_uri"], controller_id=controller_id)
                resp = check_specified_identifier_exists_in_the_system(module, session_obj, uri, CONTROLLER_NOT_EXIST_ERROR.format(controller_id=controller_id))
                reboot_required = check_apply_time_supported_and_reboot_required(module, session_obj, controller_id, greater_version)
            status_message = configure_raid_operation(module, session_obj, greater_version)
            if volume_id and reboot_server:
                controller_id = volume_id.split(":")[-1]
                uri = CONTROLLER_URI.format(storage_base_uri=storage_collection_map["storage_base_uri"], controller_id=controller_id)
                resp = check_specified_identifier_exists_in_the_system(module, session_obj, uri, CONTROLLER_NOT_EXIST_ERROR.format(controller_id=controller_id))
                reboot_required = check_apply_time_supported_and_reboot_required(module, session_obj, controller_id, greater_version)
            if reboot_required:
                perform_reboot(module, session_obj)
            if status_message.get("task_id"):
                job_tracking_required = check_job_tracking_required(module, session_obj, reboot_required, controller_id, greater_version)
                job_id = status_message.get("task_id")
                job_url = MANAGER_JOB_ID_URI.format(job_id)
                if job_tracking_required and job_id:
                    track_job(module, session_obj, job_id, job_url)
                else:
                    task_status = {"uri": job_url, "id": job_id}
                    resp = session_obj.invoke_request("GET", job_url)
                    job_data = strip_substr_dict(resp.json_data)
                    module.exit_json(msg=status_message["msg"], task=task_status, job_status=job_data, changed=True)
            else:
                module.exit_json(msg=status_message["msg"])
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, ImportError, ValueError,
            RuntimeError, TypeError, OSError, SSLError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
