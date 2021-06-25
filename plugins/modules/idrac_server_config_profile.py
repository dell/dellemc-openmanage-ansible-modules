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
module: idrac_server_config_profile
short_description: Export or Import iDRAC Server Configuration Profile (SCP)
version_added: "2.1.0"
description:
  - Export the Server Configuration Profile (SCP) from the iDRAC or import from a
    network share (CIFS, NFS, HTTP, HTTPS) or a local file.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
  command:
    description:
      - If C(import), will perform SCP import operations.
      - If C(export), will perform SCP export operations.
    type: str
    choices: ['import', 'export']
    default: 'export'
  job_wait:
    description: Whether to wait for job completion or not.
    type: bool
    required: True
  share_name:
    description:
      - Network share or local path.
      - CIFS, NFS, HTTP, and HTTPS network share types are supported.
      - OMSDK is not required if HTTP or HTTPS location is used for I(share_name).
    type: str
    required: True
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
      - This option is mandatory if I(command) is C(import).
      - The default format <idrac_ip>_YYmmdd_HHMMSS_scp is used if this option is not specified for C(import).
      - I(export_format) is used if the valid extension file is not provided for C(import).
    type: str
  scp_components:
    description:
      - If C(ALL), this module exports or imports all components configurations from SCP file.
      - If C(IDRAC), this module exports or imports iDRAC configuration from SCP file.
      - If C(BIOS), this module exports or imports BIOS configuration from SCP file.
      - If C(NIC), this module exports or imports NIC configuration from SCP file.
      - If C(RAID), this module exports or imports RAID configuration from SCP file.
    type: str
    choices: ['ALL', 'IDRAC', 'BIOS', 'NIC', 'RAID']
    default: 'ALL'
  shutdown_type:
    description:
      - This option is applicable for C(import) command.
      - If C(Graceful), it gracefully shuts down the server.
      - If C(Forced),  it forcefully shuts down the server.
      - If C(NoReboot), it does not reboot the server.
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
    description: Specify the output file format. This option is applicable for C(export) command.
    type: str
    choices: ['JSON',  'XML']
    default: 'XML'
  export_use:
    description: Specify the type of server configuration profile (SCP) to be exported.
      This option is applicable for C(export) command.
    type: str
    choices: ['Default',  'Clone', 'Replace']
    default: 'Default'

requirements:
  - "omsdk"
  - "python >= 2.7.5"
author: "Jagadeesh N V(@jagadeeshnv)"
notes:
    - This module requires 'Administrator' privilege for I(idrac_user).
    - Run this module from a system that has direct access to Dell EMC iDRAC.
    - This module does not support C(check_mode).
'''

EXAMPLES = r'''
---
- name: Export SCP with IDRAC components in JSON format to a local path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    share_name: "/scp_folder"
    scp_components: IDRAC
    scp_file: example_file
    export_format: JSON
    export_use: Clone
    job_wait: True

- name: Import SCP with IDRAC components in JSON format from a local path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    share_name: "/scp_folder"
    command: import
    scp_components: "IDRAC"
    scp_file: example_file.json
    shutdown_type: Graceful
    end_host_power_state: "On"
    job_wait: False

- name: Export SCP with BIOS components in XML format to a NFS share path with auto-generated file name
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    share_name: "192.168.0.2:/share"
    scp_components: "BIOS"
    export_format: XML
    export_use: Default
    job_wait: True

- name: Import SCP with BIOS components in XML format from a NFS share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    share_name: "192.168.0.2:/share"
    command: import
    scp_components: "BIOS"
    scp_file: 192.168.0.1_20210618_162856.xml
    shutdown_type: NoReboot
    end_host_power_state: "Off"
    job_wait: False

- name: Export SCP with RAID components in XML format to a CIFS share path with share user domain name
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    share_name: "\\\\192.168.0.2\\share"
    share_user: share_username@domain
    share_password: share_password
    share_mnt: /mnt/cifs
    scp_file: example_file.xml
    scp_components: "RAID"
    export_format: XML
    export_use: Default
    job_wait: True

- name: Import SCP with RAID components in XML format from a CIFS share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    share_name: "\\\\192.168.0.2\\share"
    share_user: share_username
    share_password: share_password
    share_mnt: /mnt/cifs
    command: import
    scp_components: "RAID"
    scp_file: example_file.xml
    shutdown_type: Forced
    end_host_power_state: "On"
    job_wait: True

