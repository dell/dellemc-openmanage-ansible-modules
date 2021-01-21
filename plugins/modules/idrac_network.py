#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.0.0
# Copyright (C) 2018-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_network
short_description: Configures the iDRAC network attributes
version_added: "2.1.0"
description:
    - This module allows to configure iDRAC network settings.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
  - dellemc.openmanage.network_share_options
options:
    setup_idrac_nic_vlan:
        type: str
        description: Allows to configure VLAN on iDRAC.
        choices: [Enabled, Disabled]
    register_idrac_on_dns:
        type: str
        description: Registers iDRAC on a Domain Name System (DNS).
        choices: [Enabled, Disabled]
    dns_idrac_name:
        type: str
        description: Name of the DNS to register iDRAC.
    auto_config:
        type: str
        description: Allows to enable or disable auto-provisioning to automatically acquire domain name from DHCP.
        choices: [Enabled, Disabled]
    static_dns:
        type: str
        description: Enter the static DNS domain name.
    vlan_id:
        type: int
        description: Enter the VLAN ID.  The VLAN ID must be a number from 1 through 4094.
    vlan_priority:
        type: int
        description: Enter the priority for the VLAN ID. The priority value must be a number from 0 through 7.
    enable_nic:
        type: str
        description: Allows to enable or disable the Network Interface Controller (NIC) used by iDRAC.
        choices: [Enabled, Disabled]
    nic_selection:
        type: str
        description: Select one of the available NICs.
        choices: [Dedicated, LOM1, LOM2, LOM3, LOM4]
    failover_network:
        type: str
        description: "Select one of the remaining LOMs. If a network fails, the traffic is routed through the failover
        network."
        choices: [ALL, LOM1, LOM2, LOM3, LOM4, T_None]
    auto_detect:
        type: str
        description: Allows to auto detect the available NIC types used by iDRAC.
        choices: [Enabled, Disabled]
    auto_negotiation:
        type: str
        description: Allows iDRAC to automatically set the duplex mode and network speed.
        choices: [Enabled, Disabled]
    network_speed:
        type: str
        description: Select the network speed for the selected NIC.
        choices: [T_10, T_100, T_1000]
    duplex_mode:
        type: str
        description: Select the type of data transmission for the NIC.
        choices: [Full, Half]
    nic_mtu:
        type: int
        description: Maximum Transmission Unit of the NIC.
    ip_address:
        type: str
        description: Enter a valid iDRAC static IPv4 address.
    enable_dhcp:
        type: str
        description: Allows to enable or disable Dynamic Host Configuration Protocol (DHCP) in iDRAC.
        choices: [Enabled, Disabled]
    enable_ipv4:
        type: str
        description: Allows to enable or disable IPv4 configuration.
        choices: [Enabled, Disabled]
    dns_from_dhcp:
        type: str
        description: Allows to enable DHCP to obtain DNS server address.
        choices: [Enabled, Disabled]
    static_dns_1:
        type: str
        description: Enter the preferred static DNS server IPv4 address.
    static_dns_2:
        type: str
        description: Enter the preferred static DNS server IPv4 address.
    static_gateway:
        type: str
        description: Enter the static IPv4 gateway address to iDRAC.
    static_net_mask:
        type: str
        description: Enter the static IP subnet mask to iDRAC.
requirements:
    - "omsdk"
    - "python >= 2.7.5"
author:
    - "Felix Stephen (@felixs88)"
    - "Anooja Vardhineni (@anooja-vardhineni)"
notes:
    - Run this module from a system that has direct access to DellEMC iDRAC.
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Configure iDRAC network settings
  dellemc.openmanage.idrac_network:
       idrac_ip:   "192.168.0.1"
       idrac_user: "user_name"
       idrac_password:  "user_password"
       share_name: "192.168.0.1:/share"
       share_password:  "share_pwd"
       share_user: "share_user"
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
       ip_address: "192.168.0.1"
       enable_dhcp: Enabled
       enable_ipv4: Enabled
       static_dns_1: "192.168.0.1"
       static_dns_2: "192.168.0.1"
       dns_from_dhcp: Enabled
       static_gateway: None
       static_net_mask: None
