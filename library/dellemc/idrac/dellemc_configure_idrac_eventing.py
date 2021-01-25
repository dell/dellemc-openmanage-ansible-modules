#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.0.0
# Copyright (C) 2018-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_configure_idrac_eventing
short_description: Configures the iDRAC eventing related attributes
version_added: "2.3.0"
description:
    - This module allows to configure the iDRAC eventing related attributes.
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
        required: True
        type: str
        description: Network share or a local path.
    share_user:
        required: False
        type: str
        description: Network share user in the format 'user@domain' or 'domain\\user' if user is
            part of a domain else 'user'. This option is mandatory for CIFS Network Share.
    share_password:
        required: False
        type: str
        description: Network share user password. This option is mandatory for CIFS Network Share.
        aliases: ['share_pwd']
    share_mnt:
        required: False
        type: str
        description: Local mount path of the network share with read-write permission for ansible user.
            This option is mandatory for Network Share.
    destination_number:
        required: False
        type: int
        description: Destination number for SNMP Trap.
    destination:
        required: False
        type: str
        description: Destination for SNMP Trap.
    snmp_v3_username:
        required: False
        type: str
        description: SNMP v3 username for SNMP Trap.
    snmp_trap_state:
        required: False
        type: str
        description: Whether to Enable or Disable SNMP alert.
        choices: [Enabled, Disabled]
    email_alert_state:
        required: False
        type: str
        description: Whether to Enable or Disable Email alert.
        choices: [Enabled, Disabled]
    alert_number:
        required: False
        type: int
        description: Alert number for Email configuration.
    address:
        required: False
        type: str
        description: Email address for SNMP Trap.
    custom_message:
        required: False
        type: str
        description: Custom message for SNMP Trap reference.
    enable_alerts:
        required: False
        type: str
        description: Whether to Enable or Disable iDRAC alerts.
        choices: [Enabled, Disabled]
    authentication:
        required: False
        type: str
        description: Simple Mail Transfer Protocol Authentication.
        choices: [Enabled, Disabled]
    smtp_ip_address:
        required: False
        type: str
        description: SMTP IP address for communication.
    smtp_port:
        required: False
        type: str
        description: SMTP Port number for access.
    username:
        required: False
        type: str
        description: Username for SMTP authentication.
    password:
        required: False
        type: str
        description: Password for SMTP authentication.
requirements:
    - "omsdk"
    - "python >= 2.7.5"
author: "Felix Stephen (@felixs88)"
notes:
    - Run this module from a system that has direct access to DellEMC iDRAC.
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Configure the iDRAC eventing attributes.
  dellemc_configure_idrac_eventing:
       idrac_ip:   "192.168.0.1"
       idrac_user: "user_name"
       idrac_password:  "user_password"
       share_name: "192.168.0.1:/share"
       share_password:  "share_user"
       share_user: "share_password"
       share_mnt: "/mnt/share"
       destination_number: "2"
       destination: "1.1.1.1"
       snmp_v3_username: "None"
       snmp_trap_state: "Enabled"
       email_alert_state: "Disabled"
       alert_number: "1"
       address: "alert_email@company.com"
       custom_message: "Custom Message"
       enable_alerts: "Disabled"
       authentication: "Enabled"
       smtp_ip_address: "192.168.0.1"
       smtp_port: "25"
       username: "username"
       password: "password"
