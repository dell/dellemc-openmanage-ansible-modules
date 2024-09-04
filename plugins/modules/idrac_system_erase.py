#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.7.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: idrac_system_erase
short_description: Erase system and storage components of the server
version_added: "9.7.0"
description:
  - This module allows erasing System components such as iDRAC, BIOS, DIAG,
    etc., and Storage components such as PERC NV cache, Non-volatile memory,
    Cryptographic erase PD, etc. of the server.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_x_auth_options
options:
  component:
    description:
      - System and storage components to erase.
      - Below are the supported components.
        AllApps
        BIOS
        CryptographicErasePD
        DIAG
        DPU
        DrvPack
        IDRAC
        LCData
        NonVolatileMemory
        OverwritePD
        PERCNVCache
        ReinstallFW
        vFlash
    type: list
    elements: str
    required: true
  power_on:
    description:
      - This allows to power on the server after erase operation. This is applicable only when I(job_wait) is C(true).
      - C(true) will power on the server.
      - C(false) will not power on the server.
    type: bool
    default: false
  job_wait:
    description:
      - Whether to wait till completion of the job. This is applicable when I(power_on) is C(true).
      - C(true) will wait for job completion.
      - C(false) will not wait for job completion.
    type: bool
    default: true
  job_wait_timeout:
    description:
      - The maximum wait time of I(job_wait) in seconds. The job is tracked only for this duration.
      - This option is applicable when I(job_wait) is C(true).
    type: int
    default: 1200
  resource_id:
    description:
      - Manager ID of the iDRAC.
    type: str
requirements:
  - "python >= 3.9.6"
author:
  - "Rajshekar P(@rajshekarp87)"
attributes:
    check_mode:
        description: Runs task to validate without performing action on the target machine.
        support: full
    diff_mode:
        description: Runs the task to report the changes made or to be made.
        support: none
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports only iDRAC9 and above.
    - This module supports IPv4 and IPv6 addresses.
"""

EXAMPLES = r"""
---
- name: Erase single component and power on the server
  dellemc.openmanage.idrac_system_erase:
    idrac_ip: 198.162.0.1
    idrac_user: username
    idrac_password: passw0rd
    ca_path: "/path/to/ca_cert.pem"
    component: ["BIOS"]
    power_on: true

- name: Erase multiple components and don't power on the server after erase operation
  dellemc.openmanage.idrac_system_erase:
    idrac_ip: 198.162.0.1
    idrac_user: username
    idrac_password: passw0rd
    ca_path: "/path/to/ca_cert.pem"
    component: ["BIOS", "DIAG", "PERCNVCache"]

- name: Erase multiple components and don't wait for the job completion
  dellemc.openmanage.idrac_system_erase:
    idrac_ip: 198.162.0.1
    idrac_user: username
    idrac_password: passw0rd
    ca_path: "/path/to/ca_cert.pem"
    component: ["IDRAC", "DPU", "LCData"]
    job_wait: false
