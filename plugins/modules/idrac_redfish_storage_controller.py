#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.0
# Copyright (C) 2019-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

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
      - C(OnlineCapacityExpansion) - To expand the size of virtual disk. I(volume_id), and I(target) or I(size) is required for this operation.
      - C(SecureErase) - To delete all the data on the physical disk securely. This option is available for
        Self-Encrypting Drives (SED), Instant Scramble Erase (ISE) drives, and PCIe SSD devices (drives and cards).
        The drives must be in a ready state. I(controller_id) and I(target) are required for this operation,
        I(target) must be a single physical disk ID. If a secure erase needs a reboot,
        the job will get scheduled and waits for no of seconds specfied in I(job_wait_time),
        to reduce the wait time either give I(job_wait_time) minimum or make I(job_wait)
        as false.
      - C(EnableSecurity) - To enable security on a storage controller. Only Applicable for 17G and above.
      - C(DisableSecurity) - To disable security on a storage controller. Only Applicable for 17G and above.
      - C(SetControllerKey), C(RemoveControllerKey), C(ReKey) and C(EnableControllerEncryption) are only supported for 16G and below.
      - Blinking of virtual disk is not supported for 17G and above.
    choices: [ResetConfig, AssignSpare, SetControllerKey, RemoveControllerKey, ReKey, UnassignSpare,
      EnableControllerEncryption, BlinkTarget, UnBlinkTarget, ConvertToRAID, ConvertToNonRAID,
      ChangePDStateToOnline, ChangePDStateToOffline, LockVirtualDisk, OnlineCapacityExpansion, SecureErase,
      EnableSecurity, DisableSecurity]
    type: str
  target:
    description:
      - Fully Qualified Device Descriptor (FQDD) of the target physical drive.
      - This is mandatory when I(command) is C(AssignSpare), C(UnassisgnSpare),
        C(ChangePDStateToOnline), C(ChangePDStateToOffline), C(ConvertToRAID), or C(ConvertToNonRAID).
      - If I(volume_id) is not specified or empty, this physical drive will be
        assigned as a global hot spare when I(command) is C(AssignSpare).
      - When I(command) is C(OnlineCapacityExpansion), then I(target) is mutually exclusive with I(size).
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
      - This option is mandatory for I(attributes).
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
  size:
    description:
      - Capacity of the virtual disk to be expanded in MB.
      - Check mode and Idempotency is not supported for I(size).
      - Minimum Online Capacity Expansion size must be greater than 100 MB of the current size.
      - When I(command) is C(OnlineCapacityExpansion), then I(size) is mutually exclusive with I(target).
    type: int
  attributes:
    type: dict
    description:
      - Dictionary of controller attributes and value pair.
      - This feature is only supported for iDRAC9 with firmware version 6.00.00.00 and above
      - I(controller_id) is required for this operation.
      - I(apply_time) and I(maintenance_window) is applicable for I(attributes).
      - I(attributes) is mutually exclusive with I(command).
      - Use U(https://I(idrac_ip)/redfish/v1/Schemas/DellOemStorageController.json) to view the attributes.
      - C(BackgroundInitializationRatePercent) and C(ReconstructRatePercent) are supported parameters for iDRAC 10.
  apply_time:
    type: str
    description:
      - Apply time of the I(attributes).
      - This is applicable only to I(attributes).
      - "C(Immediate) Allows the user to immediately reboot the host and apply the changes. I(job_wait)
      is applicable."
      - C(OnReset) Allows the user to apply the changes on the next reboot of the host server.
      - "C(AtMaintenanceWindowStart) Allows the user to apply at the start of a maintenance window as specified
      in I(maintenance_window)."
      - "C(InMaintenanceWindowOnReset) Allows to apply after a manual reset but within the maintenance window as
      specified in I(maintenance_window)."
      - Only C(Immediate) and C(OnReset) are supported for 17G.
    choices: [Immediate, OnReset, AtMaintenanceWindowStart, InMaintenanceWindowOnReset]
    default: Immediate
  maintenance_window:
    type: dict
    description:
      - Option to schedule the maintenance window.
      - This is required when I(apply_time) is C(AtMaintenanceWindowStart) or C(InMaintenanceWindowOnReset).
    suboptions:
       start_time:
           type: str
           description:
              - The start time for the maintenance window to be scheduled.
              - "The format is YYYY-MM-DDThh:mm:ss<offset>"
              - "<offset> is the time offset from UTC that the current timezone set in
              iDRAC in the format: +05:30 for IST."
           required: true
       duration:
           type: int
           description:
              - The duration in seconds for the maintenance window.
           default: 900
  job_wait:
    description:
      - Provides the option if the module has to wait for the job to be completed.
      - This is applicable for I(attributes) when I(apply_time) is C(Immediate)
       and when I(command) is C(SecureErase).
    type: bool
    default: false
  job_wait_timeout:
    description:
      - The maximum wait time of job completion in seconds before the job tracking is stopped.
      - This option is applicable when I(job_wait) is C(true).
      - "Note: When I(command) is C(SecureErase), If a secure erase needs a reboot,
        the job will get scheduled and waits for no of seconds specfied in I(job_wait_time),
        to reduce the wait time either give I(job_wait_time) a lesser value or make I(job_wait)
        as false."
    type: int
    default: 120
requirements:
  - "python >= 3.9.6"
author:
  - "Jagadeesh N V (@jagadeeshnv)"
  - "Felix Stephen (@felixs88)"
  - "Husniya Hameed (@husniya_hameed)"
  - "Abhishek Sinha (@ABHISHEK-SINHA10)"
  - "Shivam Sharma (@ShivamSh3)"
  - "Trisha Datta (@trisha-dell)"
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module is supported on iDRAC9 and iDRAC 10.
    - This module supports IPv4 and IPv6 addresses.
    - This module always reports as changes found when I(command) is C(ReKey), C(BlinkTarget), and C(UnBlinkTarget).
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

- name: Online Capacity Expansion of a volume using target
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "{{ baseuri }}"
    username: "{{ username }}"
    password: "{{ password }}"
    ca_path: "/path/to/ca_cert.pem"
    command: "OnlineCapacityExpansion"
    volume_id: "Disk.Virtual.0:RAID.Integrated.1-1"
    target:
      - "Disk.Bay.2:Enclosure.Internal.0-0:RAID.Integrated.1-1"
  tags:
    - oce_target

- name: Online Capacity Expansion of a volume using size
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "{{ baseuri }}"
    username: "{{ username }}"
    password: "{{ password }}"
    ca_path: "/path/to/ca_cert.pem"
    command: "OnlineCapacityExpansion"
    volume_id: "Disk.Virtual.0:RAID.Integrated.1-1"
    size: 362785
  tags:
    - oce_size

- name: Set controller attributes.
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    controller_id: "RAID.Slot.1-1"
    attributes:
      ControllerMode: "HBA"
    apply_time: "OnReset"
  tags:
    - controller-attribute

- name: Configure controller attributes at Maintenance window
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    controller_id: "RAID.Slot.1-1"
    attributes:
      CheckConsistencyMode: Normal
      CopybackMode: "Off"
      LoadBalanceMode: Disabled
    apply_time: AtMaintenanceWindowStart
    maintenance_window:
      start_time: "2022-09-30T05:15:40-05:00"
      duration: 1200

- name: Perform Secure Erase operation on SED drive
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    controller_id: "RAID.Slot.1-1"
    command: "SecureErase"
    target: "Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1"
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
    "uri": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/JID_XXXXXXXXXXXXX"
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


import re
import json
from ansible.module_utils.compat.version import LooseVersion
from ansible_collections.dellemc.openmanage.plugins.module_utils.redfish import Redfish, RedfishAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import wait_for_job_completion, strip_substr_dict, \
    get_dynamic_uri, validate_and_get_first_resource_id_uri, get_idrac_firmware_version, get_scheduled_job_resp
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


SYSTEMS_URI = "/redfish/v1/Systems/"
SYSTEM_ID = "System.Embedded.1"
MANAGER_ID = "iDRAC.Embedded.1"
RAID_ACTION_URI = "/redfish/v1/Systems/{system_id}/Oem/Dell/DellRaidService/Actions/DellRaidService.{action}"
CONTROLLER_URI = "/redfish/v1/Systems/{system_id}/Storage/{controller_id}"
VOLUME_URI = "/redfish/v1/Systems/{system_id}/Storage/{controller_id}/Volumes"
PD_URI = "/redfish/v1/Systems/System.Embedded.1/Storage/{controller_id}/Drives/{drive_id}"
JOB_URI_OEM = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/{job_id}"
CONTROLLERS_URI = "/redfish/v1/Systems/{system_id}/Storage/{controller_id}/Controllers/{controller_id}"
MANAGER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"
SETTINGS_URI = "/redfish/v1/Systems/{system_id}/Storage/{controller_id}/Controllers/{controller_id}/Settings"
OCE_MIN_PD_RAID_MAPPING = {'RAID0': 1, 'RAID5': 1, 'RAID6': 1, 'RAID10': 2}
ODATA_ID = "@odata.id"

JOB_SUBMISSION = "Successfully submitted the job that performs the '{0}' operation."
JOB_COMPLETION = "Successfully performed the '{0}' operation."
JOB_EXISTS = "Unable to complete the operation because another job already " \
             "exists. Wait for the pending job to complete and retry the operation."
CHANGES_FOUND = "Changes found to be applied."
NO_CHANGES_FOUND = "No changes found to be applied."
TARGET_ERR_MSG = "The Fully Qualified Device Descriptor (FQDD) of the target {0} must be only one."
CNTRL_ERROR_MSG = "Unable to locate the storage controller with the ID: {0}"
PD_ERROR_MSG = "Unable to locate the physical disk with the ID: {0}"
VD_ERROR_MSG = "Unable to locate the virtual disk with the ID: {0}"
ENCRYPT_ERR_MSG = "The storage controller '{0}' does not support encryption."
PHYSICAL_DISK_ERR = "Volume is not encryption capable."
DRIVE_NOT_SECURE_ERASE = "Drive {0} does not support secure erase operation."
DRIVE_NOT_READY = "Drive {0} is not in ready state."
OCE_RAID_TYPE_ERR = "Online Capacity Expansion is not supported for {0} virtual disks."
OCE_SIZE_100MB = "Minimum Online Capacity Expansion size must be greater than 100 MB of the current size {0}."
OCE_TARGET_EMPTY = "Provided list of targets is empty."
OCE_TARGET_RAID1_ERR = "Cannot add more than two disks to RAID1 virtual disk."
UNSUPPORTED_APPLY_TIME = "Apply time {0} is not supported."
MAINTENANCE_OFFSET = "The maintenance time must be post-fixed with local offset to {0}."
MAINTENANCE_TIME = "The specified maintenance time window occurs in the past, " \
                   "provide a future time to schedule the maintenance window."
HBA_MODE = "Other attributes cannot be updated when ControllerMode is provided as input."
INVALID_ATTRIBUTES = "The following attributes are invalid: {0}"
CONTROLLER_ID_REQUIRED = "controller_id is required to perform this operation."
JOB_COMPLETION_ATTRIBUTES = "Successfully applied the controller attributes."
JOB_SUBMISSION_ATTRIBUTES = "Successfully submitted the job that configures the controller attributes."
ERR_MSG = "Unable to configure the controller attribute(s) settings."
INVALID_KEY_ID = "The keyid should be of maximum length 32 and only alphanumeric characters are allowed without spaces."
INVALID_KEY = ("The key should be of maximum length 32 and must contain at least one "
               "character from each of the character classes: uppercase, lowercase, "
               "number, and special character.")
INVALID_START_TIME = "The start time should be in the format YYYY-MM-DDThh:mm:ss<offset>"
INVALID_COMMAND = "The command {0} is not applicable for {1}"


def check_id_exists(module, redfish_obj, key, item_id, uri):
    msg = "{0} with id '{1}' not found in system".format(key, item_id)
    try:
        resp = redfish_obj.invoke_request("GET", uri.format(system_id=SYSTEM_ID, controller_id=item_id))
        if not resp.success:
            module.exit_json(msg=msg, failed=True)
    except HTTPError as err:
        module.exit_json(msg=msg, error_info=json.load(err), failed=True)


def handle_set_controller_key(module, controller_id, ctrl_key_id, key, key_id, payload):
    if module.check_mode and ctrl_key_id is None:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    elif module.check_mode or ctrl_key_id is not None:
        module.exit_json(msg=NO_CHANGES_FOUND)
    payload.update({"TargetFQDD": controller_id, "Key": key, "Keyid": key_id})


def handle_rekey(module, controller_id, mode, key, key_id, payload):
    if module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    if mode == "LKM":
        payload.update({"TargetFQDD": controller_id, "Mode": mode, "NewKey": key,
                       "Keyid": key_id, "OldKey": module.params.get("old_key")})
    else:
        payload.update({"TargetFQDD": controller_id, "Mode": mode})


def handle_remove_controller_key(module, controller_id, ctrl_key_id, payload):
    if module.check_mode and ctrl_key_id is not None:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    elif module.check_mode or ctrl_key_id is None:
        module.exit_json(msg=NO_CHANGES_FOUND)
    payload.update({"TargetFQDD": controller_id})


def handle_enable_controller_encryption(module, controller_id, security_status, mode, key, key_id, payload):
    if module.check_mode and security_status != "SecurityKeyAssigned":
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    elif (module.check_mode and security_status == "SecurityKeyAssigned") or (not module.check_mode and security_status == "SecurityKeyAssigned"):
        module.exit_json(msg=NO_CHANGES_FOUND)
    payload.update({"TargetFQDD": controller_id, "Mode": mode})
    if mode == "LKM":
        payload.update({"Key": key, "Keyid": key_id})


def ctrl_key(module, redfish_obj):
    resp, job_uri, job_id, payload = None, None, None, {}
    controller_id = module.params.get("controller_id")
    command, mode = module.params["command"], module.params["mode"]
    key, key_id = module.params.get("key"), module.params.get("key_id")

    check_id_exists(module, redfish_obj, "controller_id",
                    controller_id, CONTROLLER_URI)
    ctrl_resp = redfish_obj.invoke_request("GET", CONTROLLER_URI.format(
        system_id=SYSTEM_ID, controller_id=controller_id))

    security_status = ctrl_resp.json_data.get("Oem", {}).get("Dell", {}).get("DellController", {}).get("SecurityStatus")
    if security_status == "EncryptionNotCapable":
        module.fail_json(msg=ENCRYPT_ERR_MSG.format(controller_id))

    ctrl_key_id = ctrl_resp.json_data.get("Oem", {}).get("Dell", {}).get("DellController", {}).get("KeyID")

    if command == "SetControllerKey":
        handle_set_controller_key(
            module, controller_id, ctrl_key_id, key, key_id, payload)
    elif command == "ReKey":
        handle_rekey(module, controller_id, mode, key, key_id, payload)
    elif command == "RemoveControllerKey":
        handle_remove_controller_key(
            module, controller_id, ctrl_key_id, payload)
    elif command == "EnableControllerEncryption":
        handle_enable_controller_encryption(
            module, controller_id, security_status, mode, key, key_id, payload)

    resp = redfish_obj.invoke_request("POST", RAID_ACTION_URI.format(
        system_id=SYSTEM_ID, action=command), data=payload)
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


def enable_security(module, redfish_obj):
    resp, job_uri, job_id = None, None, None
    controller_id = module.params.get("controller_id")
    check_id_exists(module, redfish_obj, "controller_id", controller_id, CONTROLLER_URI)
    controller_resp = redfish_obj.invoke_request("GET", CONTROLLER_URI.format(system_id=SYSTEM_ID, controller_id=controller_id))
    encryption_mode = controller_resp.json_data.get("Oem", {}).get("Dell", {}).get("DellController", {}).get("EncryptionMode")
    if encryption_mode == "Enabled":
        module.exit_json(msg=NO_CHANGES_FOUND)
    elif module.check_mode and encryption_mode == "Disabled":
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    else:
        resp = redfish_obj.invoke_request("POST", RAID_ACTION_URI.format(system_id=SYSTEM_ID,
                                                                         action=module.params["command"]),
                                          data={"TargetFQDD": controller_id})
        job_uri = resp.headers.get("Location")
        job_id = job_uri.split("/")[-1]
    return resp, job_uri, job_id


def disable_security(module, redfish_obj):
    resp, job_uri, job_id = None, None, None
    controller_id = module.params.get("controller_id")
    check_id_exists(module, redfish_obj, "controller_id", controller_id, CONTROLLER_URI)
    controller_resp = redfish_obj.invoke_request("GET", CONTROLLER_URI.format(system_id=SYSTEM_ID, controller_id=controller_id))
    encryption_mode = controller_resp.json_data.get("Oem", {}).get("Dell", {}).get("DellController", {}).get("EncryptionMode")
    if encryption_mode == "Disabled":
        module.exit_json(msg=NO_CHANGES_FOUND)
    elif module.check_mode and encryption_mode == "Enabled":
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    else:
        resp = redfish_obj.invoke_request("POST", RAID_ACTION_URI.format(system_id=SYSTEM_ID,
                                                                         action=module.params["command"]),
                                          data={"ControllerFQDD": controller_id})
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
        pd_resp = redfish_obj.invoke_request("GET", PD_URI.format(
            controller_id=controller_id, drive_id=drive_id))
    except HTTPError:
        module.fail_json(msg=PD_ERROR_MSG.format(drive_id))
    else:
        hot_spare = pd_resp.json_data.get("HotspareType")
        resp, job_uri, job_id = hot_spare_config_refactored(
            module, redfish_obj, command, volume, drive_id, hot_spare)
    return resp, job_uri, job_id


def hot_spare_config_refactored(module, redfish_obj, command, volume, drive_id, hot_spare):
    resp, job_uri, job_id = None, None, None
    if module.check_mode and hot_spare == "None" and command == "AssignSpare" or \
            (module.check_mode and hot_spare != "None" and command == "UnassignSpare"):
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
        if module.check_mode and state != raid_status:
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
    volume = module.params.get("volume_id")
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
                drive_link = disk[ODATA_ID]
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
                                                                             action="SecureVirtualDisk"),
                                              data={"TargetFQDD": volume[0]})
            job_uri = resp.headers.get("Location")
            job_id = job_uri.split("/")[-1]
    return resp, job_uri, job_id


