#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2021-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
---
module: ome_device_mgmt_network
short_description: Configure network settings of devices on OpenManage Enterprise Modular
description: This module allows to configure network settings on Chassis, Servers, and I/O Modules on OpenManage Enterprise Modular.
version_added: 4.2.0
author:
  - Jagadeesh N V(@jagadeeshnv)
extends_documentation_fragment:
  - dellemc.openmanage.omem_auth_options
options:
  device_service_tag:
    description:
      - Service tag of the device.
      - This option is mutually exclusive with I(device_id).
    type: str
  device_id:
    description:
      - ID of the device.
      - This option is mutually exclusive with I(device_service_tag).
    type: int
  enable_nic:
    description:
      - Enable or disable Network Interface Card (NIC) configuration of the device.
      - This option is not applicable to I/O Module.
    type: bool
    default: true
  delay:
    description:
      - The time in seconds, after which settings are applied.
      - This option is applicable only for Chassis.
    type: int
    default: 0
  ipv4_configuration:
    description:
      - IPv4 network configuration.
      - "C(WARNING) Ensure that you have an alternate interface to access OpenManage Enterprise Modular because these
      options can change the current IPv4 address for I(hostname)."
    type: dict
    suboptions:
      enable_ipv4:
        description:
          - Enable or disable access to the network using IPv4.
        type: bool
        required: true
      enable_dhcp:
        description:
          - "Enable or disable the automatic request to obtain an IPv4 address from the IPv4 Dynamic Host Configuration
          Protocol (DHCP) server."
          - "C(NOTE) If this option is C(true), the values provided for I(static_ip_address), I(static_subnet_mask),
          and I(static_gateway) are not applied for these fields. However, the module may report changes."
        type: bool
      static_ip_address:
        description:
          - Static IPv4 address
          - This option is applicable when I(enable_dhcp) is false.
        type: str
      static_subnet_mask:
        description:
          - Static IPv4 subnet mask address
          - This option is applicable when I(enable_dhcp) is false.
        type: str
      static_gateway:
        description:
          - Static IPv4 gateway address
          - This option is applicable when I(enable_dhcp) is false.
        type: str
      use_dhcp_to_obtain_dns_server_address:
        description:
          - This option allows to automatically request and obtain IPv4 address for the DNS Server from the DHCP server.
          - This option is applicable when I(enable_dhcp) is true.
          - "C(NOTE) If this option is C(true), the values provided for I(static_preferred_dns_server) and
          I(static_alternate_dns_server) are not applied for these fields. However, the module may report changes."
        type: bool
      static_preferred_dns_server:
        description:
          - Static IPv4 DNS preferred server
          - This option is applicable when I(use_dhcp_for_dns_server_names) is false.
        type: str
      static_alternate_dns_server:
        description:
          - Static IPv4 DNS alternate server
          - This option is applicable when I(use_dhcp_for_dns_server_names) is false.
        type: str
  ipv6_configuration:
    description:
      - IPv6 network configuration.
      - "C(WARNING) Ensure that you have an alternate interface to access OpenManage Enterprise Modular because these options can
      change the current IPv6 address for I(hostname)."
    type: dict
    suboptions:
      enable_ipv6:
        description: Enable or disable access to the network using the IPv6.
        type: bool
        required: true
      enable_auto_configuration:
        description:
          - "Enable or disable the automatic request to obtain an IPv6 address from the IPv6 DHCP server or router
          advertisements(RA)"
          - "If I(enable_auto_configuration) is C(true), OpenManage Enterprise Modular retrieves IP configuration
          (IPv6 address, prefix, and gateway address) from a DHCPv6 server on the existing network."
          - "C(NOTE) If this option is C(true), the values provided for I(static_ip_address), I(static_prefix_length),
          and I(static_gateway) are not applied for these fields. However, the module may report changes."
        type: bool
      static_ip_address:
        description:
          - Static IPv6 address
          - This option is applicable when I(enable_auto_configuration) is false.
        type: str
      static_prefix_length:
        description:
          - Static IPv6 prefix length
          - This option is applicable when I(enable_auto_configuration) is false.
        type: int
      static_gateway:
        description:
          - Static IPv6 gateway address
          - This option is applicable when I(enable_auto_configuration) is false.
        type: str
      use_dhcpv6_to_obtain_dns_server_address:
        description:
          - This option allows to automatically request and obtain a IPv6 address for the DNS server from the DHCP server.
          - This option is applicable when I(enable_auto_configuration) is true
          - "C(NOTE) If this option is C(true), the values provided for I(static_preferred_dns_server) and I(static_alternate_dns_server)
          are not applied for these fields. However, the module may report changes."
        type: bool
      static_preferred_dns_server:
        description:
          - Static IPv6 DNS preferred server
          - This option is applicable when I(use_dhcp_for_dns_server_names) is false.
        type: str
      static_alternate_dns_server:
        description:
          - Static IPv6 DNS alternate server
          - This option is applicable when I(use_dhcp_for_dns_server_names) is false.
        type: str
  management_vlan:
    description:
      - VLAN configuration.
    type: dict
    suboptions:
      enable_vlan:
        description:
          - Enable or disable VLAN for management.
          - The VLAN configuration cannot be updated if the I(register_with_dns) field under I(dns_configuration) is true.
          - "C(WARNING) Ensure that the network cable is connected to the correct port after the VLAN configuration
          is changed. If not, the VLAN configuration changes may not be applied."
        required: true
        type: bool
      vlan_id:
        description:
          - VLAN ID.
          - "The valid VLAN IDs are: 1 to 4000, and 4021 to 4094."
          - This option is applicable when I(enable_vlan) is true.
        type: int
  dns_configuration:
    description: Domain Name System(DNS) settings.
    type: dict
    suboptions:
      register_with_dns:
        description:
          - Register/Unregister I(dns_name) on the DNS Server.
          - C(WARNING) This option cannot be updated if VLAN configuration changes.
        type: bool
      use_dhcp_for_dns_domain_name:
        description: Get the I(dns_domain_name) using a DHCP server.
        type: bool
      dns_name:
        description:
          - DNS name for I(hostname)
          - This is applicable when I(register_with_dns) is true.
        type: str
      dns_domain_name:
        description:
          - Static DNS domain name
          - This is applicable when I(use_dhcp_for_dns_domain_name) is false.
        type: str
      auto_negotiation:
        description:
          - Enables or disables the auto negation of the network speed.
          - "C(NOTE): Setting I(auto_negotiation) to false and choosing a network port speed may result in the chassis
          loosing link to the top of rack network switch, or to the neighboring chassis in case of MCM mode. It is
          recommended that the I(auto_negotiation) is set to C(true) for most use cases."
          - This is applicable when I(use_dhcp_for_dns_domain_name) is false.
          - This is applicable only for Chassis.
        type: bool
      network_speed:
        description:
          - The speed of the network port.
          - This is applicable when I(auto_negotiation) is false.
          - C(10_MB) to select network speed of 10 MB.
          - C(100_MB) to select network speed of 100 MB.
          - This is applicable only for Chassis.
        choices:
          - 10_MB
          - 100_MB
        type: str
  dns_server_settings:
    description:
      - DNS server settings.
      - This is applicable only for I/O Module.
    type: dict
    suboptions:
      preferred_dns_server:
        description:
          - Enter the IP address of the preferred DNS server.
        type: str
      alternate_dns_server1:
        description:
          - Enter the IP address of the first alternate DNS server.
        type: str
      alternate_dns_server2:
        description:
          - Enter the IP address of the second alternate DNS server.
        type: str
