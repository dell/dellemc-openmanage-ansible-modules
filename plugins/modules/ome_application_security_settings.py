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

DOCUMENTATION = r'''
---
module: ome_application_security_settings
short_description: Configure the login security properties
description: This module allows you to configure the login security properties on OpenManage Enterprise or OpenManage Enterprise Modular
version_added: "4.4.0"
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  restrict_allowed_ip_range:
    description:
      - Restrict to allow inbound connections only from the specified IP address range.
      - This is mutually exclusive with I(fips_mode_enable).
      - "C(NOTE) When I(restrict_allowed_ip_range) is configured on the appliance, any inbound connection to the appliance,
      such as alert reception, firmware update, and network identities are blocked from the devices that are
      outside the specified IP address range. However, any outbound connection from the appliance will work on all devices."
    type: dict
    suboptions:
      enable_ip_range:
        description: Allow connections based on the IP address range.
        type: bool
        required: true
      ip_range:
        description: "The IP address range in Classless Inter-Domain Routing (CIDR) format.
        For example: 192.168.100.14/24 or 2001:db8::/24"
        type: str
  login_lockout_policy:
    description:
      - Locks the application after multiple unsuccessful login attempts.
      - This is mutually exclusive with I(fips_mode_enable).
    type: dict
    suboptions:
      by_user_name:
        description: "Enable or disable lockout policy settings based on the user name. This restricts the number of
        unsuccessful login attempts from a specific user for a specific time interval."
        type: bool
      by_ip_address:
        description: "Enable or disable lockout policy settings based on the IP address. This restricts the number of
        unsuccessful login attempts from a specific IP address for a specific time interval."
        type: bool
      lockout_fail_count:
        description: "The number of unsuccessful login attempts that are allowed after which the appliance prevents log
        in from the specific  username or IP Address."
        type: int
      lockout_fail_window:
        description: "Lockout fail window is the time in seconds within which the lockout fail count event must occur to
        trigger the lockout penalty time. Enter the duration for which OpenManage Enterprise must display information
        about a failed attempt."
        type: int
      lockout_penalty_time:
        description: "The duration of time, in seconds, that login attempts from the specific user or IP address must
        not be allowed."
        type: int
  job_wait:
    description:
      - Provides an option to wait for job completion.
    type: bool
    default: true
  job_wait_timeout:
    description:
      - The maximum wait time of I(job_wait) in seconds. The job is tracked only for this duration.
      - This option is applicable when I(job_wait) is C(True).
    type: int
    default: 120
  fips_mode_enable:
    description:
      - "The FIPS mode is intended to meet the requirements of FIPS 140-2 level 1. For more information refer to the FIPS
      user guide"
      - This is applicable only for OpenManage Enterprise Modular only
      - This is mutually exclusive with I(restrict_allowed_ip_range) and I(login_lockout_policy).
      - "C(WARNING) Enabling or Disabling this option resets your chassis to default settings. This may cause change in
      IP settings and loss of network connectivity."
      - "C(WARNING) The FIPS mode cannot be enabled on a lead chassis in a multi-chassis management configuration. To toggle
      enable FIPS on a lead chassis, delete the chassis group, enable FIPS and recreate the group."
      - "C(WARNING) For a Standalone or member chassis, enabling the FIPS mode deletes any fabrics created. This may cause
      loss of network connectivity and data paths to the compute sleds."
    type: bool
author:
  - Jagadeesh N V(@jagadeeshnv)
requirements:
    - "python >= 3.8.6"
notes:
    - Run this module from a system that has direct access to DellEMC OpenManage Enterprise or OpenManage Enterprise Modular.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Configure restricted allowed IP range
  dellemc.openmanage.ome_application_security_settings:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    restrict_allowed_ip_range:
      enable_ip_range: true
      ip_range: 192.1.2.3/24

- name: Configure login lockout policy
  dellemc.openmanage.ome_application_security_settings:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    login_lockout_policy:
      by_user_name: true
      by_ip_address: true
      lockout_fail_count: 3
      lockout_fail_window: 30
      lockout_penalty_time: 900

- name: Configure restricted allowed IP range and login lockout policy with job wait time out of 60 seconds
  dellemc.openmanage.ome_application_security_settings:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    restrict_allowed_ip_range:
      enable_ip_range: true
      ip_range: 192.1.2.3/24
    login_lockout_policy:
      by_user_name: true
      by_ip_address: true
      lockout_fail_count: 3
      lockout_fail_window: 30
      lockout_penalty_time: 900
    job_wait_timeout: 60

- name: Enable FIPS mode
  dellemc.openmanage.ome_application_security_settings:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    fips_mode_enable: yes
'''

