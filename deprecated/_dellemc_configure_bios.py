#!/usr/bin/python
# _*_ coding: utf-8 _*_

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0
# Copyright (C) 2018-2019 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['deprecated'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_configure_bios
short_description: Configure the BIOS configuration attributes.
version_added: "2.3"
deprecated:
  removed_in: "2.13"
  why: Replaced with M(idrac_bios).
  alternative: Use M(idrac_bios) instead.
description:
    - Configure the BIOS configuration attributes.
options:
    idrac_ip:
        required: True
        description: iDRAC IP Address.
    idrac_user:
        required: True
        description: iDRAC username.
    idrac_password:
        required: True
        description: iDRAC user password.
        aliases: ['idrac_pwd']
    idrac_port:
        required: False
        description: iDRAC port.
        default: 443
    share_name:
        required: False
        description: Network share or a local path.
    share_user:
        required: False
        description: Network share user in the format 'user@domain' or 'domain\\user' if user is
            part of a domain else 'user'. This option is mandatory for CIFS Network Share.
    share_password:
        required: False
        description: Network share user password. This option is mandatory for CIFS Network Share.
        aliases: ['share_pwd']
    share_mnt:
        required: False
        description: Local mount path of the network share with read-write permission for ansible user.
            This option is mandatory for Network Share.
    boot_mode:
        required: False
        description:
        - (deprecated)Configures the boot mode to BIOS or UEFI.
        - This option has been deprecated, and will be removed in later version. Please use the I(attributes)
            for BIOS attributes configuration instead.
        - I(boot_mode) is mutually exclusive with I(boot_sources).
        choices: [Bios, Uefi]
    nvme_mode:
        required: False
        description:
        - (deprecated)Configures the NVME mode in the 14th Generation of PowerEdge Servers.
        - This option has been deprecated, and will be removed in later version. Please use the I(attributes)
            for BIOS attributes configuration instead.
        - I(nvme_mode) is mutually exclusive with I(boot_sources).
        choices: [NonRaid, Raid]
    secure_boot_mode:
        required: False
        description:
        - (deprecated)Configures how the BIOS uses the Secure Boot Policy Objects in the 14th Generation
            of PowerEdge Servers.
        - This option has been deprecated, and will be removed in later version. Please use the I(attributes)
            for BIOS attributes configuration instead.
        - I(secure_boot_mode) is mutually exclusive with I(boot_sources).
        choices: [AuditMode, DeployedMode, SetupMode, UserMode]
    onetime_boot_mode:
        required: False
        description:
        - (deprecated)Configures the one time boot mode setting.
        - This option has been deprecated, and will be removed in later version. Please use the I(attributes)
            for BIOS attributes configuration instead.
        - I(onetime_boot_mode) is mutually exclusive with I(boot_sources).
        choices: [Disabled, OneTimeBootSeq, OneTimeCustomBootSeqStr, OneTimeCustomHddSeqStr,
            OneTimeCustomUefiBootSeqStr, OneTimeHddSeq, OneTimeUefiBootSeq]
    boot_sequence:
        required: False
        description:
        - (deprecated)Boot devices FQDDs in the sequential order for BIOS or UEFI Boot Sequence.
            Ensure that I(boot_mode) option is provided to determine the appropriate boot sequence to be applied.
        - This option has been deprecated, and will be removed in later version. Please use the I(attributes) or
            I(boot_sources) for Boot Sequence modification instead.
        - I(boot_sequence) is mutually exclusive with I(boot_sources).
    attributes:
        required: False
        description:
        - Dictionary of bios attributes and value pair. Attributes should be
            part of the Redfish Dell BIOS Attribute Registry. Redfish URI to view Bios attributes
            U(https://I(idrac_ip)/redfish/v1/Systems/System.Embedded.1/Bios)
        - If deprecated options are given and the same is repeated in I(attributes) then values in I(attributes) will
            take precedence.
        - I(attributes) is mutually exclusive with I(boot_sources).
    boot_sources:
        required: False
        description:
        - List of boot devices to set the boot sources settings. boot devices are dictionary.
        - I(boot_sources) is mutually exclusive with I(attributes), I(boot_sequence),
            I(onetime_boot_mode), I(secure_boot_mode), I(nvme_mode), I(boot_mode).

requirements:
    - "omsdk"
    - "python >= 2.7.5"
author: "Felix Stephen (@felixs88)"

"""


EXAMPLES = """
---
- name: Configure Bios Generic Attributes
  dellemc_configure_bios:
    idrac_ip:   "xx.xx.xx.xx"
    idrac_user: "xxxx"
    idrac_password:  "xxxxxxxx"
    attributes:
      BootMode : "Bios"
      OneTimeBootMode: "Enabled"
      BootSeqRetry: "Enabled"

- name: Configure PXE Generic Attributes
  dellemc_configure_bios:
    idrac_ip:   "xx.xx.xx.xx"
    idrac_user: "xxxx"
    idrac_password:  "xxxxxxxx"
    attributes:
      PxeDev1EnDis: "Enabled"
      PxeDev1Protocol: "IPV4"
      PxeDev1VlanEnDis: "Enabled"
      PxeDev1VlanId: x
      PxeDev1Interface: "NIC.Embedded.x-x-x"
      PxeDev1VlanPriority: x

- name: Configure Boot Sources
  dellemc_configure_bios:
    idrac_ip:   "xx.xx.xx.xx"
    idrac_user: "xxxx"
    idrac_password:  "xxxxxxxx"
    boot_sources:
      - Name : "NIC.Integrated.x-x-x"
        Enabled : true
        Index : 0

- name: Configure Boot Sources
  dellemc_configure_bios:
    idrac_ip:   "xx.xx.xx.xx"
    idrac_user: "xxxx"
    idrac_password:  "xxxxxxxx"
    boot_sources:
      - Name : "NIC.Integrated.x-x-x"
        Enabled : true
        Index : 0
      - Name : "NIC.Integrated.x-x-x"
        Enabled : true
        Index : 1
      - Name : "NIC.Integrated.x-x-x"
        Enabled : true
        Index : 2

- name: Configure Boot Sources - Enabled
  dellemc_configure_bios:
    idrac_ip:   "xx.xx.xx.xx"
    idrac_user: "xxxx"
    idrac_password:  "xxxxxxxx"
    boot_sources:
      - Name : "NIC.Integrated.x-x-x"
        Enabled : true

- name: Configure Boot Sources - Index
  dellemc_configure_bios:
    idrac_ip:   "xx.xx.xx.xx"
    idrac_user: "xxxx"
    idrac_password:  "xxxxxxxx"
    boot_sources:
      - Name : "NIC.Integrated.x-x-x"
        Index : 0
"""


RETURNS = """
dest:
    description: Configures the BIOS configuration attributes.
    returned: success
    type: string
"""


import os
import tempfile
from ansible.module_utils.remote_management.dellemc.dellemc_idrac import iDRACConnection
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
    """
    Get Lifecycle Controller status

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    err = False
    temp_dir = tempfile.gettempdir() + os.sep
    share_name = module.params.get('share_name')
    share_path = share_name if share_name is not None else temp_dir
    deprecation_warning_message = 'boot_mode, nvme_mode, secure_boot_mode, onetime_boot_mode and boot_sequence options ' \
                                  'have been deprecated, and will be removed. ' \
                                  'Please use the attributes option for Bios attributes configuration instead.'
    try:
        idrac.use_redfish = True
        upd_share = file_share_manager.create_share_obj(share_path=share_path,
                                                        mount_point=module.params['share_mnt'],
                                                        isFolder=True,
                                                        creds=UserCredentials(
                                                            module.params['share_user'],
                                                            module.params['share_password'])
                                                        )
        if module.params['boot_sources']:
            err, message = _validate_params(module.params['boot_sources'])
            if err:
                msg['changed'] = False
                msg['failed'] = True
                msg['msg'] = {}
                msg['msg']['Message'] = message
                msg['msg']['Status'] = "Failed"
                return msg, err
            if module.check_mode:
                msg['msg'] = idrac.config_mgr.is_change_applicable()
                if 'changes_applicable' in msg['msg']:
                    msg['changed'] = msg['msg']['changes_applicable']
                    return msg, err
            msg['msg'] = idrac.config_mgr.configure_boot_sources(
                input_boot_devices=module.params['boot_sources'])

            if "Status" in msg['msg']:
                if msg['msg']['Status'] == "Success":
                    msg['changed'] = True
                    if "Message" in msg['msg']:
                        if msg['msg']['Message'] == "No changes found to commit!":
                            msg['changed'] = False
                        elif msg['msg']['Message'] == "No changes found to apply.":
                            msg['changed'] = False
                else:
                    msg['failed'] = True
                    err = True
                    msg['changed'] = False
            return msg, err

        set_liason = idrac.config_mgr.set_liason_share(upd_share)
        if set_liason['Status'] == "Failed":
            try:
                message = set_liason['Data']['Message']
            except (IndexError, KeyError):
                message = set_liason['Message']
            err = True
            msg['msg'] = "Error: {}".format(message)
            msg['failed'] = True
            return msg, err
        if (module.params['boot_mode'] or module.params['nvme_mode']
                or ['secure_boot_mode'] or module.params['onetime_boot_mode'] or module.params["boot_mode"]):
            module.deprecate(deprecation_warning_message, version='2.9')

        if module.params['boot_mode'] and not (module.params['attributes']
                                               and 'BootMode' in module.params['attributes']):
            idrac.config_mgr.configure_boot_mode(
                boot_mode=BootModeTypes[module.params['boot_mode']])

        if module.params['nvme_mode'] and not (module.params['attributes']
                                               and 'NvmeMode' in module.params['attributes']):
            idrac.config_mgr.configure_nvme_mode(
                nvme_mode=NvmeModeTypes[module.params['nvme_mode']])

        if module.params['secure_boot_mode'] and not (module.params['attributes']
                                                      and 'SecureBootMode' in module.params['attributes']):
            idrac.config_mgr.configure_secure_boot_mode(
                secure_boot_mode=SecureBootModeTypes[module.params['secure_boot_mode']])

        if module.params['onetime_boot_mode'] and not (module.params['attributes']
                                                       and 'OneTimeBootMode' in module.params['attributes']):
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
            if msg['msg']['Status'] != 'Success':
                err = True
                msg['failed'] = True
                return msg, err

        if module.check_mode:
            msg['msg'] = idrac.config_mgr.is_change_applicable()
            if 'changes_applicable' in msg['msg']:
                msg['changed'] = msg['msg']['changes_applicable']
        else:
            msg['msg'] = idrac.config_mgr.apply_changes(reboot=True)

            if "Status" in msg['msg']:
                if msg['msg']['Status'] == "Success":
                    msg['changed'] = True
                    if "Message" in msg['msg']:
                        if msg['msg']['Message'] == "No changes found to commit!":
                            msg['changed'] = False
                        elif msg['msg']['Message'] == "No changes found to apply.":
                            msg['changed'] = False
                else:
                    msg['failed'] = True
    except Exception as e:
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True
    return msg, err


def _validate_params(params):
    """
    Validate list of dict params.
    :param params: Ansible list of dict
    :return: bool or error.
    """
    err, msg = False, ""
    fields = [
        {"name": "Name", "type": str, "required": True},
        {"name": "Index", "type": int, "required": False, "min": 0},
        {"name": "Enabled", "type": bool, "required": False}
    ]
    default = ['Name', 'Index', 'Enabled']
    for attr in params:
        if not isinstance(attr, dict):
            err, msg = True, "{} must be of type: {}. {} ({}) provided.".format(
                "attribute values", dict, attr, type(attr))
            return err, msg
        elif all(k in default for k in attr.keys()):
            err, msg = check_params(attr, fields)
            if err:
                return err, msg
        else:
            err, msg = True, "attribute keys must be one of the {}.".format(default)
            return err, msg
    err, msg = _validate_name_index_duplication(params)
    return err, msg


def _validate_name_index_duplication(params):
    """
    Validate for duplicate names and indices.
    :param params: Ansible list of dict
    :return: bool or error.
    """
    err, msg = False, ""
    for i in range(len(params) - 1):
        for j in range(i + 1, len(params)):
            if params[i]['Name'] == params[j]['Name']:
                err, msg = True, "duplicate name  {}".format(params[i]['Name'])
                return err, msg
    return err, msg


def check_params(each, fields):
    """
    Each dictionary parameters validation as per the rule defined in fields.
    :param each: validating each dictionary
    :param fields: list of dictionary which has the set of rules.
    :return: tuple which has err and message
    """
    err, msg = False, ""
    for f in fields:
        if f['name'] not in each and f["required"] is False:
            continue
        if not f["name"] in each and f["required"] is True:
            err, msg = True, "{} is required and must be of type: {}".format(f['name'],
                                                                             f['type'])
        elif not isinstance(each[f["name"]], f["type"]):
            err, msg = True, "{} must be of type: {}. {} ({}) provided.".format(
                f['name'], f['type'], each[f['name']], type(each[f['name']]))
        elif f['name'] in each and isinstance(each[f['name']], int) and 'min' in f:
            if each[f['name']] < f['min']:
                err, msg = True, "{} must be greater than or equal to: {}".format(f['name'],
                                                                                  f['min'])
    return err, msg


# Main
def main():
    mutual_exclusive_args = [['boot_sources', 'attributes'], ['boot_sources', 'secure_boot_mode'],
                             ['boot_sources', 'boot_mode'], ['boot_sources', 'boot_sequence'],
                             ['boot_sources', 'nvme_mode'], ['boot_sources', 'onetime_boot_mode']]
    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_password=dict(required=True, type='str', aliases=['idrac_pwd'], no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Export Destination
            share_name=dict(required=False, type='str'),
            share_password=dict(required=False, type='str', aliases=['share_pwd'], no_log=True),
            share_user=dict(required=False, type='str'),
            share_mnt=dict(required=False, type='str'),

            # Bios configuration Attributes
            boot_mode=dict(required=False, choices=['Bios', 'Uefi'], default=None),
            nvme_mode=dict(required=False, choices=['NonRaid', 'Raid'], default=None),
            secure_boot_mode=dict(required=False, choices=['AuditMode', 'DeployedMode', 'SetupMode', 'UserMode'],
                                  default=None),
            onetime_boot_mode=dict(required=False, choices=['Disabled', 'OneTimeBootSeq', 'OneTimeCustomBootSeqStr',
                                                            'OneTimeCustomHddSeqStr', 'OneTimeCustomUefiBootSeqStr',
                                                            'OneTimeHddSeq', 'OneTimeUefiBootSeq'], default=None),

            # Bios Boot Sequence
            boot_sequence=dict(required=False, type="str", default=None),
            attributes=dict(required=False, type='dict'),
            boot_sources=dict(required=False, type='list')
        ),
        mutually_exclusive=mutual_exclusive_args,
        supports_check_mode=True)
    module.deprecate("The 'dellemc_configure_bios' module has been deprecated. "
                     "Use 'idrac_bios instead",
                     version=2.13)

    try:
        with iDRACConnection(module.params) as idrac:
            msg, err = run_server_bios_config(idrac, module)
    except (ImportError, ValueError, RuntimeError) as e:
        module.fail_json(msg=str(e))

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
