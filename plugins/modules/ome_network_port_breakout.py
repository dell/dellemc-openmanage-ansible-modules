#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.0.0
# Copyright (C) 2020-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_network_port_breakout
short_description: This module allows to automate the port portioning or port breakout to logical sub ports
version_added: "2.1.0"
description:
  - This module allows to automate breaking out of IOMs in fabric mode into logical sub ports.
  - The port breakout operation is only supported in OpenManage Enterprise Modular.
extends_documentation_fragment:
  - dellemc.openmanage.omem_auth_options
options:
  target_port:
    required: True
    description: "The ID of the port in the switch to breakout. Enter the port ID in the format: service tag:port.
      For example, 2HB7NX2:ethernet1/1/13."
    type: str
  breakout_type:
    required: True
    description:
      - The preferred breakout type. For example, 4X10GE.
      - To revoke the default breakout configuration, enter 'HardwareDefault'.
    type: str
requirements:
    - "python >= 2.7.17"
author: "Felix Stephen (@felixs88)"
notes:
    - Run this module from a system that has direct access to DellEMC OpenManage Enterprise Modular.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Port breakout configuration
  dellemc.openmanage.ome_network_port_breakout:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    target_port: "2HB7NX2:phy-port1/1/11"
    breakout_type: "1X40GE"

- name: Revoke the default breakout configuration
  dellemc.openmanage.ome_network_port_breakout:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    target_port: "2HB7NX2:phy-port1/1/11"
    breakout_type: "HardwareDefault"
'''

RETURN = r'''
---
msg:
  description: Overall status of the port configuration.
  returned: always
  type: str
  sample: Port breakout configuration job submitted successfully.
