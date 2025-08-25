#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2024-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

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
  - dellemc.openmanage.idrac_x_auth_options
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
      - Fully Qualified Device Descriptor (FQDD) of the storage controller, for example 'RAID.Integrated.1-1'.
        Controller FQDD is required for C(create) RAID configuration.
  media_type:
    type: str
    description: Media type.
    choices: ['HDD', 'SSD']
  protocol:
    type: str
    description: Bus protocol.
    choices: ['SAS', 'SATA', 'PCIE']
  volume_id:
    type: str
    description:
      - Fully Qualified Device Descriptor (FQDD) of the virtual disk, for example 'Disk.virtual.0:RAID.Slot.1-1'.
        This option is used to get the virtual disk information.
  volumes:
    type: list
    elements: dict
    description:
      - A list of virtual disk specific iDRAC attributes. This is applicable for C(create) and C(delete) operations.
      - For C(create) operation, name and drives are applicable options, other volume options can also be specified.
      - The drives is a required option for C(create) operation and accepts either location (list of drive slot)
        or id (list of drive fqdd).
      - In iDRAC8, there is no pre-validation for the state of drives. The disk ID or slot number of the drive
        provided may or may not be in Ready state. Enter the disk ID or slot number of the drive that is already
        in Ready state.
      - For C(delete) operation, only name option is applicable.
      - See the examples for more details.
  capacity:
    type: float
    description: Virtual disk size in GB.
  raid_reset_config:
    type: str
    description:
      - This option represents whether a reset config operation needs to be performed on the RAID controller.
        Reset Config operation deletes all the virtual disks present on the RAID controller.
    choices: ['true', 'false']
    default: 'false'
  raid_init_operation:
    type: str
    description: This option represents initialization configuration operation to be performed on the virtual disk.
    choices: [None, Fast]
  job_wait:
    description:
      - This parameter provides the option to wait for the job completion.
      - This is applicable when I(state) is C(create) or C(delete).
    type: bool
    default: true
  job_wait_timeout:
    description:
      - This parameter is the maximum wait time of I(job_wait) in seconds.
      - This option is applicable when I(job_wait) is C(true).
    type: int
    default: 900
  time_to_wait:
    description:
      - The maximum wait time before shutdown in seconds for the Server Configuration Profile (SCP) import operation.
      - This option is applicable when I(state) is C(create) or C(delete).
    type: int
    default: 300

requirements:
  - "python >= 3.9.6"
author:
  - "Felix Stephen (@felixs88)"
  - "Kritika Bhateja (@Kritika-Bhateja-03)"
  - "Abhishek Sinha(@ABHISHEK-SINHA10)"
  - "Akash Shendge(@shenda1)"
notes:
    - Run this module from a system that has direct access to Integrated Dell Remote Access Controller.
    - This module supports both IPv4 and IPv6 address for I(idrac_ip).
    - This module supports C(check_mode).
    - This module does not display the controller battery details for the C(view) operation of the storage in iDRAC8.
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
      "TargetSettingsURI": null,
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

import re
import operator
from urllib.error import HTTPError, URLError
from copy import deepcopy
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, IdracAnsibleModule
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    get_dynamic_uri, validate_and_get_first_resource_id_uri, xml_data_conversion, idrac_redfish_job_tracking, remove_key, get_idrac_firmware_version)