requirements:
  - "python >= 3.9.6"
notes:
  - Run this module from a system that has direct access to Dell OpenManage Enterprise Modular.
  - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Network settings for chassis
  dellemc.openmanage.ome_device_mgmt_network:
    hostname: 192.168.0.1
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_service_tag: CHAS123
    ipv4_configuration:
      enable_ipv4: true
      enable_dhcp: false
      static_ip_address: 192.168.0.2
      static_subnet_mask: 255.255.254.0
      static_gateway: 192.168.0.3
      use_dhcp_to_obtain_dns_server_address: false
      static_preferred_dns_server: 192.168.0.4
      static_alternate_dns_server: 192.168.0.5
    ipv6_configuration:
      enable_ipv6: true
      enable_auto_configuration: false
      static_ip_address: 2626:f2f2:f081:9:1c1c:f1f1:4747:1
      static_prefix_length: 10
      static_gateway: ffff::2607:f2b1:f081:9
      use_dhcpv6_to_obtain_dns_server_address: false
      static_preferred_dns_server: 2626:f2f2:f081:9:1c1c:f1f1:4747:3
      static_alternate_dns_server: 2626:f2f2:f081:9:1c1c:f1f1:4747:4
    dns_configuration:
      register_with_dns: true
      use_dhcp_for_dns_domain_name: false
      dns_name: "MX-SVCTAG"
      dns_domain_name: "dnslocaldomain"
      auto_negotiation: false
      network_speed: 100_MB

