#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.4.0
# Copyright (C) 2019-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: idrac_server_config_profile
short_description: Export or Import iDRAC Server Configuration Profile (SCP)
version_added: "2.1.0"
description:
  - Export the Server Configuration Profile (SCP) from the iDRAC or import from a
    network share (CIFS, NFS, HTTP, HTTPS) or a local path.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_x_auth_options
options:
  command:
    description:
      - If C(import), the module performs SCP import operation.
      - If C(export), the module performs SCP export operation.
      - If C(preview), the module performs SCP preview operation.
      - C(import_custom_defaults) allows you to import custom default iDRAC settings.
      - C(export_custom_defaults) allows you to export custom default iDRAC settings.
      - C(import_custom_defaults) and C(export_custom_defaults) is supported only on iDRAC9 with firmware 7.00.00.00 and above.
    type: str
    choices: ['import', 'export', 'preview', 'import_custom_defaults', 'export_custom_defaults']
    default: 'export'
  job_wait:
    description: Whether to wait for job completion or not.
    type: bool
    required: true
  share_name:
    description:
      - Network share or local path.
      - CIFS, NFS, HTTP, and HTTPS network share types are supported.
      - I(share_name) is mutually exclusive with I(import_buffer).
      - Only "local" is supported when the I(command) is C(import_custom_defaults) or C(export_custom_defaults).
    type: str
  share_user:
    description: Network share user in the format 'user@domain' or 'domain\\user' if user is
      part of a domain else 'user'. This option is mandatory for CIFS Network Share.
    type: str
  share_password:
    description: Network share user password. This option is mandatory for CIFS Network Share.
    type: str
    aliases: ['share_pwd']
  scp_file:
    description:
      - Name of the server configuration profile (SCP) file.
      - Only XML file format is supported when I(command) is C(import) or C(import_custom_defaults) or C(export_custom_defaults).
      - The default format <idrac_ip>_YYmmdd_HHMMSS_scp is used if this option is not specified for C(export) or C(export_custom_defaults).
      - I(export_format) is used if the valid extension file is not provided for C(export).
    type: str
  scp_components:
    description:
      - If C(ALL), this option exports or imports all components configurations from the SCP file.
      - If C(IDRAC), this option exports or imports iDRAC configuration from the SCP file.
      - If C(BIOS), this option exports or imports BIOS configuration from the SCP file.
      - If C(NIC), this option exports or imports NIC configuration from the SCP file.
      - If C(RAID), this option exports or imports RAID configuration from the SCP file.
      - If C(FC), this option exports or imports FiberChannel configurations from the SCP file.
      - If C(InfiniBand), this option exports or imports InfiniBand configuration from the SCP file.
      - If C(SupportAssist), this option exports or imports SupportAssist configuration from the SCP file.
      - If C(EventFilters), this option exports or imports EventFilters configuration from the SCP file.
      - If C(System), this option exports or imports System configuration from the SCP file.
      - If C(LifecycleController), this option exports or imports SupportAssist configuration from the SCP file.
      - If C(AHCI), this option exports or imports EventFilters configuration from the SCP file.
      - If C(PCIeSSD), this option exports or imports PCIeSSD configuration from the SCP file.
      - When I(command) is C(export) or C(import) I(target) with multiple components is supported only
        on iDRAC9 with firmware 6.10.00.00 and above.
    type: list
    choices: ['ALL', 'IDRAC', 'BIOS', 'NIC', 'RAID', 'FC', 'InfiniBand', 'SupportAssist',
              'EventFilters', 'System', 'LifecycleController', 'AHCI', 'PCIeSSD']
    default: 'ALL'
    elements: str
    aliases: ['target']
  shutdown_type:
    description:
      - This option is applicable for C(import) command.
      - If C(Graceful), the job gracefully shuts down the operating system and turns off the server.
      - If C(Forced), it forcefully shuts down the server.
      - If C(NoReboot), the job that applies the SCP will pause until you manually reboot the server.
    type: str
    choices: ['Graceful', 'Forced', 'NoReboot']
    default: 'Graceful'
  end_host_power_state:
    description:
      - This option is applicable for C(import) command.
      - If C(On), End host power state is on.
      - If C(Off), End host power state is off.
    type: str
    choices: ['On' ,'Off']
    default: 'On'
  export_format:
    description:
      - Specify the output file format. This option is applicable for C(export) or C(export_custom_defaults) command.
      - The default export file format is always XML when the  I(command) is C(export_custom_defaults).
    type: str
    choices: ['JSON',  'XML']
    default: 'XML'
  export_use:
    description:
      - Specify the type of Server Configuration Profile (SCP) to be exported.
      - This option is applicable when I(command) is C(export).
      - C(Default) Creates a non-destructive snapshot of the configuration.
      - C(Replace) Replaces a server with another or restores the servers settings to a known baseline.
      - C(Clone) Clones settings from one server to another server with the identical hardware setup.
        All settings except I/O identity are updated (e.g. will reset RAID). The settings in this export
        will be destructive when uploaded to another system.
    type: str
    choices: ['Default',  'Clone', 'Replace']
    default: 'Default'
    version_added: 7.3.0
  ignore_certificate_warning:
    description:
      - If C(ignore), it ignores the certificate warnings.
      - If C(showerror), it shows the certificate warnings.
      - I(ignore_certificate_warning) is considered only when I(share_name) is of type HTTPS and is
        supported only on iDRAC9.
    type: str
    choices: [ignore, showerror]
    default: ignore
    version_added: 7.3.0
  include_in_export:
    description:
      - This option is applicable when I(command) is C(export).
      - If C(default), it exports the default Server Configuration Profile.
      - If C(readonly), it exports the SCP with readonly attributes.
      - If C(passwordhashvalues), it exports the SCP with password hash values.
      - If C(customtelemetry), exports the SCP with custom telemetry attributes supported only in the iDRAC9.
    type: str
    choices: [default, readonly, passwordhashvalues, customtelemetry]
    default: default
    version_added: 7.3.0
  import_buffer:
    description:
      - Used to import the buffer input of xml or json into the iDRAC.
      - When the  I(command) is C(import_custom_defaults), only XML file format is supported.
      - This option is applicable when I(command) is C(import) or C(preview) or C(import_custom_defaults).
      - I(import_buffer) is mutually exclusive with I(share_name).
    type: str
    version_added: 7.3.0
  proxy_support:
    description:
      - Proxy to be enabled or disabled.
      - I(proxy_support) is considered only when I(share_name) is of type HTTP or HTTPS and is supported only on iDRAC9.
    type: bool
    default: false
    version_added: 7.3.0
  proxy_type:
    description:
      - C(http) to select HTTP type proxy.
      - C(socks4) to select SOCKS4 type proxy.
      - I(proxy_type) is considered only when I(share_name) is of type HTTP or HTTPS and is supported only on iDRAC9.
    type: str
    choices: [http, socks4]
    default: http
    version_added: 7.3.0
  proxy_server:
    description:
      - I(proxy_server) is required when I(share_name) is of type HTTPS or HTTP and I(proxy_support) is C(true).
      - I(proxy_server) is considered only when I(share_name) is of type HTTP or HTTPS and is supported only on iDRAC9.
    type: str
    version_added: 7.3.0
  proxy_port:
    description:
      - Proxy port to authenticate.
      - I(proxy_port) is required when I(share_name) is of type HTTPS or HTTP and I(proxy_support) is C(true).
      - I(proxy_port) is considered only when I(share_name) is of type HTTP or HTTPS and is supported only on iDRAC9.
    type: str
    default: "80"
    version_added: 7.3.0
  proxy_username:
    description:
      - Proxy username to authenticate.
      - I(proxy_username) is considered only when I(share_name) is of type HTTP or HTTPS
        and is supported only on iDRAC9.
    type: str
    version_added: 7.3.0
  proxy_password:
    description:
      - Proxy password to authenticate.
      - I(proxy_password) is considered only when I(share_name) is of type HTTP or HTTPS
        and is supported only on iDRAC9.
    type: str
    version_added: 7.3.0
