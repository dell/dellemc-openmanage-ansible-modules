# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 9.12.2
# Copyright (C) 2022-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

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
INVALID_ID_MSG = "Unable to complete the operation because " + \
                 "the value `{0}` for the input  `{1}` parameter is invalid."
UNSUPPORTED_LC_STATUS_MSG = "Lifecycle controller status check is not supported."
LC_STATUS_MSG = "Lifecycle controller status check is {lc_status} after {retries} number of retries, Exiting.."
SYSTEM_ID = "System.Embedded.1"
MANAGER_ID = "iDRAC.Embedded.1"
SYSTEMS_URI = "/redfish/v1/Systems"
MANAGERS_URI = "/redfish/v1/Managers"
CHASSIS_URI = "/redfish/v1/Chassis"
IDRAC_RESET_URI = "/redfish/v1/Managers/{res_id}/Actions/Manager.Reset"
SYSTEM_RESET_URI = "/redfish/v1/Systems/{res_id}/Actions/ComputerSystem.Reset"
MANAGER_JOB_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs?$expand=*($levels=1)"
MANAGER_JOB_ID_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/{0}"
MANAGER_JOB_URI_10 = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs?$expand=*($levels=1)"
MANAGER_JOB_ID_URI_10 = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/{0}"
GET_IDRAC_FIRMWARE_VER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1?$select=FirmwareVersion"
HOSTNAME_REGEX = r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
OME_INFO = "ApplicationService/Info"
ODATA_ID = "@odata.id"
POWER_CHECK_RETRIES = 30
POWER_CHECK_INTERVAL = 10
GET_IDRAC_FIRMWARE_DETAILS_URI_10 = "/redfish/v1/UpdateService/Oem/Dell/DellSoftwareInventory?$select=Members"
GET_IDRAC_FIRMWARE_URI_10 = "/redfish/v1/UpdateService/Oem/Dell/DellSoftwareInventory"
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The value for the 'job_wait_timeout' parameter cannot be negative or zero."
INVALID_TIME_FORMAT_MSG = "Invalid value for time. Enter the value in positive integer."

import time
from datetime import datetime
from inspect import getfullargspec
import re
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible_collections.dellemc.openmanage.plugins.module_utils.\
    idrac_utils.info.firmware import IDRACFirmwareInfo
import logging
from ansible_collections.dellemc.openmanage.plugins.module_utils.logging_handler \
    import CustomRotatingFileHandler


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


def config_ipv6(hostname):
    ip_addr, port = hostname, None
    if hostname.count(':') == 1:
        ip_addr, port = hostname.split(':')
    if not re.match(HOSTNAME_REGEX, ip_addr):
        if ']:' in ip_addr:
            ip_addr, port = ip_addr.split(']:')
        ip_addr = ip_addr.strip('[]')
        ip_addr = compress_ipv6(ip_addr)
        if port is None or port == "":
            hostname = "[{0}]".format(ip_addr)
        else:
            hostname = "[{0}]:{1}".format(ip_addr, port)
    return hostname


