# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 8.2.0
# Copyright (C) 2022-2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:

#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.

#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

CHANGES_MSG = "Changes found to be applied."
NO_CHANGES_MSG = "No changes found to be applied."
RESET_UNTRACK = "iDRAC reset is in progress. Until the iDRAC is reset, the changes would not apply."
RESET_SUCCESS = "iDRAC has been reset successfully."
RESET_FAIL = "Unable to reset the iDRAC. For changes to reflect, manually reset the iDRAC."
SYSTEM_ID = "System.Embedded.1"
MANAGER_ID = "iDRAC.Embedded.1"
SYSTEMS_URI = "/redfish/v1/Systems"
MANAGERS_URI = "/redfish/v1/Managers"
IDRAC_RESET_URI = "/redfish/v1/Managers/{res_id}/Actions/Manager.Reset"
SYSTEM_RESET_URI = "/redfish/v1/Systems/{res_id}/Actions/ComputerSystem.Reset"
MANAGER_JOB_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs?$expand=*($levels=1)"
MANAGER_JOB_ID_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/{0}"


import time
from datetime import datetime
import re
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError


def strip_substr_dict(odata_dict, chkstr='@odata.', case_sensitive=False):
    '''
    :param odata_dict: the dict to be stripped of unwanted keys
    :param chkstr: the substring to be checked among the keys
    :param case_sensitive: should the match be case sensitive or not
    :return: dict
    '''
    cp = odata_dict.copy()
    klist = cp.keys()
    if not case_sensitive:
        chkstr = chkstr.lower()
    for k in klist:
        if case_sensitive:
            lk = k
        else:
            lk = str(k).lower()
        if chkstr in lk:
            odata_dict.pop(k, None)
    return odata_dict


def job_tracking(rest_obj, job_uri, max_job_wait_sec=600, job_state_var=('LastRunStatus', 'Id'),
                 job_complete_states=(2060, 2020, 2090), job_fail_states=(2070, 2101, 2102, 2103),
                 job_running_states=(2050, 2040, 2030, 2100),
                 sleep_interval_secs=10, max_unresponsive_wait=30, initial_wait=1):
    '''
    :param rest_obj: the rest_obj either of the below
    ansible_collections.dellemc.openmanage.plugins.module_utils.ome.RestOME
    :param job_uri: the uri to fetch the job response dict
    :param max_job_wait_sec: max time the job will wait
    :param job_state_var: The nested dict traversal path
    :param job_complete_states:
    :param job_fail_states:
    :param job_running_states:
    :param sleep_interval_secs:
    :param max_unresponsive_wait:
    :param initial_wait:
    :return:
    '''
    # ome_job_status_map = {
    #     2020: "Scheduled", 2030: "Queued", 2040: "Starting", 2050: "Running", 2060: "completed successfully",
    #     2070: "Failed", 2090: "completed with errors", 2080: "New", 2100: "Aborted", 2101: "Paused", 2102: "Stopped",
    #     2103: "Canceled"
    # }
    # ensure job states are mutually exclusive
    max_retries = max_job_wait_sec // sleep_interval_secs
    unresp = max_unresponsive_wait // sleep_interval_secs
    loop_ctr = 0
    job_failed = True
    job_dict = {}
    wait_time = 0
    if set(job_complete_states) & set(job_fail_states):
        return job_failed, "Overlapping job states found.", job_dict, wait_time
    msg = "Job tracking started."
    time.sleep(initial_wait)
    while loop_ctr < max_retries:
        loop_ctr += 1
        try:
            job_resp = rest_obj.invoke_request('GET', job_uri)
            job_dict = job_resp.json_data
            job_status = job_dict
            for x in job_state_var:
                job_status = job_status.get(x, {})
            if job_status in job_complete_states:
                job_failed = False
                msg = "Job tracking completed."
                loop_ctr = max_retries
            elif job_status in job_fail_states:
                job_failed = True
                msg = "Job is in Failed state."
                loop_ctr = max_retries
            if job_running_states:
                if job_status in job_running_states:
                    time.sleep(sleep_interval_secs)
                    wait_time = wait_time + sleep_interval_secs
            else:
                time.sleep(sleep_interval_secs)
                wait_time = wait_time + sleep_interval_secs
        except Exception as err:
            if unresp:
                time.sleep(sleep_interval_secs)
                wait_time = wait_time + sleep_interval_secs
            else:
                job_failed = True
                msg = "Exception in job tracking " + str(err)
                break
            unresp = unresp - 1
    return job_failed, msg, job_dict, wait_time


