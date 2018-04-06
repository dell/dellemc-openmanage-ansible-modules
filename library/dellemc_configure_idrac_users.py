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
from omdrivers.enums.iDRAC.iDRAC import *
# from omsdk.sdkfile import FileOnShare
# import logging.config

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_configure_idrac_users
short_description: Configures the iDRAC users attributes.
version_added: "2.3"
description:
    - This module is responsible for configuring the iDRAC users attributes.
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
    action:
        required: False
        description: This value will decide whether to create or delete or modify iDRAC user.
        choices: [create, delete, modify]
        default: create
    user_name:
        required: False
        description: Provide the user name to be created, or deleted or modified.
    user_password:
        required: False
        description: Provide the password for the user to be created or modified.
    privilege_users:
        required: False
        description: Privilege user access is configurable
        choices: [NoAccess, Readonly, Operator, Administrator]
    ipmilanprivilege_users:
        required: False
        description: IPMI Lan Privilege user access is configurable
        choices: [Administrator, No_Access, Operator, User]
    ipmiserialprivilege_users:
        required: False
        description: IPMI Serial Privilege user access is configurable
        choices: [Administrator, No_Access, Operator, User]
    enable_users:
        required: False
        description: Enabling or Disabling the new iDRAC user
        default: None
        choices: [Enabled, Disabled]
    solenable_users:
        required: False
        description: Enabling SOL for iDRAC user
        default: None
        choices: [Enabled, Disabled]
    protocolenable_users:
        required: False
        description: Enabling protocol for iDRAC user
        default: None
        choices: [Enabled, Disabled]
    authenticationprotocol_users:
        required: False
        description: Configuring authentication protocol for iDRAC user
        choices: [T_None, SHA, MD5]
    privacyprotocol_users:
        required: False
        description: Configuring privacy protocol for iDRAC user
        choices: [T_None, DES, AES]

requirements:
    - "omsdk"
    - "python >= 2.7"
author: "OpenManageAnsibleEval@dell.com"

"""

EXAMPLES = """
---
- name: Configure the iDRAC users attributes.
  dellemc_configure_idrac_users:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_pwd:  "xxxxxxxx"
       share_name: "\\\\xx.xx.xx.xx\\share"
       share_pwd:  "xxxxxxxx"
       share_user: "xxxx"
       share_mnt: "/mnt/share"
       action: "create"
       user_name: "xxxxxx"
       user_password: "xxxxxxxx"
       privilege_users: Administrator
       ipmilanprivilege_users: Administrator
       ipmiserialprivilege_users: Administrator
       enable_users: Enabled
       solenable_users: Enabled
       protocolenable_users: Enabled
       authenticationprotocol_users: SHA
       privacyprotocol_users: AES
"""

RETURNS = """
---
- dest:
    description: Configures the iDRAC users attributes.
    returned: success
    type: string
