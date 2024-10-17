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
short_description: Create, modify, and delete OMEVV firmware repository profile
version_added: "9.8.0"
description: This module allows you to create, modify, or delete an OpenManage Enterprise Integration for VMware Center (OMEVV) firmware repository profile.
extends_documentation_fragment:
  - dellemc.openmanage.omevv_auth_options
options:
  state:
    description:
      - C(present) creates an OMEVV firmware repository profile or modifies an existing profile if the profile with the same name exists.
      - C(absent) deletes the OMEVV firmware repository profile.
      - Either I(profile_name) or I(profile_id) is required when I(state) is C(absent).
    type: str
    choices: [present, absent]
    default: present
  name:
    description:
      - Name of the OMEVV firmware repository profile.
      - This parameter is required for modification operation when I(state) is C(absent).
    type: str
  description:
    description:
      - Description of OMEVV firmware repository profile.
    type: str
  new_name:
    description: Name of the new OMEVV profile name when modify operation is performed.
    type: str
  protocol_type:
    description:
      - C(NFS) represents the NFS share path.
      - C(CIFS) represents the NFS share path.
      - C(HTTP) represents the HTTP share path.
      - C(HTTPS) represents the HTTPS share path.
      - This parameter is required when I(state) is C(present) and a new profile is created.
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
      - This parameter is required when I(catalog_path) is HTTPS or CIFS.
    type: str
  share_password:
    description:
      - Password of the share.
      - This parameter is required when I(catalog_path) is HTTPS or CIFS.
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
        description: Runs the task to report the changes that are made or the changes that must be applied.
        support: full
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
"""

EXAMPLES = r"""
---
- name: Create an OMEVV firmware repository profile
  dellemc.openmanage.omevv_firmware_repository_profile:
    hostname: "192.168.0.1"
    vcenter_uuid: "xxxxx"
    vcenter_username: "username"
    vcenter_password: "password"
    ca_path: "path/to/ca_file"
    state: present
    name: profile-1
    catalog_path: http://xx.xx.xx.xx/share/Catalog/Catalog.xml

- name: Modify an OMEVV firmware repository profile
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

- name: Delete an OMEVV firmware repository profile
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
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv import RestOMEVV, OMEVVAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv_firmware_utils import OMEVVFirmwareProfile

ODATA_REGEX = "(.*?)@odata"
ODATA = "@odata.id"
MESSAGE_EXTENDED_INFO = "@Message.ExtendedInfo"
TEST_CONNECTION_URI = "/RepositoryProfiles/TestConnection"
PROFILE_URI = "/RepositoryProfiles"
SUCCESS_CREATION_MSG = "Successfully created the OMEVV firmware repository profile."
FAILED_CREATION_MSG = "Unable to create the OMEVV firmware repository profile."
SUCCESS_MODIFY_MSG = "Successfully modified the OMEVV firmware repository profile."
FAILED_MODIFY_MSG = "Unable to modify the OMEVV firmware repository profile as the details are same."
SUCCESS_DELETION_MSG = "Successfully deleted the OMEVV firmware repository profile."
FAILED_DELETION_MSG = "Unable to delete the OMEVV firmware repository profile."
PROFILE_NOT_FOUND_MSG = "Unable to delete the profile {profile_name} because the profile name is invalid. Enter a valid profile name and retry the operation."
FAILED_CONN_MSG = "Unable to complete the operation. Please check the connection details."
CHANGES_FOUND_MSG = "Changes found to be applied."
CHANGES_NOT_FOUND_MSG = "No changes found to be applied."


class FirmwareRepositoryProfile:

    def __init__(self, module, rest_obj):
        self.module = module
        self.obj = rest_obj
        self.omevv_profile_obj = OMEVVFirmwareProfile(self.obj)

    def module_params(self):
        module_params = {}
        params_list = ['name', 'new_name', 'catalog_path', 'description', 'protocol_type', 'share_username', 'share_password', 'share_domain']
        for param in params_list:
            value = self.module.params.get(param)
            module_params[param] = value if value is not None else ""
        return module_params

    def test_connection(self):
        module_params = self.module_params()
        payload = self.omevv_profile_obj.form_conn_payload(**module_params)
        resp = self.omevv_profile_obj.test_connection(payload)
        if resp.success:
            return True
        else:
            self.module.exit_json(msg=FAILED_CONN_MSG, failed=True)

    def get_firmware_repository_profile(self):
        resp = self.omevv_profile_obj.get_firmware_repository_profile()
        data = resp.json_data
        return data

    def execute(self):
        self.omevv_profile_obj.validate_catalog_path(self.module.params.get('protocol_type'), self.module.params.get('catalog_path'))
        result = self.test_connection()
        return result


