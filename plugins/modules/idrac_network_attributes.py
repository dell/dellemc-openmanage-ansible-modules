#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.4.0
# Copyright (C) 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_network_attributes
short_description: Configures the iDRAC network attributes
version_added: "8.4.0"
description:
  - This module allows to configure iDRAC network settings.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
  network_adapter_id:
    type: str
    required: true
    description:
        - FQDD of the network adapter device that represents the physical network adapter capable of connecting to a computer network.
        - An example of FQDD of the network adapter is 'NIC.Mezzanine.1A'
  network_device_function_id:
    type: str
    required: true
    description:
      - FQDD of the network adapter device function that represents a logical interface exposed by the network adapter.
      - An example of FQDD of the network adapter device function is 'NIC.Mezzanine.1A-1-1'
  network_attributes:
    type: dict
    description:
      - "Dictionary of network attributes and value. To view the list of attributes and its structure, see the below API
        U(https://I(idrac_ip)/redfish/v1/Systems/System.Embedded.1/NetworkAdapters/<network_id>/NetworkDeviceFunctions/
        <network_port_id>/Settings)."
      - I(network_attributes) is mutually exclusive with I(oem_network_attributes).
  oem_network_attributes:
    type: dict
    description:
      - "The attributes must be part of the Integrated Dell Remote Access Controller Attribute Registry.
        To view the list of attributes in Attribute Registry for iDRAC9 and newer versions. For more information,
        see, U(https://I(idrac_ip)/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/<network_id>/NetworkDeviceFunctions/
        <network_port_id>/Oem/Dell/DellNetworkAttributes/<network_port_id>)
        and U(https://I(idrac_ip)/redfish/v1/Registries/NetworkAttributesRegistry_<network_port_id>/
        NetworkAttributesRegistry_network_port_id.json)."
      - For iDRAC8 based servers, derive the network attribute name from Server Configuration Profile.
      - I(oem_network_attributes) is mutually exclusive with I(network_attributes).
  resource_id:
    type: str
    description:
      - Id of the resource.
      - If the value for resource ID is not provided, the module picks the first resource ID available from the list of system resources returned by the iDRAC.
  clear_pending:
    type: bool
    default: false
    description:
      - This parameter allows you to clear all the pending network attributes changes.
      - I(clear_pending) is applicable only when I(oem_network_attributes) is specified.
      - C(false) does not perform any operation.
      - C(true) discards any pending changes to network attributes, or if a job is in scheduled state, removes the job.
  apply_time:
    type: str
    required: true
    description:
      - Apply time of the I(network_attributes) and I(oem_network_attributes).
      - This is applicable only to I(network_attributes) and I(oem_network_attributes).
      - C(Immediate) allows the user to immediately reboot the host and apply the changes. I(job_wait)
        is applicable.
      - C(OnReset) allows the user to apply the changes on the next reboot of the host server.
      - C(AtMaintenanceWindowStart) allows the user to apply at the start of a maintenance window as specified
        in I(maintenance_window). A reboot job is scheduled.
      - C(InMaintenanceWindowOnReset) allows to apply after a manual reset but within the maintenance window as
        specified in I(maintenance_window).
    choices: [Immediate, OnReset, AtMaintenanceWindowStart, InMaintenanceWindowOnReset]
  maintenance_window:
    type: dict
    description:
      - This option allows you to schedule the maintenance window.
      - This is required when I(apply_time) is C(AtMaintenanceWindowStart) or C(InMaintenanceWindowOnReset).
    suboptions:
      start_time:
        type: str
        required: true
        description:
          - The start time for the maintenance window to be scheduled.
          - "The format is YYYY-MM-DDThh:mm:ss<offset>"
          - "<offset> is the time offset from UTC that the current timezone set in
            iDRAC in the format: +05:30 for IST."
      duration:
        type: int
        required: true
        description:
          - The duration in seconds for the maintenance window.
  job_wait:
    type: bool
    default: true
    description:
      - Provides the option to wait for job completion.
      - This is applicable for I(job_wait) when I(apply_time) is C(Immediate) for I(network_attributes).
  job_wait_timeout:
    type: int
    default: 1200
    description:
      - The maximum wait time of I(job_wait) in seconds. The job is tracked only for this duration.
      - This option is applicable when I(job_wait) is C(true).
requirements:
    - "python >= 3.9.6"
author:
    - "Felix Stephen (@felixs88)"
    - "Anooja Vardhineni (@anooja-vardhineni)"
