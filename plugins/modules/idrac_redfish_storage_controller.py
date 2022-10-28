#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 6.3.0
# Copyright (C) 2019-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: idrac_redfish_storage_controller
short_description: Configures the physical disk, virtual disk, and storage controller settings
version_added: "2.1.0"
description:
  - This module allows the users to configure the settings of the physical disk, virtual disk,
    and storage controller.
extends_documentation_fragment:
  - dellemc.openmanage.redfish_auth_options
options:
  command:
    description:
      - These actions may require a system reset, depending on the capabilities of the controller.
      - C(ResetConfig) - Deletes all the virtual disks and unassigns all hot spares on physical disks.
        I(controller_id) is required for this operation.
      - C(AssignSpare) - Assigns a physical disk as a dedicated or global hot spare for a virtual disk.
        I(target) is required for this operation.
      - C(SetControllerKey) - Sets the key on controllers, which is used to encrypt the drives in Local
        Key Management(LKM). I(controller_id), I(key), and I(key_id) are required for this operation.
      - C(RemoveControllerKey) - Deletes the encryption key on the controller.
        I(controller_id) is required for this operation.
      - C(ReKey) - Resets the key on the controller and it always reports as changes found when check mode is enabled.
        I(controller_id), I(old_key), I(key_id), and I(key) is required for this operation.
      - C(UnassignSpare) - To unassign the Global or Dedicated hot spare. I(target) is required for this operation.
      - C(EnableControllerEncryption) - To enable Local Key Management (LKM) or Secure Enterprise Key Manager (SEKM)
        on controllers that support encryption of the drives. I(controller_id), I(key), and I(key_id) are required
        for this operation.
      - C(BlinkTarget) - Blinks the target virtual drive or physical disk and it always reports as changes found
        when check mode is enabled. I(target) or I(volume_id) is required for this operation.
      - C(UnBlinkTarget) - Unblink the target virtual drive or physical disk and and it always reports as changes
        found when check mode is enabled. I(target) or I(volume_id) is required for this operation.
      - C(ConvertToRAID) - Converts the disk form non-Raid to Raid. I(target) is required for this operation.
      - C(ConvertToNonRAID) - Converts the disk form Raid to non-Raid. I(target) is required for this operation.
      - C(ChangePDStateToOnline) - To set the disk status to online. I(target) is required for this operation.
      - C(ChangePDStateToOffline) - To set the disk status to offline. I(target) is required for this operation.
      - C(LockVirtualDisk) - To encrypt the virtual disk. I(volume_id) is required for this operation.
    choices: [ResetConfig, AssignSpare, SetControllerKey, RemoveControllerKey, ReKey, UnassignSpare,
      EnableControllerEncryption, BlinkTarget, UnBlinkTarget, ConvertToRAID, ConvertToNonRAID,
      ChangePDStateToOnline, ChangePDStateToOffline, LockVirtualDisk]
    default: AssignSpare
    type: str
  target:
    description:
      - Fully Qualified Device Descriptor (FQDD) of the target physical drive.
      - This is mandatory when I(command) is C(AssignSpare), C(UnassisgnSpare),
        C(ChangePDStateToOnline), C(ChangePDStateToOffline), C(ConvertToRAID), or C(ConvertToNonRAID).
      - If I(volume_id) is not specified or empty, this physical drive will be
        assigned as a global hot spare when I(command) is C(AssignSpare).
      - "Notes: Global or Dedicated hot spare can be assigned only once for a physical disk,
        Re-assign cannot be done when I(command) is C(AssignSpare)."
    type: list
    elements: str
    aliases: [drive_id]
  volume_id:
    description:
      - Fully Qualified Device Descriptor (FQDD) of the volume.
      - Applicable if I(command) is C(AssignSpare), C(BlinkTarget), C(UnBlinkTarget) or C(LockVirtualDisk).
      - I(volume_id) or I(target) is required when the I(command) is C(BlinkTarget) or C(UnBlinkTarget),
        if both are specified I(target) is considered.
      - To know the number of volumes to which a hot spare can be assigned, refer iDRAC Redfish API documentation.
    type: list
    elements: str
  controller_id:
    description:
      - Fully Qualified Device Descriptor (FQDD) of the storage controller. For example-'RAID.Slot.1-1'.
      - This option is mandatory when I(command) is C(ResetConfig), C(SetControllerKey),
        C(RemoveControllerKey), C(ReKey), or C(EnableControllerEncryption).
    type: str
  key:
    description:
      - A new security key passphrase that the encryption-capable controller uses to create the
        encryption key. The controller uses the encryption key to lock or unlock access to the
        Self-Encrypting Drive (SED). Only one encryption key can be created for each controller.
      - This is mandatory when I(command) is C(SetControllerKey), C(ReKey), or C(EnableControllerEncryption)
        and when I(mode) is C(LKM).
      - The length of the key can be a maximum of 32 characters in length, where the expanded form of
        the special character is counted as a single character.
      - "The key must contain at least one character from each of the character classes: uppercase,
        lowercase, number, and special character."
    type: str
  key_id:
    description:
      - This is a user supplied text label associated with the passphrase.
      - This is mandatory when I(command) is C(SetControllerKey), C(ReKey), or C(EnableControllerEncryption)
        and when I(mode) is C(LKM).
      - The length of I(key_id) can be a maximum of 32 characters in length and should not have any spaces.
    type: str
  old_key:
    description:
      - Security key passphrase used by the encryption-capable controller.
      - This option is mandatory when I(command) is C(ReKey) and I(mode) is C(LKM).
    type: str
  mode:
    description:
      - Encryption mode of the encryption capable controller.
      - This option is applicable only when I(command) is C(ReKey) or C(EnableControllerEncryption).
      - C(SEKM) requires secure enterprise key manager license on the iDRAC.
      - C(LKM) to choose mode as local key mode.
    choices: [LKM, SEKM]
    default: LKM
    type: str
  job_wait:
    description:
      - Provides the option if the module has to wait for the job to be completed.
    type: bool
    default: False
  job_wait_timeout:
    description:
      - The maximum wait time of job completion in seconds before the job tracking is stopped.
      - This option is applicable when I(job_wait) is C(True).
    type: int
    default: 120