class CreateFirmwareRepositoryProfile(FirmwareRepositoryProfile):

    def __init__(self, module, rest_obj):
        self.module = module
        self.obj = rest_obj
        super().__init__(module, rest_obj)

    def diff_mode_check(self, payload):
        diff = {}
        diff = dict(
            before={},
            after=payload
        )
        return diff

    def create_firmware_repository_profile(self):
        diff = {}
        module_params = self.module_params()
        payload = self.omevv_profile_obj.get_payload_details(**module_params)
        res = FirmwareRepositoryProfile.execute(self)
        if res:
            diff = self.diff_mode_check(payload)
            resp = self.omevv_profile_obj.create_firmware_repository_profile(payload)
            if resp.success:
                profile_resp = self.omevv_profile_obj.get_firmware_repository_profile_by_id(resp.json_data)
                if self.module._diff:
                    self.module.exit_json(msg=SUCCESS_CREATION_MSG, profile_info=profile_resp.json_data, diff=diff, changed=True)
                self.module.exit_json(msg=SUCCESS_CREATION_MSG, profile_info=profile_resp.json_data, changed=True)
            else:
                self.module.exit_json(msg=FAILED_CREATION_MSG, failed=True)

    def execute(self):
        module_params = self.module_params()
        payload = self.omevv_profile_obj.get_payload_details(**module_params)
        result = self.get_firmware_repository_profile()
        profile = self.module.params.get('name')
        new_profile = self.module.params.get('new_name')
        profile_exists = self.omevv_profile_obj.search_profile_name(result, profile)
        if not profile_exists and self.module.check_mode and self.module._diff:
            diff = self.diff_mode_check(payload)
            self.module.exit_json(msg=CHANGES_FOUND_MSG, diff=diff, changed=True)
        if not profile_exists and self.module.check_mode:
            self.module.exit_json(msg=CHANGES_FOUND_MSG, changed=True)
        if not profile_exists and not self.module.check_mode:
            self.create_firmware_repository_profile()
        if profile_exists and self.module._diff and not new_profile:
            self.module.exit_json(msg=CHANGES_NOT_FOUND_MSG, changed=False, diff={"before": {}, "after": {}})
        if profile_exists and self.module.check_mode and not new_profile:
            self.module.exit_json(msg=CHANGES_NOT_FOUND_MSG, changed=False)
        if profile_exists and new_profile:
            omevv_obj = ModifyFirmwareRepositoryProfile(self.module, self.obj)
            omevv_obj.execute()
        else:
            self.module.exit_json(msg=CHANGES_NOT_FOUND_MSG, changed=False)


class ModifyFirmwareRepositoryProfile(FirmwareRepositoryProfile):

    def __init__(self, module, rest_obj):
        self.module = module
        self.obj = rest_obj
        super().__init__(module, rest_obj)

    def diff_check(self, api_response, module_response):
        diff = {}
        del module_response["protocolType"]
        del module_response["shareCredential"]
        api_response["sharePath"] = api_response["sharePath"] + '/' + api_response["fileName"]
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

    def diff_mode_check(self, payload, api_response):
        diff = {}
        del payload["shareCredential"]
        payload["profileName"] = self.module.params.get('new_name')
        if self.module._diff:
            diff = dict(
                before=self.diff_check(api_response, payload),
                after=payload
            )
        return diff

    def modify_firmware_repository_profile(self, api_response):
        module_params = self.module_params()
        payload = self.omevv_profile_obj.get_modify_payload_details(**module_params)
        res = FirmwareRepositoryProfile.execute(self)
        if res:
            diff = self.diff_mode_check(payload, self.trim_api_response(api_response))
            resp = self.omevv_profile_obj.modify_firmware_repository_profile(api_response["id"], payload)
            if resp.success:
                profile_resp = self.omevv_profile_obj.get_firmware_repository_profile_by_id(api_response["id"])
                if self.module._diff:
                    self.module.exit_json(msg=SUCCESS_MODIFY_MSG, profile_info=profile_resp.json_data, diff=diff, changed=True)
                self.module.exit_json(msg=SUCCESS_MODIFY_MSG, profile_info=profile_resp.json_data, changed=True)
            else:
                self.module.exit_json(msg=FAILED_MODIFY_MSG, failed=True)

    def execute(self):
        module_params = self.module_params()
        payload = self.omevv_profile_obj.get_modify_payload_details()
        result = self.get_firmware_repository_profile()
        profile = self.module.params.get('name')
        api_response = self.omevv_profile_obj.search_profile_name(result, profile)
        module_response = self.omevv_profile_obj.get_payload_details(**module_params)
        module_response["profileName"] = self.module.params.get('new_name')
        diff = self.diff_check(api_response, module_response)
        if diff and self.module.check_mode and self.module._diff:
            diff = self.diff_mode_check(payload, self.trim_api_response(api_response))
            self.module.exit_json(msg=CHANGES_FOUND_MSG, diff=diff, changed=True)
        if diff and self.module.check_mode:
            self.module.exit_json(msg=CHANGES_FOUND_MSG, changed=True)
        if diff and not self.module.check_mode:
            self.modify_firmware_repository_profile(api_response)
        else:
            self.module.exit_json(msg=CHANGES_NOT_FOUND_MSG, changed=False)