notes:
    - This module requires 'Administrator' privilege for I(idrac_user).
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports both IPv4 and IPv6 address for I(idrac_ip).
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Configure iDRAC oem network attributes
  dellemc.openmanage.idrac_network:
    idrac_ip:   "192.168.0.1"
    idrac_user: "user_name"
    idrac_password:  "user_password"
    ca_path: "/path/to/ca_cert.pem"
    network_adapter_id: 'NIC.Mezzanine.1A'
    network_device_function_id: 'NIC.Mezzanine.1A-1-1'
    oem_network_attributes:
        VLanId: 10
    resource_id: 'System.Embedded.1'
    apply_time: "AtMaintenanceWindowStart"
    maintenance_window:
      start_time: "2023-10-06T15:00:00-05:00"
      duration: 600
    job_wait: true
    job_wait_timeout: 1500

- name: Clear pending oem network attribute
  dellemc.openmanage.idrac_network:
    idrac_ip:   "192.168.0.1"
    idrac_user: "user_name"
    idrac_password:  "user_password"
    ca_path: "/path/to/ca_cert.pem"
    network_adapter_id: 'NIC.Mezzanine.1A'
    network_device_function_id: 'NIC.Mezzanine.1A-1-1'
    apply_time: "Immediate"
    clear_pending: true

