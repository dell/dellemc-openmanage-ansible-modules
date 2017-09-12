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
module: dellemc_idrac_nic_ipv4
short_description: Configure iDRAC Network IPv4 Settings
version_added: "2.3"
description: Configure iDRAC Network IPv4 Settings
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
    enable_ipv4:
        required: False
        description: Enable or disable the iDRAC IPv4 stack
        default: True
    dhcp_enable:
        required: False
        description: Enable or disable DHCP for assigning iDRAC IPv4 address
        default: False
    static_ipv4:
        required: False
        description:
        - iDRAC NIC static IPv4 address
        - Required if I(dhcp_enable=False)
        default: None
    static_ipv4_gw:
        required: False
        description:
        - Static IPv4 gateway address for iDRAC NIC
        - Required if I(dhcp_enable=False)
        default: None
    static_netmask:
        required: False
        description:
        - Static IPv4 subnet mask for iDRAC NIC
        - Required if I(dhcp_enable=False)
        default: None
    dns_from_dhcp:
        required: False
        description:
        - if C(True), will enable the use of DHCP server for obtaining the
          primary and secondary DNS servers addresses
        - if C(False), will disable the use of DHCP server for obtaining the
          primary and secondary DNS servers addresses
    preferred_dns:
        required: False
        description:
        - Preferred DNS Server static IPv4 Address
        - Required if I(dns_from_dhcp=False)
        default: None
    alternate_dns:
        required: False
        description:
        - Alternate DNS Server static IPv4 Address
        - Required if I(dns_from_dhcp=False)
        default: None

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
"""

EXAMPLES = """
---
- name: Configure NIC IPv4
    dellemc_idrac_nic_ipv4:
       idrac_ip:   "192.168.1.1"
       idrac_user: "root"
       idrac_pwd:  "calvin"
       share_name: "\\\\10.20.30.40\\share\\"
       share_user: "user1"
       share_pwd:  "password"
       share_mnt:  "/mnt/share"
       enable_ipv4: True
       dhcp_enable: False
"""

RETURNS = """
---
"""

from ansible.module_utils.dellemc_idrac import *
from ansible.module_utils.basic import AnsibleModule

def _setup_idrac_nw_share (idrac, module):
    """
    Setup local mount point for Network file share

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    myshare = FileOnShare(module.params['share_name'],
                          module.params['share_mnt'],
                          isFolder=True)

    myshare.addcreds(UserCredentials(module.params['share_user'],
                                    module.params['share_pwd']))

    return idrac.config_mgr.set_liason_share(myshare)

def setup_idrac_nic_ipv4 (idrac, module):
    """
    Setup iDRAC IPv4 configuration settings

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
                return msg, err

        # TODO: Check whether the IPv4 settings exists
        exists = False

        if module.check_mode or exists:
            msg['changed'] = not exists
        else:
            msg['msg'] = idrac.config_mgr.configure_idrac_ipv4(
                                             module.params["enable_ipv4"],
                                             module.params["dhcp_enable"])

            if "Status" in msg['msg'] and msg['msg']["Status"] is "Success":
                if not module.params["dhcp_enable"]:
                    msg['msg'] = idrac.config_mgr.configure_idrac_ipv4static(
                                             module.params["static_ipv4"],
                                             module.params["static_netmask"],
                                             module.params["static_ipv4_gw"],
                                             [module.params["preferred_dns"],
                                              module.params["alternate_dns"]],
                                             module.params["dns_from_dhcp"])

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

                # iDRAC Network IPv4 Settings
                enable_ipv4 = dict (required = False, default = True, type = 'bool'),
                dhcp_enable = dict (required = False, default = True, type = 'bool'),
                static_ipv4 = dict (required = False, default = None, type = 'str'),
                static_ipv4_gw = dict (required = False, default = None, type = 'str'),
                static_netmask = dict (required = False, default = None, type = 'str'),
                dns_from_dhcp = dict (required = False, default = False, type = 'bool'),
                preferred_dns = dict (required = False, default = None, type = 'str'),
                alternate_dns = dict (required = False, default = None, type = 'str')

                ),
            required_if = [
                ["dhcp_enable", False, ["static_ipv4", "static_ipv4_gw", "static_netmask"]],
                ["dns_from_dhcp", False, ["preferred_dns", "alternate_dns"]]
            ],

            supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    (msg, err) = setup_idrac_nic_ipv4 (idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
