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
module: dellemc_idrac_nic
short_description: Configure iDRAC Network settings
version_added: "2.3"
description: Configure following iDRAC Network settings:
    - Enable NIC: Enable/disable NIC
    - NIC Selection: Select one of the following modes to configure NIC as
      the primary mode in shared interface:
      - Dedicated
      - LOM1
      - LOM2
      - LOM3
      - LOM4
    - Failover Network: configure failover network if NIC selection fails
    - Auto Dedicated NIC: configure dedicated NIC as network port. This requires
      iDRAC Dedicated NIC license
    - Auto Negotiation: Set it to "On" or "Off" to let iDRAC automatically
      set the duplex mode and network speed or manually configure the options
    - Network Speed: configure the network speed manually if auto negotiation
      is not "On"
    - Duplex Mode: configure the full or half-duplex mode
    - NIC MTU: Configure the Maximum Transmission Unit (MTU) value
options:
    idrac_ip:
        required: False
        description: iDRAC IP Address
        default: None
    idrac_user:
        required: False
        description: iDRAC user name
        default: None
    idrac_pwd:
        required: False
        description: iDRAC user password
        default: None
    idrac_port:
        required: False
        description: iDRAC port
        default: None
    share_name:
        required: True
        description: CIFS or NFS Network share
    share_user:
        required: True
        description: Network share user in the format user@domain
    share_pwd:
        required: True
        description: Network share user password
    share_mnt:
        required: True
        description: Local mount path of the network file share with
        read-write permission for ansible user
    nic_selection:
        required: False
        description: NIC Selection mode
        choices: ['Dedicated','LOM1','LOM2','LOM3','LOM4']
        default: "Dedicated"
    nic_failover:
        required: False
        description: Failover network if NIC selection fails
        choices: ["None", "LOM1", "LOM2", "LOM3", "LOM4", "All"]
        default: "None"
    nic_autoneg:
        required: False
        description:
        - if C(True), will enable auto negotiation
        - if C(False), will disable auto negotiation
        default: False
    nic_speed:
        required: False
        description: Network Speed
        choices: ["10", "100", "1000"]
        default: "1000"
    nic_duplex:
        required: False
        description:
        - if C(Full), will enable the Full-Duplex mode
        - if C(Half), will enable the Half-Duplex mode
        choices: ["Full", "Half"]
        default: "Full"
    nic_autodedicated:
        required: False
        description:
        - if C(True), will enable the auto-dedicated NIC option
        - if C(False), will disable the auto-dedicated NIC option
        default: False

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
"""

EXAMPLES = """
---
- name: Configure NIC Selection
    dellemc_idrac_nic:
       idrac_ip:      "192.168.1.1"
       idrac_user:    "root"
       idrac_pwd:     "calvin"
       share_name:    "\\\\10.20.30.40\\share\\"
       share_user:    "user1"
       share_pwd:     "password"
       share_mnt:     "/mnt/share"
       nic_selection: "Dedicated"
       state:         "enable"
"""

from ansible.module_utils.basic import AnsibleModule

def _setup_idrac_nw_share (idrac, module):
    """
    Setup local mount point for Network file share

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    from omsdk.sdkfile import FileOnShare
    from omsdk.sdkcreds import UserCredentials

    myshare = FileOnShare(module.params['share_name'],
                          module.params['share_mnt'],
                          isFolder=True)

    myshare.addcreds(UserCredentials(module.params['share_user'],
                                    module.params['share_pwd']))

    return idrac.config_mgr.set_liason_share(myshare)

def setup_idrac_nic (idrac, module):
    """
    Setup iDRAC NIC configuration settings

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
        # Check first whether local mount point for network share is setup
        if idrac.config_mgr.liason_share is None:
            if not  _setup_idrac_nw_share (idrac, module):
                msg['msg'] = "Failed to setup local mount point for network share"
                msg['failed'] = True
                return msg

        # TODO: Check whether NIC settings exists or not
        exists = False

        if module.check_mode or exists:
            msg['changed'] = not exists
        else:
            msg['msg'] = idrac.config_mgr.configure_idrac_nic(
                                             module.params["nic_selection"],
                                             module.params["nic_failover"],
                                             module.params["nic_autoneg"],
                                             module.params["nic_speed"])

            if 'Status' in msg['msg']:
                if msg['msg']["Status"] == "Success":
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
    from ansible.module_utils.dellemc_idrac import iDRACConnection

    module = AnsibleModule (
            argument_spec = dict (
                # iDRAC handle
                idrac = dict (required = False, type = 'dict'),

                # iDRAC Credentials
                idrac_ip   = dict (required = False, default = None, type = 'str'),
                idrac_user = dict (required = False, default = None, type = 'str'),
                idrac_pwd  = dict (required = False, default = None,
                                   type = 'str', no_log = True),
                idrac_port = dict (required = False, default = None, type = 'int'),

                # Network File Share
                share_name = dict (required = True, type = 'str'),
                share_user = dict (required = True, type = 'str'),
                share_pwd  = dict (required = True, type = 'str', no_log = True),
                share_mnt  = dict (required = True, type = 'str'),

                # iDRAC Network Settings
                nic_selection = dict (required = False,
                                      choices = ['Dedicated',
                                                 'LOM1',
                                                 'LOM2',
                                                 'LOM3',
                                                 'LOM4'],
                                      default = 'Dedicated'),
                nic_failover = dict (required = False,
                                     choices = ['None',
                                                'LOM1',
                                                'LOM2',
                                                'LOM3',
                                                'LOM4',
                                                'All'],
                                     default = 'None'),
                nic_autoneg = dict (required = False, default = False, type = 'bool'),
                nic_speed = dict (required = False,
                                  choices = ['10', '100', '1000'],
                                  default = '1000')
                ),

            supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    (msg, err) = setup_idrac_nic (idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
