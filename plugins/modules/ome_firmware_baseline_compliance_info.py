#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.1.0
# Copyright (C) 2019-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_firmware_baseline_compliance_info
short_description: Retrieves baseline compliance details on OpenManage Enterprise
version_added: "2.0.0"
description:
   - This module allows to retrieve firmware compliance for a list of devices,
     or against a specified baseline on OpenManage Enterprise.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  baseline_name:
    description:
        - Name of the baseline, for which the device compliance report is generated.
        - This option is mandatory for generating baseline based device compliance report.
        - I(baseline_name) is mutually exclusive with I(device_ids), I(device_service_tags) and I(device_group_names).
    type: str
  device_ids:
    description:
        - A list of unique identifier for device based compliance report.
        - Either I(device_ids), I(device_service_tags) or I(device_group_names)
          is required to generate device based compliance report.
        - I(device_ids) is mutually exclusive with I(device_service_tags),
          I(device_group_names) and I(baseline_name).
        - Devices without reports are ignored.
    type: list
    elements: int
  device_service_tags:
    description:
        - A list of service tags for device based compliance report.
        - Either I(device_ids), I(device_service_tags) or I(device_group_names)
          is required to generate device based compliance report.
        - I(device_service_tags) is mutually exclusive with I(device_ids),
          I(device_group_names) and I(baseline_name).
        - Devices without reports are ignored.
    type: list
    elements: str
  device_group_names:
    description:
        - A list of group names for device based compliance report.
        - Either I(device_ids), I(device_service_tags) or I(device_group_names)
          is required to generate device based compliance report.
        - I(device_group_names) is mutually exclusive with I(device_ids),
          I(device_service_tags) and I(baseline_name).
        - Devices without reports are ignored.
    type: list
    elements: str
requirements:
    - "python >= 3.8.6"
author: "Sajna Shetty(@Sajna-Shetty)"
notes:
    - Run this module from a system that has direct access to DellEMC OpenManage Enterprise.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Retrieves device based compliance report for specified device IDs
  dellemc.openmanage.ome_firmware_baseline_compliance_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_ids:
        - 11111
        - 22222

- name: Retrieves device based compliance report for specified service Tags
  dellemc.openmanage.ome_firmware_baseline_compliance_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_service_tags:
        - MXL1234
        - MXL4567

- name: Retrieves device based compliance report for specified group names
  dellemc.openmanage.ome_firmware_baseline_compliance_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_group_names:
        - "group1"
        - "group2"

- name: Retrieves device compliance report for a specified baseline
  dellemc.openmanage.ome_firmware_baseline_compliance_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    baseline_name: "baseline_name"
'''

RETURN = r'''
---
msg:
  type: str
  description: Overall baseline compliance report status.
  returned: on error
  sample: "Failed to fetch the compliance baseline information."
baseline_compliance_info:
  type: dict
  description: Details of the baseline compliance report.
  returned: success
  sample: [
            {
                "CatalogId": 53,
                "ComplianceSummary": {
                    "ComplianceStatus": "CRITICAL",
                    "NumberOfCritical": 2,
                    "NumberOfDowngrade": 0,
                    "NumberOfNormal": 0,
                    "NumberOfWarning": 0
                },
                "Description": "",
                "DeviceComplianceReports": [
                    {
                        "ComplianceStatus": "CRITICAL",
                        "ComponentComplianceReports": [
                            {
                                "ComplianceDependencies": [],
                                "ComplianceStatus": "DOWNGRADE",
                                "Criticality": "Ok",
                                "CurrentVersion": "OSC_1.1",
                                "Id": 1258,
                                "ImpactAssessment": "",
                                "Name": "OS COLLECTOR 2.1",
                                "Path": "FOLDER04118304M/2/Diagnostics_Application_JCCH7_WN64_4.0_A00_01.EXE",
                                "PrerequisiteInfo": "",
                                "RebootRequired": false,
                                "SourceName": "DCIM:INSTALLED#802__OSCollector.Embedded.1",
                                "TargetIdentifier": "101734",
                                "UniqueIdentifier": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                                "UpdateAction": "DOWNGRADE",
                                "Uri": "http://www.dell.com/support/home/us/en/19/Drivers/DriversDetails?driverId=XXXXX",
                                "Version": "4.0"
                            },
                            {
                                "ComplianceDependencies": [],
                                "ComplianceStatus": "CRITICAL",
                                "Criticality": "Recommended",
                                "CurrentVersion": "DN02",
                                "Id": 1259,
                                "ImpactAssessment": "",
                                "Name": "TOSHIBA AL14SE 1.8 TB 2.5 12Gb 10K 512n SAS HDD Drive",
                                "Path": "FOLDER04086111M/1/SAS-Drive_Firmware_VDGFM_WN64_DN03_A00.EXE",
                                "PrerequisiteInfo": "",
                                "RebootRequired": true,
                                "SourceName": "DCIM:INSTALLED#304_C_Disk.Bay.1:Enclosure.Internal.0-1:RAID.Integrated.1-1",
                                "TargetIdentifier": "103730",
                                "UniqueIdentifier": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                                "UpdateAction": "UPGRADE",
                                "Uri": "http://www.dell.com/support/home/us/en/19/Drivers/DriversDetails?driverId=XXXXX",
                                "Version": "DN03"
                            }
                        ],
                        "DeviceId": 11603,
                        "DeviceModel": "PowerEdge R630",
                        "DeviceName": null,
                        "DeviceTypeId": 1000,
                        "DeviceTypeName": "CPGCGS",
                        "FirmwareStatus": "Non-Compliant",
                        "Id": 194,
                        "RebootRequired": true,
                        "ServiceTag": "MXL1234"
                    }
                ],
                "DowngradeEnabled": true,
                "Id": 53,
                "Is64Bit": false,
                "LastRun": "2019-09-27 05:08:16.301",
                "Name": "baseline1",
                "RepositoryId": 43,
                "RepositoryName": "catalog2",
                "RepositoryType": "CIFS",
                "Targets": [
                    {
                        "Id": 11603,
                        "Type": {
                            "Id": 1000,
                            "Name": "DEVICE"
                        }
                    }
                ],
                "TaskId": 11710,
                "TaskStatusId": 0
            }
        ]
