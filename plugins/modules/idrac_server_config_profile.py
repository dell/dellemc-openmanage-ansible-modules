#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.5.0
# Copyright (C) 2019-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: idrac_server_config_profile
short_description: Export or Import iDRAC Server Configuration Profile (SCP)
version_added: "2.1.0"
description:
  - Export the Server Configuration Profile (SCP) from the iDRAC or import from a
    network share (CIFS, NFS, HTTP, HTTPS) or a local file.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
  command:
    description:
      - If C(import), the module performs SCP import operation.
      - If C(export), the module performs SCP export operation.
      - If C(preview), the module performs SCP preview operation.
    type: str
    choices: ['import', 'export', 'preview']
    default: 'export'
  job_wait:
    description: Whether to wait for job completion or not.
    type: bool
    required: True
  share_name:
    description:
      - Network share or local path.
      - CIFS, NFS, HTTP, and HTTPS network share types are supported.
    type: str
    required: True
  share_user:
    description: Network share user in the format 'user@domain' or 'domain\\user' if user is
      part of a domain else 'user'. This option is mandatory for CIFS Network Share.
    type: str
  share_password:
    description: Network share user password. This option is mandatory for CIFS Network Share.
    type: str
    aliases: ['share_pwd']
  scp_file:
    description:
      - Name of the server configuration profile (SCP) file.
      - This option is mandatory if I(command) is C(import).
      - The default format <idrac_ip>_YYmmdd_HHMMSS_scp is used if this option is not specified for C(import).
      - I(export_format) is used if the valid extension file is not provided for C(import).
    type: str
  scp_components:
    description:
      - If C(ALL), this module exports or imports all components configurations from SCP file.
      - If C(IDRAC), this module exports or imports iDRAC configuration from SCP file.
      - If C(BIOS), this module exports or imports BIOS configuration from SCP file.
      - If C(NIC), this module exports or imports NIC configuration from SCP file.
      - If C(RAID), this module exports or imports RAID configuration from SCP file.
    type: str
    choices: ['ALL', 'IDRAC', 'BIOS', 'NIC', 'RAID']
    default: 'ALL'
  shutdown_type:
    description:
      - This option is applicable for C(import) command.
      - If C(Graceful), the job gracefully shuts down the operating system and turns off the server.
      - If C(Forced), it forcefully shuts down the server.
      - If C(NoReboot), the job that applies the SCP will pause until you manually reboot the server.
    type: str
    choices: ['Graceful', 'Forced', 'NoReboot']
    default: 'Graceful'
  end_host_power_state:
    description:
      - This option is applicable for C(import) command.
      - If C(On), End host power state is on.
      - If C(Off), End host power state is off.
    type: str
    choices: ['On' ,'Off']
    default: 'On'
  export_format:
    description: Specify the output file format. This option is applicable for C(export) command.
    type: str
    choices: ['JSON',  'XML']
    default: 'XML'
  export_use:
    description: Specify the type of server configuration profile (SCP) to be exported.
      This option is applicable for C(export) command.
    type: str
    choices: ['Default',  'Clone', 'Replace']
    default: 'Default'
requirements:
  - "python >= 3.8.6"
author:
  - "Jagadeesh N V(@jagadeeshnv)"
  - "Felix Stephen (@felixs88)"
notes:
    - This module requires 'Administrator' privilege for I(idrac_user).
    - Run this module from a system that has direct access to Dell EMC iDRAC.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Export SCP with IDRAC components in JSON format to a local path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/scp_folder"
    scp_components: IDRAC
    scp_file: example_file
    export_format: JSON
    export_use: Clone
    job_wait: True

- name: Import SCP with IDRAC components in JSON format from a local path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/scp_folder"
    command: import
    scp_components: "IDRAC"
    scp_file: example_file.json
    shutdown_type: Graceful
    end_host_power_state: "On"
    job_wait: False

- name: Export SCP with BIOS components in XML format to a NFS share path with auto-generated file name
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "192.168.0.2:/share"
    scp_components: "BIOS"
    export_format: XML
    export_use: Default
    job_wait: True

- name: Import SCP with BIOS components in XML format from a NFS share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "192.168.0.2:/share"
    command: import
    scp_components: "BIOS"
    scp_file: 192.168.0.1_20210618_162856.xml
    shutdown_type: NoReboot
    end_host_power_state: "Off"
    job_wait: False

