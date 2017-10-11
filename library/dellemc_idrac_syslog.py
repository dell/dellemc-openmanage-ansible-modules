#! /usr/bin/python
# _*_ coding: utf-8 _*_

#
# Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved.
# Dell, EMC, and other trademarks are trademarks of Dell Inc. or its
# subsidiaries. Other trademarks may be trademarks of their respective owners.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: dellemc_idrac_syslog
short_description: Configure remote system logging
version_added: "2.3"
description:
    - Configure remote system logging settings to remotely write RAC log and System Event Log (SEL) to an external server
options:
  idrac_ip:
    required: True
    description:
      - iDRAC IP Address
    type: 'str'
  idrac_user:
    required: True
    description:
      - iDRAC user name
    type: 'str'
  idrac_pwd:
    required: True
    description:
      - iDRAC user password
    type: 'str'
  idrac_port:
    required: False
    description:
      - iDRAC port
    default: 443
    type: 'int'
  syslog_servers:
    required: False
    description:
      - List of IP Addresses of the Remote Syslog Servers
    default: None
    type: 'list'
  syslog_port:
    required: False
    description:
      - Port number of remote servers
    default: 514
    type: 'int'
  state:
    description:
      - if C(present), will enable the remote syslog option and add the remote servers in I(syslog_servers)
      - if C(absent), will disable the remote syslog option
    choices: ['present', 'absent']
    default: 'absent'

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
'''

EXAMPLES = '''
---
- name: Configure Remote Syslog
    dellemc_idrac_syslog:
       idrac_ip:       "192.168.1.1"
       idrac_user:     "root"
       idrac_pwd:      "calvin"
       share_name:     "\\\\192.168.10.10\\share"
       share_user:     "user1"
       share_pwd:      "password"
       share_mnt:      "/mnt/share"
       syslog_servers: ["192.168.20.1", ""192.168.20.2", ""192.168.20.3"]
       syslog_port:    514
       state:          "present"

- name: Disable Remote Syslog
    dellemc_idrac_syslog:
      idrac_ip:       "192.168.1.1"
      idrac_user:     "root"
      idrac_pwd:      "calvin"
      share_name:     "\\\\192.168.10.10\\share"
      share_user:     "user1"
      share_pwd:      "password"
      share_mnt:      "/mnt/share"
      state:          "absent"

'''

RETURN = '''
---
'''

from ansible.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
try:
    from omsdk.sdkcenum import TypeHelper
    from omdrivers.enums.iDRAC.iDRAC import SysLogEnable_SysLogTypes
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False

def setup_idrac_syslog(idrac, module):
    """
    Setup iDRAC remote syslog settings

    idrac  -- iDRAC handle
    module -- Ansible module
    """

    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    err = False

    try:
        if module.params["state"] == "present":
            idrac.config_mgr._sysconfig.iDRAC.SysLog.SysLogEnable_SysLog = \
                TypeHelper.convert_to_enum('Enabled', SysLogEnable_SysLogTypes)
            idrac.config_mgr._sysconfig.iDRAC.SysLog.Port_SysLog = \
                module.params['syslog_port']

            if module.params['syslog_servers']:
                servers = [server for server in module.params['syslog_servers'] if server.strip()]
                if servers:
                    servers.extend(["", "", ""])
                    idrac.config_mgr._sysconfig.iDRAC.SysLog.Server1_SysLog = servers[0]
                    idrac.config_mgr._sysconfig.iDRAC.SysLog.Server2_SysLog = servers[1]
                    idrac.config_mgr._sysconfig.iDRAC.SysLog.Server3_SysLog = servers[2]
        else:
            idrac.config_mgr._sysconfig.iDRAC.SysLog.SysLogEnable_SysLog = \
                TypeHelper.convert_to_enum('Disabled', SysLogEnable_SysLogTypes)

        msg['changed'] = idrac.config_mgr._sysconfig.is_changed()

        if module.check_mode:
            # since it is running in check mode, reject the changes
            idrac.config_mgr._sysconfig.reject()
        else:
            msg['msg'] = idrac.config_mgr.apply_changes()

            if "Status" in msg['msg'] and msg['msg']["Status"] != "Success":
                msg['failed'] = True
                msg['changed'] = False

    except Exception as e:
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True

    return msg, err

# Main
def main():

    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC handle
            idrac=dict(required=False, type='dict'),

            # iDRAC Credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_pwd=dict(required=True, type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Network File Share
            share_name=dict(required=True, type='str'),
            share_user=dict(required=True, type='str'),
            share_pwd=dict(required=True, type='str', no_log=True),
            share_mnt=dict(required=True, type='path'),

            # Remote Syslog parameters
            syslog_servers=dict(required=False, default=None, type='list'),
            syslog_port=dict(required=False, default=514, type='int'),
            state=dict(required=False, choices=['present', 'absent'],
                       default='absent')
            ),
        supports_check_mode=True)

    if not HAS_OMSDK:
        module.fail_json(msg="Dell EMC OpenManage Python SDK required for this module")

    # Connect to iDRAC
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    # Setup network share as local mount
    if not idrac_conn.setup_nw_share_mount():
        module.fail_json(msg="Failed to setup network share local mount point")

    # Setup Syslog
    (msg, err) = setup_idrac_syslog(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
