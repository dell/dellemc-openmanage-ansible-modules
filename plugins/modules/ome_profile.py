#!/usr/bin/python
# -*- coding: utf-8 -*-
# Dell OpenManage Ansible Modules
# Version 10.0.0
# Copyright (C) 2021-2025 Dell Inc. or its subsidiaries. All Rights Reserved.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: ome_profile
short_description: Create, modify, delete, assign, unassign and migrate a profile on OpenManage Enterprise
version_added: "3.1.0"
description: "This module allows to create, modify, delete, assign, unassign, and migrate a profile on OpenManage Enterprise."
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  command:
    description:
      - C(create) creates new profiles.
      - "C(modify) modifies an existing profile. Only I(name), I(description), I(boot_to_network_iso), and I(attributes)
      can be modified."
      - C(delete) deletes an existing profile.
      - C(assign) Deploys an existing profile on a target device and returns a task ID.
      - C(unassign) unassigns a profile from a specified target and returns a task ID.
      - C(migrate) migrates an existing profile and returns a task ID.
    choices: [create, modify, delete, assign, unassign, migrate]
    default: create
    type: str
  name_prefix:
    description:
      - The name provided when creating a profile is used a prefix followed by the number assigned to it by OpenManage Enterprise.
      - This is applicable only for a create operation.
      - This option is mutually exclusive with I(name).
    type: str
    default: Profile
  name:
    description:
      - Name of the profile.
      - This is applicable for modify, delete, assign, unassign, and migrate operations.
      - This option is mutually exclusive with I(name_prefix) and I(number_of_profiles).
    type: str
  new_name:
    description:
      - New name of the profile.
      - Applicable when I(command) is C(modify).
    type: str
  number_of_profiles:
    description:
      - Provide the number of profiles to be created.
      - This is applicable when I(name_prefix) is used with C(create).
      - This option is mutually exclusive with I(name).
      - Openmanage Enterprise can create a maximum of 100 profiles.
    type: int
    default: 1
  template_name:
    description:
      - Name of the template for creating the profile(s).
      - This is applicable when I(command) is C(create).
      - This option is mutually exclusive with I(template_id).
    type: str
  template_id:
    description:
      - ID of the template.
      - This is applicable when I(command) is C(create).
      - This option is mutually exclusive with I(template_name).
    type: int
  device_id:
    description:
      - ID of the target device.
      - This is applicable when I(command) is C(assign) and C(migrate).
      - This option is mutually exclusive with I(device_service_tag).
    type: int
  device_service_tag:
    description:
      - Identifier of the target device.
      - This is typically 7 to 8 characters in length.
      - Applicable when I(command) is C(assign), and C(migrate).
      - This option is mutually exclusive with I(device_id).
      - If the device does not exist when I(command) is C(assign) then the profile is auto-deployed.
    type: str
  description:
    description: Description of the profile.
    type: str
  boot_to_network_iso:
    description:
      - Details of the Share iso.
      - Applicable when I(command) is C(create), C(assign), and C(modify).
    type: dict
    suboptions:
      boot_to_network:
        description: Enable or disable a network share.
        type: bool
        required: true
      share_type:
        description: Type of network share.
        type: str
        choices: [NFS, CIFS]
      share_ip:
        description: IP address of the network share.
        type: str
      share_user:
        description: User name when I(share_type) is C(CIFS).
        type: str
      share_password:
        description: User password when I(share_type) is C(CIFS).
        type: str
      workgroup:
        description: User workgroup when I(share_type) is C(CIFS).
        type: str
      iso_path:
        description: Specify the full ISO path including the share name.
        type: str
      iso_timeout:
        description: Set the number of hours that the network ISO file will remain mapped to the target device(s).
        type: int
        choices: [1, 2, 4, 8, 16]
        default: 4
  filters:
    description:
      - Filters the profiles based on selected criteria.
      - This is applicable when I(command) is C(delete) or C(unassign).
      - This supports suboption I(ProfileIds) which takes a list of profile IDs.
      - This also supports OData filter expressions with the suboption I(Filters).
      - See OpenManage Enterprise REST API guide for the filtering options available.
      - I(WARNING) When this option is used in case of C(unassign), task ID is not returned for any of the profiles affected.
    type: dict
  force:
    description:
      - Provides the option to force the migration of a profile even if the source device cannot be contacted.
      - This option is applicable when I(command) is C(migrate).
    type: bool
    default: false
  attributes:
    description: Attributes for C(modify) and C(assign).
    type: dict
    suboptions:
      Attributes:
        description:
          - List of attributes to be modified, when I(command) is C(modify).
          - List of attributes to be overridden when I(command) is C(assign).
          - "Use the I(Id) If the attribute Id is available. If not, use the comma separated I (DisplayName).
          For more details about using the I(DisplayName), see the example provided."
        type: list
        elements: dict
      Options:
        description:
          - Provides the different shut down options.
          - This is applicable when I(command) is C(assign).
        type: dict
      Schedule:
        description:
          - Schedule for profile deployment.
          - This is applicable when I(command) is C(assign).
        type: dict
