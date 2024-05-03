#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.2.0
# Copyright (C) 2018-2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: idrac_reset
short_description: Factory reset the iDRACs
version_added: "2.1.0"
description:
  - This module resets the iDRAC to factory default settings.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
  reset_to_default:
    type: str
    description:
        - If this value is not set the default behaviour is to restart the iDRAC.
        - C(All) Discards all settings and reset to default credentials.
        - C(ResetAllWithRootDefaults) Discards all settings and reset the default username to root and password to the shipping value.
        - C(Default) Discards all settings, but preserves user and network settings.
        - C(CustomDefaults) All configuration is set to custom defaults.This option is supported on firmware version 7.00.00.00 and newer versions.
    choices: ['Default', 'All', 'ResetAllWithRootDefaults', 'CustomDefaults']
    version_added: 9.2.0
  custom_defaults_file:
    description:
      - Name of the custom default configuration file in the XML format.
      - This option is applicable when I(reset_to_default) is C(CustomDefaults).
      - I(custom_defaults_file) is mutually exclusive with I(custom_defaults_buffer).
    type: str
    version_added: 9.2.0
  custom_defaults_buffer:
    description:
      - This parameter provides the option to import the buffer input in XML format as a custom default configuration.
      - This option is applicable when I(reset_to_default) is C(CustomDefaults).
      - I(custom_defaults_buffer) is mutually exclusive with I(custom_defaults_file).
    type: str
    version_added: 9.2.0
  wait_for_idrac:
    description:
      - This parameter provides the option to wait for the iDRAC to reset and lifecycle controller status to be ready.
    type: bool
    default: true
    version_added: 9.2.0
  job_wait_timeout:
    description:
      - Time in seconds to wait for job completion.
      - This is applicable when I(job_wait) is C(true).
    type: int
    default: 600
    version_added: 9.2.0
  force_reset:
    description:
      - This parameter provides the option to force reset the iDRAC without checking the iDRAC lifecycle controller status.
      - This option is applicable only for iDRAC9.
    type: bool
    default: false
    version_added: 9.2.0

requirements:
  - "python >= 3.9.6"
author:
  - "Felix Stephen (@felixs88)"
  - "Anooja Vardhineni (@anooja-vardhineni)"
  - "Lovepreet Singh (@singh-lovepreet1)"
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports both IPv4 and IPv6 address for I(idrac_ip).
    - This module supports C(check_mode).
    - If reset_to_default option is not specified, then this module triggers a graceful restart.
    - This module skips the execution if reset options are not supported by the iDRAC.
'''

EXAMPLES = r'''
---
- name: Reset the iDRAC to all and wait till the iDRAC is accessible.
  dellemc.openmanage.idrac_reset:
   idrac_ip: "192.168.0.1"
   idrac_user: "user_name"
   idrac_password: "user_password"
   ca_path: "/path/to/ca_cert.pem"
   reset_to_default: "All"

- name: Reset the iDRAC to default and do not wait till the iDRAC is accessible.
  dellemc.openmanage.idrac_reset:
   idrac_ip: "192.168.0.1"
   idrac_user: "user_name"
   idrac_password: "user_password"
   ca_path: "/path/to/ca_cert.pem"
   reset_to_default: "Default"
   wait_for_idrac: false

- name: Force reset the iDRAC to default.
  dellemc.openmanage.idrac_reset:
   idrac_ip: "192.168.0.1"
   idrac_user: "user_name"
   idrac_password: "user_password"
   ca_path: "/path/to/ca_cert.pem"
   reset_to_default: "Default"
   force_reset: true

- name: Gracefully restart the iDRAC.
  dellemc.openmanage.idrac_reset:
   idrac_ip: "192.168.0.1"
   idrac_user: "user_name"
   idrac_password: "user_password"
   ca_path: "/path/to/ca_cert.pem"

