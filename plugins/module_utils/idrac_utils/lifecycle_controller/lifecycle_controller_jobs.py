# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 9.12.1
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


BASE_URI = "/redfish/v1/Managers/"
ODATA_ID = "@odata.id"

import json


class IDRACLifecycleControllerJobs(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def get_lifecycle_controller_jobs_api(self):
        controller_jobs_baseuri_response = self._get_controller_jobs_baseuri_response()
        manager_uri = self._get_manager_uri(controller_jobs_baseuri_response)
        if manager_uri:
            manager_response = self._get_manager_response(manager_uri)
            job_service_uri = self._get_job_service_uri(manager_response)
            if job_service_uri:
                delete_job_queue_response = self._get_job_service_response(job_service_uri)
                delete_job_queue_uri = self._get_delete_job_queue_uri(delete_job_queue_response)
                if delete_job_queue_uri:
                    return delete_job_queue_uri
        return ""

    def _get_controller_jobs_baseuri_response(self):
        return self.idrac.invoke_request(uri=BASE_URI, method="GET")

    def _get_manager_uri(self, controller_status_baseuri_response):
        return controller_status_baseuri_response.json_data.get("Members", [])[0].get(ODATA_ID, "")

    def _get_manager_response(self, manager_uri):
        return self.idrac.invoke_request(uri=manager_uri, method="GET")

    def _get_job_service_uri(self, manager_response):
        return manager_response.json_data.get("Links", {}).get("Oem", {}).get("Dell", {}).get("DellJobService", {}).get(ODATA_ID, "")

    def _get_job_service_response(self, job_service_uri):
        return self.idrac.invoke_request(uri=job_service_uri, method="GET")

    def _get_delete_job_queue_uri(self, delete_job_queue_response):
        return delete_job_queue_response.json_data.get("Actions", {}).get("#DellJobService.DeleteJobQueue", {}).get("target", "")

    def extract_error_info(self, job_deletion_response):
        message_info = job_deletion_response["error"]["@Message.ExtendedInfo"][0]
        return {
            "Data": {
                "DeleteJobQueue_OUTPUT": {
                    "Message": message_info["Message"],
                    "MessageID": message_info["MessageId"].split(".")[-1],
                }
            },
            "Status": "Error",
            "Message": message_info["Message"],
            "MessageID": message_info["MessageId"].split(".")[-1],
            "Return": "Error",
            "retval": True
        }

    def extract_job_deletion_info(self, job_deletion_response):
        message_info = job_deletion_response.json_data["@Message.ExtendedInfo"][1]
        return {
            "Data": {
                "DeleteJobQueue_OUTPUT": {
                    "Message": message_info["Message"],
                    "MessageID": message_info["MessageId"].split(".")[-1],
                }
            },
            "Status": "Success",
            "Message": message_info["Message"],
            "MessageID": message_info["MessageId"].split(".")[-1],
            "Return": "Success",
            "retval": True
        }

    def lifecycle_controller_jobs_operation(self, module):
        job_id = module.params.get('job_id')
        job_str = ""
        if job_id:
            payload = {"JobID": job_id}
            job_str = "job"

        else:
            payload = {"JobID": "JID_CLEARALL"}
            job_str = "job queue"

        job_ops_uri = self.get_lifecycle_controller_jobs_api()
        if not job_ops_uri:
            return "", job_str

        data = json.dumps(payload)

        job_deletion_response = self.idrac.invoke_request(
            uri=job_ops_uri,
            method='POST',
            data=data,
            dump=False
        )

        if job_deletion_response.status_code == 200:
            resp = self.extract_job_deletion_info(job_deletion_response)
            return resp, job_str
