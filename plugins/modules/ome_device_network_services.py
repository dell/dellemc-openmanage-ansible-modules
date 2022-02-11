#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.0.1
# Copyright (C) 2021-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: ome_device_network_services
short_description: Configure chassis network services settings on OpenManage Enterprise Modular
description: This module allows to configure the network services on OpenManage Enterprise Modular.
version_added: "4.3.0"
extends_documentation_fragment:
  - dellemc.openmanage.omem_auth_options
options:
  device_id:
    type: int
    description:
      - The ID of the chassis for which the settings need to be updated.
      - If the device ID is not specified, this module updates the network services settings for the I(hostname).
      - I(device_id) is mutually exclusive with I(device_service_tag).
  device_service_tag:
    type: str
    description:
      - The service tag of the chassis for which the setting needs to be updated.
      - If the device service tag is not specified, this module updates the network
        services settings for the I(hostname).
      - I(device_service_tag) is mutually exclusive with I(device_id).
  snmp_settings:
    type: dict
    description: The settings for SNMP configuration.
    suboptions:
      enabled:
        type: bool
        required: true
        description: Enables or disables the SNMP settings.
      port_number:
        type: int
        description: The SNMP port number.
      community_name:
        type: str
        description:
          - The SNMP community string.
          - Required when I(enabled) is C(true).
  ssh_settings:
    type: dict
    description: The settings for SSH configuration.
    suboptions:
      enabled:
        required: true
        type: bool
        description: Enables or disables the SSH settings.
      port_number:
        type: int
        description: The port number for SSH service.
      max_sessions:
        type: int
        description: Number of SSH sessions.
      max_auth_retries:
        type: int
        description: The number of retries when the SSH session fails.
      idle_timeout:
        type: float
        description: SSH idle timeout in minutes.
  remote_racadm_settings:
    type: dict
    description: The settings for remote RACADM configuration.
    suboptions:
      enabled:
        type: bool
        required: true
        description: Enables or disables the remote RACADM settings.
requirements:
  - "python >= 3.8.6"
author:
  - "Felix Stephen (@felixs88)"
notes:
  - Run this module from a system that has direct access to Dell EMC OpenManage Enterprise Modular.
  - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Update network services settings of a chassis using the device ID
  dellemc.openmanage.ome_device_network_services:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_id: 25011
    snmp_settings:
      enabled: true
      port_number: 161
      community_name: public
    ssh_settings:
      enabled: false
    remote_racadm_settings:
      enabled: false

- name: Update network services settings of a chassis using the device service tag.
  dellemc.openmanage.ome_device_network_services:
    hostname: "192.168.0.2"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_service_tag: GHRT2RL
    snmp_settings:
      enabled: false
    ssh_settings:
      enabled: true
      port_number: 22
      max_sessions: 1
      max_auth_retries: 3
      idle_timeout: 1
    remote_racadm_settings:
      enabled: false

- name: Update network services settings of the host chassis.
  dellemc.openmanage.ome_device_network_services:
    hostname: "192.168.0.3"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    snmp_settings:
      enabled: false
    ssh_settings:
      enabled: false
    remote_racadm_settings:
      enabled: true
"""

RETURN = """
---
msg:
  type: str
  description: Overall status of the network services settings.
  returned: always
  sample: "Successfully updated the network services settings."
network_services_details:
  type: dict
  description: returned when network services settings are updated successfully.
  returned: success
  sample: {
    "EnableRemoteRacadm": true,
    "SettingType": "NetworkServices",
    "SnmpConfiguration": {
      "PortNumber": 161,
      "SnmpEnabled": true,
      "SnmpV1V2Credential": {
        "CommunityName": "public"
      }
    },
    "SshConfiguration": {
      "IdleTimeout": 60,
      "MaxAuthRetries": 3,
      "MaxSessions": 1,
      "PortNumber": 22,
      "SshEnabled": false
    }
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
          "MessageId": "CAPP1042",
          "RelatedProperties": [],
          "Message": "Unable to update the network configuration because the SNMP PortNumber is already in use.",
          "MessageArgs": ["SNMP PortNumber"],
          "Severity": "Informational",
          "Resolution": "Enter a different port number and retry the operation.",
        }
      ]
    }
  }
