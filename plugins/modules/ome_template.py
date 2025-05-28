#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2019-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

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
      - This option is applicable when I(command) is C(modify), C(deploy), C(delete), C(clone) and C(export).
      - This option is mutually exclusive with I(template_name).
    type: int
  template_name:
    description:
      - Name of the existing template.
      - This option is applicable when I(command) is C(modify), C(deploy), C(delete), C(clone) and C(export).
      - This option is mutually exclusive with I(template_id).
    type: str
  device_id:
    description:
      - >-
        Specify the list of targeted device ID(s) when I(command) is C(deploy). When I (command) is C(create),
        specify the ID of a single device.
      - Either I(device_id) or I(device_service_tag) is mandatory or both can be applicable.
    type: list
    elements: int
    default: []
  device_service_tag:
    description:
      - >-
        Specify the list of targeted device service tags when I (command) is C(deploy). When I(command) is C(create),
        specify the service tag of a single device.
      - Either I(device_id) or I(device_service_tag) is mandatory or both can be applicable.
    type: list
    elements: str
    default: []
  device_group_names:
    description:
      - Specify the list of groups when I (command) is C(deploy).
      - Provide at least one of the mandatory options I(device_id), I(device_service_tag), or I(device_group_names).
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
    description:
      - >-
        Payload data for the template operations. All the variables in this option are added as payload for C(create),
        C(modify), C(deploy), C(import), and C(clone) operations. It takes the following attributes.
      - >-
        Attributes: List of dictionaries of attributes (if any) to be modified in the deployment template. This is
        applicable when I(command) is C(deploy) and C(modify). Use the I(Id) If the attribute Id is available.
        If not, use the comma separated I (DisplayName). For more details about using the I(DisplayName),
        see the example provided.
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
  job_wait:
    type: bool
    description:
      - Provides the option to wait for job completion.
      - This option is applicable when I(command) is C(create), or C(deploy).
    default: true
  job_wait_timeout:
    type: int
    description:
      - The maximum wait time of I(job_wait) in seconds. The job is tracked only for this duration.
      - This option is applicable when I(job_wait) is C(true).
    default: 1200
requirements:
    - "python >= 3.9.6"
author:
    - "Jagadeesh N V (@jagadeeshnv)"
    - "Husniya Hameed (@husniya_hameed)"
    - "Kritika Bhateja (@Kritika-Bhateja)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Create a template from a reference device
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_id: 25123
    attributes:
      Name: "New Template"
      Description: "New Template description"

- name: Modify template name, description, and attribute value
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
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

- name: Modify template name, description, and attribute using detailed view
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: "modify"
    template_id: 12
    attributes:
      Name: "New Custom Template"
      Description: "Custom Template Description"
      Attributes:
        # Enter the comma separated string as appearing in the Detailed view on GUI
        # NIC -> NIC.Integrated.1-1-1 -> NIC Configuration -> Wake On LAN1
        - DisplayName: 'NIC, NIC.Integrated.1-1-1, NIC Configuration, Wake On LAN'
          Value: Enabled
          IsIgnored: false
        # System -> LCD Configuration -> LCD 1 User Defined String for LCD
        - DisplayName: 'System, LCD Configuration, LCD 1 User Defined String for LCD'
          Value: LCD str by OMAM
          IsIgnored: false

- name: Deploy template on multiple devices
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: "deploy"
    template_id: 12
    device_id:
      - 12765
      - 10173
    device_service_tag:
      - 'SVTG123'
      - 'SVTG456'

- name: Deploy template on groups
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: "deploy"
    template_id: 12
    device_group_names:
      - server_group_1
      - server_group_2

- name: Deploy template on multiple devices along with the attributes values to be modified on the target devices
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
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
            - Id: 15645
              Value: "0.0.0.0"
              IsIgnored: false
        - DeviceId: 10173
          Attributes:
            - Id: 18968,
              Value: "hostname-1"
              IsIgnored: false

- name: Deploy template and Operating System (OS) on multiple devices
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
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
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
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
            - Id: 15645
              Value: "0.0.0.0"
              IsIgnored: false
        - DeviceId: 10173
          Attributes:
            - Id: 18968,
              Value: "hostname-1"
              IsIgnored: false
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
    ca_path: "/path/to/ca_cert.pem"
    command: "delete"
    template_id: 12

- name: Export a template
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: "export"
    template_id: 12

