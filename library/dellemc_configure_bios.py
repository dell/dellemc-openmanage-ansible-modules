#!/usr/bin/python
# _*_ coding: utf-8 _*_

#
# Dell EMC OpenManage Ansible Modules
# Version 1.0
# Copyright (C) 2018 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
from ansible.module_utils.dellemc_idrac import *
from ansible.module_utils.basic import AnsibleModule
from omdrivers.enums.iDRAC.BIOS import *
from omdrivers.enums.iDRAC.iDRACEnums import BootModeEnum
from omsdk.sdkfile import FileOnShare
import logging.config

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_configure_bios
short_description: Configure the BIOS configuration attributes.
version_added: "2.3"
description:
    - Configure the BIOS configuration attributes.
options:
    idrac_ip:
        required: True
        description: iDRAC IP Address
        default: None
    idrac_user:
        required: True
        description: iDRAC username
        default: None
    idrac_pwd:
        required: True
        description: iDRAC user password
        default: None
    idrac_port:
        required: False
        description: iDRAC port
        default: 443
    share_name:
        required: True
        description: CIFS or NFS Network share
    share_user:
        required: True
        description: Network share user in the format 'user@domain' if user is part of a domain else 'user'.
    share_pwd:
        required: True
        description: Network share user password
    share_mnt:
        required: True
        description: Local mount path of the network share with read-write permission for ansible user.
    boot_mode: 
        required: False
        description: Configures the boot mode to BIOS or UEFI
        choice: [Bios, Uefi]
    nvme_mode:
        required: False
        description: Configures the NVME mode in the 14th Generation of PowerEdge Servers
        choices: [NonRaid, Raid]
    secure_boot_mode:
        required: False
        description: Configures how the BIOS uses the Secure Boot Policy Objects in the 14th Generation
            of PowerEdge Servers
        choices: [AuditMode, DeployedMode, SetupMode, UserMode]
    onetime_boot_mode:
        required: False
        description: Configures the one time boot mode setting.
        choices: [Disabled, OneTimeBootSeq, OneTimeCustomBootSeqStr, OneTimeCustomHddSeqStr,
            OneTimeCustomUefiBootSeqStr, OneTimeHddSeq, OneTimeUefiBootSeq]
    boot_sequence:
        required: False
        description: Boot devices FQDDs in the sequential order for BIOS or UEFI Boot Sequence. 
            Ensure that ‘boot_mode’ option is provided to determine the appropriate boot sequence to be applied
requirements:
    - "omsdk"
    - "python >= 2.7"
author: "OpenManageAnsibleEval@dell.com"

"""

EXAMPLES = """
---
- name: Configure the BIOS single attributes.
  dellemc_configure_bios:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_pwd:  "xxxxxxxx"
       share_name: "\\\\xx.xx.xx.xx\\share"
       share_pwd:  "xxxxxxxx"
       share_user: "xxxx"
       share_mnt: "/mnt/share"
       boot_mode : "xxxxx"
       nvme_mode: "xxxxx"
       secure_boot_mode:  "xxxxxx"
       onetime_boot_mode:  "xxxxxx"
       boot_sequence: "NIC.PxeDevice.x-x, NIC.PxeDevice.x-x"
"""

RETURNS = """
---
dest:
    description: Configures the BIOS configuration attributes.
    returned: success
    type: string
