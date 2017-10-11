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
module: dellemc_idrac_snmp
short_description: Configure SNMP settings on iDRAC
version_added: "2.3"
description:
    - Configures SNMP settings on iDRAC
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
  share_name:
    required: True
    description:
      - CIFS or NFS Network share
    type: 'str'
  share_user:
    required: True
    description:
      - Network share user in the format 'user@domain' if user is part of a domain else 'user'
    type: 'str'
  share_pwd:
    required: True
    description:
      - Network share user password
    type: 'str'
  share_mnt:
    required: True
    description:
      - Local mount path of the network file share with read-write permission for ansible user
    type: 'str'
  snmp_enable:
    required: False
    description: SNMP Agent status
      - if C(enabled), will enable the SNMP Agent
      - if C(disabled), will disable the SNMP Agent
    choices: ['Enabled', 'Disabled']
    default: 'Enabled'
  snmp_protocol:
    required: False
    description: SNMP protocol supported
      - if C(All), will enable support for SNMPv1, v2 and v3 protocols
      - if C(SNMPv3), will enable support for only SNMPv3 protocol
    choices: ['All', 'SNMPv3']
    default: 'All'
  snmp_community:
    required: False
    description:
      - SNMP Agent community string
    default: 'public'
    type: 'str'
  snmp_discover_port:
    required: False
    description:
      - SNMP discovery port
    default: '161'
    type: 'str'
  snmp_trap_port:
    required: False
    description:
      - SNMP trap port
    default: '162'
    type: 'str'
  snmp_trap_format:
    required: False
    description: SNMP trap format
      - if C(SNMPv1), will configure iDRAC to use SNMPv1 for sending traps
      - if C(SNMPv2), will configure iDRAC to use SNMPv2 for sending traps
      - if C(SNMPv3), will configure iDRAC to use SNMPv3 for sending traps
    choices: ['SNMPv1', 'SNMPv2', 'SNMPv3']
    default: 'SNMPv1'
  state:
    required: False
    description:
      - if C(present), will perform create/add/enable operations
      - if C(absent), will perform delete/remove/disable operations
    choices: ['present', 'absent']
    default: 'present'

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
'''

EXAMPLES = '''
- name: Configure SNMP
    dellemc_idrac_snmp:
      idrac_ip:             "192.168.1.1"
      idrac_user:           "root"
      idrac_pwd:            "calvin"
      share_name:           "\\\\192.168.10.10\\share"
      share_user:           "user1"
      share_pwd:            "password"
      share_mnt:            "/mnt/share"
      snmp_agent_enable:    "enabled"
      snmp_protocol:        "all"
      snmp_community:       "public"
      snmp_port:            "161"
      snmp_trap_port:       "162"
      state:                "present"
'''

RETURN = '''
---
'''

from ansible.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule

try:
    from omsdk.sdkcenum import TypeHelper
    from omdrivers.enums.iDRAC.iDRAC import (
        AgentEnable_SNMPTypes, SNMPProtocol_SNMPTypes, TrapFormat_SNMPTypes
    )
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False


def setup_idrac_snmp(idrac, module):
    """
    Setup iDRAC SNMP Configuration parameters

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
        if module.params["state"] == "present":
            idrac.config_mgr.SNMPConfiguration.AgentEnable_SNMP = \
                    AgentEnable_SNMPTypes.Enabled
            idrac.config_mgr.SNMPConfiguration.AgentCommunity_SNMP = \
                    module.params['snmp_community'].lower()
            idrac.config_mgr.SNMPConfiguration.AlertPort_SNMP = \
                    module.params['snmp_trap_port']
            idrac.config_mgr.SNMPConfiguration.DiscoveryPort_SNMP = \
                    module.params['snmp_port']
            idrac.config_mgr.SNMPConfiguration.SNMPProtocol_SNMP = \
                    TypeHelper.convert_to_enum(module.params['snmp_protocol'],
                                               SNMPProtocol_SNMPTypes)
            idrac.config_mgr.SNMPConfiguration.TrapFormat_SNMP = \
                    TypeHelper.convert_to_enum(module.params['snmp_trap_format'],
                                               TrapFormat_SNMPTypes)

        else:
            idrac.config_mgr.SNMPConfiguration.AgentEnable_SNMP = \
                    AgentEnable_SNMPTypes.Disabled

        msg['changed'] = idrac.config_mgr._sysconfig.is_changed()

        if module.check_mode:
            # since it is running in check mode, reject the changes
            idrac.config_mgr._sysconfig.reject()
        else:
            msg['msg'] = idrac.config_mgr.apply_changes()

            if "Status" in msg['msg'] and msg['msg']['Status'] != "Success":
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

            # iDRAC Handle
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

            # SNMP Configuration
            snmp_enable=dict(required=False, choice=['Enabled', 'Disabled'],
                             default='Enabled', type='str'),
            snmp_protocol=dict(required=False, choice=['All', 'SNMPv3'],
                               default='All', type='str'),
            snmp_community=dict(required=False, default='public', type='str'),
            snmp_port=dict(required=False, default=161, type='int'),
            snmp_trap_port=dict(required=False, default=162, type='int'),
            snmp_trap_format=dict(required=False,
                                  choice=['SNMPv1', 'SNMPv2', 'SNMPv3'],
                                  default='SNMPv1', type='str'),

            state=dict(required=False, choice=['present', 'absent'],
                       default='present')
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

    # Configure SNMP
    (msg, err) = setup_idrac_snmp(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()