def idrac_redfish_job_tracking(
        rest_obj, job_uri, max_job_wait_sec=600, job_state_var='JobState',
        job_complete_states=("Completed", "Downloaded", "CompletedWithErrors", "RebootCompleted"),
        job_fail_states=("Failed", "RebootFailed", "Unknown"),
        job_running_states=("Running", "RebootPending", "Scheduling", "Scheduled", "Downloading", "Waiting", "Paused",
                            "New", "PendingActivation", "ReadyForExecution"),
        sleep_interval_secs=10, max_unresponsive_wait=30, initial_wait=1):
    # idrac_redfish_job_sates = [ "New", "Scheduled", "Running", "Completed", "Downloading", "Downloaded",
    # "Scheduling", "ReadyForExecution", "Waiting", "Paused", "Failed", "CompletedWithErrors", "RebootPending",
    # "RebootFailed", "RebootCompleted", "PendingActivation", "Unknown"]
    max_retries = max_job_wait_sec // sleep_interval_secs
    unresp = max_unresponsive_wait // sleep_interval_secs
    loop_ctr = 0
    job_failed = True
    job_dict = {}
    wait_time = 0
    if set(job_complete_states) & set(job_fail_states):
        return job_failed, "Overlapping job states found.", job_dict, wait_time
    msg = "Job tracking started."
    time.sleep(initial_wait)
    while loop_ctr < max_retries:
        loop_ctr += 1
        try:
            job_resp = rest_obj.invoke_request(job_uri, 'GET')
            job_dict = job_resp.json_data
            job_status = job_dict
            job_status = job_status.get(job_state_var, "Unknown")
            if job_status in job_running_states:
                time.sleep(sleep_interval_secs)
                wait_time = wait_time + sleep_interval_secs
            elif job_status in job_complete_states:
                job_failed = False
                msg = "Job tracking completed."
                loop_ctr = max_retries
            elif job_status in job_fail_states:
                job_failed = True
                msg = "Job is in {0} state.".format(job_status)
                loop_ctr = max_retries
            else:  # unrecognised states, just wait
                time.sleep(sleep_interval_secs)
                wait_time = wait_time + sleep_interval_secs
        except Exception as err:
            if unresp:
                time.sleep(sleep_interval_secs)
                wait_time = wait_time + sleep_interval_secs
            else:
                job_failed = True
                msg = "Exception in job tracking " + str(err)
                break
            unresp = unresp - 1
    return job_failed, msg, job_dict, wait_time


def get_rest_items(rest_obj, uri="DeviceService/Devices", key="Id", value="Identifier", selector="value"):
    item_dict = {}
    resp = rest_obj.get_all_items_with_pagination(uri)
    if resp.get(selector):
        item_dict = dict((item.get(key), item.get(value)) for item in resp[selector])
    return item_dict


def get_item_and_list(rest_obj, name, uri, key='Name', value='value'):
    resp = rest_obj.invoke_request('GET', uri)
    tlist = []
    if resp.success and resp.json_data.get(value):
        tlist = resp.json_data.get(value, [])
        for xtype in tlist:
            if xtype.get(key, "") == name:
                return xtype, tlist
    return {}, tlist


def apply_diff_key(src, dest, klist):
    diff_cnt = 0
    for k in klist:
        v = src.get(k)
        if v is not None and v != dest.get(k):
            dest[k] = v
            diff_cnt = diff_cnt + 1
    return diff_cnt