- name: Network settings for server
  dellemc.openmanage.ome_device_mgmt_network:
    hostname: 192.168.0.1
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_service_tag: SRVR123
    ipv4_configuration:
      enable_ipv4: true
      enable_dhcp: false
      static_ip_address: 192.168.0.2
      static_subnet_mask: 255.255.254.0
      static_gateway: 192.168.0.3
      use_dhcp_to_obtain_dns_server_address: false
      static_preferred_dns_server: 192.168.0.4
      static_alternate_dns_server: 192.168.0.5
    ipv6_configuration:
      enable_ipv6: true
      enable_auto_configuration: false
      static_ip_address: 2626:f2f2:f081:9:1c1c:f1f1:4747:1
      static_prefix_length: 10
      static_gateway: ffff::2607:f2b1:f081:9
      use_dhcpv6_to_obtain_dns_server_address: false
      static_preferred_dns_server: 2626:f2f2:f081:9:1c1c:f1f1:4747:3
      static_alternate_dns_server: 2626:f2f2:f081:9:1c1c:f1f1:4747:4

- name: Network settings for I/O module
  dellemc.openmanage.ome_device_mgmt_network:
    hostname: 192.168.0.1
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_service_tag: IOM1234
    ipv4_configuration:
      enable_ipv4: true
      enable_dhcp: false
      static_ip_address: 192.168.0.2
      static_subnet_mask: 255.255.254.0
      static_gateway: 192.168.0.3
    ipv6_configuration:
      enable_ipv6: true
      enable_auto_configuration: false
      static_ip_address: 2626:f2f2:f081:9:1c1c:f1f1:4747:1
      static_prefix_length: 10
      static_gateway: ffff::2607:f2b1:f081:9
    dns_server_settings:
      preferred_dns_server: 192.168.0.4
      alternate_dns_server1: 192.168.0.5

- name: Management VLAN configuration of chassis using device id
  dellemc.openmanage.ome_device_mgmt_network:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_id: 12345
    management_vlan:
      enable_vlan: true
      vlan_id: 2345
    dns_configuration:
      register_with_dns: false