"""


import json
import socket
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params

DOMAIN_URI = "ManagementDomainService/Domains"
DEVICE_URI = "DeviceService/Devices"
NETWORK_SERVICE_API = "DeviceService/Devices({0})/Settings('NetworkServices')"
CONFIG_FAIL_MSG = "one of the following is required: snmp_settings, ssh_settings, remote_racadm_settings"
DOMAIN_FAIL_MSG = "The device location settings operation is supported only on " \
                  "OpenManage Enterprise Modular."
FETCH_FAIL_MSG = "Failed to retrieve the device information."
DEVICE_FAIL_MSG = "Unable to complete the operation because the entered target device {0} '{1}' is invalid."
NETWORK_SERVICE_FAIL_MSG = "Unable to complete the operation because the network services settings " \
                           "are not supported on the specified device."
CHANGES_FOUND = "Changes found to be applied."
NO_CHANGES_FOUND = "No changes found to be applied."
SUCCESS_MSG = "Successfully updated the network services settings."


def check_domain_service(module, rest_obj):
    try:
        rest_obj.invoke_request("GET", DOMAIN_URI, api_timeout=5)
    except HTTPError as err:
        err_message = json.loads(err)
        if err_message["error"]["@Message.ExtendedInfo"][0]["MessageId"] == "CGEN1006":
            module.fail_json(msg=DOMAIN_FAIL_MSG)
    return


def get_ip_from_host(hostname):
    ipaddr = hostname
    try:
        result = socket.getaddrinfo(hostname, None)
        last_element = result[-1]
        ip_address = last_element[-1][0]
        if ip_address:
            ipaddr = ip_address
    except socket.gaierror:
        ipaddr = hostname
    except Exception:
        ipaddr = hostname
    return ipaddr


def get_chassis_device(module, rest_obj):
    key, value = None, None
    ipaddress = get_ip_from_host(module.params["hostname"])
    resp = rest_obj.invoke_request("GET", DOMAIN_URI)
    for data in resp.json_data["value"]:
        if ipaddress in data["PublicAddress"]:
            key, value = ("Id", data["DeviceId"])
            break
    else:
        module.fail_json(msg=FETCH_FAIL_MSG)
    return key, value


def check_mode_validation(module, loc_data, rest_obj):
    req_snmp, req_ssh, req_comm_str, req_racadm = {}, {}, {}, {}
    exist_snmp, exist_ssh, exist_comm_str, exist_racadm = {}, {}, {}, {}
    payload = {"SettingType": "NetworkServices"}
    snmp_enabled = module.params.get("snmp_settings")
    if snmp_enabled is not None and snmp_enabled["enabled"] is True:
        req_snmp.update({"SnmpEnabled": snmp_enabled["enabled"]})
        req_comm_str.update({"CommunityName": module.params["snmp_settings"]["community_name"]})
        exist_snmp.update({"SnmpEnabled": loc_data["SnmpConfiguration"]["SnmpEnabled"]})
        exist_comm_str.update({"CommunityName": loc_data["SnmpConfiguration"]["SnmpV1V2Credential"]["CommunityName"]})
    elif snmp_enabled is not None and snmp_enabled["enabled"] is False:
        req_snmp.update({"SnmpEnabled": snmp_enabled["enabled"]})
        exist_snmp.update({"SnmpEnabled": loc_data["SnmpConfiguration"]["SnmpEnabled"]})

    if snmp_enabled is not None and snmp_enabled["enabled"] is True and snmp_enabled.get("port_number") is not None:
        req_snmp.update({"PortNumber": snmp_enabled.get("port_number")})
        exist_snmp.update({"PortNumber": loc_data["SnmpConfiguration"]["PortNumber"]})
    ssh_enabled = module.params.get("ssh_settings")
    if ssh_enabled is not None and ssh_enabled["enabled"] is True:
        req_ssh.update({"SshEnabled": ssh_enabled["enabled"]})
        exist_ssh.update({"SshEnabled": loc_data["SshConfiguration"]["SshEnabled"]})
    elif ssh_enabled is not None and ssh_enabled["enabled"] is False:
        req_ssh.update({"SshEnabled": ssh_enabled["enabled"]})
        exist_ssh.update({"SshEnabled": loc_data["SshConfiguration"]["SshEnabled"]})

    if ssh_enabled is not None and ssh_enabled["enabled"] is True and ssh_enabled.get("port_number") is not None:
        req_ssh.update({"PortNumber": module.params["ssh_settings"]["port_number"]})
        exist_ssh.update({"PortNumber": loc_data["SshConfiguration"]["PortNumber"]})
    if ssh_enabled is not None and ssh_enabled["enabled"] is True and ssh_enabled.get("max_sessions") is not None:
        req_ssh.update({"MaxSessions": module.params["ssh_settings"]["max_sessions"]})
        exist_ssh.update({"MaxSessions": loc_data["SshConfiguration"]["MaxSessions"]})
    if ssh_enabled is not None and ssh_enabled["enabled"] is True and ssh_enabled.get("max_auth_retries") is not None:
        req_ssh.update({"MaxAuthRetries": module.params["ssh_settings"]["max_auth_retries"]})
        exist_ssh.update({"MaxAuthRetries": loc_data["SshConfiguration"]["MaxAuthRetries"]})
    if ssh_enabled is not None and ssh_enabled["enabled"] is True and ssh_enabled.get("idle_timeout") is not None:
        req_ssh.update({"IdleTimeout": int(module.params["ssh_settings"]["idle_timeout"] * 60)})
        exist_ssh.update({"IdleTimeout": int(loc_data["SshConfiguration"]["IdleTimeout"])})
    recadm_enabled = module.params.get("remote_racadm_settings")
    if recadm_enabled is not None and recadm_enabled["enabled"] is True:
        req_racadm = {"EnableRemoteRacadm": recadm_enabled["enabled"]}
        exist_racadm = {"EnableRemoteRacadm": loc_data["EnableRemoteRacadm"]}
    elif recadm_enabled is not None and recadm_enabled["enabled"] is False:
        req_racadm = {"EnableRemoteRacadm": recadm_enabled["enabled"]}
        exist_racadm = {"EnableRemoteRacadm": loc_data["EnableRemoteRacadm"]}
    changes = [bool(set(req_snmp.items()) ^ set(exist_snmp.items())) or
               bool(set(req_ssh.items()) ^ set(exist_ssh.items())) or
               bool(set(req_comm_str.items()) ^ set(exist_comm_str.items())) or
               bool(set(req_racadm.items()) ^ set(exist_racadm.items()))]
    if module.check_mode and any(changes) is True:
        loc_data["SshConfiguration"]["IdleTimeout"] = loc_data["SshConfiguration"]["IdleTimeout"] / 60
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    elif module.check_mode and all(changes) is False:
        loc_data["SshConfiguration"]["IdleTimeout"] = loc_data["SshConfiguration"]["IdleTimeout"] / 60
        module.exit_json(msg=NO_CHANGES_FOUND)
    elif not module.check_mode and all(changes) is False:
        loc_data["SshConfiguration"]["IdleTimeout"] = loc_data["SshConfiguration"]["IdleTimeout"] / 60
        module.exit_json(msg=NO_CHANGES_FOUND)
    else:
        payload.update(loc_data)
        payload["SnmpConfiguration"].update(req_snmp) if req_snmp else None
        payload["SnmpConfiguration"]["SnmpV1V2Credential"].update(req_comm_str) if req_comm_str else None
        payload["SshConfiguration"].update(req_ssh) if req_ssh else None
        payload.update(req_racadm) if req_racadm else None
    return payload


def fetch_device_details(module, rest_obj):
    device_id, tag, final_resp = module.params.get("device_id"), module.params.get("device_service_tag"), {}
    if device_id is None and tag is None:
        key, value = get_chassis_device(module, rest_obj)
        device_id = value
    else:
        key, value = ("Id", device_id) if device_id is not None else ("DeviceServiceTag", tag)
        param_value = "{0} eq {1}".format(key, value) if key == "Id" else "{0} eq '{1}'".format(key, value)
        resp = rest_obj.invoke_request("GET", DEVICE_URI, query_param={"$filter": param_value})
        resp_data = resp.json_data.get("value")
        rename_key = "id" if key == "Id" else "service tag"
        if not resp_data:
            module.fail_json(msg=DEVICE_FAIL_MSG.format(rename_key, value))
        if key == "DeviceServiceTag" and resp_data[0]["DeviceServiceTag"] == tag:
            device_id = resp_data[0]["Id"]
        elif key == "Id" and resp_data[0]["Id"] == device_id:
            device_id = resp_data[0]["Id"]
        else:
            module.fail_json(msg=DEVICE_FAIL_MSG.format(rename_key, value))
    try:
        loc_resp = rest_obj.invoke_request("GET", NETWORK_SERVICE_API.format(device_id))
    except HTTPError as err:
        if err.code == 404:
            module.fail_json(msg=NETWORK_SERVICE_FAIL_MSG)
        err_message = json.load(err)
        error_msg = err_message.get('error', {}).get('@Message.ExtendedInfo')
        if error_msg and error_msg[0].get("MessageId") == "CGEN1004":
            module.fail_json(msg=NETWORK_SERVICE_FAIL_MSG)
    else:
        loc_resp_data = rest_obj.strip_substr_dict(loc_resp.json_data)
        payload = check_mode_validation(module, loc_resp_data, rest_obj)
        final_resp = rest_obj.invoke_request("PUT", NETWORK_SERVICE_API.format(device_id), data=payload)
    return final_resp


def main():
    snmp_options = {"enabled": {"type": "bool", "required": True},
                    "port_number": {"type": "int", "required": False},
                    "community_name": {"type": "str", "required": False}}
    ssh_options = {"enabled": {"type": "bool", "required": True},
                   "port_number": {"type": "int", "required": False},
                   "max_sessions": {"type": "int", "required": False},
                   "max_auth_retries": {"type": "int", "required": False},
                   "idle_timeout": {"type": "float", "required": False}}
    racadm_options = {"enabled": {"type": "bool", "required": True}}
    specs = {
        "device_id": {"required": False, "type": "int"},
        "device_service_tag": {"required": False, "type": "str"},
        "snmp_settings": {"type": "dict", "required": False, "options": snmp_options,
                          "required_if": [["enabled", True, ("community_name",)]]},
        "ssh_settings": {"type": "dict", "required": False, "options": ssh_options},
        "remote_racadm_settings": {"type": "dict", "required": False, "options": racadm_options},
    }
    specs.update(ome_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[('device_id', 'device_service_tag')],
        required_one_of=[["snmp_settings", "ssh_settings", "remote_racadm_settings"]],
        supports_check_mode=True,
    )
    if not any([module.params.get("snmp_settings"), module.params.get("ssh_settings"),
                module.params.get("remote_racadm_settings")]):
        module.fail_json(msg=CONFIG_FAIL_MSG)
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            check_domain_service(module, rest_obj)
            resp = fetch_device_details(module, rest_obj)
            resp_data = resp.json_data
            resp_data["SshConfiguration"]["IdleTimeout"] = resp_data["SshConfiguration"]["IdleTimeout"] / 60
            module.exit_json(msg=SUCCESS_MSG, network_services_details=resp_data, changed=True)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, AttributeError, IndexError, KeyError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
