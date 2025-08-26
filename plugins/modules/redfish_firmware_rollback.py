#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2023-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r"""
---
module: redfish_firmware_rollback
short_description: To perform a component firmware rollback using component name
version_added: "8.2.0"
description:
  - This module allows to rollback the firmware of different server components.
  - Depending on the component, the firmware update is applied after an automatic or manual reboot.
extends_documentation_fragment:
  - dellemc.openmanage.redfish_auth_options
options:
  name:
    type: str
    required: true
    description:
      - The name or regular expression of the component to match and is case-sensitive.
      - "The Name should be a supported rollback component. To view the list of rollback components for iDRAC9 and above,
      see, U(https://I(idrac_ip)/redfish/v1/UpdateService/FirmwareInventory?$expand=*($levels=1)'"
  reboot:
    description:
      - Reboot the server to apply the previous version of the firmware.
      - C(true) reboots the server to rollback the firmware to the available version.
      - C(false) schedules the rollback of firmware until the next restart.
      - When I(reboot) is C(false), some components update immediately, and the server may reboot.
        So, the module must wait till the server is accessible.
    type: bool
    default: true
  reboot_timeout:
    type: int
    description: Wait time in seconds. The module waits for this duration till the server reboots.
    default: 900
requirements:
  - "python >= 3.9.6"
author:
  - "Felix Stephen (@felixs88)"
  - "Sakshi Makkar (@Sakshi-dell)"
notes:
  - Run this module from a system that has direct access to Redfish APIs.
  - For components that do not require a reboot, firmware rollback proceeds irrespective of
    I(reboot) is C(true) or C(false).
  - This module supports IPv4 and IPv6 addresses.
  - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Rollback a BIOS component firmware
  dellemc.openmanage.redfish_firmware_rollback:
    baseuri: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    name: "BIOS"

- name: Rollback all NIC cards with a name starting from 'Broadcom Gigabit'.
  dellemc.openmanage.redfish_firmware_rollback:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    name: "Broadcom Gigabit Ethernet.*"

- name: Rollback all the component firmware except BIOS component.
  dellemc.openmanage.redfish_firmware_rollback:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    name: "(?!BIOS).*"

- name: Rollback all the available firmware component.
  dellemc.openmanage.redfish_firmware_rollback:
    baseuri: "192.168.0.1:443"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    name: ".*"
"""

RETURN = """
---
msg:
  type: str
  description: Overall firmware rollback status.
  returned: always
  sample: "Successfully completed the job for firmware rollback."
status:
  type: list
  description: Firmware rollback job and progress details from the iDRAC.
  returned: success
  sample: [{
    "ActualRunningStartTime": "2023-08-04T12:26:55",
    "ActualRunningStopTime": "2023-08-04T12:32:35",
    "CompletionTime": "2023-08-04T12:32:35",
    "Description": "Job Instance",
    "EndTime": "TIME_NA",
    "Id": "JID_911698303631",
    "JobState": "Completed",
    "JobType": "FirmwareUpdate",
    "Message": "Job completed successfully.",
    "MessageArgs": [],
    "MessageId": "PR19",
    "Name": "Firmware Rollback: Firmware",
    "PercentComplete": 100,
    "StartTime": "2023-08-04T12:23:50",
    "TargetSettingsURI": null
  }]
error_info:
  type: dict
  description: Details of the HTTP error.
  returned: on http error
  sample: {
    "error": {
      "@Message.ExtendedInfo": [{
        "Message": "InstanceID value provided for the update operation is invalid",
        "MessageArgs": [],
        "MessageArgs@odata.count": 0,
        "MessageId": "IDRAC.2.8.SUP024",
        "RelatedProperties": [],
        "RelatedProperties@odata.count": 0,
        "Resolution": "Enumerate inventory, copy the InstanceID value and provide that value for the update operation.",
        "Severity": "Warning"
      }],
      "code": "Base.1.12.GeneralError",
      "message": "A general error has occurred. See ExtendedInfo for more information"
    }
  }
"""


import json
import re
import time
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.redfish import Redfish, RedfishAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import wait_for_redfish_reboot_job, \
    wait_for_redfish_job_complete, strip_substr_dict, MANAGER_JOB_ID_URI_10, MANAGERS_URI
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError


UPDATE_SERVICE = "UpdateService"
SYSTEM_RESOURCE_ID = "System.Embedded.1"
NO_COMPONENTS = "There were no firmware components to rollback."
CHANGES_FOUND = "Changes found to be applied."
NO_CHANGES_FOUND = "No changes found to be applied."
NOT_SUPPORTED = "The target firmware version does not support the firmware rollback."
COMPLETED_ERROR = "The job for firmware rollback has been completed with error(s)."
SCHEDULED_ERROR = "The job for firmware rollback has been scheduled with error(s)."
ROLLBACK_SUCCESS = "Successfully completed the job for firmware rollback."
ROLLBACK_SCHEDULED = "Successfully scheduled the job for firmware rollback."
ROLLBACK_FAILED = "Failed to complete the job for firmware rollback."
REBOOT_FAIL = "Failed to reboot the server."
NEGATIVE_TIMEOUT_MESSAGE = "The parameter reboot_timeout value cannot be negative or zero."
JOB_WAIT_MSG = "Task excited after waiting for {0} seconds. Check console for firmware rollback status."
REBOOT_COMP = ["Integrated Dell Remote Access Controller", "BMC Firmware Inventory"]
BIOS_COMP = ["BIOS", "BIOS Firmware Inventory"]
BACKPLANE_COMP = ["RAID.Backplane.Firmware Firmware Inventory"]
INITIAL_DELAY_17G = 240
SESSION_RESOURCE_COLLECTION = {
    "SESSION": "/redfish/v1/SessionService/Sessions",
    "SESSION_ID": "/redfish/v1/SessionService/Sessions/{Id}",
}


def categorize_components(previous_components, component_compile):
    prev_uri, reboot_uri, bios_uri, backplane_uri = {}, [], [], []
    for comp in previous_components:
        available_name = comp["Name"]
        if not re.match(component_compile, available_name):
            continue

        uri = comp["@odata.id"]

        if available_name in REBOOT_COMP:
            reboot_uri.append(uri)
        elif available_name in BIOS_COMP:
            bios_uri.append(uri)
        elif available_name in BACKPLANE_COMP:
            backplane_uri.append(uri)
        else:
            prev_uri[comp["Version"]] = uri

    return prev_uri, reboot_uri, bios_uri, backplane_uri


def get_rollback_preview_target(redfish_obj, module):
    action_resp = redfish_obj.invoke_request("GET", "{0}{1}".format(redfish_obj.root_uri, UPDATE_SERVICE))
    action_attr = action_resp.json_data["Actions"]
    update_service = action_attr.get("#UpdateService.SimpleUpdate")

    if not update_service or 'target' not in update_service:
        module.fail_json(msg=NOT_SUPPORTED)

    update_uri = update_service.get('target')
    inventory_uri = action_resp.json_data.get('FirmwareInventory').get('@odata.id')
    inventory_uri_resp = redfish_obj.invoke_request("GET", "{0}{1}".format(inventory_uri, "?$expand=*($levels=1)"),
                                                    api_timeout=120)
    previous_component = list(filter(lambda d: d["Id"].startswith("Previous"), inventory_uri_resp.json_data["Members"]))
    if not previous_component:
        module.fail_json(msg=NO_COMPONENTS)

    component_name = module.params["name"]
    try:
        component_compile = re.compile(r"^{0}$".format(component_name))
    except Exception:
        module.exit_json(msg=NO_CHANGES_FOUND)

    prev_uri, reboot_uri, bios_uri, backplane_uri = categorize_components(previous_component, component_compile)

    if prev_uri or reboot_uri or bios_uri:
        if module.check_mode:
            module.exit_json(msg=CHANGES_FOUND, changed=True)
    else:
        module.exit_json(msg=NO_CHANGES_FOUND)

    return list(prev_uri.values()), reboot_uri, update_uri, bios_uri, backplane_uri


def get_job_status(redfish_obj, module, job_ids, job_wait=True, check_completion=False):
    each_status, failed_count, js_job_msg = [], 0, ""
    wait_timeout = module.params["reboot_timeout"]
    for each in job_ids:
        each_job_uri = MANAGER_JOB_ID_URI_10.format(each)
        job_resp, js_job_msg = wait_for_redfish_job_complete(redfish_obj, each_job_uri, job_wait=job_wait,
                                                             wait_timeout=wait_timeout, check_completion=check_completion)
        if job_resp and js_job_msg:
            module.exit_json(msg=JOB_WAIT_MSG.format(wait_timeout), job_status=[strip_substr_dict(job_resp.json_data)],
                             changed=True)
        job_status = job_resp.json_data
        if job_status["JobState"] == "Failed":
            failed_count += 1
        strip_odata = strip_substr_dict(job_status)
        each_status.append(strip_odata)
    return each_status, failed_count


def require_session(idrac, module):
    session_id, token = "", None
    payload = {'UserName': module.params["username"], 'Password': module.params["password"]}
    path = SESSION_RESOURCE_COLLECTION["SESSION"]
    resp = idrac.invoke_request('POST', path, data=payload, api_timeout=120)
    if resp and resp.success:
        session_id = resp.json_data.get("Id")
        token = resp.headers.get('X-Auth-Token')
    return session_id, token


def wait_for_redfish_idrac_reset(module, redfish_obj, wait_time_sec, generation, interval=30):
    _sleep_initial_delay(generation, interval)

    wait = wait_time_sec
    track_failed = True
    resetting = False
    while wait > 0 and track_failed:
        try:
            redfish_obj.invoke_request("GET", MANAGERS_URI, api_timeout=120)
            track_failed = False
            break
        except HTTPError as err:
            if err.getcode() == 401:
                redfish_obj, wait, resetting = _handle_unauthorized_error(module, redfish_obj, generation, wait)
                track_failed = False
            else:
                wait, resetting = _handle_connection_error(wait, interval, resetting)
        except (URLError, Exception):
            wait, resetting = _handle_connection_error(wait, interval, resetting)

    return track_failed, resetting


def _sleep_initial_delay(generation, interval):
    """Sleep before starting the polling for reset."""
    if generation >= 17:
        time.sleep(INITIAL_DELAY_17G)
    else:
        time.sleep(interval // 2)


def _handle_unauthorized_error(module, redfish_obj, generation, wait):
    """Handle 401 Unauthorized errors during reset polling."""
    if generation >= 17:
        time.sleep(INITIAL_DELAY_17G)
        wait -= INITIAL_DELAY_17G
    new_redfish_obj = Redfish(module.params, req_session=True)
    sid, token = require_session(new_redfish_obj, module)
    redfish_obj.session_id = sid
    redfish_obj._headers.update({"X-Auth-Token": token})
    return redfish_obj, wait, True


def _handle_connection_error(wait, interval, resetting):
    """Handle connection-related issues such as URLError or unknown exceptions."""
    time.sleep(interval)
    wait -= interval
    if not resetting:
        resetting = True
    return wait, resetting


def simple_update(redfish_obj, preview_uri, update_uri):
    job_ids = []
    for uri in preview_uri:
        resp = redfish_obj.invoke_request("POST", update_uri, data={"ImageURI": uri})
        time.sleep(30)
        task_uri = resp.headers.get("Location")
        task_id = task_uri.split("/")[-1]
        job_ids.append(task_id)
    return job_ids


def handle_reboot_job(redfish_obj, module):
    payload = {"ResetType": "ForceRestart"}
    job_resp_status, reset_status, reset_fail = wait_for_redfish_reboot_job(
        redfish_obj, SYSTEM_RESOURCE_ID, payload=payload
    )

    if not reset_status and reset_fail:
        module.fail_json(msg=reset_fail)

    if reset_status and job_resp_status:
        job_uri = MANAGER_JOB_ID_URI_10.format(job_resp_status["Id"])
        job_resp, job_msg = wait_for_redfish_job_complete(redfish_obj, job_uri)
        job_state = job_resp.json_data.get("JobState")

        if job_state != "RebootCompleted":
            module.fail_json(
                msg=JOB_WAIT_MSG.format(module.params["reboot_timeout"]) if job_msg else REBOOT_FAIL
            )


def rollback_firmware(redfish_obj, module, preview_uri, reboot_uri, update_uri, bios_uri, backplane_uri):
    current_job_status, failed_cnt, resetting = [], 0, False
    direct_updates = []
    job_ids = simple_update(redfish_obj, preview_uri, update_uri)

    for job_id in job_ids:
        job_uri = MANAGER_JOB_ID_URI_10.format(job_id)
        job_resp, _job_msg = wait_for_redfish_job_complete(redfish_obj, job_uri, job_wait=False)
        job_state = job_resp.json_data.get("JobState")
        if job_state in {"Running", "Scheduling"}:
            direct_updates.append(job_id)

    if direct_updates:
        _status, _failed = get_job_status(redfish_obj, module, direct_updates, job_wait=True)

    # handle backplane uri separately since they interfere with other updates in iDRAC 10 (generation >= 17G)
    if backplane_uri:
        backplane_job_id = simple_update(redfish_obj, backplane_uri, update_uri)
        status, failed = get_job_status(redfish_obj, module, backplane_job_id, job_wait=True, check_completion=True)
        current_job_status.extend(status)
        failed_cnt += failed

    if bios_uri:
        bios_job_ids = simple_update(redfish_obj, bios_uri, update_uri)
        job_ids.extend(bios_job_ids)

    if job_ids:
        if module.params["reboot"]:
            handle_reboot_job(redfish_obj, module)
            status, failed = get_job_status(redfish_obj, module, job_ids, job_wait=True, check_completion=True)
        else:
            status, failed = get_job_status(redfish_obj, module, job_ids, job_wait=False)
        current_job_status.extend(status)
        failed_cnt += failed

    if reboot_uri:
        generation = redfish_obj.get_server_generation[0]
        reboot_job_ids = simple_update(redfish_obj, reboot_uri, update_uri)
        track, resetting = wait_for_redfish_idrac_reset(module, redfish_obj, 900, generation)
        if not track and resetting:
            status, failed = get_job_status(redfish_obj, module, reboot_job_ids, job_wait=True)
            current_job_status.extend(status)
            failed_cnt += failed

    return current_job_status, failed_cnt, resetting


def main():
    specs = {
        "name": {"required": True, "type": "str"},
        "reboot": {"type": "bool", "default": True},
        "reboot_timeout": {"type": "int", "default": 900},
    }

    module = RedfishAnsibleModule(argument_spec=specs, supports_check_mode=True)
    if module.params["reboot_timeout"] <= 0:
        module.fail_json(msg=NEGATIVE_TIMEOUT_MESSAGE)
    try:
        with Redfish(module.params, req_session=True) as redfish_obj:
            preview_uri, reboot_uri, update_uri, bios_uri, backplane_uri = get_rollback_preview_target(redfish_obj, module)
            job_status, failed_count, resetting = rollback_firmware(redfish_obj, module, preview_uri, reboot_uri, update_uri, bios_uri, backplane_uri)
            if not job_status or (failed_count == len(job_status)):
                module.exit_json(msg=ROLLBACK_FAILED, status=job_status, failed=True)
            if module.params["reboot"]:
                msg, module_fail, changed = ROLLBACK_SUCCESS, False, True
                if failed_count > 0 and failed_count != len(job_status):
                    msg, module_fail, changed = COMPLETED_ERROR, True, False
            else:
                msg, module_fail, changed = ROLLBACK_SCHEDULED, False, True
                if failed_count > 0 and failed_count != len(job_status):
                    msg, module_fail, changed = SCHEDULED_ERROR, True, False
                elif resetting and len(job_status) == 1 and failed_count != len(job_status):
                    msg, module_fail, changed = ROLLBACK_SUCCESS, False, True
            module.exit_json(msg=msg, job_status=job_status, failed=module_fail, changed=changed)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError, IOError, AssertionError, OSError, SSLError) as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