def online_capacity_expansion(module, redfish_obj):
    payload = None
    volume_id = module.params.get("volume_id")
    target = module.params.get("target")
    size = module.params.get("size")
    if not isinstance(volume_id, list):
        volume_id = [volume_id]
    if len(volume_id) != 1:
        module.exit_json(msg=TARGET_ERR_MSG.format("virtual drive"), failed=True)

    controller_id = volume_id[0].split(":")[-1]
    volume_uri = VOLUME_URI + "/{volume_id}"
    try:
        volume_resp = redfish_obj.invoke_request("GET", volume_uri.format(system_id=SYSTEM_ID,
                                                                          controller_id=controller_id,
                                                                          volume_id=volume_id[0]))
    except HTTPError:
        module.exit_json(msg=VD_ERROR_MSG.format(volume_id[0]), failed=True)

    try:
        raid_type = volume_resp.json_data.get("RAIDType")
        if raid_type in ['RAID50', 'RAID60']:
            module.exit_json(msg=OCE_RAID_TYPE_ERR.format(raid_type), failed=True)

        if target is not None:
            drives_to_add = online_capacity_expansion_refactored(module, target, volume_resp, raid_type)
            payload = {"TargetFQDD": volume_id[0], "PDArray": drives_to_add}

        elif size:
            vd_size = volume_resp.json_data.get("CapacityBytes")
            vd_size_mb = vd_size // (1024 * 1024)
            if (size - vd_size_mb) < 100:
                module.exit_json(msg=OCE_SIZE_100MB.format(vd_size_mb), failed=True)
            payload = {"TargetFQDD": volume_id[0], "Size": size}

        resp = redfish_obj.invoke_request("POST", RAID_ACTION_URI.format(system_id=SYSTEM_ID,
                                          action="OnlineCapacityExpansion"),
                                          data=payload)
        job_uri = resp.headers.get("Location")
        job_id = job_uri.split("/")[-1]
        return resp, job_uri, job_id
    except HTTPError as err:
        err = json.load(err).get("error").get("@Message.ExtendedInfo", [{}])[0].get("Message")
        module.exit_json(msg=err, failed=True)