"""

RETURNS = """
msg:
    description: Configures the iDRAC eventing attributes.
    returned: always
    type: dict
    sample: {
        "CompletionTime": "2020-04-02T02:43:28",
        "Description": "Job Instance",
        "EndTime": null,
        "Id": "JID_12345123456",
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
"""

from ansible.module_utils.remote_management.dellemc.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
try:
    from omdrivers.enums.iDRAC.iDRAC import (State_SNMPAlertTypes, Enable_EmailAlertTypes,
                                             AlertEnable_IPMILanTypes,
                                             SMTPAuthentication_RemoteHostsTypes)
    from omsdk.sdkfile import file_share_manager
    from omsdk.sdkcreds import UserCredentials
except ImportError:
    pass


def run_idrac_eventing_config(idrac, module):
    """
    Get Lifecycle Controller status

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    err = False

    try:

        idrac.use_redfish = True
        upd_share = file_share_manager.create_share_obj(share_path=module.params['share_name'],
                                                        mount_point=module.params['share_mnt'],
                                                        isFolder=True,
                                                        creds=UserCredentials(
                                                            module.params['share_user'],
                                                            module.params['share_password'])
                                                        )

        set_liason = idrac.config_mgr.set_liason_share(upd_share)
        if set_liason['Status'] == "Failed":
            try:
                message = set_liason['Data']['Message']
            except (IndexError, KeyError):
                message = set_liason['Message']
            err = True
            msg['msg'] = "{0}".format(message)
            msg['failed'] = True
            return msg, err

        if module.params["destination_number"] is not None:
            if module.params["destination"] is not None:
                idrac.config_mgr.configure_snmp_trap_destination(
                    destination=module.params["destination"],
                    destination_number=module.params["destination_number"]
                )
            if module.params["snmp_v3_username"] is not None:
                idrac.config_mgr.configure_snmp_trap_destination(
                    snmp_v3_username=module.params["snmp_v3_username"],
                    destination_number=module.params["destination_number"]
                )
            if module.params["snmp_trap_state"] is not None:
                idrac.config_mgr.configure_snmp_trap_destination(
                    state=State_SNMPAlertTypes[module.params["snmp_trap_state"]],
                    destination_number=module.params["destination_number"]
                )

        if module.params["alert_number"] is not None:
            if module.params["email_alert_state"] is not None:
                idrac.config_mgr.configure_email_alerts(
                    state=Enable_EmailAlertTypes[module.params["email_alert_state"]],
                    alert_number=module.params["alert_number"]
                )
            if module.params["address"] is not None:
                idrac.config_mgr.configure_email_alerts(
                    address=module.params["address"],
                    alert_number=module.params["alert_number"]
                )
            if module.params["custom_message"] is not None:
                idrac.config_mgr.configure_email_alerts(
                    custom_message=module.params["custom_message"],
                    alert_number=module.params["alert_number"]
                )

        if module.params["enable_alerts"] is not None:
            idrac.config_mgr.configure_idrac_alerts(
                enable_alerts=AlertEnable_IPMILanTypes[module.params["enable_alerts"]],
            )

        if module.params['authentication'] is not None:
            idrac.config_mgr.configure_smtp_server_settings(
                authentication=SMTPAuthentication_RemoteHostsTypes[module.params['authentication']])
        if module.params['smtp_ip_address'] is not None:
            idrac.config_mgr.configure_smtp_server_settings(
                smtp_ip_address=module.params['smtp_ip_address'])
        if module.params['smtp_port'] is not None:
            idrac.config_mgr.configure_smtp_server_settings(
                smtp_port=module.params['smtp_port'])
        if module.params['username'] is not None:
            idrac.config_mgr.configure_smtp_server_settings(
                username=module.params['username'])
        if module.params['password'] is not None:
            idrac.config_mgr.configure_smtp_server_settings(
                password=module.params['password'])

        if module.check_mode:
            msg['msg'] = idrac.config_mgr.is_change_applicable()
            if 'changes_applicable' in msg['msg']:
                msg['changed'] = msg['msg']['changes_applicable']
        else:
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
    return msg, err


# Main
def main():
    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_password=dict(required=True, type='str', aliases=['idrac_pwd'], no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Export Destination
            share_name=dict(required=True, type='str'),
            share_password=dict(required=False, type='str', aliases=['share_pwd'], no_log=True),
            share_user=dict(required=False, type='str'),
            share_mnt=dict(required=False, type='str'),

            # setup SNMP Trap Destination
            destination_number=dict(required=False, type="int"),
            destination=dict(required=False, type="str"),
            snmp_v3_username=dict(required=False, type="str"),
            snmp_trap_state=dict(required=False, choices=["Enabled", "Disabled"], default=None),

            # setup Email Alerts
            alert_number=dict(required=False, type="int"),
            address=dict(required=False, default=None, type="str"),
            custom_message=dict(required=False, default=None, type="str"),
            email_alert_state=dict(required=False, choices=["Enabled", "Disabled"], default=None),

            # setup iDRAC Alerts
            enable_alerts=dict(required=False, choices=["Enabled", "Disabled"], default=None),

            # setup SMTP
            authentication=dict(required=False, choices=['Enabled', 'Disabled'], default=None),
            smtp_ip_address=dict(required=False, default=None, type='str'),
            smtp_port=dict(required=False, type='str'),
            username=dict(required=False, type="str"),
            password=dict(required=False, type="str", no_log=True),

        ),

        supports_check_mode=True)

    try:
        with iDRACConnection(module.params) as idrac:
            msg, err = run_idrac_eventing_config(idrac, module)
    except (ImportError, ValueError, RuntimeError) as e:
        module.fail_json(msg=str(e))

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