# Start of example to export template to a local xml file
- name: Export template to a local xml file
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
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
    ca_path: "/path/to/ca_cert.pem"
    command: "clone"
    template_id: 12
    attributes:
      Name: "New Cloned Template Name"

- name: Import template from XML content
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
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
    ca_path: "/path/to/ca_cert.pem"
    command: "import"
    attributes:
      Name: "Imported Template Name"
      Type: 2
      Content: "{{ lookup('ansible.builtin.file', '/path/to/xmlfile') }}"

- name: "Deploy template and Operating System (OS) on multiple devices."
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
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
        ShareType: "CIFS"
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

- name: Create a compliance template from reference device
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: "create"
    device_service_tag:
      - "SVTG123"
    template_view_type: "Compliance"
    attributes:
      Name: "Configuration Compliance"
      Description: "Configuration Compliance Template"
      Fqdds: "BIOS"

- name: Import a compliance template from XML file
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: "import"
    template_view_type: "Compliance"
    attributes:
      Name: "Configuration Compliance"
      Content: "{{ lookup('ansible.builtin.file', './test.xml') }}"
      Type: 2

- name: Create a template from a reference device with Job wait as false
  dellemc.openmanage.ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_id: 25123
    attributes:
      Name: "New Template"
      Description: "New Template description"
      Fqdds: iDRAC,BIOS,
    job_wait: false
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
  sample: "<SystemConfiguration Model=\"PowerEdge R940\" ServiceTag=\"DEFG123\" TimeStamp=\"Tue Sep 24 09:20:57.872551
     2019\">\n<Component FQDD=\"AHCI.Slot.6-1\">\n<Attribute Name=\"RAIDresetConfig\">True</Attribute>\n<Attribute
     Name=\"RAIDforeignConfig\">Clear</Attribute>\n</Component>\n<Component FQDD=\"Disk.Direct.0-0:AHCI.Slot.6-1\">
     \n<Attribute Name=\"RAIDPDState\">Ready</Attribute>\n<Attribute Name=\"RAIDHotSpareStatus\">No</Attribute>
     \n</Component>\n<Component FQDD=\"Disk.Direct.1-1:AHCI.Slot.6-1\">\n<Attribute Name=\"RAIDPDState\">Ready
     </Attribute>\n<Attribute Name=\"RAIDHotSpareStatus\">No</Attribute>\n</Component>\n</SystemConfiguration>"
devices_assigned:
  description: Mapping of devices with the templates already deployed on them.
  returned: I(command) is C(deploy)
  type: dict
  sample: {
        "10362": 28,
        "10312": 23
  }
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
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import apply_diff_key, job_tracking


TEMPLATES_URI = "TemplateService/Templates"
TEMPLATE_PATH = "TemplateService/Templates({template_id})"
TEMPLATE_ACTION = "TemplateService/Actions/TemplateService.{op}"
TEMPLATE_ATTRIBUTES = "TemplateService/Templates({template_id})/AttributeDetails"
DEVICE_URI = "DeviceService/Devices"
GROUP_URI = "GroupService/Groups"
PROFILE_URI = "ProfileService/Profiles"
JOB_URI = "JobService/Jobs({job_id})"
SEPRTR = ','
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
TEMPLATE_NAME_EXISTS = "Template with name '{name}' already exists."
DEPLOY_DEV_ASSIGNED = "The device(s) '{dev}' have been assigned the template(s) '{temp}' " \
                      "respectively. Please unassign the profiles from the devices."
MSG_DICT = {'create_when_job_wait_true': "Successfully created a template with ID {0}",
            'create_when_job_wait_false': "Successfully submitted a template creation with job ID {0}",
            'modify': "Successfully modified the template with ID {0}",
            'deploy_when_job_wait_false': "Successfully submitted a template deployment with job ID {0}",
            'deploy_when_job_wait_true': "Successfully deployed the template with ID {0}",
            'fail': 'Failed to {command} template.',
            'delete': "Deleted successfully",
            'export': "Exported successfully",
            'import': "Imported successfully",
            'clone': "Cloned successfully",
            'timed_out': "Template operation is in progress. Task excited after 'job_wait_timeout'."}


def get_profiles(rest_obj):
    try:
        resp = rest_obj.invoke_request('GET', PROFILE_URI)
        profile_list = resp.json_data.get("value")
    except Exception:
        profile_list = []
    return profile_list