"""

RETURN = r'''
---
msg:
  description: Successfully configured the idrac network attributes.
  returned: always
  type: str
  sample: "Successfully configured the idrac network settings."
network_status:
  description: Status of the Network settings operation job.
  returned: success
  type: dict
  sample: {
    "@odata.context": "/redfish/v1/$metadata#DellJob.DellJob",
    "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_856418531008",
    "@odata.type": "#DellJob.v1_0_2.DellJob",
    "CompletionTime": "2020-03-31T03:04:15",
    "Description": "Job Instance",
    "EndTime": null,
    "Id": "JID_856418531008",
    "JobState": "Completed",
    "JobType": "ImportConfiguration",
    "Message": "Successfully imported and applied Server Configuration Profile.",
    "MessageArgs": [],
    "MessageArgs@odata.count": 0,
    "MessageId": "SYS053",
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

import json
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, idrac_auth_params
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import remove_key, wait_for_idrac_job_completion, \
    get_dynamic_uri, get_scheduled_job_resp, delete_job, get_current_time
from ansible.module_utils.compat.version import LooseVersion
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.common.dict_transformations import recursive_diff

SYSTEMS_URI = "/redfish/v1/Systems"
CHASSIS_URI = "/redfish/v1/Chassis"
REGISTRY_URI = '/redfish/v1/Registries'
GET_ALL_JOBS = "/redfish/v1/JobService/Jobs?$expand=*($levels=1)"
SINGLE_JOB = "/redfish/v1/JobService/Jobs/{job_id}"

GET_NETWORK_ADAPTER_URI = "/redfish/v1/Systems/{resource_id}/NetworkAdapters"
GET_NETWORK_DEVICE_FUNC_URI = "/redfish/v1/Systems/{resource_id}/NetworkAdapters/{network_adapter_id}/NetworkDeviceFunctions"
DMTF_GET_PATCH_NETWORK_ATTR_URI = "/redfish/v1/Systems/{resource_id}/NetworkAdapters/{network_adapter_id}/NetworkDeviceFunctions/ \
{network_device_function_id}/Settings"
GET_IDRAC_FIRMWARE_VER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1?$select=FirmwareVersion"

SUCCESS_MSG = "Successfully updated the network attributes."
SUCCESS_CLEAR_PENDING_ATTR_MSG = "Successfully cleared the pending network attributes."
SCHEDULE_MSG = "Successfully scheduled the job for network attributes update."
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The value for the `job_wait_timeout` parameter cannot be negative or zero."
MAINTENACE_OFFSET_DIFF_MSG = "The maintenance time must be post-fixed with local offset to {0}."
MAINTENACE_OFFSET_BEHIND_MSG = "The specified maintenance time window occurs in the past, provide a future time to schedule the maintenance window."
APPLY_TIME_NOT_SUPPORTED_MSG = "Apply time {0} is not supported."
INVALID_ATTR_MSG = "Unable to update the network attributes because invalid values are entered. \
    Enter the valid values for the network attributes and retry the operation."
VALID_AND_INVALID_ATTR_MSG = "Successfully updated the network attributes for valid values. \
    Unable to update other attributes because invalid values are entered. Enter the valid values and retry the operation."
NO_CHANGES_FOUND_MSG = "No changes found to be applied."
CHANGES_FOUND_MSG = "Changes found to be applied."
INVALID_ID_MSG = "Unable to complete the operation because " + \
                 "the value `{0}` for the input  `{1}` parameter is invalid."
JOB_RUNNING_CLEAR_PENDING_ATTR = "{0} Config job is running. Wait for the job to complete. Currently can not clear pending attributes."


class IDRACNetworkAttributes:

    def __init__(self, idrac, module, base_uri) -> None:
        self.module = module
        self.idrac = idrac
        self.base_uri = base_uri
        self.network_adapter_id_uri = None
        self.network_device_function_id = None
        self.manager_uri = None

    def __get_idrac_firmware_version(self) -> str:
        firm_version = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_FIRMWARE_VER_URI)
        return firm_version.json_data.get('FirmwareVersion', '')

    def __get_resource_id(self):
        odata = '@odata.id'
        found = False
        res_id_uri = None
        res_id_input = self.module.params.get('resource_id')
        res_id_members = get_dynamic_uri(self.idrac, self.base_uri, 'Members')
        for each in res_id_members:
            if res_id_input and res_id_input == each[odata].split('/')[-1]:
                res_id_uri = each[odata]
                found = True
                break
        if not found and res_id_input:
            self.module.exit_json(failed=True, msg=INVALID_ID_MSG.format(
                res_id_input, 'resource_id'))
        elif res_id_input is None:
            res_id_uri = res_id_members[0][odata]
        return res_id_uri

    def __get_registry_fw_less_than_6_more_than_3(self):
        reg = {}
        network_device_function_id = self.module.params.get('network_device_function_id')
        registry = get_dynamic_uri(self.idrac, REGISTRY_URI, 'Members')
        for each_member in registry:
            if network_device_function_id in each_member.get('@odata.id'):
                location = get_dynamic_uri(self.idrac, each_member.get('@odata.id'), 'Location')
                if location:
                    uri = location[0].get('Uri')
                    attr = get_dynamic_uri(self.idrac, uri, 'RegistryEntries').get('Attributes', {})
                    for each_attr in attr:
                        reg.update({each_attr['AttributeName']: each_attr['CurrentValue']})
                    break
        return reg

    def __validate_time(self, mtime):
        curr_time, date_offset = get_current_time(self.idrac)
        if not mtime.endswith(date_offset):
            self.module.exit_json(failed=True, msg=MAINTENACE_OFFSET_DIFF_MSG.format(date_offset))
        if mtime < curr_time:
            self.module.exit_json(failed=True, msg=MAINTENACE_OFFSET_BEHIND_MSG)

    def __get_redfish_apply_time(self, aplytm, rf_settings):
        rf_set = {}
        reboot_req = False
        if rf_settings:
            if 'Maintenance' in aplytm:
                if aplytm not in rf_settings:
                    self.module.exit_json(failed=True, msg=APPLY_TIME_NOT_SUPPORTED_MSG.format(aplytm))
                else:
                    rf_set['ApplyTime'] = aplytm
                    m_win = self.module.params.get('maintenance_window')
                    self.__validate_time(m_win.get('start_time'))
                    rf_set['MaintenanceWindowStartTime'] = m_win.get('start_time')
                    rf_set['MaintenanceWindowDurationInSeconds'] = m_win.get('duration')
            else:  # assuming OnReset is always
                if aplytm == "Immediate" and aplytm not in rf_settings:
                    reboot_req = True
                    aplytm = 'OnReset'
                rf_set['ApplyTime'] = aplytm
        return rf_set, reboot_req

    def get_current_server_registry(self):
        reg = {}
        oem_network_attributes = self.module.params.get('oem_network_attributes')
        firm_ver = self.__get_idrac_firmware_version()
        if oem_network_attributes:
            if LooseVersion(firm_ver) >= '6.0':
                oem_links = get_dynamic_uri(self.idrac, self.network_device_function_id, 'Links')
                uri = oem_links.get('Oem').get('Dell').get('DellNetworkAttributes').get('@odata.id')
                reg = get_dynamic_uri(self.idrac, uri).get('Attributes', {})
            if '3.0' < LooseVersion(firm_ver) < '6.0':
                reg = self.__get_registry_fw_less_than_6_more_than_3()
        else:  # For Redfish
            pass
        return reg

    def extract_error_msg(self, resp):
        error_info = {}
        error = resp.json_data.get('error')
        for each_dict_err in error.get("@Message.ExtendedInfo"):
            key = each_dict_err.get('MessageArgs')[0]
            msg = each_dict_err.get('Message')
            if key not in error_info:
                error_info.update({key: msg})
        return error_info

    def get_diff_between_current_and_module_input(self, module_attr, server_attr) -> tuple[int, dict]:
        invalid = {}
        diff = recursive_diff(module_attr, server_attr)
        for each_attr in module_attr:
            if each_attr not in server_attr:
                invalid.update({each_attr: 'Attribute does not exist.'})
        return diff, invalid

    def perform_validation_for_network_adapter_id(self) -> tuple[bool, str]:
        odata = '@odata.id'
        network_adapter_id = self.module.params.get('network_adapter_id')
        found_adapter = False
        first_resource_id_uri = self.__get_resource_id()
        network_adapters = get_dynamic_uri(self.idrac, first_resource_id_uri, 'NetworkAdapters')[odata]
        network_adapter_list = get_dynamic_uri(self.idrac, network_adapters, 'Members')
        for each_adapter in network_adapter_list:
            if network_adapter_id in each_adapter.get(odata, ''):
                found_adapter = True
                self.network_adapter_id_uri = each_adapter.get(odata, '')
                break
        if not found_adapter:
            self.module.exit_json(failed=True, msg=INVALID_ID_MSG.format(network_adapter_id,
                                                                         'network_adapter_id'))

    def perform_validation_for_network_device_function_id(self) -> tuple[bool, str]:
        odata = '@odata.id'
        found_device = False
        network_device_function_id = self.module.params.get('network_device_function_id')
        network_devices = get_dynamic_uri(self.idrac, self.network_adapter_id_uri, 'NetworkDeviceFunctions')[odata]
        network_device_list = get_dynamic_uri(self.idrac, network_devices, 'Members')
        for each_device in network_device_list:
            if network_device_function_id in each_device.get(odata, ''):
                found_device = True
                self.network_device_function_id = each_device.get(odata, '')
                break
        if not found_device:
            self.module.exit_json(failed=True, msg=INVALID_ID_MSG.format(network_device_function_id,
                                                                             'network_device_function_id'))

    def validate_job_timeout(self):
        if self.module.params.get("job_wait") and self.module.params.get("job_wait_timeout") <= 0:
            self.module.exit_json(msg=TIMEOUT_NEGATIVE_OR_ZERO_MSG, failed=True)

    def apply_time(self, setting_uri):
        resp = get_dynamic_uri(self.idrac, setting_uri, "@Redfish.Settings")
        rf_settings = resp.get("SupportedApplyTimes", [])
        apply_time = self.module.params.get('apply_time', {})
        rf_set, reboot_required = self.__get_redfish_apply_time(apply_time, rf_settings)
        return rf_set


class OEMNetworkAttributes(IDRACNetworkAttributes):
    def __init__(self, idrac, module, base_uri) -> None:
        super().__init__(idrac, module, base_uri)

    def clear_pending(self):
        oem_links = get_dynamic_uri(self.idrac, self.network_device_function_id, 'Links')
        oem_uri = oem_links.get('Oem').get('Dell').get('DellNetworkAttributes').get('@odata.id')
        resp = get_dynamic_uri(self.idrac, oem_uri, '@Redfish.Settings')
        settings_uri = resp.get('SettingsObject').get('@odata.id')
        settings_uri_resp = get_dynamic_uri(self.idrac, settings_uri)
        pending_attributes = settings_uri_resp.get('Attributes')
        clear_pending_uri = settings_uri_resp.get('Actions').get('#DellManager.ClearPending').get('target')
        if not pending_attributes:
            self.module.exit_json(msg=NO_CHANGES_FOUND_MSG)
        job_resp = get_scheduled_job_resp(self.idrac, 'NICConfiguration')
        job_id, job_state = job_resp.get('Id'), job_resp.get('JobState')
        if job_id:
            if job_state in ["Running"]:
                job_resp = remove_key(job_resp, regex_pattern='(.*?)@odata')
                self.module.exit_json(failed=True, msg=JOB_RUNNING_CLEAR_PENDING_ATTR.format('NICConfiguration'),
                                      job_status=job_resp)
            elif job_state in ["Starting", "Scheduled", "Scheduling"]:
                if self.module.check_mode:
                    self.module.exit_json(msg=CHANGES_FOUND_MSG, changed=True)
                delete_job(self.idrac, job_id)
                self.module.exit_json(msg=SUCCESS_CLEAR_PENDING_ATTR_MSG, changed=True)
        if self.module.check_mode:
            self.module.exit_json(msg=CHANGES_FOUND_MSG, changed=True)
        self.idrac.invoke_request(clear_pending_uri, "POST", data="{}", dump=False)
        self.module.exit_json(msg=SUCCESS_CLEAR_PENDING_ATTR_MSG, changed=True)

    def perform_operation(self):
        oem_network_attributes = self.module.params.get('oem_network_attributes')
        job_wait = self.module.params.get('job_wait')
        job_wait_timeout = self.module.params.get('job_wait_timeout')
        payload = {'Attributes': oem_network_attributes}
        oem_links = get_dynamic_uri(self.idrac, self.network_device_function_id, 'Links')
        oem_uri = oem_links.get('Oem').get('Dell').get('DellNetworkAttributes').get('@odata.id')
        apply_time_setting = self.apply_time(oem_uri)
        if apply_time_setting:
            payload.update({"@Redfish.SettingsApplyTime": apply_time_setting})

        patch_uri = get_dynamic_uri(self.idrac, oem_uri).get('@Redfish.Settings', {}).get('SettingsObject', {}).get('@odata.id')
        response = self.idrac.invoke_request(method='PATCH', uri=patch_uri, data=payload)
        invalid_attr = self.extract_error_msg(response)
        job_tracking_uri = response.headers["Location"]
        job_resp, error_msg = wait_for_idrac_job_completion(self.idrac, job_tracking_uri,
                                                            job_wait=job_wait,
                                                            wait_timeout=job_wait_timeout)

        if error_msg:
            self.module.exit_json(msg=error_msg, failed=True)
        job_resp = remove_key(job_resp.json_data, regex_pattern='(.*?)@odata')
        return job_resp, invalid_attr


class NetworkAttributes(IDRACNetworkAttributes):
    def __init__(self, idrac, module, base_uri) -> None:
        super().__init__(idrac, module, base_uri)


def perform_operation_for_main(module, obj, diff, invalid_attr):
    if diff:
        if module.check_mode:
            module.exit_json(msg=CHANGES_FOUND_MSG, changed=True)
        else:
            job_resp, invalid_attr = obj.perform_operation()
            if job_resp.get('JobState') == "Completed":
                msg = SUCCESS_MSG if not invalid_attr else VALID_AND_INVALID_ATTR_MSG
            else:
                msg = SCHEDULE_MSG
            module.exit_json(msg=msg, invalid_attributes=invalid_attr,
                             job_status=job_resp, changed=True)
    else:
        module.exit_json(msg=NO_CHANGES_FOUND_MSG, invalid_attributes=invalid_attr)


def main():
    try:
        specs = {
            "network_adapter_id": {"type": 'str', "required": True},
            "network_device_function_id": {"type": 'str', "required": True},
            "network_attributes": {"type": 'dict'},
            "oem_network_attributes": {"type": 'dict'},
            "resource_id": {"type": 'str'},
            "clear_pending": {"type": 'bool', "default": False},
            "apply_time": {"type": 'str', "required": True,
                           "choices": ['Immediate', 'OnReset', 'AtMaintenanceWindowStart', 'InMaintenanceWindowOnReset']},
            "maintenance_window": {"type": 'dict',
                                   "options": {"start_time": {"type": 'str', "required": True},
                                               "duration": {"type": 'int', "required": True}}},
            "job_wait": {"type": "bool", "default": True},
            "job_wait_timeout": {"type": "int", "default": 1200}
        }
        specs.update(idrac_auth_params)
        module = AnsibleModule(argument_spec=specs,
                            mutually_exclusive=[
                                ('network_attributes', 'oem_network_attributes')],
                            supports_check_mode=True)
        with iDRACRedfishAPI(module.params, req_session=True) as idrac:
            if module_attribute := module.params.get('oem_network_attributes'):
                    base_uri = CHASSIS_URI
                    network_attr_obj = OEMNetworkAttributes(idrac, module, base_uri)
            else:
                module_attribute = module.params.get('network_attributes')
                base_uri = SYSTEMS_URI
                network_attr_obj = NetworkAttributes(idrac, module, base_uri)
            network_attr_obj.perform_validation_for_network_adapter_id()
            network_attr_obj.perform_validation_for_network_device_function_id()
            network_attr_obj.validate_job_timeout()
            if module.params.get('oem_network_attributes') and module.params.get('clear_pending'):
                network_attr_obj.clear_pending()
            server_reg = network_attr_obj.get_current_server_registry()
            diff, invalid_attr = network_attr_obj.get_diff_between_current_and_module_input(module_attribute, server_reg)
            perform_operation_for_main(module, network_attr_obj, diff, invalid_attr)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
