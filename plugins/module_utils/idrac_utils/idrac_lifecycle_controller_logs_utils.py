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
LC_LOG_SERVICE_URI = '/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Lclog'
LC_LOG_ENTRIES_URI = '/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Lclog/Entries'
LC_LOG_ENTRIES_PAGE_SIZE = 100
LC_LOG_MAX_RETRIES = 3
LC_LOG_RETRY_BACKOFF_SECONDS = (1, 2, 4)
IDRAC9_MIN_FIRMWARE = "7.10.90.00"
IDRAC10_MIN_FIRMWARE = "1.20.50.50"
LC_LOG_SEVERITY_LEVELS = ("OK", "Warning", "Critical")

import copy
import datetime
import time

from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    remove_key, idrac_redfish_job_tracking, get_dynamic_uri)
ODATA_PATTERN = '(.*?)@odata'


def _version_tuple(version_str):
    """Convert a dotted version string into a tuple of integers for comparison."""
    return tuple(int(part) for part in version_str.split("."))


def validate_lc_log_firmware_version(idrac):
    """Validate the connected iDRAC firmware version supports LC log enhancements.

    Keyword arguments:
    idrac -- iDRAC Redfish connection handle.

    Raises:
    ValueError -- when the detected firmware version is below the minimum
        required version for the detected iDRAC generation (iDRAC9 or iDRAC10).
    """
    generation, firmware_version, hw_model = idrac.get_server_generation
    min_version = IDRAC10_MIN_FIRMWARE if hw_model == "iDRAC 10" else IDRAC9_MIN_FIRMWARE
    if firmware_version is None or _version_tuple(firmware_version) < _version_tuple(min_version):
        raise ValueError(
            "Detected iDRAC firmware version '{0}' does not meet the minimum required "
            "version '{1}' for LC log filtering and management operations.".format(
                firmware_version, min_version))


def check_lc_log_service_available(idrac):
    """Verify the LC Log Service is available and enabled on the connected iDRAC.

    Keyword arguments:
    idrac -- iDRAC Redfish connection handle.

    Raises:
    ValueError -- when the LC Log Service endpoint is unreachable or disabled.
    """
    try:
        response = idrac.invoke_request(method='GET', uri=LC_LOG_SERVICE_URI)
    except HTTPError as err:
        raise ValueError(
            "LC Log Service is unavailable: {0}. Verify the iDRAC firmware supports "
            "the Lclog service and that the endpoint is reachable.".format(err))
    if response.status_code != 200 or not response.json_data.get("ServiceEnabled", False):
        raise ValueError(
            "LC Log Service is not enabled on this iDRAC. Enable the Lclog service "
            "before running filtered queries or management operations.")


def fetch_lc_logs(idrac, date_start=None, date_end=None, severity=None,
                  category=None, message_contains=None, max_entries=None):
    """Fetch and filter LC log entries via streaming pagination.

    Keyword arguments:
    idrac -- iDRAC Redfish connection handle.
    date_start, date_end -- optional ISO 8601 date range bounds.
    severity -- optional list of severity values to include.
    category -- optional list of Dell OEM category values to include.
    message_contains -- optional case-insensitive substring to match on Message.
    max_entries -- optional circuit breaker limiting total entries scanned.

    Returns:
    List of LC log entry dictionaries that pass the configured filter pipeline.
    """
    validate_filter_params(date_start=date_start, date_end=date_end)
    entries = []
    for entry in paginate_lc_logs(idrac, max_entries=max_entries, date_start=date_start):
        if apply_filters(entry, date_start=date_start, date_end=date_end,
                         severity_list=severity, category_list=category,
                         message_contains=message_contains):
            entries.append(entry)
    return entries


def fetch_lc_log_metadata(idrac):
    """Return LC log service metadata without returning individual log entries.

    Keyword arguments:
    idrac -- iDRAC Redfish connection handle.

    Returns:
    Dict containing total_entries, oldest_entry_timestamp, newest_entry_timestamp,
    storage_utilization_pct, and severity_breakdown.
    """
    service_response = idrac.invoke_request(method='GET', uri=LC_LOG_SERVICE_URI)
    max_records = service_response.json_data.get("MaxNumberOfRecords") or 0
    severity_breakdown = {level: 0 for level in LC_LOG_SEVERITY_LEVELS}
    timestamps = []
    total_entries = 0
    for entry in paginate_lc_logs(idrac):
        total_entries += 1
        severity_value = entry.get("Severity")
        if severity_value in severity_breakdown:
            severity_breakdown[severity_value] += 1
        created = entry.get("Created")
        if created:
            timestamps.append(created)
    storage_utilization_pct = round((total_entries / max_records) * 100, 2) if max_records else 0.0
    return {
        "total_entries": total_entries,
        "oldest_entry_timestamp": min(timestamps) if timestamps else None,
        "newest_entry_timestamp": max(timestamps) if timestamps else None,
        "storage_utilization_pct": storage_utilization_pct,
        "severity_breakdown": severity_breakdown,
    }


