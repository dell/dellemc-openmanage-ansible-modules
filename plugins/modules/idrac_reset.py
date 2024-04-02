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
import operator
import json
from urllib.error import HTTPError, URLError
from copy import deepcopy
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, idrac_auth_params
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.compat.version import LooseVersion
# from ansible_collections.ansible.builtin.plugins.module_utils.basic import pause
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    get_dynamic_uri, validate_and_get_first_resource_id_uri, xml_data_conversion, idrac_redfish_job_tracking, remove_key, get_idrac_firmware_version, wait_after_idrac_reset)


SYSTEMS_URI = "/redfish/v1/Systems"
IDRAC_RESET_RETRIES = 10
LC_STATUS_CHECK_SLEEP = 30
IDRAC_RESET_WAIT_TIME = 300
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
WAIT_TIMEOUT_MSG = "The job is not complete after {0} seconds."
INVALID_DIRECTORY_MSG = "Provided directory path '{path}' is not valid."
FAILED_RESET_MSG = "Failed to perform the reset operation."
MISSING_FILE_NAME_PARAMETER_MSG = "Missing required parameter 'file_name'."
UNSUPPORTED_FIRMWARE_MSG = "iDRAC firmware version is not supported."
NO_OPERATION_SKIP_MSG = "Task is skipped as none of import, export or delete is specified."
INVALID_FILE_MSG = "File extension is invalid. Supported extensions for local 'share_type' " \
                   "are: .txt and .xml, and for network 'share_type' is: .xml."
CHANGES_NOT_FOUND = "No changes found to commit!"
CHANGES_FOUND = "Changes found to commit!"
ODATA_ID = "@odata.id"
ODATA_REGEX = "(.*?)@odata"
ATTRIBUTE = "</Attribute>"
SUCCESS_STATUS = "Success"
FAILED_STATUS = "Failed"
STATUS_SUCCESS = [200, 202]
ERROR_CODES = ["SYS041", "SYS044", "SYS045", "SYS046", "SYS047", "SYS048", "SYS050", "SYS051", "SYS062",
               "SYS063", "SYS064", "SYS065", "SYS067", "SYS068", "SYS070", "SYS071", "SYS072",
               "SYS073", "SYS075", "SYS076", "SYS077", "SYS078", "SYS079", "SYS080"]

class FACTORYRESET(): 
    def __init__(self, idrac, module):
        self.idrac = idrac
        self.module = module
    
    def execute(self):
        if self.module.check_mode:
          res = {'Status': 'Success', 'Message': CHANGES_FOUND, 'retVal': True}
          self.module.exit_json(msg = CHANGES_FOUND, reset_status= res, changed= True)
        reset_to_default = self.module.params.get('reset_to_default')
        self.force_reset = self.module.params.get('force_reset')
        self.wait_for_idrac = self.module.params.get('wait_for_idrac')
        self.idrac_firmware_version = get_idrac_firmware_version(self.idrac)
        if LooseVersion(self.idrac_firmware_version) >= '3.0' and not self.force_reset:
            self.__check_lcstatus()
        # if reset_to_default is None:
        #     message_res, output = self.__graceful_restart()
        # return message_res,output

    def __check_lcstatus(self):
        lcStatus_dict = {}
        lcStatus_dict['LCStatus'] = ""
        retry_count = 1
        while retry_count < IDRAC_RESET_RETRIES or lcStatus_dict.get('LCStatus') != "Ready":
            # self.module.warn("Reached here")
            result = {}
            lcstatus = self.idrac.invoke_request(IDRAC_RESET_LIFECYCLE_STATUS_URI,"POST",data=result)
            lcstatus_data = lcstatus.json_data.get('LCStatus')
            lcStatus_dict['LCStatus'] = lcstatus_data
            # pause(LC_STATUS_CHECK_SLEEP)
            retry_count = retry_count + 1
        
        if retry_count == IDRAC_RESET_RETRIES and lcStatus_dict.get('LCStatus') != "Ready":
            self.module.exit_json(msg="LC status check is {{ idrac_lc_status.LCStatus }} after {{ retry_count }} number of retries, Exiting..",failed=True)
        
    # def __graceful_restart(self):
    #     payload = {}
    #     payload["ResetType"] = "GracefulRestart"
    #     run_reset_status = self.idrac.invoke_request(IDRAC_RESET_GRACEFUL_RESTART_URI, "POST", data=payload)
    #     status = run_reset_status.status_code
    #     # status = 204
    #     result = {}
    #     tmp_res = {}
    #     result['idracreset'] = {}
    #     result['idracreset']['Data'] = {'StatusCode': status}
    #     result['idracreset']['StatusCode'] = status
    #     if status in STATUS_SUCCESS:
    #       if self.wait_for_idrac:
    #         track_failed, wait_msg = wait_after_idrac_reset(self.idrac, IDRAC_RESET_WAIT_TIME)
    #       if track_failed:
    #         self.module.exit_json(msg=wait_msg, Failed=True)
    #       tmp_res['msg'] =  IDRAC_RESET_RESTART_SUCCESS_MSG if self.wait_for_idrac else IDRAC_RESET_RESET_TRIGGER_MSG
    #       tmp_res['changed'] = True
    #       result['idracreset']['Message'] = IDRAC_RESET_SUCCESS_MSG
    #       result['idracreset']['Status'] = 'Success'
    #       result['idracreset']['retVal'] = True
    #     else:
    #       tmp_res['msg']  = FAILED_RESET_MSG
    #       tmp_res['changed'] = False
    #       result['idracreset']['Message'] = "XYZ"
    #       result['idracreset']['Status'] = 'FAILED'
    #       result['idracreset']['retVal'] = False
    #     return tmp_res, result 


def main():
    specs = {
        "reset_to_default": {"choices": ['All', 'ResetAllWithRootDefaults', 'Default','CustomDefaults']},
        "wait_for_idrac": {"type": "bool", "default": True},
        "force_reset": {"type": "bool", "default": False},
        "custom_defaults_file": {"type": "str"},
        "custom_defaults_buffer": {"type": "str"}
    }
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[("custom_defaults_file", "custom_defaults_buffer")],
        supports_check_mode=True)
    try:
        with iDRACRedfishAPI(module.params) as idrac:
            reset_obj = FACTORYRESET(idrac, module)
            message_res, output = reset_obj.execute()
            module.exit_json(msg=message_res.get('msg'), reset_status=output, changed = message_res.get('changed'))
            # module.exit_json(msg="XYZ")
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)

if __name__ == '__main__':
    main()
