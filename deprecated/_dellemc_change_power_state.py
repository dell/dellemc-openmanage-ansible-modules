#!/usr/bin/python
# _*_ coding: utf-8 _*_

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0.10
# Copyright (C) 2018-2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['deprecated'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_change_power_state
short_description: Server power control.
version_added: "2.9"
deprecated:
  removed_in: "2.13"
  why: Replaced with M(redfish_powerstate).
  alternative: Use M(redfish_powerstate) instead.
description:
    - Server power control operations.
options:
    idrac_ip:
        required: True
        type: str
        description: iDRAC IP Address.
    idrac_user:
        required: True
        type: str
        description: iDRAC username.
    idrac_password:
        required: True
        description: iDRAC user password.
        type: str
        aliases: ['idrac_pwd']
    idrac_port:
        required: False
        description: iDRAC port.
        type: int
        default: 443
    change_power:
        required:  False
        type: str
        description:
           - (deprecated)Desired power state.
           - This option will be deprecated from Ansible version 2.14 onwards. It will be replaced with I(reset_type).
           - C(GracefulRestart) is applicable for idrac firmware versions below 3.30.30.30.
        choices: [ "On", "ForceOff", "GracefulRestart", "GracefulShutdown",
         "PushPowerButton", "Nmi" ]
    reset_type:
        required:  False
        type: str
        description:
           - This option resets the system.
           - C(ForceRestart) is applicable for idrac firmware versions from 3.30.30.30 and above.
        choices: ["On", "ForceOff", "ForceRestart", "GracefulShutdown",
         "PushPowerButton", "Nmi"]
requirements:
    - "omsdk"
    - "python >= 2.7.5"
author:
    - "Sajna Shetty(@Sajna-Shetty)"
    - "Felix Stephen (@felixs88)"

"""

EXAMPLES = """
---
- name: Change power state
  dellemc_change_power_state:
       idrac_ip:   "192.168.0.1"
       idrac_user: "idrac_user"
       idrac_password:  "idrac_password"
       reset_type: "ForceRestart"
"""

RETURNS = """
dest:
    description: Configures the power control option on a Dell EMC PowerEdge server.
    returned: success
    type: string

"""


from ansible.module_utils.remote_management.dellemc.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
try:
    from omdrivers.enums.iDRAC.iDRACEnums import ComputerSystemResetTypesEnum
except ImportError:
    pass


power_state_mapper = {
    "On": ["On"],
    "Off - Soft": ["ForceOff", "GracefulShutdown"],
}


def get_powerstate(idrac):
    state = idrac._get_field_device(idrac.ComponentEnum.System, "PowerState")
    return state


def is_change_applicable_for_power_state(current_power_state, apply_power_state):
    """when check_mode is enabled ,
        checks if changes are applicable or not
        :param current_power_state: Current power state
        :type current_power_state: str
        :param apply_power_state: Required power state
        :type apply_power_state: str
        :return: json message returned
    """
    apply_change_enum_list = ["GracefulRestart", "PushPowerButton", "Nmi", "ForceRestart"]
    try:
        if current_power_state == "Off - Soft" and apply_power_state == "On":
            msg = {'Status': 'Success', 'Message': 'Changes found to commit!', 'changes_applicable': True}
        elif current_power_state == "Off - Soft" and apply_power_state in apply_change_enum_list:
            msg = {'Status': 'Success', 'Message': 'No changes found to commit!', 'changes_applicable': False}
        elif apply_power_state in apply_change_enum_list or \
                apply_power_state not in power_state_mapper[current_power_state]:
            msg = {'Status': 'Success', 'Message': 'Changes found to commit!', 'changes_applicable': True}
        else:
            msg = {'Status': 'Success', 'Message': 'No changes found to commit!', 'changes_applicable': False}
    except Exception as err:
        msg = {'Status': 'Failed', 'Message': 'Failed to execute the command!', 'changes_applicable': False}
    return msg


def run_change_power_state(idrac, module):
    """
    Get Lifecycle Controller status

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    err = False

    try:
        idrac.use_redfish = True
        reset_type = module.params.get("change_power")
        if reset_type:
            deprecation_warning_message = "The change_power option is deprecated. Use the option reset_type instead."
            module.deprecate(deprecation_warning_message, version='2.14')
        else:
            reset_type = module.params["reset_type"]
        if module.check_mode:
            pstate = get_powerstate(idrac)
            msg['msg'] = is_change_applicable_for_power_state(pstate, reset_type)
            if 'changes_applicable' in msg['msg']:
                msg['changed'] = msg['msg']['changes_applicable']
        else:
            msg['msg'] = idrac.config_mgr.change_power(ComputerSystemResetTypesEnum[reset_type])
            if "Status" in msg['msg']:
                if msg['msg']['Status'] == "Success":
                    msg['changed'] = True
                else:
                    msg['failed'] = True
    except Exception as e:
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True
    return msg, err


# Main
def main():

    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_password=dict(required=True, type='str', aliases=['idrac_pwd'], no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),
            change_power=dict(required=False, type='str',
                              choices=["On", "ForceOff", "GracefulRestart", "GracefulShutdown", "PushPowerButton",
                                       "Nmi"]),
            reset_type=dict(required=False, type='str',
                            choices=["On", "ForceOff", "ForceRestart", "GracefulShutdown", "PushPowerButton",
                                     "Nmi"]),
        ),
        required_one_of=[["change_power", "reset_type"]],
        mutually_exclusive=[["change_power", "reset_type"]],
        supports_check_mode=True)
    module.deprecate("The 'dellemc_change_power_state' module has been deprecated."
                     "Use 'redfish_powerstate' instead",
                     version="2.13")
    try:
        with iDRACConnection(module.params) as idrac:
            msg, err = run_change_power_state(idrac, module)
    except (ImportError, ValueError, RuntimeError) as e:
        module.fail_json(msg=str(e))

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