requirements:
  - "python >= 3.8.6"
author:
  - "Jagadeesh N V (@jagadeeshnv)"
  - "Felix Stephen (@felixs88)"
  - "Husniya Hameed (@husniya_hameed)"
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module always reports as changes found when C(ReKey), C(BlinkTarget), and C(UnBlinkTarget).
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Assign dedicated hot spare
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    volume_id:
      - "Disk.Virtual.0:RAID.Slot.1-1"
    target: "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1"
  tags:
    - assign_dedicated_hot_spare

- name: Assign global hot spare
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    target: "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1"
  tags:
    - assign_global_hot_spare

- name: Unassign hot spare
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    target: "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1"
    command: UnassignSpare
  tags:
    - un-assign-hot-spare

- name: Set controller encryption key
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "SetControllerKey"
    controller_id: "RAID.Slot.1-1"
    key: "PassPhrase@123"
    key_id: "mykeyid123"
  tags:
    - set_controller_key

- name: Rekey in LKM mode
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "ReKey"
    controller_id: "RAID.Slot.1-1"
    key: "NewPassPhrase@123"
    key_id: "newkeyid123"
    old_key: "OldPassPhrase@123"
  tags:
    - rekey_lkm

- name: Rekey in SEKM mode
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "ReKey"
    controller_id: "RAID.Slot.1-1"
    mode: "SEKM"
  tags:
    - rekey_sekm

- name: Remove controller key
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "RemoveControllerKey"
    controller_id: "RAID.Slot.1-1"
  tags:
    - remove_controller_key

- name: Reset controller configuration
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "ResetConfig"
    controller_id: "RAID.Slot.1-1"
  tags:
    - reset_config

- name: Enable controller encryption
  idrac_redfish_storage_controller:
    baseuri: "{{ baseuri }}"
    username: "{{ username }}"
    password: "{{ password }}"
    ca_path: "/path/to/ca_cert.pem"
    command: "EnableControllerEncryption"
    controller_id: "RAID.Slot.1-1"
    mode: "LKM"
    key: "your_Key@123"
    key_id: "your_Keyid@123"
  tags:
    - enable-encrypt

- name: Blink physical disk.
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: BlinkTarget
    target: "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1"
  tags:
    - blink-target

- name: Blink virtual drive.
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: BlinkTarget
    volume_id: "Disk.Virtual.0:RAID.Slot.1-1"
  tags:
    - blink-volume

- name: Unblink physical disk.
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: UnBlinkTarget
    target: "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1"
  tags:
    - unblink-target