"""

log_root = '/var/log'
dell_emc_log_path = log_root + '/dellemc'
dell_emc_log_file = dell_emc_log_path + '/dellemc_log.conf'

logging.config.fileConfig(dell_emc_log_file, defaults={'logfilename': dell_emc_log_path + '/dellemc_bios_config.log'})
# create logger
logger = logging.getLogger('ansible')


def run_server_bios_config(idrac, module):
    """
    Get Lifecycle Controller status

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    logger.info(module.params['idrac_ip'] + ': STARTING: server bios config method')
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    err = False
    try:

        idrac.use_redfish = True
        logger.info(module.params['idrac_ip'] + ': CALLING: File on share OMSDK API')
        upd_share = FileOnShare(remote=module.params['share_name'],
                                mount_point=module.params['share_mnt'],
                                isFolder=True,
                                creds=UserCredentials(
                                    module.params['share_user'],
                                    module.params['share_pwd'])
                                )
        logger.info(module.params['idrac_ip'] + ': FINISHED: File on share OMSDK API')

        logger.info(module.params['idrac_ip'] + ': CALLING: Set liasion share OMSDK API')
        set_liason = idrac.config_mgr.set_liason_share(upd_share)
        if set_liason['Status'] == "Failed":
            try:
                message = set_liason['Data']['Message']
            except (IndexError, KeyError):
                message = set_liason['Message']
            err = True
            msg['msg'] = "{}".format(message)
            msg['failed'] = True
            logger.info(module.params['idrac_ip'] + ': FINISHED: {}'.format(message))
            return msg, err

        logger.info(module.params['idrac_ip'] + ': FINISHED: Set liasion share OMSDK API')

        logger.info(module.params['idrac_ip'] + ': CALLING: server bios config OMSDK API')

        if module.params['boot_mode']:
            logger.info(module.params['idrac_ip'] + ': CALLING: server bios Boot mode OMSDK API')
            idrac.config_mgr.configure_boot_mode(
                boot_mode=BootModeTypes[module.params['boot_mode']])

        if module.params['nvme_mode']:
            logger.info(module.params['idrac_ip'] + ': CALLING: server bios nvme mode OMSDK API')
            idrac.config_mgr.configure_nvme_mode(
                nvme_mode=NvmeModeTypes[module.params['nvme_mode']])

        if module.params['secure_boot_mode']:
            logger.info(module.params['idrac_ip'] + ': CALLING: server bios secure boot OMSDK API')
            idrac.config_mgr.configure_secure_boot_mode(
                secure_boot_mode=SecureBootModeTypes[module.params['secure_boot_mode']])

        if module.params['onetime_boot_mode']:
            logger.info(module.params['idrac_ip'] + ': CALLING: server bios one time boot  mode OMSDK API')
            idrac.config_mgr.configure_onetime_boot_mode(
                onetime_boot_mode=OneTimeBootModeTypes[module.params['onetime_boot_mode']])

        if module.params["boot_mode"] != None and module.params["boot_sequence"] != None:
            logger.info(module.params["idrac_ip"] + ': CALLING: Boot sequence configuration OMSDK API')
            idrac.config_mgr.configure_boot_sequence(
                boot_mode=BootModeEnum[module.params['boot_mode']],
                boot_sequence=module.params['boot_sequence']
            )

        msg['msg'] = idrac.config_mgr.apply_changes(reboot=True)

        logger.info(module.params['idrac_ip'] + ': FINISHED: server bios config OMSDK API')
        if "Status" in msg['msg']:
            if msg['msg']['Status'] == "Success":
                msg['changed'] = True
                if "Message" in msg['msg']:
                    if msg['msg']['Message'] == "No changes found to commit!":
                        msg['changed'] = False
            else:
                msg['failed'] = True
    except Exception as e:
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True
        logger.error(module.params['idrac_ip'] + ': EXCEPTION: server bios config OMSDK API')
    logger.info(module.params['idrac_ip'] + ': FINISHED: server bios config Method')
    return msg, err


# Main
def main():
    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC Handle
            idrac=dict(required=False, type='dict'),

            # iDRAC credentials
            idrac_ip=dict(required=True, default=None, type='str'),
            idrac_user=dict(required=True, default=None, type='str'),
            idrac_pwd=dict(required=True, default=None,
                           type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Export Destination
            share_name=dict(required=True, type='str'),
            share_pwd=dict(required=True, type='str', no_log=True),
            share_user=dict(required=True, type='str'),
            share_mnt=dict(required=True, type='str'),

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
        ),

        supports_check_mode=True)
    logger.info(module.params['idrac_ip'] + ': STARTING: Export Server Configuration Profile')
    # Connect to iDRAC
    logger.info(module.params['idrac_ip'] + ': CALLING: iDRAC Connection')
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Connection is successful')
    # Export Server Configuration Profile
    msg, err = run_server_bios_config(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)
    logger.info(module.params['idrac_ip'] + ': FINISHED: Exported Server Configuration Profile')


if __name__ == '__main__':
    main()
