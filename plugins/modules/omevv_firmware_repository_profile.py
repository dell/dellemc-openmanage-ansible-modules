#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.1
# Copyright (C) 2024-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

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
  resync:
    description: Sync the repository profile from the UMP plugin.
    type: bool
    default: false
  username:
    description:
    - OpenManage Enterprise or OpenManage Enterprise Modular username.
    - If I(resync) is true, then I(username) is required.
    type: str
    required: false
  password:
    description:
    - OpenManage Enterprise or OpenManage Enterprise Modular password.
    - If I(resync) is true, then I(password) is required.
    type: str
    required: false
requirements:
  - "python >= 3.9.6"
author:
  - "Shivam Sharma(@ShivamSh3)"
  - "Meenakshi Dembi(@meenakshidembi691)"
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
import re
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv import RestOMEVV, OMEVVAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv_utils.omevv_firmware_utils import OMEVVFirmwareProfile
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.common.dict_transformations import recursive_diff

ODATA_REGEX = "(.*?)@odata"
ODATA = "@odata.id"
XML_EXT = ".xml"
GZ_EXT = ".gz"
PLUGINS_URI = "PluginService/Plugins"
UMP_URI = "UpdateManagementService/Repositories"
MESSAGE_EXTENDED_INFO = "@Message.ExtendedInfo"
SUCCESS_CREATION_MSG = "Successfully created the OMEVV firmware repository profile."
SUCCESS_CREATION_RESYNC_MSG = "Successfully resynced and created the OMEVV firmware repository profile."
FAILED_CREATION_MSG = "Unable to create the OMEVV firmware repository profile."
SUCCESS_MODIFY_MSG = "Successfully modified the OMEVV firmware repository profile."
SUCCESS_MODIFY_RESYNC_MSG = "Successfully resynced and modified the OMEVV firmware repository profile."
FAILED_MODIFY_MSG = "Unable to modify the OMEVV firmware repository profile"
SUCCESS_DELETION_MSG = "Successfully deleted the OMEVV firmware repository profile."
SUCCESS_DELETION_RESYNC_MSG = "Successfully resynced and deleted the OMEVV firmware repository profile."
FAILED_DELETION_MSG = "Unable to delete the OMEVV firmware repository profile."
PROFILE_NOT_FOUND_MSG = "Unable to delete the profile {profile_name} because the profile name is invalid. Enter a valid profile name and retry the operation."
FAILED_CONN_MSG = "Unable to complete the operation. Please check the connection details."
CHANGES_FOUND_MSG = "Changes found to be applied."
CHANGES_NOT_FOUND_MSG = "No changes found to be applied."
UMP_PLUGIN_NOT_FOUND_MSG = "Update Manager Plug-in (UMP) is not installed. Please install the UMP plugin and retry the operation."
SUCCESS_RESYNC_MSG = "Successfully resynced the OMEVV firmware repository profile."
FAILED_RESYNC_MSG = "Unable to resync the OMEVV firmware repository profile."
NO_OPERATION_SKIP_MSG = "The operation is skipped."


