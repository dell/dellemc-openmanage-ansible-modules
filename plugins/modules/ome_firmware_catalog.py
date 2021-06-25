#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.5.0
# Copyright (C) 2019-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_firmware_catalog
short_description: Create, modify, or delete a firmware catalog on OpenManage Enterprise or OpenManage Enterprise Modular
version_added: "2.0.0"
description: This module allows to create, modify, or delete a firmware catalog on OpenManage Enterprise or OpenManage Enterprise Modular.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  state:
    description:
      - C(present) creates or modifies a catalog.
      - C(absent) deletes an existing catalog.
    choices: [present, absent]
    default: present
    type: str
    version_added: 3.4.0
  catalog_name:
    type: list
    elements: str
    description:
      - Name of the firmware catalog to be created.
      - This is option is mutually exclusive with I(catalog_id).
      - Provide the list of firmware catalog names that are supported when I(state) is C(absent).
  new_catalog_name:
    type: str
    description:
      - New name of the firmware catalog.
    version_added: 3.4.0
  catalog_id:
    type: list
    elements: int
    description:
      - ID of the catalog.
      - This option is mutually exclusive with I(catalog_name).
      - Provide the list of firmware catalog IDs that are supported when I(state) is C(absent).
    version_added: 3.4.0
  catalog_description:
    type: str
    description:
      - Description for the catalog.
  source:
    type: str
    description:
      - The IP address of the system where the firmware catalog is stored on the local network.
      - By default, this option is set to downloads.dell.com when I(repository_type) is C(DELL_ONLINE).
  source_path:
    type: str
    description:
      - Specify the complete path of the catalog file location without the file name.
      - This is option ignored when I(repository_type) is C(DELL_ONLINE).
  file_name:
    type: str
    description:
      - Catalog file name associated with the I(source_path).
      - This option is ignored when I(repository_type) is C(DELL_ONLINE).
  repository_type:
    type: str
    description:
      - Type of repository. The supported types are NFS, CIFS, HTTP, HTTPS,and DELL_ONLINE.
    choices: ["NFS", "CIFS", "HTTP", "HTTPS", "DELL_ONLINE"]
  repository_username:
    type: str
    description:
      - User name of the repository where the catalog is stored.
      - This option is mandatory when I(repository_type) is CIFS.
      - This option is ignored when I(repository_type) is C(DELL_ONLINE).
  repository_password:
    type: str
    description:
      - Password to access the repository.
      - This option is mandatory when I(repository_type) is CIFS.
      - This option is ignored when I(repository_type) is C(DELL_ONLINE).
      - C(NOTE) The module always reports the changed status, when this is provided.
  repository_domain:
    type: str
    description:
      - Domain name of the repository.
      - This option is ignored when I(repository_type) is C(DELL_ONLINE).
  check_certificate:
    type: bool
    description:
      - The certificate warnings are ignored when I(repository_type) is HTTPS. If C(True). If not, certificate warnings
       are not ignored.
    default: False
  job_wait:
    description:
      - Provides the option to wait for job completion.
      - This option is applicable when I(state) is C(present).
    type: bool
    default: true
    version_added: 3.4.0
  job_wait_timeout:
    description:
      - The maximum wait time of I(job_wait) in seconds. The job is tracked only for this duration.
      - This option is applicable when I(job_wait) is C(True).
    type: int
    default: 600
    version_added: 3.4.0
requirements:
    - "python >= 2.7.5"
author:
    - "Sajna Shetty(@Sajna-Shetty)"
    - "Jagadeesh N V(@jagadeeshnv)"
notes:
    - If I(repository_password) is provided, then the module always reports the changed status.
    - Run this module from a system that has direct access to DellEMC OpenManage Enterprise or OpenManage Enterprise Modular.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Create a catalog from HTTPS repository
  dellemc.openmanage.ome_firmware_catalog:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    catalog_name: "catalog_name"
    catalog_description: "catalog_description"
    repository_type: "HTTPS"
    source: "downloads.dell.com"
    source_path: "catalog"
    file_name: "catalog.gz"
    check_certificate: True

- name: Create a catalog from HTTP repository
  dellemc.openmanage.ome_firmware_catalog:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    catalog_name: "catalog_name"
    catalog_description: "catalog_description"
    repository_type: "HTTP"
    source: "downloads.dell.com"
    source_path: "catalog"
    file_name: "catalog.gz"