def online_capacity_expansion_refactored(module, target, volume_resp, raid_type):
    if not target:
        module.exit_json(msg=OCE_TARGET_EMPTY, failed=True)

    if raid_type == 'RAID1':
        module.fail_json(msg=OCE_TARGET_RAID1_ERR)

    current_pd = []
    links = volume_resp.json_data.get("Links")
    if links:
        for disk in volume_resp.json_data.get("Links").get("Drives"):
            drive = disk[ODATA_ID].split('/')[-1]
            current_pd.append(drive)
    drives_to_add = [each_drive for each_drive in target if each_drive not in current_pd]
    if module.check_mode and drives_to_add and len(drives_to_add) % OCE_MIN_PD_RAID_MAPPING[raid_type] == 0:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    elif len(drives_to_add) == 0 or len(drives_to_add) % OCE_MIN_PD_RAID_MAPPING[raid_type] != 0:
        module.exit_json(msg=NO_CHANGES_FOUND)
    return drives_to_add


def match_id_in_list(id, member_list):
    for each_dict in member_list:
        url = each_dict[ODATA_ID]
        _id = url.split("/")[-1]
        if id == _id:
            return url


def validate_secure_erase(module, redfish_obj):
    drive_uri = None
    drive = module.params.get("target")
    drive_id = drive[0]
    controller_id = module.params.get("controller_id")
    uri, err_msg = validate_and_get_first_resource_id_uri(module, redfish_obj,
                                                          SYSTEMS_URI)
    if err_msg:
        module.exit_json(msg=err_msg, failed=True)
    storage_uri = get_dynamic_uri(redfish_obj, uri, "Storage")['@odata.id']
    storage_member_list = get_dynamic_uri(redfish_obj, storage_uri, "Members")
    controller_uri = match_id_in_list(controller_id, storage_member_list)
    if controller_uri is None:
        module.exit_json(msg=CNTRL_ERROR_MSG.format(controller_id), skipped=True)
    drives_list = get_dynamic_uri(redfish_obj, controller_uri, 'Drives')
    drive_uri = match_id_in_list(drive_id, drives_list)
    if drive_uri is None:
        module.exit_json(msg=PD_ERROR_MSG.format(drive_id), skipped=True)
    drive_detail = get_dynamic_uri(redfish_obj, drive_uri)
    firm_ver = get_idrac_firmware_version(redfish_obj)
    if LooseVersion(firm_ver) >= '1.0':
        dell_oem = drive_detail.get("Oem", {}).get("Dell", {})
        try:
            dell_disk = dell_oem["DellPhysicalDisk"]
        except KeyError:
            dell_disk = dell_oem.get("DellPCIeSSD", {})
        drive_ready = dell_disk.get("RaidStatus", {})
        if drive_ready != "Ready":
            module.exit_json(msg=DRIVE_NOT_READY.format(drive_id),
                             skipped=True)
        capable = dell_disk.get("SystemEraseCapability", {})
        if capable != "CryptographicErasePD":
            module.exit_json(msg=DRIVE_NOT_SECURE_ERASE.format(drive_id),
                             skipped=True)
    return drive_uri


