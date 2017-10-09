#! /usr/bin/python
# _*_ coding: utf-8 _*_

#
# Copyright (c) 2017 Dell Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: dellemc_idrac_import_scp
short_description: Import SCP from a network share
version_added: "2.3"
description:
    - Import a given Server Configuration Profile (SCP) file from a network share
options:
  idrac_ip:
    required: False
    description: iDRAC IP Address
    default: None
  idrac_user:
    required: False
    description: iDRAC user name
    default: None
  idrac_pwd:
    required: False
    description: iDRAC user password
    default: None
  idrac_port:
    required: False
    description: iDRAC port
    default: None
  share_name:
    required: True
    description: Network file share
  share_user:
    required: True
    description: Network share user in the format user@domain
  share_pwd:
    required: True
    description: Network share user password
  share_mnt:
    required: True
    description: Local mount path of the network file share specified in I(share_name) with read-write permission for ansible user
  scp_file:
    required: True
    description: Server Configuration Profile file name 
    default: None
  scp_components:
    required: False
    description:
      - if C(ALL), will import all components configurations from SCP file
      - if C(IDRAC), will import iDRAC comfiguration from SCP file
      - if C(BIOS), will import BIOS configuration from SCP file
      - if C(NIC), will import NIC configuration from SCP file
      - if C(RAID), will import RAID configuration from SCP file
    choices: ['ALL', 'IDRAC', 'BIOS', 'NIC', 'RAID']
    default: 'ALL'
  reboot:
    required: False
    description: Reboot after importing the SCP
    type: 'bool'
    default: False 

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
'''

EXAMPLES = '''
# Import Server Configuration Profile from a CIFS Network Share
- name: Import Server Configuration Profile
    dellemc_idrac_import_scp:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      scp_file:   "scp_file.xml"
      scp_components: "ALL"
      reboot:      False

# Import Server Configuration Profile from a NFS Network Share
- name: Import Server Configuration Profile
    dellemc_idrac_import_scp:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "192.168.10.10:/share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      scp_file:   "scp_file.xml"
      scp_components: "ALL"
      reboot:      False
'''

RETURN = '''
---
'''

from ansible.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
try:
    from omsdk.sdkcreds import UserCredentials
    from omsdk.sdkfile import FileOnShare
    from omdrivers.enums.iDRAC.iDRACEnums import ExportFormatEnum, SCPTargetEnum
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False


def import_server_config_profile(idrac, module):
    """
    Import Server Configuration Profile from a network share

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
        if module.check_mode:
            msg['changed'] = True
        else:
            myshare = FileOnShare(remote=module.params['share_name'],
                                  mount_point=module.params['share_mnt'],
                                  isFolder=True)
            myshare.addcreds(UserCredentials(module.params['share_user'],
                                             module.params['share_pwd']))
            scp_file_path = myshare.new_file(module.params['scp_file'])

            scp_components = SCPTargetEnum.ALL

            if module.params['scp_components'] == 'IDRAC':
                scp_components = SCPTargetEnum.iDRAC
            elif module.params['scp_components'] == 'BIOS':
                scp_components = SCPTargetEnum.BIOS
            elif module.params['scp_components'] == 'NIC':
                scp_components = SCPTargetEnum.NIC
            elif module.params['scp_components'] == 'RAID':
                scp_components = SCPTargetEnum.RAID

            msg['msg'] = idrac.config_mgr.scp_import(scp_share_path=scp_file_path,
                                                     components=scp_components,
                                                     format_file=ExportFormatEnum.XML,
                                                     reboot=module.params['reboot'],
                                                     job_wait=module.params['job_wait'])

            if "Status" in msg['msg']:
                if msg['msg']['Status'] == "Success":
                    msg['changed'] = True
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

            scp_file=dict(required=True, type='str'),
            scp_components=dict(required=False,
                                choices=['ALL', 'IDRAC', 'BIOS', 'NIC', 'RAID'],
                                default='ALL'),
            reboot=dict(required=False, default=False, type='bool'),
            job_wait=dict(required=False, default=True, type='bool')
        ),

        supports_check_mode=True)

    if not HAS_OMSDK:
        module.fail_json(msg="Dell EMC OpenManage Python SDK required for this module")

    # Connect to iDRAC
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    msg, err = import_server_config_profile(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()