RETURN = r'''
---
msg:
  description: Overall status of the login security configuration.
  returned: always
  type: str
  sample: "Successfully applied the security settings."
job_id:
  description: Job ID of the security configuration task.
  returned: When security configuration properties are provided
  type: int
  sample: 10123
error_info:
  type: dict
  description: Details of http error.
  returned: on http error
  sample: {
    "error": {
        "@Message.ExtendedInfo": [
            {
                "Message": "Unable to process the request because the domain information cannot be retrieved.",
                "MessageArgs": [],
                "MessageId": "CGEN8007",
                "RelatedProperties": [],
                "Resolution": "Verify the status of the database and domain configuration, and then retry the
                operation.",
                "Severity": "Critical"
            }
        ],
        "code": "Base.1.0.GeneralError",
        "message": "A general error has occurred. See ExtendedInfo for more information."
    }
}
'''

GET_SETTINGS = "ApplicationService/Actions/ApplicationService.GetConfiguration"
SET_SETTINGS = "ApplicationService/Actions/ApplicationService.ApplyConfiguration"
FIPS_MODE = "ApplicationService/Security/SecurityConfiguration"
JOB_EXEC_HISTORY = "JobService/Jobs({job_id})/ExecutionHistories"
SEC_JOB_TRIGGERED = "Successfully triggered the job to apply security settings."
SEC_JOB_COMPLETE = "Successfully applied the security settings."
FIPS_TOGGLED = "Successfully {0} the FIPS mode."
FIPS_CONN_RESET = "The network connection may have changed. Verify the connection and try again."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
SETTLING_TIME = 2
JOB_POLL_INTERVAL = 3

import json
import time
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


def fips_mode_enable(module, rest_obj):
    resp = rest_obj.invoke_request("GET", FIPS_MODE)
    fips_payload = resp.json_data
    curr_fips_mode = fips_payload.get("FipsMode")
    if module.params.get("fips_mode_enable") is True:
        fips_mode = "ON"
    else:
        fips_mode = "OFF"
    if curr_fips_mode.lower() == fips_mode.lower():
        module.exit_json(msg=NO_CHANGES_MSG)
    if module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    payload = rest_obj.strip_substr_dict(fips_payload)
    payload["FipsMode"] = fips_mode
    rest_obj.invoke_request("PUT", FIPS_MODE, data=payload)
    module.exit_json(msg=FIPS_TOGGLED.format("disabled" if fips_mode == "OFF" else "enabled"), changed=True)


def get_security_payload(rest_obj):
    resp = rest_obj.invoke_request("POST", GET_SETTINGS, data={})
    full_set = resp.json_data
    comps = full_set.get("SystemConfiguration", {}).get("Components", [{"Attributes": []}])
    attribs = comps[0].get("Attributes")
    attr_dict = dict(
        [(sys.get('Name'), sys.get("Value")) for sys in attribs if "loginsecurity" in sys.get('Name').lower()])
    return full_set, attr_dict


def compare_merge(module, attr_dict):
    val_map = {
        "ip_range": "LoginSecurity.1#IPRangeAddr",
        "enable_ip_range": "LoginSecurity.1#IPRangeEnable",
        "by_ip_address": "LoginSecurity.1#LockoutByIPEnable",
        "by_user_name": "LoginSecurity.1#LockoutByUsernameEnable",
        "lockout_fail_count": "LoginSecurity.1#LockoutFailCount",
        "lockout_fail_window": "LoginSecurity.1#LockoutFailCountTime",
        "lockout_penalty_time": "LoginSecurity.1#LockoutPenaltyTime"
    }
    diff = 0
    inp_dicts = ["restrict_allowed_ip_range", "login_lockout_policy"]
    for d in inp_dicts:
        inp_dict = module.params.get(d, {})
        if inp_dict:
            for k, v in inp_dict.items():
                if v is not None:
                    if attr_dict[val_map[k]] != v:
                        attr_dict[val_map[k]] = v
                        diff = diff + 1
    if attr_dict.get("LoginSecurity.1#IPRangeEnable") is False:
        if attr_dict.get("LoginSecurity.1#IPRangeAddr") is not None:
            attr_dict["LoginSecurity.1#IPRangeAddr"] = None
            diff = diff - 1
    if not diff:
        module.exit_json(msg=NO_CHANGES_MSG)
    if module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    return attr_dict


