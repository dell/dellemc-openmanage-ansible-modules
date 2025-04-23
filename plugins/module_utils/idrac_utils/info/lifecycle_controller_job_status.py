# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 9.12.0
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


GET_IDRAC_LIFECYCLE_CONTROLLER_JOB_STATUS_INFO_10 = "/redfish/v1/Managers/iDRAC.Embedded.1"
NA = "Not Available"
odata = "@odata.id"


class IDRACLifecycleControllerJobStatusInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def transform_job_status_data(self, info_data):
        job_success_list = ['Completed', 'Success']
        job_failed_list = ['Failed', 'Errors']
        job_state = str(info_data.get("JobState", NA))
        if job_state in job_success_list:
            job_status = "Success"
        elif job_state in job_failed_list:
            job_status = "Failed"
        elif 'Message' in info_data and str(info_data.get("Message")) and \
                'completed' in str(info_data.get("Message")) and \
                'errors' not in str(info_data.get("Message")):
            job_status = "Success"
        else:
            job_status = "InProgress"

        if len(info_data.get("MessageArgs")) > 0:
            message_argument = str(info_data.get("MessageArgs")[0])
        else:
            message_argument = ""

        transformed_info_data = {
            "ElapsedTimeSinceCompletion": "",
            "InstanceID": str(info_data.get("Id", NA)),
            "JobStartTime": str(info_data.get("StartTime", NA)),
            "JobStatus": job_state,
            "JobUntilTime": "NA",
            "Message": str(info_data.get("Message", NA)),
            "MessageArguments": message_argument,
            "MessageID": str(info_data.get("MessageId", NA)),
            "Name": str(info_data.get("Name", NA)),
            "PercentComplete": str(info_data.get("PercentComplete", NA)),
            "Status": job_status,
            "ActualRunningStopTime": str(info_data.get("ActualRunningStopTime", NA)),
            "JobType": str(info_data.get("JobType", NA)),
            "ActualRunningStartTime": str(info_data.get("ActualRunningStartTime", NA)),
            "EndTime": str(info_data.get("EndTime", NA)),
            "CompletionTime": str(info_data.get("CompletionTime", NA)),
            "Description": str(info_data.get("Description", NA)),
            "TargetSettingsURI": str(info_data.get("TargetSettingsURI", NA))
        }
        return transformed_info_data

    def get_lifecycle_controller_job_details(self, job_id, members):
        response = "Job ID is invalid"
        for member in members:
            if job_id in member.get(odata):
                response = self.idrac.invoke_request(method='GET', uri=member.get(odata))
                break
        return response

    def get_lifecycle_controller_job_list(self, job_id, jobs):
        job_response = self.idrac.invoke_request(method='GET', uri=jobs)
        members = job_response.json_data.get("Members", [])
        response = self.get_lifecycle_controller_job_details(job_id, members)
        return response

    def get_lifecycle_controller_job_status_info(self, job_id):
        manager_response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_LIFECYCLE_CONTROLLER_JOB_STATUS_INFO_10)
        jobs = manager_response.json_data.get("Oem", {}).get("Dell", {}).get("Jobs", {}).get(odata, "")
        response = self.get_lifecycle_controller_job_list(job_id=job_id, jobs=jobs)
        return response