- name: Export SCP with RAID components in XML format to a CIFS share path with share user domain name
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "\\\\192.168.0.2\\share"
    share_user: share_username@domain
    share_password: share_password
    share_mnt: /mnt/cifs
    scp_file: example_file.xml
    scp_components: "RAID"
    export_format: XML
    export_use: Default
    job_wait: True

- name: Import SCP with RAID components in XML format from a CIFS share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "\\\\192.168.0.2\\share"
    share_user: share_username
    share_password: share_password
    share_mnt: /mnt/cifs
    command: import
    scp_components: "RAID"
    scp_file: example_file.xml
    shutdown_type: Forced
    end_host_power_state: "On"
    job_wait: True

- name: Export SCP with ALL components in JSON format to a HTTP share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "http://192.168.0.3/share"
    share_user: share_username
    share_password: share_password
    scp_file: example_file.json
    scp_components: ALL
    export_format: JSON
    job_wait: False

- name: Import SCP with ALL components in JSON format from a HTTP share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: import
    share_name: "http://192.168.0.3/share"
    share_user: share_username
    share_password: share_password
    scp_file: example_file.json
    shutdown_type: Graceful
    end_host_power_state: "On"
    job_wait: True

- name: Export SCP with ALL components in XML format to a HTTPS share path without SCP file name
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "https://192.168.0.4/share"
    share_user: share_username
    share_password: share_password
    scp_components: ALL
    export_format: XML
    export_use: Replace
    job_wait: True

- name: Import SCP with ALL components in XML format from a HTTPS share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: import
    share_name: "https://192.168.0.4/share"
    share_user: share_username
    share_password: share_password
    scp_file: 192.168.0.1_20160618_164647.xml
    shutdown_type: Graceful
    end_host_power_state: "On"
    job_wait: False

- name: Preview SCP with ALL components in XML format from a CIFS share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "{{ idrac_ip }}"
    idrac_user: "{{ idrac_user }}"
    idrac_password: "{{ idrac_password }}"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "\\\\192.168.0.2\\share"
    share_user: share_username
    share_password: share_password
    command: preview
    scp_components: "ALL"
    scp_file: example_file.xml
    job_wait: True

- name: Preview SCP with ALL components in JSON format from a NFS share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "{{ idrac_ip }}"
    idrac_user: "{{ idrac_user }}"
    idrac_password: "{{ idrac_password }}"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "192.168.0.2:/share"
    command: preview
    scp_components: "IDRAC"
    scp_file: example_file.xml
    job_wait: True

- name: Preview SCP with ALL components in XML format from a HTTP share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "{{ idrac_ip }}"
    idrac_user: "{{ idrac_user }}"
    idrac_password: "{{ idrac_password }}"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "http://192.168.0.1/http-share"
    share_user: share_username
    share_password: share_password
    command: preview
    scp_components: "ALL"
    scp_file: example_file.xml
    job_wait: True

- name: Preview SCP with ALL components in XML format from a local path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "{{ idrac_ip }}"
    idrac_user: "{{ idrac_user }}"
    idrac_password: "{{ idrac_password }}"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/scp_folder"
    command: preview
    scp_components: "IDRAC"
    scp_file: example_file.json
    job_wait: False
'''

RETURN = r'''
---
msg:
  type: str
  description: Status of the import or export SCP job.
  returned: always
  sample: "Successfully imported the Server Configuration Profile"
