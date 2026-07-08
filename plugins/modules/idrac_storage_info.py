#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.9.0
# Copyright (C) 2026 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: idrac_storage_info
short_description: Get the storage controller, physical disk, and virtual disk information
version_added: "9.9.0"
description:
  - This module allows you to query storage controllers, physical disks, and virtual disks on iDRAC.
  - Returns merged Redfish and Dell OEM attributes for the requested resource type.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_x_auth_options
options:
  resource_type:
    type: str
    required: true
    description:
      - C(controller), returns details of all storage controllers.
      - C(physical_disk), returns details of all physical disks attached to the specified I(controller_id).
      - C(virtual_disk), returns details of all virtual disks on the specified I(controller_id).
    choices: ['controller', 'physical_disk', 'virtual_disk']
  controller_id:
    type: str
    description:
      - Fully Qualified Device Descriptor (FQDD) of the storage controller, for example 'RAID.Integrated.1-1'.
      - This is required when I(resource_type) is C(physical_disk) or C(virtual_disk).

requirements:
  - "python >= 3.9.6"
author:
  - "Dell OpenManage Ansible Team"
notes:
    - Run this module from a system that has direct access to Integrated Dell Remote Access Controller.
    - This module supports both IPv4 and IPv6 address for I(idrac_ip).
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Get all storage controllers
  dellemc.openmanage.idrac_storage_info:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    resource_type: "controller"

- name: Get all physical disks for a controller
  dellemc.openmanage.idrac_storage_info:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    resource_type: "physical_disk"
    controller_id: "RAID.Slot.1-1"

- name: Get all virtual disks for a controller
  dellemc.openmanage.idrac_storage_info:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    resource_type: "virtual_disk"
    controller_id: "RAID.Slot.1-1"
'''

RETURN = r'''
---
msg:
  type: str
  description: Overall status of the storage information query operation.
  returned: always
  sample: "Successfully fetched the storage information."
storage_info:
  type: dict
  description: Details of the requested storage resource(s).
  returned: success
  sample:
    {
      "resource_count": 1,
      "resources": [
        {
          "Id": "RAID.Slot.1-1",
          "Model": "PERC H755",
          "FirmwareVersion": "25.5.9.0001",
          "Status": {"Health": "OK"}
        }
      ],
      "total_capacity": null,
      "available_capacity": null,
      "idrac_generation": 17,
      "idrac_firmware_version": "7.10.90.00",
      "idrac_model": "iDRAC 9"
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
          "MessageId": "GEN1234",
          "RelatedProperties": [],
          "Message": "Unable to process the request because an error occurred.",
          "MessageArgs": [],
          "Severity": "Critical",
          "Resolution": "Retry the operation. If the issue persists, contact your system administrator."
        }
      ]
    }
  }