- name: Unblink virtual drive.
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: UnBlinkTarget
    volume_id: "Disk.Virtual.0:RAID.Slot.1-1"
  tags:
    - unblink-drive

- name: Convert physical disk to RAID
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "ConvertToRAID"
    target: "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1"
  tags:
    - convert-raid

- name: Convert physical disk to non-RAID
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "ConvertToNonRAID"
    target: "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1"
  tags:
    - convert-non-raid

- name: Change physical disk state to online.
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "ChangePDStateToOnline"
    target: "Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1"
  tags:
    - pd-state-online

- name: Change physical disk state to offline.
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "ChangePDStateToOnline"
    target: "Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1"
  tags:
    - pd-state-offline

- name: Lock virtual drive
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "LockVirtualDisk"
    volume_id: "Disk.Virtual.0:RAID.SL.3-1"
  tags:
    - lock
'''

RETURN = r'''
---
msg:
  type: str
  description: Overall status of the storage controller configuration operation.
  returned: always
  sample: "Successfully submitted the job that performs the AssignSpare operation"
task:
  type: dict
  description: ID and URI resource of the job created.
  returned: success
  sample: {
    "id": "JID_XXXXXXXXXXXXX",
    "uri": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_XXXXXXXXXXXXX"
  }
status:
  type: dict
  description: status of the submitted job.
  returned: always
  sample: {
    "ActualRunningStartTime": "2022-02-09T04:42:41",
    "ActualRunningStopTime": "2022-02-09T04:44:00",
    "CompletionTime": "2022-02-09T04:44:00",
    "Description": "Job Instance",
    "EndTime": "TIME_NA",
    "Id": "JID_444033604418",
    "JobState": "Completed",
    "JobType": "RealTimeNoRebootConfiguration",
    "Message": "Job completed successfully.",
    "MessageArgs":[],
    "MessageId": "PR19",
    "Name": "Configure: RAID.Integrated.1-1",
    "PercentComplete": 100,
    "StartTime": "2022-02-09T04:42:40",
    "TargetSettingsURI": null
  }
error_info:
  type: dict
  description: Details of a http error.
  returned: on http error
  sample:  {
    "error": {
      "@Message.ExtendedInfo": [
        {
          "Message": "Unable to run the method because the requested HTTP method is not allowed.",
          "MessageArgs": [],
          "MessageArgs@odata.count": 0,
          "MessageId": "iDRAC.1.6.SYS402",
          "RelatedProperties": [],
          "RelatedProperties@odata.count": 0,
          "Resolution": "Enter a valid HTTP method and retry the operation. For information about
          valid methods, see the Redfish Users Guide available on the support site.",
          "Severity": "Informational"
        }
      ],
      "code": "Base.1.0.GeneralError",
      "message": "A general error has occurred. See ExtendedInfo for more information"
    }
  }
