#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.0
# Copyright (C) 2024-2026 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""Ansible module for querying iDRAC session information, including active sessions,
session service configuration, session limits, and stale session detection.
"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: idrac_session_info
short_description: Query iDRAC session information
version_added: "10.0.0"
description:
  - This module retrieves information about active sessions on a Dell iDRAC.
  - It can query active sessions, session service configuration, and session limits.
  - Supports client-side filtering by session type, username, and stale session detection.
  - This module is read-only and does not modify any sessions.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
  session_type:
    description:
      - Filter sessions by DMTF session type.
      - Case-insensitive exact match against the C(SessionType) field.
    type: str
    required: false
    choices: ['Redfish', 'WebUI', 'IPMI', 'KVMS', 'VirtualMedia', 'OEM']
  username_filter:
    description:
      - Filter sessions by username.
      - Case-insensitive substring match against the C(UserName) field.
    type: str
    required: false
  stale_threshold_minutes:
    description:
      - Flag sessions as stale if their age exceeds this threshold in minutes.
      - Sessions older than this value will have C(is_stale) set to C(true).
      - Must be a positive integer.
    type: int
    required: false
requirements:
  - "python >= 3.9.6"
author:
  - "Saksham Nautiyal (@Saksham-Nautiyal)"
notes:
  - Run this module from a system that has direct access to Dell iDRAC.
  - This module supports IPv4 and IPv6 addresses.
  - This module supports C(check_mode).
  - Minimum firmware versions - iDRAC9 >= 7.10.90.00, iDRAC10 >= 1.20.50.50.
  - Session age is computed from C(CreatedTime), which reflects session creation time, not last activity.
    For true idle time detection, use iDRAC OEM Redfish extensions (future enhancement).
  - For fleet operations, use Ansible C(forks) to parallelize queries across multiple iDRAC instances.
  - Administrator privileges are required to query all sessions. Non-admin users may only see their own sessions.
"""

EXAMPLES = r"""
---
- name: Query all active sessions
  dellemc.openmanage.idrac_session_info:
    idrac_ip: 198.162.0.1
    idrac_user: username
    idrac_password: password
    ca_path: "/path/to/ca_cert.pem"

- name: Filter sessions by type
  dellemc.openmanage.idrac_session_info:
    idrac_ip: 198.162.0.1
    idrac_user: username
    idrac_password: password
    ca_path: "/path/to/ca_cert.pem"
    session_type: Redfish

- name: Find stale sessions older than 24 hours
  dellemc.openmanage.idrac_session_info:
    idrac_ip: 198.162.0.1
    idrac_user: username
    idrac_password: password
    ca_path: "/path/to/ca_cert.pem"
    stale_threshold_minutes: 1440

- name: Filter by username and session type
  dellemc.openmanage.idrac_session_info:
    idrac_ip: 198.162.0.1
    idrac_user: username
    idrac_password: password
    ca_path: "/path/to/ca_cert.pem"
    session_type: Redfish
    username_filter: admin

- name: Query sessions using token authentication
  dellemc.openmanage.idrac_session_info:
    idrac_ip: 198.162.0.1
    ca_path: "/path/to/ca_cert.pem"
    x_auth_token: "aed4aa802b748d2f3b31deec00a6b28a"

- name: Troubleshoot Max Sessions Reached (UC-1)
  block:
    - name: Create a session
      dellemc.openmanage.idrac_session:
        hostname: 198.162.0.1
        username: "{{ vault_idrac_user }}"
        password: "{{ vault_idrac_password }}"
        ca_path: "/path/to/ca_cert.pem"
        state: present
      register: auth_data

    - name: Query session utilization
      dellemc.openmanage.idrac_session_info:
        idrac_ip: 198.162.0.1
        idrac_user: "{{ vault_idrac_user }}"
        idrac_password: "{{ vault_idrac_password }}"
        ca_path: "/path/to/ca_cert.pem"
      register: session_info

    - name: Display utilization
      ansible.builtin.debug:
        msg: "Session utilization: {{ session_info.session_limits.utilization_percent }}%"
  always:
    - name: Destroy the session
      dellemc.openmanage.idrac_session:
        hostname: 198.162.0.1
        ca_path: "/path/to/ca_cert.pem"
        state: absent
        x_auth_token: "{{ auth_data.x_auth_token }}"
        session_id: "{{ auth_data.session_data.Id }}"

- name: Fleet-wide session monitoring (UC-2)
  hosts: idrac_fleet
  gather_facts: false
  tasks:
    - name: Query sessions on each iDRAC
      dellemc.openmanage.idrac_session_info:
        idrac_ip: "{{ inventory_hostname }}"
        idrac_user: "{{ vault_idrac_user }}"
        idrac_password: "{{ vault_idrac_password }}"
        ca_path: "/path/to/ca_cert.pem"
      register: session_info

    - name: Report high utilization
      ansible.builtin.debug:
        msg: "WARNING: {{ inventory_hostname }} at {{ session_info.session_limits.utilization_percent }}% utilization"
      when: session_info.session_limits.utilization_percent | default(0) > 80