requirements:
    - "python >= 3.9.6"
author:
    - "Jagadeesh N V (@jagadeeshnv)"
    - "Bhavneet Sharma (@Bhavneet-Sharma)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
    - This module supports C(check_mode).
    - C(assign) operation on a already assigned profile will not redeploy.
'''

EXAMPLES = r'''
---
- name: Create two profiles from a template
  dellemc.openmanage.ome_profile:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    template_name: "template 1"
    name_prefix: "omam_profile"
    number_of_profiles: 2

- name: Create profile with NFS share
  dellemc.openmanage.ome_profile:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: create
    template_name: "template 1"
    name_prefix: "omam_profile"
    number_of_profiles: 1
    boot_to_network_iso:
      boot_to_network: true
      share_type: NFS
      share_ip: "192.168.0.1"
      iso_path: "path/to/my_iso.iso"
      iso_timeout: 8

- name: Create profile with CIFS share
  dellemc.openmanage.ome_profile:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: create
    template_name: "template 1"
    name_prefix: "omam_profile"
    number_of_profiles: 1
    boot_to_network_iso:
      boot_to_network: true
      share_type: CIFS
      share_ip: "192.168.0.2"
      share_user: "username"
      share_password: "password"
      workgroup: "workgroup"
      iso_path: "\\path\\to\\my_iso.iso"
      iso_timeout: 8

- name: Modify profile name with NFS share and attributes
  dellemc.openmanage.ome_profile:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: modify
    name: "Profile 00001"
    new_name: "modified profile"
    description: "new description"
    boot_to_network_iso:
      boot_to_network: true
      share_type: NFS
      share_ip: "192.168.0.3"
      iso_path: "path/to/my_iso.iso"
      iso_timeout: 8
    attributes:
      Attributes:
        - Id: 4506
          Value: "server attr 1"
          IsIgnored: false
        - Id: 4507
          Value: "server attr 2"
          IsIgnored: false
        # Enter the comma separated string as appearing in the Detailed view on GUI
        # System -> Server Topology -> ServerTopology 1 Aisle Name
        - DisplayName: 'System, Server Topology, ServerTopology 1 Aisle Name'
          Value: Aisle 5
          IsIgnored: false

- name: Delete a profile using profile name
  dellemc.openmanage.ome_profile:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: "delete"
    name: "Profile 00001"

- name: Delete profiles using filters
  dellemc.openmanage.ome_profile:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: "delete"
    filters:
      SelectAll: true
      Filters: =contains(ProfileName,'Profile 00002')

- name: Delete profiles using profile list filter
  dellemc.openmanage.ome_profile:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: "delete"
    filters:
      ProfileIds:
        - 17123
        - 16124