SYSTEMS_URI = "/redfish/v1/Systems"
iDRAC_JOB_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/{job_id}"
CONTROLLER_NOT_EXIST_ERROR = "Specified Controller {controller_id} does not exist in the System."
CONTROLLER_NOT_DEFINED = "Controller ID is required."
SUCCESSFUL_OPERATION_MSG = "Successfully completed the {operation} storage volume operation."
DRIVES_NOT_EXIST_ERROR = "No Drive(s) are attached to the specified Controller Id: {controller_id}."
DRIVES_NOT_MATCHED = "Following Drive(s) {specified_drives} are not attached to the specified Controller Id: {controller_id}."
NEGATIVE_OR_ZERO_MSG = "The value for the `{parameter}` parameter cannot be negative or zero."
NEGATIVE_MSG = "The value for the `{parameter}` parameter cannot be negative."
INVALID_VALUE_MSG = "The value for the `{parameter}` parameter is invalid."
ID_AND_LOCATION_BOTH_DEFINED = "Either id or location is allowed."
ID_AND_LOCATION_BOTH_NOT_DEFINED = "Either id or location should be specified."
DRIVES_NOT_DEFINED = "Drives must be defined for volume creation."
NOT_ENOUGH_DRIVES = "Number of sufficient disks not found in Controller '{controller_id}'!"
WAIT_TIMEOUT_MSG = "The job is not complete after {0} seconds."
TIME_TO_WAIT_MSG = "Time to wait value is invalid. Minimum value is 300 and Maximum is 3600 seconds."
JOB_TRIGERRED = "Successfully triggered the {0} storage volume operation."
VOLUME_NAME_REQUIRED_FOR_DELETE = "Virtual disk name is a required parameter for remove virtual disk operations."
VOLUME_NOT_FOUND = "Unable to find the virtual disk."
CHANGES_NOT_FOUND = "No changes found to commit!"
CHANGES_FOUND = "Changes found to commit!"
ODATA_ID = "@odata.id"
ODATA_REGEX = "(.*?)@odata"
ATTRIBUTE = "</Attribute>"
VIEW_OPERATION_FAILED = "Failed to fetch storage details."
VIEW_CONTROLLER_DETAILS_NOT_FOUND = "Failed to find the controller {controller_id}."
VIEW_OPERATION_CONTROLLER_NOT_SPECIFIED = "Controller identifier parameter is missing."
VIEW_VIRTUAL_DISK_DETAILS_NOT_FOUND = "Failed to find the volume : {volume_id} in controller : {controller_id}."
SUCCESS_STATUS = "Success"
FAILED_STATUS = "Failed"
ERROR_CODES = ["SYS041", "SYS044", "SYS045", "SYS046", "SYS047", "SYS048", "SYS050", "SYS051", "SYS062",
               "SYS063", "SYS064", "SYS065", "SYS067", "SYS068", "SYS070", "SYS071", "SYS072",
               "SYS073", "SYS075", "SYS076", "SYS077", "SYS078", "SYS079", "SYS080"]


