#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.0.0
# Copyright (C) 2019-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_template
short_description: Create, modify, deploy, delete, export, import and clone a template on OpenManage Enterprise
version_added: "2.0.0"
description: "This module creates, modifies, deploys, deletes, exports, imports and clones a template on
OpenManage Enterprise."
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  command:
    description:
      - C(create) creates a new template.
      - C(modify) modifies an existing template.
      - C(deploy) creates a template-deployment job.
      - C(delete) deletes an existing template.
      - C(export) exports an existing template.
      - C(import) creates a template from a specified configuration text in SCP XML format.
      - C(clone) creates a clone of a existing template.
    choices: [create, modify, deploy, delete, export, import, clone]
    default: create
    aliases: ['state']
    type: str
  template_id:
    description:
      - ID of the existing template.
      - This option is applicable when I(command) is C(modify), C(deploy), C(delete) and C(export).
      - This option is mutually exclusive with I(template_name).
    type: int
  template_name:
    description:
      - Name of the existing template.
      - This option is applicable when I(command) is C(modify), C(deploy), C(delete) and C(export).
      - This option is mutually exclusive with I(template_id).
    type: str
  device_id:
    description:
      - >-
        Specify the list of targeted device ID(s) when I(command) is C(deploy). When I (Command) is C(create),
        specify the ID of a single device.
      - Either I(device_id) or I(device_service_tag) is mandatory or both can be applicable.
    type: list
    elements: int
    default: []
  device_service_tag:
    description:
      - >-
        Specify the list of targeted device service tags when I (command) is C(deploy). When I(Command) is C(create),
        specify the service tag of a single device.
      - Either I(device_id) or I(device_service_tag) is mandatory or both can be applicable.
    type: list
    elements: str
    default: []
  template_view_type:
    description:
      - Select the type of view of the OME template.
      - This is applicable when I(command) is C(create),C(clone) and C(import).
    choices: [Deployment, Compliance, Inventory, Sample, None]
    type: str
    default: Deployment
  attributes:
    type: dict
    default: {}
    description:
      - >-
        Payload data for the template operations. All the variables in this option are added as payload for C(create),
        C(modify), C(deploy), C(import), and C(clone) operations. It takes the following attributes.
      - >-
        Attributes: List of dictionaries of attributes (if any) to be modified in the deployment template. This is
        applicable when I(command) is C(deploy) and C(modify.
      - >-
        Name: Name of the template. This is mandatory when I(command) is C(create), C(import), C(clone), and
        optional when I(command) is C(modify).
      - >-
        Description: Description for the template. This is applicable when I(command) is C(create) or C(modify).
      - >-
        Fqdds: This allows to create a template using components from a specified reference server. One or more, of the
        following values must be specified in a comma-separated string: iDRAC, System, BIOS, NIC, LifeCycleController,
        RAID, and EventFilters. If none of the values are specified, the default value 'All' is selected.
        This is applicable when I (command) is C(create).
      - >-
        Options: Options to control device shutdown or end power state post template deployment. This is applicable
        for C(deploy) operation.
      - >-
        Schedule: Provides options to schedule the deployment task immediately, or at a specified time. This is
        applicable when I(command) is C(deploy).
      - >-
        NetworkBootIsoModel: Payload to specify the ISO deployment details. This is applicable when I(command) is
        C(deploy).
      - >-
        Content: The XML content of template. This is applicable when I(command) is C(import).
      - >-
        Type: Template type ID, indicating the type of device for which configuration is supported, such as chassis
        and servers. This is applicable when I(command) is C(import).
      - >-
        TypeId: Template type ID, indicating the type of device for which configuration is supported, such as chassis
        and servers. This is applicable when I(command) is C(create).
      - >-
        Refer OpenManage Enterprise API Reference Guide for more details.
requirements:
    - "python >= 2.7.5"
author: "Jagadeesh N V (@jagadeeshnv)"
notes:
    - Run this module from a system that has direct access to DellEMC OpenManage Enterprise.
    - This module does not support C(check_mode).
'''

EXAMPLES = r'''
---
- name: Create a template from a reference device
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    device_id: 25123
    attributes:
      Name: "New Template"
      Description: "New Template description"

- name: Modify template name, description, and attribute value
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    command: "modify"
    template_id: 12
    attributes:
      Name: "New Custom Template"
      Description: "Custom Template Description"
      # Attributes to be modified in the template.
      # For information on any attribute id, use API /TemplateService/Templates(Id)/Views(Id)/AttributeViewDetails
      # This section is optional
      Attributes:
        - Id: 1234
          Value: "Test Attribute"
          IsIgnored: false

- name: Deploy template on multiple devices
  dellemc.openmanage.ome_template:
    hostname:  "192.168.0.1"
    username: "username"
    password: "password"
    command: "deploy"
    template_id: 12
    device_id:
      - 12765
      - 10173
    device_service_tag:
      - 'SVTG123'
      - 'SVTG456'

- name: Deploy template on multiple devices along with the attributes values to be modified on the target devices
  dellemc.openmanage.ome_template:
    hostname:  "192.168.0.1"
    username: "username"
    password: "password"
    command: "deploy"
    template_id: 12
    device_id:
      - 12765
      - 10173
    device_service_tag:
      - 'SVTG123'
    attributes:
      # Device specific attributes to be modified during deployment.
      # For information on any attribute id, use API /TemplateService/Templates(Id)/Views(Id)/AttributeViewDetails
      # This section is optional
      Attributes:
        # specific device where attribute to be modified at deployment run-time.
        # The DeviceId should be mentioned above in the 'device_id' section.
        # Service tags not allowed.
        - DeviceId: 12765
          Attributes:
            - Id : 15645
              Value : "0.0.0.0"
              IsIgnored : false
        - DeviceId: 10173
          Attributes:
            - Id : 18968,
              Value : "hostname-1"
              IsIgnored : false

- name: Deploy template and Operating System (OS) on multiple devices
  dellemc.openmanage.ome_template:
    hostname:  "192.168.0.1"
    username: "username"
    password: "password"
    command: "deploy"
    template_id: 12
    device_id:
      - 12765
    device_service_tag:
      - 'SVTG123'
    attributes:
      # Include this to install OS on the devices.
      # This section is optional
      NetworkBootIsoModel:
        BootToNetwork: true
        ShareType: "NFS"
        IsoTimeout: 1 # allowable values(1,2,4,8,16) in hours
        IsoPath: "/home/iso_path/filename.iso"
        ShareDetail:
          IpAddress: "192.168.0.2"
          ShareName: "sharename"
          User: "share_user"
          Password: "share_password"
      Options:
        EndHostPowerState: 1
        ShutdownType: 0
        TimeToWaitBeforeShutdown: 300
      Schedule:
        RunLater: true
        RunNow: false

- name: "Deploy template on multiple devices and changes the device-level attributes. After the template is deployed,
install OS using its image"
  dellemc.openmanage.ome_template:
    hostname:  "192.168.0.1"
    username: "username"
    password: "password"
    command: "deploy"
    template_id: 12
    device_id:
      - 12765
      - 10173
    device_service_tag:
      - 'SVTG123'
      - 'SVTG456'
    attributes:
      Attributes:
        - DeviceId: 12765
          Attributes:
            - Id : 15645
              Value : "0.0.0.0"
              IsIgnored : false
        - DeviceId: 10173
          Attributes:
            - Id : 18968,
              Value : "hostname-1"
              IsIgnored : false
      NetworkBootIsoModel:
        BootToNetwork: true
        ShareType: "NFS"
        IsoTimeout: 1 # allowable values(1,2,4,8,16) in hours
        IsoPath: "/home/iso_path/filename.iso"
        ShareDetail:
          IpAddress: "192.168.0.2"
          ShareName: "sharename"
          User: "share_user"
          Password: "share_password"
      Options:
        EndHostPowerState: 1
        ShutdownType: 0
        TimeToWaitBeforeShutdown: 300
      Schedule:
        RunLater: true
        RunNow: false

- name: Delete template
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    command: "delete"
    template_id: 12

- name: Export a template
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    command: "export"
    template_id: 12

# Start of example to export template to a local xml file
- name: Export template to a local xml file
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    command: "export"
    template_name: "my_template"
  register: result
- name: Save template into a file
  ansible.builtin.copy:
    content: "{{ result.Content}}"
    dest: "/path/to/exported_template.xml"
# End of example to export template to a local xml file

- name: Clone a template
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    command: "clone"
    template_id: 12
    attributes:
      Name: "New Cloned Template Name"

- name: Import template from XML content
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    command: "import"
    attributes:
      Name: "Imported Template Name"
      # Template Type from TemplateService/TemplateTypes
      Type: 2
      # xml string content
      Content: "<SystemConfiguration Model=\"PowerEdge R940\" ServiceTag=\"SVCTAG1\"
      TimeStamp=\"Tue Sep 24 09:20:57.872551 2019\">\n<Component FQDD=\"AHCI.Slot.6-1\">\n<Attribute
      Name=\"RAIDresetConfig\">True</Attribute>\n<Attribute Name=\"RAIDforeignConfig\">Clear</Attribute>\n
      </Component>\n<Component FQDD=\"Disk.Direct.0-0:AHCI.Slot.6-1\">\n<Attribute Name=\"RAIDPDState\">Ready
      </Attribute>\n<Attribute Name=\"RAIDHotSpareStatus\">No</Attribute>\n</Component>\n
      <Component FQDD=\"Disk.Direct.1-1:AHCI.Slot.6-1\">\n<Attribute Name=\"RAIDPDState\">Ready</Attribute>\n
      <Attribute Name=\"RAIDHotSpareStatus\">No</Attribute>\n</Component>\n</SystemConfiguration>\n"

- name: Import template from local XML file
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    command: "import"
    attributes:
      Name: "Imported Template Name"
      Type: 2
      Content: "{{ lookup('ansible.builtin.file.', '/path/to/xmlfile') }}"
'''

RETURN = r'''
---
msg:
  description: Overall status of the template operation.
  returned: always
  type: str
  sample: "Successfully created a template with ID 23"
return_id:
  description: ID of the template for C(create), C(modify), C(import) and C(clone) or task created in case of C(deploy).
  returned: success, when I(command) is C(create), C(modify), C(import), C(clone) and C(deploy)
  type: int
  sample: 12
TemplateId:
  description: ID of the template for C(export).
  returned: success, when I(command) is C(export)
  type: int
  sample: 13
Content:
  description: XML content of the exported template. This content can be written to a xml file.
  returned: success, when I(command) is C(export)
  type: str
  sample: "<SystemConfiguration Model=\"PowerEdge R940\" ServiceTag=\"DG22TR2\" TimeStamp=\"Tue Sep 24 09:20:57.872551
     2019\">\n<Component FQDD=\"AHCI.Slot.6-1\">\n<Attribute Name=\"RAIDresetConfig\">True</Attribute>\n<Attribute
     Name=\"RAIDforeignConfig\">Clear</Attribute>\n</Component>\n<Component FQDD=\"Disk.Direct.0-0:AHCI.Slot.6-1\">\n
     <Attribute Name=\"RAIDPDState\">Ready</Attribute>\n<Attribute Name=\"RAIDHotSpareStatus\">No</Attribute>\n
     </Component>\n<Component FQDD=\"Disk.Direct.1-1:AHCI.Slot.6-1\">\n<Attribute Name=\"RAIDPDState\">Ready
     </Attribute>\n<Attribute Name=\"RAIDHotSpareStatus\">No</Attribute>\n</Component>\n</SystemConfiguration>\n"
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
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


TEMPLATES_URI = "TemplateService/Templates"
TEMPLATE_PATH = "TemplateService/Templates({template_id})"
TEMPALTE_ACTION = "TemplateService/Actions/TemplateService.{op}"
DEVICE_URI = "DeviceService/Devices"


def get_device_ids(module, rest_obj):
    """Getting the list of device ids filtered from the device inventory."""
    device_id = list(map(str, module.params.get('device_id')))
    for devid in device_id:
        if not devid.isdigit():
            fail_module(module, msg="Invalid device id {0} found. Please provide a valid number".format(devid))
    service_tags = module.params.get('device_service_tag')
    if not service_tags:
        return list(set(device_id))
    device_list = rest_obj.get_all_report_details(DEVICE_URI)["report_list"]
    if device_list:
        device_resp = dict([(device.get('DeviceServiceTag'), str(device.get('Id'))) for device in device_list])
        device_tags = list(map(str, service_tags))
        invalid_tags = []
        for tag in device_tags:
            if device_resp.get(tag):
                device_id.append(device_resp.get(tag))
            else:
                invalid_tags.append(tag)
        if invalid_tags:
            fail_module(module, msg="Unable to complete the operation because the entered target service"
                                    " tag(s) '{0}' are invalid.".format(",".join(set(invalid_tags))))
    else:
        fail_module(module, msg="Failed to fetch the device ids.")
    invalid_ids = set(device_id) - set(device_resp.values())
    if invalid_ids:
        fail_module(module, msg="Unable to complete the operation because the entered target device"
                                " id(s) '{0}' are invalid.".format(",".join(list(map(str, set(invalid_ids))))))
    return list(map(int, set(device_id)))


def get_view_id(rest_obj, viewstr):
    resp = rest_obj.invoke_request('GET', "TemplateService/TemplateViewTypes")
    if resp.success and resp.json_data.get('value'):
        tlist = resp.json_data.get('value', [])
        for xtype in tlist:
            if xtype.get('Description', "") == viewstr:
                return xtype.get('Id')
    viewmap = {"Deployment": 2, "Compliance": 1, "Inventory": 3, "Sample": 4, "None": 0}
    return viewmap.get(viewstr)


def get_type_id_valid(rest_obj, typeid):
    resp = rest_obj.invoke_request('GET', "TemplateService/TemplateTypes")
    if resp.success and resp.json_data.get('value'):
        tlist = resp.json_data.get('value', [])
        for xtype in tlist:
            if xtype.get('Id') == typeid:  # use Name if str is passed
                return True
    return False


def get_create_payload(module_params, deviceid, view_id):
    create_payload = {"Fqdds": "All",
                      "ViewTypeId": view_id}
    if isinstance(module_params.get("attributes"), dict):
        create_payload.update(module_params.get("attributes"))
    create_payload["SourceDeviceId"] = int(deviceid)
    return create_payload


def get_modify_payload(module_params, template_id, template_dict):
    modify_payload = {}
    if isinstance(module_params.get("attributes"), dict):
        modify_payload.update(module_params.get("attributes"))
    modify_payload['Id'] = template_id
    # Update with old template values
    if not modify_payload.get("Name"):
        modify_payload["Name"] = template_dict["Name"]
    if not modify_payload.get("Description"):
        modify_payload["Description"] = template_dict["Description"]
    return modify_payload


def get_deploy_payload(module_params, deviceidlist, template_id):
    deploy_payload = {}
    if isinstance(module_params.get("attributes"), dict):
        deploy_payload.update(module_params.get("attributes"))
    deploy_payload["Id"] = template_id
    deploy_payload["TargetIds"] = deviceidlist
    return deploy_payload


def get_import_payload(module, rest_obj, view_id):
    attrib_dict = module.params.get("attributes").copy()
    import_payload = {}
    import_payload["Name"] = attrib_dict.pop("Name")
    import_payload["ViewTypeId"] = view_id
    import_payload["Type"] = 2
    typeid = attrib_dict.get("Type")
    if typeid:
        if get_type_id_valid(rest_obj, typeid):
            import_payload["Type"] = typeid   # Type is mandatory for import
        else:
            fail_module(module, msg="Type provided for 'import' operation is invalid")
    import_payload["Content"] = attrib_dict.pop("Content")
    if isinstance(attrib_dict, dict):
        import_payload.update(attrib_dict)
    return import_payload


def get_clone_payload(module_params, template_id, view_id):
    attrib_dict = module_params.get("attributes").copy()
    clone_payload = {}
    clone_payload["SourceTemplateId"] = template_id
    clone_payload["NewTemplateName"] = attrib_dict.pop("Name")
    clone_payload["ViewTypeId"] = view_id
    if isinstance(attrib_dict, dict):
        clone_payload.update(attrib_dict)
    return clone_payload


def get_template_by_id(module, rest_obj, template_id):
    path = TEMPLATE_PATH.format(template_id=template_id)
    template_req = rest_obj.invoke_request("GET", path)
    if template_req.success:
        return template_req.json_data
    else:
        fail_module(module, msg="Unable to complete the operation because the"
                                " requested template is not present.")


def get_template_by_name(template_name, module, rest_obj):
    """Filter out specific template based on name, and it returns template_id.

    :param template_name: string
    :param module: dictionary
    :param rest_obj: object
    :return: template_id: integer
    """
    template_id = None
    template = None
    template_path = TEMPLATES_URI
    query_param = {"$filter": "Name eq '{0}'".format(template_name)}
    template_req = rest_obj.invoke_request("GET", template_path, query_param=query_param)
    for each in template_req.json_data.get('value'):
        if each['Name'] == template_name:
            template_id = each['Id']
            template = each
            break
    else:
        fail_module(module, msg="Unable to complete the operation because the"
                                " requested template with name {0} is not present.".format(template_name))
    return template, template_id


def _get_resource_parameters(module, rest_obj):
    command = module.params.get("command")
    rest_method = 'POST'
    payload = {}
    template_id = module.params.get("template_id")
    template_name = module.params.get("template_name")
    if template_name:
        template, template_id = get_template_by_name(template_name, module, rest_obj)
    if command not in ["import", "create"] and template_id is None:
        fail_module(module, msg="Enter a valid template_name or template_id")
    if command == "create":
        devid_list = get_device_ids(module, rest_obj)
        if len(devid_list) != 1:
            fail_module(module, msg="Create template requires only one reference device")
        view_id = get_view_id(rest_obj, module.params['template_view_type'])
        payload = get_create_payload(module.params, devid_list[0], view_id)
        path = TEMPLATES_URI
    elif command == "modify":
        path = TEMPLATE_PATH.format(template_id=template_id)
        template_dict = get_template_by_id(module, rest_obj, template_id)
        payload = get_modify_payload(module.params, template_id, template_dict)
        rest_method = 'PUT'
    elif command == "delete":
        path = TEMPLATE_PATH.format(template_id=template_id)
        rest_method = 'DELETE'
    elif command == "export":
        path = TEMPALTE_ACTION.format(op="Export")
        payload = {'TemplateId': template_id}
    elif command == "deploy":
        devid_list = get_device_ids(module, rest_obj)
        path = TEMPALTE_ACTION.format(op="Deploy")
        payload = get_deploy_payload(module.params, devid_list, template_id)
    elif command == "clone":
        view_id = get_view_id(rest_obj, module.params['template_view_type'])
        path = TEMPALTE_ACTION.format(op="Clone")
        payload = get_clone_payload(module.params, template_id, view_id)
    else:
        view_id = get_view_id(rest_obj, module.params['template_view_type'])
        path = TEMPALTE_ACTION.format(op="Import")
        payload = get_import_payload(module, rest_obj, view_id)
    return path, payload, rest_method


def _validate_inputs(module):
    """validates input parameters"""
    command = module.params.get("command")
    if command in ["create", "deploy"]:
        dev_id = module.params["device_id"]
        dev_st = module.params["device_service_tag"]
        if None in dev_id or None in dev_st:
            fail_module(module, msg="Argument device_id or device_service_tag has null values")
    attrib_dict = {}
    if module.params.get("attributes"):
        attrib_dict = module.params.get("attributes")
    if command in ["import", "clone", "create"]:
        if not attrib_dict.get("Name"):
            fail_module(module, msg="Argument 'Name' required in attributes for {0} operation".format(command))
    if command == "import":
        if not attrib_dict.get("Content"):
            fail_module(module, msg="Argument 'Content' required in attributes for {0} operation".format(command))


def password_no_log(attributes):
    if isinstance(attributes, dict):
        netdict = attributes.get("NetworkBootIsoModel")
        if isinstance(netdict, dict):
            sharedet = netdict.get("ShareDetail")
            if isinstance(sharedet, dict) and 'Password' in sharedet:
                sharedet['Password'] = "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"


def fail_module(module, **failmsg):
    password_no_log(module.params.get("attributes"))
    module.fail_json(**failmsg)


def exit_module(module, response):
    password_no_log(module.params.get("attributes"))
    resp = None
    my_change = True
    command = module.params.get('command')
    result = {}
    if command in ["create", "modify", "deploy", "import", "clone"]:
        result["return_id"] = response.json_data
        resp = result["return_id"]
        if command == 'deploy' and result["return_id"] == 0:
            result["failed"] = True
            command = 'deploy_fail'
            my_change = False
    if command == 'export':
        my_change = False
        result = response.json_data
    msg_dict = {'create': "Successfully created a template with ID {0}".format(resp),
                'modify': "Successfully modified the template with ID {0}".format(resp),
                'deploy': "Successfully created the template-deployment job with ID {0}".format(resp),
                'deploy_fail': 'Failed to deploy template.',
                'delete': "Deleted successfully",
                'export': "Exported successfully",
                'import': "Imported successfully",
                'clone': "Cloned successfully"}
    module.exit_json(msg=msg_dict.get(command), changed=my_change, **result)


def main():
    module = AnsibleModule(
        argument_spec={
            "hostname": {"required": True, "type": 'str'},
            "username": {"required": True, "type": 'str'},
            "password": {"required": True, "type": 'str', "no_log": True},
            "port": {"required": False, "default": 443, "type": 'int'},
            "command": {"required": False, "default": "create", "aliases": ['state'],
                        "choices": ['create', 'modify', 'deploy', 'delete', 'export', 'import', 'clone']},
            "template_id": {"required": False, "type": 'int'},
            "template_name": {"required": False, "type": 'str'},
            "template_view_type": {"required": False, "default": 'Deployment',
                                   "choices": ['Deployment', 'Compliance', 'Inventory', 'Sample', 'None']},
            "device_id": {"required": False, "type": 'list', "default": [], "elements": 'int'},
            "device_service_tag": {"required": False, "type": 'list', "default": [], "elements": 'str'},
            "attributes": {"required": False, "type": 'dict'},
        },
        required_if=[
            ['command', 'create', ['attributes']],
            ['command', 'modify', ['attributes']],
            ['command', 'import', ['attributes']],
            ['command', 'clone', ['attributes']]
        ],
        mutually_exclusive=[["template_id", "template_name"]],
        supports_check_mode=False)

    try:
        _validate_inputs(module)
        with RestOME(module.params, req_session=True) as rest_obj:
            path, payload, rest_method = _get_resource_parameters(module, rest_obj)
            resp = rest_obj.invoke_request(rest_method, path, data=payload)
            if resp.success:
                exit_module(module, resp)
    except HTTPError as err:
        fail_module(module, msg=str(err), error_info=json.load(err))
    except URLError as err:
        password_no_log(module.params.get("attributes"))
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, KeyError) as err:
        fail_module(module, msg=str(err))


if __name__ == '__main__':
    main()