def secure_erase(module, redfish_obj):
    drive_uri = validate_secure_erase(module, redfish_obj)
    job_type_list = ["RAIDConfiguration", "RealTimeNoRebootConfiguration"]
    scheduled_job = get_scheduled_job_resp(redfish_obj, job_type_list)
    if scheduled_job:
        job_id = scheduled_job.get("Id")
        job_uri = JOB_URI_OEM.format(job_id=job_id)
        module.exit_json(msg=JOB_EXISTS, status=scheduled_job, changed=False,
                         task={"id": job_id, "uri": job_uri})
    action_uri = get_dynamic_uri(redfish_obj, drive_uri, "Actions")
    secure_erase_uri = action_uri.get("#Drive.SecureErase").get("target")
    if module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    resp = redfish_obj.invoke_request("POST", secure_erase_uri, data="{}",
                                      dump=False)
    job_uri = resp.headers.get("Location")
    job_id = job_uri.split("/")[-1]
    return resp, job_uri, job_id


def validate_inputs(module):
    module_params = module.params
    command = module_params.get("command")
    mode = module_params.get("mode")
    key = module_params.get("key")
    key_id = module_params.get("key_id")
    old_key = module_params.get("old_key")
    target = module_params.get("target")
    volume = module_params.get("volume_id")
    command_need_target_validation = ["AssignSpare", "UnassignSpare", "BlinkTarget", "UnBlinkTarget",
                                      "LockVirtualDisk", "ChangePDStateToOnline", "ChangePDStateToOffline",
                                      "SecureErase"]
    command_need_volume_validation = ["AssignSpare", "UnassignSpare", "BlinkTarget", "UnBlinkTarget",
                                      "LockVirtualDisk"]

    if command == "ReKey" and mode == "LKM":
        if not all([key, key_id, old_key]):
            module.fail_json(msg="All of the following: key, key_id and old_key are "
                                 "required for '{0}' operation.".format(command))

    elif command == "EnableControllerEncryption" and mode == "LKM":
        if not all([key, key_id]):
            module.fail_json(msg="All of the following: key, key_id are "
                                 "required for '{0}' operation.".format(command))

    elif command in command_need_target_validation and target is not None and len(target) != 1:
        module.fail_json(msg=TARGET_ERR_MSG.format("physical disk"))
    elif command in command_need_volume_validation and volume is not None and len(volume) != 1:
        module.fail_json(msg=TARGET_ERR_MSG.format("virtual drive"))