- name: Assign a profile to target along with network share
  dellemc.openmanage.ome_profile:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: assign
    name: "Profile 00001"
    device_id: 12456
    boot_to_network_iso:
      boot_to_network: true
      share_type: NFS
      share_ip: "192.168.0.1"
      iso_path: "path/to/my_iso.iso"
      iso_timeout: 8
    attributes:
      Attributes:
        - Id: 4506
          Value: "server attr 1"
          IsIgnored: true
      Options:
        ShutdownType: 0
        TimeToWaitBeforeShutdown: 300
        EndHostPowerState: 1
        StrictCheckingVlan: true
      Schedule:
        RunNow: true
        RunLater: false

- name: Unassign a profile using profile name
  dellemc.openmanage.ome_profile:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: "unassign"
    name: "Profile 00003"

- name: Unassign profiles using filters
  dellemc.openmanage.ome_profile:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: "unassign"
    filters:
      SelectAll: true
      Filters: =contains(ProfileName,'Profile 00003')

- name: Unassign profiles using profile list filter
  dellemc.openmanage.ome_profile:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: "unassign"
    filters:
      ProfileIds:
        - 17123
        - 16123

- name: Migrate a profile
  dellemc.openmanage.ome_profile:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: "migrate"
    name: "Profile 00001"
    device_id: 12456
'''

RETURN = r'''
---
msg:
  description: Overall status of the profile operation.
  returned: always
  type: str
  sample: "Successfully created 2 profile(s)."
profile_ids:
  description: IDs of the profiles created.
  returned: when I(command) is C(create)
  type: list
  sample: [1234, 5678]
job_id:
  description:
    - Task ID created when I(command) is C(assign), C(migrate) or C(unassign).
    - C(assign) and C(unassign) operations do not trigger a task if a profile is auto-deployed.
  returned: when I(command) is C(assign), C(migrate) or C(unassign)
  type: int
  sample: 14123
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
import time
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.common.dict_transformations import recursive_diff


PROFILE_VIEW = "ProfileService/Profiles"
GET_PORFILE_INST = "ProfileService/Profiles({profileId})"
TEMPLATE_VIEW = "TemplateService/Templates"
DEVICE_VIEW = "DeviceService/Devices"
JOB_URI = "JobService/Jobs({job_id})"
PROFILE_ACTION = "ProfileService/Actions/ProfileService.{action}"
PROFILE_ATTRIBUTES = "ProfileService/Profiles({profile_id})/AttributeDetails"
PROFILE_NOT_FOUND = "Profile with the name '{name}' not found."
CHANGES_MSG = "Changes found to be applied."
NO_CHANGES_MSG = "No changes found to be applied."
SEPRTR = ','
FILTER_QUERY_PARAM = "$filter"


def get_template_details(module, rest_obj):
    template_identifier = module.params.get('template_id')
    query_param = {FILTER_QUERY_PARAM: "Id eq {0}".format(template_identifier)}
    srch = 'Id'
    if not template_identifier:
        template_identifier = module.params.get('template_name')
        query_param = {FILTER_QUERY_PARAM: "Name eq '{0}'".format(template_identifier)}
        srch = 'Name'
    resp = rest_obj.invoke_request('GET', TEMPLATE_VIEW, query_param=query_param)

    template_details = match_profile(resp=resp, search_key=srch, identifier_value=template_identifier)

    if template_details is not None:
        return template_details

    module.exit_json(msg="Template with {0} '{1}' not found.".format(srch, template_identifier),
                     failed=True)


def get_target_details(module, rest_obj):
    device_identifier = module.params.get('device_id')
    query_param = {FILTER_QUERY_PARAM: "Id eq {0}".format(device_identifier)}
    srch = 'Id'
    if not device_identifier:
        device_identifier = module.params.get('device_service_tag')
        query_param = {FILTER_QUERY_PARAM: "Identifier eq '{0}'".format(device_identifier)}
        srch = 'Identifier'
    resp = rest_obj.invoke_request('GET', DEVICE_VIEW, query_param=query_param)
    device_details = match_profile(resp=resp, search_key=srch, identifier_value=device_identifier)
    if device_details is not None:
        return device_details
    return "Target with {0} '{1}' not found.".format(srch, device_identifier)


