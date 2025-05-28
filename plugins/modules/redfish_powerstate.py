#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.5.0
# Copyright (C) 2020-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: redfish_powerstate
short_description: Manage device power state
version_added: "2.1.0"
description:
  - This module allows to manage the different power states of the specified device.
extends_documentation_fragment:
  - dellemc.openmanage.redfish_auth_options
options:
  resource_id:
    description:
      - This option is the unique identifier of the device being managed. For example, U(https://<I(baseuri)>/redfish/v1/Systems/<I(resource_id)>).
      - This option is mandatory for I(base_uri) with multiple devices.
      - To get the device details, use the API U(https://<I(baseuri)>/redfish/v1/Systems) for reset_type operation and
        U(https://<I(baseuri)>/redfish/v1/Chassis) for oem_reset_type operation.
    required:  false
    type: str
  reset_type:
    description:
      - This option resets the device.
      - C(ForceOff) turns off the device immediately.
      - C(ForceOn) turns on the device immediately.
      - C(ForceRestart) turns off the device immediately, and then restarts the server.
      - C(GracefulRestart) performs graceful shutdown of the device, and then restarts the device.
      - C(GracefulShutdown) performs a graceful shutdown of the device, and then turns off the device.
      - C(Nmi) sends a diagnostic interrupt to the device. This option is usually a nonmaskable interrupt (NMI) on x86 systems.
      - C(On) turns on the device.
      - C(PowerCycle) performs a power cycle on the device.
      - C(PushPowerButton) simulates the pressing of a physical power button on the device.
      - I(reset_type) is mutually exclusive with I(oem_reset_type).
      - When a power control operation is performed, which is not supported on the device, an error message is displayed
       with the list of operations that can be performed.
    required:  false
    type: str
    choices: ["ForceOff", "ForceOn", "ForceRestart", "GracefulRestart", "GracefulShutdown",
               "Nmi", "On", "PowerCycle", "PushPowerButton"]
  oem_reset_type:
    description:
      - This parameter initiates a complete Alternate Current (AC) power cycle of the server which is equivalent to disconnecting power cables using OEM API.
      - I(oem_reset_type) is mutually exclusive with I(reset_type).
      - If the value of 'final_power_state' is not provided, the default value is 'Off'.
    required:  false
    type: dict
    version_added: 9.5.0
requirements:
    - "python >= 3.9.6"
author:
    - "Sajna Shetty(@Sajna-Shetty)"
    - "Lovepreet Singh (@singh-lovepreet1)"
notes:
    - Run this module from a system that has direct access to Redfish APIs.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Manage power state of the first device
  dellemc.openmanage.redfish_powerstate:
    baseuri: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    reset_type: "On"

- name: Manage power state of a specified device
  dellemc.openmanage.redfish_powerstate:
    baseuri: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    reset_type: "ForceOff"
    resource_id: "System.Embedded.1"

- name: Perform AC Power Cycle with final power state On
  dellemc.openmanage.redfish_powerstate:
    baseuri: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    oem_reset_type:
      dell:
        final_power_state: "On"
        reset_type: "PowerCycle"

- name: Perform AC Power Cycle  with final power state Off
  dellemc.openmanage.redfish_powerstate:
    baseuri: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    oem_reset_type:
      dell:
        final_power_state: "Off"
        reset_type: "PowerCycle"
'''

RETURN = r'''
---
msg:
  description: Overall status of the reset operation.
  returned: always
  type: str
  sample: "Successfully performed the reset type operation 'On'."
error_info:
  type: dict
  description: Details of the HTTP error.
  returned: on http error
  sample:  {
    "error": {
        "@Message.ExtendedInfo": [
            {
                "Message": "Unable to complete the operation because the resource
                 /redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset entered in not found.",
                "MessageArgs": [
                    "/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset"
                ],
                "MessageArgs@odata.count": 1,
                "MessageId": "IDRAC.2.1.SYS403",
                "RelatedProperties": [],
                "RelatedProperties@odata.count": 0,
                "Resolution": "Enter the correct resource and retry the operation.
                 For information about valid resource,
                 see the Redfish Users Guide available on the support site.",
                "Severity": "Critical"
            },
        ],
        "code": "Base.1.5.GeneralError",
        "message": "A general error has occurred. See ExtendedInfo for more information"
    }
}
'''

import json
import re
from ssl import SSLError
from ansible.module_utils.compat.version import LooseVersion
from ansible_collections.dellemc.openmanage.plugins.module_utils.redfish import Redfish, RedfishAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError


CHANGES_FOUND = "Changes found to be applied."
NO_CHANGES_FOUND = "No Changes found to be applied."
FIRM_VER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1?$select=FirmwareVersion"
INVALID_RESET_TYPE_OEM = "'{option}' is not supported. The supported values" \
    " are {supported_oem_reset_type_values}. Enter the valid values and retry" \
    " the operation."
TARGET_DEVICE_NOT_SUPPORTED = "The target device does not support the system reset feature using Redfish API."
INVALID_DEVICE_ID = "Invalid device Id '{0}' is provided"
MINIMUM_SUPPORTED_FIRMWARE_VERSION = "7.00.60"
UNSUPPORTED_FIRMWARE_MSG = "Unable to perform the Virtual AC power-cycle" \
    " operation because the firmware version is not supported. The minimum" \
    " supported firmware version is '{minimum_supported_firmware_version}'."
INITIAL_DESIRED_STATE_ERROR = "No changes found to be applied because system is in power ON state."
VENDOR_NOT_SUPPORTED = "The vendor is not supported. The supported vendors" \
    " are '{supported_vendors}'. Enter the valid vendor and retry the operation."
SUCCESS_AC_MSG = "Successfully performed the full virtual server AC power-cycle operation."
SUCCESS_AC_MSG_ON = "Successfully performed the full virtual server AC power-cycle operation." \
    " Please wait a few minutes, the server will automatically power on."
INVALID_RESET_TYPE = "The target device does not support a {0} operation.The acceptable values for device reset types are {1}."
OEM_RESET_KEY = '#{0}OemChassis.ExtendedReset'
INVALID_PWR_ERROR = "The target device does not support '{0}' operation. The valid values of final power states for device are '{1}'."
VENDOR_NOT_SPECIFIED = "The vendor is not specified. Enter the valid vendor and retry the operation."
OPERATION_ERROR = "No reset type is specified for the target device. Enter the valid value and retry the operation."
powerstate_map = {}


def fetch_powerstate_details(system_res_data, action_data):
    current_state = system_res_data["PowerState"]
    power_uri = action_data['#ComputerSystem.Reset']['target']
    allowable_enums = action_data['#ComputerSystem.Reset']['ResetType@Redfish.AllowableValues']
    powerstate_map.update(
        {'power_uri': power_uri, 'allowable_enums': allowable_enums, 'current_state': current_state})


def fetch_ac_powerstate_details(module, system_id_res_data, action_id_res):
    current_state = system_id_res_data.get("PowerState")
    oem_reset_type = module.params["oem_reset_type"]
    current_vendor = next(iter(oem_reset_type), None)
    oem_key_resp = action_id_res.get('Oem')
    if oem_key_resp is None:
        module.exit_json(msg=TARGET_DEVICE_NOT_SUPPORTED, skipped=True)
    sub_key = OEM_RESET_KEY.format(current_vendor.capitalize())
    sub_oem_key = None
    if oem_key_resp is not None:
        sub_oem_key = oem_key_resp.get(sub_key)
    if sub_oem_key is None:
        module.exit_json(msg=TARGET_DEVICE_NOT_SUPPORTED, skipped=True)
    power_uri = None
    allowable_enums = None
    allowable_final_power_state = None
    if sub_oem_key is not None:
        power_uri = sub_oem_key.get('target')
        allowable_enums = sub_oem_key.get('ResetType@Redfish.AllowableValues')
        allowable_final_power_state = sub_oem_key.get('FinalPowerState@Redfish.AllowableValues')
    powerstate_map.update(
        {'power_uri': power_uri, 'allowable_enums': allowable_enums,
            'current_state': current_state, 'allowable_power_state': allowable_final_power_state})


def perform_uri_fetch(session_obj, module, system_id_res, resource_id_list, resource_id):
    reset_type = module.params.get("reset_type")
    if system_id_res in resource_id_list:
        system_id_res_resp = session_obj.invoke_request("GET", system_id_res)
        system_id_res_data = system_id_res_resp.json_data
        action_id_res = system_id_res_data.get("Actions")
        if action_id_res:
            if reset_type:
                fetch_powerstate_details(system_id_res_data, action_id_res)
            else:
                fetch_ac_powerstate_details(module, system_id_res_data, action_id_res)
        else:
            module.exit_json(msg=TARGET_DEVICE_NOT_SUPPORTED, skipped=True)
    else:
        module.exit_json(msg=INVALID_DEVICE_ID.format(resource_id), skipped=True)


def fetch_power_uri_resource(module, session_obj, reset_type_map=None):
    try:
        resource_id = module.params.get("resource_id")
        static_resource_id_resource = None
        if resource_id:
            static_resource_id_resource = "{0}{1}{2}".format(session_obj.root_uri, reset_type_map + "/", resource_id)
        system_uri = "{0}{1}".format(session_obj.root_uri, reset_type_map)
        system_resp = session_obj.invoke_request("GET", system_uri)
        system_members = system_resp.json_data.get("Members")
        if system_members and len(system_members) > 0:
            resource_id_list = [system_id["@odata.id"] for system_id in system_members if "@odata.id" in system_id]
            system_id_res = static_resource_id_resource or resource_id_list[0]
            perform_uri_fetch(session_obj, module, system_id_res, resource_id_list, resource_id)
        else:
            module.exit_json(msg=TARGET_DEVICE_NOT_SUPPORTED, skipped=True)
    except HTTPError as err:
        if err.code in [404, 405]:
            module.exit_json(msg=TARGET_DEVICE_NOT_SUPPORTED,
                             error_info=json.load(err), failed=True)
        raise err


def is_change_applicable_for_power_state(current_power_state, apply_power_state):
    """ checks if changes are applicable or not for current system state
        :param current_power_state: Current power state
        :type current_power_state: str
        :param apply_power_state: Required power state
        :type apply_power_state: str
        :return: boolean True if changes is applicable
    """
    on_states = ["On", "PoweringOn"]
    off_states = ["Off", "PoweringOff"]

    reset_map_apply = {
        ("On", "ForceOn",): off_states,
        ("PushPowerButton",): on_states + off_states,
        ("ForceOff", "ForceRestart", "GracefulRestart", "GracefulShutdown", "Nmi", "PowerCycle",): on_states
    }
    is_reset_applicable = False
    for apply_states, applicable_states in reset_map_apply.items():
        if apply_power_state in apply_states:
            if current_power_state in applicable_states:
                is_reset_applicable = True
                break
            break
    return is_reset_applicable


def is_valid_reset_type(reset_type, allowable_enum, module):
    reset_type_param = module.params.get('reset_type')
    if reset_type not in allowable_enum:
        res_list = re.findall('[A-Z][^A-Z]*', reset_type)
        lw_reset_type = " ".join([word.lower() for word in res_list])
        if reset_type_param:
            error_msg = INVALID_RESET_TYPE.format(lw_reset_type, ", ".join(allowable_enum))
        else:
            error_msg = INVALID_RESET_TYPE_OEM.format(option=reset_type,
                                                      supported_oem_reset_type_values=", ".join(allowable_enum))
        module.exit_json(msg=error_msg, failed=True)


def is_valid_final_pwr_state(final_pwr_state, allowed_final_pwr_state, module):
    if final_pwr_state.capitalize() not in allowed_final_pwr_state:
        error_msg = INVALID_PWR_ERROR.format(final_pwr_state, ", ".join(allowed_final_pwr_state))
        module.exit_json(msg=error_msg, failed=True)


def is_valid_vendor(redfish_session_obj, module, vendor):
    system_resp = redfish_session_obj.invoke_request("GET", "/redfish/v1/")
    system_vendor = system_resp.json_data.get("Vendor")
    if system_vendor.lower() != vendor.lower():
        module.exit_json(msg=VENDOR_NOT_SUPPORTED.format(supported_vendors=system_vendor), skipped=True)


def check_firmware_version(module, redfish_session_obj):
    resp = redfish_session_obj.invoke_request("GET", FIRM_VER_URI)
    redfish_firmware_version = resp.json_data.get('FirmwareVersion', '')
    if LooseVersion(redfish_firmware_version) <= MINIMUM_SUPPORTED_FIRMWARE_VERSION:
        module.exit_json(msg=UNSUPPORTED_FIRMWARE_MSG.format(
            minimum_supported_firmware_version=MINIMUM_SUPPORTED_FIRMWARE_VERSION), skipped=True)


def prepare_payload(current_vendor_dict):
    payload = {}
    final_pwr_state = current_vendor_dict.get("final_power_state")
    reset_type = current_vendor_dict.get("reset_type")
    if final_pwr_state:
        final_pwr_state = final_pwr_state.capitalize()
        payload["FinalPowerState"] = final_pwr_state
    if reset_type:
        payload["ResetType"] = reset_type
    return payload


def run_change_power_state(redfish_session_obj, module):
    """
    Apply reset type to system
    Keyword arguments:
    redfish_session_obj  -- session handle
    module -- Ansible module obj
    """
    apply_reset_type = module.params["reset_type"]
    fetch_power_uri_resource(module, redfish_session_obj, "Systems")
    is_valid_reset_type(apply_reset_type, powerstate_map["allowable_enums"], module)
    current_power_state = powerstate_map["current_state"]
    reset_flag = is_change_applicable_for_power_state(current_power_state, apply_reset_type)
    if module.check_mode is True:
        if reset_flag is True:
            module.exit_json(msg=CHANGES_FOUND, changed=True)
        else:
            module.exit_json(msg=NO_CHANGES_FOUND, changed=False)

    if reset_flag is True:
        payload = {"ResetType": apply_reset_type}
        power_uri = powerstate_map["power_uri"]
        reset_resp = redfish_session_obj.invoke_request("POST", power_uri, data=payload)
        if reset_resp.success:
            module.exit_json(msg="Successfully performed the reset type operation"
                                 " '{0}'.".format(apply_reset_type), changed=True)
        else:
            module.exit_json(msg="Unable to perform the reset type operation '{0}'.".format(apply_reset_type),
                             changed=False)
    else:
        module.exit_json(msg="The device is already powered {0}.".format(current_power_state.lower()), changed=False)


def power_cycle_check_mode(module):
    current_power_state = powerstate_map["current_state"]
    if module.check_mode:
        if current_power_state.lower() != 'off':
            module.exit_json(msg=INITIAL_DESIRED_STATE_ERROR)
        module.exit_json(msg=CHANGES_FOUND, changed=True)


def run_change_ac_power_cycle(redfish_session_obj, module):
    check_firmware_version(module, redfish_session_obj)
    oem_reset_type = module.params["oem_reset_type"]
    current_vendor = next(iter(oem_reset_type), None)
    is_valid_vendor(redfish_session_obj, module, current_vendor)
    current_vendor_dict = oem_reset_type[current_vendor]
    apply_reset_type = None
    if "reset_type" in current_vendor_dict:
        apply_reset_type = current_vendor_dict['reset_type']
    final_pwr_state = None
    if "final_power_state" in current_vendor_dict:
        final_pwr_state = current_vendor_dict["final_power_state"]
    if apply_reset_type is None or apply_reset_type == "":
        module.exit_json(msg=OPERATION_ERROR, skipped=True)
    fetch_power_uri_resource(module, redfish_session_obj, "Chassis")
    is_valid_reset_type(apply_reset_type, powerstate_map["allowable_enums"], module)
    if final_pwr_state:
        is_valid_final_pwr_state(final_pwr_state, powerstate_map["allowable_power_state"], module)
    power_cycle_check_mode(module)
    payload = prepare_payload(current_vendor_dict)
    power_uri = powerstate_map["power_uri"]
    try:
        reset_resp = redfish_session_obj.invoke_request("POST", power_uri, data=payload)
        if reset_resp.status_code == 204:
            if final_pwr_state and final_pwr_state.lower() == "on":
                module.exit_json(msg=SUCCESS_AC_MSG_ON, changed=True)
            module.exit_json(msg=SUCCESS_AC_MSG, changed=True)
    except HTTPError as err:
        err_message = json.load(err)
        if err.code == 409 and err_message["error"]["@Message.ExtendedInfo"][0]["MessageId"] == "IDRAC.2.9.PSU507":
            error_msg = err_message["error"]["@Message.ExtendedInfo"][0]["Message"]
            module.exit_json(msg=error_msg, skipped=True)


def main():
    specs = {
        "resource_id": {"required": False, "type": "str"},
        "reset_type": {"required": False, "type": "str",
                       "choices": ['ForceOff', 'ForceOn', 'ForceRestart', 'GracefulRestart',
                                   'GracefulShutdown', 'Nmi', 'On', 'PowerCycle', 'PushPowerButton']},
        "oem_reset_type": {"required": False, "type": "dict"},
    }
    module = RedfishAnsibleModule(
        argument_spec=specs,
        supports_check_mode=True,
        mutually_exclusive=[("oem_reset_type", "reset_type")])
    try:
        reset_type = module.params["reset_type"]
        oem_reset_type = module.params["oem_reset_type"]
        with Redfish(module.params) as redfish_obj:
            if reset_type:
                run_change_power_state(redfish_obj, module)
            elif oem_reset_type:
                run_change_ac_power_cycle(redfish_obj, module)
            else:
                module.exit_json(msg=OPERATION_ERROR, skipped=True)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)
    except Exception as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
