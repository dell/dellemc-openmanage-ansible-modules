#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.3
# Copyright (C) 2020-2025 Dell Inc. or its subsidiaries.  All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_application_network_time
short_description: Updates the network time on OpenManage Enterprise
version_added: "2.1.0"
description: This module allows the configuration of network time on OpenManage Enterprise.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  enable_ntp:
    description:
      - Enables or disables Network Time Protocol(NTP).
      - If I(enable_ntp) is false, then the NTP addresses reset to their default values.
    required: true
    type: bool
  system_time:
    description:
      - Time in the current system.
      - This option is only applicable when I(enable_ntp) is false.
      - This option must be provided in following format 'yyyy-mm-dd hh:mm:ss'.
    type: str
  time_zone:
    description:
      - The valid timezone ID to be used.
      - This option is applicable for both system time and NTP time synchronization.
    type: str
  primary_ntp_address:
    description:
      - The primary NTP address.
      - This option is applicable when I(enable_ntp) is true.
    type: str
  secondary_ntp_address1:
    description:
      - The first secondary NTP address.
      - This option is applicable when I(enable_ntp) is true.
    type: str
  secondary_ntp_address2:
    description:
      - The second secondary NTP address.
      - This option is applicable when I(enable_ntp) is true.
    type: str
requirements:
    - "python >= 3.9.6"
author:
    - "Sajna Shetty(@Sajna-Shetty)"
    - "Mangirish Kenkare(@MangirishK)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Configure system time
  dellemc.openmanage.ome_application_network_time:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    enable_ntp: false
    system_time: "2020-03-31 21:35:18"
    time_zone: "TZ_ID_11"

- name: Configure NTP server for time synchronization
  dellemc.openmanage.ome_application_network_time:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    enable_ntp: true
    time_zone: "TZ_ID_66"
    primary_ntp_address: "192.168.0.2"
    secondary_ntp_address1: "192.168.0.2"
    secondary_ntp_address2: "192.168.0.4"
'''

RETURN = r'''
---
msg:
  type: str
  description: Overall status of the network time configuration change.
  returned: always
  sample: "Successfully configured network time."
proxy_configuration:
  type: dict
  description: Updated application network time configuration.
  returned: success
  sample: {
    "EnableNTP": false,
    "JobId": null,
    "PrimaryNTPAddress": null,
    "SecondaryNTPAddress1": null,
    "SecondaryNTPAddress2": null,
    "SystemTime": null,
    "TimeSource": "Local Clock",
    "TimeZone": "TZ_ID_1",
    "TimeZoneIdLinux": null,
    "TimeZoneIdWindows": null,
    "UtcTime": null
    }
error_info:
  description: Details of the HTTP error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
    "@Message.ExtendedInfo": [
        {
            "Message":  "Unable to complete the request because the input value
             for  SystemTime  is missing or an invalid value is entered.",
            "MessageArgs": [
                    "SystemTime"
            ],
            "MessageId": "CGEN6002",
            "RelatedProperties": [],
            "Resolution": "Enter a valid value and retry the operation.",
            "Severity": "Critical"
            }
        ],
        "code": "Base.1.0.GeneralError",
        "message": "A general error has occurred. See ExtendedInfo for more information."
        }
    }