'''


import json
from ansible_collections.dellemc.openmanage.plugins.module_utils.redfish import Redfish, redfish_auth_params
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import wait_for_job_completion, strip_substr_dict
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


SYSTEM_ID = "System.Embedded.1"
MANAGER_ID = "iDRAC.Embedded.1"
RAID_ACTION_URI = "/redfish/v1/Systems/{system_id}/Oem/Dell/DellRaidService/Actions/DellRaidService.{action}"
CONTROLLER_URI = "/redfish/v1/Dell/Systems/{system_id}/Storage/DellController/{controller_id}"
VOLUME_URI = "/redfish/v1/Systems/{system_id}/Storage/{controller_id}/Volumes"
PD_URI = "/redfish/v1/Systems/System.Embedded.1/Storage/{controller_id}/Drives/{drive_id}"
JOB_URI_OEM = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/{job_id}"

JOB_SUBMISSION = "Successfully submitted the job that performs the '{0}' operation."
JOB_COMPLETION = "Successfully performed the '{0}' operation."
CHANGES_FOUND = "Changes found to be applied."
NO_CHANGES_FOUND = "No changes found to be applied."
TARGET_ERR_MSG = "The Fully Qualified Device Descriptor (FQDD) of the target {0} must be only one."
PD_ERROR_MSG = "Unable to locate the physical disk with the ID: {0}"
ENCRYPT_ERR_MSG = "The storage controller '{0}' does not support encryption."
PHYSICAL_DISK_ERR = "Volume is not encryption capable."


def check_id_exists(module, redfish_obj, key, item_id, uri):
    msg = "{0} with id '{1}' not found in system".format(key, item_id)
    try:
        resp = redfish_obj.invoke_request("GET", uri.format(system_id=SYSTEM_ID, controller_id=item_id))
        if not resp.success:
            module.fail_json(msg=msg)
    except HTTPError as err:
        module.fail_json(msg=msg, error_info=json.load(err))


def ctrl_key(module, redfish_obj):
    resp, job_uri, job_id, payload = None, None, None, {}
    controller_id = module.params.get("controller_id")
    command, mode = module.params["command"], module.params["mode"]
    key, key_id = module.params.get("key"), module.params.get("key_id")
    check_id_exists(module, redfish_obj, "controller_id", controller_id, CONTROLLER_URI)
    ctrl_resp = redfish_obj.invoke_request("GET", CONTROLLER_URI.format(system_id=SYSTEM_ID,
                                                                        controller_id=controller_id))
    security_status = ctrl_resp.json_data.get("SecurityStatus")
    if security_status == "EncryptionNotCapable":
        module.fail_json(msg=ENCRYPT_ERR_MSG.format(controller_id))
    ctrl_key_id = ctrl_resp.json_data.get("KeyID")
    if command == "SetControllerKey":
        if module.check_mode and ctrl_key_id is None:
            module.exit_json(msg=CHANGES_FOUND, changed=True)
        elif (module.check_mode and ctrl_key_id is not None) or (not module.check_mode and ctrl_key_id is not None):
            module.exit_json(msg=NO_CHANGES_FOUND)
        payload = {"TargetFQDD": controller_id, "Key": key, "Keyid": key_id}
    elif command == "ReKey":
        if module.check_mode:
            module.exit_json(msg=CHANGES_FOUND, changed=True)
        if mode == "LKM":
            payload = {"TargetFQDD": controller_id, "Mode": mode, "NewKey": key,
                       "Keyid": key_id, "OldKey": module.params.get("old_key")}
        else:
            payload = {"TargetFQDD": controller_id, "Mode": mode}
    elif command == "RemoveControllerKey":
        if module.check_mode and ctrl_key_id is not None:
            module.exit_json(msg=CHANGES_FOUND, changed=True)
        elif (module.check_mode and ctrl_key_id is None) or (not module.check_mode and ctrl_key_id is None):
            module.exit_json(msg=NO_CHANGES_FOUND)
        payload = {"TargetFQDD": controller_id}
    elif command == "EnableControllerEncryption":
        if module.check_mode and not security_status == "SecurityKeyAssigned":
            module.exit_json(msg=CHANGES_FOUND, changed=True)
        elif (module.check_mode and security_status == "SecurityKeyAssigned") or \
                (not module.check_mode and security_status == "SecurityKeyAssigned"):
            module.exit_json(msg=NO_CHANGES_FOUND)
        payload = {"TargetFQDD": controller_id, "Mode": mode}
        if mode == "LKM":
            payload["Key"] = key
            payload["Keyid"] = key_id
    resp = redfish_obj.invoke_request("POST", RAID_ACTION_URI.format(system_id=SYSTEM_ID, action=command),
                                      data=payload)
    job_uri = resp.headers.get("Location")
    job_id = job_uri.split("/")[-1]
    return resp, job_uri, job_id


def ctrl_reset_config(module, redfish_obj):
    resp, job_uri, job_id = None, None, None
    controller_id = module.params.get("controller_id")
    check_id_exists(module, redfish_obj, "controller_id", controller_id, CONTROLLER_URI)
    member_resp = redfish_obj.invoke_request("GET", VOLUME_URI.format(system_id=SYSTEM_ID, controller_id=controller_id))
    members = member_resp.json_data.get("Members")
    if module.check_mode and members:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    elif (module.check_mode and not members) or (not module.check_mode and not members):
        module.exit_json(msg=NO_CHANGES_FOUND)
    else:
        resp = redfish_obj.invoke_request("POST", RAID_ACTION_URI.format(system_id=SYSTEM_ID,
                                                                         action=module.params["command"]),
                                          data={"TargetFQDD": controller_id})
        job_uri = resp.headers.get("Location")
        job_id = job_uri.split("/")[-1]
    return resp, job_uri, job_id


def hot_spare_config(module, redfish_obj):
    target, command = module.params.get("target"), module.params["command"]
    resp, job_uri, job_id = None, None, None
    volume = module.params.get("volume_id")
    controller_id = target[0].split(":")[-1]
    drive_id = target[0]
    try:
        pd_resp = redfish_obj.invoke_request("GET", PD_URI.format(controller_id=controller_id, drive_id=drive_id))
    except HTTPError:
        module.fail_json(msg=PD_ERROR_MSG.format(drive_id))
    else:
        hot_spare = pd_resp.json_data.get("HotspareType")
        if module.check_mode and hot_spare == "None" and command == "AssignSpare" or \
                (module.check_mode and not hot_spare == "None" and command == "UnassignSpare"):
            module.exit_json(msg=CHANGES_FOUND, changed=True)
        elif (module.check_mode and hot_spare in ["Dedicated", "Global"] and command == "AssignSpare") or \
                (not module.check_mode and hot_spare in ["Dedicated", "Global"] and command == "AssignSpare") or \
                (module.check_mode and hot_spare == "None" and command == "UnassignSpare") or \
                (not module.check_mode and hot_spare == "None" and command == "UnassignSpare"):
            module.exit_json(msg=NO_CHANGES_FOUND)
        else:
            payload = {"TargetFQDD": drive_id}
            if volume is not None and command == "AssignSpare":
                payload["VirtualDiskArray"] = volume
            resp = redfish_obj.invoke_request("POST", RAID_ACTION_URI.format(system_id=SYSTEM_ID,
                                                                             action=command),
                                              data=payload)
            job_uri = resp.headers.get("Location")
            job_id = job_uri.split("/")[-1]
    return resp, job_uri, job_id


def change_pd_status(module, redfish_obj):
    resp, job_uri, job_id = None, None, None
    command, target = module.params["command"], module.params.get("target")
    controller_id = target[0].split(":")[-1]
    drive_id = target[0]
    state = "Online" if command == "ChangePDStateToOnline" else "Offline"
    try:
        pd_resp = redfish_obj.invoke_request("GET", PD_URI.format(controller_id=controller_id, drive_id=drive_id))
        raid_status = pd_resp.json_data["Oem"]["Dell"]["DellPhysicalDisk"]["RaidStatus"]
    except HTTPError:
        module.fail_json(msg=PD_ERROR_MSG.format(drive_id))
    else:
        if module.check_mode and not state == raid_status:
            module.exit_json(msg=CHANGES_FOUND, changed=True)
        elif (module.check_mode and state == raid_status) or (not module.check_mode and state == raid_status):
            module.exit_json(msg=NO_CHANGES_FOUND)
        else:
            resp = redfish_obj.invoke_request("POST", RAID_ACTION_URI.format(system_id=SYSTEM_ID,
                                                                             action="ChangePDState"),
                                              data={"TargetFQDD": drive_id, "State": state})
            job_uri = resp.headers.get("Location")
            job_id = job_uri.split("/")[-1]
    return resp, job_uri, job_id


def convert_raid_status(module, redfish_obj):
    resp, job_uri, job_id = None, None, None
    command, target = module.params["command"], module.params.get("target")
    ctrl, pd_ready_state = None, []
    try:
        for ctrl in target:
            controller_id = ctrl.split(":")[-1]
            pd_resp = redfish_obj.invoke_request("GET", PD_URI.format(controller_id=controller_id, drive_id=ctrl))
            raid_status = pd_resp.json_data["Oem"]["Dell"]["DellPhysicalDisk"]["RaidStatus"]
            pd_ready_state.append(raid_status)
    except HTTPError:
        module.fail_json(msg=PD_ERROR_MSG.format(ctrl))
    else:
        if (command == "ConvertToRAID" and module.check_mode and 0 < pd_ready_state.count("NonRAID")) or \
                (command == "ConvertToNonRAID" and module.check_mode and 0 < pd_ready_state.count("Ready")):
            module.exit_json(msg=CHANGES_FOUND, changed=True)
        elif (command == "ConvertToRAID" and module.check_mode and
              len(pd_ready_state) == pd_ready_state.count("Ready")) or \
                (command == "ConvertToRAID" and not module.check_mode and
                 len(pd_ready_state) == pd_ready_state.count("Ready")) or \
                (command == "ConvertToNonRAID" and module.check_mode and
                 len(pd_ready_state) == pd_ready_state.count("NonRAID")) or \
                (command == "ConvertToNonRAID" and not module.check_mode and
                 len(pd_ready_state) == pd_ready_state.count("NonRAID")):
            module.exit_json(msg=NO_CHANGES_FOUND)
        else:
            resp = redfish_obj.invoke_request("POST", RAID_ACTION_URI.format(system_id=SYSTEM_ID,
                                                                             action=command),
                                              data={"PDArray": target})
            job_uri = resp.headers.get("Location")
            job_id = job_uri.split("/")[-1]
    return resp, job_uri, job_id


def target_identify_pattern(module, redfish_obj):
    target, volume = module.params.get("target"), module.params.get("volume_id")
    command = module.params.get("command")
    payload = {"TargetFQDD": None}

    if target is not None and volume is None:
        payload = {"TargetFQDD": target[0]}
    elif volume is not None and target is None:
        payload = {"TargetFQDD": volume[0]}
    elif target is not None and volume is not None:
        payload = {"TargetFQDD": target[0]}

    if module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    resp = redfish_obj.invoke_request("POST", RAID_ACTION_URI.format(system_id=SYSTEM_ID,
                                                                     action=command),
                                      data=payload)
    return resp


def lock_virtual_disk(module, redfish_obj):
    volume, command = module.params.get("volume_id"), module.params["command"]
    resp, job_uri, job_id = None, None, None
    controller_id = volume[0].split(":")[-1]
    check_id_exists(module, redfish_obj, "controller_id", controller_id, CONTROLLER_URI)
    volume_uri = VOLUME_URI + "/{volume_id}"
    try:
        volume_resp = redfish_obj.invoke_request("GET", volume_uri.format(system_id=SYSTEM_ID,
                                                                          controller_id=controller_id,
                                                                          volume_id=volume[0]))
        links = volume_resp.json_data.get("Links")
        if links:
            for disk in volume_resp.json_data.get("Links").get("Drives"):
                drive_link = disk["@odata.id"]
                drive_resp = redfish_obj.invoke_request("GET", drive_link)
                encryption_ability = drive_resp.json_data.get("EncryptionAbility")
                if encryption_ability != "SelfEncryptingDrive":
                    module.fail_json(msg=PHYSICAL_DISK_ERR)
        lock_status = volume_resp.json_data.get("Oem").get("Dell").get("DellVolume").get("LockStatus")
    except HTTPError:
        module.fail_json(msg=PD_ERROR_MSG.format(controller_id))
    else:
        if lock_status == "Unlocked" and module.check_mode:
            module.exit_json(msg=CHANGES_FOUND, changed=True)
        elif lock_status == "Locked":
            module.exit_json(msg=NO_CHANGES_FOUND)
        else:
            resp = redfish_obj.invoke_request("POST", RAID_ACTION_URI.format(system_id=SYSTEM_ID,
                                                                             action="LockVirtualDisk"),
                                              data={"TargetFQDD": volume[0]})
            job_uri = resp.headers.get("Location")
            job_id = job_uri.split("/")[-1]
    return resp, job_uri, job_id


def validate_inputs(module):
    module_params = module.params
    command = module_params.get("command")
    mode = module_params.get("mode")
    if command == "ReKey" and mode == "LKM":
        key = module_params.get("key")
        key_id = module_params.get("key_id")
        old_key = module_params.get("old_key")
        if not all([key, key_id, old_key]):
            module.fail_json(msg="All of the following: key, key_id and old_key are "
                                 "required for '{0}' operation.".format(command))
    elif command == "EnableControllerEncryption" and mode == "LKM":
        key = module_params.get("key")
        key_id = module_params.get("key_id")
        if not all([key, key_id]):
            module.fail_json(msg="All of the following: key, key_id are "
                                 "required for '{0}' operation.".format(command))
    elif command in ["AssignSpare", "UnassignSpare", "BlinkTarget", "UnBlinkTarget", "LockVirtualDisk"]:
        target, volume = module_params.get("target"), module_params.get("volume_id")
        if target is not None and not 1 >= len(target):
            module.fail_json(msg=TARGET_ERR_MSG.format("physical disk"))
        if volume is not None and not 1 >= len(volume):
            module.fail_json(msg=TARGET_ERR_MSG.format("virtual drive"))
    elif command in ["ChangePDStateToOnline", "ChangePDStateToOffline"]:
        target = module.params.get("target")
        if target is not None and not 1 >= len(target):
            module.fail_json(msg=TARGET_ERR_MSG.format("physical disk"))


def main():
    specs = {
        "command": {"required": False, "default": "AssignSpare",
                    "choices": ["ResetConfig", "AssignSpare", "SetControllerKey", "RemoveControllerKey",
                                "ReKey", "UnassignSpare", "EnableControllerEncryption", "BlinkTarget",
                                "UnBlinkTarget", "ConvertToRAID", "ConvertToNonRAID", "ChangePDStateToOnline",
                                "ChangePDStateToOffline", "LockVirtualDisk"]},
        "controller_id": {"required": False, "type": "str"},
        "volume_id": {"required": False, "type": "list", "elements": "str"},
        "target": {"required": False, "type": "list", "elements": "str", "aliases": ["drive_id"]},
        "key": {"required": False, "type": "str", "no_log": True},
        "key_id": {"required": False, "type": "str"},
        "old_key": {"required": False, "type": "str", "no_log": True},
        "mode": {"required": False, "choices": ["LKM", "SEKM"], "default": "LKM"},
        "job_wait": {"required": False, "type": "bool", "default": False},
        "job_wait_timeout": {"required": False, "type": "int", "default": 120}
    }
    specs.update(redfish_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        required_if=[
            ["command", "SetControllerKey", ["controller_id", "key", "key_id"]],
            ["command", "ReKey", ["controller_id", "mode"]], ["command", "ResetConfig", ["controller_id"]],
            ["command", "RemoveControllerKey", ["controller_id"]], ["command", "AssignSpare", ["target"]],
            ["command", "UnassignSpare", ["target"]], ["command", "EnableControllerEncryption", ["controller_id"]],
            ["command", "BlinkTarget", ["target", "volume_id"], True],
            ["command", "UnBlinkTarget", ["target", "volume_id"], True], ["command", "ConvertToRAID", ["target"]],
            ["command", "ConvertToNonRAID", ["target"]], ["command", "ChangePDStateToOnline", ["target"]],
            ["command", "ChangePDStateToOffline", ["target"]],
            ["command", "LockVirtualDisk", ["volume_id"]]
        ],
        supports_check_mode=True)
    validate_inputs(module)
    try:
        command = module.params["command"]
        with Redfish(module.params, req_session=True) as redfish_obj:
            if command == "ResetConfig":
                resp, job_uri, job_id = ctrl_reset_config(module, redfish_obj)
            elif command == "SetControllerKey" or command == "ReKey" or \
                    command == "RemoveControllerKey" or command == "EnableControllerEncryption":
                resp, job_uri, job_id = ctrl_key(module, redfish_obj)
            elif command == "AssignSpare" or command == "UnassignSpare":
                resp, job_uri, job_id = hot_spare_config(module, redfish_obj)
            elif command == "BlinkTarget" or command == "UnBlinkTarget":
                resp = target_identify_pattern(module, redfish_obj)
                if resp.success and resp.status_code == 200:
                    module.exit_json(msg=JOB_COMPLETION.format(command), changed=True)
            elif command == "ConvertToRAID" or command == "ConvertToNonRAID":
                resp, job_uri, job_id = convert_raid_status(module, redfish_obj)
            elif command == "ChangePDStateToOnline" or command == "ChangePDStateToOffline":
                resp, job_uri, job_id = change_pd_status(module, redfish_obj)
            elif command == "LockVirtualDisk":
                resp, job_uri, job_id = lock_virtual_disk(module, redfish_obj)
            oem_job_url = JOB_URI_OEM.format(job_id=job_id)
            job_wait = module.params["job_wait"]
            if job_wait:
                resp, msg = wait_for_job_completion(redfish_obj, oem_job_url, job_wait=job_wait,
                                                    wait_timeout=module.params["job_wait_timeout"])
                job_data = strip_substr_dict(resp.json_data)
                if job_data["JobState"] == "Failed":
                    changed, failed = False, True
                else:
                    changed, failed = True, False
                module.exit_json(msg=JOB_COMPLETION.format(command), task={"id": job_id, "uri": oem_job_url},
                                 status=job_data, changed=changed, failed=failed)
            else:
                resp, msg = wait_for_job_completion(redfish_obj, oem_job_url, job_wait=job_wait,
                                                    wait_timeout=module.params["job_wait_timeout"])
                job_data = strip_substr_dict(resp.json_data)
            module.exit_json(msg=JOB_SUBMISSION.format(command), task={"id": job_id, "uri": oem_job_url},
                             status=job_data)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError, AttributeError) as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