def get_execution_details(rest_obj, job_id, job_message):
    try:
        resp = rest_obj.invoke_request('GET', JOB_EXEC_HISTORY.format(job_id=job_id))
        ex_hist = resp.json_data.get('value')
        # Sorting based on startTime and to get latest execution instance.
        tmp_dict = dict((x["StartTime"], x["Id"]) for x in ex_hist)
        sorted_dates = sorted(tmp_dict.keys())
        ex_url = JOB_EXEC_HISTORY.format(job_id=job_id) + "({0})/ExecutionHistoryDetails".format(tmp_dict[sorted_dates[-1]])
        resp = rest_obj.invoke_request('GET', ex_url)
        ex_hist = resp.json_data.get('value')
        message = job_message
        if len(ex_hist) > 0:
            message = ex_hist[0].get("Value")
    except Exception:
        message = job_message
    message = message.replace('\n', '. ')
    return message


def exit_settings(module, rest_obj, job_id):
    msg = SEC_JOB_TRIGGERED
    time.sleep(SETTLING_TIME)
    if module.params.get("job_wait"):
        job_failed, job_message = rest_obj.job_tracking(
            job_id=job_id, job_wait_sec=module.params["job_wait_timeout"], sleep_time=JOB_POLL_INTERVAL)
        if job_failed is True:
            job_message = get_execution_details(rest_obj, job_id, job_message)
            module.exit_json(msg=job_message, failed=True, job_id=job_id)
        msg = SEC_JOB_COMPLETE
    module.exit_json(msg=msg, job_id=job_id, changed=True)


def login_security_setting(module, rest_obj):
    security_set, attr_dict = get_security_payload(rest_obj)
    new_attr_dict = compare_merge(module, attr_dict)
    comps = security_set.get("SystemConfiguration", {}).get("Components", [{"Attributes": []}])
    comps[0]["Attributes"] = [{"Name": k, "Value": v} for k, v in new_attr_dict.items()]
    resp = rest_obj.invoke_request("POST", SET_SETTINGS, data=security_set)
    job_id = resp.json_data.get("JobId")
    exit_settings(module, rest_obj, job_id)


def main():
    specs = {
        "restrict_allowed_ip_range": {
            "type": 'dict', "options": {
                "enable_ip_range": {"type": 'bool', "required": True},
                "ip_range": {"type": 'str'}
            },
            "required_if": [("enable_ip_range", True, ("ip_range",))]
        },
        "login_lockout_policy": {
            "type": 'dict', "options": {
                "by_user_name": {"type": 'bool'},
                "by_ip_address": {"type": 'bool'},
                "lockout_fail_count": {"type": 'int'},
                "lockout_fail_window": {"type": 'int'},
                "lockout_penalty_time": {"type": 'int'}
            },
            "required_one_of": [("by_user_name", "by_ip_address", "lockout_fail_count",
                                 "lockout_fail_window", "lockout_penalty_time")]
        },
        "fips_mode_enable": {"type": 'bool'},
        "job_wait": {"type": 'bool', "default": True},
        "job_wait_timeout": {"type": 'int', "default": 120}
    }
    specs.update(ome_auth_params)

    module = AnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[("fips_mode_enable", "login_lockout_policy"),
                            ("fips_mode_enable", "restrict_allowed_ip_range")],
        required_one_of=[("restrict_allowed_ip_range", "login_lockout_policy", "fips_mode_enable")],
        supports_check_mode=True)

    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            if module.params.get("fips_mode_enable") is not None:
                fips_mode_enable(module, rest_obj)
            else:
                login_security_setting(module, rest_obj)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, TypeError, SSLError, ConnectionError, SSLValidationError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