scp_status:
  type: dict
  description: SCP operation job and progress details from the iDRAC.
  returned: success
  sample:
    {
      "Id": "JID_XXXXXXXXX",
      "JobState": "Completed",
      "JobType": "ImportConfiguration",
      "Message": "Successfully imported and applied Server Configuration Profile.",
      "MessageArgs": [],
      "MessageId": "XXX123",
      "Name": "Import Configuration",
      "PercentComplete": 100,
      "StartTime": "TIME_NOW",
      "Status": "Success",
      "TargetSettingsURI": null,
      "retval": true
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
'''

import os
import json
import re
import copy
from datetime import datetime
from os.path import exists
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, idrac_auth_params
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import strip_substr_dict
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.parse import urlparse


REDFISH_SCP_BASE_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"
CHANGES_FOUND = "Changes found to be applied."
NO_CHANGES_FOUND = "No changes found to be applied."
INVALID_FILE = "Invalid file path provided."
JOB_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/{job_id}"


def get_scp_file_format(module):
    scp_file = module.params['scp_file']
    if scp_file:
        scp_file_name_format = scp_file
        if not str(scp_file.lower()).endswith(('.xml', '.json')):
            scp_file_name_format = "{0}.{1}".format(scp_file, module.params['export_format'].lower())
    else:
        d = datetime.now()
        scp_file_name_format = "{0}_{1}{2}{3}_{4}{5}{6}_scp.{7}".format(
            module.params["idrac_ip"], d.date().year, d.date().month, d.date().day,
            d.time().hour, d.time().minute, d.time().second,
            module.params['export_format'].lower())
    return scp_file_name_format


def response_format_change(response, params, file_name):
    resp = {}
    if params["job_wait"]:
        response = response.json_data
        response.pop("Description", None)
        response.pop("Name", None)
        response.pop("EndTime", None)
        response.pop("StartTime", None)
        response.pop("TaskState", None)
        response.pop("Messages", None)
        if response.get("Oem") is not None:
            response.update(response["Oem"]["Dell"])
            response.pop("Oem", None)
        sep = "/" if "/" in params["share_name"] else "\\"
        response["file"] = "{0}{1}{2}".format(params["share_name"], sep, file_name)
        response["retval"] = True
    else:
        location = response.headers.get("Location")
        job_id = location.split("/")[-1]
        job_uri = JOB_URI.format(job_id=job_id)
        resp["Data"] = {"StatusCode": response.status_code, "jobid": job_id, "next_uri": job_uri}
        resp["Job"] = {"JobId": job_id, "ResourceURI": job_uri}
        resp["Return"] = "JobCreated"
        resp["Status"] = "Success"
        resp["Message"] = "none"
        resp["StatusCode"] = response.status_code
        sep = "/" if "/" in params["share_name"] else "\\"
        resp["file"] = "{0}{1}{2}".format(params["share_name"], sep, file_name)
        resp["retval"] = True
        response = resp
    return response


def run_export_import_scp_http(idrac, module):
    share_url = urlparse(module.params["share_name"])
    share = {}
    scp_file = module.params.get("scp_file")
    share["share_ip"] = share_url.netloc
    share["share_name"] = share_url.path.strip('/')
    share["share_type"] = share_url.scheme.upper()
    share["file_name"] = scp_file
    scp_file_name_format = scp_file
    share["username"] = module.params.get("share_user")
    share["password"] = module.params.get("share_password")
    command = module.params["command"]
    if command == "import":
        scp_response = idrac.import_scp_share(shutdown_type=module.params["shutdown_type"],
                                              host_powerstate=module.params["end_host_power_state"],
                                              job_wait=module.params["job_wait"],
                                              target=module.params["scp_components"], share=share, )
    elif command == "export":
        scp_file_name_format = get_scp_file_format(module)
        share["file_name"] = scp_file_name_format
        scp_response = idrac.export_scp(export_format=module.params["export_format"],
                                        export_use=module.params["export_use"],
                                        target=module.params["scp_components"],
                                        job_wait=module.params["job_wait"], share=share, )
    scp_response = response_format_change(scp_response, module.params, scp_file_name_format)
    if isinstance(scp_response, dict) and scp_response.get("TaskStatus") == "Critical":
        module.fail_json(msg="Failed to {0} scp.".format(command), scp_status=scp_response)
    return scp_response


def get_scp_share_details(module):
    share_name = module.params.get("share_name")
    command = module.params["command"]
    scp_file_name_format = get_scp_file_format(module)
    if ":" in share_name:
        nfs_split = share_name.split(":")
        share = {"share_ip": nfs_split[0], "share_name": nfs_split[1], "share_type": "NFS"}
        if command == "export":
            share["file_name"] = scp_file_name_format
    elif "\\" in share_name:
        ip_pattern = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        share_path = re.split(ip_pattern, share_name)
        share_ip = re.findall(ip_pattern, share_name)
        share_path_name = "\\".join(list(filter(None, share_path[-1].split("\\"))))
        share = {"share_ip": share_ip[0], "share_name": share_path_name, "share_type": "CIFS",
                 "username": module.params.get("share_user"), "password": module.params.get("share_password")}
        if command == "export":
            share["file_name"] = scp_file_name_format
    else:
        share = {"share_type": "LOCAL", "share_name": share_name}
        if command == "export":
            share["file_name"] = scp_file_name_format
    return share, scp_file_name_format


def export_scp_redfish(module, idrac):
    command = module.params["command"]
    share, scp_file_name_format = get_scp_share_details(module)
    if share["share_type"] == "LOCAL":
        scp_response = idrac.export_scp(export_format=module.params["export_format"],
                                        export_use=module.params["export_use"],
                                        target=module.params["scp_components"],
                                        job_wait=False, share=share, )
        scp_response = wait_for_response(scp_response, module, share, idrac)
    else:
        scp_response = idrac.export_scp(export_format=module.params["export_format"],
                                        export_use=module.params["export_use"],
                                        target=module.params["scp_components"],
                                        job_wait=module.params["job_wait"], share=share, )
    scp_response = response_format_change(scp_response, module.params, scp_file_name_format)
    if isinstance(scp_response, dict) and scp_response.get("TaskStatus") == "Critical":
        module.fail_json(msg="Failed to {0} scp.".format(command), scp_status=scp_response)
    return scp_response


def wait_for_response(scp_resp, module, share, idrac):
    task_uri = scp_resp.headers["Location"]
    job_id = task_uri.split("/")[-1]
    job_uri = JOB_URI.format(job_id=job_id)
    wait_resp = idrac.wait_for_job_complete(task_uri, job_wait=True)
    with open("{0}/{1}".format(share["share_name"], share["file_name"]), "w") as file_obj:
        if module.params["export_format"] == "JSON":
            json.dump(wait_resp.json_data, file_obj, indent=4)
        else:
            wait_resp_value = wait_resp.decode("utf-8")
            file_obj.write(wait_resp_value)
    if module.params["job_wait"]:
        scp_resp = idrac.invoke_request(job_uri, "GET")
    return scp_resp


def preview_scp_redfish(module, idrac, http_share, import_job_wait=False):
    command = module.params["command"]
    scp_target = module.params["scp_components"]
    job_wait_option = module.params["job_wait"]
    if command == "import":
        job_wait_option = import_job_wait
    if http_share:
        share_url = urlparse(module.params["share_name"])
        share = {"share_ip": share_url.netloc, "share_name": share_url.path.strip('/'),
                 "share_type": share_url.scheme.upper(), "file_name": module.params.get("scp_file"),
                 "username": module.params.get("share_user"), "password": module.params.get("share_password")}
    else:
        share, scp_file_name_format = get_scp_share_details(module)
        share["file_name"] = module.params.get("scp_file")
    buffer_text = None
    if share["share_type"] == "LOCAL":
        scp_target = "ALL"
        file_path = "{0}{1}{2}".format(share["share_name"], os.sep, share["file_name"])
        if not exists(file_path):
            module.fail_json(msg=INVALID_FILE)
        with open(file_path, "r") as file_obj:
            buffer_text = file_obj.read()
    scp_response = idrac.import_preview(import_buffer=buffer_text, target=scp_target,
                                        share=share, job_wait=job_wait_option)
    scp_response = response_format_change(scp_response, module.params, share["file_name"])
    if isinstance(scp_response, dict) and scp_response.get("TaskStatus") == "Critical":
        module.fail_json(msg="Failed to {0} scp.".format(command), scp_status=scp_response)
    return scp_response


def import_scp_redfish(module, idrac, http_share):
    command = module.params["command"]
    scp_target = module.params["scp_components"]
    job_wait = copy.copy(module.params["job_wait"])
    if module.check_mode:
        module.params["job_wait"] = True
        scp_resp = preview_scp_redfish(module, idrac, http_share, import_job_wait=True)
        if "SYS081" in scp_resp["MessageId"] or "SYS082" in scp_resp["MessageId"]:
            module.exit_json(msg=CHANGES_FOUND, changed=True)
        else:
            module.fail_json(msg=scp_resp)
    if http_share:
        share_url = urlparse(module.params["share_name"])
        share = {"share_ip": share_url.netloc, "share_name": share_url.path.strip('/'),
                 "share_type": share_url.scheme.upper(), "file_name": module.params.get("scp_file"),
                 "username": module.params.get("share_user"), "password": module.params.get("share_password")}
    else:
        share, scp_file_name_format = get_scp_share_details(module)
        share["file_name"] = module.params.get("scp_file")
    buffer_text = None
    share_dict = share
    if share["share_type"] == "LOCAL":
        scp_target = "ALL"
        file_path = "{0}{1}{2}".format(share["share_name"], os.sep, share["file_name"])
        if not exists(file_path):
            module.fail_json(msg=INVALID_FILE)
        with open(file_path, "r") as file_obj:
            buffer_text = file_obj.read()
        share_dict = {}
    module.params["job_wait"] = job_wait
    scp_response = idrac.import_scp_share(shutdown_type=module.params["shutdown_type"],
                                          host_powerstate=module.params["end_host_power_state"],
                                          job_wait=module.params["job_wait"],
                                          target=scp_target,
                                          import_buffer=buffer_text, share=share_dict, )
    scp_response = response_format_change(scp_response, module.params, share["file_name"])
    if isinstance(scp_response, dict) and scp_response.get("TaskStatus") == "Critical":
        module.fail_json(msg="Failed to {0} scp.".format(command), scp_status=scp_response)
    return scp_response


def main():
    specs = {
        "command": {"required": False, "type": 'str',
                    "choices": ['export', 'import', 'preview'], "default": 'export'},
        "job_wait": {"required": True, "type": 'bool'},
        "share_name": {"required": True, "type": 'str'},
        "share_user": {"required": False, "type": 'str'},
        "share_password": {"required": False, "type": 'str',
                           "aliases": ['share_pwd'], "no_log": True},
        "scp_components": {"required": False,
                           "choices": ['ALL', 'IDRAC', 'BIOS', 'NIC', 'RAID'],
                           "default": 'ALL'},
        "scp_file": {"required": False, "type": 'str'},
        "shutdown_type": {"required": False,
                          "choices": ['Graceful', 'Forced', 'NoReboot'],
                          "default": 'Graceful'},
        "end_host_power_state": {"required": False,
                                 "choices": ['On', 'Off'],
                                 "default": 'On'},
        "export_format": {"required": False, "type": 'str',
                          "choices": ['JSON', 'XML'], "default": 'XML'},
        "export_use": {"required": False, "type": 'str',
                       "choices": ['Default', 'Clone', 'Replace'], "default": 'Default'}
    }
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        required_if=[
            ["command", "import", ["scp_file"]],
            ["command", "preview", ["scp_file"]],
        ],
        supports_check_mode=True)

    try:
        changed = False
        http_share = module.params["share_name"].lower().startswith(('http://', 'https://'))
        with iDRACRedfishAPI(module.params) as idrac:
            command = module.params['command']
            if command == 'import':
                if http_share:
                    scp_status = run_export_import_scp_http(idrac, module)
                    if "SYS069" in scp_status.get("MessageId", ""):
                        changed = False
                    elif "SYS053" in scp_status.get("MessageId", ""):
                        changed = True
                else:
                    scp_status = import_scp_redfish(module, idrac, http_share)
                    if "No changes were applied" not in scp_status.get('Message', ""):
                        changed = True
                    elif "SYS043" in scp_status.get("MessageId", ""):
                        changed = True
                    elif "SYS069" in scp_status.get("MessageId", ""):
                        changed = False
            elif command == "export":
                if http_share:
                    scp_status = run_export_import_scp_http(idrac, module)
                else:
                    scp_status = export_scp_redfish(module, idrac)
            else:
                scp_status = preview_scp_redfish(module, idrac, http_share, import_job_wait=False)
        if module.params.get('job_wait'):
            scp_status = strip_substr_dict(scp_status)
            msg = "Successfully {0}ed the Server Configuration Profile."
            module.exit_json(changed=changed, msg=msg.format(command), scp_status=scp_status)
        else:
            msg = "Successfully triggered the job to {0} the Server Configuration Profile."
            module.exit_json(msg=msg.format(command), scp_status=scp_status)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (ImportError, ValueError, RuntimeError, SSLValidationError,
            ConnectionError, KeyError, TypeError, IndexError) as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
