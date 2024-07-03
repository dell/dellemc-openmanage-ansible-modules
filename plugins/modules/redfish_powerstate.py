#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.5.0
# Copyright (C) 2020-2024 Dell Inc. or its subsidiaries. All Rights Reserved.

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
      - The unique identifier of the device being managed.
       For example- U(https://<I(baseuri)>/redfish/v1/Systems/<I(resource_id)>).
      - This option is mandatory for I(base_uri) with multiple devices.
      - To get the device details, use the API U(https://<I(baseuri)>/redfish/v1/Systems).
    required:  false
    type: str
  reset_type:
    description:
      - This option resets the device.
      - If C(ForceOff), Turns off the device immediately.
      - If C(ForceOn), Turns on the device immediately.
      - If C(ForceRestart), Turns off the device immediately, and then restarts the device.
      - If C(GracefulRestart), Performs graceful shutdown of the device, and then restarts the device.
      - If C(GracefulShutdown), Performs a graceful shutdown of the device, and the turns off the device.
      - If C(Nmi), Sends a diagnostic interrupt to the device. This is usually a non-maskable interrupt
       (NMI) on x86 device.
      - If C(On), Turns on the device.
      - If C(PowerCycle), Performs power cycle on the device.
      - If C(PushPowerButton), Simulates the pressing of a physical power button on the device.
      - I(reset_type) is mutually exclusive with I(oem_reset_type).
      - When a power control operation is performed, which is not supported on the device, an error message is displayed
       with the list of operations that can be performed.
    required:  false
    type: str
    choices: ["ForceOff", "ForceOn", "ForceRestart", "GracefulRestart", "GracefulShutdown",
               "Nmi", "On", "PowerCycle", "PushPowerButton"]
  oem_reset_type:
    description:
      - This initiates a complete A/C cycle of the server, equivalent to the action of disconnecting power cables using OEM API.
      - I(oem_reset_type) is mutually exclusive with I(reset_type).
    required:  false
    type: dict
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

- name: Perform AC Power Cycle
  dellemc.openmanage.redfish_powerstate:
       baseuri: "192.168.0.1"
       username: "username"
       password: "password"
       ca_path: "/path/to/ca_cert.pem"
       oem_reset_type:
            dell:
                final_power_state: "On"
                reset_type: "PowerCycle"

- name: Perform AC Power Cycle
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
NO_CHANGES_FOUND = "No changes found to be applied."
FIRM_VER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1?$select=FirmwareVersion"
INAVALID_RESET_TYPE_OEM = "{option} is not supported. The supported values" \
    " are {supported_oem_reset_type_values}. Enter the valid values and retry" \
    " the operation."
TARGET_DEVICE_NOT_SUPPORTED = "The target device does not support the system" \
    " reset feature using Redfish API."
INVALID_DEVICE_ID = "Invalid device Id '{0}' is provided"
MINIMUM_SUPPORTED_FIRMWARE_VERSION = "7.00.60"
UNSUPPORTED_FIRMWARE_MSG = "Unable to perform the Virtual AC power-cycle" \
    " operation because the firmware version is not supported. The minimum" \
    " supported firmware version is {minimum_supported_firmware_version}."
INITIAL_DESIRED_STATE_ERROR = "No changes found to be applied because system is powered on."
VENDOR_NOT_SUPPORTED = "The vendor is not supported. The supported vendors" \
    " are '{supported_vendors}'. Enter the valid vendor and retry the operation."
SUCCESS_AC_MSG = "Successfully performed the full virtual server a/c power" \
    " cycle operation."
INAVALID_RESET_TYPE = "The target device does not support a {0} operation." \
    " The acceptable values for device reset types are {1}."
OEM_RESET_KEY = '#DellOemChassis.ExtendedReset'
INVALID_PWR_ERROR = "The target device does not support" \
                    " '{0}' operation. The acceptable values for device final power states" \
                    " are '{1}'."

powerstate_map = {}


def fetch_powerstate_details(system_res_data, action_data):
    current_state = system_res_data["PowerState"]
    power_uri = action_data['#ComputerSystem.Reset']['target']
    allowable_enums = action_data['#ComputerSystem.Reset']['ResetType@Redfish.AllowableValues']
    powerstate_map.update(
        {'power_uri': power_uri, 'allowable_enums': allowable_enums, 'current_state': current_state})


def fetch_ac_powerstate_details(system_id_res_data, action_id_res):
    current_state = system_id_res_data["PowerState"]
    power_uri = action_id_res['Oem'][OEM_RESET_KEY]['target']
    allowable_enums = action_id_res['Oem'][OEM_RESET_KEY]['ResetType@Redfish.AllowableValues']
    allowable_final_power_state = action_id_res['Oem'][OEM_RESET_KEY]['FinalPowerState@Redfish.AllowableValues']
    powerstate_map.update(
        {'power_uri': power_uri, 'allowable_enums': allowable_enums,
            'current_state': current_state, 'allowable_power_state': allowable_final_power_state})


def fetch_power_uri_resource(module, session_obj, reset_type_map=None):
    try:
        resource_id = module.params.get("resource_id")
        reset_type = module.params.get("reset_type")
        static_resource_id_resource = None
        if resource_id:
            static_resource_id_resource = "{0}{1}{2}".format(session_obj.root_uri, reset_type_map + "/", resource_id)
        system_uri = "{0}{1}".format(session_obj.root_uri, reset_type_map)
        system_resp = session_obj.invoke_request("GET", system_uri)
        system_members = system_resp.json_data.get("Members")
        if len(system_members) > 1 and static_resource_id_resource is None:
            module.fail_json(msg="Multiple devices exists in the system, but option 'resource_id' is not specified.")
        if system_members:
            resource_id_list = [system_id["@odata.id"] for system_id in system_members if "@odata.id" in system_id]
            system_id_res = static_resource_id_resource or resource_id_list[0]
            if system_id_res in resource_id_list:
                system_id_res_resp = session_obj.invoke_request("GET", system_id_res)
                system_id_res_data = system_id_res_resp.json_data
                action_id_res = system_id_res_data.get("Actions")
                if action_id_res:
                    if reset_type:
                        fetch_powerstate_details(system_id_res_data, action_id_res)
                    else:
                        fetch_ac_powerstate_details(system_id_res_data, action_id_res)
                else:
                    module.fail_json(msg=TARGET_DEVICE_NOT_SUPPORTED)
            else:
                module.fail_json(msg=INVALID_DEVICE_ID.format(resource_id))
        else:
            module.fail_json(msg=TARGET_DEVICE_NOT_SUPPORTED)
    except HTTPError as err:
        if err.code in [404, 405]:
            module.fail_json(msg=TARGET_DEVICE_NOT_SUPPORTED,
                             error_info=json.load(err))
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
            error_msg = INAVALID_RESET_TYPE.format(lw_reset_type, ", ".join(allowable_enum))
        else:
            error_msg = INAVALID_RESET_TYPE_OEM.format(option=lw_reset_type,
                                                    supported_oem_reset_type_values= ", ".join(allowable_enum))
        module.exit_json(msg=error_msg, failed=True)


def is_valid_final_pwr_state(final_pwr_state, allowed_final_pwr_state, module):
    if final_pwr_state.capitalize() not in allowed_final_pwr_state:
        error_msg = INVALID_PWR_ERROR.format(final_pwr_state, ", ".join(allowed_final_pwr_state))
        module.exit_json(msg=error_msg, failed=True)


def is_valid_vendor(redfish_session_obj, module, vendor):
    system_resp = redfish_session_obj.invoke_request("GET", "/redfish/v1/")
    system_vendor = system_resp.json_data.get("Vendor")
    if system_vendor.lower() != vendor.lower():
        module.exit_json(msg=VENDOR_NOT_SUPPORTED.format(supported_vendors=system_vendor), failed=True)


def check_firmware_version(module, redfish_session_obj):
    resp = redfish_session_obj.invoke_request("GET", FIRM_VER_URI)
    redfish_firmware_version = resp.json_data.get('FirmwareVersion', '')
    if LooseVersion(redfish_firmware_version) <= MINIMUM_SUPPORTED_FIRMWARE_VERSION:
        module.exit_json(msg=UNSUPPORTED_FIRMWARE_MSG.format(
            MINIMUM_SUPPORTED_FIRMWARE_VERSION), failed=True)


def prepare_payload(module, vendor):
    payload = {}
    final_power_state = module.params['oem_reset_type'].get(vendor).get("final_power_state").capitalize()
    reset_type = module.params['oem_reset_type'].get(vendor).get("reset_type")
    if final_power_state:
        payload["FinalPowerState"] = final_power_state
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


def run_change_ac_power_cycle(redfish_session_obj, module):
    check_firmware_version(module, redfish_session_obj)
    oem_reset_type = module.params["oem_reset_type"]
    current_vendor = next(iter(oem_reset_type), None)
    is_valid_vendor(redfish_session_obj, module, current_vendor)
    apply_reset_type = module.params["oem_reset_type"][current_vendor]['reset_type']
    final_pwr_state = module.params["oem_reset_type"][current_vendor]["final_power_state"]
    fetch_power_uri_resource(module, redfish_session_obj, "Chassis")
    is_valid_reset_type(apply_reset_type, powerstate_map["allowable_enums"], module)
    if final_pwr_state is not None:
        is_valid_final_pwr_state(final_pwr_state, powerstate_map["allowable_power_state"], module)
    current_power_state = powerstate_map["current_state"]
    if module.check_mode:
        if current_power_state.lower() != 'off':
            module.exit_json(msg=INITIAL_DESIRED_STATE_ERROR)
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    payload = prepare_payload(module, current_vendor)
    power_uri = powerstate_map["power_uri"]
    try:
        reset_resp = redfish_session_obj.invoke_request("POST", power_uri, data=payload)
        if reset_resp.status_code == 204:
            module.exit_json(msg=SUCCESS_AC_MSG, changed=True)
    except HTTPError as err:
        err_message = json.load(err)
        if err_message["error"]["@Message.ExtendedInfo"][0]["MessageId"] == "IDRAC.2.9.PSU507":
            error_msg =err_message["error"]["@Message.ExtendedInfo"][0]["Message"]
            module.exit_json(msg= error_msg, failed=True)


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
        with Redfish(module.params) as redfish_obj:
            if reset_type:
                run_change_power_state(redfish_obj, module)
            else:
                run_change_ac_power_cycle(redfish_obj, module)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, OSError) as err:
        module.fail_json(msg=str(err))
    except Exception as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