class StorageBase:
    def __init__(self, idrac, module):
        self.module_ext_params = self.module_extend_input(module)
        self.idrac = idrac
        self.module = module

    def data_conversion(self, module, each_volume):
        volume_related_input = [
            'volume_type', 'span_length', 'span_depth',
            'number_dedicated_hot_spare', 'disk_cache_policy',
            'write_cache_policy', 'read_cache_policy', 'stripe_size',
            'capacity', 'raid_init_operation', 'protocol', 'media_type'
        ]
        for key in volume_related_input:
            value = module.params.get(key)
            if key not in each_volume:
                each_volume[key] = value
        return each_volume

    def module_extend_input(self, module):
        """
        Extends the input module with additional volume-related parameters.

        Args:
            module (object): The module object.

        Returns:
            object: The updated module object.
        """

        module_copy = deepcopy(module.params)
        volumes = module_copy.get('volumes')
        if volumes:
            for index in range(len(volumes)):
                volumes[index] = self.data_conversion(module, volumes[index])
        else:
            tmp_volume = self.data_conversion(module, {})
            required_pd = int(module_copy.get('span_length', 1)) * int(module_copy.get('span_depth', 1))
            tmp_volume['drives'] = {'id': [(-i) for i in range(1, required_pd + 1)]}
            module_copy['volumes'] = [tmp_volume]

        int_input = ['span_length', 'span_depth', 'number_dedicated_hot_spare',
                     'stripe_size']
        if volumes:
            for each_volume in volumes:
                for each_input in each_volume:
                    if each_input in int_input:
                        each_volume[each_input] = int(each_volume[each_input])
        return module_copy

    def payload_for_disk(self, volume):
        disk_payload = ''
        if 'drives' in volume and 'id' in volume['drives']:
            for each_pd_id in volume['drives']['id']:
                scp = '<Attribute Name="IncludedPhysicalDiskID">{id}</Attribute>'.format(id=each_pd_id)
                disk_payload = disk_payload + scp
        if 'dedicated_hot_spare' in volume:
            for each_dhs in volume['dedicated_hot_spare']:
                scp = '<Attribute Name="RAIDdedicatedSpare">{id}</Attribute>'.format(id=each_dhs)
                disk_payload = disk_payload + scp
        return disk_payload

    def construct_volume_payload(self, vd_id, volume):

        """
        Constructs a payload dictionary for the given key mappings.

        Returns:
            dict: The constructed payload dictionary.
        """
        key_mapping: dict = {
            'raid_init_operation': 'RAIDinitOperation',
            'state': "RAIDaction",
            'disk_cache_policy': "DiskCachePolicy",
            'write_cache_policy': "RAIDdefaultWritePolicy",
            'read_cache_policy': "RAIDdefaultReadPolicy",
            'stripe_size': "StripeSize",
            'span_depth': "SpanDepth",
            'span_length': "SpanLength",
            'volume_type': "RAIDTypes",
            'name': 'Name',
            'capacity': 'Size',
        }
        controller_id = self.module_ext_params.get("controller_id")
        state = self.module_ext_params.get("state")
        #  Including state in each_volume as it mapped to RAIDaction
        volume.update({'state': state.capitalize()})
        payload = ''
        attr = {}
        vdfqdd = "Disk.Virtual.{0}:{1}".format(vd_id, controller_id)
        for key in volume:
            if volume[key] and key in key_mapping:
                attr[key_mapping[key]] = volume[key]
        disk_paylod = self.payload_for_disk(volume)
        payload = xml_data_conversion(attr, vdfqdd, disk_paylod)
        return payload

    def constuct_payload(self, name_id_mapping):
        number_of_existing_vd = len(name_id_mapping)
        volume_payload, attr = '', {}
        raid_reset_config_value = self.module_ext_params.get('raid_reset_config')
        raid_key_mapping = {'raid_reset_config': 'RAIDresetConfig'}
        if raid_reset_config_value == 'true':
            raid_reset_config_value = 'True'
            attr = {raid_key_mapping['raid_reset_config']: raid_reset_config_value}
        for each_volume in self.module_ext_params.get('volumes'):
            volume_payload = volume_payload + self.construct_volume_payload(number_of_existing_vd,
                                                                            each_volume)
            number_of_existing_vd = number_of_existing_vd + 1
        raid_payload = xml_data_conversion(attr, self.module_ext_params.get('controller_id'), volume_payload)
        return raid_payload

    def wait_for_job_completion(self, job_resp):
        job_wait = self.module_ext_params.get('job_wait')
        job_wait_timeout = self.module_ext_params.get('job_wait_timeout')
        job_dict = {}
        if (job_tracking_uri := job_resp.headers.get("Location")):
            job_id = job_tracking_uri.split("/")[-1]
            job_uri = iDRAC_JOB_URI.format(job_id=job_id)
            if job_wait:
                job_failed, msg, job_dict, wait_time = idrac_redfish_job_tracking(self.idrac, job_uri,
                                                                                  max_job_wait_sec=job_wait_timeout,
                                                                                  sleep_interval_secs=1)
                job_dict = remove_key(job_dict, regex_pattern=ODATA_REGEX)
                if int(wait_time) >= int(job_wait_timeout):
                    self.module.exit_json(msg=WAIT_TIMEOUT_MSG.format(job_wait_timeout), changed=True, storage_status=job_dict)
                if job_failed or job_dict.get("MessageId", "") in ERROR_CODES:
                    self.module.exit_json(msg=job_dict.get("Message"), storage_status=job_dict, failed=True)
            else:
                job_resp = self.idrac.invoke_request(job_uri, 'GET')
                job_dict = job_resp.json_data
                job_dict = remove_key(job_dict, regex_pattern=ODATA_REGEX)
                self.module.exit_json(msg=JOB_TRIGERRED.format(self.module.params.get('state')), storage_status=job_dict, changed=True)
        return job_dict


