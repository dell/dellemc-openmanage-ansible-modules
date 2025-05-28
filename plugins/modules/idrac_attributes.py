#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.1
# Copyright (C) 2022-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: idrac_attributes
short_description: Configure the iDRAC attributes.
version_added: "6.0.0"
description:
  - This module allows to configure the iDRAC attributes.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_x_auth_options
options:
  idrac_attributes:
    type: dict
    description:
      - "Dictionary of iDRAC attributes and value. The attributes should be
      part of the Integrated Dell Remote Access Controller Attribute Registry.
      To view the list of attributes in Attribute Registry for iDRAC9 and above,
      see, U(https://I(idrac_ip)/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/iDRAC.Embedded.1)
      and U(https://I(idrac_ip)/redfish/v1/Registries/ManagerAttributeRegistry)."
      - "For iDRAC8 based servers, derive the manager attribute name from Server Configuration Profile.
      If the manager attribute name in Server Configuration Profile is <GroupName>.<Instance>#<AttributeName>
      (for Example, 'SNMP.1#AgentCommunity') then the equivalent attribute name for Redfish is
      <GroupName>.<Instance>.<AttributeName> (for Example, 'SNMP.1.AgentCommunity')."
  system_attributes:
    type: dict
    description:
      - "Dictionary of System attributes and value. The attributes should be
      part of the Integrated Dell Remote Access Controller Attribute Registry. To view the list of attributes in Attribute Registry for iDRAC9 and above,
      see, U(https://I(idrac_ip)/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/System.Embedded.1)
      and U(https://I(idrac_ip)/redfish/v1/Registries/ManagerAttributeRegistry)."
      - "For iDRAC8 based servers, derive the manager attribute name from Server Configuration Profile.
      If the manager attribute name in Server Configuration Profile is <GroupName>.<Instance>#<AttributeName>
      (for Example, 'ThermalSettings.1#ThermalProfile') then the equivalent attribute name for Redfish is
      <GroupName>.<Instance>.<AttributeName> (for Example, 'ThermalSettings.1.ThermalProfile')."
  lifecycle_controller_attributes:
    type: dict
    description:
      - "Dictionary of Lifecycle Controller attributes and value. The attributes should be
      part of the Integrated Dell Remote Access Controller Attribute Registry.To view the list of attributes in Attribute Registry for iDRAC9 and above,
      see, U(https://I(idrac_ip)/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/LifecycleController.Embedded.1)
      and U(https://I(idrac_ip)/redfish/v1/Registries/ManagerAttributeRegistry)."
      - "For iDRAC8 based servers, derive the manager attribute name from Server Configuration Profile.
      If the manager attribute name in Server Configuration Profile is <GroupName>.<Instance>#<AttributeName>
      (for Example, 'LCAttributes.1#AutoUpdate') then the equivalent attribute name for Redfish is
      <GroupName>.<Instance>.<AttributeName> (for Example, 'LCAttributes.1.AutoUpdate')."
  resource_id:
    type: str
    description: Redfish ID of the resource.
requirements:
  - "python >= 3.9.6"
author:
  - Husniya Abdul Hameed (@husniya-hameed)
  - Felix Stephen (@felixs88)
notes:
  - Run this module from a system that has direct access to Dell iDRAC.
  - This module supports C(check_mode).
  - For iDRAC8 based servers, the value provided for the attributes are not be validated.
    Ensure appropriate values are passed.
'''

EXAMPLES = """
---
- name: Configure iDRAC attributes
  dellemc.openmanage.idrac_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    idrac_attributes:
      SNMP.1.AgentCommunity: public

- name: Configure System attributes
  dellemc.openmanage.idrac_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    system_attributes:
      ThermalSettings.1.ThermalProfile: Sound Cap

- name: Configure Lifecycle Controller attributes
  dellemc.openmanage.idrac_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    lifecycle_controller_attributes:
      LCAttributes.1.AutoUpdate: Enabled

- name: Configure the iDRAC attributes for email alert settings.
  dellemc.openmanage.idrac_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    idrac_attributes:
      EmailAlert.1.CustomMsg: Display Message
      EmailAlert.1.Enable: Enabled
      EmailAlert.1.Address: test@test.com

- name: Configure the iDRAC attributes for SNMP alert settings.
  dellemc.openmanage.idrac_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    idrac_attributes:
      SNMPAlert.1.Destination: 192.168.0.2
      SNMPAlert.1.State: Enabled
      SNMPAlert.1.SNMPv3Username: username

- name: Configure the iDRAC attributes for SMTP alert settings.
  dellemc.openmanage.idrac_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    idrac_attributes:
      RemoteHosts.1.SMTPServerIPAddress: 192.168.0.3
      RemoteHosts.1.SMTPAuthentication: Enabled
      RemoteHosts.1.SMTPPort: 25
      RemoteHosts.1.SMTPUserName: username
      RemoteHosts.1.SMTPPassword: password

- name: Configure the iDRAC attributes for webserver settings.
  dellemc.openmanage.idrac_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    idrac_attributes:
      WebServer.1.SSLEncryptionBitLength: 128-Bit or higher
      WebServer.1.TLSProtocol: TLS 1.1 and Higher

- name: Configure the iDRAC attributes for SNMP settings.
  dellemc.openmanage.idrac_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    idrac_attributes:
      SNMP.1.SNMPProtocol: All
      SNMP.1.AgentEnable: Enabled
      SNMP.1.TrapFormat: SNMPv1
      SNMP.1.AlertPort: 162
      SNMP.1.AgentCommunity: public

- name: Configure the iDRAC LC attributes for collecting system inventory.
  dellemc.openmanage.idrac_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    lifecycle_controller_attributes:
      LCAttributes.1.CollectSystemInventoryOnRestart: Enabled

- name: Configure the iDRAC system attributes for LCD configuration.
  dellemc.openmanage.idrac_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    system_attributes:
      LCD.1.Configuration: Service Tag
      LCD.1.vConsoleIndication: Enabled
      LCD.1.FrontPanelLocking: Full-Access
      LCD.1.UserDefinedString: custom string

- name: Configure the iDRAC attributes for Timezone settings.
  dellemc.openmanage.idrac_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    idrac_attributes:
      Time.1.Timezone: CST6CDT
      NTPConfigGroup.1.NTPEnable: Enabled
      NTPConfigGroup.1.NTP1: 192.168.0.5
      NTPConfigGroup.1.NTP2: 192.168.0.6
      NTPConfigGroup.1.NTP3: 192.168.0.7

- name: Configure all attributes
  dellemc.openmanage.idrac_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    idrac_attributes:
      SNMP.1.AgentCommunity: test
      SNMP.1.AgentEnable: Enabled
      SNMP.1.DiscoveryPort: 161
    system_attributes:
      ServerOS.1.HostName: demohostname
    lifecycle_controller_attributes:
      LCAttributes.1.AutoUpdate: Disabled

- name: Enable idrac basic syslog
  dellemc.openmanage.idrac_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    idrac_attributes:
      SysLog.1.SysLogEnable: Enabled
      SysLog.1.Server1: 192.168.0.2
      SysLog.1.Server2: 192.168.0.3
      SysLog.1.Server3: 192.168.0.4
      SysLog.1.Port: 514

- name: Disable idrac basic syslog
  dellemc.openmanage.idrac_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    idrac_attributes:
      SysLog.1.SysLogEnable: Disabled

- name: Enable idrac secure syslog
  dellemc.openmanage.idrac_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    idrac_attributes:
      SysLog.1.securesyslogenable: Enabled
      SysLog.1.secureserver1: 192.168.0.2
      SysLog.1.secureport: 6511
      SysLog.1.secureclientauth: Anonymous

- name: Disable idrac secure syslog
  dellemc.openmanage.idrac_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    idrac_attributes:
      SysLog.1.securesyslogenable: Disabled
"""

RETURN = r'''
---
msg:
  type: str
  description: Status of the attribute update operation.
  returned: always
  sample: "Successfully updated the attributes."
invalid_attributes:
  type: dict
  description: Dict of invalid attributes provided.
  returned: on invalid attributes or values.
  sample: {
        "LCAttributes.1.AutoUpdate": "Invalid value for Enumeration.",
        "LCAttributes.1.StorageHealthRollupStatus": "Read only Attribute cannot be modified.",
        "SNMP.1.AlertPort": "Not a valid integer.",
        "SNMP.1.AlertPorty": "Attribute does not exist.",
        "SysLog.1.PowerLogInterval": "Integer out of valid range.",
        "ThermalSettings.1.AirExhaustTemp": "Invalid value for Enumeration."
    }
error_info:
  description: Error information of the operation.
  returned: when attribute value is invalid.
  type: dict
  sample: {
    "error": {
      "@Message.ExtendedInfo": [
        {
          "Message": "The value 'false' for the property LCAttributes.1.BIOSRTDRequested is of a different type than the property can accept.",
          "MessageArgs": [
            "false",
            "LCAttributes.1.BIOSRTDRequested"
          ],
          "MessageArgs@odata.count": 2,
          "MessageId": "Base.1.12.PropertyValueTypeError",
          "RelatedProperties": [
            "#/Attributes/LCAttributes.1.BIOSRTDRequested"
          ],
          "RelatedProperties@odata.count": 1,
          "Resolution": "Correct the value for the property in the request body and resubmit the request if the operation failed.",
          "Severity": "Warning"
        }
      ],
      "code": "Base.1.12.GeneralError",
      "message": "A general error has occurred. See ExtendedInfo for more information"
    }
  }
'''

import json
import re
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, IdracAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import get_manager_res_id


SUCCESS_MSG = "Successfully updated the attributes."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_MSG = "Changes found to be applied."
ATTR_FAIL_MSG = "Application of some of the attributes failed due to invalid value or enumeration."
SYSTEM_ID = "System.Embedded.1"
MANAGER_ID = "iDRAC.Embedded.1"
LC_ID = "LifecycleController.Embedded.1"
MANAGERS_URI = "/redfish/v1/Managers"
ATTR = "Attributes"
JOB_URI = "/redfish/v1/Managers/{manager_id}/Jobs/{job_id}"


def xml_data_conversion(attrbite, fqdd=None):
    component = """<Component FQDD="{0}">{1}</Component>"""
    attr = ""
    json_data = {}
    for k, v in attrbite.items():
        key = re.sub(r"\.(?!\d)", "#", k)
        attr += '<Attribute Name="{0}">{1}</Attribute>'.format(key, v)
        json_data[key] = str(v)
    root = component.format(fqdd, attr)
    return root, json_data


def validate_attr_name(attribute, req_data):
    invalid_attr = {}
    data_dict = {attr["Name"]: attr["Value"] for attr in attribute if attr["Name"] in req_data.keys()}
    if not len(data_dict) == len(req_data):
        for key in req_data.keys():
            if key not in data_dict:
                act_key = key.replace("#", ".")
                invalid_attr[act_key] = "Attribute does not exist."
    return data_dict, invalid_attr


def get_check_mode(module, idrac, idrac_json, sys_json, lc_json):
    scp_response = idrac.export_scp(export_format="JSON", export_use="Default",
                                    target="iDRAC,System,LifecycleController", job_wait=True)
    comp = scp_response.json_data["SystemConfiguration"]["Components"]
    exist_idrac, exist_sys, exist_lc, invalid = {}, {}, {}, {}
    for cmp in comp:
        if idrac_json and cmp.get("FQDD") == MANAGER_ID:
            exist_idrac, invalid_attr = validate_attr_name(cmp["Attributes"], idrac_json)
            if invalid_attr:
                invalid.update(invalid_attr)
        if sys_json and cmp.get("FQDD") == SYSTEM_ID:
            exist_sys, invalid_attr = validate_attr_name(cmp["Attributes"], sys_json)
            if invalid_attr:
                invalid.update(invalid_attr)
        if lc_json and cmp.get("FQDD") == LC_ID:
            exist_lc, invalid_attr = validate_attr_name(cmp["Attributes"], lc_json)
            if invalid_attr:
                invalid.update(invalid_attr)
    if invalid:
        module.fail_json(msg="Attributes have invalid values.", invalid_attributes=invalid)
    diff_change = [bool(set(exist_idrac.items()) ^ set(idrac_json.items())) or
                   bool(set(exist_sys.items()) ^ set(sys_json.items())) or
                   bool(set(exist_lc.items()) ^ set(lc_json.items()))]
    if module.check_mode and any(diff_change) is True:
        module.exit_json(msg=CHANGES_MSG, changed=True)
    elif (module.check_mode and all(diff_change) is False) or \
            (not module.check_mode and all(diff_change) is False):
        module.exit_json(msg=NO_CHANGES_MSG)


def scp_idrac_attributes(module, idrac, res_id):
    job_wait = module.params.get("job_wait", True)
    idrac_attr = module.params.get("idrac_attributes")
    system_attr = module.params.get("system_attributes")
    lc_attr = module.params.get("lifecycle_controller_attributes")
    root = """<SystemConfiguration>{0}</SystemConfiguration>"""
    component = ""
    idrac_json_data, system_json_data, lc_json_data = {}, {}, {}
    if idrac_attr is not None:
        idrac_xml_payload, idrac_json_data = xml_data_conversion(idrac_attr, fqdd=MANAGER_ID)
        component += idrac_xml_payload
    if system_attr is not None:
        system_xml_payload, system_json_data = xml_data_conversion(system_attr, fqdd=SYSTEM_ID)
        component += system_xml_payload
    if lc_attr is not None:
        lc_xml_payload, lc_json_data = xml_data_conversion(lc_attr, fqdd=LC_ID)
        component += lc_xml_payload
    get_check_mode(module, idrac, idrac_json_data, system_json_data, lc_json_data,)
    payload = root.format(component)
    resp = idrac.import_scp(import_buffer=payload, target="ALL", job_wait=False)
    job_id = resp.headers["Location"].split("/")[-1]
    job_uri = JOB_URI.format(manager_id=res_id, job_id=job_id)
    job_resp = idrac.wait_for_job_completion(job_uri, job_wait=job_wait)
    return job_resp


def get_response_attr(idrac, idrac_id, attr, uri_dict):
    response_attr = {}
    diff = 0
    response = idrac.invoke_request(uri_dict.get(idrac_id), "GET")
    for k in attr.keys():
        if response.json_data[ATTR].get(k) != attr.get(k):
            # response_attr[k] = response.json_data[ATTR].get(k)
            response_attr[k] = attr.get(k)
            diff += 1
    return diff, response_attr


def get_attributes_registry(idrac):
    reggy = {}
    try:
        resp = idrac.invoke_request("/redfish/v1/Registries/ManagerAttributeRegistry", "GET")
        loc_list = resp.json_data.get("Location", [])
        if loc_list:
            reg_json_uri = loc_list[-1].get("Uri")
            reg_resp = idrac.invoke_request(reg_json_uri, "GET")
            attr_list = reg_resp.json_data.get("RegistryEntries").get("Attributes")
            reggy = dict((x["AttributeName"], x) for x in attr_list)
    except Exception:
        reggy = {}
    return reggy


def validate_vs_registry(registry, attr_dict):
    invalid = {}
    for k, v in attr_dict.items():
        if k in registry:
            val_dict = registry.get(k)
            if val_dict.get("Readonly"):
                invalid[k] = "Read only Attribute cannot be modified."
            else:
                type = val_dict.get("Type")
                if type == "Enumeration":
                    found = False
                    for val in val_dict.get("Value", []):
                        if v == val.get("ValueDisplayName"):
                            found = True
                            break
                    if not found:
                        invalid[k] = "Invalid value for Enumeration."
                if type == "Integer":
                    try:
                        i = int(v)
                    except Exception:
                        invalid[k] = "Not a valid integer."
                    else:
                        if not (val_dict.get("LowerBound") <= i <= val_dict.get("UpperBound")):
                            invalid[k] = "Integer out of valid range."
        else:
            invalid[k] = "Attribute does not exist."
    return invalid


def fetch_idrac_uri_attr(idrac, module, res_id):
    diff = 0
    uri_dict = {}
    idrac_response_attr = {}
    system_response_attr = {}
    lc_response_attr = {}
    response = idrac.invoke_request("{0}/{1}".format(MANAGERS_URI, res_id), "GET")
    dell_attributes = response.json_data.get('Links', {}).get('Oem', {}).get('Dell', {}).get('DellAttributes')
    if dell_attributes:
        for item in dell_attributes:
            uri = item.get('@odata.id')
            attr_id = uri.split("/")[-1]
            uri_dict[attr_id] = uri
        idrac_attr = module.params.get("idrac_attributes")
        system_attr = module.params.get("system_attributes")
        lc_attr = module.params.get("lifecycle_controller_attributes")
        invalid = {}
        attr_registry = get_attributes_registry(idrac)
        if idrac_attr is not None:
            x, idrac_response_attr = get_response_attr(idrac, MANAGER_ID, idrac_attr, uri_dict)
            invalid.update(validate_vs_registry(attr_registry, idrac_response_attr))
            diff += x
        if system_attr is not None:
            x, system_response_attr = get_response_attr(idrac, SYSTEM_ID, system_attr, uri_dict)
            invalid.update(validate_vs_registry(attr_registry, system_response_attr))
            diff += x
        if lc_attr is not None:
            x, lc_response_attr = get_response_attr(idrac, LC_ID, lc_attr, uri_dict)
            invalid.update(validate_vs_registry(attr_registry, lc_response_attr))
            diff += x
        if invalid:
            module.exit_json(failed=True, msg="Attributes have invalid values.", invalid_attributes=invalid)
    else:
        job_resp = scp_idrac_attributes(module, idrac, res_id)
        if job_resp.status_code == 200:
            error_msg = ["Unable to complete application of configuration profile values.",
                         "Import of Server Configuration Profile operation completed with errors."]
            message = job_resp.json_data["Message"]
            message_id = job_resp.json_data["MessageId"]
            if message_id == "SYS069":
                module.exit_json(msg=NO_CHANGES_MSG)
            elif message_id == "SYS053":
                module.exit_json(msg=SUCCESS_MSG, changed=True)
            elif message in error_msg:
                module.fail_json(msg=ATTR_FAIL_MSG)
            else:
                module.fail_json(msg=message)
    return diff, uri_dict, idrac_response_attr, system_response_attr, lc_response_attr


def process_check_mode(module, diff):
    if not diff:
        module.exit_json(msg=NO_CHANGES_MSG)
    elif diff and module.check_mode:
        module.exit_json(msg=CHANGES_MSG, changed=True)


def update_idrac_attributes(idrac, module, uri_dict, idrac_response_attr, system_response_attr, lc_response_attr):
    resp = {}
    idrac_payload = module.params.get("idrac_attributes")
    system_payload = module.params.get("system_attributes")
    lc_payload = module.params.get("lifecycle_controller_attributes")
    if idrac_payload is not None and idrac_response_attr is not None:
        idrac_response = idrac.invoke_request(uri_dict.get(MANAGER_ID), "PATCH", data={ATTR: idrac_payload})
        resp["iDRAC"] = idrac_response.json_data
    if system_payload is not None and system_response_attr is not None:
        system_response = idrac.invoke_request(uri_dict.get(SYSTEM_ID), "PATCH", data={ATTR: system_payload})
        resp["System"] = system_response.json_data
    if lc_payload is not None and lc_response_attr is not None:
        lc_response = idrac.invoke_request(uri_dict.get(LC_ID), "PATCH", data={ATTR: lc_payload})
        resp["Lifecycle Controller"] = lc_response.json_data
    return resp


def main():
    specs = {
        "idrac_attributes": {"required": False, "type": 'dict'},
        "system_attributes": {"required": False, "type": 'dict'},
        "lifecycle_controller_attributes": {"required": False, "type": 'dict'},
        "resource_id": {"required": False, "type": 'str'}
    }

    module = IdracAnsibleModule(
        argument_spec=specs,
        required_one_of=[('idrac_attributes', 'system_attributes', 'lifecycle_controller_attributes')],
        supports_check_mode=True
    )
    try:
        with iDRACRedfishAPI(module.params, req_session=True) as idrac:
            res_id = module.params.get('resource_id')
            if not res_id:
                res_id = get_manager_res_id(idrac)
            diff, uri_dict, idrac_response_attr, system_response_attr, lc_response_attr = fetch_idrac_uri_attr(idrac, module, res_id)
            process_check_mode(module, diff)
            update_idrac_attributes(idrac, module, uri_dict, idrac_response_attr, system_response_attr, lc_response_attr)
            module.exit_json(msg=SUCCESS_MSG, changed=True)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, TypeError, ConnectionError, AttributeError, IndexError, KeyError) as err:
        module.fail_json(msg=str(err), error_info=json.load(err))


if __name__ == '__main__':
    main()
