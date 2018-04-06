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
module: dellemc_configure_idrac_eventing
short_description: Configures the iDRAC eventing attributes.
version_added: "2.3"
description:
    - This module is responsible for configuring the iDRAC eventing attributes.
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
    destination_number:
        required: False
        description: Destination number for SNMP Trap
        default: None
    destination:
        required: False
        description: Destination for SNMP Trap
        default: None
    snmp_v3_username:
        required: False
        description: SNMP v3 username for SNMP Trap
        default: None
    snmp_trap_state:
        required: False
        description: Whether to Enable or Disable SNMP alert.
        choices: [Enabled, Disabled]
    email_alert_state:
        required: False
        description: Whether to Enable or Disable Email alert.
        choices: [Enabled, Disabled]
    alert_number:
        required: False
        description: Alert number for Email configuration
        default: None
    address:
        required: False
        description: Email address for SNMP Trap
    custom_message:
        required: False
        description: Custom message for SNMP Trap reference.
    enable_alerts:
        required: False
        description: Whether to Enable or Disable iDRAC alerts.
        choices: [Enabled, Disabled]
    authentication:
        required: False
        description: Simple Mail Transfer Protocol Authentication
        choices: [Enabled, Disabled]
    smtp_ip_address: 
        required: False
        description: SMTP IP address for communication
    smtp_port:
        required: False
        description: SMTP Port number for access.
        default: None
    username:
        required: False
        description: Username for SMTP authentication
        default: None
    password:
        required: False
        description: Password for SMTP authentication
        default: None
requirements:
    - "omsdk"
    - "python >= 2.7"
author: "OpenManageAnsibleEval@dell.com"

"""

EXAMPLES = """
---
- name: Configure the iDRAC eventing attributes.
  dellemc_configure_idrac_eventing:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_pwd:  "xxxxxxxx"
       share_name: "\\\\xx.xx.xx.xx\\share"
       share_pwd:  "xxxxxxxx"
       share_user: "xxxx"
       share_mnt: "/mnt/share"
       destination_number: xxxx
       destination: xxxx
       snmp_v3_username: xxxx
       snmp_trap_state: xxxx
       email_alert_state: xxxx
       alert_number: xxxx
       address: "xxxxxxxx"
       custom_message: "xxxx"
       enable_alerts: xxxx
       authentication: xxxx
       smtp_ip_address: "x.x.x.x"
       smtp_port: xxxx
       username: "xxxx"
       password: "xxxxxxxx"
"""

RETURNS = """
---
- dest:
    description: Configures the iDRAC eventing attributes.
    returned: success
    type: string