class DeleteFirmwareRepositoryProfile(FirmwareRepositoryProfile):

    def __init__(self, module, rest_obj):
        self.module = module
        self.obj = rest_obj
        super().__init__(module, rest_obj)

    def diff_mode_check(self, payload):
        diff = {}
        diff_dict = {}
        diff_dict["profileName"] = payload["profileName"]
        diff_dict["description"] = payload["description"]
        diff_dict["profileType"] = payload["profileType"]
        diff_dict["sharePath"] = payload["sharePath"]
        diff_dict["protocolType"] = payload["protocolType"]
        if self.module._diff:
            diff = dict(
                before=diff_dict,
                after={}
            )
        return diff

    def delete_firmware_repository_profile(self, api_response):
        diff = {}
        diff = self.diff_mode_check(api_response)
        resp = self.omevv_profile_obj.delete_firmware_repository_profile(api_response["id"])
        if resp.success:
            if self.module._diff:
                self.module.exit_json(msg=SUCCESS_DELETION_MSG, profile_info={}, diff=diff, changed=True)
            self.module.exit_json(msg=SUCCESS_DELETION_MSG, profile_info={}, changed=True)
        else:
            self.module.exit_json(msg=FAILED_DELETION_MSG, failed=True)

    def execute(self):
        result = self.get_firmware_repository_profile()
        profile = self.module.params.get('name')
        api_response = self.omevv_profile_obj.search_profile_name(result, profile)
        profile_exists = self.omevv_profile_obj.search_profile_name(result, profile)
        if profile_exists and self.module.check_mode and self.module._diff:
            diff = self.diff_mode_check(api_response)
            self.module.exit_json(msg=CHANGES_FOUND_MSG, diff=diff, changed=True)
        if not profile_exists and self.module.check_mode:
            self.module.exit_json(msg=CHANGES_NOT_FOUND_MSG, changed=False)
        if not profile_exists and not self.module.check_mode and self.module._diff:
            self.module.exit_json(msg=PROFILE_NOT_FOUND_MSG.format(profile_name=profile), diff={"before": {}, "after": {}}, profile_info={}, changed=False)
        if not profile_exists and not self.module.check_mode:
            self.module.exit_json(msg=PROFILE_NOT_FOUND_MSG.format(profile_name=profile), profile_info={}, changed=False)
        if profile_exists and not self.module.check_mode:
            self.delete_firmware_repository_profile(api_response)
        if profile_exists and self.module.check_mode:
            self.module.exit_json(msg=CHANGES_FOUND_MSG, changed=True)


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
            ["state", 'present', ("name", "catalog_path", "protocol_type")],
            ["protocol_type", "NFS", ("catalog_path",)],
            ["protocol_type", "CIFS", ("catalog_path", "share_username", "share_password")],
            ["protocol_type", "HTTP", ("catalog_path",)],
            ["protocol_type", "HTTPS", ("catalog_path",)],
            ["state", 'absent', ("name",)]
        ],
        supports_check_mode=True)
    try:
        with RestOMEVV(module.params) as rest_obj:
            if module.params.get('state') == 'present':
                omevv_obj = CreateFirmwareRepositoryProfile(module, rest_obj)
            if module.params.get('state') == 'absent':
                omevv_obj = DeleteFirmwareRepositoryProfile(module, rest_obj)
            omevv_obj.execute()
    except HTTPError as err:
        if err.code == 500:
            module.exit_json(msg=json.load(err), failed=True)
        error_info = json.load(err)
        code = error_info.get('errorCode')
        message = error_info.get('message')
        if '18001' in code and module.check_mode:
            module.exit_json(msg=CHANGES_NOT_FOUND_MSG)
        if '500' in code:
            module.exit_json(msg=message, skipped=True)
        module.exit_json(msg=message, error_info=error_info, failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, TypeError, ConnectionError,
            AttributeError, IndexError, KeyError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
