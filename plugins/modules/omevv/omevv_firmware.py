#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.10.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: omevv_firmware
short_description: Update the firmware of a specific host in the cluster
version_added: "9.10.0"
description: This module allows you to update the firmware of a specific host in the cluster.
extends_documentation_fragment:
  - dellemc.openmanage.omevv_auth_options
options:
  check_vSAN_health:
    description:
      - Check vSAN health while updating the firmware.
      - C(true) checks the vSAN health while updating the firmware.
      - C(false) does not check the vSAN health while updating the firmware.
    type: bool
  date_time:
    description:
      - Date and time when the job must run. This is applicable when I(run_now) is C(false).
      - The supported format is YYYY-MM-DDThh:mm:ss<offset>.
    type: str
  delete_job_queue:
    description:
      - Whether to delete the job queue in iDRAC while updating firmware.
      - C(true) deletes the job queue in iDRAC while updating firmware.
      - C(false) does not delete the job queue in iDRAC while updating firmware.
    type: bool
  drs_check:
    description:
      - Allows you to check if DRS of the cluster is enabled or not.
      - C(true) checks if Distributed Resource Scheduler (DRS) of the cluster is enabled.
      - C(false) does not check if DRS of the cluster is enabled.
    type: bool
    default: false
  enter_maintenance_mode_options:
    description:
      - VM migration policy during management mode.
      - C(FULL_DATA_MIGRATION) for full data migration.
      - C(ENSURE_ACCESSIBILITY) for ensuring accessibility.
      - C(NO_DATA_MIGRATION) does not migrate any data.
    type: str
    choices: [FULL_DATA_MIGRATION, ENSURE_ACCESSIBILITY, NO_DATA_MIGRATION]
  enter_maintenance_mode_timeout:
    description:
      - Time out value during maintenance mode in minutes.
    type: int
    default: 60
  evacuate_VMs:
    description:
      - Allows to move the virtual machine (VM) to other host when current host is powered off.
      - C(true) moves the VM to another host when the current host is powered off.
      - C(false) does not move the VM to another host when the current host is powered off.
    type: bool
    default: false
  exit_maintenance_mode:
    description:
      - Whether to exit management mode after Update.
      - C(true) exits the management mode after Update.
      - C(false) does not exit the management mode after Update.
    type: bool
    default: false
  job_description:
    description:
      - Update job description.
    type: str
  job_name:
    description:
      - Update job name.
    type: str
  job_wait:
    description:
      - Whether to wait till completion of the job. This is applicable when I(power_on) is C(true).
      - C(true) waits for job completion.
      - C(false) does not wait for job completion.
    type: bool
    default: true
  job_wait_timeout:
    description:
      - The maximum wait time of I(job_wait) in seconds. The job is tracked only for this duration.
      - This option is applicable when I(job_wait) is C(true).
    type: int
    default: 1200
  maintenance_mode_count_check:
    description:
      - Allows to check if any host in cluster is in management mode.
      - C(true) checks if any host in cluster is in management mode.
      - C(false) does not check if any host in cluster is in management mode.
    type: bool
  reboot_options:
    description:
      - Host reboot option for firmware update.
      - C(FORCEREBOOT) will force reboot the server.
      - C(SAFEREBOOT) reboots the server in safe mode.
      - C(NEXTREBOOT) does not reboot the server.
    type: str
    choices: [FORCEREBOOT, SAFEREBOOT, NEXTREBOOT]
    default: SAFEREBOOT
  reset_idrac:
    description:
      - Whether to reset the iDRAC while performing firmware update.
      - C(true) resets the iDRAC while performing firmware update.
      - C(false) does not reset the iDRAC while performing firmware update.
    type: bool
  run_now:
    description:
      - Whether to run the update job now or later.
      - C(true) runs the update job instantly.
      - C(false) runs the update at the specified I(date_time).
    type: bool
    required: true
  targets:
    description:
      - The target details for the firmware update operation.
      - Either I(cluster), I(servicetag) or I(host) is required for the firmware update operation.
    type: list
    elements: dict
    required: true
    suboptions:
      cluster:
        description:
          - Name of the cluster to which firmware needs to updated.
          - I(cluster) is mutually exclusive with I(servicetag) and I(host).
        type: str
        required: false
      firmware_components:
        description:
          - List of host firmware components to update.
          - M(dellemc.openmanage.omevv_firmware_compliance_info) module can
            be used to fetch the supported firmware components.
        type: list
        elements: str
        required: true
      host:
        description:
          - The IP address or hostname of the host.
          - I(host) is mutually exclusive with I(servicetag) and I(cluster).
          - M(dellemc.openmanage.omevv_device_info) module can be used to fetch the device
            information.
        type: str
      servicetag:
        description:
          - The service tag of the host.
          - I(servicetag) is mutually exclusive with I(host) and I(cluster).
          - M(dellemc.openmanage.omevv_device_info) module can be used to fetch the
            device information.
        type: str
