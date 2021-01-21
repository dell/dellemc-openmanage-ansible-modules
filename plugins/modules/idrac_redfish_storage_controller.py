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
module: idrac_redfish_storage_controller
short_description: Configures the storage controller settings
version_added: "2.1.0"
description:
  - This module configures the settings of the storage controller using Redfish.
extends_documentation_fragment:
  - dellemc.openmanage.redfish_auth_options
options:
  command:
    description:
      - These actions may require a system reset, depending on the controller's capabilities.
      - C(ResetConfig) - Deletes all the virtual disks and unassigns all hot spares on physical disks.
      - C(AssignSpare) - Assigns a physical disk as a dedicated or global hot spare for a virtual disk.
      - >-
        C(SetControllerKey) - Sets the key on controllers, which is used to encrypt the drives in Local key
        Management(LKM).
      - C(RemoveControllerKey) - Erases the encryption key on the controller.
      - C(ReKey) - Resets the key on the controller.
    choices: [ResetConfig, AssignSpare, SetControllerKey, RemoveControllerKey, ReKey]
    default: AssignSpare
    type: str
  target:
    description:
      - Fully Qualified Device Descriptor (FQDD) of the target physical drive that is assigned as a spare.
      - This is mandatory when I(command) is C(AssignSpare).
      - If I(volume_id) is not specified or empty, this physical drive will be assigned as a global hot spare.
    type: str
  volume_id:
    description:
      - FQDD of the volumes to which a hot spare is assigned.
      - Applicable if I(command) is C(AssignSpare).
      - To know the number of volumes to which a hot spare can be assigned, refer iDRAC Redfish API guide.
    type: list
    elements: str
  controller_id:
    description:
      - FQDD of the storage controller. For example- 'RAID.Slot.1-1'.
      - >-
        This option is mandatory when I(command) is C(ResetConfig), C(SetControllerKey), C(RemoveControllerKey) and
        C(ReKey).
    type: str
  key:
    description:
      - >-
        A new security key passphrase that the encryption-capable controller uses to create the encryption key. The
        controller uses the encryption key to lock or unlock access to the Self Encryption Disk(SED). Only one
        encryption key can be created for each controller.
      - This is mandatory when I(command) is C(SetControllerKey) or C(ReKey), and when I(mode) is C(LKM).
    type: str
  key_id:
    description:
      - This is a user supplied text label associated with the passphrase.
      - This is mandatory when I(command) is C(SetControllerKey) or C(ReKey), and when I(mode) is C(LKM).
    type: str
  old_key:
    description:
      - Security key passphrase used by the encryption-capable controller..
      - This option is mandatory when I(command) is C(ReKey) and I(mode) is C(LKM).
    type: str
  mode:
    description:
      - >-
        Encryption mode of the encryption-capable controller: 1 - Local Key Management (LKM),
        2 - Security Enterprise Key Manager(SEKM).
      - This option is applicable only when I(command) is C(ReKey).
      - C(SEKM) requires secure enterprise key manager license on the iDRAC.
    choices: [LKM, SEKM]
    default: LKM
    type: str
requirements:
  - "python >= 2.7.5"
author: "Jagadeesh N V (@jagadeeshnv)"
notes:
    - Run this module from a system that has direct access to DellEMC iDRAC.
    - This module does not support C(check_mode).
'''

EXAMPLES = r'''
---
- name: Assign dedicated hot spare
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
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
    target: "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1"
  tags:
    - assign_global_hot_spare

- name: Set controller encryption key
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
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
    command: "RemoveControllerKey"
    controller_id: "RAID.Slot.1-1"
  tags:
    - remove_controller_key

- name: Reset controller configuration
  dellemc.openmanage.idrac_redfish_storage_controller:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    command: "ResetConfig"
    controller_id: "RAID.Slot.1-1"
  tags:
    - reset_config
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
from ansible_collections.dellemc.openmanage.plugins.module_utils.redfish import Redfish
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


SYSTEM_ID = "System.Embedded.1"
DRIVES_URI = "/redfish/v1/Systems/{system_id}/Storage/Drives/{id}"
CONTROLLER_URI = "/redfish/v1/Systems/{system_id}/Storage/{id}"
VOLUME_ID_URI = "/redfish/v1/Systems/{system_id}/Storage/Volumes/{id}"
RAID_ACTION_URI_PREFIX = "/redfish/v1/Dell/Systems/{system_id}/DellRaidService/Actions/DellRaidService.{op}"
RAID_SERVICE_URI = "/redfish/v1/Dell/Systems/{system_id}/DellRaidService"
DELL_CONTROLLER_URI = "/redfish/v1/Systems/{system_id}/Storage/{id}"


def check_id_exists(module, redfish_obj, item_id, uri):
    specified_id = module.params.get(item_id)
    item_uri = uri.format(system_id=SYSTEM_ID, id=specified_id)
    msg = "{0} with id {1} not found in system".format(item_id, specified_id)
    try:
        resp = redfish_obj.invoke_request('GET', item_uri)
        if not resp.success:
            module.fail_json(msg=msg)
    except HTTPError as err:
        module.fail_json(msg=msg, error_info=json.load(err))
    except (RuntimeError, URLError, SSLValidationError, ConnectionError, KeyError, ImportError,
            ValueError, TypeError) as err:
        module.fail_json(msg=str(err))


def check_volume_array_exists(module, redfish_obj):
    volume_array = module.params.get("volume_id")
    msg = "Unable to locate the virtual disk with the ID: {vol}"
    for vol in volume_array:
        try:
            resp = redfish_obj.invoke_request('GET', VOLUME_ID_URI.format(system_id=SYSTEM_ID, id=vol))
            if not resp.success:
                module.fail_json(msg=msg.format(vol=vol))
        except HTTPError as err:
            module.fail_json(msg=msg.format(vol=vol), error_info=json.load(err))
        except (RuntimeError, URLError, SSLValidationError, ConnectionError, KeyError, ImportError,
                ValueError, TypeError) as err:
            module.fail_json(msg=str(err))