def get_current_time(redfish_obj):
    try:
        resp = redfish_obj.invoke_request("GET", MANAGER_URI)
        curr_time = resp.json_data.get("DateTime")
        date_offset = resp.json_data.get("DateTimeLocalOffset")
    except Exception:
        return None, None
    return curr_time, date_offset


def validate_time(module, redfish_obj, mtime):
    curr_time, date_offset = get_current_time(redfish_obj)
    if not mtime.endswith(date_offset):
        module.exit_json(failed=True, status_msg=MAINTENANCE_OFFSET.format(date_offset))
    if mtime < curr_time:
        module.exit_json(failed=True, status_msg=MAINTENANCE_TIME)


def get_attributes(module, redfish_obj):
    resp_data = {}
    controller_id = module.params["controller_id"]
    try:
        resp = redfish_obj.invoke_request("GET", CONTROLLERS_URI.format(system_id=SYSTEM_ID,
                                                                        controller_id=controller_id))
        resp_data = resp.json_data
    except HTTPError:
        resp_data = {}
    return resp_data


def check_attr_exists(module, curr_attr, inp_attr):
    invalid_attr = []
    pending_attr = {}
    diff = 0
    for each in inp_attr:
        if each not in curr_attr.keys():
            invalid_attr.append(each)
        elif curr_attr[each] != inp_attr[each]:
            diff = 1
            pending_attr[each] = inp_attr[each]
    if invalid_attr:
        module.exit_json(msg=INVALID_ATTRIBUTES.format(invalid_attr), failed=True)
    if diff and module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    elif not diff:
        module.exit_json(msg=NO_CHANGES_FOUND)
    return pending_attr