def match_profile(resp, search_key, identifier_value=None):
    """get profile/target/device details based on profile name."""
    if resp.success and resp.json_data.get('value'):
        tlist = resp.json_data.get('value', [])
        for xtype in tlist:
            if (xtype.get(search_key) == identifier_value) or xtype.get('DeploymentTaskId'):
                return xtype


def get_profile(rest_obj, module):
    """Get profile details based on profile ID or profile name from filters."""
    query_filter = module.params.get("filters", {})
    profile = None
    srch_key = "ProfileName"

    # when ProfileIds are in filters
    profile_ids = query_filter.get("ProfileIds", []) if query_filter is not None else []
    if profile_ids:
        profile_id = profile_ids[0]
        resp = rest_obj.invoke_request("GET", GET_PORFILE_INST.format(profileId=profile_id))
        if resp.json_data:
            profile = resp.json_data

    # when Profilename in filters
    filter_string = query_filter.get('Filters') if query_filter is not None else None
    if filter_string and 'ProfileName' in filter_string:
        query_param = {FILTER_QUERY_PARAM: filter_string[1:]}
        resp = rest_obj.invoke_request('GET', PROFILE_VIEW, query_param=query_param)
        profile = match_profile(resp=resp, search_key=srch_key)

    # when profile name is provided
    profile_name = module.params.get("name")
    if profile_name:
        query_param = {FILTER_QUERY_PARAM: "ProfileName eq '{0}'".format(profile_name)}
        resp = rest_obj.invoke_request('GET', PROFILE_VIEW, query_param=query_param)
        profile = match_profile(resp=resp, search_key=srch_key, identifier_value=profile_name)

    return profile


def get_network_iso_payload(module):
    boot_iso_dict = module.params.get("boot_to_network_iso")
    iso_payload = {}
    if boot_iso_dict:
        iso_payload = {"BootToNetwork": False}
        if boot_iso_dict.get("boot_to_network"):
            iso_payload["BootToNetwork"] = True
            share_type = boot_iso_dict.get("share_type")
            iso_payload["ShareType"] = share_type
            share_detail = {}
            sh_ip = boot_iso_dict.get("share_ip")
            share_detail["IpAddress"] = sh_ip
            share_detail["ShareName"] = sh_ip
            share_detail["User"] = boot_iso_dict.get("share_user")
            share_detail["Password"] = boot_iso_dict.get("share_password")
            share_detail["WorkGroup"] = boot_iso_dict.get("workgroup")
            iso_payload["ShareDetail"] = share_detail
            if str(boot_iso_dict.get("iso_path")).lower().endswith('.iso'):
                iso_payload["IsoPath"] = boot_iso_dict.get("iso_path")
            else:
                module.exit_json(msg="ISO path does not have extension '.iso'", failed=True)
            iso_payload["IsoTimeout"] = boot_iso_dict.get("iso_timeout")
    return iso_payload


def recurse_subattr_list(subgroup, prefix, attr_detailed, attr_map, adv_list):
    if not isinstance(subgroup, list):
        return

    for each_sub in subgroup:
        new_prefix = f"{prefix}{SEPRTR}{each_sub.get('DisplayName')}"
        if each_sub.get("SubAttributeGroups"):
            recurse_subattr_list(each_sub.get("SubAttributeGroups"),
                                 new_prefix, attr_detailed,
                                 attr_map, adv_list)
        else:
            for attr in each_sub.get('Attributes'):
                attr['prefix'] = new_prefix
                # case sensitive, remove whitespaces for optim
                constr = "{0}{1}{2}".format(new_prefix, SEPRTR, attr['DisplayName'])
                if constr in adv_list:
                    attr_detailed[constr] = attr['AttributeId']
                attr_map[attr['AttributeId']] = attr


def get_subattr_all(attr_dtls, adv_list):
    attr_detailed = {}
    attr_map = {}
    for each in attr_dtls:
        recurse_subattr_list(each.get('SubAttributeGroups'), each.get('DisplayName'),
                             attr_detailed, attr_map, adv_list)
    return attr_detailed, attr_map