- name: Reset the iDRAC to custom defaults XML and do not wait till the iDRAC is accessible.
  dellemc.openmanage.idrac_reset:
   idrac_ip: "192.168.0.1"
   idrac_user: "user_name"
   idrac_password: "user_password"
   ca_path: "/path/to/ca_cert.pem"
   reset_to_default: "CustomDefaults"
   custom_defaults_file: "/path/to/custom_defaults.xml"

- name: Reset the iDRAC to custom defaults buffer input and do not wait till the iDRAC is accessible.
  dellemc.openmanage.idrac_reset:
   idrac_ip: "192.168.0.1"
   idrac_user: "user_name"
   idrac_password: "user_password"
   ca_path: "/path/to/ca_cert.pem"
   reset_to_default: "CustomDefaults"
   custom_defaults_buffer: "<SystemConfiguration Model=\"PowerEdge R7525\" ServiceTag=\"ABCD123\">\n<Component FQDD=\"iDRAC.Embedded.1\">\n
                               <Attribute Name=\"IPMILan.1#Enable\">Disabled</Attribute>\n </Component>\n\n</SystemConfiguration>"
'''

RETURN = r'''
---
msg:
  type: str
  description: Status of the iDRAC reset operation.
  returned: always
  sample: "Successfully performed iDRAC reset."
reset_status:
  type: dict
  description: Details of iDRAC reset operation.
  returned: reset operation is triggered.
  sample: {
    "idracreset": {
            "Data": {
                "StatusCode": 204
            },
            "Message": "none",
            "Status": "Success",
            "StatusCode": 204,
            "retval": true
        }
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
import time
from urllib.error import HTTPError, URLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, idrac_auth_params
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.compat.version import LooseVersion
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    get_idrac_firmware_version, remove_key, get_dynamic_uri, validate_and_get_first_resource_id_uri, idrac_redfish_job_tracking)


MANAGERS_URI = "/redfish/v1/Managers"
OEM = "Oem"
MANUFACTURER = "Dell"
ACTIONS = "Actions"
IDRAC_RESET_RETRIES = 50
LC_STATUS_CHECK_SLEEP = 30
IDRAC_JOB_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/{job_id}"
RESET_TO_DEFAULT_ERROR = "{reset_to_default} is not supported. The supported values are {supported_values}. Enter the valid values and retry the operation."
RESET_TO_DEFAULT_ERROR_MSG = "{reset_to_default} is not supported."
CUSTOM_ERROR = "{reset_to_default} is not supported on this firmware version of iDRAC. The supported values are {supported_values}. \
Enter the valid values and retry the operation."
IDRAC_RESET_RESTART_SUCCESS_MSG = "iDRAC restart operation completed successfully."
IDRAC_RESET_SUCCESS_MSG = "Successfully performed iDRAC reset."
IDRAC_RESET_RESET_TRIGGER_MSG = "iDRAC reset operation triggered successfully."
IDRAC_RESET_RESTART_TRIGGER_MSG = "iDRAC restart operation triggered successfully."
INVALID_DIRECTORY_MSG = "Provided directory path '{path}' is invalid."
FAILED_RESET_MSG = "Failed to perform the reset operation."
RESET_UNTRACK = "iDRAC reset is in progress. Changes will apply once the iDRAC reset operation is successfully completed."
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The value of `job_wait_timeout` parameter cannot be negative or zero. Enter the valid value and retry the operation."
INVALID_FILE_MSG = "File extension is invalid. Supported extension for 'custom_default_file' is: .xml."
LC_STATUS_MSG = "Lifecycle controller status check is {lc_status} after {retries} number of retries, Exiting.."
INSUFFICIENT_DIRECTORY_PERMISSION_MSG = "Provided directory path '{path}' is not writable. Please check if the directory has appropriate permissions."
UNSUPPORTED_LC_STATUS_MSG = "Lifecycle controller status check is not supported."
MINIMUM_SUPPORTED_FIRMWARE_VERSION = "7.00.00"
CHANGES_NOT_FOUND = "No changes found to commit!"
CHANGES_FOUND = "Changes found to commit!"
ODATA_ID = "@odata.id"
ODATA_REGEX = "(.*?)@odata"
ATTRIBUTE = "</Attribute>"
SUCCESS_STATUS = "Success"
FAILED_STATUS = "Failed"
STATUS_SUCCESS = [200, 202, 204]
ERR_STATUS_CODE = [400, 404]
PASSWORD_CHANGE_OPTIONS = ['All', 'ResetAllWithRootDefaults']
RESET_KEY = "Oem.#DellManager.ResetToDefaults"
GRACEFUL_RESTART_KEY = "#Manager.Reset"


