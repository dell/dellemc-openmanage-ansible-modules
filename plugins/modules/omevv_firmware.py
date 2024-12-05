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
short_description: Update firmware of specific host in the cluster
version_added: "9.10.0"
description: This module allows you to update firmware of specific host in the cluster.
extends_documentation_fragment:
  - dellemc.openmanage.omevv_auth_options
options:
  check_vSAN_health:
    description:
      - Whether to check vSAN health whilst update.
      - C(true) checks the vSAN health whilst update.
      - C(false) does not check the vSAN health whilst update.
    type: bool
  date_time:
    description:
      - Date and time when the job must run. This is applicable when I(run_now) is C(false).
      - The format is YYYY-MM-DDThh:mm:ss<UTC>.
    type: str
  delete_job_queue:
    description:
      - Whether to delete the job queue in iDRAC while performing firmware update.
      - C(true) deletes the job queue in iDRAC while performing firmware update.
      - C(false) does not delete the job queue in iDRAC while performing firmware update.
    type: bool
  drs_check:
    description:
      - Allows to check if cluster's DRS is enabled or not.
      - C(true) checks if cluster's DRS is enabled.
      - C(false) does not check if cluster's DRS is enabled.
    type: bool
    default: false
  enter_maintenance_mode_options:
    description:
      - VM migration policy during MM mode.
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
      - Allows to move the VM to other host when host is powered off.
      - C(true) moves the VM to other host when host is powered off.
      - C(false) does not move the VM to other host when host is powered off.
    type: bool
    default: false
  exit_maintenance_mode:
    description:
      - Whether to exit MM mode after Update.
      - C(true) exits the MM mode after Update.
      - C(false) does not exit the MM mode after Update.
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
      - Allows to check if any host in cluster is in MM mode.
      - C(true) checks if any host in cluster is in MM mode.
      - C(false) does not check if any host in cluster is in MM mode.
    type: bool
  reboot_options:
    description:
      - Host reboot option for firmware update.
      - C(FORCEREBOOT) will force reboot the server.
      - C(SAFEREBOOT) will reboot the server in safe mode.
      - C(NEXTREBOOT) will not reboot the server.
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
      - C(true) will run the update job instantly.
      - C(false) will run the update at the specified I(date_time).
    type: bool
    required: true
  target:
    description:
      - The target details for the firmware update operation.
      - Either I(servicetag) or I(host) is required for the firmware update operation.
    type: list
    elements: dict
    required: true
    suboptions:
      cluster:
        description:
          - Name of the cluster the hosts belong to.
        type: str
        required: true
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
          - I(host) is mutually exclusive with I(servicetag).
          - M(dellemc.openmanage.omevv_device_info) module can be used to fetch the device
            information.
        type: str
      servicetag:
        description:
          - The service tag of the host.
          - I(servicetag) is mutually exclusive with I(host).
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
- name: Update firmware at the scheduled time for a specific host
  dellemc.openmanage.omevv_firmware:
    hostname: "192.168.0.1"
    vcenter_uuid: "xxxxx"
    vcenter_username: "username"
    vcenter_password: "password"
    ca_path: "path/to/ca_file"
    run_now: false
    date_time: "2024-09-10T20:50:00Z"
    enter_maintenance_mode_timeout: 60
    drs_check: true
    evacuate_VMs: true
    exit_maintenance_mode: true
    reboot_options: SAFEREBOOT
    maintenance_mode_count_check: true
    check_vSAN_health: true
    reset_idrac: true
    delete_job_queue: true
    target:
      - cluster: cluster_a
        servicetag: SVCTAG1
        firmware_components:
          - "DCIM:INSTALLED#802__Diagnostics.Embedded.1:LC.Embedded.1"

- name: Fetch firmware compliance report of all the hosts in the specific cluster
  dellemc.openmanage.omevv_firmware_compliance_info:
    hostname: "192.168.0.1"
    vcenter_uuid: "xxxxx"
    vcenter_username: "username"
    vcenter_password: "password"
    ca_path: "path/to/ca_file"
    clusters:
      - cluster_name: cluster_a
  register: compliance_data

- name: Extract sourceName
  set_fact:
    source_names: "{{ compliance_data.hostComplianceReports[0].componentCompliances|json_query('*.sourceName') }}"

- name: Extract sourceName for specific component
  set_fact:
    source_name: "{{ compliance_data.hostComplianceReports[0].componentCompliances[0].sourceName }}"