- name: Nightly stale session cleanup (UC-3)
  hosts: idrac_fleet
  gather_facts: false
  tasks:
    - name: Find stale sessions
      dellemc.openmanage.idrac_session_info:
        idrac_ip: "{{ inventory_hostname }}"
        idrac_user: "{{ vault_idrac_user }}"
        idrac_password: "{{ vault_idrac_password }}"
        ca_path: "/path/to/ca_cert.pem"
        stale_threshold_minutes: 1440
      register: session_info

    - name: Terminate stale sessions
      dellemc.openmanage.idrac_session:
        hostname: "{{ inventory_hostname }}"
        ca_path: "/path/to/ca_cert.pem"
        state: absent
        x_auth_token: "{{ vault_idrac_auth_token }}"
        session_id: "{{ item.id }}"
      loop: "{{ session_info.sessions | selectattr('is_stale', 'equalto', true) | list }}"
      when: session_info.sessions | selectattr('is_stale', 'equalto', true) | list | length > 0
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
            "id": "74",
            "user_name": "root",
            "client_origin_ip": "100.96.37.58",
            "session_type": "Redfish",
            "created_time": "2024-04-05T01:14:01-05:00",
            "description": "User Session",
            "name": "User Session",
            "session_age_minutes": 120,
            "is_stale": false
        }
    ]
session_count:
    description: Number of sessions returned (after filtering).
    returned: success
    type: int
    sample: 3
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
        "max_sessions": 64,
        "active_count": 5,
        "utilization_percent": 7.81,
        "source": "idrac_attributes"
    }
idrac_firmware_version:
    description: Detected iDRAC firmware version.
    returned: success
    type: str
    sample: "7.10.90.00"
idrac_model:
    description: Detected iDRAC model.
    returned: success
    type: str
    sample: "iDRAC 9"
error_info:
    description: Details of the HTTP Error.
    returned: on HTTP error
    type: dict
    sample: {
        "error": {
            "@Message.ExtendedInfo": [
                {
                    "Message": "Unable to complete the operation.",
                    "MessageId": "IDRAC.2.9.SYS415",
                    "Resolution": "Enter valid credentials.",
                    "Severity": "Warning"
                }
            ],
            "code": "Base.1.12.GeneralError",
            "message": "A general error has occurred."
        }
    }