def normalize_display_names(attributes):
    normalized = []
    for attr in attributes:
        if attr.get("DisplayName"):
            split_k = str(attr.get("DisplayName")).split(SEPRTR)
            trimmed = map(str.strip, split_k)
            n_k = SEPRTR.join(trimmed)
            normalized.append(n_k)
    return normalized


def attributes_check(rest_obj, inp_attr, profile_id):
    diff = 0
    try:
        resp = rest_obj.invoke_request("GET", PROFILE_ATTRIBUTES.format(profile_id=profile_id))
        attr_dtls = resp.json_data
        adv_list = normalize_display_names(attributes=inp_attr.get("Attributes", []))
        attr_detailed, attr_map = get_subattr_all(attr_dtls.get('AttributeGroups'), adv_list)
        payload_attr = inp_attr.get("Attributes", [])
        rem_attrs = []
        for attr in payload_attr:
            if attr.get("DisplayName"):
                split_k = str(attr.get("DisplayName")).split(SEPRTR)
                trimmed = map(str.strip, split_k)
                n_k = SEPRTR.join(trimmed)
                obj_id = attr_detailed.get(n_k, "")
                attr['Id'] = obj_id
                attr.pop("DisplayName", None)
            else:
                obj_id = attr.get('Id')
            if obj_id:
                ex_val = attr_map.get(obj_id, {})
                if not ex_val:
                    rem_attrs.append(attr)
                    continue
                if attr.get('Value') != ex_val.get("Value") or attr.get('IsIgnored') != ex_val.get("IsIgnored"):
                    diff = diff + 1
        for rem in rem_attrs:
            payload_attr.remove(rem)
    except Exception:
        diff = 1
    return diff


def assign_profile(module, rest_obj):
    mparam = module.params
    payload = {}
    prof = prepare_profile_payload(module, rest_obj, mparam, payload)

    target = get_target_details(module, rest_obj)
    if isinstance(target, dict):
        payload['TargetId'] = target['Id']
        _validate_profile_assignment(module=module, payload=payload, prof=prof, target=target)

        action = "AssignProfile"
        try:
            resp = rest_obj.invoke_request('POST', PROFILE_ACTION.format(action='GetInvalidTargetsForAssignProfile'),
                                           data={'Id': prof['Id']})
            if target['Id'] in list(resp.json_data):
                module.exit_json(msg="The target device is invalid for the given profile.", failed=True)
        except HTTPError:
            resp = None
        ad_opts_list = ['Attributes', 'Options', 'Schedule']
    else:
        if mparam.get('device_id'):
            module.exit_json(msg=target, failed=True)
        action = "AssignProfileForAutoDeploy"
        payload['Identifier'] = mparam.get('device_service_tag')
        _validate_profile_assignment(module=module, payload=payload, prof=prof)

        ad_opts_list = ['Attributes']
    boot_iso_dict = get_network_iso_payload(module)
    if boot_iso_dict:
        payload["NetworkBootToIso"] = boot_iso_dict
    ad_opts = mparam.get("attributes")
    for opt in ad_opts_list:
        if ad_opts and ad_opts.get(opt):
            attributes_check(rest_obj, ad_opts, prof['Id'])
            payload[opt] = ad_opts.get(opt)
    if module.check_mode:
        module.exit_json(msg=CHANGES_MSG, changed=True)
    rest_obj.invoke_request('POST', PROFILE_ACTION.format(action=action), data=payload)
    handle_post_assignment(module=module, rest_obj=rest_obj, action=action)


