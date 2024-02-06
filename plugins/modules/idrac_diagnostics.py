#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.0.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: idrac_diagnostics
short_description: Run and Export iDRAC diagnostics
version_added: "9.0.0"
description:
  - This module allows to run and export diagnostics on iDRAC.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
  run:
    description:
      - Run the diagnostics job.
      - Run the diagnostics job based on the I(run_mode) and saves the report in the internal storage. I(reboot_type) is applicable.
    type: bool
    default: true
  export:
    description:
      - Exports the diagnostics information to the given share.
      - This requires I(share_parameters).
    type: bool
    default: true
  run_mode:
    description:
      - This option provides the choices to run the diagnostics.
      - C(express) The Express diagnostics runs a test package for each server subsystem,
        but does not run the full set of tests available in the package for each subsystem
      - C(extended) The Extended diagnostics runs all available tests in each test package for all subsystems.
      - C(long_run) The long run diagnostics runs both Express and Extended tests.
    type: str
    choices: [express, extended, long_run]
    default: express
  reboot_type:
    description:
      - This option provides the choices to reboot the host immediately to run the diagnostics.
      - This is applicable when I(run) is C(True)
      - C(force) Forced Graceful shutdown signals operating system to turn off and waits for 10 minutes.
        If the operating system does not turn off, the iDRAC power cycles the system.
      - C(graceful) Graceful shutdown waits for operating system to turn off or for system restart.
      - C(power_cycle) performs a power cycle for a hard reset on the device.
    type: str
    choices: [force, graceful, power_cycle]
    default: graceful
  scheduled_start_time:
    description:
      - Schedules the job at the time specified.
      - The accepted formats are yyyymmddhhmmss and YYYY-MM-DDThh:mm:ss+HH:MM
      - This is applicable when I(run) is C(run) or C(run_and_export) and I(reboot_type) is power_cycle
    type: str
  scheduled_end_time:
    description:
      - Run the diagnostic until a date and time after the I(scheduled_start_time)
      - The accepted formats are yyyymmddhhmmss and YYYY-MM-DDThh:mm:ss+HH:MM
      - If it is not started by End time, it is marked as failed with End time expired. if not specified, no end time.
      - This is applicable when I(scheduled_start_time) is specified
      - This is applicable when I(run) is C(True) and I(reboot_type) is C(power_cycle)
    type: str
  job_wait:
    description:
      - Provides the option to wait for job completion.
      - This is applicable when I(run) is C(True) and I(reboot_type) is C(power_cycle)
    type: bool
    default: true
  job_wait_timeout:
    description:
      - Time in seconds to wait for job completion
      - This is applicable when I(job_wait) is C(true).
    type: int
    default: 1200
  share_parameters:
    description:
      - Parameters that are required for the export operation of diagnostics.
      - I(share_parameters) is required when I(export) is C(true).
    type: dict
    suboptions:
      share_type:
        description:
          - Share type of the network share.
          - C(local) uses local path for I(export) operation.
          - C(nfs) uses NFS share for I(export) operation.
          - C(cifs) uses CIFS share for I(export) operation.
          - C(http) uses HTTP share for I(export) operation.
          - C(https) uses HTTPS share for I(export) operation.
        type: str
        choices: [local, nfs, cifs, http, https]
        default: local
      file_name:
        description:
          - Diagnostics file name for I(export) operation.
        type: str
      ip_address:
        description:
          - IP address of the network share.
          - I(ip_address) is required when I(share_type) is C(nfs), C(cifs), C(http) or C(https).
        type: str
      share_name:
        description:
          - Network share or local path of the diagnostics file.
        type: str
      workgroup:
        description:
          - Workgroup of the network share.
          - I(workgroup) is applicable only when I(share_type) is C(cifs).
        type: str
      username:
        description:
          - Username of the network share.
          - I(username) is required when I(share_type) is C(cifs).
        type: str
      password:
        description:
          - Password of the network share.
          - I(password) is required when I(share_type) is C(cifs).
        type: str
      ignore_certificate_warning:
        description:
          - Ignores the certificate warning while connecting to Share and is only applicable when I(share_type) is C(https).
          - C(off) ignores the certificate warning.
          - C(on) does not ignore the certificate warning.
        type: str
        choices: ["off", "on"]
        default: "off"
      proxy_support:
        description:
          - Specifies if proxy is to be used or not.
          - C(off) does not use proxy settings.
          - C(default_proxy) uses the default proxy settings.
          - C(parameters_proxy) uses the specified proxy settings. I(proxy_server) is required when I(proxy_support) is C(parameters_proxy).
          - I(proxy_support) is only applicable when I(share_type) is C(https) or C(https).
        type: str
        choices: ["off", "default_proxy", "parameters_proxy"]
        default: "off"
      proxy_type:
        description:
          - The proxy type of the proxy server.
          - C(http) to select HTTP proxy.
          - C(socks) to select SOCKS proxy.
          - I(proxy_type) is only applicable when I(share_type) is C(https) or C(https) and when I(proxy_support) is C(parameters_proxy).
        type: str
        choices: [http, socks]
        default: http
      proxy_server:
        description:
          - The IP address of the proxy server.
          - I(proxy_server) is required when I(proxy_support) is C(parameters_proxy).
          - I(proxy_server) is only applicable when I(share_type) is C(https) or C(https) and when I(proxy_support) is C(parameters_proxy).
        type: str
      proxy_port:
        description:
          - The port of the proxy server.
          - I(proxy_port) is only applicable when I(share_type) is C(https) or C(https) and when I(proxy_support) is C(parameters_proxy).
        type: str
        default: '80'
      proxy_username:
        description:
          - The username of the proxy server.
          - I(proxy_username) is only applicable when I(share_type) is C(https) or C(https) and when I(proxy_support) is C(parameters_proxy).
        type: str
      proxy_password:
        description:
          - The password of the proxy server.
          - I(proxy_password) is only applicable when I(share_type) is C(https) or C(https) and when I(proxy_support) is C(parameters_proxy).
        type: str
  resource_id:
    type: str
    description:
      - Id of the resource.
      - If the value for resource ID is not provided, the module picks the first resource ID available from the list of system resources returned by the iDRAC.