def get_redfish_apply_time(module, redfish_obj, apply_time, time_settings):
    time_set = {}
    if time_settings:
        if 'Maintenance' in apply_time:
            if apply_time not in time_settings:
                module.exit_json(failed=True, status_msg=UNSUPPORTED_APPLY_TIME.format(apply_time))
            else:
                time_set['ApplyTime'] = apply_time
                m_win = module.params.get('maintenance_window')
                validate_time(module, redfish_obj, m_win.get('start_time'))
                time_set['MaintenanceWindowStartTime'] = m_win.get('start_time')
                time_set['MaintenanceWindowDurationInSeconds'] = m_win.get('duration')
        else:
            time_set['ApplyTime'] = apply_time
    return time_set


def apply_attributes(module, redfish_obj, pending, time_settings):
    payload = {"Oem": {"Dell": {"DellStorageController": pending}}}
    apply_time = module.params.get('apply_time')
    time_set = get_redfish_apply_time(module, redfish_obj, apply_time, time_settings)
    if time_set:
        payload["@Redfish.SettingsApplyTime"] = time_set
    try:
        resp = redfish_obj.invoke_request("PATCH", SETTINGS_URI.format(system_id=SYSTEM_ID,
                                                                       controller_id=module.params["controller_id"]),
                                          data=payload)
        if resp.status_code == 202 and "error" in resp.json_data:
            msg_err_id = resp.json_data.get("error").get("@Message.ExtendedInfo", [{}])[0].get("MessageId")
            if "Created" not in msg_err_id:
                module.exit_json(msg=ERR_MSG, error_info=resp.json_data, failed=True)
    except HTTPError as err:
        err = json.load(err).get("error")
        module.exit_json(msg=ERR_MSG, error_info=err, failed=True)
    job_id = resp.headers["Location"].split("/")[-1]
    return job_id, time_set


