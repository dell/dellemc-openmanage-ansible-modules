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

DOCUMENTATION = '''
---
module: dellemc_idrac_nic
short_description: Configure iDRAC Network settings
version_added: "2.3"
description:
    - Configure iDRAC Network settings
options:
  idrac_ip:
    required: False
    description:
      - iDRAC IP Address
    default: None
  idrac_user:
    required: False
    description:
      - iDRAC user name
    default: None
  idrac_pwd:
    required: False
    description:
      - iDRAC user password
    default: None
  idrac_port:
    required: False
    description:
      - iDRAC port
    default: None
  share_name:
    required: True
    description:
      - CIFS or NFS Network share
  share_user:
    required: True
    description:
      - Network share user in the format user@domain
  share_pwd:
    required: True
    description:
      - Network share user password
  share_mnt:
    required: True
    description:
      - Local mount path of the network file share with read-write permission for ansible user
  nic_selection:
    required: False
    description:
      - NIC Selection mode
    choices: ['Dedicated','LOM1','LOM2','LOM3','LOM4']
    default: "Dedicated"
  nic_failover:
    required: False
    description:
      - Failover network if NIC selection fails
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
    description:
      - Network Speed
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
'''

EXAMPLES = '''
# Configure NIC Selection using a CIFS Network share
- name: Configure NIC Selection
    dellemc_idrac_nic:
      idrac_ip:      "192.168.1.1"
      idrac_user:    "root"
      idrac_pwd:     "calvin"
      share_name:    "\\\\192.168.10.10\\share"
      share_user:    "user1"
      share_pwd:     "password"
      share_mnt:     "/mnt/share"
      nic_selection: "Dedicated"
      state:         "enable"
'''

RETURN = '''
'''

from ansible.module_utils.dellemc_idrac import *
from ansible.module_utils.basic import AnsibleModule
try:
    from omsdk.sdkcenum import TypeHelper
    from omdrivers.enums.iDRAC.iDRAC import (
        AutoConfig_NICTypes, Autoneg_NICTypes, DHCPEnable_IPv4Types,
        DNSDomainFromDHCP_NICStaticTypes, DNSFromDHCP_IPv4StaticTypes,
        DNSRegister_NICTypes, Duplex_NICTypes, Enable_IPv4Types,
        Enable_NICTypes, Failover_NICTypes, Selection_NICTypes, Speed_NICTypes,
        VLanEnable_NICTypes
    )
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False

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


