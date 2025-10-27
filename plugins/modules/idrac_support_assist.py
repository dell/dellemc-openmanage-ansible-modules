#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.6.0
# Copyright (C) 2024-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: idrac_support_assist
short_description: Run and Export iDRAC SupportAssist collection logs
version_added: "9.6.0"
description:
  - This module allows you to run and export SupportAssist collection logs on iDRAC.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_x_auth_options
options:
  run:
    description:
      - Run the SupportAssist job based on the different types of logs in the collection on iDRAC.
    type: bool
    default: true
  export:
    description:
      - Exports the SupportAssist collection to the given network share.
      - This operation requires I(share_parameters).
    type: bool
    default: true
  accept_eula:
    description:
      - This parameter accepts the EULA terms and conditions that are required for SupportAssist registration.
      - If EULA terms and conditions are not accepted, then the SupportAssist collection cannot be run or exported.
    type: bool
  filter_data:
    description:
      - This option provides the choice to filter data for privacy. It does not include hostname, MAC address, thermal data, logs, or registry content.
    type: bool
    default: false
  data_collector:
    description:
      - This option provides the choice of data to keep in SupportAssist collection.
      - System Information is available in on the SupportAssist collection by default.
      - C(hardware_data), SupportAssist collection includes data that are related to hardware.
      - C(storage_logs), SupportAssist collection includes logs that are related to storage devices.
      - C(os_app_data), SupportAssist collection includes data that is related to the operating system and applications.
      - C(debug_logs), SupportAssist collection includes logs that are related to debugging.
      - C(telemetry_reports), SupportAssist collection includes reports that are related to telemetry.
      - C(gpu_logs), SupportAssist collection includes logs that are related to GPUs.
    type: list
    elements: str
    choices: [hardware_data, storage_logs, os_app_data, debug_logs, telemetry_reports, gpu_logs]
  job_wait:
    description:
      - This option determines whether to wait for the job completion or not.
    type: bool
    default: true
  job_wait_timeout:
    description:
      - Time in seconds to wait for job completion.
      - This is applicable when I(job_wait) is C(true).
    type: int
    default: 3600
  share_parameters:
    description:
      - Parameters that are required for the export operation of SupportAssist collection.
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
          - C(ftp) uses FTP share for I(export) operation.
        type: str
        choices: [local, nfs, cifs, http, https, ftp]
        default: local
      ip_address:
        description:
          - IP address of the network share.
          - I(ip_address) is required when I(share_type) is C(nfs), C(cifs), C(http), or C(https).
          - I(ip_address) is not required when I(share_type) is C(local).
        type: str
      share_name:
        description:
          - Network share path or full local path of the directory for exporting the SupportAssist collection file.
          - The default path will be current directory when I(share_type) is C(local)
        type: str
      workgroup:
        description:
          -(deprecated) Workgroup of the network share.
          - I(workgroup) is applicable only when I(share_type) is C(cifs).
          - The argument is not supported by iDRAC9 and iDRAC10.
        type: str
      username:
        description:
          - Username of the network share.
          - I(username) is required when I(share_type) is C(cifs).
        type: str
        aliases: ['share_username']
      password:
        description:
          - Password of the network share.
          - I(password) is required when I(share_type) is C(cifs).
        type: str
        aliases: ['share_password']
      ignore_certificate_warning:
        description:
          - Ignores the certificate warning when connecting to the network share and is only applicable when I(share_type) is C(https).
          - C(on) ignores the certificate warning.
          - C(off) does not ignore the certificate warning.
        type: str
        choices: ["off", "on"]
        default: "off"
      proxy_support:
        description:
          - Specifies if proxy support must be used or not.
          - C(off) does not use proxy settings.
          - C(default_proxy) uses the default proxy settings.
          - C(parameters_proxy) uses the specified proxy settings. I(proxy_server) is required when I(proxy_support) is C(parameters_proxy).
          - I(proxy_support) is only applicable when I(share_type) is C(http) or C(https).
        type: str
        choices: ["off", "default_proxy", "parameters_proxy"]
        default: "off"
      proxy_type:
        description:
          - The proxy type of the proxy server.
          - C(http) to select HTTP proxy.
          - C(socks) to select SOCKS proxy.
          - I(proxy_type) is only applicable when I(share_type) is C(http) or C(https) and when I(proxy_support) is C(parameters_proxy).
        type: str
        choices: [http, socks]
        default: http
      proxy_server:
        description:
          - The IP address of the proxy server.
          - I(proxy_server) is required when I(proxy_support) is C(parameters_proxy).
          - I(proxy_server) is only applicable when I(share_type) is C(http) or C(https) and when I(proxy_support) is C(parameters_proxy).
        type: str
      proxy_port:
        description:
          - The port of the proxy server.
          - I(proxy_port) is only applicable when I(share_type) is C(http) or C(https) and when I(proxy_support) is C(parameters_proxy).
        type: int
        default: 80
      proxy_username:
        description:
          - The username of the proxy server.
          - I(proxy_username) is only applicable when I(share_type) is C(http) or C(https) and when I(proxy_support) is C(parameters_proxy).
        type: str
      proxy_password:
        description:
          - The password of the proxy server.
          - I(proxy_password) is only applicable when I(share_type) is C(http) or C(https) and when I(proxy_support) is C(parameters_proxy).
        type: str
  resource_id:
    type: str
    description:
      - Id of the resource.
      - If the value for resource ID is not provided, the module picks the first resource ID available from the list of system resources that
        are returned by the iDRAC.
