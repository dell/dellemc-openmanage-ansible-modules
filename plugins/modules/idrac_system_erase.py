#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.2
# Copyright (C) 2024-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

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
  - This module allows you to erase system components such as iDRAC, BIOS, DIAG,
    and so forth. You can also erase storage components such as PERC NV cache,
    non-volatile memory, cryptographic erase of physical disks, and so on of the server
extends_documentation_fragment:
  - dellemc.openmanage.idrac_x_auth_options
options:
  component:
    description:
      - List of system and storage components that can be deleted.
      - The following are the supported components.
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
      - This parameter allows you to power on the server after the erase operation is completed. This is applicable when I(job_wait) is C(true).
      - C(true) power on the server.
      - C(false) does not power on the server.
    type: bool
    default: false
  job_wait:
    description:
      - Whether to wait till completion of the job. This is applicable when I(power_on) is C(true).
      - C(true) waits for job completion.
      - C(false) does not wait for job completion.
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
  - "Saksham Nautiyal (@Saksham-Nautiyal)"
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
- name: Erase a single component and power on the server
  dellemc.openmanage.idrac_system_erase:
    idrac_ip: 198.162.0.1
    idrac_user: username
    idrac_password: passw0rd
    ca_path: "/path/to/ca_cert.pem"
    component: ["BIOS"]
    power_on: true

- name: Erase multiple components and do not power on the server after the erase operation is completed
  dellemc.openmanage.idrac_system_erase:
    idrac_ip: 198.162.0.1
    idrac_user: username
    idrac_password: passw0rd
    ca_path: "/path/to/ca_cert.pem"
    component: ["BIOS", "DIAG", "PERCNVCache"]

- name: Erase multiple components and do not wait for the job completion
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
    get_dynamic_uri, trigger_restart_operation, validate_and_get_first_resource_id_uri, remove_key, idrac_redfish_job_tracking)


MANAGERS_URI = "/redfish/v1/Managers"
IDRAC_JOB_URI = "{res_uri}/Oem/Dell/Jobs/{job_id}"
ODATA = "@odata.id"
ODATA_REGEX = "(.*?)@odata"

OEM = "Oem"
MANUFACTURER = "Dell"
LC_SERVICE = "DellLCService"
ACTIONS = "Actions"
SYSTEM_ERASE = "DellLCService.SystemErase"
SYSTEM_ERASE_FETCH = "#DellLCService.SystemErase"
COMPONENT_ALLOWABLE_VALUES = "Component@Redfish.AllowableValues"
JOB_FILTER = "/Oem/Dell/Jobs?$expand=*($levels=1)"

ERASE_SUCCESS_COMPLETION_MSG = "Successfully completed the system erase operation."
ERASE_SUCCESS_SCHEDULED_MSG = "Successfully submitted the job for system erase operation."
ERASE_SUCCESS_POWER_ON_MSG = "Successfully completed the system erase operation and powered on " \
                             "the server."
NO_COMPONENT_MATCH = "Unable to complete the operation because the value entered for the " \
                     "'component' is not in the list of acceptable values."
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The value for the 'job_wait_timeout' parameter cannot be " \
                               "negative or zero."
WAIT_TIMEOUT_MSG = "The job is not complete after {0} seconds."
INVALID_COMPONENT_WARN_MSG = "Erase operation is not performed on these components - " \
                             "{unmatching_components_str_format} as they are either invalid or " \
                             "inapplicable."
FAILURE_MSG = "Unable to complete the system erase operation."
CHANGES_FOUND_MSG = "Changes found to be applied."
NO_CHANGES_FOUND_MSG = "No changes found to be applied."


