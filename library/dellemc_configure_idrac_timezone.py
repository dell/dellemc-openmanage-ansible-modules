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
module: dellemc_configure_idrac_timezone
short_description: Configures the iDRAC timezone attributes.
version_added: "2.3"
description:
    - This module is responsible for configuring the iDRAC timezone attributes.
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
    setup_idrac_timezone:
        required: False
        description: Configuring the timezone for iDRAC.
    enable_ntp:
        required: False
        description: Whether to Enable or Disable NTP for iDRAC
    ntp_server_1:
        required: False
        description: NTP configuration for iDRAC
    ntp_server_2:
        required: False
        description: NTP configuration for iDRAC
    ntp_server_3:
        required: False
        description: NTP configuration for iDRAC

requirements:
    - "omsdk"
    - "python >= 2.7"
author: "OpenManageAnsibleEval@dell.com"

"""

EXAMPLES = """
---
- name: Configure the iDRAC timezone attributes.
  dellemc_configure_idrac_timezone:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_pwd:  "xxxxxxxx"
       share_name: "\\\\xx.xx.xx.xx\\share"
       share_pwd:  "xxxxxxxx"
       share_user: "xxxx"
       share_mnt: "/mnt/share"
       setup_idrac_timezone: "UTC"
       enable_ntp: Enabled
       ntp_server_1: "x.x.x.x"
       ntp_server_2: "x.x.x.x"
       ntp_server_3: "x.x.x.x"
"""

RETURNS = """
---
- dest:
    description: Configures the iDRAC timezone attributes.
    returned: success
    type: string
"""


# log_root = '/var/log'
# dell_emc_log_path = log_root + '/dellemc'
# dell_emc_log_file = dell_emc_log_path + '/dellemc_log.conf'
#
# logging.config.fileConfig(dell_emc_log_file,
#                           defaults={'logfilename': dell_emc_log_path + '/dellemc_idrac_timezone_config.log'})
# # create logger
# logger = logging.getLogger('ansible')


def run_idrac_timezone_config(idrac, module):
    """
    Get Lifecycle Controller status

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    logger.info(module.params['idrac_ip'] + ': STARTING: iDRAC timezone configuration method')
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
        logger.info(module.params['idrac_ip'] + ': CALLING: setup iDRAC timezone method')
        if module.params['setup_idrac_timezone'] != None:
            idrac.config_mgr.configure_timezone(module.params['setup_idrac_timezone'])
        logger.info(module.params['idrac_ip'] + ': FINISHED: setup iDRAC timezone method')

        logger.info(module.params['idrac_ip'] + ': CALLING: Setup iDRAC NTP Configuration')

        if module.params['enable_ntp'] != None:
            idrac.config_mgr.configure_ntp(
                enable_ntp=NTPEnable_NTPConfigGroupTypes[module.params['enable_ntp']]
            )
        if module.params['ntp_server_1'] != None:
            idrac.config_mgr.configure_ntp(
                ntp_server_1=module.params['ntp_server_1']
            )
        if module.params['ntp_server_2'] != None:
            idrac.config_mgr.configure_ntp(
                ntp_server_2=module.params['ntp_server_2']
            )
        if module.params['ntp_server_3'] != None:
            idrac.config_mgr.configure_ntp(
                ntp_server_3=module.params['ntp_server_3']
            )
        logger.info(module.params['idrac_ip'] + ': FINISHED: Setup iDRAC NTP Configuration')

        msg['msg'] = idrac.config_mgr.apply_changes(reboot=False)

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
        logger.error(module.params['idrac_ip'] + ': EXCEPTION: iDRAC timezone configuration method')
    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC timezone configuration method')
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

            # setup NTP
            enable_ntp=dict(required=False, choices=['Enabled', 'Disabled'], default=None),
            ntp_server_1=dict(required=False, default=None),
            ntp_server_2=dict(required=False, default=None),
            ntp_server_3=dict(required=False, default=None),

            # set up timezone
            setup_idrac_timezone=dict(required=False, type='str', default=None),

        ),

        supports_check_mode=True)
    logger.info(module.params['idrac_ip'] + ': CALLING: iDRAC Server Configuration')
    # Connect to iDRAC
    logger.info(module.params['idrac_ip'] + ': CALLING: iDRAC Connection')
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Connection is successful')
    # Export Server Configuration Profile
    msg, err = run_idrac_timezone_config(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)
    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Server Configuration')


if __name__ == '__main__':
    main()