"""

RETURN = r'''
---
msg:
  description: Successfully configured the idrac network settings.
  returned: always
  type: str
  sample: "Successfully configured the idrac network settings."
network_status:
  description: Status of the Network settings operation job.
  returned: success
  type: dict
  sample: {
    "@odata.context": "/redfish/v1/$metadata#DellJob.DellJob",
    "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_856418531008",
    "@odata.type": "#DellJob.v1_0_2.DellJob",
    "CompletionTime": "2020-03-31T03:04:15",
    "Description": "Job Instance",
    "EndTime": null,
    "Id": "JID_856418531008",
    "JobState": "Completed",
    "JobType": "ImportConfiguration",
    "Message": "Successfully imported and applied Server Configuration Profile.",
    "MessageArgs": [],
    "MessageArgs@odata.count": 0,
    "MessageId": "SYS053",
    "Name": "Import Configuration",
    "PercentComplete": 100,
    "StartTime": "TIME_NOW",
    "Status": "Success",
    "TargetSettingsURI": null,
    "retval": true
}
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
      "code": "Base.1.0.GeneralError",
      "message": "A general error has occurred. See ExtendedInfo for more information.",
      "@Message.ExtendedInfo": [
        {
          "MessageId": "GEN1234",
          "RelatedProperties": [],
          "Message": "Unable to process the request because an error occurred.",
          "MessageArgs": [],
          "Severity": "Critical",
          "Resolution": "Retry the operation. If the issue persists, contact your system administrator."
        }
      ]
    }
  }
'''

import json
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection
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
    idrac.use_redfish = True
    upd_share = file_share_manager.create_share_obj(share_path=module.params['share_name'],
                                                    mount_point=module.params['share_mnt'],
                                                    isFolder=True,
                                                    creds=UserCredentials(
                                                        module.params['share_user'],
                                                        module.params['share_password'])
                                                    )

    idrac.config_mgr.set_liason_share(upd_share)
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
        msg = idrac.config_mgr.is_change_applicable()
    else:
        msg = idrac.config_mgr.apply_changes(reboot=False)
    return msg


# Main
def main():
    module = AnsibleModule(
        argument_spec={

            # iDRAC credentials
            "idrac_ip": {"required": True, "type": 'str'},
            "idrac_user": {"required": True, "type": 'str'},
            "idrac_password": {"required": True, "type": 'str', "aliases": ['idrac_pwd'], "no_log": True},
            "idrac_port": {"required": False, "default": 443, "type": 'int'},

            # Export Destination
            "share_name": {"required": True, "type": 'str'},
            "share_password": {"required": False, "type": 'str', "aliases": ['share_pwd'], "no_log": True},
            "share_user": {"required": False, "type": 'str'},
            "share_mnt": {"required": False, "type": 'str'},

            # setup DNS
            "register_idrac_on_dns": {"required": False, "choices": ['Enabled', 'Disabled'], "default": None},
            "dns_idrac_name": {"required": False, "default": None, "type": 'str'},
            "auto_config": {"required": False, "choices": ['Enabled', 'Disabled'], "default": None, 'type': 'str'},
            "static_dns": {"required": False, "default": None, "type": "str"},

            # set up idrac vlan
            "setup_idrac_nic_vlan": {"required": False, "choices": ['Enabled', 'Disabled']},
            "vlan_id": {"required": False, "type": 'int'},
            "vlan_priority": {"required": False, "type": 'int'},

            # set up NIC
            "enable_nic": {"required": False, "choices": ['Enabled', 'Disabled'], "default": None},
            "nic_selection": {"required": False, "choices": ['Dedicated', 'LOM1', 'LOM2', 'LOM3', 'LOM4'], "default": None},
            "failover_network": {"required": False, "choices": ['ALL', 'LOM1', 'LOM2', 'LOM3', 'LOM4', 'T_None'],
                                 "default": None},
            "auto_detect": {"required": False, "choices": ['Enabled', 'Disabled'], "default": None},
            "auto_negotiation": {"required": False, "choices": ['Enabled', 'Disabled'], "default": None},
            "network_speed": {"required": False, "choices": ['T_10', 'T_100', 'T_1000'], "default": None},
            "duplex_mode": {"required": False, "choices": ['Full', 'Half'], "default": None},
            "nic_mtu": {"required": False, 'type': 'int'},

            # setup iDRAC IPV4
            "ip_address": {"required": False, "default": None, "type": "str"},
            "enable_dhcp": {"required": False, "choices": ["Enabled", "Disabled"], "default": None},
            "enable_ipv4": {"required": False, "choices": ["Enabled", "Disabled"], "default": None},

            # setup iDRAC Static IPv4
            "dns_from_dhcp": {"required": False, "choices": ["Enabled", "Disabled"], "default": None},
            "static_dns_1": {"required": False, "default": None, "type": "str"},
            "static_dns_2": {"required": False, "default": None, "type": "str"},
            "static_gateway": {"required": False, "type": "str"},
            "static_net_mask": {"required": False, "type": "str"},
        },
        supports_check_mode=True)

    try:
        with iDRACConnection(module.params) as idrac:
            msg = run_idrac_network_config(idrac, module)
            changed, failed = False, False
            if msg.get('Status') == "Success":
                changed = True
                if msg.get('Message') == "No changes found to commit!":
                    changed = False
                if "No changes were applied" in msg.get('Message'):
                    changed = False
            elif msg.get('Status') == "Failed":
                failed = True
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError) as e:
        module.fail_json(msg=str(e))
    module.exit_json(msg="Successfully configured the idrac network settings.",
                     network_status=msg, changed=changed, failed=failed)


if __name__ == '__main__':
    main()
