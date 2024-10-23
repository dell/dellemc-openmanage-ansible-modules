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
short_description: Create, modify, or delete OMEVV firmware repository profile
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
import time
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv import RestOMEVV, OMEVVAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv_utils.omevv_firmware_utils import OMEVVFirmwareProfile
from ansible.module_utils.common.dict_transformations import recursive_diff

ODATA_REGEX = "(.*?)@odata"
ODATA = "@odata.id"
XML_EXT = ".xml"
GZ_EXT = ".gz"
MESSAGE_EXTENDED_INFO = "@Message.ExtendedInfo"
SUCCESS_CREATION_MSG = "Successfully created the OMEVV firmware repository profile."
FAILED_CREATION_MSG = "Unable to create the OMEVV firmware repository profile."
SUCCESS_MODIFY_MSG = "Successfully modified the OMEVV firmware repository profile."
FAILED_MODIFY_MSG = "Unable to modify the OMEVV firmware repository profile"
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

    def get_payload_details(self):
        payload = {}
        payload["profileName"] = self.module.params.get('name')
        payload["protocolType"] = self.module.params.get('protocol_type')
        payload["sharePath"] = self.module.params.get('catalog_path')
        if self.module.params.get('description') is not None:
            payload["description"] = self.module.params.get('description')
        payload["profileType"] = "Firmware"
        payload["shareCredential"] = {
            "username": self.module.params.get('share_username'),
            "password": self.module.params.get('share_password'),
            "domain": self.module.params.get('share_domain')
        }
        return payload

    def test_connection(self, protocol_type, catalog_path):
        resp = self.omevv_profile_obj.test_connection(
            protocol_type=self.module.params.get('protocol_type') if protocol_type is None else protocol_type,
            catalog_path=self.module.params.get('catalog_path') if catalog_path is None else catalog_path,
            share_username=self.module.params.get('share_username'),
            share_password=self.module.params.get('share_password'),
            share_domain=self.module.params.get('share_domain')
        )
        if resp.success:
            return True
        else:
            self.module.exit_json(msg=FAILED_CONN_MSG, failed=True)

    def trim_api_response(self, api_response):
        trimmed_resp = {}
        if api_response["description"] is not None:
            trimmed_resp["description"] = api_response["description"]
        if api_response["protocolType"] == "CIFS" and not (api_response["sharePath"].endswith(XML_EXT) or api_response["sharePath"].endswith(GZ_EXT)):
            api_response["sharePath"] = api_response["sharePath"] + '\\' + api_response["fileName"]
        if not (api_response["sharePath"].endswith(XML_EXT) or api_response["sharePath"].endswith(GZ_EXT)):
            api_response["sharePath"] = api_response["sharePath"] + '/' + api_response["fileName"]
        trimmed_resp["profileName"] = api_response["profileName"]
        trimmed_resp["sharePath"] = api_response["sharePath"]
        return trimmed_resp

    def execute(self):
        # To be overridden by the subclasses
        pass


