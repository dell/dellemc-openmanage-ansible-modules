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
from typing import Optional, Dict, Any

from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    remove_key, idrac_redfish_job_tracking, get_dynamic_uri)
ODATA_PATTERN = '(.*?)@odata'


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

    def get_lc_log_metadata(self, idrac, module):
        """
        Get LC log service metadata including statistics.

        Args:
            idrac: iDRAC Redfish API client
            module: Ansible module instance

        Returns:
            dict: Metadata including total entries, timestamps, severity breakdown
        """
        metadata = {}

        try:
            # Get LC log service URI
            managers_details = get_dynamic_uri(
                self.idrac, MANAGER_URI, search_label='Members')
            if len(managers_details) > 0:
                manager_uri = managers_details[0].get("@odata.id", "")
                manager_data = idrac.invoke_request(method='GET', uri=manager_uri).json_data
                lc_service_uri = manager_data.get("Links", {}).get("Oem", {}).get("Dell", {}).get("DellLCService", {}).get("@odata.id", "")
                lc_service_data = idrac.invoke_request(method='GET', uri=lc_service_uri).json_data

                # Get log entries URI
                log_services_uri = manager_data.get("Links", {}).get("Oem", {}).get("Dell", {}).get("DellLCLogService", {}).get("@odata.id", "")
                if log_services_uri:
                    log_service_data = idrac.invoke_request(method='GET', uri=log_services_uri).json_data
                    entries_uri = log_service_data.get("Entries", {}).get("@odata.id", "")

                    if entries_uri:
                        # Get total entries count
                        total_entries = self._get_total_entries_count(idrac, entries_uri)
                        metadata["total_entries"] = total_entries

                        # Get oldest and newest timestamps
                        metadata["oldest_timestamp"] = self._get_oldest_entry_timestamp(idrac, entries_uri)
                        metadata["newest_timestamp"] = self._get_newest_entry_timestamp(idrac, entries_uri)

                        # Get severity breakdown
                        metadata["severity_breakdown"] = self._get_severity_breakdown(idrac, entries_uri)

                        # Get storage utilization
                        max_records = log_service_data.get('MaxNumberOfRecords', 0)
                        overwrite_policy = log_service_data.get('OverWritePolicy', 'Unknown')

                        storage_utilization = 0
                        if max_records > 0:
                            storage_utilization = (total_entries / max_records) * 100

                        metadata["storage_utilization_pct"] = round(storage_utilization, 2)
                        metadata["max_records"] = max_records
                        metadata["overwrite_policy"] = overwrite_policy

        except Exception as e:
            metadata["error"] = str(e)

        return metadata

    def _get_total_entries_count(self, idrac, entries_uri: str) -> int:
        """Get total number of LC log entries without fetching all entries."""
        try:
            uri = f"{entries_uri}?$top=0"
            response = idrac.invoke_request(uri, 'GET')
            response_data = response.json_data
            return response_data.get('Members@odata.count', 0)
        except Exception:
            return 0

    def _get_oldest_entry_timestamp(self, idrac, entries_uri: str) -> Optional[str]:
        """Get the oldest entry timestamp."""
        try:
            uri = f"{entries_uri}?$top=1&$orderby=Created asc"
            response = idrac.invoke_request(uri, 'GET')
            response_data = response.json_data
            entries = response_data.get('Members', [])
            if entries:
                return entries[0].get('Created')
        except Exception:
            pass
        return None

    def _get_newest_entry_timestamp(self, idrac, entries_uri: str) -> Optional[str]:
        """Get the newest entry timestamp."""
        try:
            uri = f"{entries_uri}?$top=1&$orderby=Created desc"
            response = idrac.invoke_request(uri, 'GET')
            response_data = response.json_data
            entries = response_data.get('Members', [])
            if entries:
                return entries[0].get('Created')
        except Exception:
            pass
        return None

    def _get_severity_breakdown(self, idrac, entries_uri: str) -> Dict[str, int]:
        """Get severity breakdown of log entries."""
        severity_counts = {"Critical": 0, "Warning": 0, "OK": 0, "Other": 0}

        try:
            # Fetch all entries (limit to 1000 for performance)
            uri = f"{entries_uri}?$top=1000"
            response = idrac.invoke_request(uri, 'GET')
            response_data = response.json_data
            entries = response_data.get('Members', [])

            for entry in entries:
                severity = entry.get('Severity', 'Other')
                if severity in severity_counts:
                    severity_counts[severity] += 1
                else:
                    severity_counts["Other"] += 1

        except Exception:
            pass

        return severity_counts