class FirmwareRepositoryProfile:
    diff_dict = {
        'before': {},
        'after': {}
    }

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
        if resp:
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
        if "shareCredential" in payload:
            payload.pop("shareCredential")
        self.diff_dict['before'].update({})
        self.diff_dict['after'].update(payload)

    def create_firmware_repository_profile(self):
        payload = self.get_payload_details()
        res = FirmwareRepositoryProfile.test_connection(self, None, None)
        if res:
            self.diff_mode_check(payload)
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
                self.diff_mode_behaviour(resp)
            else:
                self.module.exit_json(msg=FAILED_CREATION_MSG, failed=True)

    def diff_mode_behaviour(self, resp):
        profile_resp = self.omevv_profile_obj.get_firmware_repository_profile_by_id(resp.json_data)
        while profile_resp.json_data["status"] != "Success" and profile_resp.json_data["status"] != "Failed":
            time.sleep(3)
            profile_resp = self.omevv_profile_obj.get_firmware_repository_profile_by_id(resp.json_data)
        if self.module._diff and profile_resp.json_data["status"] == "Success" and self.module.params.get('resync'):
            self.module.exit_json(msg=SUCCESS_CREATION_RESYNC_MSG, profile_info=profile_resp.json_data, diff=self.diff_dict, changed=True)
        if self.module._diff and profile_resp.json_data["status"] == "Success":
            self.module.exit_json(msg=SUCCESS_CREATION_MSG, profile_info=profile_resp.json_data, diff=self.diff_dict, changed=True)
        if profile_resp.json_data["status"] == "Success" and self.module.params.get('resync'):
            self.module.exit_json(msg=SUCCESS_CREATION_RESYNC_MSG, profile_info=profile_resp.json_data, changed=True)
        if profile_resp.json_data["status"] == "Success":
            self.module.exit_json(msg=SUCCESS_CREATION_MSG, profile_info=profile_resp.json_data, changed=True)
        else:
            self.module.exit_json(msg=FAILED_CREATION_MSG, profile_info=profile_resp.json_data, failed=True)

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
            self.diff_mode_check(payload)
            self.module.exit_json(msg=CHANGES_FOUND_MSG, diff=self.diff_dict, changed=True)
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
        if api_response["protocolType"] in ("HTTP", "HTTPS"):
            api_response["sharePath"] = re.sub(r'(?<!:)//+', '/', api_response["sharePath"])
            module_response["sharePath"] = re.sub(r'(?<!:)//+', '/', module_response["sharePath"])
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
        self.diff_dict = {'before': {}, 'after': {}}
        trim = self.trim_api_response(api_response, payload)
        if payload.get("shareCredential") is not None:
            del payload["shareCredential"]
        output = recursive_diff(trim, payload)
        self.diff_dict['before'].update(output[0])
        self.diff_dict['after'].update(output[1])
        return self.diff_dict

    def modify_firmware_repository_profile(self, api_response, module_response):
        protocol_type = api_response["protocolType"]
        catalog_path = api_response["sharePath"]
        res = FirmwareRepositoryProfile.test_connection(self, protocol_type, catalog_path)
        name = self.module.params.get('new_name') if self.module.params.get('new_name') is not None else self.module.params.get('name')
        if res:
            self.rec_diff(api_response, module_response)
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
                self.output_modify_response(api_response)
            else:
                self.module.exit_json(msg=FAILED_MODIFY_MSG, failed=True)

    def output_modify_response(self, api_response):
        profile_resp = self.omevv_profile_obj.get_firmware_repository_profile_by_id(api_response["id"])
        while profile_resp.json_data["status"] != "Success" and profile_resp.json_data["status"] != "Failed":
            time.sleep(3)
            profile_resp = self.omevv_profile_obj.get_firmware_repository_profile_by_id(api_response["id"])
        if self.module._diff and profile_resp.json_data["status"] == "Success" and self.module.params.get('resync'):
            self.module.exit_json(msg=SUCCESS_MODIFY_RESYNC_MSG, profile_info=profile_resp.json_data, diff=self.diff_dict, changed=True)
        if self.module._diff and profile_resp.json_data["status"] == "Success":
            self.module.exit_json(msg=SUCCESS_MODIFY_MSG, profile_info=profile_resp.json_data, diff=self.diff_dict, changed=True)
        if profile_resp.json_data["status"] == "Success" and self.module.params.get('resync'):
            self.module.exit_json(msg=SUCCESS_MODIFY_RESYNC_MSG, profile_info=profile_resp.json_data, changed=True)
        if profile_resp.json_data["status"] == "Success":
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
            self.module.exit_json(msg=CHANGES_NOT_FOUND_MSG, diff={"before": {}, "after": {}}, changed=False)