requirements:
  - "python >= 3.9.6"
author:
  - "Shivam Sharma(@ShivamSh3)"
attributes:
    check_mode:
        description: Runs task to validate without performing action on the target machine.
        support: full
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports only iDRAC9 and above.
    - This module supports IPv4 and IPv6 addresses.
    - C(local) for I(share_type) is applicable only when I(run) and I(export) is C(true).
    - When I(share_type) is C(local) for I(run) and (export) operation, then job_wait is not applicable.
"""

EXAMPLES = r"""
---
- name: Accept the EULA and run and export the SupportAssist Collection to local path
  dellemc.openmanage.idrac_support_assist:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    accept_eula: true
    ca_path: "path/to/ca_file"
    data_collector: ["debug_logs", "hardware_data", "os_app_data", "storage_logs"]
    share_parameters:
      share_type: "local"
      share_path: "/opt/local/support_assist_collections/"

- name: Run the SupportAssist Collection with with custom data_to_collect with filter_data
  dellemc.openmanage.idrac_support_assist:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "path/to/ca_file"
    export: false
    filter_data: true
    data_collector: ["debug_logs", "hardware_data"]

- name: Run and export the SupportAssist Collection to HTTPS share
  dellemc.openmanage.idrac_support_assist:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "path/to/ca_file"
    data_collector: ["hardware_data"]
    share_parameters:
      share_type: "https"
      ignore_certificate_warning: "on"
      share_name: "/share_path/support_assist_collections"
      ip_address: "192.168.0.2"

- name: Run and export the SupportAssist Collection to NFS share
  dellemc.openmanage.idrac_support_assist:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "path/to/ca_file"
    data_collector: ["debug_logs"]
    share_parameters:
      share_type: "nfs"
      share_name: "nfsshare/support_assist_collections/"
      ip_address: "192.168.0.3"

- name: Export the last SupportAssist Collection to CIFS share
  dellemc.openmanage.idrac_support_assist:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "path/to/ca_file"
    run: false
    share_parameters:
      share_type: "nfs"
      share_name: "/cifsshare/support_assist_collections/"
      ip_address: "192.168.0.4"

- name: Export the last SupportAssist Collection to HTTPS share via proxy
  dellemc.openmanage.idrac_support_assist:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "path/to/ca_file"
    run: false
    share_parameters:
      share_type: "https"
      share_name: "/share_path/support_assist_collections"
      ignore_certificate_warning: "on"
      ip_address: "192.168.0.2"
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
  description: Status of the SupportAssist operation.
  returned: always
  sample: "Successfully ran and exported the SupportAssist collection."
job_details:
    description: Returns the output for status of the job.
    returned: For run and export operations
    type: dict
    sample: {
        "ActualRunningStartTime": "2024-07-08T01:50:54",
        "ActualRunningStopTime": "2024-07-08T01:56:45",
        "CompletionTime": "2024-07-08T01:56:45",
        "Description": "Job Instance",
        "EndTime": null,
        "Id": "JID_XXXXXXXXXXXX",
        "JobState": "Completed",
        "JobType": "SACollectExportHealthData",
        "Message": "The SupportAssist Collection and Transmission Operation is completed successfully.",
        "MessageArgs": [],
        "MessageArgs@odata.count": 0,
        "MessageId": "SRV088",
        "Name": "SupportAssist Collection",
        "PercentComplete": 100,
        "StartTime": "2024-07-08T01:50:54",
        "TargetSettingsURI": null
    }
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
      "code": "Base.1.12.GeneralError",
      "message": "A general error has occurred. See ExtendedInfo for more information.",
      "@Message.ExtendedInfo": [
        {
            "Message": "Unable to start the operation because the SupportAssist End User License Agreement (EULA) is not accepted.",
            "MessageArgs": [],
            "MessageArgs@odata.count": 0,
            "MessageId": "IDRAC.2.8.SRV085",
            "RelatedProperties": [],
            "RelatedProperties@odata.count": 0,
            "Resolution": "Accept the SupportAssist End User License Agreement (EULA) by navigating to the SupportAssist page on the iDRAC GUI.",
            "Severity": "Warning"
        }
      ]
    }
  }
