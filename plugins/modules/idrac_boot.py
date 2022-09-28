#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 6.1.0
# Copyright (C) 2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_boot
short_description: Configure the boot order settings.
version_added: "6.1.0"
description:
  - This module allows to configure the boot order settings.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
  boot_options:
    type: list
    elements: dict
    description:
      - Options to enable or disable the boot devices.
      - This is mutually exclusive with I(boot_order), I(boot_source_override_mode), I(boot_source_override_enabled)
        I(boot_source_override_target), and I(uefi_target_boot_source_override).
    suboptions:
      boot_option_reference:
        type: str
        description:
          - FQDD of the boot device.
          - This is mutually exclusive with I(display_name).
      display_name:
        type: str
        description:
          - Display name of the boot source device.
          - This is mutually exclusive with I(boot_option_reference).
      enabled:
        type: bool
        required: true
        description: Enable or disable the boot device.
  boot_order:
    type: list
    elements: str
    description:
      - This option allows to set the boot devices in the required boot order sequences.
      - This is mutually exclusive with I(boot_options).
  boot_source_override_mode:
    type: str
    description:
      - The BIOS boot mode (either Legacy or UEFI) to be used when I(boot_source_override_target)
        boot source is booted from.
      - C(legacy) The system boot in non-UEFI(Legacy) boot mode to the I(boot_source_override_target).
      - C(uefi) The system boot in UEFI boot mode to the I(boot_source_override_target).
      - This is mutually exclusive with I(boot_options).
    choices: [legacy, uefi]
  boot_source_override_enabled:
    type: str
    description:
      - The state of the Boot Source Override feature.
      - C(disabled) The system boots normally.
      - C(once) The system boots (one time) to the I(boot_source_override_target).
      - C(continuous) The system boots to the target specified in the I(boot_source_override_target)
        until this property is set to Disabled.
      - The state is set to C(once) for the one-time boot override and C(continuous) for the
        remain-active-until—canceled override. If the state is set C(once), the value is reset
        to C(disabled) after the I(boot_source_override_target) actions have completed successfully.
      - Changes to this options do not alter the BIOS persistent boot order configuration.
      - This is mutually exclusive with I(boot_options).
    choices: [continuous, disabled, once]
  boot_source_override_target:
    type: str
    description:
      - The boot source override target device to use during the next boot instead of the normal boot device.
      - C(pxe) performs PXE boot from the primary NIC.
      - C(floppy), C(cd), C(hdd), C(sd_card) performs boot from their devices respectively.
      - C(bios_setup) performs boot into the native BIOS setup.
      - C(utilities) performs boot from the local utilities.
      - C(uefi_target) performs boot from the UEFI device path found in I(uefi_target_boot_source_override).
      - If the I(boot_source_override_target) is set to a value other than C(none) then the
        I(boot_source_override_enabled) is automatically set to C(once).
      - Changes to this options do not alter the BIOS persistent boot order configuration.
      - This is mutually exclusive with I(boot_options).
    choices: [uefi_http, sd_card, uefi_target, utilities, bios_setup, hdd, cd, floppy, pxe, none]
  uefi_target_boot_source_override:
    type: str
    description:
      - The UEFI device path of the device from which to boot when I(boot_source_override_target) is C(uefi_target).
      - I(boot_source_override_enabled) cannot be set to c(continuous) if I(boot_source_override_target)
        set to C(uefi_target) because this settings is defined in UEFI as a one-time-boot setting.
      - Changes to this options do not alter the BIOS persistent boot order configuration.
      - This is required if I(boot_source_override_target) is C(uefi_target).
      - This is mutually exclusive with I(boot_options).
  reset_type:
    type: str
    description:
      - C(none) Host system is not rebooted and I(job_wait) is not applicable.
      - C(force_reset) Forcefully reboot the Host system.
      - C(graceful_reset) Gracefully reboot the Host system.
    choices: [graceful_restart, force_restart, none]
    default: graceful_restart
  job_wait:
    type: bool
    description:
      - Provides the option to wait for job completion.
      - This is applicable when I(reset_type) is C(force_reset) or C(graceful_reset).
    default: true
  job_wait_timeout:
    type: int
    description:
      - The maximum wait time of I(job_wait) in seconds. The job is tracked only for this duration.
      - This option is applicable when I(job_wait) is C(True).
    default: 900
  resource_id:
    type: str
    description: Redfish ID of the resource.
