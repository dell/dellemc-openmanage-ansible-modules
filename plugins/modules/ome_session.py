#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2024-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ome_session
short_description: Manage OpenManage Enterprise and OpenManage Enterprise modular sessions
version_added: "9.3.0"
description:
  - This module allows you  to create and delete sessions on OpenManage Enterprise and OpenManage Enterprise Modular.
options:
  hostname:
    description:
      - IP address or hostname of the OpenManage Enterprise.
    type: str
  username:
    description:
      - Username of the OpenManage Enterprise. If the username is not provided, then
        the environment variable E(OME_USERNAME) is used.
      - I(username) is required when I(state) is C(present).
    type: str
  password:
    description:
      - Password of the OpenManage Enterprise. If the password is not provided, then
        the environment variable E(OME_PASSWORD) is used.
      - I(password) is required when I(state) is C(present).
    type: str
  port:
    description:
      - Port of the OpenManage Enterprise.
    type: int
    default: 443
  validate_certs:
    description:
     - If C(false), the SSL certificates will not be validated.
     - Configure C(false) only on personally controlled sites where self-signed certificates are used.
    type: bool
    default: true
  ca_path:
    description:
     - The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.
    type: path
  timeout:
    description:
     - The HTTPS socket level timeout in seconds.
    type: int
    default: 30
  state:
    description:
     - The state of the session in OpenManage Enterprise.
     - C(present) creates a session.
     - C(absent) deletes a session.
     - Module will always report changes found to be applied when I(state) is C(present).
    choices: [present, absent]
    type: str
    default: present
  x_auth_token:
    description:
     - Authentication token.
     - I(x_auth_token) is required when I(state) is C(absent).
    type: str
    aliases: ['auth_token']
  session_id:
    description:
     - Session ID of the OpenManage Enterprise.
     - I(session_id) is required when I(state) is C(absent).
    type: str
requirements:
  - "python >= 3.9.6"
author:
  - "Kritika Bhateja (@Kritika-Bhateja-03)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
    - This module supports IPv4 and IPv6 addresses.
    - This module supports C(check_mode).
    - This module will always report changes found to be applied when I(state) is C(present).
"""

EXAMPLES = r"""
---
- name: Create a session
  dellemc.openmanage.ome_session:
    hostname: 198.162.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    state: present

- name: Delete a session
  dellemc.openmanage.ome_session:
    hostname: 198.162.0.1
    ca_path: "/path/to/ca_cert.pem"
    state: absent
    x_auth_token: aed4aa802b748d2f3b31deec00a6b28a
    session_id: 4b48e9ab-809e-4087-b7c4-201a16e0143d

- name: Create a session and execute other modules
  block:
    - name: Create a session
      dellemc.openmanage.ome_session:
        hostname: 198.162.0.1
        username: username
        password: password
        ca_path: "/path/to/ca_cert.pem"
        state: present
        register: authData

    - name: Call ome_user_info module
      dellemc.openmanage.ome_user_info:
        hostname: 198.162.0.1
        ca_path: "/path/to/ca_cert.pem"
        x_auth_token: "{{ authData.x_auth_token }}"

    - name: Call ome_network_vlan_info module
      dellemc.openmanage.ome_network_vlan_info:
        hostname: 198.162.0.1
        ca_path: "/path/to/ca_cert.pem"
        x_auth_token: "{{ authData.x_auth_token }}"
  always:
    - name: Destroy a session
      dellemc.openmanage.ome_session:
        hostname: 198.162.0.1
        ca_path: "/path/to/ca_cert.pem"
        state: absent
        x_auth_token: "{{ authData.x_auth_token }}"
        session_id: "{{ authData.session_data.Id }}"