def wait_for_job_completion(redfish_obj, uri, job_wait=True, wait_timeout=120, sleep_time=10):
    max_sleep_time = wait_timeout
    sleep_interval = sleep_time
    if job_wait:
        while max_sleep_time:
            if max_sleep_time > sleep_interval:
                max_sleep_time = max_sleep_time - sleep_interval
            else:
                sleep_interval = max_sleep_time
                max_sleep_time = 0
            time.sleep(sleep_interval)
            job_resp = redfish_obj.invoke_request("GET", uri)
            if job_resp.json_data.get("PercentComplete") == 100:
                time.sleep(10)
                return job_resp, ""
    else:
        job_resp = redfish_obj.invoke_request("GET", uri)
        time.sleep(10)
        return job_resp, ""
    return {}, "The job is not complete after {0} seconds.".format(wait_timeout)


def wait_after_idrac_reset(idrac, wait_time_sec, interval=30):
    time.sleep(interval // 2)
    msg = RESET_UNTRACK
    wait = wait_time_sec
    track_failed = True
    while wait > 0:
        try:
            idrac.invoke_request(MANAGERS_URI, 'GET')
            time.sleep(interval // 2)
            msg = RESET_SUCCESS
            track_failed = False
            break
        except Exception:
            time.sleep(interval)
            wait = wait - interval
    return track_failed, msg


# Can this be in idrac_redfish???
def reset_idrac(idrac_restobj, wait_time_sec=300, res_id=MANAGER_ID, interval=30):
    track_failed = True
    reset_msg = "iDRAC reset triggered successfully."
    try:
        idrac_restobj.invoke_request(IDRAC_RESET_URI.format(res_id=res_id), 'POST',
                                     data={"ResetType": "GracefulRestart"})
        if wait_time_sec:
            track_failed, reset_msg = wait_after_idrac_reset(idrac_restobj, wait_time_sec, interval)
        reset = True
    except Exception:
        reset = False
        reset_msg = RESET_FAIL
    return reset, track_failed, reset_msg


def get_manager_res_id(idrac):
    try:
        resp = idrac.invoke_request(MANAGERS_URI, "GET")
        membs = resp.json_data.get("Members")
        res_uri = membs[0].get('@odata.id')
        res_id = res_uri.split("/")[-1]
    except HTTPError:
        res_id = MANAGER_ID
    return res_id


def wait_for_idrac_job_completion(idrac, uri, job_wait=True, wait_timeout=120, sleep_time=10):
    max_sleep_time = wait_timeout
    sleep_interval = sleep_time
    job_msg = "The job is not complete after {0} seconds.".format(wait_timeout)
    if job_wait:
        while max_sleep_time:
            if max_sleep_time > sleep_interval:
                max_sleep_time = max_sleep_time - sleep_interval
            else:
                sleep_interval = max_sleep_time
                max_sleep_time = 0
            time.sleep(sleep_interval)
            job_resp = idrac.invoke_request(uri, "GET")
            if job_resp.json_data.get("PercentComplete") == 100:
                time.sleep(10)
                return job_resp, ""
            if job_resp.json_data.get("JobState") == "RebootFailed":
                time.sleep(10)
                return job_resp, job_msg
    else:
        job_resp = idrac.invoke_request(uri, "GET")
        time.sleep(10)
        return job_resp, ""
    return {}, "The job is not complete after {0} seconds.".format(wait_timeout)


def idrac_system_reset(idrac, res_id, payload=None, job_wait=True, wait_time_sec=300, interval=30):
    track_failed, reset, job_resp = True, False, {}
    reset_msg = RESET_UNTRACK
    try:
        idrac.invoke_request(SYSTEM_RESET_URI.format(res_id=res_id), 'POST', data=payload)
        time.sleep(10)
        if wait_time_sec:
            resp = idrac.invoke_request(MANAGER_JOB_URI, "GET")
            job = list(filter(lambda d: d["JobState"] in ["RebootPending"], resp.json_data["Members"]))
            if job:
                job_resp, msg = wait_for_idrac_job_completion(idrac, MANAGER_JOB_ID_URI.format(job[0]["Id"]),
                                                              job_wait=job_wait, wait_timeout=wait_time_sec)
                if "job is not complete" in msg:
                    reset, reset_msg = False, msg
                if not msg:
                    reset = True
    except Exception:
        reset = False
        reset_msg = RESET_FAIL
    return reset, track_failed, reset_msg, job_resp


def get_system_res_id(idrac):
    res_id = SYSTEM_ID
    error_msg = ""
    try:
        resp = idrac.invoke_request(SYSTEMS_URI, "GET")
    except HTTPError:
        error_msg = "Unable to complete the request because the resource URI " \
                    "does not exist or is not implemented."
    else:
        member = resp.json_data.get("Members")
        res_uri = member[0].get('@odata.id')
        res_id = res_uri.split("/")[-1]
    return res_id, error_msg


def get_all_data_with_pagination(ome_obj, uri, query_param=None):
    """To get all the devices with pagination based on the filter provided."""
    query, resp, report_list = "", None, []
    try:
        resp = ome_obj.invoke_request('GET', uri, query_param=query_param)
        next_uri = resp.json_data.get("@odata.nextLink", None)
        report_list = resp.json_data.get("value")
        if query_param is not None:
            for k, v in query_param.items():
                query += "{0}={1}".format(k, v.replace(" ", "%20"))
        while next_uri is not None:
            next_uri_query = "{0}&{1}".format(next_uri.strip("/api"), query) if query else next_uri.strip("/api")
            resp = ome_obj.invoke_request('GET', next_uri_query)
            report_list.extend(resp.json_data.get("value"))
            next_uri = resp.json_data.get("@odata.nextLink", None)
    except (URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError) as err:
        raise err
    return {"resp_obj": resp, "report_list": report_list}


def remove_key(data, regex_pattern='@odata.'):
    '''
    :param data: the dict/list to be stripped of unwanted keys
    :param remove_char: the substring to be checked among the keys
    :return: dict/list
    '''
    try:
        if isinstance(data, dict):
            for key in list(data.keys()):
                if re.match(regex_pattern, key):
                    data.pop(key, None)
                else:
                    remove_key(data[key], regex_pattern)
        elif isinstance(data, list):
            for item in data:
                remove_key(item, regex_pattern)
    except Exception:
        pass
    return data


def wait_for_redfish_reboot_job(redfish_obj, res_id, payload=None, wait_time_sec=300):
    reset, job_resp, msg = False, {}, ""
    try:
        resp = redfish_obj.invoke_request('POST', SYSTEM_RESET_URI.format(res_id=res_id), data=payload, api_timeout=120)
        time.sleep(10)
        if wait_time_sec and resp.status_code == 204:
            resp = redfish_obj.invoke_request("GET", MANAGER_JOB_URI)
            reboot_job_lst = list(filter(lambda d: (d["JobType"] in ["RebootNoForce"]), resp.json_data["Members"]))
            job_resp = max(reboot_job_lst, key=lambda d: datetime.strptime(d["StartTime"], "%Y-%m-%dT%H:%M:%S"))
            if job_resp:
                reset = True
            else:
                msg = RESET_FAIL
    except Exception:
        reset = False
    return job_resp, reset, msg


def wait_for_redfish_job_complete(redfish_obj, job_uri, job_wait=True, wait_timeout=120, sleep_time=10):
    max_sleep_time = wait_timeout
    sleep_interval = sleep_time
    job_msg = "The job is not complete after {0} seconds.".format(wait_timeout)
    job_resp = {}
    if job_wait:
        while max_sleep_time:
            if max_sleep_time > sleep_interval:
                max_sleep_time = max_sleep_time - sleep_interval
            else:
                sleep_interval = max_sleep_time
                max_sleep_time = 0
            time.sleep(sleep_interval)
            job_resp = redfish_obj.invoke_request("GET", job_uri, api_timeout=120)
            if job_resp.json_data.get("PercentComplete") == 100:
                time.sleep(10)
                return job_resp, ""
            if job_resp.json_data.get("JobState") == "RebootFailed":
                time.sleep(10)
                return job_resp, job_msg
    else:
        time.sleep(10)
        job_resp = redfish_obj.invoke_request("GET", job_uri, api_timeout=120)
        return job_resp, ""
    return job_resp, job_msg
