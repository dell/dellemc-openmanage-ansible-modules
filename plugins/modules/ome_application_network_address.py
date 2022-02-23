#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.1.0
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_application_network_address
short_description: Updates the network configuration on OpenManage Enterprise
version_added: "2.1.0"
description:
  - This module allows the configuration of a DNS and an IPV4 or IPV6 network on OpenManage Enterprise.
notes:
  - The configuration changes can only be applied to one interface at a time.
  - The system management consoles might be unreachable for some time after the configuration changes are applied.
  - This module supports C(check_mode).
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  enable_nic:
    description: Enable or disable Network Interface Card (NIC) configuration.
    type: bool
    default: true
  interface_name:
    description:
      - "If there are multiple interfaces, network configuration changes can be applied to a single interface using the
      interface name of the NIC."
      - If this option is not specified, Primary interface is chosen by default.
    type: str
  ipv4_configuration:
    description:
      - IPv4 network configuration.
      - "I(Warning) Ensure that you have an alternate interface to access OpenManage Enterprise as these options can
      change the current IPv4 address for I(hostname)."
    type: dict
    suboptions:
      enable:
        description:
          - Enable or disable access to the network using IPv4.
        type: bool
        required: true
      enable_dhcp:
        description:
          - "Enable or disable the automatic request to get an IPv4 address from the IPv4 Dynamic Host Configuration
          Protocol (DHCP) server"
          - "If I(enable_dhcp) option is true, OpenManage Enterprise retrieves the IP configuration—IPv4 address,
          subnet mask, and gateway from a DHCP server on the existing network."
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
      use_dhcp_for_dns_server_names:
        description:
          - This option allows to automatically request and obtain a DNS server IPv4 address from the DHCP server.
          - This option is applicable when I(enable_dhcp) is true.
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
      - "I(Warning) Ensure that you have an alternate interface to access OpenManage Enterprise as these options can
      change the current IPv6 address for I(hostname)."
    type: dict
    suboptions:
      enable:
        description: Enable or disable access to the network using the IPv6.
        type: bool
        required: true
      enable_auto_configuration:
        description:
          - "Enable or disable the automatic request to get an IPv6 address from the IPv6 DHCP server or router
          advertisements(RA)"
          - "If I(enable_auto_configuration) is true, OME retrieves IP configuration-IPv6 address, prefix, and gateway,
          from a DHCPv6 server on the existing network"
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
      use_dhcp_for_dns_server_names:
        description:
          - This option allows to automatically request and obtain a DNS server IPv6 address from the DHCP server.
          - This option is applicable when I(enable_auto_configuration) is true
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
      - vLAN configuration.
      - These settings are applicable for OpenManage Enterprise Modular.
    type: dict
    suboptions:
      enable_vlan:
        description:
          - Enable or disable vLAN for management.
          - The vLAN configuration cannot be updated if the I(register_with_dns) field under I(dns_configuration) is true.
          - "I(WARNING) Ensure that the network cable is plugged to the correct port after the vLAN configuration
          changes have been made. If not, the configuration change may not be effective."
        required: true
        type: bool
      vlan_id:
        description:
          - vLAN ID.
          - This option is applicable when I(enable_vlan) is true.
        type: int
  dns_configuration:
    description: Domain Name System(DNS) settings.
    type: dict
    suboptions:
      register_with_dns:
        description:
          - Register/Unregister I(dns_name) on the DNS Server.
          - This option cannot be updated if vLAN configuration changes.
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
  reboot_delay:
    description:
      - The time in seconds, after which settings are applied.
      - This option is not mandatory.
    type: int
requirements:
    - "python >= 3.8.6"
author:
    - "Jagadeesh N V(@jagadeeshnv)"
'''

EXAMPLES = r'''
---
- name: IPv4 network configuration for primary interface
  dellemc.openmanage.ome_application_network_address:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    enable_nic: true
    ipv4_configuration:
      enable: true
      enable_dhcp: false
      static_ip_address: 192.168.0.2
      static_subnet_mask: 255.255.254.0
      static_gateway: 192.168.0.3
      use_dhcp_for_dns_server_names: false
      static_preferred_dns_server: 192.168.0.4
      static_alternate_dns_server: 192.168.0.5
    reboot_delay: 5