- name: Update firmware at the scheduled time for a specific host
  dellemc.openmanage.omevv_firmware:
    hostname: "192.168.0.1"
    vcenter_uuid: "xxxxx"
    vcenter_username: "username"
    vcenter_password: "password"
    ca_path: "path/to/ca_file"
    run_now: false
    date_time: "2024-09-10T20:50:00Z"
    enter_maintenance_mode_timeout: 60
    drs_check: true
    evacuate_VMs: true
    exit_maintenance_mode: true
    reboot_options: SAFEREBOOT
    maintenance_mode_count_check: true
    check_vSAN_health: true
    reset_idrac: true
    delete_job_queue: true
    target:
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
      "errorCode": "18001",
      "message": "Baseline profile with name Test already exists."
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
CHANGES_FOUND_MSG = "Changes found to be applied."
CHANGES_NOT_FOUND_MSG = "No changes found to be applied."
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The value for the 'job_wait_timeout' parameter cannot be " \
                               "negative or zero."
UNREACHABLE_MSG = "The URL with the {ip}:{port} cannot be reached."
SOURCE_NOT_FOUND_MSG = "The Requested resource cannot be found."


class FirmwareUpdate():

    def __init__(self, module, rest_obj):
        self.module = module
        self.obj = rest_obj
        self.omevv_info_obj = OMEVVInfo(self.obj)
        self.omevv_update_obj = OMEVVFirmwareUpdate(self.obj)
        self.omevv_baseline_obj = OMEVVBaselineProfile(self.obj)

    def extract_host_id(self, svctag, hostname, cluster_name):
        host_id = []
        uuid = self.module.params.get('vcenter_uuid')
        managed_hosts, invalid_result = self.omevv_info_obj.get_managed_host_details(
            uuid=uuid,
            servicetags=svctag,
            hostnames=hostname)
        if invalid_result:
            hostnames = invalid_result["hostnames"]
            servicetags = invalid_result["servicetags"]
            # if hostnames or servicetags:
            #     host_invalid_list = ', '.join(hostnames + servicetags)
            #     self.module.warn(PARTIAL_HOST_WARN_MSG.format(host_invalid_list))

        for each_host in managed_hosts:
            if each_host.get('clusterName') == cluster_name:
                host_id.append(each_host.get('id'))
        return host_id

    def get_payload_details(self, host_id):
        device_id = host_id
        parameters = self.module.params
        target_list = parameters['target']
        firmware = {
            "targets": []
        }
        payload = {}

        if parameters.get('check_vSAN_health') is not None:
            firmware['checkvSANHealth'] = parameters.get('check_vSAN_health')

        if parameters.get('run_now') is True:
            payload["schedule"] = {
                "runNow": parameters.get('run_now')
            }
        else:
            payload["schedule"] = {
                "runNow": parameters.get('run_now'),
                "dateTime": parameters.get('date_time')
            }

        if parameters.get('delete_job_queue') is not None:
            firmware['deleteJobsQueue'] = parameters.get('delete_job_queue')

        if parameters.get('drs_check') is not None:
            firmware['drsCheck'] = parameters.get('drs_check')

        if parameters.get('enter_maintenance_mode_options') is not None:
            firmware['enterMaintenanceModeOption'] = parameters.get('enter_maintenance_mode_options')

        if parameters.get('enter_maintenance_mode_timeout') is not None:
            firmware['enterMaintenanceModetimeout'] = parameters.get('enter_maintenance_mode_timeout')

        if parameters.get('evacuate_VMs') is not None:
            firmware['evacuateVMs'] = parameters.get('evacuate_VMs')

        if parameters.get('exit_maintenance_mode') is not None:
            firmware['exitMaintenanceMode'] = parameters.get('exit_maintenance_mode')

        if self.module.params.get('job_description'):
            payload["jobDescription"] = self.module.params.get('job_description')

        if self.module.params.get('job_name'):
            payload["jobName"] = self.module.params.get('job_name')
        else:
            date_time = datetime.now()
            job_name = (
                f"omam_firmware_update_job_{date_time.year}{date_time.month:02}{date_time.day:02}_"
                f"{date_time.hour:02}{date_time.minute:02}{date_time.second:02}")
            payload["jobName"] = job_name

        if parameters.get('maintenance_mode_count_check') is not None:
            firmware['maintenanceModeCountCheck'] = parameters.get('maintenance_mode_count_check')

        if parameters.get('reboot_options') is not None:
            firmware['rebootOptions'] = parameters.get('reboot_options')

        if parameters.get('reset_idrac') is not None:
            firmware['resetIDrac'] = parameters.get('reset_idrac')

        for target in target_list:
            actual_target = {
                "firmwarecomponents": target['firmware_components'],
                "id": device_id
            }

        firmware['targets'].append(actual_target)

        payload["firmware"] = firmware

        return payload

    def validate_date_time(self):
        try:
            ftime = datetime.strptime(self.module.params.get('date_time'), "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            self.module.exit_json(msg=INVALID_DATE_TIME_MSG, failed=True)
        return ftime

    def enter_maintenance_mode_timeout(self):
        enter_maintenance_mode_timeout = self.module.params.get('enter_maintenance_mode_timeout')
        if enter_maintenance_mode_timeout < 60 or enter_maintenance_mode_timeout > 1440:
            self.module.exit_json(msg=MAINTENANCE_MODE_TIMEOUT_INVALID_MSG, failed=True)

    def validate_params(self):
        # Validate the job wait parameter
        if validate_job_wait(self.module):
            self.module.exit_json(msg=TIMEOUT_NEGATIVE_OR_ZERO_MSG, failed=True)

        # Validate the date_time parameter
        self.validate_date_time()

        # Validate the enter_maintenance_mode_timeout parameter
        self.enter_maintenance_mode_timeout()

        # Validate the cluster names
        parameters = self.module.params
        target_list = parameters['target']
        for target in target_list:
            cluster_name = target['cluster']
        vcenter_uuid = self.module.params.get('vcenter_uuid')
        is_valid_cluster, invalid_cluster_err_msg = self.omevv_baseline_obj.validate_cluster_names(cluster_name, vcenter_uuid)
        if not is_valid_cluster:
            self.module.exit_json(msg=invalid_cluster_err_msg, failed=True)

    def execute(self):
        """To be overridden by subclasses to implement specific profile creation or deletion logic."""
        pass


class UpdateCluster(FirmwareUpdate):

    def execute(self):
        self.validate_params()
        vcenter_uuid = self.module.params.get('vcenter_uuid')
        parameters = self.module.params
        target_list = parameters['target']
        for target in target_list:
            cluster_name = target['cluster']
            service_tag = target['servicetag']
            host = target['host']
        cluster_group_id = self.omevv_info_obj.get_group_id_of_cluster(vcenter_uuid, cluster_name)
        if service_tag:
            host_id = self.extract_host_id(svctag=service_tag, cluster_name=cluster_name, hostname=None)
        else:
            host_id = self.extract_host_id(svctag=None, cluster_name=cluster_name, hostname=host)
        payload = self.get_payload_details(host_id=host_id[0])
        resp, error_msg = self.omevv_update_obj.update_cluster(payload, vcenter_uuid, cluster_group_id)
        if resp.success:
            job_resp, err_msg = self.omevv_update_obj.firmware_update_job_track(vcenter_uuid, resp.json_data)
            if parameters.get('run_now') is False:
                self.module.exit_json(msg=SUCCESS_UPDATE_SCHEDULED_MSG, changed=True, job_details=job_resp)
            else:
                job_wait = self.module.params.get('job_wait')
                if job_wait:
                    while job_resp["state"] not in ["COMPLETED", "FAILED"]:
                        time.sleep(3)
                        job_resp, err_msg = self.omevv_update_obj.firmware_update_job_track(vcenter_uuid, resp.json_data)
                    if job_resp["state"] == "COMPLETED":
                        self.module.exit_json(msg=SUCCESS_UPDATE_MSG, changed=True, job_details=job_resp)
                    else:
                        self.module.exit_json(msg=FAILED_UPDATE_MSG, failed=True, error_info=err_msg)
                else:
                    self.module.exit_json(msg=SUCCESS_UPDATE_SUBMIT_MSG, changed=True, job_details=job_resp)
        else:
            self.module.exit_json(msg=FAILED_UPDATE_MSG, failed=True, error_info=error_msg)


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
        "exit_maintenance_mode": {"type": 'bool', "default": False},
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
        "target": {
            "type": 'list',
            "elements": 'dict',
            "required": True,
            "options": {
                "cluster": {"type": 'str', "required": True},
                "firmware_components": {
                    "type": 'list',
                    "elements": 'str',
                    "required": True
                },
                "host": {"type": 'str'},
                "servicetag": {"type": 'str'}
            }
        }
    }

    module = OMEVVAnsibleModule(
        argument_spec=argument_spec,
        # mutually_exclusive=[
        #     [('servicetag", "host')],
        # ],
        required_if=[
            ["run_now", "true", ["date_time"]],
        ],
        supports_check_mode=True
    )

    try:
        with RestOMEVV(module.params) as rest_obj:
            # if module.params.get('target').get('servicetag') or module.params.get('target').get('host'):
            #     omevv_obj = UpdateSingleHost(module, rest_obj)
            # else:
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

        if err.code == 404:
            response_data["msg"] = SOURCE_NOT_FOUND_MSG
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
