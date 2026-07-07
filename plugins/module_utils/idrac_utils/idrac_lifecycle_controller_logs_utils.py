# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 9.12.2
# Copyright (C) 2025 Dell Inc. or its subsidiaries. All Rights Reserved.

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

SUCCESS_MSG = "Successfully exported the lifecycle controller logs."
SCHEDULE_MSG = "The export lifecycle controller log job is submitted successfully."
NO_CHANGES_FOUND_MSG = "No changes found to be applied."
CHANGES_FOUND_MSG = "Changes found to be applied."
MANAGER_URI = '/redfish/v1/Managers'

import copy
import datetime
import time

from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    remove_key, idrac_redfish_job_tracking, get_dynamic_uri)
ODATA_PATTERN = '(.*?)@odata'
LC_LOG_PAGE_SIZE = 100
RETRYABLE_EXCEPTIONS = (ConnectionError, SSLValidationError, URLError, HTTPError)


def paginate_lc_logs(idrac, entries_uri, max_entries=None, date_start=None):
    """
    Stream LC log entries page-by-page using $skip-based pagination.

    Yields a list of entries for each page. Stops early if max_entries is
    reached, or if date_start is provided and entries fall below it
    (entries are assumed newest-first).

    Keyword arguments:
    idrac -- iDRAC handle
    entries_uri -- base URI for the LC log entries collection
    max_entries -- optional circuit breaker on total entries yielded
    date_start -- optional ISO 8601 string; pagination stops once
                  entry 'Created' timestamps fall below this value
    """
    skip = 0
    total_yielded = 0
    while True:
        query_uri = entries_uri if skip == 0 else "{0}?$skip={1}".format(entries_uri, skip)
        response = retry_with_backoff(idrac.invoke_request, method='GET', uri=query_uri)
        page = response.json_data.get("Members", [])
        if not page:
            break

        stop_index = None
        if date_start:
            for idx, entry in enumerate(page):
                if entry.get("Created", "") < date_start:
                    stop_index = idx
                    break
            if stop_index is not None:
                page = page[:stop_index]

        if max_entries is not None and total_yielded + len(page) > max_entries:
            page = page[:max_entries - total_yielded]

        if page:
            yield page
            total_yielded += len(page)

        if max_entries is not None and total_yielded >= max_entries:
            break
        if stop_index is not None:
            break

        next_link = response.json_data.get("Members@odata.nextLink")
        if not next_link:
            break
        skip += LC_LOG_PAGE_SIZE


def date_filter(entry, date_start=None, date_end=None):
    """Return True if entry's 'Created' timestamp falls within [date_start, date_end]."""
    created = entry.get("Created", "")
    if date_start and created < date_start:
        return False
    if date_end and created > date_end:
        return False
    return True


def severity_filter(entry, severity_list=None):
    """Return True if entry's 'Severity' is within severity_list."""
    if not severity_list:
        return True
    return entry.get("Severity") in severity_list


def category_filter(entry, category_list=None):
    """Return True if entry's Dell OEM category is within category_list."""
    if not category_list:
        return True
    category = entry.get("Oem", {}).get("Dell", {}).get("DellLCLogEntry", {}).get("Category")
    return category in category_list


def message_filter(entry, message_contains=None):
    """Return True if message_contains is a case-insensitive substring of entry's Message."""
    if not message_contains:
        return True
    message = entry.get("Message", "")
    return message_contains.lower() in message.lower()


def apply_filters(entries, filters):
    """
    Apply a chainable pipeline of filter callables to a list of entries.

    Keyword arguments:
    entries -- list of LC log entry dicts
    filters -- list of callables, each taking an entry and returning bool
    """
    if not filters:
        return entries
    return [entry for entry in entries if all(f(entry) for f in filters)]


def validate_date_range(date_start=None, date_end=None):
    """Raise ValueError if date_end is earlier than date_start."""
    if date_start and date_end and date_end < date_start:
        raise ValueError(
            "date_end ({0}) cannot be earlier than date_start ({1})".format(date_end, date_start))