def handle_post_assignment(module, rest_obj, action):
    """
    Handle the post assignment of a profile based on the action type.

    Parameters:
        module (AnsibleModule): The Ansible module object.
        rest_obj (REST Object): The REST object used for API calls.
        action (str): The action type, e.g. 'AssignProfile'.

    Returns:
        dict: A dictionary containing a success message and a job ID if applicable.
    """

    action_map = {
        "AssignProfile": "assign",
        "UnassignProfiles": "unassign",
        "MigrateProfile": "migrate"
    }

    performed_action = action_map.get(action)

    if action in ["AssignProfile", "UnassignProfiles", "MigrateProfile"]:
        res_dict = {'msg': f"Successfully applied the {performed_action} operation. No job was triggered.",
                    'changed': True}
        try:
            res_prof = get_profile(rest_obj, module)
            time.sleep(5)
            if res_prof.get('DeploymentTaskId'):
                res_dict['job_id'] = res_prof.get('DeploymentTaskId')
                res_dict['msg'] = f"Successfully triggered the job for the {performed_action} operation."
        except HTTPError:
            res_dict['msg'] += " Failed to fetch job details."
    module.exit_json(**res_dict)


def prepare_profile_payload(module, rest_obj, mparam, payload):
    """
    Prepare the profile payload for a given profile name and module.

    Parameters:
        module (AnsibleModule): The Ansible module object.
        rest_obj (REST Object): The REST object used for API calls.
        mparam (dict): The module parameters.
        payload (dict): The payload to be prepared.

    Returns:
        dict: The prepared profile payload.
    """
    profile_name = mparam.get('name')
    if profile_name:
        prof = get_profile(rest_obj, module)
        if not prof:
            module.exit_json(msg=PROFILE_NOT_FOUND.format(name=mparam.get('name')), failed=True)
        payload['Id'] = prof['Id']
    return prof


def _validate_profile_assignment(module, payload, prof, target=None):
    """
    Validates if a profile is assigned to a target based on the profile state.

    Parameters:
        module (AnsibleModule): The Ansible module object.
        payload (dict): The payload containing the profile assignment details.
        prof (dict): The profile details.
        target (dict): The target details. Defaults to None.

    Returns:
        None
    """
    if prof['ProfileState'] in [1, 4]:
        target_id = target.get('Id') if prof.get('ProfileState') == 4 else payload.get('Identifier')
        if prof.get('TargetId') == target_id or prof.get('TargetName') == target_id:
            module.exit_json(msg="The profile is assigned to the target {0}.".format(target_id))
        else:
            module.exit_json(
                msg="The profile is assigned to a different target. Use the migrate command or "
                    "unassign the profile and then proceed with assigning the profile to the target.",
                failed=True)


def unassign_profile(module, rest_obj):
    mparam = module.params
    prof = {}
    if mparam.get('name'):
        payload = {}
        prof = get_profile(rest_obj, module)
        if prof:
            _validate_profile_deployed(module, prof)
            if prof['DeploymentTaskId']:
                resp = rest_obj.invoke_request('GET', JOB_URI.format(job_id=prof['DeploymentTaskId']))
                job_dict = resp.json_data
                job_status = job_dict.get('LastRunStatus')
                if job_status.get('Name') == 'Running':
                    module.exit_json(msg="Profile deployment task is in progress. Wait for the job to finish.", failed=True)
            payload['ProfileIds'] = [prof['Id']]
        else:
            module.exit_json(msg=PROFILE_NOT_FOUND.format(name=mparam.get('name')), failed=True)
    if mparam.get('filters'):
        payload = mparam.get('filters')
    if module.check_mode:
        module.exit_json(msg=CHANGES_MSG, changed=True)
    rest_obj.invoke_request('POST', PROFILE_ACTION.format(action="UnassignProfiles"), data=payload)
    handle_post_assignment(module=module, rest_obj=rest_obj, action="UnassignProfiles")


def _validate_profile_deployed(module, prof):
    if prof.get('ProfileState') == 0:
        module.exit_json(msg="Profile is in an unassigned state.")