class SystemErase():
    def __init__(self, idrac, module):
        """
        Initializes the class instance with the provided idrac and module parameters.

        :param idrac: The idrac parameter.
        :type idrac: Any
        :param module: The module parameter.
        :type module: Any
        """
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
        """
        Retrieves the URL for the system erase operation.

        Returns:
            str: The URL for the system erase operation.
        """
        url = self.get_url()
        resp = get_dynamic_uri(self.idrac, url)
        system_erase_url = (
            resp.get('Links', {})
            .get(OEM, {})
            .get(MANUFACTURER, {})
            .get(LC_SERVICE, {})
            .get(ODATA, {})
        )
        return system_erase_url

    def get_url(self):
        """
        Retrieves the URL for the resource.

        Returns:
            str: The URL for the resource.

        Raises:
            AnsibleExitJson: If the resource ID is not found.
        """
        res_id = self.module.params.get('resource_id')
        if res_id:
            uri = MANAGERS_URI + "/" + res_id
        else:
            uri, error_msg = validate_and_get_first_resource_id_uri(
                self.module, self.idrac, MANAGERS_URI)
            if error_msg:
                self.module.exit_json(msg=error_msg, failed=True)
        return uri

    def get_job_status(self, erase_component_response):
        """
        Retrieves the status of a job.

        Args:
            erase_component_response (object): The response object for the erase component
            operation.

        Returns:
            dict: The job details.

        Raises:
            AnsibleExitJson: If the job tracking times out.
        """
        job_wait_timeout = self.module.params.get('job_wait_timeout')
        res_uri = validate_and_get_first_resource_id_uri(self.module, self.idrac, MANAGERS_URI)
        job_tracking_uri = erase_component_response.headers.get("Location")
        job_id = job_tracking_uri.split("/")[-1]
        job_uri = IDRAC_JOB_URI.format(job_id=job_id, res_uri=res_uri[0])
        job_failed, msg, job_dict, wait_time = idrac_redfish_job_tracking(
            self.idrac, job_uri, max_job_wait_sec=job_wait_timeout)
        job_dict = remove_key(job_dict, regex_pattern=ODATA_REGEX)
        if int(wait_time) >= int(job_wait_timeout):
            self.module.exit_json(msg=WAIT_TIMEOUT_MSG.format(
                job_wait_timeout), changed=True, job_status=job_dict)
        if job_failed:
            self.module.exit_json(
                msg=job_dict.get('Message'),
                failed=True,
                job_details=job_dict)
        return job_dict

    def get_job_details(self, erase_component_response):
        """
        Retrieves the details of a job.

        Args:
            erase_component_response (object): The response object for the erase component
            operation.

        Returns:
            dict: The job details.

        Raises:
            None.
        """
        res_uri = validate_and_get_first_resource_id_uri(self.module, self.idrac, MANAGERS_URI)
        job_tracking_uri = erase_component_response.headers.get("Location")
        job_id = job_tracking_uri.split("/")[-1]
        job_uri = IDRAC_JOB_URI.format(job_id=job_id, res_uri=res_uri[0])
        job_response = self.idrac.invoke_request(job_uri, 'GET')
        job_details = job_response.json_data
        job_details = remove_key(job_details, regex_pattern=ODATA_REGEX)
        return job_details

    def check_system_erase_job(self):
        """
        Retrieves the state of the most recent SystemErase job.

        Returns:
            str: The state of the most recent SystemErase job. Possible values are:
                - "New"
                - "Scheduling"
                - "Running"
                - "Completed"
                - "Failed"
                - "Unknown" if no SystemErase job is found.
        """
        url = self.get_url()
        job_details_url = url + f"/{JOB_FILTER}"
        job_resp = self.idrac.invoke_request(job_details_url, "GET")
        job_list = job_resp.json_data.get('Members', [])
        job_list_reversed = list(reversed(job_list))
        jb_state = 'Unknown'
        for jb in job_list_reversed:
            if jb.get("JobType") == "SystemErase" and jb.get("JobState") in [
                    "New", "Scheduling", "Running", "Completed", "Failed"]:
                jb_state = jb.get("JobState")
                break
        return jb_state

    def validate_job_wait(self):
        """
        Validates job_wait and job_wait_timeout parameters.
        """
        if self.module.params.get('job_wait') and self.module.params.get('job_wait_timeout') <= 0:
            self.module.exit_json(
                msg=TIMEOUT_NEGATIVE_OR_ZERO_MSG, failed=True)

    def check_allowable_value(self, component):
        """
        Check if the given component values are in the allowable values.

        Args:
            component (list): A list of component values.

        Returns:
            tuple: A tuple containing two lists. The first list contains the matching values, and
            the second list contains the unmatching values.

        Raises:
            None.
        """
        sytem_erase_url = self.get_system_erase_url()
        system_erase_response = self.idrac.invoke_request(sytem_erase_url, "GET")
        allowable_values = system_erase_response.json_data[ACTIONS][SYSTEM_ERASE_FETCH][
            COMPONENT_ALLOWABLE_VALUES]
        actual_values = component
        matching_values = []
        unmatching_values = []
        for value in actual_values:
            if value in allowable_values:
                matching_values.append(value)
            else:
                unmatching_values.append(value)
        if len(matching_values) == 0 and not self.module.check_mode:
            self.module.exit_json(msg=NO_COMPONENT_MATCH, skipped=True)
        if len(unmatching_values) > 0 and self.module.check_mode:
            if len(matching_values) > 0 :
                self.module.exit_json(msg=CHANGES_FOUND_MSG, changed=True)
            else:
                self.module.exit_json(msg=NO_CHANGES_FOUND_MSG, changed=False)
        return matching_values, unmatching_values

    def warn_unmatching_components(self, unmatching_components):
        """
        Warn the user about unmatching components.

        Args:
            unmatching_components (list): A list of unmatching components.

        Returns:
            None
        """
        if len(unmatching_components) > 0:
            unmatching_components_str_format = ", '".join(
                item + "'" for item in unmatching_components)
            self.module.warn(INVALID_COMPONENT_WARN_MSG.format(
                unmatching_components_str_format=unmatching_components_str_format))