- name: Create a catalog using CIFS share
  dellemc.openmanage.ome_firmware_catalog:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    catalog_name: "catalog_name"
    catalog_description: "catalog_description"
    repository_type: "CIFS"
    source: "192.167.0.1"
    source_path: "cifs/R940"
    file_name: "catalog.gz"
    repository_username: "repository_username"
    repository_password: "repository_password"
    repository_domain: "repository_domain"

- name: Create a catalog using NFS share
  dellemc.openmanage.ome_firmware_catalog:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    catalog_name: "catalog_name"
    catalog_description: "catalog_description"
    repository_type: "NFS"
    source: "192.166.0.2"
    source_path: "/nfs/R940"
    file_name: "catalog.xml"

- name: Create a catalog using repository from Dell.com
  dellemc.openmanage.ome_firmware_catalog:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    catalog_name: "catalog_name"
    catalog_description: "catalog_description"
    repository_type: "DELL_ONLINE"
    check_certificate: True

- name: Modify a catalog using a repository from CIFS share
  dellemc.openmanage.ome_firmware_catalog:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    catalog_name: "catalog_name"
    catalog_description: "new catalog_description"
    repository_type: "CIFS"
    source: "192.167.0.2"
    source_path: "cifs/R941"
    file_name: "catalog1.gz"
    repository_username: "repository_username"
    repository_password: "repository_password"
    repository_domain: "repository_domain"

- name: Modify a catalog using a repository from Dell.com
  dellemc.openmanage.ome_firmware_catalog:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    catalog_id: 10
    new_catalog_name: "new_catalog_name"
    repository_type: "DELL_ONLINE"
    catalog_description: "catalog_description"

- name: Delete catalog using catalog name
  dellemc.openmanage.ome_firmware_catalog:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    state: absent
    catalog_name: ["catalog_name1", "catalog_name2"]

- name: Delete catalog using catalog id
  dellemc.openmanage.ome_firmware_catalog:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    state: absent
    catalog_id: [11, 34]
'''

RETURN = r'''
---
msg:
  description: Overall status of the firmware catalog operation.
  returned: always
  type: str
  sample: "Successfully triggered the job to create a catalog with Task ID : 10094"
catalog_status:
  description: Details of the catalog operation.
  returned: When I(state) is C(present)
  type: dict
  sample:  {
        "AssociatedBaselines": [],
        "BaseLocation": null,
        "BundlesCount": 0,
        "Filename": "catalog.gz",
        "Id": 0,
        "LastUpdated": null,
        "ManifestIdentifier": null,
        "ManifestVersion": null,
        "NextUpdate": null,
        "PredecessorIdentifier": null,
        "ReleaseDate": null,
        "ReleaseIdentifier": null,
        "Repository": {
            "CheckCertificate": true,
            "Description": "HTTPS Desc",
            "DomainName": null,
            "Id": null,
            "Name": "catalog4",
            "Password": null,
            "RepositoryType": "HTTPS",
            "Source": "company.com",
            "Username": null
        },
        "Schedule": null,
        "SourcePath": "catalog",
        "Status": null,
        "TaskId": 10094
    }
job_id:
  description: Job ID of the catalog task.
  returned: When catalog job is in a running state
  type: int
  sample: 10123
catalog_id:
  description: IDs of the deleted catalog.
  returned: When I(state) is C(absent)
  type: int
  sample: 10123
associated_baselines:
  description: IDs of the baselines associated with catalog.
  returned: When I(state) is C(absent)
  type: list
  elements: dict
  sample: [
    {
        "BaselineId": 24,
        "BaselineName": "new"
    },
    {
        "BaselineId": 25,
        "BaselineName": "c7"
    },
    {
        "BaselineId": 27,
        "BaselineName": "c4"
    }
  ]
error_info:
  type: dict
  description: Details of the http error.
  returned: on http error
  sample:  {
        "error": {
            "@Message.ExtendedInfo": [
                {
                    "Message": "Unable to create or update the catalog because a
                    repository with the same name already exists.",
                    "Resolution": "Enter a different name and retry the operation.",
                    "Severity": "Critical"
                }
            ],
            "code": "Base.1.0.GeneralError",
            "message": "A general error has occurred. See ExtendedInfo for more information."
        }
    }

