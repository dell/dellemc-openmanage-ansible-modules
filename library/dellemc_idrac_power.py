#! /usr/bin/python
# _*_ coding: utf-8 _*_

#
# Copyright (c) 2017 Dell Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_idrac_power
short_description: Configure the Power Cycle options on PowerEdge Server
version_added: "2.3"
description:
    - Configure the Power Cycle options on a Dell EMC PowerEdge Server
options:
    idrac_ipv4:
        required: True
        description: iDRAC IPv4 Address
    idrac_user:
        description: iDRAC user name
        default: root
    idrac_pwd:
        description: iDRAC user password
    idrac_port:
        description: iDRAC port
    state:
        description:
            - if C(PowerOn), will Power On the server
            - if C(SoftPowerCycle), will close the running applications and
              Reboot the Server
            - if C(SoftPowerOff), will close the running applications and Power
              Off the server
            - if C(HardReset), will Reboot the Server immediately
            - if C(DiagnosticInterrupt), will reboot the Server for
              troubleshooting
            - if C(GracefulPowerOff), will close the running applications and
              Power Off the server
        choices: ["PowerOn", "SoftPowerCycle", "SoftPowerOff", "HardReset",
                  "DiagnosticInterrupt", "GracefulPowerOff"]
        required: True

requirements: ['omsdk']
author: "anupam.aloke@dell.com"

"""

EXAMPLES = """
---
"""

RETURNS = """
---
"""

import sys
import os
import json
from ansible.module_utils.basic import AnsibleModule


# Change Power State
# idrac: iDRAC Handle
# module: Ansible module
#
# supports check mode
def change_power_state (idrac, module):

    from omsdk.sdkcenum import TypeHelper
    msg = {}
    msg['RequestPowerStateChange'] = {}
    msg['changed'] = False
    msg['failed'] = False

    if module.params['state'] == "PowerOn":
        power_state = idrac.ePowerStateEnum.PowerOn
    elif module.params['state'] == "SoftPowerCycle":
        power_state = idrac.ePowerStateEnum.SoftPowerCycle
    elif module.params['state'] == "SoftPowerOff":
        power_state = idrac.ePowerStateEnum.SoftPowerOff
    elif module.params['state'] == "HardReset":
        power_state = idrac.ePowerStateEnum.HardReset
    elif module.params['state'] == "DiagnosticInterrupt":
        power_state = idrac.ePowerStateEnum.DiagnosticInterrupt
    elif module.params['state'] == "GracefulPowerOff":
        power_state = idrac.ePowerStateEnum.GracefulPowerOff

    current_power_state = idrac.PowerState
    is_power_on = (int(current_power_state) ==
                      TypeHelper.resolve(idrac.ePowerStateEnum.PowerOn))

    if module.params['state'] == "PowerOn":
        if module.check_mode or is_power_on:
            msg['changed'] = False
        else:
            msg['ChangePowerState'] = idrac.config_mgr.change_power(power_state)

            if msg['ChangePowerState']['Status'] == "Error":
                msg['failed'] = True
            else:
                msg['changed'] = True

    elif module.params['state'] == "PowerOff":
        if module.check_mode or not is_power_on:
            msg['changed'] = False
        else:
            msg['ChangePowerState'] = idrac.config_mgr.change_power(power_state)

            if msg['ChangePowerState']['Status'] == "Error":
                msg['failed'] = True
            else:
                msg['changed'] = True
    else:
        if module.check_mode:
            msg['changed'] = True
        else:
            msg['ChangePowerState'] = idrac.config_mgr.change_power(power_state)
            msg['changed'] = True

    return msg


# Main()
def main():
    from ansible.module_utils.dellemc_idrac import iDRACConnection

    module = AnsibleModule (
            argument_spec = dict (

                # iDRAC Handle
                idrac = dict (required = False, type = 'dict'),

                # iDRAC Credentials
                idrac_ipv4 = dict (required = True, type = 'str'),
                idrac_user = dict (required = False, default = None, type = 'str'),
                idrac_pwd  = dict (required = False, default = None, type = 'str'),
                idrac_port = dict (required = False, default = None),

                # Power Cycle State
                state      = dict (required = False,
                                   choice = ["PowerOn",
                                       "SoftPowerCycle",
                                       "SoftPowerOff",
                                       "HardReset",
                                       "DiagnosticInterrupt",
                                       "GracefulPowerOff"],
                                   type = 'str')
                ),

                supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    # Setup Power Cycle State
    msg = change_power_state (idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    module.exit_json(**msg)

if __name__ == '__main__':
    main()