- name: IPv6 network configuration for primary interface
  dellemc.openmanage.ome_application_network_address:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    ipv6_configuration:
      enable: true
      enable_auto_configuration: true
      static_ip_address: 2626:f2f2:f081:9:1c1c:f1f1:4747:1
      static_prefix_length: 10
      static_gateway: 2626:f2f2:f081:9:1c1c:f1f1:4747:2
      use_dhcp_for_dns_server_names: true
      static_preferred_dns_server: 2626:f2f2:f081:9:1c1c:f1f1:4747:3
      static_alternate_dns_server: 2626:f2f2:f081:9:1c1c:f1f1:4747:4

- name: Management vLAN configuration for primary interface
  dellemc.openmanage.ome_application_network_address:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    management_vlan:
      enable_vlan: true
      vlan_id: 3344
    dns_configuration:
      register_with_dns: false
    reboot_delay: 1

- name: DNS settings
  dellemc.openmanage.ome_application_network_address:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    ipv4_configuration:
      enable: true
      use_dhcp_for_dns_server_names: false
      static_preferred_dns_server: 192.168.0.4
      static_alternate_dns_server: 192.168.0.5
    dns_configuration:
      register_with_dns: true
      use_dhcp_for_dns_domain_name: false
      dns_name: "MX-SVCTAG"
      dns_domain_name: "dnslocaldomain"

- name: Disbale nic interface eth1
  dellemc.openmanage.ome_application_network_address:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    enable_nic: false
    interface_name: eth1

- name: Complete network settings for interface eth1
  dellemc.openmanage.ome_application_network_address:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    enable_nic: true
    interface_name: eth1
    ipv4_configuration:
      enable: true
      enable_dhcp: false
      static_ip_address: 192.168.0.2
      static_subnet_mask: 255.255.254.0
      static_gateway: 192.168.0.3
      use_dhcp_for_dns_server_names: false
      static_preferred_dns_server: 192.168.0.4
      static_alternate_dns_server: 192.168.0.5
    ipv6_configuration:
      enable: true
      enable_auto_configuration: true
      static_ip_address: 2626:f2f2:f081:9:1c1c:f1f1:4747:1
      static_prefix_length: 10
      static_gateway: ffff::2607:f2b1:f081:9
      use_dhcp_for_dns_server_names: true
      static_preferred_dns_server: 2626:f2f2:f081:9:1c1c:f1f1:4747:3
      static_alternate_dns_server: 2626:f2f2:f081:9:1c1c:f1f1:4747:4
    dns_configuration:
      register_with_dns: true
      use_dhcp_for_dns_domain_name: false
      dns_name: "MX-SVCTAG"
      dns_domain_name: "dnslocaldomain"
    reboot_delay: 5
'''

RETURN = r'''
---
msg:
  type: str
  description: Overall status of the network address configuration change.
  returned: always
  sample: Successfully updated network address configuration
network_configuration:
  type: dict
  description: Updated application network address configuration.
  returned: on success
  sample: {
    "Delay": 0,
    "DnsConfiguration": {
        "DnsDomainName": "",
        "DnsName": "MX-SVCTAG",
        "RegisterWithDNS": false,
        "UseDHCPForDNSDomainName": true
    },
    "EnableNIC": true,
    "InterfaceName": "eth0",
    "PrimaryInterface": true,
    "Ipv4Configuration": {
        "Enable": true,
        "EnableDHCP": false,
        "StaticAlternateDNSServer": "",
        "StaticGateway": "192.168.0.2",
        "StaticIPAddress": "192.168.0.3",
        "StaticPreferredDNSServer": "192.168.0.4",
        "StaticSubnetMask": "255.255.254.0",
        "UseDHCPForDNSServerNames": false
    },
    "Ipv6Configuration": {
        "Enable": true,
        "EnableAutoConfiguration": true,
        "StaticAlternateDNSServer": "",
        "StaticGateway": "",
        "StaticIPAddress": "",
        "StaticPreferredDNSServer": "",
        "StaticPrefixLength": 0,
        "UseDHCPForDNSServerNames": true
    },
    "ManagementVLAN": {
        "EnableVLAN": false,
        "Id": 1
    }
  }
