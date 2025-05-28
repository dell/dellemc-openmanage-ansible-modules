#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.1.0
# Copyright (C) 2018-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
---
module: dellemc_configure_idrac_eventing
short_description: Configures the iDRAC eventing related attributes
version_added: "1.0.0"
deprecated:
  removed_at_date: "2024-12-31"
  why: Replaced with M(dellemc.openmanage.idrac_attributes).
  alternative: Use M(dellemc.openmanage.idrac_attributes) instead.
  removed_from_collection: dellemc.openmanage
description:
    - This module allows to configure the iDRAC eventing related attributes.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
    share_name:
        type: str
        description:
          - (deprecated)Network share or a local path.
          - This option is deprecated and will be removed in the later version.
    share_user:
        type: str
        description:
          - (deprecated)Network share user in the format 'user@domain' or 'domain\\user' if user is
            part of a domain else 'user'. This option is mandatory for CIFS Network Share.
          - This option is deprecated and will be removed in the later version.
    share_password:
        type: str
        description:
          - (deprecated)Network share user password. This option is mandatory for CIFS Network Share.
          - This option is deprecated and will be removed in the later version.
        aliases: ['share_pwd']
    share_mnt:
        type: str
        description:
          - (deprecated)Local mount path of the network share with read-write permission for ansible user.
            This option is mandatory for Network Share.
          - This option is deprecated and will be removed in the later version.
    destination_number:
        type: int
        description: Destination number for SNMP Trap.
    destination:
        type: str
        description: Destination for SNMP Trap.
    snmp_v3_username:
        type: str
        description: SNMP v3 username for SNMP Trap.
    snmp_trap_state:
        type: str
        description: Whether to Enable or Disable SNMP alert.
        choices: [Enabled, Disabled]
    email_alert_state:
        type: str
        description: Whether to Enable or Disable Email alert.
        choices: [Enabled, Disabled]
    alert_number:
        type: int
        description: Alert number for Email configuration.
    address:
        type: str
        description: Email address for SNMP Trap.
    custom_message:
        type: str
        description: Custom message for SNMP Trap reference.
    enable_alerts:
        type: str
        description: Whether to Enable or Disable iDRAC alerts.
        choices: [Enabled, Disabled]
    authentication:
        type: str
        description: Simple Mail Transfer Protocol Authentication.
        choices: [Enabled, Disabled]
    smtp_ip_address:
        type: str
        description: Enter the IPv4 or IPv6 address of the SMTP server or the FQDN or DNS name.
    smtp_port:
        type: str
        description: SMTP Port number for access.
    username:
        type: str
        description: Username for SMTP authentication.
    password:
        type: str
        description: Password for SMTP authentication.
requirements:
    - "omsdk >= 1.2.503"
    - "python >= 3.9.6"
author: "Felix Stephen (@felixs88)"
notes:
    - This module requires 'Administrator' privilege for I(idrac_user).
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports both IPv4 and IPv6 address for I(idrac_ip).
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Configure the iDRAC eventing attributes
  dellemc.openmanage.dellemc_configure_idrac_eventing:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       ca_path: "/path/to/ca_cert.pem"
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

RETURN = r'''
---
msg:
  description: Successfully configured the iDRAC eventing settings.
  returned: always
  type: str
  sample: Successfully configured the iDRAC eventing settings.
eventing_status:
  description: Configures the iDRAC eventing attributes.
  returned: success
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
from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection, idrac_auth_params
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
try:
    from omdrivers.enums.iDRAC.iDRAC import (State_SNMPAlertTypes, Enable_EmailAlertTypes,
                                             AlertEnable_IPMILanTypes,
                                             SMTPAuthentication_RemoteHostsTypes)
    from omsdk.sdkfile import file_share_manager
except ImportError:
    pass


def run_idrac_eventing_config(idrac, module):
    """
    Get Lifecycle Controller status

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    idrac.use_redfish = True
    share_path = tempfile.gettempdir() + os.sep
    upd_share = file_share_manager.create_share_obj(share_path=share_path, isFolder=True)
    if not upd_share.IsValid:
        module.fail_json(msg="Unable to access the share. Ensure that the share name, "
                             "share mount, and share credentials provided are correct.")
    set_liason = idrac.config_mgr.set_liason_share(upd_share)
    if set_liason['Status'] == "Failed":
        try:
            message = set_liason['Data']['Message']
        except (IndexError, KeyError):
            message = set_liason['Message']
        module.fail_json(msg=message)

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
        status = idrac.config_mgr.is_change_applicable()
        if status.get("changes_applicable"):
            module.exit_json(msg="Changes found to commit!", changed=True)
        else:
            module.exit_json(msg="No changes found to commit!")
    else:
        status = idrac.config_mgr.apply_changes(reboot=False)

    return status


def main():
    specs = dict(
        share_name=dict(required=False, type='str'),
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
    )
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        supports_check_mode=True)

    try:
        with iDRACConnection(module.params) as idrac:
            status = run_idrac_eventing_config(idrac, module)
            msg, changed = "Successfully configured the iDRAC eventing settings.", True
            if status.get('Status') == "Success":
                if (status.get('Message') == "No changes found to commit!") or \
                        ("No changes were applied" in status.get('Message')):
                    msg = status.get('Message')
                    changed = False
            elif status.get('Status') == "Failed":
                module.fail_json(msg="Failed to configure the iDRAC eventing settings")
            module.exit_json(msg=msg, eventing_status=status, changed=changed)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, ImportError, SSLValidationError, IOError, ValueError, TypeError, ConnectionError) as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