requirements:
  - "python >= 3.9.6"
author:
  - "Shivam Sharma(@ShivamSh3)"
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports only iDRAC9 and above.
    - This module supports IPv4 and IPv6 addresses.
    - This module does not support C(check_mode).
    - This module will always report "Changes found".
"""

EXAMPLES = r"""
---
- name: Run and export the diagnostics to local path
  dellemc.openmanage.idrac_diagnostics:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "path/to/ca_file"
    run: true
    export: true
    share_parameters:
        share_type: "local"
        share_path: "/opt/local/diagnostics/"
        file_name: "diagnostics.txt"

- name: Run the diagnostics with force reboot on schedule
  dellemc.openmanage.idrac_diagnostics:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "path/to/ca_file"
    run: true
    run_mode: "express"
    reboot_type: "force"
    scheduled_start_time: 20240101101015

- name: Run and export the diagnostics to HTTPS share
  dellemc.openmanage.idrac_diagnostics:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "path/to/ca_file"
    run: true
    export: true
    share_parameters:
        share_type: "HTTPS"
        ignore_certificate_warning: "on"
        share_name: "/share_path/diagnostics_collection_path"
        ip_address: "192.168.0.2"
        file_name: "diagnostics.txt"

- name: Run and export the diagnostics to NFS share
  dellemc.openmanage.idrac_diagnostics:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "path/to/ca_file"
    run: true
    export: true
    share_parameters:
        share_type: "NFS"
        share_name: "nfsshare/diagnostics_collection_path/"
        ip_address: "192.168.0.3"
        file_name: "diagnostics.txt"

- name: Export the diagnostics to CIFS share
  dellemc.openmanage.idrac_diagnostics:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "path/to/ca_file"
    export: true
    share_parameters:
        share_type: "NFS"
        share_name: "/cifsshare/diagnostics_collection_path/"
        ip_address: "192.168.0.4"
        file_name: "diagnostics.txt"