def _setup_nic (idrac, module):
    """
    Setup iDRAC NIC attributes

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    idrac.config_mgr._sysconfig.iDRAC.NIC.Enable_NIC = \
            TypeHelper.convert_to_enum(module.params['nic_enable'],
                                       Enable_NICTypes)
    idrac.config_mgr._sysconfig.iDRAC.NIC.Selection_NIC = \
            TypeHelper.convert_to_enum(module.params['nic_selection'],
                                       Selection_NICTypes)

    # NIC Selection mode and failover mode should not be same
    if module.params['nic_selection'] == module.params['nic_failover']:
        module.fail_json(msg="NIC Selection mode and Failover mode cannot be same")
    elif module.params['nic_selection'] != 'Dedicated':
        idrac.config_mgr._sysconfig.iDRAC.NIC.FailoverNIC = \
            TypeHelper.convert_to_enum(module.params['nic_failover'],
                                       Failover_NICTypes)

    # if NIC Selection is not 'Dedicated', then Auto-Negotiation is always ON
    if module.params['nic_selection'] != 'Dedicated':
        idrac.config_mgr._sysconfig.IDRAC.NIC.Autoneg_NIC = Autoneg_NICTypes.Enabled
    else:
        idrac.config_mgr._sysconfig.iDRAC.NIC.Autoneg_NIC = \
            TypeHelper.convert_to_enum(module.params['nic_autoneg'],
                                       Autoneg_NICTypes)

    # NIC Speed and Duplex mode can only be set when Auto-Negotiation is not ON
    if module.params['nic_autoneg'] != 'Enabled':
        if module.params['nic_selection'] != 'Dedicated':
            idrac.config_mgr._sysconfig.iDRAC.NIC.Speed_NIC = Speed_NICTypes.T_100
        else:
            idrac.config_mgr._sysconfig.iDRAC.NIC.Speed_NIC = \
                TypeHelper.convert_to_enum(module.params['nic_speed'],
                                           Speed_NICTypes)
        idrac.config_mgr._sysconfig.iDRAC.NIC.Duplex_NIC = \
                TypeHelper.convert_to_enum(module.params['nic_duplex'],
                                           Duplex_NICTypes)

    idrac.config_mgr._sysconfig.iDRAC.NIC.MTU_NIC = module.params['nic_mtu']

    # DNS Registration
    idrac.config_mgr._sysconfig.iDRAC.NIC.DNSRegister_NIC = \
        TypeHelper.convert_to_enum(module.params['dns_register'],
                                   DNSRegister_NICTypes)
    if module.params['dns_idrac_name']: 
        idrac.config_mgr._sysconfig.iDRAC.NIC.DNSRacName = module.params['dns_idrac_name']

    # Enable Auto-Config can 
    if module.params['nic_auto_config'] != 'Disabled':
        if module.params['ipv4_enable'] != 'Enabled' or \
           module.params['ipv4_dhcp_enable'] != 'Enabled':
            module.fail_json(msg="IPv4 and DHCPv4 must be enabled for Auto-Config")
        idrac.config_mgr._sysconfig.iDRAC.NIC.AutoConfig_NIC = \
                TypeHelper.convert_to_enum(module.params['nic_auto_config'],
                                           AutoConfig_NICTypes)

    # VLAN
    idrac.config_mgr._sysconfig.iDRAC.NIC.VLanEnable_NIC = \
        TypeHelper.convert_to_enum(module.params['vlan_enable'],
                                   VLanEnable_NICTypes)
    idrac.config_mgr._sysconfig.iDRAC.NIC.VLanID_NIC = module.params['vlan_id']
    idrac.config_mgr._sysconfig.iDRAC.NIC.VLanPriority_NIC = module.params['vlan_priority']

def _setup_nic_static (idrac, module):
    """
    Setup iDRAC NIC Static attributes

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    idrac.config_mgr._sysconfig.iDRAC.NICStatic.DNSDomainFromDHCP_NICStatic = \
            TypeHelper.convert_to_enum(module.params['dns_domain_from_dhcp'],
                                       DNSDomainFromDHCP_NICStaticTypes)

    if module.params['dns_domain_name']:
        idrac.config_mgr._sysconfig.iDRAC.NICStatic.DNSDomainName_NICStatic = \
                module.params['dns_domain_name']

