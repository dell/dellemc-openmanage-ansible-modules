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
module: dellemc_configure_idrac_timezone
short_description: Configures the iDRAC timezone attributes.
version_added: "2.3"
deprecated:
  removed_in: "3.2"
  why: Replaced with M(idrac_timezone_ntp).
  alternative: Use M(idrac_timezone_ntp) instead.
description:
    - This module is responsible for configuring the iDRAC timezone attributes.
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
    setup_idrac_timezone:
        required: False
        description: Configuring the timezone for iDRAC.
    enable_ntp:
        required: False
        description: Whether to Enable or Disable NTP for iDRAC.
        choices: [Enabled, Disabled]
    ntp_server_1:
        required: False
        description: NTP configuration for iDRAC.
    ntp_server_2:
        required: False
        description: NTP configuration for iDRAC.
    ntp_server_3:
        required: False
        description: NTP configuration for iDRAC.

requirements:
    - "omsdk"
    - "python >= 2.7.5"
author: "Felix Stephen (@felixs88)"

"""

EXAMPLES = """
---
- name: Configure the iDRAC timezone attributes.
  idrac_timezone_ntp:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_password:  "xxxxxxxx"
       share_name: "xx.xx.xx.xx:/share"
       share_password:  "xxxxxxxx"
       share_user: "xxxx"
       share_mnt: "/mnt/share"
       setup_idrac_timezone: "UTC"
       enable_ntp: Enabled
       ntp_server_1: "x.x.x.x"
       ntp_server_2: "x.x.x.x"
       ntp_server_3: "x.x.x.x"
"""

RETURNS = """
dest:
    description: Configures the iDRAC timezone attributes.
    returned: success
    type: string
"""


from ansible.module_utils.remote_management.dellemc.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
try:
    from omdrivers.enums.iDRAC.iDRAC import NTPEnable_NTPConfigGroupTypes
    from omsdk.sdkfile import file_share_manager
    from omsdk.sdkcreds import UserCredentials
except ImportError:
    pass


def run_idrac_timezone_config(idrac, module):
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
            msg['msg'] = "{}".format(message)
            msg['failed'] = True
            return msg, err

        if module.params['setup_idrac_timezone'] is not None:
            idrac.config_mgr.configure_timezone(module.params['setup_idrac_timezone'])

        if module.params['enable_ntp'] is not None:
            idrac.config_mgr.configure_ntp(
                enable_ntp=NTPEnable_NTPConfigGroupTypes[module.params['enable_ntp']]
            )
        if module.params['ntp_server_1'] is not None:
            idrac.config_mgr.configure_ntp(
                ntp_server_1=module.params['ntp_server_1']
            )
        if module.params['ntp_server_2'] is not None:
            idrac.config_mgr.configure_ntp(
                ntp_server_2=module.params['ntp_server_2']
            )
        if module.params['ntp_server_3'] is not None:
            idrac.config_mgr.configure_ntp(
                ntp_server_3=module.params['ntp_server_3']
            )

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
            idrac_password=dict(required=True,
                           type='str', aliases=['idrac_pwd'], no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Export Destination
            share_name=dict(required=True, type='str'),
            share_password=dict(required=False, type='str', aliases=['share_pwd'], no_log=True),
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
    module.deprecate("The 'dellemc_configure_idrac_timezone' module has been deprecated. "
                     "Use 'idrac_timezone_ntp' instead",
                     version=3.2)

    try:
        with iDRACConnection(module.params) as idrac:
            msg, err = run_idrac_timezone_config(idrac, module)
    except (ImportError, ValueError, RuntimeError) as e:
        module.fail_json(msg=str(e))

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