"""

# log_root = '/var/log'
# dell_emc_log_path = log_root + '/dellemc'
# dell_emc_log_file = dell_emc_log_path + '/dellemc_log.conf'
#
# logging.config.fileConfig(dell_emc_log_file,
#                           defaults={'logfilename': dell_emc_log_path + '/dellemc_idrac_users_config.log'})
# # create logger
# logger = logging.getLogger('ansible')


def run_idrac_users_config(idrac, module):
    """
    Get Lifecycle Controller status
    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    logger.info(module.params['idrac_ip'] + ': STARTING: iDRAC users configuration method')
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    err = False

    try:

        idrac.use_redfish = True
        logger.info(module.params['idrac_ip'] + ': CALLING: File on share OMSDK API')
        upd_share = file_share_manager.create_share_obj(share_path=module.params['share_name'],
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

        enable_users = solenable_users = protocolenable_users = None
        privilege_users = ipmilanprivilege_users = ipmiserialprivilege_users = None
        if module.params['enable_users'] != None:
            enable_users = Enable_UsersTypes[module.params['enable_users']]
        if module.params['solenable_users'] != None:
            solenable_users = SolEnable_UsersTypes[module.params['solenable_users']]
        if module.params['protocolenable_users'] != None:
            protocolenable_users = ProtocolEnable_UsersTypes[module.params['protocolenable_users']]

        if module.params['privilege_users'] != None:
            privilege_users = Privilege_UsersTypes[module.params['privilege_users']]
        if module.params['ipmilanprivilege_users'] != None:
            ipmilanprivilege_users = IpmiLanPrivilege_UsersTypes[
                module.params['ipmilanprivilege_users']]
        if module.params['ipmiserialprivilege_users'] != None:
            ipmiserialprivilege_users = IpmiSerialPrivilege_UsersTypes[
                module.params['ipmiserialprivilege_users']]

        authenticationprotocol_users = privacyprotocol_users = None
        if module.params['authenticationprotocol_users'] != None:
            authenticationprotocol_users = AuthenticationProtocol_UsersTypes[
                module.params['authenticationprotocol_users']]
        if module.params['privacyprotocol_users'] != None:
            privacyprotocol_users = PrivacyProtocol_UsersTypes[
                module.params['privacyprotocol_users']]

        if module.params['action'] == 'create':
            logger.info(module.params['idrac_ip'] + ': CALLING: create iDRAC user method')
            idrac.user_mgr.Users.new(
                UserName_Users=module.params['user_name'],
                Password_Users=module.params['user_password'],
                Privilege_Users=privilege_users,
                IpmiLanPrivilege_Users=ipmilanprivilege_users,
                IpmiSerialPrivilege_Users=ipmiserialprivilege_users,
                Enable_Users=enable_users,
                SolEnable_Users=solenable_users,
                ProtocolEnable_Users=protocolenable_users,
                AuthenticationProtocol_Users=authenticationprotocol_users,
                PrivacyProtocol_Users=privacyprotocol_users
            )
            logger.info(module.params['idrac_ip'] + ': FINISHED: create iDRAC user method')

        if module.params['action'] == 'modify':
            logger.info(module.params['idrac_ip'] + ': CALLING: modify iDRAC user method')
            user = idrac.config_mgr._sysconfig.iDRAC.Users.find_first(
                UserName_Users=module.params['user_name']
            )
            if user:
                if module.params['user_password'] is not None:
                    user.Password_Users.set_value(module.params['user_password'])
                if privilege_users is not None:
                    user.Privilege_Users.set_value(privilege_users)
                if ipmilanprivilege_users is not None:
                    user.IpmiLanPrivilege_Users.set_value(ipmilanprivilege_users)
                if ipmiserialprivilege_users is not None:
                    user.IpmiSerialPrivilege_Users.set_value(ipmiserialprivilege_users)
                if enable_users is not None:
                    user.Enable_Users.set_value(enable_users)
                if solenable_users is not None:
                    user.SolEnable_Users.set_value(solenable_users)
                if protocolenable_users is not None:
                    user.ProtocolEnable_Users.set_value(protocolenable_users)
                if authenticationprotocol_users is not None:
                    user.AuthenticationProtocol_Users.set_value(authenticationprotocol_users)
                if privacyprotocol_users is not None:
                    user.PrivacyProtocol_Users.set_value(privacyprotocol_users)
            else:
                message = "User: {} does not exist".format(module.params['user_name'])
                err = True
                msg['msg'] = "{}".format(message)
                msg['failed'] = True
                logger.info(module.params['idrac_ip'] + ': FINISHED: {}'.format(message))
                return msg, err
            logger.info(module.params['idrac_ip'] + ': FINISHED: modify iDRAC user method')

        if module.params['action'] == 'delete':
            logger.info(module.params['idrac_ip'] + ': CALLING: remove iDRAC user method')
            idrac.user_mgr.Users.remove(UserName_Users=module.params['user_name'])
            logger.info(module.params['idrac_ip'] + ': FINISHED: remove iDRAC user method')

        msg['msg'] = idrac.config_mgr.apply_changes()

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
        logger.error(module.params['idrac_ip'] + ': EXCEPTION: iDRAC users configuration method')
    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC users configuration method')
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
            share_pwd=dict(required=False, type='str', no_log=True),
            share_user=dict(required=False, type='str'),
            share_mnt=dict(required=False, type='str'),

            # change idrac user
            action=dict(required=False, choices=['create', 'delete', 'modify'], default='create'),
            user_name=dict(required=False, default=None, type='str'),
            user_password=dict(required=False, default=None,
                               type='str', no_log=True),
            privilege_users=dict(required=False, choices=['Administrator', 'NoAccess', 'Readonly', 'Operator'],
                                 default=None),
            ipmilanprivilege_users=dict(required=False,
                                        choices=['Administrator', 'No_Access', 'Operator', 'User'],
                                        default=None),
            ipmiserialprivilege_users=dict(required=False,
                                           choices=['Administrator', 'No_Access', 'Operator', 'User'],
                                           default=None),
            enable_users=dict(required=False, choices=['Enabled', 'Disabled'], default=None),
            solenable_users=dict(required=False, choices=['Enabled', 'Disabled'], default=None),
            protocolenable_users=dict(required=False, choices=['Enabled', 'Disabled'], default=None),
            authenticationprotocol_users=dict(required=False, choices=['T_None', 'SHA', 'MD5'], default=None),
            privacyprotocol_users=dict(required=False, choices=['T_None', 'DES', 'AES'], default=None),

        ),

        supports_check_mode=True)
    logger.info(module.params['idrac_ip'] + ': CALLING: iDRAC Server Configuration')
    # Connect to iDRAC
    logger.info(module.params['idrac_ip'] + ': CALLING: iDRAC Connection')
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Connection is successful')
    # Export Server Configuration Profile
    msg, err = run_idrac_users_config(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)
    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Server Configuration')


if __name__ == '__main__':
    main()