class ResyncFirmwareRepositoryProfile(FirmwareRepositoryProfile):

    def __init__(self, module, rest_obj, rest_ome_obj):
        self.module = module
        super().__init__(module, rest_obj)
        self.rest_obj = rest_obj
        self.ome_obj = rest_ome_obj

    def check_plugin_availability(self):
        ump_plugin = 0
        details = self.ome_obj.invoke_request("GET", PLUGINS_URI)
        resp = details.json_data["value"]
        for item in resp:
            if item.get("Name") == "Update Manager":
                ump_plugin = 1
                break
        if not ump_plugin:
            self.module.exit_json(msg=UMP_PLUGIN_NOT_FOUND_MSG, failed=True)

    def check_mode_support(self):
        omevv_profiles = self.omevv_profile_obj.get_firmware_repository_profile()
        res = self.ome_obj.invoke_request("GET", UMP_URI)
        ump_profiles = res.json_data["value"]
        relevant_catalog_types = {"ESXi Catalog for Enterprise Servers", "vSAN Catalog for Enterprise Servers"}
        filtered_ump_profiles = [p for p in ump_profiles if p["CatalogType"] in relevant_catalog_types]
        not_avail = []
        omevv_profile_names = {p["profileName"] for p in omevv_profiles}
        for profile in filtered_ump_profiles:
            if profile["Name"] not in omevv_profile_names:
                not_avail.append(profile)
        self.remove_keys(filtered_ump_profiles, not_avail)
        if len(not_avail) > 0 and self.module._diff:
            self.diff_dict['after'].update({"ump_profiles": not_avail})
            self.module.exit_json(msg=CHANGES_FOUND_MSG, diff=self.diff_dict, changed=True)
        if len(not_avail) > 0:
            self.module.exit_json(msg=CHANGES_FOUND_MSG, changed=True)
        if len(not_avail) == 0 and self.module._diff:
            self.module.exit_json(msg=CHANGES_NOT_FOUND_MSG, diff={"before": {}, "after": {}}, changed=False)
        if len(not_avail) == 0:
            self.module.exit_json(msg=CHANGES_NOT_FOUND_MSG, changed=False)

    def remove_keys(self, filtered_ump_profiles, not_avail):
        keys_to_remove = {"@odata.type", "@odata.id", "BaseCatalogID", "BaseCatalogName", "AvailableVersions", "DevicesRepo", "UrgentComponentsCount",
                          "RecommendedComponentsCount", "OptionalComponentsCount", "BaselineId", "BaselineName", "BaselineDescription", "BaselineVersion",
                          "RefreshedVersion", "Details@odata.navigationLink", "Size", "Label", "ComponentsCount", "AvailableCatalog", "CatalogType",
                          "Owner", "LastModifiedBy", "DateModified", "Id"}
        for profile in not_avail:
            for key in keys_to_remove:
                if key in profile:
                    del profile[key]
        for profile in filtered_ump_profiles:
            for key in keys_to_remove:
                if key in profile:
                    del profile[key]
        for item in not_avail:
            name = item.get('Name', '')
            version = item.get('Version', '')
            profilename = name
            sharepath = "//shared/dell/omc/cifs/idrac/RepositoryStore"
            profiletype = "Firmware"
            filename = f"{name}_{version}_Catalog.xml"
            del item['Name']
            del item['Version']
            item['profileName'] = profilename
            item['sharePath'] = sharepath
            item['profileType'] = profiletype
            item['fileName'] = filename
            item['factoryCreated'] = False
            item['factoryType'] = "Custom"
            item['checkCertificate'] = None
            item['protocolType'] = "Not Applicable"
            item['createdBy'] = "Not Available"
            item['modifiedBy'] = "Not Available"
            item['owner'] = "UMP"

    def sort_profiles(self, profiles):
        return sorted(profiles, key=lambda x: x["id"])

    def execute(self):
        self.check_plugin_availability()
        if self.module.check_mode:
            self.check_mode_support()
        presync_result = self.omevv_profile_obj.get_firmware_repository_profile()
        resp = self.omevv_profile_obj.resync_repository_profiles_from_ump()
        if resp.success:
            time.sleep(14)
            postsync_result = self.omevv_profile_obj.get_firmware_repository_profile()
            presync_ump_profiles = [profile for profile in presync_result if profile.get("owner") == "UMP"]
            postsync_ump_profiles = [profile for profile in postsync_result if profile.get("owner") == "UMP"]
            presync_ump_profiles = self.sort_profiles(presync_ump_profiles)
            postsync_ump_profiles = self.sort_profiles(postsync_ump_profiles)
            difference = [item for item in postsync_ump_profiles if item not in presync_ump_profiles]
            diff = presync_ump_profiles != postsync_ump_profiles
            self.diff_mode_behaviour(presync_ump_profiles, postsync_ump_profiles, difference, diff)
        else:
            self.module.exit_json(msg=FAILED_RESYNC_MSG, failed=True)

    def diff_mode_behaviour(self, presync_ump_profiles, postsync_ump_profiles, difference, diff):
        if diff and self.module._diff and self.module.params.get('name') is None:
            self.diff_dict['after'].update({"ump_profiles": difference})
            self.module.exit_json(msg=SUCCESS_RESYNC_MSG, diff=self.diff_dict, firmware_repository_profile=difference, changed=True)
        if diff and self.module.params.get('name') is None:
            self.module.exit_json(msg=SUCCESS_RESYNC_MSG, firmware_repository_profile=postsync_ump_profiles, changed=True)
        if diff and self.module._diff:
            self.diff_dict['after'].update({"ump_profiles": difference})
        if not diff and self.module.params.get('name') is None and self.module._diff:
            self.diff_dict['before'].update({"ump_profiles": presync_ump_profiles})
            self.diff_dict['after'].update({"ump_profiles": postsync_ump_profiles})
            self.module.exit_json(msg=CHANGES_NOT_FOUND_MSG, diff=self.diff_dict, changed=False)
        if not diff and self.module.params.get('name') is None:
            self.module.exit_json(msg=CHANGES_NOT_FOUND_MSG, changed=False)