error_info:
  type: dict
  description: Details of http error.
  returned: on http error
  sample:  {
        "error": {
            "@Message.ExtendedInfo": [
                {
                    "Message": "Unable to retrieve baseline list either because the device ID(s) entered are invalid",
                    "Resolution": "Make sure the entered device ID(s) are valid and retry the operation.",
                    "Severity": "Critical"
                }
            ],
            "code": "Base.1.0.GeneralError",
            "message": "A general error has occurred. See ExtendedInfo for more information."
        }
    }
'''

import json
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


base_line_path = "UpdateService/Baselines"
baselines_report_by_device_ids_path = "UpdateService/Actions/UpdateService.GetBaselinesReportByDeviceids"
device_is_list_path = "DeviceService/Devices"
baselines_compliance_report_path = "UpdateService/Baselines({Id})/DeviceComplianceReports"
group_service_path = "GroupService/Groups"
EXIT_MESSAGE = "Unable to retrieve baseline list either because the device ID(s) entered are invalid, " \
               "the ID(s) provided are not associated with a baseline or a group is used as a target for a baseline."
MSG_ID = "CUPD3090"


def _get_device_id_from_service_tags(service_tags, rest_obj, module):
    """
    Get device ids from device service tag
    Returns :dict : device_id to service_tag map
    :arg service_tags: service tag
    :arg rest_obj: RestOME class object in case of request with session.
    :returns: dict eg: {1345:"MXL1245"}
    """
    try:
        resp = rest_obj.get_all_report_details("DeviceService/Devices")
        devices_list = resp["report_list"]
        if devices_list:
            service_tag_dict = {}
            for item in devices_list:
                if item["DeviceServiceTag"] in service_tags:
                    service_tag_dict.update({item["Id"]: item["DeviceServiceTag"]})
            return service_tag_dict
        else:
            module.exit_json(msg="Unable to fetch the device information.", baseline_compliance_info=[])
    except (URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError) as err:
        raise err


def get_device_ids_from_group_ids(module, grou_id_list, rest_obj):
    try:
        device_id_list = []
        for group_id in grou_id_list:
            group_id_path = group_service_path + "({group_id})/Devices".format(group_id=group_id)
            resp_val = rest_obj.get_all_items_with_pagination(group_id_path)
            grp_list_value = resp_val["value"]
            if grp_list_value:
                for device_item in grp_list_value:
                    device_id_list.append(device_item["Id"])
        if len(device_id_list) == 0:
            module.exit_json(msg="Unable to fetch the device ids from specified device_group_names.",
                             baseline_compliance_info=[])
        return device_id_list
    except (URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError) as err:
        raise err


def get_device_ids_from_group_names(module, rest_obj):
    try:
        grp_name_list = module.params.get("device_group_names")
        resp = rest_obj.get_all_report_details(group_service_path)
        group_id_list = []
        grp_list_resp = resp["report_list"]
        if grp_list_resp:
            for name in grp_name_list:
                for group in grp_list_resp:
                    if group["Name"] == name:
                        group_id_list.append(group['Id'])
                        break
        else:
            module.exit_json(msg="Unable to fetch the specified device_group_names.",
                             baseline_compliance_info=[])
        return get_device_ids_from_group_ids(module, group_id_list, rest_obj)
    except (URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError) as err:
        raise err


def get_identifiers(rest_obj, module):
    if module.params.get("device_ids") is not None:
        return module.params.get("device_ids"), "device_ids"
    elif module.params.get("device_group_names") is not None:
        return get_device_ids_from_group_names(module, rest_obj), "device_group_names"
    else:
        service_tags = module.params.get("device_service_tags")
        service_tags_mapper = _get_device_id_from_service_tags(service_tags, rest_obj, module)
        return list(service_tags_mapper.keys()), "device_service_tags"


def get_baseline_id_from_name(rest_obj, module):
    try:
        baseline_name = module.params.get("baseline_name")
        baseline_id = 0
        if baseline_name is not None:
            resp_val = rest_obj.get_all_items_with_pagination(base_line_path)
            baseline_list = resp_val["value"]
            if baseline_list:
                for baseline in baseline_list:
                    if baseline["Name"] == baseline_name:
                        baseline_id = baseline["Id"]
                        break
                else:
                    module.exit_json(msg="Specified baseline_name does not exist in the system.",
                                     baseline_compliance_info=[])
            else:
                module.exit_json(msg="No baseline exists in the system.", baseline_compliance_info=[])
        else:
            module.fail_json(msg="baseline_name is a mandatory option.")
        return baseline_id
    except (URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError) as err:
        raise err


def get_baselines_report_by_device_ids(rest_obj, module):
    try:
        device_ids, identifier = get_identifiers(rest_obj, module)
        if device_ids or identifier == "device_ids":
            resp = rest_obj.invoke_request('POST', baselines_report_by_device_ids_path, data={"Ids": device_ids})
            return resp.json_data
        else:
            identifier_map = {
                "device_group_names": "Device details not available as the group name(s) provided are invalid.",
                "device_service_tags": "Device details not available as the service tag(s) provided are invalid."
            }
            message = identifier_map[identifier]
            module.exit_json(msg=message)
    except HTTPError as err:
        err_message = json.load(err)
        err_list = err_message.get('error', {}).get('@Message.ExtendedInfo', [{"Message": EXIT_MESSAGE}])
        if err_list:
            err_reason = err_list[0].get("Message", EXIT_MESSAGE)
            if MSG_ID in err_list[0].get('MessageId'):
                module.exit_json(msg=err_reason)
        raise err
    except (URLError, SSLValidationError, ConnectionError, TypeError, ValueError) as err:
        raise err


def get_baseline_compliance_reports(rest_obj, module):
    try:
        baseline_id = get_baseline_id_from_name(rest_obj, module)
        path = baselines_compliance_report_path.format(Id=baseline_id)
        resp_val = rest_obj.get_all_items_with_pagination(path)
        resp_data = resp_val["value"]
        return resp_data
    except (URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError) as err:
        raise err


def validate_inputs(module):
    module_params = module.params
    device_service_tags = module_params.get("device_service_tags")
    device_group_names = module_params.get("device_group_names")
    device_ids = module_params.get("device_ids")
    baseline_name = module_params.get("baseline_name")
    if all(not identifer for identifer in [device_ids, device_service_tags, device_group_names, baseline_name]):
        module.fail_json(msg="one of the following is required: device_ids, device_service_tags, "
                             "device_group_names, baseline_name to generate device based compliance report.")


def main():
    specs = {
        "baseline_name": {"type": 'str', "required": False},
        "device_service_tags": {"required": False, "type": "list", "elements": 'str'},
        "device_ids": {"required": False, "type": "list", "elements": 'int'},
        "device_group_names": {"required": False, "type": "list", "elements": 'str'},
    }
    specs.update(ome_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[['baseline_name', 'device_service_tags', 'device_ids', 'device_group_names']],
        required_one_of=[['device_ids', 'device_service_tags', 'device_group_names', 'baseline_name']],
        supports_check_mode=True
    )
    try:
        validate_inputs(module)
        with RestOME(module.params, req_session=True) as rest_obj:
            baseline_name = module.params.get("baseline_name")
            if baseline_name is not None:
                data = get_baseline_compliance_reports(rest_obj, module)
            else:
                data = get_baselines_report_by_device_ids(rest_obj, module)
        if data:
            module.exit_json(baseline_compliance_info=data)
        else:
            module.exit_json(msg="Unable to fetch the compliance baseline information.")
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except (URLError, SSLValidationError, ConnectionError, TypeError, ValueError, SSLError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