- name: Export the diagnostics to HTTPS share via proxy
  dellemc.openmanage.idrac_diagnostics:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "path/to/ca_file"
    export: true
    share_parameters:
        share_type: "HTTPS"
        share_name: "/share_path/diagnostics_collection_path"
        ignore_certificate_warning: "on"
        ip_address: "192.168.0.2"
        file_name: "diagnostics.txt"
        proxy_support: parameters_proxy
        proxy_type: http
        proxy_server: "192.168.0.5"
        proxy_port: 1080
        proxy_username: "proxy_user"
        proxy_password: "proxy_password"
"""

RETURN = r'''
---
msg:
  type: str
  description: Status of the diagnostics operation.
  returned: always
  sample: "Successfully run and exported the diagnostics."
job_details:
    description: Returns the output for status of the job.
    returned: For import and export operations
    type: dict
    sample: {
        "ActualRunningStartTime": "2024-01-10T10:14:31",
        "ActualRunningStopTime": "2024-01-10T10:26:34",
        "CompletionTime": "2024-01-10T10:26:34",
        "Description": "Job Instance",
        "EndTime": "2024-01-10T10:30:15",
        "Id": "JID_XXXXXXXXXXXX",
        "JobState": "Completed",
        "JobType": "RemoteDiagnostics",
        "Message": "Job completed successfully.",
        "MessageArgs": [],
        "MessageArgs@odata.count": 0,
        "MessageId": "SYS018",
        "Name": "Remote Diagnostics",
        "PercentComplete": 100,
        "StartTime": "2024-01-10T10:12:15",
        "TargetSettingsURI": null
    }
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
      "code": "Base.1.8.GeneralError",
      "message": "A general error has occurred. See ExtendedInfo for more information.",
      "@Message.ExtendedInfo": [
        {
          "MessageId": "Base.1.8.AccessDenied",
          "Message": "The authentication credentials included with this request are missing or invalid.",
          "MessageArgs": [],
          "RelatedProperties": [],
          "Severity": "Critical",
          "Resolution": "Attempt to ensure that the URI is correct and that the service has the appropriate credentials."
        }
      ]
    }
  }
'''

import json
import os
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.compat.version import LooseVersion
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, idrac_auth_params
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    get_idrac_firmware_version, get_dynamic_uri, validate_and_get_first_resource_id_uri, remove_key, idrac_redfish_job_tracking)
from datetime import datetime

MANAGERS_URI = "/redfish/v1/Managers"
IDRAC_JOB_URI = "{res_uri}/Jobs/{job_id}"

OEM = "Oem"
MANUFACTURER = "Dell"
LC_SERVICE = "DellLCService"
ACTIONS = "Actions"
EXPORT = "#DellLCService.ExportePSADiagnosticsResult"
RUN = "#DellLCService.RunePSADiagnostics"

SUCCESS_EXPORT_MSG = "Successfully exported the diagnostics."
EXPORT_NO_RESULTS_MSG = "Unable to export the diagnostics results because the results do not exist."
SUCCESS_RUN_MSG = "Successfully run the diagnostics operation."
SUCCESS_RUN_AND_EXPORT_MSG = "Successfully run and exported the diagnostics."
RUNNING_RUN_MSG = "Successfully triggered the job to run diagnostics."
INVALID_FILE_MSG = "File extension is invalid. Supported extension is: .txt."
INVALID_DIRECTORY_MSG = "Provided directory path '{path}' is not valid."
INSUFFICIENT_DIRECTORY_PERMISSION_MSG = "Provided directory path '{path}' is not writable. " \
                                        "Please check if the directory has appropriate permissions"
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The parameter `job_wait_timeout` value cannot be negative or zero."
WAIT_TIMEOUT_MSG = "The job is not complete after {0} seconds."
START_TIME = "The specified scheduled start time occurs in the past, " \
             "provide a future time to schedule the start time."
INVALID_TIME = "The specified date and time `{0}` to schedule the diagnostics is not valid. Enter a valid date and time."
END_START_TIME = "The end time `{0}` to schedule the diagnostics must be greater than the start time `{1}`."

IGNORE_CERTIFICATE_WARNING = {"off": "Off", "on": "On"}
PROXY_SUPPORT = {"off": "Off", "default_proxy": "DefaultProxy", "parameters_proxy": "ParametersProxy"}
PROXY_TYPE = {"http": "HTTP", "socks": "SOCKS"}


class ExportDiagnostics:
    STATUS_SUCCESS = [200, 202]

    def __init__(self, idrac, module):
        self.idrac = idrac
        self.module = module

    def execute(self, module):
        try:
            share_type = module.params.get('share_parameters').get('share_type')
            export_diagnostics_url = self.__get_export_diagnostics_url(module)
            job_status = {}
            self.__check_file_extension(module)
            if share_type == "local":
                export_diagnostics_status = self.__export_diagnostics_local(module, export_diagnostics_url)
            elif share_type in ["http", "https"]:
                export_diagnostics_status = self.__export_diagnostics_http(module, export_diagnostics_url)
                job_status = self.get_job_status(module, export_diagnostics_status)
            elif share_type == "cifs":
                export_diagnostics_status = self.__export_diagnostics_cifs(module, export_diagnostics_url)
                job_status = self.get_job_status(module, export_diagnostics_status)
            elif share_type == "nfs":
                export_diagnostics_status = self.__export_diagnostics_nfs(module, export_diagnostics_url)
                job_status = self.get_job_status(module, export_diagnostics_status)
            status = export_diagnostics_status.status_code
            if status in self.STATUS_SUCCESS:
                msg = SUCCESS_EXPORT_MSG
                job_details = job_status
                return msg, job_details
        except HTTPError as err:
            err_msg = json.loads(err.read())["error"]["@Message.ExtendedInfo"][0]["Message"]
            if err_msg == EXPORT_NO_RESULTS_MSG:
                module.exit_json(msg=EXPORT_NO_RESULTS_MSG, skipped=True)
            module.exit_json(msg=err_msg, failed=True)
        return export_diagnostics_status

    def __export_diagnostics_local(self, module, export_diagnostics_url):
        payload = {}
        payload["ShareType"] = "Local"
        path = module.params.get('share_parameters').get('share_name')
        if not (os.path.exists(path) or os.path.isdir(path)):
            module.fail_json(msg=INVALID_DIRECTORY_MSG.format(path=path), failed=True)
        if not os.access(path, os.W_OK):
            module.fail_json(msg=INSUFFICIENT_DIRECTORY_PERMISSION_MSG.format(path=path), failed=True)
        diagnostics_status = self.__export_diagnostics(module, payload, export_diagnostics_url)
        diagnostics_file_name = payload.get("FileName")
        diagnostics_data = self.idrac.invoke_request(diagnostics_status.headers.get("Location"), "GET")
        diagnostics_output = [line + "\n" for line in diagnostics_data.body.decode().split("\r\n")]
        file_name = os.path.join(path, diagnostics_file_name)
        with open(file_name, "w") as fp:
            fp.writelines(diagnostics_output)
        return diagnostics_status

    def __export_diagnostics_http(self, module, export_diagnostics_url):
        payload = {}
        proxy_details = self.get_proxy_details(module)
        payload.update(proxy_details)
        export_status = self.__export_diagnostics(module, payload, export_diagnostics_url)
        return export_status

    def __export_diagnostics_cifs(self, module, export_diagnostics_url):
        payload = {}
        payload["ShareType"] = "CIFS"
        if module.params.get('share_parameters').get('workgroup'):
            payload["Workgroup"] = module.params.get('share_parameters').get('workgroup')
        share_details = self.get_share_details(module)
        payload.update(share_details)
        export_status = self.__export_diagnostics(module, payload, export_diagnostics_url)
        return export_status

    def __export_diagnostics_nfs(self, module, export_diagnostics_url):
        payload = {}
        payload["ShareType"] = "NFS"
        payload["IPAddress"] = module.params.get('share_parameters').get('ip_address')
        payload["ShareName"] = module.params.get('share_parameters').get('share_name')
        payload["FileName"] = module.params.get('share_parameters').get('file_name')
        export_status = self.__export_diagnostics(module, payload, export_diagnostics_url)
        return export_status

    def __get_export_diagnostics_url(self, module):
        uri, error_msg = validate_and_get_first_resource_id_uri(
            self.module, self.idrac, MANAGERS_URI)
        if error_msg:
            self.module.exit_json(msg=error_msg, failed=True)
        resp = get_dynamic_uri(self.idrac, uri)
        url = resp.get('Links', {}).get(OEM, {}).get(MANUFACTURER, {}).get(LC_SERVICE, {}).get('@odata.id', {})
        action_resp = get_dynamic_uri(self.idrac, url)
        export_url = action_resp.get(ACTIONS, {}).get(EXPORT, {}).get('target', {})
        return export_url

    def __export_diagnostics(self, module, payload, export_diagnostics_url):
        diagnostics_file_name = module.params.get('share_parameters').get('file_name')
        if not diagnostics_file_name:
            now = datetime.now()
            hostname = module.params.get('idrac_ip')
            diagnostics_file_name = "{}_{}.txt".format(hostname, now.strftime("%Y%m%d_%H%M%S"))
        payload["FileName"] = diagnostics_file_name
        diagnostics_status = self.idrac.invoke_request(export_diagnostics_url, "POST", data=payload)
        return diagnostics_status

    def __check_file_extension(self, module):
        file_name = module.params.get('share_parameters').get('file_name')
        if file_name:
            file_extension = file_name.lower().endswith(".txt")
            if not file_extension:
                module.exit_json(msg=INVALID_FILE_MSG, failed=True)

    def get_job_status(self, module, export_diagnostics_status):
        res_uri = validate_and_get_first_resource_id_uri(self.module, self.idrac, MANAGERS_URI)
        job_tracking_uri = export_diagnostics_status.headers.get("Location")
        job_id = job_tracking_uri.split("/")[-1]
        job_uri = IDRAC_JOB_URI.format(job_id=job_id, res_uri=res_uri[0])
        job_failed, msg, job_dict, wait_time = idrac_redfish_job_tracking(self.idrac, job_uri)
        job_dict = remove_key(job_dict, regex_pattern='(.*?)@odata')
        if job_failed:
            module.exit_json(msg=job_dict.get('Message'), failed=True, job_details=job_dict)
        return job_dict

    def get_share_details(self, module):
        share_details = {}
        share_details["IPAddress"] = module.params.get('share_parameters').get('ip_address')
        share_details["ShareName"] = module.params.get('share_parameters').get('share_name')
        share_details["UserName"] = module.params.get('share_parameters').get('username')
        share_details["Password"] = module.params.get('share_parameters').get('password')
        share_details["FileName"] = module.params.get('share_parameters').get('file_name')
        return share_details

    def get_proxy_details(self, module):
        proxy_details = {}
        if module.params.get('share_parameters').get('share_type') == "http":
            proxy_details["ShareType"] = "HTTP"
        else:
            proxy_details["ShareType"] = "HTTPS"
        proxy_details["IPAddress"] = module.params.get('share_parameters').get('ip_address')
        proxy_details["ShareName"] = module.params.get('share_parameters').get('share_name')
        proxy_details["UserName"] = module.params.get('share_parameters').get('username')
        proxy_details["Password"] = module.params.get('share_parameters').get('password')
        proxy_details["FileName"] = module.params.get('share_parameters').get('file_name')
        proxy_details["IgnoreCertWarning"] = IGNORE_CERTIFICATE_WARNING[module.params.get('share_parameters').get('ignore_certificate_warning')]
        if module.params.get('share_parameters').get('proxy_support') == "parameters_proxy":
            proxy_details["ProxySupport"] = PROXY_SUPPORT[module.params.get('share_parameters').get('proxy_support')]
            proxy_details["ProxyType"] = PROXY_TYPE[module.params.get('share_parameters').get('proxy_type')]
            proxy_details["ProxyServer"] = module.params.get('share_parameters').get('proxy_server')
            proxy_details["ProxyPort"] = module.params.get('share_parameters').get('proxy_port')
            if module.params.get('share_parameters').get('proxy_username') and module.params.get('share_parameters').get('proxy_password'):
                proxy_details["ProxyUname"] = module.params.get('share_parameters').get('proxy_username')
                proxy_details["ProxyPasswd"] = module.params.get('share_parameters').get('proxy_password')
        return proxy_details


def main():
    specs = get_argument_spec()
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        required_if=[
            ["run", True, ("reboot_type", "run_mode",)],
            ["export", True, ("share_parameters",)]
        ],
        supports_check_mode=False
    )

    try:
        with iDRACRedfishAPI(module.params) as idrac:
            idrac_firmware_version = get_idrac_firmware_version(idrac)
            if LooseVersion(idrac_firmware_version) <= '3.0':
                module.exit_json(msg="iDRAC firmware version is not supported.", failed=True)
            diagnostics_ob = None
            if module.params["export"]:
                diagnostics_ob = ExportDiagnostics(idrac, module)
            if diagnostics_ob:
                msg, job_status = diagnostics_ob.execute(module)
                module.exit_json(msg=msg, changed=True, job_details=job_status)
            else:
                module.exit_json(msg="Task is skipped as none of run, export or run and export is specified.", skipped=True)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (ImportError, ValueError, RuntimeError, SSLValidationError,
            ConnectionError, KeyError, TypeError, IndexError) as e:
        module.exit_json(msg=str(e), failed=True)


def get_argument_spec():
    return {
        "run": {"type": 'bool', "default": True},
        "export": {"type": 'bool', "default": True},
        "run_mode": {
            "type": 'str',
            "default": 'express',
            "choices": ['express', 'extended', 'long_run']
        },
        "reboot_type": {
            "type": 'str',
            "default": 'graceful',
            "choices": ['force', 'graceful', 'power_cycle']
        },
        "scheduled_start_time": {"type": 'str'},
        "scheduled_end_time": {"type": 'str'},
        "job_wait": {"type": 'bool', "default": True},
        "job_wait_timeout": {"type": 'int', "default": 1200},
        "share_parameters": {
            "type": 'dict',
            "options": {
                "share_type": {
                    "type": 'str',
                    "default": 'local',
                    "choices": ['local', 'nfs', 'cifs', 'http', 'https']
                },
                "file_name": {"type": 'str'},
                "ip_address": {"type": 'str'},
                "share_name": {"type": 'str'},
                "workgroup": {"type": 'str'},
                "username": {"type": 'str'},
                "password": {"type": 'str', "no_log": True},
                "ignore_certificate_warning": {
                    "type": 'str',
                    "default": "off",
                    "choices": ["off", "on"]
                },
                "proxy_support": {
                    "type": 'str',
                    "default": "off",
                    "choices": ["off", "default_proxy", "parameters_proxy"]
                },
                "proxy_type": {
                    "type": 'str',
                    "default": 'http',
                    "choices": ['http', 'socks']
                },
                "proxy_server": {"type": 'str'},
                "proxy_port": {"type": 'str', "default": '80'},
                "proxy_username": {"type": 'str'},
                "proxy_password": {"type": 'str', "no_log": True}
            },
            "required_if": [
                ["share_type", "local", ["share_name"]],
                ["share_type", "nfs", ["ip_address", "share_name"]],
                ["share_type", "cifs", ["ip_address", "share_name", "username", "password"]],
                ["share_type", "http", ["ip_address", "share_name"]],
                ["share_type", "https", ["ip_address", "share_name"]],
                ["proxy_support", "parameters_proxy", ["proxy_server"]]
            ],
            "required_together": [
                ("username", "password"),
                ("proxy_username", "proxy_password")
            ]
        },
        "resource_id": {"type": 'str'}
    }


if __name__ == '__main__':
    main()