- name: Export SCP with ALL components in JSON format to a HTTP share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    share_name: "http://192.168.0.3/share"
    share_user: share_username
    share_password: share_password
    scp_file: example_file.json
    scp_components: ALL
    export_format: JSON
    job_wait: False

- name: Import SCP with ALL components in JSON format from a HTTP share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    command: import
    share_name: "http://192.168.0.3/share"
    share_user: share_username
    share_password: share_password
    scp_file: example_file.json
    shutdown_type: Graceful
    end_host_power_state: "On"
    job_wait: True

- name: Export SCP with ALL components in XML format to a HTTPS share path without SCP file name
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    share_name: "https://192.168.0.4/share"
    share_user: share_username
    share_password: share_password
    scp_components: ALL
    export_format: XML
    export_use: Replace
    job_wait: True

- name: Import SCP with ALL components in XML format from a HTTPS share path
  dellemc.openmanage.idrac_server_config_profile:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    command: import
    share_name: "https://192.168.0.4/share"
    share_user: share_username
    share_password: share_password
    scp_file: 192.168.0.1_20160618_164647.xml
    shutdown_type: Graceful
    end_host_power_state: "On"
    job_wait: False
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
import json
from datetime import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.parse import urlparse
try:
    from omsdk.sdkfile import file_share_manager
    from omsdk.sdkcreds import UserCredentials
    from omdrivers.enums.iDRAC.iDRACEnums import (SCPTargetEnum, EndHostPowerStateEnum,
                                                  ShutdownTypeEnum, ExportFormatEnum, ExportUseEnum)
except ImportError:
    pass


def run_import_server_config_profile(idrac, module):
    """Import Server Configuration Profile from a network share."""
    target = SCPTargetEnum[module.params['scp_components']]
    job_wait = module.params['job_wait']
    end_host_power_state = EndHostPowerStateEnum[module.params['end_host_power_state']]
    shutdown_type = ShutdownTypeEnum[module.params['shutdown_type']]
    idrac.use_redfish = True

    try:
        myshare = file_share_manager.create_share_obj(
            share_path="{0}{1}{2}".format(module.params['share_name'], os.sep, module.params['scp_file']),
            creds=UserCredentials(module.params['share_user'],
                                  module.params['share_password']), isFolder=False)
        import_status = idrac.config_mgr.scp_import(myshare,
                                                    target=target, shutdown_type=shutdown_type,
                                                    end_host_power_state=end_host_power_state,
                                                    job_wait=job_wait)
        if not import_status or import_status.get('Status') != "Success":
            module.fail_json(msg='Failed to import scp.', scp_status=import_status)
    except RuntimeError as e:
        module.fail_json(msg=str(e))
    return import_status


def run_export_server_config_profile(idrac, module):
    """Export Server Configuration Profile to a network share."""
    export_format = ExportFormatEnum[module.params['export_format']]
    scp_file = module.params['scp_file']
    if scp_file:
        scp_file_name_format = scp_file
        if not str(scp_file.lower()).endswith(('.xml', '.json')):
            scp_file_name_format = "{0}.{1}".format(scp_file, module.params['export_format'].lower())
    else:
        scp_file_name_format = "%ip_%Y%m%d_%H%M%S_scp.{0}".format(module.params['export_format'].lower())
    target = SCPTargetEnum[module.params['scp_components']]
    export_use = ExportUseEnum[module.params['export_use']]
    idrac.use_redfish = True

    try:
        myshare = file_share_manager.create_share_obj(share_path=module.params['share_name'],
                                                      creds=UserCredentials(module.params['share_user'],
                                                                            module.params['share_password']),
                                                      isFolder=True)
        scp_file_name = myshare.new_file(scp_file_name_format)
        export_status = idrac.config_mgr.scp_export(scp_file_name, target=target, export_format=export_format,
                                                    export_use=export_use, job_wait=module.params['job_wait'])
        if not export_status or export_status.get('Status') != "Success":
            module.fail_json(msg='Failed to export scp.', scp_status=export_status)
    except RuntimeError as e:
        module.fail_json(msg=str(e))
    return export_status


