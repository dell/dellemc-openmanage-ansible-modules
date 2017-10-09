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
module: dellemc_idrac_export_scp
short_description: Export Server Configuration Profile (SCP) to network share
version_added: "2.3"
description:
    - Export Server Configuration Profile to a given network share (CIFS, NFS)
options:
  idrac_ip:
    required: True
    description:
      - iDRAC IP Address
  idrac_user:
    required: True
    description:
      - iDRAC user name
  idrac_pwd:
    required: True
    description:
      - iDRAC user password
  idrac_port:
    required: True
    description:
      - iDRAC port
  share_name:
    required: True
    description:
      - CIFS or NFS Network share
  share_user:
    required: True
    description:
      - Network share user in the format user@domain
  share_pwd:
    required: True
    description:
      - Network share user password
  scp_components:
    required: False
    description:
      - if C(ALL), will export all components configurations in SCP file
      - if C(IDRAC), will export iDRAC configuration in SCP file
      - if C(BIOS), will export BIOS configuration in SCP file
      - if C(NIC), will export NIC configuration in SCP file
      - if C(RAID), will export RAID configuration in SCP file
    choices: ['ALL', 'IDRAC', 'BIOS', 'NIC', 'RAID']
    default: 'ALL'
  job_wait:
    required: False
    description:
      - if C(True), will wait for the SCP export job to finish and return the job completion status
      - if C(False), will return immediately with a JOB ID after queueing the SCP export jon in LC job queue
    type: 'bool'
    default: True

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
'''

EXAMPLES = '''
# Export SCP to a CIFS network share
- name: Export Server Configuration Profile (SCP)
    dellemc_idrac_export_scp:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_pwd:  "password"
      share_user: "user1"

# Export SCP to a NFS network shre
- name: Export Server Configuration Profile (SCP)
    dellemc_idrac_export_scp:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "10.20.30.40:/share"
      share_pwd:  "password"
      share_user: "user1"

'''

RETURN = '''
---
'''

from ansible.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
try:
    from omsdk.sdkcreds import UserCredentials
    from omsdk.sdkfile import FileOnShare
    from omsdk.sdkcenum import TypeHelper
    from omdrivers.enums.iDRAC.iDRACEnums import (
        ExportFormatEnum, ExportMethodEnum, SCPTargetEnum
    )
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False

def export_server_config_profile(idrac, module):
    """
    Export Server Configuration Profile to a network share

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    err = False

    try:
        scp_file_name_format = "%ip_%Y%m%d_%H%M%S_" + \
            module.params['scp_components'] + "_SCP.xml"

        myshare = FileOnShare(remote=module.params['share_name'],
                              isFolder=True)
        myshare.addcreds(UserCredentials(module.params['share_user'],
                                         module.params['share_pwd']))
        scp_file_name = myshare.new_file(scp_file_name_format)

        scp_components = TypeHelper.convert_to_enum(module.params['scp_components'],
                                                    SCPTargetEnum)

        msg['msg'] = idrac.config_mgr.scp_export(scp_share_path=scp_file_name,
                                                 components=scp_components,
                                                 format_file=ExportFormatEnum.XML,
                                                 method=ExportMethodEnum.Default,
                                                 job_wait=module.params['job_wait'])

        if 'Status' in msg['msg'] and msg['msg']['Status'] != "Success":
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

            # iDRAC Handle
            idrac=dict(required=False, type='dict'),

            # iDRAC credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_pwd=dict(required=True, type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Network File Share
            share_name=dict(required=True, type='str'),
            share_pwd=dict(required=True, type='str', no_log=True),
            share_user=dict(required=True, type='str'),

            scp_components=dict(required=False,
                                choices=['ALL', 'IDRAC', 'BIOS', 'NIC', 'RAID'],
                                default='ALL', type='str'),
            job_wait=dict(required=False, default=True, type='bool')
        ),

        supports_check_mode=True)

    if not HAS_OMSDK:
        module.fail_json(msg="Dell EMC OpenManage Python SDK required for this module")

    # Connect to iDRAC
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    # Export Server Configuration Profile
    msg, err = export_server_config_profile(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