class StorageData:
    def __init__(self, idrac, module):
        self.idrac = idrac
        self.module = module

    def fetch_controllers_uri(self):
        uri, err_msg = validate_and_get_first_resource_id_uri(
            self.module, self.idrac, SYSTEMS_URI)
        if err_msg:
            self.module.exit_json(msg=err_msg, failed=True)
        storage_controllers = get_dynamic_uri(self.idrac, uri, 'Storage')
        return storage_controllers

    def fetch_api_data(self, uri, key_index_from_end):
        key = uri.split("/")[key_index_from_end]
        uri_data = self.idrac.invoke_request(uri, "GET")
        return key, uri_data

    def all_storage_data(self):
        storage_info = {"Controllers": {}}
        controllers_details_uri = self.fetch_controllers_uri()[ODATA_ID] + "?$expand=*($levels=1)"
        controllers_list = get_dynamic_uri(self.idrac, controllers_details_uri)
        for each_controller in controllers_list["Members"]:
            controller_id = each_controller.get("Id")
            if controller_id.startswith("CPU"):
                continue
            storage_info["Controllers"][controller_id] = deepcopy(each_controller)
            storage_info["Controllers"][controller_id]["Drives"] = {}
            storage_info["Controllers"][controller_id]["Volumes"] = {}
            storage_info["Controllers"][controller_id]["Links"]["Enclosures"] = {}
            # To fetch drives data
            for each_drive_uri in each_controller["Drives"]:
                key, uri_data = self.fetch_api_data(each_drive_uri[ODATA_ID], -1)
                storage_info["Controllers"][controller_id]["Drives"][key] = uri_data.json_data

            # To fetch volumes data
            volume_uri = each_controller['Volumes'][ODATA_ID]
            volumes_list = get_dynamic_uri(self.idrac, volume_uri, "Members")
            for each_volume_uri in volumes_list:
                key, uri_data = self.fetch_api_data(each_volume_uri[ODATA_ID], -1)
                storage_info["Controllers"][controller_id]["Volumes"][key] = uri_data.json_data
            # To fetch enclosures
            for each_enclosure_uri in each_controller["Links"]["Enclosures"]:
                key, uri_data = self.fetch_api_data(each_enclosure_uri[ODATA_ID], -1)
                storage_info["Controllers"][controller_id]["Links"]["Enclosures"][key] = uri_data.json_data
        return storage_info

    def fetch_storage_data(self):
        storage_info = {"Controller": {}}
        storage_data = self.all_storage_data()
        firm_ver = get_idrac_firmware_version(self.idrac)
        for controller_id, controller_data in storage_data["Controllers"].items():
            storage_info["Controller"][controller_id] = {
                "ControllerSensor": {controller_id: {}}
            }
            if firm_ver >= "3.00":
                battery_data = controller_data["Oem"]["Dell"].get("DellControllerBattery")
                if battery_data:
                    storage_info["Controller"][controller_id]["ControllerSensor"][controller_id]["ControllerBattery"] = [battery_data["Id"]]
            self.fetch_volumes(controller_id, controller_data, storage_info)
            self.fetch_enclosures_and_physical_disk(controller_id, controller_data, storage_info)
        return storage_info

    def fetch_volumes(self, controller_id, controller_data, storage_info):
        if controller_data["Volumes"]:
            storage_info.setdefault("Controller", {}).setdefault(controller_id, {})["VirtualDisk"] = {}
            for volume_id, volume_data in controller_data["Volumes"].items():
                physical_disk = [self.fetch_api_data(drive[ODATA_ID], -1)[0] for drive in volume_data["Links"]["Drives"]]
                storage_info["Controller"][controller_id]["VirtualDisk"][volume_id] = {"PhysicalDisk": physical_disk}

    def fetch_enclosures_and_physical_disk(self, controller_id, controller_data, storage_info):
        enclosures = [enclosure_id for enclosure_id in controller_data["Links"]["Enclosures"].keys() if enclosure_id.startswith("Enclosure")]
        if len(enclosures) >= 1:
            storage_info.setdefault("Controller", {})
            storage_info["Controller"].setdefault(controller_id, {})
            storage_info["Controller"][controller_id].setdefault("Enclosure", {})
            for enclosure_id in enclosures:
                storage_info["Controller"][controller_id]["Enclosure"][enclosure_id] = {"EnclosureSensor": {enclosure_id: {}}}
                physical_disk = [self.fetch_api_data(drive[ODATA_ID], -1)[0] for drive in
                                 controller_data["Links"]["Enclosures"][enclosure_id]["Links"]["Drives"]]
                if physical_disk:
                    storage_info["Controller"][controller_id]["Enclosure"][enclosure_id]["PhysicalDisk"] = physical_disk
        else:
            if controller_data["Drives"].keys():
                storage_info["Controller"][controller_id]["PhysicalDisk"] = list(controller_data["Drives"].keys())