def compress_ipv6(ipv6_long):
    groups = ipv6_long.split(':')
    temp = []
    for group in groups:
        group = re.sub(r'^0+', '', group)
        group = group.lower()
        if 0 == len(group):
            group = '0'
        temp.append(group)
    tempstr = ':'.join(temp)
    ipv6_short = re.sub(r'(:0)+', ':', tempstr, 1)
    return ipv6_short


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
        res_uri = membs[0].get(ODATA_ID)
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
        resp = idrac.invoke_request(SYSTEM_RESET_URI.format(res_id=res_id), 'POST', data=payload)
        if resp.status_code == 204:
            reset = True
            return reset, track_failed, reset_msg, job_resp
        time.sleep(10)
        if wait_time_sec:
            resp = idrac.invoke_request(MANAGER_JOB_URI_10, "GET")
            job = list(filter(lambda d: d["JobState"] in ["RebootPending", "RebootCompleted"], resp.json_data["Members"]))
            if job:
                job_resp, msg = wait_for_idrac_job_completion(idrac, MANAGER_JOB_ID_URI_10.format(job[0]["Id"]),
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
        res_uri = member[0].get(ODATA_ID)
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
            resp = redfish_obj.invoke_request("GET", get_job_uri(redfish_obj))
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


def get_dynamic_uri(idrac_obj, base_uri, search_label=''):
    args = getfullargspec(idrac_obj.invoke_request)[0]
    data = {'uri': base_uri} if 'uri' in args else {'path': base_uri}
    resp = idrac_obj.invoke_request(method='GET', **data).json_data
    if search_label:
        if search_label in resp:
            return resp[search_label]
        return None
    return resp


def get_scheduled_job_resp(idrac_obj, job_type):
    job_state = {"Scheduled", "New", "Running"}
    args = getfullargspec(idrac_obj.invoke_request)[0]
    data = {'uri': get_job_uri(idrac_obj)} if 'uri' in args else {'path': get_job_uri(idrac_obj)}
    job_list = idrac_obj.invoke_request(method="GET", **data).json_data.get('Members', [])
    if isinstance(job_type, str):
        job_resp = next((j for j in job_list if (j.get("JobState") in job_state) and (j.get("JobType") == job_type)), {})
    elif isinstance(job_type, list):
        job_resp = next((j for j in job_list if (j.get("JobState") in job_state) and (j.get("JobType") in job_type)), {})
    return remove_key(job_resp, regex_pattern='(.*?)@odata')


def delete_job(idrac_obj, job_id):
    resp = idrac_obj.invoke_request(uri=get_job_uri_id(idrac_obj).format(job_id), method="DELETE")
    return resp.json_data


def get_current_time(redfish_obj):
    res_id = get_manager_res_id(redfish_obj)
    resp = redfish_obj.invoke_request(MANAGERS_URI + '/' + res_id, "GET")
    curr_time = resp.json_data.get("DateTime")
    date_offset = resp.json_data.get("DateTimeLocalOffset")
    return curr_time, date_offset


def xml_data_conversion(attr_dict, fqdd=None, custom_payload_to_add=None):
    component = """<Component FQDD="{0}">{1}</Component>"""
    attr = ""
    for k, v in attr_dict.items():
        key = re.sub(r"\.(?!\d)", "#", k)
        attr += '<Attribute Name="{0}">{1}</Attribute>'.format(key, v)
    if custom_payload_to_add:
        attr += custom_payload_to_add
    root = component.format(fqdd, attr)
    return root


def validate_and_get_first_resource_id_uri(resource_id, idrac, base_uri):
    found = False
    res_id_uri = None
    if resource_id and not isinstance(resource_id, str):
        resource_id = resource_id.params.get('resource_id')
    res_id_members = get_dynamic_uri(idrac, base_uri, 'Members')
    for each in res_id_members:
        if resource_id and resource_id == each[ODATA_ID].split('/')[-1]:
            res_id_uri = each[ODATA_ID]
            found = True
            break
    if not found and resource_id:
        return res_id_uri, INVALID_ID_MSG.format(
            resource_id, 'resource_id')
    elif resource_id is None:
        res_id_uri = res_id_members[0][ODATA_ID]
    return res_id_uri, ''


def get_idrac_firmware_version(idrac):
    args = getfullargspec(idrac.invoke_request)[0]
    data = {'uri': GET_IDRAC_FIRMWARE_VER_URI} if 'uri' in args else {'path': GET_IDRAC_FIRMWARE_VER_URI}
    firm_version = idrac.invoke_request(method='GET', **data)
    return firm_version.json_data.get('FirmwareVersion', '')


def get_ome_version(ome_obj):
    resp = ome_obj.invoke_request('GET', OME_INFO)
    return resp.json_data.get("Version")


def trigger_restart_operation(idrac, restart_type="GracefulRestart", resource_id=None):
    resp, error_msg = {}, {}
    uri, error_msg = validate_and_get_first_resource_id_uri(resource_id, idrac, SYSTEMS_URI)
    if error_msg:
        return resp, error_msg
    actions_uri = get_dynamic_uri(idrac, uri, 'Actions').get("#ComputerSystem.Reset", {}).get("target", '')
    payload = {"ResetType": restart_type}
    resp = idrac.invoke_request(method='POST', uri=actions_uri, data=payload)
    return resp, error_msg


def wait_for_lc_status(idrac, job_wait_timeout=300, resource_id=None, interval=10):
    lc_status_completed, error_msg = False, ''
    lcstatus = ""
    retry_count = 1
    # LCStatus remain 'Ready' even after triggering restart
    # so waiting few seconds before loop
    waiting_before_lc_status_check = 12 * interval
    if job_wait_timeout >= waiting_before_lc_status_check:
        time.sleep(waiting_before_lc_status_check)
        job_wait_timeout = job_wait_timeout - waiting_before_lc_status_check
    max_idrac_reset_try = job_wait_timeout // interval
    uri, error_msg = validate_and_get_first_resource_id_uri(resource_id, idrac, MANAGERS_URI)
    if error_msg:
        return lc_status_completed, error_msg
    resp = get_dynamic_uri(idrac, uri, "Links")
    url = resp.get("Oem", {}).get("Dell", {}).get('DellLCService', {}).get(ODATA_ID, {})
    if url:
        action_resp = get_dynamic_uri(idrac, url)
        lc_url = action_resp.get('Actions', {}).get('#DellLCService.GetRemoteServicesAPIStatus', {}).get('target', {})
    else:
        return lc_status_completed, UNSUPPORTED_LC_STATUS_MSG
    lc_resp = idrac.invoke_request(lc_url, "POST", data="{}", dump=False)
    lcstatus = lc_resp.json_data.get('LCStatus')
    while retry_count < max_idrac_reset_try:
        try:
            lc_resp = idrac.invoke_request(lc_url, "POST", data="{}", dump=False)
            lcstatus = lc_resp.json_data.get('LCStatus')
            if lcstatus == 'Ready':
                lc_status_completed = True
                break
            time.sleep(interval)
            retry_count = retry_count + 1
        except URLError:
            time.sleep(interval)
            retry_count = retry_count + 1
            if retry_count == max_idrac_reset_try:
                error_msg = LC_STATUS_MSG.format(lc_status='unreachable', retries=max_idrac_reset_try)
                break
    if retry_count == max_idrac_reset_try and lcstatus != "Ready":
        error_msg = LC_STATUS_MSG.format(lc_status=lcstatus, retries=retry_count)
    return lc_status_completed, error_msg


def get_lc_log_or_current_log_time(idrac, curr_time=None, lc_log_ids_list=None, resource_id=None):
    lc_log_found = False
    msg = "No LC log found."

    uri, error_msg = validate_and_get_first_resource_id_uri(
        resource_id, idrac, MANAGERS_URI
    )
    if error_msg:
        return lc_log_found, error_msg

    log_services_uri = get_dynamic_uri(idrac, uri, "LogServices").get(
        ODATA_ID, {}
    )
    log_svc_member = get_dynamic_uri(idrac, log_services_uri, "Members")
    log_lc_uri = [
        each[ODATA_ID]
        for each in log_svc_member
        if each[ODATA_ID].split("/")[-1] == "Lclog"
    ][0]
    log_entries_uri = get_dynamic_uri(
        idrac, log_lc_uri, "Entries"
    ).get(ODATA_ID, {})

    try:
        resp = idrac.invoke_request(log_lc_uri, "GET")
        logs_list = idrac.invoke_request(log_entries_uri, "GET").json_data.get(
            "Members"
        )

        if not curr_time:
            curr_time = resp.json_data.get("DateTime")

        if not lc_log_ids_list:
            return curr_time

        for log in logs_list:
            if log.get("Created") >= curr_time:
                for err_id in lc_log_ids_list:
                    if err_id in log.get("MessageId"):
                        lc_log_found = True
                        msg = log.get("Message")
                        break

    except Exception:
        msg = "No LC log found."

    return lc_log_found, msg


def expand_ipv6(ip):
    sections = ip.split(':')
    num_sections = len(sections)
    double_colon_index = sections.index('') if '' in sections else -1
    if double_colon_index != -1:
        missing_sections = 8 - num_sections + 1
        sections[double_colon_index:double_colon_index + 1] = ['0000'] * missing_sections
    sections = [section.zfill(4) for section in sections]
    expanded_ip = ':'.join(sections)
    return expanded_ip


def cert_file_format_string(ip, prefix="",
                            postfix="",
                            datetime_format="%Y%m%d_%H%M%S"):
    now = datetime.now()
    hostname = expand_ipv6(ip).replace(":", ".")
    data = f"{prefix}{hostname}_{now.strftime(datetime_format)}{postfix}"
    return data


def track_power_state(idrac, base_uri, desired_state, retries=POWER_CHECK_RETRIES, interval=POWER_CHECK_INTERVAL):
    count = retries
    while count:
        ps = get_power_state(idrac, base_uri)
        if ps in desired_state:
            achieved = True
            break
        else:
            time.sleep(interval)
        count = count - 1
    else:
        achieved = False
    return achieved


def get_power_state(idrac, base_uri):
    retries = 10
    pstate = "Unknown"
    while retries > 0:
        try:
            resp = idrac.invoke_request(base_uri, "GET")
            pstate = resp.json_data.get("PowerState")
            break
        except Exception:
            retries = retries - 1
    return pstate


def power_act_host(idrac, system_uri, p_state):
    try:
        _resp, error_msg = {}, {}
        uri, error_msg = validate_and_get_first_resource_id_uri(None, idrac, system_uri)
        if error_msg:
            return False
        actions_uri = get_dynamic_uri(idrac, uri, 'Actions').get("#ComputerSystem.Reset", {}).get("target", '')
        idrac.invoke_request(actions_uri, "POST", data={'ResetType': p_state})
        p_act = True
    except HTTPError:
        p_act = False
    return p_act


def reset_host(idrac, restart_type, system_uri, base_uri):
    p_state = 'On'
    ps = get_power_state(idrac, base_uri)
    on_state = ["On"]
    if ps in on_state:
        p_state = 'GracefulShutdown'
        if 'Force' in restart_type:
            p_state = 'ForceOff'
        p_act = power_act_host(idrac, system_uri, p_state)
        if not p_act:
            return False
        state_achieved = track_power_state(idrac, base_uri, ["Off"])
        p_state = "On"
        if not state_achieved:
            time.sleep(10)
            p_state = "ForceRestart"
    p_act = power_act_host(idrac, system_uri, p_state)
    if not p_act:
        return False
    state_achieved = track_power_state(idrac, base_uri, on_state)
    return state_achieved


def validate_job_wait(module):
    """
    Validates job_wait and job_wait_timeout parameters.
    :param module: The Ansible module instance.
    :param job_wait_param: The name of the job wait parameter to check (default is "job_wait").
    :param job_wait_timeout_param: The name of the job wait timeout parameter to check (default is "job_wait_timeout").
    """
    job_wait = module.params.get('job_wait')
    job_wait_timeout = module.params.get('job_wait_timeout')

    if job_wait and (job_wait_timeout is None or job_wait_timeout <= 0):
        return True

    return False


def validate_time(time, module):
    # Ensure the time is a string (or cast it to a string if it's not)
    if not isinstance(time, str):
        module.exit_json(msg="Time must be a string in HH:MM format", failed=True)

    # Check if the time matches the 24-hour format (HH:MM)
    if time and not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", time):
        module.exit_json(msg=INVALID_TIME_FORMAT_MSG, failed=True)


def get_job_uri_id(rest_obj):
    firmware_obj = IDRACFirmwareInfo(rest_obj)
    job_uri_id = MANAGER_JOB_ID_URI
    if not firmware_obj.is_omsdk_required():
        job_uri_id = MANAGER_JOB_ID_URI_10
    return job_uri_id


def get_job_uri(rest_obj):
    firmware_obj = IDRACFirmwareInfo(rest_obj)
    job_uri = MANAGER_JOB_URI
    if not firmware_obj.is_omsdk_required():
        job_uri = MANAGER_JOB_URI_10
    return job_uri


def get_logger(module_name, log_file_name='ansible_openmanage.log',
               log_devel=logging.INFO):
    FORMAT = '%(asctime)-15s %(filename)s %(levelname)s : %(message)s'
    max_bytes = 5 * 1024 * 1024
    logging.basicConfig(filename=log_file_name, format=FORMAT)
    LOG = logging.getLogger(module_name)
    LOG.setLevel(log_devel)
    handler = CustomRotatingFileHandler(log_file_name,
                                        maxBytes=max_bytes,
                                        backupCount=5)
    formatter = logging.Formatter(FORMAT)
    handler.setFormatter(formatter)
    LOG.addHandler(handler)
    LOG.propagate = False
    return LOG