"""

RETURN = r'''
---
msg:
    description: Status of the session operation.
    returned: always
    type: str
    sample: "The session has been created successfully."
session_data:
    description: The session details.
    returned: For session creation operation
    type: dict
    sample: {
        "Id": "d5c28d8e-1084-4055-9c01-e1051cfee2dd",
        "Description": "admin",
        "Name": "API",
        "UserName": "admin",
        "UserId": 10078,
        "Password": null,
        "Roles": [
            "BACKUP_ADMINISTRATOR"
        ],
        "IpAddress": "100.198.162.0",
        "StartTimeStamp": "2023-07-03 07:22:43.683",
        "LastAccessedTimeStamp": "2023-07-03 07:22:43.683",
        "DirectoryGroup": []
            }
x_auth_token:
    description: Authentication token.
    returned: For session creation operation
    type: str
    sample: "d15f17f01cd627c30173b1582642497d"
error_info:
    description: Details of the HTTP Error.
    returned: On HTTP error
    type: dict
    sample: {
        "error": {
            "@Message.ExtendedInfo": [
                {
                    "Message": "Unable to complete the operation because an invalid username and/or password is entered, and therefore authentication failed.",
                    "MessageArgs": [],
                    "MessageArgs@odata.count": 0,
                    "MessageId": "IDRAC.2.7.SYS415",
                    "RelatedProperties": [],
                    "RelatedProperties@odata.count": 0,
                    "Resolution": "Enter valid user name and password and retry the operation.",
                    "Severity": "Warning"
                }
            ],
            "code": "Base.1.12.GeneralError",
            "message": "A general error has occurred. See ExtendedInfo for more information"
        }
    }
'''


import json
from urllib.error import HTTPError, URLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.session_utils import Session
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.common.parameters import env_fallback
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import remove_key

SESSION_URL = "/api/SessionService/Sessions"
ODATA = "@odata.id"
ODATA_REGEX = "(.*?)@odata"

CREATE_SUCCESS_MSG = "The session has been created successfully."
DELETE_SUCCESS_MSG = "The session has been deleted successfully."
FAILURE_MSG = "Unable to '{operation}' a session."
CHANGES_FOUND_MSG = "Changes found to be applied."
NO_CHANGES_FOUND_MSG = "No changes found to be applied."


class OMESession(Session):
    def __init__(self, module):
        super().__init__(module)
        self.url_kwrags = {"force_basic_auth": True,
                           "url_username": self.module.params.get("username"),
                           "url_password": self.module.params.get("password")}

    def get_session_status(self, session_url, session_id):
        """
        Retrieves the status of a session given its URL and ID.

        Args:
            session_url (str): The URL of the session.
            session_id (str): The ID of the session.

        Returns:
            int: The status code of the session status response. If an HTTPError occurs, the status
            code of the error is returned.
        """
        session_status_response = self.instance.invoke_request(SESSION_URL, "GET")
        sessions_data = session_status_response.json_data
        session_ids = [session_id["@odata.id"].split("'")[1] for session_id in sessions_data["value"]]
        session_status = session_id in session_ids
        return session_status

    def create_session(self):
        """
        Executes the session creation process.

        This function creates a session by sending a POST request to the session URL with the
        provided username and password.
        If the request is successful (status code 201), it retrieves the session details, removes
        any OData keys from the response,
        and extracts the X-Auth-Token from the response headers. It then exits the module with a
        success message, indicating that
        the session was created successfully, and provides the session data and X-Auth-Token as
        output variables.

        If the request fails (status code other than 201), it exits the module with a failure
        message, indicating that the session creation failed.

        Parameters:
            None

        Returns:
            None
        """
        payload = {"UserName": self.module.params.get("username"),
                   "Password": self.module.params.get("password")}
        if self.module.check_mode:
            self.module.exit_json(msg=CHANGES_FOUND_MSG, changed=True)
        session_response = self.instance.invoke_request(SESSION_URL, "POST", data=payload, url_kwargs=self.url_kwrags)
        status = session_response.status_code
        if status == 201:
            session_details = session_response.json_data
            session_data = remove_key(session_details, regex_pattern=ODATA_REGEX)
            x_auth_token = session_response.headers.get('X-Auth-Token')
            self.module.exit_json(msg=CREATE_SUCCESS_MSG,
                                  changed=True,
                                  session_data=session_data,
                                  x_auth_token=x_auth_token)
        else:
            self.module.exit_json(msg=FAILURE_MSG.format(operation="create"), failed=True)

    def delete_session(self):
        """
        Executes the deletion of a session.
        This function retrieves the session ID from the module parameters.It then invokes a
        DELETE request to the session URL with the session ID appended. The response from
        the request is stored in the `session_response` variable.

        If the response status code is 200, indicating a successful deletion, the function exits
        the module with a success message and sets the `changed` parameter to True. Otherwise, it
        exits the module with a failure message and sets the `failed` parameter to True.

        Parameters:
            None

        Returns:
            None
        """
        session_id = self.module.params.get("session_id")
        session_status = self.get_session_status(SESSION_URL, session_id)
        if self.module.check_mode:
            if session_status:
                self.module.exit_json(msg=CHANGES_FOUND_MSG, changed=True)
            else:
                self.module.exit_json(msg=NO_CHANGES_FOUND_MSG)
        else:
            if session_status:
                try:
                    delete_session_url = SESSION_URL + "('" + session_id + "')"
                    session_response = self.instance.invoke_request(delete_session_url, "DELETE")
                    status = session_response.status_code
                    if status == 204:
                        self.module.exit_json(msg=DELETE_SUCCESS_MSG, changed=True)
                except HTTPError as err:
                    filter_err = remove_key(json.load(err), regex_pattern=ODATA_REGEX)
                    self.module.exit_json(msg=FAILURE_MSG.format(operation="delete"),
                                          error_info=filter_err,
                                          failed=True)
            else:
                self.module.exit_json(msg=NO_CHANGES_FOUND_MSG)


def main():
    """
    Main function that initializes the Ansible module with the argument specs and required if
    conditions.
    It then creates a SessionAPI object with the module parameters and performs a session operation
    based on the state parameter.
    If the state is "present", it creates a CreateSession object and executes it. If the state is
    "absent", it creates a DeleteSession object and executes it.
    The session status is returned.

    Raises:
        HTTPError: If an HTTP error occurs, the error message and filtered error information are
        returned in the module's exit_json.
        URLError: If a URL error occurs, the error message is returned in the module's exit_json.
        SSLValidationError, ConnectionError, TypeError, ValueError, OSError: If any other error
        occurs, the error message is returned in the module's exit_json.

    Returns:
        None
    """
    specs = get_argument_spec()
    module = AnsibleModule(
        argument_spec=specs,
        required_if=[
            ["state", "present", ("username", "password",)],
            ["state", "absent", ("x_auth_token", "session_id",)]
        ],
        supports_check_mode=True
    )
    try:
        ome = OMESession(module)
        session_operation = module.params.get("state")
        if session_operation == "present":
            ome.create_session()
        else:
            ome.delete_session()
    except HTTPError as err:
        filter_err = {}
        if isinstance(err, dict):
            filter_err = remove_key(json.load(err), regex_pattern=ODATA_REGEX)
        module.exit_json(msg=str(err), error_info=filter_err, failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


def get_argument_spec():
    """
    Returns a dictionary representing the argument specification for a module.

    The dictionary contains the following keys and their corresponding values:
    - "hostname": A string representing the hostname.
    - "username": A string representing the username. It has a fallback option to retrieve the
    value from the environment variable 'IDRAC_USERNAME'.
    - "password": A string representing the password. It is marked as not to be logged and has a
    fallback option to retrieve the value from the environment variable 'IDRAC_PASSWORD'.
    - "port": An integer representing the port number. The default value is 443.
    - "validate_certs": A boolean representing whether to validate certificates. The default value
    is True.
    - "ca_path": A path representing the certificate authority path. The default value is None.
    - "timeout": An integer representing the timeout value. The default value is 30.
    - "state": A string representing the state. The default value is "present". The choices are
    ["present", "absent"].
    - "x_auth_token": A string representing the authentication token. It is marked as not to be
    logged.
    - "session_id": A string representing the session ID.

    Returns:
        A dictionary representing the argument specification.
    """
    return {
        "hostname": {"type": "str"},
        "username": {"type": "str", "fallback": (env_fallback, ['OME_USERNAME'])},
        "password": {"type": "str", "no_log": True, "fallback": (env_fallback, ['OME_PASSWORD'])},
        "port": {"type": "int", "default": 443},
        "validate_certs": {"type": "bool", "default": True},
        "ca_path": {"type": "path", "default": None},
        "timeout": {"type": "int", "default": 30},
        "state": {"type": 'str', "default": "present", "choices": ["present", "absent"]},
        "x_auth_token": {"type": "str", "no_log": True, "aliases": ['auth_token']},
        "session_id": {"type": "str"}
    }


if __name__ == '__main__':
    main()