job_info:
  description: Details of the job to update in case OME version is >= 3.3.
  returned: on success
  type: dict
  sample: {
        "Builtin": false,
        "CreatedBy": "system",
        "Editable": true,
        "EndTime": null,
        "Id": 14902,
        "JobDescription": "Generic OME runtime task",
        "JobName": "OMERealtime_Task",
        "JobStatus": {
            "Id": 2080,
            "Name": "New"
        },
        "JobType": {
            "Id": 207,
            "Internal": true,
            "Name": "OMERealtime_Task"
        },
        "LastRun": null,
        "LastRunStatus": {
            "Id": 2080,
            "Name": "New"
        },
        "NextRun": null,
        "Params": [
            {
                "JobId": 14902,
                "Key": "Nmcli_Update",
                "Value": "{\"interfaceName\":\"eth0\",\"profileName\":\"eth0\",\"enableNIC\":true,
                \"ipv4Configuration\":{\"enable\":true,\"enableDHCP\":true,\"staticIPAddress\":\"\",
                \"staticSubnetMask\":\"\",\"staticGateway\":\"\",\"useDHCPForDNSServerNames\":true,
                \"staticPreferredDNSServer\":\"\",\"staticAlternateDNSServer\":\"\"},
                \"ipv6Configuration\":{\"enable\":false,\"enableAutoConfiguration\":true,\"staticIPAddress\":\"\",
                \"staticPrefixLength\":0,\"staticGateway\":\"\",\"useDHCPForDNSServerNames\":false,
                \"staticPreferredDNSServer\":\"\",\"staticAlternateDNSServer\":\"\"},
                \"managementVLAN\":{\"enableVLAN\":false,\"id\":0},\"dnsConfiguration\":{\"registerWithDNS\":false,
                \"dnsName\":\"\",\"useDHCPForDNSDomainName\":false,\"dnsDomainName\":\"\",\"fqdndomainName\":\"\",
                \"ipv4CurrentPreferredDNSServer\":\"\",\"ipv4CurrentAlternateDNSServer\":\"\",
                \"ipv6CurrentPreferredDNSServer\":\"\",\"ipv6CurrentAlternateDNSServer\":\"\"},
                \"currentSettings\":{\"ipv4Address\":[],\"ipv4Gateway\":\"\",\"ipv4Dns\":[],\"ipv4Domain\":\"\",
                \"ipv6Address\":[],\"ipv6LinkLocalAddress\":\"\",\"ipv6Gateway\":\"\",\"ipv6Dns\":[],
                \"ipv6Domain\":\"\"},\"delay\":0,\"primaryInterface\":true,\"modifiedConfigs\":{}}"
            }
        ],
        "Schedule": "startnow",
        "StartTime": null,
        "State": "Enabled",
        "Targets": [],
        "UpdatedBy": null,
        "Visible": true
    }
error_info:
  description: Details of the HTTP error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
    "@Message.ExtendedInfo": [
        {
            "Message": "Unable to update the address configuration because a dependent field is missing for  Use DHCP
            for DNS Domain Name, Enable DHCP for ipv4 or Enable Autoconfig for ipv6 settings for valid configuration .",
            "MessageArgs": [
                "Use DHCP for DNS Domain Name, Enable DHCP for ipv4 or Enable Autoconfig for ipv6 settings for valid
                configuration"
            ],
            "MessageId": "CAPP1304",
            "RelatedProperties": [],
            "Resolution": "Make sure that all dependent fields contain valid content and retry the operation.",
            "Severity": "Critical"
        }
    ],
    "code": "Base.1.0.GeneralError",
    "message": "A general error has occurred. See ExtendedInfo for more information."
    }
  }
