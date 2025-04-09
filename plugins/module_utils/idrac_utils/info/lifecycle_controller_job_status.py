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


GET_IDRAC_LIFECYCLE_CONTROLLER_JOB_STATUS_INFO_10 = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/{0}"
NA = "Not Available"


class IDRACLifecycleControllerJobStatusInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def transform_job_status_data(self, info_data):

        job_success_list = ['Completed', 'Success']
        job_failed_list = ['Failed', 'Errors']
        job_state = str(info_data.get("JobState"))
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
            "InstanceID": str(info_data.get("Id")),
            "JobStartTime": str(info_data.get("StartTime")),
            "JobStatus": job_state,
            "JobUntilTime": "NA",
            "Message": str(info_data.get("Message")),
            "MessageArguments": message_argument,
            "MessageID": str(info_data.get("MessageId")),
            "Name": str(info_data.get("Name")),
            "PercentComplete": str(info_data.get("PercentComplete")),
            "Status": job_status,
            "ActualRunningStopTime": str(info_data.get("ActualRunningStopTime")),
            "JobType": str(info_data.get("JobType")),
            "ActualRunningStartTime": str(info_data.get("ActualRunningStartTime")),
            "EndTime": str(info_data.get("EndTime")),
            "CompletionTime": str(info_data.get("CompletionTime")),
            "Description": str(info_data.get("Description")),
            "TargetSettingsURI": str(info_data.get("TargetSettingsURI"))
        }
        return transformed_info_data

    def get_lifecycle_controller_job_status_info(self, module):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_LIFECYCLE_CONTROLLER_JOB_STATUS_INFO_10.format(module.params.get('job_id')))
        return response