def get_group_devices_all(rest_obj, uri):
    total_items = []
    next_link = uri
    while next_link:
        resp = rest_obj.invoke_request('GET', next_link)
        data = resp.json_data
        total_items.extend(data.get("value", []))
        next_link_list = str(data.get('@odata.nextLink', '')).split('/api')
        next_link = next_link_list[-1]
    return total_items


def get_group(rest_obj, module, group_name):
    query_param = {"$filter": "Name eq '{0}'".format(group_name)}
    group_req = rest_obj.invoke_request("GET", GROUP_URI, query_param=query_param)
    for grp in group_req.json_data.get('value'):
        if grp['Name'] == group_name:
            return grp
    module.fail_json(msg="Group name '{0}' is invalid. Please provide a valid group name.".format(group_name))


def get_group_details(rest_obj, module):
    group_name_list = module.params.get('device_group_names')
    device_ids = []
    for group_name in group_name_list:
        group = get_group(rest_obj, module, group_name)
        group_uri = GROUP_URI + "({0})/Devices".format(group['Id'])
        group_device_list = get_group_devices_all(rest_obj, group_uri)
        device_ids.extend([dev['Id'] for dev in group_device_list])
    return device_ids


def get_device_ids(module, rest_obj):
    """Getting the list of device ids filtered from the device inventory."""
    target_ids = []
    if module.params.get('device_service_tag') or module.params.get('device_id'):
        # device_list = get_group_devices_all(rest_obj, DEVICE_URI)
        device_list = rest_obj.get_all_report_details(DEVICE_URI)['report_list']
        device_tag_id_map = dict([(device.get('DeviceServiceTag'), device.get('Id')) for device in device_list])
        device_id = module.params.get('device_id')
        invalid_ids = set(device_id) - set(device_tag_id_map.values())
        if invalid_ids:
            fail_module(module, msg="Unable to complete the operation because the entered target device"
                                    " id(s) '{0}' are invalid.".format(",".join(list(map(str, set(invalid_ids))))))
        target_ids.extend(device_id)
        service_tags = module.params.get('device_service_tag')
        invalid_tags = set(service_tags) - set(device_tag_id_map.keys())
        if invalid_tags:
            fail_module(module, msg="Unable to complete the operation because the entered target service"
                                    " tag(s) '{0}' are invalid.".format(",".join(set(invalid_tags))))
        for tag in service_tags:  # append ids for service tags
            target_ids.append(device_tag_id_map.get(tag))
    if module.params.get('device_group_names'):
        target_ids.extend(get_group_details(rest_obj, module))
    return list(set(target_ids))  # set to eliminate duplicates


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
            if xtype.get('Id') == typeid:
                return True
    return False


def get_template_by_name(template_name, module, rest_obj):
    template = {}
    template_path = TEMPLATES_URI
    query_param = {"$filter": "Name eq '{0}'".format(template_name)}
    template_req = rest_obj.invoke_request("GET", template_path, query_param=query_param)
    for each in template_req.json_data.get('value'):
        if each['Name'] == template_name:
            template = each
            break
    return template


def recurse_subattr_list(subgroup, prefix, attr_detailed, attr_map, adv_list):
    if isinstance(subgroup, list):
        for each_sub in subgroup:
            nprfx = "{0}{1}{2}".format(prefix, SEPRTR, each_sub.get("DisplayName"))
            if each_sub.get("SubAttributeGroups"):
                recurse_subattr_list(each_sub.get("SubAttributeGroups"), nprfx, attr_detailed, attr_map, adv_list)
            else:
                for attr in each_sub.get('Attributes'):
                    attr['prefix'] = nprfx
                    # case sensitive, remove whitespaces for optim
                    constr = "{0}{1}{2}".format(nprfx, SEPRTR, attr['DisplayName'])
                    if constr in adv_list:
                        attr_detailed[constr] = attr['AttributeId']
                    attr_map[attr['AttributeId']] = attr


def get_subattr_all(attr_dtls, adv_list):
    attr_detailed = {}
    attr_map = {}
    for each in attr_dtls:
        recurse_subattr_list(each.get('SubAttributeGroups'), each.get('DisplayName'), attr_detailed, attr_map, adv_list)
    return attr_detailed, attr_map