def response_format_change(response, params, file_name):
    resp = {}
    if params["job_wait"]:
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
        if params["command"] == "export":
            response["file"] = "{0}{1}{2}".format(params["share_name"], os.sep, file_name)
        response["retval"] = True
    else:
        location = response.headers.get("Location")
        job_id = location.split("/")[-1]
        resp["Data"] = {"StatusCode": response.status_code, "joburi": job_id, "next_uri": location}
        resp["Job"] = {"JobId": job_id, "ResourceURI": location}
        resp["Message"] = "none"
        resp["Return"] = "JobCreated"
        resp["Status"] = "Success"
        resp["StatusCode"] = response.status_code
        if params["command"] == "export":
            resp["file"] = "{0}{1}{2}".format(params["share_name"], os.sep, file_name)
        resp["retval"] = True
        response = resp
    return response


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
    command = module.params["command"]
    if command == "import":
        scp_response = idrac.import_scp_share(shutdown_type=module.params["shutdown_type"],
                                              host_powerstate=module.params["end_host_power_state"],
                                              job_wait=module.params["job_wait"],
                                              target=module.params["scp_components"], share=share, )
    else:
        if scp_file:
            if not str(scp_file.lower()).endswith(('.xml', '.json')):
                scp_file_name_format = "{0}.{1}".format(scp_file, module.params['export_format'].lower())
        else:
            d = datetime.now()
            scp_file_name_format = "{0}_{1}{2}{3}_{4}{5}{6}_scp.{7}".format(
                module.params["idrac_ip"], d.date().year, d.date().month, d.date().day,
                d.time().hour, d.time().minute, d.time().second,
                module.params['export_format'].lower())
        share["file_name"] = scp_file_name_format
        scp_response = idrac.export_scp(export_format=module.params["export_format"],
                                        export_use=module.params["export_use"],
                                        target=module.params["scp_components"],
                                        job_wait=module.params["job_wait"], share=share, )
    scp_response = response_format_change(scp_response, module.params,
                                          scp_file_name_format)
    if isinstance(scp_response, dict) and scp_response.get("TaskStatus") == "Critical":
        module.fail_json(msg="Failed to {0} scp.".format(command), scp_status=scp_response)
    return scp_response


def main():
    module = AnsibleModule(
        argument_spec={
            "idrac_ip": {"required": True, "type": 'str'},
            "idrac_user": {"required": True, "type": 'str'},
            "idrac_password": {"required": True, "type": 'str',
                               "aliases": ['idrac_pwd'], "no_log": True},
            "idrac_port": {"required": False, "default": 443, "type": 'int'},

            "command": {"required": False, "type": 'str',
                        "choices": ['export', 'import'], "default": 'export'},
            "job_wait": {"required": True, "type": 'bool'},

            "share_name": {"required": True, "type": 'str'},
            "share_user": {"required": False, "type": 'str'},
            "share_password": {"required": False, "type": 'str',
                               "aliases": ['share_pwd'], "no_log": True},
            "scp_components": {"required": False,
                               "choices": ['ALL', 'IDRAC', 'BIOS', 'NIC', 'RAID'],
                               "default": 'ALL'},

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
                           "choices": ['Default', 'Clone', 'Replace'], "default": 'Default'}
        },
        required_if=[
            ["command", "import", ["scp_file"]]
        ],
        supports_check_mode=False)

    try:
        changed = False
        http_share = module.params["share_name"].lower().startswith(('http://', 'https://'))
        with iDRACConnection(module.params) if not http_share else iDRACRedfishAPI(module.params) as idrac:
            command = module.params['command']
            if command == 'import':
                if http_share:
                    scp_status = run_export_import_scp_http(idrac, module)
                    if isinstance(scp_status, dict):
                        if scp_status.get("MessageId") == "SYS069":
                            changed = False
                        elif scp_status.get("MessageId") == "SYS053":
                            changed = True
                else:
                    scp_status = run_import_server_config_profile(idrac, module)
                    if "No changes were applied" not in scp_status.get('Message', ""):
                        changed = True
                    elif scp_status.get("MessageId") == "SYS043":
                        changed = True
                    elif scp_status.get("MessageId") == "SYS069":
                        changed = False
            else:
                if http_share:
                    scp_status = run_export_import_scp_http(idrac, module)
                else:
                    scp_status = run_export_server_config_profile(idrac, module)

        if module.params.get('job_wait'):
            msg = "Successfully {0}ed the Server Configuration Profile."
            module.exit_json(changed=changed, msg=msg.format(command), scp_status=scp_status)
        else:
            msg = "Successfully triggered the job to {0} the Server Configuration Profile."
            module.exit_json(msg=msg.format(command), scp_status=scp_status)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (ImportError, ValueError, RuntimeError, SSLValidationError,
            ConnectionError, KeyError, TypeError, IndexError) as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