requirements:
  - "python >= 3.9.14"
author:
  - "Jagadeesh N V(@jagadeeshnv)"
  - "Felix Stephen (@felixs88)"
  - "Jennifer John (@Jennifer-John)"
  - "Shivam Sharma (@ShivamSh3)"
  - "Lovepreet Singh (@singh-lovepreet1)"
notes:
    - This module requires 'Administrator' privilege for I(idrac_user).
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports C(check_mode).
    - To import Server Configuration Profile (SCP) on the iDRAC8-based servers,
      the servers must have iDRAC Enterprise license or later.
    - For C(import) operation, C(check_mode) is supported only when I(target) is C(ALL).
    - This module supports IPv4 and IPv6 addresses.
'''

EXAMPLES = r'''
---
- name: Export SCP with IDRAC components in JSON format to a local path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/scp_folder"
    scp_components:
      - IDRAC
    scp_file: example_file
    export_format: JSON
    export_use: Clone
    job_wait: true

- name: Import SCP with IDRAC components in JSON format from a local path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/scp_folder"
    command: import
    scp_components:
      - IDRAC
    scp_file: example_file.json
    shutdown_type: Graceful
    end_host_power_state: "On"
    job_wait: false

- name: Export SCP with BIOS components in XML format to a NFS share path with auto-generated file name
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "192.168.0.2:/share"
    scp_components:
      - BIOS
    export_format: XML
    export_use: Default
    job_wait: true

- name: Import SCP with BIOS components in XML format from a NFS share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "192.168.0.2:/share"
    command: import
    scp_components:
      - BIOS
    scp_file: 192.168.0.1_20210618_162856.xml
    shutdown_type: NoReboot
    end_host_power_state: "Off"
    job_wait: false

- name: Export SCP with RAID components in XML format to a CIFS share path with share user domain name
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "\\\\192.168.0.2\\share"
    share_user: share_username@domain
    share_password: share_password
    scp_file: example_file.xml
    scp_components:
      - RAID
    export_format: XML
    export_use: Default
    job_wait: true

- name: Import SCP with RAID components in XML format from a CIFS share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "\\\\192.168.0.2\\share"
    share_user: share_username
    share_password: share_password
    command: import
    scp_components:
      - RAID
    scp_file: example_file.xml
    shutdown_type: Forced
    end_host_power_state: "On"
    job_wait: true

- name: Export SCP with ALL components in JSON format to a HTTP share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "http://192.168.0.3/share"
    share_user: share_username
    share_password: share_password
    scp_file: example_file.json
    scp_components:
      - ALL
    export_format: JSON
    job_wait: false

- name: Import SCP with ALL components in JSON format from a HTTP share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: import
    share_name: "http://192.168.0.3/share"
    share_user: share_username
    share_password: share_password
    scp_file: example_file.json
    shutdown_type: Graceful
    end_host_power_state: "On"
    job_wait: true

- name: Export SCP with ALL components in XML format to a HTTPS share path without SCP file name
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "https://192.168.0.4/share"
    share_user: share_username
    share_password: share_password
    scp_components:
      - ALL
    export_format: XML
    export_use: Replace
    job_wait: true

- name: Import SCP with ALL components in XML format from a HTTPS share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: import
    share_name: "https://192.168.0.4/share"
    share_user: share_username
    share_password: share_password
    scp_file: 192.168.0.1_20160618_164647.xml
    shutdown_type: Graceful
    end_host_power_state: "On"
    job_wait: false