def attributes_check(module, rest_obj, inp_attr, template_id):
    diff = 0
    try:
        resp = rest_obj.invoke_request("GET", TEMPLATE_ATTRIBUTES.format(template_id=template_id))
        attr_dtls = resp.json_data
        disp_adv_list = inp_attr.get("Attributes", {})
        adv_list = []
        for attr in disp_adv_list:
            if attr.get("DisplayName"):
                split_k = str(attr.get("DisplayName")).split(SEPRTR)
                trimmed = map(str.strip, split_k)
                n_k = SEPRTR.join(trimmed)
                adv_list.append(n_k)
        attr_detailed, attr_map = get_subattr_all(attr_dtls.get('AttributeGroups'), adv_list)
        payload_attr = inp_attr.get("Attributes", [])
        rem_attrs = []
        for attr in payload_attr:
            if attr.get("DisplayName"):
                split_k = str(attr.get("DisplayName")).split(SEPRTR)
                trimmed = map(str.strip, split_k)
                n_k = SEPRTR.join(trimmed)
                id = attr_detailed.get(n_k, "")
                attr['Id'] = id
                attr.pop("DisplayName", None)
            else:
                id = attr.get('Id')
            if id:
                ex_val = attr_map.get(id, {})
                if not ex_val:
                    rem_attrs.append(attr)
                    continue
                if attr.get('Value') != ex_val.get("Value") or attr.get('IsIgnored') != ex_val.get("IsIgnored"):
                    diff = diff + 1
        for rem in rem_attrs:
            payload_attr.remove(rem)
        # module.exit_json(attr_detailed=attr_detailed, inp_attr=disp_adv_list, payload_attr=payload_attr, adv_list=adv_list)
    except Exception:
        diff = 1
    return diff


def get_create_payload(module, rest_obj, deviceid, view_id):
    create_payload = {"Fqdds": "All",
                      "ViewTypeId": view_id}
    attrib_dict = module.params.get("attributes").copy()
    if isinstance(attrib_dict, dict):
        typeid = attrib_dict.get("Type") if attrib_dict.get("Type") else attrib_dict.get("TypeId")
        if typeid:
            create_payload["TypeId"] = typeid
        attrib_dict.pop("Type", None)  # remove if exists as it is not required for create payload
        create_payload.update(attrib_dict)
        template = get_template_by_name(attrib_dict.get("Name"), module, rest_obj)
        if template:
            module.exit_json(msg=TEMPLATE_NAME_EXISTS.format(name=attrib_dict.get("Name")))
    create_payload["SourceDeviceId"] = int(deviceid)
    return create_payload


def get_modify_payload(module, rest_obj, template_dict):
    modify_payload = {}
    attrib_dict = module.params.get("attributes")
    attrib_dict['Id'] = template_dict.get('Id')
    modify_payload["Name"] = template_dict["Name"]
    diff = 0
    if attrib_dict.get("Name", template_dict["Name"]) != template_dict["Name"]:
        template = get_template_by_name(attrib_dict.get("Name"), module, rest_obj)
        if template:
            module.exit_json(msg=TEMPLATE_NAME_EXISTS.format(name=attrib_dict.get("Name")))
        modify_payload["Name"] = attrib_dict.get("Name")
        diff = diff + 1
    modify_payload["Description"] = template_dict["Description"]
    diff = diff + apply_diff_key(attrib_dict, modify_payload, ["Description"])
    # check attributes
    if attrib_dict.get("Attributes"):
        diff = diff + attributes_check(module, rest_obj, attrib_dict, template_dict.get('Id'))

    if not diff:
        module.exit_json(msg=NO_CHANGES_MSG)
    if isinstance(attrib_dict, dict):
        modify_payload.update(attrib_dict)
    # module.exit_json(attrib_dict=attrib_dict, modify_payload=modify_payload)
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
    template = get_template_by_name(import_payload["Name"], module, rest_obj)
    if template:
        module.exit_json(msg=TEMPLATE_NAME_EXISTS.format(name=import_payload["Name"]))
    import_payload["ViewTypeId"] = view_id
    import_payload["Type"] = 2
    typeid = attrib_dict.get("Type") if attrib_dict.get("Type") else attrib_dict.get("TypeId")
    if typeid:
        if get_type_id_valid(rest_obj, typeid):
            import_payload["Type"] = typeid   # Type is mandatory for import
        else:
            fail_module(module, msg="Type provided for 'import' operation is invalid")
    import_payload["Content"] = attrib_dict.pop("Content")
    if isinstance(attrib_dict, dict):
        attrib_dict.pop("TypeId", None)  # remove if exists as it is not required for import payload
        import_payload.update(attrib_dict)
    return import_payload


