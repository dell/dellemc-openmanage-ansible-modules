#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 6.1.0
# Copyright (C) 2021-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: ome_configuration_compliance_info
short_description: Device compliance report for devices managed in OpenManage Enterprise
version_added: "3.2.0"
description: This module allows the generation of a compliance report of a specific or all
  of devices in a configuration compliance baseline.
extends_documentation_fragment:
  - dellemc.openmanage.oment_auth_options
options:
  baseline:
    required: True
    description:
      - The name of the created baseline.
      - A compliance report is generated even when the template is not associated with the baseline.
    type: str
  device_id:
    required: False
    description:
      - The ID of the target device which is associated with the I(baseline).
    type: int
  device_service_tag:
    required: False
    description:
      - The device service tag of the target device associated with the I(baseline).
      - I(device_service_tag) is mutually exclusive with I(device_id).
    type: str
requirements:
  - "python >= 3.8.6"
author:
  - "Felix Stephen A (@felixs88)"
  - "Kritika Bhateja (@Kritika-Bhateja)"
notes:
  - Run this module from a system that has direct access to Dell OpenManage Enterprise.
  - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Retrieve the compliance report of all of the devices in the specified configuration compliance baseline.
  dellemc.openmanage.ome_configuration_compliance_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    baseline: baseline_name

- name: Retrieve the compliance report for a specific device associated with the baseline using the device ID.
  dellemc.openmanage.ome_configuration_compliance_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    baseline: baseline_name
    device_id: 10001

- name: Retrieve the compliance report for a specific device associated with the baseline using the device service tag.
  dellemc.openmanage.ome_configuration_compliance_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    baseline: baseline_name
    device_service_tag: 2HFGH3
'''

RETURN = r'''
---
msg:
  type: str
  description: Over all compliance report status.
  returned: on error
  sample: "Unable to complete the operation because the entered target baseline name 'baseline' is invalid."
compliance_info:
  type: dict
  description: Returns the compliance report information.
  returned: success
  sample: [{
    "ComplianceAttributeGroups": [{
      "Attributes": [],
      "ComplianceReason": "One or more attributes on the target device(s) does not match the compliance template.",
      "ComplianceStatus": 2,
      "ComplianceSubAttributeGroups": [{
        "Attributes": [{
          "AttributeId": 75369,
          "ComplianceReason": "Attribute has different value from template",
          "ComplianceStatus": 3,
          "CustomId": 0,
          "Description": null,
          "DisplayName": "Workload Profile",
          "ExpectedValue": "HpcProfile",
          "Value": "NotAvailable"
          }],
        "ComplianceReason": "One or more attributes on the target device(s) does not match the compliance template.",
        "ComplianceStatus": 2,
        "ComplianceSubAttributeGroups": [],
        "DisplayName": "System Profile Settings",
        "GroupNameId": 1
      }],
      "DisplayName": "BIOS",
      "GroupNameId": 1
    }],
    "ComplianceStatus": "NONCOMPLIANT",
    "DeviceName": "WIN-PLOV8MPIP40",
    "DeviceType": 1000,
    "Id": 25011,
    "InventoryTime": "2021-03-18 00:01:57.809771",
    "Model": "PowerEdge R7525",
    "ServiceTag": "JHMBX53"
  }]
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
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError

BASELINE_URI = "TemplateService/Baselines"
CONFIG_COMPLIANCE_URI = "TemplateService/Baselines({0})/DeviceConfigComplianceReports"
COMPLIANCE_URI = "TemplateService/Baselines({0})/DeviceConfigComplianceReports({1})/DeviceComplianceDetails"


def validate_device(module, report, device_id=None, service_tag=None, base_id=None):
    for each in report.get("value"):
        if each["Id"] == device_id:
            break
        if each["ServiceTag"] == service_tag:
            device_id = each["Id"]
            break
    else:
        device_name = device_id if device_id is not None else service_tag
        module.fail_json(msg="Unable to complete the operation because the entered "
                             "target device id or service tag '{0}' is invalid.".format(device_name))
    return device_id


def get_baseline_id(module, baseline_name, rest_obj):
    report = rest_obj.get_all_report_details(BASELINE_URI)
    base_id, template_id = None, None
    for base in report["report_list"]:
        if base["Name"] == baseline_name:
            base_id = base["Id"]
            template_id = base["TemplateId"]
            break
    else:
        module.fail_json(msg="Unable to complete the operation because the entered "
                             "target baseline name '{0}' is invalid.".format(baseline_name))
    return base_id, template_id


def compliance_report(module, rest_obj):
    baseline_name = module.params.get("baseline")
    device_id = module.params.get("device_id")
    device_service_tag = module.params.get("device_service_tag")
    baseline_id, template_id = get_baseline_id(module, baseline_name, rest_obj)
    report = []
    if device_id:
        compliance_uri = COMPLIANCE_URI.format(baseline_id, device_id)
        baseline_report = rest_obj.invoke_request("GET", compliance_uri)
        if not baseline_report.json_data.get("ComplianceAttributeGroups") and template_id == 0:
            module.fail_json(msg="The compliance report of the device not found as "
                                 "there is no template associated with the baseline.")
        device_compliance = baseline_report.json_data.get("ComplianceAttributeGroups")
    else:
        baseline_report = rest_obj.get_all_items_with_pagination(CONFIG_COMPLIANCE_URI.format(baseline_id))
        if device_service_tag:
            device_id = validate_device(module, baseline_report, device_id=device_id,
                                        service_tag=device_service_tag, base_id=baseline_id)
            report = list(filter(lambda d: d['Id'] in [device_id], baseline_report.get("value")))
        else:
            report = baseline_report.get("value")
        device_compliance = report
        if device_compliance:
            for each in device_compliance:
                compliance_uri = COMPLIANCE_URI.format(baseline_id, each["Id"])
                attr_group = rest_obj.invoke_request("GET", compliance_uri)
                each["ComplianceAttributeGroups"] = attr_group.json_data.get("ComplianceAttributeGroups")
    return device_compliance


def main():
    specs = {
        "baseline": {"required": True, "type": "str"},
        "device_id": {"required": False, "type": "int"},
        "device_service_tag": {"required": False, "type": "str"},
    }
    specs.update(ome_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[["device_id", "device_service_tag"]],
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            report = compliance_report(module, rest_obj)
            module.exit_json(compliance_info=report)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, TypeError, SSLError, ConnectionError, SSLValidationError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