'''

import json
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError

TIME_CONFIG = "ApplicationService/Network/TimeConfiguration"
TIME_ZONE = "ApplicationService/Network/TimeZones"


def remove_unwanted_keys(key_list, payload):
    [payload.pop(key) for key in key_list if key in payload]


def get_payload(module):
    params = module.params
    proxy_payload_map = {
        "enable_ntp": "EnableNTP",
        "time_zone": "TimeZone",
        "system_time": "SystemTime",
        "primary_ntp_address": "PrimaryNTPAddress",
        "secondary_ntp_address1": "SecondaryNTPAddress1",
        "secondary_ntp_address2": "SecondaryNTPAddress2"
    }
    backup_params = params.copy()
    remove_keys = ["hostname", "username", "password", "port", "ca_path", "validate_certs", "timeout"]
    remove_unwanted_keys(remove_keys, backup_params)
    payload = dict([(proxy_payload_map[key], val) for key, val in backup_params.items() if val is not None])
    return payload


def update_time_config_output(back_up_settings):
    remove_keys = ["@odata.context", "@odata.type", "@odata.id"]
    remove_unwanted_keys(remove_keys, back_up_settings)
    back_up_settings.update({"JobId": None})


def get_updated_payload(rest_obj, module, payload):
    remove_keys = ["@odata.context", "@odata.type", "@odata.id", "TimeZoneIdLinux", "TimeZoneIdWindows", "TimeSource", "UtcTime"]
    resp = rest_obj.invoke_request("GET", TIME_CONFIG, api_timeout=150)
    current_setting = resp.json_data
    back_up_settings = current_setting.copy()
    remove_unwanted_keys(remove_keys, current_setting)
    diff = any(key in current_setting and val != current_setting[key] for key, val in payload.items())
    if module.check_mode:
        if diff:
            module.exit_json(changed=True, msg="Changes found to be applied to the time configuration.")
        else:
            module.exit_json(changed=False, msg="No changes found to be applied to the time configuration.")
    else:
        if diff:
            current_setting.update(payload)
        else:
            update_time_config_output(back_up_settings)
            module.exit_json(changed=False, msg="No changes made to the time configuration as the entered"
                                                " values are the same as the current configuration.", time_configuration=back_up_settings)
    return current_setting


def validate_time_zone(module, rest_obj):
    params = module.params
    time_zone = params.get("time_zone", None)
    if time_zone is not None:
        time_zone_resp = rest_obj.invoke_request("GET", TIME_ZONE)
        time_zone_val = time_zone_resp.json_data["value"]
        time_id_list = [time_dict["Id"] for time_dict in time_zone_val]
        if time_zone not in time_id_list:
            sorted_time_id_list = sorted(time_id_list, key=lambda time_id: [int(i) for i in time_id.split("_") if i.isdigit()])
            module.exit_json(msg="Provide valid time zone.Choices are {0}".format(",".join(sorted_time_id_list)), failed=True)


def validate_input(module):
    system_time = module.params.get("system_time")
    enable_ntp = module.params["enable_ntp"]
    primary_ntp_address = module.params.get("primary_ntp_address")
    secondary_ntp_address1 = module.params.get("secondary_ntp_address1")
    secondary_ntp_address2 = module.params.get("secondary_ntp_address2")
    if enable_ntp is True and system_time is not None:
        module.exit_json(msg="When enable NTP is true,the option system time is not accepted.", failed=True)
    if enable_ntp is False and any([primary_ntp_address, secondary_ntp_address1, secondary_ntp_address2]):
        module.exit_json(msg="When enable NTP is false,the option(s) primary_ntp_address, secondary_ntp_address1 and secondary_ntp_address2 is not accepted.",
                         failed=True)


def main():
    specs = {
        "enable_ntp": {"required": True, "type": "bool"},
        "time_zone": {"required": False, "type": "str"},
        "system_time": {"required": False, "type": "str"},
        "primary_ntp_address": {"required": False, "type": "str"},
        "secondary_ntp_address1": {"required": False, "type": "str"},
        "secondary_ntp_address2": {"required": False, "type": "str"},
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        required_if=[['enable_ntp', False, ('time_zone', 'system_time',), True],
                     ['enable_ntp', True, ('time_zone', 'primary_ntp_address',
                                           'secondary_ntp_address1', 'secondary_ntp_address2'), True]],
        mutually_exclusive=[['system_time', 'primary_ntp_address'],
                            ['system_time', 'secondary_ntp_address1'],
                            ['system_time', 'secondary_ntp_address2']],
        supports_check_mode=True,
    )
    try:
        validate_input(module)
        with RestOME(module.params, req_session=False) as rest_obj:
            validate_time_zone(module, rest_obj)
            payload = get_payload(module)
            updated_payload = get_updated_payload(rest_obj, module, payload)
            resp = rest_obj.invoke_request("PUT", TIME_CONFIG, data=updated_payload, api_timeout=150)
            module.exit_json(msg="Successfully configured network time.", time_configuration=resp.json_data, changed=True)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, SSLValidationError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == "__main__":
    main()