def get_clone_payload(module, rest_obj, template_id, view_id):
    attrib_dict = module.params.get("attributes").copy()
    clone_payload = {}
    clone_payload["SourceTemplateId"] = template_id
    clone_payload["NewTemplateName"] = attrib_dict.pop("Name")
    template = get_template_by_name(clone_payload["NewTemplateName"], module, rest_obj)
    if template:
        module.exit_json(msg=TEMPLATE_NAME_EXISTS.format(name=clone_payload["NewTemplateName"]))
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


def get_template_details(module, rest_obj):
    id = module.params.get('template_id')
    query_param = {"$filter": "Id eq {0}".format(id)}
    srch = 'Id'
    if not id:
        id = module.params.get('template_name')
        query_param = {"$filter": "Name eq '{0}'".format(id)}
        srch = 'Name'
    template = {}
    resp = rest_obj.invoke_request('GET', TEMPLATES_URI, query_param=query_param)
    if resp.success and resp.json_data.get('value'):
        tlist = resp.json_data.get('value', [])
        for xtype in tlist:
            if xtype.get(srch) == id:
                template = xtype
    return template


def _get_resource_parameters(module, rest_obj):
    command = module.params.get("command")
    rest_method = 'POST'
    payload = {}
    template = get_template_details(module, rest_obj)
    template_id = template.get('Id')
    # template_name = template.get('Name')
    if command not in ["import", "create", "delete"] and not template:
        fail_module(module, msg="Enter a valid template_name or template_id")
    if command == "create":
        devid_list = get_device_ids(module, rest_obj)
        if len(devid_list) != 1:
            fail_module(module, msg="Create template requires only one reference device")
        view_id = get_view_id(rest_obj, module.params['template_view_type'])
        payload = get_create_payload(module, rest_obj, devid_list[0], view_id)
        path = TEMPLATES_URI
    elif command == 'import':
        view_id = get_view_id(rest_obj, module.params['template_view_type'])
        path = TEMPLATE_ACTION.format(op="Import")
        payload = get_import_payload(module, rest_obj, view_id)
    elif command == "delete":
        if not template:
            module.exit_json(msg=NO_CHANGES_MSG)
        path = TEMPLATE_PATH.format(template_id=template_id)
        rest_method = 'DELETE'
    elif command == "modify":
        path = TEMPLATE_PATH.format(template_id=template_id)
        template_dict = get_template_by_id(module, rest_obj, template_id)
        payload = get_modify_payload(module, rest_obj, template_dict)
        rest_method = 'PUT'
    elif command == "export":
        path = TEMPLATE_ACTION.format(op="Export")
        payload = {'TemplateId': template_id}
    elif command == "deploy":
        devid_list = get_device_ids(module, rest_obj)
        if not devid_list:
            fail_module(module, msg="There are no devices provided for deploy operation")
        profile_list = get_profiles(rest_obj)
        dev_temp_map = {}
        for prof in profile_list:
            target = prof["TargetId"]
            if prof["ProfileState"] > 0 and target in devid_list:
                if template_id == prof['TemplateId']:  # already same template deployed
                    devid_list.remove(target)
                else:
                    dev_temp_map[prof["TargetId"]] = prof['TemplateId']
        if dev_temp_map:
            module.exit_json(devices_assigned=dev_temp_map,
                             msg=DEPLOY_DEV_ASSIGNED.format(dev=','.join(map(str, dev_temp_map.keys())),
                                                            temp=','.join(map(str, dev_temp_map.values()))))
        if not devid_list:
            module.exit_json(msg=NO_CHANGES_MSG)
        path = TEMPLATE_ACTION.format(op="Deploy")
        payload = get_deploy_payload(module.params, devid_list, template_id)
    elif command == "clone":
        view_id = get_view_id(rest_obj, module.params['template_view_type'])
        path = TEMPLATE_ACTION.format(op="Clone")
        payload = get_clone_payload(module, rest_obj, template_id, view_id)
    if module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
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


