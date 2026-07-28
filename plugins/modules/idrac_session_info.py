#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.1
# Copyright (C) 2024-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: idrac_session_info
short_description: Query iDRAC session information
version_added: "9.13.0"
description:
  - This module queries active iDRAC sessions, session service configuration,
    and session limits with utilization reporting.
  - Supports client-side filtering by session type, username, and stale
    threshold.
  - This module is read-only and does not modify any state on the iDRAC.
options:
  idrac_ip:
    description: IP address or hostname of the iDRAC.
    type: str
    required: true
  idrac_user:
    description: Username of the iDRAC.
    type: str
    required: true
  idrac_password:
    description: Password of the iDRAC.
    type: str
    required: true
  port:
    description: Port of the iDRAC.
    type: int
    default: 443
  validate_certs:
    description: If C(false), the SSL certificates will not be validated.
    type: bool
    default: true
  ca_path:
    description: The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.
    type: path
  timeout:
    description: The https socket level timeout in seconds.
    type: int
    default: 30
  session_type:
    description:
      - Filter sessions by DMTF SessionType enum value.
      - Case-insensitive matching.
      - Valid values include C(Redfish), C(IPMI), C(OEM), C(WebUI), etc.
    type: str
    choices: ['Redfish', 'IPMI', 'OEM', 'WebUI', 'VirtualMedia', 'KVMIP']
  username_filter:
    description:
      - Filter sessions by username substring match.
      - Case-insensitive matching.
    type: str
  stale_threshold_minutes:
    description:
      - Flag sessions older than the specified number of minutes as stale.
      - Must be a positive integer.
      - Session age is computed from C(CreatedTime); this is a proxy for
        idle time as iDRAC Redfish has no C(LastAccessedTime).
    type: int
requirements:
  - "python >= 3.9.6"
author:
  - "Saksham Nautiyal (@Saksham-Nautiyal)"
notes:
  - Run this module from a system that has direct access to Dell iDRAC.
  - This module supports IPv4 and IPv6 addresses.
  - This module supports C(check_mode).
  - Minimum firmware requirements - iDRAC9 >= 7.10.90.00, iDRAC10 >= 1.20.50.50.
  - Session age is computed from C(CreatedTime) and is a proxy for idle time.
  - Output is structured JSON via C(exit_json()). To export as CSV or text,
    use Ansible native filters (C(to_json), C(to_nice_yaml)) or Jinja2 templates.
"""

EXAMPLES = r"""
---
- name: Query all active iDRAC sessions
  dellemc.openmanage.idrac_session_info:
    idrac_ip: 198.162.0.1
    idrac_user: admin
    idrac_password: password
    ca_path: "/path/to/ca_cert.pem"

- name: Filter sessions by type
  dellemc.openmanage.idrac_session_info:
    idrac_ip: 198.162.0.1
    idrac_user: admin
    idrac_password: password
    session_type: Redfish

- name: Find stale sessions older than 24 hours
  dellemc.openmanage.idrac_session_info:
    idrac_ip: 198.162.0.1
    idrac_user: admin
    idrac_password: password
    stale_threshold_minutes: 1440

- name: Filter sessions by username
  dellemc.openmanage.idrac_session_info:
    idrac_ip: 198.162.0.1
    idrac_user: admin
    idrac_password: password
    username_filter: root

- name: Combined filtering
  dellemc.openmanage.idrac_session_info:
    idrac_ip: 198.162.0.1
    idrac_user: admin
    idrac_password: password
    session_type: Redfish
    username_filter: admin
    stale_threshold_minutes: 60

- name: Export session data to CSV file using Jinja2 template
  block:
    - name: Query sessions
      dellemc.openmanage.idrac_session_info:
        idrac_ip: 198.162.0.1
        idrac_user: admin
        idrac_password: password
      register: result

    - name: Write CSV report
      ansible.builtin.copy:
        content: |
          Id,UserName,SessionType,ClientOriginIPAddress,CreatedTime,AgeMinutes
          {% for s in result.sessions %}
          {{ s.Id }},{{ s.UserName }},{{ s.SessionType }},{{ s.ClientOriginIPAddress }},{{ s.CreatedTime }},{{ s.session_age_minutes }}
          {% endfor %}
        dest: /tmp/session_report.csv
      delegate_to: localhost

- name: Display session data as YAML
  block:
    - name: Query sessions
      dellemc.openmanage.idrac_session_info:
        idrac_ip: 198.162.0.1
        idrac_user: admin
        idrac_password: password
      register: result

    - name: Show sessions in YAML format
      ansible.builtin.debug:
        msg: "{{ result.sessions | to_nice_yaml }}"