class EraseComponent(SystemErase):
    """
    Class to erase component and perform all the operations
    """
    STATUS_SUCCESS = [202]
    JOB_STATUS = ["New", "Scheduling", "Running"]

    def execute(self):
        """
        Executes the system erase operation.

        This function checks if the job_wait parameter is set and validates the job wait.
        It also checks if the module is in check mode and checks the state of the system erase job.
        If the job state is in the JOB_STATUS list, it exits with a message indicating no changes
        found.
        If the job state is not in the JOB_STATUS list, it exits with a message indicating changes
        found.

        The function then creates a payload dictionary and assigns the matching components to
        the 'Component' key.
        It retrieves the system erase URL and sends a POST request to initiate the erase operation.
        The response status code is checked and if it is in the STATUS_SUCCESS list, it proceeds to
        handle the job.
        If the job_wait parameter is set and the power_on parameter is also set, it retrieves the
        job status, performs the power on operation, warns about unmatching components, and exits
        with a message indicating the erase operation was successful and the job details.
        If the job_wait parameter is set but the power_on parameter is not set, it retrieves the
        job status, warns about unmatching components, and exits with a message indicating the
        erase operation was successful and the job details.
        If the job_wait parameter is not set, it retrieves the job details, warns about unmatching
        components, and exits with a message indicating the erase operation was scheduled and the
        job details.
        If the response status code is not in the STATUS_SUCCESS list, it retrieves the job status
        and exits with a message indicating the operation failed.

        Returns:
            None
        """
        if self.module.params.get('job_wait'):
            self.validate_job_wait()
        component_list = self.module.params.get('component')
        matching_components, unmatching_components = self.check_allowable_value(component_list)
        if self.module.check_mode:
            job_state = self.check_system_erase_job()
            if job_state in self.JOB_STATUS:
                self.module.exit_json(msg=NO_CHANGES_FOUND_MSG, changed=False)
            else:
                self.module.exit_json(msg=CHANGES_FOUND_MSG, changed=True)
        payload = {}
        payload["Component"] = matching_components
        system_erase_url = self.get_system_erase_url()
        erase_component_response = self.idrac.invoke_request(
            system_erase_url + f"/{ACTIONS}/{SYSTEM_ERASE}", "POST", data=payload)
        status = erase_component_response.status_code
        if status in self.STATUS_SUCCESS:
            if self.module.params.get('job_wait'):
                if self.module.params.get('power_on'):
                    job_dict = self.get_job_status(erase_component_response)
                    trigger_restart_operation(self.idrac, restart_type="On")
                    self.warn_unmatching_components(unmatching_components)
                    self.module.exit_json(msg=ERASE_SUCCESS_POWER_ON_MSG, changed=True,
                                          job_details=job_dict)
                else:
                    job_dict = self.get_job_status(erase_component_response)
                    self.warn_unmatching_components(unmatching_components)
                    self.module.exit_json(msg=ERASE_SUCCESS_COMPLETION_MSG, changed=True,
                                          job_details=job_dict)
            else:
                job_dict = self.get_job_details(erase_component_response)
                self.warn_unmatching_components(unmatching_components)
                self.module.exit_json(msg=ERASE_SUCCESS_SCHEDULED_MSG, changed=False,
                                      job_details=job_dict)
        else:
            job_dict = self.get_job_status(erase_component_response)
            self.module.exit_json(msg=FAILURE_MSG, failed=True, job_details=job_dict)


def main():
    """
    Executes the main function of the program.

    This function initializes the necessary modules and arguments, and then
    creates an instance of the iDRACRedfishAPI class. It then creates an
    instance of the EraseComponent class and calls its execute method.

    If any exceptions are raised during the execution of the code, the
    appropriate error message is returned.

    Parameters:
        None

    Returns:
        None
    """
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
    """
    Returns a dictionary specifying the argument specification for the function.

    Parameters:
        None

    Returns:
        dict: A dictionary containing the argument specification.
              The dictionary has the following keys:
              - "component": A dictionary specifying the type and required status of the
              "component" argument.
              - "power_on": A dictionary specifying the type and default value of the "power_on"
              argument.
              - "job_wait": A dictionary specifying the type and default value of the "job_wait"
              argument.
              - "job_wait_timeout": A dictionary specifying the type and default value of the
              "job_wait_timeout" argument.
              - "resource_id": A dictionary specifying the type of the "resource_id" argument.
    """
    return {
        "component": {"type": 'list', "elements": 'str', "required": True},
        "power_on": {"type": 'bool', "default": False},
        "job_wait": {"type": 'bool', "default": True},
        "job_wait_timeout": {"type": 'int', "default": 1200},
        "resource_id": {"type": 'str'}
    }


if __name__ == '__main__':
    main()