"""

RETURN = r'''
---
msg:
    description: Status of the component system erase operation.
    returned: always
    type: str
    sample: "Successfully completed the system erase operation."
job_details:
    description: Returns the output for status of the job.
    returned: For system erase operation
    type: dict
    sample: {
        "ActualRunningStartTime": null,
        "ActualRunningStopTime": null,
        "CompletionTime": "2024-08-06T19:55:01",
        "Description": "Job Instance",
        "EndTime": "TIME_NA",
        "Id": "JID_229917427823",
        "JobState": "Completed",
        "JobType": "SystemErase",
        "Message": "Job completed successfully.",
        "MessageArgs": [],
        "MessageArgs@odata.count": 0,
        "MessageId": "SYS018",
        "Name": "System_Erase",
        "PercentComplete": 100,
        "StartTime": "2024-08-06T19:49:02",
        "TargetSettingsURI": null
    }
error_info:
    description: Details of the HTTP Error.
    returned: On HTTP error
    type: dict
    sample: {
            "error": {
                "@Message.ExtendedInfo": [
                    {
                        "Message": "Unable to complete the operation because the value NonVolatileMemor entered for the property Component is not in the list
                            of acceptable values.",
                        "MessageArgs": [
                            "NonVolatileMemor",
                            "Component"
                        ],
                        "MessageArgs@odata.count": 2,
                        "MessageId": "IDRAC.2.9.SYS426",
                        "RelatedProperties": [],
                        "RelatedProperties@odata.count": 0,
                        "Resolution": "Enter a valid value from the enumeration list that Redfish service supports and retry the operation.For information
                            about valid values, see the iDRAC User's Guide available on the support site.",
                        "Severity": "Warning"
                    },
                    {
                        "Message": "The value 'NonVolatileMemor' for the property Component is not in the list of acceptable values.",
                        "MessageArgs": [
                            "NonVolatileMemor",
                            "Component"
                        ],
                        "MessageArgs@odata.count": 2,
                        "MessageId": "Base.1.12.PropertyValueNotInList",
                        "RelatedProperties": [],
                        "RelatedProperties@odata.count": 0,
                        "Resolution": "Choose a value from the enumeration list that the implementation can support and resubmit the request if the operation
                            failed.",
                        "Severity": "Warning"
                    }
                ],
                "code": "Base.1.12.GeneralError",
                "message": "A general error has occurred. See ExtendedInfo for more information"
            }
        }
'''


import json
from urllib.error import HTTPError, URLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, IdracAnsibleModule
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    get_dynamic_uri, power_on_operation, validate_and_get_first_resource_id_uri, remove_key, idrac_redfish_job_tracking)


REDFISH = "/redfish/v1"
MANAGERS_URI = "/redfish/v1/Managers"
IDRAC_JOB_URI = "{res_uri}/Jobs/{job_id}"
ODATA = "@odata.id"
ODATA_REGEX = "(.*?)@odata"

OEM = "Oem"
MANUFACTURER = "Dell"
LC_SERVICE = "DellLCService"
ACTIONS = "Actions"
SYSTEM_ERASE = "DellLCService.SystemErase"
SYSTEM_ERASE_FETCH = "#DellLCService.SystemErase"
COMPONENT_ALLOWABLE_VALUSE = "Component@Redfish.AllowableValues"

ERASE_SUCCESS_COMPLETION_MSG = "Successfully completed the system erase operation."
ERASE_SUCCESS_SCHEDULED_MSG = "Successfully submitted the job for system erase operation."
ERASE_SUCCESS_POWER_ON_MSG = "Successfully completed the system erase operation and powered on " \
                             "the server."
NO_COMPONENT_MATCH = "Unable to complete the operation because the value entered for the " \
                     "'component' is not in the list of acceptable values."
FAILURE_MSG = "Unable to complete the system erase operation."
CHANGES_FOUND_MSG = "Changes found to be applied."
NO_CHANGES_FOUND_MSG = "No changes found to be applied."


class SystemErase():
    def __init__(self, idrac, module):
        self.idrac = idrac
        self.module = module

    def execute(self):
        """
        Executes the function with the given module.

        :param module: The module to execute.
        :type module: Any
        :return: None
        """

    def get_system_erase_url(self):
        res_id = self.module.params.get('resource_id')
        if res_id:
            uri = MANAGERS_URI + "/" + res_id
        else:
            uri, error_msg = validate_and_get_first_resource_id_uri(
                self.module, self.idrac, MANAGERS_URI)
            if error_msg:
                self.module.exit_json(msg=error_msg, failed=True)
        resp = get_dynamic_uri(self.idrac, uri)
        system_erase_url = resp.get('Links', {}).get(OEM, {}).get(MANUFACTURER, {}).get(LC_SERVICE, {}).get(ODATA, {})
        return system_erase_url

    def get_job_status(self, erase_component_response):
        res_uri = validate_and_get_first_resource_id_uri(self.module, self.idrac, MANAGERS_URI)
        job_tracking_uri = erase_component_response.headers.get("Location")
        job_id = job_tracking_uri.split("/")[-1]
        job_uri = IDRAC_JOB_URI.format(job_id=job_id, res_uri=res_uri[0])
        job_failed, msg, job_dict, wait_time = idrac_redfish_job_tracking(self.idrac, job_uri)
        job_dict = remove_key(job_dict, regex_pattern=ODATA_REGEX)
        if job_failed:
            self.module.exit_json(
                msg=job_dict.get('Message'),
                failed=True,
                job_details=job_dict)
        return job_dict

    def check_allowable_value(self, component):
        sytem_erase_url = self.get_system_erase_url()
        system_erase_response = self.idrac.invoke_request(sytem_erase_url, "GET")
        allowable_values = system_erase_response.json_data[ACTIONS][SYSTEM_ERASE_FETCH]
        [COMPONENT_ALLOWABLE_VALUSE]
        actual_values = component
        matching_values = []
        unmatching_values = []
        for value in actual_values:
            if value in allowable_values:
                matching_values.append(value)
            else:
                unmatching_values.append(value)
        if len(matching_values) == 0:
            self.module.exit_json(msg=NO_COMPONENT_MATCH, skipped=True)
        return matching_values, unmatching_values


class EraseComponent(SystemErase):
    STATUS_SUCCESS = [202]

    def execute(self):
        payload = {}
        component_list = self.module.params.get('component')
        matchin_components, unmatching_components = self.check_allowable_value(component_list)
        payload["Component"] = matchin_components
        system_erase_url = self.get_system_erase_url()
        erase_component_response = self.idrac.invoke_request(
            system_erase_url + f"/{ACTIONS}/{SYSTEM_ERASE}", "POST", data=payload)
        status = erase_component_response.status_code
        if status in self.STATUS_SUCCESS:
            if self.module.params.get('job_wait'):
                if self.module.params.get('power_on'):
                    job_dict = self.get_job_status(erase_component_response)
                    power_on_operation(self.idrac)
                    self.module.exit_json(msg=ERASE_SUCCESS_POWER_ON_MSG, changed=True,
                                          job_details=job_dict)
                else:
                    job_dict = self.get_job_status(erase_component_response)
                    self.module.exit_json(msg=ERASE_SUCCESS_COMPLETION_MSG, changed=True,
                                          job_details=job_dict)
            else:
                self.module.exit_json(msg=ERASE_SUCCESS_SCHEDULED_MSG, changed=False)
        else:
            job_status = self.get_job_status(erase_component_response)
            self.module.exit_json(msg=FAILURE_MSG, failed=True)


def main():
    specs = get_argument_spec()
    module = IdracAnsibleModule(
        argument_spec=specs,
        supports_check_mode=True
    )
    try:
        with iDRACRedfishAPI(module.params) as idrac:
            system_erase_obj = EraseComponent(idrac, module)
            system_erase_obj.execute()
    except HTTPError as err:
        filter_err = remove_key(json.load(err), regex_pattern=ODATA_REGEX)
        module.exit_json(msg=str(err), error_info=filter_err, failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


def get_argument_spec():
    return {
        "component": {"type": 'list', "elements": 'str', "required": True},
        "power_on": {"type": 'bool', "default": False},
        "job_wait": {"type": 'bool', "default": True},
        "job_wait_timeout": {"type": 'int', "default": 1200},
        "resource_id": {"type": 'str'}
    }


if __name__ == '__main__':
    main()