def set_attributes(module, redfish_obj):
    resp_data = get_attributes(module, redfish_obj)
    curr_attr = resp_data.get("Oem").get("Dell").get("DellStorageController")
    inp_attr = module.params.get("attributes")
    if inp_attr.get("ControllerMode") and len(inp_attr.keys()) > 1:
        module.exit_json(msg=HBA_MODE, failed=True)
    pending = check_attr_exists(module, curr_attr, inp_attr)
    time_settings = resp_data.get("@Redfish.Settings", {}).get("SupportedApplyTimes", [])
    job_id, time_set = apply_attributes(module, redfish_obj, pending, time_settings)
    return job_id, time_set


def job_condition_check(module, redfish_obj, job_id, job_uri,
                        job_completion_msg, job_submission_msg,
                        condition=True):
    job_wait = module.params.get("job_wait")
    if condition and job_wait:
        resp, msg = wait_for_job_completion(redfish_obj, job_uri, job_wait=job_wait,
                                            wait_timeout=module.params["job_wait_timeout"])
        if not resp:
            job_completion_msg = msg
            resp = redfish_obj.invoke_request("GET", job_uri)
        job_data = strip_substr_dict(resp.json_data)
        if job_data["JobState"] == "Failed":
            changed, failed = False, True
        else:
            changed, failed = True, False
        module.exit_json(msg=job_completion_msg, changed=changed, failed=failed,
                         task={"id": job_id, "uri": job_uri}, status=job_data)
    else:
        resp, msg = wait_for_job_completion(redfish_obj, job_uri, job_wait=job_wait,
                                            wait_timeout=module.params["job_wait_timeout"])
        if resp == {}:
            module.exit_json(msg=msg, task={"id": job_id, "uri": job_uri})
        job_data = strip_substr_dict(resp.json_data)
        module.exit_json(msg=job_submission_msg, task={"id": job_id, "uri": job_uri},
                         status=job_data)


def validate_operations(module, server_generation_op):
    generation = server_generation_op[0]
    command = module.params.get("command")
    idrac9_invalid_commands = ["EnableSecurity", "DisableSecurity"]
    idrac10_invalid_commands = ["SetControllerKey", "RemoveControllerKey",
                                "ReKey", "EnableControllerEncryption"]
    if (generation < 17 and command in idrac9_invalid_commands) or \
            (generation >= 17 and command in idrac10_invalid_commands):
        module.exit_json(msg=INVALID_COMMAND.format(command, server_generation_op[2]), changed=False)


def validate_params(module):
    start_time = None
    key_id = module.params.get("key_id")
    key = module.params.get("key")
    maintenance_window = module.params.get("maintenance_window")
    if maintenance_window:
        start_time = maintenance_window.get('start_time')
    if key:
        pattern_key = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{1,32}$'
        if not re.match(pattern_key, key):
            module.exit_json(failed=True, msg=INVALID_KEY)
    if key_id:
        pattern_key_id = r'^[^\s]{1,32}$'
        if not re.match(pattern_key_id, key_id):
            module.exit_json(failed=True, msg=INVALID_KEY_ID)
    if start_time:
        pattern_start_time = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})$'
        if not re.match(pattern_start_time, start_time):
            module.exit_json(failed=True, msg=INVALID_START_TIME)


def get_server_generation(redfish_obj: Redfish):
    """
    Function wrapping redfish_obj.get_server_generation. Helps with mocked testing.

    Args:
        redfish_obj (Redfish): Redfish object.

    Returns:
        Tuple[int, str, str]: A tuple containing the server generation, firmware version, and hardware model.
    """
    return redfish_obj.get_server_generation


