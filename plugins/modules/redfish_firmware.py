#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2019-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
---
module: redfish_firmware
short_description: To perform a component firmware update using the image file available on the local or remote system
version_added: "2.1.0"
description:
    - This module allows the firmware update of only one component at a time.
      If the module is run for more than one component, an error message is returned.
    - Depending on the component, the firmware update is applied after an automatic or manual reboot.
extends_documentation_fragment:
  - dellemc.openmanage.redfish_auth_options
options:
    image_uri:
        description:
            - Firmware Image location URI or local path.
            - For example- U(http://<web_address>/components.exe) or /home/firmware_repo/component.exe.
        type: str
        required: true
    transfer_protocol:
        description: Protocol used to transfer the firmware image file. Applicable for URI based update.
        type: str
        default: HTTP
        choices: ["CIFS", "FTP", "HTTP", "HTTPS", "NSF", "OEM", "SCP", "SFTP", "TFTP"]
    job_wait:
        description: Provides the option to wait for job completion.
        type: bool
        default: true
    job_wait_timeout:
        type: int
        description:
            - The maximum wait time of I(job_wait) in seconds. The job is tracked only for this duration.
            - This option is applicable when I(job_wait) is C(true).
            - "Note: If a firmware update needs a reboot, the job will get scheduled and waits for
              no of seconds specfied in I(job_wait_time). to reduce the wait time either give
              I(job_wait_time) minimum or make I(job_wait)as false and retrigger."
        default: 3600
requirements:
    - "python >= 3.9.6"
    - "urllib3"
author:
    - "Felix Stephen (@felixs88)"
    - "Husniya Hameed (@husniya_hameed)"
    - "Shivam Sharma (@Shivam-Sharma)"
    - "Kritika Bhateja (@Kritika_Bhateja)"
    - "Abhishek Sinha (@ABHISHEK-SINHA10)"
    - "Sakshi Makkar (@Sakshi-dell)"
notes:
    - Run this module from a system that has direct access to Redfish APIs.
    - This module supports both IPv4 and IPv6 addresses.
    - This module supports only iDRAC9 and above.
    - This module does not support C(check_mode).
"""

EXAMPLES = """
---
- name: Update the firmware from a single executable file available in a HTTP protocol
  dellemc.openmanage.redfish_firmware:
    baseuri: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    image_uri: "http://192.168.0.2/firmware_repo/component.exe"
    transfer_protocol: "HTTP"

- name: Update the firmware from a single executable file available in a HTTP protocol with job_Wait
  dellemc.openmanage.redfish_firmware:
    baseuri: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    image_uri: "http://192.168.0.2/firmware_repo/component.exe"
    transfer_protocol: "HTTP"
    job_wait: true
    job_wait_timeout: 600

- name: Update the firmware from a single executable file available in a local path
  dellemc.openmanage.redfish_firmware:
    baseuri: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    image_uri: "/home/firmware_repo/component.exe"
"""

RETURN = """
---
msg:
  description: Overall status of the firmware update task.
  returned: always
  type: str
  sample: "Successfully updated the firmware."
task:
  description: Returns ID and URI of the created task.
  returned: success
  type: dict
  sample: {
        "id": "JID_XXXXXXXXXXXX",
        "uri": "/redfish/v1/TaskService/Tasks/JID_XXXXXXXXXXXX"
    }
error_info:
  type: dict
  description: Details of http error.
  returned: on http error
  sample:  {
        "error": {
            "@Message.ExtendedInfo": [
                {
                    "Message": "Unable to complete the operation because the JSON data format entered is invalid.",
                    "Resolution": "Do the following and the retry the operation:
                        1) Enter the correct JSON data format and retry the operation.
                        2) Make sure that no syntax error is present in JSON data format.
                        3) Make sure that a duplicate key is not present in JSON data format.",
                    "Severity": "Critical"
                },
                {
                    "Message": "The request body submitted was malformed JSON and
                        could not be parsed by the receiving service.",
                    "Resolution": "Ensure that the request body is valid JSON and resubmit the request.",
                    "Severity": "Critical"
                }
            ],
            "code": "Base.1.2.GeneralError",
            "message": "A general error has occurred. See ExtendedInfo for more information."
        }
    }
