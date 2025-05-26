#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2023-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_network_attributes
short_description: Configures the iDRAC network attributes
version_added: "8.4.0"
description:
  - This module allows you to configure the port and partition network attributes on the network interface cards.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_x_auth_options
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
        U(https://I(idrac_ip)/redfish/v1/Systems/System.Embedded.1/NetworkAdapters/<network_adapter_id>/NetworkDeviceFunctions/
        <network_device_function_id>/Settings) and U(https://<idrac_ip>/redfish/v1/Schemas/NetworkDeviceFunction.v1_8_0.json)."
      - I(network_attributes) is mutually exclusive with I(oem_network_attributes).
  oem_network_attributes:
    type: dict
    description:
      - "The attributes must be part of the Integrated Dell Remote Access Controller Attribute Registry.
        To view the list of attributes in Attribute Registry for iDRAC9 and newer versions. For more information,
        see, U(https://I(idrac_ip)/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/<network_adapter_id>/NetworkDeviceFunctions/
        <network_device_function_id>/Oem/Dell/DellNetworkAttributes/<network_device_function_id>)
        and U(https://I(idrac_ip)/redfish/v1/Registries/NetworkAttributesRegistry_<network_device_function_id>/
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
      - This parameter allows you to clear all the pending OEM network attributes changes.
      - C(false) does not perform any operation.
      - C(true) discards any pending changes to network attributes, or if a job is in scheduled state, removes the job.
      - I(apply_time) value will be ignored and will not have any impact for I(clear_pending) operation.
      - This operation is not supported for iDRAC8.
  apply_time:
    type: str
    required: true
    description:
      - Apply time of the I(network_attributes) and I(oem_network_attributes).
      - This is applicable only to I(network_attributes) and I(oem_network_attributes).
      - C(Immediate) allows the user to immediately reboot the host and apply the changes. I(job_wait)
        is applicable. This is applicable for I(oem_network_attributes) and I(job_wait).
      - C(OnReset) allows the user to apply the changes on the next reboot of the host server.
      - C(AtMaintenanceWindowStart) allows the user to apply at the start of a maintenance window as specified
        in I(maintenance_window). A reboot job is scheduled.
      - C(InMaintenanceWindowOnReset) allows to apply after a manual reset but within the maintenance window as
        specified in I(maintenance_window).
      - This is not applicable for iDRAC8 and value will be ignored and will not have any impact for configuring I(oem_network_attributes).
      - For iDRAC10, only C(OnReset) is supported.
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
      - This is applicable when I(apply_time) is C(Immediate) for I(oem_network_attributes).
  job_wait_timeout:
    type: int
    default: 1200
    description:
      - The maximum wait time of I(job_wait) in seconds. The job is tracked only for this duration.
      - This option is applicable when I(job_wait) is C(true).
requirements:
    - "python >= 3.9.6"
author:
    - "Abhishek Sinha(@ABHISHEK-SINHA10)"
    - "Kritika Bhateja (@Kritika-Bhateja-03)"
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports both IPv4 and IPv6 address.
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Configure OEM network attributes
  dellemc.openmanage.idrac_network_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_adapter_id: "NIC.Integrated.1"
    network_device_function_id: "NIC.Integrated.1-1-1"
    apply_time: "Immediate"
    oem_network_attributes:
      BannerMessageTimeout: "4"

- name: Configure OEM network attributes to apply on reset
  dellemc.openmanage.idrac_network_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_adapter_id: NIC.Integrated.1
    network_device_function_id: "NIC.Integrated.1-1-1"
    oem_network_attributes:
      BannerMessageTimeout: "4"
    apply_time: OnReset

- name: Configure OEM network attributes to apply at maintainance window
  dellemc.openmanage.idrac_network_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_adapter_id: NIC.Integrated.1
    network_device_function_id: "NIC.Integrated.1-1-1"
    oem_network_attributes:
      BannerMessageTimeout: "4"
    apply_time: AtMaintenanceWindowStart
    maintenance_window:
      start_time: "2022-09-30T05:15:40-05:00"
      duration: 600

- name: Clearing the pending attributes
  dellemc.openmanage.idrac_network_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_adapter_id: NIC.Integrated.1
    network_device_function_id: "NIC.Integrated.1-1-1"
    apply_time: "Immediate"
    clear_pending: true

- name: Clearing the OEM pending attributes and apply the OEM network attributes
  dellemc.openmanage.idrac_network_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_adapter_id: NIC.Integrated.1
    network_device_function_id: "NIC.Integrated.1-1-1"
    apply_time: "Immediate"
    clear_pending: true
    oem_network_attributes:
      BannerMessageTimeout: "4"

- name: Configure OEM network attributes and wait for the job
  dellemc.openmanage.idrac_network_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_adapter_id: NIC.Integrated.1
    network_device_function_id: "NIC.Integrated.1-1-1"
    apply_time: "Immediate"
    oem_network_attributes:
      LnkSpeed: "10MbpsHalf"
      WakeOnLan: "Enabled"
      VLanMode: "Enabled"
    job_wait: true
    job_wait_timeout: 2000

- name: Configure redfish network attributes to update fiber channel on reset
  dellemc.openmanage.idrac_network_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_adapter_id: NIC.Integrated.1
    network_device_function_id: "NIC.Integrated.1-1-1"
    apply_time: OnReset
    network_attributes:
      Ethernet:
        VLAN:
          VLANEnable: true

- name: Configure redfish network attributes to apply on reset
  dellemc.openmanage.idrac_network_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_adapter_id: NIC.Integrated.1
    network_device_function_id: "NIC.Integrated.1-1-1"
    network_attributes:
      Ethernet:
        VLAN:
          VLANEnable: true
    apply_time: OnReset

- name: Configure redfish network attributes of iscsi to apply at maintainance window start
  dellemc.openmanage.idrac_network_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_adapter_id: NIC.Integrated.1
    network_device_function_id: "NIC.Integrated.1-1-1"
    network_attributes:
      iSCSIBoot:
        InitiatorIPAddress: 1.0.0.1
    apply_time: AtMaintenanceWindowStart
    maintenance_window:
      start_time: "2022-09-30T05:15:40-05:00"
      duration: 600

- name: Configure redfish network attributes to apply at maintainance window on reset
  dellemc.openmanage.idrac_network_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_adapter_id: NIC.Integrated.1
    network_device_function_id: "NIC.Integrated.1-1-1"
    network_attributes:
      Ethernet:
        VLAN:
          VLANEnable: false
          VLANId: 1
    apply_time: AtMaintenanceWindowStart
    maintenance_window:
      start_time: "2022-09-30T05:15:40-05:00"
      duration: 600
"""

RETURN = r'''
---
msg:
  description: Status of the attribute update operation.
  returned: when network attributes is applied
  type: str
  sample: "Successfully updated the network attributes."
invalid_attributes:
    description: Dictionary of invalid attributes provided that cannot be applied.
    returned: On invalid attributes or values
    type: dict
    sample: {
        "IscsiInitiatorIpAddr": "Attribute is not valid.",
        "IscsiInitiatorSubnet": "Attribute is not valid."
    }
job_status:
    description: Returns the output for status of the job.
    returned: always
    type: dict
    sample: {
        "ActualRunningStartTime": null,
        "ActualRunningStopTime": null,
        "CompletionTime": null,
        "Description": "Job Instance",
        "EndTime": "TIME_NA",
        "Id": "JID_XXXXXXXXX",
        "JobState": "Scheduled",
        "JobType": "NICConfiguration",
        "Message": "Task successfully scheduled.",
        "MessageArgs": [],
        "MessageId": "JCP001",
        "Name": "Configure: NIC.Integrated.1-1-1",
        "PercentComplete": 0,
        "StartTime": "2023-08-07T06:21:24",
        "TargetSettingsURI": null
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
import time
from urllib.error import HTTPError, URLError
from ansible.module_utils.compat.version import LooseVersion
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, IdracAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    delete_job, get_current_time, get_dynamic_uri,
    get_scheduled_job_resp, remove_key, validate_and_get_first_resource_id_uri,
    idrac_redfish_job_tracking, xml_data_conversion)


REGISTRY_URI = '/redfish/v1/Registries'
SYSTEMS_URI = "/redfish/v1/Systems"
iDRAC_JOB_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/{job_id}"
iDRAC_JOB_URI_10 = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/{job_id}"

SUCCESS_MSG = "Successfully updated the network attributes."
SUCCESS_CLEAR_PENDING_ATTR_MSG = "Successfully cleared the pending network attributes."
SCHEDULE_MSG = "Successfully scheduled the job for network attributes update."
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The value for the `job_wait_timeout` parameter cannot be negative or zero."
MAINTENACE_OFFSET_DIFF_MSG = "The maintenance time must be post-fixed with local offset to {0}."
MAINTENACE_OFFSET_BEHIND_MSG = "The specified maintenance time window occurs in the past, provide a future time to schedule the maintenance window."
APPLY_TIME_NOT_SUPPORTED_MSG = "Apply time {0} is not supported."
INVALID_ATTR_MSG = "Unable to update the network attributes because invalid values are entered. " + \
    "Enter the valid values for the network attributes and retry the operation."
VALID_AND_INVALID_ATTR_MSG = "Successfully updated the network attributes for valid values. " + \
    "Unable to update other attributes because invalid values are entered. Enter the valid values and retry the operation."
NO_CHANGES_FOUND_MSG = "No changes found to be applied."
CHANGES_FOUND_MSG = "Changes found to be applied."
INVALID_ID_MSG = "Unable to complete the operation because " + \
                 "the value `{0}` for the input `{1}` parameter is invalid."
JOB_RUNNING_CLEAR_PENDING_ATTR = "{0} Config job is running. Wait for the job to complete. Currently can not clear pending attributes."
ATTRIBUTE_NOT_EXIST_CHECK_IDEMPOTENCY_MODE = 'Attribute is not valid.'
CLEAR_PENDING_NOT_SUPPORTED_WITHOUT_ATTR_IDRAC8 = "Clear pending is not supported."
WAIT_TIMEOUT_MSG = "The job is not complete after {0} seconds."
HARDWARE_8 = "iDRAC 8"
ODATA_ID = "(.*?)@odata"


class IDRACNetworkAttributes:

    def __init__(self, idrac, module):
        self.module = module
        self.idrac = idrac
        self.redfish_uri = None
        self.oem_uri = None

    def validate_idrac10_and_above(self):
        gen_details = self.idrac.get_server_generation
        hw_model = gen_details[2]
        return hw_model == 'iDRAC 10'

    def get_job_uri(self):
        idrac10_or_above = self.validate_idrac10_and_above()
        if idrac10_or_above:
            return iDRAC_JOB_URI_10
        return iDRAC_JOB_URI

    def __perform_validation_for_network_adapter_id(self):
        odata = '@odata.id'
        network_adapter_id = self.module.params.get('network_adapter_id')
        network_adapter_id_uri, found_adapter = '', False
        uri, error_msg = validate_and_get_first_resource_id_uri(
            self.module, self.idrac, SYSTEMS_URI)
        if error_msg:
            self.module.exit_json(msg=error_msg, failed=True)
        network_adapters = get_dynamic_uri(
            self.idrac, uri, 'NetworkInterfaces')[odata]
        network_adapter_list = get_dynamic_uri(
            self.idrac, network_adapters, 'Members')
        for each_adapter in network_adapter_list:
            if network_adapter_id in each_adapter.get(odata):
                found_adapter = True
                network_adapter_id_uri = each_adapter.get(odata)
                break
        if not found_adapter:
            self.module.exit_json(failed=True, msg=INVALID_ID_MSG.format(network_adapter_id,
                                                                         'network_adapter_id'))
        return network_adapter_id_uri

    def __perform_validation_for_network_device_function_id(self):
        odata = '@odata.id'
        network_device_function_id_uri, found_device = '', False
        network_device_function_id = self.module.params.get(
            'network_device_function_id')
        network_adapter_id_uri = self.__perform_validation_for_network_adapter_id()
        network_devices = get_dynamic_uri(
            self.idrac, network_adapter_id_uri, 'NetworkDeviceFunctions')[odata]
        network_device_list = get_dynamic_uri(
            self.idrac, network_devices, 'Members')
        for each_device in network_device_list:
            if network_device_function_id in each_device.get(odata):
                found_device = True
                network_device_function_id_uri = each_device.get(odata)
                break
        if not found_device:
            self.module.exit_json(failed=True, msg=INVALID_ID_MSG.format(network_device_function_id,
                                                                         'network_device_function_id'))
        return network_device_function_id_uri

    def __get_registry_fw_less_than_6_more_than_3(self):
        reg = {}
        network_device_function_id = self.module.params.get(
            'network_device_function_id')
        registry = get_dynamic_uri(self.idrac, REGISTRY_URI, 'Members')
        for each_member in registry:
            if network_device_function_id in each_member.get('@odata.id'):
                location = get_dynamic_uri(
                    self.idrac, each_member.get('@odata.id'), 'Location')
                if location:
                    uri = location[0].get('Uri')
                    attr = get_dynamic_uri(
                        self.idrac, uri, 'RegistryEntries').get('Attributes', {})
                    for each_attr in attr:
                        reg.update(
                            {each_attr['AttributeName']: each_attr['CurrentValue']})
                    break
        return reg

    def __validate_time(self, mtime):
        curr_time, date_offset = get_current_time(self.idrac)
        if not mtime.endswith(date_offset):
            self.module.exit_json(
                failed=True, msg=MAINTENACE_OFFSET_DIFF_MSG.format(date_offset))
        if mtime < curr_time:
            self.module.exit_json(
                failed=True, msg=MAINTENACE_OFFSET_BEHIND_MSG)

    def __get_redfish_apply_time(self, aplytm, rf_settings):
        rf_set = {}
        if rf_settings:
            if aplytm not in rf_settings:
                self.module.exit_json(
                    failed=True, msg=APPLY_TIME_NOT_SUPPORTED_MSG.format(aplytm))
            elif 'Maintenance' in aplytm:
                rf_set['ApplyTime'] = aplytm
                m_win = self.module.params.get('maintenance_window')
                self.__validate_time(m_win.get('start_time'))
                rf_set['MaintenanceWindowStartTime'] = m_win.get('start_time')
                rf_set['MaintenanceWindowDurationInSeconds'] = m_win.get(
                    'duration')
            else:
                rf_set['ApplyTime'] = aplytm
        return rf_set

    def __get_registry_fw_less_than_3(self):
        reg = {}
        network_device_function_id = self.module.params.get(
            'network_device_function_id')
        scp_response = self.idrac.export_scp(export_format="JSON", export_use="Default",
                                             target="NIC", job_wait=True)
        comp = scp_response.json_data.get("SystemConfiguration", {}).get("Components", {})
        for each in comp:
            if each.get('FQDD') == network_device_function_id:
                for each_attr in each.get('Attributes'):
                    reg.update({each_attr['Name']: each_attr['Value']})
        return reg

    def get_current_server_registry(self):
        reg = {}
        oem_network_attributes = self.module.params.get(
            'oem_network_attributes')
        network_attributes = self.module.params.get('network_attributes')
        gen_details = self.idrac.get_server_generation
        firm_ver, hw_model = gen_details[1], gen_details[2]
        idrac_9_flag = LooseVersion(firm_ver) >= '6.0' and hw_model == "iDRAC 9"
        if oem_network_attributes:
            if idrac_9_flag or hw_model == "iDRAC 10":
                reg = get_dynamic_uri(self.idrac, self.oem_uri, 'Attributes')
            elif '3.0' < LooseVersion(firm_ver) < '6.0' and hw_model == "iDRAC 9":
                reg = self.__get_registry_fw_less_than_6_more_than_3()
            else:
                reg = self.__get_registry_fw_less_than_3()
        if network_attributes:  # For Redfish
            resp = get_dynamic_uri(self.idrac, self.redfish_uri)
            reg.update({'Ethernet': resp.get('Ethernet', {})})
            reg.update({'FibreChannel': resp.get('FibreChannel', {})})
            reg.update({'iSCSIBoot': resp.get('iSCSIBoot', {})})
        return reg

    def extract_error_msg(self, resp):
        error_info = {}
        if resp.body:
            error = resp.json_data.get('error')
            for each_dict_err in error.get("@Message.ExtendedInfo"):
                key = each_dict_err.get('MessageArgs')[0]
                msg = each_dict_err.get('Message')
                if key not in error_info:
                    error_info.update({key: msg})
        return error_info

    def get_diff_between_current_and_module_input(self, module_attr, server_attr):
        diff, invalid = 0, {}
        if module_attr is None:
            module_attr = {}
        for each_attr in module_attr:
            if each_attr in server_attr:
                data_type = type(server_attr[each_attr])
                if not isinstance(module_attr[each_attr], data_type):
                    diff += 1
                elif isinstance(module_attr[each_attr], dict) and isinstance(server_attr[each_attr], dict):
                    tmp_diff, tmp_invalid = self.get_diff_between_current_and_module_input(
                        module_attr[each_attr], server_attr[each_attr])
                    diff += tmp_diff
                    invalid.update(tmp_invalid)
                elif module_attr[each_attr] != server_attr[each_attr]:
                    diff += 1
            elif each_attr not in server_attr:
                invalid.update(
                    {each_attr: ATTRIBUTE_NOT_EXIST_CHECK_IDEMPOTENCY_MODE})
        return diff, invalid

    def validate_job_timeout(self):
        if self.module.params.get("job_wait") and self.module.params.get("job_wait_timeout") <= 0:
            self.module.exit_json(
                msg=TIMEOUT_NEGATIVE_OR_ZERO_MSG, failed=True)

    def apply_time(self, setting_uri):
        resp = get_dynamic_uri(self.idrac, setting_uri, "@Redfish.Settings")
        rf_settings = resp.get("SupportedApplyTimes", [])
        apply_time = self.module.params.get('apply_time', {})
        rf_set = self.__get_redfish_apply_time(apply_time, rf_settings)
        return rf_set

    def set_dynamic_base_uri_and_validate_ids(self):
        network_device_function_id_uri = self.__perform_validation_for_network_device_function_id()
        resp = get_dynamic_uri(self.idrac, network_device_function_id_uri)
        self.oem_uri = resp.get('Links', {}).get('Oem', {}).get(
            'Dell', {}).get('DellNetworkAttributes', {}).get('@odata.id', {})
        self.redfish_uri = network_device_function_id_uri


class OEMNetworkAttributes(IDRACNetworkAttributes):
    def __init__(self, idrac, module):
        super().__init__(idrac, module)

    def check_idrac8(self, firm_ver, hw_model, oem_network_attributes):
        if LooseVersion(firm_ver) < '3.0' and hw_model == HARDWARE_8:
            if oem_network_attributes:
                return None
            self.module.exit_json(
                msg=CLEAR_PENDING_NOT_SUPPORTED_WITHOUT_ATTR_IDRAC8)

    def clear_pending_job_track(self, job_state, job_id, oem_network_attributes, job_resp):
        if job_id:
            if job_state in ["Running"]:
                job_resp = remove_key(job_resp, regex_pattern=ODATA_ID)
                self.module.exit_json(
                    failed=True,
                    msg=JOB_RUNNING_CLEAR_PENDING_ATTR.format('NICConfiguration'),
                    job_status=job_resp
                )
            elif job_state in ["Starting", "Scheduled", "Scheduling"]:
                if self.module.check_mode and not oem_network_attributes:
                    self.module.exit_json(msg=CHANGES_FOUND_MSG, changed=True)
                if not self.module.check_mode:
                    delete_job(self.idrac, job_id)

    def clear_pending(self):
        gen_details = self.idrac.get_server_generation
        firm_ver, hw_model = gen_details[1], gen_details[2]
        oem_network_attributes = self.module.params.get(
            'oem_network_attributes')
        self.check_idrac8(firm_ver, hw_model, oem_network_attributes)
        resp = get_dynamic_uri(self.idrac, self.oem_uri, '@Redfish.Settings')
        settings_uri = resp.get('SettingsObject').get('@odata.id')
        settings_uri_resp = get_dynamic_uri(self.idrac, settings_uri)
        pending_attributes = settings_uri_resp.get('Attributes')
        clear_pending_uri = settings_uri_resp.get('Actions').get(
            '#DellManager.ClearPending').get('target')
        if not pending_attributes and not oem_network_attributes:
            self.module.exit_json(msg=NO_CHANGES_FOUND_MSG)
        job_resp = get_scheduled_job_resp(self.idrac, 'NICConfiguration')
        job_id, job_state = job_resp.get('Id'), job_resp.get('JobState')
        self.clear_pending_job_track(job_state, job_id, oem_network_attributes, job_resp)
        if self.module.check_mode and not oem_network_attributes:
            self.module.exit_json(msg=CHANGES_FOUND_MSG, changed=True)
        time.sleep(5)
        settings_uri_resp = get_dynamic_uri(self.idrac, settings_uri)
        pending_attributes = settings_uri_resp.get('Attributes')
        if pending_attributes and not self.module.check_mode:
            self.idrac.invoke_request(
                clear_pending_uri, "POST", data="{}", dump=False)
        if not oem_network_attributes:
            self.module.exit_json(
                msg=SUCCESS_CLEAR_PENDING_ATTR_MSG, changed=True)

    def perform_operation(self):
        oem_network_attributes = self.module.params.get(
            'oem_network_attributes')
        network_device_function_id = self.module.params.get(
            'network_device_function_id')
        apply_time = self.module.params.get('apply_time')
        job_wait = self.module.params.get('job_wait')
        invalid_attr = {}
        gen_details = self.idrac.get_server_generation
        firm_ver, hw_model = gen_details[1], gen_details[2]
        if LooseVersion(firm_ver) < '3.0' and hw_model == HARDWARE_8:
            root = """<SystemConfiguration>{0}</SystemConfiguration>"""
            scp_payload = root.format(xml_data_conversion(
                oem_network_attributes, network_device_function_id))
            resp = self.idrac.import_scp(
                import_buffer=scp_payload, target="NIC", job_wait=False)
        else:
            payload = {'Attributes': oem_network_attributes}
            apply_time_setting = self.apply_time(self.oem_uri)
            if apply_time_setting:
                payload.update(
                    {"@Redfish.SettingsApplyTime": apply_time_setting})
            patch_uri = get_dynamic_uri(self.idrac, self.oem_uri).get(
                '@Redfish.Settings').get('SettingsObject').get('@odata.id')
            resp = self.idrac.invoke_request(
                method='PATCH', uri=patch_uri, data=payload)
            job_wait = job_wait if apply_time == "Immediate" else False
        invalid_attr = self.extract_error_msg(resp)
        return resp, invalid_attr, job_wait


class NetworkAttributes(IDRACNetworkAttributes):
    def __init__(self, idrac, module):
        super().__init__(idrac, module)

    def perform_operation(self):
        updatable_fields = ['Ethernet', 'iSCSIBoot', 'FibreChannel']
        network_attributes = self.module.params.get('network_attributes')
        apply_time = self.module.params.get('apply_time')
        job_wait = self.module.params.get('job_wait')
        payload, invalid_attr = {}, {}
        for each_attr in network_attributes:
            if each_attr in updatable_fields:
                payload.update({each_attr: network_attributes[each_attr]})
        apply_time_setting = self.apply_time(self.redfish_uri)
        if apply_time_setting:
            payload.update({"@Redfish.SettingsApplyTime": apply_time_setting})
        resp = get_dynamic_uri(self.idrac, self.redfish_uri)
        patch_uri = resp.get(
            "@Redfish.Settings", {}).get("SettingsObject", {}).get("@odata.id", {})
        resp = self.idrac.invoke_request(
            method='PATCH', uri=patch_uri, data=payload)
        invalid_attr = self.extract_error_msg(resp)
        job_wait = job_wait if apply_time == "Immediate" else False
        return resp, invalid_attr, job_wait


def check_status_on_idrac8(idrac, module, obj, job_dict, msg):
    gen_details = idrac.get_server_generation
    firm_ver, hw_model = gen_details[1], gen_details[2]
    if LooseVersion(firm_ver) < '3.0' and isinstance(obj, OEMNetworkAttributes) and hw_model == HARDWARE_8:
        message_id = job_dict.get("MessageId")
        if message_id == "SYS053":
            module.exit_json(msg=msg, changed=True, job_status=job_dict)
        elif message_id == "SYS055":
            module.exit_json(
                msg=VALID_AND_INVALID_ATTR_MSG, changed=True, job_status=job_dict)
        elif message_id == "SYS067":
            module.fail_json(msg=INVALID_ATTR_MSG,
                             job_status=job_dict)
        else:
            module.fail_json(msg=job_dict.get("Message"))


def job_tracking_in_diff(idrac, module, obj, job_resp, invalid_attr, job_wait, job_wait_timeout):
    job_dict = {}
    if (job_tracking_uri := job_resp.headers.get("Location")):
        job_id = job_tracking_uri.split("/")[-1]
        job_uri = obj.get_job_uri().format(job_id=job_id)
        if job_wait:
            job_failed, msg, job_dict, wait_time = idrac_redfish_job_tracking(
                idrac,
                job_uri,
                max_job_wait_sec=job_wait_timeout,
                sleep_interval_secs=1
            )
            job_dict = remove_key(job_dict,
                                  regex_pattern=ODATA_ID)
            if int(wait_time) >= int(job_wait_timeout):
                module.exit_json(msg=WAIT_TIMEOUT_MSG.format(
                    job_wait_timeout), changed=True, job_status=job_dict)
            if job_failed:
                module.fail_json(
                    msg=job_dict.get("Message"), invalid_attributes=invalid_attr, job_status=job_dict)
        else:
            job_resp = idrac.invoke_request(job_uri, 'GET')
            job_dict = job_resp.json_data
            job_dict = remove_key(job_dict,
                                  regex_pattern=ODATA_ID)
    if job_dict.get('JobState') == "Completed":
        msg = SUCCESS_MSG if not invalid_attr else VALID_AND_INVALID_ATTR_MSG
        check_status_on_idrac8(idrac, module, obj, job_dict, msg)
    else:
        msg = SCHEDULE_MSG
    module.exit_json(msg=msg,
                     invalid_attributes=invalid_attr,
                     job_status=job_dict,
                     changed=True)


def perform_operation_for_main(idrac, module, obj, diff, _invalid_attr):
    job_wait_timeout = module.params.get('job_wait_timeout')
    if diff:
        if module.check_mode:
            module.exit_json(msg=CHANGES_FOUND_MSG, changed=True,
                             invalid_attributes=_invalid_attr)
        else:
            job_resp, invalid_attr, job_wait = obj.perform_operation()
            job_tracking_in_diff(idrac,
                                 module,
                                 obj,
                                 job_resp, invalid_attr, job_wait,
                                 job_wait_timeout)
    else:
        if module.check_mode:
            module.exit_json(msg=NO_CHANGES_FOUND_MSG,
                             invalid_attributes=_invalid_attr)
        # When user has given only invalid attribute, diff will 0 and _invalid_attr will have dictionary,
        elif _invalid_attr:  # Expecting HTTP Error from server.
            job_resp, invalid_attr, job_wait = obj.perform_operation()
        module.exit_json(msg=NO_CHANGES_FOUND_MSG,
                         invalid_attributes=_invalid_attr)


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

        module = IdracAnsibleModule(argument_spec=specs,
                                    mutually_exclusive=[('network_attributes', 'oem_network_attributes')],
                                    required_if=[["apply_time", "AtMaintenanceWindowStart", ("maintenance_window",)],
                                                 ["apply_time", "InMaintenanceWindowOnReset", ("maintenance_window",)]],
                                    supports_check_mode=True)
        with iDRACRedfishAPI(module.params, req_session=True) as idrac:
            if module_attribute := module.params.get('network_attributes'):
                network_attr_obj = NetworkAttributes(idrac, module)
            else:
                module_attribute = module.params.get('oem_network_attributes')
                network_attr_obj = OEMNetworkAttributes(idrac, module)
            network_attr_obj.set_dynamic_base_uri_and_validate_ids()
            network_attr_obj.validate_job_timeout()
            if module.params.get('clear_pending') and 'clear_pending' in dir(network_attr_obj):
                network_attr_obj.clear_pending()
            server_reg = network_attr_obj.get_current_server_registry()
            diff, invalid_attr = network_attr_obj.get_diff_between_current_and_module_input(
                module_attribute, server_reg)
            perform_operation_for_main(idrac,
                                       module, network_attr_obj, diff, invalid_attr)
    except HTTPError as err:
        filter_err = remove_key(json.load(err), regex_pattern=ODATA_ID)
        module.exit_json(msg=str(err), error_info=filter_err, failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