class StorageValidation(StorageBase):
    def __init__(self, idrac, module):
        super().__init__(idrac, module)
        self.idrac_data = StorageData(idrac, module).all_storage_data()
        self.controller_id = module.params.get("controller_id")

    def validate_time_to_wait(self):
        to_wait = self.module_ext_params.get("time_to_wait")
        if to_wait < 300 or to_wait > 3600:
            self.module.exit_json(msg=TIME_TO_WAIT_MSG, failed=True)

    def validate_controller_exists(self):
        if not self.controller_id:
            self.module.exit_json(msg=CONTROLLER_NOT_DEFINED, failed=True)
        controllers = self.idrac_data["Controllers"]
        if self.controller_id not in controllers.keys():
            self.module.exit_json(msg=CONTROLLER_NOT_EXIST_ERROR.format(controller_id=self.controller_id), failed=True)

    def validate_job_wait_negative_values(self):
        if self.module_ext_params.get("job_wait") and self.module_ext_params.get("job_wait_timeout") <= 0:
            self.module.exit_json(msg=NEGATIVE_OR_ZERO_MSG.format(parameter="job_wait_timeout"), failed=True)

    def validate_negative_values_for_volume_params(self, each_volume):
        inner_params = ["span_depth", "span_length", "capacity", "strip_size"]
        for param in inner_params:
            value = each_volume.get(param)
            if value is not None and value <= 0:
                self.module.exit_json(msg=NEGATIVE_OR_ZERO_MSG.format(parameter=param), failed=True)
        if each_volume.get("number_dedicated_hot_spare") < 0:
            self.module.exit_json(msg=NEGATIVE_MSG.format(parameter="number_dedicated_hot_spare"), failed=True)

    def validate_volume_drives(self, specified_volume):
        specified_drives = specified_volume.get("drives")
        if not specified_drives:
            self.module.exit_json(msg=DRIVES_NOT_DEFINED, failed=True)
        if specified_drives.get("id") and specified_drives.get("location"):
            self.module.exit_json(msg=ID_AND_LOCATION_BOTH_DEFINED, failed=True)
        elif "id" not in specified_drives and "location" not in specified_drives:
            self.module.exit_json(msg=ID_AND_LOCATION_BOTH_NOT_DEFINED, failed=True)
        drives_count = len(specified_drives.get("location")) if specified_drives.get("location") is not None else len(specified_drives.get("id"))
        return self.raid_std_validation(specified_volume.get("span_length"),
                                        specified_volume.get("span_depth"),
                                        specified_volume.get("volume_type"),
                                        drives_count)

    def raid_std_validation(self, span_length, span_depth, volume_type, pd_count):
        raid_std = {
            "RAID 0": {'pd_slots': range(1, 2), 'span_length': 1, 'checks': operator.ge, 'span_depth': 1},
            "RAID 1": {'pd_slots': range(1, 3), 'span_length': 2, 'checks': operator.eq, 'span_depth': 1},
            "RAID 5": {'pd_slots': range(1, 4), 'span_length': 3, 'checks': operator.ge, 'span_depth': 1},
            "RAID 6": {'pd_slots': range(1, 5), 'span_length': 4, 'checks': operator.ge, 'span_depth': 1},
            "RAID 10": {'pd_slots': range(1, 5), 'span_length': 2, 'checks': operator.ge, 'span_depth': 2},
            "RAID 50": {'pd_slots': range(1, 7), 'span_length': 3, 'checks': operator.ge, 'span_depth': 2},
            "RAID 60": {'pd_slots': range(1, 9), 'span_length': 4, 'checks': operator.ge, 'span_depth': 2}
        }
        raid_info = raid_std.get(volume_type)
        if not raid_info.get('checks')(span_length, raid_info.get('span_length')):
            self.module.exit_json(msg=INVALID_VALUE_MSG.format(parameter="span_length"), failed=True)
        if volume_type in ["RAID 0", "RAID 1", "RAID 5", "RAID 6"] and operator.ne(span_depth, raid_info.get('span_depth')):
            self.module.exit_json(msg=INVALID_VALUE_MSG.format(parameter="span_depth"), failed=True)
        if volume_type in ["RAID 10", "RAID 50", "RAID 60"] and operator.lt(span_depth, raid_info.get('span_depth')):
            self.module.exit_json(msg=INVALID_VALUE_MSG.format(parameter="span_depth"), failed=True)
        if not operator.eq(pd_count, span_depth * span_length):
            self.module.exit_json(msg=INVALID_VALUE_MSG.format(parameter="drives"), failed=True)
        return True