breakout_status:
  description: Details of the OpenManage Enterprise jobs.
  returned: success
  type: dict
  sample: {
    "Builtin": false,
    "CreatedBy": "root",
    "Editable": true,
    "EndTime": null,
    "Id": 11111,
    "JobDescription": "",
    "JobName": "Breakout Port",
    "JobStatus": {"Id": 1112, "Name": "New"},
    "JobType": {"Id": 3, "Internal": false, "Name": "DeviceAction_Task"},
    "LastRun": null,
    "LastRunStatus": {"Id": 1113, "Name": "NotRun"},
    "NextRun": null,
    "Params": [
      {"JobId": 11111, "Key": "operationName", "Value": "CONFIGURE_PORT_BREAK_OUT"},
      {"JobId": 11111, "Key": "interfaceId", "Value": "2HB7NX2:phy-port1/1/11"},
      {"JobId": 11111, "Key": "breakoutType", "Value": "1X40GE"}],
    "Schedule": "startnow",
    "StartTime": null,
    "State": "Enabled",
    "Targets": [
      {"Data": "", "Id": 11112, "JobId": 34206, "TargetType": { "Id": 1000, "Name": "DEVICE"}}
      ],
    "UpdatedBy": null,
    "UserGenerated": true,
    "Visible": true
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
import re
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError

DEVICE_URI = "DeviceService/Devices"
PORT_INFO_URI = "DeviceService/Devices({0})/InventoryDetails('portInformation')"
JOB_URI = "JobService/Jobs"


def get_device_id(module, rest_obj):
    """
    This function returns device id.
    :param module: ansible module arguments.
    :param rest_obj: rest object for making requests.
    :return: device id
    """
    regex = "^[a-z0-9A-Z]+[:][a-z0-9A-Z/-]+$"
    target_port = module.params["target_port"]
    if re.search(regex, target_port) is None:
        module.fail_json(msg="Invalid target port {0}.".format(target_port))
    service_tag = target_port.split(":")
    query = "DeviceServiceTag eq '{0}'".format(service_tag[0])
    device_id, failed_msg = None, "Unable to retrieve the device information because" \
                                  " the device with the entered service tag {0} is not present."
    response = rest_obj.invoke_request("GET", DEVICE_URI, query_param={"$filter": query})
    if response.status_code == 200 and response.json_data.get("value"):
        device_info = response.json_data.get("value")[0]
        device_id = device_info["Id"]
    else:
        module.fail_json(msg=failed_msg.format(service_tag[0]))
    return device_id


def get_port_information(module, rest_obj, device_id):
    """
    This function returns the existing breakout configuration details.
    :param module: ansible module arguments.
    :param rest_obj: rest object for making requests.
    :param device_id: device id
    :return: str, {}, str
    """
    response = rest_obj.invoke_request("GET", PORT_INFO_URI.format(device_id))
    breakout_config, breakout_capability, target_port = None, None, module.params["target_port"]
    for each in response.json_data.get("InventoryInfo"):
        if not each["Configuration"] == "NoBreakout" and each["Id"] == target_port:
            breakout_capability = each["PortBreakoutCapabilities"]
            breakout_config = each["Configuration"]
            interface_id = each["Id"]
            break
    else:
        module.fail_json(msg="{0} does not support port breakout"
                             " or invalid port number entered.".format(target_port))
    return breakout_config, breakout_capability, interface_id


def get_breakout_payload(device_id, breakout_type, interface_id):
    """
    Payload for breakout configuration.
    :param device_id: device id
    :param breakout_type: requested breakout type
    :param interface_id: port number with service tag
    :return: json
    """
    payload = {
        "Id": 0, "JobName": "Breakout Port", "JobDescription": "",
        "Schedule": "startnow", "State": "Enabled",
        "JobType": {"Id": 3, "Name": "DeviceAction_Task"},
        "Params": [
            {"Key": "breakoutType", "Value": breakout_type},
            {"Key": "interfaceId", "Value": interface_id},
            {"Key": "operationName", "Value": "CONFIGURE_PORT_BREAK_OUT"}],
        "Targets": [
            {"JobId": 0, "Id": device_id, "Data": "", "TargetType": {"Id": 4000, "Name": "DEVICE"}}
        ]}
    return payload


def check_mode(module, changes=False):
    """
    The check mode function to check whether the changes found or not.
    :param module: ansible module arguments
    :param changes: boolean to return the appropriate message.
    :return: None
    """
    if module.check_mode:
        message = "Changes found to commit!" if changes else "No changes found to commit!"
        module.exit_json(msg=message, changed=changes)


def set_breakout(module, rest_obj, breakout_config, breakout_capability, interface_id, device_id):
    """
    Configuration the breakout feature for given option.
    :param module: ansible module arguments.
    :param rest_obj: rest object for making requests.
    :param breakout_config: Existing breakout configuration.
    :param breakout_capability: Available breakout configuration.
    :param interface_id: port number with service tag
    :param device_id: device id
    :return: rest object
    """
    breakout_type, response = module.params["breakout_type"], {}
    payload = get_breakout_payload(device_id, breakout_type, interface_id)
    if breakout_config == "HardwareDefault" and not breakout_type == "HardwareDefault":
        for config in breakout_capability:
            if breakout_type == config["Type"]:
                check_mode(module, changes=True)
                response = rest_obj.invoke_request("POST", JOB_URI, data=payload)
                break
        else:
            supported_type = ", ".join(i["Type"] for i in breakout_capability)
            module.fail_json(msg="Invalid breakout type: {0}, supported values are {1}.".format(breakout_type,
                                                                                                supported_type))
    elif not breakout_config == "HardwareDefault" and breakout_type == "HardwareDefault":
        check_mode(module, changes=True)
        response = rest_obj.invoke_request("POST", JOB_URI, data=payload)
    elif breakout_config == breakout_type:
        check_mode(module, changes=False)
        module.exit_json(msg="The port is already configured with the selected breakout configuration.")
    else:
        module.fail_json(msg="Device does not support changing a port breakout"
                             " configuration to different breakout type. Configure the port to"
                             " HardwareDefault and retry the operation.")
    return response


def main():
    module = AnsibleModule(
        argument_spec={
            "hostname": {"required": True, "type": 'str'},
            "username": {"required": True, "type": 'str'},
            "password": {"required": True, "type": 'str', "no_log": True},
            "port": {"required": False, "type": 'int', "default": 443},
            "target_port": {"required": True, "type": 'str'},
            "breakout_type": {"required": True, "type": 'str'},
        },
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            device_id = get_device_id(module, rest_obj)
            breakout_config, breakout_capability, interface_id = get_port_information(module, rest_obj, device_id)
            breakout_status = set_breakout(module, rest_obj, breakout_config,
                                           breakout_capability, interface_id, device_id)
            if breakout_status:
                module.exit_json(msg="Port breakout configuration job submitted successfully.",
                                 breakout_status=breakout_status.json_data, changed=True)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, IndexError, SSLError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