'''

import json
import socket
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError

IP_CONFIG = "ApplicationService/Network/AddressConfiguration"
JOB_IP_CONFIG = "ApplicationService/Network/AdapterConfigurations"
POST_IP_CONFIG = "ApplicationService/Actions/Network.ConfigureNetworkAdapter"
CHANGES_FOUND = "Changes found to be applied."
NO_CHANGES_FOUND = "No changes found to be applied."


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


def remove_unwanted_keys(key_list, payload):
    for key in key_list:
        if key in payload:
            payload.pop(key)


def format_payload(src_dict):
    address_payload_map = {"enable_nic": "EnableNIC",
                           "interface_name": "InterfaceName",
                           "enable": "Enable",
                           "enable_dhcp": "EnableDHCP",
                           "static_ip_address": "StaticIPAddress",
                           "static_subnet_mask": "StaticSubnetMask",
                           "static_gateway": "StaticGateway",
                           "use_dhcp_for_dns_server_names": "UseDHCPForDNSServerNames",
                           "static_preferred_dns_server": "StaticPreferredDNSServer",
                           "static_alternate_dns_server": "StaticAlternateDNSServer",
                           "enable_auto_configuration": "EnableAutoConfiguration",
                           "static_prefix_length": "StaticPrefixLength",
                           "enable_vlan": "EnableVLAN",
                           "vlan_id": "Id",
                           "register_with_dns": "RegisterWithDNS",
                           "use_dhcp_for_dns_domain_name": "UseDHCPForDNSDomainName",
                           "dns_name": "DnsName",
                           "dns_domain_name": "DnsDomainName",
                           "reboot_delay": "Delay"}
    if src_dict:
        return dict([(address_payload_map[key], val) for key, val in src_dict.items() if val is not None])


def get_payload(module):
    params = module.params
    backup_params = params.copy()
    remove_keys = ["hostname", "username", "password", "port"]
    remove_unwanted_keys(remove_keys, backup_params)
    ipv4_payload = format_payload(backup_params.get("ipv4_configuration", {}))
    ipv6_payload = format_payload(backup_params.get("ipv6_configuration", {}))
    dns_payload = format_payload(backup_params.get("dns_configuration", {}))
    vlan_payload = format_payload(backup_params.get("management_vlan", {}))
    return ipv4_payload, ipv6_payload, dns_payload, vlan_payload


def _compare_dict_merge(src_dict, new_dict, param_list):
    diff = 0
    for parm in param_list:
        val = new_dict.get(parm)
        if val is not None:
            if val != src_dict.get(parm):
                src_dict[parm] = val
                diff += 1
    return diff


def update_ipv4_payload(src_dict, new_dict):
    diff = 0
    if new_dict:
        if new_dict.get("Enable") != src_dict.get("Enable"):  # Mandatory
            src_dict["Enable"] = new_dict.get("Enable")
            diff += 1
        if new_dict.get("Enable"):
            tmp_dict = {"EnableDHCP": ["StaticIPAddress", "StaticSubnetMask", "StaticGateway"],
                        "UseDHCPForDNSServerNames": ["StaticPreferredDNSServer", "StaticAlternateDNSServer"]}
            for key, val in tmp_dict.items():
                if new_dict.get(key) is not None:
                    if new_dict.get(key) != src_dict.get(key):
                        src_dict[key] = new_dict.get(key)
                        diff += 1
                    if not new_dict.get(key):
                        diff = diff + _compare_dict_merge(src_dict, new_dict, val)
    return diff


def update_ipv6_payload(src_dict, new_dict):
    diff = 0
    if new_dict:
        if new_dict.get("Enable") != src_dict.get("Enable"):  # Mandatory
            src_dict["Enable"] = new_dict.get("Enable")
            diff += 1
        if new_dict.get("Enable"):
            tmp_dict = {"EnableAutoConfiguration": ["StaticIPAddress", "StaticPrefixLength", "StaticGateway"],
                        "UseDHCPForDNSServerNames": ["StaticPreferredDNSServer", "StaticAlternateDNSServer"]}
            for key, val in tmp_dict.items():
                if new_dict.get(key) is not None:
                    if new_dict.get(key) != src_dict.get(key):
                        src_dict[key] = new_dict.get(key)
                        diff += 1
                    if not new_dict.get(key):
                        diff = diff + _compare_dict_merge(src_dict, new_dict, val)
    return diff


def update_dns_payload(src_dict, new_dict):
    diff = 0
    if new_dict:
        mkey = "RegisterWithDNS"
        if new_dict.get(mkey) is not None:
            if new_dict.get(mkey) != src_dict.get(mkey):
                src_dict[mkey] = new_dict.get(mkey)
                diff += 1
            if new_dict.get(mkey) is True:
                diff = diff + _compare_dict_merge(src_dict, new_dict, ["DnsName"])
        mkey = "UseDHCPForDNSDomainName"
        if new_dict.get(mkey) is not None:
            if new_dict.get(mkey) != src_dict.get(mkey):
                src_dict[mkey] = new_dict.get(mkey)
                diff += 1
            if not new_dict.get(mkey):
                diff = diff + _compare_dict_merge(src_dict, new_dict, ["DnsDomainName"])
    return diff


def update_vlan_payload(src_dict, new_dict):
    diff = 0
    if new_dict:
        mkey = "EnableVLAN"
        if new_dict.get(mkey) is not None:
            if new_dict.get(mkey) != src_dict.get(mkey):
                src_dict[mkey] = new_dict.get(mkey)
                diff += 1
            if new_dict.get(mkey) is True:
                diff = diff + _compare_dict_merge(src_dict, new_dict, ["Id"])
    return diff


def get_network_config_data(rest_obj, module):
    try:
        interface = module.params.get("interface_name")
        resp = rest_obj.invoke_request("GET", JOB_IP_CONFIG)
        adapter_list = resp.json_data.get("value")
        int_adp = None
        pri_adp = None
        if adapter_list:
            for adp in adapter_list:
                if interface and adp.get("InterfaceName") == interface:
                    int_adp = adp
                    break
                if adp.get("PrimaryInterface"):
                    pri_adp = adp
        if interface and int_adp is None:
            module.fail_json(msg="The 'interface_name' value provided {0} is invalid".format(interface))
        elif int_adp:
            return int_adp, "POST", POST_IP_CONFIG
        else:
            return pri_adp, "POST", POST_IP_CONFIG
    except HTTPError as err:
        pass
    except Exception as err:
        raise err
    resp = rest_obj.invoke_request("GET", IP_CONFIG)
    return resp.json_data, "PUT", IP_CONFIG


def get_updated_payload(rest_obj, module, ipv4_payload, ipv6_payload, dns_payload, vlan_payload):
    current_setting = {}
    remove_keys = ["@odata.context", "@odata.type", "@odata.id", "CurrentSettings"]
    current_setting, rest_method, uri = get_network_config_data(rest_obj, module)
    remove_unwanted_keys(remove_keys, current_setting)
    payload_dict = {"Ipv4Configuration": [ipv4_payload, update_ipv4_payload],
                    "Ipv6Configuration": [ipv6_payload, update_ipv6_payload],
                    "DnsConfiguration": [dns_payload, update_dns_payload],
                    "ManagementVLAN": [vlan_payload, update_vlan_payload]}
    diff = 0
    enable_nic = module.params.get("enable_nic")
    if current_setting.get("EnableNIC") != enable_nic:
        current_setting["EnableNIC"] = enable_nic
        diff += 1
    if enable_nic:
        for config, pload in payload_dict.items():
            if pload[0]:
                diff = diff + pload[1](current_setting.get(config), pload[0])
    delay = module.params.get("reboot_delay")
    if delay is not None:
        if current_setting["Delay"] != delay:
            current_setting["Delay"] = delay
    if diff == 0:
        module.exit_json(
            msg=NO_CHANGES_FOUND, network_configuration=current_setting)
    if module.check_mode:
        module.exit_json(changed=True, msg=CHANGES_FOUND)
    return current_setting, rest_method, uri


def validate_ipaddress(module, ip_type, config, var_list, ip_func):
    ipv_input = module.params.get(config)
    if ipv_input:
        for ipname in var_list:
            val = ipv_input.get(ipname)
            if val and not ip_func(val):
                module.fail_json(msg="Invalid {0} address provided for the {1}".format(ip_type, ipname))


def validate_input(module):
    ip_addr = ["static_ip_address", "static_gateway", "static_preferred_dns_server", "static_alternate_dns_server"]
    validate_ipaddress(module, "IPv6", "ipv6_configuration", ip_addr, validate_ip_v6_address)
    ip_addr.append("static_subnet_mask")
    validate_ipaddress(module, "IPv4", "ipv4_configuration", ip_addr, validate_ip_address)
    delay = module.params.get("reboot_delay")
    if delay and delay < 0:
        module.fail_json(msg="Invalid value provided for 'reboot_delay'")


def main():
    ipv4_options = {"enable": {"required": True, "type": "bool"},
                    "enable_dhcp": {"required": False, "type": "bool"},
                    "static_ip_address": {"required": False, "type": "str"},
                    "static_subnet_mask": {"required": False, "type": "str"},
                    "static_gateway": {"required": False, "type": "str"},
                    "use_dhcp_for_dns_server_names": {"required": False, "type": "bool"},
                    "static_preferred_dns_server": {"required": False, "type": "str"},
                    "static_alternate_dns_server": {"required": False, "type": "str"}}
    ipv6_options = {"enable": {"required": True, "type": "bool"},
                    "enable_auto_configuration": {"required": False, "type": "bool"},
                    "static_ip_address": {"required": False, "type": "str"},
                    "static_prefix_length": {"required": False, "type": "int"},
                    "static_gateway": {"required": False, "type": "str"},
                    "use_dhcp_for_dns_server_names": {"required": False, "type": "bool"},
                    "static_preferred_dns_server": {"required": False, "type": "str"},
                    "static_alternate_dns_server": {"required": False, "type": "str"}}
    dns_options = {"register_with_dns": {"required": False, "type": "bool"},
                   "use_dhcp_for_dns_domain_name": {"required": False, "type": "bool"},
                   "dns_name": {"required": False, "type": "str"},
                   "dns_domain_name": {"required": False, "type": "str"}}
    management_vlan = {"enable_vlan": {"required": True, "type": "bool"},
                       "vlan_id": {"required": False, "type": "int"}}

    specs = {
        "enable_nic": {"required": False, "type": "bool", "default": True},
        "interface_name": {"required": False, "type": "str"},
        "ipv4_configuration":
            {"required": False, "type": "dict", "options": ipv4_options,
             "required_if": [
                 ['enable', True, ('enable_dhcp',), True],
                 ['enable_dhcp', False, ('static_ip_address', 'static_subnet_mask', "static_gateway"), False],
                 ['use_dhcp_for_dns_server_names', False,
                  ('static_preferred_dns_server', 'static_alternate_dns_server'), True]
             ]
             },
        "ipv6_configuration":
            {"required": False, "type": "dict", "options": ipv6_options,
             "required_if": [
                 ['enable', True, ('enable_auto_configuration',), True],
                 ['enable_auto_configuration', False, ('static_ip_address', 'static_prefix_length', "static_gateway"),
                  False],
                 ['use_dhcp_for_dns_server_names', False,
                  ('static_preferred_dns_server', 'static_alternate_dns_server'), True]
             ]
             },
        "dns_configuration":
            {"required": False, "type": "dict", "options": dns_options,
             "required_if": [
                 ['register_with_dns', True, ('dns_name',), False],
                 ['use_dhcp_for_dns_domain_name', False, ('dns_domain_name',)]
             ]
             },
        "management_vlan":
            {"required": False, "type": "dict", "options": management_vlan,
             "required_if": [
                 ['enable_vlan', True, ('vlan_id',), True]
             ]
             },
        "reboot_delay": {"required": False, "type": "int"}
    }
    specs.update(ome_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        required_if=[
            ["enable_nic", True,
             ("ipv4_configuration", "ipv6_configuration", "dns_configuration", "management_vlan"), True]
        ],
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            validate_input(module)
            ipv4_payload, ipv6_payload, dns_payload, vlan_payload = get_payload(module)
            updated_payload, rest_method, uri = get_updated_payload(
                rest_obj, module, ipv4_payload, ipv6_payload, dns_payload, vlan_payload)
            resp = rest_obj.invoke_request(rest_method, uri, data=updated_payload, api_timeout=150)
            if rest_method == "POST":
                module.exit_json(msg="Successfully triggered job to update network address configuration.",
                                 network_configuration=updated_payload, job_info=resp.json_data, changed=True)
            module.exit_json(msg="Successfully triggered task to update network address configuration.",
                             network_configuration=resp.json_data, changed=True)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, SSLValidationError, OSError) as err:
        module.fail_json(msg=str(err))
    except Exception as err:
        module.fail_json(msg=str(err))


if __name__ == "__main__":
    main()
