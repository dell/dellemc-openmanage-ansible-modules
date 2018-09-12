#!/usr/bin/python
# _*_ coding: utf-8 _*_

#
# Dell EMC OpenManage Ansible Modules
# Version 1.0
# Copyright (C) 2018 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#


from __future__ import (absolute_import, division, print_function)


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_configure_idrac_network
short_description: Configures the iDRAC network attributes.
version_added: "2.3"
description:
    - This module is responsible for configuring the iDRAC network attributes.
options:
    idrac_ip:
        required: True
        description: iDRAC IP Address.
    idrac_user:
        required: True
        description: iDRAC username.
    idrac_pwd:
        required: True
        description: iDRAC user password.
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
    share_pwd:
        required: False
        description: Network share user password. This option is mandatory for CIFS Network Share.
    share_mnt:
        required: False
        description: Local mount path of the network share with read-write permission for ansible user.
            This option is mandatory for Network Share.
    setup_idrac_nic_vlan:
        required: False
        description: Configuring the VLAN related setting for iDRAC.
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
        default: None
    vlan_priority:
        required: False
        description: Configuring the vlan priority for iDRAC.
        default: None
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
        default: None
    ip_address:
        required: False
        description: IP Address needs to be defined.
    enable_dhcp:
        required: False
        description: Whether to Enable or Disable DHCP Protocol for iDRAC.
    dns_1:
        required: False
        description: Needs to specify Domain Name Server Configuration.
    dns_2:
        required: False
        description: Needs to specify Domain Name Server configuration.
    dns_from_dhcp:
        required: False
        description: Specifying Domain Name Server from Dynamic Host Configuration Protocol.
        choices: [Enabled, Disabled]
    enable_ipv4:
        required: False
        description: Whether to Enable or Disable IPv4 configuration.
        choices: [Enabled, Disabled]
    gateway:
        required: False
        description: iDRAC network gateway address.
        default: None
    net_mask:
        required: False
        description: iDRAC network netmask details.
        default: None
    static_dns_from_dhcp:
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
        default: None
    static_net_mask:
        required: False
        description: Determine whether IP address belongs to host.
        default: None
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
       idrac_pwd:  "xxxxxxxx"
       share_name: "xx.xx.xx.xx:/share"
       share_pwd:  "xxxxxxxx"
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
       dns_1: "x.x.x.x"
       dns_2: "x.x.x.x"
       dns_from_dhcp: Enabled
       enable_ipv4: Enabled
       gateway: None
       net_mask: None
       static_dns_1: "x.x.x.x"
       static_dns_2: "x.x.x.x"
       static_dns_from_dhcp: Enabled
       static_gateway: None
       static_net_mask: None
"""

RETURNS = """
dest:
    description: Configures the iDRAC network attributes.
    returned: success
    type: string