'''

from datetime import datetime, timezone
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import (
    iDRACRedfishAPI, idrac_auth_params
)

REDFISH = "/redfish/v1"
SESSION_SERVICE_URI = "/redfish/v1/SessionService"
SESSIONS_URI = "/redfish/v1/SessionService/Sessions"
MANAGER_ATTRIBUTES_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Attributes"
MANAGER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"

ALLOWED_SESSION_FIELDS = [
    "Id", "UserName", "ClientOriginIPAddress", "SessionType",
    "CreatedTime", "Description", "Name"
]

SUCCESS_MSG = "Successfully retrieved session information."
FIRMWARE_UNSUPPORTED_MSG = "Minimum firmware requirement not met. Detected: {model} {version}. Required: {minimum}."
NO_SESSIONS_MSG = "No sessions found matching the specified filters."


def compute_session_age(created_time):
    """Compute session age in minutes from CreatedTime string."""
    if not created_time:
        return None
    try:
        created_dt = datetime.fromisoformat(created_time)
        if created_dt.tzinfo is None:
            created_dt = created_dt.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        delta = now - created_dt
        return int(delta.total_seconds() / 60)
    except (ValueError, TypeError):
        return None


def extract_session_fields(session, stale_threshold=None):
    """Extract allowed fields from a session dict and compute derived fields."""
    result = {
        "id": session.get("Id"),
        "user_name": session.get("UserName"),
        "client_origin_ip": session.get("ClientOriginIPAddress"),
        "session_type": session.get("SessionType"),
        "created_time": session.get("CreatedTime"),
        "description": session.get("Description"),
        "name": session.get("Name"),
    }
    age = compute_session_age(result["created_time"])
    result["session_age_minutes"] = age
    if stale_threshold is not None and age is not None:
        result["is_stale"] = age >= stale_threshold
    else:
        result["is_stale"] = False
    return result


def filter_sessions(sessions, session_type=None, username_filter=None):
    """Apply client-side filters to session list using AND logic."""
    filtered = sessions
    if session_type:
        filtered = [s for s in filtered
                    if s.get("session_type") and s["session_type"].lower() == session_type.lower()]
    if username_filter:
        filtered = [s for s in filtered
                    if s.get("user_name") and username_filter.lower() in s["user_name"].lower()]
    return filtered


def get_session_service_config(idrac):
    """Query SessionService for timeout and enabled status."""
    response = idrac.invoke_request(SESSION_SERVICE_URI, "GET")
    if response.status_code == 200:
        data = response.json_data
        return {
            "session_timeout": data.get("SessionTimeout"),
            "service_enabled": data.get("ServiceEnabled"),
        }
    return None


def get_active_sessions(idrac):
    """Retrieve all active sessions from SessionService."""
    expand_uri = SESSIONS_URI + "?$expand=*($levels=1)"
    response = idrac.invoke_request(expand_uri, "GET")
    if response.status_code == 200:
        return response.json_data.get("Members", [])
    return []


def get_session_limits(idrac, active_count):
    """Query session limits. Try iDRAC Attributes first, fall back to Manager endpoint."""
    max_sessions = None
    source = None
    try:
        response = idrac.invoke_request(MANAGER_ATTRIBUTES_URI, "GET")
        if response.status_code == 200:
            attrs = response.json_data.get("Attributes", {})
            max_val = attrs.get("WebServer.1.MaxNumberOfSessions")
            if max_val is not None:
                max_sessions = int(max_val)
                source = "idrac_attributes"
    except (HTTPError, URLError, ValueError, KeyError):
        pass

    if max_sessions is None:
        try:
            response = idrac.invoke_request(MANAGER_URI, "GET")
            if response.status_code == 200:
                data = response.json_data
                max_sessions = data.get("MaxSessions")
                if max_sessions is not None:
                    max_sessions = int(max_sessions)
                    source = "manager_endpoint"
        except (HTTPError, URLError, ValueError, KeyError):
            pass

    if max_sessions is not None and max_sessions > 0:
        utilization = round((active_count / max_sessions) * 100, 2)
        return {
            "max_sessions": max_sessions,
            "active_count": active_count,
            "utilization_percent": utilization,
            "source": source,
        }
    return None


def main():
    argument_spec = idrac_auth_params.copy()
    argument_spec.update({
        "session_type": {
            "type": "str",
            "required": False,
            "choices": ["Redfish", "WebUI", "IPMI", "KVMS", "VirtualMedia", "OEM"],
        },
        "username_filter": {
            "type": "str",
            "required": False,
        },
        "stale_threshold_minutes": {
            "type": "int",
            "required": False,
        },
    })

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    stale_threshold = module.params.get("stale_threshold_minutes")
    if stale_threshold is not None and stale_threshold <= 0:
        module.fail_json(msg="stale_threshold_minutes must be a positive integer.")

    warnings = []

    try:
        with iDRACRedfishAPI(module.params) as idrac:
            # FR-1: Firmware version gate
            generation, firmware_version, hw_model = idrac.get_server_generation
            is_compliant, minimum_version, error_msg = iDRACRedfishAPI.check_minimum_firmware_requirement(
                hw_model, firmware_version
            )
            if not is_compliant:
                module.fail_json(
                    msg=FIRMWARE_UNSUPPORTED_MSG.format(
                        model=hw_model, version=firmware_version, minimum=minimum_version
                    )
                )

            # FR-2: Active session query
            raw_sessions = get_active_sessions(idrac)

            # FR-4: Session age computation + extract fields
            sessions = []
            for raw in raw_sessions:
                session = extract_session_fields(raw, stale_threshold)
                if raw.get("SessionType") is None:
                    warnings.append("SessionType not available on this firmware version.")
                if raw.get("CreatedTime") is None:
                    warnings.append("CreatedTime not available; session age cannot be computed.")
                sessions.append(session)

            # FR-5: Client-side filtering
            session_type_filter = module.params.get("session_type")
            username_filter = module.params.get("username_filter")
            sessions = filter_sessions(sessions, session_type_filter, username_filter)

            if not sessions and (session_type_filter or username_filter):
                warnings.append(NO_SESSIONS_MSG)

            # FR-3: Session service configuration
            session_service = get_session_service_config(idrac)
            if session_service and not session_service.get("service_enabled"):
                warnings.append("SessionService is disabled on this iDRAC.")

            # FR-6: Session limits query
            session_limits = get_session_limits(idrac, len(raw_sessions))
            if session_limits is None:
                warnings.append("Unable to determine session limits.")

            # Deduplicate warnings
            warnings = list(dict.fromkeys(warnings))

            module.exit_json(
                msg=SUCCESS_MSG,
                changed=False,
                sessions=sessions,
                session_count=len(sessions),
                session_service=session_service,
                session_limits=session_limits,
                idrac_firmware_version=firmware_version,
                idrac_model=hw_model,
                warnings=warnings,
            )

    except HTTPError as e:
        if e.code in [401, 403]:
            module.fail_json(msg="Authentication failed: {0}".format(e.msg))
        else:
            module.fail_json(msg="HTTP error {0}: {1}".format(e.code, e.msg))
    except SSLValidationError as e:
        module.fail_json(msg="SSL validation error: {0}".format(str(e)))
    except ConnectionError as e:
        module.fail_json(msg="Connection error: {0}".format(str(e)))
    except URLError as e:
        module.fail_json(msg="Network error: {0}".format(str(e)))
    except Exception as e:
        if type(e).__name__ in ['AnsibleExitJson', 'AnsibleFailJson']:
            raise
        module.fail_json(msg="Unexpected error: {0}".format(str(e)))


if __name__ == '__main__':
    main()
