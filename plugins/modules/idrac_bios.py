#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.6.0
# Copyright (C) 2018-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_bios
short_description: Modify and clear BIOS attributes, reset BIOS settings, and configure boot sources
version_added: "2.1.0"
description:
    - This module allows to modify the BIOS attributes. Also clears pending BIOS attributes and resets BIOS to default settings.
    - Boot sources can be enabled or disabled. Boot sequence can be configured.
extends_documentation_fragment:
    - dellemc.openmanage.idrac_auth_options
options:
    apply_time:
        type: str
        description:
          - Apply time of the I(attributes).
          - This is applicable only to I(attributes).
          - "C(Immediate) Allows the user to immediately reboot the host and apply the changes. I(job_wait)
          is applicable."
          - C(OnReset) Allows the user to apply the changes on the next reboot of the host server.
          - "C(AtMaintenanceWindowStart) Allows the user to apply at the start of a maintenance window as specified
          in I(maintenance_window). A reboot job will be scheduled."
          - "C(InMaintenanceWindowOnReset) Allows to apply after a manual reset but within the maintenance window as
          specified in I(maintenance_window)."
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
               required: true
    attributes:
        type: dict
        description:
          - "Dictionary of BIOS attributes and value pair. Attributes should be
          part of the Redfish Dell BIOS Attribute Registry. Use
          U(https://I(idrac_ip)/redfish/v1/Systems/System.Embedded.1/Bios) to view the Redfish URI."
          - This is mutually exclusive with I(clear_pending) and I(reset_bios).
    clear_pending:
        type: bool
        description:
          - Allows the user to clear all pending BIOS attributes changes.
          - C(true) will discard any pending changes to bios attributes or remove job if in scheduled state.
          - This operation will not create any job.
          - C(false) will not perform any operation.
          - This is mutually exclusive with I(attributes) and I(reset_bios).
    reset_bios:
        type: bool
        description:
          - Resets the BIOS to default settings and triggers a reboot of host system.
          - This is applied to the host after the restart.
          - This operation will not create any job.
          - C(false) will not perform any operation.
          - This is mutually exclusive with I(attributes), I(clear_pending), and I(boot_sources).
          - When C(true), this action will always report as changes found to be applicable.
    boot_sources:
        type: list
        elements: dict
        description:
          - Options to enable or disable the boot sources.
          - This is mutually exclusive with I(attributes), I(clear_pending), and I(reset_bios).
        suboptions:
          Name:
            type: str
            required: true
            description: FQDD of the boot device.
          Enabled:
            type: bool
            description: Enable or disable the boot device.
          Index:
            type: int
            description: Boot index of the device.
    reset_type:
        type: str
        description:
          - C(force_restart) Forcefully reboot the host system.
          - C(graceful_restart) Gracefully reboot the host system.
          - This is applicable for I(reset_bios), and I(attributes) when I(apply_time) is C(Immediate).
        choices: [graceful_restart, force_restart]
        default: graceful_restart
    job_wait:
        type: bool
        description:
          - Provides the option to wait for job completion.
          - This is applicable for I(attributes) when I(apply_time) is C(Immediate).
        default: true
    job_wait_timeout:
        type: int
        description:
          - The maximum wait time of I(job_wait) in seconds. The job is tracked only for this duration.
          - This option is applicable when I(job_wait) is C(true).
        default: 1200
requirements:
    - "python >= 3.9.6"
author:
    - "Felix Stephen (@felixs88)"
    - "Anooja Vardhineni (@anooja-vardhineni)"
    - "Jagadeesh N V (@jagadeeshnv)"
    - "Shivam Sharma (@shivam-sharma)"
notes:
    - This module requires 'Administrator' privilege for I(idrac_user).
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports both IPv4 and IPv6 address for I(idrac_ip).
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Configure generic attributes of the BIOS
  dellemc.openmanage.idrac_bios:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    attributes:
      BootMode: "Bios"
      OneTimeBootMode: "Enabled"
      BootSeqRetry: "Enabled"

- name: Configure PXE generic attributes
  dellemc.openmanage.idrac_bios:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    attributes:
      PxeDev1EnDis: "Enabled"
      PxeDev1Protocol: "IPV4"
      PxeDev1VlanEnDis: "Enabled"
      PxeDev1VlanId: 1
      PxeDev1Interface: "NIC.Embedded.1-1-1"
      PxeDev1VlanPriority: 2

- name: Configure BIOS attributes at Maintenance window
  dellemc.openmanage.idrac_bios:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    apply_time: AtMaintenanceWindowStart
    maintenance_window:
      start_time: "2022-09-30T05:15:40-05:00"
      duration: 600
    attributes:
      BootMode: "Bios"
      OneTimeBootMode: "Enabled"
      BootSeqRetry: "Enabled"

- name: Clear pending BIOS attributes
  dellemc.openmanage.idrac_bios:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    clear_pending: true

- name: Reset BIOS attributes to default settings.
  dellemc.openmanage.idrac_bios:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    validate_certs: false
    reset_bios: true

- name: Configure Boot Sources
  dellemc.openmanage.idrac_bios:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    boot_sources:
      - Name: "NIC.Integrated.1-1-1"
        Enabled: true
        Index: 1
      - Name: "NIC.Integrated.1-1-2"
        Enabled: true
        Index: 0
"""

RETURN = """
---
status_msg:
    description: Overall status of the bios operation.
    returned: success
    type: str
    sample: Successfully cleared pending BIOS attributes.
msg:
    description: Status of the action performed on bios.
    returned: success
    type: dict
    sample: {
       "CompletionTime": "2020-04-20T18:50:20",
       "Description": "Job Instance",
       "EndTime": null,
       "Id": "JID_873888162305",
       "JobState": "Completed",
       "JobType": "ImportConfiguration",
       "Message": "Successfully imported and applied Server Configuration Profile.",
       "MessageArgs": [],
       "MessageId": "SYS053",
       "Name": "Import Configuration",
       "PercentComplete": 100,
       "StartTime": "TIME_NOW",
       "Status": "Success",
       "TargetSettingsURI": null,
       "retval": true
    }
invalid_attributes:
  type: dict
  description: Dict of invalid attributes provided.
  returned: on invalid attributes or values.
  sample: {
        "PxeDev1VlanId": "Not a valid integer.",
        "AcPwrRcvryUserDelay": "Integer out of valid range.",
        "BootSeqRetry": "Invalid value for Enumeration.",
        "Proc1Brand": "Read only Attribute cannot be modified.",
        "AssetTag": "Attribute does not exist."
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
"""

SYSTEM_URI = "/redfish/v1/Systems/System.Embedded.1"
MANAGER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"
BIOS_URI = "/redfish/v1/Systems/System.Embedded.1/Bios"
BIOS_REGISTRY = "/redfish/v1/Systems/System.Embedded.1/Bios/BiosRegistry"
CLEAR_PENDING_URI = "/redfish/v1/Systems/System.Embedded.1/Bios/Settings/Actions/Oem/DellManager.ClearPending"
RESET_BIOS_DEFAULT = "/redfish/v1/Systems/System.Embedded.1/Bios/Actions/Bios.ResetBios"
BIOS_SETTINGS = "/redfish/v1/Systems/System.Embedded.1/Bios/Settings"
POWER_HOST_URI = "/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset"
IDRAC_JOBS_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs"
iDRAC_JOBS_EXP = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs?$expand=*($levels=1)"
iDRAC_JOB_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/{job_id}"
BOOT_SEQ_URI = "/redfish/v1/Systems/System.Embedded.1/Oem/Dell/DellBootSources"
PATCH_BOOT_SEQ_URI = "/redfish/v1/Systems/System.Embedded.1/Oem/Dell/DellBootSources/Settings"
LOG_SERVICE_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Lclog"
iDRAC9_LC_LOG = "/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Lclog/Entries"
iDRAC8_LC_LOG = "/redfish/v1/Managers/iDRAC.Embedded.1/Logs/Lclog"
LC_LOG_FILTER = "?$filter=MessageId%20eq%20'UEFI0157'"
CPU_RST_FILTER = "?$filter=MessageId%20eq%20'SYS1003'"
BIOS_JOB_RUNNING = "BIOS Config job is running. Wait for the job to complete."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_MSG = "Changes found to be applied."
SUCCESS_CLEAR = "Successfully cleared the pending BIOS attributes."
SUCCESS_COMPLETE = "Successfully applied the BIOS attributes update."
SUCCESS_BOOT_SOURCES = "Successfully configured the boot sources."
SCHEDULED_SUCCESS = "Successfully scheduled the job for the BIOS attributes update."
COMMITTED_SUCCESS = "Successfully committed changes. The job is in pending state. The changes will be applied {0}"
RESET_TRIGGERRED = "Reset BIOS action triggered successfully."
HOST_RESTART_FAILED = "Unable to restart the host. Check the host status and restart the host manually."
BIOS_RESET_TRIGGERED = "The BIOS reset action has been triggered successfully. The host reboot is complete."
BIOS_RESET_COMPLETE = "BIOS reset to defaults has been completed successfully."
BIOS_RESET_PENDING = "Pending attributes to be applied. " \
                     "Clear or apply the pending changes before resetting the BIOS."
FORCE_BIOS_DELETE = "The BIOS configuration job is scheduled. Use 'force' to delete the job."
INVALID_ATTRIBUTES_MSG = "The values specified for the attributes are invalid."
UNSUPPORTED_APPLY_TIME = "Apply time {0} is not supported."
MAINTENANCE_OFFSET = "The maintenance time must be post-fixed with local offset to {0}."
MAINTENANCE_TIME = "The specified maintenance time window occurs in the past, " \
                   "provide a future time to schedule the maintenance window."
NEGATIVE_TIMEOUT_MESSAGE = "The parameter job_wait_timeout value cannot be negative or zero."
POWER_CHECK_RETRIES = 30
POWER_CHECK_INTERVAL = 10
ODATA_REGEX = "(.*?)@odata"
AUTH_ERROR_MSG = "Unable to communicate with iDRAC {0}. This may be due to one of the following: " \
                 "Incorrect username or password, unreachable iDRAC IP or a failure in TLS/SSL handshake."
BOOT_SOURCES_INVALID = "Invalid boot_sources parameter. Each item must be a dict with 'Name' (required), 'Enabled' (bool), and 'Index' (int)."


import json
import time
from ansible.module_utils.common.dict_transformations import recursive_diff
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import idrac_auth_params
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import idrac_redfish_job_tracking, remove_key, \
    strip_substr_dict



def check_scheduled_bios_job(redfish_obj):
    job_resp = redfish_obj.invoke_request(iDRAC_JOBS_EXP, "GET")
    job_list = job_resp.json_data.get('Members', [])
    sch_jb = None
    jb_state = 'Unknown'
    for jb in job_list:
        if jb.get("JobType") == "BIOSConfiguration" and jb.get("JobState") in ["Scheduled", "Running", "Starting"]:
            sch_jb = jb['Id']
            jb_state = jb.get("JobState")
            break
    return sch_jb, jb_state


def delete_scheduled_bios_job(redfish_obj, job_id):
    resp = redfish_obj.invoke_request(iDRAC_JOB_URI.format(job_id=job_id), "DELETE")
    return resp


def get_pending_attributes(redfish_obj):
    try:
        resp = redfish_obj.invoke_request(BIOS_SETTINGS, "GET")
        attr = resp.json_data.get("Attributes")
    except Exception:
        attr = {}
    return attr


def get_power_state(redfish_obj):
    retries = 3
    pstate = "Unknown"
    while retries > 0:
        try:
            resp = redfish_obj.invoke_request(SYSTEM_URI, "GET")
            pstate = resp.json_data.get("PowerState")
            break
        except Exception:
            retries = retries - 1
    return pstate


def power_act_host(redfish_obj, p_state):
    try:
        redfish_obj.invoke_request(POWER_HOST_URI, "POST", data={'ResetType': p_state})
        p_act = True
    except HTTPError:
        p_act = False
    return p_act


def track_power_state(redfish_obj, desired_state, retries=POWER_CHECK_RETRIES, interval=POWER_CHECK_INTERVAL):
    count = retries
    while count:
        ps = get_power_state(redfish_obj)
        if ps in desired_state:
            achieved = True
            break
        else:
            time.sleep(interval)
        count = count - 1
    else:
        achieved = False
    return achieved


def reset_host(module, redfish_obj):
    reset_type = module.params.get('reset_type')
    p_state = 'On'
    ps = get_power_state(redfish_obj)
    on_state = ["On"]
    if ps in on_state:
        p_state = 'GracefulShutdown'
        if 'force' in reset_type:
            p_state = 'ForceOff'
        p_act = power_act_host(redfish_obj, p_state)
        if not p_act:
            module.exit_json(failed=True, status_msg=HOST_RESTART_FAILED)
        state_achieved = track_power_state(redfish_obj, ["Off"])  # 30x10= 300 secs
        p_state = "On"
        if not state_achieved:
            time.sleep(10)
            p_state = "ForceRestart"
    p_act = power_act_host(redfish_obj, p_state)
    if not p_act:
        module.exit_json(failed=True, status_msg=HOST_RESTART_FAILED)
    state_achieved = track_power_state(redfish_obj, on_state)  # 30x10= 300 secs
    return state_achieved


def get_current_time(redfish_obj):
    try:
        resp = redfish_obj.invoke_request(MANAGER_URI, "GET")
        curr_time = resp.json_data.get("DateTime")
        date_offset = resp.json_data.get("DateTimeLocalOffset")
    except Exception:
        return None, None
    return curr_time, date_offset


def track_log_entry(redfish_obj):
    msg = None
    filter_list = [LC_LOG_FILTER, CPU_RST_FILTER]
    intrvl = 15
    retries = 360 // intrvl
    time.sleep(intrvl)
    try:
        resp = redfish_obj.invoke_request(LOG_SERVICE_URI, "GET")
        uri = resp.json_data.get('Entries').get('@odata.id')
        fltr_uris = []
        for fltr in filter_list:
            fltr_uris.append("{0}{1}".format(uri, fltr))
        flen = len(fltr_uris)
        fln = 1
        pvt = retries // 3  # check for the SYS1003 after 2/3rds of retries
        curr_time = resp.json_data.get('DateTime')
        while retries:
            resp = redfish_obj.invoke_request(fltr_uris[retries % fln], "GET")
            logs_list = resp.json_data.get("Members")
            for log in logs_list:
                if log.get('Created') > curr_time:
                    msg = BIOS_RESET_COMPLETE
                    break
            if msg:
                break
            retries = retries - 1
            time.sleep(intrvl)
            if retries < pvt:
                fln = flen
        else:
            # msg = "{0}{1}".format(BIOS_RESET_TRIGGERED, "LOOPOVER")
            msg = BIOS_RESET_TRIGGERED
    except Exception:
        # msg = "{0}{1}".format(BIOS_RESET_TRIGGERED, str(ex))
        msg = BIOS_RESET_TRIGGERED
    return msg


def reset_bios(module, redfish_obj):
    attr = get_pending_attributes(redfish_obj)
    if attr:
        module.exit_json(status_msg=BIOS_RESET_PENDING, failed=True)
    if module.check_mode:
        module.exit_json(status_msg=CHANGES_MSG, changed=True)
    redfish_obj.invoke_request(RESET_BIOS_DEFAULT, "POST", data={}, dump=True)
    reset_success = reset_host(module, redfish_obj)
    if not reset_success:
        module.exit_json(failed=True, status_msg="{0} {1}".format(RESET_TRIGGERRED, HOST_RESTART_FAILED))
    log_msg = track_log_entry(redfish_obj)
    module.exit_json(status_msg=log_msg, changed=True)


def clear_pending_bios(module, redfish_obj):
    attr = get_pending_attributes(redfish_obj)
    if not attr:
        module.exit_json(status_msg=NO_CHANGES_MSG)
    job_id, job_state = check_scheduled_bios_job(redfish_obj)
    if job_id:
        if job_state in ["Running", "Starting"]:
            module.exit_json(failed=True, status_msg=BIOS_JOB_RUNNING, job_id=job_id)
        elif job_state in ["Scheduled", "Scheduling"]:
            # if module.params.get("force", True) == False:
            #     module.exit_json(status_msg=FORCE_BIOS_DELETE, job_id=job_id, failed=True)
            if module.check_mode:
                module.exit_json(status_msg=CHANGES_MSG, changed=True)
            delete_scheduled_bios_job(redfish_obj, job_id)
            module.exit_json(status_msg=SUCCESS_CLEAR, changed=True)
    if module.check_mode:
        module.exit_json(status_msg=CHANGES_MSG, changed=True)
    redfish_obj.invoke_request(CLEAR_PENDING_URI, "POST", data="{}", dump=False)
    module.exit_json(status_msg=SUCCESS_CLEAR, changed=True)


def get_attributes_registry(idrac):
    reggy = {}
    try:
        resp = idrac.invoke_request(BIOS_REGISTRY, "GET")
        attr_list = resp.json_data.get("RegistryEntries").get("Attributes")
        reggy = dict((x["AttributeName"], x) for x in attr_list)
    except Exception:
        reggy = {}
    return reggy


def check_bios_attributes_enum(val_dict, invalid, k, v):
    enum_type = val_dict.get("Type")
    if enum_type == "Enumeration":
        found = False
        for val in val_dict.get("Value", []):
            if v == val.get("ValueName"):
                found = True
                break
        if not found:
            invalid[k] = "Invalid value for enumeration."


def check_bios_attributes_int(val_dict, invalid, k, v):
    field_type = val_dict.get("Type")
    if field_type == "Integer":
        try:
            i = int(v)
        except Exception:
            invalid[k] = "Invalid integer."
        else:
            if not (val_dict.get("LowerBound") <= i <= val_dict.get("UpperBound")):
                invalid[k] = "Integer not in a valid range."


def validate_vs_registry(registry, attr_dict):
    invalid = {}
    for k, v in attr_dict.items():
        if k in registry:
            val_dict = registry.get(k)
            check_bios_attributes_enum(val_dict, invalid, k, v)
            check_bios_attributes_int(val_dict, invalid, k, v)
        else:
            invalid[k] = "The attribute does not exist."

    # Removing invalid keys from the payload
    if invalid:
        for k, v in invalid.items():
            del attr_dict[k]
    return invalid


def get_current_attributes(redfish_obj):
    try:
        resp = redfish_obj.invoke_request(BIOS_URI, "GET")
        setting = resp.json_data
    except Exception:
        setting = {}
    return setting


def validate_time(module, redfish_obj, mtime):
    curr_time, date_offset = get_current_time(redfish_obj)
    if not mtime.endswith(date_offset):
        module.exit_json(failed=True, status_msg=MAINTENANCE_OFFSET.format(date_offset))
    if mtime < curr_time:
        module.exit_json(failed=True, status_msg=MAINTENANCE_TIME)


def get_redfish_apply_time(module, redfish_obj, aplytm, rf_settings):
    rf_set = {}
    reboot_req = False
    if rf_settings:
        if 'Maintenance' in aplytm:
            if aplytm not in rf_settings:
                module.exit_json(failed=True, status_msg=UNSUPPORTED_APPLY_TIME.format(aplytm))
            else:
                rf_set['ApplyTime'] = aplytm
                m_win = module.params.get('maintenance_window')
                validate_time(module, redfish_obj, m_win.get('start_time'))
                rf_set['MaintenanceWindowStartTime'] = m_win.get('start_time')
                rf_set['MaintenanceWindowDurationInSeconds'] = m_win.get('duration')
        else:  # assuming OnReset is always
            if aplytm == "Immediate":
                if aplytm not in rf_settings:
                    reboot_req = True
                    aplytm = 'OnReset'
            rf_set['ApplyTime'] = aplytm
    return rf_set, reboot_req


def trigger_bios_job(redfish_obj):
    job_id = None
    payload = {"TargetSettingsURI": BIOS_SETTINGS}
    resp = redfish_obj.invoke_request(IDRAC_JOBS_URI, "POST", data=payload)
    job_id = resp.headers["Location"].split("/")[-1]
    return job_id


def apply_attributes(module, redfish_obj, pending, rf_settings):
    payload = {"Attributes": pending}
    aplytm = module.params.get('apply_time')
    rf_set, reboot_required = get_redfish_apply_time(module, redfish_obj, aplytm, rf_settings)
    if rf_set:
        payload["@Redfish.SettingsApplyTime"] = rf_set
    resp = redfish_obj.invoke_request(BIOS_SETTINGS, "PATCH", data=payload)
    if rf_set:
        redfish_obj.invoke_request(resp.headers["Location"], "GET")
        job_id = resp.headers["Location"].split("/")[-1]
    else:
        if aplytm == "Immediate":
            reboot_required = True
        job_id = trigger_bios_job(redfish_obj)
    return job_id, reboot_required


def check_pending_jobs(module, redfish_obj, pending):
    if pending:
        job_id, job_state = check_scheduled_bios_job(redfish_obj)
        if job_id:
            if job_state in ["Running", "Starting"]:
                module.exit_json(status_msg=BIOS_JOB_RUNNING, job_id=job_id, failed=True)
            elif job_state in ["Scheduled", "Scheduling"]:
                # changes staged in pending attributes
                # if module.params.get("force", True) == False:
                #     module.exit_json(status_msg=FORCE_BIOS_DELETE, job_id=job_id, failed=True)
                delete_scheduled_bios_job(redfish_obj, job_id)


def wait_for_job_completion(module, redfish_obj, reboot_required, job_id, invalid):
    if reboot_required and job_id:
        reset_success = reset_host(module, redfish_obj)
        if not reset_success:
            module.exit_json(status_msg="Attributes committed but reboot has failed {0}".format(HOST_RESTART_FAILED),
                             failed=True)
        if module.params.get("job_wait"):
            job_details = idrac_redfish_job_tracking(
                redfish_obj, iDRAC_JOB_URI.format(job_id=job_id),
                max_job_wait_sec=module.params.get('job_wait_timeout'))
            job_failed = job_details[0]
            msg = job_details[1]
            job_dict = job_details[2]
            if job_failed:
                module.exit_json(failed=True, status_msg=msg, job_id=job_id)
            module.exit_json(status_msg=SUCCESS_COMPLETE, job_id=job_id, msg=strip_substr_dict(job_dict), invalid_attributes=invalid, changed=True)
        else:
            module.exit_json(status_msg=SCHEDULED_SUCCESS, job_id=job_id, invalid_attributes=invalid, changed=True)


def attributes_config(module, redfish_obj):
    curr_resp = get_current_attributes(redfish_obj)
    curr_attr = curr_resp.get("Attributes", {})
    inp_attr = module.params.get("attributes")
    diff_tuple = recursive_diff(inp_attr, curr_attr)
    attr = {}
    if diff_tuple:
        if diff_tuple[0]:
            attr = diff_tuple[0]
    invalid = {}
    attr_registry = get_attributes_registry(redfish_obj)
    if attr_registry:
        invalid.update(validate_vs_registry(attr_registry, attr))
    if not attr:
        module.exit_json(status_msg=NO_CHANGES_MSG)
    if module.check_mode:
        module.exit_json(status_msg=CHANGES_MSG, changed=True)
    pending = get_pending_attributes(redfish_obj)
    pending.update(attr)
    check_pending_jobs(module, redfish_obj, pending)
    rf_settings = curr_resp.get("@Redfish.Settings", {}).get("SupportedApplyTimes", [])
    job_id, reboot_required = apply_attributes(module, redfish_obj, pending, rf_settings)
    wait_for_job_completion(module, redfish_obj, reboot_required, job_id, invalid)
    module.exit_json(status_msg=COMMITTED_SUCCESS.format(module.params.get('apply_time')),
                     job_id=job_id, invalid_attributes=invalid, changed=True)


def validate_negative_job_time_out(module):
    if module.params.get("job_wait_timeout") <= 0:
        module.fail_json(msg=NEGATIVE_TIMEOUT_MESSAGE)


def validate_boot_sources_params(boot_sources):
    """Validate boot_sources parameter format."""
    if not boot_sources:
        return None
    valid_keys = ['Name', 'Index', 'Enabled']
    for source in boot_sources:
        if not isinstance(source, dict):
            return BOOT_SOURCES_INVALID
        if 'Name' not in source:
            return BOOT_SOURCES_INVALID
        for key in source.keys():
            if key not in valid_keys:
                return BOOT_SOURCES_INVALID
        if 'Index' in source and not isinstance(source['Index'], int):
            return BOOT_SOURCES_INVALID
        if 'Enabled' in source and not isinstance(source['Enabled'], bool):
            return BOOT_SOURCES_INVALID
    return None


def configure_boot_sources(redfish_obj, boot_sources):
    """Configure boot sources using Redfish API."""
    resp = redfish_obj.invoke_request(BOOT_SEQ_URI, "GET")
    boot_seq_data = resp.json_data.get("Attributes", {})
    seq_key = None
    if "BootSeq" in boot_seq_data:
        seq_key = "BootSeq"
    elif "UefiBootSeq" in boot_seq_data:
        seq_key = "UefiBootSeq"
    else:
        return None, "Unable to determine boot sequence type from system."
    
    current_seq = boot_seq_data.get(seq_key, [])
    updated_seq = []
    changes_found = False
    
    # Build a lookup map from user input
    source_map = {}
    for source in boot_sources:
        source_map[source['Name']] = {'Enabled': source.get('Enabled'), 'Index': source.get('Index')}
    
    # Update boot sequence with user values
    for device in current_seq:
        device_name = device.get('Name')
        if device_name in source_map:
            user_source = source_map[device_name]
            if 'Enabled' in user_source and device.get('Enabled') != user_source['Enabled']:
                device['Enabled'] = user_source['Enabled']
                changes_found = True
            if 'Index' in user_source and device.get('Index') != user_source['Index']:
                device['Index'] = user_source['Index']
                changes_found = True
        updated_seq.append(device)
    
    if not changes_found:
        return None, NO_CHANGES_MSG
    
    payload = {"Attributes": {seq_key: updated_seq}, "@Redfish.SettingsApplyTime": {"ApplyTime": "OnReset"}}
    resp = redfish_obj.invoke_request(PATCH_BOOT_SEQ_URI, "PATCH", data=payload)
    if resp.status_code in [200, 202]:
        location = resp.headers.get("Location", "")
        if location:
            job_id = location.split("/")[-1]
            return job_id, SUCCESS_BOOT_SOURCES
        return None, SUCCESS_BOOT_SOURCES
    return None, "Failed to configure boot sources. HTTP status: {0}".format(resp.status_code)


def main():
    specs = {
        "attributes": {"type": 'dict'},
        "apply_time": {"type": 'str', "default": 'Immediate',
                       "choices": ['Immediate', 'OnReset', 'AtMaintenanceWindowStart', 'InMaintenanceWindowOnReset']},
        "maintenance_window": {"type": 'dict',
                               "options": {"start_time": {"type": 'str', "required": True},
                                           "duration": {"type": 'int', "required": True}}},
        "clear_pending": {"type": 'bool'},
        "reset_bios": {"type": 'bool'},
        "boot_sources": {"type": 'list', 'elements': 'dict'},
        "reset_type": {"type": 'str', "choices": ['graceful_restart', 'force_restart'], "default": 'graceful_restart'},
        "job_wait": {"type": 'bool', "default": True},
        "job_wait_timeout": {"type": 'int', "default": 1200}
    }
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[('attributes', 'clear_pending', 'reset_bios', 'boot_sources')],
        required_one_of=[('attributes', 'clear_pending', 'reset_bios', 'boot_sources')],
        required_if=[["apply_time", "AtMaintenanceWindowStart", ("maintenance_window",)],
                     ["apply_time", "InMaintenanceWindowOnReset", ("maintenance_window",)]],
        supports_check_mode=True)
    validate_negative_job_time_out(module)
    boot_sources = module.params.get("boot_sources")
    if boot_sources:
        validation_error = validate_boot_sources_params(boot_sources)
        if validation_error:
            module.fail_json(msg=validation_error, failed=True)
    try:
        with iDRACRedfishAPI(module.params, req_session=True) as redfish_obj:
            _handle_redfish_api(module, redfish_obj)
        module.exit_json(status_msg=NO_CHANGES_MSG)
    except HTTPError as err:
        filter_err = remove_key(json.load(err), regex_pattern=ODATA_REGEX)
        module.exit_json(msg=str(err), error_info=filter_err, failed=True)
    except URLError:
        module.exit_json(msg=AUTH_ERROR_MSG.format(module.params["idrac_ip"]), unreachable=True)
    except (ImportError, ValueError, RuntimeError, SSLValidationError,
            ConnectionError, KeyError, TypeError, IndexError) as e:
        module.exit_json(msg=str(e), failed=True)


def _handle_redfish_api(module, redfish_obj):
    if module.params.get("clear_pending"):
        clear_pending_bios(module, redfish_obj)
    if module.params.get("reset_bios"):
        reset_bios(module, redfish_obj)
    if module.params.get('attributes'):
        attributes_config(module, redfish_obj)
    if module.params.get('boot_sources'):
        boot_sources_config(module, redfish_obj)


def boot_sources_config(module, redfish_obj):
    """Handle boot sources configuration using Redfish API."""
    boot_sources = module.params.get('boot_sources')
    if module.check_mode:
        module.exit_json(status_msg=CHANGES_MSG, changed=True)
    job_id, status_msg = configure_boot_sources(redfish_obj, boot_sources)
    if status_msg == NO_CHANGES_MSG:
        module.exit_json(status_msg=status_msg)
    elif job_id:
        module.exit_json(status_msg=status_msg, job_id=job_id, changed=True)
    else:
        module.exit_json(status_msg=status_msg, failed=True)


if __name__ == '__main__':
    main()