"""

RETURN = r'''
---
msg:
    description: Status of the session query operation.
    returned: always
    type: str
    sample: "Successfully retrieved session information."
sessions:
    description: List of active sessions with details.
    returned: success
    type: list
    elements: dict
    sample: [
        {
            "id": "1",
            "username": "root",
            "client_origin_ip": "192.168.1.10",
            "session_type": "Redfish",
            "created_time": "2024-07-28T10:00:00+00:00",
            "description": "User Session",
            "session_age_minutes": 30,
            "is_stale": false
        }
    ]
session_count:
    description: Number of sessions returned (after filtering).
    returned: success
    type: int
    sample: 2
session_service:
    description: Session service configuration.
    returned: success
    type: dict
    sample: {
        "session_timeout": 1800,
        "service_enabled": true
    }
session_limits:
    description: Session limits and utilization.
    returned: success
    type: dict
    sample: {
        "max_sessions": 8,
        "active_sessions": 2,
        "utilization_percent": 25.0
    }
'''


from datetime import datetime, timezone
from urllib.error import HTTPError, URLError

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import (
    iDRACRedfishAPI, idrac_auth_params,
)

SESSION_SERVICE_URI = "/redfish/v1/SessionService"
SESSIONS_URI = "/redfish/v1/SessionService/Sessions"
MANAGER_ATTRIBUTES_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Attributes"
MANAGER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"

SUCCESS_MSG = "Successfully retrieved session information."
NO_SESSIONS_MSG = "No active sessions found."
FIRMWARE_ERROR_MSG = ("Minimum firmware requirement not met. Detected: {model} {version}. "
                      "Minimum required: {min_version}. Please upgrade firmware.")


def _parse_created_time(created_time_str):
    """Parse CreatedTime string to datetime object. Returns None on failure."""
    if not created_time_str:
        return None
    try:
        return datetime.fromisoformat(created_time_str)
    except (ValueError, TypeError):
        return None


def _compute_session_age(created_time_str):
    """Compute session age in minutes from CreatedTime string."""
    created = _parse_created_time(created_time_str)
    if created is None:
        return None
    now = datetime.now(timezone.utc)
    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)
    delta = now - created
    return int(delta.total_seconds() / 60)


def _normalize_session(raw_session, stale_threshold=None):
    """Normalize a raw Redfish session dict to a clean output dict."""
    created_time = raw_session.get("CreatedTime")
    age_minutes = _compute_session_age(created_time)

    session = {
        "id": raw_session.get("Id"),
        "username": raw_session.get("UserName"),
        "client_origin_ip": raw_session.get("ClientOriginIPAddress"),
        "session_type": raw_session.get("SessionType"),
        "created_time": created_time,
        "description": raw_session.get("Description"),
        "session_age_minutes": age_minutes,
    }

    if stale_threshold is not None and age_minutes is not None:
        session["is_stale"] = age_minutes >= stale_threshold
    else:
        session["is_stale"] = False

    return session


def _filter_sessions(sessions, session_type=None, username_filter=None):
    """Apply client-side filters to session list."""
    filtered = sessions
    if session_type:
        st_lower = session_type.lower()
        filtered = [s for s in filtered
                    if s.get("session_type") and s["session_type"].lower() == st_lower]
    if username_filter:
        uf_lower = username_filter.lower()
        filtered = [s for s in filtered
                    if s.get("username") and uf_lower in s["username"].lower()]
    return filtered


def _query_sessions(idrac):
    """Query all sessions via Redfish API."""
    resp = idrac.invoke_request(
        SESSIONS_URI, "GET",
        query_param={"$expand": "*($levels=1)"}
    )
    members = resp.json_data.get("Members", [])
    return members


def _query_session_service(idrac):
    """Query SessionService configuration."""
    resp = idrac.invoke_request(SESSION_SERVICE_URI, "GET")
    data = resp.json_data
    return {
        "session_timeout": data.get("SessionTimeout"),
        "service_enabled": data.get("ServiceEnabled"),
    }


def _query_session_limits(idrac, active_count):
    """Query session limits. Try Attributes first, fall back to Manager."""
    max_sessions = None

    try:
        attr_resp = idrac.invoke_request(MANAGER_ATTRIBUTES_URI, "GET")
        attrs = attr_resp.json_data.get("Attributes", {})
        max_sessions = attrs.get("WebServer.1.MaxSessions")
    except HTTPError:
        pass

    if max_sessions is None:
        try:
            mgr_resp = idrac.invoke_request(MANAGER_URI, "GET")
            mgr_data = mgr_resp.json_data
            oem = mgr_data.get("Oem", {}).get("Dell", {})
            max_sessions = oem.get("MaxSessions")
        except HTTPError:
            pass

    utilization = None
    if max_sessions is not None and max_sessions > 0:
        utilization = round((active_count / max_sessions) * 100, 1)

    return {
        "max_sessions": max_sessions,
        "active_sessions": active_count,
        "utilization_percent": utilization,
    }


def main():
    specs = dict(idrac_auth_params)
    specs.update({
        "session_type": {
            "type": "str",
            "choices": ["Redfish", "IPMI", "OEM", "WebUI", "VirtualMedia", "KVMIP"],
        },
        "username_filter": {"type": "str"},
        "stale_threshold_minutes": {"type": "int"},
    })

    module = AnsibleModule(
        argument_spec=specs,
        supports_check_mode=True,
    )

    stale_threshold = module.params.get("stale_threshold_minutes")
    if stale_threshold is not None and stale_threshold <= 0:
        module.fail_json(msg="stale_threshold_minutes must be a positive integer.")

    try:
        with iDRACRedfishAPI(module.params, req_session=True) as idrac:
            generation, firmware_version, idrac_model = idrac.get_server_generation
            is_compliant, min_ver, err_msg = iDRACRedfishAPI.check_minimum_firmware_requirement(
                idrac_model, firmware_version
            )
            if not is_compliant:
                module.fail_json(msg=err_msg)

            raw_sessions = _query_sessions(idrac)

            sessions = [
                _normalize_session(s, stale_threshold)
                for s in raw_sessions
            ]

            sessions = _filter_sessions(
                sessions,
                session_type=module.params.get("session_type"),
                username_filter=module.params.get("username_filter"),
            )

            session_service = _query_session_service(idrac)
            session_limits = _query_session_limits(idrac, len(sessions))

            msg = SUCCESS_MSG if sessions else NO_SESSIONS_MSG
            module.exit_json(
                changed=False,
                msg=msg,
                sessions=sessions,
                session_count=len(sessions),
                session_service=session_service,
                session_limits=session_limits,
            )
    except HTTPError as err:
        module.exit_json(msg=str(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True, failed=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
