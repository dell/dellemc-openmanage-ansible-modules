#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.2.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: idrac_reset
short_description: Factory reset the iDRACs
version_added: "9.2.0"
description:
  - This module is responsible to reset the iDRAC to factory default settings.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
  reset_to_default:
    type: str
    description:
        - If this value is not set the default behavior is to restart the IDRAC.
        - C(All) Discards all settings and reset to default credentials.
        - C(ResetAllWithRootDefaults) Discards all settings and reset the default username to root and password to the shipping value (root/shipping value.
        - C(Default) Discards all settings, but preserves user and network settings.
        - C(CustomDefaults) All configuration is set to custom defaults.This option is supported on firmware version 7.00.30.00 and above.
    choices: ['Default', 'All', 'ResetAllWithRootDefaults', 'CustomDefaults']
    default: 'Default'
  custom_defaults_file:
    description:
      - Name of the custom default configuration file in the XML format.
      - This option is applicable when I(reset_to_default) is C(CustomDefaults).
      - I(custom_defaults_file) is mutually exclusive with I(custom_defaults_buffer).
    type: str
  custom_defaults_buffer:
    description:
      - This parameter provides the opton to import the buffer input of xml as custom default configuration.
      - This option is applicable when I(reset_to_default) is C(CustomDefaults).
      - I(custom_defaults_buffer) is mutually exclusive with I(custom_defaults_file).
    type: str    
  wait_for_idrac:
    description:
      - This parameter provides the option to wait for the iDRAC to reset and LC status to be ready.
    type: bool
    default: true
  job_wait_timeout:
    description:
      - Time in seconds to wait for job completion.
      - This is applicable when I(job_wait) is C(true).
    type: int
    default: 300 
  force_reset:
    description:
      - This parameter provides the option to force reset the iDRAC without checking the iDRAC lifecycle controller status.
      - This option is applicable only for iDRAC9.
    type: bool
    default: false

requirements:
  - "python >= 3.9.6"
author:
  - "Lovepreet Singh (@singh-lovepreet1)"
notes:
    - This module supports both IPv4 and IPv6 address for I(idrac_ip).
    - This module supports C(check_mode).
    - This module will by default trigger a graceful restart if nothing is specified.
    - This module skips the execution if reset options is not supported by the iDRAC.
'''

EXAMPLES = r'''
---
- name: Reset the iDRAC to all and wait for the iDRAC to be up.
  dellemc.openmanage.idrac_reset:
   idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    reset_to_default: "All"
 
- name: Reset the iDRAC to default and do not wait for the iDRAC to be up.
  dellemc.openmanage.idrac_reset:
   idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    reset_to_default: "Default"
    wait_for_idrac: false
 
- name: Force reset the iDRAC to default.
  dellemc.openmanage.idrac_reset:
   idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    reset_to_default: "Default"
    force_reset: true
 
- name: Gracefully restart the iDRAC.
  dellemc.openmanage.idrac_reset:
   idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
 
- name: Reset the iDRAC to custom defaults xml and do not wait for the iDRAC to be up.
  dellemc.openmanage.idrac_reset:
   idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    reset_to_default: "CustomDefaults"
    custom_defaults_file: "/path/to/custom_defaults.xml"
 
- name: Reset the iDRAC to custom defaults buffer input and do not wait for the iDRAC to be up.
  dellemc.openmanage.idrac_reset:
   idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    reset_to_default: "CustomDefaults"
    custom_defaults_buffer: "<SystemConfiguration><Component FQDD='iDRAC.Embedded.1'><Attribute Name='IPMILan.1'>
      Disabled</Attribute></Component></SystemConfiguration>"
'''

RETURN = r'''
---
msg:
  type: str
  description: Overall status of the storage configuration operation.
  returned: always
  sample: "Successfully completed the "
reset_status:
  type: dict
  description: Reset status and progress details from the iDRAC.
  returned: success
  sample:
    {
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

import re
import json
import time
import socket
import subprocess
from urllib.error import HTTPError, URLError
from copy import deepcopy
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, idrac_auth_params
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.compat.version import LooseVersion
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    get_idrac_firmware_version, wait_after_idrac_reset)


SYSTEMS_URI = "/redfish/v1/Systems"
MANAGERS_URI = "/redfish/v1/Managers"
IDRAC_RESET_RETRIES = 10
LC_STATUS_CHECK_SLEEP = 30
IDRAC_RESET_OPTIONS_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"
iDRAC_JOB_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/{job_id}"
IDRAC_RESET_LIFECYCLE_STATUS_URI =  "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellLCService/Actions/DellLCService.GetRemoteServicesAPIStatus"
IDRAC_RESET_SET_CUSTOM_DEFAULTS_URI = "/redfish/v1/Managers/{ManagerId}/Actions/Oem/DellManager.SetCustomDefaults"
IDRAC_RESET__GET_CUSTOM_DEFAULTS_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/CustomDefaultsDownloadURI" 
IDRAC_RESET_GRACEFUL_RESTART_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Manager.Reset"
IDRAC_RESET_RESET_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/DellManager.ResetToDefaults"
RESET_TO_DEFAULT_ERROR = "{0} is not supported. The supported values are {1}. Enter the valid values and retry the operation."

IDRAC_RESET_RESTART_SUCCESS_MSG = "iDRAC restart operation completed successfully"
IDRAC_RESET_SUCCESS_MSG = "iDRAC reset operation completed successfully"
IDRAC_RESET_RESET_TRIGGER_MSG = "iDRAC reset operation triggered successfully"
IDRAC_RESET_RESTART_TRIGGER_MSG = "iDRAC restart operation triggered successfully"
INVALID_VALUE_MSG = "The value for the `{parameter}` parameter is invalid."
NOT_ALLOWED_VALUE_MSG = "`{reset_to_default}` is not supported. The supported values are `{supported_reset_to_default_values}`. Enter the valid values and retry the operation.}"
WAIT_TIMEOUT_MSG = "The job is not complete after {0} seconds."
INVALID_DIRECTORY_MSG = "Provided directory path '{path}' is not valid."
FAILED_RESET_MSG = "Failed to perform the reset operation."
MISSING_FILE_NAME_PARAMETER_MSG = "Missing required parameter 'file_name'."
UNSUPPORTED_FIRMWARE_MSG = "iDRAC firmware version is not supported."
RESET_UNTRACK = "iDRAC reset is in progress. Until the iDRAC is reset, the changes would not apply."
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The parameter `job_wait_timeout` value cannot be negative or zero."
NO_OPERATION_SKIP_MSG = "Task is skipped as none of import, export or delete is specified."
INVALID_FILE_MSG = "File extension is invalid. Supported extensions for local 'share_type' " \
                   "are: .txt and .xml, and for network 'share_type' is: .xml."
LC_STATUS_MSG = "LC status check is {{ lc_status }} after {{ retries }} number of retries, Exiting.."                   
CHANGES_NOT_FOUND = "No changes found to commit!"
CHANGES_FOUND = "Changes found to commit!"
ODATA_ID = "@odata.id"
ODATA_REGEX = "(.*?)@odata"
ATTRIBUTE = "</Attribute>"
SUCCESS_STATUS = "Success"
FAILED_STATUS = "Failed"
STATUS_SUCCESS = [200, 204]
RESET_KEY = "Oem.#DellManager.ResetToDefaults"



class FACTORYRESET(): 
    def __init__(self, idrac, module, allowed_choices):
        self.idrac = idrac
        self.module = module
        self.allowed_choices = allowed_choices
    
    def execute(self):
        msg_res, job_res = None, None
        self.__validate_job_timeout()
        if self.module.check_mode:
          self.module.exit_json(msg = CHANGES_FOUND, changed= True)
        self.reset_to_default = self.module.params.get('reset_to_default')
        self.force_reset = self.module.params.get('force_reset')
        self.wait_for_idrac = self.module.params.get('wait_for_idrac')
        self.idrac_firmware_version = get_idrac_firmware_version(self.idrac)
        if LooseVersion(self.idrac_firmware_version) >= '3.0' and not self.force_reset:
          self.__check_lcstatus(post_op=False)
        if self.reset_to_default is None:
          msg_res, job_res = self.__graceful_restart()
        elif self.reset_to_default == 'All':
          msg_res, job_res = self.__reset_to_default_all()  
        elif self.reset_to_default == 'Default':
          msg_res, job_res = self.__reset_to_defaults()
        elif self.reset_to_default == 'ResetAllWithRootDefaults':
          msg_res, job_res = self.__reset_all_with_root_defaults()       
        if LooseVersion(self.idrac_firmware_version) >= '3.0' and self.wait_for_idrac:
          self.__check_lcstatus()    
        return msg_res,job_res
      
    def __validate_job_timeout(self):
        if self.module.params.get("job_wait") and self.module.params.get("job_wait_timeout") <= 0:
            self.module.exit_json(msg=TIMEOUT_NEGATIVE_OR_ZERO_MSG, failed=True)

    def __validate_reset_options(self, api_key):
        res = self.idrac.invoke_request(IDRAC_RESET_OPTIONS_URI, "GET")
        key_list = api_key.split(".",1)
        if key_list[0] in res.json_data["Actions"] and key_list[1] in res.json_data["Actions"][key_list[0]]:
          reset_to_defaults = res.json_data["Actions"][key_list[0]][key_list[1]]
          reset_type_values = reset_to_defaults["ResetType@Redfish.AllowableValues"]
          if self.reset_to_default in reset_type_values:
            return True
        return False

    def __check_lcstatus(self, post_op=True):
        if self.reset_to_default == 'All' and post_op and self.staus_code_after_wait == 401:
          return
        lc_status_dict = {}
        lc_status_dict['LCStatus'] = ""
        retry_count = 1
        while retry_count < IDRAC_RESET_RETRIES:
          try:
            lcstatus = self.idrac.invoke_request(IDRAC_RESET_LIFECYCLE_STATUS_URI,"POST",data="{}", dump=False)
            lcstatus_data = lcstatus.json_data.get('LCStatus')
            lc_status_dict['LCStatus'] = lcstatus_data
            if lc_status_dict.get('LCStatus') == 'Ready':
              break
            time.sleep(10)
            retry_count = retry_count + 1
          except URLError as err:
            time.sleep(10)
            retry_count = retry_count + 1
            if retry_count == IDRAC_RESET_RETRIES:
              self.module.exit_json(msg=LC_STATUS_MSG.format(lc_status= 'unreachable', retries=retry_count), unreachable=True)

        if retry_count == IDRAC_RESET_RETRIES and lc_status_dict.get('LCStatus') != "Ready":
            self.module.exit_json(msg=LC_STATUS_MSG.format(lc_status=lc_status_dict.get('LCStatus'), retries=retry_count),failed=True)
    
    def __create_output(self,status):
      result = {}
      tmp_res = {}
      result['idracreset'] = {}
      result['idracreset']['Data'] = {'StatusCode': status}
      result['idracreset']['StatusCode'] = status
      track_failed, wait_msg = None, None
      self.staus_code_after_wait = 202
      if status in STATUS_SUCCESS:
        if self.wait_for_idrac:
          track_failed, status_code, wait_msg = self.__wait_for_port_open()
          self.staus_code_after_wait = status_code
          if track_failed:
            self.module.exit_json(msg=wait_msg, changed=True)
        tmp_res['msg'] = IDRAC_RESET_SUCCESS_MSG
        tmp_res['changed'] = True
        result['idracreset']['Message'] = IDRAC_RESET_SUCCESS_MSG if self.wait_for_idrac else IDRAC_RESET_RESET_TRIGGER_MSG
        result['idracreset']['Status'] = 'Success'
        result['idracreset']['retVal'] = True
      else:
        tmp_res['msg']  = FAILED_RESET_MSG
        tmp_res['changed'] = False
        result['idracreset']['Message'] = FAILED_RESET_MSG
        result['idracreset']['Status'] = 'FAILED'
        result['idracreset']['retVal'] = False
      return tmp_res, result

    def __perform_operation(self, payload):
      tmp_res, res = None, None
      run_reset_status = self.idrac.invoke_request(IDRAC_RESET_RESET_URI, "POST", data=payload)
      status = run_reset_status.status_code
      tmp_res, res = self.__create_output(status)
      return tmp_res, res 
    
    def __wait_for_port_open(self,interval=30):
      timeout_wait = self.module.params.get('job_wait_timeout')
      time.sleep(interval // 2)
      msg = RESET_UNTRACK
      wait = timeout_wait
      track_failed = True
      status_code = 503
      while wait > 0:
          try:
              self.idrac.invoke_request(MANAGERS_URI, 'GET')
              time.sleep(interval // 2)
              msg = IDRAC_RESET_SUCCESS_MSG
              track_failed = False
              status_code= 200
              break
          except HTTPError as err:
            status_code = err.code
            if status_code == 401:
              time.sleep(interval // 2)
              msg = IDRAC_RESET_SUCCESS_MSG
              track_failed = False
              break
          except URLError as err:
              time.sleep(interval)
              wait = wait - interval
      return track_failed, status_code, msg
             
    def __reset_to_default_all(self):
        payload = {}
        payload["ResetType"] = "All"
        valid_reset_option = self.__validate_reset_options(RESET_KEY)
        if not valid_reset_option:
          self.module.exit_json(msg=NOT_ALLOWED_VALUE_MSG.format(reset_to_default=self.reset_to_default, supported_reset_to_default_values=self.allowed_choices),skipped=True)
        return self.__perform_operation(payload)

    def __reset_to_defaults(self):
        payload = {}
        payload["ResetType"] = "Default"
        valid_reset_option = self.__validate_reset_options(RESET_KEY)
        if not valid_reset_option:
          self.module.exit_json(msg=NOT_ALLOWED_VALUE_MSG.format(reset_to_default=self.reset_to_default, supported_reset_to_default_values=self.allowed_choices),skipped=True)
        return self.__perform_operation(payload)
    
    def __reset_all_with_root_defaults(self):
        payload = {}
        payload["ResetType"] = "ResetAllWithRootDefaults"
        valid_reset_option = self.__validate_reset_options(RESET_KEY)
        if not valid_reset_option:
          self.module.exit_json(msg=NOT_ALLOWED_VALUE_MSG.format(reset_to_default=self.reset_to_default, supported_reset_to_default_values=self.allowed_choices),skipped=True)
        return self.__perform_operation(payload)  
     
    def __graceful_restart(self):
        payload = {}
        payload["ResetType"] = "GracefulRestart"
        run_reset_status = self.idrac.invoke_request(IDRAC_RESET_GRACEFUL_RESTART_URI, "POST", data=payload)
        status = run_reset_status.status_code
        tmp_res, resp = self.__create_output(status)
        if status in STATUS_SUCCESS:
          resp['idracreset']['Message'] = IDRAC_RESET_RESTART_SUCCESS_MSG if self.wait_for_idrac else IDRAC_RESET_RESTART_TRIGGER_MSG
        return tmp_res, resp 

def main():
    specs = {
        "reset_to_default": {"choices": ['All', 'ResetAllWithRootDefaults', 'Default','CustomDefaults']},
        "custom_defaults_file": {"type": "str"},
        "custom_defaults_buffer": {"type": "str"},
        "wait_for_idrac": {"type": "bool", "default": True},
        "job_wait_timeout": {"type": 'int', "default": 300},
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
            reset_obj = FACTORYRESET(idrac, module, allowed_choices)
            message_resp, output = reset_obj.execute()
            if not message_resp.get('changed'):
              module.exit_json(msg=message_resp.get('msg'), reset_status=output, failed=True)
            module.exit_json(msg=message_resp.get('msg'), reset_status=output, changed=True)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)

if __name__ == '__main__':
    main()