def retry_with_backoff(func, *args, max_retries=3, backoff_seconds=(1, 2, 4), **kwargs):
    """
    Invoke func(*args, **kwargs), retrying on transient API failures with
    exponential backoff.

    Keyword arguments:
    func -- callable to invoke
    max_retries -- maximum number of attempts (default 3)
    backoff_seconds -- sleep durations between attempts (default 1s, 2s, 4s)
    """
    last_exc = None
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except RETRYABLE_EXCEPTIONS as exc:
            last_exc = exc
            if attempt < max_retries - 1:
                sleep_time = backoff_seconds[attempt] if attempt < len(backoff_seconds) else backoff_seconds[-1]
                time.sleep(sleep_time)
    raise last_exc


class IDRACLifecycleControllerLogs(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def get_file_name(self, module):
        file_name = None
        ip = copy.deepcopy(module.params.get("idrac_ip"))
        file_format = "{ip}_%Y%m%d_%H%M%S_LC_Log.log".format(ip=ip.replace(":", ".").replace("..", "."))
        current_date = datetime.datetime.now()
        current_date_str = current_date.strftime("%Y%m%d_%H%M%S")
        file_name = file_format.replace("%Y%m%d_%H%M%S", current_date_str)
        return file_name

    def get_share_details(self, module, idrac, sharename):
        ip_address = idrac.find_ip_address(sharename=sharename)
        file_name = self.get_file_name(module)
        if ip_address:
            if sharename.startswith("\\\\"):
                share_type = "CIFS"
                slash1 = "\\\\"
                slash2 = "\\"
                share_name = sharename.replace(slash1 + ip_address + slash2, "")
                file_path = module.params.get("share_name") + slash2 + file_name
            elif sharename.startswith(ip_address):
                share_type = "NFS"
                share_name = sharename.replace(ip_address + ":/", "")
                file_path = module.params.get("share_name") + "/" + file_name
        else:
            share_type = "Local"
            share_name = sharename
            file_path = module.params.get("share_name") + "/" + file_name

        return share_name, share_type, file_name, ip_address, file_path

    def export_logs_job_wait(self, idrac, module, job_uri, file_path):
        job_tracking_data = idrac_redfish_job_tracking(
            idrac, job_uri, sleep_interval_secs=1)
        job_failed = job_tracking_data[0]
        job_dict = job_tracking_data[2]
        job_dict["file"] = file_path
        job_dict = remove_key(job_dict, regex_pattern=ODATA_PATTERN)
        if job_failed:
            module.exit_json(
                msg=job_dict.get("Message"), job_status=job_dict, failed=True)
        if job_dict.get('JobState') == "Completed":
            msg = SUCCESS_MSG
            message_id = job_dict.get("MessageId")
            if message_id == "LC022":
                changed = False
            else:
                module.exit_json(msg=job_dict.get("Message"), failed=True)
        elif job_dict.get('JobState') is None:
            msg = SUCCESS_MSG
            changed = False
        else:
            msg = SCHEDULE_MSG
            changed = False
        job_dict["Return"] = "JobCreated"
        job_dict["Status"] = "Success"
        job_dict["Job"] = {
            "jobId": job_dict["Id"]
        }
        job_dict["JobStatus"] = job_dict["JobState"]
        job_dict = remove_key(job_dict,
                              regex_pattern=ODATA_PATTERN)
        return msg, job_dict, changed

    def create_local_file(self, module, file_path, job_resp_file):
        try:
            with open(file_path, "w") as log_file:
                log_file.write(str(job_resp_file.body))
        except FileNotFoundError:
            msg = "No such file or directory"
            module.exit_json(
                msg=msg, failed=True,
                lc_logs_status={}, changed=False)

    def export_local_logs(self, idrac, module, file_path, job_resp, final_data):
        job_resp_file = idrac.invoke_request(
            method='GET',
            uri=job_resp.headers.get("Location"), data=final_data)
        self.create_local_file(
            module=module,
            file_path=file_path,
            job_resp_file=job_resp_file)
        msg = SUCCESS_MSG
        changed = False
        job_dict = {
            "ElapsedTimeSinceCompletion": "0",
            "InstanceID": "",
            "JobStartTime": "NA",
            "JobStatus": "Completed",
            "JobUntilTime": "NA",
            "Message": "LCL Export was successful",
            "MessageArguments": "NA",
            "MessageID": "LC022",
            "Name": "LC Export",
            "PercentComplete": "100",
            "Status": "Success",
            "file": file_path,
            "retval": True
        }
        return msg, job_dict, changed

    def get_export_lc_logs_uri(self, idrac):
        managers_details = get_dynamic_uri(
            self.idrac, MANAGER_URI, search_label='Members')
        if len(managers_details) > 0:
            manager_uri = managers_details[0].get("@odata.id", "")
            manager_data = idrac.invoke_request(method='GET', uri=manager_uri).json_data
            lc_service_uri = manager_data.get("Links", {}).get("Oem", {}).get("Dell", {}).get("DellLCService", {}).get("@odata.id", "")
            lc_service_data = idrac.invoke_request(method='GET', uri=lc_service_uri).json_data
            lc_logs_uri = lc_service_data.get("Actions", {}).get("#DellLCService.ExportLCLog", {}).get("target", "")
            return lc_logs_uri

    def export_lc_logs_idrac_9_10(self, idrac, module, share_name, share_type, file_name, ip_address, file_path):
        changed = False
        payload_data = {
            "ShareName": share_name,
            "ShareType": share_type,
            "UserName": module.params.get("share_user"),
            "Password": module.params.get("share_password"),
            "FileName": file_name,
            "IPAddress": ip_address,
            "IgnoreCertWarning": "Off"
        }
        final_data = dict()
        for key in payload_data.keys():
            if payload_data[key] is not None:
                final_data[key] = payload_data[key]
        log_uri = self.get_export_lc_logs_uri(idrac=idrac)
        job_resp = idrac.invoke_request(method='POST', uri=log_uri, data=final_data)
        job_dict = {}
        if share_type == 'Local':
            msg, job_dict, changed = self.export_local_logs(idrac, module, file_path, job_resp, final_data)
        if (job_tracking_uri := job_resp.headers.get("Location")) and share_type != 'Local':
            job_id = job_tracking_uri.split("/")[-1]
            job_uri = idrac.get_job_uri().format(job_id=job_id)
            if module.params.get('job_wait'):
                msg, job_dict, changed = self.export_logs_job_wait(
                    idrac=idrac,
                    module=module,
                    job_uri=job_uri,
                    file_path=file_path)
            else:
                job_resp = idrac.invoke_request(job_uri, 'GET')
                job_dict = job_resp.json_data
                job_dict["file"] = file_path
                job_dict["Return"] = "JobCreated"
                job_dict["Status"] = "Success"
                job_dict["Job"] = {
                    "jobId": job_dict["Id"]
                }
                job_dict["JobStatus"] = job_dict["JobState"]
                job_dict = remove_key(
                    job_dict,
                    regex_pattern=ODATA_PATTERN)
                msg = SCHEDULE_MSG
                changed = False

        return msg, job_dict, changed

    def lifecycle_controller_logs_operation(self, idrac, module):
        share_name, share_type, file_name, ip_address, file_path = \
            self.get_share_details(
                module=module,
                idrac=idrac,
                sharename=module.params["share_name"])
        msg, job_dict, changed = self.export_lc_logs_idrac_9_10(
            idrac=idrac,
            module=module,
            share_name=share_name,
            share_type=share_type,
            file_name=file_name,
            ip_address=ip_address,
            file_path=file_path)
        return msg, job_dict, changed
