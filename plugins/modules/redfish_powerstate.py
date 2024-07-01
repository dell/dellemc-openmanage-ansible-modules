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
from ansible_collections.dellemc.openmanage.plugins.module_utils.redfish import Redfish, RedfishAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError

powerstate_map = {}

CHANGES_FOUND = "Changes found to be applied."
NO_CHANGES_FOUND = "No changes found to be applied."
RESET_TYPE_NOT_SUPPORTED = "{option} is not supported. The supported values are {supported_oem_reset_type_values}. Enter the valid values and retry the operation."
TARGET_DEVICE_NOT_SUPPORTED = "The target device does not support the system reset feature" \
                         " using Redfish API."
INVALID_DEVICE_ID = "Invalid device Id '{0}' is provided"

def fetch_powerstate_details(system_res_data, action_data):
        current_state = system_res_data["PowerState"]
        power_uri = action_data['#ComputerSystem.Reset']['target']
        allowable_enums = action_data['#ComputerSystem.Reset']['ResetType@Redfish.AllowableValues']
        powerstate_map.update(
            {'power_uri': power_uri, 'allowable_enums': allowable_enums, 'current_state': current_state})

def fetch_ac_powerstate_details(system_id_res_data, action_id_res):
        current_state = system_id_res_data["PowerState"]
        power_uri = action_id_res['Oem']['#DellOemChassis.ExtendedReset']['target']
        allowable_enums = action_id_res['Oem']['#DellOemChassis.ExtendedReset']['ResetType@Redfish.AllowableValues']
        allowable_final_power_state = action_id_res['Oem']['#DellOemChassis.ExtendedReset']['FinalPowerState@Redfish.AllowableValues']
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
    if reset_type not in allowable_enum:
        res_list = re.findall('[A-Z][^A-Z]*', reset_type)
        lw_reset_type = " ".join([word.lower() for word in res_list])
        error_msg = "The target device does not support a" \
                    " {0} operation.The acceptable values for device reset types" \
                    " are {1}.".format(lw_reset_type, ", ".join(allowable_enum))
        module.fail_json(msg=error_msg)

def is_valid_final_pwr_state(final_pwr_state, allowed_final_pwr_state, module):
    if final_pwr_state not in allowed_final_pwr_state:
        error_msg = "The target device does not support a" \
                    " {0} operation.The acceptable values for device final power states" \
                    " are {1}.".format(final_pwr_state, ", ".join(allowed_final_pwr_state))
        module.exit_josn(msg=error_msg, failed=True)
def is_valid_initial_pwr_state(initial_pwr_state, module):
    if initial_pwr_state.lower() != 'off':
        error_msg = "Unable to perform the Virtual AC power-cycle operation because the server is powered on."
        module.exit_josn(msg=error_msg, failed=True)

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
            module.exit_json(msg="Changes found to be applied.", changed=True)
        else:
            module.exit_json(msg="No Changes found to be applied.", changed=False)

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
    """
    Apply reset type to system
    Keyword arguments:
    redfish_session_obj  -- session handle
    module -- Ansible module obj
    """
    apply_reset_type = module.params["reset_type"]
    fetch_power_uri_resource(module, redfish_session_obj)
    is_valid_reset_type(apply_reset_type, powerstate_map["allowable_enums"], module)
    current_power_state = powerstate_map["current_state"]
    reset_flag = is_change_applicable_for_power_state(current_power_state, apply_reset_type)
    if module.check_mode is True:
        if reset_flag is True:
            module.exit_json(msg="Changes found to be applied.", changed=True)
        else:
            module.exit_json(msg="No Changes found to be applied.", changed=False)

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


def main():
    specs = {
        "resource_id": {"required": False, "type": "str"},
        "reset_type": {"required": False, "type": "str",
                       "choices": ['ForceOff', 'ForceOn', 'ForceRestart', 'GracefulRestart',
                                   'GracefulShutdown', 'Nmi', 'On', 'PowerCycle', 'PushPowerButton']},
        "oem_reset_type": {"required:": False, "type": "dict"},
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