"""

# log_root = '/var/log'
# dell_emc_log_path = log_root + '/dellemc'
# dell_emc_log_file = dell_emc_log_path + '/dellemc_log.conf'
#
# logging.config.fileConfig(dell_emc_log_file,
#                           defaults={'logfilename': dell_emc_log_path + '/dellemc_idrac_eventing_config.log'})
# # create logger
# logger = logging.getLogger('ansible')


def run_idrac_eventing_config(idrac, module):
    """
    Get Lifecycle Controller status

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    logger.info(module.params['idrac_ip'] + ': STARTING: iDRAC eventing configuration method')
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

        logger.info(module.params["idrac_ip"] + ': CALLING: Configure SNMP Trap Destination')

        if module.params["destination_number"] != None:
            if module.params["destination"] != None:
                idrac.config_mgr.configure_snmp_trap_destination(
                    destination=module.params["destination"],
                    destination_number=module.params["destination_number"]
                )
            if module.params["snmp_v3_username"] != None:
                idrac.config_mgr.configure_snmp_trap_destination(
                    snmp_v3_username=module.params["snmp_v3_username"],
                    destination_number=module.params["destination_number"]
                )
            if module.params["snmp_trap_state"] != None:
                idrac.config_mgr.configure_snmp_trap_destination(
                    state=State_SNMPAlertTypes[module.params["snmp_trap_state"]],
                    destination_number=module.params["destination_number"]
                )

        logger.info(module.params["idrac_ip"] + ': FINISHED: Configure SNMP Trap Destination')

        logger.info(module.params['idrac_ip'] + ': CALLING: Configure email alerts')
        if module.params["alert_number"] != None:
            if module.params["email_alert_state"] != None:
                idrac.config_mgr.configure_email_alerts(
                    state=Enable_EmailAlertTypes[module.params["email_alert_state"]],
                    alert_number=module.params["alert_number"]
                )
            if module.params["address"] != None:
                idrac.config_mgr.configure_email_alerts(
                    address=module.params["address"],
                    alert_number=module.params["alert_number"]
                )
            if module.params["custom_message"] != None:
                idrac.config_mgr.configure_email_alerts(
                    custom_message=module.params["custom_message"],
                    alert_number=module.params["alert_number"]
                )

        logger.info(module.params['idrac_ip'] + ': FINISHED: Configure email alerts')

        logger.info(module.params['idrac_ip'] + ': CALLING: Configure iDRAC Alerts')
        if module.params["enable_alerts"] != None:
            idrac.config_mgr.configure_idrac_alerts(
                enable_alerts=AlertEnable_IPMILanTypes[module.params["enable_alerts"]],
            )
        logger.info(module.params['idrac_ip'] + ': FINISHED: Configure iDRAC Alerts')

        logger.info(module.params['idrac_ip'] + ': CALLING: Setup iDRAC SMTP authentication')

        if module.params['authentication'] != None:
            idrac.config_mgr.configure_smtp_server_settings(
                authentication=SMTPAuthentication_RemoteHostsTypes[module.params['authentication']])
        if module.params['smtp_ip_address'] != None:
            idrac.config_mgr.configure_smtp_server_settings(
                smtp_ip_address=module.params['smtp_ip_address'])
        if module.params['smtp_port'] != None:
            idrac.config_mgr.configure_smtp_server_settings(
                smtp_port=module.params['smtp_port'])
        if module.params['username'] != None:
            idrac.config_mgr.configure_smtp_server_settings(
                username=module.params['username'])
        if module.params['password'] != None:
            idrac.config_mgr.configure_smtp_server_settings(
                password=module.params['password'])
        logger.info(module.params['idrac_ip'] + ': FINISHED: Setup iDRAC SMTP authentication')

        msg['msg'] = idrac.config_mgr.apply_changes(reboot=False)

        if "Status" in msg['msg']:
            if msg['msg']['Status'] == "Success":
                msg['changed'] = True
                if "Message" in msg['msg']:
                    if msg['msg']['Message'] == "No changes found to commit!":
                        msg['changed'] = False
                    if "No changes were applied" in msg['msg']['Message']:
                        msg['changed'] = False
            else:
                msg['failed'] = True
    except Exception as e:
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True
        logger.error(module.params['idrac_ip'] + ': EXCEPTION: iDRAC eventing configuration method')
    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC eventing configuration method')
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

            # setup SNMP Trap Destination
            destination_number=dict(required=False, default=None, type="str"),
            destination=dict(required=False, default=None, type="str"),
            snmp_v3_username=dict(required=False, default=None),
            snmp_trap_state=dict(required=False, choices=["Enabled", "Disabled"], default=None),

            # setup Email Alerts
            alert_number=dict(required=False, default=None, type="int"),
            address=dict(required=False, default=None, type="str"),
            custom_message=dict(required=False, default=None, type="str"),
            email_alert_state=dict(required=False, choices=["Enabled", "Disabled"], default=None),

            # setup iDRAC Alerts
            enable_alerts=dict(required=False, choices=["Enabled", "Disabled"], default=None),

            # setup SMTP
            authentication=dict(required=False, choices=['Enabled', 'Disabled'], default=None),
            smtp_ip_address=dict(required=False, default=None, type='str'),
            smtp_port=dict(required=False, default=None, type='str'),
            username=dict(required=False, default=None, type="str"),
            password=dict(required=False, default=None, type="str", no_log=True),

        ),

        supports_check_mode=True)
    logger.info(module.params['idrac_ip'] + ': CALLING: iDRAC Server Configuration')
    # Connect to iDRAC
    logger.info(module.params['idrac_ip'] + ': CALLING: iDRAC Connection')
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Connection is successful')
    # Export Server Configuration Profile
    msg, err = run_idrac_eventing_config(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)
    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Server Configuration')


if __name__ == '__main__':
    main()