def main():
    specs = {
        "attributes": {"type": 'dict'},
        "command": {"required": False,
                    "choices": ["ResetConfig", "AssignSpare", "SetControllerKey", "RemoveControllerKey",
                                "ReKey", "UnassignSpare", "EnableControllerEncryption", "BlinkTarget",
                                "UnBlinkTarget", "ConvertToRAID", "ConvertToNonRAID", "ChangePDStateToOnline",
                                "ChangePDStateToOffline", "LockVirtualDisk", "OnlineCapacityExpansion", "SecureErase",
                                "EnableSecurity", "DisableSecurity"]},
        "controller_id": {"required": False, "type": "str"},
        "volume_id": {"required": False, "type": "list", "elements": "str"},
        "target": {"required": False, "type": "list", "elements": "str", "aliases": ["drive_id"]},
        "key": {"required": False, "type": "str", "no_log": True},
        "key_id": {"required": False, "type": "str"},
        "old_key": {"required": False, "type": "str", "no_log": True},
        "mode": {"required": False, "choices": ["LKM", "SEKM"], "default": "LKM"},
        "apply_time": {"type": 'str', "default": 'Immediate',
                       "choices": ['Immediate', 'OnReset', 'AtMaintenanceWindowStart', 'InMaintenanceWindowOnReset']},
        "maintenance_window": {"type": 'dict',
                               "options": {"start_time": {"type": 'str', "required": True},
                                           "duration": {"type": 'int', "required": False, "default": 900}}},
        "job_wait": {"required": False, "type": "bool", "default": False},
        "job_wait_timeout": {"required": False, "type": "int", "default": 120},
        "size": {"required": False, "type": "int"}
    }
    module = RedfishAnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[('attributes', 'command'), ("target", "size")],
        required_one_of=[('attributes', 'command')],
        required_if=[
            ["command", "SetControllerKey", ["controller_id", "key", "key_id"]],
            ["command", "ReKey", ["controller_id", "mode"]], ["command", "ResetConfig", ["controller_id"]],
            ["command", "RemoveControllerKey", ["controller_id"]], ["command", "AssignSpare", ["target"]],
            ["command", "UnassignSpare", ["target"]], ["command", "EnableControllerEncryption", ["controller_id"]],
            ["command", "BlinkTarget", ["target", "volume_id"], True],
            ["command", "UnBlinkTarget", ["target", "volume_id"], True], ["command", "ConvertToRAID", ["target"]],
            ["command", "ConvertToNonRAID", ["target"]], ["command", "ChangePDStateToOnline", ["target"]],
            ["command", "ChangePDStateToOffline", ["target"]],
            ["command", "LockVirtualDisk", ["volume_id"]], ["command", "OnlineCapacityExpansion", ["volume_id"]],
            ["command", "OnlineCapacityExpansion", ["target", "size"], True],
            ["command", "LockVirtualDisk", ["volume_id"]],
            ["command", "SecureErase", ["controller_id", "target"]],
            ["apply_time", "AtMaintenanceWindowStart", ("maintenance_window",)],
            ["apply_time", "InMaintenanceWindowOnReset", ("maintenance_window",)]
        ],
        supports_check_mode=True)
    try:
        command = module.params["command"]
        with Redfish(module.params, req_session=True) as redfish_obj:
            server_generation_op = get_server_generation(redfish_obj)
            validate_operations(module, server_generation_op)
            validate_params(module)
            if not bool(module.params["attributes"]):
                validate_inputs(module)
            command_function_mapping = {
                "ResetConfig": ctrl_reset_config,
                "SetControllerKey": ctrl_key,
                "ReKey": ctrl_key,
                "RemoveControllerKey": ctrl_key,
                "EnableControllerEncryption": ctrl_key,
                "AssignSpare": hot_spare_config,
                "UnassignSpare": hot_spare_config,
                "ConvertToRAID": convert_raid_status,
                "ConvertToNonRAID": convert_raid_status,
                "ChangePDStateToOnline": change_pd_status,
                "ChangePDStateToOffline": change_pd_status,
                "LockVirtualDisk": lock_virtual_disk,
                "OnlineCapacityExpansion": online_capacity_expansion,
                "SecureErase": secure_erase,
                "EnableSecurity": enable_security,
                "DisableSecurity": disable_security
            }

            if command in ["BlinkTarget", "UnBlinkTarget"]:
                resp = target_identify_pattern(module, redfish_obj)
                if resp.success and resp.status_code == 200:
                    module.exit_json(msg=JOB_COMPLETION.format(command), changed=True)
            elif command:
                func = command_function_mapping[command]
                resp, job_uri, job_id = func(module, redfish_obj)

            if module.params["attributes"]:
                controller_id = module.params["controller_id"]
                if controller_id is None:
                    module.exit_json(msg=CONTROLLER_ID_REQUIRED, failed=True)
                check_id_exists(module, redfish_obj, "controller_id", controller_id, CONTROLLER_URI)
                job_id, time_set = set_attributes(module, redfish_obj)
                job_uri = JOB_URI_OEM.format(job_id=job_id)
                job_condition_check(module, redfish_obj, job_id,
                                    job_uri, JOB_COMPLETION_ATTRIBUTES,
                                    JOB_SUBMISSION_ATTRIBUTES,
                                    time_set["ApplyTime"] == "Immediate")
            oem_job_url = JOB_URI_OEM.format(job_id=job_id)
            job_condition_check(module, redfish_obj, job_id, oem_job_url,
                                JOB_COMPLETION.format(command),
                                JOB_SUBMISSION.format(command))
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError, AttributeError) as e:
        module.exit_json(msg=str(e), failed=True)


if __name__ == '__main__':
    main()