'''
import json
import os
from datetime import datetime
import time
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, IdracAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    get_dynamic_uri, validate_and_get_first_resource_id_uri, remove_key, idrac_redfish_job_tracking)

MANAGERS_URI = "/redfish/v1/Managers"

OEM = "Oem"
MANUFACTURER = "Dell"
JOBS = "Jobs"
JOBS_EXPAND = "?$expand=*($levels=1)"
LC_SERVICE = "DellLCService"
ACTIONS = "Actions"
ACCEPT_EULA = "#DellLCService.SupportAssistAcceptEULA"
EULA_STATUS = "#DellLCService.SupportAssistGetEULAStatus"
EXPORT = "#DellLCService.SupportAssistExportLastCollection"
RUN = "#DellLCService.SupportAssistCollection"
TEST_SHARE = "#DellLCService.TestNetworkShare"
DATA_SELECTOR = "DataSelectorArrayIn@Redfish.AllowableValues"
ODATA_REGEX = "(.*?)@odata"
ODATA = "@odata.id"
MESSAGE_EXTENDED_INFO = "@Message.ExtendedInfo"
SUCCESS_EXPORT_MSG = "Successfully exported the support assist collections."
SUCCESS_RUN_MSG = "Successfully ran the support assist collections."
SUCCESS_RUN_AND_EXPORT_MSG = "Successfully ran and exported the support assist collections."
RUNNING_RUN_MSG = "Successfully triggered the job to run support assist collections."
RUNNING_RUN_AND_EXPORT_MSG = "Successfully triggered the job to run and export support assist collections."
ALREADY_RUN_MSG = "The support assist collections job is already present."
INVALID_DIRECTORY_MSG = "Provided directory path '{path}' is not valid."
NO_OPERATION_SKIP_MSG = "The operation is skipped."
OPERATION_NOT_ALLOWED_MSG = "Export to local is only supported when both run and export is set to true."
INSUFFICIENT_DIRECTORY_PERMISSION_MSG = "Provided directory path '{path}' is not writable. " \
                                        "Please check if the directory has appropriate permissions"
UNSUPPORTED_FIRMWARE_MSG = "iDRAC firmware version is not supported."
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The parameter `job_wait_timeout` value cannot be negative or zero."
WAIT_TIMEOUT_MSG = "The job is not complete after {0} seconds."
CHANGES_FOUND_MSG = "Changes found to be applied."
CHANGES_NOT_FOUND_MSG = "No changes found to be applied."
ALLOWED_VALUES_MSG = "Enter a valid value from the list of allowable values: {0}"
NO_VALUE_MSG = "data_collector can't be empty. Enter a valid value."
NO_FILE = "The support assist collections log does not exist."
TIME_FORMAT = "%Y%m%d_%H%M%S"

PROXY_SUPPORT = {"off": "Off", "default_proxy": "DefaultProxy",
                 "parameters_proxy": "ParametersProxy"}
STATUS_SUCCESS = [200, 202]


class SupportAssist:

    def __init__(self, idrac, module):
        self.idrac = idrac
        self.module = module
        self.run_url = None
        self.export_url = None
        self.share_name = None

    def execute(self):
        # To be overridden by the subclasses
        pass

    def get_payload_details(self):
        payload = {}
        payload["ShareType"] = self.module.params.get(
            'share_parameters').get('share_type').upper()
        payload["IPAddress"] = self.module.params.get(
            'share_parameters').get('ip_address')
        payload["ShareName"] = self.module.params.get(
            'share_parameters').get('share_name')
        payload["UserName"] = self.module.params.get(
            'share_parameters').get('username')
        payload["Password"] = self.module.params.get(
            'share_parameters').get('password')
        payload["IgnoreCertWarning"] = self.module.params.get(
            'share_parameters').get('ignore_certificate_warning').capitalize()
        if self.module.params.get('share_parameters').get('proxy_support') == "parameters_proxy":
            payload["ProxySupport"] = PROXY_SUPPORT[self.module.params.get(
                'share_parameters').get('proxy_support')]
            payload["ProxyType"] = self.module.params.get(
                'share_parameters').get('proxy_type').upper()
            payload["ProxyServer"] = self.module.params.get(
                'share_parameters').get('proxy_server')
            payload["ProxyPort"] = str(self.module.params.get(
                'share_parameters').get('proxy_port'))
            if self.module.params.get('share_parameters').get('proxy_username') and self.module.params.get('share_parameters').get('proxy_password'):
                payload["ProxyUname"] = self.module.params.get(
                    'share_parameters').get('proxy_username')
                payload["ProxyPasswd"] = self.module.params.get(
                    'share_parameters').get('proxy_password')
        return payload

    def test_network_share(self):
        payload = self.get_payload_details()
        payload = {key: value for key,
                   value in payload.items() if value is not None}
        if payload.get("ShareType") == "LOCAL":
            path = payload.get("ShareName")
            if not (os.path.exists(path)):
                self.module.exit_json(
                    msg=INVALID_DIRECTORY_MSG.format(path=path), failed=True)
            if not os.access(path, os.W_OK):
                self.module.exit_json(
                    msg=INSUFFICIENT_DIRECTORY_PERMISSION_MSG.format(path=path), failed=True)
        else:
            try:
                test_url = self.get_test_network_share_url()
                self.idrac.invoke_request(test_url, "POST", data=payload)
            except HTTPError as err:
                filter_err = remove_key(
                    json.load(err), regex_pattern=ODATA_REGEX)
                message_details = filter_err.get(
                    'error').get(MESSAGE_EXTENDED_INFO)[0]
                message = message_details.get('Message')
                self.module.exit_json(
                    msg=message, error_info=filter_err, failed=True)

    def get_test_network_share_url(self):
        uri, error_msg = validate_and_get_first_resource_id_uri(
            self.module, self.idrac, MANAGERS_URI)
        if error_msg:
            self.module.exit_json(msg=error_msg, failed=True)
        resp = get_dynamic_uri(self.idrac, uri)
        url = resp.get('Links', {}).get(OEM, {}).get(
            MANUFACTURER, {}).get(LC_SERVICE, {}).get(ODATA, {})
        action_resp = get_dynamic_uri(self.idrac, url)
        url = action_resp.get(ACTIONS, {}).get(
            TEST_SHARE, {}).get('target', {})
        return url


class AcceptEULA(SupportAssist):
    def __init__(self, idrac, module):
        self.idrac = idrac
        self.module = module
        self.eula_status_url = None
        self.eula_accept_url = None

    def execute(self):
        msg = None
        self.__get_eula_status_url()
        if self.module.check_mode:
            self.perform_check_mode()
        self.__get_eula_accept_url()
        eula_status = self.eula_status()
        if eula_status.status_code in STATUS_SUCCESS:
            data = eula_status.json_data.get(MESSAGE_EXTENDED_INFO)
            message_details = data[0]
            msg = message_details.get('Message')
            message_ids = [dict_item['MessageId'] for dict_item in data]
            for string in message_ids:
                if 'SRV074' in string and (self.module.params.get("run") or self.module.params.get("export")):
                    return msg
        if self.module.params.get("accept_eula"):
            eula_accept_status = self.accept_eula()
        if eula_accept_status.status_code in STATUS_SUCCESS:
            data = eula_accept_status.json_data.get(MESSAGE_EXTENDED_INFO)
            message_details = data[0]
            message_id = message_details.get('MessageId')
            msg = message_details.get('Message')
            if 'SRV074' in message_id:
                return msg

    def __get_eula_status_url(self):
        uri, error_msg = validate_and_get_first_resource_id_uri(
            self.module, self.idrac, MANAGERS_URI)
        if error_msg:
            self.module.exit_json(msg=error_msg, failed=True)
        resp = get_dynamic_uri(self.idrac, uri)
        url = resp.get('Links', {}).get(OEM, {}).get(
            MANUFACTURER, {}).get(LC_SERVICE, {}).get(ODATA, {})
        if url:
            action_resp = get_dynamic_uri(self.idrac, url)
            eula_status_url = action_resp.get(ACTIONS, {}).get(
                EULA_STATUS, {}).get('target', {})
            self.eula_status_url = eula_status_url
        else:
            self.module.exit_json(msg=UNSUPPORTED_FIRMWARE_MSG, failed=True)

    def __get_eula_accept_url(self):
        uri, error_msg = validate_and_get_first_resource_id_uri(
            self.module, self.idrac, MANAGERS_URI)
        if error_msg:
            self.module.exit_json(msg=error_msg, failed=True)
        resp = get_dynamic_uri(self.idrac, uri)
        url = resp.get('Links', {}).get(OEM, {}).get(
            MANUFACTURER, {}).get(LC_SERVICE, {}).get(ODATA, {})
        if url:
            action_resp = get_dynamic_uri(self.idrac, url)
            eula_accept_url = action_resp.get(ACTIONS, {}).get(
                ACCEPT_EULA, {}).get('target', {})
            self.eula_accept_url = eula_accept_url
        else:
            self.module.exit_json(msg=UNSUPPORTED_FIRMWARE_MSG, failed=True)

    def eula_status(self):
        eula_status = self.idrac.invoke_request(
            self.eula_status_url, "POST", data="{}", dump=False)
        return eula_status

    def accept_eula(self):
        eula_accept_status = self.idrac.invoke_request(
            self.eula_accept_url, "POST", data="{}", dump=False)
        return eula_accept_status

    def perform_check_mode(self):
        eula_status = self.eula_status()
        if eula_status.status_code in STATUS_SUCCESS:
            data = eula_status.json_data.get(MESSAGE_EXTENDED_INFO)
            message_ids = [dict_item['MessageId'] for dict_item in data]
            # Create a mapping of conditions to actions
            actions = {
                'SRV104': {
                    True: (CHANGES_FOUND_MSG, True),
                    False: (CHANGES_NOT_FOUND_MSG, False),
                    None: (CHANGES_NOT_FOUND_MSG, False)
                },
                'SRV074': {
                    True: (CHANGES_NOT_FOUND_MSG, False),
                    False: (CHANGES_FOUND_MSG, True),
                    None: (CHANGES_FOUND_MSG, True)
                }
            }
            # Iterate over message IDs and determine the action
            for string in message_ids:
                for key, value in actions.items():
                    if key in string:
                        msg, changed = value[self.module.params.get(
                            "accept_eula")]
                        self.module.exit_json(msg=msg, changed=changed)


class RunSupportAssist(SupportAssist):

    def execute(self):
        msg, job_details = None, None
        if self.module.params.get('export'):
            self.test_network_share()
        self.__get_run_support_assist_url()
        self.check_support_assist_jobs()
        self.__validate_job_timeout()
        run_support_assist_status = self.__run_support_assist()
        job_status = self.__perform_job_wait(run_support_assist_status)
        status = run_support_assist_status.status_code
        if status in STATUS_SUCCESS and job_status.get('JobState') in ["Completed", "CompletedWithErrors"]:
            msg = SUCCESS_RUN_MSG
            if self.module.params.get('run') and self.module.params.get('export'):
                msg = SUCCESS_RUN_AND_EXPORT_MSG
            job_details = job_status
        if status in STATUS_SUCCESS and job_status.get('JobState') in ["Scheduled", "Scheduling", "Running", "New"]:
            msg = RUNNING_RUN_MSG
            if self.module.params.get('run') and self.module.params.get('export'):
                msg = RUNNING_RUN_AND_EXPORT_MSG
            job_details = job_status
        return msg, job_details

    def __run_support_assist(self):
        data_selector = {
            "hardware_data": "HWData",
            "storage_logs": "TTYLogs",
            "os_app_data": "OSAppData",
            "debug_logs": "DebugLogs",
            "telemetry_reports": "TelemetryReports",
            "gpu_logs": "GPULogs"
        }
        payload = {}
        data_selected = self.module.params.get('data_collector')
        if data_selected == []:
            self.module.exit_json(msg=NO_VALUE_MSG, skipped=True)
        data = [data_selector.get(item, item) for item in data_selected]
        self.__validate_input(data, data_selector)
        payload["DataSelectorArrayIn"] = data
        if self.module.params.get('filter_data'):
            payload["Filter"] = "Yes"
        if self.module.params.get('export'):
            share_payload_obj = ExportSupportAssist(self.idrac, self.module)
            share_payload = share_payload_obj.execute()
            payload.update(share_payload)
            payload = {k: v for k, v in payload.items() if v is not None}
        run_support_assist_status = self.idrac.invoke_request(
            self.run_url, "POST", data=payload)
        return run_support_assist_status

    def __validate_input(self, data_selected, data_selector):
        uri, error_msg = validate_and_get_first_resource_id_uri(
            self.module, self.idrac, MANAGERS_URI)
        if error_msg:
            self.module.exit_json(msg=error_msg, failed=True)
        resp = get_dynamic_uri(self.idrac, uri)
        url = resp.get('Links', {}).get(OEM, {}).get(
            MANUFACTURER, {}).get(LC_SERVICE, {}).get(ODATA, {})
        allowable_values_response = self.idrac.invoke_request(url, "GET")
        allowable_values = allowable_values_response.json_data[ACTIONS][RUN][DATA_SELECTOR]
        invalid_values = [
            item for item in data_selected if item not in allowable_values]
        if invalid_values:
            allowed_keys = [
                key for key, value in data_selector.items() if value not in invalid_values]
            allowed_values = [
                key for key, value in data_selector.items() if key in allowed_keys]
            self.module.exit_json(msg=ALLOWED_VALUES_MSG.format(
                allowed_values), skipped=True)

    def __get_run_support_assist_url(self):
        uri, error_msg = validate_and_get_first_resource_id_uri(
            self.module, self.idrac, MANAGERS_URI)
        if error_msg:
            self.module.exit_json(msg=error_msg, failed=True)
        resp = get_dynamic_uri(self.idrac, uri)
        url = resp.get('Links', {}).get(OEM, {}).get(
            MANUFACTURER, {}).get(LC_SERVICE, {}).get(ODATA, {})
        if url:
            action_resp = get_dynamic_uri(self.idrac, url)
            run_url = action_resp.get(ACTIONS, {}).get(
                RUN, {}).get('target', {})
            self.run_url = run_url
        else:
            self.module.exit_json(msg=UNSUPPORTED_FIRMWARE_MSG, failed=True)

    def __validate_job_timeout(self):
        if self.module.params.get("job_wait") and self.module.params.get("job_wait_timeout") <= 0:
            self.module.exit_json(
                msg=TIMEOUT_NEGATIVE_OR_ZERO_MSG, failed=True)

    def __perform_job_wait(self, run_support_assist_status):
        job_details = {}
        job_wait = self.module.params.get('job_wait')
        share_params = self.module.params.get('share_parameters') or {}
        local_share = share_params.get('share_type') or False
        timeout_of_job_wait = self.module.params.get('job_wait_timeout')
        job_tracking_uri = run_support_assist_status.headers.get("Location")
        if job_tracking_uri:
            job_id = job_tracking_uri.split("/")[-1]
            res_uri = validate_and_get_first_resource_id_uri(
                self.module, self.idrac, MANAGERS_URI)
            job_uri = f"{res_uri[0]}/{OEM}/{MANUFACTURER}/{JOBS}/{job_id}"
            if job_wait or local_share == 'local':
                failed_job, message, job_details, time_to_wait = idrac_redfish_job_tracking(self.idrac, job_uri,
                                                                                            max_job_wait_sec=timeout_of_job_wait,
                                                                                            sleep_interval_secs=1)
                job_details = remove_key(job_details, regex_pattern=ODATA_REGEX)
                if int(time_to_wait) >= int(timeout_of_job_wait):
                    self.module.exit_json(msg=WAIT_TIMEOUT_MSG.format(
                        timeout_of_job_wait), changed=True, job_status=job_details)
                if failed_job:
                    self.module.exit_json(
                        msg=job_details.get("Message"), job_status=job_details, failed=True)
            else:
                job_response = self.idrac.invoke_request(job_uri, 'GET')
                job_details = job_response.json_data
                job_details = remove_key(job_details, regex_pattern=ODATA_REGEX)
        self.file_download(job_tracking_uri, local_share)
        return job_details

    def file_download(self, job_tracking_uri, local_share):
        if job_tracking_uri and local_share == 'local':
            file_path = self.module.params.get(
                'share_parameters').get('share_name')
            now = datetime.now()
            hostname = self.module.params.get('idrac_ip')
            hostname = self.expand_ipv6(hostname)
            hostname = hostname.replace(":", ".")
            sa_file_name = f"{hostname}_{now.strftime(TIME_FORMAT)}.zip"
            file_name = (os.path.join(file_path, sa_file_name))
            time.sleep(10)
            file_dict = self.idrac.invoke_request(job_tracking_uri, "GET",
                                                  api_timeout=200)
            time.sleep(10)
            file_dnld = self.idrac.invoke_request(file_dict.headers.get(
                "Location"), "GET",
                headers={"Content-Type": "application/x-tar"},
                api_timeout=200)
            if file_dnld.status_code == 200:
                with open(file_name, "wb") as file:
                    file.write(file_dnld.body)

    def expand_ipv6(self, ip):
        sections = ip.split(':')
        num_sections = len(sections)
        double_colon_index = sections.index('') if '' in sections else -1
        if double_colon_index != -1:
            missing_sections = 8 - num_sections + 1
            sections[double_colon_index:double_colon_index + 1] = ['0000'] * missing_sections
        sections = [section.zfill(4) for section in sections]
        expanded_ip = ':'.join(sections)
        return expanded_ip

    def check_support_assist_jobs(self):
        res_uri = validate_and_get_first_resource_id_uri(
            self.module, self.idrac, MANAGERS_URI)
        job_uri = f"{res_uri[0]}/{OEM}/{MANUFACTURER}/{JOBS}{JOBS_EXPAND}"
        job_resp = self.idrac.invoke_request(job_uri, "GET")
        job_list = job_resp.json_data.get('Members', [])
        job_id = ""
        for jb in job_list:
            if (jb.get("JobType") == "SACollectHealthData" or jb.get("JobType") ==
               "SACollectExportHealthData") and jb.get("JobState") in ["Scheduled", "Running", "Starting", "New"]:
                job_id = jb['Id']
                job_dict = remove_key(jb, regex_pattern=ODATA_REGEX)
                break
        if self.module.check_mode and job_id:
            self.module.exit_json(msg=ALREADY_RUN_MSG,
                                  job_details=job_dict, skipped=True)
        if self.module.check_mode and not job_id:
            eula_status_obj = AcceptEULA(self.idrac, self.module)
            eula_status_obj.execute()
        if job_id:
            self.module.exit_json(msg=ALREADY_RUN_MSG,
                                  job_details=job_dict, skipped=True)


class ExportSupportAssist(SupportAssist):

    def execute(self):
        self.test_network_share()
        RunSupportAssist.check_support_assist_jobs(self)
        self.__get_export_support_assist_url()
        if self.module.check_mode:
            self.perform_check_mode()
        job_status = {}
        share_type = self.module.params.get(
            'share_parameters').get('share_type')
        share_type_methods = {
            "local": self.__export_support_assist_local,
            "http": self.__export_support_assist_remote_shares,
            "https": self.__export_support_assist_remote_shares,
            "cifs": self.__export_support_assist_remote_shares,
            "nfs": self.__export_support_assist_nfs,
            "ftp": self.__export_support_assist_remote_shares
        }
        payload = share_type_methods[share_type]()
        if share_type == "local":
            if self.module.params.get('run') and self.module.params.get('export'):
                return payload
            else:
                self.module.exit_json(
                    msg=OPERATION_NOT_ALLOWED_MSG, skipped=True)
        if self.module.params.get('run'):
            return payload
        export_support_assist_status = self.__export_support_assist(payload)
        job_status = self.get_job_status(export_support_assist_status)
        status = export_support_assist_status.status_code
        if status in STATUS_SUCCESS:
            msg = SUCCESS_EXPORT_MSG
            job_details = job_status
            return msg, job_details

    def __export_support_assist_local(self):
        payload = {}
        payload["ShareType"] = "Local"
        return payload

    def __export_support_assist_remote_shares(self):
        payload = self.get_payload_details()
        return payload

    def __export_support_assist_nfs(self):
        payload = self.get_payload_details()
        del payload["UserName"], payload["Password"]
        return payload

    def __get_export_support_assist_url(self):
        uri, error_msg = validate_and_get_first_resource_id_uri(
            self.module, self.idrac, MANAGERS_URI)
        if error_msg:
            self.module.exit_json(msg=error_msg, failed=True)
        resp = get_dynamic_uri(self.idrac, uri)
        url = resp.get('Links', {}).get(OEM, {}).get(
            MANUFACTURER, {}).get(LC_SERVICE, {}).get(ODATA, {})
        if url:
            action_resp = get_dynamic_uri(self.idrac, url)
            export_url = action_resp.get(ACTIONS, {}).get(
                EXPORT, {}).get('target', {})
            self.export_url = export_url
        else:
            self.module.exit_json(msg=UNSUPPORTED_FIRMWARE_MSG, failed=True)

    def __export_support_assist(self, payload):
        if self.module.params.get('run') or self.module.params.get('share_parameters').get('share_type') == "local":
            return payload
        export_support_assist_status = self.idrac.invoke_request(
            self.export_url, "POST", data=payload)
        return export_support_assist_status

    def get_job_status(self, export_support_assist_status):
        res_uri = validate_and_get_first_resource_id_uri(
            self.module, self.idrac, MANAGERS_URI)
        job_tracking_uri = export_support_assist_status.headers.get("Location")
        job_id = job_tracking_uri.split("/")[-1]
        job_uri = f"{res_uri[0]}/{OEM}/{MANUFACTURER}/{JOBS}/{job_id}"
        job_failed, msg, job_dict, wait_time = idrac_redfish_job_tracking(
            self.idrac, job_uri)
        job_dict = remove_key(job_dict, regex_pattern=ODATA_REGEX)
        if job_failed:
            self.module.exit_json(msg=job_dict.get(
                'Message'), failed=True, job_details=job_dict)
        return job_dict


class SupportAssistType:
    _support_assist_classes = {
        "accept_eula": AcceptEULA,
        "run": RunSupportAssist,
        "export": ExportSupportAssist
    }

    @staticmethod
    def support_assist_operation(idrac, module):
        class_type = None
        if module.params.get("run"):
            class_type = "run"
        elif module.params.get("export"):
            class_type = "export"
        if class_type:
            support_assist_class = SupportAssistType._support_assist_classes.get(
                class_type)
            return support_assist_class(idrac, module)
        else:
            if not module.params.get("accept_eula"):
                module.exit_json(msg=NO_OPERATION_SKIP_MSG, skipped=True)


def main():
    specs = get_argument_spec()

    module = IdracAnsibleModule(
        argument_spec=specs,
        required_one_of=[["run", "export"]],
        required_if=[
            ["run", True, ("data_collector",)],
            ["export", True, ("share_parameters",)]
        ],
        supports_check_mode=True
    )

    msg = None
    try:
        with iDRACRedfishAPI(module.params) as idrac:
            if module.params.get("accept_eula"):
                accept_eula_obj = AcceptEULA(idrac, module)
                msg = accept_eula_obj.execute()
            support_assist_obj = SupportAssistType.support_assist_operation(
                idrac, module)
            if support_assist_obj is None:
                module.exit_json(msg=msg, changed=True)
            msg, job_status = support_assist_obj.execute()
            module.exit_json(msg=msg, changed=True, job_details=job_status)
    except HTTPError as err:
        filter_err = remove_key(json.load(err), regex_pattern=ODATA_REGEX)
        message_details = filter_err.get('error').get(MESSAGE_EXTENDED_INFO)[0]
        message_id = message_details.get('MessageId')
        if 'SRV095' in message_id:
            module.exit_json(msg=message_details.get('Message'), skipped=True)
        if 'SRV085' in message_id:
            module.exit_json(msg=message_details.get('Message'), skipped=True)
        if 'LIC501' in message_id:
            module.exit_json(msg=message_details.get('Message'), skipped=True)
        if 'SRV113' in message_id:
            module.exit_json(msg=message_details.get('Message'), skipped=True)
        module.exit_json(msg=str(err), error_info=filter_err, failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (OSError, ValueError, SSLValidationError, ConnectionError, TypeError) as e:
        module.exit_json(msg=str(e), failed=True)


def get_argument_spec():
    """
    Function to generate the argument specification for the IdracAnsibleModule.
    It returns a dictionary containing the argument specification for the module.

    The argument specification is a dictionary that contains the following keys:
    - run: a boolean that defaults to True
    - export: a boolean that defaults to True
    - accept_eula: a boolean
    - filter_data: a boolean that defaults to False
    - data_collector: a list of strings with choices including hardware_data, storage_logs, os_app_data, debug_logs, telemetry_reports, gpu_logs
    - job_wait: a boolean that defaults to True
    - job_wait_timeout: an integer that defaults to 3600
    - share_parameters: a dictionary with options including
        - share_type: a string with default 'local' and choices ['local', 'nfs', 'cifs', 'http', 'https', 'ftp']
        - proxy_type: a string with default 'http' and choices ['http', 'socks']
        - username:
            description: User name for accessing the share, required when share_type is 'cifs'
            type: str
            aliases: ['share_username']
        - password:
            description: Password for accessing the share, required when share_type is 'cifs', will not be logged
            type: str
            aliases: ['share_password']
        - proxy_support:
            description: Proxy support, a string with default 'off' and choices ['off', 'default_proxy', 'parameters_proxy']
        - proxy_port:
            description: Proxy port, an integer with default 80
        - proxy_server:
            description: Proxy server address, a string
        - proxy_username:
            description: User name for the proxy server, a string
        - proxy_password:
            description: Password for the proxy server, a string, will not be logged
        - workgroup:
            description: Workgroup for accessing the share, a string
        - ignore_certificate_warning:
            description: Ignores the certificate warning when connecting to the share, a string with default 'off' and choices ['off', 'on']
        - share_name:
            description: Share path or name, a string
        - ip_address:
            description: IP address of the share, a string
    - resource_id: a string

    """
    return {
        "run": {"type": 'bool', "default": True},
        "export": {"type": 'bool', "default": True},
        "accept_eula": {"type": 'bool'},
        "filter_data": {"type": 'bool', "default": False},
        "data_collector": {
            "type": 'list',
            "elements": 'str',
            "choices": ['hardware_data', 'storage_logs', 'os_app_data', 'debug_logs', 'telemetry_reports', 'gpu_logs']
        },
        "job_wait": {"type": 'bool', "default": True},
        "job_wait_timeout": {"type": 'int', "default": 3600},
        "share_parameters": {
            "type": 'dict',
            "options": {
                "share_type": {
                    "type": 'str',
                    "default": 'local',
                    "choices": ['local', 'nfs', 'cifs', 'http', 'https', 'ftp']
                },
                "proxy_type": {
                    "type": 'str',
                    "default": 'http',
                    "choices": ['http', 'socks']
                },
                "username": {
                    "type": 'str',
                    "aliases": ['share_username'],
                    'required_if': [('share_type', 'cifs', True)]
                },
                "password": {
                    "type": 'str',
                    "no_log": True,
                    "aliases": ['share_password'],
                    'required_if': [('share_type', 'cifs', True)]
                },
                "proxy_port": {"type": 'int', "default": 80},
                "proxy_server": {"type": 'str'},
                "proxy_username": {"type": 'str'},
                "proxy_password": {"type": 'str', "no_log": True},
                "workgroup": {"type": 'str'},
                "proxy_support": {
                    "type": 'str',
                    "default": "off",
                    "choices": ["off", "default_proxy", "parameters_proxy"]
                },
                "ignore_certificate_warning": {
                    "type": 'str',
                    "default": "off",
                    "choices": ["off", "on"]
                },
                "share_name": {"type": 'str'},
                "ip_address": {"type": 'str'},
            },
            "required_together": [
                ("username", "password"),
                ("proxy_username", "proxy_password")
            ],
            "required_if": [
                ["share_type", "local", ["share_name"]],
                ["share_type", "nfs", ["ip_address", "share_name"]],
                ["share_type", "cifs", ["ip_address",
                                        "share_name", "username", "password"]],
                ["share_type", "http", ["ip_address", "share_name"]],
                ["share_type", "https", ["ip_address", "share_name"]],
                ["proxy_support", "parameters_proxy", ["proxy_server"]]
            ],
        },
        "resource_id": {"type": 'str'}
    }


if __name__ == '__main__':
    main()
