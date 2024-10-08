#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.8.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: omevv_firmware_repository_profile
short_description: Create, modify and delete firmware repository profile
version_added: "9.8.0"
description:
  - This module allows to create, modify and delete firmware repository profile.
extends_documentation_fragment:
  - dellemc.openmanage.omevv_auth_options
options:
  state:
    description:
      - C(present) creates a new OMEVV firmware repository profile or modifies an existing profile if the profile with the same name already exists.
      - C(absent) deletes the OMEVV firmware repository profile.
      - Either I(profile_name) or I(profile_id) is required when I(state) is C(absent).
    type: str
    choices: [present, absent]
    default: present
  name:
    description:
      - Name of the profile.
      - This is required for modification operation and when I(state) is C(absent).
    type: str
  description:
    description:
      - Description of OMEVV firmware repository profile..
    type: str
  new_name:
    description: New profile name when modify operation is performed.
    type: str
  protocol_type:
    description:
      - C(NFS) represents NFS share path.
      - C(CIFS) represents NFS share path.
      - C(HTTP) represents HTTP share path.
      - C(HTTPS) represents HTTPS share path.
      - This is required when I(state) is C(present) and when creating a new profile.
    type: str
    choices: [NFS, CIFS, HTTP, HTTPS]
  catalog_path:
    description:
      - Absolute path of the catalog.
      - HTTP, HTTPS, NFS, and CIFS paths are supported.
      - This parameter is required when I(state) is C(present).
    type: str
  share_username:
    description:
      - Username of the share.
      - This is required when I(catalog_path) is HTTPS or CIFS.
    type: str
  share_password:
    description:
      - Password of the share.
      - This is required when I(catalog_path) is HTTPS or CIFS.
    type: str
  share_domain:
    description: Domain of the share.
    type: str
requirements:
  - "python >= 3.9.6"
author:
  - "Shivam Sharma(@ShivamSh3)"
attributes:
    check_mode:
        description: Runs task to validate without performing action on the target machine.
        support: full
    diff_mode:
        description: Runs the task to report the changes made or to be made.
        support: full
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
    - This module supports IPv4 and IPv6 addresses.
"""

EXAMPLES = r"""
---
- name: Create a firmware repository profile
  dellemc.openmanage.omevv_firmware_repository_profile:
    hostname: "192.168.0.1"
    vcenter_uuid: "xxxxx"
    vcenter_username: "username"
    vcenter_password: "password"
    ca_path: "path/to/ca_file"
    state: present
    name: profile-1
    catalog_path: http://xx.xx.xx.xx/share/Catalog/Catalog.xml

- name: Modify a firmware repository profile
  dellemc.openmanage.omevv_firmware_repository_profile:
    hostname: "192.168.0.1"
    vcenter_uuid: "xxxxx"
    vcenter_username: "username"
    vcenter_password: "password"
    ca_path: "path/to/ca_file"
    state: present
    name: profile-1
    new_name: profile-2
    catalog_path: http://xx.xx.xx.xx/new_share/Catalog/Catalog.xml

- name: Delete a firmware repository profile
  dellemc.openmanage.omevv_firmware_repository_profile:
    hostname: "192.168.0.1"
    vcenter_uuid: "xxxxx"
    vcenter_username: "username"
    vcenter_password: "password"
    ca_path: "path/to/ca_file"
    state: absent
    name: profile-1