def exit_module(rest_obj, module, response, time_out=False):
    password_no_log(module.params.get("attributes"))
    resp = None
    changed_flag = True
    command = module.params.get('command')
    result = {}
    if command in ["create", "modify", "deploy", "import", "clone"]:
        result["return_id"] = response.json_data
        resp = result["return_id"]
        if command == 'deploy':
            if time_out:
                command = 'timed_out'
                changed_flag = False
            elif not result["return_id"]:
                result["failed"] = True
                command = 'deploy_fail'
                changed_flag = False
            elif module.params["job_wait"]:
                command = 'deploy_when_job_wait_true'
            else:
                command = 'deploy_when_job_wait_false'
        elif command == 'create':
            if time_out:
                resp = get_job_id(rest_obj, resp)
                command = 'timed_out'
                changed_flag = False
            elif module.params["job_wait"]:
                command = 'create_when_job_wait_true'
            else:
                time.sleep(5)
                resp = get_job_id(rest_obj, resp)
                command = 'create_when_job_wait_false'
    if command == 'export':
        changed_flag = False
        result = response.json_data
    message = MSG_DICT.get(command).format(resp)
    module.exit_json(msg=message, changed=changed_flag, **result)


def get_job_id(rest_obj, template_id):
    template = rest_obj.invoke_request("GET", TEMPLATE_PATH.format(template_id=template_id))
    job_id = template.json_data.get("TaskId")
    return job_id


def main():
    specs = {
        "command": {"required": False, "default": "create", "aliases": ['state'],
                    "choices": ['create', 'modify', 'deploy', 'delete', 'export', 'import', 'clone']},
        "template_id": {"required": False, "type": 'int'},
        "template_name": {"required": False, "type": 'str'},
        "template_view_type": {"required": False, "default": 'Deployment',
                               "choices": ['Deployment', 'Compliance', 'Inventory', 'Sample', 'None']},
        "device_id": {"required": False, "type": 'list', "default": [], "elements": 'int'},
        "device_service_tag": {"required": False, "type": 'list', "default": [], "elements": 'str'},
        "device_group_names": {"required": False, "type": 'list', "default": [], "elements": 'str'},
        "attributes": {"required": False, "type": 'dict'},
        "job_wait": {"required": False, "type": "bool", "default": True},
        "job_wait_timeout": {"required": False, "type": "int", "default": 1200}
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        required_if=[
            ['command', 'create', ['attributes']],
            ['command', 'modify', ['attributes']],
            ['command', 'import', ['attributes']],
            ['command', 'modify', ['template_id', 'template_name'], True],
            ['command', 'delete', ['template_id', 'template_name'], True],
            ['command', 'export', ['template_id', 'template_name'], True],
            ['command', 'clone', ['template_id', 'template_name'], True],
            ['command', 'deploy', ['template_id', 'template_name'], True],
            ['command', 'deploy', ['device_id', 'device_service_tag', 'device_group_names'], True],
        ],
        mutually_exclusive=[["template_id", "template_name"]],
        supports_check_mode=True)

    try:
        _validate_inputs(module)
        with RestOME(module.params, req_session=True) as rest_obj:
            path, payload, rest_method = _get_resource_parameters(module, rest_obj)
            resp = rest_obj.invoke_request(rest_method, path, data=payload)
            job_wait = module.params["job_wait"]
            job_id = None
            if job_wait:
                if module.params["command"] == "create":
                    template_id = resp.json_data
                    count = 30
                    sleep_time = 5
                    while count > 0:
                        try:
                            job_id = get_job_id(rest_obj, template_id)
                            if job_id:
                                break
                            time.sleep(sleep_time)
                            count = count - sleep_time
                        except HTTPError:
                            time.sleep(sleep_time)
                            count = count - sleep_time
                            continue
                elif module.params["command"] == "deploy":
                    job_id = resp.json_data
                if job_id:
                    job_uri = JOB_URI.format(job_id=job_id)
                    job_failed, msg, job_dict, wait_time = job_tracking(rest_obj, job_uri, max_job_wait_sec=module.params["job_wait_timeout"])
                    if job_failed:
                        if job_dict.get('LastRunStatus').get('Name') == "Running":
                            exit_module(rest_obj, module, resp, True)
                        else:
                            message = MSG_DICT.get('fail').format(command=module.params["command"])
                            module.fail_json(msg=message)
            if resp.success:
                exit_module(rest_obj, module, resp)
    except HTTPError as err:
        fail_module(module, msg=str(err), error_info=json.load(err))
    except URLError as err:
        password_no_log(module.params.get("attributes"))
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, SSLError, SSLValidationError, ConnectionError, TypeError, ValueError, KeyError, OSError) as err:
        fail_module(module, msg=str(err))


if __name__ == '__main__':
    main()