"""


from ansible.module_utils.dellemc_idrac import iDRACConnection, logger
from ansible.module_utils.basic import AnsibleModule
from omdrivers.enums.iDRAC.iDRAC import (DNSRegister_NICTypes, DNSDomainFromDHCP_NICStaticTypes,
                                         Enable_NICTypes, VLanEnable_NICTypes,
                                         Selection_NICTypes, Failover_NICTypes,
                                         AutoDetect_NICTypes, Autoneg_NICTypes,
                                         Speed_NICTypes, Duplex_NICTypes, DHCPEnable_IPv4Types,
                                         DNSFromDHCP_IPv4Types, Enable_IPv4Types,
                                         DNSFromDHCP_IPv4StaticTypes)
from omsdk.sdkfile import file_share_manager
from omsdk.sdkcreds import UserCredentials


def run_idrac_network_config(idrac, module):
    """
    Get Lifecycle Controller status

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    logger.info(module.params['idrac_ip'] + ': STARTING: iDRAC network configuration method')
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    err = False

    try:

        idrac.use_redfish = True
        logger.info(module.params['idrac_ip'] + ': CALLING: File on share OMSDK API')
        upd_share = file_share_manager.create_share_obj(share_path=module.params['share_name'],
                                                        mount_point=module.params['share_mnt'],
                                                        isFolder=True,
                                                        creds=UserCredentials(
                                                            module.params['share_user'],
                                                            module.params['share_pwd'])
                                                        )
        logger.info(module.params['idrac_ip'] + ': FINISHED: File on share OMSDK API')

        logger.info(module.params['idrac_ip'] + ': CALLING: Set liasion share OMSDK API')
        set_liason = idrac.config_mgr.set_liason_share(upd_share)
        if set_liason['Status'] == "Failed":
            try:
                message = set_liason['Data']['Message']
            except (IndexError, KeyError):
                message = set_liason['Message']
            err = True
            msg['msg'] = "{}".format(message)
            msg['failed'] = True
            logger.info(module.params['idrac_ip'] + ': FINISHED: {}'.format(message))
            return msg, err

        logger.info(module.params['idrac_ip'] + ': FINISHED: Set liasion share OMSDK API')

        logger.info(module.params['idrac_ip'] + ': CALLING: Register DNS on iDRAC')

        if module.params['register_idrac_on_dns'] != None:
            idrac.config_mgr.configure_dns(
                register_idrac_on_dns=DNSRegister_NICTypes[module.params['register_idrac_on_dns']]
            )
        if module.params['dns_idrac_name'] != None:
            idrac.config_mgr.configure_dns(
                dns_idrac_name=module.params['dns_idrac_name']
            )
        if module.params['auto_config'] != None:
            idrac.config_mgr.configure_dns(
                auto_config=DNSDomainFromDHCP_NICStaticTypes[module.params['auto_config']]
            )
        if module.params['static_dns'] != None:
            idrac.config_mgr.configure_dns(
                static_dns=module.params['static_dns']
            )
        logger.info(module.params['idrac_ip'] + ': FINISHED: Register DNS on iDRAC')

        logger.info(module.params['idrac_ip'] + ': CALLING: setup iDRAC vlan method')
        if module.params['setup_idrac_nic_vlan'] != None:
            idrac.config_mgr.configure_nic_vlan(
                vlan_enable=VLanEnable_NICTypes[module.params['setup_idrac_nic_vlan']]
            )
        if module.params['vlan_id'] != None:
            idrac.config_mgr.configure_nic_vlan(
                vlan_id=module.params['vlan_id']
            )
        if module.params['vlan_priority'] != None:
            idrac.config_mgr.configure_nic_vlan(
                vlan_priority=module.params['vlan_priority']
            )
        logger.info(module.params['idrac_ip'] + ': FINISHED: setup iDRAC vlan method')

        logger.info(module.params["idrac_ip"] + ': CALLING: Setup NIC for iDRAC')
        if module.params['enable_nic'] != None:
            idrac.config_mgr.configure_network_settings(
                enable_nic=Enable_NICTypes[module.params['enable_nic']]
            )
        if module.params['nic_selection'] != None:
            idrac.config_mgr.configure_network_settings(
                nic_selection=Selection_NICTypes[module.params['nic_selection']]
            )
        if module.params['failover_network'] != None:
            idrac.config_mgr.configure_network_settings(
                failover_network=Failover_NICTypes[module.params['failover_network']]
            )
        if module.params['auto_detect'] != None:
            idrac.config_mgr.configure_network_settings(
                auto_detect=AutoDetect_NICTypes[module.params['auto_detect']]
            )
        if module.params['auto_negotiation'] != None:
            idrac.config_mgr.configure_network_settings(
                auto_negotiation=Autoneg_NICTypes[module.params['auto_negotiation']]
            )
        if module.params['network_speed'] != None:
            idrac.config_mgr.configure_network_settings(
                network_speed=Speed_NICTypes[module.params['network_speed']]
            )
        if module.params['duplex_mode'] != None:
            idrac.config_mgr.configure_network_settings(
                duplex_mode=Duplex_NICTypes[module.params['duplex_mode']]
            )
        if module.params['nic_mtu'] != None:
            idrac.config_mgr.configure_network_settings(
                nic_mtu=module.params['nic_mtu']
            )
        logger.info(module.params['idrac_ip'] + ': FINISHED: Setup NIC for iDRAC')

        logger.info(module.params['idrac_ip'] + ': CALLING: Setup iDRAC IPv4 Configuration')

        if module.params['enable_dhcp'] != None:
            idrac.config_mgr.configure_ipv4(
                enable_dhcp=DHCPEnable_IPv4Types[module.params["enable_dhcp"]]
            )
        if module.params['ip_address'] != None:
            idrac.config_mgr.configure_ipv4(
                ip_address=module.params["ip_address"]
            )
        if module.params['dns_1'] != None:
            idrac.config_mgr.configure_ipv4(
                dns_1=module.params["dns_1"]
            )
        if module.params['dns_2'] != None:
            idrac.config_mgr.configure_ipv4(
                dns_2=module.params["dns_2"]
            )
        if module.params['dns_from_dhcp'] != None:
            idrac.config_mgr.configure_ipv4(
                dns_from_dhcp=DNSFromDHCP_IPv4Types[module.params["dns_from_dhcp"]]
            )
        if module.params['enable_ipv4'] != None:
            idrac.config_mgr.configure_ipv4(
                enable_ipv4=Enable_IPv4Types[module.params["enable_ipv4"]]
            )
        if module.params['gateway'] != None:
            idrac.config_mgr.configure_ipv4(
                gateway=module.params["gateway"]
            )
        if module.params['net_mask'] != None:
            idrac.config_mgr.configure_ipv4(
                net_mask=module.params["net_mask"]
            )
        logger.info(module.params['idrac_ip'] + ': FINISHED: Setup iDRAC IPv4 configuration')

        logger.info(module.params["idrac_ip"] + ': CALLING: Setup iDRAC IPv4 Static configuration')
        if module.params['static_dns_from_dhcp'] != None:
            idrac.config_mgr.configure_static_ipv4(
                dns_from_dhcp=DNSFromDHCP_IPv4StaticTypes[module.params["static_dns_from_dhcp"]]
            )
        if module.params['static_dns_1'] != None:
            idrac.config_mgr.configure_static_ipv4(
                dns_1=module.params["static_dns_1"]
            )
        if module.params['static_dns_2'] != None:
            idrac.config_mgr.configure_static_ipv4(
                dns_2=module.params["static_dns_2"]
            )
        if module.params['static_gateway'] != None:
            idrac.config_mgr.configure_static_ipv4(
                gateway=module.params["static_gateway"]
            )
        if module.params['static_net_mask'] != None:
            idrac.config_mgr.configure_static_ipv4(
                net_mask=module.params["static_net_mask"]
            )

        if module.check_mode:
            msg['msg'] = idrac.config_mgr.is_change_applicable()
            if 'changes_applicable' in msg['msg']:
                msg['changed'] = msg['msg']['changes_applicable']
        else:
            logger.info(module.params["idrac_ip"] + ':FINISHED: Setup iDRAC IPv4 Static configuration')
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
        logger.error(module.params['idrac_ip'] + ': EXCEPTION: iDRAC network configuration method')
    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC network configuration method')
    return msg, err