class StorageCreate(StorageValidation):
    def disk_slot_location_to_id_conversion(self, each_volume):
        drives = {}
        if "location" in each_volume['drives']:
            regex_pattern = r"\d+"
            physical_disk = self.idrac_data["Controllers"][self.controller_id]["Drives"]
            slot_id_mapping = {int(re.search(regex_pattern, key).group()): key for key in physical_disk.keys()}
            drives['id'] = [slot_id_mapping.get(each_pd) for each_pd in each_volume['drives']['location']
                            if slot_id_mapping.get(each_pd)]
        elif "id" in each_volume['drives']:
            drives['id'] = each_volume['drives']['id']
        return drives

    def perform_intersection_on_disk(self, each_volume, healthy_disk, available_disk,
                                     media_type_supported_disk, protocol_supported_disk):
        filtered_disk = healthy_disk
        firm_ver = get_idrac_firmware_version(self.idrac)
        if firm_ver >= "3.00":
            filtered_disk = filtered_disk.intersection(available_disk)
        if filtered_disk and each_volume.get('media_type'):
            filtered_disk = filtered_disk.intersection(media_type_supported_disk)
        if filtered_disk and each_volume.get('protocol'):
            filtered_disk = filtered_disk.intersection(protocol_supported_disk)
        return sorted(list(filtered_disk))

    def filter_disk(self, each_volume):
        disk_dict = self.idrac_data["Controllers"][self.controller_id]["Drives"]
        healthy_disk = set()
        available_disk = set()
        media_type_supported_disk = set()
        protocol_supported_disk = set()
        raid_reset_config_value = self.module_ext_params.get('raid_reset_config')
        raid_status_list = ["Ready", "NonRAID"]
        if raid_reset_config_value == "true":
            raid_status_list.append("Online")
        for key, value in disk_dict.items():
            if each_volume.get('media_type') and value.get('MediaType') == each_volume.get('media_type'):
                media_type_supported_disk.add(key)
            if each_volume.get('protocol') and value.get('Protocol') == each_volume.get('protocol'):
                protocol_supported_disk.add(key)
            status = value.get('Status', {}).get('Health', {})
            if status == "OK":
                healthy_disk.add(key)
            raid_status = value.get('Oem', {}).get('Dell', {}).get('DellPhysicalDisk', {}).get('RaidStatus', {})
            if raid_status in raid_status_list:
                available_disk.add(key)
        return self.perform_intersection_on_disk(each_volume, healthy_disk, available_disk,
                                                 media_type_supported_disk, protocol_supported_disk)

    def updating_drives_module_input_when_given(self, each_volume, filter_disk_output):
        updated_disk_id_list = []
        if 'id' in each_volume['drives']:
            for each_pd in each_volume['drives']['id']:
                if each_pd in filter_disk_output:
                    updated_disk_id_list.append(each_pd)
        return updated_disk_id_list

    def updating_volume_module_input_for_hotspare(self, each_volume, filter_disk_output, reserved_pd, drives_exists_in_id):
        tmp_list = []
        if 'number_dedicated_hot_spare' in each_volume and each_volume['number_dedicated_hot_spare'] > 0:
            for each_pd in filter_disk_output:
                if each_pd not in reserved_pd and each_pd not in drives_exists_in_id:
                    tmp_list.append(each_pd)
                if len(tmp_list) == each_volume['number_dedicated_hot_spare']:
                    break
        return tmp_list

    def updating_volume_module_input(self, drives_exists_in_id):
        volumes = self.module_ext_params.get('volumes', [])
        reserved_pd = []
        for each in volumes:
            required_pd = int(each['span_depth']) * int(each['span_length'])
            filtered_disk = self.filter_disk(each)
            if 'stripe_size' in each:
                each['stripe_size'] = int(each['stripe_size'] / 512)

            if each.get('capacity') is not None:
                each['capacity'] = str(int(float(each['capacity']) * 1073741824))

            if self.module.params.get('volumes') is None:
                each['drives']['id'] = filtered_disk[:required_pd]

            if 'drives' in each:
                drives_id_list = self.updating_drives_module_input_when_given(each, filtered_disk)
                reserved_pd += drives_id_list
                each['drives']['id'] = drives_id_list

            if 'number_dedicated_hot_spare' in each:
                hotspare_disk_list = self.updating_volume_module_input_for_hotspare(each, filtered_disk, reserved_pd,
                                                                                    drives_exists_in_id)
                reserved_pd += hotspare_disk_list
                each['dedicated_hot_spare'] = hotspare_disk_list
            self.validate_enough_drives_available(each)
        if self.module.check_mode:
            self.module.exit_json(msg=CHANGES_FOUND, changed=True)
        self.module_ext_params['volumes'] = volumes

    def validate_enough_drives_available(self, each_volume):
        controller_id = self.module_ext_params.get('controller_id')
        required_pd = each_volume['span_depth'] * each_volume['span_length']
        drives_available = each_volume['drives']['id']
        dedicated_hot_spare_required = int(each_volume['number_dedicated_hot_spare'])
        dedicated_hot_spare_available = len(each_volume['dedicated_hot_spare'])
        changed, failed = False, False
        if (required_pd > len(drives_available) or dedicated_hot_spare_required != dedicated_hot_spare_available):
            if not self.module.check_mode:
                msg, failed = NOT_ENOUGH_DRIVES.format(controller_id=controller_id), True
            else:
                msg, changed = CHANGES_NOT_FOUND, False
            self.module.exit_json(msg=msg, changed=changed, failed=failed)

    def validate(self):
        #  Validate upper layer input
        self.validate_time_to_wait()
        self.validate_controller_exists()
        self.validate_job_wait_negative_values()
        #  Validate std raid validation for inner layer
        drives_exists_in_id = []
        for each_volume in self.module_ext_params.get('volumes', []):
            #  Validatiing for negative values
            self.validate_negative_values_for_volume_params(each_volume)
            self.validate_volume_drives(each_volume)
            if 'location' in each_volume['drives'] and each_volume['drives']['location']:
                each_volume['drives'] = self.disk_slot_location_to_id_conversion(each_volume)
            drives_exists_in_id += each_volume['drives']['id']
        #  Extendeding volume module input in module_ext_params for drives id and hotspare
        self.updating_volume_module_input(drives_exists_in_id)

    def execute(self):
        self.validate()
        job_dict = {}
        name_id_mapping = {value.get('Name'): key for key, value in self.idrac_data["Controllers"][self.controller_id]["Volumes"].items()}
        parent_payload = """<SystemConfiguration>{0}</SystemConfiguration>"""
        payload = self.constuct_payload(name_id_mapping)
        parent_payload = parent_payload.format(payload)
        resp = self.idrac.import_scp(import_buffer=parent_payload, target=["RAID"], job_wait=False, time_to_wait=self.module.params.get('time_to_wait'))
        job_dict = self.wait_for_job_completion(resp)
        return job_dict