class Validation():
    def __init__(self, idrac, module):
        self.idrac = idrac
        self.module = module
        self.base_uri = self.get_base_uri()

    def get_base_uri(self):
        uri, error_msg = validate_and_get_first_resource_id_uri(
            self.module, self.idrac, MANAGERS_URI)
        if error_msg:
            self.module.exit_json(msg=error_msg, failed=True)
        return uri

    def validate_reset_options(self, api_key):
        res = self.idrac.invoke_request(self.base_uri, "GET")
        reset_to_default = self.module.params.get('reset_to_default')
        key_list = api_key.split(".", 1)
        is_valid = True
        allowed_values = None
        if key_list[0] in res.json_data["Actions"] and key_list[1] in res.json_data["Actions"][key_list[0]]:
            reset_to_defaults_val = res.json_data["Actions"][key_list[0]][key_list[1]]
            reset_type_values = reset_to_defaults_val["ResetType@Redfish.AllowableValues"]
            allowed_values = reset_type_values
            if reset_to_default not in reset_type_values:
                is_valid = False
        else:
            is_valid = False
        return allowed_values, is_valid

    def validate_graceful_restart_option(self, api_key):
        res = self.idrac.invoke_request(self.base_uri, "GET")
        is_valid = True
        if api_key in res.json_data["Actions"]:
            reset_to_defaults_val = res.json_data["Actions"][api_key]
            reset_type_values = reset_to_defaults_val["ResetType@Redfish.AllowableValues"]
            if "GracefulRestart" not in reset_type_values:
                is_valid = False
        else:
            is_valid = False
        return is_valid

    def validate_job_timeout(self):
        if self.module.params.get("wait_for_idrac") and self.module.params.get("job_wait_timeout") <= 0:
            self.module.exit_json(msg=TIMEOUT_NEGATIVE_OR_ZERO_MSG, failed=True)

    def validate_path(self, file_path):
        if not (os.path.exists(file_path)):
            self.module.exit_json(msg=INVALID_DIRECTORY_MSG.format(path=file_path), failed=True)
        if not os.access(file_path, os.W_OK):
            self.module.exit_json(msg=INSUFFICIENT_DIRECTORY_PERMISSION_MSG.format(path=file_path), failed=True)

    def validate_file_format(self, file_name):
        if not (file_name.endswith(".xml")):
            self.module.exit_json(msg=INVALID_FILE_MSG, failed=True)

    def validate_custom_option(self, reset_to_default=None, allowed_choices=None):
        url = None
        resp = get_dynamic_uri(self.idrac, self.base_uri, OEM)
        if resp:
            url = resp.get(MANUFACTURER, {}).get('CustomDefaultsDownloadURI', {})
        try:
            if url:
                self.idrac.invoke_request(url, "GET")
                return True
            return False
        except HTTPError as err:
            if err.code in ERR_STATUS_CODE:
                self.module.exit_json(msg=RESET_TO_DEFAULT_ERROR.format(reset_to_default=reset_to_default, supported_values=allowed_choices), skipped=True)