# Main
def main():
    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC Handle
            idrac=dict(required=False, type='dict'),

            # iDRAC credentials
            idrac_ip=dict(required=True, default=None, type='str'),
            idrac_user=dict(required=True, default=None, type='str'),
            idrac_pwd=dict(required=True, default=None,
                           type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Export Destination
            share_name=dict(required=True, type='str'),
            share_pwd=dict(required=False, type='str', no_log=True),
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
            setup_idrac_nic_vlan=dict(required=False, choices=['Enabled', 'Disabled'], default=None),
            vlan_id=dict(required=False, default=None, type='int'),
            vlan_priority=dict(required=False, default=None, type='int'),

            # set up NIC
            enable_nic=dict(required=False, choices=['Enabled', 'Disabled'], default=None),
            nic_selection=dict(required=False, choices=['Dedicated', 'LOM1', 'LOM2', 'LOM3', 'LOM4'], default=None),
            failover_network=dict(required=False, choices=['ALL', 'LOM1', 'LOM2', 'LOM3', 'LOM4', 'T_None'],
                                  default=None),
            auto_detect=dict(required=False, choices=['Enabled', 'Disabled'], default=None),
            auto_negotiation=dict(required=False, choices=['Enabled', 'Disabled'], default=None),
            network_speed=dict(required=False, choices=['T_10', 'T_100', 'T_1000'], default=None),
            duplex_mode=dict(required=False, choices=['Full', 'Half'], default=None),
            nic_mtu=dict(required=False, default=None, type='int'),

            # setup iDRAC IPV4
            ip_address=dict(required=False, default=None, type="str"),
            enable_dhcp=dict(required=False, choices=["Enabled", "Disabled"], default=None),
            dns_1=dict(required=False, default=None, type="str"),
            dns_2=dict(required=False, default=None, type="str"),
            dns_from_dhcp=dict(required=False, choices=["Enabled", "Disabled"], default=None),
            enable_ipv4=dict(required=False, choices=["Enabled", "Disabled"], default=None),
            gateway=dict(required=False, default=None, type="str"),
            net_mask=dict(required=False, default=None, type="str"),

            # setup iDRAC Static IPv4
            static_dns_from_dhcp=dict(required=False, choices=["Enabled", "Disabled"], default=None),
            static_dns_1=dict(required=False, default=None, type="str"),
            static_dns_2=dict(required=False, default=None, type="str"),
            static_gateway=dict(required=False, default=None, type="str"),
            static_net_mask=dict(required=False, default=None, type="str"),

        ),

        supports_check_mode=True)
    logger.info(module.params['idrac_ip'] + ': CALLING: iDRAC Server Configuration')
    # Connect to iDRAC
    logger.info(module.params['idrac_ip'] + ': CALLING: iDRAC Connection')
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Connection is successful')
    # Export Server Configuration Profile
    msg, err = run_idrac_network_config(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)
    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Server Configuration')


if __name__ == '__main__':
    main()