class StorageDelete(StorageValidation):
    def check_even_single_given_volume_exists(self, volume_name_input_list):
        for each_name in volume_name_input_list:
            for cntrl_id, detail in self.idrac_data.get('Controllers').items():
                for vol_id, volume in detail.get('Volumes').items():
                    if each_name == volume.get('Name'):
                        return True

    def validate_volume_exists_in_server(self, volume_name_input_list):
        changed, failed = False, False
        single_volume_name_matched = self.check_even_single_given_volume_exists(volume_name_input_list)
        if single_volume_name_matched:
            if self.module.check_mode:
                msg, changed = CHANGES_FOUND, True
            else:
                return
        else:
            msg, failed = VOLUME_NOT_FOUND, True
        self.module.exit_json(msg=msg, failed=failed, changed=changed)

    def validate(self):
        #  Validate upper layer input
        self.validate_time_to_wait()
        self.validate_job_wait_negative_values()

        #  Validate for volume and volume_name
        if (not (volumes := self.module.params.get('volumes'))) or (volumes and not all("name" in each for each in volumes)):
            self.module.exit_json(msg=VOLUME_NAME_REQUIRED_FOR_DELETE, failed=True)

    def construct_payload_for_delete(self, cntrl_id_vd_id_mapping):
        parent_payload = """<SystemConfiguration>{0}</SystemConfiguration>"""
        raid_payload = ""
        for each_controller, value in cntrl_id_vd_id_mapping.items():
            volume_payload = ""
            for each_value in value:
                volume_payload += xml_data_conversion({'RAIDaction': 'Delete'}, each_value)
            raid_payload += xml_data_conversion({}, each_controller, volume_payload)
        parent_payload = parent_payload.format(raid_payload)
        return parent_payload

    def get_vd_id_based_on_controller_id_vd_name(self, user_volume_input_list):
        cntrl_id_vd_id_mapping = {}
        for cntrl_id, detail in self.idrac_data.get('Controllers').items():
            for vd_id, volume in detail.get('Volumes').items():
                if volume.get('Name') in user_volume_input_list:
                    if cntrl_id not in cntrl_id_vd_id_mapping:
                        cntrl_id_vd_id_mapping[cntrl_id] = [vd_id]
                    else:
                        cntrl_id_vd_id_mapping[cntrl_id].append(vd_id)
        return cntrl_id_vd_id_mapping

    def execute(self):
        self.validate()
        job_dict = {}
        volume_name_input_list = [each.get('name') for each in self.module.params.get('volumes')]
        self.validate_volume_exists_in_server(set(volume_name_input_list))
        cntrl_id_vd_id_mapping = self.get_vd_id_based_on_controller_id_vd_name(set(volume_name_input_list))
        payload = self.construct_payload_for_delete(cntrl_id_vd_id_mapping)
        resp = self.idrac.import_scp(import_buffer=payload, target=["RAID"], job_wait=False, time_to_wait=self.module.params.get('time_to_wait'))
        job_dict = self.wait_for_job_completion(resp)
        return job_dict