"""

RETURN = """
---
msg:
  type: str
  description: Overall status of the network config operation.
  returned: always
  sample: Successfully applied the network settings.
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
                "MessageId": "CGEN1004",
                "RelatedProperties": [],
                "Message": "Unable to complete the request because IPV4 Settings Capability is not Supported does not
                exist or is not applicable for the resource URI.",
                "MessageArgs": [
                    "IPV4 Settings Capability is not Supported"
                ],
                "Severity": "Critical",
                "Resolution": "Check the request resource URI. Refer to the OpenManage Enterprise-Modular User's Guide
                for more information about resource URI and its properties."
            }
        ]
    }
}
"""

import json
import socket
import copy
from ssl import SSLError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.common.dict_transformations import recursive_diff

DEVICE_URI = "DeviceService/Devices"
MGMT_DOMAIN = "ManagementDomainService/Domains"
LEAD_CONFIG = "ApplicationService/Network/AddressConfiguration"
NETWORK_SETTINGS = "DeviceService/Devices({0})/Settings('Network')"
DEVICE_NOT_FOUND = "Device with {0} '{1}' not found."
NON_CONFIG_NETWORK = "Network settings for {0} is not configurable."
SUCCESS_MSG = "Successfully applied the network settings."
INVALID_IP = "Invalid {0} address provided for the {1}"
DNS_SETT_ERR1 = "'SecondaryDNS' requires 'PrimaryDNS' to be provided."
DNS_SETT_ERR2 = "'TertiaryDNS' requires both 'PrimaryDNS' and 'SecondaryDNS' to be provided."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
SERVER = 1000
CHASSIS = 2000
IO_MODULE = 4000
API_TIMEOUT = 120


def validate_ip_address(address):
    try:
        socket.inet_aton(address)
    except socket.error:
        return False
    return address.count('.') == 3


def validate_ip_v6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:
        return False
    return True


def validate_ipaddress(module, ip_type, config, var_list, ip_func):
    ipv_input = module.params.get(config)
    if ipv_input:
        for ipname in var_list:
            val = ipv_input.get(ipname)
            if val and not ip_func(val):
                module.fail_json(msg=INVALID_IP.format(ip_type, ipname))
    return


def validate_input(module):
    ip_addr = ["static_ip_address", "static_gateway", "static_preferred_dns_server", "static_alternate_dns_server"]
    validate_ipaddress(module, "IPv6", "ipv6_configuration", ip_addr, validate_ip_v6_address)
    ip_addr.append("static_subnet_mask")
    validate_ipaddress(module, "IPv4", "ipv4_configuration", ip_addr, validate_ip_address)
    ipv6 = module.params.get("ipv6_configuration")
    dns_settings = module.params.get("dns_server_settings")
    if dns_settings:
        for k, v in dns_settings.items():
            if v is not None:
                if not validate_ip_address(v) and not validate_ip_v6_address(v):
                    module.fail_json(msg=INVALID_IP.format("IP", k))
    # int to str
    if ipv6 and ipv6.get("static_prefix_length"):
        ipv6["static_prefix_length"] = str(ipv6["static_prefix_length"])
    vlan = module.params.get("management_vlan")
    if vlan and vlan.get("vlan_id"):
        vlan["vlan_id"] = str(vlan["vlan_id"])
    return


def get_device_details(module, rest_obj):
    id = module.params.get('device_id')
    srch = 'Id'
    query_param = {"$filter": "{0} eq {1}".format(srch, id)}
    if not id:
        id = module.params.get('device_service_tag')
        srch = 'Identifier'
        query_param = {"$filter": "{0} eq '{1}'".format(srch, id)}
    resp = rest_obj.invoke_request('GET', DEVICE_URI, query_param=query_param)
    if resp.success and resp.json_data.get('value'):
        tlist = resp.json_data.get('value', [])
        for xtype in tlist:
            if xtype.get(srch) == id:
                dvc = xtype
                return dvc
    module.fail_json(msg=DEVICE_NOT_FOUND.format(srch, id))


def transform_diff(params, translator, sub_payload, bool_trans=None):
    df = {}
    inp_dict = {}
    for k, v in translator.items():
        inp = params.get(k)
        if inp is not None:
            if isinstance(inp, bool) and bool_trans:
                inp = bool_trans.get(inp)
            inp_dict[v] = inp
    id_diff = recursive_diff(inp_dict, sub_payload)
    if id_diff and id_diff[0]:
        df = id_diff[0]
        sub_payload.update(inp_dict)
    return df


def validate_dependency(mparams):
    params = copy.deepcopy(mparams)
    ipv4 = params.get('ipv4_configuration')
    if ipv4:
        rm_list = []
        dhcp = ["static_preferred_dns_server", "static_alternate_dns_server"]
        static = ["static_ip_address", "static_gateway", "static_subnet_mask"]
        bools = ["enable_dhcp", "use_dhcp_to_obtain_dns_server_address"]
        if ipv4.get("use_dhcp_to_obtain_dns_server_address") is True:
            rm_list.extend(dhcp)
        if ipv4.get("enable_dhcp") is True:
            rm_list.extend(static)
        if ipv4.get("enable_ipv4") is False:
            rm_list.extend(dhcp)
            rm_list.extend(static)
            rm_list.extend(bools)
        for prm in rm_list:
            ipv4.pop(prm, None)
    ipv6 = params.get('ipv6_configuration')
    if ipv6:
        rm_list = []
        dhcp = ["static_preferred_dns_server", "static_alternate_dns_server"]
        static = ["static_ip_address", "static_gateway", "static_prefix_length"]
        bools = ["enable_auto_configuration", "use_dhcpv6_to_obtain_dns_server_address"]
        if ipv6.get("use_dhcpv6_to_obtain_dns_server_address") is True:
            rm_list.extend(dhcp)
        if ipv6.get("enable_auto_configuration") is True:
            rm_list.extend(static)
        if ipv6.get("enable_ipv6") is False:
            rm_list.extend(dhcp)
            rm_list.extend(static)
            rm_list.extend(bools)
        for prm in rm_list:
            ipv6.pop(prm, None)
    vlan = params.get('management_vlan')
    if vlan:
        if vlan.get('enable_vlan') is False:
            vlan.pop('vlan_id', None)
    dns = params.get('dns_configuration')
    if dns:
        if dns.get('auto_negotiation') is True:
            dns.pop('network_speed', None)
        if dns.get('use_dhcp_for_dns_domain_name') is True:
            dns.pop('dns_domain_name', None)
    return params


def update_chassis_payload(module, payload):
    ipv4 = {
        "enable_dhcp": "EnableDHCP",
        "enable_ipv4": "EnableIPv4",
        "static_alternate_dns_server": "StaticAlternateDNSServer",
        "static_gateway": "StaticGateway",
        "static_ip_address": "StaticIPAddress",
        "static_preferred_dns_server": "StaticPreferredDNSServer",
        "static_subnet_mask": "StaticSubnetMask",
        "use_dhcp_to_obtain_dns_server_address": "UseDHCPObtainDNSServerAddresses"
    }
    ipv6 = {
        "enable_auto_configuration": "EnableAutoconfiguration",
        "enable_ipv6": "EnableIPv6",
        "static_alternate_dns_server": "StaticAlternateDNSServer",
        "static_gateway": "StaticGateway",
        "static_ip_address": "StaticIPv6Address",
        "static_preferred_dns_server": "StaticPreferredDNSServer",
        "static_prefix_length": "StaticPrefixLength",
        "use_dhcpv6_to_obtain_dns_server_address": "UseDHCPv6ObtainDNSServerAddresses"
    }
    dns = {
        "auto_negotiation": "AutoNegotiation",
        "dns_domain_name": "DnsDomainName",
        "dns_name": "DnsName",
        "network_speed": "NetworkSpeed",
        "register_with_dns": "RegisterDNS",
        "use_dhcp_for_dns_domain_name": "UseDHCPForDomainName"
    }
    vlan = {"enable_vlan": "EnableVLAN", "vlan_id": "MgmtVLANId"}
    gnrl = payload.get('GeneralSettings')  # where enable NIC is present
    diff = {}
    mparams = validate_dependency(module.params)
    enable_nic = mparams.get('enable_nic')
    delay = mparams.get('delay')
    if enable_nic:
        if mparams.get('ipv4_configuration'):
            df = transform_diff(mparams.get('ipv4_configuration'), ipv4, payload.get('Ipv4Settings'))
            diff.update(df)
        if mparams.get('ipv6_configuration'):
            df = transform_diff(mparams.get('ipv6_configuration'), ipv6, payload.get('Ipv6Settings'))
            diff.update(df)
        if mparams.get('dns_configuration'):
            df = transform_diff(mparams.get('dns_configuration'), dns, payload.get('GeneralSettings'))
            diff.update(df)
        if mparams.get('management_vlan'):
            df = transform_diff(mparams.get('management_vlan'), vlan, payload)
            diff.update(df)
    if gnrl.get('EnableNIC') != enable_nic:
        gnrl['EnableNIC'] = enable_nic
        diff.update({'EnableNIC': enable_nic})
    if delay != gnrl.get('Delay'):
        gnrl['Delay'] = delay
        diff.update({'Delay': delay})
    return diff


def update_server_payload(module, payload):
    ipv4 = {
        "enable_dhcp": "enableDHCPIPv4",
        "enable_ipv4": "enableIPv4",
        "static_alternate_dns_server": "staticAlternateDNSIPv4",
        "static_gateway": "staticGatewayIPv4",
        "static_ip_address": "staticIPAddressIPv4",
        "static_preferred_dns_server": "staticPreferredDNSIPv4",
        "static_subnet_mask": "staticSubnetMaskIPv4",
        "use_dhcp_to_obtain_dns_server_address": "useDHCPToObtainDNSIPv4"
    }
    ipv6 = {
        "enable_auto_configuration": "enableAutoConfigurationIPv6",
        "enable_ipv6": "enableIPv6",
        "static_alternate_dns_server": "staticAlternateDNSIPv6",
        "static_gateway": "staticGatewayIPv6",
        "static_ip_address": "staticIPAddressIPv6",
        "static_preferred_dns_server": "staticPreferredDNSIPv6",
        "static_prefix_length": "staticPrefixLengthIPv6",
        "use_dhcpv6_to_obtain_dns_server_address": "useDHCPToObtainDNSIPv6"
    }
    vlan = {"enable_vlan": "vlanEnable", "vlan_id": "vlanId"}
    diff = {}
    mparams = validate_dependency(module.params)
    enable_nic = mparams.get('enable_nic')
    bool_trans = {True: 'Enabled', False: 'Disabled'}
    if enable_nic:
        if mparams.get('ipv4_configuration'):
            df = transform_diff(mparams.get('ipv4_configuration'), ipv4, payload, bool_trans)
            diff.update(df)
        if mparams.get('ipv6_configuration'):
            df = transform_diff(mparams.get('ipv6_configuration'), ipv6, payload, bool_trans)
            diff.update(df)
        if mparams.get('management_vlan'):
            df = transform_diff(mparams.get('management_vlan'), vlan, payload, bool_trans)
            diff.update(df)
    enable_nic = bool_trans.get(enable_nic)
    if payload.get('enableNIC') != enable_nic:
        payload['enableNIC'] = enable_nic
        diff.update({'enableNIC': enable_nic})
    return diff


def update_iom_payload(module, payload):
    ipv4 = {
        "enable_dhcp": "EnableDHCP",
        "enable_ipv4": "EnableIPv4",
        "static_gateway": "StaticGateway",
        "static_ip_address": "StaticIPAddress",
        "static_subnet_mask": "StaticSubnetMask",
    }
    ipv6 = {
        "enable_ipv6": "EnableIPv6",
        "static_gateway": "StaticGateway",
        "static_ip_address": "StaticIPv6Address",
        "static_prefix_length": "StaticPrefixLength",
        "enable_auto_configuration": "UseDHCPv6"
    }
    dns = {"preferred_dns_server": "PrimaryDNS",
           "alternate_dns_server1": "SecondaryDNS",
           "alternate_dns_server2": "TertiaryDNS"}
    vlan = {"enable_vlan": "EnableMgmtVLANId", "vlan_id": "MgmtVLANId"}
    diff = {}
    mparams = validate_dependency(module.params)
    if mparams.get('ipv4_configuration'):
        df = transform_diff(mparams.get('ipv4_configuration'), ipv4, payload.get('IomIPv4Settings'))
        diff.update(df)
    if mparams.get('ipv6_configuration'):
        df = transform_diff(mparams.get('ipv6_configuration'), ipv6, payload.get('IomIPv6Settings'))
        diff.update(df)
    if mparams.get('management_vlan'):
        df = transform_diff(mparams.get('management_vlan'), vlan, payload)
        diff.update(df)
    if mparams.get('dns_server_settings'):
        df = transform_diff(mparams.get('dns_server_settings'), dns, payload.get('IomDNSSettings'))
        dns_iom = payload.get('IomDNSSettings')
        if dns_iom.get("SecondaryDNS") and not dns_iom.get("PrimaryDNS"):
            module.fail_json(msg=DNS_SETT_ERR1)
        if dns_iom.get("TertiaryDNS") and (not dns_iom.get("PrimaryDNS") or not dns_iom.get("SecondaryDNS")):
            module.fail_json(msg=DNS_SETT_ERR2)
        diff.update(df)
    return diff


def get_network_payload(module, rest_obj, dvc):
    resp = rest_obj.invoke_request('GET', NETWORK_SETTINGS.format(dvc.get('Id')))
    got_payload = resp.json_data
    payload = rest_obj.strip_substr_dict(got_payload)
    update_dict = {
        CHASSIS: update_chassis_payload,
        SERVER: update_server_payload,
        IO_MODULE: update_iom_payload
    }
    diff = update_dict[dvc.get('Type')](module, payload)
    # module.warn(json.dumps(diff))
    if not diff:
        module.exit_json(msg=NO_CHANGES_MSG)
    if module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    return payload


def main():
    ipv4_options = {"enable_ipv4": {"required": True, "type": 'bool'},
                    "enable_dhcp": {"type": 'bool'},
                    "static_ip_address": {"type": 'str'},
                    "static_subnet_mask": {"type": 'str'},
                    "static_gateway": {"type": 'str'},
                    "use_dhcp_to_obtain_dns_server_address": {"type": 'bool'},
                    "static_preferred_dns_server": {"type": 'str'},
                    "static_alternate_dns_server": {"type": 'str'}}
    ipv6_options = {"enable_ipv6": {"required": True, "type": 'bool'},
                    "enable_auto_configuration": {"type": 'bool'},
                    "static_ip_address": {"type": 'str'},
                    "static_prefix_length": {"type": 'int'},
                    "static_gateway": {"type": 'str'},
                    "use_dhcpv6_to_obtain_dns_server_address": {"type": 'bool'},
                    "static_preferred_dns_server": {"type": 'str'},
                    "static_alternate_dns_server": {"type": 'str'}}
    dns_options = {"register_with_dns": {"type": 'bool'},
                   "use_dhcp_for_dns_domain_name": {"type": 'bool'},
                   "dns_name": {"type": 'str'},
                   "dns_domain_name": {"type": 'str'},
                   "auto_negotiation": {"type": 'bool'},
                   "network_speed": {"type": 'str', "choices": ['10_MB', '100_MB']}}
    management_vlan = {"enable_vlan": {"required": True, "type": 'bool'},
                       "vlan_id": {"type": 'int'}}
    dns_server_settings = {"preferred_dns_server": {"type": 'str'},
                           "alternate_dns_server1": {"type": 'str'},
                           "alternate_dns_server2": {"type": 'str'}}
    specs = {
        "enable_nic": {"type": 'bool', "default": True},
        "device_id": {"type": 'int'},
        "device_service_tag": {"type": 'str'},
        "delay": {"type": 'int', "default": 0},
        "ipv4_configuration":
            {"type": "dict", "options": ipv4_options,
             "required_if": [
                 ['enable_ipv4', True, ('enable_dhcp',), True],
                 ['enable_dhcp', False, ('static_ip_address', 'static_subnet_mask', "static_gateway"), False],
                 ['use_dhcp_to_obtain_dns_server_address', False,
                  ('static_preferred_dns_server', 'static_alternate_dns_server'), True]]
             },
        "ipv6_configuration":
            {"type": "dict", "options": ipv6_options,
             "required_if": [
                 ['enable_ipv6', True, ('enable_auto_configuration',), True],
                 ['enable_auto_configuration', False,
                  ('static_ip_address', 'static_prefix_length', "static_gateway"), False],
                 ['use_dhcpv6_to_obtain_dns_server_address', False,
                  ('static_preferred_dns_server', 'static_alternate_dns_server'), True]]
             },
        "dns_configuration":
            {"type": "dict", "options": dns_options,
             "required_if": [
                 ['register_with_dns', True, ('dns_name',), False],
                 ['use_dhcp_for_dns_domain_name', False, ('dns_domain_name',)],
                 ['auto_negotiation', False, ('network_speed',)]]
             },
        "management_vlan":
            {"type": "dict", "options": management_vlan,
             "required_if": [
                 ['enable_vlan', True, ('vlan_id',), True]]
             },
        "dns_server_settings":
            {"type": "dict", "options": dns_server_settings,
             "required_one_of": [("preferred_dns_server", "alternate_dns_server1", "alternate_dns_server2")]
             }
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        required_one_of=[('device_id', 'device_service_tag')],
        mutually_exclusive=[('device_id', 'device_service_tag')],
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            validate_input(module)
            dvc = get_device_details(module, rest_obj)
            if dvc.get('Type') in [SERVER, CHASSIS, IO_MODULE]:
                nw_setting = get_network_payload(module, rest_obj, dvc)
                resp = rest_obj.invoke_request('PUT', NETWORK_SETTINGS.format(dvc.get('Id')),
                                               data=nw_setting, api_timeout=API_TIMEOUT)
                module.exit_json(msg=SUCCESS_MSG, network_details=resp.json_data, changed=True)
            else:
                module.fail_json(msg=NON_CONFIG_NETWORK.format(dvc.get('Model')))
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, AttributeError, IndexError, KeyError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