'''

JOB_URI = "JobService/Jobs({TaskId})"
BASELINE_URI = "UpdateService/Baselines"
CATALOG_URI = "UpdateService/Catalogs"
CATALOG_URI_ID = "UpdateService/Catalogs({Id})"
DELETE_CATALOG_URI = "UpdateService/Actions/UpdateService.RemoveCatalogs"
CATALOG_JOB_RUNNING = "Catalog job '{name}' with ID {id} is running.Retry after job completion."
CHECK_MODE_CHANGE_FOUND_MSG = "Changes found to be applied."
CHECK_MODE_CHANGE_NOT_FOUND_MSG = "No changes found to be applied."
INVALID_CATALOG_ID = "Invalid catalog ID provided."
CATALOG_DEL_SUCCESS = "Successfully deleted the firmware catalog(s)."
CATALOG_BASELINE_ATTACHED = "Unable to delete the catalog as it is with baseline(s)."
CATALOG_EXISTS = "The catalog with the name '{new_name}' already exists in the system."
DELL_ONLINE_EXISTS = "Catalog with 'DELL_ONLINE' repository already exists with the name '{catalog_name}'."
NAMES_ERROR = "Only delete operations accept multiple catalog names or IDs."
CATALOG_ID_NOT_FOUND = "Catalog with ID '{catalog_id}' not found."
CATALOG_NAME_NOT_FOUND = "Catalog '{catalog_name}' not found."
CATALOG_UPDATED = "Successfully {operation} the firmware catalog."
JOB_POLL_INTERVAL = 10
SETTLING_TIME = 3

import json
import time
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


def check_existing_catalog(module, rest_obj, state, name=None):
    catalog_cfgs = []
    if name:
        catalog_id = None
        catalog_name = [name]
    else:
        catalog_id = module.params.get("catalog_id")
        catalog_name = module.params.get("catalog_name")
    resp = rest_obj.get_all_items_with_pagination(CATALOG_URI)
    catalogs_detail = resp.get("value")
    all_catalog = {}
    if state == "present":
        all_catalog = dict(
            [(each_catalog["Repository"]["Name"], each_catalog["Repository"]["RepositoryType"]) for each_catalog in
             catalogs_detail])
    for each_catalog in catalogs_detail:
        if catalog_name:
            if each_catalog['Repository']['Name'] in catalog_name:
                catalog_cfgs.append(each_catalog)
                if state == "present":
                    break
                continue
        if catalog_id:
            if each_catalog['Id'] in catalog_id:
                catalog_cfgs.append(each_catalog)
                if state == "present":
                    break
                continue
    return catalog_cfgs, all_catalog


def get_updated_catalog_info(module, rest_obj, catalog_resp):
    try:
        catalog, all_catalog = check_existing_catalog(module, rest_obj, "present", name=catalog_resp["Repository"]["Name"])
    except Exception:
        catalog = catalog_resp
    return catalog[0]


def exit_catalog(module, rest_obj, catalog_resp, operation, msg):
    if module.params.get("job_wait"):
        job_failed, job_message = rest_obj.job_tracking(
            catalog_resp.get('TaskId'), job_wait_sec=module.params["job_wait_timeout"], sleep_time=JOB_POLL_INTERVAL)
        catalog = get_updated_catalog_info(module, rest_obj, catalog_resp)
        if job_failed is True:
            module.fail_json(msg=job_message, catalog_status=catalog)
        catalog_resp = catalog
        msg = CATALOG_UPDATED.format(operation=operation)
    time.sleep(SETTLING_TIME)
    catalog = get_updated_catalog_info(module, rest_obj, catalog_resp)
    module.exit_json(msg=msg, catalog_status=catalog, changed=True)


def _get_catalog_payload(params, name):
    catalog_payload = {}
    repository_type = params.get("repository_type")
    if params.get("file_name") is not None:
        catalog_payload["Filename"] = params["file_name"]
    if params.get("source_path") is not None:
        catalog_payload["SourcePath"] = params["source_path"]
    repository_dict = {
        "Name": name,
        "Description": params.get("catalog_description"),
        "RepositoryType": repository_type,
        "Source": params.get("source"),
        "CheckCertificate": params.get("check_certificate"),
    }
    if repository_type != "DELL_ONLINE":
        repository_dict.update({"DomainName": params.get("repository_domain"),
                                "Username": params.get("repository_username"),
                                "Password": params.get("repository_password")
                                })
    if repository_type == "DELL_ONLINE" and not params.get("source"):
        repository_dict["Source"] = "downloads.dell.com"
    repository_payload = dict([(k, v) for k, v in repository_dict.items() if v is not None])
    if repository_payload:
        catalog_payload["Repository"] = repository_payload
    return catalog_payload


def validate_dell_online(all_catalog, module):
    """
    only one dell_online repository type catalog creation is possible from ome
    """
    catalog_name = module.params["catalog_name"][0]
    for name, repo_type in all_catalog.items():
        if repo_type == "DELL_ONLINE" and name != catalog_name:
            module.fail_json(
                msg=DELL_ONLINE_EXISTS.format(
                    catalog_name=name))


def create_catalog(module, rest_obj):
    if module.check_mode:
        module.exit_json(msg=CHECK_MODE_CHANGE_FOUND_MSG, changed=True)
    payload = _get_catalog_payload(module.params, module.params.get("catalog_name")[0])
    resp = rest_obj.invoke_request("POST", CATALOG_URI, data=payload)
    resp_data = resp.json_data
    job_id = resp_data.get("TaskId")
    msg = "Successfully triggered the job to create a catalog with Task Id : {0}".format(job_id)
    exit_catalog(module, rest_obj, resp_data, "created", msg)


def get_current_catalog_settings(current_payload):
    catalog_payload = {}
    if current_payload.get("Filename") is not None:
        catalog_payload["Filename"] = current_payload["Filename"]
    if current_payload.get("SourcePath") is not None:
        catalog_payload["SourcePath"] = current_payload["SourcePath"]
    repository_dict = {
        "Name": current_payload["Repository"].get("Name"),
        "Id": current_payload["Repository"].get("Id"),
        "Description": current_payload["Repository"].get("Description"),
        "RepositoryType": current_payload["Repository"].get("RepositoryType"),
        "Source": current_payload["Repository"].get("Source"),
        "DomainName": current_payload["Repository"].get("DomainName"),
        "Username": current_payload["Repository"].get("Username"),
        "Password": current_payload["Repository"].get("Password"),
        "CheckCertificate": current_payload["Repository"].get("CheckCertificate"),
    }
    repository_payload = dict([(k, v) for k, v in repository_dict.items() if v is not None])
    if repository_payload:
        catalog_payload["Repository"] = repository_payload
    return catalog_payload


def compare_payloads(modify_payload, current_payload):
    """
    :param modify_payload: payload created to update existing setting
    :param current_payload: already existing payload for specified baseline
    :return: bool - compare existing and requested setting values of baseline in case of modify operations
    if both are same return True
    """
    diff = False
    for key, val in modify_payload.items():
        if current_payload is None or current_payload.get(key) is None:
            return True
        elif isinstance(val, dict):
            if compare_payloads(val, current_payload.get(key)):
                return True
        elif val != current_payload.get(key):
            return True
    return diff


def modify_catalog(module, rest_obj, catalog_list, all_catalog):
    params = module.params
    catalog_id = catalog_list[0]["Id"]
    name = catalog_list[0]["Repository"]["Name"]
    modify_payload = _get_catalog_payload(module.params, name)
    new_catalog_name = params.get("new_catalog_name")
    if new_catalog_name:
        if new_catalog_name != name and new_catalog_name in all_catalog:
            module.fail_json(msg=CATALOG_EXISTS.format(new_name=new_catalog_name))
        modify_payload["Repository"]["Name"] = new_catalog_name
    catalog_payload = get_current_catalog_settings(catalog_list[0])
    if modify_payload.get("Repository") and \
            modify_payload.get("Repository").get("RepositoryType") and \
            modify_payload.get("Repository").get("RepositoryType") != catalog_payload["Repository"]["RepositoryType"]:
        module.fail_json(msg="Repository type cannot be changed to another repository type.")
    new_catalog_current_setting = catalog_payload.copy()
    repo_id = new_catalog_current_setting["Repository"]["Id"]
    del new_catalog_current_setting["Repository"]["Id"]
    diff = compare_payloads(modify_payload, new_catalog_current_setting)
    if module.check_mode and diff:
        module.exit_json(msg=CHECK_MODE_CHANGE_FOUND_MSG, changed=True)
    if not diff:
        module.exit_json(msg=CHECK_MODE_CHANGE_NOT_FOUND_MSG, changed=False)
    new_catalog_current_setting["Repository"].update(modify_payload["Repository"])
    catalog_payload.update(modify_payload)
    catalog_payload["Repository"] = new_catalog_current_setting["Repository"]
    catalog_payload["Repository"]["Id"] = repo_id
    catalog_payload["Id"] = catalog_id
    catalog_put_uri = CATALOG_URI_ID.format(Id=catalog_id)
    resp = rest_obj.invoke_request('PUT', catalog_put_uri, data=catalog_payload)
    resp_data = resp.json_data
    job_id = resp_data.get("TaskId")
    msg = "Successfully triggered the job to update a catalog with Task Id : {0}".format(job_id)
    exit_catalog(module, rest_obj, resp_data, "modified", msg)


def validate_delete_operation(rest_obj, module, catalog_list, delete_ids):
    associated_baselines = []
    for catalog in catalog_list:
        if catalog.get('AssociatedBaselines'):
            associated_baselines.append({"catalog_id": catalog["Id"],
                                         "associated_baselines": catalog.get("AssociatedBaselines")})
        if catalog.get('Status') != "Completed":
            resp = rest_obj.invoke_request("GET", JOB_URI.format(TaskId=catalog['TaskId']))
            job_data = resp.json_data
            if job_data['LastRunStatus']['Id'] == 2050:
                module.fail_json(msg=CATALOG_JOB_RUNNING.format(name=catalog["Name"], id=catalog["Id"]),
                                 job_id=catalog['TaskId'])
    if associated_baselines:
        module.fail_json(msg=CATALOG_BASELINE_ATTACHED, associated_baselines=associated_baselines)
    if module.check_mode and len(catalog_list) > 0:
        module.exit_json(msg=CHECK_MODE_CHANGE_FOUND_MSG, changed=True, catalog_id=delete_ids)
    if len(catalog_list) == 0:
        module.exit_json(msg=CHECK_MODE_CHANGE_NOT_FOUND_MSG, changed=False)


def delete_catalog(module, rest_obj, catalog_list):
    delete_ids = [d["Id"] for d in catalog_list]
    validate_delete_operation(rest_obj, module, catalog_list, delete_ids)
    delete_payload = {"CatalogIds": delete_ids}
    rest_obj.invoke_request('POST', DELETE_CATALOG_URI, data=delete_payload)
    module.exit_json(msg=CATALOG_DEL_SUCCESS, changed=True, catalog_id=delete_ids)


def validate_names(state, module):
    """
    The state present doest not supports more than one name/id
    """
    catalog_name = module.params.get("catalog_name", [])
    catalog_id = module.params.get("catalog_id", [])
    if state != "absent" and ((catalog_name and len(catalog_name) > 1) or (catalog_id and len(catalog_id) > 1)):
        module.fail_json(msg=NAMES_ERROR)


def perform_present_action(module, rest_obj, requested_catalog_list, all_catalog):
    if requested_catalog_list:
        modify_catalog(module, rest_obj, requested_catalog_list, all_catalog)
    else:
        if module.params.get('catalog_id'):
            module.fail_json(msg=INVALID_CATALOG_ID)
        repository_type = module.params.get("repository_type")
        if repository_type and repository_type == "DELL_ONLINE":
            validate_dell_online(all_catalog, module)
        create_catalog(module, rest_obj)


def main():
    module = AnsibleModule(
        argument_spec={
            "hostname": {"required": True, "type": 'str'},
            "username": {"required": True, "type": 'str'},
            "password": {"required": True, "type": 'str', "no_log": True},
            "port": {"required": False, "default": 443, "type": 'int'},
            "state": {"default": "present", "choices": ['present', 'absent']},
            "catalog_name": {"type": 'list', "elements": 'str'},
            "new_catalog_name": {"type": 'str'},
            "catalog_id": {"type": 'list', "elements": 'int'},
            "catalog_description": {"required": False, "type": 'str'},
            "source": {"required": False, "type": 'str'},
            "source_path": {"required": False, "type": 'str'},
            "file_name": {"required": False, "type": 'str'},
            "repository_type": {"required": False,
                                "choices": ["NFS", "CIFS", "HTTP", "HTTPS", "DELL_ONLINE"]},
            "repository_username": {"required": False, "type": 'str'},
            "repository_password": {"required": False, "type": 'str', "no_log": True},
            "repository_domain": {"required": False, "type": 'str'},
            "check_certificate": {"required": False, "type": 'bool', "default": False},
            "job_wait": {"type": 'bool', "default": True},
            "job_wait_timeout": {"type": 'int', "default": 600}
        },
        required_if=[
            ['state', 'present',
             ['repository_type'], False],
            ['state', 'present',
             ['new_catalog_name', 'catalog_description', 'catalog_name', 'catalog_id', 'source', 'source_path',
              'file_name', 'repository_type', 'repository_username', 'repository_password',
              'repository_domain', 'check_certificate'], True],
        ],
        mutually_exclusive=[('catalog_name', 'catalog_id')],
        required_one_of=[('catalog_name', 'catalog_id')],
        supports_check_mode=True)

    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            state = module.params['state']
            validate_names(state, module)
            requested_catalog_list, all_catalog = check_existing_catalog(module, rest_obj, state)
            if state == 'absent':
                delete_catalog(module, rest_obj, requested_catalog_list)
            else:
                perform_present_action(module, rest_obj, requested_catalog_list, all_catalog)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, TypeError, SSLError, ConnectionError, SSLValidationError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