class StorageView(StorageData):
    def __init__(self, idrac, module):
        super().__init__(idrac, module)

    def execute(self):
        status = SUCCESS_STATUS
        storage_data = self.fetch_storage_data()
        controller_id = self.module.params.get("controller_id")
        volume_id = self.module.params.get("volume_id")
        if volume_id:
            status, storage_data = self.process_volume_id(volume_id, controller_id, storage_data)
        elif controller_id:
            status, storage_data = self.process_controller_id(controller_id, storage_data)
        return {"Message": storage_data, "Status": status}

    def process_volume_id(self, volume_id, controller_id, storage_data):
        status = SUCCESS_STATUS
        if controller_id:
            ctrl_data = storage_data["Controller"].get(controller_id)
            if ctrl_data:
                virtual_disk = ctrl_data.get("VirtualDisk")
                if not virtual_disk or volume_id not in virtual_disk:
                    status = FAILED_STATUS
                    message = VIEW_VIRTUAL_DISK_DETAILS_NOT_FOUND.format(volume_id=volume_id, controller_id=controller_id)
                    self.module.exit_json(msg=VIEW_OPERATION_FAILED,
                                          storage_status={"Message": message, "Status": status},
                                          failed=True)
                else:
                    storage_data[controller_id] = {"VirtualDisk": ctrl_data["VirtualDisk"]}
                    del storage_data["Controller"]
            else:
                status = FAILED_STATUS
                message = VIEW_CONTROLLER_DETAILS_NOT_FOUND.format(controller_id=controller_id)
                self.module.exit_json(msg=VIEW_OPERATION_FAILED,
                                      storage_status={"Message": message, "Status": status},
                                      failed=True)
        else:
            status = FAILED_STATUS
            message = VIEW_OPERATION_CONTROLLER_NOT_SPECIFIED
            self.module.exit_json(msg=VIEW_OPERATION_FAILED,
                                  storage_status={"Message": message, "Status": status},
                                  failed=True)
        return status, storage_data

    def process_controller_id(self, controller_id, storage_data):
        status = SUCCESS_STATUS
        ctrl_data = storage_data["Controller"].get(controller_id)
        if ctrl_data:
            storage_data[controller_id] = ctrl_data
            del storage_data["Controller"]
        else:
            status = FAILED_STATUS
            message = VIEW_CONTROLLER_DETAILS_NOT_FOUND.format(controller_id=controller_id)
            self.module.exit_json(msg=VIEW_OPERATION_FAILED,
                                  storage_status={"Message": message, "Status": status},
                                  failed=True)
        return status, storage_data


def main():
    specs = {
        "state": {"choices": ['create', 'delete', 'view'], "default": 'view'},
        "volume_id": {"type": 'str'},
        "volumes": {"type": 'list', "elements": 'dict'},
        "span_depth": {"type": 'int', "default": 1},
        "span_length": {"type": 'int', "default": 1},
        "number_dedicated_hot_spare": {"type": 'int', "default": 0},
        "volume_type": {"choices": ['RAID 0', 'RAID 1', 'RAID 5', 'RAID 6', 'RAID 10', 'RAID 50', 'RAID 60'],
                        "default": 'RAID 0'},
        "disk_cache_policy": {"choices": ["Default", "Enabled", "Disabled"],
                              "default": "Default"},
        "write_cache_policy": {"choices": ["WriteThrough", "WriteBack", "WriteBackForce"],
                               "default": "WriteThrough"},
        "read_cache_policy": {"choices": ["NoReadAhead", "ReadAhead", "AdaptiveReadAhead"],
                              "default": "NoReadAhead"},
        "stripe_size": {"type": 'int', "default": 64 * 1024},
        "capacity": {"type": 'float'},
        "controller_id": {"type": 'str'},
        "media_type": {"choices": ['HDD', 'SSD']},
        "protocol": {"choices": ['SAS', 'SATA', 'PCIE']},
        "raid_reset_config": {"choices": ['true', 'false'], "default": 'false'},
        "raid_init_operation": {"choices": ['None', 'Fast']},
        "job_wait": {"type": "bool", "default": True},
        "job_wait_timeout": {"type": "int", "default": 900},
        "time_to_wait": {"type": "int", "default": 300}
    }

    module = IdracAnsibleModule(
        argument_spec=specs,
        supports_check_mode=True)
    try:
        with iDRACRedfishAPI(module.params) as idrac:
            changed = False
            state_class_mapping = {
                'create': StorageCreate,
                'view': StorageView,
                'delete': StorageDelete,
            }
            state_type = state_class_mapping.get(module.params['state'])
            obj = state_type(idrac, module)
            output = obj.execute()
            msg = SUCCESSFUL_OPERATION_MSG.format(operation=module.params['state'])
            changed = True if module.params['state'] in ['create', 'delete'] else False
            module.exit_json(msg=msg, changed=changed, storage_status=output)
    except HTTPError as err:
        import json
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