requirements:
    - "python >= 3.8.6"
author:
    - "Felix Stephen (@felixs88)"
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports C(check_mode).
"""


EXAMPLES = """
---
- name: Configure the system boot options settings.
  dellemc.openmanage.idrac_boot:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    boot_options:
      - display_name: Hard drive C
        enabled: true
      - boot_option_reference: NIC.PxeDevice.2-1
        enabled: true

- name: Configure the boot order settings.
  dellemc.openmanage.idrac_boot:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    boot_order:
      - Boot0001
      - Boot0002
      - Boot0004
      - Boot0003

- name: Configure the boot source override mode.
  dellemc.openmanage.idrac_boot:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    boot_source_override_mode: legacy
    boot_source_override_target: cd
    boot_source_override_enabled: once

- name: Configure the UEFI target settings.
  dellemc.openmanage.idrac_boot:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    boot_source_override_mode: uefi
    boot_source_override_target: uefi_target
    uefi_target_boot_source_override: "VenHw(3A191845-5F86-4E78-8FCE-C4CFF59F9DAA)"

- name: Configure the boot source override mode as pxe.
  dellemc.openmanage.idrac_boot:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    boot_source_override_mode: legacy
    boot_source_override_target: pxe
    boot_source_override_enabled: continuous
"""


RETURN = r'''
---
msg:
  description: Successfully updated the boot settings.
  returned: success
  type: str
  sample: Successfully updated the boot settings.
job:
  description: Configured job details.
  returned: success
  type: dict
  sample: {
    "ActualRunningStartTime": "2019-06-19T00:57:24",
    "ActualRunningStopTime": "2019-06-19T01:00:27",
    "CompletionTime": "2019-06-19T01:00:27",
    "Description": "Job Instance",
    "EndTime": "TIME_NA",
    "Id": "JID_609237056489",
    "JobState": "Completed",
    "JobType": "BIOSConfiguration",
    "Message": "Job completed successfully.",
    "MessageArgs": [],
    "MessageId": "PR19",
    "Name": "Configure: BIOS.Setup.1-1",
    "PercentComplete": 100,
    "StartTime": "2019-06-19T00:55:05",
    "TargetSettingsURI": null }
boot:
  description: Configured boot settings details.
  returned: success
  type: dict
  sample: {
    "BootOptions": {
      "Description": "Collection of BootOptions",
      "Members": [{
        "BootOptionEnabled": false,
        "BootOptionReference": "HardDisk.List.1-1",
        "Description": "Current settings of the Legacy Boot option",
        "DisplayName": "Hard drive C:",
        "Id": "HardDisk.List.1-1",
        "Name": "Legacy Boot option",
        "UefiDevicePath": "VenHw(D6C0639F-C705-4EB9-AA4F-5802D8823DE6)"}],
      "Name": "Boot Options Collection"
      },
      "BootOrder": [ "HardDisk.List.1-1"],
      "BootSourceOverrideEnabled": "Disabled",
      "BootSourceOverrideMode": "Legacy",
      "BootSourceOverrideTarget": "None",
      "UefiTargetBootSourceOverride": null }
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
import time
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, idrac_auth_params
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (strip_substr_dict, idrac_system_reset,
                                                                               get_system_res_id,
                                                                               wait_for_idrac_job_completion)
from ansible.module_utils.basic import AnsibleModule

SYSTEM_URI = "/redfish/v1/Systems"
BOOT_OPTIONS_URI = "/redfish/v1/Systems/{0}/BootOptions?$expand=*($levels=1)"
JOB_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs?$expand=*($levels=1)"
JOB_URI_ID = "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/{0}"
BOOT_SEQ_URI = "/redfish/v1/Systems/{0}/BootSources"
PATCH_BOOT_SEQ_URI = "/redfish/v1/Systems/{0}/BootSources/Settings"

NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_MSG = "Changes found to be applied."
JOB_EXISTS = "Unable to complete the request because the BIOS configuration job already " \
             "exists. Wait for the pending job to complete."
BOOT_OPT_ERROR_MSG = "{0} boot_options provided."
INVALID_BOOT_OPT = "{0} boot order reference provided."
SUCCESS_MSG = "Successfully updated the boot settings."
FAILED_MSG = "Failed to update the boot settings."
UNSUPPORTED_MSG = "The system does not support the BootOptions feature."
JOB_WAIT_MSG = "The boot settings job is triggered successfully."
AUTH_ERROR_MSG = "Unable to communicate with iDRAC {0}. This may be due to one of the following: " \
                 "Incorrect username or password, unreachable iDRAC IP or a failure in TLS/SSL handshake."

BS_OVERRIDE_MODE = {"legacy": "Legacy", "uefi": "UEFI"}
BS_OVERRIDE_ENABLED = {"continuous": "Continuous", "disabled": "Disabled", "once": "Once"}
BS_OVERRIDE_TARGET = {"none": "None", "pxe": "Pxe", "floppy": "Floppy", "cd": "Cd",
                      "hdd": "Hdd", "bios_setup": "BiosSetup", "utilities": "Utilities",
                      "uefi_target": "UefiTarget", "sd_card": "SDCard", "uefi_http": "UefiHttp"}
RESET_TYPE = {"graceful_restart": "GracefulRestart", "force_restart": "ForceRestart", "none": None}


def get_response_attributes(module, idrac, res_id):
    resp = idrac.invoke_request("{0}/{1}".format(SYSTEM_URI, res_id), "GET")
    resp_data = resp.json_data["Boot"]
    resp_data.pop("Certificates", None)
    resp_data.pop("BootOrder@odata.count", None)
    resp_data.pop("BootSourceOverrideTarget@Redfish.AllowableValues", None)
    if resp_data.get("BootOptions") is None and module.params.get("boot_options") is not None:
        module.fail_json(msg=UNSUPPORTED_MSG)
    if resp.json_data.get("Actions") is not None:
        type_reset = resp.json_data["Actions"]["#ComputerSystem.Reset"]["ResetType@Redfish.AllowableValues"]
        if "GracefulRestart" not in type_reset:
            RESET_TYPE["graceful_restart"] = "ForceRestart"
    return resp_data


def get_existing_boot_options(idrac, res_id):
    resp = idrac.invoke_request(BOOT_OPTIONS_URI.format(res_id), "GET")
    resp_data = strip_substr_dict(resp.json_data)
    strip_members = []
    for each in resp_data["Members"]:
        strip_members.append(strip_substr_dict(each))
    resp_data["Members"] = strip_members
    return resp_data


def system_reset(module, idrac, res_id):
    reset_msg, track_failed, reset, reset_type, job_resp = "", False, True, module.params.get("reset_type"), {}
    if reset_type is not None and not reset_type == "none":
        data = {"ResetType": RESET_TYPE[reset_type]}
        reset, track_failed, reset_msg, job_resp = idrac_system_reset(idrac, res_id, payload=data, job_wait=True)
        if RESET_TYPE["graceful_restart"] == "ForceRestart":
            reset = True
        if reset_type == "force_restart" and RESET_TYPE["graceful_restart"] == "GracefulRestart":
            reset = True
    return reset, track_failed, reset_msg, job_resp


def get_scheduled_job(idrac, job_state=None):
    if job_state is None:
        job_state = ["Scheduled", "New", "Running"]
    is_job, job_type_name, progress_job = False, "BIOSConfiguration", []
    time.sleep(10)
    job_resp = idrac.invoke_request(JOB_URI, "GET")
    job_resp_member = job_resp.json_data["Members"]
    if job_resp_member:
        bios_config_job = list(filter(lambda d: d.get("JobType") in [job_type_name], job_resp_member))
        progress_job = list(filter(lambda d: d.get("JobState") in job_state, bios_config_job))
        if progress_job:
            is_job = True
    return is_job, progress_job


def configure_boot_options(module, idrac, res_id, payload):
    is_job, progress_job = get_scheduled_job(idrac)
    job_data, job_wait = {}, module.params["job_wait"]
    resp_data = get_response_attributes(module, idrac, res_id)
    override_mode = resp_data["BootSourceOverrideMode"]
    if module.params["reset_type"] == "none":
        job_wait = False
    if is_job:
        module.fail_json(msg=JOB_EXISTS)
    boot_seq_resp = idrac.invoke_request(BOOT_SEQ_URI.format(res_id), "GET")
    seq_key = "BootSeq" if override_mode == "Legacy" else "UefiBootSeq"
    boot_seq_data = boot_seq_resp.json_data["Attributes"][seq_key]
    [each.update({"Enabled": payload.get(each["Name"])}
                 ) for each in boot_seq_data if payload.get(each["Name"]) is not None]
    seq_payload = {"Attributes": {seq_key: boot_seq_data}, "@Redfish.SettingsApplyTime": {"ApplyTime": "OnReset"}}
    if seq_key == "UefiBootSeq":
        for i in range(len(boot_seq_data)):
            if payload.get(resp_data["BootOrder"][i]) is not None:
                boot_seq_data[i].update({"Enabled": payload.get(resp_data["BootOrder"][i])})
        seq_payload["Attributes"][seq_key] = boot_seq_data
    resp = idrac.invoke_request(PATCH_BOOT_SEQ_URI.format(res_id), "PATCH", data=seq_payload)
    if resp.status_code == 202:
        location = resp.headers["Location"]
        job_id = location.split("/")[-1]
        reset, track_failed, reset_msg, reset_job_resp = system_reset(module, idrac, res_id)
        if reset_job_resp:
            job_data = reset_job_resp.json_data
        if reset:
            job_resp, error_msg = wait_for_idrac_job_completion(idrac, JOB_URI_ID.format(job_id),
                                                                job_wait=job_wait,
                                                                wait_timeout=module.params["job_wait_timeout"])
            if error_msg:
                module.fail_json(msg=error_msg)
            job_data = job_resp.json_data
        else:
            module.fail_json(msg=reset_msg)
    return job_data


def apply_boot_settings(module, idrac, payload, res_id):
    job_data, job_wait = {}, module.params["job_wait"]
    if module.params["reset_type"] == "none":
        job_wait = False
    resp = idrac.invoke_request("{0}/{1}".format(SYSTEM_URI, res_id), "PATCH", data=payload)
    if resp.status_code == 200:
        reset, track_failed, reset_msg, reset_job_resp = system_reset(module, idrac, res_id)
        if reset_job_resp:
            job_data = reset_job_resp.json_data
        is_job, progress_job = get_scheduled_job(idrac)
        if is_job:
            if reset:
                job_resp, error_msg = wait_for_idrac_job_completion(idrac, JOB_URI_ID.format(progress_job[0]["Id"]),
                                                                    job_wait=job_wait,
                                                                    wait_timeout=module.params["job_wait_timeout"])
                if error_msg:
                    module.fail_json(msg=error_msg)
                job_data = job_resp.json_data
            else:
                module.fail_json(msg=reset_msg)
    return job_data


def configure_boot_settings(module, idrac, res_id):
    job_resp, diff_change, payload = {}, [], {"Boot": {}}
    boot_order = module.params.get("boot_order")
    override_mode = module.params.get("boot_source_override_mode")
    override_enabled = module.params.get("boot_source_override_enabled")
    override_target = module.params.get("boot_source_override_target")
    response = get_response_attributes(module, idrac, res_id)
    if boot_order is not None:
        exist_boot_order = response.get("BootOrder")
        invalid_boot_order = [bo for bo in boot_order if bo not in exist_boot_order]
        if invalid_boot_order:
            module.fail_json(msg=INVALID_BOOT_OPT.format("Invalid"), invalid_boot_order=invalid_boot_order)
        if not len(set(boot_order)) == len(boot_order):
            dup_order = boot_order[:]
            [dup_order.remove(bo) for bo in exist_boot_order if bo in dup_order]
            module.fail_json(msg=INVALID_BOOT_OPT.format("Duplicate"),
                             duplicate_boot_order=dup_order)
        if not len(boot_order) == len(exist_boot_order):
            module.fail_json(msg="Unable to complete the operation because all boot devices "
                                 "are required for this operation.")
        if not boot_order == exist_boot_order:
            payload["Boot"].update({"BootOrder": boot_order})
    if override_mode is not None and \
            (not BS_OVERRIDE_MODE.get(override_mode) == response.get("BootSourceOverrideMode")):
        payload["Boot"].update({"BootSourceOverrideMode": BS_OVERRIDE_MODE.get(override_mode)})
    if override_enabled is not None and \
            (not BS_OVERRIDE_ENABLED.get(override_enabled) == response.get("BootSourceOverrideEnabled")):
        payload["Boot"].update({"BootSourceOverrideEnabled": BS_OVERRIDE_ENABLED.get(override_enabled)})
    if override_target is not None and \
            (not BS_OVERRIDE_TARGET.get(override_target) == response.get("BootSourceOverrideTarget")):
        payload["Boot"].update({"BootSourceOverrideTarget": BS_OVERRIDE_TARGET.get(override_target)})
        uefi_override_target = module.params.get("uefi_target_boot_source_override")
        if override_target == "uefi_target" and not uefi_override_target == response.get("UefiTargetBootSourceOverride"):
            payload["Boot"].update({"UefiTargetBootSourceOverride": uefi_override_target})
    if module.check_mode and payload["Boot"]:
        module.exit_json(msg=CHANGES_MSG, changed=True)
    elif (module.check_mode or not module.check_mode) and not payload["Boot"]:
        module.exit_json(msg=NO_CHANGES_MSG)
    else:
        job_resp = apply_boot_settings(module, idrac, payload, res_id)
    return job_resp


def configure_idrac_boot(module, idrac, res_id):
    boot_options = module.params.get("boot_options")
    inv_boot_options, diff_change, payload, job_resp, boot_attr = [], [], {}, {}, {}
    if boot_options is not None:
        boot_option_data = get_existing_boot_options(idrac, res_id)
        for each in boot_options:
            attr_val = each["display_name"] if each.get("display_name") is not None else each.get("boot_option_reference")
            attr_key = "DisplayName" if each.get("display_name") is not None else "BootOptionReference"
            report = list(filter(lambda d: d[attr_key] in [attr_val], boot_option_data["Members"]))
            if not report:
                inv_boot_options.append(each)
            else:
                act_val = {"BootOptionEnabled": each["enabled"]}
                ext_val = {"BootOptionEnabled": report[0]["BootOptionEnabled"]}
                diff_change.append(bool(set(ext_val.items()) ^ set(act_val.items())))
                payload[report[0]["Id"]] = each["enabled"]
        if inv_boot_options:
            module.fail_json(msg=BOOT_OPT_ERROR_MSG.format("Invalid"), invalid_boot_options=inv_boot_options)
        if not len(payload) == len(boot_options):
            module.fail_json(msg=BOOT_OPT_ERROR_MSG.format("Duplicate"), duplicate_boot_options=boot_options)
        if module.check_mode and any(diff_change) is True:
            module.exit_json(msg=CHANGES_MSG, changed=True)
        elif (module.check_mode and all(diff_change) is False) or (not module.check_mode and not any(diff_change)):
            module.exit_json(msg=NO_CHANGES_MSG)
        else:
            job_resp = configure_boot_options(module, idrac, res_id, payload)
    else:
        job_resp = configure_boot_settings(module, idrac, res_id)
    return job_resp


def main():
    specs = {
        "boot_options": {
            "required": False, "type": "list", "elements": "dict",
            "options": {
                "boot_option_reference": {"required": False, "type": "str"},
                "display_name": {"required": False, "type": "str"},
                "enabled": {"required": True, "type": "bool"},
            },
            "mutually_exclusive": [("boot_option_reference", "display_name")],
            "required_one_of": [("boot_option_reference", "display_name")],
        },
        "boot_order": {"required": False, "type": "list", "elements": "str"},
        "boot_source_override_mode": {"required": False, "type": "str", "choices": ["legacy", "uefi"]},
        "boot_source_override_enabled": {"required": False, "type": "str",
                                         "choices": ["continuous", "disabled", "once"]},
        "boot_source_override_target": {"required": False, "type": "str",
                                        "choices": ["uefi_http", "sd_card", "uefi_target", "utilities", "bios_setup",
                                                    "hdd", "cd", "floppy", "pxe", "none"]},
        "uefi_target_boot_source_override": {"required": False, "type": "str"},
        "reset_type": {"required": False, "type": "str", "default": "graceful_restart",
                       "choices": ["graceful_restart", "force_restart", "none"]},
        "job_wait": {"required": False, "type": "bool", "default": True},
        "job_wait_timeout": {"required": False, "type": "int", "default": 900},
        "resource_id": {"required": False, "type": "str"}
    }
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        required_one_of=[["boot_options", "boot_order", "boot_source_override_mode",
                          "boot_source_override_enabled", "boot_source_override_target",
                          "uefi_target_boot_source_override"]],
        mutually_exclusive=[
            ("boot_options", "boot_order"), ("boot_options", "boot_source_override_mode"),
            ("boot_options", "boot_source_override_enabled"), ("boot_options", "boot_source_override_target"),
            ("boot_options", "uefi_target_boot_source_override")
        ],
        required_if=[
            ["boot_source_override_target", "uefi_target", ("uefi_target_boot_source_override",)],
        ],
        supports_check_mode=True,
    )
    try:
        with iDRACRedfishAPI(module.params, req_session=True) as idrac:
            res_id = module.params.get("resource_id")
            if not res_id:
                res_id, error_msg = get_system_res_id(idrac)
                if error_msg:
                    module.fail_json(msg=error_msg)
            job_resp = configure_idrac_boot(module, idrac, res_id)
            job_resp_data = strip_substr_dict(job_resp)
            boot_option_data = get_existing_boot_options(idrac, res_id)
            boot_attr = get_response_attributes(module, idrac, res_id)
            boot_attr["BootOptions"] = boot_option_data
            if job_resp_data and \
                    (job_resp_data.get("JobState") in ["Failed", "RebootFailed"] or
                     "failed" in job_resp_data.get("Message").lower()):
                module.fail_json(msg=FAILED_MSG, job=job_resp_data)
            if (not module.params["job_wait"] or module.params["reset_type"] == "none") and \
                    not job_resp_data.get("JobState") == "RebootCompleted":
                module.exit_json(msg=JOB_WAIT_MSG, job=job_resp_data, boot=boot_attr)
            module.exit_json(msg=SUCCESS_MSG, job=job_resp_data, boot=boot_attr, changed=True)
    except HTTPError as err:
        if err.code == 401:
            module.fail_json(msg=AUTH_ERROR_MSG.format(module.params["idrac_ip"]))
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=AUTH_ERROR_MSG.format(module.params["idrac_ip"]), unreachable=True)
    except (ImportError, ValueError, RuntimeError, SSLValidationError,
            ConnectionError, KeyError, TypeError, IndexError) as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