def check_raid_service(module, redfish_obj):
    msg = "Installed version of iDRAC does not support this feature using Redfish API"
    try:
        resp = redfish_obj.invoke_request('GET', RAID_SERVICE_URI.format(system_id=SYSTEM_ID))
        if not resp.success:
            module.fail_json(msg=msg)
    except HTTPError as err:
        module.fail_json(msg=msg, error_info=json.load(err))
    except (RuntimeError, URLError, SSLValidationError, ConnectionError, KeyError, ImportError,
            ValueError, TypeError) as err:
        module.fail_json(msg=str(err))


def check_encryption_capability(module, redfish_obj):
    ctrl_id = module.params["controller_id"]
    uri = DELL_CONTROLLER_URI.format(system_id=SYSTEM_ID, id=ctrl_id)
    response = redfish_obj.invoke_request('GET', uri)
    if response.success:
        data = response.json_data
        if data['Oem']['Dell']['DellController']['SecurityStatus'] == "EncryptionNotCapable":
            module.fail_json(msg="Encryption is not supported on the storage controller: {0}".format(ctrl_id))


def validate_inputs(module):
    module_params = module.params
    if module_params.get("command") == "ReKey" and module_params.get("mode") == "LKM":
        key = module_params.get("key")
        key_id = module_params.get("key_id")
        old_key = module_params.get("old_key")
        if not all([key, key_id, old_key]):
            module.fail_json(msg="All of the following: key, key_id and old_key are required for ReKey operation.")


def main():
    payload_map = {
        "controller_id": "TargetFQDD",
        "volume_id": "VirtualDiskArray",
        "target": "TargetFQDD",
        "key": "Key",
        "key_id": "Keyid",
        "old_key": "OldKey",
        "mode": "Mode"
    }
    req_map = {
        'ResetConfig': ["controller_id"],
        'AssignSpare': ["volume_id", "target"],
        'SetControllerKey': ["controller_id", "key", "key_id"],
        'RemoveControllerKey': ["controller_id"],
        'ReKey': ["controller_id", "mode"]
    }
    module = AnsibleModule(
        argument_spec={
            "baseuri": {"required": True, "type": 'str'},
            "username": {"required": True, "type": 'str'},
            "password": {"required": True, "type": 'str', "no_log": True},
            "command": {"required": False,
                        "choices": ['ResetConfig', 'AssignSpare', 'SetControllerKey', 'RemoveControllerKey', 'ReKey'],
                        "default": 'AssignSpare'},
            "controller_id": {"required": False, "type": 'str'},
            "volume_id": {"required": False, "type": 'list', "elements": 'str'},
            "target": {"required": False, "type": 'str'},
            "key": {"required": False, "type": 'str', "no_log": True},
            "key_id": {"required": False, "type": 'str'},
            "old_key": {"required": False, "type": 'str', "no_log": True},
            "mode": {"required": False, "choices": ['LKM', 'SEKM'], "default": 'LKM'}
        },
        required_if=[
            ["command", "SetControllerKey", req_map["SetControllerKey"]],
            ["command", "ReKey", req_map["ReKey"]],
            ["command", "ResetConfig", req_map["ResetConfig"]],
            ["command", "RemoveControllerKey", req_map["RemoveControllerKey"]],
            ["command", "AssignSpare", ["target"]]
        ],
        supports_check_mode=False)
    try:
        validate_inputs(module)
        with Redfish(module.params, req_session=True) as redfish_obj:
            ctrl_fn = module.params['command']
            check_raid_service(module, redfish_obj)
            if ctrl_fn == "AssignSpare":
                if module.params.get("volume_id"):
                    check_volume_array_exists(module, redfish_obj)
                check_id_exists(module, redfish_obj, "target", DRIVES_URI)
            else:
                check_id_exists(module, redfish_obj, "controller_id", CONTROLLER_URI)
            msg = "Failed to submit the job to that performs the {0} operation.".format(ctrl_fn)
            if ctrl_fn in ["SetControllerKey", "ReKey"]:
                check_encryption_capability(module, redfish_obj)
            payload_list = req_map[ctrl_fn]
            payload = {}
            for p in payload_list:
                payload[payload_map[p]] = module.params.get(p)
            if ctrl_fn == "ReKey":
                if module.params["mode"] == "LKM":
                    payload["NewKey"] = module.params.get("key")
                    payload["OldKey"] = module.params.get("old_key")
                    payload["Keyid"] = module.params.get("key_id")
            if ctrl_fn == "AssignSpare" and not payload.get("VirtualDiskArray"):
                payload.pop("VirtualDiskArray")
            built_uri = RAID_ACTION_URI_PREFIX.format(system_id=SYSTEM_ID, op=ctrl_fn)
            resp = redfish_obj.invoke_request("POST", built_uri, data=payload)
            if resp.success:
                status = {}
                status["uri"] = resp.headers.get("Location")
                if status.get("uri") is not None:
                    status["id"] = status["uri"].split("/")[-1]
                module.exit_json(changed=True, msg="Successfully submitted the job that performs the {0} operation"
                                 .format(ctrl_fn), task=status)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except (RuntimeError, URLError, SSLValidationError, ConnectionError, KeyError, ImportError,
            ValueError, TypeError) as err:
        module.fail_json(msg=str(err))
    module.fail_json(msg=msg)


if __name__ == '__main__':
    main()