- name: Preview SCP with IDRAC components in XML format from a CIFS share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "{{ idrac_ip }}"
    idrac_user: "{{ idrac_user }}"
    idrac_password: "{{ idrac_password }}"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "\\\\192.168.0.2\\share"
    share_user: share_username
    share_password: share_password
    command: preview
    scp_components:
      - ALL
    scp_file: example_file.xml
    job_wait: true

- name: Preview SCP with IDRAC components in JSON format from a NFS share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "{{ idrac_ip }}"
    idrac_user: "{{ idrac_user }}"
    idrac_password: "{{ idrac_password }}"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "192.168.0.2:/share"
    command: preview
    scp_components:
      - IDRAC
    scp_file: example_file.xml
    job_wait: true

- name: Preview SCP with IDRAC components in XML format from a HTTP share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "{{ idrac_ip }}"
    idrac_user: "{{ idrac_user }}"
    idrac_password: "{{ idrac_password }}"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "http://192.168.0.1/http-share"
    share_user: share_username
    share_password: share_password
    command: preview
    scp_components:
      - ALL
    scp_file: example_file.xml
    job_wait: true

- name: Preview SCP with IDRAC components in XML format from a local path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "{{ idrac_ip }}"
    idrac_user: "{{ idrac_user }}"
    idrac_password: "{{ idrac_password }}"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/scp_folder"
    command: preview
    scp_components:
      - IDRAC
    scp_file: example_file.json
    job_wait: false

- name: Import SCP with IDRAC components in XML format from the XML content.
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "{{ idrac_ip }}"
    idrac_user: "{{ idrac_user }}"
    idrac_password: "{{ idrac_password }}"
    ca_path: "/path/to/ca_cert.pem"
    command: import
    scp_components:
      - IDRAC
    job_wait: true
    import_buffer: "<SystemConfiguration><Component FQDD='iDRAC.Embedded.1'><Attribute Name='IPMILan.1#Enable'>
      Disabled</Attribute></Component></SystemConfiguration>"

- name: Export SCP with ALL components in XML format using HTTP proxy.
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "{{ idrac_ip }}"
    idrac_user: "{{ idrac_user }}"
    idrac_password: "{{ idrac_password }}"
    ca_path: "/path/to/ca_cert.pem"
    scp_components:
      - ALL
    share_name: "http://192.168.0.1/http-share"
    proxy_support: true
    proxy_server: 192.168.0.5
    proxy_port: 8080
    proxy_username: proxy_username
    proxy_password: proxy_password
    proxy_type: http
    include_in_export: passwordhashvalues
    job_wait: true

- name: Import SCP with IDRAC and BIOS components in XML format using SOCKS4 proxy
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "{{ idrac_ip }}"
    idrac_user: "{{ idrac_user }}"
    idrac_password: "{{ idrac_password }}"
    ca_path: "/path/to/ca_cert.pem"
    command: import
    scp_components:
      - IDRAC
      - BIOS
    share_name: "https://192.168.0.1/http-share"
    proxy_support: true
    proxy_server: 192.168.0.6
    proxy_port: 8080
    proxy_type: socks4
    scp_file: filename.xml
    job_wait: true