class CreateFirmwareRepositoryProfile(FirmwareRepositoryProfile):

    def __init__(self, module, rest_obj):
        self.module = module
        self.obj = rest_obj
        super().__init__(module, rest_obj)

    def diff_mode_check(self, payload):
        diff = {}
        if "shareCredential" in payload:
            payload.pop("shareCredential")
        diff = dict(
            before={},
            after=payload
        )
        return diff

    def create_firmware_repository_profile(self):
        diff = {}
        payload = self.get_payload_details()
        res = FirmwareRepositoryProfile.test_connection(self, None, None)
        if res:
            diff = self.diff_mode_check(payload)
            resp, _err_msg = self.omevv_profile_obj.create_firmware_repository_profile(
                name=self.module.params.get('name'),
                catalog_path=self.module.params.get('catalog_path'),
                description=self.module.params.get('description'),
                protocol_type=self.module.params.get('protocol_type'),
                share_username=self.module.params.get('share_username'),
                share_password=self.module.params.get('share_password'),
                share_domain=self.module.params.get('share_domain')
            )
            if resp.success:
                profile_resp = self.omevv_profile_obj.get_firmware_repository_profile_by_id(resp.json_data)
                while profile_resp.json_data["status"] != "Success" and profile_resp.json_data["status"] != "Failed":
                    time.sleep(3)
                    profile_resp = self.omevv_profile_obj.get_firmware_repository_profile(resp.json_data["profileName"])
                if self.module._diff and profile_resp.json_data["status"] == "Success":
                    self.module.exit_json(msg=SUCCESS_CREATION_MSG, profile_info=profile_resp.json_data, diff=diff, changed=True)
                elif profile_resp.json_data["status"] == "Success":
                    self.module.exit_json(msg=SUCCESS_CREATION_MSG, profile_info=profile_resp.json_data, changed=True)
                else:
                    self.module.exit_json(msg=FAILED_CREATION_MSG, profile_info=profile_resp.json_data, failed=True)
            else:
                self.module.exit_json(msg=FAILED_CREATION_MSG, failed=True)

    def execute(self):
        modified_payload = {}
        payload = self.get_payload_details()
        result = self.omevv_profile_obj.get_firmware_repository_profile()
        profile = self.module.params.get('name')
        profile_exists = self.omevv_profile_obj.search_profile_name(result, profile)
        modified_payload.update(payload)
        del modified_payload["protocolType"]
        del modified_payload["profileType"]
        del modified_payload["shareCredential"]
        if profile_exists:
            trimmed_resp = FirmwareRepositoryProfile.trim_api_response(self, profile_exists)
            diff = recursive_diff(modified_payload, trimmed_resp)
            new_profile = diff and (diff[0] != diff[1])
        if not profile_exists and self.module.check_mode and self.module._diff:
            FirmwareRepositoryProfile.test_connection(self, None, None)
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
        if api_response["protocolType"] == "CIFS" and not (api_response["sharePath"].endswith(XML_EXT) or api_response["sharePath"].endswith(GZ_EXT)):
            api_response["sharePath"] = api_response["sharePath"] + '\\' + api_response["fileName"]
        if not (api_response["sharePath"].endswith(XML_EXT) or api_response["sharePath"].endswith(GZ_EXT)):
            api_response["sharePath"] = api_response["sharePath"] + '/' + api_response["fileName"]
        if module_response["sharePath"] is None:
            module_response["sharePath"] = api_response["sharePath"]
        for key in module_response.keys():
            if key not in api_response or api_response[key] != module_response[key]:
                diff[key] = module_response[key]
        return diff

    def trim_api_response(self, api_response, payload=None):
        trimmed_resp = {}
        trimmed_resp["profileName"] = api_response["profileName"]
        trimmed_resp["sharePath"] = api_response["sharePath"]
        if payload.get("description") is not None:
            trimmed_resp["description"] = api_response["description"]
        return trimmed_resp

    def rec_diff(self, api_response, payload):
        diff = {}
        trim = self.trim_api_response(api_response, payload)
        if payload.get("shareCredential") is not None:
            del payload["shareCredential"]
        output = recursive_diff(trim, payload)
        if self.module._diff:
            diff = dict(
                before=output[0],
                after=output[1]
            )
        return diff

    def modify_firmware_repository_profile(self, api_response, module_response):
        protocol_type = api_response["protocolType"]
        catalog_path = api_response["sharePath"]
        res = FirmwareRepositoryProfile.test_connection(self, protocol_type, catalog_path)
        name = self.module.params.get('new_name') if self.module.params.get('new_name') is not None else self.module.params.get('name')
        if res:
            diff = self.rec_diff(api_response, module_response)
            resp, _err_msg = self.omevv_profile_obj.modify_firmware_repository_profile(
                api_response["id"],
                name=name,
                catalog_path=self.module.params.get('catalog_path') if self.module.params.get('catalog_path') is not None else api_response["sharePath"],
                description=self.module.params.get('description') if self.module.params.get('description') is not None else api_response["description"],
                share_username=self.module.params.get('share_username'),
                share_password=self.module.params.get('share_password'),
                share_domain=self.module.params.get('share_domain')
            )
            if resp.success:
                self.output_modify_response(api_response, diff)
            else:
                self.module.exit_json(msg=FAILED_MODIFY_MSG, failed=True)

    def output_modify_response(self, api_response, diff):
        profile_resp = self.omevv_profile_obj.get_firmware_repository_profile_by_id(api_response["id"])
        while profile_resp.json_data["status"] != "Success" and profile_resp.json_data["status"] != "Failed":
            time.sleep(3)
            profile_resp = self.omevv_profile_obj.get_firmware_repository_profile_by_id(api_response["id"])
        if self.module._diff and profile_resp.json_data["status"] == "Success":
            self.module.exit_json(msg=SUCCESS_MODIFY_MSG, profile_info=profile_resp.json_data, diff=diff, changed=True)
        elif profile_resp.json_data["status"] == "Success":
            self.module.exit_json(msg=SUCCESS_MODIFY_MSG, profile_info=profile_resp.json_data, changed=True)
        else:
            self.module.exit_json(msg=FAILED_MODIFY_MSG, profile_info=profile_resp.json_data, failed=True)

    def execute(self):
        module_response = {}
        payload = self.get_payload_details()
        del payload["profileType"]
        del payload["protocolType"]
        result = self.omevv_profile_obj.get_firmware_repository_profile()
        profile = self.module.params.get('name')
        api_response = self.omevv_profile_obj.search_profile_name(result, profile)
        module_response.update(payload)
        new_name = self.module.params.get('new_name')
        profile_name = self.module.params.get('name')
        module_response["profileName"] = (
            new_name if new_name is not None else profile_name
        )
        del module_response["shareCredential"]
        diff = self.diff_check(api_response, module_response)
        if diff and self.module.check_mode and self.module._diff:
            diff = self.rec_diff(api_response, module_response)
            self.module.exit_json(msg=CHANGES_FOUND_MSG, diff=diff, changed=True)
        if diff and self.module.check_mode:
            self.module.exit_json(msg=CHANGES_FOUND_MSG, changed=True)
        if diff and not self.module.check_mode:
            self.modify_firmware_repository_profile(api_response, module_response)
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
        result = self.omevv_profile_obj.get_firmware_repository_profile()
        profile = self.module.params.get('name')
        api_response = self.omevv_profile_obj.search_profile_name(result, profile)
        profile_exists = self.omevv_profile_obj.search_profile_name(result, profile)
        if profile_exists and self.module.check_mode and self.module._diff:
            diff = self.diff_mode_check(api_response)
            self.module.exit_json(msg=CHANGES_FOUND_MSG, diff=diff, changed=True)
        if not profile_exists and self.module.check_mode:
            self.module.exit_json(msg=CHANGES_NOT_FOUND_MSG, changed=False)
        if not profile_exists and not self.module.check_mode and self.module._diff:
            self.module.exit_json(msg=PROFILE_NOT_FOUND_MSG.format(profile_name=profile), diff={"before": {}, "after": {}}, profile_info={}, failed=True)
        if not profile_exists and not self.module.check_mode:
            self.module.exit_json(msg=PROFILE_NOT_FOUND_MSG.format(profile_name=profile), profile_info={}, failed=True)
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