def _parse_iso8601(timestamp):
    """Parse an ISO 8601 timestamp string into a datetime object.

    Keyword arguments:
    timestamp -- ISO 8601 formatted timestamp string, optionally suffixed with 'Z'.
    """
    normalized = timestamp.replace("Z", "+00:00") if timestamp.endswith("Z") else timestamp
    return datetime.datetime.fromisoformat(normalized)


def _invoke_with_retry(invoke_fn, max_retries=LC_LOG_MAX_RETRIES,
                       backoff_seconds=LC_LOG_RETRY_BACKOFF_SECONDS):
    """Invoke a callable with exponential backoff retry on transient failures.

    Keyword arguments:
    invoke_fn -- zero-argument callable performing the API request.
    max_retries -- maximum number of retry attempts.
    backoff_seconds -- sequence of sleep durations between retries.
    """
    attempt = 0
    last_error = None
    while attempt <= max_retries:
        try:
            return invoke_fn()
        except (ConnectionError, TimeoutError, OSError) as err:
            last_error = err
            if attempt >= max_retries:
                break
            time.sleep(backoff_seconds[min(attempt, len(backoff_seconds) - 1)])
            attempt += 1
    raise last_error


def paginate_lc_logs(idrac, base_uri=LC_LOG_ENTRIES_URI, page_size=LC_LOG_ENTRIES_PAGE_SIZE,
                     max_entries=None, date_start=None):
    """Stream LC log entries page-by-page using $skip-based pagination.

    Keyword arguments:
    idrac -- iDRAC Redfish connection handle.
    base_uri -- Redfish collection URI for LC log entries.
    page_size -- number of entries fetched per page.
    max_entries -- optional circuit breaker limiting total entries yielded.
    date_start -- optional ISO 8601 string; pagination stops once entries fall below it
        (entries are returned newest-first by the LC log service).

    Yields:
    Individual LC log entry dictionaries.
    """
    skip = 0
    yielded = 0
    date_start_dt = _parse_iso8601(date_start) if date_start else None
    while True:
        uri = "{0}?$skip={1}&$top={2}".format(base_uri, skip, page_size)
        response = _invoke_with_retry(lambda uri=uri: idrac.invoke_request(method='GET', uri=uri))
        members = response.json_data.get("Members", [])
        if not members:
            break
        for entry in members:
            if date_start_dt is not None:
                created = entry.get("Created")
                if created and _parse_iso8601(created) < date_start_dt:
                    return
            yield entry
            yielded += 1
            if max_entries is not None and yielded >= max_entries:
                return
        if len(members) < page_size:
            break
        skip += page_size


def date_filter(entry, date_start=None, date_end=None):
    """Filter an LC log entry by its Created timestamp against a date range."""
    created = entry.get("Created")
    if created is None:
        return False
    created_dt = _parse_iso8601(created)
    if date_start is not None and created_dt < _parse_iso8601(date_start):
        return False
    if date_end is not None and created_dt > _parse_iso8601(date_end):
        return False
    return True


def severity_filter(entry, severity_list=None):
    """Filter an LC log entry by its Severity field."""
    if not severity_list:
        return True
    return entry.get("Severity") in severity_list


def category_filter(entry, category_list=None):
    """Filter an LC log entry by its Dell OEM category."""
    if not category_list:
        return True
    category = entry.get("Oem", {}).get("Dell", {}).get("DellLCLogEntry", {}).get("Category")
    return category in category_list


def message_filter(entry, message_contains=None):
    """Filter an LC log entry by a case-insensitive substring match on Message."""
    if not message_contains:
        return True
    message = entry.get("Message") or ""
    return message_contains.lower() in message.lower()


def validate_filter_params(date_start=None, date_end=None):
    """Validate that date_end is not earlier than date_start.

    Raises:
    ValueError -- when date_end precedes date_start.
    """
    if date_start is not None and date_end is not None:
        if _parse_iso8601(date_end) < _parse_iso8601(date_start):
            raise ValueError("date_end must not be earlier than date_start.")


def apply_filters(entry, date_start=None, date_end=None, severity_list=None,
                  category_list=None, message_contains=None):
    """Apply the chainable filter pipeline to a single LC log entry.

    Returns:
    True if the entry passes all configured filters, False otherwise.
    """
    return (
        date_filter(entry, date_start=date_start, date_end=date_end)
        and severity_filter(entry, severity_list=severity_list)
        and category_filter(entry, category_list=category_list)
        and message_filter(entry, message_contains=message_contains)
    )


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