"""

RETURN = r'''
---
msg:
  type: str
  description: Status of the profile operation.
  returned: always
  sample: "Successfully created the OMEVV firmware repository profile."
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample:
    {
      "errorCode": "18001",
      "message": "Repository profile with name Test already exists."
    }
'''
import json
from ssl import SSLError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv import RestOMEVV, OMEVVAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import remove_key

ODATA_REGEX = "(.*?)@odata"
ODATA = "@odata.id"
XML_EXT = ".xml"
GZ_EXT = ".gz"
XML_GZ_EXT = ".xml.gz"
MESSAGE_EXTENDED_INFO = "@Message.ExtendedInfo"
TEST_CONNECTION_URI = "/RepositoryProfiles/TestConnection"
PROFILE_URI = "/RepositoryProfiles"
SUCCESS_CREATION_MSG = "Successfully created the OMEVV firmware repository profile."
SAME_PROFILE_MSG = "Firmware repository profile with name {profile_name} already exists."
FAILED_CREATION_MSG = "Unable to create the OMEVV firmware repository profile."
SUCCESS_MODIFY_MSG = "Successfully modified the OMEVV firmware repository profile."
FAILED_MODIFY_MSG = "Unable to modify the OMEVV firmware repository profile as the details are same."
FAILED_CONN_MSG = "Unable to complete the operation. Please check the connection details."
CHANGES_FOUND_MSG = "Changes found to be applied."
CHANGES_NOT_FOUND_MSG = "No changes found to be applied."


class FirmwareRepositoryProfile:

    def __init__(self, module, rest_obj):
        self.module = module
        self.obj = rest_obj

    def get_payload_details(self):
        payload = {}
        payload["profileName"] = self.module.params.get('name')
        payload["protocolType"] = self.module.params.get('protocol_type').upper()
        payload["sharePath"] = self.module.params.get('catalog_path')
        payload["description"] = self.module.params.get('description')
        payload["profileType"] = "Firmware"
        payload["shareCredential"] = {
            "username": self.module.params.get('share_username'),
            "password": self.module.params.get('share_password'),
            "domain": self.module.params.get('share_dommain')
        }
        return payload

    def form_conn_payload(self):
        payload = self.get_payload_details()
        del payload["profileName"]
        del payload["sharePath"]
        payload["catalogPath"] = self.module.params.get('catalog_path')
        del payload["description"]
        del payload["profileType"]
        payload["checkCertificate"] = False
        return payload

    def get_modify_payload_details(self):
        payload = {}
        payload["profileName"] = self.module.params.get('new_name')
        payload["sharePath"] = self.module.params.get('catalog_path')
        payload["description"] = self.module.params.get('description')
        payload["shareCredential"] = {
            "username": self.module.params.get('share_username'),
            "password": self.module.params.get('share_password'),
            "domain": self.module.params.get('share_dommain')
        }
        return payload

    def test_connection(self):
        payload = self.form_conn_payload()
        resp = self.obj.invoke_request("POST", TEST_CONNECTION_URI, payload)
        if resp.success:
            return True
        else:
            self.module.exit_json(msg=FAILED_CONN_MSG, failed=True)

    def get_firmware_repository_profile(self):
        res = FirmwareRepositoryProfile.execute(self)
        if res:
            resp = self.obj.invoke_request("GET", PROFILE_URI)
            data = resp.json_data
        return data

    def search_profile_name(self, data, profile_name):
        for d in data:
            if d.get('profileName') == profile_name:
                return d
        return {}

    def validate_catalog_path(self, protocol_type, catalog_path):
        protocol_mapping = {
            'CIFS': (lambda path: path.endswith(XML_EXT) or path.endswith(GZ_EXT) or path.endswith(XML_GZ_EXT)),
            'NFS': (lambda path: path.endswith(XML_EXT) or path.endswith(GZ_EXT) or path.endswith(XML_GZ_EXT)),
            'HTTP': (lambda path: path.startswith('http://') and (path.endswith(XML_EXT) or path.endswith(GZ_EXT) or path.endswith(XML_GZ_EXT))),
            "HTTPS": (lambda path: path.startswith('https://') and (path.endswith(XML_EXT) or path.endswith(GZ_EXT) or path.endswith(XML_GZ_EXT)))
        }
        validator = protocol_mapping.get(protocol_type)
        if validator is None:
            self.module.exit_json(msg="Invalid catalog_path", failed=True)
        if not validator(catalog_path):
            self.module.exit_json(msg="Invalid catalog_path", failed=True)

    def execute(self):
        self.validate_catalog_path(self.module.params.get('protocol_type'), self.module.params.get('catalog_path'))
        result = self.test_connection()
        return result


class CreateFirmwareRepositoryProfile(FirmwareRepositoryProfile):

    def __init__(self, module, rest_obj):
        self.module = module
        self.obj = rest_obj

    def create_firmware_repository_profile(self):
        diff = {}
        payload = self.get_payload_details()
        res = FirmwareRepositoryProfile.execute(self)
        if res:
            if self.module._diff:
                diff = dict(
                    before={},
                    after=payload
                )
                self.module.exit_json(changed=True, diff=diff)
            resp = self.obj.invoke_request("POST", PROFILE_URI, payload)
            if resp.success:
                self.module.exit_json(msg=SUCCESS_CREATION_MSG, changed=True)
            else:
                self.module.exit_json(msg=FAILED_CREATION_MSG, failed=True)

    def execute(self):
        result = self.get_firmware_repository_profile()
        profile = self.module.params.get('name')
        new_profile = self.module.params.get('new_name')
        profile_exists = self.search_profile_name(result, profile)
        if not profile_exists and self.module.check_mode:
            self.module.exit_json(msg=CHANGES_FOUND_MSG, changed=True)
        if not profile_exists and not self.module.check_mode:
            result = self.create_firmware_repository_profile()
            return result
        if profile_exists and self.module.check_mode and not new_profile:
            self.module.exit_json(msg=CHANGES_NOT_FOUND_MSG, changed=False)
        if profile_exists and new_profile:
            omevv_obj = ModifyFirmwareRepositoryProfile(self.module, self.obj)
            omevv_obj.execute()
        else:
            self.module.exit_json(msg=SAME_PROFILE_MSG.format(profile_name=profile), skipped=True)


class ModifyFirmwareRepositoryProfile(FirmwareRepositoryProfile):

    def __init__(self, module, rest_obj):
        self.module = module
        self.obj = rest_obj

    def diff_check(self, api_response, module_response):
        diff = {}
        del module_response["protocolType"]
        del module_response["shareCredential"]
        for key in module_response.keys():
            if key not in api_response or api_response[key] != module_response[key]:
                diff[key] = module_response[key]
        return diff

    def trim_api_response(self, api_response):
        trimmed_resp = {}
        trimmed_resp["profileName"] = api_response["profileName"]
        trimmed_resp["sharePath"] = api_response["sharePath"]
        trimmed_resp["description"] = api_response["description"]
        return trimmed_resp

    def modify_firmware_repository_profile(self, api_response):
        diff = {}
        MODIFY_PROFILE_URI = PROFILE_URI + "/" + str(api_response["id"])
        payload = self.get_modify_payload_details()
        res = FirmwareRepositoryProfile.execute(self)
        if res:
            if self.module._diff:
                del payload["shareCredential"]
                diff = dict(
                    before=self.trim_api_response(api_response),
                    after=payload
                )
                self.module.exit_json(changed=True, diff=diff)
            resp = self.obj.invoke_request("PUT", MODIFY_PROFILE_URI, payload)
            if resp.success:
                self.module.exit_json(msg=SUCCESS_MODIFY_MSG, changed=True)
            else:
                self.module.exit_json(msg=FAILED_MODIFY_MSG, failed=True)

    def execute(self):
        result = self.get_firmware_repository_profile()
        profile = self.module.params.get('name')
        api_response = self.search_profile_name(result, profile)
        module_response = self.get_payload_details()
        diff = self.diff_check(api_response, module_response)
        if diff and self.module.check_mode:
            self.module.exit_json(msg=CHANGES_FOUND_MSG, changed=True)
        if diff and not self.module.check_mode:
            result = self.modify_firmware_repository_profile(api_response)
            return result
        if not diff and self.module.check_mode:
            self.module.exit_json(msg=CHANGES_NOT_FOUND_MSG, changed=False)
        else:
            self.module.exit_json(msg=SAME_PROFILE_MSG.format(profile_name=profile), skipped=True)


def main():
    argument_spec = {
        "state": {"type": 'str', "choices": ['present', 'absent'], "default": 'present'},
        "share_username": {"type": 'str'},
        "share_password": {"type": 'str', "no_log": True},
        "name": {"type": 'str'},
        "new_name": {"type": 'str'},
        "catalog_path": {"type": 'str'},
        "description": {"type": 'str'},
        "protocol_type": {"type": 'str', "choices": ['NFS', 'CIFS', 'HTTP', 'HTTPS']},
        "share_domain": {"type": 'str'}
    }
    module = OMEVVAnsibleModule(
        argument_spec=argument_spec,
        required_if=[
            ["state", 'present', ("name", "catalog_path", "description", "protocol_type")],
            ["protocol_type", "NFS", ("catalog_path", "share_domain")],
            ["protocol_type", "CIFS", ("catalog_path", "share_username", "share_password", "share_domain")],
            ["protocol_type", "HTTP", ("catalog_path", "share_domain")],
            ["protocol_type", "HTTPS", ("catalog_path", "share_username", "share_password", "share_domain")],
            ["state", 'absent', ("name",)]
        ],
        supports_check_mode=True)
    try:
        with RestOMEVV(module.params) as rest_obj:
            omevv_obj = CreateFirmwareRepositoryProfile(module, rest_obj)
            omevv_obj.execute()
    except HTTPError as err:
        filter_err = remove_key(json.load(err), regex_pattern=ODATA_REGEX)
        code = filter_err.get('errorCode')
        message = filter_err.get('message')
        if '18001' in code:
            module.exit_json(msg=message, skipped=True)
        if '500' in code:
            module.exit_json(msg=message, skipped=True)
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError,
            AttributeError, IndexError, KeyError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
