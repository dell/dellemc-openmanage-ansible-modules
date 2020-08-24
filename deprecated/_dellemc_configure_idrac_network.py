#!/usr/bin/python
# _*_ coding: utf-8 _*_

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0
# Copyright (C) 2018-2019 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['deprecated'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_configure_idrac_network
short_description: Configures the iDRAC network attributes.
version_added: "2.3"
deprecated:
  removed_in: "3.2"
  why: Replaced with M(idrac_network).
  alternative: Use M(idrac_network) instead.
description:
    - This module is responsible for configuring the iDRAC network attributes.
options:
    idrac_ip:
        required: True
        description: iDRAC IP Address.
    idrac_user:
        required: True
        description: iDRAC username.
    idrac_password:
        required: True
        description: iDRAC user password.
        aliases: ['idrac_pwd']
    idrac_port:
        required: False
        description: iDRAC port.
        default: 443
    share_name:
        required: True
        description: Network share or a local path.
    share_user:
        required: False
        description: Network share user in the format 'user@domain' or 'domain\\user' if user is
            part of a domain else 'user'. This option is mandatory for CIFS Network Share.
    share_password:
        required: False
        description: Network share user password. This option is mandatory for CIFS Network Share.
        aliases: ['share_pwd']
    share_mnt:
        required: False
        description: Local mount path of the network share with read-write permission for ansible user.
            This option is mandatory for Network Share.
    setup_idrac_nic_vlan:
        required: False
        description: Configuring the VLAN related setting for iDRAC.
        choices: [Enabled, Disabled]
    register_idrac_on_dns:
        required: False
        description: Registering Domain Name System for iDRAC.
        choices: [Enabled, Disabled]
    dns_idrac_name:
        required: False
        description: DNS Name for iDRAC.
    auto_config:
        required: False
        description: Automatically creates the records for DNS.
        choices: [Enabled, Disabled]
    static_dns:
        required: False
        description: Static configuration for DNS.
    vlan_id:
        required: False
        description: Configuring the vlan id for iDRAC.
    vlan_priority:
        required: False
        description: Configuring the vlan priority for iDRAC.
    enable_nic:
        required: False
        description: Whether to Enable or Disable Network Interface Controller for iDRAC.
        choices: [Enabled, Disabled]
    nic_selection:
        required: False
        description: Selecting Network Interface Controller types for iDRAC.
        choices: [Dedicated, LOM1, LOM2, LOM3, LOM4]
    failover_network:
        required: False
        description: Failover Network Interface Controller types for iDRAC.
        choices: [ALL, LOM1, LOM2, LOM3, LOM4, T_None]
    auto_detect:
        required: False
        description: Auto detect Network Interface Controller types for iDRAC.
        choices: [Enabled, Disabled]
    auto_negotiation:
        required: False
        description: Auto negotiation of Network Interface Controller for iDRAC.
        choices: [Enabled, Disabled]
    network_speed:
        required: False
        description: Network speed for Network Interface Controller types for iDRAC.
        choices: [T_10, T_100, T_1000]
    duplex_mode:
        required: False
        description: Transmission of data Network Interface Controller types for iDRAC.
        choices: [Full, Half]
    nic_mtu:
        required: False
        description: NIC Maximum Transmission Unit.
    ip_address:
        required: False
        description: IP Address needs to be defined.
    enable_dhcp:
        required: False
        description: Whether to Enable or Disable DHCP Protocol for iDRAC.
        choices: [Enabled, Disabled]
    enable_ipv4:
        required: False
        description: Whether to Enable or Disable IPv4 configuration.
        choices: [Enabled, Disabled]
    dns_from_dhcp:
        required: False
        description: Specifying Domain Name Server from Dynamic Host Configuration Protocol.
        choices: [Enabled, Disabled]
    static_dns_1:
        required: False
        description: Needs to specify Domain Name Server Configuration.
    static_dns_2:
        required: False
        description: Needs to specify Domain Name Server configuration.
    static_gateway:
        required: False
        description: Interfacing the network with another protocol.
    static_net_mask:
        required: False
        description: Determine whether IP address belongs to host.
requirements:
    - "omsdk"
    - "python >= 2.7.5"
author: "Felix Stephen (@felixs88)"

"""

EXAMPLES = """
---
- name: Configure the iDRAC network attributes.
  dellemc_configure_idrac_network:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_password:  "xxxxxxxx"
       share_name: "xx.xx.xx.xx:/share"
       share_password:  "xxxxxxxx"
       share_user: "xxxx"
       share_mnt: "/mnt/share"
       register_idrac_on_dns: Enabled
       dns_idrac_name: None
       auto_config: None
       static_dns: None
       setup_idrac_nic_vlan: Enabled
       vlan_id: 0
       vlan_priority: 1
       enable_nic: Enabled
       nic_selection: Dedicated
       failover_network: T_None
       auto_detect: Disabled
       auto_negotiation: Enabled
       network_speed: T_1000
       duplex_mode: Full
       nic_mtu: 1500
       ip_address: "x.x.x.x"
       enable_dhcp: Enabled
       enable_ipv4: Enabled
       static_dns_1: "x.x.x.x"
       static_dns_2: "x.x.x.x"
       dns_from_dhcp: Enabled
       static_gateway: None
       static_net_mask: None