def create_profile(module, rest_obj):
    mparam = module.params
    payload = {}
    template = get_template_details(module, rest_obj)
    payload["TemplateId"] = template["Id"]
    payload["NamePrefix"] = mparam.get("name_prefix")
    payload["NumberOfProfilesToCreate"] = mparam["number_of_profiles"]
    if mparam.get("description"):
        payload["Description"] = mparam["description"]
    boot_iso_dict = get_network_iso_payload(module)
    if boot_iso_dict:
        payload["NetworkBootToIso"] = boot_iso_dict
    if module.check_mode:
        module.exit_json(msg=CHANGES_MSG, changed=True)
    resp = rest_obj.invoke_request('POST', PROFILE_VIEW, data=payload)
    profile_id_list = resp.json_data
    module.exit_json(msg="Successfully created {0} profile(s).".format(len(profile_id_list)),
                     changed=True, profile_ids=profile_id_list)


def modify_profile(module, rest_obj):
    mparam = module.params
    payload = {}
    prof = get_profile(rest_obj, module)
    if not prof:
        module.exit_json(msg=PROFILE_NOT_FOUND.format(name=mparam.get('name')), failed=True)
    diff = 0
    diff += _update_name(mparam, payload, prof)
    diff += _update_description(mparam, payload, prof)
    boot_iso_dict = get_network_iso_payload(module)
    rdict = prof.get('NetworkBootToIso') if prof.get('NetworkBootToIso') else {}
    if boot_iso_dict:
        nest_diff = recursive_diff(boot_iso_dict, rdict)
        if nest_diff and nest_diff[0]:
            diff += 1
        payload["NetworkBootToIso"] = boot_iso_dict
    ad_opts = mparam.get("attributes")
    if ad_opts and ad_opts.get("Attributes"):
        diff = diff + attributes_check(rest_obj, ad_opts, prof['Id'])
        if ad_opts.get("Attributes"):
            payload["Attributes"] = ad_opts.get("Attributes")
    payload['Id'] = prof['Id']
    if diff:
        if module.check_mode:
            module.exit_json(msg=CHANGES_MSG, changed=True)
        rest_obj.invoke_request('PUT', PROFILE_VIEW + "({0})".format(payload['Id']), data=payload)
        module.exit_json(msg="Successfully modified the profile.", changed=True)
    module.exit_json(msg=NO_CHANGES_MSG)


def _update_name(mparam, payload, prof):
    new_name = mparam.get('new_name')
    payload['Name'] = prof['ProfileName']
    if new_name and new_name != prof['ProfileName']:
        payload['Name'] = new_name
        return 1
    return 0


def _update_description(mparam, payload, prof):
    desc = mparam.get('description')
    if desc and desc != prof['ProfileDescription']:
        payload['Description'] = desc
        return 1
    return 0


def delete_profile(module, rest_obj):
    mparam = module.params
    if mparam.get('name'):
        prof = get_profile(rest_obj, module)
        if prof:
            if prof['ProfileState'] > 0:
                module.exit_json(msg="Profile has to be in an unassigned state for it to be deleted.", failed=True)
            if module.check_mode:
                module.exit_json(msg=CHANGES_MSG, changed=True)
            rest_obj.invoke_request('DELETE', PROFILE_VIEW + "({0})".format(prof['Id']))
            module.exit_json(msg="Successfully deleted the profile.", changed=True)
        else:
            module.exit_json(msg=PROFILE_NOT_FOUND.format(name=mparam.get('name')))
    if mparam.get('filters'):
        payload = mparam.get('filters')
        if module.check_mode:
            module.exit_json(msg=CHANGES_MSG, changed=True)
        rest_obj.invoke_request('POST', PROFILE_ACTION.format(action='Delete'), data=payload)
        module.exit_json(msg="Successfully completed the delete operation.", changed=True)