- name: Import SCP with IDRAC components in JSON format from the JSON content.
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "{{ idrac_ip }}"
    idrac_user: "{{ idrac_user }}"
    idrac_password: "{{ idrac_password }}"
    ca_path: "/path/to/ca_cert.pem"
    command: import
    scp_components:
      - IDRAC
    job_wait: true
    import_buffer: "{\"SystemConfiguration\": {\"Components\": [{\"FQDD\": \"iDRAC.Embedded.1\",\"Attributes\":
      [{\"Name\": \"SNMP.1#AgentCommunity\",\"Value\": \"public1\"}]}]}}"

- name: Export custom default
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    job_wait: true
    share_name: "/scp_folder"
    command: export_custom_defaults
    scp_file: example_file

- name: Import custom default
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    job_wait: true
    share_name: "/scp_folder"
    command: import_custom_defaults
    scp_file: example_file.xml

- name: Import custom default using buffer
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    job_wait: true
    command: import_custom_defaults
    import_buffer: "<SystemConfiguration><Component FQDD='iDRAC.Embedded.1'><Attribute Name='IPMILan.1#Enable'>Disabled</Attribute>
                  </Component></SystemConfiguration>"
'''

RETURN = r'''
---
msg:
  type: str
  description: Status of the import or export SCP job.
  returned: always
  sample: "Successfully imported the Server Configuration Profile"
scp_status:
  type: dict
  description: SCP operation job and progress details from the iDRAC.
  returned: success
  sample:
    {
      "Id": "JID_XXXXXXXXX",
      "JobState": "Completed",
      "JobType": "ImportConfiguration",
      "Message": "Successfully imported and applied Server Configuration Profile.",
      "MessageArgs": [],
      "MessageId": "XXX123",
      "Name": "Import Configuration",
      "PercentComplete": 100,
      "StartTime": "TIME_NOW",
      "Status": "Success",
      "TargetSettingsURI": null,
      "retval": true
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

import os
import re
import json
from datetime import datetime
from os.path import exists
import xml.etree.ElementTree as ET
from ansible.module_utils.compat.version import LooseVersion
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, IdracAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import idrac_redfish_job_tracking, \
    strip_substr_dict, get_idrac_firmware_version, get_dynamic_uri
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.parse import urlparse


REDFISH_SCP_BASE_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"
MANAGER_ID = 'iDRAC.Embedded.1'
CHANGES_FOUND = "Changes found to be applied."
INVALID_SHARE_NAME = "Unable to perform the {command} operation because an invalid Share name is entered. \
Only 'local' share name is supported. Enter the valid Share name and retry the operation."
ERR_STATUS_CODE = [400, 404]
CUSTOM_DEFAULTS_NOT_FOUND = "Custom defaults is not available on the iDRAC."
SHARE_NAME_REQUIRED = "Share name is required. Enter the valid Share name and retry the operation."
NO_CHANGES_FOUND = "No changes found to be applied."
INVALID_FILE = "Invalid file path provided."
INVALID_FILE_FORMAT = "An invalid export format is selected. File format '.xml' is supported. Select a valid file format and retry the operation."
INVALID_XML_CONTENT = "An invalid XML content is provided. Provide custom default content in a valid XML format."
CUSTOM_ERROR = "{command} is not supported on this firmware version of iDRAC. \
Enter the valid values and retry the operation."
JOB_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/{job_id}"
IGNORE_WARNING = {"ignore": "Enabled", "showerror": "Disabled"}
IN_EXPORTS = {"default": "Default", "readonly": "IncludeReadOnly", "passwordhashvalues": "IncludePasswordHashValues",
              "customtelemetry": "IncludeCustomTelemetry"}
SCP_ALL_ERR_MSG = "The option ALL cannot be used with options IDRAC, BIOS, NIC, or RAID."
MINIMUM_SUPPORTED_FIRMWARE_VERSION = "7.00.00"
MUTUALLY_EXCLUSIVE = "import_buffer is mutually exclusive with {0}."
PROXY_ERR_MSG = "proxy_support is enabled but all of the following are missing: proxy_server"
iDRAC_JOB_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/{job_id}"
FAIL_MSG = "Failed to {0} scp."
TARGET_INVALID_MSG = "Unable to {command} the {invalid_targets} from the SCP file\
 because the values {invalid_targets} are invalid.\
 The valid values are {valid_targets}. Enter the valid values and retry the operation."
DOMAIN_LIST = ["\\", "@"]
ERROR_CODES = ["SYS041", "SYS044", "SYS045", "SYS046", "SYS047", "SYS048", "SYS050", "SYS051", "SYS062",
               "SYS063", "SYS064", "SYS065", "SYS067", "SYS068", "SYS070", "SYS071", "SYS072",
               "SYS073", "SYS075", "SYS076", "SYS077", "SYS078", "SYS079", "SYS080"]


def get_scp_file_format(module):
    scp_file = module.params['scp_file']
    if scp_file:
        scp_file_name_format = scp_file
        if not str(scp_file.lower()).endswith(('.xml', '.json')):
            scp_file_name_format = "{0}.{1}".format(scp_file, module.params['export_format'].lower())
    else:
        d = datetime.now()
        scp_file_name_format = "{0}_{1}{2}{3}_{4}{5}{6}_scp.{7}".format(
            module.params["idrac_ip"], d.date().year, d.date().month, d.date().day,
            d.time().hour, d.time().minute, d.time().second,
            module.params['export_format'].lower())
    return scp_file_name_format


def response_format_change(response, params, file_name):
    resp = {}
    if params["job_wait"]:
        if hasattr(response, "json_data"):
            response = response.json_data
        response.pop("Description", None)
        response.pop("Name", None)
        response.pop("EndTime", None)
        response.pop("StartTime", None)
        response.pop("TaskState", None)
        response.pop("Messages", None)
        if response.get("Oem") is not None:
            response.update(response["Oem"]["Dell"])
            response.pop("Oem", None)
        response = get_file(params, response, file_name)
        response["retval"] = True
    else:
        location = response.headers.get("Location")
        job_id = location.split("/")[-1]
        job_uri = JOB_URI.format(job_id=job_id)
        resp["Data"] = {"StatusCode": response.status_code, "jobid": job_id, "next_uri": job_uri}
        resp["Job"] = {"JobId": job_id, "ResourceURI": job_uri}
        resp["Return"] = "JobCreated"
        resp["Status"] = "Success"
        resp["Message"] = "none"
        resp["StatusCode"] = response.status_code
        resp = get_file(params, resp, file_name)
        resp["retval"] = True
        response = resp
    return response


def get_file(params, response, file_name):
    if params.get("share_name") is not None:
        sep = "/" if "/" in params.get("share_name") else "\\"
        response["file"] = "{0}{1}{2}".format(params.get("share_name"), sep, file_name)
    return response


def get_proxy_share(module):
    proxy_share = {}
    proxy_support = module.params.get("proxy_support")
    proxy_type = module.params["proxy_type"]
    proxy_server = module.params.get("proxy_server")
    proxy_port = module.params["proxy_port"]
    proxy_username = module.params.get("proxy_username")
    proxy_password = module.params.get("proxy_password")
    if proxy_support is True and proxy_server is None:
        module.fail_json(msg=PROXY_ERR_MSG)
    if proxy_support is True:
        proxy_share["proxy_server"] = proxy_server
        proxy_share["proxy_username"] = proxy_username
        proxy_share["proxy_password"] = proxy_password
        proxy_share["proxy_port"] = proxy_port
        proxy_share["proxy_type"] = proxy_type.upper()
        proxy_share["proxy_support"] = "Enabled"
    else:
        proxy_share["proxy_support"] = "Disabled"
    return proxy_share


def run_export_import_scp_http(idrac, module):
    share_url = urlparse(module.params["share_name"])
    share = {}
    scp_file = module.params.get("scp_file")
    share["share_ip"] = share_url.netloc
    share["share_name"] = share_url.path.strip('/')
    share["share_type"] = share_url.scheme.upper()
    share["file_name"] = scp_file
    scp_file_name_format = scp_file
    share["username"] = module.params.get("share_user")
    share["password"] = module.params.get("share_password")
    scp_target = ",".join(module.params["scp_components"])
    command = module.params["command"]
    if share["share_type"] == "HTTPS":
        share["ignore_certificate_warning"] = IGNORE_WARNING[module.params["ignore_certificate_warning"]]
    if command == "import":
        perform_check_mode(module, idrac)
        if share["share_type"] in ["HTTP", "HTTPS"]:
            proxy_share = get_proxy_share(module)
            share.update(proxy_share)
        idrac_import_scp_params = {
            "target": scp_target, "share": share, "job_wait": module.params["job_wait"],
            "host_powerstate": module.params["end_host_power_state"], "shutdown_type": module.params["shutdown_type"]
        }
        scp_response = idrac.import_scp_share(**idrac_import_scp_params)
        scp_response = wait_for_job_tracking_redfish(module, idrac, scp_response)
    elif command == "export":
        scp_file_name_format = get_scp_file_format(module)
        share["file_name"] = scp_file_name_format
        include_in_export = IN_EXPORTS[module.params["include_in_export"]]
        if share["share_type"] in ["HTTP", "HTTPS"]:
            proxy_share = get_proxy_share(module)
            share.update(proxy_share)
        scp_response = idrac.export_scp(export_format=module.params["export_format"],
                                        export_use=module.params["export_use"],
                                        target=scp_target,
                                        job_wait=False, share=share,  # Hardcoding it as false because job tracking is done in idrac_redfish.py as well.
                                        include_in_export=include_in_export)
        scp_response = wait_for_job_tracking_redfish(
            module, idrac, scp_response
        )
    scp_response = response_format_change(scp_response, module.params, scp_file_name_format)
    exit_on_failure(module, scp_response, command)
    return scp_response


def perform_check_mode(module, idrac, http_share=True):
    if module.check_mode:
        module.params["job_wait"] = True
        scp_resp = preview_scp_redfish(module, idrac, http_share, import_job_wait=True)
        if "SYS081" in scp_resp["MessageId"] or "SYS082" in scp_resp["MessageId"]:
            module.exit_json(msg=CHANGES_FOUND, changed=True)
        elif "SYS069" in scp_resp["MessageId"]:
            module.exit_json(msg=NO_CHANGES_FOUND)
        else:
            module.fail_json(msg=scp_resp)


def get_scp_share_details(module):
    share_name = module.params.get("share_name")
    command = module.params["command"]
    scp_file_name_format = get_scp_file_format(module)
    share = {}
    if share_name:
        share = parse_share_name(module, share_name)
        if command in ["export", "export_custom_defaults"]:
            share["file_name"] = scp_file_name_format
    return share, scp_file_name_format


def parse_share_name(module, share_name):
    if ":/" in share_name:
        nfs_split = share_name.split(":/", 1)
        return {"share_ip": nfs_split[0], "share_name": "/{0}".format(nfs_split[1]), "share_type": "NFS"}
    elif "\\" in share_name:
        cifs_share = share_name.split("\\", 3)
        share_ip = cifs_share[2]
        share_path_name = cifs_share[-1]
        if not any(domain in module.params.get("share_user") for domain in DOMAIN_LIST):
            module.params["share_user"] = ".\\{0}".format(module.params.get("share_user"))
        return {"share_ip": share_ip, "share_name": share_path_name, "share_type": "CIFS",
                "username": module.params.get("share_user"), "password": module.params.get("share_password")}
    else:
        return {"share_type": "LOCAL", "share_name": share_name}


def export_scp_redfish(module, idrac):
    command = module.params["command"]
    share, scp_file_name_format = get_scp_share_details(module)
    scp_components = ",".join(module.params["scp_components"])
    include_in_export = IN_EXPORTS[module.params["include_in_export"]]
    scp_response = idrac.export_scp(export_format=module.params["export_format"],
                                    export_use=module.params["export_use"],
                                    target=scp_components, include_in_export=include_in_export,
                                    job_wait=False, share=share, )  # Assigning it as false because job tracking is done in idrac_redfish.py as well.
    if share["share_type"] == "LOCAL":
        scp_response = wait_for_response(scp_response, module, share, idrac)
    scp_response = wait_for_job_tracking_redfish(
        module, idrac, scp_response
    )
    scp_response = response_format_change(scp_response, module.params, scp_file_name_format)
    exit_on_failure(module, scp_response, command)
    return scp_response


def wait_for_response(scp_resp, module, share, idrac):
    task_uri = scp_resp.headers["Location"]
    wait_resp = idrac.wait_for_job_complete(task_uri, job_wait=True)
    with open("{0}/{1}".format(share["share_name"], share["file_name"]), "w") as file_obj:
        if module.params["export_format"] == "JSON":
            json.dump(wait_resp.json_data, file_obj, indent=4)
        else:
            wait_resp_value = wait_resp.decode("utf-8")
            file_obj.write(wait_resp_value)
    return scp_resp


def preview_scp_redfish(module, idrac, http_share, import_job_wait=False):
    import_buffer = module.params.get("import_buffer")
    command = module.params["command"]
    scp_targets = 'ALL'  # Assigning it as ALL because it is the only target for preview.
    job_wait_option = module.params["job_wait"]
    if command == "import":
        job_wait_option = import_job_wait
    share = {}
    if not import_buffer:
        if http_share:
            share_url = urlparse(module.params["share_name"])
            share = {"share_ip": share_url.netloc, "share_name": share_url.path.strip('/'),
                     "share_type": share_url.scheme.upper(), "file_name": module.params.get("scp_file"),
                     "username": module.params.get("share_user"), "password": module.params.get("share_password")}
            if http_share == "HTTPS":
                share["ignore_certificate_warning"] = IGNORE_WARNING[module.params["ignore_certificate_warning"]]
        else:
            share, _scp_file_name_format = get_scp_share_details(module)
            share["file_name"] = module.params.get("scp_file")
        buffer_text = get_buffer_text(module, share)
        scp_response = idrac.import_preview(import_buffer=buffer_text, target=scp_targets,
                                            share=share, job_wait=False)  # Assigning it as false because job tracking is done in idrac_redfish.py as well
        scp_response = wait_for_job_tracking_redfish(
            module, idrac, scp_response)
    else:
        scp_response = idrac.import_preview(import_buffer=import_buffer, target=scp_targets, job_wait=job_wait_option)
    scp_response = response_format_change(scp_response, module.params, share.get("file_name"))
    exit_on_failure(module, scp_response, command)
    return scp_response


def exit_on_failure(module, scp_response, command):
    if isinstance(scp_response, dict) and (scp_response.get("TaskStatus") == "Critical" or
                                           scp_response.get("JobState") in ("Failed", "CompletedWithErrors")):
        module.exit_json(msg=FAIL_MSG.format(command), scp_status=scp_response, failed=True)


def get_buffer_text(module, share):
    buffer_text = None
    if share["share_type"] == "LOCAL":
        file_path = "{0}{1}{2}".format(share["share_name"], os.sep, share["file_name"])
        if not exists(file_path):
            module.fail_json(msg=INVALID_FILE)
        with open(file_path, "r") as file_obj:
            buffer_text = file_obj.read()
    return buffer_text


def get_xml_content(module, xml_content):
    idrac_content = None
    try:
        root = ET.fromstring(xml_content)
        component = next((c for c in root.iter('Component') if c.get('FQDD') == MANAGER_ID), None)
        if component:
            idrac_content = ET.tostring(component).decode('utf-8')
        return idrac_content
    except ET.ParseError:
        module.exit_json(msg=INVALID_XML_CONTENT, failed=True)


def clean_buffer_text(buffer_text):
    buffer_text = re.sub(r'\s+', ' ', buffer_text)
    buffer_text = re.sub(r'>\s+<', '><', buffer_text)
    return buffer_text


def compare_custom_default_configs(module, idrac):
    diff = True
    scp_file = module.params.get("scp_file")
    buffer_text = module.params.get("import_buffer")
    idrac_cds = idrac_custom_option(idrac)
    if idrac_cds is None:
        return diff
    idrac_cds = idrac_cds.body
    if scp_file is not None:
        share, _scp_file_name_format = get_scp_share_details(module)
        share["file_name"] = module.params.get("scp_file")
        buffer_text = get_buffer_text(module, share)
    buffer_text = clean_buffer_text(buffer_text)
    if isinstance(idrac_cds, bytes):
        idrac_cds = idrac_cds.decode('utf-8')
    idrac_cds = clean_buffer_text(idrac_cds)
    imported_cds = get_xml_content(module, buffer_text)
    idrac_cds_data = get_xml_content(module, idrac_cds)
    if imported_cds == idrac_cds_data:
        diff = False
    return diff


def idrac_custom_option(idrac):
    url = None
    result = None
    resp = get_dynamic_uri(idrac, REDFISH_SCP_BASE_URI, "Oem")
    if resp:
        url = resp.get("Dell", {}).get('CustomDefaultsDownloadURI', {})
    try:
        if url:
            result = idrac.invoke_request(url, "GET")
        return result
    except HTTPError as err:
        if err.code in ERR_STATUS_CODE:
            return result


def check_mode_custom_defaults(module, content_diff):
    if module.check_mode:
        if content_diff:
            module.exit_json(msg=CHANGES_FOUND, changed=True)
        return module.exit_json(msg=NO_CHANGES_FOUND, changed=False)


def import_scp_redfish(module, idrac, http_share):
    import_buffer = module.params.get("import_buffer")
    command = module.params["command"]
    scp_targets = ",".join(module.params["scp_components"])
    perform_check_mode(module, idrac, http_share)
    share = {}
    if not import_buffer:
        share, _scp_file_name_format = get_scp_share_details(module)
        share["file_name"] = module.params.get("scp_file")
        buffer_text = get_buffer_text(module, share)
        share_dict = share
        if share["share_type"] == "LOCAL":
            share_dict = {}
        idrac_import_scp_params = {
            "import_buffer": buffer_text, "target": scp_targets, "share": share_dict, "job_wait": module.params["job_wait"],
            "host_powerstate": module.params["end_host_power_state"], "shutdown_type": module.params["shutdown_type"]
        }
        scp_response = idrac.import_scp_share(**idrac_import_scp_params)
        scp_response = wait_for_job_tracking_redfish(module, idrac, scp_response)
    else:
        scp_response = idrac.import_scp(import_buffer=import_buffer, target=scp_targets, job_wait=module.params["job_wait"])
    scp_response = response_format_change(scp_response, module.params, share.get("file_name"))
    exit_on_failure(module, scp_response, command)
    return scp_response


def wait_for_job_tracking_redfish(module, idrac, scp_response):
    job_id = scp_response.headers["Location"].split("/")[-1]
    if module.params["job_wait"]:
        job_failed, _msg, job_dict, _wait_time = idrac_redfish_job_tracking(
            idrac, iDRAC_JOB_URI.format(job_id=job_id))
        if job_failed or job_dict.get("MessageId", "") in ERROR_CODES:
            module.exit_json(failed=True, status_msg=job_dict, job_id=job_id, msg=FAIL_MSG.format(module.params["command"]))
        scp_response = job_dict
    return scp_response


def validate_share_name(module):
    share_name = module.params.get("share_name")
    command = module.params.get("command")
    import_buffer = module.params.get("import_buffer")
    if share_name is None and not import_buffer:
        module.exit_json(msg=SHARE_NAME_REQUIRED, skipped=True)
    elif share_name and (":/" in share_name or "\\" in share_name):
        module.exit_json(msg=INVALID_SHARE_NAME.format(share_name=share_name, command=command), skipped=True)


def validate_input(module, scp_components):
    if len(scp_components) != 1 and "ALL" in scp_components:
        module.fail_json(msg=SCP_ALL_ERR_MSG)
    if module.params["command"] in ["import", "preview"]:
        if module.params.get("import_buffer") is not None:
            if module.params.get("scp_file") is not None:
                module.fail_json(msg=MUTUALLY_EXCLUSIVE.format("scp_file"))
            if module.params.get("share_name") is not None:
                module.fail_json(msg=MUTUALLY_EXCLUSIVE.format("share_name"))


def validate_customdefault_input(module, command):
    export_format = module.params.get("export_format")
    validate_share_name(module)
    if command == "export_custom_defaults" and export_format:
        if export_format.lower() != 'xml':
            module.exit_json(msg=INVALID_FILE_FORMAT.format(export_format=export_format), failed=True)
    if command == "import_custom_defaults":
        if module.params.get("import_buffer") is not None:
            if module.params.get("scp_file") is not None:
                module.exit_json(msg=MUTUALLY_EXCLUSIVE.format("scp_file"), failed=True)
            if module.params.get("share_name") is not None:
                module.exit_json(msg=MUTUALLY_EXCLUSIVE.format("share_name"), failed=True)


def validate_scp_components(module, idrac):
    components = idrac.invoke_request(REDFISH_SCP_BASE_URI, "GET")
    all_components = strip_substr_dict(components.json_data)
    scp_components = module.params.get("scp_components")
    command = module.params.get("command")
    oem = all_components['Actions']['Oem']
    operation_dict = {
        "export": "ExportSystemConfiguration",
        "import": "ImportSystemConfiguration",
        "preview": "ImportSystemConfigurationPreview"
    }
    for each in oem:
        if each.endswith(operation_dict.get(command.lower())):
            allowable = oem.get(each).get('ShareParameters').get('Target@Redfish.AllowableValues')
            invalid_comp = list(set(scp_components) - set(allowable))
            if invalid_comp:
                msg = TARGET_INVALID_MSG.format(command=command, invalid_targets=invalid_comp, valid_targets=allowable)
                module.exit_json(msg=msg, failed=True)


def is_check_idrac_latest(firmware_version):
    if LooseVersion(firmware_version) >= MINIMUM_SUPPORTED_FIRMWARE_VERSION:
        return True
    return False


def import_custom_defaults(module, idrac):
    import_buffer = module.params.get("import_buffer")
    command = module.params["command"]
    cds_diff = compare_custom_default_configs(module, idrac)
    check_mode_custom_defaults(module, cds_diff)
    if not cds_diff:
        module.exit_json(msg=NO_CHANGES_FOUND, changed=False)
    share = {}
    if import_buffer:
        buffer_text = import_buffer
    else:
        share, _scp_file_name_format = get_scp_share_details(module)
        share["file_name"] = module.params.get("scp_file")
        buffer_text = get_buffer_text(module, share)
    payload = {"CustomDefaults": buffer_text}
    url = None
    resp = get_dynamic_uri(idrac, REDFISH_SCP_BASE_URI, "Actions")
    if resp:
        url = resp.get("Oem", {}).get('#DellManager.SetCustomDefaults', {}).get('target', {})
    job_resp = idrac.invoke_request(url, "POST", data=payload)
    scp_response = wait_for_job_tracking_redfish(module, idrac, job_resp)
    scp_response = response_format_change(scp_response, module.params, share.get("file_name"))
    exit_on_failure(module, scp_response, command)
    return scp_response


def export_custom_defaults(module, idrac):
    share, _scp_file_name_format = get_scp_share_details(module)
    idrac_resp_cds = idrac_custom_option(idrac)
    if idrac_resp_cds is None:
        module.exit_json(msg=CUSTOM_DEFAULTS_NOT_FOUND, changed=False)
    idrac_resp_cds = idrac_resp_cds.body
    res = {}
    if share["share_type"] == "LOCAL":
        if isinstance(idrac_resp_cds, bytes):
            idrac_resp_cds = idrac_resp_cds.decode('utf-8')
        with open("{0}/{1}".format(share["share_name"], share["file_name"]), "w") as file_obj:
            file_obj.write(idrac_resp_cds)
    res = get_file(module.params, res, _scp_file_name_format)
    return res


class ImportCustomDefaultCommand():
    def __init__(self, idrac, module):
        self.idrac = idrac
        self.module = module
        self.idrac_firmware_version = get_idrac_firmware_version(self.idrac)

    def execute(self):
        changed = True
        command = self.module.params["command"]
        if not is_check_idrac_latest(self.idrac_firmware_version):
            self.module.exit_json(msg=CUSTOM_ERROR.format(command=command),
                                  skipped=True)
        validate_customdefault_input(self.module, command)
        scp_status = import_custom_defaults(self.module, self.idrac)
        return scp_status, changed


class ImportCommand():
    def __init__(self, idrac, http_share, module):
        self.idrac = idrac
        self.http_share = http_share
        self.module = module

    def execute(self):
        changed = False
        if self.http_share:
            scp_status = run_export_import_scp_http(self.idrac, self.module)
            if "SYS069" in scp_status.get("MessageId", ""):
                changed = False
            elif "SYS053" in scp_status.get("MessageId", ""):
                changed = True
        else:
            scp_status = import_scp_redfish(self.module, self.idrac, self.http_share)
            if "No changes were applied" not in scp_status.get('Message', ""):
                changed = True
            elif "SYS043" in scp_status.get("MessageId", ""):
                changed = True
            elif "SYS069" in scp_status.get("MessageId", ""):
                changed = False
        return scp_status, changed


class ExportCustomDefaultCommand():
    def __init__(self, idrac, module):
        self.idrac = idrac
        self.module = module
        self.idrac_firmware_version = get_idrac_firmware_version(self.idrac)

    def execute(self):
        command = self.module.params["command"]
        if not is_check_idrac_latest(self.idrac_firmware_version):
            self.module.exit_json(msg=CUSTOM_ERROR.format(command=command),
                                  skipped=True)
        validate_customdefault_input(self.module, command)
        scp_status = export_custom_defaults(self.module, self.idrac)
        return scp_status, False


class ExportCommand():
    def __init__(self, idrac, http_share, module):
        self.idrac = idrac
        self.http_share = http_share
        self.module = module

    def execute(self):
        if self.http_share:
            scp_status = run_export_import_scp_http(self.idrac, self.module)
        else:
            scp_status = export_scp_redfish(self.module, self.idrac)
        return scp_status, False


class PreviewCommand():
    def __init__(self, idrac, http_share, module):
        self.idrac = idrac
        self.http_share = http_share
        self.module = module

    def execute(self):
        scp_status = preview_scp_redfish(self.module, self.idrac, self.http_share, import_job_wait=False)
        return scp_status, False


def main():
    specs = get_argument_spec()

    module = IdracAnsibleModule(
        argument_spec=specs,
        required_one_of=[("share_name", "import_buffer")],
        required_if=[
            ["command", "export", ["share_name"]],
            ["command", "export_custom_defaults", ["share_name"]],
            ["proxy_support", True, ["proxy_server"]]
        ],
        supports_check_mode=True)

    validate_input(module, module.params.get("scp_components"))
    try:
        http_share = False
        msg = None
        command = module.params.get("command")
        if module.params.get("share_name") is not None:
            http_share = module.params["share_name"].lower().startswith(('http://', 'https://'))
        with iDRACRedfishAPI(module.params) as idrac:
            if command in ["import", "export", "preview"]:
                validate_scp_components(module, idrac)
            command_map = {
                "import": (ImportCommand, True),
                "export": (ExportCommand, True),
                "import_custom_defaults": (ImportCustomDefaultCommand, False),
                "export_custom_defaults": (ExportCustomDefaultCommand, False),
                "preview": (PreviewCommand, True)
            }
            command_obj_class, http_share_req = command_map.get(command)
            if http_share_req:
                command_obj = command_obj_class(idrac, http_share, module)
            else:
                command_obj = command_obj_class(idrac, module)
            scp_status, changed = command_obj.execute()

        if module.params.get('job_wait'):
            scp_status = strip_substr_dict(scp_status)
            if command in ["import", "export", "preview"]:
                msg = "Successfully {0}ed the Server Configuration Profile."
            else:
                command = command.split("_")[0]
                msg = "Successfully {0}ed the custom defaults Server Configuration Profile."
            module.exit_json(changed=changed, msg=msg.format(command), scp_status=scp_status)
        else:
            if command in ["import", "export", "preview"]:
                msg = "Successfully triggered the job to {0} the Server Configuration Profile."
            else:
                command = command.split("_")[0]
                msg = "Successfully triggered the job to {0} the custom defaults Server Configuration Profile."
            module.exit_json(msg=msg.format(command), scp_status=scp_status)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (ImportError, ValueError, RuntimeError, SSLValidationError,
            ConnectionError, KeyError, TypeError, IndexError, FileNotFoundError) as e:
        module.exit_json(msg=str(e), failed=True)


def get_argument_spec():
    return {
        "command": {"required": False, "type": 'str',
                    "choices": ['export', 'import', 'preview', 'import_custom_defaults', 'export_custom_defaults'], "default": 'export'},
        "job_wait": {"required": True, "type": 'bool'},
        "share_name": {"required": False, "type": 'str'},
        "share_user": {"required": False, "type": 'str'},
        "share_password": {"required": False, "type": 'str',
                           "aliases": ['share_pwd'], "no_log": True},
        "scp_components": {"type": "list", "required": False, "elements": "str",
                           "choices": ['ALL', 'IDRAC', 'BIOS', 'NIC', 'RAID', 'FC', 'InfiniBand', 'SupportAssist',
                                       'EventFilters', 'System', 'LifecycleController', 'AHCI', 'PCIeSSD'],
                           "default": ['ALL'], "aliases": ["target"]},
        "scp_file": {"required": False, "type": 'str'},
        "shutdown_type": {"required": False,
                          "choices": ['Graceful', 'Forced', 'NoReboot'],
                          "default": 'Graceful'},
        "end_host_power_state": {"required": False,
                                 "choices": ['On', 'Off'],
                                 "default": 'On'},
        "export_format": {"required": False, "type": 'str',
                          "choices": ['JSON', 'XML'], "default": 'XML'},
        "export_use": {"required": False, "type": 'str',
                       "choices": ['Default', 'Clone', 'Replace'], "default": 'Default'},
        "ignore_certificate_warning": {"required": False, "choices": ["ignore", "showerror"], "default": "ignore"},
        "include_in_export": {"required": False, "type": "str", "default": "default",
                              "choices": ["default", "readonly", "passwordhashvalues", "customtelemetry"]},
        "import_buffer": {"type": "str", "required": False},
        "proxy_support": {"type": "bool", "required": False, "default": False},
        "proxy_type": {"type": "str", "required": False, "choices": ["http", "socks4"], "default": "http"},
        "proxy_server": {"type": "str", "required": False},
        "proxy_port": {"type": "str", "required": False, "default": "80"},
        "proxy_username": {"type": "str", "required": False},
        "proxy_password": {"type": "str", "required": False, "no_log": True},
    }


if __name__ == '__main__':
    main()
