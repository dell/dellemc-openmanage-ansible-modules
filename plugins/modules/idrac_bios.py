#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.0.1
# Copyright (C) 2018-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_bios
short_description: Configure the BIOS attributes
version_added: "2.1.0"
description:
    - This module allows to configure the BIOS attributes.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
    share_name:
        type: str
        description: Network share or a local path.
    share_user:
        type: str
        description: Network share user name. Use the format 'user@domain' or 'domain\\user' if user is part of a domain.
            This option is mandatory for CIFS share.
    share_password:
        type: str
        description: Network share user password. This option is mandatory for CIFS share.
        aliases: ['share_pwd']
    share_mnt:
        type: str
        description: Local mount path of the network share with read-write permission for ansible user.
            This option is mandatory for network shares.
    boot_mode:
        type: str
        description:
        - (deprecated)Sets boot mode to BIOS or UEFI.
        - This option is deprecated, and will be removed in later version. Use I(attributes)
            for configuring the BIOS attributes.
        - I(boot_mode) is mutually exclusive with I(boot_sources).
        choices: [Bios, Uefi]
    nvme_mode:
        type: str
        description:
        - (deprecated)Configures the NVME mode in the iDRAC 9 based PowerEdge Servers.
        - This option is deprecated, and will be removed in later version. Use I(attributes)
            for configuring the BIOS attributes.
        - I(nvme_mode) is mutually exclusive with I(boot_sources).
        choices: [NonRaid, Raid]
    secure_boot_mode:
        type: str
        description:
        - (deprecated)Configures how the BIOS uses the Secure Boot Policy Objects in iDRAC 9 based PowerEdge Servers.
        - This option is deprecated, and will be removed in later version. Use I(attributes)
            for configuring the BIOS attributes.
        - I(secure_boot_mode) is mutually exclusive with I(boot_sources).
        choices: [AuditMode, DeployedMode, SetupMode, UserMode]
    onetime_boot_mode:
        type: str
        description:
        - (deprecated)Configures the one time boot mode setting.
        - This option is deprecated, and will be removed in later version. Use I(attributes)
            for configuring the BIOS attributes.
        - I(onetime_boot_mode) is mutually exclusive with I(boot_sources).
        choices: [Disabled, OneTimeBootSeq, OneTimeCustomBootSeqStr, OneTimeCustomHddSeqStr,
            OneTimeCustomUefiBootSeqStr, OneTimeHddSeq, OneTimeUefiBootSeq]
    boot_sequence:
        type: str
        description:
        - "(deprecated)Allows to set the boot sequence in  BIOS boot mode or Secure UEFI boot mode by rearranging the
        boot entries in Fully Qualified Device Descriptor (FQDD)."
        - TThis option is deprecated, and will be removed in later version. Use I(attributes)
            for configuring the BIOS attributes.
        - I(boot_sequence) is mutually exclusive with I(boot_sources).
    attributes:
        type: dict
        description:
        - Dictionary of BIOS attributes and value pair. Attributes should be
            part of the Redfish Dell BIOS Attribute Registry. Use
            U(https://I(idrac_ip)/redfish/v1/Systems/System.Embedded.1/Bios) to view the Redfish URI.
        - If deprecated options are provided and the same is repeated in I(attributes) then values in I(attributes) will
            take precedence.
        - I(attributes) is mutually exclusive with I(boot_sources).
    boot_sources:
        type: list
        elements: raw
        description:
        - List of boot devices to set the boot sources settings.
        - I(boot_sources) is mutually exclusive with I(attributes), I(boot_sequence),
            I(onetime_boot_mode), I(secure_boot_mode), I(nvme_mode), I(boot_mode).

requirements:
    - "omsdk >= 1.2.488"
    - "python >= 3.8.6"
author:
    - "Felix Stephen (@felixs88)"
    - "Anooja Vardhineni (@anooja-vardhineni)"
notes:
    - This module requires 'Administrator' privilege for I(idrac_user).
    - Run this module from a system that has direct access to DellEMC iDRAC.
    - This module supports C(check_mode).
"""


EXAMPLES = """
---
- name: Configure generic attributes of the BIOS
  dellemc.openmanage.idrac_bios:
    idrac_ip:   "192.168.0.1"
    idrac_user: "user_name"
    idrac_password:  "user_password"
    ca_path: "/path/to/ca_cert.pem"
    attributes:
      BootMode : "Bios"
      OneTimeBootMode: "Enabled"
      BootSeqRetry: "Enabled"

- name: Configure PXE generic attributes
  dellemc.openmanage.idrac_bios:
    idrac_ip:   "192.168.0.1"
    idrac_user: "user_name"
    idrac_password:  "user_password"
    ca_path: "/path/to/ca_cert.pem"
    attributes:
      PxeDev1EnDis: "Enabled"
      PxeDev1Protocol: "IPV4"
      PxeDev1VlanEnDis: "Enabled"
      PxeDev1VlanId: 1
      PxeDev1Interface: "NIC.Embedded.1-1-1"
      PxeDev1VlanPriority: 2

- name: Configure boot sources
  dellemc.openmanage.idrac_bios:
    idrac_ip:   "192.168.0.1"
    idrac_user: "user_name"
    idrac_password:  "user_password"
    ca_path: "/path/to/ca_cert.pem"
    boot_sources:
      - Name : "NIC.Integrated.1-2-3"
        Enabled : true
        Index : 0

- name: Configure multiple boot sources
  dellemc.openmanage.idrac_bios:
    idrac_ip:   "192.168.0.1"
    idrac_user: "user_name"
    idrac_password:  "user_password"
    ca_path: "/path/to/ca_cert.pem"
    boot_sources:
      - Name : "NIC.Integrated.1-1-1"
        Enabled : true
        Index : 0
      - Name : "NIC.Integrated.2-2-2"
        Enabled : true
        Index : 1
      - Name : "NIC.Integrated.3-3-3"
        Enabled : true
        Index : 2

- name: Configure boot sources - Enabling
  dellemc.openmanage.idrac_bios:
    idrac_ip:   "192.168.0.1"
    idrac_user: "user_name"
    idrac_password:  "user_password"
    ca_path: "/path/to/ca_cert.pem"
    boot_sources:
      - Name : "NIC.Integrated.1-1-1"
        Enabled : true

- name: Configure boot sources - Index
  dellemc.openmanage.idrac_bios:
    idrac_ip:   "192.168.0.1"
    idrac_user: "user_name"
    idrac_password:  "user_password"
    ca_path: "/path/to/ca_cert.pem"
    boot_sources:
      - Name : "NIC.Integrated.1-1-1"
        Index : 0
"""


RETURN = r'''
---
msg:
    description: Configures the BIOS configuration attributes.
    returned: success
    type: dict
    sample: {
       "@odata.context": "/redfish/v1/$metadata#DellJob.DellJob",
       "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_873888162305",
       "@odata.type": "#DellJob.v1_0_0.DellJob",
       "CompletionTime": "2020-04-20T18:50:20",
       "Description": "Job Instance",
       "EndTime": null,
       "Id": "JID_873888162305",
       "JobState": "Completed",
       "JobType": "ImportConfiguration",
       "Message": "Successfully imported and applied Server Configuration Profile.",
       "MessageArgs": [],
       "MessageId": "SYS053",
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
import tempfile
import json
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection, idrac_auth_params
from ansible.module_utils.basic import AnsibleModule
try:
    from omdrivers.enums.iDRAC.BIOS import (BootModeTypes, NvmeModeTypes, SecureBootModeTypes,
                                            OneTimeBootModeTypes)
    from omdrivers.enums.iDRAC.iDRACEnums import BootModeEnum
    from omsdk.sdkfile import file_share_manager
    from omsdk.sdkcreds import UserCredentials
except ImportError:
    pass


def run_server_bios_config(idrac, module):
    msg = {}
    temp_dir = tempfile.gettempdir() + os.sep
    share_name = module.params.get('share_name')
    share_path = share_name if share_name is not None else temp_dir

    idrac.use_redfish = True
    upd_share = file_share_manager.create_share_obj(share_path=share_path,
                                                    mount_point=module.params['share_mnt'],
                                                    isFolder=True,
                                                    creds=UserCredentials(
                                                        module.params['share_user'],
                                                        module.params['share_password'])
                                                    )
    if not upd_share.IsValid:
        module.fail_json(msg="Unable to access the share. Ensure that the share name, "
                             "share mount, and share credentials provided are correct.")
    if module.params['boot_sources']:
        _validate_params(module.params['boot_sources'])
        if module.check_mode:
            idrac.config_mgr.is_change_applicable()
        msg = idrac.config_mgr.configure_boot_sources(
            input_boot_devices=module.params['boot_sources'])
        return msg

    idrac.config_mgr.set_liason_share(upd_share)

    if module.params['boot_mode'] and not (module.params['attributes'] and 'BootMode' in module.params['attributes']):
        idrac.config_mgr.configure_boot_mode(boot_mode=BootModeTypes[module.params['boot_mode']])

    if module.params['nvme_mode'] and not (module.params['attributes'] and 'NvmeMode' in module.params['attributes']):
        idrac.config_mgr.configure_nvme_mode(nvme_mode=NvmeModeTypes[module.params['nvme_mode']])

    if module.params['secure_boot_mode'] and not (module.params['attributes'] and 'SecureBootMode' in
                                                  module.params['attributes']):
        idrac.config_mgr.configure_secure_boot_mode(
            secure_boot_mode=SecureBootModeTypes[module.params['secure_boot_mode']])

    if module.params['onetime_boot_mode'] and not (module.params['attributes'] and 'OneTimeBootMode' in
                                                   module.params['attributes']):
        idrac.config_mgr.configure_onetime_boot_mode(
            onetime_boot_mode=OneTimeBootModeTypes[module.params['onetime_boot_mode']])

    if module.params["boot_mode"] is not None and module.params["boot_sequence"] is not None:
        idrac.config_mgr.configure_boot_sequence(
            boot_mode=BootModeEnum[module.params['boot_mode']],
            boot_sequence=module.params['boot_sequence']
        )

    if module.params['attributes']:
        msg['msg'] = idrac.config_mgr.configure_bios(
            bios_attr_val=module.params['attributes'])

    if module.check_mode:
        msg = idrac.config_mgr.is_change_applicable()
    else:
        msg = idrac.config_mgr.apply_changes(reboot=True)
    return msg


def _validate_params(params):
    """
    Validate list of dict params.
    :param params: Ansible list of dict
    :return: bool or error.
    """
    fields = [
        {"name": "Name", "type": str, "required": True},
        {"name": "Index", "type": int, "required": False, "min": 0},
        {"name": "Enabled", "type": bool, "required": False}
    ]
    default = ['Name', 'Index', 'Enabled']
    for attr in params:
        if not isinstance(attr, dict):
            msg = "{0} must be of type: {1}. {2} ({3}) provided.".format(
                "attribute values", dict, attr, type(attr))
            return msg
        elif all(k in default for k in attr.keys()):
            msg = check_params(attr, fields)
            return msg
        else:
            msg = "attribute keys must be one of the {0}.".format(default)
            return msg
    msg = _validate_name_index_duplication(params)
    return msg


def _validate_name_index_duplication(params):
    """
    Validate for duplicate names and indices.
    :param params: Ansible list of dict
    :return: bool or error.
    """
    msg = ""
    for i in range(len(params) - 1):
        for j in range(i + 1, len(params)):
            if params[i]['Name'] == params[j]['Name']:
                msg = "duplicate name  {0}".format(params[i]['Name'])
                return msg
    return msg


def check_params(each, fields):
    """
    Each dictionary parameters validation as per the rule defined in fields.
    :param each: validating each dictionary
    :param fields: list of dictionary which has the set of rules.
    :return: tuple which has err and message
    """
    msg = ""
    for f in fields:
        if f['name'] not in each and f["required"] is False:
            continue
        if not f["name"] in each and f["required"] is True:
            msg = "{0} is required and must be of type: {1}".format(f['name'], f['type'])
        elif not isinstance(each[f["name"]], f["type"]):
            msg = "{0} must be of type: {1}. {2} ({3}) provided.".format(
                  f['name'], f['type'], each[f['name']], type(each[f['name']]))
        elif f['name'] in each and isinstance(each[f['name']], int) and 'min' in f:
            if each[f['name']] < f['min']:
                msg = "{0} must be greater than or equal to: {1}".format(f['name'], f['min'])
    return msg


def main():
    mutual_exclusive_args = [['boot_sources', 'attributes'], ['boot_sources', 'secure_boot_mode'],
                             ['boot_sources', 'boot_mode'], ['boot_sources', 'boot_sequence'],
                             ['boot_sources', 'nvme_mode'], ['boot_sources', 'onetime_boot_mode']]
    specs = {
        "share_name": {"required": False, "type": 'str'},
        "share_user": {"required": False, "type": 'str'},
        "share_password": {"required": False, "type": 'str', "aliases": ['share_pwd'], "no_log": True},
        "share_mnt": {"required": False, "type": 'str'},
        "boot_mode": {"required": False, "choices": ['Bios', 'Uefi']},
        "nvme_mode": {"required": False, "choices": ['NonRaid', 'Raid']},
        "secure_boot_mode": {"required": False, "choices": ['AuditMode', 'DeployedMode', 'SetupMode', 'UserMode']},
        "onetime_boot_mode": {"required": False, "choices": ['Disabled', 'OneTimeBootSeq',
                                                             'OneTimeCustomBootSeqStr', 'OneTimeCustomHddSeqStr',
                                                             'OneTimeCustomUefiBootSeqStr', 'OneTimeHddSeq',
                                                             'OneTimeUefiBootSeq']},
        "boot_sequence": {"required": False, "type": "str"},
        "attributes": {"required": False, "type": 'dict'},
        "boot_sources": {"required": False, "type": 'list', 'elements': 'raw'}
    }
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        mutually_exclusive=mutual_exclusive_args,
        supports_check_mode=True
    )
    try:
        with iDRACConnection(module.params) as idrac:
            msg = run_server_bios_config(idrac, module)
            changed, failed = False, False
            if msg.get('Status') == "Success":
                changed = True
                if msg.get('Message') == "No changes found to commit!":
                    changed = False
            elif msg.get('Status') == "Failed":
                failed = True
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except AttributeError as err:
        if "NoneType" in str(err):
            module.fail_json(msg="Unable to access the share. Ensure that the share name, "
                                 "share mount, and share credentials provided are correct.")
    except (RuntimeError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError) as e:
        module.fail_json(msg=str(e))
    module.exit_json(msg=msg, changed=changed, failed=failed)


if __name__ == '__main__':
    main()