requirements:
  - "python >= 3.9.6"
author:
  - "Rajshekar P(@rajshekarp87)"
attributes:
    check_mode:
        description: Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.
        support: full
    diff_mode:
        description: Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode.
        support: full
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
    - This module supports IPv4 and IPv6 addresses.
"""

EXAMPLES = r"""
---
- name: Immediately update the firmware of a single component for a specific host
  dellemc.openmanage.omevv.omevv_firmware:
    hostname: "192.168.0.1"
    vcenter_uuid: "xxxxx"
    vcenter_username: "username"
    vcenter_password: "password"
    ca_path: "path/to/ca_file"
    run_now: false
    date_time: "2024-09-10T20:50:00Z"
    enter_maintenance_mode_timeout: 60
    enter_maintenance_mode_options: FULL_DATA_MIGRATION
    drs_check: true
    evacuate_VMs: true
    exit_maintenance_mode: true
    reboot_options: NEXTREBOOT
    maintenance_mode_count_check: true
    check_vSAN_health: true
    reset_idrac: true
    delete_job_queue: true
    targets:
      - servicetag: SVCTAG1
        firmware_components:
          - "DCIM:INSTALLED#802__Diagnostics.Embedded.1:LC.Embedded.1"

- name: Update the firmware of multiple components at scheduled time for a specific host
  dellemc.openmanage.omevv.omevv_firmware:
    hostname: "192.168.0.1"
    vcenter_uuid: "xxxxx"
    vcenter_username: "username"
    vcenter_password: "password"
    ca_path: "path/to/ca_file"
    run_now: false
    date_time: "2024-09-10T20:50:00+05:30"
    enter_maintenance_mode_timeout: 60
    enter_maintenance_mode_options: ENSURE_ACCESSIBILITY
    drs_check: true
    evacuate_VMs: true
    exit_maintenance_mode: true
    reboot_options: FORCEREBOOT
    maintenance_mode_count_check: true
    check_vSAN_health: true
    reset_idrac: false
    delete_job_queue: false
    targets:
      - host: 192.168.0.2
        firmware_components:
          - "DCIM:INSTALLED#iDRAC.Embedded.1-1#IDRACinfo"
          - "DCIM:INSTALLED#301_C_BOSS.SL.14-1"
          - "DCIM:INSTALLED#807__TPM.Integrated.1-1"

- name: Retrieve firmware compliance report of all the hosts in the specific cluster
  dellemc.openmanage.omevv_firmware_compliance_info:
    hostname: "192.168.0.1"
    vcenter_uuid: "xxxxx"
    vcenter_username: "username"
    vcenter_password: "password"
    ca_path: "path/to/ca_file"
    clusters:
      - cluster_name: cluster_a
  register: compliance_data

- name: Extract source name of all components
  set_fact:
    source_names: "{{ compliance_data.hostComplianceReports[0].componentCompliances|json_query('*.sourceName') }}"

- name: Extract source name of a specific component
  set_fact:
    source_name: "{{ compliance_data.hostComplianceReports[0].componentCompliances[0].sourceName }}"

- name: Update firmware at the scheduled time for a specific host
  dellemc.openmanage.omevv.omevv_firmware:
    hostname: "192.168.0.1"
    vcenter_uuid: "xxxxx"
    vcenter_username: "username"
    vcenter_password: "password"
    ca_path: "path/to/ca_file"
    run_now: false
    date_time: "2024-09-10T20:50:00Z"
    enter_maintenance_mode_timeout: 60
    enter_maintenance_mode_options: NO_DATA_MIGRATION
    drs_check: true
    evacuate_VMs: false
    exit_maintenance_mode: true
    reboot_options: SAFEREBOOT
    maintenance_mode_count_check: true
    check_vSAN_health: true
    reset_idrac: true
    delete_job_queue: true
    targets:
      - servicetag: SVCTAG1
        firmware_components:
          - "{{ source_name }}"