"""

RETURNS = """
dest:
    description: Configures the iDRAC network attributes.
    returned: success
    type: string
"""


from ansible.module_utils.remote_management.dellemc.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
try:
    from omdrivers.enums.iDRAC.iDRAC import (DNSRegister_NICTypes, DNSDomainFromDHCP_NICStaticTypes,
                                             Enable_NICTypes, VLanEnable_NICTypes,
                                             Selection_NICTypes, Failover_NICTypes,
                                             AutoDetect_NICTypes, Autoneg_NICTypes,
                                             Speed_NICTypes, Duplex_NICTypes, DHCPEnable_IPv4Types,
                                             DNSFromDHCP_IPv4Types, Enable_IPv4Types,
                                             DNSFromDHCP_IPv4StaticTypes)
    from omsdk.sdkfile import file_share_manager
    from omsdk.sdkcreds import UserCredentials
except ImportError:
    pass


def run_idrac_network_config(idrac, module):
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
        upd_share = file_share_manager.create_share_obj(share_path=module.params['share_name'],
                                                        mount_point=module.params['share_mnt'],
                                                        isFolder=True,
                                                        creds=UserCredentials(
                                                            module.params['share_user'],
                                                            module.params['share_password'])
                                                        )

        set_liason = idrac.config_mgr.set_liason_share(upd_share)
        if set_liason['Status'] == "Failed":
            try:
                message = set_liason['Data']['Message']
            except (IndexError, KeyError):
                message = set_liason['Message']
            err = True
            msg['msg'] = "{}".format(message)
            msg['failed'] = True
            return msg, err

        if module.params['register_idrac_on_dns'] is not None:
            idrac.config_mgr.configure_dns(
                register_idrac_on_dns=DNSRegister_NICTypes[module.params['register_idrac_on_dns']]
            )
        if module.params['dns_idrac_name'] is not None:
            idrac.config_mgr.configure_dns(
                dns_idrac_name=module.params['dns_idrac_name']
            )
        if module.params['auto_config'] is not None:
            idrac.config_mgr.configure_dns(
                auto_config=DNSDomainFromDHCP_NICStaticTypes[module.params['auto_config']]
            )
        if module.params['static_dns'] is not None:
            idrac.config_mgr.configure_dns(
                static_dns=module.params['static_dns']
            )

        if module.params['setup_idrac_nic_vlan'] is not None:
            idrac.config_mgr.configure_nic_vlan(
                vlan_enable=VLanEnable_NICTypes[module.params['setup_idrac_nic_vlan']]
            )
        if module.params['vlan_id'] is not None:
            idrac.config_mgr.configure_nic_vlan(
                vlan_id=module.params['vlan_id']
            )
        if module.params['vlan_priority'] is not None:
            idrac.config_mgr.configure_nic_vlan(
                vlan_priority=module.params['vlan_priority']
            )

        if module.params['enable_nic'] is not None:
            idrac.config_mgr.configure_network_settings(
                enable_nic=Enable_NICTypes[module.params['enable_nic']]
            )
        if module.params['nic_selection'] is not None:
            idrac.config_mgr.configure_network_settings(
                nic_selection=Selection_NICTypes[module.params['nic_selection']]
            )
        if module.params['failover_network'] is not None:
            idrac.config_mgr.configure_network_settings(
                failover_network=Failover_NICTypes[module.params['failover_network']]
            )
        if module.params['auto_detect'] is not None:
            idrac.config_mgr.configure_network_settings(
                auto_detect=AutoDetect_NICTypes[module.params['auto_detect']]
            )
        if module.params['auto_negotiation'] is not None:
            idrac.config_mgr.configure_network_settings(
                auto_negotiation=Autoneg_NICTypes[module.params['auto_negotiation']]
            )
        if module.params['network_speed'] is not None:
            idrac.config_mgr.configure_network_settings(
                network_speed=Speed_NICTypes[module.params['network_speed']]
            )
        if module.params['duplex_mode'] is not None:
            idrac.config_mgr.configure_network_settings(
                duplex_mode=Duplex_NICTypes[module.params['duplex_mode']]
            )
        if module.params['nic_mtu'] is not None:
            idrac.config_mgr.configure_network_settings(
                nic_mtu=module.params['nic_mtu']
            )

        if module.params['enable_dhcp'] is not None:
            idrac.config_mgr.configure_ipv4(
                enable_dhcp=DHCPEnable_IPv4Types[module.params["enable_dhcp"]]
            )
        if module.params['ip_address'] is not None:
            idrac.config_mgr.configure_ipv4(
                ip_address=module.params["ip_address"]
            )
        if module.params['enable_ipv4'] is not None:
            idrac.config_mgr.configure_ipv4(
                enable_ipv4=Enable_IPv4Types[module.params["enable_ipv4"]]
            )
        if module.params['dns_from_dhcp'] is not None:
            idrac.config_mgr.configure_static_ipv4(
                dns_from_dhcp=DNSFromDHCP_IPv4StaticTypes[module.params["dns_from_dhcp"]]
            )
        if module.params['static_dns_1'] is not None:
            idrac.config_mgr.configure_static_ipv4(
                dns_1=module.params["static_dns_1"]
            )
        if module.params['static_dns_2'] is not None:
            idrac.config_mgr.configure_static_ipv4(
                dns_2=module.params["static_dns_2"]
            )
        if module.params['static_gateway'] is not None:
            idrac.config_mgr.configure_static_ipv4(
                gateway=module.params["static_gateway"]
            )
        if module.params['static_net_mask'] is not None:
            idrac.config_mgr.configure_static_ipv4(
                net_mask=module.params["static_net_mask"]
            )

        if module.check_mode:
            msg['msg'] = idrac.config_mgr.is_change_applicable()
            if 'changes_applicable' in msg['msg']:
                msg['changed'] = msg['msg']['changes_applicable']
        else:
            msg['msg'] = idrac.config_mgr.apply_changes(reboot=False)
            if "Status" in msg['msg']:
                if msg['msg']['Status'] == "Success":
                    msg['changed'] = True
                    if "Message" in msg['msg']:
                        if msg['msg']['Message'] == "No changes found to commit!":
                            msg['changed'] = False
                        if "No changes were applied" in msg['msg']['Message']:
                            msg['changed'] = False
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
            idrac_password=dict(required=True,
                           type='str', aliases=['idrac_pwd'], no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Export Destination
            share_name=dict(required=True, type='str'),
            share_password=dict(required=False, type='str', aliases=['share_pwd'], no_log=True),
            share_user=dict(required=False, type='str'),
            share_mnt=dict(required=False, type='str'),

            # setup DNS
            register_idrac_on_dns=dict(required=False, choices=['Enabled', 'Disabled'],
                                       default=None),
            dns_idrac_name=dict(required=False, default=None, type='str'),
            auto_config=dict(required=False, choices=['Enabled', 'Disabled'],
                             default=None, type='str'),
            static_dns=dict(required=False, default=None, type="str"),

            # set up idrac vlan
            setup_idrac_nic_vlan=dict(required=False, choices=['Enabled', 'Disabled']),
            vlan_id=dict(required=False, type='int'),
            vlan_priority=dict(required=False, type='int'),

            # set up NIC
            enable_nic=dict(required=False, choices=['Enabled', 'Disabled'], default=None),
            nic_selection=dict(required=False, choices=['Dedicated', 'LOM1', 'LOM2', 'LOM3', 'LOM4'], default=None),
            failover_network=dict(required=False, choices=['ALL', 'LOM1', 'LOM2', 'LOM3', 'LOM4', 'T_None'],
                                  default=None),
            auto_detect=dict(required=False, choices=['Enabled', 'Disabled'], default=None),
            auto_negotiation=dict(required=False, choices=['Enabled', 'Disabled'], default=None),
            network_speed=dict(required=False, choices=['T_10', 'T_100', 'T_1000'], default=None),
            duplex_mode=dict(required=False, choices=['Full', 'Half'], default=None),
            nic_mtu=dict(required=False, type='int'),

            # setup iDRAC IPV4
            ip_address=dict(required=False, default=None, type="str"),
            enable_dhcp=dict(required=False, choices=["Enabled", "Disabled"], default=None),
            enable_ipv4=dict(required=False, choices=["Enabled", "Disabled"], default=None),

            # setup iDRAC Static IPv4
            dns_from_dhcp=dict(required=False, choices=["Enabled", "Disabled"], default=None),
            static_dns_1=dict(required=False, default=None, type="str"),
            static_dns_2=dict(required=False, default=None, type="str"),
            static_gateway=dict(required=False, type="str"),
            static_net_mask=dict(required=False, type="str"),

        ),

        supports_check_mode=True)
    module.deprecate("The 'dellemc_configure_idrac_network' module has been deprecated. "
                     "Use 'idrac_network' instead",
                     version=3.2)

    try:
        with iDRACConnection(module.params) as idrac:
            msg, err = run_idrac_network_config(idrac, module)
    except (ImportError, ValueError, RuntimeError) as e:
        module.fail_json(msg=str(e))

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