def migrate_profile(module, rest_obj):
    mparam = module.params
    payload = {}
    payload['ForceMigrate'] = mparam.get('force')
    target = get_target_details(module, rest_obj)
    if not isinstance(target, dict):
        module.exit_json(msg=target, failed=True)
    payload['TargetId'] = target['Id']
    prof = get_profile(rest_obj, module)
    if prof:
        if target['Id'] == prof['TargetId']:
            module.exit_json(msg=NO_CHANGES_MSG)
        try:
            resp = rest_obj.invoke_request('POST', PROFILE_ACTION.format(action='GetInvalidTargetsForAssignProfile'),
                                           data={'Id': prof['Id']})
            if target['Id'] in list(resp.json_data):
                module.exit_json(msg="The target device is invalid for the given profile.", failed=True)
        except HTTPError:
            resp = None
        if prof['ProfileState'] == 4:  # migrate applicable in deployed state only
            payload['ProfileId'] = prof['Id']
            if module.check_mode:
                module.exit_json(msg=CHANGES_MSG, changed=True)
            rest_obj.invoke_request('POST', PROFILE_ACTION.format(action='MigrateProfile'), data=payload)
            handle_post_assignment(module=module, rest_obj=rest_obj, action="MigrateProfile")
        else:
            module.exit_json(msg="Profile needs to be in a deployed state for a migrate operation.", failed=True)
    else:
        module.exit_json(msg=PROFILE_NOT_FOUND.format(name=mparam.get('name')), failed=True)


def profile_operation(module, rest_obj):
    command = module.params.get("command")
    if command == "create":
        create_profile(module, rest_obj)
    if command == "modify":
        modify_profile(module, rest_obj)
    if command == "delete":
        delete_profile(module, rest_obj)
    if command == "assign":
        assign_profile(module, rest_obj)
    if command == "unassign":
        unassign_profile(module, rest_obj)
    if command == "migrate":
        migrate_profile(module, rest_obj)


def main():
    network_iso_spec = {"boot_to_network": {"required": True, "type": 'bool'},
                        "share_type": {"choices": ['NFS', 'CIFS']},
                        "share_ip": {"type": 'str'},
                        "share_user": {"type": 'str'},
                        "share_password": {"type": 'str', "no_log": True},
                        "workgroup": {"type": 'str'},
                        "iso_path": {"type": 'str'},
                        "iso_timeout": {"type": 'int', "default": 4,
                                        "choices": [1, 2, 4, 8, 16]}}
    assign_spec = {"Attributes": {"type": 'list', "elements": 'dict'},
                   "Options": {"type": 'dict'},
                   "Schedule": {"type": 'dict'}}
    specs = {
        "command": {"default": "create",
                    "choices": ['create', 'modify', 'delete', 'assign', 'unassign', 'migrate']},
        "name_prefix": {"default": "Profile", "type": 'str'},
        "name": {"type": 'str'},
        "new_name": {"type": 'str'},
        "number_of_profiles": {"default": 1, "type": 'int'},
        "template_name": {"type": 'str'},
        "template_id": {"type": "int"},
        "device_id": {"type": 'int'},
        "device_service_tag": {"type": 'str'},
        "description": {"type": 'str'},
        "boot_to_network_iso": {"type": 'dict', "options": network_iso_spec,
                                "required_if": [
                                    ['boot_to_network', True, ['share_type', 'share_ip', 'iso_path']],
                                    ['share_type', 'CIFS', ['share_user', 'share_password']]
                                ]},
        "filters": {"type": 'dict'},
        "attributes": {"type": 'dict', "options": assign_spec},
        "force": {"default": False, "type": 'bool'}
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        required_if=[
            ['command', 'create', ['template_name', 'template_id'], True],
            ['command', 'modify', ['name']],
            ['command', 'modify', ['new_name', 'description', 'attributes', 'boot_to_network_iso'], True],
            ['command', 'assign', ['name']],
            ['command', 'assign', ['device_id', 'device_service_tag'], True],
            ['command', 'unassign', ['name', "filters"], True],
            ['command', 'delete', ['name', "filters"], True],
            ['command', 'migrate', ['name']],
            ['command', 'migrate', ['device_id', 'device_service_tag'], True],
        ],
        mutually_exclusive=[
            ['name', 'name_prefix'],
            ['name', 'number_of_profiles'],
            ['name', 'filters'],
            ['device_id', 'device_service_tag'],
            ['template_name', 'template_id']],
        supports_check_mode=True)
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            profile_operation(module, rest_obj)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True, failed=True)
    except (IOError, ValueError, TypeError, ConnectionError, SSLValidationError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