"""

RETURN = r'''
---
msg:
  type: str
  description: Status of the firmware update operation.
  returned: always
  sample: "Successfully created the OMEVV baseline profile."
error_info:
  description: Details of the module HTTP Error.
  returned: on HTTP error
  type: dict
  sample:
    {
        "errorCode": "20058",
        "message": "Update Job already running for group id 1004 corresponding to cluster OMAM-Cluster-1. Wait for its completion and trigger."
    }
'''

import json
import time
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv import RestOMEVV, OMEVVAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import validate_job_wait
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv_utils.omevv_firmware_utils import OMEVVFirmwareUpdate, OMEVVBaselineProfile
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv_utils.omevv_info_utils import OMEVVInfo
from datetime import datetime

SUCCESS_UPDATE_SUBMIT_MSG = "Successfully submitted the firmware updated job."
SUCCESS_UPDATE_MSG = "Successfully completed the firmware update."
SUCCESS_UPDATE_SCHEDULED_MSG = "Successfully scheduled the firmware update job."
FAILED_UPDATE_MSG = "Failed to complete the firmware update."
INVALID_DATE_TIME_MSG = "Invalid date time. Enter a valid date time in the format of " \
                        "YYYY-MM-DDTHH:MM:SSZ."
MAINTENANCE_MODE_TIMEOUT_INVALID_MSG = "The value for the 'enter_maintenance_mode_timeout' " \
                                       "parameter must be between 60 and 1440."
CLUSTER_HOST_SERVICETAG_MUTUAL_EXCLUSIVE_MSG = "parameters are mutually " \
                                               "exclusive: cluster|host|servicetag."
CLUSTER_HOST_SERVICETSAG_REQUIRED_MSG = "Either 'cluster' or 'host' or 'servicetag' must " \
                                        "be specified."
UPDATE_JOB_PRESENT_MSG = "Update Job already running for cluster {cluster_name}. Wait for its " \
                         "completion and trigger."
JOB_NAME_ALREADY_EXISTS_MSG = "Job with name {job_name} already exists. Provide different name."
CLUSTER_HOST_NOT_FOUND_MSG = "No managed hosts found in the cluster."
HOST_NOT_FOUND_MSG = "Host not found under managed hosts."
CHANGES_FOUND_MSG = "Changes found to be applied."
CHANGES_NOT_FOUND_MSG = "No changes found to be applied."
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The value for the 'job_wait_timeout' parameter cannot be " \
                               "negative or zero."
UNREACHABLE_MSG = "The URL with the {ip}:{port} cannot be reached."
SOURCE_NOT_FOUND_MSG = "The Requested resource cannot be found."
TRIGGER_UPDATE_CHECK_URI = "/Consoles/{vcenter_uuid}/CanTriggerUpdate"


class FirmwareUpdate():

    def __init__(self, module, rest_obj):
        self.module = module
        self.obj = rest_obj
        self.omevv_info_obj = OMEVVInfo(self.obj)
        self.omevv_update_obj = OMEVVFirmwareUpdate(self.obj)
        self.omevv_baseline_obj = OMEVVBaselineProfile(self.obj)

    def execute(self):
        """
        Executes the function with the given module.
        :param module: The module to execute.
        :type module: Any
        :return: None
        """

    def get_payload_details(self, host_id):
        """
        Retrieves the payload details for the firmware update.

        Args:
            host_id (str): The ID of the host.

        Returns:
            dict: The payload details for the firmware update.
        """
        device_id = host_id
        parameters = self.module.params
        target_list = parameters['targets']
        payload = {"firmware": {"targets": []}}
        firmware = payload["firmware"]

        self.add_optional_fields(firmware, parameters)
        self.set_schedule(payload, parameters)
        self.set_job_details(payload, parameters)
        self.add_targets(firmware, target_list, device_id)

        return payload

    def add_optional_fields(self, firmware, parameters):
        optional_fields = [
            ('check_vSAN_health', 'checkvSANHealth'),
            ('delete_job_queue', 'deleteJobsQueue'),
            ('drs_check', 'drsCheck'),
            ('enter_maintenance_mode_options', 'enterMaintenanceModeOption'),
            ('enter_maintenance_mode_timeout', 'enterMaintenanceModetimeout'),
            ('evacuate_VMs', 'evacuateVMs'),
            ('exit_maintenance_mode', 'exitMaintenanceMode'),
            ('maintenance_mode_count_check', 'maintenanceModeCountCheck'),
            ('reboot_options', 'rebootOptions'),
            ('reset_idrac', 'resetIDrac'),
        ]

        for param_key, firmware_key in optional_fields:
            if parameters.get(param_key) is not None:
                firmware[firmware_key] = parameters.get(param_key)

    def set_schedule(self, payload, parameters):
        payload["schedule"] = {"runNow": parameters.get('run_now')}

        if not payload["schedule"]["runNow"]:
            payload["schedule"]["dateTime"] = parameters.get('date_time')

    def set_job_details(self, payload, parameters):
        if parameters.get('job_description'):
            payload["jobDescription"] = parameters.get('job_description')

        if parameters.get('job_name'):
            payload["jobName"] = parameters.get('job_name')
        else:
            date_time = datetime.now()
            job_name = (
                f"omam_firmware_update_job_{date_time.year}{date_time.month:02}{date_time.day:02}_"
                f"{date_time.hour:02}{date_time.minute:02}{date_time.second:02}")
            payload["jobName"] = job_name

    def add_targets(self, firmware, target_list, device_id):
        for target in target_list:
            if isinstance(device_id, list):
                # If device_id is a list, iterate through each id and add to the targets
                for single_device_id in device_id:
                    actual_target = {
                        "firmwarecomponents": target['firmware_components'],
                        "id": single_device_id
                    }
                    firmware['targets'].append(actual_target)
            else:
                # If device_id is a single string, add it directly to the targets
                actual_target = {
                    "firmwarecomponents": target['firmware_components'],
                    "id": device_id
                }
                firmware['targets'].append(actual_target)

    def host_servicetag_existence(self):
        for target in self.module.params.get('targets', []):
            cluster = target.get('cluster')
            host = target.get('host')
            servicetag = target.get('servicetag')

            if (host and servicetag) or (host and cluster) or (servicetag and cluster):
                self.module.exit_json(msg=CLUSTER_HOST_SERVICETAG_MUTUAL_EXCLUSIVE_MSG,
                                      failed=True)
            if not host and not servicetag and not cluster:
                self.module.exit_json(msg=CLUSTER_HOST_SERVICETSAG_REQUIRED_MSG, failed=True)
        return True

    def validate_date_time(self):
        try:
            ftime = datetime.strptime(self.module.params.get('date_time'), "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            self.module.exit_json(msg=INVALID_DATE_TIME_MSG, failed=True)
        return ftime

    def enter_maintenance_mode_timeout(self):
        enter_maintenance_mode_timeout = self.module.params.get('enter_maintenance_mode_timeout')
        if enter_maintenance_mode_timeout < 60 or enter_maintenance_mode_timeout > 1440:
            self.module.exit_json(msg=MAINTENANCE_MODE_TIMEOUT_INVALID_MSG, failed=True)

    def validate_params(self):

        # Validate the 'host' and 'servicetag' parameter existence
        self.host_servicetag_existence()

        # Validate the job_wait parameter
        if validate_job_wait(self.module):
            self.module.exit_json(msg=TIMEOUT_NEGATIVE_OR_ZERO_MSG, failed=True)

        # Validate the date_time parameter
        if self.module.params.get('date_time'):
            self.validate_date_time()

        # Validate the enter_maintenance_mode_timeout parameter
        if self.module.params.get('enter_maintenance_mode_timeout'):
            self.enter_maintenance_mode_timeout()


class UpdateCluster(FirmwareUpdate):

    def execute(self):
        cluster_name = None
        cluster_group_id = None
        host_service_tags = None
        new_host_id = None
        payload = None
        before_dict = {}
        after_dict = {}
        diff_before = json.dumps(before_dict)
        diff_after = json.dumps(after_dict)
        self.validate_params()
        vcenter_uuid = self.module.params.get('vcenter_uuid')
        parameters = self.module.params

        target = self.get_target(parameters['targets'])

        if target['cluster']:
            host_ids, host_service_tags = self.get_host_id(vcenter_uuid, target)
            if host_ids is None or not host_ids:
                self.module.exit_json(msg=CLUSTER_HOST_NOT_FOUND_MSG, failed=True)
            else:
                cluster_name = target['cluster']
                cluster_group_id = self.omevv_info_obj.get_group_id_of_cluster(vcenter_uuid, cluster_name)
                payload = self.get_payload_details(host_id=host_ids)
                new_host_id = host_ids

        else:
            host_id, host_service_tags = self.get_host_from_parameters(vcenter_uuid, parameters)
            if host_id is None:
                self.module.exit_json(msg=HOST_NOT_FOUND_MSG, failed=True)
            else:
                cluster_name = self.omevv_info_obj.get_cluster_name(vcenter_uuid, host_id)
                cluster_group_id = self.omevv_info_obj.get_group_id_of_cluster(vcenter_uuid, cluster_name)
                payload = self.get_payload_details(host_id=host_id)
                new_host_id = host_id

        if not self.is_update_job_allowed(vcenter_uuid, cluster_group_id, cluster_name):
            return

        if self.is_job_name_existing(vcenter_uuid, self.module.params.get('job_name')):
            return

        # Ensure host_service_tags is a list when host_ids is an int
        if isinstance(new_host_id, int):
            new_host_id = [new_host_id]
            host_service_tags = [host_service_tags]

        firmware_update_needed, diff_before, diff_after, retrieved_service_tag = self.is_firmware_update_needed(vcenter_uuid,
                                                                                                                cluster_group_id,
                                                                                                                new_host_id,
                                                                                                                parameters['targets'], host_service_tags)

        if self.module.check_mode or self.module.params.get('_ansible_check_mode'):
            self.handle_check_mode(firmware_update_needed, diff_before, diff_after, retrieved_service_tag)

        if firmware_update_needed:
            self.handle_firmware_update(vcenter_uuid, cluster_group_id, payload, parameters, diff_before, diff_after, retrieved_service_tag)
        else:
            self.module.exit_json(msg=CHANGES_NOT_FOUND_MSG,
                                  diff={"service_tag": retrieved_service_tag, "before": diff_before, "after": diff_after}, changed=False)

    def get_host_from_parameters(self, vcenter_uuid, parameters, host_ids=None, host_service_tags=None):
        target = self.get_target(parameters['targets'])
        if target['cluster']:
            return host_ids, host_service_tags
        else:
            host_id, host_service_tag = self.get_host_id(vcenter_uuid, target)
            return host_id, host_service_tag

    def handle_check_mode(self, firmware_update_needed, diff_before, diff_after, retrieved_service_tag=None):
        if firmware_update_needed:
            if self.module._diff:
                self.module.exit_json(msg=CHANGES_FOUND_MSG, changed=True,
                                      diff={"service_tag": retrieved_service_tag, "before": diff_before, "after": diff_after})
            else:
                self.module.exit_json(msg=CHANGES_FOUND_MSG, changed=True)
        else:
            self.module.exit_json(msg=CHANGES_NOT_FOUND_MSG, changed=False)

    def handle_firmware_update(self, vcenter_uuid, cluster_group_id, payload, parameters,
                               diff_before, diff_after, retrieved_service_tag=None):
        job_resp = self.execute_update_job(vcenter_uuid, cluster_group_id, payload, parameters)
        if self.module.params.get('run_now'):
            self.module.exit_json(msg=SUCCESS_UPDATE_MSG, changed=True, job_details=job_resp,
                                  diff={"service_tag": retrieved_service_tag, "before": diff_before, "after": diff_after})
        else:
            self.module.exit_json(msg=SUCCESS_UPDATE_SCHEDULED_MSG, changed=True,
                                  job_details=job_resp, diff={"service_tag": retrieved_service_tag,
                                                              "before": diff_before,
                                                              "after": diff_after})

    def get_target(self, target_list):
        for target in target_list:
            return target

    def get_host_id(self, vcenter_uuid, target):
        cluster_name = target['cluster']
        service_tag = target['servicetag']
        host = target['host']

        if service_tag:
            host_id, host_service_tag = self.omevv_info_obj.get_host_id(vcenter_uuid, hostname=None, servicetag=service_tag)
            return host_id, host_service_tag
        elif host:
            host_id, host_service_tag = self.omevv_info_obj.get_host_id(vcenter_uuid, hostname=host, servicetag=None)
            return host_id, host_service_tag
        else:
            cluster_group_id = self.omevv_info_obj.get_group_id_of_cluster(vcenter_uuid, cluster_name)
            host_ids, host_service_tags = self.omevv_info_obj.get_cluster_managed_host_details(vcenter_uuid, cluster_group_id)
            return host_ids, host_service_tags

    def is_firmware_update_needed(self, vcenter_uuid, cluster_group_id, host_ids, target, host_service_tags):
        firmware_update_needed = False
        before_dict = {}
        after_dict = {}
        before_no_change_dict = {}
        after_no_change_dict = {}
        diff_before = json.dumps(before_dict)
        diff_after = json.dumps(after_dict)
        diff_no_change_before = json.dumps(before_no_change_dict)
        diff_no_change_after = json.dumps(after_no_change_dict)

        # Ensure host_ids is a list for uniform processing
        if isinstance(host_ids, int):
            host_ids = [host_ids]
        if isinstance(host_service_tags, str):
            host_service_tags = [host_service_tags]

        for idx, one_host_id in enumerate(host_ids):
            before_dict = {}
            after_dict = {}
            before_no_change_dict = {}
            after_no_change_dict = {}

            update_needed, before_dict, after_dict, before_no_change_dict, after_no_change_dict = self.check_firmware_update(
                vcenter_uuid, cluster_group_id, one_host_id, target,
                before_dict, after_dict, before_no_change_dict, after_no_change_dict
            )

            if update_needed:
                firmware_update_needed = True
                device_service_tag = host_service_tags[idx]
                diff_before = before_dict
                diff_after = after_dict
                return firmware_update_needed, diff_before, diff_after, device_service_tag

            else:
                device_service_tag = host_service_tags[idx]
                diff_no_change_before = before_no_change_dict
                diff_no_change_after = after_no_change_dict
                return firmware_update_needed, diff_no_change_before, diff_no_change_after, device_service_tag

    def check_firmware_update(self, vcenter_uuid, cluster_group_id, host_id, target,
                              before_dict, after_dict, before_no_change_dict,
                              after_no_change_dict):
        if 'cluster' in target[0] and target[0]['cluster']:
            cluster_firmware_drift_info = self.omevv_info_obj.get_firmware_drift_info_for_single_host(
                vcenter_uuid, cluster_group_id, host_id)
            current_firmware_components = cluster_firmware_drift_info.get(
                'hostComplianceReports', [])[0].get('componentCompliances', [])
        else:
            firmware_drift_info = self.omevv_info_obj.get_firmware_drift_info_for_single_host(
                vcenter_uuid, cluster_group_id, host_id)
            current_firmware_components = firmware_drift_info.get(
                'hostComplianceReports', [])[0].get('componentCompliances', [])

        required_firmware_components = target[0]['firmware_components']
        firmware_update_needed = False

        for component in required_firmware_components:
            for current_component in current_firmware_components:
                if current_component['sourceName'] == component and current_component['driftStatus'] == 'NonCompliant':
                    before_dict[current_component["sourceName"]] = {
                        "firmwareversion": current_component["currentValue"]}
                    after_dict[current_component["sourceName"]] = {
                        "firmwareversion": current_component["baselineValue"]}
                    firmware_update_needed = True
                elif current_component['sourceName'] == component and current_component['driftStatus'] == 'Compliant':
                    before_no_change_dict[current_component["sourceName"]] = {
                        "firmwareversion": current_component["currentValue"]}
                    after_no_change_dict[current_component["sourceName"]] = {
                        "firmwareversion": current_component["baselineValue"]}

        return firmware_update_needed, before_dict, after_dict, before_no_change_dict, after_no_change_dict

    def is_update_job_allowed(self, vcenter_uuid, cluster_group_id, cluster_name):
        update_job_status = self.omevv_update_obj.check_existing_update_job(vcenter_uuid, cluster_group_id)
        if update_job_status is not True:
            self.module.exit_json(msg=UPDATE_JOB_PRESENT_MSG.format(cluster_name=cluster_name), skipped=True)
            return False
        return True

    def is_job_name_existing(self, vcenter_uuid, job_name):
        job_exist_status = self.omevv_update_obj.check_existing_job_name(vcenter_uuid, job_name)
        if job_exist_status is True:
            self.module.exit_json(msg=JOB_NAME_ALREADY_EXISTS_MSG.format(job_name=job_name), skipped=True)
            return True
        return False

    def execute_update_job(self, vcenter_uuid, cluster_group_id, payload, parameters):
        resp, error_msg = self.omevv_update_obj.update_cluster(payload, vcenter_uuid, cluster_group_id)
        if resp.success:
            job_resp, err_msg = self.omevv_update_obj.firmware_update_job_track(vcenter_uuid, resp.json_data)
            self.handle_job_response(parameters, vcenter_uuid, resp, job_resp, err_msg)
        else:
            self.module.exit_json(msg=FAILED_UPDATE_MSG, failed=True, error_info=error_msg)
        return job_resp

    def handle_job_response(self, parameters, vcenter_uuid, resp, job_resp, err_msg):
        run_now = parameters.get('run_now')
        if not run_now:
            self.module.exit_json(msg=SUCCESS_UPDATE_SCHEDULED_MSG, changed=True, job_details=job_resp)
        else:
            job_wait = self.module.params.get('job_wait')
            if job_wait:
                self.wait_for_job_completion(vcenter_uuid, resp, job_resp, err_msg)
            else:
                self.module.exit_json(msg=SUCCESS_UPDATE_SUBMIT_MSG, changed=True, job_details=job_resp)

    def wait_for_job_completion(self, vcenter_uuid, resp, job_resp, err_msg):
        while job_resp["state"] not in ["COMPLETED", "FAILED"]:
            time.sleep(3)
            job_resp, err_msg = self.omevv_update_obj.firmware_update_job_track(vcenter_uuid, resp.json_data)

        if job_resp["state"] == "COMPLETED":
            self.module.exit_json(msg=SUCCESS_UPDATE_MSG, changed=True, job_details=job_resp)
        else:
            self.module.exit_json(msg=FAILED_UPDATE_MSG, failed=True, error_info=err_msg)


def main():
    argument_spec = {
        "check_vSAN_health": {"type": 'bool'},
        "date_time": {"type": 'str'},
        "delete_job_queue": {"type": 'bool'},
        "drs_check": {"type": 'bool', "default": False},
        "enter_maintenance_mode_options": {
            "type": 'str',
            "choices": [
                'FULL_DATA_MIGRATION',
                'ENSURE_ACCESSIBILITY',
                'NO_DATA_MIGRATION'
            ]
        },
        "enter_maintenance_mode_timeout": {"type": 'int', "default": 60},
        "evacuate_VMs": {"type": 'bool', "default": False},
        "exit_maintenance_mode": {"type": "bool", "default": False},
        "job_description": {"type": 'str'},
        "job_name": {"type": 'str'},
        "job_wait": {"type": 'bool', "default": True},
        "job_wait_timeout": {"type": 'int', "default": 1200},
        "maintenance_mode_count_check": {"type": 'bool'},
        "reboot_options": {
            "type": 'str',
            "choices": [
                'FORCEREBOOT',
                'SAFEREBOOT',
                'NEXTREBOOT'
            ],
            "default": 'SAFEREBOOT'
        },
        "reset_idrac": {"type": 'bool'},
        "run_now": {"type": 'bool', "required": True},
        "targets": {
            "type": 'list',
            "elements": 'dict',
            "required": True,
            "options": {
                "firmware_components": {
                    "type": 'list',
                    "elements": 'str',
                    "required": True
                },
                "cluster": {"type": 'str'},
                "host": {"type": 'str'},
                "servicetag": {"type": 'str'}
            }
        }
    }

    module = OMEVVAnsibleModule(
        argument_spec=argument_spec,
        required_if=[
            ["run_now", False, ("date_time",)]
        ],
        supports_check_mode=True
    )

    try:
        with RestOMEVV(module.params) as rest_obj:
            omevv_obj = UpdateCluster(module, rest_obj)
            omevv_obj.execute()
    except HTTPError as err:
        response_data = {"msg": str(err), "failed": True}
        error_info = {}
        try:
            error_info = json.load(err)
        except ValueError:
            # If the error can't be loaded as JSON, capture it as a plain string
            error_info["message"] = str(err)
            error_info["type"] = "HTTPError"

        if err.code == 500:
            response_data["msg"] = error_info.get("message", str(error_info))
        elif err.code == 404:
            response_data["msg"] = SOURCE_NOT_FOUND_MSG
        else:
            response_data.update({
                "msg": error_info.get("message", str(error_info)),
                "error_info": error_info
            })
        module.exit_json(**response_data)

    except URLError as err:
        response_data = {
            "msg": f"The URL with IP {module.params.get('hostname')} and port {module.params.get('port')} cannot be reached.",
            "unreachable": True,
            "error_info": {"message": str(err), "type": "URLError"}
        }
        module.exit_json(**response_data)

    except (IOError, ValueError, TypeError, ConnectionError,
            AttributeError, IndexError, KeyError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