class FactoryReset():
    def __init__(self, idrac, module, allowed_choices):
        self.idrac = idrac
        self.module = module
        self.allowed_choices = allowed_choices
        self.reset_to_default = self.module.params.get('reset_to_default')
        self.force_reset = self.module.params.get('force_reset')
        self.wait_for_idrac = self.module.params.get('wait_for_idrac')
        self.validate_obj = Validation(self.idrac, self.module)
        self.uri = self.validate_obj.base_uri
        self.idrac_firmware_version = get_idrac_firmware_version(self.idrac)

    def execute(self):
        msg_res, job_res = None, None
        self.validate_obj.validate_job_timeout()
        is_idrac9 = self.is_check_idrac_latest()
        if not is_idrac9 and self.reset_to_default:
            allowed_values, is_valid_option = self.validate_obj.validate_reset_options(RESET_KEY)
            if self.module.check_mode and not is_valid_option:
                self.module.exit_json(msg=CHANGES_NOT_FOUND)
            if not is_valid_option:
                self.module.exit_json(msg=RESET_TO_DEFAULT_ERROR_MSG.format(reset_to_default=self.reset_to_default),
                                      skipped=True)
        if self.module.check_mode:
            self.check_mode_output(is_idrac9)
        if is_idrac9 and not self.force_reset:
            self.check_lcstatus(post_op=False)
        reset_status_mapping = {key: self.reset_to_default_mapped for key in ['Default', 'All', 'ResetAllWithRootDefaults']}
        reset_status_mapping.update({
            'CustomDefaults': self.reset_custom_defaults,
            'None': self.graceful_restart
        })
        msg_res, job_res = reset_status_mapping[str(self.reset_to_default)]()
        if is_idrac9 and self.wait_for_idrac:
            self.check_lcstatus()
        return msg_res, job_res

    def check_mode_output(self, is_idrac9):
        if is_idrac9 and self.reset_to_default == 'CustomDefaults' and LooseVersion(self.idrac_firmware_version) < MINIMUM_SUPPORTED_FIRMWARE_VERSION:
            self.module.exit_json(msg=CHANGES_NOT_FOUND)
        if self.reset_to_default:
            allowed_values, is_valid_option = self.validate_obj.validate_reset_options(RESET_KEY)
        else:
            is_valid_option = self.validate_obj.validate_graceful_restart_option(GRACEFUL_RESTART_KEY)
        custom_default_file = self.module.params.get('custom_defaults_file')
        custom_default_buffer = self.module.params.get('custom_defaults_buffer')
        if is_valid_option:
            self.module.exit_json(msg=CHANGES_FOUND, changed=True)
        elif self.reset_to_default and self.reset_to_default == 'CustomDefaults' and (custom_default_file or custom_default_buffer):
            self.module.exit_json(msg=CHANGES_FOUND, changed=True)
        else:
            self.module.exit_json(msg=CHANGES_NOT_FOUND)

    def is_check_idrac_latest(self):
        if LooseVersion(self.idrac_firmware_version) >= '3.0':
            return True

    def check_lcstatus(self, post_op=True):
        if self.reset_to_default in PASSWORD_CHANGE_OPTIONS and post_op and self.staus_code_after_wait == 401:
            return
        lc_status_dict = {}
        lc_status_dict['LCStatus'] = ""
        retry_count = 1
        resp = get_dynamic_uri(self.idrac, self.uri, "Links")
        url = resp.get(OEM, {}).get(MANUFACTURER, {}).get('DellLCService', {}).get(ODATA_ID, {})
        if url:
            action_resp = get_dynamic_uri(self.idrac, url)
            lc_url = action_resp.get(ACTIONS, {}).get('#DellLCService.GetRemoteServicesAPIStatus', {}).get('target', {})
        else:
            self.module.exit_json(msg=UNSUPPORTED_LC_STATUS_MSG, failed=True)
        while retry_count < IDRAC_RESET_RETRIES:
            try:
                lcstatus = self.idrac.invoke_request(lc_url, "POST", data="{}", dump=False)
                lcstatus_data = lcstatus.json_data.get('LCStatus')
                lc_status_dict['LCStatus'] = lcstatus_data
                if lc_status_dict.get('LCStatus') == 'Ready':
                    break
                time.sleep(10)
                retry_count = retry_count + 1
            except URLError:
                time.sleep(10)
                retry_count = retry_count + 1
                if retry_count == IDRAC_RESET_RETRIES:
                    self.module.exit_json(msg=LC_STATUS_MSG.format(lc_status='unreachable', retries=IDRAC_RESET_RETRIES), unreachable=True)

        if retry_count == IDRAC_RESET_RETRIES and lc_status_dict.get('LCStatus') != "Ready":
            self.module.exit_json(msg=LC_STATUS_MSG.format(lc_status=lc_status_dict.get('LCStatus'), retries=retry_count), failed=True)

    def create_output(self, status):
        result = {}
        tmp_res = {}
        result['idracreset'] = {}
        result['idracreset']['Data'] = {'StatusCode': status}
        result['idracreset']['StatusCode'] = status
        track_failed, wait_msg = None, None
        self.staus_code_after_wait = 202
        if status in STATUS_SUCCESS:
            if self.wait_for_idrac:
                track_failed, status_code, wait_msg = self.wait_for_port_open()
                self.staus_code_after_wait = status_code
                if track_failed:
                    self.module.exit_json(msg=wait_msg, changed=True)
            tmp_res['msg'] = IDRAC_RESET_SUCCESS_MSG if self.wait_for_idrac else IDRAC_RESET_RESET_TRIGGER_MSG
            tmp_res['changed'] = True
            result['idracreset']['Message'] = IDRAC_RESET_SUCCESS_MSG if self.wait_for_idrac else IDRAC_RESET_RESET_TRIGGER_MSG
            result['idracreset']['Status'] = 'Success'
            result['idracreset']['retVal'] = True
        else:
            tmp_res['msg'] = FAILED_RESET_MSG
            tmp_res['changed'] = False
            result['idracreset']['Message'] = FAILED_RESET_MSG
            result['idracreset']['Status'] = 'FAILED'
            result['idracreset']['retVal'] = False
        if self.reset_to_default:
            result = None
        return tmp_res, result

    def perform_operation(self, payload):
        tmp_res, res = None, None
        url = None
        resp = get_dynamic_uri(self.idrac, self.uri, ACTIONS)
        if resp:
            url = resp.get(OEM, {}).get('#DellManager.ResetToDefaults', {}).get('target', {})
        run_reset_status = self.idrac.invoke_request(url, "POST", data=payload)
        status = run_reset_status.status_code
        tmp_res, res = self.create_output(status)
        return tmp_res, res

    def upload_cd_content(self, data):
        payload = {"CustomDefaults": data}
        job_wait_timeout = self.module.params.get('job_wait_timeout')
        url = None
        resp = get_dynamic_uri(self.idrac, self.uri, ACTIONS)
        if resp:
            url = resp.get(OEM, {}).get('#DellManager.SetCustomDefaults', {}).get('target', {})
        job_resp = self.idrac.invoke_request(url, "POST", data=payload)
        if (job_tracking_uri := job_resp.headers.get("Location")):
            job_id = job_tracking_uri.split("/")[-1]
            job_uri = IDRAC_JOB_URI.format(job_id=job_id)
            job_failed, msg, job_dict, wait_time = idrac_redfish_job_tracking(self.idrac, job_uri,
                                                                              max_job_wait_sec=job_wait_timeout,
                                                                              sleep_interval_secs=1)
            job_dict = remove_key(job_dict, regex_pattern='(.*?)@odata')
            if job_failed:
                self.module.exit_json(msg=job_dict.get("Message"), job_status=job_dict, failed=True)

    def wait_for_port_open(self, interval=45):
        timeout_wait = self.module.params.get('job_wait_timeout')
        time.sleep(interval)
        msg = RESET_UNTRACK
        wait = timeout_wait
        track_failed = True
        status_code = 503
        while int(wait) > 0:
            try:
                self.idrac.invoke_request(MANAGERS_URI, 'GET')
                time.sleep(interval)
                msg = IDRAC_RESET_SUCCESS_MSG
                track_failed = False
                status_code = 200
                break
            except HTTPError as err:
                status_code = err.code
                if status_code == 401:
                    time.sleep(interval // 2)
                    msg = IDRAC_RESET_SUCCESS_MSG
                    track_failed = False
                    break
            except Exception:
                time.sleep(interval)
                wait = wait - interval
        return track_failed, status_code, msg

    def reset_to_default_mapped(self):
        payload = {"ResetType": self.reset_to_default}
        self.allowed_choices, is_valid_option = self.validate_obj.validate_reset_options(RESET_KEY)
        if not is_valid_option:
            self.module.exit_json(msg=RESET_TO_DEFAULT_ERROR.format(reset_to_default=self.reset_to_default, supported_values=self.allowed_choices),
                                  skipped=True)
        return self.perform_operation(payload)

    def get_xml_content(self, file_path):
        with open(file_path, 'r') as file:
            xml_content = file.read()
        return xml_content

    def reset_custom_defaults(self):
        self.allowed_choices, is_valid_option = self.validate_obj.validate_reset_options(RESET_KEY)
        if LooseVersion(self.idrac_firmware_version) < MINIMUM_SUPPORTED_FIRMWARE_VERSION:
            self.module.exit_json(msg=CUSTOM_ERROR.format(reset_to_default=self.reset_to_default,
                                                          supported_values=self.allowed_choices), skipped=True)
        custom_default_file = self.module.params.get('custom_defaults_file')
        custom_default_buffer = self.module.params.get('custom_defaults_buffer')
        upload_perfom = False
        default_data = None
        if custom_default_file:
            self.validate_obj.validate_path(custom_default_file)
            self.validate_obj.validate_file_format(custom_default_file)
            upload_perfom = True
            default_data = self.get_xml_content(custom_default_file)
        elif custom_default_buffer:
            upload_perfom = True
            default_data = custom_default_buffer
        if upload_perfom:
            self.upload_cd_content(default_data)
        self.validate_obj.validate_custom_option(self.reset_to_default, self.allowed_choices)
        return self.reset_to_default_mapped()

    def graceful_restart(self):
        url = None
        resp = get_dynamic_uri(self.idrac, self.uri, ACTIONS)
        if resp:
            url = resp.get('#Manager.Reset', {}).get('target', {})
        payload = {"ResetType": "GracefulRestart"}
        run_reset_status = self.idrac.invoke_request(url, "POST", data=payload)
        status = run_reset_status.status_code
        tmp_res, resp = self.create_output(status)
        if status in STATUS_SUCCESS:
            tmp_res['msg'] = IDRAC_RESET_SUCCESS_MSG
            resp['idracreset']['Message'] = IDRAC_RESET_RESTART_SUCCESS_MSG if self.wait_for_idrac else IDRAC_RESET_RESTART_TRIGGER_MSG
        return tmp_res, resp


def main():
    specs = {
        "reset_to_default": {"choices": ['All', 'ResetAllWithRootDefaults', 'Default', 'CustomDefaults']},
        "custom_defaults_file": {"type": "str"},
        "custom_defaults_buffer": {"type": "str"},
        "wait_for_idrac": {"type": "bool", "default": True},
        "job_wait_timeout": {"type": 'int', "default": 600},
        "force_reset": {"type": "bool", "default": False}
    }
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[("custom_defaults_file", "custom_defaults_buffer")],
        supports_check_mode=True)
    try:
        with iDRACRedfishAPI(module.params) as idrac:
            allowed_choices = specs['reset_to_default']['choices']
            reset_obj = FactoryReset(idrac, module, allowed_choices)
            message_resp, output = reset_obj.execute()
            if output:
                if not message_resp.get('changed'):
                    module.exit_json(msg=message_resp.get('msg'), reset_status=output, failed=True)
                module.exit_json(msg=message_resp.get('msg'), reset_status=output, changed=True)
            else:
                if not message_resp.get('changed'):
                    module.exit_json(msg=message_resp.get('msg'), failed=True)
                module.exit_json(msg=message_resp.get('msg'), changed=True)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, SSLValidationError, ConnectionError, TypeError, KeyError, ValueError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