'''

import json
from urllib.error import HTTPError, URLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, IdracAnsibleModule
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    get_dynamic_uri, validate_and_get_first_resource_id_uri)

CONTROLLER_ID_REQUIRED_MSG = "controller_id is required when resource_type is '{resource_type}'."
SUCCESS_MSG = "Successfully fetched the storage information."
MIN_FIRMWARE_VERSION = {
    "iDRAC 9": "7.10.90.00",
    "iDRAC 10": "1.20.50.50",
}
UNSUPPORTED_FIRMWARE_MSG = ("Installed {hw_model} firmware version {firmware_version} does not meet the minimum "
                            "required version {min_version} for this module.")
UNSUPPORTED_GENERATION_MSG = "This module is not supported on {hw_model}."
SYSTEMS_URI = "/redfish/v1/Systems"
ODATA_ID = "@odata.id"
STORAGE_EXPAND_QUERY = "?$expand=*($levels=1)"
CONTROLLER_OEM_FIELDS = ["PatrolReadRatePercent", "RebuildRatePercent", "CopybackMode",
                         "EncryptionCapability", "EncryptionMode"]
PHYSICAL_DISK_OEM_FIELDS = ["RaidStatus", "HotSpareStatus", "UsedSizeBytes", "FreeSizeInBytes",
                            "EncryptionCapable", "PredictiveFailureState"]
VIRTUAL_DISK_OEM_FIELDS = ["RaidStatus", "ReadCachePolicy", "WriteCachePolicy", "DiskCachePolicy"]
CONTROLLER_NOT_FOUND_MSG = "Specified controller '{controller_id}' does not exist."


class StorageInfo:
    def __init__(self, idrac, module):
        self.idrac = idrac
        self.module = module
        self._generation_info = None

    def validate_params(self):
        resource_type = self.module.params.get("resource_type")
        controller_id = self.module.params.get("controller_id")
        if resource_type in ("physical_disk", "virtual_disk") and not controller_id:
            self.module.exit_json(
                msg=CONTROLLER_ID_REQUIRED_MSG.format(resource_type=resource_type), failed=True)

    @staticmethod
    def _version_meets_minimum(current_version, min_version):
        def to_tuple(version):
            return tuple(int(part) for part in version.split('.'))
        current = to_tuple(current_version)
        minimum = to_tuple(min_version)
        max_len = max(len(current), len(minimum))
        current = current + (0,) * (max_len - len(current))
        minimum = minimum + (0,) * (max_len - len(minimum))
        return current >= minimum

    def validate_firmware_version(self):
        self._generation_info = self.idrac.get_server_generation
        generation, firmware_version, hw_model = self._generation_info
        min_version = MIN_FIRMWARE_VERSION.get(hw_model)
        if min_version is None:
            self.module.exit_json(msg=UNSUPPORTED_GENERATION_MSG.format(hw_model=hw_model), failed=True)
        if not self._version_meets_minimum(firmware_version, min_version):
            self.module.exit_json(
                msg=UNSUPPORTED_FIRMWARE_MSG.format(hw_model=hw_model, firmware_version=firmware_version,
                                                     min_version=min_version),
                failed=True)

    def fetch_storage_uri(self):
        uri, err_msg = validate_and_get_first_resource_id_uri(None, self.idrac, SYSTEMS_URI)
        if err_msg:
            self.module.exit_json(msg=err_msg, failed=True)
        storage = get_dynamic_uri(self.idrac, uri, 'Storage')
        return storage[ODATA_ID]

    def get_controllers(self):
        storage_uri = self.fetch_storage_uri()
        controllers_data = get_dynamic_uri(self.idrac, storage_uri + STORAGE_EXPAND_QUERY)
        controllers = []
        for member in controllers_data.get("Members", []):
            controller_id = member.get("Id", "")
            if controller_id.startswith("CPU"):
                continue
            controllers.append(self._map_controller(member))
        return controllers

    @staticmethod
    def _map_controller(member):
        storage_controllers = member.get("StorageControllers") or [{}]
        controller_detail = storage_controllers[0] if storage_controllers else {}
        oem_dell = member.get("Oem", {}).get("Dell", {}).get("DellController", {})
        mapped = {
            "Id": member.get("Id"),
            "Name": member.get("Name"),
            "Model": controller_detail.get("Model"),
            "FirmwareVersion": controller_detail.get("FirmwareVersion"),
            "Status": member.get("Status"),
        }
        for field in CONTROLLER_OEM_FIELDS:
            mapped[field] = oem_dell.get(field)
        return mapped

    def get_controller_by_id(self, controller_id):
        storage_uri = self.fetch_storage_uri()
        controllers_data = get_dynamic_uri(self.idrac, storage_uri + STORAGE_EXPAND_QUERY)
        for member in controllers_data.get("Members", []):
            if member.get("Id") == controller_id:
                return member
        self.module.exit_json(msg=CONTROLLER_NOT_FOUND_MSG.format(controller_id=controller_id), failed=True)

    def get_physical_disks(self, controller_id):
        controller = self.get_controller_by_id(controller_id)
        physical_disks = []
        for drive_ref in controller.get("Drives", []):
            drive_data = get_dynamic_uri(self.idrac, drive_ref.get(ODATA_ID))
            physical_disks.append(self._map_physical_disk(drive_data))
        return physical_disks

    @staticmethod
    def _map_physical_disk(drive):
        oem_dell = drive.get("Oem", {}).get("Dell", {}).get("DellPhysicalDisk", {})
        mapped = {
            "Id": drive.get("Id"),
            "Name": drive.get("Name"),
            "CapacityBytes": drive.get("CapacityBytes"),
            "MediaType": drive.get("MediaType"),
            "Protocol": drive.get("Protocol"),
            "Status": drive.get("Status"),
            "PhysicalLocation": drive.get("PhysicalLocation"),
        }
        for field in PHYSICAL_DISK_OEM_FIELDS:
            mapped[field] = oem_dell.get(field)
        return mapped

    def get_virtual_disks(self, controller_id):
        controller = self.get_controller_by_id(controller_id)
        volumes_uri = controller.get("Volumes", {}).get(ODATA_ID)
        virtual_disks = []
        if volumes_uri:
            volume_refs = get_dynamic_uri(self.idrac, volumes_uri, "Members") or []
            for volume_ref in volume_refs:
                volume_data = get_dynamic_uri(self.idrac, volume_ref.get(ODATA_ID))
                virtual_disks.append(self._map_virtual_disk(volume_data))
        return virtual_disks

    @staticmethod
    def _map_virtual_disk(volume):
        oem_dell = volume.get("Oem", {}).get("Dell", {}).get("DellVirtualDisk", {})
        mapped = {
            "Id": volume.get("Id"),
            "Name": volume.get("Name"),
            "RAIDType": volume.get("RAIDType"),
            "CapacityBytes": volume.get("CapacityBytes"),
            "Status": volume.get("Status"),
        }
        for field in VIRTUAL_DISK_OEM_FIELDS:
            mapped[field] = oem_dell.get(field)
        return mapped

    @staticmethod
    def _compute_capacity(resource_type, resources):
        if resource_type == "physical_disk":
            total_capacity = sum(resource.get("CapacityBytes") or 0 for resource in resources)
            available_capacity = sum(resource.get("FreeSizeInBytes") or 0 for resource in resources)
            return total_capacity, available_capacity
        if resource_type == "virtual_disk":
            total_capacity = sum(resource.get("CapacityBytes") or 0 for resource in resources)
            return total_capacity, None
        return None, None

    def fetch_resources(self):
        resource_type = self.module.params.get("resource_type")
        controller_id = self.module.params.get("controller_id")
        if resource_type == "controller":
            resources = self.get_controllers()
        elif resource_type == "physical_disk":
            resources = self.get_physical_disks(controller_id)
        else:
            resources = self.get_virtual_disks(controller_id)
        total_capacity, available_capacity = self._compute_capacity(resource_type, resources)
        generation, firmware_version, hw_model = self._generation_info or self.idrac.get_server_generation
        return {
            "resource_count": len(resources),
            "resources": resources,
            "total_capacity": total_capacity,
            "available_capacity": available_capacity,
            "idrac_generation": generation,
            "idrac_firmware_version": firmware_version,
            "idrac_model": hw_model,
        }


def main():
    specs = {
        "resource_type": {"type": "str", "required": True,
                           "choices": ["controller", "physical_disk", "virtual_disk"]},
        "controller_id": {"type": "str"},
    }
    module = IdracAnsibleModule(
        argument_spec=specs,
        supports_check_mode=True)
    try:
        with iDRACRedfishAPI(module.params) as idrac:
            storage_info_obj = StorageInfo(idrac, module)
            storage_info_obj.validate_params()
            storage_info_obj.validate_firmware_version()
            storage_info = storage_info_obj.fetch_resources()
        module.exit_json(msg=SUCCESS_MSG, storage_info=storage_info)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