class DeleteFirmwareRepositoryProfile(FirmwareRepositoryProfile):

    def __init__(self, module, rest_obj):
        self.module = module
        self.obj = rest_obj
        super().__init__(module, rest_obj)

    def diff_mode_check(self, payload):
        diff_dict = {}
        diff_dict["profileName"] = payload["profileName"]
        diff_dict["description"] = payload["description"]
        diff_dict["profileType"] = payload["profileType"]
        diff_dict["sharePath"] = payload["sharePath"]
        diff_dict["protocolType"] = payload["protocolType"]
        self.diff_dict['before'].update(diff_dict)
        return self.diff_dict

    def delete_firmware_repository_profile(self, api_response):
        self.diff_mode_check(api_response)
        resp = self.omevv_profile_obj.delete_firmware_repository_profile(api_response["id"])
        if resp.success:
            if self.module._diff and self.module.params.get('resync'):
                self.module.exit_json(msg=SUCCESS_DELETION_RESYNC_MSG, diff=self.diff_dict, changed=True)
            if self.module._diff and self.module.params.get('resync'):
                self.module.exit_json(msg=SUCCESS_DELETION_RESYNC_MSG, diff=self.diff_dict, changed=True)
            if self.module._diff:
                self.module.exit_json(msg=SUCCESS_DELETION_MSG, diff=self.diff_dict, changed=True)
            self.module.exit_json(msg=SUCCESS_DELETION_MSG, changed=True)
        else:
            self.module.exit_json(msg=FAILED_DELETION_MSG, failed=True)

    def execute(self):
        profile = self.module.params.get('name')
        if profile is None:
            self.module.exit_json(msg=NO_OPERATION_SKIP_MSG, skipped=True)
        result = self.omevv_profile_obj.get_firmware_repository_profile()
        api_response = self.omevv_profile_obj.search_profile_name(result, profile)
        profile_exists = self.omevv_profile_obj.search_profile_name(result, profile)
        if profile_exists and self.module.check_mode and self.module._diff:
            diff = self.diff_mode_check(api_response)
            self.module.exit_json(msg=CHANGES_FOUND_MSG, diff=diff, changed=True)
        if not profile_exists and self.module.check_mode:
            self.module.exit_json(msg=CHANGES_NOT_FOUND_MSG, changed=False)
        if not profile_exists and not self.module.check_mode and self.module._diff:
            self.module.exit_json(msg=PROFILE_NOT_FOUND_MSG.format(profile_name=profile), diff={"before": {}, "after": {}}, failed=True)
        if not profile_exists and not self.module.check_mode:
            self.module.exit_json(msg=PROFILE_NOT_FOUND_MSG.format(profile_name=profile), failed=True)
        if profile_exists and not self.module.check_mode:
            self.delete_firmware_repository_profile(api_response)
        if profile_exists and self.module.check_mode:
            self.module.exit_json(msg=CHANGES_FOUND_MSG, changed=True)


def main():
    argument_spec = {
        "username": {"type": 'str'},
        "password": {"type": 'str', "no_log": True},
        "state": {"type": 'str', "choices": ['present', 'absent'], "default": 'present'},
        "share_username": {"type": 'str'},
        "share_password": {"type": 'str', "no_log": True},
        "name": {"type": 'str'},
        "new_name": {"type": 'str'},
        "catalog_path": {"type": 'str'},
        "description": {"type": 'str'},
        "protocol_type": {"type": 'str', "choices": ['NFS', 'CIFS', 'HTTP', 'HTTPS']},
        "share_domain": {"type": 'str'},
        "resync": {"type": 'bool', "default": False}
    }
    module = OMEVVAnsibleModule(
        argument_spec=argument_spec,
        required_if=[
            ["protocol_type", "NFS", ("catalog_path",)],
            ["protocol_type", "CIFS", ("catalog_path", "share_username", "share_password")],
            ["protocol_type", "HTTP", ("catalog_path",)],
            ["protocol_type", "HTTPS", ("catalog_path",)],
        ],
        supports_check_mode=True)
    try:
        with RestOMEVV(module.params) as rest_obj:
            if module.params.get('resync'):
                ome_module = OmeAnsibleModule(argument_spec, supports_check_mode=True)
                with RestOME(ome_module.params, req_session=True) as rest_ome_obj:
                    omevv_obj = ResyncFirmwareRepositoryProfile(module, rest_obj, rest_ome_obj)
                    omevv_obj.execute()
            if module.params.get('state') == 'present':
                if module.params.get('name') is None:
                    module.exit_json(msg=NO_OPERATION_SKIP_MSG, skipped=True)
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