"""


import json
import os
import time
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.redfish import Redfish, RedfishAnsibleModule
from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError

try:
    from urllib3.fields import RequestField
    from urllib3.filepost import encode_multipart_formdata
    HAS_LIB = True
except ImportError:
    HAS_LIB = False

UPDATE_SERVICE = "UpdateService"
JOB_URI = "JobService/Jobs/{job_id}"
JOB_WAIT_MSG = 'Job wait timed out after {0} seconds.'
FAIL_JOB_MSG = "Firmware update failed."
SUCCESS_JOB_MSG = "Successfully updated the firmware."
SCHEDULE_JOB_MSG = "Successfully scheduled the firmware job."
JOBSTATUS_SUCCESS = "success"
JOBSTATUS_FAILED = "failed"
JOBSTATUS_TIMED_OUT = "timed_out"
JOBSTATUS_SCHEDULED = "scheduled"
JOBSTATUS_ERRORED = "errored"
FILE_PAYLOAD_HEADER = "UpdateFile"


def _encode_form_data(payload_file, payload_file_header):
    """Encode multipart/form-data for file upload."""
    fields = []
    f_name, f_data, f_type = payload_file.get(payload_file_header)
    f_binary = f_data.read()
    req_field = RequestField(name=payload_file_header, data=f_binary, filename=f_name)
    req_field.make_multipart(content_type=f_type)
    fields.append(req_field)
    data, content_type = encode_multipart_formdata(fields)
    return data, content_type


def _get_update_service_target(obj, module, generation):
    """Returns all the URI which is required for firmware update dynamically."""
    action_resp = obj.invoke_request("GET", "{0}{1}".format(obj.root_uri, UPDATE_SERVICE))
    action_attr = action_resp.json_data["Actions"]
    protocol = module.params["transfer_protocol"]
    update_uri = None
    if generation <= 16:
        push_uri = action_resp.json_data.get('HttpPushUri')
    else:
        push_uri = action_resp.json_data.get('MultipartHttpPushUri')
    inventory_uri = action_resp.json_data.get('FirmwareInventory').get('@odata.id')
    if "#UpdateService.SimpleUpdate" in action_attr:
        update_service = action_attr.get("#UpdateService.SimpleUpdate")
        proto = update_service.get("TransferProtocol@Redfish.AllowableValues")
        if isinstance(proto, list) and protocol in proto and 'target' in update_service:
            update_uri = update_service.get('target')
        else:
            module.fail_json(msg="Target firmware version does not support {0} protocol.".format(protocol))
    if update_uri is None or push_uri is None or inventory_uri is None:
        module.fail_json(msg="Target firmware version does not support redfish firmware update.")
    return str(inventory_uri), str(push_uri), str(update_uri)


def firmware_update(obj, module):
    """Firmware update using single binary file from Local path or HTTP location."""
    gen_details = obj.get_server_generation
    generation = gen_details[0]
    image_path = module.params.get("image_uri")
    trans_proto = module.params["transfer_protocol"]
    inventory_uri, push_uri, update_uri = _get_update_service_target(obj, module, generation)
    if image_path.startswith("http"):
        payload = {"ImageURI": image_path, "TransferProtocol": trans_proto}
        update_status = obj.invoke_request("POST", update_uri, data=payload)
    else:
        payload_file_header = FILE_PAYLOAD_HEADER
        headers = {}
        if generation <= 16:
            resp_inv = obj.invoke_request("GET", inventory_uri)
            headers = {"If-Match": resp_inv.headers.get("etag")}
            payload_file_header = "file"

        with open(os.path.join(image_path), "rb") as img_file:
            binary_payload = {payload_file_header: (image_path.split(os.sep)[-1], img_file, "multipart/form-data")}
            data, ctype = _encode_form_data(binary_payload, payload_file_header)
        headers.update({"Content-Type": ctype})
        upload_status = obj.invoke_request("POST", push_uri, data=data, headers=headers, dump=False, api_timeout=module.params["timeout"])
        if generation <= 16 and upload_status.status_code == 201:
            payload = {"ImageURI": upload_status.headers.get("location")}
            update_status = obj.invoke_request("POST", update_uri, data=payload)
        else:
            update_status = upload_status
    return update_status


def wait_for_job_completion(module, job_uri, job_wait_timeout=900, interval=30):
    try:
        with Redfish(module.params, req_session=False) as obj:
            track_counter = 0
            final_jobstatus = ""
            job_msg = ""
            while track_counter <= job_wait_timeout:
                try:
                    response = obj.invoke_request("GET", "{0}{1}".format(obj.root_uri, job_uri))
                    if response.json_data.get("PercentComplete") == 100 and response.json_data.get("JobState") == "Completed":
                        if response.json_data.get("JobStatus") == "OK":
                            final_jobstatus = JOBSTATUS_SUCCESS
                            job_msg = SUCCESS_JOB_MSG
                        else:
                            final_jobstatus = JOBSTATUS_FAILED
                            job_msg = FAIL_JOB_MSG
                        break
                    track_counter += interval
                    time.sleep(interval)
                except (HTTPError, URLError):
                    track_counter += interval
                    time.sleep(interval)
            # TIMED OUT
            # when job is scheduled
            if not final_jobstatus:
                if response.json_data.get("PercentComplete") == 0 and response.json_data.get("JobState") == "Starting":
                    final_jobstatus = JOBSTATUS_SCHEDULED
                    job_msg = SCHEDULE_JOB_MSG
                # when job timed out
                else:
                    job_msg = JOB_WAIT_MSG.format(job_wait_timeout)
                    final_jobstatus = JOBSTATUS_TIMED_OUT
    except Exception as error_message:
        job_msg = str(error_message)
        module.exit_json(msg=str(job_msg))
        final_jobstatus = JOBSTATUS_ERRORED
    return final_jobstatus, job_msg


def main():
    specs = {
        "image_uri": {"required": True, "type": "str"},
        "transfer_protocol": {"type": "str", "default": "HTTP", "choices": ["CIFS", "FTP", "HTTP", "HTTPS", "NSF", "OEM", "SCP", "SFTP", "TFTP"]},
        "job_wait": {"required": False, "type": 'bool', "default": True},
        "job_wait_timeout": {"required": False, "type": "int", "default": 3600}
    }

    module = RedfishAnsibleModule(
        argument_spec=specs,
        supports_check_mode=False)
    if not HAS_LIB:
        module.fail_json(msg=missing_required_lib("urllib3"))
    try:
        message = "Failed to submit the firmware update task."
        with Redfish(module.params, req_session=True) as obj:
            status = firmware_update(obj, module)
            if status.success:
                message = "Successfully submitted the firmware update task."
                task_uri = status.headers.get("Location")
                job_id = task_uri.split("/")[-1]
            else:
                module.fail_json(msg=message, error_info=json.loads(status))
        job_wait = module.params['job_wait']
        job_wait_timeout = module.params['job_wait_timeout']
        if job_wait and job_wait_timeout > 0:
            job_uri = JOB_URI.format(job_id=job_id)
            job_resp, job_msg = wait_for_job_completion(module, job_uri, job_wait_timeout=module.params['job_wait_timeout'])
            if job_resp == JOBSTATUS_FAILED:
                module.exit_json(msg=job_msg, task={"id": job_id, "uri": JOB_URI.format(job_id=job_id)}, failed=True)
            else:
                module.exit_json(msg=job_msg, task={"id": job_id, "uri": JOB_URI.format(job_id=job_id)}, changed=True)
        else:
            module.exit_json(msg=message, task={"id": job_id, "uri": JOB_URI.format(job_id=job_id)}, changed=True)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except (RuntimeError, URLError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError, IOError, AssertionError, OSError, SSLError) as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