def _setup_ipv4 (idrac, module):
    """
    Setup IPv4 parameters

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    idrac.config_mgr._sysconfig.iDRAC.IPv4.Enable_IPv4 = \
            TypeHelper.convert_to_enum(module.params['ipv4_enable'],
                                       Enable_IPv4Types)
    idrac.config_mgr._sysconfig.iDRAC.IPv4.DHCPEnable_IPv4 = \
            TypeHelper.convert_to_enum(module.params['ipv4_dhcp_enable'],
                                       DHCPEnable_IPv4Types)

def _setup_ipv4_static (idrac, module):
    """
    Setup IPv4 Static parameters

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    if module.params['ipv4_dhcp_enable'] == 'Disabled':
        if module.params['ipv4_static']:
            idrac.config_mgr._sysconfig.iDRAC.IPv4Static.Address_IPv4Static = \
                    module.params['ipv4_static']

        if module.params['ipv4_static_gw']:
            idrac.config_mgr._sysconfig.iDRAC.IPv4Static.Gateway_IPv4Static = \
                    module.params['ipv4_static_gw']

        if module.params['ipv4_static_mask']:
            idrac.config_mgr._sysconfig.iDRAC.IPv4Static.Netmask_IPv4Static = \
                    module.params['ipv4_static_mask']

    idrac.config_mgr._sysconfig.iDRAC.IPv4Static.DNSFromDHCP_IPv4Static = \
            TypeHelper.convert_to_enum(module.params['ipv4_dns_from_dhcp'],
                                       DNSFromDHCP_IPv4StaticTypes)

    if module.params['ipv4_dns_from_dhcp'] != 'Enabled':
        if module.params['ipv4_preferred_dns']:
            idrac.config_mgr._sysconfig.iDRAC.IPv4Static.DNS1_IPv4Static = \
                    module.params['ipv4_prefered_dns']

        if module.params['ipv4_alternate_dns']:
            idrac.config_mgr._sysconfig.iDRAC.IPv4Static.DNS2_IPv4Static = \
                    module.params['ipv4_alternate_dns']


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

        _setup_nic(idrac, module)
        _setup_nic_static(idrac, module)

        _setup_ipv4(idrac, module)
        _setup_ipv4_static(idrac, module)

        msg['changed'] = idrac.config_mgr._sysconfig.is_changed()

        if module.check_mode:
            # since it is running in check mode, reject the changes
            idrac.config_mgr._sysconfig.reject()
        else:
            msg['msg'] = idrac.config_mgr.apply_changes()

            if 'Status' in msg['msg'] and msg['msg']["Status"] != "Success":
                msg['failed'] = True
                msg['changed'] = False

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
                idrac_ip   = dict (required = True, type = 'str'),
                idrac_user = dict (required = True, type = 'str'),
                idrac_pwd  = dict (required = True, type = 'str', no_log = True),
                idrac_port = dict (required = False, default = 443, type = 'int'),

                # Network File Share
                share_name = dict (required = True, type = 'str'),
                share_user = dict (required = True, type = 'str'),
                share_pwd  = dict (required = True, type = 'str', no_log = True),
                share_mnt  = dict (required = True, type = 'path'),

                # iDRAC Network Settings
                nic_enable = dict (required = False,
                                   choices = ['Enabled', 'Disabled'],
                                   default = 'Enabled', type = 'str'),
                nic_selection = dict (required = False,
                                      choices = ['Dedicated', 'LOM1', 'LOM2', 'LOM3', 'LOM4'],
                                      default = 'Dedicated', type = 'str'),
                nic_failover = dict (required = False,
                                     choices = ['ALL', 'LOM1', 'LOM2', 'LOM3', 'LOM4', 'None'],
                                     default = 'None'),
                nic_autoneg = dict (required = False,
                                    choices = ['Enabled', 'Disabled'],
                                    default = 'Enabled', type = 'str'),
                nic_speed = dict (required = False,
                                  choices = ['10', '100', '1000'],
                                  default = 1000, type = 'str'),
                nic_duplex = dict (required = False, choices = ['Full', 'Half'],
                                   default = 'Full', type = 'str'),
                nic_mtu = dict (required = False, default = 1500, type = 'int'),

                # Network Common Settings
                dns_register = dict (required = False,
                                     choices = ['Enabled', 'Disabled'],
                                     default = 'Disabled', type = 'str'),
                dns_idrac_name = dict (required = False, default = None, type = 'str'),
                dns_domain_from_dhcp = dict (required = False,
                                             choices = ['Disabled', 'Enabled'],
                                             default = 'Disabled', type = 'str'),
                dns_domain_name = dict (required = False, default = None, type = 'str'),

                # Auto-Config Settings
                nic_auto_config = dict (required = False,
                                        choices = ['Disabled', 'Enable Once', 'Enable Once After Reset'],
                                        default = 'Disabled', type = 'str'),


                # IPv4 Settings
                ipv4_enable = dict (required = False,
                                    choices = ['Enabled', 'Disabled'],
                                    default = 'Enabled', type ='str'),
                ipv4_dhcp_enable = dict (required = False,
                                         choices = ['Enabled', 'Disabled'],
                                         default = 'Disabled', type = 'str'),
                ipv4_static = dict (required = False, default = None, type = 'str'),
                ipv4_static_gw = dict (required = False, default = None, type = 'str'),
                ipv4_static_mask = dict (required = False, default = None, type = 'str'),
                ipv4_dns_from_dhcp = dict (required = False,
                                           choices = ['Enabled', 'Disabled'],
                                           default = 'Disabled', type = 'str'),
                ipv4_preferred_dns = dict (required = False, default = None, type = 'str'),
                ipv4_alternate_dns = dict (required = False, default = None, type = 'str'),

                # VLAN Settings
                vlan_enable = dict (required = False,
                                    choices = ['Enabled', 'Disabled'],
                                    default = 'Disabled', type = 'str'),
                vlan_id = dict (required = False, default = None, type = 'int'),
                vlan_priority = dict (required = False, default = None, type = 'int'),
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
